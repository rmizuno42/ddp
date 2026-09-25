# Degree 15, diameter 5: 100,000 vertices

**$N(15,5)\ge 100,000$.** Simple undirected connected graph; 750,000 edges,
maximum degree 15, diameter exactly 5.

Compared with the [Comellas table](https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html) accessed on **2026-09-25** (page last changed 2026-09-24): **82,684 → 100,000**, an increase of **17,316 vertices (20.94%)**.

A 32-state cubic controller is lifted over $\mathbb F_5^5$. Full-rank routes and finite subspace covers handle all 1,024 ordered controller pairs.

This uses a variant of the affine route-chart construction in [arXiv:2606.15860](../diameter5-paper/), with a new controller and finite-field chart and subspace covers that combine several routes to reach an entire fiber.

## Materials

- [Edge list](certificate/graph_d15_D5_n100000.edges) — first line `n m`, followed by one undirected edge `u v` per line, with zero-based vertex numbers.
- [Original package guide (Japanese)](certificate/README_ja.md).
- [Construction and proof (Japanese)](certificate/PROOF_ja.md).
- [Original certificate package](certificate/) — construction data, verification code, saved reports, and integrity manifest.

## Reproduce the verification

Python 3.10 or later, standard library only. From the repository root, copy the
package to a temporary directory because its scripts write regenerated files
and reports beside the construction data:

```bash
verify_dir=$(mktemp -d)
cp -R results/degree15-diameter5/certificate/. "$verify_dir/"
cd "$verify_dir"
python3 verify_small.py
python3 verify_independent.py
python3 regenerate.py --output regenerated.edges
cmp regenerated.edges graph_d15_D5_n100000.edges
```

All commands above passed during the **2026-09-25 repository update**. The
regenerated edge file matched the supplied file byte for byte. A subsequent
[final check directly from the edge list](../../verification/final/degree15-diameter5.json)
verified every vertex and every ordered pair, confirming the degree distribution,
connectivity, and exact diameter. Its distance histogram matches the supplied
BFS report. See [the method and reproduction commands](../../verification/README.md)
and [the repository verification record](../../VERIFICATION.md).

Edge-file SHA-256:

```text
ed2b9ad5303034e7875d369c6915b0dd8e84c3bded60b821f7720966fb1ef271
```

The imported package is preserved without edits. This result is compared with
the dated public table; listing here does not assert table acceptance,
independent peer review, or optimality. This package has no separate paper.

[All results](../../README.md)
