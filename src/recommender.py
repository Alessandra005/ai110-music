from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
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

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

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

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    
    Scoring breakdown:
    - Genre match: +2.0 points
    - Mood match: +1.5 points
    - Energy closeness: +1.0 * (1 - |user_energy - song_energy|)
    - Valence closeness: +1.0 * (1 - |user_valence - song_valence|)
    - Danceability closeness: +0.5 * (1 - |user_danceability - song_danceability|)
    - Acousticness closeness: +0.5 * (1 - |user_acousticness - song_acousticness|)
    
    Returns: Tuple of (total_score, list_of_reason_strings)
    """
    total_score = 0.0
    reasons = []
    
    # Genre match
    if user_prefs.get('favorite_genre', '').lower() == song.get('genre', '').lower():
        total_score += 2.0
        reasons.append('genre match (+2.0)')
    
    # Mood match
    if user_prefs.get('favorite_mood', '').lower() == song.get('mood', '').lower():
        total_score += 1.5
        reasons.append('mood match (+1.5)')
    
    # Energy closeness
    if 'target_energy' in user_prefs and 'energy' in song:
        energy_diff = abs(user_prefs['target_energy'] - song['energy'])
        energy_score = 1.0 * (1.0 - energy_diff)
        total_score += energy_score
        reasons.append(f'energy closeness (+{energy_score:.2f})')
    
    # Valence closeness
    if 'target_valence' in user_prefs and 'valence' in song:
        valence_diff = abs(user_prefs['target_valence'] - song['valence'])
        valence_score = 1.0 * (1.0 - valence_diff)
        total_score += valence_score
        reasons.append(f'valence closeness (+{valence_score:.2f})')
    
    # Danceability closeness
    if 'target_danceability' in user_prefs and 'danceability' in song:
        danceability_diff = abs(user_prefs['target_danceability'] - song['danceability'])
        danceability_score = 0.5 * (1.0 - danceability_diff)
        total_score += danceability_score
        reasons.append(f'danceability closeness (+{danceability_score:.2f})')
    
    # Acousticness closeness
    if 'target_acousticness' in user_prefs and 'acousticness' in song:
        acousticness_diff = abs(user_prefs['target_acousticness'] - song['acousticness'])
        acousticness_score = 0.5 * (1.0 - acousticness_diff)
        total_score += acousticness_score
        reasons.append(f'acousticness closeness (+{acousticness_score:.2f})')
    
    return (total_score, reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Scores all songs using score_song and returns the top k recommendations.
    
    Returns: List of tuples (song_dict, score, reasons_list)
    """
    # Score all songs
    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored_songs.append((song, score, reasons))
    
    # Sort by score (highest first) without modifying the original list
    sorted_songs = sorted(scored_songs, key=lambda x: x[1], reverse=True)
    
    # Return top k results
    return sorted_songs[:k]
