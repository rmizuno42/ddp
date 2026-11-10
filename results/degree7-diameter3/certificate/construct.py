#!/usr/bin/env python3
"""Construct the graph of order 171, maximum degree 7 and diameter 3 from its Z_9 voltage description.

Base graph B (19 vertices): hub 0; core vertices 1..12; spoke vertices 13..18.
Voltage group Z_9.  Vertex (u, x), u in B, x in Z_9, has ID 9u + x.
A base edge u - v (u < v) with voltage a joins (u, x) to (v, x + a) for every x.
A loop at u with voltage a joins (u, x) to (u, x + a) (hence also to (u, x - a)).
The 9 vertices (0, x) have degree 6; all other vertices have degree 7.

    python3 construct.py --out DIR      writes DIR/graph.edges and DIR/graph.adjlist
    python3 construct.py --check        compares with the published graph.edges and graph.adjlist
Standard library only.
"""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
M = 9
K = 19

# hub-spoke edges
HUB = [(0, 13, 5), (0, 14, 5), (0, 15, 2), (0, 16, 2), (0, 17, 8), (0, 18, 8)]
# spoke pairs (double edges with voltages 3 and 6) and spoke loops
SPOKE_PAIRS = [(13, 14, 3), (13, 14, 6), (15, 16, 3), (15, 16, 6), (17, 18, 3), (17, 18, 6)]
LOOPS = [(13, 1), (14, 1), (15, 4), (16, 4), (17, 2), (18, 2)]
# spoke-core edges
SPOKE_CORE = [(8, 13, 1), (11, 13, 1), (2, 14, 1), (5, 14, 1), (6, 15, 4), (12, 15, 4),
              (3, 16, 4), (9, 16, 4), (4, 17, 7), (7, 17, 7), (1, 18, 7), (10, 18, 7)]
# core edges (the six double edges are listed twice with different voltages)
CORE = [(1, 5, 8), (1, 6, 5), (1, 8, 7), (1, 10, 2), (1, 10, 7), (1, 12, 7),
        (2, 4, 1), (2, 5, 8), (2, 5, 1), (2, 7, 2), (2, 9, 5), (2, 12, 1),
        (3, 4, 4), (3, 8, 4), (3, 9, 5), (3, 9, 4), (3, 10, 2), (3, 11, 8),
        (4, 7, 2), (4, 7, 7), (4, 9, 7), (4, 11, 7),
        (5, 9, 1), (5, 10, 2), (5, 12, 5),
        (6, 7, 2), (6, 8, 8), (6, 11, 4), (6, 12, 5), (6, 12, 4),
        (7, 11, 8), (7, 12, 5),
        (8, 10, 1), (8, 11, 8), (8, 11, 1),
        (9, 10, 4)]
BASE_EDGES = HUB + SPOKE_PAIRS + SPOKE_CORE + CORE
assert len(CORE) == 36 and len(BASE_EDGES) == 60 and len(LOOPS) == 6


def build():
    edges = set()
    for u, v, a in BASE_EDGES:
        assert u < v
        for x in range(M):
            p, q = M * u + x, M * v + (x + a) % M
            e = (min(p, q), max(p, q))
            assert e not in edges, 'parallel edge'
            edges.add(e)
    for u, a in LOOPS:
        assert a % M != 0 and (2 * a) % M != 0
        for x in range(M):
            p, q = M * u + x, M * u + (x + a) % M
            e = (min(p, q), max(p, q))
            assert e not in edges, 'parallel edge'
            edges.add(e)
    n = K * M
    adj = [[] for _ in range(n)]
    for p, q in edges:
        adj[p].append(q)
        adj[q].append(p)
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
    degs = sorted(set(len(a) for a in adj))
    assert degs == [6, 7] and all(len(adj[9 * 0 + x]) == 6 for x in range(M))
    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)
        (args.out / 'graph.edges').write_text(et)
        (args.out / 'graph.adjlist').write_text(at)
    if args.json:
        args.json.write_text(json.dumps({
            'voltage_group': 'Z9', 'base_vertices': K, 'vertex_id': '9*u + x',
            'edge_rule': '(u,x) ~ (v,x+a) for base edge u-v (u<v) with voltage a; loop at u with voltage a: (u,x) ~ (u,x+a)',
            'base_edges': [{'u': u, 'v': v, 'voltage': a} for u, v, a in BASE_EDGES],
            'loops': [{'u': u, 'voltage': a} for u, a in LOOPS]}, indent=1) + '\n')
    if args.check:
        assert (HERE / 'graph.edges').read_text() == et, 'graph.edges differs from the construction'
        assert (HERE / 'graph.adjlist').read_text() == at, 'graph.adjlist differs from the construction'
    print(f"n={n} m={len(edges)} degrees={degs} sha256(graph.edges)={hashlib.sha256(et.encode()).hexdigest()}")


if __name__ == '__main__':
    main()
