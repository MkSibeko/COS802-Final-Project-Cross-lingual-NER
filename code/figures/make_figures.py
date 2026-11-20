# Draws Figures 2-4 of the report from the verified outputs of COS802_Experiment.ipynb
# (cells 58, 62 and 64; means over seeds 13, 42 and 2026).
# Run from code/: python figures/make_figures.py
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({"pdf.fonttype": 42, "font.family": "serif",
                     "font.serif": ["Times New Roman", "DejaVu Serif"], "font.size": 7.5,
                     "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8C8C8C", "axes.linewidth": 0.6,
                     "xtick.color": "#404040", "ytick.color": "#404040",
                     "xtick.major.width": 0.6, "ytick.major.width": 0.6})

# Same colour code as the presentation: Nguni blue, Sotho-Tswana orange, other Bantu green, comparison grey.
BLUE, ORANGE, GREEN, GREY = "#005BAA", "#D98010", "#3E7526", "#A6A6A6"
INK, MUTED, GRIDC = "#231F20", "#595959", "#E3E3E3"


from decimal import Decimal, ROUND_HALF_UP
def r1(v):
    """Round half up to one decimal, as in the report's tables (57.65 -> 57.7)."""
    return str(Decimal(str(v)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def save(fig, name):
    fig.savefig(f"figures/{name}.pdf")
    fig.savefig(f"figures/{name}.png", dpi=220)
    print("saved", name)


# ---------------------------------------------------------------- Figure 2: RQ1
# Mean transfer ratio by relatedness and corpus match (cell 58; transfer pairs only; n = seed-level rows).
levels = ["Same\nlanguage", "Same\ncluster", "Other\nS. Bantu", "Other\nBantu"]
tr_other = [0.73, 0.68, 0.51, 0.49]      # source from the other corpus
tr_same = [None, 0.76, 0.56, 0.53]       # source from the test set's corpus (same language is always cross-corpus)
fig, ax = plt.subplots(figsize=(3.33, 1.85))
x = np.arange(len(levels))
w = 0.36
ax.yaxis.grid(True, color=GRIDC, lw=0.6)
ax.set_axisbelow(True)
for i, (o, s) in enumerate(zip(tr_other, tr_same)):
    ax.bar(i - w / 2 - 0.01, o, w, color=GREY, edgecolor="white", lw=0.8)
    ax.text(i - w / 2 - 0.01, o + 0.015, f"{o:.2f}", ha="center", va="bottom", fontsize=6.5, color=INK)
    if s is not None:
        ax.bar(i + w / 2 + 0.01, s, w, color=BLUE, edgecolor="white", lw=0.8)
        ax.text(i + w / 2 + 0.01, s + 0.015, f"{s:.2f}", ha="center", va="bottom", fontsize=6.5, color=INK)
ax.set_xticks(x, levels)
ax.tick_params(axis="x", length=0)
ax.set_ylim(0, 0.92)
ax.set_yticks([0, 0.25, 0.5, 0.75])
ax.set_ylabel("Transfer ratio")
ax.set_xlabel("Source relatedness to the target", labelpad=2)
from matplotlib.patches import Patch
ax.legend([Patch(color=GREY), Patch(color=BLUE)], ["Source from the other corpus", "Source from the test's corpus"],
          loc="upper right", frameon=False, fontsize=6.5, handlelength=1, handleheight=0.8, borderaxespad=0)
fig.subplots_adjust(left=0.14, right=0.99, top=0.97, bottom=0.27)
save(fig, "rq1_relatedness_corpus")


# ---------------------------------------------------------------- Figure 3: RQ3
# Few-shot curves (cell 62). Orange: same language from the other corpus; blue: sister language.
panels = [
    ("isiZulu news", 87.63, [("NCHLT zul (same lang., govt)", ORANGE, "s", [50.35, 75.06, 83.50]),
                             ("News xho (sister lang.)", BLUE, "o", [82.39, 83.85, 86.24])]),
    ("isiXhosa news", 88.09, [("NCHLT xho (same lang., govt)", ORANGE, "s", [70.03, 75.77, 83.57]),
                              ("News zul (sister lang.)", BLUE, "o", [82.74, 82.69, 85.80])]),
    ("Setswana news", 89.02, [("NCHLT tsn (same lang., govt)", ORANGE, "s", [70.59, 77.03, 84.00]),
                              ("NCHLT nso (sister lang., govt)", BLUE, "o", [65.71, 77.76, 85.05])]),
]
fig, axes = plt.subplots(1, 3, figsize=(7.0, 1.95), sharey=True)
xs = [0, 1, 2]
for ax, (title, inlang, series) in zip(axes, panels):
    ax.yaxis.grid(True, color=GRIDC, lw=0.6)
    ax.set_axisbelow(True)
    ax.axhline(inlang, color=MUTED, lw=0.8, ls=(0, (3, 2)))
    ax.text(2.08, inlang + 0.6, f"in-language {r1(inlang)}", ha="right", va="bottom", fontsize=6.2, color=MUTED)
    ends = [s[3][2] for s in series]
    close = abs(ends[0] - ends[1]) < 2.5           # nudge end labels apart when the curves finish together
    for j, (label, col, mk, ys) in enumerate(series):
        ax.plot(xs, ys, color=col, lw=1.6, marker=mk, ms=4.2, mec="white", mew=0.8, zorder=3)
        ax.text(-0.12, ys[0], f"{r1(ys[0])}", ha="right", va="center", fontsize=6.2, color=INK)
        dy = 0 if not close else (1.3 if ys[2] >= max(ends) else -1.3)
        ax.text(2.12, ys[2] + dy, f"{r1(ys[2])}", ha="left", va="center", fontsize=6.2, color=INK)
    ax.set_title(title, fontsize=7.5, fontweight="bold", color=INK, pad=3)
    ax.set_xticks(xs, ["0", "100", "500"])
    ax.set_xlim(-0.55, 2.55)
    ax.set_xlabel("Target sentences ($k$)", labelpad=1.5)
    ax.tick_params(axis="x", length=2)
axes[0].set_ylabel("Entity F1")
axes[0].set_ylim(45, 93)
# legend per panel (series differ by panel), placed bottom-right
for ax, (_, _, series) in zip(axes, panels):
    from matplotlib.lines import Line2D
    ax.legend([Line2D([0], [0], color=c, marker=m, lw=1.6, ms=4, mec="white") for _, c, m, _ in series],
              [l for l, _, _, _ in series], loc="lower right", frameon=False, fontsize=6, handlelength=1.6,
              borderaxespad=0.2)
fig.subplots_adjust(left=0.065, right=0.985, top=0.89, bottom=0.21, wspace=0.16)
save(fig, "rq3_fewshot_curves")


# ---------------------------------------------------------------- Figure 4: RQ4
# Zero-shot F1 on the two Setswana test sets by source (cell 64; mean and SD over 3 seeds).
# Colour = language group of the source; grey = Setswana from the other corpus.
GROUP = {"swa": GREEN, "nya": GREEN, "nso": ORANGE, "sot": ORANGE, "tsn": GREY,
         "xho": BLUE, "zul": BLUE, "ssw": BLUE}
news = [("Swahili (news)", "swa", 80.01, 2.56), ("Chichewa (news)", "nya", 76.33, 2.21),
        ("Setswana (govt)", "tsn", 70.59, 2.99), ("Sepedi (govt)", "nso", 65.71, 1.13),
        ("isiXhosa (news)", "xho", 65.59, 1.26), ("siSwati (govt)", "ssw", 63.03, 1.94),
        ("isiZulu (news)", "zul", 63.01, 1.82), ("Sesotho (govt)", "sot", 61.05, 5.84),
        ("isiXhosa (govt)", "xho", 57.22, 4.19), ("isiZulu (govt)", "zul", 49.03, 3.97)]
govt = [("Setswana (news)", "tsn", 63.31, 0.61), ("Swahili (news)", "swa", 62.88, 2.62),
        ("Sesotho (govt)", "sot", 57.65, 2.36), ("isiXhosa (govt)", "xho", 57.65, 3.27),
        ("isiXhosa (news)", "xho", 56.06, 1.39), ("Chichewa (news)", "nya", 51.90, 0.74),
        ("Sepedi (govt)", "nso", 49.86, 1.73), ("siSwati (govt)", "ssw", 49.86, 1.39),
        ("isiZulu (news)", "zul", 46.77, 2.55), ("isiZulu (govt)", "zul", 40.40, 0.87)]
fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.25))
for ax, (title, rows, inlang) in zip(axes, [("Setswana news test (MasakhaNER)", news, 89.02),
                                            ("Setswana government test (NCHLT)", govt, 78.59)]):
    y = np.arange(len(rows))[::-1]
    ax.xaxis.grid(True, color=GRIDC, lw=0.6)
    ax.set_axisbelow(True)
    for yi, (lab, g, m, sd) in zip(y, rows):
        ax.barh(yi, m, height=0.68, color=GROUP[g], edgecolor="white", lw=0.8)
        ax.errorbar(m, yi, xerr=sd, color=INK, lw=0.7, capsize=1.6, capthick=0.7)
        ax.text(m + sd + 0.8, yi, f"{r1(m)}", va="center", fontsize=6.3, color=INK)
    ax.axvline(inlang, color=MUTED, lw=0.8, ls=(0, (3, 2)))
    ax.text(inlang - 0.6, y[0] + 0.55, f"in-language {r1(inlang)}", ha="right", va="bottom", fontsize=6.2, color=MUTED)
    ax.set_yticks(y, [r[0] for r in rows], fontsize=6.6)
    for tl, r in zip(ax.get_yticklabels(), rows):      # the three pre-specified RQ4 sources in bold
        if r[1] in ("nso", "sot", "swa"):
            tl.set_fontweight("bold")
    ax.tick_params(axis="y", length=0)
    ax.set_xlim(30, 92)
    ax.set_ylim(-0.6, len(rows) - 0.1)
    ax.set_xlabel("Zero-shot entity F1 (mean $\\pm$ SD, 3 seeds)", labelpad=1.5)
    ax.set_title(title, fontsize=7.5, fontweight="bold", color=INK, pad=3)
axes[1].legend([Patch(color=ORANGE), Patch(color=GREEN), Patch(color=BLUE), Patch(color=GREY)],
               ["Sotho-Tswana", "Other Bantu", "Nguni", "Setswana, other corpus"],
               loc="lower right", frameon=True, framealpha=0.95, edgecolor="none", fontsize=6.2,
               handlelength=1, handleheight=0.8, borderaxespad=0.3)
fig.subplots_adjust(left=0.105, right=0.99, top=0.91, bottom=0.17, wspace=0.40)
save(fig, "rq4_setswana_sources")


# ---------------------------------------------------------------- Figure 5: tokenizer fertility (data section)
# Subwords per word on each training corpus (robustness cell 71).
fert = [("Swahili (news)", "swa", 1.51), ("Setswana (news)", "tsn", 1.77), ("Sesotho (govt)", "sot", 1.82),
        ("Setswana (govt)", "tsn", 1.85), ("Sepedi (govt)", "nso", 1.87), ("Chichewa (news)", "nya", 2.25),
        ("isiZulu (news)", "zul", 2.43), ("isiXhosa (news)", "xho", 2.48), ("isiZulu (govt)", "zul", 2.69),
        ("isiXhosa (govt)", "xho", 2.75), ("siSwati (govt)", "ssw", 2.78)]
FCOL = dict(GROUP, tsn=ORANGE)          # here Setswana is just a Sotho-Tswana corpus
fig, ax = plt.subplots(figsize=(3.33, 1.75))
x = np.arange(len(fert))
ax.yaxis.grid(True, color=GRIDC, lw=0.6)
ax.set_axisbelow(True)
for xi, (lab, g, v) in zip(x, fert):
    ax.bar(xi, v, 0.72, color=FCOL[g], edgecolor="white", lw=0.8)
    ax.text(xi, v + 0.04, f"{v:.2f}", ha="center", va="bottom", fontsize=5.6, color=INK)
ax.set_xticks(x, [f"{g}\n{lab.split('(')[1][:-1]}" for lab, g, _ in fert], fontsize=6.2)
ax.tick_params(axis="x", length=0, pad=1.5)
ax.set_ylim(0, 3.2)
ax.set_yticks([0, 1, 2, 3])
ax.set_ylabel("Subwords per word")
ax.legend([Patch(color=ORANGE), Patch(color=GREEN), Patch(color=BLUE)], ["Sotho-Tswana", "Other Bantu", "Nguni"],
          loc="upper left", frameon=False, fontsize=6.2, ncol=3, handlelength=1, handleheight=0.8,
          borderaxespad=0, columnspacing=1.0)
fig.subplots_adjust(left=0.12, right=0.995, top=0.95, bottom=0.2)
save(fig, "fertility_by_corpus")
