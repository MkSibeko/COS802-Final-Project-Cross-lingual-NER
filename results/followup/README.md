# Follow-up results (run 12–13 Nov 2026, after the report's scope was fixed)

These runs are **not in the report**. The report covers RQ1–RQ4 only and describes these experiments as future work. They are recorded here so the numbers are not lost. The raw cell outputs are in `logs/`.

Setting: the Colab notebook on a T4 GPU, AfroXLMR-base, the deduplicated (v2) data and the main run's settings.

## 1. Experiment 14 v2: is head switching a valid measurement? (positive and null controls)

**Design.** Setswana news training data (MasakhaNER) is split into two disjoint halves of 1,740 sentences.
- Head "orig" is trained on gold labels.
- Head "synthetic" is trained on labels changed by a known rule, `per_drop_first`: the first token of every PER span is dropped.

Both heads share one encoder. Switching heads at test time should recover the known effect of the rule. The *known* effect is the difference between the gold-trained model and a model trained on the synthetic labels alone.

The null control trains two heads on two samples of the **same** corpus with nothing different. It is 18 runs: 6 corpora × 3 seeds.

| Strict F1, Setswana news, 3 seeds | Estimate [95% CI] |
|---|---|
| Effect recovered by switching heads | **23.0** [20.7, 25.4] |
| Known effect | 23.2 [20.9, 25.5] |
| Recovered − known | −0.2 [−0.6, 0.2] |
| Recovered ÷ known | **0.99** [0.97, 1.01] |
| Null control (two heads, no difference) | 0.5 [0.1, 0.9] |
| Relaxed F1 effect (the rule only moves boundaries) | 0.0 [−0.3, 0.4] |

Per seed, the recovered effect was 22.78, 22.86 and 23.29 F1. **Verdict printed by the notebook:** "PASS: head switching recovers the known effect (99%)".

What this shows: on this corpus and for a boundary-only convention, the head-switch effect measures a convention difference without detectable bias, and two identical heads differ by only about 0.5 F1. It is one synthetic rule on one corpus, so it validates the tool, not every use of it.

**Not yet read:** block 14v2.A (27 runs: joint NCHLT + news models and matched single-corpus baselines) and its decomposition analysis. The runtime was still training them when the browser link dropped on 13 Nov. Every finished run is saved to Drive under `COS802_project_backup/v2_deduplicated/results/guideline_heads_v2/runs/`. Re-running cells 14v2.1 to 14v2.A-analysis restores the finished runs from Drive and trains only the missing ones.

## 2. Analysis 4: relaxed and type-insensitive scoring (no new models)

These are seed-13 predictions from Test 1. The gap is between the in-corpus news model and the same-language government (NCHLT) model, both tested on news. "Share closed" is the fraction of the strict gap that disappears under relaxed (overlap) scoring. It is computed from the per-metric F1 table in `logs/exp14_alt_analyses_4_and_2_run.log`.

| News test | In-corpus strict / relaxed | NCHLT model strict / relaxed | Strict gap | Relaxed gap | Share closed |
|---|---|---|---|---|---|
| isiZulu | 86.6 / 90.3 | 47.4 / 77.6 | 39.2 | 12.7 | about 68% |
| isiXhosa | 87.9 / 91.7 | 66.6 / 82.1 | 21.3 | 9.6 | about 55% |
| Setswana | 88.2 / 93.0 | 73.2 / 84.1 | 15.1 [13.0, 17.2] | 8.9 [7.5, 10.3] | 41% [32, 49] |

Reading: a large part of the government-to-news gap is about span boundaries, not about finding the entities at all. Boundaries are where the two annotation guidelines differ, for example titles inside PER spans. It is largest for isiZulu.

## 3. Analysis 2: converting predictions to the news convention

Frozen rules R1–R3 (trim titles from PER, drop role phrases, drop generic institution ORG spans) are applied to the NCHLT-trained models' predictions on news. The vetted lexicon is `473a7ee55c`.

| Comparison (strict F1) | Before | After | Gain [95% CI] |
|---|---|---|---|
| Setswana news, NCHLT tsn source | 73.2 | 76.5 | +3.3 [2.4, 4.2] |
| Setswana news, NCHLT nso (Sepedi) source | 66.0 | 71.7 | +5.7 [4.8, 6.7] |
| isiXhosa news, NCHLT xho source | 66.6 | 66.6 | 0.0 |
| isiZulu news, NCHLT zul source | 47.4 | 47.4 | 0.0 |

Pooled over the two RQ1/RQ4 Setswana comparisons, the conversion closes 41% [33, 50] of the strict gap to Swahili. Over the three same-language comparisons it closes only 4% [3, 5], because the Nguni rules almost never fire.

**Caveat (printed by the notebook):** these rules were not checked on dev data and were designed after inspecting test errors, so the gains are an optimistic, upper-bound estimate. Only seed 13 was used.

## Files

| File | Content |
|---|---|
| `logs/colab_setup_run.log` | Setup cells 7–46 (data download, deduplication, splits) |
| `logs/exp14_v2_positive_control_run.log` | 14v2.1–14v2.P: setup and positive-control training |
| `logs/exp14_v2_validity_analysis_run.log` | 14v2.P-analysis: validity verdict |
| `logs/exp14_alt_analyses_4_and_2_run.log` | AltA cells: Analyses 4 and 2 |
