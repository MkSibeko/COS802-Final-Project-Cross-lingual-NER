# COS802 results captured from the executed Colab notebook (11 Nov 2026)

Read from the saved outputs of `notebooks/COS802_Experiment.ipynb`, as executed in Google Colab.
Cell numbers are positions in that notebook (0-based). All F1 values are entity-level micro-F1 on PER/LOC/ORG,
means over seeds 13, 42 and 2026 unless stated.

## Data (section 6.0, cells 39 and 41)

Duplicates detected by exact match on lower-cased, whitespace-normalised token sequences.

| Corpus | Before | After | Removed |
|---|---|---|---|
| NCHLT zul / xho / ssw / nso / sot / tsn | 10,955 / 6,283 / 10,797 / 7,116 / 9,471 / 7,943 | 10,851 / 6,174 / 10,512 / 6,980 / 9,358 / 7,768 | 104 / 109 / 285 / 136 / 113 / 175 (0.9–2.6%) |
| MasakhaNER train zul / xho / tsn / swa / nya | 5,848 / 5,718 / 3,489 / 6,593 / 6,250 | 5,843 / 5,249 / 3,481 / 6,552 / 6,161 | 5 / 469 / 8 / 41 / 89 |
| MasakhaNER dev zul / xho / tsn / swa / nya | 836 / 817 / 499 / 942 / 893 | 836 / 817 / 498 / 937 / 885 | 0 / 0 / 1 / 5 / 8 |

NCHLT splits (train/dev/test, after deduplication, no sentence shared between splits): zul 8,680/1,085/1,086; xho 4,939/617/618; ssw 8,409/1,051/1,052; nso 5,584/698/698; sot 7,486/935/937; tsn 6,214/776/778.

Design (cell 48): 11 sources x 3 seeds = 33 zero-shot training runs; 99 source-test pairs per seed.

## RQ1: relatedness vs domain (corpus) match (cell 58; transfer pairs only)

| Relatedness | Same corpus | Pairs | F1 | TR |
|---|---|---|---|---|
| Same language | no | 18 | 60.96 | 0.73 |
| Same cluster | no | 36 | 56.27 | 0.68 |
| Same cluster | yes | 42 | 59.00 | 0.76 |
| Other Southern Bantu | no | 54 | 41.36 | 0.51 |
| Other Southern Bantu | yes | 66 | 43.52 | 0.56 |
| Other Bantu | no | 36 | 36.88 | 0.49 |
| Other Bantu | yes | 18 | 46.69 | 0.53 |

(Pairs count seed-level rows: 3 per source-test pair.)

## RQ2: seen vs unseen targets (cell 60)

| Target | Relatedness | F1 | TR | Pairs |
|---|---|---|---|---|
| Unseen (0) | other Bantu | 55.09 | 0.66 | 24 |
| Unseen | other Southern Bantu | 50.78 | 0.61 | 57 |
| Unseen | same cluster | 57.80 | 0.71 | 33 |
| Unseen | same language | 66.95 | 0.80 | 6 |
| Seen (1) | other Bantu | 28.19 | 0.38 | 30 |
| Seen | other Southern Bantu | 35.10 | 0.47 | 63 |
| Seen | same cluster | 57.70 | 0.73 | 45 |
| Seen | same language | 57.97 | 0.69 | 12 |

## RQ3: few-shot (cell 62)

| Target | Source | k=0 | k=100 | k=500 | In-language | Gap closure at 100 / 500 |
|---|---|---|---|---|---|---|
| tsn news | NCHLT nso | 65.706 | 77.760 | 85.052 | 89.024 | 0.517 / 0.830 |
| tsn news | NCHLT tsn | 70.594 | 77.028 | 84.003 | 89.024 | 0.349 / 0.728 |
| xho news | MasakhaNER zul | 82.744 | 82.694 | 85.796 | 88.094 | −0.009 / 0.570 |
| xho news | NCHLT xho | 70.031 | 75.771 | 83.568 | 88.094 | 0.318 / 0.749 |
| zul news | MasakhaNER xho | 82.390 | 83.852 | 86.237 | 87.632 | 0.279 / 0.734 |
| zul news | NCHLT zul | 50.350 | 75.064 | 83.502 | 87.632 | 0.663 / 0.889 |

## RQ4: sources for Setswana (cell 64; mean, SD over seeds, TR)

News test (MasakhaNER tsn): in-language 89.02 (0.14); Swahili 80.01 (2.56); Chichewa 76.33 (2.21); NCHLT tsn 70.59 (2.99); NCHLT nso 65.71 (1.13); MasakhaNER xho 65.59 (1.26); NCHLT ssw 63.03 (1.94); MasakhaNER zul 63.01 (1.82); NCHLT sot 61.05 (5.84); NCHLT xho 57.22 (4.19); NCHLT zul 49.03 (3.97).

Government test (NCHLT tsn): in-language 78.59 (2.05); MasakhaNER tsn 63.31 (0.61); Swahili 62.88 (2.62); NCHLT sot 57.65 (2.36); NCHLT xho 57.65 (3.27); MasakhaNER xho 56.06 (1.39); Chichewa 51.90 (0.74); NCHLT nso 49.86 (1.73); NCHLT ssw 49.86 (1.39); MasakhaNER zul 46.77 (2.55); NCHLT zul 40.40 (0.87).

## Statistics (cells 67 and 68)

Paired bootstrap, 1,000 resamples, seed-averaged F1; Holm over the five contrasts.

| Contrast | Diff | Per seed (13, 42, 2026) | p one-sided | p two-sided | Holm one-sided | Holm two-sided |
|---|---|---|---|---|---|---|
| RQ1 zul news: sister news vs same-language gov | +32.04 | 37.2, 31.4, 27.6 | .001 | .002 | .005 | .01 |
| RQ1 xho news: sister news vs same-language gov | +12.71 | 12.7, 12.7, 12.8 | .001 | .002 | .005 | .01 |
| RQ4 tsn news: Sepedi vs Swahili | −14.31 | −14.6, −12.7, −15.5 | 1.000 | .002 | 1.000 | .01 |
| RQ4 tsn news: Sesotho vs Swahili | −18.96 | −16.5, −22.9, −17.4 | 1.000 | .002 | 1.000 | .01 |
| RQ4 tsn gov: Sepedi vs Swahili | −13.02 | −12.8, −11.3, −14.9 | 1.000 | .002 | 1.000 | .01 |

Mixed model (REML; 90 seed-averaged transfer pairs; random intercept for 6 target languages; "MLE may be on the boundary" warning):
transfer_ratio ~ rel_score * domain_match + target_exposure + entity_overlap.
Intercept 0.490 (SE 0.067); rel_score 0.101 (SE 0.025, z 4.11, p < .001, 95% CI 0.053–0.149); domain_match 0.023 (p = .705); rel_score:domain_match 0.012 (p = .788); target_exposure −0.076 (SE 0.083, p = .356); entity_overlap 0.312 (p = .610); group variance 0.008.

## Robustness checks (cells 71, 72, 74)

ML re-fits (cell 71):
- M0, same formula: rel 0.098 (p < .001), domain 0.022 (p = .712), exposure −0.078 (p = .218), LL 41.1, AIC −66.3.
- M1, corpus terms: rel 0.112 (p < .001), src_news 0.016 (p = .700), test_news 0.014 (p = .776), src_news:test_news 0.113 (p = .119), exposure −0.085 (p = .205), LL 44.6, AIC −71.2.
- M2, M1 + fertility gap: rel 0.078 (p = .001), src_news:test_news 0.135 (p = .049), exposure −0.091 (p = .192), fert_gap −0.177 (p = .001), LL 49.4, AIC −78.8.
- Fertility per corpus: swa 1.51, MasakhaNER tsn 1.77, sot 1.82, NCHLT tsn 1.85, nso 1.87, nya 2.25, MasakhaNER zul 2.43, MasakhaNER xho 2.48, NCHLT zul 2.69, NCHLT xho 2.75, ssw 2.78.

Truncation at 128 subwords (cell 72): gold entities lost 0.58–2.79% on NCHLT test sets (tsn highest, 14 of 502), 0% on MasakhaNER.

Entity-capped RQ4 re-run (cell 74; each source trained on about 2,500 PER/LOC/ORG spans; per seed 13, 42, 2026):

| Source | Sentences used | Setswana news | Setswana gov |
|---|---|---|---|
| Swahili | 1,342–1,377 | 77.2, 79.3, 78.9 (mean 78.5) | 57.9, 63.9, 61.7 (61.2) |
| Chichewa | 1,558–1,572 | 76.9, 75.3, 67.3 (73.2) | 55.1, 52.0, 39.8 (49.0) |
| Sepedi | 2,431–2,527 | 65.3, 65.6, 61.7 (64.2) | 48.8, 51.3, 45.9 (48.7) |
| Sesotho | 2,968–3,100 | 62.2, 59.7, 62.3 (61.4) | 56.2, 51.9, 55.7 (54.6) |
| isiXhosa (NCHLT) | 4,683–4,763 | 61.0, 60.6, 60.0 (60.5) | 59.4, 56.8, 58.0 (58.1) |

Swahili minus Sepedi: news 14.3 F1, government 12.5 F1.

## Published baselines (cell 76)

| Target | Published best source (F1) | English | Published in-language | Ours: best source (F1) | Ours in-language | Ours − published |
|---|---|---|---|---|---|---|
| zul | xho (82.1) | 44.7 | 88.6 | MasakhaNER xho (82.39) | 87.63 | +0.29 |
| xho | zul (83.7) | 24.5 | 90.8 | MasakhaNER zul (82.74) | 88.09 | −0.96 |
| tsn | deu (73.3) | 65.8 | 88.7 | MasakhaNER swa (80.01) | 89.02 | +6.71 |

## Not in the saved outputs

The full 99-pair table of means and SDs is truncated in the notebook output (cell 55 shows only its head and tail). Producing it needs a new cell run against the saved `results.csv` on Drive.
