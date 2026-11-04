#!/usr/bin/env python3
"""Check the published graph against its formula, trees, voltages and symmetry proof."""
import json
from pathlib import Path
import construct
import check_certificate
import verify_structure
import verify_voltage

ROOT = Path(__file__).resolve().parent


def main():
    n, expected = construct.construct()
    rows = [tuple(map(int, line.split())) for line in (ROOT / 'graph.edges').read_text().splitlines()]
    assert rows[0] == (n, len(expected))
    assert rows[1:] == sorted(expected)
    adjacency = [set() for _ in range(n)]
    for u, v in rows[1:]:
        adjacency[u].add(v)
        adjacency[v].add(u)
    assert adjacency == [check_certificate.neighbours(v) for v in range(n)]
    adjrows = [line for line in (ROOT / 'graph.adjlist').read_text().splitlines() if not line.startswith('#')]
    assert [list(map(int, line.split())) for line in adjrows] == [
        [v, *sorted(adjacency[v])] for v in range(n)]
    trees = check_certificate.check()
    voltage = verify_voltage.verify()
    for i, arcs in enumerate(voltage['arcs']):
        assert {16*j+t for j, t in arcs} == adjacency[16*i]
    structure = verify_structure.check()
    assert trees['valid'] and structure['valid']
    print(json.dumps({'status': 'PASS', 'vertices': n, 'edges': len(expected),
                     'degree': 3, 'diameter': 7, 'girth': structure['girth'],
                     'full_automorphism_group': 'C16', 'full_automorphism_group_order': 16,
                     'tree_certificate': trees,
                     'modular_reachability_pairs': voltage['checked_root_target_orbit_pairs']}, indent=2))


if __name__ == '__main__':
    main()
