# Repository verification — 2026-09-25

The checks below were rerun while organizing the repository. The five imported
certificate packages retain their original bytes. Scripts that write reports
were executed on temporary copies, preserving the original manifests and logs.

## Final direct verification of all seven graphs

All seven indexed graphs passed a final check directly from their edge lists,
including the two graphs in arXiv:2606.15860. The verifier checked every vertex
and every ordered pair, using exact bit-parallel BFS in batches. It used no
construction certificate, symmetry reduction, or sampling.

| Result | Vertices | Edges | Measured degrees | Measured diameter | Report |
|---|---:|---:|---|---:|---|
| (12,4) | 5,832 | 34,992 | 12-regular | 4 | [PASS](verification/final/degree12-diameter4.json) |
| (14,5) | 88,452 | 618,786 | 756 vertices of degree 13; 87,696 of degree 14 | 5 | [PASS](verification/final/degree14-diameter5.json) |
| (15,3) | 1,458 | 10,935 | 15-regular | 3 | [PASS](verification/final/degree15-diameter3.json) |
| (15,5) | 100,000 | 750,000 | 15-regular | 5 | [PASS](verification/final/degree15-diameter5.json) |
| (16,3) | 1,920 | 15,360 | 16-regular | 3 | [PASS](verification/final/degree16-diameter3.json) |
| (12,5), arXiv:2606.15860 | 34,992 | 209,952 | 12-regular | 5 | [PASS](verification/final/paper-degree12-diameter5.json) |
| (16,5), arXiv:2606.15860 | 147,456 | 1,179,648 | 16-regular | 5 | [PASS](verification/final/paper-degree16-diameter5.json) |

All graphs are simple, undirected, and connected. Reports record the input
SHA-256, degree distribution, exact distance histogram, and a vertex pair at
the claimed diameter. Ordinary Python BFS additionally checked all seven
diameter witnesses. The five new distance distributions agree with the supplied
BFS reports; the clean/provenance copies of the arXiv graphs are equivalent.
See the [method and reproduction commands](verification/README.md) and
[machine-readable summary](verification/final/summary.json).

## New results

All five edge lists passed direct checks for vertex numbering, absence of
self-loops and duplicate undirected edges, edge count, and degree distribution.
Their SHA-256 hashes are recorded in [results.json](results.json). All **156**
manifest entries across the five imported certificate packages matched.

| Result | Checks rerun in this update | Outcome |
|---|---|---|
| [(12,4), 5,832](results/degree12-diameter4/) | `verify_certificate.py --write-edges`; byte comparison; supplied C++17 BFS and the repository's direct verifier | Finite certificate passed; regenerated graph identical; both BFS implementations agree on the distance distribution over 34,012,224 ordered pairs; diameter exactly 4 |
| [(14,5), 88,452](results/degree14-diameter5/) | `verify_small.py`; `build_graph.py`; byte comparison with supplied edge list | Finite diameter certificate passed; regenerated graph identical |
| [(15,3), 1,458](results/degree15-diameter3/) | `verify.py`; `verify_uniform.py`; byte comparison with supplied edge list | Finite certificates and all-source distances passed; regenerated graph identical |
| [(15,5), 100,000](results/degree15-diameter5/) | `verify_small.py`; `verify_independent.py`; `regenerate.py`; byte comparison with supplied edge list | Both finite-certificate implementations passed; regenerated graph identical |
| [(16,3), 1,920](results/degree16-diameter3/) | `verify.py`; byte comparison with supplied edge list | Finite certificates and all-source distances passed; regenerated graph identical |

For (12,4), the subsequently supplied package verifies inverse consistency,
nonsingularity of the controllability matrices for 100 reduced words of length 4,
all 12 pencils of hyperplanes, the union of 18 two-dimensional subspaces used
for equal controller endpoints, and all 5,184 ordered pairs of controller
vertices. Regeneration reproduced the
existing edge list byte for byte. The supplied C++ BFS was rerun and agreed
with both the original package report and the repository's earlier BFS report.
The saved Python/Numba BFS report was preserved but that implementation was
not rerun. The canonical edge file now lives in
`results/degree12-diameter4/certificate/`; the repository's original verifier
and report remain one directory above it.

For (14,5), the finite checker verifies the rank-5 controllability matrices
for all 324 reduced words of length 5, and reachability using inserted
translations for all 13,104 state/length-3-word pairs and 1,456
state/length-1-word pairs. For (15,5), both finite checkers verify the diameter
upper bound for all 1,024 ordered pairs of controller vertices.
These checks prove the diameter upper bounds without traversing every pair of
vertices in the large graphs. Their orders exceed the degree-specific Moore
bounds for diameter 4, so both diameters are exactly 5.

The imported full-graph BFS and bitset reports are preserved unchanged. The
final direct verification above independently recomputed all-pairs distances
for both large diameter-5 graphs and reproduced their saved distributions.
Checks using a different implementation are not claims of independent peer review.

Each linked result summary provides the exact reproduction commands. The new
(12,4) verifier requires a C++17 compiler and the standard library. The imported
minimal certificate checks use Python 3.10 or later and its standard library;
optional search and full-graph checks have the dependencies listed in their
original package guides.

## arXiv:2606.15860 after relocation

Run from the repository root:

```bash
python3 results/diameter5-paper/anc/verify_provenance_equivalence.py
python3 results/diameter5-paper/anc/route_chart_clean_package/scripts/12_5_34992/verify_candidate.py
python3 results/diameter5-paper/anc/route_chart_clean_package/scripts/16_5_147456/verify_candidate.py
```

All three commands passed. The clean and provenance packages still contain
equivalent certificates and identical uncompressed graph data. Both
construction certificates verify their controller coverage and full-rank
length-5 fiber routes. Existing paper sources, bibliography, transcript,
supplementary data, and scripts were moved together without changing their
bytes; only the package README was updated. The paper was not recompiled.
Both edge lists also passed the final all-pairs distance verification above.

## Layout and publication checks

Local documentation links and machine-readable result paths were checked after
the move. `legacy/`, the local paper PDF, and the arXiv ZIP are excluded by
`.gitignore`. Imported certificate logs are explicitly retained despite the
general LaTeX `*.log` ignore rule. Final verification reports and their
reproduction code are included in the repository.
