# The 6-regular graph of order 126 and diameter 3

## Construction

Let $N=\mathbb Z_3\times\mathbb Z_3$. The base multigraph $B$ has 14 vertices:
two hubs $h=0$ and $h'=1$, a triangle $A=\{a_0,a_1,a_2\}=\{2,3,4\}$ whose vertices
are all adjacent to $h$, three further vertices $B_0=\{b_0,b_1,b_2\}=\{5,6,7\}$ joined
to $A$ by a complete bipartite graph, and the same configuration
$A'=\{8,9,10\}$, $B'_0=\{11,12,13\}$ attached to $h'$. Finally $h$ and $h'$ are
joined by three parallel edges, and so are $b_j$ and $b'_j$ for $j=0,1,2$.
Every base vertex has degree 6.

The vertices of the graph are the pairs $(u,x)$ with $u\in B$ and $x\in N$.
A base edge $u\to v$ carrying the voltage $g\in N$ joins $(u,x)$ to $(v,x+g)$ for all $x$.
The voltages (see [construct.py](construct.py) and [voltage_graph.json](voltage_graph.json)) are:

| base edges | voltages |
|---|---|
| $h\to h'$ (three edges) | $(0,0),(1,1),(2,1)$, the parabola $\{(t,t^2)\}$ |
| $h\to a_l$, $h'\to a'_l$, $a_0\to b_j$, $a'_0\to b'_j$ | $0$ |
| $a_l\to a_m$, $a'_l\to a'_m$ | $(m-l)\,(0,2)$ |
| $a_l\to b_j$, $a'_l\to b'_j$ | $l\,w_j$ with $w_0=(2,0)$, $w_1=(1,1)$, $w_2=(1,0)$ |
| $b_0\to b'_0$ | $(2,2),(0,2),(0,1)$ |
| $b_1\to b'_1$ | $(2,0),(2,1),(1,2)$ |
| $b_2\to b'_2$ | $(1,0),(0,0),(0,2)$ |

Vertex $(u,(x_0,x_1))$ has ID $9u+3x_0+x_1$.

## Order, degree and simplicity

There are $14\cdot 9=126$ vertices. Each base vertex has degree 6, so every vertex has
degree 6 provided the graph is simple. Parallel base edges carry distinct voltages, and no
base edge is a loop, so no two lifted edges coincide and there are no loops; the constructor
asserts this edge by edge. The graph is simple and 6-regular, with $126\cdot6/2=378$ edges.

## Diameter

The translations $(u,x)\mapsto(u,x+c)$, $c\in N$, preserve every edge. It therefore suffices
to reach every vertex from the 14 representatives $(u,0)$. The file
[base_trees.json](certificates/base_trees.json) gives a spanning tree rooted at each
representative, of depth at most 3. The [tree checker](check_certificate.py) verifies every
parent edge against the construction formula, every depth, and the translation invariance of the
edge set. Hence every pair of vertices is at distance at most 3.

A second, independent finite certificate is [verify_voltage.py](verify_voltage.py): for each of
the $14^2$ ordered pairs $(u,v)$ of base vertices it computes the set of voltage sums of base walks
from $u$ to $v$ of length at most 3. All 196 sets are equal to $N$.

The Moore bound for maximum degree 6 and diameter 2 is $1+6+6\cdot5=37<126$. Hence the
diameter is exactly 3. Ordinary BFS from every vertex of the published edge list confirms this.

## Symmetry

The group of translations is a normal subgroup $N\cong C_3\times C_3$ of the automorphism group
that acts freely on the vertices, so the graph is a regular $N$-cover of $B$. The full
automorphism group, **computed** with nauty (dreadnaut) and identified with GAP 4.16.1, has
order 162 and is isomorphic to SmallGroup(162,40) $=(C_3\times((C_3\times C_3)\rtimes C_3))\rtimes C_2$.
It has three vertex orbits: the fibres over $\{h,h',b_0,b_2,b'_0,b'_2\}$ (54 vertices, stabilizer
$C_3$), the fibres over the two triangles (54 vertices, stabilizer $C_3$), and the fibres over
$\{b_1,b'_1\}$ (18 vertices, stabilizer $C_3\times C_3$). In particular the hubs are equivalent to
four of the vertices $b_j,b'_j$.
The generators are listed in [automorphisms.json](automorphisms.json); `verify.py` checks that
each of them preserves the edge set. The group order itself is a computation, not part of the
proof of the degree and diameter.

## How the graph was found

The graph was found as an *orbit graph*: a union of orbitals of the group
SmallGroup(108,33) $\cong C_3\times((C_3\times C_3)\rtimes C_4)$ acting on the disjoint union of
its coset spaces $G/C_6\sqcup G/C_2\sqcup G/C_2$ (18 + 54 + 54 points; the central involution
acts trivially). The file [orbit_graph_certificate.json](orbit_graph_certificate.json) contains the
permutation generators, one representative edge for each of the 10 edge orbits, and an explicit
isomorphism to the published labelling; [check_isomorphism.py](check_isomorphism.py) rebuilds the
orbit graph from these data and checks the isomorphism. The voltage description above was
obtained from the same graph by normalising the voltages along a spanning tree of $B$.

## Remark on the voltages

Each triple of parallel voltages is a $(3,3,3,1)$ relative difference set in $N$: its six
differences are distinct and avoid exactly one 1-dimensional subspace. The hub bundle avoids
$\langle(0,1)\rangle$, the direction of the triangle voltages; the bundle at $b_j$ avoids the
direction of $(0,2)+w_j$, which is the direction of the lines along which the clique over a point
meets the fibre of $b_j$. The four directions of $\mathbb F_3^2$ each occur once.
For example, a vertex $(h,x)$ reaches the hub fibre within 3 steps only along $h\,h'\,h$
(differences of the parabola: 6 nonzero elements, none in $\langle(0,1)\rangle$) and along
$h\,a_l\,a_m\,h$ (the multiples of $(0,2)$); together with $x$ itself these are exactly the
9 elements of $N$. These are observations about this graph, not a general theorem.
No optimality of $N(6,3)$ is claimed.
