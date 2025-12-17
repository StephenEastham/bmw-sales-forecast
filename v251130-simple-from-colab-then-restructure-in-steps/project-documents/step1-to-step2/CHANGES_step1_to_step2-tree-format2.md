# Changes: step1 → step2

Generated: 2025-12-16

This document highlights only the delta between `step1` and `step2`. The nested bullet layout mirrors `CHANGES_step2_to_step3-format2.md`, so the runtime notes remain visible while following a consistent format.

## Summary — key deltas observed when moving to Step 2

- Step 2 now imports `pandas`, configures its display options, and introduces the `ENABLE_DATA_PROCESSING` flag before running any helpers.
- The new `data.py` module downloads the CSV, explores it with pandas, and performs in-memory preprocessing, all while keeping IO localized to download, read, and cleanup steps.
- `main.py` now orchestrates the data workflow: it downloads (if needed), loads, and preprocesses the dataset whenever `ENABLE_DATA_PROCESSING` is true and still relies on `clean_outputs()` to reset `outputs/` first.
- The utility helpers (`clean_outputs`, `print_section`, `zip_all_outputs`) remain unchanged and continue to support both steps without additional modification.

- `step[1->2]/`  [Delta-only tree following the nested bullet format]
   - `config.py` — Modified to load pandas, adjust display, and expose the new feature flag.
      - `+ import pandas as pd` — Enables display configuration and data exploration without IO by itself.
      - `+ pd.set_option('display.max_columns', None)` — Ensures pandas prints every column when logging DataFrames.
      - `+ pd.set_option('display.max_rows', 100)` — Limits console output to 100 rows for clarity.
      - `+ ENABLE_DATA_PROCESSING = True` — Controls whether `test_data_module()` runs the new download/load/preprocess sequence.
   - `data.py` — Added module dedicated to CSV download and preprocessing.
      - `download_data_file(file_name, data_url)` — Performs HTTP GET when the file is missing, writes bytes to disk under `file_name`, prints success/failure, and handles network exceptions.
      - `download_required_files()` — Calls `download_data_file(DATA_CSV_FILE, DATA_CSV_URL)` so other modules can ensure the dataset exists locally.
      - `load_and_explore_data(csv_path)` — Reads the CSV with `pd.read_csv`, prints shape/head/dtypes/describe stats, and returns the DataFrame (disk read + console output).
      - `preprocess_data(df)` — Operates in memory: copies the DataFrame, trims column whitespace, reports empty/missing columns, and returns the cleaned DataFrame; no writes.
   - `main.py` — Reimagined around the new data test.
      - Imports now include `DATA_CSV_FILE`, `ENABLE_DATA_PROCESSING`, and the `data` module so the workflow can access required constants and helpers.
      - `test_data_module()` prints its header, runs `clean_outputs()` (destructive), and, if the flag is true, executes `data.download_required_files()`, `data.load_and_explore_data(DATA_CSV_FILE)`, and `data.preprocess_data(df)`, returning the cleaned DataFrame at the end.
   - `utils.py` — No behavioral changes; `clean_outputs`, `print_section`, and `zip_all_outputs` continue to provide the same disk-side effects described in Step 1.

Legend: `+` marks Step 2 additions, while each bullet keeps the new runtime note tied to the node it describes.
