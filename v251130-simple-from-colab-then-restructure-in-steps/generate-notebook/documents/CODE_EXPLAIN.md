make_notebook.py — Code Explanation
=================================

Purpose
-------
This document explains the structure and behavior of `make_notebook.py` (located beside this file). The script combines multiple Python modules into a single Jupyter notebook, writes processed `.py` files next to the notebook for import compatibility, copies CSV files from the source folder, and performs a cleanup of the notebook directory before generation.

High-level flow
----------------
1. Parse command-line arguments (`--src`, `--output`, `--order-file`).
2. If `--output` is left at the default `combined.ipynb`, compute a timestamped output filename using the source folder name: `{src.name}-combined-YYYYMMDD-HHMMSS.ipynb`.
3. Verify `--src` exists and is a directory.
4. Run `cleanup_directories()` on the notebook directory (deletes `outputs/*` and top-level files except a small whitelist).
5. Gather `.py` files from the source folder via `find_py_files()`.
6. Optionally read `order.txt` (or the path you pass via `--order-file`) to get an explicit ordering; otherwise compute an order using imports with `build_dependency_graph()` + `topo_sort()`; if that fails, fall back to alphabetical order.
7. Call `make_notebook(order, output)` to create the notebook and write supporting files.

Key functions and responsibilities
---------------------------------
- `cleanup_directories(notebook_dir: Path)`
  - Deletes everything inside `notebook_dir/outputs` (files and directories).
  - Deletes top-level files under `notebook_dir` except for a small whitelist: `make_notebook.py` and `order.txt`.
  - Prints deleted filenames for visibility.
  - Note: this is intentionally aggressive to ensure a clean environment; change the whitelist or disable this function if you need to preserve files.

- `find_py_files(src: Path) -> List[Path]`
  - Recursively finds `.py` files under `src` (sorted), skipping any path that includes `__pycache__` or `outputs` in its parts.

- `parse_imports(path: Path) -> Set[str]`
  - Parses a Python file using `ast` and extracts top-level import module base names (e.g., `from foo.bar import x` -> `foo`).
  - Returns a set of module base names referenced by the file.

- `build_dependency_graph(files: List[Path]) -> (module_map, deps)`
  - Builds a mapping from module name (stem) to file path and a dependency map where `deps[name]` is the set of module names that must come before `name` (i.e., modules referenced by `name`).

- `topo_sort(nodes: List[str], deps: Dict[str, Set[str]]) -> List[str]`
  - Performs Kahn's algorithm for topological sorting to order modules so dependencies come first.
  - If a cycle is detected, it returns an empty list to signal failure.

- `strip_module_docstring(src: str) -> str`
  - Uses `ast` to detect a leading module-level docstring and removes that docstring text from the code string (so the code cells in the notebook won't duplicate the docstring when a markdown cell is generated for documentation).

- `make_notebook(order: List[Path], output: Path)`
  - Core notebook generation function. For each file in `order`:
    - Reads the source text.
    - Replaces common `__file__` patterns with `Path.cwd()` (and replaces raw `__file__` with `str(Path.cwd())`) so code works inside a notebook.
    - Stores processed text in a dictionary and writes the processed `.py` file into the notebook directory (so the notebook kernel can import it).
  - Copies any `*.csv` files from the source directory to the notebook directory.
  - Builds the notebook JSON structure in memory: an initialization code cell, optional markdown cells for module docstrings, and code cells with the module source (docstring-stripped where appropriate).
  - Writes the `.ipynb` file to `output`.

Design notes and rationale
-------------------------
- Writing processed `.py` files to disk:
  - Jupyter notebook kernels import modules relative to the notebook's working directory. Writing the processed `.py` files alongside the notebook avoids import errors inside the notebook.

- Replacing `__file__` and `Path(__file__)...`:
  - Many scripts use `Path(__file__).resolve().parent` to locate relative data files. In a notebook, `__file__` is undefined. The script uses regex replacements to convert these patterns to `Path.cwd()` so relative paths resolve relative to the notebook directory.

- Cleanup behavior:
  - The script aggressively clears `outputs/` and top-level files to give a deterministic environment and avoid stale outputs or code. This is intentional for reproducibility; modify `cleanup_directories()` if you want a softer behavior.

- Ordering heuristics:
  - The primary strategy uses AST-derived import relationships to compute a topological order. If that cannot be determined (cycles or ambiguous dependencies), the script falls back to alphabetical order.

Customization points
--------------------
- Change timestamp format: edit the `datetime.now().strftime('%Y%m%d-%H%M%S')` pattern in `main()` to include milliseconds or UTC as needed.
- Modify the whitelist in `cleanup_directories()` (variable `keep_files`) to preserve additional files.
- Disable or soften cleanup by altering or removing the calls in `main()` to `cleanup_directories()`.
- Adjust `__file__` replacement rules in `make_notebook()` (the regexes at the start of the function) if you see patterns not covered by the current replacements.

Troubleshooting
---------------
- "Source directory not found": check the `--src` path is correct and that you run the script from the folder containing `make_notebook.py` or provide absolute paths.
- Imports failing inside the notebook: confirm that the generated `.py` files were written into the same directory as the `.ipynb` and that the notebook's current working directory contains them.
- If the script deletes files you didn't expect: open `cleanup_directories()` and change `keep_files` or comment out the deletion logic.

Command examples
----------------
Run with a timestamped default name (recommended):

```powershell
python .\make_notebook.py --src ..\step6
```

Run and force an explicit output name (no timestamping):

```powershell
python .\make_notebook.py --src ..\step6 --output my-notebook.ipynb
```

Run using an order file (one filename per line):

```powershell
python .\make_notebook.py --src ..\step6 --order-file order.txt
```

Contact points in the source file
-------------------------------
- `cleanup_directories` (top) — controls deletion behavior.
- `find_py_files`, `parse_imports`, `build_dependency_graph`, `topo_sort` — ordering logic.
- `strip_module_docstring` — docstring handling for nicer notebook cells.
- `make_notebook` — central processing and file writes.
- `main` — argument parsing, timestamping logic, and orchestration.

If you want, I can also add inline code comments to `make_notebook.py` to annotate each step directly in the source. Would you like that? 
