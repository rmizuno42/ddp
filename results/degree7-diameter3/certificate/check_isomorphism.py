#!/usr/bin/env python3
"""Check that the published graph is the orbit graph found by the search (standard library only).

orbit_graph_certificate.json gives, in the discovery labelling, permutation generators of the
acting group and one representative edge per edge orbit.  The orbit graph is the union of the
orbits of these edges.  The certificate also gives an explicit bijection to the published
labelling; this script rebuilds the orbit graph and checks that the bijection maps its edge set
onto the published edge set.
"""
import json
from pathlib import Path

import construct

HERE = Path(__file__).resolve().parent


def main():
    c = json.loads((HERE / 'orbit_graph_certificate.json').read_text())
    n, gens = c['n'], c['generators']
    for p in gens:
        assert sorted(p) == list(range(n))
    E = set()
    for u, v in c['edge_orbit_representatives']:
        e = (min(u, v), max(u, v))
        if e in E:
            continue
        E.add(e)
        stack = [e]
        while stack:
            a, b = stack.pop()
            for p in gens:
                f = (min(p[a], p[b]), max(p[a], p[b]))
                if f not in E:
                    E.add(f)
                    stack.append(f)
    iso = c['isomorphism']
    assert sorted(iso) == list(range(n)), 'not a bijection'
    mapped = {(min(iso[a], iso[b]), max(iso[a], iso[b])) for a, b in E}
    n2, edges, _ = construct.build()
    assert n2 == n and mapped == set(edges), 'isomorphism check failed'
    print(f"PASS: orbit graph of {c['group']} ({len(c['edge_orbit_representatives'])} edge orbits, "
          f"{len(E)} edges) maps onto the published graph")


if __name__ == '__main__':
    main()
