#!/usr/bin/env python3
"""
Independently verify the order / degree / diameter of an edge list using igraph.

Usage:
    python3 verify_with_igraph.py <edge_file.tsv.gz> <n> <d> [<k>]

Examples:
    python3 verify_with_igraph.py final_graph_edges.tsv.gz 34992 12
    python3 verify_with_igraph.py final_graph_edges.tsv.gz 147456 16

Arguments:
    edge_file : edge list to verify (gzip-compressed TSV). Line 1 is "n m",
                every other line is "u<TAB>v".
    n         : claimed number of vertices
    d         : claimed degree (Delta)
    k         : claimed diameter upper bound (default 5)

Checks (any single violation stops with an AssertionError):
    1. no self-loops                          (u != v on every file line)
    2. file edge count == header m
    3. simple graph (no self-loops, no parallel edges)   (G.is_simple())
    4. order (G.vcount()) == n
    5. every vertex has degree == d  (= Delta-regular)
    6. 2 * m == n * d   (handshake)
    7. connected (G.is_connected()) and diameter (G.diameter()) <= k
"""

import sys
import gzip
import igraph as ig


def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)

    edge_file = sys.argv[1]
    n_expected = int(sys.argv[2])
    d_expected = int(sys.argv[3])
    k_expected = int(sys.argv[4]) if len(sys.argv) >= 5 else 5

    # ---- 1. read the file ----
    print(f'reading: {edge_file}')
    edges = []
    with gzip.open(edge_file, 'rt') as f:
        n_hdr, m_hdr = map(int, f.readline().split())
        print(f'  header: n={n_hdr}, m={m_hdr}')
        for line in f:
            u_str, v_str = line.split('\t')
            u, v = int(u_str), int(v_str)
            assert u != v, f'self-loop at vertex {u}'
            edges.append((u, v))

    assert len(edges) == m_hdr, (
        f'file edge count {len(edges)} != header m={m_hdr}'
    )

    # ---- 2. build the igraph graph ----
    # Passing n=n_expected pre-creates vertices 0..n-1, so isolated vertices are
    # included too. ig.Graph is undirected by default.
    G = ig.Graph(n=n_expected, edges=edges)

    # ---- 3. simple graph (no self-loops, no parallel edges) ----
    # igraph keeps parallel edges and self-loops as given, so is_simple() detects
    # them.
    assert G.is_simple(), 'not a simple graph (self-loop or duplicate edge)'

    # ---- 4. order ----
    assert G.vcount() == n_expected, (
        f'order = {G.vcount()} != {n_expected}'
    )

    # ---- 5. degree: Delta-regular ----
    degs = G.degree()
    assert min(degs) == max(degs) == d_expected, (
        f'degree range [{min(degs)}, {max(degs)}] != {d_expected}'
    )

    # ---- 6. handshake ----
    assert 2 * G.ecount() == G.vcount() * d_expected

    print(f'  order      = {G.vcount()}')
    print(f'  edges      = {G.ecount()}')
    print(f'  degree     = {d_expected} (regular)')
    print(f'  simple     = yes (no self-loops, no duplicate edges)')

    # ---- 7. diameter ----
    # "diameter <= k" is only meaningful when the graph is connected, and igraph's
    # diameter() would otherwise return the longest shortest path *within a
    # component* on a disconnected graph. So check connectivity first; for a
    # connected graph diameter() returns the EXACT diameter (not an approximation).
    assert G.is_connected(), 'graph is disconnected'
    print(f'  computing diameter (ig.Graph.diameter) ...')
    diam = G.diameter()
    assert diam <= k_expected, f'diameter = {diam} > {k_expected}'

    print(f'  diameter   = {diam} (<= {k_expected})')
    print()
    print('PASS')


if __name__ == '__main__':
    main()
