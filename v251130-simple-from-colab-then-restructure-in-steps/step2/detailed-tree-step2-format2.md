```markdown
# Step 2 — Step-by-step tree (nested bullet format)

This file mirrors the new nested bullet summaries so the behavior notes remain clear while matching `CHANGES_step2_to_step3.md`.

## Summary — key runtime flow when running `step2/main.py`

- Importing `config.py` resolves `PROJECT_ROOT`, derives `OUTPUT_DIR`, and immediately calls `mkdir(parents=True, exist_ok=True)` so the folder exists before any helpers run.
- `clean_outputs()` runs before the data work begins and wipes every file/directory from `outputs/`, ensuring a clean workspace.
- The data step downloads the CSV if missing, reads it into pandas for exploration, and then preprocesses it in memory before returning a cleaned DataFrame.
- After preprocessing, downstream helpers can still zip `outputs/` if desired, but the core behavior is in-memory only; network and disk activity are limited to download, read, and clean-up.

- `step2/` — Files and runtimes
   - `BMW-sales-data-2010-2024.csv` — Local dataset that exists once `data.download_data_file()` writes it; Step 2 reads it if present but does not create it unless the download helper runs.
   - `config.py` — Defines constants and display settings.
      - Import-time sequence: compute `PROJECT_ROOT`, set `OUTPUT_DIR`, and create the folder via `mkdir(parents=True, exist_ok=True)` so later helpers have a writable directory.
      - `out_path(name: str)` — Builds `OUTPUT_DIR / name` paths for artifacts.
      - pandas display options, `DATA_CSV_URL`, `DATA_CSV_FILE`, and `ENABLE_DATA_PROCESSING` control exploration behavior and gate the data test; none trigger IO by themselves.
   - `utils.py` — Same helper trio as other steps; `clean_outputs()` rewrites outputs, `print_section` logs headers, and `zip_all_outputs()` optionally compresses matching artifacts.
   - `data.py` — Handles download, loading, and preprocessing.
      - `download_data_file()` performs HTTP GET when the CSV is missing, writes bytes to disk, and logs results.
      - `load_and_explore_data()` reads the CSV, prints its shape/head/dtypes/describe, and returns the DataFrame.
      - `preprocess_data()` copies the DataFrame, trims whitespace, reports missing/empty columns, and returns the cleaned frame without writing back to disk.
   - `main.py` — `test_data_module()` prints its section header, cleans `outputs/`, and, if `ENABLE_DATA_PROCESSING` is true, downloads, loads, and preprocesses the data before returning the cleaned result.
   - `outputs/` — Created at import; hosts artifacts zipped by `zip_all_outputs()` and any files created during the test.

