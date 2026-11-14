"""Integer route charts and the primes at which they reduce to universal charts.

An integer route chart has A_0, A_2 in GL_5(Z) with det = +-1 (so A_1 = A_0^-1,
A_3 = A_2^-1 are integer matrices), integer b_0, b_2, and b_1 = A_1 b_0,
b_3 = A_3 b_2.  If every one of the 324 integer determinants det M_w is nonzero,
then for each prime p dividing none of them the reduction mod p is a universal
route chart on GF(p)^5, and hence (same matrices) on GF(p^m)^5 for every m.

Usage:
  python3 intchart.py search K SEED OUT.json
      draws random small integer charts until K of them have all 324
      determinants nonzero, and records them with their determinants.
  python3 intchart.py analyse CHARTS.json
      recomputes every determinant exactly and reports the primes that are
      bad for all charts (they divide gcd_i prod_w |det M_w^(i)|).
"""
import json
import math
import random
import sys
from itertools import product

SINV = {0: 1, 1: 0, 2: 3, 3: 2}
WORDS = [w for w in product(range(4), repeat=5)
         if all(w[i + 1] != SINV[w[i]] for i in range(4))]
assert len(WORDS) == 324


def matmul(X, Y):
    return [[sum(X[i][k] * Y[k][j] for k in range(len(Y))) for j in range(len(Y[0]))]
            for i in range(len(X))]


def matvec(X, v):
    return [sum(a * b for a, b in zip(row, v)) for row in X]


def det_bareiss(M):
    """Exact integer determinant (Bareiss fraction-free elimination)."""
    A = [list(r) for r in M]
    n = len(A)
    sign, prev = 1, 1
    for k in range(n - 1):
        if A[k][k] == 0:
            sw = next((i for i in range(k + 1, n) if A[i][k] != 0), None)
            if sw is None:
                return 0
            A[k], A[sw] = A[sw], A[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                A[i][j] = (A[i][j] * A[k][k] - A[i][k] * A[k][j]) // prev
        prev = A[k][k]
    return sign * A[n - 1][n - 1]


def inverse_unimodular(M):
    """Integer inverse of a matrix with det +-1 (adjugate / det)."""
    n = len(M)
    d = det_bareiss(M)
    assert d in (1, -1), d
    adj = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = [row[:j] + row[j + 1:] for k, row in enumerate(M) if k != i]
            adj[j][i] = (-1) ** (i + j) * det_bareiss(minor)
    return [[x * d for x in row] for row in adj]


def full_chart(A0, A2, b0, b2):
    A1, A3 = inverse_unimodular(A0), inverse_unimodular(A2)
    return [A0, A1, A2, A3], [b0, matvec(A1, b0), b2, matvec(A3, b2)]


def word_dets(A, b):
    dets = []
    for w in WORDS:
        cols, suffix = [], [[int(i == j) for j in range(5)] for i in range(5)]
        for t in reversed(w):
            cols.append(matvec(suffix, b[t]))
            suffix = matmul(suffix, A[t])
        cols.reverse()
        dets.append(det_bareiss([list(r) for r in zip(*cols)]))
    return dets


def random_unimodular(rng):
    """L * U * (signed permutation) with small unitriangular factors."""
    n = 5
    L = [[1 if i == j else (rng.choice((-1, 0, 0, 1)) if i > j else 0) for j in range(n)] for i in range(n)]
    U = [[1 if i == j else (rng.choice((-1, 0, 0, 1)) if i < j else 0) for j in range(n)] for i in range(n)]
    perm = list(range(n))
    rng.shuffle(perm)
    P = [[(rng.choice((-1, 1)) if perm[i] == j else 0) for j in range(n)] for i in range(n)]
    return matmul(matmul(L, U), P)


def search(K, seed, out):
    rng = random.Random(seed)
    charts, tries = [], 0
    while len(charts) < K:
        tries += 1
        A0, A2 = random_unimodular(rng), random_unimodular(rng)
        b0 = [rng.choice((-2, -1, 0, 1, 2)) for _ in range(5)]
        b2 = [rng.choice((-2, -1, 0, 1, 2)) for _ in range(5)]
        A, b = full_chart(A0, A2, b0, b2)
        dets = word_dets(A, b)
        if all(dets):
            charts.append({'A': A, 'b': b, 'dets': dets})
            print(f'chart {len(charts)} after {tries} draws; max |det| = {max(map(abs, dets))}', flush=True)
    json.dump({'seed': seed, 'charts': charts}, open(out, 'w'))


def small_prime_factors(n, bound=10 ** 6):
    fs, d = [], 2
    while d * d <= n and d <= bound:
        while n % d == 0:
            fs.append(d)
            n //= d
        d += 1 if d == 2 else 2
    return fs, n          # n is the cofactor (1, a prime, or unfactored)


def analyse(path):
    data = json.load(open(path))
    g = 0
    for i, ch in enumerate(data['charts']):
        A, b = ch['A'], ch['b']
        for p_, r_ in [(0, 1), (2, 3)]:
            assert matmul(A[p_], A[r_]) == [[int(i == j) for j in range(5)] for i in range(5)]
            assert matvec(A[r_], b[p_]) == b[r_]
        dets = word_dets(A, b)
        assert dets == ch['dets'] and all(dets)
        Ni = math.prod(abs(d) for d in dets)
        g = Ni if g == 0 else math.gcd(g, Ni)
        fs, cof = small_prime_factors(g)
        print(f'after chart {i + 1}: primes bad for every chart so far divide g, '
              f'g = {sorted(set(fs))} x cofactor {cof}')
    return g


if __name__ == '__main__':
    if sys.argv[1] == 'search':
        search(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
    else:
        analyse(sys.argv[2])
