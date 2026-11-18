Figures of the report. Regenerate them from report_final/:

  python figures/make_heatmap.py    -> zero_shot_heatmap.pdf/.png      (Figure 1, zero-shot F1 for all pairs)
  python figures/make_figures.py    -> rq1_relatedness_corpus.pdf/.png (RQ1: transfer ratio by relatedness x corpus)
                                       rq3_fewshot_curves.pdf/.png     (RQ3: few-shot learning curves)
                                       rq4_setswana_sources.pdf/.png   (RQ4: every source on the two Setswana tests)
                                       fertility_by_corpus.pdf/.png    (data: tokenizer fertility per corpus)

All values come from the executed Colab notebook, as recorded in results/main_results_RQ1-RQ4.md
(cells 56, 58, 62, 64 and 71). Colours follow the presentation: Nguni blue, Sotho-Tswana orange,
other Bantu green, comparison grey.
