# Route-chart lifts for general q: $N(4n,5)\ge 144\,n^5$

This folder extends the construction of [arXiv:2606.15860](https://arxiv.org/abs/2606.15860)
beyond $q=3$ and $q=4$.

**[English proof (PDF)](proof/general_q.pdf)** · [LaTeX source](proof/general_q.tex) ·
[Lean formalization](lean/)

## Results

Let $N(\Delta,D)$ be the largest order of a graph with maximum degree at most $\Delta$ and
diameter at most $D$.

1. **Theorem 1.** $N(4n,5)\ge 144\,n^5$ for every $n\ge 1$ with $n\not\equiv 2\pmod 4$, in
   particular for every prime power $q\ge 3$. The graph is the route-chart lift of the
   paper's 144-vertex controller over a finite commutative ring with $n$ elements.
   That ring is a product of copies of $\mathrm{GF}(4)$, $\mathrm{GF}(8)$ and
   $\mathbb Z/p\mathbb Z$ for odd primes $p$.
   **This theorem is formalized in Lean 4, including every finite check.**
2. **Theorem 2 (field version).** For every prime power $q\ge 3$, a universal route chart
   on $\mathbb F_q^5$ exists. The lift over $\mathbb F_q$ is then $4q$-regular, of order
   $144\,q^5$ and diameter 5.
3. **Proposition 3.** No universal route chart exists on $\mathbb F_2^5$, so no finite
   commutative ring of order $\equiv 2 \pmod 4$ carries one. Theorem 1 is therefore the full
   range of this construction.

For $n=3,4$ these are the paper's graphs on 34,992 and 147,456 vertices. For $n=5$ the
lift is 20-regular on 450,000 vertices. Its edge list was checked directly by
breadth-first search from every vertex: diameter 5. Comellas's table stops at
$\Delta=16$. The CombinatoricsWiki table, last modified 2022-02-18, lists 281,820 for
$(20,5)$; later results have not been checked.

### How Theorems 1 and 2 differ

For a prime power $q\ge 3$ both theorems give the same bound $N(4q,5)\ge 144\,q^5$. As a
lower bound, Theorem 2 adds nothing to Theorem 1. The two differ in the graph.

| | Theorem 1 (formalized in Lean) | Theorem 2 (not formalized) |
|---|---|---|
| Ring used for the lift | some commutative ring with $q$ elements | the field $\mathbb F_q$, as in the paper |
| $q=9$ | $\mathbb Z/3\times\mathbb Z/3$ | $\mathrm{GF}(9)$ |
| $q=32$ | $\mathrm{GF}(8)\times\mathrm{GF}(4)$ | $\mathrm{GF}(32)$ |
| Charts needed | $\mathrm{GF}(4)$, $\mathrm{GF}(8)$, $\mathbb Z/p$ | also $\mathrm{GF}(32)$, $\mathrm{GF}(128)$, $\mathrm{GF}(2048)$, $\mathrm{GF}(8192)$ |
| Further arguments | products of rings | field extensions, Schwartz–Zippel |

For $q$ prime and for $q=4,8$ the two graphs coincide; they differ only for
$q=9,16,25,27,32,\dots$ Theorem 1 uses products of rings to avoid the large fields and the
Schwartz–Zippel argument, which would be costly to formalize. This is why Theorem 1, not
Theorem 2, is the one formalized in Lean.

## How each part is verified

| Part | Finite facts checked by | Formalized in Lean |
|---|---|---|
| Lift lemma, products, induction on $n$ | — (general proof) | yes |
| Controller: inverse arcs, a reduced word for all $144^2$ pairs | Lean kernel, Python | yes |
| Charts over $\mathrm{GF}(4)$, $\mathrm{GF}(8)$, $\mathbb Z/p$ ($p\le 79$) with inverse certificates | Lean kernel, Python | yes |
| Six integer charts, adjugate certificates, $\gcd$ factorization (primes $p>79$) | Lean kernel, Python | yes |
| Field version: charts over $\mathrm{GF}(32)$, $\mathrm{GF}(128)$, $\mathrm{GF}(2048)$, $\mathrm{GF}(8192)$; Schwartz–Zippel | Python | no |
| No chart over $\mathbb F_2$ (exhaustive search) | C program, cross-checked with Python | no |

In Lean the finite facts are proved by `decide +kernel`, so the kernel itself evaluates them.
`native_decide` is not used, and `DDP.main` has no hypotheses beyond its statement.

**Continuous integration.** The [GitHub Actions workflow](../../../.github/workflows/lean-general-q.yml)
builds the whole project, every chart check included, and runs `#print axioms`. It fails if
`DDP.main` or `DDP.main_prime_power` depends on anything other than Lean's standard axioms
`propext`, `Classical.choice` and `Quot.sound`. On a GitHub runner the build takes about
20 minutes. The heaviest
check, the controller, needs about 10 GB of memory, and each chart check needs 5–8 GB.

## Contents

```text
proof/general_q.tex, .pdf   English proof of Theorems 1–2 and Proposition 3
data/controller.json        arc maps of the 144-vertex controller and a reduced word for every
                            ordered pair of vertices (exported from the paper's code)
data/charts/gf<q>.json      universal charts over GF(q): q = 3, 4 (from the paper), every odd
                            prime 5 ≤ q ≤ 79, and q = 8, 32, 128, 2048, 8192
data/charts/integer_charts.json   six integer charts
scripts/verify_all.py       independent Python checks of all data (add --f2 for the GF(2) search)
scripts/gen_lean_data.py    writes the Lean chart files with inverse / adjugate certificates
scripts/export_controller.py, chartsearch.c, random_chart_gf2k.py, f2exhaust.c, ...
lean/                       Lean 4 project (Lean 4.32.2, Mathlib)
  DDPGeneralQ/Basic.lean    controllers, route charts over commutative rings, lift graph,
                            degree bound and walks of length ≤ 5
  DDPGeneralQ/Good.lean     transport along ring maps, products, induction on n
  DDPGeneralQ/Codes.lean    list arithmetic used by the checks and its agreement with matrices
  DDPGeneralQ/Checks.lean   Boolean checks and what a passing check proves
  DDPGeneralQ/Instances.lean  arithmetic modulo p, integers, GF(4) and GF(8) as rings
  DDPGeneralQ/Charts/       generated data with `decide +kernel` checks
  DDPGeneralQ/LargePrimes.lean  primes p > 79 via the integer charts
  DDPGeneralQ/Main.lean     `DDP.main` and `DDP.main_prime_power`
```

## Reproduce

```bash
cd results/diameter5-paper/general-q
python3 scripts/verify_all.py --f2
python3 scripts/gen_lean_data.py        # regenerates lean/DDPGeneralQ/Charts/*.lean
cd lean && lake exe cache get && ./ci_build.sh   # or `lake build`; see the memory note above
lake env lean AxiomsCheck.lean
```

The Lean statement of Theorem 1:

```lean
theorem DDP.main (n : ℕ) (hn : 0 < n) (h : n % 4 ≠ 2) :
    ∃ (V : Type) (_ : Fintype V) (G : SimpleGraph V) (_ : DecidableRel G.Adj),
      Fintype.card V = 144 * n ^ 5 ∧ (∀ v, G.degree v ≤ 4 * n) ∧
        ∀ u v, ∃ w : G.Walk u v, w.length ≤ 5
```

## License

As in the rest of the repository: the code in this folder (`scripts/`, and the Lean sources
and build files in `lean/`) is licensed under the [MIT License](../../../LICENSE-MIT); the data,
the proof document and the other material are licensed under
[CC BY 4.0](../../../LICENSE-CC-BY).
