# Degree/diameter graph constructions

Explicit graphs, construction certificates, and verification code for the
degree/diameter problem. Let $N(\Delta,D)$ denote the largest possible order of a
simple undirected connected graph with maximum degree at most $\Delta$ and
diameter at most $D$.

The materials for [arXiv:2606.15860](results/diameter5-paper/) and the new results
are sibling packages under [`results/`](results/). Each package has its own
summary and data. The new packages contain concise documentation and
verification materials.

## Results at a glance

Comparison source: [Francesc Comellas's degree/diameter table](https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html),
accessed **2026-09-25**, with the page reporting its last change as **2026-09-24**.
Differences below are relative to that dated table, not to earlier candidates.

| Package | $(\Delta,D)$ | Vertices | Table order | Difference | Increase |
|---|---:|---:|---:|---:|---:|
| [Degree 12, diameter 4](results/degree12-diameter4/) | (12,4) | **5,832** | 5,184 | +648 | +12.50% |
| [Degree 14, diameter 5](results/degree14-diameter5/) | (14,5) | **88,452** | 61,887 | +26,565 | +42.93% |
| [Degree 15, diameter 3](results/degree15-diameter3/) | (15,3) | **1,458** | 1,224 | +234 | +19.12% |
| [Degree 15, diameter 5](results/degree15-diameter5/) | (15,5) | **100,000** | 82,684 | +17,316 | +20.94% |
| [Degree 16, diameter 3](results/degree16-diameter3/) | (16,3) | **1,920** | 1,610 | +310 | +19.25% |

These comparisons do not imply acceptance into the public table or optimality.
See [verification performed during this repository update](VERIFICATION.md)
and the [machine-readable result index](results.json).

All seven indexed graphs, including the two from arXiv:2606.15860, passed
[final verification directly from their edge lists](verification/README.md):
vertex counts, degrees, connectivity, and exact diameters were checked over
every ordered pair of vertices.

## Construction terminology

We use the terminology of [arXiv:2606.15860](results/diameter5-paper/),
especially §§A.2–A.4. In that paper, a **controller** is an auxiliary simple
regular graph $C$. A **route-chart lift graph** has vertex set
$V(C)\times\mathbb F_q^s$, and the **fiber** over $u\in V(C)$ is
$\{u\}\times\mathbb F_q^s$. The directed edges of $C$ carry an
**inverse-consistent labeling**. A **route chart** assigns an invertible matrix
$A_t\in\operatorname{GL}_s(\mathbb F_q)$ and a vector $b_t\in\mathbb F_q^s$
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

The constructions below use the same controller-and-fiber approach, with the
modifications specified in each summary. Their diameter bounds are established
by the accompanying certificates. Rank statements refer to **controllability
matrices**. For a fixed controller walk with label word $w$, the paper's edge
rule gives reachable fiber coordinates $A_wx+\operatorname{im}M_w$, using the
same matrix formula with one column per step. In the generalizations with
matrices depending on directed edges, these products and controllability
matrices depend on the directed-edge sequence. When several walks are needed,
the certificate verifies that
their affine reachable sets cover all target fiber coordinates for every
initial coordinate $x$. The new proof notes also use **pencils of hyperplanes**:
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

### (14,5): 88,452 vertices

A graph on $C\times\mathbb F_3^5$, where $C$ is a set of 364 states with four
labeled involutions, some of which fix states. This generalizes the controller
used in [arXiv:2606.15860](results/diameter5-paper/) to allow transitions from
a state to itself and adds translation edges within each fiber. After removing
loops and repeated edges, the graph is simple, has maximum degree 14 and diameter
exactly 5; 756 vertices have degree 13 and 87,696 have degree 14.
[Construction, proof, and certificates](results/degree14-diameter5/).

### (15,3): 1,458 vertices

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

| $(\Delta,D)$ | Order in arXiv:2606.15860 | Table order on 2026-09-25 | Current status |
|---|---:|---:|---|
| (12,5) | 34,992 | 38,167 | Historical result; the table now has a larger graph |
| (16,5) | 147,456 | 147,456 | Matches the table |

[Paper PDF](https://github.com/rmizuno42/ddp/releases/latest/download/paper.pdf)
· [arXiv:2606.15860](https://arxiv.org/abs/2606.15860)
· [LaTeX source](results/diameter5-paper/paper.tex)
· [Citation formats](results/diameter5-paper/README.md#citation)

## Layout and selection

```text
README.md                       summaries and dated comparisons
results.json                    machine-readable index
VERIFICATION.md                 checks performed and reproduction notes
verification/                   final edge-list verifier and all-pairs reports
results/
  diameter5-paper/              arXiv:2606.15860 and its supplementary materials
  degree12-diameter4/           summary, certificate package, and direct verifier
  degree14-diameter5/           summary and original certificate package
  degree15-diameter3/           summary and original certificate package
  degree15-diameter5/           summary and original certificate package
  degree16-diameter3/           summary and original certificate package
```

For the September import, keep the largest new graph for each parameter pair,
then retain it here if its order exceeds the dated table by at least **5%**.
The results in arXiv:2606.15860 are retained independently of this filter. Smaller
improvements, results below the table, and superseded candidates were moved to
the local-only `legacy/` directory, which is excluded from Git. Original import
ZIPs are also kept there as local backups; the extracted certificate packages
are published under `results/`.

The five imported `certificate/` directories preserve their source bytes,
including the Japanese proof notes, manifests, and verification/search logs.
Their original notes describe the status at package creation. Use the package
summaries and `VERIFICATION.md` for the checks performed in this repository.
