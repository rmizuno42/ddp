# Orbit-graph search

Search code that found the [(6,3), 126-vertex](../../results/degree6-diameter3/) and
[(7,3), 171-vertex](../../results/degree7-diameter3/) graphs on 2026-11-10.

## Method

Let a finite group $G$ act on $V=G/H_1\sqcup\cdots\sqcup G/H_b$. A simple graph on $V$ is
$G$-invariant exactly when its edge set is a union of *edge classes* $R\cup R^{*}$, where $R$ is
an orbital (a $G$-orbit on ordered pairs of distinct points) and $R^{*}$ its transpose. Each class
adds a constant number of neighbours to every vertex of the orbits it meets, so degrees are
constant on orbits; eccentricities are constant on orbits too, so the diameter is at most $D$
if and only if a BFS from one representative per orbit reaches all of $V$ within $D$ steps.

For a group $G$, `gsets.g` (GAP 4) exports the coset actions $G/H$ for representatives $H$ of
the conjugacy classes of subgroups of index at most a bound, on a common generating set.
`orbsearch2` reads these actions, forms the multisets of at most $b$ actions whose total size lies
in the requested windows, computes the edge classes, and searches for a selection of classes with
maximum degree at most $\Delta$ and diameter at most $D$:

- only *maximal* selections are considered (adding edges never increases distances);
- exact depth-first search with a sound prune — if the current classes together with all classes
  that still fit individually do not give diameter $\le D$, no completion does — decides the
  existence of such a graph when the number of classes is small;
- otherwise a staged simulated annealing over class selections is used (pre-screen, screen,
  middle stage, heavy stage), whose thresholds were calibrated on known record graphs.

Every reported graph is re-checked by an all-pairs BFS inside the program and should be checked
again independently, as done for the published packages.

## Reproducing the two graphs

    c++ -O3 -std=c++17 -o orbsearch2 orbsearch2.cpp
    ARGS="--maxclasses 60 --nodecap 20000 --prescreen 200 --prescreen-restarts 2 --prescreen-cut 0.22 \
          --screen 500 --screen-restarts 4 --esc2 500 --esc2-restarts 12 --esc2frac 0.15 \
          --esc 20000 --escfrac 0.04 --restarts 3"
    ./orbsearch2 examples/SG108_19.gs examples/cell_7_3_171.txt --combo 10,16,17 $ARGS --seed 1 --outdir /tmp
    ./orbsearch2 examples/SG108_33.gs examples/cell_6_3_126.txt --combo 22,40,40 $ARGS --seed 1 --outdir /tmp

`examples/SG108_19.gs` and `examples/SG108_33.gs` are the exported actions of SmallGroup(108,19)
and SmallGroup(108,33) used in the search; the combo indices refer to the order of the actions in
these files (GAP's subgroup order may differ between versions, so the files are included). With
these settings the 171-vertex graph was found for 20 of the seeds 1–20 and the 126-vertex graph
for 8 of them; a `FOUND` line reports the orbits as `size[stabilizer order]` and writes the edge list.

To export actions for another group (GAP 4, from this directory):

    Read("gsets.g");
    ExportGSets(SmallGroup(108,19), "SG108_19", 345, "SG108_19.gs");

## Scope of the search on 2026-11-10

714 non-abelian groups from the SmallGroups library of orders 100 to 160 (orders with at most
300 groups) with up to 3 orbits; 104 groups of orders 96–99 with up to 4 orbits; and 38 non-affine
primitive groups (orders 60 to about 10,000) with up to 4 orbits — about 32 million
(orbit multiset, cell) pairs, roughly two thirds of them decided exactly — against the cells of the
Comellas table with recorded orders at most 300. The search was stopped before reaching larger
groups. The two graphs above were the only results exceeding the table. Near misses and exact
non-existence results within this restricted family are not claims about the cells.
