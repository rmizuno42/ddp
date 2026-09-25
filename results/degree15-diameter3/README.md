# Degree 15, diameter 3: 1,458 vertices

**$N(15,3)\ge 1,458$.** Simple undirected connected graph; 10,935 edges,
maximum degree 15, diameter exactly 3.

Compared with the [Comellas table](https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html) accessed on **2026-09-25** (page last changed 2026-09-24): **1,224 → 1,458**, an increase of **234 vertices (19.12%)**.

A 54-state Cayley controller is lifted over $\mathbb F_3^3$. Inverse-compatible linear maps, full-rank three-step routes, and four-plane covers establish the diameter bound.

This shares the controller/fiber affine-lift framework of [arXiv:2606.15860](../diameter5-paper/), adapted to diameter 3 with edge-dependent maps and subspace covers.

## Materials

- [Edge list](certificate/graph_d15_D3_n1458.edges) — first line `n m`, followed by one undirected edge `u v` per line, with zero-based vertex numbers.
- [Original package guide (Japanese)](certificate/README_ja.md).
- [Construction and proof (Japanese)](certificate/PROOF_ja.md).
- [Original certificate package](certificate/) — construction data, verification code, saved reports, and integrity manifest.

## Reproduce the verification

Python 3.10 or later, standard library only. From the repository root, copy the
package to a temporary directory because its scripts write regenerated files
and reports beside the construction data:

```bash
verify_dir=$(mktemp -d)
cp -R results/degree15-diameter3/certificate/. "$verify_dir/"
cd "$verify_dir"
python3 verify.py
python3 verify_uniform.py
cmp regenerated.edges graph_d15_D3_n1458.edges
```

All commands above passed during the **2026-09-25 repository update**. The
regenerated edge file matched the supplied file byte for byte. A subsequent
[final check directly from the edge list](../../verification/final/degree15-diameter3.json)
verified every vertex and every ordered pair, confirming the degree distribution,
connectivity, and exact diameter. Its distance histogram matches the supplied
BFS report. See [the method and reproduction commands](../../verification/README.md)
and [the repository verification record](../../VERIFICATION.md).

Edge-file SHA-256:

```text
85182ecb372ce24b3fdc1912ca0c14a6cec5353400ef3a6f4bd94b4520113546
```

The imported package is preserved without edits. This result is compared with
the dated public table; listing here does not assert table acceptance,
independent peer review, or optimality. This package has no separate paper.

[All results](../../README.md)
