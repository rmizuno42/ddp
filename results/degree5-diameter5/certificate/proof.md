# A loopless folded Cayley graph of maximum degree 5

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
involution $h$; explicitly, $h^2=1$ and $h^{-1}=h$.
Its first three listed elements are involutions; the last
two are mutual inverses.

## The graph

On $L$, join $x$ to $hxs$ for each $s\in S$, removing loops.
These operations stay in $L$. If $y=hxs$, then $x=hys^{-1}$,
so adjacency is symmetric. Distinct elements of $S$ give distinct images
of each $x$. A loop occurs precisely when $x^{-1}hx\in S$.

The constructor enumerates all projective matrices, confirming 30 loop sites
and no other degree deficiency. The simple graph consequently has
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

Starting at $z_0=x$, define $z_k=hz_{k-1}s_k$. Associativity gives

$$
z_k=h^kx(s_1\cdots s_k).
$$

For example, $z_2=h(hxs_1)s_2=h^2xs_1s_2$. This calculation does not
require $h$ to commute with $x$ or any $s_i$.
To have $z_5=y$, the required product is $x^{-1}h^{-5}y$.
Since $h^2=1$, we have $h^{-5}=h$, so this product equals $x^{-1}hy$.
It lies in $P\setminus L$, and the identity $S^5=P\setminus L$ supplies
$s_1,\ldots,s_5\in S$ with $s_1\cdots s_5=x^{-1}hy$. Substitution gives

$$
z_5=h^5x(x^{-1}hy)=h^6y=(h^2)^3y=y.
$$

Deleting stationary steps gives a walk of length at most 5 in the
loopless graph. Thus its diameter is at most 5.
The archived package also checks this identity using an independent
permutation representation on 12 points and lists a word for every
element of $P\setminus L$.

The Moore bound for maximum degree 5 and diameter at most 4 is
$1+5(1+4+16+64)=426<660$, so the diameter is exactly 5.
The degree/diameter problem requires maximum degree at most 5, not
5-regularity. The loopless graph therefore establishes $N(5,5)\ge660$
without adding any edges.

## Symmetry

Let $A=C_L(h)$ and $B=\{b\in L:b^{-1}Sb=S\}$. Enumeration gives
$|A|=10$ and $|B|=6$, with $A$ dihedral and $B\cong S_3$.
The maps $x\mapsto axb^{-1}$, for $a\in A$ and $b\in B$, preserve
adjacency: if $y=hxs$, then
$ayb^{-1}=h(axb^{-1})(bsb^{-1})$, and $bsb^{-1}\in S$.
These bijections also preserve the removal of loops.

The constructor and verifier check the group relations, the 60 distinct
actions, and preservation of all edges. The full automorphism-group
calculation with nauty gives order 60, and its generators generate exactly
these actions; see [symmetry](symmetry/README.md). Thus the full group is
the direct product of the dihedral group of order 10 and $S_3$.

This does not assert that 660 is optimal for $N(5,5)$.
