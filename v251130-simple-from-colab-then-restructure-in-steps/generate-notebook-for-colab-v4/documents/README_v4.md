Generate Notebook — Usage Guide (v4)

This document explains how to use `make_notebook-v4.py` to create a single, self-contained Jupyter notebook from a folder of Python modules.

Overview
- Purpose: Combine multiple `.py` modules into a single `.ipynb` that runs without external `.py` files. Module sources are embedded into code cells and executed as in-memory modules so `import` works normally.
- v4 highlights: human-readable triple-quoted embedding (with automatic escaping), `ensure_ascii=False` for Unicode preservation, cell source written as line lists for cleaner editing/diffs, and a final post-run cell that displays outputs generated in `outputs/` (text, PNG, HTML), excluding `07_all_outputs.html` and `all_outputs.zip`.

Quick examples

- From the generator folder (recommended):

```powershell
cd C:\Users\easts\github\bmw-sales-forecast\v251130-simple-from-colab-then-restructure-in-steps\generate-notebook-for-colab-v4
python .\make_notebook-v4.py --src ..\step6 --output combined.ipynb
```

- From anywhere (absolute paths):

```powershell
python C:\Users\easts\github\bmw-sales-forecast\v251130-simple-from-colab-then-restructure-in-steps\generate-notebook-for-colab-v4\make_notebook-v4.py --src C:\Users\easts\github\bmw-sales-forecast\v251130-simple-from-colab-then-restructure-in-steps\step6 --output combined.ipynb
```

Options
- `--src`: Source directory with `.py` modules (default: `step6`).
- `--output`: Output notebook path (default: `combined.ipynb`). If left as default, the script will write a timestamped name like `step6-combined-YYYYMMDD-HHMMSS.ipynb`.
- `--order-file`: Optional `order.txt` to force ordering (one filename per line).

Behavior notes (v4)
- Embedding: Module code is placed inside triple-quoted literals and executed with `exec()` into a `types.ModuleType`. Internal `"""` sequences and backslashes are escaped automatically.
- Readability: Each code cell `source` is saved as a list of lines for better readability in editors and VCS.
- Unicode: The notebook file is written with `ensure_ascii=False` so non-ASCII characters are preserved.
- Post-run display: After the main pipeline runs, a final cell displays all `.txt`, `.png`, and `.html` files found under `outputs/`, excluding `07_all_outputs.html` and `all_outputs.zip`.
- CSV handling: Any `*.csv` files in the source folder are copied into the notebook directory.

Requirements
- Python 3.8+
- Optional (for automated execution): `nbconvert`, `nbformat`, and `ipykernel` if you want to execute the generated notebook programmatically.

Troubleshooting
- `Source directory not found`: Confirm the `--src` path and your current working directory.
- `Imports failing` inside the generated notebook: Execute cells in order — the module shim cells must run before other cells that `import` those modules.
- `No outputs displayed` in final cell: Verify `outputs/` exists and contains `.txt`, `.png`, or `.html` files (and not only the excluded filenames).

Notes
- The generator replaces common `__file__` and `Path(__file__)` patterns with `Path.cwd()` so relative paths resolve inside the notebook environment.
- To change cleanup behavior, edit `cleanup_directories()` in `make_notebook-v4.py`.

Examples

```powershell
python .\make_notebook-v4.py --src ..\step6
python .\make_notebook-v4.py --src ..\step5 --output my-step5-notebook.ipynb
```
