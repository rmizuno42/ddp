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

All five new constructions use variants of the
controller/fiber affine route-chart framework described in
[arXiv:2606.15860](results/diameter5-paper/). Their adaptations include
state-dependent translations, edge-dependent maps, and subspace covers that
combine several routes to reach an entire fiber.

### (12,4): 5,832 vertices

A 12-regular lift of a 72-state controller over $\mathbb F_3^4$, with 34,992
edges and diameter exactly 4. This extends the affine route-chart method in
[arXiv:2606.15860](results/diameter5-paper/) by combining full-rank routes with subspace covers for short
routes and pairs in the same fiber. A finite certificate and all-source BFS
verify the construction. [Construction, proof, and certificates](results/degree12-diameter4/).

### (14,5): 88,452 vertices

A lift of a 364-state controller over $\mathbb F_3^5$, with additional
state-dependent translations inside each fiber. The graph has maximum degree
14 and diameter exactly 5; 756 vertices have degree 13 and 87,696 have degree
14. [Construction, proof, and certificates](results/degree14-diameter5/).

### (15,3): 1,458 vertices

A 15-regular affine lift of a 54-state Cayley controller over
$\mathbb F_3^3$. Short routes and finite subspace covers certify diameter 3.
[Construction, proof, and certificates](results/degree15-diameter3/).

### (15,5): 100,000 vertices

A 15-regular lift of a 32-state cubic controller over $\mathbb F_5^5$.
Two finite-certificate implementations verify coverage of all 1,024 controller
pairs and the diameter-5 bound.
[Construction, proof, and certificates](results/degree15-diameter5/).

### (16,3): 1,920 vertices

A 16-regular lift of a 30-state controller over $\mathbb F_4^3$, using
edge-dependent linear maps and local subspace covers. All-source verification
confirms diameter 3. [Construction, proof, and certificates](results/degree16-diameter3/).

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
