#!/usr/bin/env python3
"""Check the spanning-tree certificate for diameter <= 3 (standard library only).

certificates/base_trees.json holds one tree per base vertex u, rooted at the fibre
representative (u, 0).  Every parent edge is checked against the construction formula, and
every depth is at most 3.  Translations (u, x) -> (u, x + c) are automorphisms, so the tree
rooted at (u, 0) translates to a depth-3 tree at every (u, c); hence every pair of vertices
is at distance at most 3.
"""
import json
from pathlib import Path

import construct

HERE = Path(__file__).resolve().parent


def main():
    n, edges, adj = construct.build()
    E = set(edges)
    cert = json.loads((HERE / 'certificates' / 'base_trees.json').read_text())
    radius, fib = cert['radius'], cert['fibre_size']
    assert radius == 3 and n % fib == 0
    roots = sorted(t['root'] for t in cert['trees'])
    assert roots == [fib * u for u in range(n // fib)], 'one tree per fibre representative'
    for t in cert['trees']:
        r, par, dep = t['root'], t['parent'], t['depth']
        assert len(par) == n and len(dep) == n and par[r] == r and dep[r] == 0
        for v in range(n):
            if v == r:
                continue
            p = par[v]
            assert (min(p, v), max(p, v)) in E, f'tree edge {p}-{v} is not an edge'
            assert dep[v] == dep[p] + 1 and 1 <= dep[v] <= radius
    # translation invariance of the edge set (the automorphisms used in the argument)
    for c in range(construct.M):
        def tr(w):
            return 9 * (w // 9) + (w % 9 + c) % 9
        for a, b in edges:
            p, q = tr(a), tr(b)
            assert (min(p, q), max(p, q)) in E
    print(f"PASS: {len(cert['trees'])} trees of depth <= {radius}; translations preserve all {len(edges)} edges")


if __name__ == '__main__':
    main()
