# Degree 14, diameter 5: 88,452 vertices

**$N(14,5)\ge 88,452$.** Simple undirected connected graph; 618,786 edges,
maximum degree 14, diameter exactly 5.

Compared with the [Comellas table](https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html) accessed on **2026-09-25** (page last changed 2026-09-24): **61,887 → 88,452**, an increase of **26,565 vertices (42.93%)**.

A 364-state controller is lifted over $\mathbb F_3^5$. State-dependent translations inside each fiber supply the missing short routes. The graph is not regular: 756 vertices have degree 13 and 87,696 have degree 14.

This builds on the affine route-chart method in [arXiv:2606.15860](../diameter5-paper/), adding state-dependent translations to cover short controller routes.

## Materials

- [Edge list](certificate/graph_d14_D5_n88452.edges) — first line `n m`, followed by one undirected edge `u v` per line, with zero-based vertex numbers.
- [Original package guide (Japanese)](certificate/README_ja.md).
- [Construction and proof (Japanese)](certificate/PROOF_ja.md).
- [Original certificate package](certificate/) — construction data, verification code, saved reports, and integrity manifest.

## Reproduce the verification

Python 3.10 or later, standard library only. From the repository root, copy the
package to a temporary directory because its scripts write regenerated files
and reports beside the construction data:

```bash
verify_dir=$(mktemp -d)
cp -R results/degree14-diameter5/certificate/. "$verify_dir/"
cd "$verify_dir"
python3 verify_small.py
python3 build_graph.py --output regenerated.edges
cmp regenerated.edges graph_d14_D5_n88452.edges
```

All commands above passed during the **2026-09-25 repository update**. The
regenerated edge file matched the supplied file byte for byte. A subsequent
[final check directly from the edge list](../../verification/final/degree14-diameter5.json)
verified every vertex and every ordered pair, confirming the degree distribution,
connectivity, and exact diameter. Its distance histogram matches the supplied
BFS report. See [the method and reproduction commands](../../verification/README.md)
and [the repository verification record](../../VERIFICATION.md).

Edge-file SHA-256:

```text
ae192f45dc5cfb5a44530f520fe258610ff5a46e720e2cb739cca9fbc929b39a
```

The imported package is preserved without edits. This result is compared with
the dated public table; listing here does not assert table acceptance,
independent peer review, or optimality. This package has no separate paper.

[All results](../../README.md)
