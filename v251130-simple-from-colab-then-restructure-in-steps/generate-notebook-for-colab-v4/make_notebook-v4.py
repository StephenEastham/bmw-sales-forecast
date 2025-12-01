#!/usr/bin/env python3
"""Combine Python files into a Jupyter notebook using heuristics.

Usage examples:
  python make_notebook.py --src ../step6 --output combined.ipynb
  python make_notebook.py --src ../step6 --output combined.ipynb --order-file order.txt

Notes:
- The script ignores directories named `__pycache__` and `outputs` and files matching CSV patterns.
- Ordering: if an `--order-file` is provided and non-empty, that order is used. Otherwise a heuristic
  derived from imports is used (best effort). If the heuristic fails, alphabetical order is used.
"""

import argparse
import ast
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple
import sys
import re
import shutil
from datetime import datetime


def cleanup_directories(notebook_dir: Path):
    """Clean up the notebook directory and outputs folder before generating."""
    # Delete all files in outputs folder
    outputs_dir = notebook_dir / 'outputs'
    if outputs_dir.exists():
        for item in outputs_dir.iterdir():
            try:
                if item.is_file():
                    item.unlink()
                    print(f'Deleted: {item.name}')
                elif item.is_dir():
                    shutil.rmtree(item)
                    print(f'Deleted directory: {item.name}')
            except Exception as e:
                print(f'Failed to delete {item}: {e}')
    
    # Delete all files in notebook_dir EXCEPT make_notebook.py and order.txt
    # Also preserve the running script itself so the generator doesn't delete itself.
    # Protect the running script (and common name variants) so the generator
    # will not delete itself. Compare resolved paths and also keep name variants
    # (dash vs underscore) because filenames can differ across OS/tools.
    script_path = Path(__file__).resolve()
    keep_paths = {script_path}
    try:
        argv0 = Path(sys.argv[0]).resolve()
        keep_paths.add(argv0)
    except Exception:
        pass

    script_name = script_path.name
    alt_name_underscore = script_name.replace('-', '_')
    alt_name_dash = script_name.replace('_', '-')
    keep_names = {script_name, alt_name_underscore, alt_name_dash, 'make_notebook-v2.py', 'order.txt'}

    for item in notebook_dir.iterdir():
        # Never delete files whose resolved path matches the running script or argv[0]
        try:
            if item.resolve() in keep_paths:
                continue
        except Exception:
            # If resolve fails, fall back to name-based check
            pass

        if item.is_file() and item.name not in keep_names:
            try:
                item.unlink()
                print(f'Deleted: {item.name}')
            except Exception as e:
                print(f'Failed to delete {item}: {e}')


def find_py_files(src: Path) -> List[Path]:
    files = []
    for p in sorted(src.rglob('*.py')):
        # skip __pycache__ and outputs directories
        if any(part == '__pycache__' or part == 'outputs' for part in p.parts):
            continue
        # skip files in top-level outputs or other non-source locations
        files.append(p)
    return files


def parse_imports(path: Path) -> Set[str]:
    names = set()
    try:
        src = path.read_text(encoding='utf-8')
        tree = ast.parse(src)
    except Exception:
        return names
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                base = alias.name.split('.')[0]
                names.add(base)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                base = node.module.split('.')[0]
                names.add(base)
    return names


def build_dependency_graph(files: List[Path]) -> Tuple[Dict[str, Path], Dict[str, Set[str]]]:
    # map module name -> path
    module_map: Dict[str, Path] = {p.stem: p for p in files}
    deps: Dict[str, Set[str]] = {p.stem: set() for p in files}
    for p in files:
        imports = parse_imports(p)
        for imp in imports:
            if imp in module_map and imp != p.stem:
                # dependency: imp should come before p.stem
                deps[p.stem].add(imp)
    return module_map, deps


def topo_sort(nodes: List[str], deps: Dict[str, Set[str]]) -> List[str]:
    # Kahn's algorithm -- edges are deps[file] = set(files that must come before file)
    from collections import deque

    indeg = {n: 0 for n in nodes}
    rev: Dict[str, Set[str]] = {n: set() for n in nodes}
    for n in nodes:
        for d in deps.get(n, []):
            indeg[n] += 1
            rev.setdefault(d, set()).add(n)

    q = deque([n for n, d in indeg.items() if d == 0])
    out = []
    while q:
        n = q.popleft()
        out.append(n)
        for m in rev.get(n, ()):  # nodes that depend on n
            indeg[m] -= 1
            if indeg[m] == 0:
                q.append(m)

    if len(out) != len(nodes):
        # cycle detected; return empty to signal failure
        return []
    return out


def strip_module_docstring(src: str) -> str:
    # Remove leading module-level docstring if present using AST node locs
    try:
        tree = ast.parse(src)
        if tree.body and isinstance(tree.body[0], ast.Expr):
            expr = tree.body[0]
            val = expr.value
            # ast.Constant (py3.8+)
            if isinstance(val, ast.Constant) and isinstance(val.value, str):
                # determine line range to remove
                start = getattr(expr, 'lineno', None)
                end = getattr(expr, 'end_lineno', None)
                if start is not None:
                    lines = src.splitlines(True)
                    if end is None:
                        end = start
                    # slice out the docstring lines (1-indexed to 0-indexed)
                    del lines[start-1:end]
                    return ''.join(lines)
    except Exception:
        pass
    return src


def make_notebook(order: List[Path], output: Path):
    cells = []
    
    # Store processed module texts (with __file__ replacements already applied)
    processed_modules: Dict[str, str] = {}
    
    # Write module files to disk next to the notebook AND store processed text
    notebook_dir = output.parent
    for p in order:
        text = p.read_text(encoding='utf-8')
        # Replace __file__ patterns for notebook compatibility
        text = re.sub(r"Path\s*\(\s*__file__\s*\)\s*\.resolve\s*\(\s*\)\s*\.parent", "Path.cwd()", text)
        text = re.sub(r"Path\s*\(\s*__file__\s*\)\s*\.parent", "Path.cwd()", text)
        text = text.replace("__file__", "str(Path.cwd())")

        # Keep original import statements intact. Module shims will be
        # registered in sys.modules so imports like `import data` will work
        # during notebook execution.
        
        # Store the processed text for use in notebook cells
        processed_modules[p.name] = text
        
        # Write module file to disk
        # module_path = notebook_dir / p.name
        # module_path.write_text(text, encoding='utf-8')
        # print(f'Wrote module: {module_path}')
    
    # Copy CSV data files from source directory to notebook directory
    src_dir = order[0].parent if order else Path('.')
    for csv_file in src_dir.glob('*.csv'):
        dest_csv = notebook_dir / csv_file.name
        dest_csv.write_bytes(csv_file.read_bytes())
        print(f'Copied data file: {dest_csv}')
    
    # Add simple initialization cell
    init_code = (
        "# Notebook initialization\n"
        "# This notebook combines multiple Python modules into a single executable notebook.\n"
        "# All module code is embedded directly in the cells below.\n"
        "\n"
        "import sys\n"
        "import types\n"
        "from pathlib import Path\n"
        "\n"
        "# Ensure current directory is in path for imports\n"
        "if str(Path.cwd()) not in sys.path:\n"
        "    sys.path.insert(0, str(Path.cwd()))\n"
        "\n"
        "print('✅ Notebook initialized. All modules are embedded and ready to run.')"
    )
    
    cells.append({
        'cell_type': 'code',
        'metadata': {'language': 'python'},
        'source': [init_code],
        'outputs': [],
        'execution_count': None
    })

    # Add documentation and module-initialization cells for each module
    # Each module is executed into a ModuleType and registered in sys.modules
    for p in order:
        # Use the processed text (with __file__ replacements already done)
        text = processed_modules[p.name]

        # module docstring for markdown
        try:
            tree = ast.parse(text)
            doc = ast.get_docstring(tree)
        except Exception:
            doc = None

        if doc:
            md = f"## {p.name}\n\n" + doc
            cells.append({
                'cell_type': 'markdown',
                'metadata': {'language': 'markdown'},
                'source': [md]
            })

        # Build a cell that creates a ModuleType, execs the module source into it,
        # and registers it in sys.modules so `import <module>` works in later cells.
        module_name = p.stem
        # Use triple-quoted string for readability, escaping backslashes and triple quotes.
        # We escape backslashes first so we don't double-escape the ones we add for quotes.
        escaped_text = text.replace('\\', '\\\\').replace('"""', '\\"\\"\\"')
        
        module_init_code = (
            f"# Module shim for: {p.name}\n"
            "import types, sys\n"
            "from pathlib import Path\n"
            f"_src = \"\"\"{escaped_text}\"\"\"\n"
            f"mod = types.ModuleType(\"{module_name}\")\n"
            f"mod.__file__ = str(Path.cwd() / \"{p.name}\")\n"
            "exec(_src, mod.__dict__)\n"
            f"sys.modules[\"{module_name}\"] = mod\n"
        )

        cells.append({
            'cell_type': 'code',
            'metadata': {'language': 'python'},
            'source': module_init_code.splitlines(True),
            'outputs': [],
            'execution_count': None
        })

    # Add a final cell to run the main pipeline if main.py exists
    run_main_code = (
        "# Run the main pipeline\n"
        "import sys, inspect\n"
        "if 'main' in sys.modules:\n"
        "    import main\n"
        "    print(\"🚀 Running available entrypoint in main module...\")\n"
        "    # Preferred entrypoints in order: test_full_pipeline, main, any test_* function\n"
        "    if hasattr(main, 'test_full_pipeline'):\n"
        "        main.test_full_pipeline()\n"
        "    elif hasattr(main, 'main'):\n"
        "        main.main()\n"
        "    else:\n"
        "        called = False\n"
        "        for name, obj in vars(main).items():\n"
        "            if callable(obj) and name.startswith('test_'):\n"
        "                print(f\"ℹ️ Calling {name}() from main module\")\n"
        "                try:\n"
        "                    obj()\n"
        "                    called = True\n"
        "                except Exception as e:\n"
        "                    print(f\"❌ Exception while running {name}(): {e}\")\n"
        "                break\n"
        "        if not called:\n"
        "            print(\"⚠️ No 'test_full_pipeline', 'main', or 'test_*' function found in main module.\")\n"
    )
    cells.append({
        'cell_type': 'code',
        'metadata': {'language': 'python'},
        'source': [run_main_code],
        'outputs': [],
        'execution_count': None
    })

    # Add a cell to display generated outputs
    display_outputs_code = (
        "# Display generated outputs\n"
        "import IPython\n"
        "from pathlib import Path\n"
        "\n"
        "output_dir = Path('outputs')\n"
        "exclusions = {'07_all_outputs.html', 'all_outputs.zip'}\n"
        "\n"
        "if output_dir.exists():\n"
        "    print(\"📊 Displaying generated outputs...\")\n"
        "\n"
        "    # 1. Text files\n"
        "    for txt in sorted(output_dir.glob('*.txt')):\n"
        "        if txt.name in exclusions: continue\n"
        "        print(f\"\\n📄 {txt.name}\")\n"
        "        print(\"-\" * 40)\n"
        "        print(txt.read_text(encoding='utf-8', errors='replace'))\n"
        "        print(\"-\" * 40)\n"
        "\n"
        "    # 2. PNG files\n"
        "    for png in sorted(output_dir.glob('*.png')):\n"
        "        if png.name in exclusions: continue\n"
        "        print(f\"\\n🖼️ {png.name}\")\n"
        "        IPython.display.display(IPython.display.Image(filename=str(png)))\n"
        "\n"
        "    # 3. HTML files\n"
        "    for html in sorted(output_dir.glob('*.html')):\n"
        "        if html.name in exclusions: continue\n"
        "        print(f\"\\n🌐 {html.name}\")\n"
        "        IPython.display.display(IPython.display.HTML(filename=str(html)))\n"
        "\n"
        "else:\n"
        "    print(\"⚠️ No 'outputs' directory found.\")\n"
    )

    cells.append({
        'cell_type': 'code',
        'metadata': {'language': 'python'},
        'source': display_outputs_code.splitlines(True),
        'outputs': [],
        'execution_count': None
    })

    nb = {
        'cells': cells,
        'metadata': {
            'language_info': {'name': 'python'}
        },
        'nbformat': 4,
        'nbformat_minor': 5
    }

    output.write_text(json.dumps(nb, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'Wrote notebook: {output}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', type=Path, default=Path('step6'), help='source directory containing .py files')
    parser.add_argument('--output', type=Path, default=Path('combined.ipynb'), help='output notebook path')
    parser.add_argument('--order-file', type=Path, default=Path('order.txt'), help='optional order file (one filename per line)')
    args = parser.parse_args()

    src = args.src
    # If the user left the default output filename, generate a timestamped name
    # based on the source folder (e.g. 'step1-combined-YYYYMMDD-HHMMSS.ipynb')
    output: Path = args.output
    if output.name == 'combined.ipynb':
        ts = datetime.now().strftime('%Y%m%d-%H%M%S')
        output = output.with_name(f"{src.name}-combined-{ts}.ipynb")
    if not src.exists() or not src.is_dir():
        print(f'Source directory not found: {src}', file=sys.stderr)
        sys.exit(2)

    # Clean up before generating
    notebook_dir = output.parent
    cleanup_directories(notebook_dir)

    files = find_py_files(src)
    if not files:
        print('No python files found under', src)
        sys.exit(1)

    # read optional order file
    order_list: List[Path] = []
    if args.order_file and args.order_file.exists():
        lines = [l.strip() for l in args.order_file.read_text(encoding='utf-8').splitlines() if l.strip()]
        for name in lines:
            p = src / name
            if p.exists():
                order_list.append(p)
            else:
                # try path as-is
                p2 = Path(name)
                if p2.exists():
                    order_list.append(p2)

    if order_list:
        print('Using explicit order from', args.order_file)
        order = order_list
    else:
        module_map, deps = build_dependency_graph(files)
        nodes = [p.stem for p in files]
        sorted_names = topo_sort(nodes, deps)
        if sorted_names:
            # map back to paths
            order = [module_map[n] for n in sorted_names]
            print('Using heuristic import-based order')
        else:
            order = sorted(files)
            print('Heuristic ordering failed; using alphabetical order')

    make_notebook(order, output)


if __name__ == '__main__':
    main()
