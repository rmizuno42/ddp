# Degree/diameter graph constructions

Explicit graphs, construction certificates, and verification code for the
degree/diameter problem. Let $N(\Delta,D)$ denote the largest possible order of a
simple undirected connected graph with maximum degree at most $\Delta$ and
diameter at most $D$.

## Published records and new graph — 2026-10-13

The following repository constructions match or exceed the record orders in
[Francesc Comellas's degree/diameter table](https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html),
accessed **2026-10-13** (page last changed **2026-10-11**).
The new (13,5) graph exceeds its entry and is not yet reflected in that table.
This dated overview does not assert optimality. See the
[saved comparison and incoming links](verification/table-snapshot-2026-10-13.json).

| $(\Delta,D)$ | Vertices | Published table order | Status | Construction and data |
|---|---:|---:|---|---|
| (12,4) | **5,832** | 5,832 | Matches table | [Degree 12, diameter 4](results/degree12-diameter4/) |
| **(13,5)** | **88,452** | 51,417 | **New; exceeds table** | [Degree 13, diameter 5](results/degree13-diameter5/) |
| (14,5) | **88,452** | 88,452 | Matches table | [Degree 14, diameter 5](results/degree14-diameter5/) |
| (15,5) | **100,000** | 100,000 | Matches table | [Degree 15, diameter 5](results/degree15-diameter5/) |
| (16,3) | **1,920** | 1,920 | Matches table | [Degree 16, diameter 3](results/degree16-diameter3/) |
| (16,5) | **147,456** | 147,456 | Matches table | [arXiv:2606.15860](results/diameter5-paper/) |

## Added in this update — 2026-10-13

**New: [degree 13, diameter 5, 88,452 vertices](results/degree13-diameter5/).**
The graph is simple and 13-regular, with diameter exactly 5. It has the same
order and diameter as the existing (14,5) graph, with a smaller maximum degree.

The new graph exceeds the published order by **37,035 vertices (+72.03%)**.
A [separate ordinary-BFS verification](verification/independent-2026-10-13/)
measured its order, every vertex degree, and exact diameter from the edge list,
without a search-depth limit or any construction data.

This result **exceeds the table entry and is not yet reflected in the table**
as accessed on 2026-10-13. Only this package is newly imported in this update.
Its finite construction data, proof, edge list, and verification programs are
in [the certificate directory](results/degree13-diameter5/certificate/).

## Complete result index

All comparisons below use the same **2026-10-13** table snapshot.
The package locations remain stable when their record status changes.

| $(\Delta,D)$ | Repository order | Table order | Status | Package |
|---|---:|---:|---|---|
| (12,4) | 5,832 | 5,832 | Matches table | [Summary](results/degree12-diameter4/) |
| (12,5) | 34,992 | 42,342 | Below table | [arXiv:2606.15860](results/diameter5-paper/) |
| (13,5) | 88,452 | 51,417 | **New; exceeds table** | [Summary](results/degree13-diameter5/) |
| (14,5) | 88,452 | 88,452 | Matches table | [Summary](results/degree14-diameter5/) |
| (15,3) | 1,458 | 1,539 | Below table | [Summary](results/degree15-diameter3/) |
| (15,5) | 100,000 | 100,000 | Matches table | [Summary](results/degree15-diameter5/) |
| (16,3) | 1,920 | 1,920 | Matches table | [Summary](results/degree16-diameter3/) |
| (16,5) | 147,456 | 147,456 | Matches table | [arXiv:2606.15860](results/diameter5-paper/) |

All eight indexed graphs passed
[verification directly from their edge lists](verification/README.md):
vertex counts, degrees, connectivity, and exact diameters were checked over
every ordered pair of vertices. See the [verification record](VERIFICATION.md)
and [machine-readable index](results.json), which also preserves the dated
September comparisons.

## Construction terminology

We use the terminology of [arXiv:2606.15860](results/diameter5-paper/),
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

The constructions below extend this controller-and-fiber approach as specified
in each summary. The (13,5) construction also uses matching maps that are not
all affine in the given fiber coordinates. Their diameter bounds are established
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
transitions as the (14,5) construction below. The graph combines affine
edges, a perfect matching between paired fibers, and a matching on 756
remaining vertices of degree 12. Some maps defining the main matching are
not affine. This develops the controller-and-fiber approach of
[arXiv:2606.15860](results/diameter5-paper/) through matching completion;
the complete graph is not asserted to be a route-chart lift as defined there.
The explicit edge list has been checked from every source.
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

This result is below the table order 1,539 as of 2026-10-13; its published
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

| $(\Delta,D)$ | Order in arXiv:2606.15860 | Table order on 2026-10-13 | Status on that date |
|---|---:|---:|---|
| (12,5) | 34,992 | 42,342 | Below the table order |
| (16,5) | 147,456 | 147,456 | Matches the table order |

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

The six imported `certificate/` directories preserve their source bytes,
including proof notes, manifests, and verification/search logs. Their source
notes describe the status at package creation; use the maintained summaries
and dated table snapshot for the status at this update. The September 2026
selection rule is retained as historical metadata in `results.json`.
Local-only archives and previously excluded candidates remain under the
Git-ignored `legacy/` directory.
