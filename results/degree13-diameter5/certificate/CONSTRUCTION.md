# A 13-regular graph of diameter 5 on 88,452 vertices

## Result

The supplied finite data define a simple undirected graph with

- 88,452 vertices;
- degree 13 at every vertex;
- 574,938 edges;
- diameter exactly 5.

The [UPC degree–diameter table](https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html), checked on 9 October 2026, lists 51,417 for degree 13 and diameter 5. The order of this graph is larger by 37,035 vertices, or

\[
100\left(\frac{88452}{51417}-1\right)=72.0287064589\ldots\%.
\]

This is a comparison with that table entry. The finite graph and its degree and diameter certificates are the mathematical result; acceptance into an external table is a separate matter.

## Explicit construction

All arithmetic in the affine maps below is over the field \(\mathbf F_3\).

### Vertices and labels

The vertex set is

\[
V=\{0,\ldots,363\}\times\mathbf F_3^5.
\]

Write a fibre vector as \(x=(x_0,y_0,x_1,y_1,z)\), and define

\[
\operatorname{enc}(x)=x_0+3y_0+9x_1+27y_1+81z.
\]

The integer label of \((u,x)\) is \(243u+\operatorname{enc}(x)\). Thus every label from 0 to 88,451 is used exactly once.

### Ordinary affine edges

The file `data/controller_affine_chart.txt` is the complete controller and affine-map specification. Its first integer is 364. It is followed, in order of controller \(u=0,\ldots,363\) and port \(p=0,1,2,3\), by a record

\[
(v_{u,p},A_{u,p},b_{u,p}),
\]

where \(v_{u,p}\) is one controller label, \(A_{u,p}\) is a \(5\times5\) matrix in row-major order, and \(b_{u,p}\) is a five-entry column vector. Each record contains 31 integers.

For every \(x\in\mathbf F_3^5\) and \(\ell\in\mathbf F_3\), include the unordered edge

\[
\big\{(u,x),\ (v_{u,p},A_{u,p}x+\ell b_{u,p})\big\}.
\]

Discard self-loops and merge repeated edges. Call the resulting simple graph \(B\). The supplied data make the adjacency relation symmetric. Exactly 756 vertices have degree 11 in \(B\); the other 87,696 vertices have degree 12.

### Main involution

The file `data/main_matching.txt` contains 88,452 integers. Its entry in position \(v\), with positions counted from zero, is \(m(v)\). Include

\[
\{v,m(v)\}\qquad(v<m(v)).
\]

The data satisfy \(m(m(v))=v\) and \(m(v)\ne v\) for every vertex. None of these 44,226 edges is an ordinary edge. Consequently \(B\cup M\) has degree 12 on precisely 756 vertices and degree 13 elsewhere.

### Spare-slot matching

The file `data/spare_matching.txt` contains 378 unordered pairs of integer vertex labels. These pairs form a matching on all 756 degree-12 vertices of \(B\cup M\). Every listed edge is absent from \(B\cup M\).

The final graph is

\[
G=B\cup M\cup P,
\]

where \(P\) is this spare-slot matching. The four data files, together with the formulas above, specify \(G\) completely. No optimization, random seed, solver, or unavailable intermediate construction is needed to regenerate it.

## Proof of the parameters

### Order, simplicity, and degree

The vertex description gives \(|V|=364\cdot3^5=88,452\). The ordinary graph is made simple by the explicit loop and duplicate removal. The main involution is fixed-point-free and contributes exactly one new neighbour at every vertex. The spare matching contributes one new neighbour at each remaining degree-12 vertex and uses no other vertex. Thus every vertex of \(G\) has exactly 13 distinct neighbours. The graph has \(88452\cdot13/2=574,938\) edges.

All assertions about the finite input data in this argument are checked directly by the supplied generator/verifier: matrix dimensions and field entries, ordinary symmetry and degree counts, all main involution identities, absence of duplicate matching edges, the spare endpoint partition, and final symmetry and degree.

### Diameter at most five

Exhaustive breadth-first search to depth five verifies that every vertex is reached from every source. This is an exact finite calculation using literal adjacency; it does not infer global coverage from random samples or from a search objective.

There is also an independently checked reduction by a free automorphism of order seven. The file `data/controller_order7_permutation.txt` specifies a permutation \(g\) of the 364 controller labels. All its cycles have length seven, and

\[
(u,x)\longmapsto(g(u),x)
\]

preserves the final adjacency relation. Therefore it is sufficient to run breadth-first search from all 243 fibre states over one representative of each of the 52 controller cycles: 12,636 sources. The verifier checks the permutation and every adjacency image before using this reduction.

Both this orbit-reduced verification and an independent verification from all 88,452 sources returned zero ordered pairs at distance greater than five. An independently verified spanning subgraph using only 77 of the 378 spare edges already has this property, so completing the spare matching cannot invalidate the diameter bound.

### Diameter is not smaller than five

The degree-13 Moore bound for diameter four is

\[
1+13+13\cdot12+13\cdot12^2+13\cdot12^3=24,506.
\]

Since \(88,452>24,506\), a graph of maximum degree 13 on this many vertices cannot have diameter at most four. Together with the exhaustive upper bound, this proves \(\operatorname{diam}(G)=5\).

## General completion method

The construction uses an exact matching-completion principle that applies more broadly than this one set of affine matrices.

Fix a backbone graph \(H\), and reserve one degree slot at every vertex of an even set \(S\). Let \(F\) be a variable matching on \(S\). A shortest path in \(H\cup F\) cannot contain consecutive \(F\)-edges, because traversing a matching twice immediately returns to the previous vertex. A path of length at most five therefore uses at most three matching edges. Its possibilities are exactly:

1. one matching edge with at most four backbone edges in its prefix and suffix;
2. two matching edges with at most three backbone edges in its prefix, middle and suffix;
3. three matching edges in the pattern \(FHFHF\).

Backbone distance tables turn each pair not already covered within five steps into an exact disjunction of matching-edge conditions. This includes preservation of pairs that were already covered by a previous matching, not only repair of its current defects.

For a compact nonlinear family, partition one side of a fixed matching into nine-point cells and permute the nine images independently within each cell. Row and column bijection constraints guarantee a matching. Every possible new matching edge is controlled by one assignment literal, so each radius-five condition is a disjunction of monomials of degree at most three.

The constraints can be solved by counterexample-guided refinement: solve a subset exactly, evaluate the proposed matching against every global pair constraint, and add newly failed conditions. The subset optimum is a rigorous lower bound; a matching attaining that bound on the complete pair set certifies the optimum of that particular family. A full score of zero certifies a completion.

A useful further step is to alternate the main matching with the matching on spare degree slots. Their optima are conditional on one another. In this construction, an equal-score main-matching change enabled a different spare matching to remove the last distance-five defect. The final main change was especially small: it exchanges fibre states 236 and 241 over controller 15 and repeats that exchange on its seven controller translates.

The general path-to-constraint reduction is proved above. The present data establish one explicit degree-13, diameter-5 graph. They do not by themselves establish an infinite parameter family, a closed formula for other degrees, or optimality of the order 88,452.

## Reproduction

The primary generation program uses Python 3 standard library only. The independent edge-list verifier uses portable C++17 and the standard thread library.

```sh
python3 verify_checksums.py
python3 generate_graph.py
c++ -O3 -std=c++17 -pthread verify_graph.cpp -o verify_graph
./verify_graph graph.edges 2
python3 verify_checksums.py --graph graph.edges
```

The last line of a successful distance verification is:

```text
PASS: simple undirected 13-regular graph; order 88452; diameter exactly 5.
```

The supplied `graph.edges.gz` contains the same canonical edge list: one header `88452 574938`, followed by the edges `u v` with `0 <= u < v < 88452`, in lexicographic order.

A second construction-and-verification implementation is in `independent/construct_verify.cpp`. It reads its data from the working directory. It can be run independently with:

```sh
c++ -O3 -std=c++17 independent/construct_verify.cpp -o construct_verify
(cd data && ../construct_verify --orbits)
# Or replace --orbits with --all to avoid symmetry reduction.
```

The SHA-256 manifest identifies all supplied files. The canonical uncompressed edge-list SHA-256 is recorded separately in `certificate.json`. Verification logs are in `verification/`.
