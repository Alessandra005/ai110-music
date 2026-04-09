from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class ScoringStrategy:
    """Base scoring strategy. Different modes use different weight settings."""
    def __init__(
        self,
        genre_weight: float = 2.0,
        mood_weight: float = 1.5,
        energy_weight: float = 1.0,
        valence_weight: float = 1.0,
        danceability_weight: float = 0.5,
        acousticness_weight: float = 0.5,
    ):
        self.genre_weight = genre_weight
        self.mood_weight = mood_weight
        self.energy_weight = energy_weight
        self.valence_weight = valence_weight
        self.danceability_weight = danceability_weight
        self.acousticness_weight = acousticness_weight

    def score_song(self, user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
        return score_song(user_prefs, song, strategy=self)


class GenreFirstStrategy(ScoringStrategy):
    def __init__(self):
        super().__init__(
            genre_weight=2.5,
            mood_weight=1.0,
            energy_weight=1.0,
            valence_weight=0.75,
            danceability_weight=0.5,
            acousticness_weight=0.5,
        )


class MoodFirstStrategy(ScoringStrategy):
    def __init__(self):
        super().__init__(
            genre_weight=1.0,
            mood_weight=2.5,
            energy_weight=1.0,
            valence_weight=1.0,
            danceability_weight=0.5,
            acousticness_weight=0.5,
        )


class EnergyFocusedStrategy(ScoringStrategy):
    def __init__(self):
        super().__init__(
            genre_weight=1.0,
            mood_weight=1.0,
            energy_weight=2.0,
            valence_weight=1.0,
            danceability_weight=0.25,
            acousticness_weight=0.25,
        )


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song], strategy: Optional[ScoringStrategy] = None):
        self.songs = songs
        self.strategy = strategy or ScoringStrategy()

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        user_prefs = asdict(user)
        scored_songs = [
            (song, self.strategy.score_song(user_prefs, song.__dict__)[0])
            for song in self.songs
        ]
        scored_songs.sort(key=lambda item: item[1], reverse=True)
        return [song for song, _score in scored_songs][:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        _, reasons = self.strategy.score_song(asdict(user), song.__dict__)
        return "; ".join(reasons) if reasons else "No matching reasons"


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    
    Converts numeric fields:
    - energy, valence, danceability, acousticness → float
    - tempo_bpm → int
    
    Returns: List of dictionaries with parsed values
    """
    print(f"Loading songs from {csv_path}...")
    songs = []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert numeric fields to appropriate types
            row['id'] = int(row['id'])
            row['energy'] = float(row['energy'])
            row['valence'] = float(row['valence'])
            row['danceability'] = float(row['danceability'])
            row['acousticness'] = float(row['acousticness'])
            row['tempo_bpm'] = int(row['tempo_bpm'])
            
            songs.append(row)
    
    return songs

def score_song(
    user_prefs: Dict,
    song: Dict,
    strategy: Optional[ScoringStrategy] = None,
) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences using the provided strategy.
    
    The default strategy uses the same weights as the original starter logic,
    but alternate modes can adjust genre, mood, and energy importance.

    Returns: Tuple of (total_score, list_of_reason_strings)
    """
    strategy = strategy or ScoringStrategy()
    total_score = 0.0
    reasons = []

    # Genre match
    if user_prefs.get('favorite_genre', '').lower() == song.get('genre', '').lower():
        total_score += strategy.genre_weight
        reasons.append(f'genre match (+{strategy.genre_weight:.2f})')

    # Mood match
    if user_prefs.get('favorite_mood', '').lower() == song.get('mood', '').lower():
        total_score += strategy.mood_weight
        reasons.append(f'mood match (+{strategy.mood_weight:.2f})')

    # Energy closeness
    if 'target_energy' in user_prefs and 'energy' in song:
        energy_diff = abs(user_prefs['target_energy'] - song['energy'])
        energy_score = strategy.energy_weight * (1.0 - energy_diff)
        total_score += energy_score
        reasons.append(f'energy closeness (+{energy_score:.2f})')

    # Valence closeness
    if 'target_valence' in user_prefs and 'valence' in song:
        valence_diff = abs(user_prefs['target_valence'] - song['valence'])
        valence_score = strategy.valence_weight * (1.0 - valence_diff)
        total_score += valence_score
        reasons.append(f'valence closeness (+{valence_score:.2f})')

    # Danceability closeness
    if 'target_danceability' in user_prefs and 'danceability' in song:
        danceability_diff = abs(user_prefs['target_danceability'] - song['danceability'])
        danceability_score = strategy.danceability_weight * (1.0 - danceability_diff)
        total_score += danceability_score
        reasons.append(f'danceability closeness (+{danceability_score:.2f})')

    # Acousticness closeness
    if 'target_acousticness' in user_prefs and 'acousticness' in song:
        acousticness_diff = abs(user_prefs['target_acousticness'] - song['acousticness'])
        acousticness_score = strategy.acousticness_weight * (1.0 - acousticness_diff)
        total_score += acousticness_score
        reasons.append(f'acousticness closeness (+{acousticness_score:.2f})')

    return (total_score, reasons)

def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    strategy: Optional[ScoringStrategy] = None,
) -> List[Tuple[Dict, float, List[str]]]:
    """
    Functional implementation of the recommendation logic.
    Scores all songs using score_song and returns the top k recommendations.
    
    Returns: List of tuples (song_dict, score, reasons_list)
    """
    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, strategy=strategy)
        scored_songs.append((song, score, reasons))

    sorted_songs = sorted(scored_songs, key=lambda x: x[1], reverse=True)
    return sorted_songs[:k]
