"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import (
    EnergyFocusedStrategy,
    GenreFirstStrategy,
    MoodFirstStrategy,
    load_songs,
    recommend_songs,
)


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Pick one of: 'genre-first', 'mood-first', 'energy-focused'
    strategy_name = "energy-focused"
    strategy_map = {
        "genre-first": GenreFirstStrategy,
        "mood-first": MoodFirstStrategy,
        "energy-focused": EnergyFocusedStrategy,
    }
    strategy = strategy_map[strategy_name]()

    # Starter example profile
    # user_prefs = {
    #     "favorite_genre": "pop",
    #     "favorite_mood": "happy",
    #     "target_energy": 0.8,
    #     "target_valence": 0.75,
    #     "target_danceability": 0.7,
    #     "target_acousticness": 0.2,
    # }

    # Profile 2: Chill Lofi
    # user_prefs = {
    #     "favorite_genre": "lofi",
    #     "favorite_mood": "chill",
    #     "target_energy": 0.35,
    #     "target_valence": 0.55,
    #     "target_danceability": 0.4,
    #     "target_acousticness": 0.7
    # }

    # Profile 3: Deep Intense Rock
    user_prefs = {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.92,
        "target_valence": 0.45,
        "target_danceability": 0.5,
        "target_acousticness": 0.1
    }
    
    print(f"\n=== Mode: {strategy_name} ===\n")
    recommendations = recommend_songs(user_prefs, songs, k=5, strategy=strategy)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {', '.join(explanation)}")
        print()


if __name__ == "__main__":
    main()
