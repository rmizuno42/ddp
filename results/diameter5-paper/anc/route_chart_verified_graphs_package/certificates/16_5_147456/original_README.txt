CRT-block route-chart generalization candidate
============================================

This package contains a verified controllable route-chart construction for

  Delta = 16, diameter <= 5, |V| = 147456.

It improves the earlier 132-controller C22 candidate by replacing the controller
voltage group with C4 x C6 and a different 6-vertex 4-regular loopless multibase.

Construction outline
--------------------
1. Controller:
   A 6-vertex loopless 4-regular multigraph with edge voltages in C4 x C6.
   Its voltage lift has 6*24 = 144 vertices. The verifier checks that it is
   simple, 4-regular, connected, and that every ordered pair of controller
   vertices is connected by an exact nonbacktracking walk of length 5.

2. Fiber chart:
   The same GF(4)^5 universal route-chart control data used in the previous
   (16,5) candidate. For every reduced word of length 5 over
   {a,a^-1,b,b^-1}, the associated 5x5 controllability matrix is nonsingular.

3. Final graph:
   V = V(controller) x GF(4)^5, so |V| = 144*4^5 = 147456.
   Each controller edge contributes 4 fiber-control edges, hence Delta = 16.
   The controller route plus the universal fiber chart gives diameter <= 5.

Files
-----
- controller_c4xc6_multibase.txt: base multigraph and C4 x C6 voltages.
- gf4_s5_universal.txt: GF(4)^5 chart data.
- verify_candidate.py: verifies controller coverage and chart ranks.
- generate_final_graph.py: generates the final edge list.
- final_graph_edges.tsv.gz: generated edge list.
