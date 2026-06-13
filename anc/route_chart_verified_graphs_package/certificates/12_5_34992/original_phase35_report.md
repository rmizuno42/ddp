# Phase 35: C4 x C6 controller combined with GF(3)^5 route chart

## Result

The 144-vertex controller from the verified `C4 x C6` construction can be combined not only with the existing `GF(4)^5` chart, but also with the existing `GF(3)^5` 4-symbol universal chart.

This gives a simple undirected graph with

- maximum degree: 12,
- diameter at most 5,
- number of vertices: `144 * 3^5 = 34,992`.

Within the working baseline used in this project, the previous `(12,5)` candidate was `32,076`; this improves it by `2,916` vertices.

## Controller

The controller is the same as in Phase 34:

- base: a 6-vertex loopless 4-regular multigraph,
- voltage group: `C4 x C6`,
- lift size: `6 * 24 = 144`,
- property: every ordered controller pair is joined by an exact nonbacktracking walk of length 5.

The base voltage data is in `controller_c4xc6_multibase.txt`.

## Fiber chart

The fiber is `GF(3)^5`.  The directed symbols are

`a, a^-1, b, b^-1`.

For each reduced word of length 5, the corresponding controllability matrix has full rank 5 over `GF(3)`.  Hence one controller route of length 5 routes bijectively onto all `3^5 = 243` fiber targets.

The chart data is in `gf3_s5_universal.txt`.

## Verification

Run:

```bash
python verify_candidate.py
python generate_final_graph.py
```

Expected verification output:

```text
Base voltage coverage over C4 x C6: OK
Controller: OK; 144 vertices, simple 4-regular, exact labeled NB length-5 coverage
GF(3)^5 universal chart: OK; 324 reduced words checked, min rank 5; inverse-symbol data verified
Certificate complete: degree 12, diameter <=5, vertices = 144*3^5 = 34992
```

The generated edge list has:

```text
34,992 vertices
209,952 edges
all degrees 12
```

Since `34992 * 12 / 2 = 209952`, the edge count agrees with 12-regularity.

## Interpretation

This is an immediate and safe generalization of the Phase 34 controller.  The route-chart principle is modular: once a controller has exact nonbacktracking length-5 coverage, any compatible universal chart over `GF(q)^5` yields a degree `4q` graph of diameter at most 5.

Thus the same controller yields:

- `q=4`: degree 16, `144 * 4^5 = 147,456` vertices;
- `q=3`: degree 12, `144 * 3^5 = 34,992` vertices.

The second item is the new Phase 35 result.
