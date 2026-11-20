# Builds the COS802 presentation from the course template (7 content slides + thank-you).
# Every number comes from the final report (RQ1-RQ4 version of 11 Nov 2026).
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION

ROOT = __import__("pathlib").Path(__file__).resolve().parents[2]   # repository root
TEMPLATE = str(ROOT / "docs" / "course" / "COS802 2025 Presentation Template.pptx")
OUT = sys.argv[1] if len(sys.argv) > 1 else str(ROOT / "19144832_Sibeko_COS802_Presentation.pptx")

# Template palette (UP blue and the kente pattern colours)
BLUE, RED, ORANGE, GREEN = RGBColor(0x00, 0x5B, 0xAA), RGBColor(0xC8, 0x2A, 0x30), RGBColor(0xD9, 0x80, 0x10), RGBColor(0x3E, 0x75, 0x26)
INK, MUTED, GRID = RGBColor(0x23, 0x1F, 0x20), RGBColor(0x59, 0x59, 0x59), RGBColor(0xA6, 0xA6, 0xA6)
TINT = {"blue": RGBColor(0xE6, 0xEF, 0xF8), "red": RGBColor(0xF9, 0xE6, 0xE7), "orange": RGBColor(0xFC, 0xEF, 0xDD),
        "green": RGBColor(0xE8, 0xF1, 0xE3), "gray": RGBColor(0xF2, 0xF2, 0xF2)}
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
# Colour meaning, fixed for the whole deck: Nguni = BLUE, Sotho-Tswana = ORANGE, other Bantu (Swahili, Chichewa) = GREEN,
# same-language / other-corpus comparison = GRID grey. Cards and panels use neutral blue or grey tints only;
# verdicts use symbols (\u2713 / \u2717), not green/red, so no colour carries two meanings.
FONT = "Arial"
L, R = 0.92, 11.15            # content area: left margin to just before the pattern strip (x = 11.46")
W = R - L

prs = Presentation(TEMPLATE)
S = list(prs.slides)


def remove_body(slide):
    for sh in list(slide.shapes):
        if sh.is_placeholder and sh.placeholder_format.type == 2:   # BODY
            sh._element.getparent().remove(sh._element)


def text(slide, x, y, w, h, paras, size=14, color=INK, bold=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, name=None, space=4):
    # paras: list of str, or list of list-of-(text, {opts}) runs
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    if name:
        tb.name = name
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    for i, p in enumerate(paras):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = align
        para.space_after = Pt(space)
        runs = p if isinstance(p, list) else [(p, {})]
        for t, o in runs:
            r = para.add_run()
            r.text = t
            f = r.font
            f.name = FONT
            f.size = Pt(o.get("size", size))
            f.bold = o.get("bold", bold)
            f.italic = o.get("italic", False)
            f.color.rgb = o.get("color", color)
    return tb


def card(slide, x, y, w, h, fill, name=None):
    s = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    s.adjustments[0] = 0.06
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    s.line.fill.background()
    s.shadow.inherit = False
    if name:
        s.name = name
    return s


def badge(slide, x, y, label, fill, d=0.55, size=13):
    c = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d))
    c.fill.solid()
    c.fill.fore_color.rgb = fill
    c.line.fill.background()
    c.shadow.inherit = False
    tf = c.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = label
    r.font.name, r.font.size, r.font.bold, r.font.color.rgb = FONT, Pt(size), True, WHITE
    return c


def arrow(slide, x, y, w=0.35, h=0.32, color=GRID):
    a = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x), Inches(y), Inches(w), Inches(h))
    a.fill.solid()
    a.fill.fore_color.rgb = color
    a.line.fill.background()
    a.shadow.inherit = False
    return a


def headline(slide, msg):
    text(slide, L, 1.45, W, 0.5, [msg], size=20, bold=True, color=INK, name="Key message")


def style_chart(chart, title, legend=False, vmax=100, label_pos=XL_LABEL_POSITION.OUTSIDE_END):
    chart.font.name = FONT
    chart.font.size = Pt(12)
    chart.font.color.rgb = INK
    chart.has_title = True
    tf = chart.chart_title.text_frame
    tf.text = title
    tf.paragraphs[0].runs[0].font.size = Pt(13)
    tf.paragraphs[0].runs[0].font.bold = True
    tf.paragraphs[0].runs[0].font.name = FONT
    chart.has_legend = legend
    if legend:
        chart.legend.position = XL_LEGEND_POSITION.BOTTOM
        chart.legend.include_in_layout = False
        chart.legend.font.size = Pt(12)
    va = chart.value_axis
    va.has_major_gridlines = False
    va.maximum_scale = vmax
    va.minimum_scale = 0
    va.visible = False
    ca = chart.category_axis
    ca.tick_labels.font.size = Pt(12)
    ca.format.line.color.rgb = GRID
    ca.has_major_gridlines = False
    plot = chart.plots[0]
    plot.has_data_labels = True
    dl = plot.data_labels
    dl.number_format = "0.0"
    dl.number_format_is_linked = False
    dl.font.size = Pt(12)
    dl.font.bold = True
    dl.position = label_pos
    return plot


def color_series(series, rgb):
    series.format.fill.solid()
    series.format.fill.fore_color.rgb = rgb


def label_points(series, values, color=INK, pos=XL_LABEL_POSITION.OUTSIDE_END):
    # text labels: the "0.0" number format follows the Windows locale (decimal comma on en-ZA), these do not
    for pt, v in zip(series.points, values):
        dl = pt.data_label
        dl.position = pos
        tf = dl.text_frame
        tf.text = f"{v:.1f}"
        r = tf.paragraphs[0].runs[0]
        r.font.size, r.font.bold, r.font.name = Pt(12), True, FONT
        r.font.color.rgb = color


# ---------------------------------------------------------------- 1. Title
s = S[0]
tb = [sh for sh in s.shapes if sh.has_text_frame and sh.text_frame.text.startswith("Title")][0]
tf = tb.text_frame
for p in list(tf.paragraphs)[1:]:
    p._p.getparent().remove(p._p)
tf.paragraphs[0].clear() if hasattr(tf.paragraphs[0], "clear") else None
lines = [("Language, Domain, or Pretraining Exposure?", 26, True), ("Cross-lingual NER for South African Bantu languages", 18, False),
         ("", 10, False), ("Mpendulo Sibeko", 24, False), ("COS 802 Presentation", 18, False), ("November 2026", 18, False)]
first = tf.paragraphs[0]
for i, (t, sz, b) in enumerate(lines):
    para = first if i == 0 else tf.add_paragraph()
    for r in list(para.runs):
        r._r.getparent().remove(r._r)
    para.space_after = Pt(4)
    r = para.add_run()
    r.text = t
    r.font.name, r.font.size, r.font.bold, r.font.color.rgb = FONT, Pt(sz), b, WHITE
s.notes_slide.notes_text_frame.text = (
    "(About 30 seconds.) Good morning, everyone. My name is Mpendulo Sibeko, and my project is called \"Language, Domain, or Pretraining "
    "Exposure?\". It is about cross-lingual named entity recognition for South African Bantu languages. The practical question "
    "behind it is simple: when we build an entity recogniser for one of these languages and do not have enough labelled data, "
    "which other language, and which corpus, should the model learn from?")

# Headshot: fill the template's rounded "Your Headshot/Selfie" frame with the photo, keeping its rounded corners and border
import os
from PIL import Image
from pptx.oxml.ns import qn
HEADSHOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "headshot.jpg")
frame = [sh for sh in s.shapes if sh.has_text_frame and "Headshot" in sh.text_frame.text][0]
for para in frame.text_frame.paragraphs:                 # remove the placeholder text
    for run in list(para.runs):
        run._r.getparent().remove(run._r)
_, rId = s.part.get_or_add_image_part(HEADSHOT)
spPr = frame._element.spPr
for tag in ("a:noFill", "a:solidFill", "a:gradFill", "a:blipFill", "a:pattFill"):
    for el in spPr.findall(qn(tag)):
        spPr.remove(el)
iw, ih = Image.open(HEADSHOT).size
box, img = frame.width / frame.height, iw / ih            # crop the photo to the frame's aspect ratio, centred
lr = max(0.0, (1 - box / img) / 2)
tb = max(0.0, (1 - img / box) / 2)
blip_fill = spPr.makeelement(qn("a:blipFill"), {"rotWithShape": "1"})
blip_fill.append(blip_fill.makeelement(qn("a:blip"), {qn("r:embed"): rId}))
blip_fill.append(blip_fill.makeelement(qn("a:srcRect"), {"l": str(round(lr * 100000)), "r": str(round(lr * 100000)),
                                                          "t": str(round(tb * 100000)), "b": str(round(tb * 100000))}))
stretch = blip_fill.makeelement(qn("a:stretch"), {})
stretch.append(stretch.makeelement(qn("a:fillRect"), {}))
blip_fill.append(stretch)
spPr.find(qn("a:prstGeom")).addnext(blip_fill)

# ---------------------------------------------------------------- 2. Motivation
s = S[1]
remove_body(s)
headline(s, "Which source language should a South African NER model learn from?")
card(s, L, 2.2, 4.4, 2.35, TINT["blue"], "Stat card")
text(s, L + 0.3, 2.4, 3.9, 0.8, [[("24.5", {"color": GRID}), ("  \u2192  ", {"color": MUTED}), ("83.7", {"color": BLUE})]], size=44, bold=True, name="Stat")
text(s, L + 0.3, 3.35, 3.9, 1.1, ["Zero-shot isiXhosa F1 when the source switches from English to isiZulu (MasakhaNER 2.0)"], size=14, color=INK)
text(s, L, 4.85, 4.4, 2.0, [
    [("Labelled NER data is scarce ", {"bold": True}), ("for South African Bantu languages, so models borrow from a source language", {})],
    [("Prior evidence is limited: ", {"bold": True}), ("news only, and no Sepedi or Sesotho in MasakhaNER 2.0", {})]],
    size=14, space=10, name="Context")
rq = [("RQ1", BLUE, "blue", "Relatedness or domain", "Which predicts zero-shot transfer better?"),
      ("RQ2", BLUE, "blue", "Pretraining exposure", "Do targets seen in pretraining transfer better?"),
      ("RQ3", BLUE, "blue", "Few-shot data", "How far do 100 and 500 target sentences close the gap?"),
      ("RQ4", BLUE, "blue", "Sources for Setswana", "Are Sepedi and Sesotho better sources than Swahili and Chichewa?")]
cx, cw, ch, gap = 5.65, 2.65, 2.15, 0.2
for i, (lab, col, tint, head, body) in enumerate(rq):
    x = cx + (i % 2) * (cw + gap)
    y = 2.2 + (i // 2) * (ch + gap)
    card(s, x, y, cw, ch, TINT[tint], f"{lab} card")
    badge(s, x + 0.2, y + 0.2, lab, col, d=0.62, size=12)
    text(s, x + 0.2, y + 0.95, cw - 0.4, 0.4, [head], size=14, bold=True)
    text(s, x + 0.2, y + 1.3, cw - 0.4, 0.8, [body], size=12, color=MUTED)
s.notes_slide.notes_text_frame.text = (
    "(About 1 minute.) For most South African Bantu languages there is little labelled NER data, so the standard approach is "
    "cross-lingual transfer: fine-tune a multilingual model on a source language and apply it to the target. The choice of "
    "source matters a lot. In MasakhaNER 2.0, zero-shot isiXhosa scores 24.5 F1 with an English source and 83.7 with an "
    "isiZulu source. What we do not know is why a source works. Is it a related language? Text from the same domain? Or a "
    "language the model saw during pretraining? For South African languages, the evidence is limited: MasakhaNER covers news "
    "only, and it has no Sepedi or Sesotho. So I ask four questions. RQ1: does relatedness or domain match better predict "
    "transfer? RQ2: do targets seen in pretraining transfer better? RQ3: how far do 100 and 500 target sentences close the "
    "gap? And RQ4: are Sepedi and Sesotho, Setswana's closest relatives, better Setswana sources than Swahili and Chichewa?")

# ---------------------------------------------------------------- 3. Data
s = S[2]
remove_body(s)
headline(s, "Two corpora, six target languages: language and corpus crossed")
corp = [("NCHLT NER", "Government text", "isiZulu, isiXhosa, Siswati, Sepedi, Sesotho, Setswana", "Our seeded 80/10/10 split", "gray"),
        ("MasakhaNER 2.0", "News", "isiZulu, isiXhosa, Setswana; Swahili and Chichewa as sources only", "Published splits", "blue")]
for i, (name, dom, langs, split, tint) in enumerate(corp):
    y = 2.2 + i * 1.6
    card(s, L, y, 4.6, 1.4, TINT[tint], f"{name} card")
    text(s, L + 0.25, y + 0.15, 4.1, 1.2, [[(name, {"bold": True, "size": 16, "color": BLUE}), ("   " + dom, {"color": MUTED, "size": 13})],
                                          [(langs, {})], [(split, {"color": MUTED, "size": 12})]], size=13, space=3)
# language map
text(s, 5.85, 2.2, 5.3, 0.35, ["Languages and AfroXLMR pretraining exposure"], size=14, bold=True)
groups = [("Nguni", BLUE, [("isiZulu", True), ("isiXhosa", True), ("Siswati", False)]),
          ("Sotho-Tswana", ORANGE, [("Sepedi", False), ("Sesotho", True), ("Setswana", False)]),
          ("Other Bantu\n(sources only)", GREEN, [("Swahili", None), ("Chichewa", None)])]
for gi, (g, col, langs) in enumerate(groups):
    y = 2.7 + gi * 0.78
    text(s, 5.85, y, 1.45, 0.6, [g], size=13, bold=True, color=col, anchor=MSO_ANCHOR.MIDDLE)
    for li, (lang, seen) in enumerate(langs):
        x = 7.35 + li * 1.27
        chip = card(s, x, y + 0.05, 1.17, 0.5, col if seen else TINT["green"] if seen is None else TINT["gray"], f"{lang} chip")
        tf = chip.text_frame
        tf.margin_left = tf.margin_right = 0
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = lang
        r.font.name, r.font.size, r.font.bold = FONT, Pt(13), True
        r.font.color.rgb = WHITE if seen else INK
card(s, 5.85, 5.08, 0.32, 0.25, BLUE)
card(s, 6.22, 5.08, 0.32, 0.25, ORANGE)
text(s, 6.65, 5.03, 4.5, 0.35, ["Filled = seen in AfroXLMR pretraining"], size=13, color=MUTED)
stats = [("11", "sources"), ("9", "test sets"), ("3", "seeds"), ("333", "evaluations")]
for i, (n, lab) in enumerate(stats):
    x = L + i * 2.6
    text(s, x, 5.65, 1.0, 0.7, [n], size=36, bold=True, color=BLUE, anchor=MSO_ANCHOR.MIDDLE)
    text(s, x + (0.45 if len(n) == 1 else 0.7 if len(n) == 2 else 1.0), 5.75, 1.5, 0.55, [lab], size=14, color=INK, anchor=MSO_ANCHOR.MIDDLE)
text(s, L, 6.55, W, 0.35, ["PER, LOC, ORG only  \u00b7  3,000 training sentences per source  \u00b7  deduplicated data"],
     size=14, color=MUTED)
s.notes_slide.notes_text_frame.text = (
    "(About 1 minute.) I use two public corpora. NCHLT is government text, annotated for all six target languages; it has no "
    "official splits, so I made one fixed 80/10/10 split. MasakhaNER 2.0 is news: it has isiZulu, isiXhosa and Setswana, and "
    "I use Swahili and Chichewa only as sources. The useful property is that isiZulu, isiXhosa and Setswana appear in both "
    "corpora, so I can separate language from corpus. The languages form two clusters, Nguni and Sotho-Tswana. The filled "
    "boxes are the three languages AfroXLMR saw in pretraining: isiZulu, isiXhosa and Sesotho. Eleven sources, nine test sets "
    "and three seeds give 333 evaluations. To keep the comparison fair, I score only PER, LOC and ORG, I mask MISC and DATE, "
    "every source is capped at 3,000 training sentences, and all results come from a deduplicated run.")

# ---------------------------------------------------------------- 4. Approach
s = S[3]
remove_body(s)
headline(s, "Pre-specified tests answer the questions; checks test the surprises")
steps = [("1", "Fine-tune", "AfroXLMR-base on one source, 3 seeds"),
         ("2", "Zero-shot", "Score on all 9 test sets (297 evaluations)"),
         ("3", "Few-shot", "Add 100 or 500 target sentences (36)"),
         ("4", "Measure", "Entity F1 and transfer ratio (transfer F1 \u00f7 in-language F1)")]
bw, bgap = 2.3, 0.33
for i, (n, head, body) in enumerate(steps):
    x = L + i * (bw + bgap)
    card(s, x, 2.15, bw, 1.85, TINT["blue"], f"Step {n}")
    badge(s, x + 0.18, 2.3, n, BLUE, d=0.48, size=14)
    text(s, x + 0.78, 2.32, bw - 0.9, 0.45, [head], size=15, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    text(s, x + 0.18, 2.9, bw - 0.36, 1.05, [body], size=14, color=INK)
    if i < 3:
        arrow(s, x + bw + 0.0, 2.92, w=0.32, h=0.3)
card(s, L, 4.2, W, 0.75, TINT["gray"], "Statistics")
text(s, L + 0.25, 4.27, W - 0.5, 0.65, [[("Statistics:  ", {"bold": True}),
     ("5 pre-planned comparisons (paired bootstrap, Holm correction) + a regression over 90 source\u2013target pairs", {})]],
     size=15, anchor=MSO_ANCHOR.MIDDLE)
text(s, L, 5.15, W, 0.35, [[("Robustness checks", {"bold": True, "color": BLUE}), ("  (added after seeing the main results)", {"color": MUTED, "size": 13})]], size=15)
fu = [("Equal entity counts", "Setswana sources re-trained on 2,500 entity spans each"),
      ("Corpus terms", "Source and test corpus as separate regression terms"),
      ("Tokenizer fit", "Fertility gap (subwords per word) in the regression")]
fw, fgap = 3.15, 0.37
for i, (head, body) in enumerate(fu):
    x = L + i * (fw + fgap)
    card(s, x, 5.6, fw, 1.25, TINT["gray"], head)
    text(s, x + 0.2, 5.7, fw - 0.4, 1.1, [[(head, {"bold": True, "size": 15})], [(body, {"size": 14, "color": INK})]], space=3)
    if i < 2:
        arrow(s, x + fw + 0.02, 6.07, w=0.32, h=0.3)
s.notes_slide.notes_text_frame.text = (
    "(About 1 minute.) Everything uses one model, AfroXLMR-base, with one set of hyperparameters. Step one: I fine-tune it on "
    "a single source, with three seeds. Step two: I score every model zero-shot on all nine test sets. Step three: for the "
    "three news targets, I continue training on 100 or 500 target sentences. Step four: I measure entity-level F1 and the "
    "transfer ratio, which divides the cross-lingual score by the in-language score, so that easy and hard targets can be "
    "compared. Before the run I fixed five contrasts, tested with a paired bootstrap and Holm correction, and a mixed-effects "
    "regression over the 90 transfer pairs. The bottom row is different: I added these checks after seeing the main results, "
    "to test whether the surprises survive. I re-trained the Setswana sources on the same number of entities, I split domain "
    "match into source-corpus and test-corpus terms, and I added tokenizer fit to the regression.")

# ---------------------------------------------------------------- 5. Results
s = S[4]
remove_body(s)
headline(s, "Relatedness predicts transfer, but the corpus can override it")
cd = CategoryChartData()
cd.categories = ["isiZulu news test", "isiXhosa news test"]
cd.add_series("Sister language, news source", (82.4, 82.7))
cd.add_series("Same language, government source", (50.4, 70.0))
ch = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(L), Inches(2.05), Inches(4.85), Inches(3.55), cd).chart
plot = style_chart(ch, "RQ1: news test sets, F1", legend=True)
plot.gap_width, plot.overlap = 70, -10
color_series(plot.series[0], BLUE)
color_series(plot.series[1], GRID)
label_points(plot.series[0], (82.4, 82.7))
label_points(plot.series[1], (50.4, 70.0))
cd = CategoryChartData()
cd.categories = ["Swahili", "Chichewa", "Setswana (govt)", "Sepedi", "Sesotho"]
cd.add_series("F1", (80.0, 76.3, 70.6, 65.7, 61.0))
ch = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(6.05), Inches(2.05), Inches(5.1), Inches(3.55), cd).chart
plot = style_chart(ch, "RQ4: Setswana news F1 by source")
plot.gap_width = 55
ser = plot.series[0]
color_series(ser, BLUE)
for i, col in enumerate([GREEN, GREEN, GRID, ORANGE, ORANGE]):
    pt = ser.points[i]
    pt.format.fill.solid()
    pt.format.fill.fore_color.rgb = col
label_points(ser, (80.0, 76.3, 70.6, 65.7, 61.0))
text(s, 6.05, 5.55, 5.1, 0.3, [[("Green", {"bold": True, "color": GREEN}), (" other Bantu (news)   ", {}), ("Orange", {"bold": True, "color": ORANGE}), (" Sotho-Tswana (govt)", {})]],
     size=13, color=MUTED, align=PP_ALIGN.CENTER)
verdicts = [("H1", "\u2713 Supported", BLUE, "+0.10 TR per step; corpus can override"),
            ("H2", "\u2717 Not supported", INK, "No advantage for seen targets"),
            ("H3", "\u2713 Supported", BLUE, "500 sentences close 57\u201389%"),
            ("H4", "\u2717 Reversed", INK, "Swahili ahead by 13\u201319 F1")]
vw, vgap = 2.4, 0.18
for i, (h, v, col, ev) in enumerate(verdicts):
    x = L + i * (vw + vgap)
    card(s, x, 5.95, vw, 0.95, TINT["blue"] if col == BLUE else TINT["gray"], f"{h} verdict")
    text(s, x + 0.15, 6.02, vw - 0.3, 0.85, [[(h + "  ", {"bold": True, "color": INK}), (v, {"bold": True, "color": col})], [(ev, {"size": 12, "color": INK})]],
         size=13, space=2)
s.notes_slide.notes_text_frame.text = (
    "(About 1 minute 20 seconds.) These are the pre-specified results. First, relatedness is the most consistent predictor: "
    "each step closer on the relatedness scale adds about 0.10 to the transfer ratio. But look at the left chart. On the "
    "isiZulu news test, an isiXhosa news model scores 82.4, while an isiZulu model trained on government text scores only "
    "50.4. A different language from the same corpus beats the same language from the other corpus, by 32 points for isiZulu "
    "and 13 for isiXhosa. On the government test sets the picture is mixed: it also happens for isiZulu, but not for "
    "isiXhosa or Setswana. Second, H2 is not supported: targets seen in pretraining do not score higher than unseen ones, "
    "although with six targets exposure moves together with language cluster. Third, H3 is "
    "supported: 500 target sentences close 57 to 89 percent of the gap. The surprise is on the right. For Setswana news, "
    "Swahili scores 80 and Chichewa 76, but Setswana's close relatives, Sepedi and Sesotho, score only 66 and 61. That is the "
    "reverse of my fourth hypothesis, by 13 to 19 points, and it held when I gave every source the same number of entities.")

# ---------------------------------------------------------------- 6. Discussion
s = S[5]
remove_body(s)
headline(s, "The surprises survive the checks, but text and labels stay entangled")
cd = CategoryChartData()
cd.categories = ["Swahili", "Chichewa", "Sepedi", "Sesotho", "isiXhosa"]
cd.add_series("F1", (78.5, 73.2, 64.2, 61.4, 60.5))
ch = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(L), Inches(2.05), Inches(4.5), Inches(3.45), cd).chart
plot = style_chart(ch, "Equal entity counts: Setswana news F1")
plot.gap_width = 55
ser = plot.series[0]
for i, col in enumerate([GREEN, GREEN, ORANGE, ORANGE, BLUE]):
    pt = ser.points[i]
    pt.format.fill.solid()
    pt.format.fill.fore_color.rgb = col
label_points(ser, (78.5, 73.2, 64.2, 61.4, 60.5))
text(s, L, 5.5, 4.5, 0.3, [[("Green", {"bold": True, "color": GREEN}), (" other Bantu  ", {}), ("Orange", {"bold": True, "color": ORANGE}),
     (" Sotho-Tswana  ", {}), ("Blue", {"bold": True, "color": BLUE}), (" Nguni", {})]], size=13, color=MUTED, align=PP_ALIGN.CENTER)
# Tokenizer fit as a stat panel (replaces the small fertility bar chart)
card(s, 5.65, 2.15, 2.8, 3.6, TINT["gray"], "Fertility card")
text(s, 5.85, 2.3, 2.45, 3.35, [
    [("Tokenizer fit", {"bold": True, "size": 16})],
    [("Subwords per word", {"size": 13, "color": MUTED})],
    [("1.51  ", {"bold": True, "size": 26, "color": GREEN}), ("Swahili", {"size": 14})],
    [("1.8  ", {"bold": True, "size": 26, "color": ORANGE}), ("Sotho-Tswana", {"size": 14})],
    [("2.4\u20132.8  ", {"bold": True, "size": 26, "color": BLUE}), ("Nguni", {"size": 14})],
    [("The fertility gap explains about a third of the relatedness effect", {"size": 13})]],
    size=14, space=6)
card(s, 8.65, 2.15, 2.5, 3.6, TINT["gray"], "Example card")
text(s, 8.8, 2.3, 2.25, 3.35, [
    [("Same words, different rules?", {"bold": True, "size": 15})],
    [("NCHLT (government)", {"bold": True, "color": MUTED, "size": 13})],
    [("[Tona Motsoaledi]", {"bold": True, "color": BLUE, "size": 15}), ("PER", {"size": 11, "color": BLUE})],
    [("MasakhaNER (news)", {"bold": True, "color": MUTED, "size": 13})],
    [("Tona ", {"bold": True, "size": 15}), ("[Motsoaledi]", {"bold": True, "color": BLUE, "size": 15}), ("PER", {"size": 11, "color": BLUE})],
    [("Tona = minister. Not tested here.", {"size": 13, "color": MUTED})]],
    size=14, space=7)
card(s, L, 5.95, W, 0.95, TINT["blue"], "Takeaway")
text(s, L + 0.25, 6.02, W - 0.5, 0.85, [[("Swahili still leads Sepedi by 14.3 F1 with equal entity counts. ", {"bold": True}),
     ("Corpus = text domain + annotation guideline, so this design cannot separate the two.", {})]],
     size=15, anchor=MSO_ANCHOR.MIDDLE)
s.notes_slide.notes_text_frame.text = (
    "(About 1 minute.) Do the surprises survive? Maybe Swahili wins only because news has more entities, so I re-trained "
    "every Setswana source on exactly 2,500 entity spans. Swahili still scores 78.5 and Sepedi 64.2, a 14-point gap. "
    "Tokenizer fit matters too: the fertility gap, subword pieces per word, absorbs about a third of the relatedness effect, "
    "and Swahili's fertility, 1.51, is close to the Sotho-Tswana languages. What I cannot separate is text from labels, "
    "because each corpus has its own guideline. A government sentence may tag \"Tona Motsoaledi\", Minister Motsoaledi, "
    "with the title inside the person, while news tags only the name. So the corpus effect may come from text, labels, or both.")

# ---------------------------------------------------------------- 7. Conclusion
s = S[6]
remove_body(s)
headline(s, "Four answers, and what I would test next")
cols = [("Takeaways", BLUE, "blue", [
            "For news NER, start from a news-annotated related source, not same-language government text",
            "Swahili is a strong Setswana source (80.0 F1)",
            "500 target sentences bring every source within 1–5 F1 of in-language"]),
        ("Reflection", INK, "gray", [
            "One model, three seeds",
            "Corpus bundles text domain and annotation guideline",
            "Exposure confounded with language cluster",
            "Setswana result was the opposite of my prediction"]),
        ("Not finished in time", INK, "gray", [
            "Error analysis: strict vs relaxed matching",
            "Guideline-specific output heads",
            "Relabel titles and roles in Sepedi/Sesotho, with a speaker-checked word list",
            "Relabel test data under one guideline"])]
kw, kgap = 3.2, 0.3
for i, (head, col, tint, items) in enumerate(cols):
    x = L + i * (kw + kgap)
    card(s, x, 2.15, kw, 3.75, TINT[tint], head)
    text(s, x + 0.25, 2.3, kw - 0.5, 0.45, [head], size=18, bold=True, color=col)
    tb = text(s, x + 0.25, 2.85, kw - 0.5, 3.0, items, size=14, space=9)
    for p in tb.text_frame.paragraphs:
        pPr = p._p.get_or_add_pPr()
        pPr.set("marL", "228600")
        pPr.set("indent", "-228600")
        bu = pPr.makeelement("{http://schemas.openxmlformats.org/drawingml/2006/main}buChar", {"char": "\u2022"})
        pPr.append(bu)
card(s, L, 6.1, W, 0.8, BLUE, "Answer banner")
text(s, L + 0.3, 6.1, W - 0.6, 0.8, [[("Answer: ", {"bold": True}), ("relatedness is the best general predictor, matching the target's corpus can override it, and for Setswana a news source beats its closest relatives", {})]],
     size=15, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
s.notes_slide.notes_text_frame.text = (
    "(About 1 minute.) To conclude: relatedness is the best general predictor, matching the target's corpus can override "
    "it, and for Setswana, Swahili news beats its closest relatives. In practice, start news NER from a news-annotated related "
    "source, use Swahili for Setswana, and expect 500 target sentences to bring any source within five points of a fully "
    "trained model. The limits: one model, three seeds, corpus mixed with guideline, exposure tied to language cluster, and a Setswana result that was the opposite of my prediction. "
    "The right-hand column lists follow-ups I started but could not finish in time: an error analysis, separate output heads "
    "per guideline, relabelling titles and roles in the Sepedi and Sesotho data with a speaker-checked word list, and "
    "relabelling test data under one guideline, the causal test. Thank you.")

# ---------------------------------------------------------------- 8. Thank you (template slide kept as is)
S[7].notes_slide.notes_text_frame.text = "Questions."

prs.save(OUT)
print("saved", OUT)
