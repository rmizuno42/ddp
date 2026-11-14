"""Finite-field arithmetic GF(q), q = p^k, for the route-chart experiments.

Elements are the integers 0..q-1. The integer x stands for the polynomial
c_0 + c_1 X + ... + c_{k-1} X^{k-1} over GF(p), where x = sum c_i p^i.
Multiplication is reduction modulo a fixed monic irreducible polynomial,
chosen as the lexicographically first one of degree k (so the encoding is
reproducible). For k = 1 this is ordinary arithmetic modulo p.
"""
from functools import lru_cache


def factor_prime_power(q):
    """Return (p, k) with q = p^k, or raise ValueError."""
    if q < 2:
        raise ValueError(q)
    p = next(d for d in range(2, q + 1) if q % d == 0)
    k, r = 0, q
    while r % p == 0:
        r //= p
        k += 1
    if r != 1:
        raise ValueError(f'{q} is not a prime power')
    return p, k


def _poly_mulmod(a, b, mod, p):
    """Multiply coefficient lists a, b (low degree first) modulo monic `mod`."""
    k = len(mod) - 1
    res = [0] * (2 * k)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                res[i + j] = (res[i + j] + x * y) % p
    for d in range(len(res) - 1, k - 1, -1):
        c = res[d]
        if c:
            for i in range(k + 1):
                res[d - k + i] = (res[d - k + i] - c * mod[i]) % p
    return res[:k]


def _is_irreducible(mod, p):
    """Brute force: a monic polynomial of degree k <= 4 (enough here) or any
    degree is irreducible iff it has no monic factor of degree 1..k//2."""
    k = len(mod) - 1
    from itertools import product
    for d in range(1, k // 2 + 1):
        for tail in product(range(p), repeat=d):
            f = list(tail) + [1]
            # polynomial long division of mod by f
            r = list(mod)
            for i in range(k, d - 1, -1):
                c = r[i]
                if c:
                    for j in range(d + 1):
                        r[i - d + j] = (r[i - d + j] - c * f[j]) % p
            if not any(r[:d]):
                return False
    return True


@lru_cache(maxsize=None)
def irreducible(p, k):
    """Lexicographically first monic irreducible polynomial of degree k over GF(p)
    (coefficient list, low degree first, leading 1 included)."""
    from itertools import product
    if k == 1:
        return (0, 1)
    for tail in product(range(p), repeat=k):
        mod = list(tail) + [1]
        if mod[0] == 0:
            continue
        if _is_irreducible(mod, p):
            return tuple(mod)
    raise RuntimeError('no irreducible polynomial found')


class GF:
    """Table-driven GF(q)."""

    def __init__(self, q):
        self.q = q
        self.p, self.k = factor_prime_power(q)
        p, k = self.p, self.k
        self.modulus = irreducible(p, k)

        def digits(x):
            return [(x // p ** i) % p for i in range(k)]

        def undigits(c):
            return sum(ci * p ** i for i, ci in enumerate(c))

        self.add = [[undigits([(a + b) % p for a, b in zip(digits(x), digits(y))])
                     for y in range(q)] for x in range(q)]
        self.mul = [[undigits(_poly_mulmod(digits(x), digits(y), list(self.modulus), p))
                     for y in range(q)] for x in range(q)]
        self.neg = [undigits([(-a) % p for a in digits(x)]) for x in range(q)]
        self.inv = [None] * q
        for x in range(1, q):
            for y in range(1, q):
                if self.mul[x][y] == 1:
                    self.inv[x] = y
                    break
        assert all(self.inv[x] is not None for x in range(1, q)), 'not a field'

    def sub(self, x, y):
        return self.add[x][self.neg[y]]

    # --- linear algebra over GF(q) ---
    def matmul(self, X, Y):
        add, mul = self.add, self.mul
        n, m, r = len(X), len(Y), len(Y[0])
        out = []
        for i in range(n):
            row = []
            for j in range(r):
                s = 0
                for t in range(m):
                    s = add[s][mul[X[i][t]][Y[t][j]]]
                row.append(s)
            out.append(row)
        return out

    def matvec(self, X, v):
        add, mul = self.add, self.mul
        out = []
        for row in X:
            s = 0
            for a, b in zip(row, v):
                s = add[s][mul[a][b]]
            out.append(s)
        return out

    def rank(self, rows):
        M = [list(r) for r in rows]
        add, mul, neg, inv = self.add, self.mul, self.neg, self.inv
        nr, nc = len(M), len(M[0])
        r = 0
        for c in range(nc):
            piv = next((i for i in range(r, nr) if M[i][c]), None)
            if piv is None:
                continue
            M[r], M[piv] = M[piv], M[r]
            f = inv[M[r][c]]
            M[r] = [mul[f][x] for x in M[r]]
            for i in range(nr):
                if i != r and M[i][c]:
                    g = neg[M[i][c]]
                    M[i] = [add[x][mul[g][y]] for x, y in zip(M[i], M[r])]
            r += 1
            if r == nr:
                break
        return r

    def inverse(self, A):
        """Inverse of a square matrix, or None if singular (Gauss-Jordan)."""
        n = len(A)
        add, mul, neg, inv = self.add, self.mul, self.neg, self.inv
        M = [list(A[i]) + [1 if i == j else 0 for j in range(n)] for i in range(n)]
        for c in range(n):
            piv = next((i for i in range(c, n) if M[i][c]), None)
            if piv is None:
                return None
            M[c], M[piv] = M[piv], M[c]
            f = inv[M[c][c]]
            M[c] = [mul[f][x] for x in M[c]]
            for i in range(n):
                if i != c and M[i][c]:
                    g = neg[M[i][c]]
                    M[i] = [add[x][mul[g][y]] for x, y in zip(M[i], M[c])]
        return [row[n:] for row in M]

    def identity(self, n):
        return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


if __name__ == '__main__':
    import sys
    for q in map(int, sys.argv[1:] or ['2', '3', '4', '5', '7', '8', '9', '16', '25', '27']):
        F = GF(q)
        # field axioms spot check: distributivity on all triples for small q
        if q <= 16:
            for x in range(q):
                for y in range(q):
                    for z in range(q):
                        assert F.mul[x][F.add[y][z]] == F.add[F.mul[x][y]][F.mul[x][z]]
        print(f'GF({q}) = GF({F.p}^{F.k}), modulus {F.modulus}: OK')
