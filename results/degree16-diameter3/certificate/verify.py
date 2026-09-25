#!/usr/bin/env python3
"""Verify and regenerate the edge-local F4^3 construction, without a solver.

Python standard library only.  Default: verify all local algebraic certificates,
regenerate the edge list, and run all-source bitset BFS to depth three.
Finite field: F2[a]/(a^2+a+1); integers 0,1,2,3 encode 0,1,a,a+1.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path

IDENTITY = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
INVERSE_PORT = (1, 0, 3, 2)
ZERO = (0, 0, 0)

def require(condition, message):
    if not condition:
        raise ValueError(message)

def xor_sum(values):
    answer = 0
    for value in values:
        answer ^= value
    return answer

def mul(a, b):
    answer = 0
    for k in range(2):
        if (b >> k) & 1:
            answer ^= a << k
    if answer & 4:
        answer ^= 7
    return answer

def add(x, y):
    return tuple(a ^ b for a, b in zip(x, y))

def scale(c, x):
    return tuple(mul(c, a) for a in x)

def matvec(A, x):
    return tuple(xor_sum(mul(a, b) for a, b in zip(row, x)) for row in A)

def matmul(A, B):
    return tuple(tuple(xor_sum(mul(A[i][k], B[k][j]) for k in range(3))
                       for j in range(3)) for i in range(3))

def span(columns):
    points = {ZERO}
    for column in columns:
        points = {add(x, scale(c, column)) for x in points for c in range(4)}
    return frozenset(points)

def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=here / 'construction.json')
    parser.add_argument('--output', type=Path, default=here / 'regenerated.edges')
    parser.add_argument('--report', type=Path, default=here / 'verification_run.json')
    args = parser.parse_args()
    data = json.loads(args.config.read_text(encoding='utf-8'))
    C = data['controller']
    matrices = data['matrices']
    L = [tuple(v) for v in data['outgoing_return_directions']]
    n = len(C)
    require(data['q'] == 4 and data['dimension'] == 3, 'wrong field or dimension')
    require(len(L) == 4 and all(len(v) == 3 and any(v) for v in L), 'invalid directions')
    require(all(0 <= c < 4 for v in L for c in v), 'invalid field element')
    require(len(matrices) == n, 'wrong number of matrix rows')
    for u in range(n):
        require(len(C[u]) == 4 and len(set(C[u])) == 4 and u not in C[u], 'not simple four-regular')
        require(len(matrices[u]) == 4, 'missing edge matrices')
        for t in range(4):
            v, reverse = C[u][t], INVERSE_PORT[t]
            require(0 <= v < n and C[v][reverse] == u, 'inconsistent reverse port')
            M = matrices[u][t]
            require(len(M) == 3 and all(len(row) == 3 for row in M), 'wrong matrix dimension')
            require(all(0 <= c < 4 for row in M for c in row), 'invalid matrix entry')
            require(matmul(matrices[v][reverse], M) == IDENTITY, 'matrices not inverse')
            require(matvec(M, L[t]) == L[reverse], 'directions not reverse-consistent')

    def route(start, word):
        u, product, columns = start, IDENTITY, []
        for t in word:
            require(0 <= t < 4, 'invalid port in route')
            T = matrices[u][t]
            columns = [matvec(T, c) for c in columns] + [L[INVERSE_PORT[t]]]
            product = matmul(T, product)
            u = C[u][t]
        return u, product, span(columns)

    # The middle-edge matrix has exactly one deficient turn among the nine.
    local_turn_sizes = collections.Counter()
    for u in range(n):
        for t in range(4):
            q = INVERSE_PORT[t]
            sizes = [len(span([matvec(matrices[u][t], L[i]), L[q], L[j]]))
                     for i in range(4) if i != t
                     for j in range(4) if j != q]
            require(sorted(sizes) == [16] + [64] * 8, 'wrong local bad-turn pattern')
            local_turn_sizes.update(sizes)

    # Check pencils by their actual sets of F4^3 points, not by a rank routine.
    for u in range(n):
        for t in range(4):
            v, T, core = route(u, [t])
            planes = set()
            require(len(core) == 4, 'wrong pencil core size')
            for h in range(4):
                for word in [(h, INVERSE_PORT[h], t), (t, h, INVERSE_PORT[h])]:
                    endpoint, product, H = route(u, word)
                    require(endpoint == v and product == T and core <= H,
                            'pencil has wrong endpoint, centre, or core')
                    if len(H) == 16:
                        planes.add(H)
            require(len(planes) == 5 and len(set().union(*planes)) == 64, 'incomplete pencil')

    counts, covered = collections.Counter(), set()
    for record in data['pair_certificate']:
        u, v, word = record['u'], record['v'], record['word']
        require(0 <= u < n and 0 <= v < n and (u, v) not in covered, 'invalid/duplicate pair')
        endpoint, product, points = route(u, word)
        require(endpoint == v, 'certificate route has wrong endpoint')
        if record['kind'] == 'full_rank':
            require(len(word) <= 3 and len(points) == 64, 'route does not cover full fibre')
        else:
            require(record['kind'] == 'edge_pencil' and len(word) == 1, 'invalid repair type')
        counts[record['kind']] += 1
        covered.add((u, v))
    require(len(covered) == n * n, 'not all controller pairs covered')

    N = 64 * n
    points = [(i % 4, (i // 4) % 4, i // 16) for i in range(64)]
    encode = lambda x: x[0] + 4 * x[1] + 16 * x[2]
    edges = set()
    for u in range(n):
        for i, x in enumerate(points):
            a = u * 64 + i
            for t in range(4):
                y = matvec(matrices[u][t], x)
                for c in range(4):
                    z = add(y, scale(c, L[INVERSE_PORT[t]]))
                    b = C[u][t] * 64 + encode(z)
                    require(a != b, 'self-loop in generated graph')
                    edges.add((min(a, b), max(a, b)))
    adjacency = [set() for _ in range(N)]
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    require(all(len(row) == 16 for row in adjacency), 'generated graph is not 16-regular')
    args.output.write_text(f'{N} {len(edges)}\n' + ''.join(f'{a} {b}\n' for a, b in sorted(edges)), encoding='ascii')
    sha = hashlib.sha256(args.output.read_bytes()).hexdigest()
    reference = here / 'graph_d16_D3_n1920.edges'
    reference_match = reference.exists() and reference.read_bytes() == args.output.read_bytes()

    # Independently check graph distances using only the generated adjacency list.
    neighbourhood_bits = [sum(1 << v for v in row) for row in adjacency]
    all_bits = (1 << N) - 1
    histogram = [0, 0, 0, 0]
    for u in range(N):
        reached, previous_size = 1 << u, 1
        histogram[0] += 1
        for depth in range(1, 4):
            new_reached, remaining = reached, reached
            while remaining:
                bit = remaining & -remaining
                remaining -= bit
                new_reached |= neighbourhood_bits[bit.bit_length() - 1]
            reached = new_reached
            size = reached.bit_count()
            histogram[depth] += size - previous_size
            previous_size = size
        require(reached == all_bits, f'not all vertices reached from {u} within three steps')
    require(sum(histogram) == N * N and histogram[3] > 0, 'invalid distance histogram')
    report = dict(
        implementation='standard-library Python, explicit finite-field point sets and all-source bitset BFS',
        field='F2[a]/(a^2+a+1)', controller_vertices=n, controller_edges=2*n,
        pair_certificate_counts=dict(counts), directed_pencils_verified=4*n,
        local_three_step_image_size_counts=dict(local_turn_sizes),
        vertices=N, edges=len(edges), min_degree=16, max_degree=16, diameter=3,
        all_sources_checked=N, distance_histogram=histogram,
        all_pairs_reached_in_three_steps=True, edge_sha256=sha,
        reference_edge_file_byte_identical=reference_match)
    args.report.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
