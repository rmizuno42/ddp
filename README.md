# Degree/diameter graph constructions

Explicit graphs, construction certificates, and verification code for the
degree/diameter problem. Let $N(\Delta,D)$ denote the largest possible order of a
simple undirected connected graph with maximum degree at most $\Delta$ and
diameter at most $D$.

## Published records and latest additions — 2026-11-04

The following repository constructions match or exceed the record orders in
[Francesc Comellas's degree/diameter table](https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html),
accessed **2026-11-04** (page last changed **2026-11-03**).
The **(3,7) and (5,5) graphs added on 2026-11-04**, and the (13,5) graph
added on 2026-10-13, exceed their entries and are not yet reflected in that
table. The (16,3) graph matches its table entry.
This dated overview does not assert optimality. See the
[saved comparison and incoming links](verification/table-snapshot-2026-11-04.json).

Comparisons use the main table: some linked detail pages still describe earlier
records. In particular, their orders for (12,4), (15,5), and (16,5) have not yet
caught up with the main table.

| $(\Delta,D)$ | Vertices | Published table order | Status | Construction and data |
|---|---:|---:|---|---|
| **(3,7)** | **208** | 200 | **New; exceeds table** | [Degree 3, diameter 7](results/degree3-diameter7/) |
| **(5,5)** | **660** | 650 | **New; exceeds table** | [Degree 5, diameter 5](results/degree5-diameter5/) |
| **(13,5)** | **88,452** | 51,417 | **Added 2026-10-13; exceeds table** | [Degree 13, diameter 5](results/degree13-diameter5/) |
| (16,3) | **1,920** | 1,920 | Matches table | [Degree 16, diameter 3](results/degree16-diameter3/) |

## Latest additions — 2026-11-04

- **[(3,7), 208 vertices](results/degree3-diameter7/)**: a cubic cyclic voltage
  graph, exceeding the table order by **8 (+4%)**. Its full automorphism
  group is $C_{16}$. The package includes diagrams showing its 16-fold
  rotational symmetry and the quotient with its edge shifts.
- **[(5,5), 660 vertices](results/degree5-diameter5/)**: a folded Cayley graph
  with an added matching, exceeding the table order by **10 (+1.54%)**.
  The main graph is 5-regular and has full automorphism-group order 60.
  The base graph and the September regular completion are also preserved.

Both have the exact claimed diameter. Their published edge lists passed
[independent ordinary BFS from every vertex](verification/independent-2026-11-04/)
and the common C++ verifier. Each package includes an English construction
proof, reproducible code, and its unmodified September source archive.
The 660-vertex main graph uses the invariant matching obtained on 2026-11-03.

## Earlier addition — 2026-10-13

**[degree 13, diameter 5, 88,452 vertices](results/degree13-diameter5/).**
The graph is simple and 13-regular, with diameter exactly 5. It has the same
order and diameter as the existing (14,5) graph, with a smaller maximum degree.

This graph exceeds the published order by **37,035 vertices (+72.03%)**.
A [separate ordinary-BFS verification](verification/independent-2026-10-13/)
measured its order, every vertex degree, and exact diameter from the edge list,
without a search-depth limit or any construction data.

This result **exceeds the table entry and is not yet reflected in the table**
as accessed on 2026-11-04. This package was added on 2026-10-13.
Its finite construction data, proof, edge list, and verification programs are
in [the certificate directory](results/degree13-diameter5/certificate/).

## Subsequent records based on repository graphs

The detail pages describe two larger graphs by Sami Hani Badaoui and Sarah
Ellen Mary Vaughan, communicated on 2026-10-22, as modifications and extensions
of the corresponding Mizuno graphs below. One remains the table record; the
other has since been surpassed.

| $(\Delta,D)$ | Repository graph | Described extension | Current table order |
|---|---:|---|---:|
| (14,5) | [88,452](results/degree14-diameter5/) | [SamSar_94186: 94,186](https://web.mat.upc.edu/francesc.comellas/delta-d/desc_g/desc_g5.html#145) | 94,186 |
| (15,5) | [100,000](results/degree15-diameter5/) | [SamSar_100132: 100,132](https://web.mat.upc.edu/francesc.comellas/delta-d/desc_g/desc_g5.html#155) | 102,060 |

The former edge lists linked on that site have exactly the same labeled edge
sets as the repository graphs. The attribution above follows the published
descriptions; a vertex correspondence to the new graphs has not been
reconstructed. See the [source review and edge-file comparison](verification/external-records-2026-10-23/).
The (15,5) detail page still describes the 100,132-vertex graph, so this
attribution does not establish that the current 102,060-vertex graph is based
on the repository construction.
Both repository packages retain their published paths as former records.

## Complete result index

All comparisons below use the same **2026-11-04** table snapshot.
The package locations remain stable when their record status changes.

| $(\Delta,D)$ | Repository order | Table order | Status | Package |
|---|---:|---:|---|---|
| **(3,7)** | **208** | 200 | **Added 2026-11-04; exceeds table** | [Summary](results/degree3-diameter7/) |
| **(5,5)** | **660** | 650 | **Added 2026-11-04; exceeds table** | [Summary](results/degree5-diameter5/) |
| (12,4) | 5,832 | 6,156 | Below table | [Summary](results/degree12-diameter4/) |
| (12,5) | 34,992 | 42,342 | Below table | [arXiv:2606.15860](results/diameter5-paper/) |
| (13,5) | 88,452 | 51,417 | **Added 2026-10-13; exceeds table** | [Summary](results/degree13-diameter5/) |
| (14,5) | 88,452 | 94,186 | Below table; basis of the current record | [Summary](results/degree14-diameter5/) |
| (15,3) | 1,458 | 1,620 | Below table | [Summary](results/degree15-diameter3/) |
| (15,5) | 100,000 | 102,060 | Below table; basis of the earlier 100,132-vertex record | [Summary](results/degree15-diameter5/) |
| (16,3) | 1,920 | 1,920 | Matches table | [Summary](results/degree16-diameter3/) |
| (16,5) | 147,456 | 153,600 | Below table | [arXiv:2606.15860](results/diameter5-paper/) |

All ten indexed graphs passed
[verification directly from their edge lists](verification/README.md):
vertex counts, degrees, connectivity, and exact diameters were checked over
every ordered pair of vertices. See the [verification record](VERIFICATION.md)
and [machine-readable index](results.json), which also preserves the earlier
dated comparisons.

## Construction terminology

For the route-chart constructions, we use the terminology of [arXiv:2606.15860](results/diameter5-paper/),
especially §§A.2–A.4. In that paper, a **controller** is an auxiliary simple
regular graph $C$. A **route-chart lift graph** has vertex set
$V(C)\times\mathbb F_q^s$, and the **fiber** over $u\in V(C)$ is
$\{u\}\times\mathbb F_q^s$. The directed edges of $C$ carry an
**inverse-consistent labeling**. A **route chart** assigns an invertible matrix
$A_t\in\mathrm{GL}_s(\mathbb F_q)$ and a vector $b_t\in\mathbb F_q^s$
to each label $t$, with the inverse-symbol conditions specified in §A.4.
The edge rule is

$$
(u,x)\sim(v,A_tx+\lambda b_t),\qquad \lambda\in\mathbb F_q,
$$

where the directed controller edge $u\to v$ has label $t$.

The paper's sufficient conditions for diameter at most $s$ are an
**exact-NB-$s$ controller** (every ordered pair of controller vertices is joined
by a nonbacktracking walk of length exactly $s$) and a **universal route chart**
(the controllability matrix $M_w$ is nonsingular for every reduced word $w$ of
length $s$). The inverse map on labels is fixed-point-free in the paper.

The (12,4), (13,5), (14,5), (15,3), (15,5), and (16,3) constructions
use or extend this controller-and-fiber approach as specified in each summary.
The (3,7) cyclic voltage construction and the (5,5) folded Cayley construction
use different methods, described separately below.

The (13,5) construction also uses matching maps that are not all affine in the given fiber coordinates. Their diameter bounds are established
by the accompanying certificates. Rank statements for the affine parts refer
to **controllability matrices**. For a fixed controller walk with label word
$w$, the paper's edge rule gives reachable fiber coordinates
$A_wx+\mathrm{im}(M_w)$, using the
same matrix formula with one column per step. In the generalizations with
matrices depending on directed edges, these products and controllability
matrices depend on the directed-edge sequence. In affine diameter certificates
using several walks, their affine reachable sets are verified to cover all
target fiber coordinates for every initial coordinate $x$. Some of these
certificates use **pencils of hyperplanes**:
the $q+1$ hyperplanes containing a fixed subspace of codimension two. These
hyperplanes, and their translates by a common vector, cover $\mathbb F_q^s$.

## Construction summaries

### (3,7): 208 vertices — added 2026-11-04

A simple cubic graph on $\{0,\ldots,12\}\times\mathbb Z_{16}$ with 312 edges,
diameter exactly 7, and girth 9. A path through the 13 states, six translated
chord families, one cycle, and one matching specify every edge. Its full
automorphism group is $C_{16}$. Thirteen depth-7 spanning trees and cyclic
translation give a finite diameter certificate. This is a cyclic voltage
construction, rather than a route-chart lift as defined in arXiv:2606.15860.
[Construction, proof, certificates, and diagrams](results/degree3-diameter7/).

### (5,5): 660 vertices — added 2026-11-04

A simple 5-regular graph on $\mathrm{PSL}(2,11)$ with 1,650 edges and diameter
exactly 5. The base adjacency $x\sim hxs$ folds a bipartite Cayley graph on
$\mathrm{PGL}(2,11)$. A 15-edge matching on its degree-4 vertices makes it
regular while retaining the full automorphism group, the direct product of
the dihedral group of order 10 and $S_3$. The identity
$S^5=\mathrm{PGL}(2,11)\setminus\mathrm{PSL}(2,11)$ proves the diameter upper
bound. This construction uses a different method from arXiv:2606.15860.
[Construction, proof, and certificates](results/degree5-diameter5/).

### (12,4): 5,832 vertices

A simple 12-regular route-chart lift graph on $V(C)\times\mathbb F_3^4$,
where $C$ is a 72-vertex simple 4-regular controller. The graph has 34,992 edges
and diameter exactly 4. This uses the route-chart lift definition in
[arXiv:2606.15860](results/diameter5-paper/), with a different diameter
certificate: nonsingular controllability matrices for selected length-4 walks,
pencils of affine hyperplanes, and unions of affine planes establish the upper
bound 4. [Construction, proof, and certificates](results/degree12-diameter4/).

### (13,5): 88,452 vertices — added 2026-10-13

A simple 13-regular graph on $C\times\mathbb F_3^5$ with 574,938 edges
and diameter exactly 5. Its 364-state, four-port controller has the same
transitions as the (14,5) construction below, including transitions from a
state to itself. It uses different affine data, a perfect matching between
paired fibers, and a further matching on the 756 vertices whose degree is
still 12 after the first matching is added. The affine part alone has vertex
pairs at distance greater than 5; the added edges also provide paths needed
to achieve the diameter bound.

This construction develops the controller-and-fiber approach of
[arXiv:2606.15860](results/diameter5-paper/) by changing both the controller
and the fiber connections. Some maps defining the main matching are not
affine in the given fiber coordinates. The resulting graph is not asserted
to be a route-chart lift graph as defined in that paper. Its diameter is
certified by exhaustive BFS from every vertex, rather than by applying the
paper's route-chart lift principle.
[Construction, proof, and certificates](results/degree13-diameter5/).

### (14,5): 88,452 vertices

A graph on $C\times\mathbb F_3^5$, where $C$ is a set of 364 states with four
labeled involutions, some of which fix states. This generalizes the controller
used in [arXiv:2606.15860](results/diameter5-paper/) to allow transitions from
a state to itself and adds translation edges within each fiber. After removing
loops and repeated edges, the graph is simple, has maximum degree 14 and diameter
exactly 5; 756 vertices have degree 13 and 87,696 have degree 14.
[Construction, proof, and certificates](results/degree14-diameter5/).

### (15,3): 1,458 vertices

This result is below the table order 1,620 as of 2026-11-04; its published
package path and all certificates are retained.

A simple 15-regular graph on $V(C)\times\mathbb F_3^3$, where $C$ is a
54-vertex simple 5-regular Cayley graph. The route-chart lift construction of
[arXiv:2606.15860](results/diameter5-paper/) is generalized to allow a
self-inverse label and transition matrices depending on directed controller
edges. Controllability matrices of rank 3 and pencils of affine planes give
diameter at most 3; direct verification establishes diameter exactly 3.
[Construction, proof, and certificates](results/degree15-diameter3/).

### (15,5): 100,000 vertices

A simple 15-regular graph on $V(C)\times\mathbb F_5^5$, where $C$ is a
32-vertex simple 3-regular controller. This generalizes the route-chart lift
construction of [arXiv:2606.15860](results/diameter5-paper/) to allow a
self-inverse label. Nonsingular controllability matrices and pencils of affine
hyperplanes establish diameter at most 5 for all 1,024 ordered pairs of
controller vertices; the graph has diameter exactly 5.
[Construction, proof, and certificates](results/degree15-diameter5/).

### (16,3): 1,920 vertices

A simple 16-regular graph on $V(C)\times\mathbb F_4^3$, where $C$ is a
30-vertex simple 4-regular controller. This generalizes the route-chart lift
construction of [arXiv:2606.15860](results/diameter5-paper/) by allowing
transition matrices to depend on directed controller edges. Controllability
matrices of rank 3 and pencils of affine planes establish diameter at most 3;
direct verification establishes diameter exactly 3.
[Construction, proof, and certificates](results/degree16-diameter3/).

### arXiv:2606.15860: (12,5) and (16,5)

[arXiv:2606.15860](https://arxiv.org/abs/2606.15860) established $N(12,5)\ge34{,}992$ and
$N(16,5)\ge147{,}456$, improving the then-recorded orders 29,621 and 132,496.
It also documents the discovery process through a browser-based ChatGPT
dialogue. The paper, bibliography, transcript, and supplementary packages are
preserved together in [the arXiv:2606.15860 package](results/diameter5-paper/).

| $(\Delta,D)$ | Order in arXiv:2606.15860 | Table order on 2026-11-04 | Status on that date |
|---|---:|---:|---|
| (12,5) | 34,992 | 42,342 | Below the table order |
| (16,5) | 147,456 | 153,600 | Below the table order |

[Paper PDF](https://github.com/rmizuno42/ddp/releases/latest/download/paper.pdf)
· [arXiv:2606.15860](https://arxiv.org/abs/2606.15860)
· [LaTeX source](results/diameter5-paper/paper.tex)
· [Citation formats](results/diameter5-paper/README.md#citation)

## Layout and stable links

```text
README.md                       current table status, updates, and summaries
results.json                    machine-readable index and dated comparisons
VERIFICATION.md                 checks performed and reproduction notes
verification/                   direct verifier, reports, and table snapshot
results/
  diameter5-paper/              arXiv:2606.15860 and its supplementary materials
  degree3-diameter7/            summary, certificates, and symmetry diagrams
  degree5-diameter5/            summary, certificates, and graph variants
  degree12-diameter4/           summary and certificate package
  degree13-diameter5/           added 2026-10-13: summary and certificate package
  degree14-diameter5/           summary and certificate package
  degree15-diameter3/           summary and certificate package
  degree15-diameter5/           summary and certificate package
  degree16-diameter3/           summary and certificate package
```

Existing result directories and graph files keep their published paths,
including the five directories linked from the Comellas detail pages.
Results that fall below later table entries remain alongside the other
packages; the overview and index identify their status.

The six certificate directories imported before November preserve their source bytes,
including proof notes, manifests, and verification/search logs. Their source
notes describe the status at package creation; use the maintained summaries
and dated table snapshot for the status at this update. The September 2026
selection rule is retained as historical metadata in `results.json`.
The two November packages provide maintained English proofs and portable
verification programs, with their unmodified source ZIPs in `certificate/archive/`.
Previously excluded candidates remain outside the published result index.
