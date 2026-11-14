"""Independent Python checks of the data in ../data (no Lean, no search code).

1. Controller: sigma[inv t][sigma[t][u]] = u, and every certificate word is
   reduced and leads from u to v (all 144 x 144 ordered pairs).
2. Every chart in data/charts/gf<q>.json: relations (A.1) and rank 5 for all 324
   controllability matrices (verify_chart.py).
3. Integer charts: relations (A.1) over Z, all 324 determinants nonzero, and the
   primes dividing all six products of determinants (intchart.py).
4. Optional (--f2): the exhaustive search showing that no universal chart exists
   on GF(2)^5 (compiles and runs f2exhaust.c; about 30 s on 8 cores).

Usage: python3 verify_all.py [--f2]
"""
import glob
import json
import os
import subprocess
import sys
import tempfile
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, os.pardir, 'data')
sys.path.insert(0, HERE)

from verify_chart import check_chart  # noqa: E402
import intchart  # noqa: E402

INV = [1, 0, 3, 2]


def check_controller():
    c = json.load(open(os.path.join(DATA, 'controller.json')))
    n, sigma, cert = c['vertices'], c['sigma'], c['certificates']
    for t in range(4):
        for u in range(n):
            assert sigma[INV[t]][sigma[t][u]] == u
    for u in range(n):
        for v in range(n):
            w = [(cert[u][v] >> (2 * i)) & 3 for i in range(5)]
            assert all(w[i + 1] != INV[w[i]] for i in range(4)), (u, v, w)
            x = u
            for t in w:
                x = sigma[t][x]
            assert x == v, (u, v, w)
    print(f'controller: {n} vertices; inverse arcs and {n * n} certificate words: OK')


def check_charts():
    paths = sorted(glob.glob(os.path.join(DATA, 'charts', 'gf*.json')),
                   key=lambda p: int(os.path.basename(p)[2:-5]))
    for path in paths:
        chart = json.load(open(path))
        nwords, min_rank, bad = check_chart(chart)
        assert not bad, f'{path}: {len(bad)} singular words'
        print(f'chart over GF({chart["q"]}): {nwords} reduced words, min rank {min_rank}: OK')


def check_integer_charts():
    g = intchart.analyse(os.path.join(DATA, 'charts', 'integer_charts.json'))
    fs, cof = intchart.small_prime_factors(g)
    assert cof == 1 and max(fs) <= 79 and 43 not in fs
    print('integer charts: every prime > 79, and 43, is good for one of the six charts: OK')


def run_f2():
    with tempfile.TemporaryDirectory() as tmp:
        exe = os.path.join(tmp, 'f2exhaust')
        subprocess.run(['cc', '-O3', '-o', exe, os.path.join(HERE, 'f2exhaust.c')], check=True)
        procs = [subprocess.Popen([exe, str(f)], stdout=subprocess.PIPE, text=True) for f in range(16)]
        total = 0
        for p in procs:
            out = p.communicate()[0]
            total += int(out.strip().rsplit(' ', 1)[1])
        assert total == 0
    print('GF(2): exhaustive search over the 16 companion classes: no universal chart: OK')


def main():
    check_controller()
    check_charts()
    check_integer_charts()
    if '--f2' in sys.argv:
        run_f2()
    print('ALL CHECKS PASSED')


if __name__ == '__main__':
    main()
