
# fatigue_detector.py

from collections import deque



def label_true_fatigue(
    plays: list[dict],
    window: int = 5,
    true_threshold: int = 3,
) -> list[bool]:
   
    n = len(plays)
    labels = [False] * n

    for i in range(n):
       
        start = max(0, i - window + 1)
        window_artists = [plays[j]["artist"] for j in range(start, i + 1)]

        
        from collections import Counter
        counts = Counter(window_artists)
        max_repeats = max(counts.values())

        if max_repeats >= true_threshold:
            labels[i] = True

    return labels



def detect_fatigue(
    plays: list[dict],
    window: int = 5,
    threshold: int = 2,
) -> list[bool]:
    
    n = len(plays)
    predictions = [False] * n
    
    recent = deque(maxlen=window)

    for i, play in enumerate(plays):
        recent.append(play["artist"])

        from collections import Counter
        counts = Counter(recent)
        max_repeats = max(counts.values())

        if max_repeats >= threshold:
            predictions[i] = True

    return predictions


def precision_recall(
    true_labels: list[bool],
    pred_labels: list[bool],
) -> dict:
    
    TP = sum(1 for t, p in zip(true_labels, pred_labels) if t and p)
    FP = sum(1 for t, p in zip(true_labels, pred_labels) if not t and p)
    FN = sum(1 for t, p in zip(true_labels, pred_labels) if t and not p)
    TN = sum(1 for t, p in zip(true_labels, pred_labels) if not t and not p)

    precision = TP / (TP + FP) if (TP + FP) > 0 else 0.0
    recall    = TP / (TP + FN) if (TP + FN) > 0 else 0.0
    f1 = (2 * precision * recall / (precision + recall)
          if (precision + recall) > 0 else 0.0)

    return {
        "TP": TP, "FP": FP, "FN": FN, "TN": TN,
        "precision": round(precision, 4),
        "recall":    round(recall,    4),
        "f1":        round(f1,        4),
    }




def sweep_thresholds(
    plays: list[dict],
    window: int = 5,
    true_threshold: int = 3,
    thresholds_to_try: list[int] = None,
) -> list[dict]:
    
    if thresholds_to_try is None:
        thresholds_to_try = [1, 2, 3, 4, 5]

    true_labels = label_true_fatigue(plays, window, true_threshold)
    results = []

    for T in thresholds_to_try:
        preds = detect_fatigue(plays, window, T)
        metrics = precision_recall(true_labels, preds)
        metrics["threshold"] = T
        results.append(metrics)

    return results


if __name__ == "__main__":
    import json

    with open("data/playlist.json") as f:
        plays = json.load(f)

    print("── Threshold Sweep (window=5, true_threshold=3) ──\n")
    print(f"{'T':>4}  {'Precision':>10}  {'Recall':>8}  {'F1':>8}  {'TP':>5}  {'FP':>5}  {'FN':>5}")
    print("─" * 60)

    results = sweep_thresholds(plays)
    for r in results:
        print(
            f"  {r['threshold']:>2}  "
            f"{r['precision']:>10.4f}  "
            f"{r['recall']:>8.4f}  "
            f"{r['f1']:>8.4f}  "
            f"{r['TP']:>5}  "
            f"{r['FP']:>5}  "
            f"{r['FN']:>5}"
        )
