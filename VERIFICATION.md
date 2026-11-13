# Repository verification — 2026-11-10

The 2026-11-10 update adds **degree 6, diameter 3, order 126** and
**degree 7, diameter 3, order 171**. All twelve indexed graphs passed the common
verifier directly from their edge lists, rerun on 2026-11-10. This check assumes no
construction certificate or graph symmetry. Previously published graph paths are preserved.

## Final direct verification of all twelve graphs

| Result | Vertices | Edges | Measured degrees | Measured diameter | Report |
|---|---:|---:|---|---:|---|
| **(6,3), added 2026-11-10** | **126** | **378** | **6-regular** | **3** | [PASS](verification/final/degree6-diameter3.json) |
| **(7,3), added 2026-11-10** | **171** | **594** | **9 vertices of degree 6; 162 of degree 7** | **3** | [PASS](verification/final/degree7-diameter3.json) |
| (3,7), added 2026-11-04 | 208 | 312 | 3-regular | 7 | [PASS](verification/final/degree3-diameter7.json) |
| (5,5), added 2026-11-04 | 660 | 1,635 | 30 vertices of degree 4; 630 of degree 5 | 5 | [PASS](verification/final/degree5-diameter5.json) |
| (12,4) | 5,832 | 34,992 | 12-regular | 4 | [PASS](verification/final/degree12-diameter4.json) |
| (12,5), arXiv:2606.15860 | 34,992 | 209,952 | 12-regular | 5 | [PASS](verification/final/paper-degree12-diameter5.json) |
| (13,5), added 2026-10-13 | 88,452 | 574,938 | 13-regular | 5 | [PASS](verification/final/degree13-diameter5.json) |
| (14,5) | 88,452 | 618,786 | 756 vertices of degree 13; 87,696 of degree 14 | 5 | [PASS](verification/final/degree14-diameter5.json) |
| (15,3) | 1,458 | 10,935 | 15-regular | 3 | [PASS](verification/final/degree15-diameter3.json) |
| (15,5) | 100,000 | 750,000 | 15-regular | 5 | [PASS](verification/final/degree15-diameter5.json) |
| (16,3) | 1,920 | 15,360 | 16-regular | 3 | [PASS](verification/final/degree16-diameter3.json) |
| (16,5), arXiv:2606.15860 | 147,456 | 1,179,648 | 16-regular | 5 | [PASS](verification/final/paper-degree16-diameter5.json) |

The checks cover every vertex and every ordered pair. The [machine-readable summary](verification/final/summary.json)
records the index and verifier hashes. For the ten earlier graphs only run times and timestamps changed
relative to the 2026-11-04 reports.

## November 10 additions: (6,3), 126 vertices, and (7,3), 171 vertices

Both graphs were found on 2026-11-10 by the [orbit-graph search](search/orbit-graphs/) as unions of
orbitals of SmallGroup(108,33) and SmallGroup(108,19). They are published in voltage-graph labellings:
a regular $\mathbb Z_3^2$-cover of a 14-vertex base graph and a regular $\mathbb Z_9$-cover of a
19-vertex base graph. The [import record](verification/import-2026-11-10/import.json) gives the hashes of
the discovered edge lists. For each graph, `certificate/verify.py`
([126](results/degree6-diameter3/certificate/verify.py), [171](results/degree7-diameter3/certificate/verify.py))
checks:

- the construction formula reproduces the published edge and adjacency lists byte for byte, and the graph is simple;
- spanning trees of depth at most 3 from one vertex per fibre, with translation invariance (diameter at most 3);
- modular reachability of every ordered pair of base vertices within 3 steps (an independent second certificate);
- the Moore bound for diameter 2 (37 and 50) is below the order, so the diameter is exactly 3;
- an explicit isomorphism from the discovered orbit graph, rebuilt from group generators and edge-orbit representatives;
- every listed automorphism generator preserves the edge set (group orders 162 and 216 were computed with nauty and GAP).

Records: [126](verification/import-2026-11-10/degree6-diameter3-construction.json),
[171](verification/import-2026-11-10/degree7-diameter3-construction.json).
The [ordinary-BFS verifier](verification/independent-2026-11-10/) measured all four November additions from
their edge lists alone; its distance histograms agree with the C++ reports.

Comparison: [Comellas's table](https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html),
accessed 2026-11-10 (page last changed 2026-11-04), lists 120 for (6,3) and 170 for (7,3)
([snapshot](verification/table-snapshot-2026-11-10.json)).

## Update of 2026-11-04 (historical)

The 2026-11-04 update added **degree 3, diameter 7, order 208** and
**degree 5, diameter 5, order 660**. All ten indexed graphs passed the common
verifier directly from their edge lists. This check assumes no construction
certificate or graph symmetry. Previously published graph paths are preserved.

## Final direct verification of all ten graphs — 2026-11-04 (historical)

| Result | Vertices | Edges | Measured degrees | Measured diameter | Report |
|---|---:|---:|---|---:|---|
| **(3,7), added 2026-11-04** | **208** | **312** | **3-regular** | **7** | [PASS](verification/final/degree3-diameter7.json) |
| **(5,5), added 2026-11-04** | **660** | **1,635** | **30 vertices of degree 4; 630 of degree 5** | **5** | [PASS](verification/final/degree5-diameter5.json) |
| (12,4) | 5,832 | 34,992 | 12-regular | 4 | [PASS](verification/final/degree12-diameter4.json) |
| (12,5), arXiv:2606.15860 | 34,992 | 209,952 | 12-regular | 5 | [PASS](verification/final/paper-degree12-diameter5.json) |
| **(13,5), added 2026-10-13** | **88,452** | **574,938** | **13-regular** | **5** | [PASS](verification/final/degree13-diameter5.json) |
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
After the initial ten-graph run, the 660-vertex input was changed to the
loopless graph without the 15 regularizing edges and checked again. The other
nine graph reports were retained after confirming their input hashes and
parameters against the current index. The summary distinguishes this update
from the initial full run.

## November import: (3,7), 208 vertices, and (5,5), 660 vertices

The [import record](verification/import-2026-11-04/import.json) identifies
both September source archives by SHA-256. Their published copies retain
exactly the original bytes. All source-package checks passed on extracted
temporary copies, including the archived 660-vertex permutation certificate.

The maintained packages reproduce their public edge lists directly from the
construction formulas. The 208-vertex edge set and labels agree with the
September source. The 660-vertex main graph agrees with the loopless algebraic
graph in the September source archive. For both, the edge-list header was changed
from the vertex count alone to the vertex and edge counts; edge rows did not change.
The initial import used a 15-edge regular completion; those additional edges
have been removed from the maintained graph and its constructor.

The [independent Python verifier](verification/verify_small_graphs.py) reads
only these edge lists and performs unrestricted ordinary BFS from every
vertex. It checked all **43,264** ordered pairs for the 208-vertex graph and
all **435,600** for the 660-vertex graph. The
[saved reports](verification/independent-2026-11-04/) agree with the common
C++ verifier on every distance count, as well as on order, size, degrees,
connectivity, and exact diameter.

The 208-vertex package additionally checks 13 spanning trees, all 169 modular
reachability sets, girth 9, and a proof that its full automorphism group is
$C_{16}$. The 660-vertex package checks the projective-matrix identity, the
degree distribution, all 60 explicit automorphisms, and agreement with nauty's
generators. The [full-group reports](results/degree5-diameter5/certificate/symmetry/)
give order 60 for the loopless main graph and order 12 for the historical
September regular variant. The algebraic edge-list URL remains an identical
copy of the main edge list.

## October import: (13,5), 88,452 vertices (historical)

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

## October independent verification of the (13,5) graph (historical)

A [separately written ordinary BFS implementation](verification/independent-2026-10-13/)
reads only the edge list and measures distances without a depth limit. It
confirmed order 88,452, degree 13 at all vertices, and diameter exactly 5,
checking all 7,823,756,304 ordered pairs. Every vertex has eccentricity 5.
The measured distance histogram also agrees with the earlier bit-parallel run.

The implementation passed 16 comparisons with a separate Floyd–Warshall
reference, including a graph of diameter 8 and a disconnected graph, and
rejected eight malformed inputs. A separate Python BFS verified that vertices
0 and 40,562 have distance exactly 5. The [saved report](verification/independent-2026-10-13/result.json)
records all measurements and hashes of the input and verification programs.

## Public-table status and link preservation

The [current snapshot](verification/table-snapshot-2026-11-13.json) records
the main-table values read on 2026-11-13, the page's stated last-change date
2026-11-12, six source-page hashes, the cell colours that credit entries, and
eight incoming GitHub links: seven package directories and the repository root.
All linked directories and their graph files retain their existing public paths.
The README identifies (6,3), (3,7), (5,5), (13,5), and (16,3) as listed in the
main table, and (7,3) as below the table's new entry of 176. It uses the main
table when a detail page still describes an earlier record. Earlier dated
snapshots remain available.

Only the 208- and 660-vertex source archives are included in the November
import. The other root archives and local exploration files are not published.

## September 2026 verification (historical)

The checks in this historical section were performed on 2026-09-25.
The direct edge-list report files were refreshed for the ten-graph run above.
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
