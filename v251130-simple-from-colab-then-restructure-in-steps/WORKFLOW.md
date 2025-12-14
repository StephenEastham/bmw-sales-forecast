**Project Workflow & Folder Guide**

This document explains the purpose of files and folders in this directory, how they relate, and how to run the project as a reproducible workflow.

**Overview**: This repository snapshot contains a stepwise data-analysis project that started in Colab and was refactored into discrete development steps. Each `stepN/` folder contains the working code for that step. The `generate-notebook*` folders contain helper scripts that build combined Jupyter notebooks and HTML outputs for sharing.

**Top-level files**
- `bmw_v3_simple-from-colab.py`: a compact script version of the analysis (legacy/quick-run).
- `BMW-sales-data-2010-2024.csv`: dataset (copy used across steps).

**Key folders**
- `step1/` ... `step7/`: progressive iterations of the analysis. Each step typically contains:
  - `main.py` — runner script for that step (loads data, calls modules).
  - `config.py` — constants and feature flags (paths, toggles for plotting/reporting).
  - `data.py`, `analysis.py`, `visualization.py`, `reporting.py`, `aggregator.py`, `forecasting.py` — modular code split across responsibilities.
  - `outputs/` — runtime outputs (PNGs, HTML, text reports). These are produced when you run `main.py`.

- `generate-notebook/`, `generate-notebook-for-colab/`, `generate-notebook-for-colab-v3/`, `generate-notebook-for-colab-v4/`:
  - Contain the `make_notebook*.py` scripts that assemble the project modules into a single Jupyter notebook (for sharing or running in Colab).
  - Also contain copies of the dataset and previously generated combined notebooks and outputs.

- `evolution/`: documentation and diagrams that track how the codebase evolved (useful for project history or presentation).

**How the pieces relate**
- The `stepN/` folders are sequential snapshots — `step7/` is the latest development stage in this tree.
- The `generate-notebook*` folders take the modular source files and produce a self-contained notebook (`step7-combined-*.ipynb`) and aggregated HTML in `outputs/` for sharing. These tools are convenience utilities for packaging the code for Colab or other notebook environments.
- `outputs/` in each step holds results produced by running `main.py` (plots, dashboards, reports, `ANALYSIS_SUMMARY.txt`, aggregator HTML).

**Recommended workflow (run locally)**

1. Pick the step you want to run (usually `step7/` for latest work).

2. Install minimal Python requirements (use a venv):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt  # if present; otherwise install: requests pandas matplotlib seaborn plotly
```

3. Run the step's main script (example for `step7`):

```powershell
cd v251130-simple-from-colab-then-restructure-in-steps\step7
python main.py
```

This will:
- download the CSV (if enabled in `config.py`),
- run preprocessing and analysis,
- save static visualizations to `outputs/`,
- create interactive HTML dashboards (if dependencies present),
- run reporting and aggregator to produce `07_all_outputs.html` and zip archive.

4. View results:
- Open files in `step7\outputs\` with your browser (e.g., `07_all_outputs.html`, `05_interactive_dashboard.html`, `08_sales_forecast.png`).

**How to produce a combined notebook for Colab**

Use the `generate-notebook-for-colab-v4` folder (example):

```powershell
cd v251130-simple-from-colab-then-restructure-in-steps\generate-notebook-for-colab-v4
python make_notebook-v4.py --src ..\step7 --output step7-combined.ipynb
# The script writes a combined notebook you can open locally or upload to Colab
```

**Quick notes & troubleshooting**
- If plots don’t appear, confirm headless backend is set in `config.py` (matplotlib `Agg`) or run in an environment that supports GUI rendering.
- If downloads fail, check `DATA_CSV_URL` in `config.py` and network access.
- Use `outputs/` as the canonical location for generated files — aggregator and reporting expect outputs there.
- If a module changes, re-run `main.py` in the step folder to refresh outputs.

**Useful commands**
- Run a single step: `python step7\main.py` (from the project root)
- Combine code into notebook: run the `make_notebook-*.py` in the corresponding `generate-notebook*` folder as shown above.
- Serve outputs folder for local viewing:

```powershell
cd v251130-simple-from-colab-then-restructure-in-steps\step7\outputs
python -m http.server 8000
# Open http://localhost:8000/07_all_outputs.html
```

**Where to look for the latest work**
- `step7/` is the most recent functional iteration and contains `forecasting.py` and aggregator utilities — start here for analysis and forecasting.

If you want, I can:
- Add a `requirements.txt` capturing used packages, or
- Create a short runnable `README.md` inside `step7/` with step-specific commands and minimal env instructions.

---

Generated on: 2025-12-14
