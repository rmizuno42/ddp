# Repository verification — 2026-10-13

This update imports only **degree 13, diameter 5, order 88,452**. The seven
previously indexed graphs retain their existing package and edge-file paths.
All eight indexed graphs passed the common verifier directly from their edge
lists. No construction certificate or graph symmetry is assumed by this check.

## Final direct verification of all eight graphs

| Result | Vertices | Edges | Measured degrees | Measured diameter | Report |
|---|---:|---:|---|---:|---|
| (12,4) | 5,832 | 34,992 | 12-regular | 4 | [PASS](verification/final/degree12-diameter4.json) |
| (12,5), arXiv:2606.15860 | 34,992 | 209,952 | 12-regular | 5 | [PASS](verification/final/paper-degree12-diameter5.json) |
| **(13,5), added in this update** | **88,452** | **574,938** | **13-regular** | **5** | [PASS](verification/final/degree13-diameter5.json) |
| (14,5) | 88,452 | 618,786 | 756 vertices of degree 13; 87,696 of degree 14 | 5 | [PASS](verification/final/degree14-diameter5.json) |
| (15,3) | 1,458 | 10,935 | 15-regular | 3 | [PASS](verification/final/degree15-diameter3.json) |
| (15,5) | 100,000 | 750,000 | 15-regular | 5 | [PASS](verification/final/degree15-diameter5.json) |
| (16,3) | 1,920 | 15,360 | 16-regular | 3 | [PASS](verification/final/degree16-diameter3.json) |
| (16,5), arXiv:2606.15860 | 147,456 | 1,179,648 | 16-regular | 5 | [PASS](verification/final/paper-degree16-diameter5.json) |

The checks cover every vertex and every ordered pair, verifying simplicity,
connectivity, degree distributions, and exact diameters. Input hashes, exact
ordered-pair distance histograms, and diameter witnesses are in the reports.
See the [method and reproduction commands](verification/README.md) and
[machine-readable run summary](verification/final/summary.json).

## October import: (13,5), 88,452 vertices

The [import record](verification/import-2026-10-13.json) identifies the source
archive by SHA-256 and records its 20 extracted files. All 19 entries in the
source checksum manifest passed; every extracted file is byte-identical to
its archive member. The supplied package was tested on a temporary copy:

- `verify_checksums.py` checked the source-file manifest.
- `generate_graph.py` regenerated the graph and checked the degree counts,
  main involution, spare matching, final degree, and symmetric adjacency.
- The output matched the decompressed supplied edge list byte for byte.
- `verify_checksums.py --graph graph.edges` checked the canonical edge hash.
- The supplied portable C++17 verifier checked all 88,452 sources, without
  symmetry reduction, and confirmed diameter exactly 5.
- The repository's separate common verifier also checked all 7,823,756,304
  ordered pairs and reproduced the distance histogram in `certificate.json`.

The [execution log](verification/import-2026-10-13/degree13-diameter5.txt)
records the completed commands. The additional source-package verification
logs are preserved; the order-seven orbit verifier and the 77-spare-edge
subgraph check were not rerun in this update.

## Public-table status and link preservation

The [table snapshot](verification/table-snapshot-2026-10-13.json) records the
orders and detail-page URLs read on 2026-10-13, the page's stated last-change
date (2026-10-11), source-page hashes, and five incoming GitHub links.
All five linked directories are preserved:

- `results/degree12-diameter4/`
- `results/degree14-diameter5/`
- `results/degree15-diameter3/`
- `results/degree15-diameter5/`
- `results/degree16-diameter3/`

All previously tracked files remain at their existing paths. The old
certificate files and paper sources retain their bytes. The root overview
lists the five constructions matching the current table orders. The added
(13,5) result exceeds its entry and is shown separately as not yet reflected
in the table. The (12,5) and (15,3) packages remain available at their published
locations although their orders are now below the table entries.

The index preserves the September comparison values as historical data.
Only the (13,5) source archive is imported in this update; other root ZIPs and
local exploration files are outside this import.

## September 2026 verification (historical)

The checks in this historical section were performed on 2026-09-25.
The direct edge-list report files were refreshed for the eight-graph run above.
The construction-certificate checks described below were not rerun in October.
The five September certificate packages retain their original bytes. Scripts that write reports
were executed on temporary copies, preserving the original manifests and logs.

### Final direct verification of all seven graphs

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

### New results

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

### arXiv:2606.15860 after relocation

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

### Layout and publication checks

Local documentation links and machine-readable result paths were checked after
the move. `legacy/`, the local paper PDF, and the arXiv ZIP are excluded by
`.gitignore`. Imported certificate logs are explicitly retained despite the
general LaTeX `*.log` ignore rule. Final verification reports and their
reproduction code are included in the repository.
