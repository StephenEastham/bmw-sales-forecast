# Step 3 — Detailed ASCII Tree (generated from step3 code)

Generated from the `step3` folder's code on 2025-12-17. This file contains one expanded ASCII tree with bracketed runtime explanations and a short summary of the most important side-effects (placed before the tree as requested).

## Summary — most important side-effects when running `main.py` in this step

- `outputs/` is created at import time by `config.py` via `mkdir(parents=True, exist_ok=True)`.
- `clean_outputs()` deletes files and subdirectories inside `outputs/` (destructive disk-side effect) and is called at test start.
- `data.download_required_files()` may perform an HTTP `GET` and write `BMW-sales-data-2010-2024.csv` if missing (network + disk write).
- Analysis functions (`exploratory_data_analysis`, `aggregate_time_series`) perform in-memory aggregations and print diagnostics; they return DataFrames/arrays but do not, by default, write new files.

```
step3/
├─ BMW-sales-data-2010-2024.csv  [Local CSV file used by `data.load_and_explore_data()` when present; disk read if used; created only by downloader if missing.]
├─ config.py
│  ├─ PROJECT_ROOT -> Path(__file__).resolve().parent  [Computed at import: absolute Path to step3 folder; used as base for output paths and other file joins.]
│  ├─ OUTPUT_DIR -> PROJECT_ROOT / 'outputs'  [Constructed at import and `mkdir(parents=True, exist_ok=True)` executed immediately — ensures outputs/ exists (import-time side-effect).]
│  ├─ def out_path(name: str) -> str  [Signature: returns str(OUTPUT_DIR / name); purpose: canonicalize artifact paths for writing; no IO performed when called.]
│  ├─ pd.set_option(...)  [At import: configures pandas display options for console output; no disk IO.]
│  ├─ DATA_CSV_URL -> '<remote CSV URL>'  [Constant string used by downloader; no network until `download_data_file()` is invoked.]
│  ├─ DATA_CSV_FILE -> 'BMW-sales-data-2010-2024.csv'  [Local filename expected by data loader; used as path argument to `pd.read_csv`.]
│  └─ Feature flags (ENABLE_DATA_PROCESSING=True, ENABLE_EXPLORATORY_ANALYSIS=True, ENABLE_TIME_SERIES=True)  [Constants that gate runtime branches inside `main.test_analysis_module()`; no side-effects at import.]
├─ utils.py
│  ├─ imports: OUTPUT_DIR from config  [Relies on import-time side-effect that ensures `outputs/` exists before utils code runs.]
│  ├─ def clean_outputs():
│  │  ├─ Signature: clean_outputs()  [Purpose: remove stale artifacts in `outputs/` to ensure tests start clean.]
│  │  ├─ Behavior: prints cleaning header, if OUTPUT_DIR.exists() iterates OUTPUT_DIR.iterdir()  [Logs which directory will be cleaned; reads disk entries.]
│  │  ├─ For each item: if item.is_file(): item.unlink()  [Deletes files in `outputs/` — destructive disk-side effect; may raise and exceptions are caught inside function.] 
│  │  ├─ elif item.is_dir(): shutil.rmtree(item)  [Removes subdirectories recursively; destructive disk-side effect.] 
│  │  └─ else: OUTPUT_DIR.mkdir(parents=True, exist_ok=True)  [If outputs/ missing, create it.]
│  ├─ def print_section(title):
│  │  ├─ Signature: print_section(title: str)  [Purpose: print a formatted header to stdout; pure logging, no IO.]
│  │  └─ Behavior: prints separators and title  [Helps human-readability in console output.]
│  └─ def zip_all_outputs(zip_filename=None, patterns=('*.png','*.html','*.csv','*.txt')):
│     ├─ Signature: zip_all_outputs(zip_filename: Optional[str], patterns: Tuple[str]) -> Path  [Creates a zip archive of matching files in `outputs/` and returns the Path to zip file.]
│     ├─ Behavior: ensures OUTPUT_DIR exists, searches for patterns, writes matching files into zip using zipfile.ZipFile  [Reads files from disk and writes an archive to disk; returns path to created zip; prints success.]
│     └─ Exceptions: any IO errors printed and function attempts to continue gracefully.]
├─ data.py
│  ├─ imports: os, requests, pandas as pd, print_section, DATA_CSV_FILE, DATA_CSV_URL  [Requires `requests` for download and `pandas` for CSV parsing; importing does not perform network IO.]
│  ├─ def download_data_file(file_name: str, data_url: str):
│  │  ├─ Signature: download_data_file(file_name, data_url)  [Purpose: download remote CSV and save locally if missing; side-effect: disk write and network GET.]
│  │  ├─ Behavior: if not os.path.exists(file_name): r = requests.get(data_url, stream=True) -> open(file_name,'wb') and write r.content/chunks  [Performs HTTP GET and writes bytes to disk; prints progress and error messages; exceptions caught and printed but not re-raised.]
│  │  └─ else: print("already exists")  [Skips network and write when local file present.] 
│  ├─ def download_required_files():
│  │  ├─ Behavior: wrapper that calls download_data_file(DATA_CSV_FILE, DATA_CSV_URL)  [Convenience function invoked by `main` to ensure required files are present; may cause network IO and disk writes.]
│  ├─ def load_and_explore_data(csv_path: str) -> pd.DataFrame:
│  │  ├─ Signature: load_and_explore_data(csv_path)  [Purpose: read CSV into DataFrame and print basic diagnostics; side-effect: disk read and console prints.] 
│  │  ├─ Behavior: df = pd.read_csv(csv_path); prints df.shape, df.head(), df.dtypes, df.describe()  [Reads file into memory and displays summaries to stdout; returns DataFrame for downstream processing.]
│  │  └─ Exceptions: IO errors printed if CSV missing or malformed.]
│  └─ def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
│     ├─ Signature: preprocess_data(df)  [Purpose: perform in-memory cleanup and column normalization; no disk IO by default.] 
│     ├─ Behavior: df.copy(), strip column whitespace, drop empty columns, report missing values  [Operates purely in memory and returns cleaned DataFrame; prints summary to console.]
     └─ Return: cleaned DataFrame
├─ analysis.py
│  ├─ imports: numpy as np, pandas as pd, print_section  [Provides numeric and aggregation helpers for EDA and time-series operations; import has no side-effects.]
│  ├─ def exploratory_data_analysis(df_clean: pd.DataFrame):
│  │  ├─ Signature: exploratory_data_analysis(df_clean)  [Purpose: print grouped summaries and top model/region reports; operates in-memory.] 
│  │  ├─ Behavior: compute groupby aggregations (by Model, Region, Year), print top results and descriptive stats  [Creates intermediate DataFrames in memory and prints results to stdout; no files written by default.] 
│  │  └─ Return: None (side-effect: console prints only).]
│  └─ def aggregate_time_series(df_clean: pd.DataFrame):
│     ├─ Signature: aggregate_time_series(df_clean) -> tuple  [Purpose: aggregate sales by Year and produce arrays for modeling and reporting; returns (df_yearly, ts_data, ts_years, df_model_yearly, df_region_yearly).]
     ├─ Behavior: df_yearly = df_clean.groupby('Year').agg({'Sales_Volume':'sum'}).reset_index()  [In-memory aggregation and sorting; prints summary statistics such as count, range, average, peak; computes YoY growth column.] 
     ├─ Additional steps: compute ts_data = df_yearly['Total_Sales'].values and groupby Model/Region yearly frames  [Extracts numpy arrays for downstream modeling and builds auxiliary DataFrames; no disk IO.] 
     └─ Return: in-memory tuple of DataFrames/arrays for caller; no files written.]
├─ main.py
│  ├─ imports: DATA_CSV_FILE, ENABLE_DATA_PROCESSING, ENABLE_TIME_SERIES, ENABLE_EXPLORATORY_ANALYSIS from config  [Importing config executes its import-time side-effects (e.g., creating `outputs/`).]
│  ├─ imports: clean_outputs, print_section from utils; imports data and analysis modules  [Brings helper functions and domain logic into scope; no immediate IO beyond config import.]
│  ├─ def test_analysis_module():
│  │  ├─ Signature: test_analysis_module()  [Purpose: orchestrate a smoke test that ensures data is present, preprocesses it, runs EDA and time-series aggregation, and returns results; may call disk/network helpers.] 
│  │  ├─ Step: print_section("STEP 3: ANALYSIS MODULE TEST")  [Console-only header to separate output.]
│  │  ├─ Step: clean_outputs()  [Deletes files/dirs in `outputs/` to ensure a fresh run (destructive).]
│  │  ├─ If ENABLE_DATA_PROCESSING:
│  │  │  ├─ data.download_required_files()  [May perform HTTP GET and write CSV to disk if missing; otherwise skips.] 
│  │  │  ├─ df = data.load_and_explore_data(DATA_CSV_FILE)  [Reads CSV into DataFrame from disk and prints diagnostics; disk read occurs here.] 
│  │  │  ├─ df_clean = data.preprocess_data(df)  [In-memory transforms and returns cleaned DataFrame; prints summary.] 
│  │  │  ├─ If ENABLE_EXPLORATORY_ANALYSIS: analysis.exploratory_data_analysis(df_clean)  [In-memory EDA with printed summaries; no files written.] 
│  │  │  ├─ If ENABLE_TIME_SERIES: results = analysis.aggregate_time_series(df_clean)  [Aggregates time-series data and returns multiple in-memory results; prints summary statistics.] 
│  │  │  └─ print completion and return results  [Function returns in-memory analysis outputs to caller; no automatic plotting or file outputs by default.] 
│  └─ if __name__ == "__main__": test_analysis_module()  [Entry point: running `python -m step3.main` executes the orchestrated test sequence described above.] 
└─ outputs/  [Directory created at `config` import; holds artifacts if other code writes them (zip_all_outputs() or manual writes); `clean_outputs()` will remove its contents.]
```

Generated per the prompt in project-documents/prompt-that-generates-tree-from-step.md: single ASCII tree, summary inserted before the tree, and bracketed runtime notes for files, constants, and functions.
