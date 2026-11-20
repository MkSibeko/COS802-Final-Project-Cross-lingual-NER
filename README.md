# Language, Domain, or Pretraining Exposure? Cross-Lingual NER for South African Bantu Languages

**COS802 Natural Language Processing project, University of Pretoria, 2026.** Mpendulo Sibeko (19144832).

| File | Content |
|---|---|
| [`19144832_Sibeko_COS802_Final_Report.pdf`](19144832_Sibeko_COS802_Final_Report.pdf) | Final report (8 pages, SIGKDD Explorations format) |
| [`19144832_Sibeko_COS802_Presentation.pptx`](19144832_Sibeko_COS802_Presentation.pptx) | Presentation slides with speaker notes |
| [`code/COS802_Experiment.ipynb`](code/COS802_Experiment.ipynb) | The complete experiment: data download, label harmonisation, deduplication and splits, fine-tuning AfroXLMR-base, evaluation, statistics and plots |
| `code/figures/` | Scripts that draw the report's figures |
| [`code/requirements.txt`](code/requirements.txt) | Python packages needed by the notebook and scripts |

## Running the code

The notebook runs in Google Colab on a GPU runtime (T4). Run it from top to bottom; it downloads NCHLT NER (SADiLaR, CC BY 2.5 ZA) and MasakhaNER 2.0 (CC BY-NC 4.0), trains every model and writes the results, which are mirrored to Google Drive. The datasets are not included in this repository.

The report's figures can be redrawn locally:

```bash
cd code && python figures/make_heatmap.py && python figures/make_figures.py
```

To install the Python packages outside Colab:

```bash
pip install -r code/requirements.txt
```
