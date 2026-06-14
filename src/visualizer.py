
# visualizer.py

import json
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


def load_results(path: str = "outputs/results.json") -> dict:
    with open(path) as f:
        return json.load(f)


def plot(data: dict, save_path: str = "outputs/pr_curve.png"):
    results   = data["results"]
    optimal_T = data["optimal_threshold"]

    thresholds = [r["threshold"]  for r in results]
    precisions = [r["precision"]  for r in results]
    recalls    = [r["recall"]     for r in results]
    f1s        = [r["f1"]         for r in results]

   
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))
    fig.patch.set_facecolor("#0f0f14")
    for ax in (ax1, ax2):
        ax.set_facecolor("#16161e")
        ax.spines["bottom"].set_color("#3a3a4a")
        ax.spines["left"].set_color("#3a3a4a")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.tick_params(colors="#9090a8", labelsize=9)
        ax.xaxis.label.set_color("#c0c0d0")
        ax.yaxis.label.set_color("#c0c0d0")
        ax.title.set_color("#e8e8f0")

    
    ax1.set_title("Precision–Recall Curve", fontsize=13, fontweight="bold", pad=14)
    ax1.set_xlabel("Recall  (coverage — did we catch all fatigue?)", fontsize=10)
    ax1.set_ylabel("Precision  (accuracy — were our flags correct?)", fontsize=10)
    ax1.set_xlim(-0.05, 1.1)
    ax1.set_ylim(-0.05, 1.1)
    ax1.axhline(0.5, color="#2a2a3a", linewidth=0.8, linestyle="--")
    ax1.axvline(0.5, color="#2a2a3a", linewidth=0.8, linestyle="--")

    
    ax1.plot(recalls, precisions, color="#5555cc", linewidth=1.5,
             linestyle="--", alpha=0.5, zorder=1)

    
    cmap = plt.cm.plasma
    colors = cmap(np.linspace(0.2, 0.85, len(thresholds)))

    for i, (r, p, T) in enumerate(zip(recalls, precisions, thresholds)):
        is_opt = (T == optimal_T)
        ax1.scatter(r, p,
                    color=colors[i],
                    s=180 if is_opt else 90,
                    zorder=3,
                    edgecolors="white" if is_opt else "none",
                    linewidths=1.5)
        ax1.annotate(
            f"T={T}",
            xy=(r, p),
            xytext=(8, 6),
            textcoords="offset points",
            color=colors[i],
            fontsize=8.5,
            fontweight="bold" if is_opt else "normal",
        )

   
    opt = next(r for r in results if r["threshold"] == optimal_T)
    ax1.annotate(
        f"★ Optimal (T={optimal_T})\nF1={opt['f1']:.2f}",
        xy=(opt["recall"], opt["precision"]),
        xytext=(-90, -40),
        textcoords="offset points",
        color="#f0e060",
        fontsize=8.5,
        arrowprops=dict(arrowstyle="->", color="#f0e060", lw=1.2),
    )

    ax1.text(0.02, 0.08,
             "← Low precision\n   (too many false alarms)",
             transform=ax1.transAxes, color="#606078", fontsize=7.5)
    ax1.text(0.55, 0.08,
             "Low recall →\n(missing real fatigue)",
             transform=ax1.transAxes, color="#606078", fontsize=7.5)

    
    ax2.set_title("F1 Score by Threshold", fontsize=13, fontweight="bold", pad=14)
    ax2.set_xlabel("Threshold T  (repeats-in-window before flagging)", fontsize=10)
    ax2.set_ylabel("F1 Score  (balance of precision + recall)", fontsize=10)
    ax2.set_ylim(0, 1.15)

    bar_colors = ["#f0e060" if T == optimal_T else "#5555cc" for T in thresholds]
    bars = ax2.bar(thresholds, f1s, color=bar_colors,
                   width=0.55, zorder=2, edgecolor="none")

    for bar, f1, T in zip(bars, f1s, thresholds):
        ax2.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.025,
            f"{f1:.2f}",
            ha="center", va="bottom",
            color="#f0e060" if T == optimal_T else "#9090a8",
            fontsize=9,
            fontweight="bold" if T == optimal_T else "normal",
        )

    ax2.set_xticks(thresholds)
    ax2.set_xticklabels([f"T={T}" for T in thresholds])
    ax2.axhline(1.0, color="#3a3a4a", linewidth=0.8, linestyle="--")

    
    opt_patch = mpatches.Patch(color="#f0e060", label=f"Optimal (T={optimal_T})")
    other_patch = mpatches.Patch(color="#5555cc", label="Other thresholds")
    ax2.legend(handles=[opt_patch, other_patch],
               facecolor="#1e1e2a", edgecolor="#3a3a4a",
               labelcolor="#c0c0d0", fontsize=8.5,
               loc="upper right")

    
    fig.text(0.5, -0.02,
             f"EncoreGuard · window={data['window']} songs · "
             f"ground-truth threshold={data['true_threshold']} · "
             f"n={data['n_plays']} plays",
             ha="center", color="#505060", fontsize=8)

    plt.tight_layout(pad=2.5)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close()
    print(f" Chart saved → {save_path}")


if __name__ == "__main__":
    data = load_results()
    plot(data)
