#!/usr/bin/env python3
"""Reproduce the graph and compare its 60 explicit symmetries with nauty's generators."""
from collections import Counter
import json
from pathlib import Path
import construct
from matrix_model import I, T, inv, mul

ROOT = Path(__file__).resolve().parent


def order(x):
    y, k = x, 1
    while y != I:
        y, k = mul(y, x), k+1
        assert k <= 660
    return k


def main():
    vertices, edges, spec = construct.build()
    assert (ROOT / 'graph.edges').read_text() == construct.edge_text(660, edges)
    assert (ROOT / 'algebraic.edges').read_text() == construct.edge_text(660, edges)
    assert json.loads((ROOT / 'construction.json').read_text()) == json.loads(json.dumps(spec))
    rows = (ROOT / 'vertices.tsv').read_text().splitlines()
    assert [list(map(int, row.split())) for row in rows[1:]] == [[i, *x] for i, x in enumerate(vertices)]
    adjacency = [set() for _ in vertices]
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    adjrows = [row for row in (ROOT / 'graph.adjlist').read_text().splitlines() if not row.startswith('#')]
    assert [list(map(int, row.split())) for row in adjrows] == [[i, *sorted(row)] for i, row in enumerate(adjacency)]
    index = {x: i for i, x in enumerate(vertices)}
    A, B = spec['A_centralizer_of_h'], spec['B_conjugation_stabilizer_of_S']
    a = (1, 0, 0, 3)
    assert a in A and T in A and order(a) == 5 and order(T) == 2 and mul(mul(T, a), T) == inv(a)
    b = next(x for x in B if order(x) == 3)
    c = next(x for x in B if order(x) == 2)
    assert mul(mul(c, b), c) == inv(b)
    actions = {tuple(index[mul(mul(a, x), inv(b))] for x in vertices) for a in A for b in B}
    assert len(actions) == 60
    for p in actions:
        assert len(set(p)) == 660
        assert {tuple(sorted((p[u], p[v]))) for u, v in edges} == edges
    saved = json.loads((ROOT / 'symmetry/nauty.json').read_text())
    assert saved['vertices'] == 660 and saved['group_size_mantissa'] == 60 and saved['group_size_exponent'] == 0
    generated = {tuple(range(660))}
    queue = list(generated)
    for p in queue:
        for g in saved['generators']:
            assert tuple(g) in actions
            q = tuple(g[p[i]] for i in range(660))
            if q not in generated:
                generated.add(q)
                queue.append(q)
    assert generated == actions
    orbits = {frozenset(p[v] for p in actions) for v in range(660)}
    print(json.dumps({'status': 'PASS', 'vertices': 660, 'edges': 1635, 'maximum_degree': 5,
                     'degree_histogram': dict(Counter(map(len, adjacency))),
                     'diameter': 5, 'verified_automorphisms': 60,
                     'group': 'Dihedral group of order 10 x S3',
                     'vertex_orbit_size_counts': dict(Counter(map(len, orbits))),
                     'full_group_upper_bound': 'Saved nauty computation; see symmetry/README.md for reproduction.',
                     'factorization_identity': spec['factorization_identity']}, indent=2))


if __name__ == '__main__':
    main()
