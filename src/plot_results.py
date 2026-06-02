import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ============================================================
# DỮ LIỆU — từ hap.py PASS rows
# Đơn vị recall / precision / f1: %
# ============================================================

SNP = {
    "Hard Filter": {
        "recall": 99.2957,
        "precision": 99.2897,
        "f1": 99.2957,
        "fp": 1116,
        "fn": 1102,
        "tp": 156349
    },
    "VQSR": {
        "recall": 98.2679,
        "precision": 99.6702,
        "f1": 98.9697,
        "fp": 511,
        "fn": 2711,
        "tp": 154740
    },
    "VEF": {
        "recall": 99.2798,
        "precision": 99.7110,
        "f1": 99.4949,
        "fp": 453,
        "fn": 1134,
        "tp": 156317
    },
    "TabPFN": {
        "recall": 99.3223,
        "precision": 99.7232,
        "f1": 99.5224,
        "fp": 434,
        "fn": 1067,
        "tp": 156384
    },
    "Stack": {
        "recall": 99.3020,
        "precision": 99.7353,
        "f1": 99.5182,
        "fp": 415,
        "fn": 1099,
        "tp": 156352
    },
}

INDEL = {
    "Hard Filter": {
        "recall": 95.8976,
        "precision": 97.4896,
        "f1": 96.6871,
        "fp": 647,
        "fn": 1046,
        "tp": 24427
    },
    "VQSR": {
        "recall": 95.5247,
        "precision": 98.5791,
        "f1": 97.0279,
        "fp": 351,
        "fn": 1140,
        "tp": 24333
    },
    "VEF": {
        "recall": 95.8976,
        "precision": 97.4896,
        "f1": 96.6871,
        "fp": 647,
        "fn": 1045,
        "tp": 24428
    },
    "TabPFN": {
        "recall": 95.6542,
        "precision": 97.7761,
        "f1": 96.7035,
        "fp": 570,
        "fn": 1107,
        "tp": 24366
    },
    "Stack": {
        "recall": 95.7367,
        "precision": 97.6943,
        "f1": 96.7056,
        "fp": 592,
        "fn": 1086,
        "tp": 24387
    },
}

METHODS = ["Hard Filter", "VQSR", "VEF", "TabPFN", "Stack"]
COLORS = {
    "Hard Filter": "#6b7280",
    "VQSR": "#f59e0b",
    "VEF": "#10b981",
    "TabPFN": "#6366f1",
    "Stack": "#ef4444",
}

# ============================================================
# THEME SÁNG
# ============================================================

plt.rcParams.update({
    "figure.facecolor": "#ffffff",
    "axes.facecolor": "#ffffff",
    "axes.edgecolor": "#d1d5db",
    "axes.labelcolor": "#111827",
    "axes.titlecolor": "#111827",
    "xtick.color": "#111827",
    "ytick.color": "#111827",
    "grid.color": "#e5e7eb",
    "grid.linestyle": "--",
    "grid.alpha": 0.8,
    "text.color": "#111827",
    "legend.facecolor": "#ffffff",
    "legend.edgecolor": "#d1d5db",
    "legend.labelcolor": "#111827",
    "font.family": "DejaVu Sans",
})

def save_and_show(fig, filename):
    plt.tight_layout()
    fig.savefig(filename, dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.show()
    plt.close(fig)
    print(f"✅ Saved: {filename}")

# ============================================================
# BẢNG GROUPED BY METRIC
# ============================================================

def print_metric_tables():
    def make_table(data):
        rows = []
        for metric, label, direction in [
            ("recall", "Recall ↑", "max"),
            ("precision", "Precision ↑", "max"),
            ("f1", "F1-score ↑", "max"),
            ("fp", "FP ↓", "min"),
            ("fn", "FN ↓", "min"),
            ("tp", "TP ↑", "max"),
        ]:
            row = {"Metric": label}
            values = {}

            for method in METHODS:
                values[method] = data[method][metric]
                row[method] = data[method][metric]

            if direction == "max":
                best = max(values, key=values.get)
            else:
                best = min(values, key=values.get)

            row["Best"] = best
            rows.append(row)

        return pd.DataFrame(rows)

    snp_table = make_table(SNP)
    indel_table = make_table(INDEL)

    print("SNP — grouped by metric")
    display(snp_table)

    print("INDEL — grouped by metric")
    display(indel_table)

    return snp_table, indel_table

# ============================================================
# BIỂU ĐỒ SCORE: F1 / RECALL / PRECISION
# Chỉ để dấu sao ★, không ghi BEST
# ============================================================

def plot_score_metric(metric, title, ylabel, snp_ylim, indel_ylim, filename):
    fig, axes = plt.subplots(1, 2, figsize=(16, 5))
    fig.suptitle(title, fontsize=15, fontweight="bold", y=1.03)

    configs = [
        ("SNP", SNP, snp_ylim),
        ("INDEL", INDEL, indel_ylim),
    ]

    for ax, (variant, data, ylim) in zip(axes, configs):
        values = [data[m][metric] for m in METHODS]
        x = np.arange(len(METHODS))

        bars = ax.bar(
            x,
            values,
            color=[COLORS[m] for m in METHODS],
            width=0.62,
            alpha=0.9,
            zorder=3
        )

        best_idx = int(np.argmax(values))
        bars[best_idx].set_edgecolor("black")
        bars[best_idx].set_linewidth(2)

        # Gắn số trên cột
        for i, (bar, value) in enumerate(zip(bars, values)):
            label_y = value + (ylim[1] - ylim[0]) * 0.010
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                label_y,
                f"{value:.3f}%",
                ha="center",
                va="bottom",
                fontsize=9,
                color=COLORS[METHODS[i]],
                fontweight="bold",
                rotation=20
            )

        # Chỉ để dấu sao, đẩy cao hơn số để không chồng
        star_y = values[best_idx] + (ylim[1] - ylim[0]) * 0.070
        ax.text(
            best_idx,
            star_y,
            "★",
            ha="center",
            va="bottom",
            fontsize=16,
            color="#eab308",
            fontweight="bold"
        )

        ax.set_title(f"{variant}", fontsize=13, fontweight="bold")
        ax.set_ylabel(ylabel)
        ax.set_xticks(x)
        ax.set_xticklabels(METHODS, rotation=20, ha="right")
        ax.set_ylim(*ylim)
        ax.grid(axis="y", zorder=0)
        ax.spines[["top", "right"]].set_visible(False)

    save_and_show(fig, filename)

# ============================================================
# BIỂU ĐỒ COUNT: FP / FN
# Chỉ để dấu sao ★
# ============================================================

def plot_count_metric(metric, title, xlabel, filename):
    fig, axes = plt.subplots(1, 2, figsize=(16, 5))
    fig.suptitle(title, fontsize=15, fontweight="bold", y=1.03)

    configs = [
        ("SNP", SNP),
        ("INDEL", INDEL),
    ]

    for ax, (variant, data) in zip(axes, configs):
        sorted_items = sorted(
            [(m, data[m][metric]) for m in METHODS],
            key=lambda x: x[1]
        )

        methods_sorted = [x[0] for x in sorted_items]
        values = [x[1] for x in sorted_items]
        colors = [COLORS[m] for m in methods_sorted]

        bars = ax.barh(
            methods_sorted,
            values,
            color=colors,
            alpha=0.9,
            zorder=3
        )

        bars[0].set_edgecolor("black")
        bars[0].set_linewidth(2)

        max_value = max(values)

        for bar, value, method in zip(bars, values, methods_sorted):
            ax.text(
                value + max_value * 0.015,
                bar.get_y() + bar.get_height() / 2,
                f"{value:,}",
                ha="left",
                va="center",
                fontsize=10,
                color=COLORS[method],
                fontweight="bold"
            )

        # chỉ dấu sao
        ax.text(
            values[0] + max_value * 0.18,
            0,
            "★",
            color="#eab308",
            fontsize=16,
            fontweight="bold",
            va="center"
        )

        ax.set_title(f"{variant}", fontsize=13, fontweight="bold")
        ax.set_xlabel(xlabel)
        ax.grid(axis="x", zorder=0)
        ax.spines[["top", "right"]].set_visible(False)
        ax.invert_yaxis()

    save_and_show(fig, filename)

# ============================================================
# CHẠY
# ============================================================

snp_table, indel_table = print_metric_tables()
COMMON_PERFORMANCE_YLIM = (96, 100)
plot_score_metric(
    metric="f1",
    title="F1-score comparison by method",
    ylabel="F1-score (%)",
    snp_ylim=COMMON_PERFORMANCE_YLIM,
    indel_ylim=COMMON_PERFORMANCE_YLIM,
    filename="plot_f1_score.png"
)

plot_score_metric(
    metric="recall",
    title="Recall comparison by method",
    ylabel="Recall (%)",
    snp_ylim=COMMON_PERFORMANCE_YLIM,
    indel_ylim=(94.5,100.0),
    filename="plot_recall.png"
)

plot_score_metric(
    metric="precision",
    title="Precision comparison by method",
    ylabel="Precision (%)",
    snp_ylim=COMMON_PERFORMANCE_YLIM,
    indel_ylim=COMMON_PERFORMANCE_YLIM,
    filename="plot_precision.png"
)

plot_count_metric(
    metric="fp",
    title="False Positive comparison by method",
    xlabel="False Positive count, lower is better",
    filename="plot_false_positive.png"
)

plot_count_metric(
    metric="fn",
    title="False Negative comparison by method",
    xlabel="False Negative count, lower is better",
    filename="plot_false_negative.png"
)

print("✅ Done.")
print("Các biểu đồ đã giữ lại:")
print("- plot_f1_score.png")
print("- plot_recall.png")
print("- plot_precision.png")
print("- plot_false_positive.png")
print("- plot_false_negative.png")