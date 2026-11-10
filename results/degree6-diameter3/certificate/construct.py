#!/usr/bin/env python3
"""Construct the 6-regular graph of order 126 and diameter 3 from its voltage description.

Base graph B (14 vertices): hubs h=0, h'=1; A = {a_0,a_1,a_2} = {2,3,4} adjacent to h;
B = {b_0,b_1,b_2} = {5,6,7}; A' = {8,9,10} adjacent to h'; B' = {11,12,13}.
Voltage group N = Z_3 x Z_3.  Vertex (u, x) with u in B and x = (x0, x1) in N has ID 9u + 3*x0 + x1.
A base edge u -> v with voltage g joins (u, x) to (v, x + g) for every x in N.

    python3 construct.py --out DIR      writes DIR/graph.edges and DIR/graph.adjlist
    python3 construct.py --check        compares with the published graph.edges and graph.adjlist
Standard library only.
"""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

# (u, v, [voltages]) ; each voltage gives one base edge u -> v.
BASE_EDGES = [
    (0, 1, [(0, 0), (1, 1), (2, 1)]),          # hub bundle: the parabola {(t, t^2)}
    (0, 2, [(0, 0)]), (0, 3, [(0, 0)]), (0, 4, [(0, 0)]),
    (2, 3, [(0, 2)]), (2, 4, [(0, 1)]), (3, 4, [(0, 2)]),      # triangle A: a_l -> a_m : (m-l)(0,2)
    (2, 5, [(0, 0)]), (2, 6, [(0, 0)]), (2, 7, [(0, 0)]),      # a_l -> b_j : l * w_j
    (3, 5, [(2, 0)]), (3, 6, [(1, 1)]), (3, 7, [(1, 0)]),      # w = (2,0), (1,1), (1,0)
    (4, 5, [(1, 0)]), (4, 6, [(2, 2)]), (4, 7, [(2, 0)]),
    (1, 8, [(0, 0)]), (1, 9, [(0, 0)]), (1, 10, [(0, 0)]),     # second half: same voltages
    (8, 9, [(0, 2)]), (8, 10, [(0, 1)]), (9, 10, [(0, 2)]),
    (8, 11, [(0, 0)]), (8, 12, [(0, 0)]), (8, 13, [(0, 0)]),
    (9, 11, [(2, 0)]), (9, 12, [(1, 1)]), (9, 13, [(1, 0)]),
    (10, 11, [(1, 0)]), (10, 12, [(2, 2)]), (10, 13, [(2, 0)]),
    (5, 11, [(2, 2), (0, 2), (0, 1)]),        # bundles b_j - b'_j
    (6, 12, [(2, 0), (2, 1), (1, 2)]),
    (7, 13, [(1, 0), (0, 0), (0, 2)]),
]
K, Q = 14, 3
N = [(a, b) for a in range(Q) for b in range(Q)]


def vid(u, x):
    return 9 * u + 3 * x[0] + x[1]


def build():
    edges = set()
    for u, v, gs in BASE_EDGES:
        for g in gs:
            for x in N:
                y = ((x[0] + g[0]) % Q, (x[1] + g[1]) % Q)
                a, b = vid(u, x), vid(v, y)
                assert a != b, 'loop'
                e = (min(a, b), max(a, b))
                assert e not in edges, 'parallel edge'
                edges.add(e)
    n = K * Q * Q
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    return n, sorted(edges), [sorted(x) for x in adj]


def texts(n, edges, adj):
    et = f"{n} {len(edges)}\n" + "".join(f"{a} {b}\n" for a, b in edges)
    at = "".join(f"{i} " + " ".join(map(str, adj[i])) + "\n" for i in range(n))
    return et, at


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--out', type=Path)
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--json', type=Path, help='also write the voltage description as JSON')
    args = ap.parse_args()
    n, edges, adj = build()
    et, at = texts(n, edges, adj)
    assert all(len(a) == 6 for a in adj)
    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)
        (args.out / 'graph.edges').write_text(et)
        (args.out / 'graph.adjlist').write_text(at)
    if args.json:
        args.json.write_text(json.dumps({
            'voltage_group': 'Z3 x Z3 (pairs (x0,x1) mod 3)', 'base_vertices': K,
            'vertex_id': '9*u + 3*x0 + x1',
            'edge_rule': '(u,x) ~ (v,x+g) for each listed voltage g of the base edge u-v',
            'base_edges': [{'u': u, 'v': v, 'voltages': [list(g) for g in gs]} for u, v, gs in BASE_EDGES]},
            indent=1) + '\n')
    if args.check:
        assert (HERE / 'graph.edges').read_text() == et, 'graph.edges differs from the construction'
        assert (HERE / 'graph.adjlist').read_text() == at, 'graph.adjlist differs from the construction'
    print(f"n={n} m={len(edges)} degree=6 sha256(graph.edges)={hashlib.sha256(et.encode()).hexdigest()}")


if __name__ == '__main__':
    main()
