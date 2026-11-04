# The cubic graph of order 208

Let $V=\{0,\ldots,12\}\times\mathbb Z_{16}$. The edges are the path edges
$(i,x)\sim(i+1,x)$ for $0\le i<12$, the cycle edges
$(0,x)\sim(0,x+1)$, the matching edges $(12,x)\sim(12,x+8)$,
and the six chord families in the [summary](../README.md).
All edges are undirected, and all second coordinates are read modulo 16.

## Order and degree

There are $13\cdot16=208$ vertices. State 0 has one path neighbor and two
cycle neighbors. States 1 through 11 each have two path neighbors and one
chord neighbor. State 12 has one path neighbor, one chord neighbor, and
one matching neighbor. These neighbors are distinct and none is the
vertex itself. In particular, the chord between states 10 and 11 has
shift −1, so it does not duplicate their path edge. The graph is simple
and 3-regular, with $208\cdot3/2=312$ edges.

## Diameter

Translation $(i,x)\mapsto(i,x+c)$ preserves every edge. It therefore
suffices to reach every vertex from the 13 representatives $(i,0)$.
The file [thirteen_trees.json](certificates/thirteen_trees.json) specifies
a spanning tree rooted at each representative, with depth at most 7.
The [tree checker](check_certificate.py) verifies every parent edge from
the explicit formula, every depth, and every translation. Hence every pair
of vertices is at distance at most 7.

There is a second finite certificate: [verify_voltage.py](verify_voltage.py)
computes, for each ordered pair of states, the set of coordinate changes
obtainable by walks of length at most 7. All 169 sets equal $\mathbb Z_{16}$.

The Moore bound for maximum degree 3 and diameter at most 6 is
$1+3\sum_{k=0}^{5}2^k=190$. Since $208>190$, the diameter is exactly 7.
Ordinary all-pairs BFS on the published edge list also checks this directly.

## Girth

Every radius-4 distance sphere sequence begins $(1,3,6,12,24)$, as
checked by [verify_structure.py](verify_structure.py). In a cubic graph
this excludes cycles of length at most 8. The vertex IDs

    0, 16, 114, 130, 83, 99, 115, 17, 1, 0

give a cycle of length 9, so the girth is exactly 9.

## Full automorphism group

For each vertex, record its distance sphere sizes, together with the
multiset of these sequences at its three neighbors. This is an intrinsic
graph invariant. Its 13 distinct classes are precisely the fibers
$\{i\}\times\mathbb Z_{16}$; this finite assertion is checked by
[verify_structure.py](verify_structure.py).
Every automorphism therefore preserves each fiber.

Fiber 0 induces a 16-cycle, so an automorphism acts there as
$x\mapsto\varepsilon x+c$, with $\varepsilon\in\{1,-1\}$.
For each path edge between fibers 0 through 10, a vertex has a unique
neighbor in the next fiber. Thus the same coordinate map propagates
through these fibers. The chord from $(1,x)$ to $(7,x+2)$ requires
$2\varepsilon=2\pmod{16}$, excluding $\varepsilon=-1$.
The unique-neighbor links from fiber 2 to fiber 12, then from fiber 12
to fiber 11, determine the remaining action. An automorphism fixing
fiber 0 pointwise is consequently the identity.

There are at most 16 automorphisms, and the 16 translations provide all
of them. Thus the full automorphism group is $C_{16}$.
This statement is about symmetry; no optimality of $N(3,7)$ is claimed.
