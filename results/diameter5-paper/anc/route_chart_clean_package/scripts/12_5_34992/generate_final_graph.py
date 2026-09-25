#!/usr/bin/env python3
"""(12,5): regenerate the final edge list from the route-chart lift.

Using the 144-vertex controller and the GF(3)^5 chart that verify_candidate.py
checks, this reproduces the exact contents of
graphs/12_5_34992/final_graph_edges.tsv.gz.

Output format: gzip-compressed TSV. Line 1 is the header "n m"; every other
line is one undirected edge "u<TAB>v" with u < v, edges in ascending order.

Usage:
    python3 generate_final_graph.py [OUTPUT_PATH]
        Defaults to ./final_graph_edges.tsv.gz. A path not ending in .gz is
        written uncompressed.
"""
import sys
import gzip
from collections import Counter
from verify_candidate import (
    Q, A, B, mv,
    build_controller, euler_2factor_coloring, orient_two_factors,
)

FIB = Q ** 5  # |GF(3)^5| = 243


def dec(n):
    """Expand an integer into a GF(3)^5 vector (5 entries, least significant first)."""
    v = []
    for _ in range(5):
        v.append(n % Q)
        n //= Q
    return v


def enc(v):
    """Pack a GF(3)^5 vector back into an integer (inverse of dec)."""
    n = 0
    p = 1
    for x in v:
        n += x * p
        p *= Q
    return n


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else 'final_graph_edges.tsv.gz'

    # Build the controller and assign a symbol su to each arc via the 2-factor coloring.
    adj, cedges = build_controller()
    color = euler_2factor_coloring(adj, cedges)
    arc = orient_two_factors(adj, cedges, color)
    nctrl = len(adj)
    n = nctrl * FIB

    # For each controller edge (u < v), the fiber chart adds Q = 3 lifted edges.
    edges = set()
    for u in range(nctrl):
        for v, _eid in adj[u]:
            if u < v:
                su = arc[(u, v)]
                for xi in range(FIB):
                    Ax = mv(A[su], dec(xi))
                    for lam in range(Q):
                        yvec = [(Ax[i] + lam * B[su][i]) % Q for i in range(5)]
                        a = u * FIB + xi
                        b = v * FIB + enc(yvec)
                        if a > b:
                            a, b = b, a
                        edges.add((a, b))

    # Degree check: no self-loops, every vertex 12-regular.
    deg = Counter()
    for a, b in edges:
        assert a != b, 'self-loop'
        deg[a] += 1
        deg[b] += 1
    assert len(deg) == n, (len(deg), n)
    assert min(deg.values()) == max(deg.values()) == 12, \
        (min(deg.values()), max(deg.values()))

    opener = gzip.open if out.endswith('.gz') else open
    with opener(out, 'wt') as f:
        f.write(f'{n} {len(edges)}\n')
        for a, b in sorted(edges):
            f.write(f'{a}\t{b}\n')
    print(f'Wrote {out}: {n} vertices, {len(edges)} edges, all degrees 12.')


if __name__ == '__main__':
    main()
