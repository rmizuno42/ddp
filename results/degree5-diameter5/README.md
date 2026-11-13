# Degree 5, diameter 5: 660 vertices

A simple graph of order **660**, size **1,635**, maximum degree **5**, and
diameter **exactly 5**. There are **30 vertices of degree 4** and **630 of
degree 5**. Thus $N(5,5)\ge660$; regularity is not required for this bound.

Added to this repository on **2026-11-04**. The underlying construction
package is dated 2026-09-25. The order exceeded the **650** in
[Comellas's table](https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html)
as accessed on 2026-11-04 by **10 vertices (1.54%)**. This comparison does not
assert optimality.

**Table status on 2026-11-13:** the main table (page last changed 2026-11-12) lists
**660** for (5,5), credited to Ryosuke Mizuno. The [detail page](https://web.mat.upc.edu/francesc.comellas/delta-d/desc_g/desc_g5.html#55)
still describes the earlier 650-vertex graph. See the [dated repository comparison](../../verification/table-snapshot-2026-11-13.json).

## Construction and symmetry

The vertices are the 660 elements of $L=\mathrm{PSL}(2,11)$, represented
as normalized projective matrices. Inside $P=\mathrm{PGL}(2,11)$, put
$h=\mathrm{diag}(1,-1)$, so $h^2=1$, and choose the inverse-closed five-element set
$S\subset P\setminus L$ given in [construction.json](certificate/construction.json).
The graph has edges $x\sim hxs$, for $s\in S$, with loops removed.
It has 1,635 edges, 30 vertices of degree 4, and 630 vertices of degree 5.
The finite identity $S^5=P\setminus L$ proves diameter at most 5.

To see why the diameter bound holds, take any $x,y\in L$. Since
$x^{-1}hy\in P\setminus L=S^5$, it can be written as $s_1\cdots s_5$ with
each $s_i\in S$. The five successive maps $z\mapsto hzs_i$ take $x$ to

$$
h^5x(s_1\cdots s_5)=h^5x(x^{-1}hy)=h^6y=(h^2)^3y=y.
$$

Thus the factor $h^5$ is accounted for using $h^2=1$.
Any stationary steps can be omitted, so removing
loops leaves a walk of length at most 5. The Moore bound for maximum degree
5 and diameter at most 4 is 426, which is less than 660; thus the diameter
is exactly 5. No additional edges are needed.

Its full automorphism group is the direct product of the **dihedral group
of order 10** and $S_3$, of order **60**. Explicitly, these automorphisms are
$x\mapsto axb^{-1}$, where $a\in C_L(h)$ and
$b\in B=\{b\in L:b^{-1}Sb=S\}$.
There are six vertex orbits of size 30 and eight of size 60.
The explicit actions and the [full-group computation](certificate/symmetry/)
are both checked. The graph is not vertex-transitive.

This construction folds a bipartite Cayley graph on $\mathrm{PGL}(2,11)$
by identifying $g$ with $hg$, then removes loops.
See the [construction proof](certificate/proof.md).

## Data history

The main edge list is the loopless algebraic graph from the September source
archive. The existing [algebraic edge-list link](certificate/algebraic.edges)
is retained as an identical copy. Vertex labels and public file paths are preserved.
An earlier repository version added a 15-edge matching; that completion is
retained in Git history. The unmodified source archive also contains a
September regular completion. The maintained constructor generates the
1,635-edge graph without either matching.

## Data and verification

- [Main edge list](certificate/graph.edges): first line is the vertex count
  660 and edge count 1,635, then one undirected edge per line, with IDs 0–659.
- [Adjacency list](certificate/graph.adjlist) and
  [vertex ID to projective matrix table](certificate/vertices.tsv).
- [Construction data](certificate/construction.json),
  [constructor](certificate/construct.py), and [proof](certificate/proof.md).
- [Construction verification](../../verification/import-2026-11-04/degree5-diameter5-construction.json),
  [independent ordinary BFS](../../verification/independent-2026-11-04/degree5-diameter5.json),
  and [common C++ verification](../../verification/final/degree5-diameter5.json).
- [Exact September source archive](certificate/archive/n55_660_construction_2026-09-25.zip)
  and [provenance](certificate/provenance.json). The main graph corresponds
  to `graphs/n55_660_algebraic.edges` in the archive, with a standardized header.
- [SHA-256 manifest](SHA256SUMS).

From the repository root, using Python 3.10 or later:

    python3 results/degree5-diameter5/certificate/verify.py
    python3 results/degree5-diameter5/certificate/construct.py --output-dir /tmp/ddp-660
    python3 verification/verify_small_graphs.py --output /tmp/ddp-small-checks

The first command checks reconstruction, the product-set identity, the degree distribution,
and the explicit symmetries against saved nauty generators. Recomputing the
full automorphism group requires nauty; its
[instructions](certificate/symmetry/README.md) are separate from the degree
and diameter verification, which requires no graph library.
