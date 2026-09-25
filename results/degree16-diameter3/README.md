# Degree 16, diameter 3: 1,920 vertices

**$N(16,3)\ge 1{,}920$.** Simple undirected connected 16-regular graph;
15,360 edges, diameter exactly 3.

Compared with the [Comellas table](https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html) accessed on **2026-09-25** (page last changed 2026-09-24): **1,610 → 1,920**, an increase of **310 vertices (19.25%)**.

The vertex set is $V(C)\times\mathbb F_4^3$, where $C$ is a 30-vertex simple
4-regular controller. Here $\mathbb F_4=\mathbb F_2[\alpha]/(\alpha^2+\alpha+1)$.
This generalizes the route-chart lift construction in §A.4 of
[arXiv:2606.15860](../diameter5-paper/) by assigning transition matrices $T_e$
to directed controller edges $e$, with $T_{\bar e}=T_e^{-1}$, rather than
assigning one matrix to each label.

For 780 ordered pairs of controller vertices, including all equal-endpoint
pairs, the certificate supplies a length-3 walk whose controllability matrix
has rank 3. The other 120 pairs are adjacent controller vertices. For each
such pair and each starting fiber coordinate, reachable affine planes form a
pencil of five planes containing a common affine line; their union is
$\mathbb F_4^3$. This proves diameter at most 3. The Moore bound for maximum
degree 16 and diameter at most 2 is 257, less than 1,920, so the diameter is
exactly 3.

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
