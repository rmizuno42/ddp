# Degree 12, diameter 4: 5,832 vertices

**$N(12,4)\ge 5,832$.** Simple undirected connected 12-regular graph,
34,992 edges, diameter exactly 4.

Compared with the [Comellas table](https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html) accessed on **2026-09-25** (page last changed 2026-09-24): **5,184 → 5,832**, an increase of **648 vertices (12.50%)**.

A 72-state 4-regular controller is lifted over $\mathbb F_3^4$, giving
$72\cdot3^4=5,832$ vertices. The controller is a cyclic lift of an eight-state
base, with voltages modulo 9.

This extends the affine route-chart method in [arXiv:2606.15860](../diameter5-paper/)
by combining full-rank routes with subspace covers: four-hyperplane covers handle
short routes, and 18 planes cover pairs within the same fiber.

## Materials

- [Construction and proof (Japanese)](certificate/proof_ja.md).
- [Original package guide (Japanese)](certificate/README.md).
- [construction.json](certificate/construction.json) — matrices, control vectors, and base-edge voltages.
- [Edge list](certificate/graph_12_4_5832.edges) — **no header**; one undirected edge `u v` per line, listed once, with vertices numbered 0 through 5,831.
- [verify_certificate.py](certificate/verify_certificate.py) — finite-certificate verifier and edge generator.
- [Controller routes](certificate/controller_routes.json), [pencil routes](certificate/pencil_routes.json), and [search provenance](certificate/search_provenance.json).
- [verify_bfs.cpp](certificate/verify_bfs.cpp) — the supplied C++17 all-source BFS verifier.
- [verify.cpp](verify.cpp) and [verification.json](verification.json) — the repository's earlier direct verifier and its all-source BFS report.
- [SHA256SUMS](SHA256SUMS) — integrity of the repository wrapper files and the [original package manifest](certificate/SHA256SUMS).

The imported package, created on 2026-09-24 and added here on 2026-09-25,
is preserved without edits. Its edge list is byte-for-byte identical to the
one already held in this repository; the single copy now lives in `certificate/`.

## Reproduce the construction and verification

Python 3.10 or later and a C++17 compiler, standard libraries only. From the
repository root, copy the package to a temporary directory because its scripts
write regenerated files and reports:

```bash
verify_dir=$(mktemp -d)
cp -R results/degree12-diameter4/certificate/. "$verify_dir/"
cd "$verify_dir"
python3 verify_certificate.py --write-edges
c++ -O3 -std=c++17 verify_bfs.cpp -o verify_bfs
./verify_bfs graph_12_4_5832.edges > bfs-rerun.json
```

The Python verifier checks inverse consistency, 100 full-rank length-4 words,
all 12 pencils, the 18-plane same-fiber cover, and all 5,184 ordered controller
pairs. It also regenerates the edge list and checks its expected SHA-256.
Both commands passed on 2026-09-25: the regenerated edges matched the supplied
file, and C++ BFS reproduced the repository's existing all-pairs distance
distribution. The package also includes a saved Python/Numba BFS report;
that implementation was not rerun during this update.

The [final edge-list report](../../verification/final/degree12-diameter4.json)
also confirms all vertex degrees and all-pairs distances using the repository's
[common verifier](../../verification/README.md).

## Additional direct check

From this directory:

```bash
c++ -O3 -std=c++17 verify.cpp -o /tmp/ddp-verify-12-4
/tmp/ddp-verify-12-4 certificate/graph_12_4_5832.edges
```

The verifier rejects loops, duplicate edges, invalid vertex numbers, and
incorrect degrees. Ordinary BFS from all 5,832 vertices then verifies
connectivity and diameter exactly 4. The ordered-pair distance counts are:

| Distance | Ordered pairs |
|---:|---:|
| 0 | 5,832 |
| 1 | 69,984 |
| 2 | 676,512 |
| 3 | 6,342,300 |
| 4 | 26,917,596 |
| Total | 34,012,224 |

Edge-file SHA-256:

```text
ea0846865021f05f38825ac03ca96a387815b50634a9117f9f42533080dbd05b
```

See [the repository verification record](../../VERIFICATION.md). This package
has no separate paper and does not assert acceptance into the public table or
optimality.

[All results](../../README.md)
