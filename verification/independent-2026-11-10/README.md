# Independent verification of the November additions — 2026-11-10

The [Python verifier](../verify_small_graphs.py) reads only the published edge lists and checks
every source with ordinary queue-based BFS. It uses no depth limit, symmetry reduction,
construction data, or prior distance report. On 2026-11-10 it was extended from the two
2026-11-04 graphs to all four November additions.

| Graph | Vertices | Edges | Degrees | Exact diameter | Ordered pairs checked |
|---|---:|---:|---|---:|---:|
| [Degree 6, diameter 3](degree6-diameter3.json) | 126 | 378 | 6-regular | 3 | 15,876 |
| [Degree 7, diameter 3](degree7-diameter3.json) | 171 | 594 | 9 of degree 6; 162 of degree 7 | 3 | 29,241 |
| [Degree 3, diameter 7](degree3-diameter7.json) | 208 | 312 | 3-regular | 7 | 43,264 |
| [Degree 5, diameter 5](degree5-diameter5.json) | 660 | 1,635 | 30 of degree 4; 630 of degree 5 | 5 | 435,600 |

All four graphs are simple and connected. Their complete distance histograms agree with the
repository's separate C++ bit-parallel verifier ([final reports](../final/)):

| Graph | Ordered-pair distance histogram |
|---|---|
| (6,3), 126 | 126, 756, 3,672, 11,322 |
| (7,3), 171 | 171, 1,188, 6,426, 21,456 |

The JSON reports record input hashes, the verifier's hash, and witnesses for the exact diameters.
The reports for the (3,7) and (5,5) graphs repeat the 2026-11-04 measurements with the extended
verifier; the [2026-11-04 reports](../independent-2026-11-04/) are kept unchanged.

To reproduce from the repository root:

    python3 verification/verify_small_graphs.py --output /tmp/ddp-small-checks
