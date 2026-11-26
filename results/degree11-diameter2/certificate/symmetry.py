"""Check the nauty generators, identify the direct factors and compute both orbit partitions."""
import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
IDENTITY = tuple(range(108))


def compose(g, h):
    return tuple(g[x] for x in h)


def closure(generators):
    seen = {IDENTITY}
    queue = [IDENTITY]
    for p in queue:
        for g in generators:
            q = compose(g, p)
            if q not in seen:
                seen.add(q)
                queue.append(q)
    return seen


def power(g, k):
    p = IDENTITY
    for _ in range(k):
        p = compose(g, p)
    return p


def fibre_actions(v):
    if v < 17:
        return v, v
    i, x = divmod(v - 17, 7)
    shift = 17 + 7*i + (x+1) % 7
    # Multiplier -2 cycles the three scales, and inversion interchanges A and B.
    if i < 7:
        return shift, 17 + 7*i + (-2*x) % 7
    r, side = divmod(i-7, 2)
    scale = (1, 2, 4)[(r+1) % 3]
    target = 7 + 2*((r+1) % 3) + 1-side
    return shift, 17 + 7*target + (-2*x+scale) % 7


def analyse(generator_file):
    edges = {tuple(map(int, line.split())) for line in (HERE/'graph.edges').read_text().splitlines()[1:]}
    cert = json.loads(generator_file.read_text())
    generators = [tuple(g) for g in cert['generators']]
    for g in generators:
        assert sorted(g) == list(IDENTITY)
        assert {tuple(sorted((g[u], g[v]))) for u,v in edges} == edges
    group = closure(generators)
    assert len(group) == cert['group_size_mantissa'] * 10**cert['group_size_exponent'] == 252
    shift, multiplier = map(tuple, zip(*(fibre_actions(v) for v in IDENTITY)))
    affine = closure([shift, multiplier])
    assert affine <= group and len(affine) == 42
    assert power(multiplier, 6) == IDENTITY and compose(multiplier, shift) == compose(power(shift,5), multiplier)
    center = {p for p in group if all(compose(p,g) == compose(g,p) for g in generators)}
    z = min(p for p in center if len(closure([p])) == 6)
    assert len(center) == 6 and center & affine == {IDENTITY} and closure([z,shift,multiplier]) == group
    orbits = sorted({tuple(sorted({g[u] for g in group})) for u in IDENTITY})
    labels = {u:i for i,vs in enumerate(orbits) for u in vs}
    edge_orbits = []
    pending = set(edges)
    while pending:
        u,v = min(pending)
        orbit = {tuple(sorted((g[u],g[v]))) for g in group}
        assert orbit <= pending
        pending -= orbit
        edge_orbits.append(dict(representative=[u,v],size=len(orbit),classes=sorted([labels[u],labels[v]])))
    neighbors = [set() for _ in IDENTITY]
    for u,v in edges:
        neighbors[u].add(v)
        neighbors[v].add(u)
    adjacency = ''.join(' '.join(map(str,[i,*sorted(ns)]))+'\n' for i,ns in enumerate(neighbors))
    assert (HERE/'graph.adjlist').read_text() == adjacency
    common = Counter(len(neighbors[u] & neighbors[v]) for u,v in combinations(IDENTITY,2)
                     if v not in neighbors[u])
    assert common[0] == 0 and sum(common.values()) == 5184
    matrix = []
    for vs in orbits:
        rows = {tuple(sum(v in neighbors[u] for v in target) for target in orbits) for u in vs}
        assert len(rows)==1
        matrix.append(list(rows.pop()))
    assert all(sum(row)==11 for row in matrix)
    assert sum(e['size'] for e in edge_orbits)==594
    return dict(full_group_order=len(group),small_group_id=[252,28],structure='C6 x AGL(1,7)',
                vertices=list(map(list,orbits)),edge_orbits=edge_orbits,neighbors_per_vertex=matrix,
                nonadjacent_common_neighbors={str(k):v for k,v in sorted(common.items())},
                translation=list(shift),multiplier=list(multiplier),central_generator=list(z))


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true',help='replace the saved derived orbit data')
    parser.add_argument('--automorphisms',type=Path,default=HERE/'automorphisms.json',
                        help='nauty generator file to verify against the published orbit data')
    args=parser.parse_args()
    result=analyse(args.automorphisms)
    destination=HERE/'orbits.json'
    if args.write:
        destination.write_text(json.dumps(result,indent=2)+'\n')
    else:
        assert json.loads(destination.read_text())==result
    print(f"Full group: {result['full_group_order']}, vertex orbits: {len(result['vertices'])}, edge orbits: {len(result['edge_orbits'])}")
