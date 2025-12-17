# Changes: Step2 → Step3 (delta-only tree)

Generated from a side-by-side comparison of `step2` and `step3` on 2025-12-17. The single ASCII tree below only lists the files and behaviors that changed, with bracketed runtime notes. A short summary of key side-effects appears first (per the prompt's requirement to place the summary before the tree).

## Summary — most important new side-effects introduced in Step 3

- Added `analysis.py`, which performs in-memory EDA and time-series aggregation and prints summaries without writing new files.
- `config.py` now exposes `ENABLE_EXPLORATORY_ANALYSIS` and `ENABLE_TIME_SERIES`, gating the new analysis branches in `main.py` without additional IO.
- `main.py` was repurposed into `test_analysis_module()`, which still calls `clean_outputs()` (destructive on `outputs/`) but now drives the new analysis routines after preprocessing.
- The existing data download/load/preprocess helpers remain, but their outputs now feed the new analysis module instead of ending after preprocessing.

- step[2→3]/ — Delta-only tree highlighting what changed when advancing from step2 to step3.
	- `+ analysis.py` — Added module defining `exploratory_data_analysis(df_clean)` and `aggregate_time_series(df_clean)` so Step 3 can print grouped summaries and yearly stats without writing files.
		- `imports: numpy as np, pandas as pd, print_section` — Provides numeric and aggregation helpers for EDA and time-series operations; import has no side-effects.
		- `def exploratory_data_analysis(df_clean: pd.DataFrame):`
			- Signature: exploratory_data_analysis(df_clean)  [Purpose: print grouped summaries and top model/region reports; operates in-memory.]
			- Behavior: compute groupby aggregations (by Model, Region, Year), print top results and descriptive stats  [Creates intermediate DataFrames in memory and prints results to stdout; no files written by default.]
			- Return: None (side-effect: console prints only).
		- `def aggregate_time_series(df_clean: pd.DataFrame):`
			- Signature: aggregate_time_series(df_clean) -> tuple  [Purpose: aggregate sales by Year and produce arrays for modeling and reporting; returns (df_yearly, ts_data, ts_years, df_model_yearly, df_region_yearly).]
			- Behavior: df_yearly = df_clean.groupby('Year').agg({'Sales_Volume':'sum'}).reset_index()  [In-memory aggregation and sorting; prints summary statistics such as count, range, average, peak; computes YoY growth column.]
			- Additional steps: compute ts_data = df_yearly['Total_Sales'].values and groupby Model/Region yearly frames  [Extracts numpy arrays for downstream modeling and builds auxiliary DataFrames; no disk IO.]
			- Return: in-memory tuple of DataFrames/arrays for caller; no files written.
	- `config.py` — Same file as Step 2 but with new runtime switches to control the added analysis branches.
		- `+ ENABLE_EXPLORATORY_ANALYSIS = True` — New flag that turns on the EDA call path; no disk or network activity when read.
		- `+ ENABLE_TIME_SERIES = True` — New flag that allows aggregation of yearly totals and extraction of numpy arrays; no IO.
	- `main.py` — Modified into `test_analysis_module()` that still cleans `outputs/` and runs download/load/preprocess but now calls the added analysis functions before returning results.
		- `+ If ENABLE_EXPLORATORY_ANALYSIS: analysis.exploratory_data_analysis(df_clean)` — New branch printing model/region/year summaries using cleaned DataFrame; purely console output.
		- `+ If ENABLE_TIME_SERIES: analysis.aggregate_time_series(df_clean)` — New branch computing totals, YoY growth, and arrays; prints stats and returns multiple in-memory DataFrames/arrays.
	- `data.py` — Behavior unchanged, but its cleaned DataFrame now flows into the new analysis module; still downloads (network) and reads CSV (disk), then preprocesses in memory.
	- `utils.py` — No changes: `clean_outputs()` continues to delete files/directories under `outputs/`, while `print_section()` and `zip_all_outputs()` remain helpers for Step 3's tests.

Legend: `+` indicates new or expanded behavior in Step 3, while unchanged files are described with how their existing behavior now feeds into the new analysis flow.
