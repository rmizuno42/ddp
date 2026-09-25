# Degree 16, diameter 3: 1,920 vertices

**$N(16,3)\ge 1,920$.** Simple undirected connected graph; 15,360 edges,
maximum degree 16, diameter exactly 3.

Compared with the [Comellas table](https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html) accessed on **2026-09-25** (page last changed 2026-09-24): **1,610 → 1,920**, an increase of **310 vertices (19.25%)**.

A 30-state 4-regular controller is lifted over $\mathbb F_4^3$. Edge-dependent matrices and five-plane covers establish the diameter bound. Here $\mathbb F_4$ is the field with four elements, not integers modulo 4.

This uses an edge-dependent variant of the affine route-chart framework in [arXiv:2606.15860](../diameter5-paper/), with local subspace covers adapted to diameter 3.

## Materials

- [Edge list](certificate/graph_d16_D3_n1920.edges) — first line `n m`, followed by one undirected edge `u v` per line, with zero-based vertex numbers.
- [Original package guide (Japanese)](certificate/README_ja.md).
- [Construction and proof (Japanese)](certificate/PROOF_ja.md).
- [Original certificate package](certificate/) — construction data, verification code, saved reports, and integrity manifest.

## Reproduce the verification

Python 3.10 or later, standard library only. From the repository root, copy the
package to a temporary directory because its scripts write regenerated files
and reports beside the construction data:

```bash
verify_dir=$(mktemp -d)
cp -R results/degree16-diameter3/certificate/. "$verify_dir/"
cd "$verify_dir"
python3 verify.py
cmp regenerated.edges graph_d16_D3_n1920.edges
```

All commands above passed during the **2026-09-25 repository update**. The
regenerated edge file matched the supplied file byte for byte. A subsequent
[final check directly from the edge list](../../verification/final/degree16-diameter3.json)
verified every vertex and every ordered pair, confirming the degree distribution,
connectivity, and exact diameter. Its distance histogram matches the supplied
BFS report. See [the method and reproduction commands](../../verification/README.md)
and [the repository verification record](../../VERIFICATION.md).

Edge-file SHA-256:

```text
dbdd15deead3c83b7e07f9e056846dd9a478feaa437385841ef36971c0af9a8a
```

The imported package is preserved without edits. This result is compared with
the dated public table; listing here does not assert table acceptance,
independent peer review, or optimality. This package has no separate paper.

[All results](../../README.md)
