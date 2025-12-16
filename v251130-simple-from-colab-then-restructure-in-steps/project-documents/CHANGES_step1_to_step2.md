# Changes: step1 → step2

Generated: 2025-12-16

This document shows only what changed between `step1` and `step2`:
(1) configuring pandas display,
(2) performing HTTP downloads of CSV data,
(3) loading and exploring the dataset, and
(4) running in-memory preprocessing.

```
step[1->2]/
├─ config.py  [modified]
│  ├─ + import pandas as pd  [Added: `pandas` imported to allow configuration of display options used by data-printing and exploration; no network/file IO by itself.]
│  ├─ + pd.set_option('display.max_columns', None)  [Added: configures pandas display to show all columns when printing DataFrames for inspection; no side-effect on disk.]
│  ├─ + pd.set_option('display.max_rows', 100)  [Added: limits printed rows to 100 for console output; runtime display-only setting.]
│  └─ + ENABLE_DATA_PROCESSING = True  [Added: feature flag controlling whether Step 2 runs download/load/preprocess; changes runtime control flow in `main.py`.]

├─ data.py  [added]
│  ├─ def download_data_file(file_name, data_url)  [New: attempts HTTP GET to `data_url`, writes bytes to `file_name` if missing; prints success or error; network + disk-write side-effects when invoked.]
│  ├─ def download_required_files()  [New: convenience wrapper calling `download_data_file()` for configured constants; invoked by `main` to ensure local data presence.]
│  ├─ def load_and_explore_data(csv_path)  [New: reads CSV into `pandas.DataFrame` (`pd.read_csv`), prints shape/head/dtypes/describe; disk-read + memory allocation side-effects.]
│  └─ def preprocess_data(df)  [New: performs in-memory cleaning (trim column names, detect empty columns, report missing values) and returns a cleaned DataFrame; no disk writes here.]

├─ main.py  [modified]
│  ├─ - previous `test_infrastructure()` focus remains available in docs but is replaced by a new `test_data_module()` in Step 2  [Change: main now tests the data module rather than only infra; imports and runtime flow changed accordingly.]
│  ├─ + imports: DATA_CSV_FILE, ENABLE_DATA_PROCESSING from config  [Modified imports: `ENABLE_DATA_PROCESSING` added to control new data steps; `DATA_CSV_FILE` used for path passed to data functions.]
│  ├─ + imports: data  [New: `data` module imported so main can call download/load/preprocess functions.]
│  └─ def test_data_module():
│     ├─ print_section("STEP 2: DATA MODULE TEST")  [New: header for the data test sequence.]
│     ├─ clean_outputs()  [Reused: called to ensure `outputs/` is clean before data processing — destructive on-disk effect for outputs/.]
│     ├─ if ENABLE_DATA_PROCESSING: (guard)
│     │  ├─ data.download_required_files()  [Invokes network download if CSV missing; writes CSV to disk.]
│     │  ├─ df = data.load_and_explore_data(DATA_CSV_FILE)  [Loads CSV from disk into memory and prints diagnostics.]
│     │  ├─ df_clean = data.preprocess_data(df)  [Runs in-memory preprocessing and returns cleaned DataFrame.]
│     │  └─ returns df_clean  [Makes cleaned DataFrame available to tests or callers.]
│     └─ if __name__ == '__main__': test_data_module()  [Entrypoint runs new data test when executed directly.]

└─ utils.py  [unchanged]
   [Note: utility functions (`clean_outputs`, `print_section`, `zip_all_outputs`) remain the same across step1 and step2; they provide the same IO behaviors used by both steps.]
```
