#!/usr/bin/env python3
"""(16,5): regenerate the final edge list from the route-chart lift.

Using the 144-vertex controller and the GF(4)^5 chart that verify_candidate.py
checks, this reproduces the exact contents of
graphs/16_5_147456/final_graph_edges.tsv.gz.

Output format: gzip-compressed TSV. Line 1 is the header "n m"; every other
line is one undirected edge "u<TAB>v" with u < v.

Usage:
    python3 generate_final_graph.py [OUTPUT_PATH]
        Defaults to ./final_graph_edges.tsv.gz. A path not ending in .gz is
        written uncompressed.
"""
import sys
import gzip
from verify_candidate import (
    A, B, MUL,
    build_controller, euler_2factor_coloring, orient_two_factors,
)

FIB = 4 ** 5  # |GF(4)^5| = 1024


def idx_to_vec(x):
    """Expand an integer into a GF(4)^5 vector (5 entries, 2 bits each)."""
    v = []
    for _ in range(5):
        v.append(x & 3)
        x >>= 2
    return v


def vec_to_idx(v):
    """Pack a GF(4)^5 vector back into an integer (inverse of idx_to_vec)."""
    x = 0
    for i, a in enumerate(v):
        x |= (a & 3) << (2 * i)
    return x


def mv(M, v):
    """Matrix-times-vector over GF(4) (products via MUL, sums via XOR)."""
    out = []
    for row in M:
        z = 0
        for a, b in zip(row, v):
            z ^= MUL[a][b]
        out.append(z)
    return out


def add_scaled(v, lam, b):
    """Compute v + lam*b over GF(4)."""
    return [v[i] ^ MUL[lam][b[i]] for i in range(5)]


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else 'final_graph_edges.tsv.gz'

    # Build the controller and assign a symbol to each arc via the 2-factor coloring.
    adj, cedges = build_controller()
    color = euler_2factor_coloring(adj, cedges)
    arc = orient_two_factors(adj, cedges, color)

    # Orient each controller edge in its forward-symbol direction (a or b, i.e. 0 or 2).
    oriented = []
    for u, v, _ in cedges:
        su = arc[(u, v)]
        sv = arc[(v, u)]
        if su in (0, 2):
            tail, head, sym = u, v, su
        elif sv in (0, 2):
            tail, head, sym = v, u, sv
        else:
            raise RuntimeError('no forward orientation')
        oriented.append((tail, head, sym))

    n_final = len(adj) * FIB
    m_final = len(cedges) * FIB * 4
    deg = [0] * n_final
    seen = set()

    # For each controller edge (tail->head, symbol sym), the chart adds 4 lifted edges.
    opener = gzip.open if out.endswith('.gz') else open
    with opener(out, 'wt') as f:
        f.write(f'{n_final} {m_final}\n')
        for tail, head, sym in oriented:
            M = A[sym]
            b = B[sym]
            for xidx in range(FIB):
                Ax = mv(M, idx_to_vec(xidx))
                U = tail * FIB + xidx
                for lam in range(4):
                    yidx = vec_to_idx(add_scaled(Ax, lam, b))
                    V = head * FIB + yidx
                    if U == V:
                        raise RuntimeError('self loop')
                    key = (U, V) if U < V else (V, U)
                    if key in seen:
                        raise RuntimeError(f'duplicate edge {key}')
                    seen.add(key)
                    deg[U] += 1
                    deg[V] += 1
                    f.write(f'{key[0]}\t{key[1]}\n')

    assert len(seen) == m_final, (len(seen), m_final)
    assert min(deg) == max(deg) == 16, (min(deg), max(deg))
    print(f'Wrote {out}: {n_final} vertices, {m_final} edges, all degrees 16.')


if __name__ == '__main__':
    main()
