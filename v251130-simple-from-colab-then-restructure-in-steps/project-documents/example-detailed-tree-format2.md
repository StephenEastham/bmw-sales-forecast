# Step 1 — Step-by-step tree (nested bullet format)

This file expands on the previous ASCII tree by reformatting it as nested Markdown bullets so the behavior notes remain clear while matching the structure used in `CHANGES_step2_to_step3.md`.

## Summary — essential side-effects when running `step1/main.py`

- Importing `config.py` happens before any helper runs; it resolves `PROJECT_ROOT` and immediately creates `outputs/` with `mkdir(parents=True, exist_ok=True)`, so the directory exists for downstream helpers.
- `clean_outputs()` is invoked early in the infrastructure test and deletes all files/directories under `outputs/`, ensuring each run starts with an empty artifact folder.
- The test writes `test_infrastructure.txt` into `outputs/` to prove write access, then `zip_all_outputs()` can archive any matching artifacts created in that folder.
- Step 1 exercises only the infrastructure helpers—no network downloads or CSV parsing occur here.

- `step1/` — Files and runtimes
  - `BMW-sales-data-2010-2024.csv` — Raw dataset placeholder for later steps; Step 1 does not load it, so no IO occurs during this test.
  - `config.py` — Defines paths, constants, and display settings that shape behavior across modules.
    - Import-time sequence: compute `PROJECT_ROOT -> Path(__file__).resolve().parent`, then derive `OUTPUT_DIR -> PROJECT_ROOT / 'outputs'`, and finally call `OUTPUT_DIR.mkdir(parents=True, exist_ok=True)` so the directory exists immediately for other modules.
    - `out_path(name: str) -> str` — Combines `OUTPUT_DIR` with a filename; no IO by itself but standardizes artifact paths.
    - `DATA_CSV_URL` & `DATA_CSV_FILE` — Constants holding the remote source and local filename for the dataset; no network or disk access occurs unless future steps invoke download functions.
  - `utils.py` — Provides reusable helpers for cleaning, logging, and archiving outputs.
    - `clean_outputs()` — Prints a header, iterates over `OUTPUT_DIR.iterdir()` if the directory exists, unlinks files, removes subdirectories with `shutil.rmtree`, catches exceptions, and creates `outputs/` if it was missing; destructive disk-side effect used by Step 1 to start clean.
    - `print_section(title)` — Prints formatted separators and the provided title; pure logging for human-readable grouping.
    - `zip_all_outputs(zip_filename=None, patterns=('*.png','*.html','*.csv','*.txt'))` — Ensures `OUTPUT_DIR` exists, globs the provided patterns, writes matching files into a ZIP archive using `zipfile.ZipFile`, prints the created path, and returns the final `Path`; reads output files and writes the archive to disk.
  - `main.py` — Orchestrates the infrastructure test and exercises the helpers.
    - Imports `PROJECT_ROOT`, `OUTPUT_DIR`, `DATA_CSV_URL`, `DATA_CSV_FILE` from `config.py`, triggering the import-time creation of `outputs/` before testing begins.
    - Imports `clean_outputs`, `print_section`, `zip_all_outputs` from `utils.py` to use the helper behavior described above.
    - `def test_infrastructure()` — Prints a section header, validates configuration fields by printing `PROJECT_ROOT`, `OUTPUT_DIR`, and a truncated `DATA_CSV_URL`, then runs `clean_outputs()` to clear prior artifacts, writes `test_infrastructure.txt` inside `outputs/` to prove write access, prints success messages or errors, and finally calls `zip_all_outputs()` to package whatever is in `outputs/`, reporting the path of the resulting zip.
    - `if __name__ == "__main__": test_infrastructure()` — Entry point that executes the test when running `python main.py`.
  - `outputs/` — Directory created at import; hosts `test_infrastructure.txt` (created during the test) and `all_outputs.zip` (created by `zip_all_outputs()`), both of which demonstrate write/delete capabilities for this folder.

Legend: This nested bullet style mirrors the delta tree formatting and keeps detailed runtime notes on the same line as their subjects.


