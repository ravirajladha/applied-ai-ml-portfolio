"""Build the ROUGE comparison figure for the paper.

Run from the paper/ directory:
    ../.venv/Scripts/python.exe figures/make_rouge_figure.py

Writes figures/rouge_comparison.pdf as vector output, so it stays sharp at any
zoom and embeds cleanly in LaTeX.

The numbers are hard-coded from EXPERIMENT_FACTS.md section 4 on purpose. That
file is the single source of truth for every number in the paper; if a value
changes there, change it here and rebuild. Do not re-derive it from the
notebook.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# --- data -------------------------------------------------------------
METRICS = ["ROUGE-1", "ROUGE-2", "ROUGE-L"]
SERIES = [
    ("Lead-1 (extractive)",   [0.1255, 0.0341, 0.1145]),
    ("t5-small, not tuned",   [0.1086, 0.0266, 0.0974]),
    ("t5-small, fine-tuned",  [0.1751, 0.0448, 0.1723]),
]

# Categorical hues in fixed order. Validated for colour-vision deficiency:
# worst adjacent pair dE 28.0 protan / 20.4 tritan, all above the dE 8 target.
# Every bar is also directly labelled, which is the secondary encoding that
# keeps the figure readable when the paper is photocopied in greyscale.
COLORS = ["#3b6fd4", "#d97706", "#9333ea"]

# --- figure -----------------------------------------------------------
# Match the paper's body font. This must be set BEFORE the figure is created,
# or matplotlib has already chosen a font and silently ignores it.
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Nimbus Roman", "Times New Roman", "DejaVu Serif"]

# 3.5in is one IEEE column.
fig, ax = plt.subplots(figsize=(3.5, 2.5))

x = np.arange(len(METRICS))
n = len(SERIES)
width = 0.26
gap = 0.015          # a small surface gap so adjacent bars never touch

for i, ((label, values), color) in enumerate(zip(SERIES, COLORS)):
    offset = (i - (n - 1) / 2) * (width + gap)
    bars = ax.bar(x + offset, values, width, label=label,
                  color=color, edgecolor="none")
    # Direct labels: identity and magnitude are never carried by colour alone.
    for bar, v in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 0.004, f"{v:.3f}",
                ha="center", va="bottom", fontsize=5.2, color="#3f3f46")

# Recessive axes: horizontal reference lines only, no box around the plot.
ax.set_axisbelow(True)
ax.yaxis.grid(True, color="#e4e4e7", linewidth=0.6)
ax.xaxis.grid(False)
for side in ("top", "right", "left"):
    ax.spines[side].set_visible(False)
ax.spines["bottom"].set_color("#d4d4d8")

ax.set_xticks(x)
ax.set_xticklabels(METRICS, fontsize=8)
ax.set_ylabel("F-measure", fontsize=8)
ax.tick_params(axis="y", labelsize=7, length=0, colors="#52525b")
ax.tick_params(axis="x", length=0, colors="#3f3f46")
ax.set_ylim(0, 0.21)

ax.legend(fontsize=6.2, frameon=False, loc="upper center",
          bbox_to_anchor=(0.5, 1.18), ncol=3, columnspacing=1.0,
          handlelength=1.1, handletextpad=0.4)

fig.tight_layout()
fig.savefig("figures/rouge_comparison.pdf", bbox_inches="tight",
            transparent=True)
print("wrote figures/rouge_comparison.pdf")

# Set FIG_PNG=<path> to also emit a raster copy for eyeballing the layout.
# Vector output is what LaTeX embeds; this is only for looking at.
import os
if os.environ.get("FIG_PNG"):
    fig.savefig(os.environ["FIG_PNG"], dpi=300, bbox_inches="tight",
                facecolor="white")
    print("wrote", os.environ["FIG_PNG"])
