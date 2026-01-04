#!/usr/bin/env python3
"""
tools/build_import_graph.py

Scan Python files in a step folder and build a simple import graph.

Usage examples:
  python tools/build_import_graph.py step2
  python tools/build_import_graph.py step3 --root v251130-simple-from-colab-then-restructure-in-steps --json > step3_graph.json

The script prints lines of the form:
  step2/main.py -> ['os', 'sys', 'pandas']

Or when `--json` is passed it writes a JSON object mapping relative
file paths to lists of imported module names.
"""

from __future__ import annotations
import argparse
import ast
import json
import os
import sys
from collections import defaultdict
from typing import Dict, List


def build_import_graph(path: str, recursive: bool = False) -> Dict[str, List[str]]:
    graph: Dict[str, List[str]] = defaultdict(list)

    if not os.path.exists(path):
        raise FileNotFoundError(path)

    for root, dirs, files in os.walk(path):
        # skip caches
        if "__pycache__" in root:
            continue
        for f in files:
            if not f.endswith(".py"):
                continue
            full = os.path.join(root, f)
            try:
                with open(full, "r", encoding="utf-8") as fh:
                    src = fh.read()
            except Exception as e:
                print(f"WARN: could not read {full}: {e}", file=sys.stderr)
                continue

            try:
                tree = ast.parse(src)
            except SyntaxError as e:
                print(f"WARN: syntax error in {full}: {e}", file=sys.stderr)
                continue

            rel = os.path.relpath(full, path)

            imports: List[str] = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        # record top-level name (e.g. 'os.path' -> 'os.path')
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    mod = node.module if node.module else ""
                    if node.level:
                        # indicate relative imports with leading dots (e.g. '..module')
                        mod = ("." * node.level) + (mod or "")
                    imports.append(mod or "(relative)")

            # dedupe while preserving order
            seen = set()
            deduped = []
            for i in imports:
                if i not in seen:
                    deduped.append(i)
                    seen.add(i)

            graph[rel] = deduped

        if not recursive:
            break

    return dict(graph)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build import graph for a step folder")
    parser.add_argument("step", help="Step folder name (e.g. step2) or path to folder")
    parser.add_argument(
        "--root",
        default="v251130-simple-from-colab-then-restructure-in-steps",
        help="Base folder that contains the step folders (default: %(default)s)",
    )
    parser.add_argument("--recursive", action="store_true", help="Recurse into subdirectories")
    parser.add_argument("--json", action="store_true", help="Output JSON mapping file->imports")
    parser.add_argument("--dot", action="store_true", help="Output Graphviz DOT to stdout")
    parser.add_argument("--dot-file", help="Write Graphviz DOT to a file")

    args = parser.parse_args()

    # Resolve target path
    if os.path.isabs(args.step) or os.sep in args.step:
        target = args.step
    else:
        target = os.path.join(args.root, args.step)

    try:
        graph = build_import_graph(target, recursive=args.recursive)
    except FileNotFoundError:
        print(f"Target folder not found: {target}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(graph, indent=2))
    else:
        for file, deps in sorted(graph.items()):
            print(f"{file} -> {deps}")

    if args.dot or args.dot_file:
        # Build DOT: files as boxes, modules as ellipses
        def safe_id(s: str) -> str:
            # Make a safe DOT id by replacing non-alphanum with underscore
            return 'n_' + ''.join(c if c.isalnum() else '_' for c in s)

        lines = ["digraph imports {", "  rankdir=LR;", "  node [fontname=\"DejaVu Sans\"];"]
        # define file nodes
        for file in sorted(graph.keys()):
            nid = safe_id(file)
            lines.append(f'  {nid} [label="{file}", shape=box, style=filled, fillcolor=lightgrey];')

        # collect module nodes
        modules = set(m for deps in graph.values() for m in deps)
        for mod in sorted(modules):
            mid = safe_id(mod)
            lines.append(f'  {mid} [label="{mod}", shape=ellipse, style=filled, fillcolor=white];')

        # edges
        for file, deps in sorted(graph.items()):
            fid = safe_id(file)
            for mod in deps:
                mid = safe_id(mod)
                lines.append(f'  {fid} -> {mid};')

        lines.append('}')
        dot = '\n'.join(lines)
        if args.dot:
            print(dot)
        if args.dot_file:
            with open(args.dot_file, 'w', encoding='utf-8') as fh:
                fh.write(dot)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
