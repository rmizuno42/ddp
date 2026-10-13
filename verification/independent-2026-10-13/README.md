# Independent verification of the (13,5) graph — 2026-10-13

**PASS: order 88,452; degree 13 at every vertex; diameter exactly 5.**
The graph has 574,938 edges and is simple, undirected, and connected.

This check uses a separately written implementation of ordinary queue-based
breadth-first search. Its only graph input is the published
[edge list](../../results/degree13-diameter5/certificate/graph.edges.gz).
It does not load the graph generator, affine data, matchings, symmetry data,
source-package verifiers, or earlier verification reports.

## Measurements

| Property | Measured value |
|---|---:|
| Declared vertex set, checked against the endpoints | 0 through 88,451 |
| Distinct vertex labels occurring in the edges | 88,452 |
| Undirected edges | 574,938 |
| Minimum degree | 13 |
| Maximum degree | 13 |
| Diameter | 5 |
| Sources checked | 88,452 |
| Ordered vertex pairs checked, including the diagonal | 7,823,756,304 |
| Unreachable ordered pairs | 0 |

Every vertex has eccentricity 5. The exact ordered-pair distance distribution is:

| Distance | Ordered pairs |
|---|---:|
| 0 | 88,452 |
| 1 | 1,149,876 |
| 2 | 12,381,390 |
| 3 | 123,020,534 |
| 4 | 1,157,788,198 |
| 5 | 6,529,327,854 |

Vertices **0 and 40,562** have distance exactly 5. A separate Python BFS
confirmed this distance and returned the shortest path
`0 → 27702 → 3 → 40402 → 163 → 40562`.

## Independence and implementation checks

The C++ program accepts no claimed degree or diameter. It parses the literal
edge list, rejects loops and repeated undirected edges, computes the degree of
every vertex, and runs BFS from every source. There is **no depth limit** and
no sampling or symmetry reduction. An individual search ends when all vertices
have been discovered, or its reachable component has been exhausted.
The resulting distance distribution measures the diameter directly.

Before the graph run, the implementation was checked against a Python
Floyd–Warshall reference on eight small graphs, with one and three threads
(16 comparisons). These include a path of diameter 8, a disconnected graph,
an isolated vertex, and reproducible random graphs. Eight malformed inputs
were rejected. The graph's reported parameters are compared with the measured
values only after the all-source computation finishes.

## Reproduce

Python 3.10 or later and a C++17 compiler, standard libraries only.
From the repository root:

```bash
python3 verification/independent-2026-10-13/run.py
```

The script compiles in a temporary directory, performs the implementation
checks, decompresses the edge file, computes all-source distances, checks a
diameter witness in Python, and writes [result.json](result.json). Use
`--output /tmp/ddp-independent-result.json` to preserve the saved report.

- [Ordinary BFS implementation](verify_bfs.cpp).
- [Runner, reference checks, and witness verification](run.py).
- [Measured result and input/source hashes](result.json).

The uncompressed edge-list SHA-256 is
`b95760a4cf5c009694d099f62613ea932a6d64b539b7c9c6cc9812ca19835c2b`.

[Repository verification record](../../VERIFICATION.md)
