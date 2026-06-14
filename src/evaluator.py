
# evaluator.py


import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from fatigue_detector import sweep_thresholds


def find_optimal(results: list[dict]) -> dict:
    
    return max(results, key=lambda r: r["f1"])


def print_table(results: list[dict], optimal: dict):
    print("\n╔══════════════════════════════════════════════════════════════╗")
    print("║              EncoreGuard — Threshold Sweep Results           ║")
    print("╚══════════════════════════════════════════════════════════════╝\n")
    print(f"  {'T':>3}  {'Precision':>10}  {'Recall':>8}  {'F1':>8}  {'TP':>5}  {'FP':>5}  {'FN':>5}")
    print("  " + "─" * 58)

    for r in results:
        marker = "   BEST" if r["threshold"] == optimal["threshold"] else ""
        print(
            f"  {r['threshold']:>3}  "
            f"{r['precision']:>10.4f}  "
            f"{r['recall']:>8.4f}  "
            f"{r['f1']:>8.4f}  "
            f"{r['TP']:>5}  "
            f"{r['FP']:>5}  "
            f"{r['FN']:>5}"
            f"{marker}"
        )

    print()
    print(f"   Optimal threshold  : T = {optimal['threshold']}")
    print(f"   Precision          : {optimal['precision']:.4f}  (of all flagged moments, this % were real fatigue)")
    print(f"   Recall             : {optimal['recall']:.4f}  (of all real fatigue moments, we caught this %)")
    print(f"   F1 Score           : {optimal['f1']:.4f}  (harmonic mean — the balance metric)")
    print()


def main():
    with open("data/playlist.json") as f:
        plays = json.load(f)

    results = sweep_thresholds(
        plays,
        window=5,
        true_threshold=3,
        thresholds_to_try=[1, 2, 3, 4, 5, 6],
    )

    optimal = find_optimal(results)
    print_table(results, optimal)

    
    output = {
        "results": results,
        "optimal_threshold": optimal["threshold"],
        "window": 5,
        "true_threshold": 3,
        "n_plays": len(plays),
    }
    os.makedirs("outputs", exist_ok=True)
    with open("outputs/results.json", "w") as f:
        json.dump(output, f, indent=2)
    print("  Saved → outputs/results.json\n")


if __name__ == "__main__":
    main()
