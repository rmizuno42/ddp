# A folded Cayley graph and an invariant regular completion

All matrices below are projective classes over $\mathbb F_{11}$, represented
by the tuple $(a,b,c,d)$ of entries in row order, scaled so the first nonzero
entry is 1. Multiplication is followed by this normalization.
Let $P=\mathrm{PGL}(2,11)$, and identify $L=\mathrm{PSL}(2,11)$ with the
subgroup of projective matrices whose determinant is a nonzero square.
Then $|P|=1320$ and $|L|=660$.

Put

$$
h=(1,0,0,10),\qquad
S=\{h,(1,1,4,10),(1,5,3,10),(0,1,3,8),(1,4,1,0)\}.
$$

The set $S$ is inverse-closed, lies in $P\setminus L$, and contains the
involution $h$. Its first three listed elements are involutions; the last
two are mutual inverses.

## The base graph

On $L$, join $x$ to $hxs$ for each $s\in S$, removing loops.
These operations stay in $L$. If $y=hxs$, then $x=hys^{-1}$,
so adjacency is symmetric. Distinct elements of $S$ give distinct images
of each $x$. A loop occurs precisely when $x^{-1}hx\in S$.

The constructor enumerates all projective matrices, confirming 30 loop sites
and no other degree deficiency. The simple base graph consequently has
30 vertices of degree 4, 630 of degree 5, and 1,635 edges.
These finite counts and the matrix data are recorded in
[construction.json](construction.json).

The interpretation as a folding is explicit. Start with the bipartite
Cayley graph on $P$ having edges $g\sim gs$. Left multiplication by $h$
is a fixed-point-free automorphism interchanging its two cosets. Each
orbit $\{g,hg\}$ contains exactly one element of $L$. The induced
adjacency on these representatives is $x\sim hxs$, including the loops
that are removed above.

## Diameter bound

For the sets of products of exactly $k$ elements of $S$, direct
enumeration gives

$$
(|S^0|,|S^1|,|S^2|,|S^3|,|S^4|,|S^5|)
=(1,5,21,85,341,660),\qquad S^5=P\setminus L.
$$

For any $x,y\in L$, choose $s_1,\ldots,s_5\in S$ with
$s_1\cdots s_5=x^{-1}hy$. Applying the five maps $z\mapsto hzs_i$
in order takes $x$ to $h^5x(s_1\cdots s_5)=y$.
Deleting stationary steps gives a walk of length at most 5 in the
loopless base graph. Thus its diameter is at most 5.
The archived package also checks this identity using an independent
permutation representation on 12 points and lists a word for every
element of $P\setminus L$.

## Invariant matching

Let $A=C_L(h)$ and $B=\{b\in L:b^{-1}Sb=S\}$. Enumeration gives
$|A|=10$ and $|B|=6$, with $A$ dihedral and $B\cong S_3$.
For each involution $s\in S$, there is a unique nonidentity involution
$b_s\in B$ commuting with $s$:

| $s$ | $b_s$ |
|---|---|
| $(1,0,0,10)$ | $(0,1,8,0)$ |
| $(1,1,4,10)$ | $(1,1,5,10)$ |
| $(1,5,3,10)$ | $(1,9,3,10)$ |

For a loop site $x$, set $s=x^{-1}hx$ and $f(x)=xb_s$.
Then $f(x)^{-1}hf(x)=b_s^{-1}sb_s=s$, so $f(x)$ is also a loop site
and $f(f(x))=x$. Since $b_s\ne1$, there are no fixed points.
The resulting 15 pairs are checked to be nonedges of the base graph.
Adding them therefore produces a simple 5-regular graph with 1,650 edges.
Its diameter is at most 5 because it contains the base graph.
The Moore bound for maximum degree 5 and diameter at most 4 is
$1+5(1+4+16+64)=426<660$, so both graphs have diameter exactly 5.

## Symmetry

The maps $x\mapsto axb^{-1}$, for $a\in A$ and $b\in B$, preserve
base adjacency. They also preserve the matching: left multiplication
by $a$ leaves $x^{-1}hx$ unchanged, while right multiplication by
$b^{-1}$ conjugates it by $b$. Uniqueness of $b_s$ makes its choice
equivariant under this conjugation.

The constructor and verifier check the group relations, the 60 distinct
actions, and preservation of all edges. The full automorphism-group
calculation with nauty gives order 60, and its generators generate exactly
these actions; see [symmetry](symmetry/README.md). Thus the full group is
the direct product of the dihedral group of order 10 and $S_3$.

The September archive uses the alternative matching $x\sim tx$ at the
loop sites, with $t=(0,1,10,0)$. Its full automorphism group has order 12.
The new matching retains all 60 symmetries of the base graph without
changing the order or diameter. This does not assert that 660 is optimal
for $N(5,5)$.
