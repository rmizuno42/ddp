#!/usr/bin/env python3
"""Run all construction-level checks for the (6,3) graph of order 126 (standard library only).

1. The construction formula reproduces graph.edges and graph.adjlist byte for byte; the graph is
   simple and 6-regular with 126 vertices and 378 edges.
2. Spanning-tree certificate (check_certificate.py): diameter <= 3.
3. Modular reachability (verify_voltage.py): diameter <= 3, independently of the trees.
4. The Moore bound for degree 6 and diameter 2 is 1 + 6 + 30 = 37 < 126, so the diameter is exactly 3.
5. The orbit graph found by the search maps onto the published graph (check_isomorphism.py).
6. Every generator listed in automorphisms.json preserves the edge set.
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import construct  # noqa: E402


def main():
    n, edges, adj = construct.build()
    assert n == 126 and len(edges) == 378 and all(len(a) == 6 for a in adj)
    for script in ['construct.py --check', 'check_certificate.py', 'verify_voltage.py', 'check_isomorphism.py']:
        out = subprocess.run([sys.executable, str(HERE / script.split()[0])] + script.split()[1:],
                             capture_output=True, text=True, cwd=HERE)
        assert out.returncode == 0, out.stderr
        print(out.stdout.strip())
    assert 1 + 6 + 6 * 5 < n
    E = set(edges)
    aut = json.loads((HERE / 'automorphisms.json').read_text())
    for p in aut['generators']:
        assert sorted(p) == list(range(n))
        assert all((min(p[a], p[b]), max(p[a], p[b])) in E for a, b in edges)
    print(f"PASS: {len(aut['generators'])} automorphism generators preserve the edge set "
          f"(group order {aut['group_order']} computed with nauty)")
    print("PASS: order 126, 6-regular, diameter exactly 3")


if __name__ == '__main__':
    main()
