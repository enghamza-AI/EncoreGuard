# data_generator.py

import random
import json
from datetime import datetime, timedelta

random.seed(42)

ARTISTS = {
    "Radiohead":        0.18,
    "Tame Impala":      0.15,
    "Arctic Monkeys":   0.12,
    "Travis Scott":      0.10,
    "LCD Soundsystem":  0.08,
    "Bon Iver":         0.07,
    "Foals":            0.06,
    "Portishead":       0.05,
    "The National":     0.05,
    "Cigarettes After Sex": 0.04,
    "Warpaint":         0.04,
    "Moderat":          0.03,
    "Four Tet":         0.02,
    "Burial":           0.01,
}

ARTIST_NAMES = list(ARTISTS.keys())
WEIGHTS = list(ARTISTS.values())

def generate_playlist(n_plays: int = 200) -> list[dict]:
    plays = []
    start_time = datetime(2026,1,1,9,0,0)

    for i in range(n_plays):
        artist = random.choices(ARTIST_NAMES, weights=WEIGHTS, k=1)[0]
        timestamp = start_time + timedelta(minutes=3.5 * i)

        plays.append({
            "position": i + 1,
            "artist": artist,
            "timestamp": timestamp.isoformat(),
        })

    return plays

def save_playlist(plays: list[dict], path: str = "data/playlist.json"):
    with open(path, "w") as f:
        json.dump(plays, f, indent=2)
    print(f"SAVED {len(plays)} play events -> {path}")


if __name__ == "__main__":
    playlist = generate_playlist(200)
    save_playlist(playlist, "data/playlist.json")

    print("\n-- first 5 plays --")
    for p in playlist[:5]:
        print(f" #{p['position']:>3} {p['artist']:<30} {p['timestamp']}")


        
