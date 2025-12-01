Generate Notebook — Usage Guide

This document explains how to use `make_notebook.py` to combine a folder of Python modules into a single Jupyter notebook.

Overview:
- Purpose: Combine multiple `.py` modules into one self-contained `.ipynb` file. Modules are embedded directly into the notebook cells, allowing them to run without external `.py` files. It also copies any CSV data files from the source folder.
- Clean behavior: Before generating, the script deletes files in the `outputs/` folder and removes files in the notebook directory except `make_notebook.py` and `order.txt`.

Quick Examples:

- Default (timestamped output):

  ```powershell
  PS C:\Users\easts\github\bmw-sales-forecast\v251130-simple-from-colab-then-restructure-in-steps\generate-notebook> \
    python .\make_notebook.py --src ..\step6
  ```

  When `--output` is left as the default (`combined.ipynb`), the script will create a timestamped file named like `step6-combined-YYYYMMDD-HHMMSS.ipynb`.

- Explicit output name:

  ```powershell
  PS> python .\make_notebook.py --src ..\step6 --output my-notebook.ipynb
  ```

  If you provide an explicit `--output` path/name, that path will be used (no timestamp injected).

Command-line Options:
- `--src`: Path to the source folder containing `.py` modules (default: `step6`).
- `--output`: Path for the generated `.ipynb` (default: `combined.ipynb`, which triggers timestamping).
- `--order-file`: Optional `order.txt` (one filename per line) to force a specific file ordering.

Behavior Notes:
- Modules are embedded as string literals and loaded dynamically into `sys.modules`. This allows standard `import` statements to work without writing `.py` files to disk.
- It replaces common `__file__` patterns with `Path.cwd()` so modules run correctly in a notebook environment.
- CSV files found in the source folder are copied into the notebook directory.
- The cleanup step will delete files in `outputs/` and remove all top-level files in the notebook directory except `make_notebook.py` and `order.txt`. Use version control or backups if you keep other files there.

Requirements:
- Python 3.8+ (script uses only standard library modules: `argparse`, `ast`, `json`, `pathlib`, `re`, `shutil`, `datetime`).

Troubleshooting:
- If you see `Source directory not found: <path>`, confirm the `--src` path is correct and relative to the current working directory.
- If imports fail inside the notebook, ensure you have run all the cells in order. The cells containing the module code must be executed to register the modules before they can be imported.

Customizations:
- Timestamp format can be changed in `make_notebook.py` (the script uses `%Y%m%d-%H%M%S`).
- To prevent cleanup, modify `cleanup_directories()` in `make_notebook.py` (not recommended unless you understand the consequences).

Example run (PowerShell):

```powershell
cd C:\Users\easts\github\bmw-sales-forecast\v251130-simple-from-colab-then-restructure-in-steps\generate-notebook
python .\make_notebook.py --src ..\step6
```

This will create a file similar to `step6-combined-20251201-072529.ipynb` in the `generate-notebook` folder and place the processed module `.py` files there.
