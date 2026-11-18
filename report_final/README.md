# Final report

`19144832_Sibeko_COS802_Final_Report.pdf` is the final report: 8 pages including references, in SIGKDD Explorations format. `main.pdf` is the same document as built from the sources.

Build:

```bash
cd report_final && latexmk -pdf main.tex
```

| Path | Content |
|---|---|
| `main.tex` | Preamble, title, author and section order |
| `sections/` | One file per section, from the abstract (`00`) to the acknowledgements (`10`) |
| `references.bib` | Bibliography (`abbrv` style) |
| `sigkddExp.cls` | SIGKDD Explorations class |
| `figures/` | Figures, and the scripts that draw them from the verified results in `results/main_results_RQ1-RQ4.md` |
