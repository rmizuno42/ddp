"""Independent small certificate: Leibniz determinants and explicit finite-set unions.

Python standard library only.  No Gaussian elimination is used.  The graph's
100,000-by-100,000 distance matrix is not constructed by this verifier.
"""
from __future__ import annotations
import collections
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
Q, S = 5, 5
INV = (1, 0, 2)
I = tuple(tuple(int(i == j) for j in range(S)) for i in range(S))
data = json.loads((ROOT / 'chart.json').read_text())
A = data['matrices']
b = data['vectors']
C = [tuple(map(int, line.split())) for line in (ROOT / 'controller.adj').read_text().splitlines() if line.strip()]

def mv(M, x):
    return tuple(sum(a * v for a, v in zip(row, x)) % Q for row in M)

def mm(M, N):
    return tuple(tuple(sum(M[i][k] * N[k][j] for k in range(S)) % Q for j in range(S)) for i in range(S))

def reduce_word(w):
    stack = []
    for t in w:
        if stack and INV[stack[-1]] == t:
            stack.pop()
        else:
            stack.append(t)
    return tuple(stack)

def control(w):
    T, columns = I, []
    for t in w:
        T = mm(A[t], T)
        columns = [mv(A[t], col) for col in columns] + [tuple(b[t])]
    return T, tuple(columns)

signed_permutations = []
for perm in itertools.permutations(range(S)):
    parity = sum(perm[i] > perm[j] for i in range(S) for j in range(i + 1, S))
    signed_permutations.append((perm, -1 if parity % 2 else 1))

def determinant(columns):
    value = 0
    for perm, sign in signed_permutations:
        term = sign
        for row in range(S):
            term *= columns[perm[row]][row]
        value += term
    return value % Q

def image(columns):
    # Successive Minkowski sums enumerate the image directly; dependencies
    # are removed by Python set membership, not by a rank calculation.
    points = {(0,) * S}
    for col in columns:
        multiples = [tuple(c * x % Q for x in col) for c in range(Q)]
        points = {tuple((x + y) % Q for x, y in zip(v, m)) for v in points for m in multiples}
    return points

for t in range(3):
    assert mm(A[t], A[INV[t]]) == I
    assert mv(A[INV[t]], b[t]) == tuple(b[INV[t]])
    for u in range(len(C)):
        assert C[C[u][t]][INV[t]] == u
assert all(len(set(row)) == 3 and u not in row for u, row in enumerate(C))

reduced = {k: [w for w in itertools.product(range(3), repeat=k) if reduce_word(w) == w] for k in (3, 5)}
determinants = {w: determinant(control(w)[1]) for w in reduced[5]}
good5 = [w for w, det in determinants.items() if det]
repair_sizes = {}
good3 = []
for r in reduced[3]:
    Tr, _ = control(r)
    reached = set()
    routes = 0
    for k in (3, 5):
        for w in itertools.product(range(3), repeat=k):
            if reduce_word(w) != r:
                continue
            T, columns = control(w)
            assert T == Tr  # All starting fibers are translated by the same Ar*x.
            reached |= image(columns)
            routes += 1
    repair_sizes[''.join(map(str, r))] = {'reachable_points': len(reached), 'routes': routes}
    if len(reached) == Q ** S:
        good3.append(r)

def endpoint(u, word):
    for t in word:
        u = C[u][t]
    return u

full = pencil = 0
for u in range(len(C)):
    reached5 = {endpoint(u, w) for w in good5}
    reached3 = {endpoint(u, w) for w in good3}
    assert len(reached5 | reached3) == len(C), (u, set(range(len(C))) - reached5 - reached3)
    full += len(reached5)
    pencil += len(reached3 - reached5)

result = {
    'implementation': 'standard-library Python: Leibniz determinants + explicit image sets',
    'field': Q, 'dimension': S, 'controller_order': len(C),
    'simple_cubic_controller': True,
    'full_rank_length5_words': len(good5),
    'length5_determinant_histogram': dict(sorted(collections.Counter(determinants.values()).items())),
    'length3_union_sizes': repair_sizes,
    'complete_length3_repair_words': [''.join(map(str, w)) for w in good3],
    'controller_pairs_full_rank': full, 'controller_pairs_repaired': pencil,
    'certified_graph_order': len(C) * Q ** S,
    'certified_regular_degree': 3 * Q,
    'certified_diameter_upper_bound': 5,
}
(ROOT / 'independent_small_certificate.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
