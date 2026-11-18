# Results

| File | What it holds |
|---|---|
| [`main_results_RQ1-RQ4.md`](main_results_RQ1-RQ4.md) | **Source of every number in the report and the deck.** Verified outputs of the executed Colab notebook: data and deduplication, RQ1–RQ4 tables, bootstrap contrasts with Holm, mixed models, robustness checks and published baselines. |
| [`results_vs_hypotheses.md`](results_vs_hypotheses.md) | A working note mapping results to H1–H4. It is older than the final report; where they differ, the report and `main_results_RQ1-RQ4.md` win. |
| [`followup/`](followup/README.md) | Follow-up runs from 12–13 Nov that are **not in the report**: the Experiment 14 v2 validity test (head switching recovers 99% of a known effect) and Analyses 4 and 2 (relaxed scoring, prediction conversion). The raw logs are included. |
| `figures/notebook_exports/` | Figures exported from the notebook, as drawn there. The report figures are redrawn by `report_final/figures/*.py`. |

## Headline results (AfroXLMR-base, 3 seeds, entity-level F1 on PER/LOC/ORG)

| Hypothesis | Verdict | Key number |
|---|---|---|
| H1: related sources transfer better, but domain match may override | Supported, with exceptions | +0.10 transfer ratio per relatedness step (p < .001). Sister language from the same corpus beats the same language from the other corpus by +32.0 F1 (isiZulu news) and +12.7 F1 (isiXhosa news), both with Holm p = .005. |
| H2: seen targets transfer better | Not supported (inconclusive) | Exposure p = .19 to .36, confounded with cluster and fertility |
| H3: target data narrows gaps | Supported | 500 target sentences close 57–89% of every gap |
| H4: Sepedi and Sesotho beat Swahili as Setswana sources | Rejected (reversed) | Swahili is ahead by 13.0–19.0 F1 (two-sided Holm p = .01), and the gap is unchanged with equal entity counts |

The raw per-run CSVs (`results.csv`, per-sentence counts) live on Google Drive under `COS802_project_backup/v2_deduplicated/results/`. They are not in this repository.
