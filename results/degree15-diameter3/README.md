# Degree 15, diameter 3: 1,458 vertices

**$N(15,3)\ge 1{,}458$.** Simple undirected connected 15-regular graph;
10,935 edges, diameter exactly 3.

Compared with the [Comellas table](https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html) accessed on **2026-09-25** (page last changed 2026-09-24): **1,224 → 1,458**, an increase of **234 vertices (19.12%)**.

The vertex set is $V(C)\times\mathbb F_3^3$, where the controller $C$ is a
54-vertex simple 5-regular Cayley graph. This generalizes the route-chart lift
construction in §A.4 of [arXiv:2606.15860](../diameter5-paper/) by allowing a
self-inverse label and transition matrices that depend on the directed
controller edge. The reverse-edge conditions ensure that the adjacency
relation is symmetric. The Cayley graph here is the controller; no Cayley
property of the final graph is asserted.

For 2,646 ordered pairs of controller vertices, the certificate supplies a
length-3 walk whose controllability matrix has rank 3. The remaining 270 pairs
are adjacent controller vertices. For each such pair and each starting fiber
coordinate, reachable affine planes form a pencil of four planes containing a
common affine line; their union is $\mathbb F_3^3$. This proves diameter at
most 3. The Moore bound for maximum degree 15 and diameter at most 2 is 226,
less than 1,458, so the diameter is exactly 3.

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
