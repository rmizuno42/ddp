#!/usr/bin/env python3
"""Verify the small certificate for a (12,4)-graph on 5,832 vertices.
Python 3 standard library only. No network access and no external packages.

Usage: python verify_certificate.py
       python verify_certificate.py --write-edges
The second form regenerates the entire undirected edge list as well.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)

def multiply(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    return [[sum(a[i][k] * b[k][j] for k in range(4)) % 3
             for j in range(4)] for i in range(4)]

def reduced(word: tuple[int, ...]) -> tuple[int, ...]:
    stack: list[int] = []
    for t in word:
        if stack and stack[-1] == 3 - t:
            stack.pop()
        else:
            stack.append(t)
    return tuple(stack)

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-edges', action='store_true')
    args = parser.parse_args()
    data = json.loads((ROOT / 'construction.json').read_text())
    matrices = data['matrices']
    vectors = data['control_vectors']
    identity = [[int(i == j) for j in range(4)] for i in range(4)]
    require(vectors == identity, 'The supplied certificate uses standard-basis controls.')
    for t in range(4):
        require(multiply(matrices[3-t], matrices[t]) == identity, 'Inverse matrix failure.')
        transported = [sum(matrices[3-t][i][j] * vectors[t][j] for j in range(4)) % 3
                       for i in range(4)]
        require(transported == vectors[3-t], 'Inverse control-vector failure.')

    def encode(x: tuple[int, ...] | list[int]) -> int:
        return sum(x[i] * 3**i for i in range(4))

    coords = [tuple((x // 3**i) % 3 for i in range(4)) for x in range(81)]
    add = [[encode(tuple((coords[x][i] + coords[y][i]) % 3 for i in range(4)))
            for y in range(81)] for x in range(81)]
    maps = [[encode(tuple(sum(matrices[t][i][j] * coords[x][j] for j in range(4)) % 3
                          for i in range(4))) for x in range(81)] for t in range(4)]
    shifts = [[encode(tuple(lam * vectors[t][i] % 3 for i in range(4)))
               for lam in range(3)] for t in range(4)]
    words = [w for length in range(5) for w in itertools.product(range(4), repeat=length)]
    images: dict[tuple[int, ...], frozenset[int]] = {(): frozenset({0})}
    products: dict[tuple[int, ...], list[list[int]]] = {(): identity}
    for w in words[1:]:
        t = w[-1]
        images[w] = frozenset(add[maps[t][x]][shift] for x in images[w[:-1]] for shift in shifts[t])
        products[w] = multiply(matrices[t], products[w[:-1]])
        require(len(images[w]) in (1, 3, 9, 27, 81), 'Route image is not of the expected size.')
        require(products[w] == products[reduced(w)], 'Free reduction changed the linear product.')

    reduced4 = [w for w in words if len(w) == 4 and reduced(w) == w]
    good4 = [w for w in reduced4 if len(images[w]) == 81]
    bad4 = [''.join('ABCD'[t] for t in w) for w in reduced4 if len(images[w]) != 81]
    require(len(reduced4) == 108 and len(good4) == 100, 'Unexpected rank counts.')
    require(bad4 == ['AABD','ACDD','BBAC','BDCC','CABB','CCDB','DBAA','DDCA'], 'Unexpected exceptional words.')

    def span2(v: list[int], w: list[int]) -> frozenset[int]:
        return frozenset(encode(tuple((a*v[i] + b*w[i]) % 3 for i in range(4)))
                         for a in range(3) for b in range(3))

    planes = [span2(vectors[i], vectors[j]) for i in range(4) for j in range(i+1, 4)]
    planes += [span2(vectors[t], [matrices[t][i][j] for i in range(4)])
               for t in range(4) for j in range(4) if j != 3-t]
    require(len(set(planes)) == 18 and all(len(h) == 9 for h in planes), 'Unexpected self-repair planes.')
    require(set().union(*planes) == set(range(81)), 'Same-fiber plane cover is incomplete.')
    balanced = [w for w in words if reduced(w) == ()]
    require(len(balanced) == 33, 'Unexpected balanced-word count.')
    require(set().union(*(images[w] for w in balanced)) == set(range(81)), 'Balanced routes fail.')

    reduced2 = [w for w in words if len(w) == 2 and reduced(w) == w]
    pencil_counts = []
    for r in reduced2:
        family = [w for w in words if reduced(w) == r]
        hyperplanes = set(images[w] for w in family if len(images[w]) == 27)
        core = images[r]
        require(len(family) == 11 and len(core) == 9 and len(hyperplanes) == 4, 'Unexpected pencil dimensions.')
        require(all(core <= h for h in hyperplanes), 'A hyperplane misses its common core.')
        require(all(h & k == core for h, k in itertools.combinations(hyperplanes, 2)), 'Wrong pencil intersection.')
        require(set().union(*hyperplanes) == set(range(81)), 'Pencil does not cover the fiber.')
        require(all(products[w] == products[r] for w in family), 'Affine centers are inconsistent.')
        pencil_counts.append({'word': ''.join('ABCD'[t] for t in r), 'routes': 11,
                              'distinct_hyperplanes': 4, 'hyperplane_size': 27, 'core_size': 9})

    dest = [[-1]*4 for _ in range(8)]
    voltage = [[0]*4 for _ in range(8)]
    for e in data['base_edges']:
        g, h, delta, t = (e[k] for k in ('tail','head','voltage','label'))
        require(g != h and dest[g][t] == -1 and dest[h][3-t] == -1, 'Invalid base labels.')
        dest[g][t] = h
        dest[h][3-t] = g
        voltage[g][t] = delta % 9
        voltage[h][3-t] = -delta % 9
    require(all(h >= 0 for row in dest for h in row), 'Incomplete label assignment.')
    controller = [[dest[g][t]*9 + (i + voltage[g][t]) % 9 for t in range(4)]
                  for g in range(8) for i in range(9)]
    for u in range(72):
        require(len(set(controller[u])) == 4 and u not in controller[u], 'Controller is not simple 4-regular.')
        for t in range(4):
            require(controller[controller[u][t]][3-t] == u, 'Controller inverse failure.')

    def endpoint(u: int, word: tuple[int, ...]) -> int:
        for t in word:
            u = controller[u][t]
        return u

    singles = pencils = self_pairs = 0
    missing_nb4_per_source = []
    for u in range(72):
        targets4 = {endpoint(u, w) for w in good4}
        targets2 = {endpoint(u, w) for w in reduced2}
        targets_nb4 = {endpoint(u, w) for w in reduced4}
        require(targets4 | targets2 | {u} == set(range(72)), 'Controller route coverage fails.')
        require(targets4 == targets_nb4, 'A nonbacktracking target has no good rank-4 word.')
        missing_nb4_per_source.append(72-len(targets_nb4))
        singles += len(targets4)
        for v in set(range(72)) - targets4:
            if u == v:
                self_pairs += 1
            else:
                require(v in targets2, 'Unclassified controller pair.')
                pencils += 1
    require((singles, pencils, self_pairs) == (4464,648,72), 'Unexpected controller certificate counts.')

    certificate = {'result': 'PASS', 'order': 5832, 'degree': 12, 'diameter_upper_bound': 4,
                   'full_rank_reduced_words_length4': 100, 'exceptional_words': bad4,
                   'self_repair_distinct_planes': 18, 'self_repair_union_size': 81,
                   'pencils': pencil_counts, 'controller_pairs_checked': 72**2,
                   'single_route_controller_pairs': singles, 'pencil_controller_pairs': pencils,
                   'self_repair_controller_pairs': self_pairs,
                   'missing_nb4_per_source_histogram': {str(k): missing_nb4_per_source.count(k)
                                                       for k in sorted(set(missing_nb4_per_source))}}
    if args.write_edges:
        adjacency = []
        for u in range(72):
            for x in range(81):
                row = sorted(controller[u][t]*81 + add[maps[t][x]][shift]
                             for t in range(4) for shift in shifts[t])
                require(len(set(row)) == 12 and u*81+x not in row, 'Lift is not simple 12-regular.')
                adjacency.append(row)
        for u, row in enumerate(adjacency):
            require(all(u in adjacency[v] for v in row), 'Lift is not undirected.')
        path = ROOT / 'graph_12_4_5832.edges'
        with path.open('w') as f:
            for u, row in enumerate(adjacency):
                for v in row:
                    if u < v:
                        f.write(f'{u} {v}\n')
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        require(digest == 'ea0846865021f05f38825ac03ca96a387815b50634a9117f9f42533080dbd05b', 'Regenerated edge list differs.')
        certificate['edge_sha256'] = digest
    (ROOT / 'small_certificate.json').write_text(json.dumps(certificate, indent=2) + '\n')
    print(json.dumps(certificate, indent=2))

if __name__ == '__main__':
    main()
