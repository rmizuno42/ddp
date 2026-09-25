# Final verification from edge lists

All seven graphs in [results.json](../results.json) passed a direct check of
their vertex count, edge count, maximum degree, degree distribution, simplicity,
connectivity, and exact diameter. The [summary](final/summary.json) lists the
seven reports. Each report includes the input file hash, verifier hash,
execution time, ordered-pair distance histogram, and a pair of vertices at the
claimed diameter.

## Reproduce

Python 3.10 or later and a C++17 compiler are sufficient. Run from the repository
root; a temporary directory holds the compiled program and decompressed inputs:

```bash
python3 verification/verify_all.py --output /tmp/ddp-final-verification
```

Without `--output`, reports are written to `verification/final/`. The runner
checks every entry of `results.json` and returns a failure if any claim or
input checksum fails. It writes an overall PASS summary only after every graph
passes. `--threads` (default up to 8) and `--batch-size` (default 16,384 sources)
control computation and memory use.

## Method

The verifier reads only the edge list and the claimed parameters. Vertex IDs
are the integers from 0 to the claimed order minus one, including any vertices
absent from the edges. A header, where present, must agree with the vertex and
edge counts. Loops, duplicate undirected edges, malformed rows, and vertex IDs
outside the stated range are rejected.

After computing the degree of every vertex, the verifier runs an exact
bit-parallel breadth-first search from **every source**. For a batch of sources,
each vertex stores a bit for every source that can reach it within the current
radius. A synchronous union with its neighbors' bitsets advances the radius
by one. Subtracting successive reachability counts gives the exact ordered-pair
distance histogram. The batches partition all vertices; no source is sampled
or omitted. The largest run uses about 576 MiB for its two reachability arrays.

All $n^2$ ordered pairs must be reached within the claimed diameter, and at
least one pair must first be reached at that diameter. Together these establish
connectivity and the exact diameter, without construction data or symmetry
assumptions. The maximum degree and full degree distribution must also match
the index; in particular, the (14,5) graph has degrees 13 and 14.

Before the final run, the verifier was compared with ordinary Python queue BFS
on 16 combinations of graphs, batch sizes, and thread counts, including partial
batches and 64-bit boundaries. Eight malformed-input or false-claim cases were
rejected. The final diameter witnesses were additionally checked by ordinary
Python BFS, and the five new graphs' complete distance distributions matched
their supplied BFS reports.

[Repository verification record](../VERIFICATION.md)
