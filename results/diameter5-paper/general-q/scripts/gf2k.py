"""GF(2^k) with log tables, for fields too large for gfq.GF's q x q tables.

Elements are integers 0..2^k-1 read as polynomials over GF(2) (bit i is the
coefficient of X^i); addition is XOR; multiplication is modulo the
lexicographically first primitive polynomial of degree k (smallest integer
encoding with the top bit set), found by checking that X has order 2^k - 1.
Interface matches the linear-algebra part of gfq.GF used by verify_chart.py.
"""


def _order_of_x(mod, k):
    q1 = (1 << k) - 1
    x, e = 1, 0
    while True:
        x <<= 1
        if x >> k:
            x ^= mod
        e += 1
        if x == 1:
            return e
        if e > q1:
            return None


def primitive_polynomial(k):
    for mod in range((1 << k) + 1, 1 << (k + 1), 2):   # constant term 1
        if _order_of_x(mod, k) == (1 << k) - 1:
            return mod
    raise RuntimeError('no primitive polynomial')


class GF2k:
    def __init__(self, k):
        self.k, self.q, self.p = k, 1 << k, 2
        self.modulus = primitive_polynomial(k)
        q1 = self.q - 1
        self.exp = [0] * (2 * q1)
        self.log = [0] * self.q
        x = 1
        for e in range(q1):
            self.exp[e] = x
            self.log[x] = e
            x <<= 1
            if x >> k:
                x ^= self.modulus
        for e in range(q1, 2 * q1):
            self.exp[e] = self.exp[e - q1]

    def mul(self, a, b):
        if a == 0 or b == 0:
            return 0
        return self.exp[self.log[a] + self.log[b]]

    def inv(self, a):
        return self.exp[(self.q - 1 - self.log[a]) % (self.q - 1)]

    def identity(self, n):
        return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

    def matmul(self, X, Y):
        out = []
        for i in range(len(X)):
            row = []
            for j in range(len(Y[0])):
                s = 0
                for t in range(len(Y)):
                    s ^= self.mul(X[i][t], Y[t][j])
                row.append(s)
            out.append(row)
        return out

    def matvec(self, X, v):
        out = []
        for row in X:
            s = 0
            for a, b in zip(row, v):
                s ^= self.mul(a, b)
            out.append(s)
        return out

    def rank(self, rows):
        M = [list(r) for r in rows]
        nr, nc, r = len(M), len(M[0]), 0
        for c in range(nc):
            piv = next((i for i in range(r, nr) if M[i][c]), None)
            if piv is None:
                continue
            M[r], M[piv] = M[piv], M[r]
            f = self.inv(M[r][c])
            M[r] = [self.mul(f, x) for x in M[r]]
            for i in range(nr):
                if i != r and M[i][c]:
                    g = M[i][c]
                    M[i] = [x ^ self.mul(g, y) for x, y in zip(M[i], M[r])]
            r += 1
            if r == nr:
                break
        return r

    def inverse(self, A):
        n = len(A)
        M = [list(A[i]) + [1 if i == j else 0 for j in range(n)] for i in range(n)]
        for c in range(n):
            piv = next((i for i in range(c, n) if M[i][c]), None)
            if piv is None:
                return None
            M[c], M[piv] = M[piv], M[c]
            f = self.inv(M[c][c])
            M[c] = [self.mul(f, x) for x in M[c]]
            for i in range(n):
                if i != c and M[i][c]:
                    g = M[i][c]
                    M[i] = [x ^ self.mul(g, y) for x, y in zip(M[i], M[c])]
        return [row[n:] for row in M]
