"""Export the 144-vertex controller of arXiv:2606.15860 as four permutation
tables, with a reduced word of length 5 for every ordered pair of vertices.

The controller, its 2-factor colouring and the orientation that labels every
arc with a symbol (0 = a, 1 = a^-1, 2 = b, 3 = b^-1) are imported unchanged from
the paper's supplementary verify_candidate.py.  sigma[t][u] is the head of the
arc with symbol t leaving u.  For each ordered pair (u, v) the certificate is a
word t1..t5, encoded as t1 + 4 t2 + 16 t3 + 64 t4 + 256 t5, with t_{i+1} not
the inverse of t_i and sigma[t5](...sigma[t1](u)...) = v.

Usage: python3 export_controller.py OUT.json
"""
import json
import os
import sys
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))
PAPER = os.path.join(HERE, os.pardir, os.pardir, 'anc', 'route_chart_clean_package', 'scripts', '12_5_34992')
sys.path.insert(0, os.path.abspath(PAPER))
import verify_candidate as paper  # noqa: E402

INV = [1, 0, 3, 2]


def main():
    out = sys.argv[1]
    paper.verify_base_voltage_coverage()
    adj, cedges = paper.build_controller()
    color = paper.euler_2factor_coloring(adj, cedges)
    arc = paper.orient_two_factors(adj, cedges, color)
    paper.verify_labeled_nb5(adj, arc)
    n = len(adj)
    sigma = [[None] * n for _ in range(4)]
    for (u, v), s in arc.items():
        assert sigma[s][u] is None
        sigma[s][u] = v
    assert all(x is not None for row in sigma for x in row)
    for t in range(4):
        for u in range(n):
            assert sigma[INV[t]][sigma[t][u]] == u

    words = [w for w in product(range(4), repeat=5) if all(w[i + 1] != INV[w[i]] for i in range(4))]
    assert len(words) == 324
    cert = [[None] * n for _ in range(n)]
    for u in range(n):
        for w in words:
            x = u
            for t in w:
                x = sigma[t][x]
            if cert[u][x] is None:
                cert[u][x] = sum(t * 4 ** i for i, t in enumerate(w))
    missing = sum(c is None for row in cert for c in row)
    assert missing == 0, f'{missing} pairs without a reduced word of length 5'

    json.dump({'vertices': n,
               'symbols': '0 = a, 1 = a^-1, 2 = b, 3 = b^-1 (inverse pairs 0<->1, 2<->3)',
               'source': 'arXiv:2606.15860 supplementary route_chart_clean_package/scripts/12_5_34992/verify_candidate.py '
                         '(build_controller, euler_2factor_coloring, orient_two_factors)',
               'sigma': sigma,
               'word_code': 't1 + 4*t2 + 16*t3 + 64*t4 + 256*t5',
               'certificates': cert}, open(out, 'w'))
    print(f'controller: {n} vertices; sigma tables and {n * n} word certificates written to {out}')


if __name__ == '__main__':
    main()
