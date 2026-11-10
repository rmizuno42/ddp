# Degree 6, diameter 3: 126 vertices

A simple **6-regular** graph of order **126**, size **378**, and diameter **exactly 3**.
Thus $N(6,3)\ge126$.

Added to this repository on **2026-11-10**. The order exceeds the **120** in
[Comellas's table](https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html)
as accessed on 2026-11-10 (page last changed 2026-11-04) by **6 vertices (5%)**; the Moore bound
is 187. It is not yet reflected in that table. This comparison does not assert optimality.

## Construction

The graph is a regular cover of a 14-vertex base multigraph with voltage group
$N=\mathbb Z_3\times\mathbb Z_3$. Vertices are $(u,x)$ with $u\in\{0,\ldots,13\}$ and
$x\in N$, numbered $9u+3x_0+x_1$; a base edge $u\to v$ with voltage $g$ joins
$(u,x)$ to $(v,x+g)$.

The base graph has two hubs $h=0$, $h'=1$ joined by three parallel edges; a triangle
$A=\{2,3,4\}$ adjacent to $h$; vertices $\{5,6,7\}$ joined to $A$ by a complete bipartite graph;
the same configuration $A'=\{8,9,10\}$, $\{11,12,13\}$ attached to $h'$; and three parallel edges
between $5+j$ and $11+j$ for $j=0,1,2$. Writing $a_l=2+l$ and $b_j=5+j$:

| base edges | voltages in $\mathbb Z_3^2$ |
|---|---|
| $h\to h'$ (3 edges) | $(0,0),(1,1),(2,1)$ — the parabola $\{(t,t^2)\}$ |
| $h\to a_l$, and $a_0\to b_j$ | $0$ |
| $a_l\to a_m$ | $(m-l)\,(0,2)$ |
| $a_l\to b_j$ | $l\,w_j$, with $w_0=(2,0)$, $w_1=(1,1)$, $w_2=(1,0)$ |
| $b_0\to b'_0$ (3 edges) | $(2,2),(0,2),(0,1)$ |
| $b_1\to b'_1$ (3 edges) | $(2,0),(2,1),(1,2)$ |
| $b_2\to b'_2$ (3 edges) | $(1,0),(0,0),(0,2)$ |

The second half ($h'$, $A'$, $b'_j$) carries exactly the same voltages as the first.
Each triple of parallel voltages is a relative difference set in $\mathbb F_3^2$ avoiding one
direction, and the four directions each occur once; see the [proof](certificate/proof.md).

## Symmetry and origin

The translations by $N$ act freely, so the graph is a regular $\mathbb Z_3^2$-cover of the base
graph. The full automorphism group, computed with nauty and identified with GAP, has order
**162** (SmallGroup(162,40)) and three vertex orbits of sizes 54, 54 and 18.

The graph was found on 2026-11-10 by a systematic search over *orbit graphs* — unions of orbitals
of a finite group acting on a disjoint union of coset spaces — as the graph of
SmallGroup(108,33) on $G/C_6\sqcup G/C_2\sqcup G/C_2$ (18 + 54 + 54 points). The same graph, up to
isomorphism, also arose from SmallGroup(108,8) and SmallGroup(108,43). The search code is in
[search/orbit-graphs](../../search/orbit-graphs/).

## Data and verification

- [Edge list](certificate/graph.edges): first line is the vertex count 126 and edge count 378,
  then one undirected edge per line, with IDs 0–125.
- [Adjacency list](certificate/graph.adjlist): each row gives a vertex and its six neighbors.
- [Constructor](certificate/construct.py), [voltage description](certificate/voltage_graph.json),
  [proof](certificate/proof.md), and [14 spanning trees](certificate/certificates/base_trees.json).
- [Orbit-graph certificate](certificate/orbit_graph_certificate.json) with an explicit isomorphism
  to the published labelling, and [automorphism generators](certificate/automorphisms.json).
- [Construction verification](../../verification/import-2026-11-10/degree6-diameter3-construction.json),
  [independent ordinary BFS](../../verification/independent-2026-11-10/degree6-diameter3.json),
  and [common C++ verification](../../verification/final/degree6-diameter3.json).
- [Provenance](certificate/provenance.json) and [SHA-256 manifest](SHA256SUMS).

From the repository root, using Python 3.10 or later (standard library only):

    python3 results/degree6-diameter3/certificate/verify.py
    python3 results/degree6-diameter3/certificate/construct.py --out /tmp/ddp-126
    python3 verification/verify_small_graphs.py --output /tmp/ddp-small-checks

The first command checks that the formula reproduces the published files, the 14 spanning trees,
the modular reachability of all 196 pairs of base vertices, the isomorphism with the orbit graph
found by the search, and the automorphism generators. The last command independently checks the
November additions by ordinary BFS from every vertex, without a depth limit or construction data.
