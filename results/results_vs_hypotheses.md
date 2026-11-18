# Results Against the Hypotheses

COS802: *Language, Domain, or Pretraining Exposure? Cross-Lingual NER for South African Bantu Languages*. Written 25 Oct 2026.

**Evidence base.**
- **Main run (v2):** the deduplicated run, 333 evaluations (11 sources × 9 test sets × 3 seeds, plus 36 few-shot), AfroXLMR-base.
- **Follow-ups:** the regression with separate corpus terms and fertility gap (10.8), the truncation check (10.8c) and the RQ4 entity-capped re-run (10.9).
- **Section 12:** base-model representation analysis.
- **Section 13:** annotation tests 1–3 (seed 13).
- **Section 14 (added 26 Oct):** guideline-head models. 14A decomposes the cross-corpus gap into annotation and text (9 runs). 14B tests whether Sepedi/Sesotho help Setswana once their conventions are kept apart (12 runs).
- **Details:** in the notebook and in `COS802_Notes_Domain_vs_Relatedness.md`.

## Summary

| Hypothesis | Verdict | Key evidence |
|---|---|---|
| **H1:** related sources transfer better on average, but domain match may reduce or reverse this | **Supported, with a different mechanism than assumed** | Relatedness +0.10 transfer ratio per step (p < .001). Domain reverses it among close relatives on news targets only (+32 / +13 F1). The "domain" effect is largely annotation conventions: at least 44% of the cross-corpus gap is guideline-driven (14A) |
| **H2a:** seen targets have higher absolute F1 | **Not supported** | Unseen targets score as high or higher. Exposure is not significant (p = .18–.36) |
| **H2b:** transfer ratio may not follow; unseen targets can gain more | **Direction consistent, not significant, confounded** | Unseen targets show higher transfer ratios from distant sources, but unseen also means mostly Sotho-Tswana, low fertility |
| **H3:** target data narrows the gap, with most of the gain by 100 sentences | **First half supported; second half only for weak sources** | Gap closure at 500 is 0.57–0.89. "Most by 100" holds only for the two weakest starting points |
| **H4:** Sepedi/Sesotho beat Swahili/Chichewa for Setswana | **Rejected (reversed)**, with a nuance | Swahili wins by 13–19 F1 (two-sided Holm p = .01), robust to equal entity counts. Sepedi *finds* Setswana entities better but over-labels. Keeping NCHLT conventions in a separate head does not rescue it (14B). Relabelling titles/roles/institutions in the Sepedi training data recovers +8.2 F1 (58% of the gap), but Swahili stays 6.1 F1 ahead (Exp 15) |

---

## H1: relatedness vs domain match (RQ1)

> **H1.** Related sources transfer better on average, but domain match may reduce or reverse this.

**The first part holds.** Relatedness is the most consistent predictor:
- Same-language and same-cluster sources average 56–61 F1, against 37–47 for sources from other clusters (section 10.2).
- In the mixed-effects regression (90 seed-averaged pairs), relatedness gives **+0.10 transfer ratio per step (p < .001)** and stays significant in every model specification.

**"Domain may reduce or reverse this" holds partly, and only in one direction.**
- Among close relatives, a sister-language **news** source beats a same-language **government** source on **news** targets: **+32.0 F1 for isiZulu** and **+12.7 for isiXhosa**, both significant (Holm p = .005).
- On **government** targets it does not hold. Language identity wins for isiXhosa (−21 F1) and Setswana (−6 to −13 F1).
- In the regression, domain match is not significant overall (p = .71). With source corpus and test corpus as separate terms, the benefit appears **only for news targets** (+0.13 transfer ratio, p = .12; p = .049 with the fertility gap; exploratory). A news source does not help a government target (p = .70).

**Two findings change how H1 should be read.**

1. **Much of the "domain" effect is really annotation.** H1 assumed the contrast is government vs news *text*, but:
   - In the base model, same-language text from the two corpora is about as similar as text from two sister languages in one corpus. isiZulu distance is 0.23 against 0.20, and Setswana only 0.06, yet cross-corpus transfer drops by 18–32 F1 (section 12).
   - Relaxing span boundaries closes **54% of the cross-corpus gap** (23.7 → 10.9 F1), against 36% for sister languages (Test 1).
   - The remaining errors are **scope disagreements**. NCHLT labels titles and role nouns as PER (*uNgqongqoshe*, "the minister"; *kuMongameli*, "to the president") and generic institutions as ORG (*ePhalamende*, "in parliament"; *uMkhandlu*, "the council"); MasakhaNER does not (Tests 1–2).
   - Locations, which both guidelines define alike, transfer almost fully for Setswana and into NCHLT isiXhosa (gap 5–6 F1). PER and ORG do not (15–30 F1).
   - `MISC` is not the mechanism. It holds mostly numbers and common words that MasakhaNER also leaves unlabelled (Test 3).
   - So what H1 calls domain match is mostly **matching annotation conventions**. News-only vocabulary (*ANC*, *Ramaphosa*) is a real but smaller part.
   - **Direct measurement (Experiment 14A).** One encoder is trained jointly on NCHLT-L and MasakhaNER-L, with a separate adapter and head per guideline. Scoring the same test sentences through the two heads isolates the guideline effect: same text, same encoder, different labelling rule.

     | | Guideline part | Text part (upper bound) | Total gap | Guideline share (lower bound) |
     |---|---|---|---|---|
     | isiZulu (news / govt test) | 20.9 / 15.4 | 14.8 / 13.5 | 35.6 / 28.9 | **59% / 53%** |
     | isiXhosa | 3.6 / 4.4 | 13.2 / 7.2 | 16.8 / 11.6 | 21% / 38% |
     | Setswana | 4.3 / 6.5 | 13.2 / 8.9 | 17.5 / 15.4 | 25% / 42% |
     | **Mean** | **9.2** | **11.8** | **21.0** | **44%** |

     At least 44% of the cross-corpus gap is the guideline, and more than half for isiZulu. About half of the guideline part disappears under relaxed matching, so it is mostly a boundary convention. The guideline share is a lower bound because the shared encoder also sees target-guideline labels.
2. **Part of "relatedness" is tokenizer fertility.** The fertility gap between source and target (subwords per word) is a strong predictor (−0.18 transfer ratio per unit, p = .001). It absorbs about a third of the relatedness effect (0.112 → 0.078), though relatedness stays significant. The two are partly collinear: the Nguni languages are high-fertility, and Sotho-Tswana and Swahili low.

**Statement for the report.**

> H1 is supported: relatedness is the stronger general predictor of transfer. Domain match reverses it only for news targets among close relatives, and an error analysis shows that this "domain" effect reflects differences in annotation conventions more than differences in text. A joint model with guideline-specific output heads attributes at least 44% of the cross-corpus gap to the annotation guideline alone (53–59% for isiZulu). About a third of the relatedness effect is shared with the tokenizer-fertility gap between source and target.

---

## H2: pretraining exposure (RQ2)

> **H2a.** Seen targets have higher absolute F1. **H2b.** Transfer ratio may not follow; unseen targets can gain more.

Seen targets (in AfroXLMR pretraining): isiZulu, isiXhosa, Sesotho. Unseen: Siswati, Sepedi, Setswana.

**H2a: not supported.**
- Unseen targets score as high as or higher than seen ones at every relatedness level (section 10.3):

  | Source relatedness | Seen targets (mean F1) | Unseen targets (mean F1) |
  |---|---|---|
  | Same language (other corpus) | 58.0 | 67.0 |
  | Same cluster | 57.7 | 57.8 |
  | Other Southern Bantu | 35.1 | 50.8 |
  | Other Bantu | 28.2 | 55.1 |

- In-language NCHLT scores are highest for unseen Sepedi (83.6) and lowest for seen Sesotho (59.5).
- Exposure is not significant in any regression (p = .18–.36).

**H2b: the direction fits, but it cannot be attributed to exposure.**
- Unseen targets do get higher transfer ratios from distant sources (0.66 against 0.38 from other-Bantu sources).
- But two of the three unseen targets are **Sotho-Tswana**, which accept low-fertility sources such as Swahili well. Exposure, language cluster and fertility move together.
- The seen target Sesotho has an anomalous NCHLT corpus (noted in the literature review and confirmed here), which lowers the "seen" group.

**Why RQ2 cannot be answered in this design.** With six targets, exposure is confounded with cluster, fertility and corpus quality. As the literature review noted, every unseen target has a seen relative. The XLM-R-base contrast (same tokenizer, different exposure) is the proper test.

**Statement for the report.**

> H2a is not supported: unseen targets score as high as or higher than seen ones. H2b is directionally consistent, with higher transfer ratios for unseen targets, but the effect cannot be separated from language cluster and tokenizer fertility with six targets, so RQ2 remains exploratory.

---

## H3: few-shot narrowing (RQ3)

> **H3.** Target data narrows the gap, with most of the gain by 100 sentences.

**"Target data narrows the gap": supported.**
- With 500 target sentences, **57–89% of the gap** to the in-language model closes.
- Government sources nearly catch up with sister-language news sources (isiZulu 83.5 against 86.2; isiXhosa 83.6 against 85.8).
- For Setswana, the Sepedi source (85.1) slightly passes the Setswana government source (84.0).

**"Most of the gain by 100 sentences": only for weak starting points.**

| Source → target | k = 0 | k = 100 | k = 500 | Share of gain by 100 |
|---|---|---|---|---|
| NCHLT zul → zul news | 50.4 | 75.1 | 83.5 | **75%** |
| NCHLT nso → tsn news | 65.7 | 77.8 | 85.1 | **62%** |
| NCHLT tsn → tsn news | 70.6 | 77.0 | 84.0 | 48% |
| NCHLT xho → xho news | 70.0 | 75.8 | 83.6 | 42% |
| News xho → zul news | 82.4 | 83.9 | 86.2 | 38% |
| News zul → xho news | 82.7 | 82.7 | 85.8 | 0% |

Sources far from the target gain most in the first 100 sentences. Sources already close to the ceiling gain little by 100 and most between 100 and 500. That contradicts the general "most gains by 100" pattern in the literature (for example Lauscher et al. 2020) for strong sources.

**The annotation lens offers a plausible reading** (interpretive, not tested). The large early jumps for government sources fit 100 target sentences teaching the target corpus's conventions, for example not tagging titles. Those conventions are learned quickly and account for much of the gap.

**Statement for the report.**

> H3 is supported in that target data narrows every transfer gap (57–89% closed at 500 sentences). The claim that most of the gain arrives by 100 sentences holds only for weak, cross-corpus starting points; near-ceiling sister-language sources gain mainly between 100 and 500 sentences.

---

## H4: Setswana source choice (RQ4)

> **H4.** Exploratory: Sepedi/Sesotho are better Setswana sources than Swahili/Chichewa, tested on Setswana news where relatedness and domain conflict.

**Rejected, and the reversal is robust.**
- Swahili beats Sepedi and Sesotho by **13–19 F1** on both Setswana test sets (news: Swahili 80.0, Chichewa 76.3, Sepedi 65.7, Sesotho 61.0). All three pre-specified contrasts go the opposite way to the hypothesis (two-sided Holm p = .01).
- **Within NCHLT,** where the corpus is held fixed, Sepedi (49.9) and Sesotho (57.7) are no better than isiXhosa (57.7) on Setswana.
- **Not entity density:** with every source trained on the same 2,500 entity spans, Swahili still leads Sepedi by 14.3 F1, from about half as many sentences (10.9).
- **Not representational closeness:** Swahili is the *most distant* source from Setswana in the base model (distance 1.29, against about 0.2 for related pairs), yet the best one (section 12).
- **Not truncation:** at most 2.8% of Setswana gold entities are cut off (10.8c).
- **Against the literature review's prediction.** The review proposed that a Sepedi score inside the published 73–74 band would mean "domain absorbs relatedness". Sepedi lands *below* it (65.7), while Swahili lands well above the published 73.1 (80.0; a different model, mDeBERTaV3 vs AfroXLMR-base).

**The nuance (Section 13): relatedness is not useless.**
- On Setswana news, the Sepedi model **misses fewer gold entities than Swahili** (1.0% against 4.8%) and locates 95% of the entities it gets wrong.
- It loses on **over-labelling** (28% of its predictions are spurious; 1,878 predictions for 1,327 gold entities) and on **boundaries**, conventions it learned from NCHLT Sepedi. Inside NCHLT, the Sepedi model predicts 899 entities where NCHLT Setswana has 502.
- With relaxed matching, the Sepedi–Swahili gap shrinks from 14.6 to 9.4 F1.
- So relatedness helps **recognition**, while the source corpus's annotation conventions cost **precision**.

**Can the conventions be kept out? (Experiment 14B: no.)** NCHLT Sepedi or Sesotho was trained together with MasakhaNER Swahili, either mixed into one head or with a separate adapter and head per guideline. Setswana news was then scored through the news head.

| Training data | Setswana news F1 | vs Swahili alone (per seed) | Predicted / gold entities |
|---|---|---|---|
| Swahili alone (main run) | 80.0 | – | – |
| Sepedi + Swahili, guideline heads | 71.1 | **−8.9** (−8.8, −5.2, −12.8) | 1,765 / 1,327 |
| Sepedi + Swahili, shared head | 71.3 | −8.7 | 1,793 / 1,327 |
| Sesotho + Swahili, guideline heads | 73.6 | **−6.4** (−6.5, −3.8, −9.0) | 1,788 / 1,327 |
| Sesotho + Swahili, shared head | 72.6 | −7.4 | 1,774 / 1,327 |

- Adding the related source **hurts** in every seed, and separate heads recover at most 1 F1.
- Over-labelling survives the news head (about 1,780 predictions for 1,327 gold), so it sits in the **shared encoder**, not just the output layer.
- Swahili alone (62.9) also beats every mixed model on the Setswana **government** test (49.9–58.2).
- In 14A the two heads differ by 4–7 F1 for in-language Setswana. For an unseen target they differ by only 1–2 F1: **guideline heads separate conventions for languages seen in training, not for a new target language.**

**Can the labels be fixed at the source? (Experiment 15: partly.)** Rule-based relabelling of the NCHLT Sepedi and Sesotho *training* labels: strip titles from PER spans, drop role-only PER spans and role phrases, drop generic institution ORG spans. 101-word lexicon (revised once; fingerprint `473a7ee55c`), 3 seeds, main-run Trainer, same sentences.

| Training data | Setswana news F1 | Pred / gold (news) | Setswana NCHLT F1 |
|---|---|---|---|
| Swahili alone | 80.0 | 1,532 / 1,327 | 62.9 |
| Sepedi original → relabelled | 65.7 → **73.9** (+7.9, +11.7, +5.2; Holm p .004) | 1,860 → 1,715 | 49.9 → **54.4** |
| Sesotho original → relabelled | 61.0 → 56.4 (+3.2, −15.3, −2.0) | 1,836 → 1,759 | 57.7 → 55.3 |

- **Sepedi gains 8.2 F1**, almost all in PER (66.8 → 84.3), and closes 58% of its 14.3-point gap to Swahili. Swahili is still 6.1 F1 better (p .008).
- **Dose-response.** An earlier 73-word version of the list (archived run) gave +6.1; the larger list removes more of these labels and helps more.
- **The pre-registered reverse check failed.** Relabelling also *raises* NCHLT Setswana F1, so the removed labels are not "the NCHLT guideline" that NCHLT Setswana shares; they behave like **inconsistent title/role annotation across NCHLT languages**.
- **Sesotho is inconclusive:** seed 42 collapsed to 39.0 F1 with both lexicons, so it is the seed, not the labels.

**Statement for the report.**

> H4 is not supported: Swahili and Chichewa are stronger Setswana sources than Sepedi and Sesotho, and the result is robust to equalising entity counts. An error analysis suggests that the Sotho-Tswana sources recognise Setswana entities well but carry over NCHLT annotation conventions, which costs precision. Relabelling titles, role nouns and generic institution nouns in the Sepedi training data recovers 8.2 F1 on Setswana news (58% of the deficit) and also helps on NCHLT Setswana, which points to inconsistent source annotation rather than a clean guideline difference. Routing the NCHLT data through its own guideline head does not remove this: joint Sepedi/Sesotho + Swahili models remain 6–9 F1 below Swahili alone, and their over-labelling persists through the news-guideline head. Whether a Sotho-Tswana source annotated like MasakhaNER would outperform Swahili therefore remains open; relabelling (Test 4) is the step that could answer it.

---

## The thread across all four hypotheses

**In this setup, which annotation conventions the source and target share decides transfer more than how related the languages are.** The evidence lines up across the research questions:

| Observation | Hypothesis it bears on | What it shows |
|---|---|---|
| Cross-corpus gap closes 54% under relaxed matching; errors are titles and institution nouns | H1 | The "domain" effect is mostly annotation scope and boundaries |
| Same-language cross-corpus text is as close as sister languages in the base model | H1 | Text domain is a small part of the gap |
| Weak transfer between isiZulu and isiXhosa inside NCHLT (46–52 F1 vs about 83 on news) | H1, H4 | NCHLT conventions differ even between its own languages |
| Large early few-shot gains for government sources | H3 | Consistent with quickly learning the target's conventions (interpretive) |
| Sepedi finds Setswana entities but over-labels | H4 | Relatedness helps recognition; annotation conventions cost precision |
| Same text, same encoder, different guideline head: 9.2 F1 lost on average (14A) | H1 | At least 44% of the cross-corpus gap is the guideline itself |
| Separate heads do not stop Sepedi data hurting Setswana (14B) | H4 | NCHLT conventions reach the shared encoder; a head-level fix is not enough |

This fits the literature review's prediction that "domain, annotation scheme and entity-string overlap move together" in this design. Tests 1–3 go a step further by separating annotation from text, and Experiment 14A measures the annotation part directly. 14B shows the limit: annotation effects can be measured at the output head, but they cannot be removed there.

## Limits to state in the report

- **One model** (AfroXLMR-base); results may differ for other encoders.
- **Seeds:** three for the main run; **one** for the Section 13 error analysis.
- **RQ2 has only six targets,** so exposure is confounded with cluster, fertility and corpus quality.
- **RQ4 confound:** source language and source corpus coincide perfectly for the Sotho-Tswana and distant-Bantu sources.
- **Automatic error categories** with most-frequent examples, not a manual review. A manual check of a sample would confirm the mechanisms.
- **The causal test of the annotation explanation (Test 4, relabelling) is designed but not run.** It needs about 10–12 person-hours with two Setswana-literate annotators.
- **Experiment 14 design limits:** one adapter on the final layer only; a hand-written training loop without gradient clipping (the main run clips at 1.0), so joint-vs-single comparisons mix two changes; 3 seeds and no formal significance test (per-seed signs reported). The guideline share is a lower bound.
- **Exploratory analyses:** the regression variants in 10.8, the representation and error analyses, and Experiment 14 were chosen after seeing the main results. Report them as exploratory, separate from the pre-specified contrasts in 10.6.
