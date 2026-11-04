# Independent verification of the November additions

The [Python verifier](../verify_small_graphs.py) reads only the two published
edge lists and checks every source with ordinary queue-based BFS. It uses no
depth limit, symmetry reduction, construction data, or prior distance report.

| Graph | Vertices | Edges | Degrees | Exact diameter | Ordered pairs checked |
|---|---:|---:|---|---:|---:|
| [Degree 3, diameter 7](degree3-diameter7.json) | 208 | 312 | 3-regular | 7 | 43,264 |
| [Degree 5, diameter 5](degree5-diameter5.json) | 660 | 1,635 | 30 of degree 4; 630 of degree 5 | 5 | 435,600 |

Both graphs are simple and connected. The complete distance histograms
agree with the repository's separate C++ bit-parallel verifier.
The JSON reports record input hashes, the verifier's hash, and witnesses
for the exact diameters.

To reproduce from the repository root:

    python3 verification/verify_small_graphs.py --output /tmp/ddp-small-checks

The 660-vertex input is the loopless folded Cayley graph, with no additional
matching. Its report was regenerated after removing the 15 regularizing
edges from the main graph. The September regular graph in the source archive
is a historical variant with the same maximum degree, diameter, and order.
