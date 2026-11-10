# The graph of order 171, maximum degree 7 and diameter 3

## Construction

The base multigraph $B$ has 19 vertices: a hub $0$, twelve *core* vertices $1,\dots,12$ and six
*spoke* vertices $13,\dots,18$. The voltage group is $\mathbb Z_9$, and the vertices of the graph
are the pairs $(u,x)$, $u\in B$, $x\in\mathbb Z_9$, with ID $9u+x$. A base edge $u-v$ ($u<v$)
with voltage $a$ joins $(u,x)$ to $(v,x+a)$; a loop at $u$ with voltage $a$ joins $(u,x)$ to
$(u,x+a)$, so that $(u,x)$ is also adjacent to $(u,x-a)$. The base graph consists of

- the six hub edges $0-13, 0-14$ (voltage 5), $0-15, 0-16$ (voltage 2), $0-17, 0-18$ (voltage 8);
- three spoke pairs $13-14$, $15-16$, $17-18$, each a double edge with voltages 3 and 6, and a loop
  at every spoke vertex (voltage 1 at 13 and 14, 4 at 15 and 16, 2 at 17 and 18);
- two edges from every spoke to the core: $13-8, 13-11, 14-2, 14-5$ (voltage 1),
  $15-6, 15-12, 16-3, 16-9$ (voltage 4), $17-4, 17-7, 18-1, 18-10$ (voltage 7);
- 36 core edges, in which the six pairs $\{1,10\},\{2,5\},\{3,9\},\{4,7\},\{6,12\},\{8,11\}$ are
  double edges; the full list is in [construct.py](construct.py) and [voltage_graph.json](voltage_graph.json).

The hub has degree 6 and every other base vertex has degree 7 (a loop counts twice).

## Order, degree and simplicity

There are $19\cdot9=171$ vertices. Parallel base edges carry distinct voltages, every loop voltage
$a$ satisfies $a\ne0$ and $2a\ne0$, and different loops at a vertex do not exist, so the lifted
edges are pairwise distinct and there are no loops; the constructor asserts this edge by edge.
The 9 vertices $(0,x)$ have degree 6, the other 162 vertices have degree 7, and there are
$(9\cdot6+162\cdot7)/2=594$ edges. The maximum degree is 7.

## Diameter

The translations $(u,x)\mapsto(u,x+c)$ preserve every edge, so it suffices to reach every vertex
from the 19 representatives $(u,0)$. The file [base_trees.json](certificates/base_trees.json) gives
a spanning tree of depth at most 3 rooted at each of them; the [tree checker](check_certificate.py)
verifies every parent edge against the construction formula, every depth, and the translation
invariance. Hence the diameter is at most 3.

Independently, [verify_voltage.py](verify_voltage.py) computes for each of the $19^2$ ordered pairs
$(u,v)$ of base vertices the set of voltage sums of base walks of length at most 3 from $u$ to $v$;
all 361 sets equal $\mathbb Z_9$.

The Moore bound for maximum degree 7 and diameter 2 is $1+7+7\cdot6=50<171$, so the diameter is
exactly 3. Ordinary BFS from every vertex of the published edge list confirms this.

## Symmetry

The translations form a normal subgroup $\mathbb Z_9$ of the automorphism group acting freely on the
vertices, so the graph is a regular $\mathbb Z_9$-cover of $B$. The full automorphism group,
**computed** with nauty (dreadnaut) and identified with GAP 4.16.1, has order 216 and is isomorphic
to SmallGroup(216,96) $=(C_2\times C_2)\rtimes(C_9\rtimes C_6)$. Its vertex orbits are the hub fibre
(9 vertices, stabilizer $C_2\times A_4$), the core fibres (108 vertices, stabilizer $C_2$) and the spoke
fibres (54 vertices, stabilizer $C_2\times C_2$). The generators are in
[automorphisms.json](automorphisms.json); `verify.py` checks that each preserves the edge set.
The group order is a computation and is not used in the proof of the degree and diameter.

## How the graph was found

The graph was found as an *orbit graph* of SmallGroup(108,19) $\cong(C_2\times C_2)\rtimes(C_9\rtimes C_3)$
acting on $G/A_4\sqcup G\sqcup G/C_2$ (9 + 108 + 54 points): a union of 7 orbitals.
[orbit_graph_certificate.json](orbit_graph_certificate.json) contains the permutation generators,
one representative edge per edge orbit and an explicit isomorphism to the published labelling,
which [check_isomorphism.py](check_isomorphism.py) verifies. The voltage description was obtained
by passing to the quotient by the freely acting normal subgroup $C_9$ of the automorphism group.

No optimality of $N(7,3)$ is claimed.
