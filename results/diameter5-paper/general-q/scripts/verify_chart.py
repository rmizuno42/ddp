"""Independent check that a route chart on GF(q)^5 is universal.

Checks, in pure Python with gfq.GF arithmetic:
  * A_0 A_1 = A_1 A_0 = I and A_2 A_3 = A_3 A_2 = I        (A_{t^-1} = A_t^{-1})
  * b_1 = A_1 b_0 and b_3 = A_3 b_2                         (b_{t^-1} = A_t^{-1} b_t)
  * for all 324 reduced words t1..t5 over {0,1,2,3} (0<->1, 2<->3 inverse),
    M_w = [A_t5..A_t2 b_t1 | ... | A_t5 b_t4 | b_t5] has rank 5.

Usage: python3 verify_chart.py CHART.json [CHART.json ...]
The JSON object has keys "q", "A" (four 5x5 matrices) and "b" (four 5-vectors),
with field elements encoded as in gfq.py.
"""
import json
import sys
from itertools import product

from gf2k import GF2k
from gfq import GF, factor_prime_power

SINV = {0: 1, 1: 0, 2: 3, 3: 2}


def reduced_words(length=5):
    return [w for w in product(range(4), repeat=length)
            if all(w[i + 1] != SINV[w[i]] for i in range(length - 1))]


def controllability_columns(F, A, b, w):
    """Columns of M_w in the order of (A.2): A_t5..A_t2 b_t1, ..., b_t5."""
    cols = []
    suffix = F.identity(5)                      # A_t5 ... A_t(j+1)
    for t in reversed(w):
        cols.append(F.matvec(suffix, b[t]))
        suffix = F.matmul(suffix, A[t])
    return cols[::-1]


def field_for(chart):
    """gfq.GF tables up to q = 1024; GF(2^k) log tables beyond (encodings as
    documented in gfq.py and gf2k.py respectively)."""
    q = chart['q']
    p, k = factor_prime_power(q)
    if p == 2 and q > 1024:
        F = GF2k(k)
        assert chart.get('modulus_int', F.modulus) == F.modulus, 'chart uses another modulus'
        return F
    return GF(q)


def check_chart(chart):
    q = chart['q']
    F = field_for(chart)
    A, b = chart['A'], chart['b']
    I = F.identity(5)
    for x in [v for M in A for row in M for v in row] + [v for vec in b for v in vec]:
        assert 0 <= x < q, f'entry {x} outside GF({q})'
    for p, r in [(0, 1), (2, 3)]:
        assert F.matmul(A[p], A[r]) == I and F.matmul(A[r], A[p]) == I, f'A_{r} != A_{p}^-1'
        assert F.matvec(A[r], b[p]) == b[r], f'b_{r} != A_{r} b_{p}'
    words = reduced_words()
    assert len(words) == 324
    ranks = []
    for w in words:
        cols = controllability_columns(F, A, b, w)
        rows = [list(r) for r in zip(*cols)]
        ranks.append(F.rank(rows))
    bad = [w for w, r in zip(words, ranks) if r < 5]
    return len(words), min(ranks), bad


def main():
    ok = True
    for path in sys.argv[1:]:
        with open(path) as fh:
            chart = json.load(fh)
        n, mr, bad = check_chart(chart)
        status = 'OK' if not bad else f'FAIL ({len(bad)} singular words, e.g. {bad[:3]})'
        print(f'{path}: GF({chart["q"]})^5 chart, {n} reduced words, min rank {mr}: {status}')
        ok &= not bad
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
