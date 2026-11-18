# Notebook

`COS802_Experiment.ipynb` is the complete experiment: setup, data download (NCHLT from SADiLaR, MasakhaNER 2.0 from Hugging Face), label harmonisation, EDA, deduplication and splits, training, evaluation, statistics and plots, followed by follow-up sections 12–15.

- The notebook was developed and run in Google Colab; this copy covers sections 1–15 (setup, main run, analysis and follow-up checks).
- Runs on a Colab T4 GPU. Results are mirrored to Drive (`COS802_project_backup/v2_deduplicated/results/`).
- After a runtime reset, run cells 4–46 (configuration, Drive mount, data, splits, model utilities), then cell 52 (restore results) before any analysis.
- Datasets are downloaded by the notebook and are not stored in this repository. NCHLT NER is CC BY 2.5 ZA; MasakhaNER 2.0 is CC BY-NC 4.0.
