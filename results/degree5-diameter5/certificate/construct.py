#!/usr/bin/env python3
"""Construct the 660-vertex graph and a regular completion preserving 60 automorphisms.

Uses only Python's standard library; no search or input edge list is used.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
from matrix_model import I, H, S, SQUARES, det, inv, mul, projective_group


def build():
    group = projective_group()
    vertices = [x for x in group if det(x) in SQUARES]
    odd = set(group) - set(vertices)
    index = {x: i for i, x in enumerate(vertices)}
    assert len(group) == 1320 and len(vertices) == len(odd) == 660
    assert set(S) <= odd and {inv(s) for s in S} == set(S) and mul(H, H) == I
    products = {I}
    sizes = [1]
    for _ in range(5):
        products = {mul(x, s) for x in products for s in S}
        sizes.append(len(products))
    assert products == odd and sizes == [1, 5, 21, 85, 341, 660]

    adjacency = [set() for _ in vertices]
    for u, x in enumerate(vertices):
        for s in S:
            v = index[mul(mul(H, x), s)]
            if u != v:
                adjacency[u].add(v)
    assert all(u in adjacency[v] for u in range(660) for v in adjacency[u])
    base = {(u, v) for u in range(660) for v in adjacency[u] if u < v}
    assert len(base) == 1635 and Counter(map(len, adjacency)) == {4: 30, 5: 630}
    A = [a for a in vertices if mul(a, H) == mul(H, a)]
    B = [b for b in vertices if {mul(mul(inv(b), s), b) for s in S} == set(S)]
    assert len(A) == 10 and len(B) == 6
    choices = {}
    for s in S:
        if mul(s, s) == I:
            allowed = [b for b in B if b != I and mul(b, b) == I and mul(b, s) == mul(s, b)]
            assert len(allowed) == 1
            choices[s] = allowed[0]
    matching = set()
    deficient = {u for u in range(660) if len(adjacency[u]) == 4}
    for u in sorted(deficient):
        x = vertices[u]
        s = mul(mul(inv(x), H), x)
        assert s in choices
        v = index[mul(x, choices[s])]
        assert v in deficient and v != u and v not in adjacency[u]
        matching.add(tuple(sorted((u, v))))
    assert len(matching) == 15
    assert Counter(v for e in matching for v in e) == {v: 1 for v in deficient}
    edges = base | matching
    assert len(edges) == 1650 and Counter(v for e in edges for v in e) == {v: 5 for v in range(660)}
    specification = {
        'prime': 11, 'vertices': 660, 'edges': 1650, 'degree': 5, 'diameter': 5,
        'vertex_order': 'Lexicographically sorted normalized projective matrices of square determinant; first nonzero entry equals 1.',
        'h': H, 'S': S, 'base_edge_rule': 'x -- h*x*s for s in S; remove loops.',
        'exact_product_set_sizes_k_0_to_5': sizes,
        'factorization_identity': 'S^5 = PGL(2,11) minus PSL(2,11)',
        'base_edges': 1635, 'base_degree_histogram': {'4': 30, '5': 630},
        'A_centralizer_of_h': A, 'B_conjugation_stabilizer_of_S': B,
        'matching_rule': 'At a loop site x, set s=x^-1*h*x and join x to x*b_s.',
        'matching_choices': [{'s': s, 'b_s': b} for s, b in choices.items()],
        'matching_edges': sorted(matching),
    }
    return vertices, base, edges, specification


def edge_text(n, edges):
    return f'{n} {len(edges)}\n' + ''.join(f'{u} {v}\n' for u, v in sorted(edges))


def write(output):
    vertices, base, edges, specification = build()
    output.mkdir(parents=True, exist_ok=True)
    (output / 'graph.edges').write_text(edge_text(660, edges))
    (output / 'algebraic.edges').write_text(edge_text(660, base))
    (output / 'construction.json').write_text(json.dumps(specification, indent=2) + '\n')
    (output / 'vertices.tsv').write_text('id\ta\tb\tc\td\n' + ''.join(
        '\t'.join(map(str, [i, *x])) + '\n' for i, x in enumerate(vertices)))
    adjacency = [set() for _ in vertices]
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    (output / 'graph.adjlist').write_text('# Each row: vertex ID followed by all neighbors.\n' + ''.join(
        ' '.join(map(str, [i, *sorted(row)])) + '\n' for i, row in enumerate(adjacency)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    write(args.output_dir)
    print('Constructed 660 vertices, 1650 edges, and the 15-edge invariant matching.')
