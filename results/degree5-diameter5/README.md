# Degree 5, diameter 5: 660 vertices

A simple **5-regular** graph of order **660**, size **1,650**, and diameter
**exactly 5**. Thus $N(5,5)\ge660$.

Added to this repository on **2026-11-04**. The underlying construction
package is dated 2026-09-25; the regular completion used here was obtained
on 2026-11-03. The order exceeds the **650** in
[Comellas's table](https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html)
as accessed on 2026-11-04 by **10 vertices (1.54%)**. It is not yet reflected
in that table. This comparison does not assert optimality.

## Construction and symmetry

The vertices are the 660 elements of $L=\mathrm{PSL}(2,11)$, represented
as normalized projective matrices. Inside $P=\mathrm{PGL}(2,11)$, put
$h=\mathrm{diag}(1,-1)$ and choose the inverse-closed five-element set
$S\subset P\setminus L$ given in [construction.json](certificate/construction.json).
The base graph has edges $x\sim hxs$, for $s\in S$, with loops removed.
It has 1,635 edges, 30 vertices of degree 4, and 630 vertices of degree 5.
The finite identity $S^5=P\setminus L$ proves diameter at most 5.

The main graph adds a perfect matching on the 30 vertices of degree 4.
Write $B=\{b\in L:b^{-1}Sb=S\}$. At such a vertex $x$, set $s=x^{-1}hx$,
and let $b_s$ be the unique nonidentity involution in $B$ commuting with $s$.
The added edge is $x\sim xb_s$. These 15 edges make the graph 5-regular.

Its full automorphism group is the direct product of the **dihedral group
of order 10** and $S_3$, of order **60**. Explicitly, these automorphisms are
$x\mapsto axb^{-1}$, where $a\in C_L(h)$ and $b\in B$.
There are six vertex orbits of size 30 and eight of size 60.
The explicit actions and the [full-group computation](certificate/symmetry/)
are both checked. The graph is not vertex-transitive.

This construction folds a bipartite Cayley graph on $\mathrm{PGL}(2,11)$
and then adds a matching. It uses a different method from the route-chart
lift construction in [arXiv:2606.15860](../diameter5-paper/); it is not
obtained by changing that paper's controller.
See the [construction proof](certificate/proof.md).

## Variants

| Graph | Edges | Degrees | Full automorphism group order | Location |
|---|---:|---|---:|---|
| **Main graph: invariant matching** | **1,650** | **5-regular** | **60** | [Edge list](certificate/graph.edges) |
| Base graph, loops removed | 1,635 | 30 of degree 4; 630 of degree 5 | 60 | [Edge list](certificate/algebraic.edges) |
| September regular completion | 1,650 | 5-regular | 12 | Source archive: graphs/n55_660_regular.edges |

All three have 660 vertices and diameter 5. The main graph and the September
regular graph have different matchings; they are nonisomorphic, as their
automorphism groups have different orders. They establish the same numerical
lower bound, so the result index counts this parameter pair once.

## Data and verification

- [Main edge list](certificate/graph.edges): first line is the vertex count
  660 and edge count 1,650, then one undirected edge per line, with IDs 0–659.
- [Adjacency list](certificate/graph.adjlist) and
  [vertex ID to projective matrix table](certificate/vertices.tsv).
- [Construction data](certificate/construction.json),
  [constructor](certificate/construct.py), and [proof](certificate/proof.md).
- [Construction verification](../../verification/import-2026-11-04/degree5-diameter5-construction.json),
  [independent ordinary BFS](../../verification/independent-2026-11-04/degree5-diameter5.json),
  and [common C++ verification](../../verification/final/degree5-diameter5.json).
- [Exact September source archive](certificate/archive/n55_660_construction_2026-09-25.zip)
  and [provenance](certificate/provenance.json). The archive's regular graph
  is the September variant, not the main graph linked above.
- [SHA-256 manifest](SHA256SUMS).

From the repository root, using Python 3.10 or later:

    python3 results/degree5-diameter5/certificate/verify.py
    python3 results/degree5-diameter5/certificate/construct.py --output-dir /tmp/ddp-660
    python3 verification/verify_small_graphs.py --output /tmp/ddp-small-checks

The first command checks reconstruction, the product-set identity, the matching,
and the explicit symmetries against saved nauty generators. Recomputing the
full automorphism group requires nauty; its
[instructions](certificate/symmetry/README.md) are separate from the degree
and diameter verification, which requires no graph library.
