"""Build the route-chart lift graph G(C, S, l, A, b) for a chart on GF(q)^5.

C is the 144-vertex controller of arXiv:2606.15860 with the paper's own
inverse-consistent labeling (imported from the paper's supplementary
verify_candidate.py, which also re-checks that C is exact-NB-5 under it).
The vertex (u, x) with x = (x_0..x_4) in GF(q)^5 gets the integer label
u * q^5 + sum_i x_i q^i, as in the paper's generators.  For each controller
edge u -> v with forward symbol t in {a, b}, each x and each lambda in GF(q),
the edge {(u, x), (v, A_t x + lambda b_t)} is added (Definition A.4).

Usage: python3 build_graph.py CHART.json OUT.tsv.gz
Writes "n m" and then the sorted edges "u<TAB>v" (u < v), after checking that
the graph is loopless, has no repeated edge and is 4q-regular.
"""
import gzip
import json
import os
import sys

import numpy as np

PAPER_SCRIPTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir,
                             'anc', 'route_chart_clean_package', 'scripts', '12_5_34992')
sys.path.insert(0, os.path.abspath(PAPER_SCRIPTS))
sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)))

import verify_candidate as paper  # noqa: E402  (controller construction from the paper)
from gfq import GF  # noqa: E402


def controller_arcs():
    paper.verify_base_voltage_coverage()
    adj, cedges = paper.build_controller()
    color = paper.euler_2factor_coloring(adj, cedges)
    arc = paper.orient_two_factors(adj, cedges, color)
    paper.verify_labeled_nb5(adj, arc)
    oriented = []
    for u, v, _ in cedges:
        if arc[(u, v)] in (0, 2):
            oriented.append((u, v, arc[(u, v)]))
        elif arc[(v, u)] in (0, 2):
            oriented.append((v, u, arc[(v, u)]))
        else:
            raise RuntimeError('edge without a forward symbol')
    return len(adj), oriented


def main():
    chart_path, out = sys.argv[1], sys.argv[2]
    chart = json.load(open(chart_path))
    q = chart['q']
    F = GF(q)
    ADD = np.array(F.add, dtype=np.int64)
    MUL = np.array(F.mul, dtype=np.int64)
    Q = q ** 5

    nctrl, oriented = controller_arcs()
    print(f'controller: {nctrl} vertices, {len(oriented)} edges, exact-NB-5 under the paper labeling: OK')

    # all fiber vectors: X[k] = k-th coordinate of index x
    idx = np.arange(Q, dtype=np.int64)
    X = np.stack([(idx // q ** k) % q for k in range(5)])
    weights = np.array([q ** k for k in range(5)], dtype=np.int64)

    def apply(Amat, vecs):
        out = np.zeros_like(vecs)
        for i in range(5):
            s = np.zeros(vecs.shape[1], dtype=np.int64)
            for k in range(5):
                s = ADD[s, MUL[Amat[i][k], vecs[k]]]
            out[i] = s
        return out

    us, vs = [], []
    for tail, head, sym in oriented:
        AX = apply(chart['A'][sym], X)
        bt = chart['b'][sym]
        for lam in range(q):
            shift = np.array([F.mul[lam][c] for c in bt], dtype=np.int64)
            Y = ADD[AX, shift[:, None]]
            yidx = weights @ Y
            us.append(tail * Q + idx)
            vs.append(head * Q + yidx)
    U = np.concatenate(us)
    V = np.concatenate(vs)
    n, m = nctrl * Q, U.size
    assert np.all(U != V), 'loop'
    lo, hi = np.minimum(U, V), np.maximum(U, V)
    key = lo * n + hi
    order = np.argsort(key, kind='stable')
    key, lo, hi = key[order], lo[order], hi[order]
    assert np.all(key[1:] != key[:-1]), 'repeated edge'
    deg = np.bincount(lo, minlength=n) + np.bincount(hi, minlength=n)
    assert deg.min() == deg.max() == 4 * q, (deg.min(), deg.max())
    print(f'graph: {n} vertices, {m} edges, simple, all degrees {4 * q}')

    with gzip.open(out, 'wt', compresslevel=6) as fh:
        fh.write(f'{n} {m}\n')
        chunk = 500000
        for s in range(0, m, chunk):
            fh.write('\n'.join(f'{a}\t{b}' for a, b in zip(lo[s:s + chunk].tolist(), hi[s:s + chunk].tolist())))
            fh.write('\n')
    print(f'wrote {out}')


if __name__ == '__main__':
    main()
