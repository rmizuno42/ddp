# Degree 13, diameter 5: 88,452 vertices

**$N(13,5)\ge 88{,}452$.** Simple undirected connected 13-regular graph;
574,938 edges, diameter exactly 5. **Added to this repository on 2026-10-13.**

The [Comellas table entry](https://web.mat.upc.edu/francesc.comellas/delta-d/desc_g/desc_g5.html#135)
is **51,417** as accessed on **2026-10-13**: this construction has **37,035
more vertices (+72.03%)**. Its order is not yet reflected in that table.
The dated comparison is recorded in the [repository snapshot](../../verification/table-snapshot-2026-10-13.json).

## Construction and relation to arXiv:2606.15860

The vertex set is $C\times\mathbb F_3^5$, where $C$ has 364 states and four
ports at each state. The controller transitions agree with those in the
[degree-14, diameter-5 package](../degree14-diameter5/). Some ports return to
the same state. Both the affine data and the additional edges differ from
those in the degree-14 construction, giving a new graph on the same vertex
set.

For the record $(v_{u,p},A_{u,p},b_{u,p})$ at state $u$ and port $p$, the
ordinary affine edges are

$$
(u,x)\sim(v_{u,p},A_{u,p}x+\lambda b_{u,p}),\qquad \lambda\in\mathbb F_3.
$$

After loops and repeated edges are removed, the ordinary graph $B$ has
87,696 vertices of degree 12 and 756 of degree 11. A perfect matching $M$
adds one new neighbor at every vertex. A further matching $P$ has 378 edges
and pairs all 756 vertices that still have degree 12. Thus

$$
G=B\cup M\cup P
$$

is 13-regular. The main matching pairs distinct fibers by bijections of their
243 vectors. Some of these bijections are not affine in the given fiber
coordinates.

This construction retains the controller-and-fiber organization of
[arXiv:2606.15860](../diameter5-paper/), while changing both the controller
and the fiber connections. The $q=3$ construction in that paper uses a
144-vertex simple 4-regular controller and a universal route chart on
$\mathbb F_3^5$. Here the controller has 364 states and permits transitions
from a state to itself; the affine maps depend on the state and port, and
the added matchings include non-affine maps. The resulting graph is not
asserted to be a route-chart lift graph as defined in §A.4, and the diameter
certificate below does not apply the paper's route-chart lift principle.

The degree-14 construction uses translations within each fiber. The present
construction uses different affine data and the matchings $M$ and $P$ to
obtain the same order and diameter with maximum degree 13.

## Diameter certificate

The ordinary affine graph $B$ alone does not meet the diameter bound. Using
the supplied integer vertex labels, BFS in $B$ gives distance 6 between
vertices 0 and 1,953. Thus the added matching edges provide paths needed for
diameter at most 5, as well as completing the degrees to 13.

An exact breadth-first search from every vertex verifies diameter at most 5.
The supplied package also contains a separate construction-and-verification
implementation using a verified free automorphism of order seven.
The Moore bound for maximum degree 13 and diameter at most 4 is

$$
1+13(1+12+12^2+12^3)=24{,}506<88{,}452,
$$

so the diameter is exactly 5.

The proof notes describe the matching-completion method: with all other edges
fixed, a shortest path of length at most 5 uses at most three edges of a
matching. This gives exact conditions on the matching assignments. The finite
data specify the completed graph; regeneration does not require rerunning the
search. No infinite parameter family or optimality claim is made.

## Materials

- [Compressed edge list](certificate/graph.edges.gz) — after decompression,
  the first line is `88452 574938`, followed by one undirected edge `u v`
  per line, with zero-based vertex numbers and `u < v`.
- [Construction and proof (English)](certificate/CONSTRUCTION.md).
- [Source package guide (Japanese)](certificate/README_ja.md).
- [Construction data](certificate/data/) — controller, affine maps, two
  matchings, and the order-seven permutation.
- [Generator](certificate/generate_graph.py) and
  [edge-list verifier](certificate/verify_graph.cpp).
- [Separate construction/verifier implementation](certificate/independent/construct_verify.cpp).
- [Source certificate](certificate/certificate.json) and
  [source-file checksums](certificate/SHA256SUMS.json).
- [Repository import checks](../../verification/import-2026-10-13.json) and
  [final edge-list report](../../verification/final/degree13-diameter5.json).
- [Additional independent verification](../../verification/independent-2026-10-13/)
  — ordinary BFS from every source, without a depth limit.

## Reproduce the verification

Python 3 and a C++17 compiler, standard libraries only. From the repository
root, run on a temporary copy to preserve the supplied files:

```bash
verify_dir=$(mktemp -d)
cp -R results/degree13-diameter5/certificate/. "$verify_dir/"
cd "$verify_dir"
python3 verify_checksums.py
python3 generate_graph.py
python3 verify_checksums.py --graph graph.edges
c++ -O3 -std=c++17 -pthread verify_graph.cpp -o verify_graph
./verify_graph graph.edges 8
```

All commands passed during the **2026-10-13 repository update**. The generated
edge list matched the decompressed supplied file byte for byte. The repository's
[common verifier](../../verification/README.md) also checked all 88,452 sources
and all 7,823,756,304 ordered pairs, reproducing the supplied exact distance
histogram. See the [verification record](../../VERIFICATION.md).

A subsequent [independent ordinary-BFS check](../../verification/independent-2026-10-13/)
also measured order 88,452, degree 13 at every vertex, and diameter exactly 5.
It used only the edge list and confirmed that every vertex has eccentricity 5.

Uncompressed edge-file SHA-256:

```text
b95760a4cf5c009694d099f62613ea932a6d64b539b7c9c6cc9812ca19835c2b
```

The 20 files in `certificate/` preserve the supplied package bytes. Its source
notes compare against the table accessed on 2026-10-09; the maintained summary
above uses 2026-10-13. This package has no separate paper.

[All results](../../README.md)
