#!/usr/bin/env python3
"""
Render import graph for a step folder to an SVG using NetworkX+Matplotlib.

This does not require the Graphviz `dot` binary; it uses matplotlib to
layout and render the graph. It's best-effort and intended for quick
visual checks.

Usage:
  python tools/render_import_graph_svg.py step3 --out step3_imports.svg
"""

from __future__ import annotations
import argparse
import os
import sys
from typing import Dict, List

try:
    import networkx as nx
    import matplotlib.pyplot as plt
except Exception:
    print("Required packages (networkx, matplotlib) not found. Please run: pip install networkx matplotlib", file=sys.stderr)
    raise

# import the build_import_graph function from our tools
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from build_import_graph import build_import_graph


def draw_graph(graph: Dict[str, List[str]], out_path: str) -> None:
    G = nx.DiGraph()

    # Add file nodes and module nodes separately
    for file in graph:
        G.add_node(file, type='file')
    modules = set(m for deps in graph.values() for m in deps)
    for m in modules:
        G.add_node(m, type='module')

    for f, deps in graph.items():
        for m in deps:
            G.add_edge(f, m)

    # Position with bipartite like layout: files on left, modules on right
    files = [n for n, d in G.nodes(data=True) if d.get('type') == 'file']
    mods = [n for n, d in G.nodes(data=True) if d.get('type') == 'module']

    pos = {}
    # vertical spacing
    def col_positions(nodes, x):
        h = len(nodes)
        if h == 0:
            return {}
        ys = list(range(h))[::-1]
        return {n: (x, ys[i]) for i, n in enumerate(nodes)}

    pos.update(col_positions(files, 0))
    pos.update(col_positions(mods, 1))

    plt.figure(figsize=(10, max(4, len(files) * 0.5)))
    # draw nodes
    nx.draw_networkx_nodes(G, pos, nodelist=files, node_shape='s', node_color='lightgrey', node_size=1600)
    nx.draw_networkx_nodes(G, pos, nodelist=mods, node_shape='o', node_color='white', node_size=1200)
    nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle='->')
    # labels
    labels = {n: os.path.basename(n) if '/' in n or '\\\\' in n else n for n in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=8)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(out_path, format='svg')
    plt.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('step')
    parser.add_argument('--root', default='v251130-simple-from-colab-then-restructure-in-steps')
    parser.add_argument('--recursive', action='store_true')
    parser.add_argument('--out', default=None, help='Output SVG path')
    args = parser.parse_args()

    if os.path.isabs(args.step) or os.sep in args.step:
        target = args.step
    else:
        target = os.path.join(args.root, args.step)

    if not os.path.exists(target):
        print(f"Target folder not found: {target}", file=sys.stderr)
        return 2

    graph = build_import_graph(target, recursive=args.recursive)
    out = args.out or f"{args.step}_imports.svg"
    draw_graph(graph, out)
    print(f"Wrote {out}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
