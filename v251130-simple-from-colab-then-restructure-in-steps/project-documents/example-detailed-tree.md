# prompts to ai

Do not rely on or repeat previous conversations. Instead, work only with the code in the step1 folder and produce an ASCII tree that helps a learner understand that code and how it works.

Extend and expand the ASCII-tree diagram. In the same, single diagram, provide about three times more depth and detail than the current diagram.

For the following items:
├─ PROJECT_ROOT → Path(file).resolve().parent
├─ OUTPUT_DIR → PROJECT_ROOT / 'outputs' (created at import)
├─ out_path(name) → returns str(OUTPUT_DIR / name)
├─ DATA_CSV_URL → remote CSV URL (string)
└─ DATA_CSV_FILE → local CSV filename string

add, in brackets, an explicit note describing exactly what happens at each stage of processing. Then rewrite the ASCII tree to include those bracketed notes.

Finally, do the same (expand with bracketed explanations) for the entire ASCII tree of the step1 folder and save the result as a Markdown file.

# ai said

I'll add a new markdown file step1/DETAILED_TREE.md containing the full ASCII tree with bracketed explanations for each node.

# Step 1 — Detailed ASCII Tree (with explanations)

This file documents the Step 1 folder contents and explains exactly what each file, function, and statement does at runtime. Each line has a bracketed note describing the action or side effect.

```
step1/
├─ BMW-sales-data-2010-2024.csv
│    [Raw dataset file present for later steps; NOT loaded by `main.py` in Step 1.]
├─ config.py
│  ├─ PROJECT_ROOT → Path(__file__).resolve().parent
│  │     [At import: resolves this module's file to an absolute path and sets the project base directory (step1 folder).]
│  ├─ OUTPUT_DIR → PROJECT_ROOT / 'outputs' (created at import)
│  │     [At import: constructs OUTPUT_DIR and calls `mkdir(parents=True, exist_ok=True)` — ensures outputs/ exists on disk (side-effect).]
│  ├─ out_path(name) → returns str(OUTPUT_DIR / name)
│  │     [Function: join `name` to OUTPUT_DIR and return the full path as a string; used by other modules to write/read files into outputs/.]
│  ├─ DATA_CSV_URL → remote CSV URL (string)
│  │     [Constant: holds URL where dataset can be downloaded; no network action here until other code uses it.]
│  └─ DATA_CSV_FILE → local CSV filename string
│        [Constant: canonical local filename expected by other modules when reading the CSV (e.g., pandas.read_csv()).]
├─ utils.py
│  ├─ clean_outputs()
│  │  ├─ print("Cleaning output directory: {OUTPUT_DIR}")
│  │  │     [Logs which directory is being cleaned (visible to the user).]
│  │  ├─ if OUTPUT_DIR.exists(): iterate OUTPUT_DIR.iterdir()
│  │  │  ├─ if item.is_file(): item.unlink()    [Deletes file entries; side-effect on disk.]
│  │  │  ├─ elif item.is_dir(): shutil.rmtree(item)  [Deletes subdirectories recursively; side-effect on disk.]
│  │  │  └─ exceptions caught → print failure message  [Non-fatal; reports but continues.]
│  │  └─ else: OUTPUT_DIR.mkdir(parents=True, exist_ok=True)  [Ensures outputs/ exists when it didn't before.]
│  ├─ print_section(title)
│  │  └─ print formatted header with separators  [Makes console logs readable and groups steps visually.]
│  └─ zip_all_outputs(zip_filename=None, patterns=('*.png','*.html','*.csv','*.txt'))
│     ├─ determine zip_path (default: OUTPUT_DIR / 'all_outputs.zip')  [Chooses where the zip will be created; supports custom name.]
│     ├─ ensure OUTPUT_DIR exists  [Creates outputs/ if missing to avoid errors.]
│     ├─ for each pat in patterns: for p in OUTPUT_DIR.glob(pat): if p.is_file(): zf.write(p, arcname=p.name)
│     ├─ print created zip path and count of files added  [User-visible confirmation of success.]
│     └─ return zip_path  [Allows caller to inspect where the zip was written.] 
├─ main.py
│  ├─ imports: PROJECT_ROOT, OUTPUT_DIR, DATA_CSV_URL, DATA_CSV_FILE from config.py
│  │     [Importing config triggers OUTPUT_DIR creation side-effect before main runs.] 
│  ├─ imports: clean_outputs, print_section, zip_all_outputs from utils.py
│  ├─ def test_infrastructure():
│  │  ├─ print_section("STEP 1: INFRASTRUCTURE & CONFIGURATION TEST")
│  │  │     [Prints a clear header to group the validation steps in console output.]
│  │  ├─ # 1. Verify Configuration
│  │  │  ├─ print(f"✅ Project Root: {PROJECT_ROOT}")
│  │  │  │    [Shows absolute path used as base; helps developer confirm location.] 
│  │  │  ├─ print(f"✅ Output Directory: {OUTPUT_DIR}")
│  │  │  │    [Shows path where artifacts will be written; useful for debugging file permissions.] 
│  │  │  └─ print(f"✅ Data URL Configured: {DATA_CSV_URL[:50]}...")
│  │  │       [Prints head of DATA_CSV_URL to confirm a URL is configured; no download performed here.] 
│  │  ├─ # 2. Verify Utils - Clean
│  │  │  ├─ print("\nTesting clean_outputs()...")
│  │  │  └─ clean_outputs()  [Calls helper that removes files/dirs in outputs/; side-effect on disk.] 
│  │  ├─ # 3. Verify Utils - File Operations
│  │  │  ├─ print("\nTesting file generation in Output Directory...")
│  │  │  ├─ test_file = OUTPUT_DIR / "test_infrastructure.txt"
│  │  │  ├─ with open(test_file, "w") as f: f.write("This is a test file to verify Step 1 infrastructure.")
│  │  │  │    [Creates a small text file in outputs/ to confirm write access and correct path.] 
│  │  │  └─ print success or catch exception and print failure message  [Reports result to user console.] 
│  │  ├─ # 4. Verify Utils - Zip
│  │  │  ├─ print("\nTesting zip_all_outputs()...")
│  │  │  ├─ zip_path = zip_all_outputs()
│  │  │  │    [Creates all_outputs.zip in outputs/ containing files that match configured patterns; returns zip Path.] 
│  │  │  └─ print zip success or catch and print exception  [Reports zip creation outcome.] 
│  │  └─ end test_infrastructure
│  └─ if __name__ == "__main__": test_infrastructure()  [Entry point: run validations when script executed directly.] 
└─ outputs/
   ├─ test_infrastructure.txt
   │   [Created by main.py test step; contains a short string to prove write permissions.] 
   └─ all_outputs.zip
       [Created when zip_all_outputs() runs; contains files matching patterns (if any exist).]

```
