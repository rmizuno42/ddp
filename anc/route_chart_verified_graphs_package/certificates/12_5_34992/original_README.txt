Phase 35: GF(3)^5 chart combined with the C4 x C6 144-vertex controller.

This is an immediate generalization of the phase34 controller.  The controller is the same 6-vertex loopless 4-regular multigraph with voltage group C4 x C6, yielding a simple 144-vertex 4-regular controller with exact nonbacktracking length-5 coverage.

Fiber chart: GF(3)^5, 4 symbols a,a^-1,b,b^-1, verified over all 324 reduced words of length 5.

Resulting graph:
  vertices = 144 * 3^5 = 34992
  max degree = 4 * 3 = 12
  diameter <= 5

Run:
  python verify_candidate.py
  python generate_final_graph.py
