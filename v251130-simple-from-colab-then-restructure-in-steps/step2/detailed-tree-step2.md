# Step 2 — Detailed ASCII Tree (generated from step2 code)

Generated from the files in the `step2` folder on 2025-12-16. This single ASCII tree documents the files, key constants, functions, and runtime behaviors (import-time side effects and function-level side effects). Keep the file open while exploring the code to understand what happens when `main.py` runs.

```
step2/
├─ BMW-sales-data-2010-2024.csv
│    [Raw dataset file included in the folder; used by `data` functions when present. It is NOT created by step2 code unless `download_data_file()` runs and writes it.]
├─ config.py
│  ├─ PROJECT_ROOT -> Path(__file__).resolve().parent  [At import: resolves to the absolute path of the `step2` folder and is used as the base path for outputs and file locations.]
│  ├─ OUTPUT_DIR -> PROJECT_ROOT / 'outputs'  [At import: `OUTPUT_DIR` is constructed and `mkdir(parents=True, exist_ok=True)` is executed immediately — ensures `outputs/` exists on disk as an import-time side-effect.]
│  ├─ def out_path(name: str) -> str  [Function: returns `str(OUTPUT_DIR / name)`; computes where artifacts should be written; no disk IO by itself.]
│  ├─ pandas display options set  [At import: `pd.set_option(...)` configures pandas display behavior for REPL/prints; no IO side-effect.]
│  ├─ DATA_CSV_URL -> '<remote CSV URL>'  [Constant string: holds the remote CSV location; no network access until `download_data_file()` is called.]
│  ├─ DATA_CSV_FILE -> 'BMW-sales-data-2010-2024.csv'  [Constant string: expected local filename for the dataset; code reads/writes this filename in the repository root when download or load runs.]
│  └─ ENABLE_DATA_PROCESSING -> True  [Feature flag: when True, `main.test_data_module()` will run download/load/preprocess steps; controls runtime flow, no side-effect at import.]
├─ utils.py
│  ├─ import OUTPUT_DIR from config  [Importing `utils` expects `config` to have created `OUTPUT_DIR` already (import-time dependency).]
│  ├─ def clean_outputs():
│  │  ├─ print cleaning message  [Logs which OUTPUT_DIR is being cleaned to console; visible side-effect.]
│  │  ├─ if OUTPUT_DIR.exists(): iterate OUTPUT_DIR.iterdir()
│  │  │  ├─ if item.is_file(): item.unlink()  [Deletes files in `outputs/` — immediate disk-side effect; may remove previously generated artifacts.]
│  │  │  ├─ elif item.is_dir(): shutil.rmtree(item)  [Removes subdirectories recursively — destructive disk-side effect.]
│  │  │  └─ exceptions caught and printed  [Non-fatal: reports failures but continues processing remaining items.]
│  │  └─ else: OUTPUT_DIR.mkdir(parents=True, exist_ok=True)  [If outputs/ missing, create it.]
│  ├─ def print_section(title):
│  │  └─ prints a formatted header block  [Purely logging; improves console readability; no IO beyond stdout.]
│  └─ def zip_all_outputs(zip_filename=None, patterns=('*.png','*.html','*.csv','*.txt')):
│     ├─ determine `zip_path` (default `OUTPUT_DIR / 'all_outputs.zip'`)  [Chooses archive destination; supports custom relative/absolute names.]
│     ├─ ensure OUTPUT_DIR exists (mkdir if needed)  [Import-time guarantee but rechecked here to avoid errors; may create outputs/ if absent.]
│     ├─ open ZipFile(zip_path, 'w', ZIP_DEFLATED) and glob files by pattern  [Reads matching files from `outputs/` and writes them into the zip — disk read + write side-effects.]
│     ├─ print created zip path and count of files added  [User-visible confirmation on success.]
│     └─ return zip_path  [Returns Path to caller for further use.]
├─ data.py
│  ├─ imports: os, requests, pandas, print_section, DATA_CSV_FILE, DATA_CSV_URL  [Module-level imports; `requests` and `pandas` are required to run download and load operations.]
│  ├─ def download_data_file(file_name, data_url):
│  │  ├─ if not os.path.exists(file_name):
│  │  │  ├─ print attempt message  [Logs the network attempt to console.]
│  │  │  ├─ response = requests.get(data_url)
│  │  │  ├─ response.raise_for_status()  [Raises on HTTP error — exception will be caught by outer try and printed.]
│  │  │  ├─ open(file_name, 'wb') and write response.content  [Writes the downloaded bytes to a file in the current working directory — disk write side-effect.]
│  │  │  └─ print success message  [Confirmation on successful download.]
│  │  └─ else: print "already exists"  [Avoids re-downloading if file is present.]
│  │  └─ except requests.exceptions.RequestException as e: print error message  [Reports network errors; does not re-raise here.]
│  ├─ def download_required_files():
│  │  └─ calls download_data_file(DATA_CSV_FILE, DATA_CSV_URL)  [Convenience wrapper: triggers network download when invoked by `main`.]
│  ├─ def load_and_explore_data(csv_path):
│  │  ├─ print_section("DATASET OVERVIEW")  [Logs a section header.]
│  │  ├─ df = pd.read_csv(csv_path)  [Reads CSV from disk into a DataFrame — disk read side-effect and memory allocation.]
│  │  ├─ print shape, head, dtypes, describe  [Console output of the loaded data; useful for debugging/inspection.]
│  │  └─ return df  [Returns DataFrame to caller for preprocessing.]
│  └─ def preprocess_data(df):
│     ├─ df_clean = df.copy()  [Operates on a defensive copy to avoid mutating the original DataFrame in the caller.]
│     ├─ print_section("COLUMN ANALYSIS") and list columns/types  [Console reporting of column metadata and dtypes.]
│     ├─ compute missing values and trim whitespace from column names  [Data cleaning steps performed in-memory; no disk IO until caller writes results.]
│     ├─ detect empty columns by checking non-empty string values  [Logs warnings if columns are effectively empty and suggests actions.]
│     └─ return df_clean  [Returns cleaned DataFrame for further steps; no write-back to disk inside this function.]
├─ main.py
│  ├─ imports: DATA_CSV_FILE, ENABLE_DATA_PROCESSING from config  [Importing `config` executes its top-level code (OUTPUT_DIR.mkdir), so outputs/ exists before `main` runs.]
│  ├─ imports: clean_outputs, print_section from utils
+ │  └─ imports: data module (exposes download/load/preprocess functions)
│  ├─ def test_data_module():
│  │  ├─ print_section("STEP 2: DATA MODULE TEST")  [Console header for the step.]
│  │  ├─ clean_outputs()  [Deletes existing artifacts in `outputs/` — destructive disk-side effect to ensure a clean workspace.]
│  │  ├─ if ENABLE_DATA_PROCESSING: control flow enters download/load/preprocess steps  [Feature-flag guarded sequence; if False, data steps are skipped.]
│  │  │  ├─ print "Testing data download..." then data.download_required_files()  [Triggers network download if CSV missing; writes CSV to disk.]
│  │  │  ├─ print "Testing data loading..." then df = data.load_and_explore_data(DATA_CSV_FILE)  [Loads CSV from disk into memory and prints exploration info.]
│  │  │  ├─ print "Testing data preprocessing..." then df_clean = data.preprocess_data(df)  [Runs in-memory cleaning and returns cleaned DataFrame.]
│  │  │  └─ print completion and return df_clean  [Reports success and returns cleaned DataFrame to caller; useful for tests or chaining.]
│  └─ if __name__ == "__main__": test_data_module()  [Entry point: running the script executes the test sequence described above.] 
└─ outputs/  [Directory created at `config` import; holds generated artifacts.]
   └─ (may contain zip files, PNG/HTML/TXT/CSV outputs created by other steps or tests)  [Contents depend on which utilities or later steps have run; `clean_outputs()` will remove these files.]
```

## Summary — most important side-effects to know when running `main.py` in this step

- **Outputs directory created on import:** Importing `config` creates `outputs/` immediately (`mkdir(parents=True, exist_ok=True)`), so expect that folder to exist before any tests run.
- **Cleaning is destructive:** `clean_outputs()` will delete files and subdirectories in `outputs/` (use with care; it's called at the start of the test). 
- **Network download may occur:** `data.download_required_files()` calls `requests.get()` and will write `BMW-sales-data-2010-2024.csv` to disk if it's missing; network errors are printed but not re-raised.
- **Data loading and preprocessing are in-memory:** `load_and_explore_data()` reads the CSV into a pandas DataFrame and prints diagnostics; `preprocess_data()` returns a cleaned DataFrame but does not write cleaned data to disk.
- **Zip/archive creation is optional and explicit:** `zip_all_outputs()` will bundle matching files from `outputs/` into `all_outputs.zip` (or a custom path) and returns the zip path.

If you want, I can now run the same process for another `step` folder (`step1`, `step3`, etc.), or I can open a PR adding this `DETAILED_TREE.md`. Which would you like next?
