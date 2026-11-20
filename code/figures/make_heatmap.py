# Redraws Figure 1 at column width. Values are the whole-number labels printed on the
# zero-shot heatmap in the notebook (section 10.1, cell 56; means of 3 seeds).
# Run from code/: python figures/make_heatmap.py
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

plt.rcParams.update({"pdf.fonttype": 42, "font.family": "serif",
                     "font.serif": ["Times New Roman", "DejaVu Serif"], "font.size": 7.5})

TESTS = [("nchlt", "zul"), ("nchlt", "xho"), ("nchlt", "ssw"), ("nchlt", "nso"), ("nchlt", "sot"),
         ("nchlt", "tsn"), ("news", "zul"), ("news", "xho"), ("news", "tsn")]
# source: F1 on the tests above
F1 = {
    ("nchlt", "zul"): [74, 46, 52, 51, 43, 40, 50, 53, 49],
    ("nchlt", "xho"): [52, 83, 64, 54, 39, 58, 57, 70, 57],
    ("nchlt", "ssw"): [57, 74, 78, 63, 49, 50, 58, 65, 63],
    ("nchlt", "nso"): [48, 53, 53, 84, 49, 50, 55, 55, 66],
    ("nchlt", "sot"): [27, 17, 34, 61, 59, 58, 39, 17, 61],
    ("nchlt", "tsn"): [20, 19, 31, 54, 44, 79, 42, 19, 71],
    ("news", "zul"): [44, 62, 58, 51, 37, 47, 88, 83, 63],
    ("news", "xho"): [43, 67, 58, 51, 38, 56, 82, 88, 66],
    ("news", "tsn"): [20, 19, 29, 54, 41, 63, 51, 28, 89],
    ("news", "swa"): [21, 15, 27, 55, 43, 63, 41, 20, 80],
    ("news", "nya"): [20, 19, 29, 58, 40, 52, 42, 21, 76],
}
sources = list(F1)
M = np.array([F1[s] for s in sources], dtype=float)

fig, ax = plt.subplots(figsize=(3.33, 2.65))
im = ax.imshow(M, cmap="Blues", vmin=0, vmax=100, aspect="auto")
for r in range(M.shape[0]):
    for c in range(M.shape[1]):
        ax.text(c, r, f"{int(M[r, c])}", ha="center", va="center", fontsize=7,
                color="white" if M[r, c] >= 55 else "#17212B")
        if sources[r] == TESTS[c]:  # in-language cell
            ax.add_patch(Rectangle((c - .5, r - .5), 1, 1, fill=False, ec="#17212B", lw=1.3))

ax.set_xticks(range(len(TESTS)), [t[1] for t in TESTS])
ax.set_yticks(range(len(sources)), [s[1] for s in sources])
ax.xaxis.tick_top()
ax.tick_params(length=0, pad=1.5)
for sp in ax.spines.values():
    sp.set_visible(False)
ax.axvline(5.5, color="white", lw=2.5)   # corpus boundary, test sets
ax.axhline(5.5, color="white", lw=2.5)   # corpus boundary, sources
ax.text(2.5, -1.35, "NCHLT test", ha="center", fontweight="bold")
ax.text(7, -1.35, "News test", ha="center", fontweight="bold")
ax.text(-1.55, 2.5, "NCHLT source", rotation=90, va="center", ha="center", fontweight="bold")
ax.text(-1.55, 8, "News source", rotation=90, va="center", ha="center", fontweight="bold")
fig.subplots_adjust(left=.125, right=.995, top=.885, bottom=.01)
fig.savefig("figures/zero_shot_heatmap.pdf")
fig.savefig("figures/zero_shot_heatmap.png", dpi=200)
print("saved", M.shape)
