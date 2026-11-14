import DDPGeneralQ.Charts.Controller
import DDPGeneralQ.Charts.ZMod3
import DDPGeneralQ.Charts.ZMod5
import DDPGeneralQ.Charts.ZMod7
import DDPGeneralQ.Charts.ZMod11
import DDPGeneralQ.Charts.ZMod13
import DDPGeneralQ.Charts.ZMod17
import DDPGeneralQ.Charts.ZMod19
import DDPGeneralQ.Charts.ZMod23
import DDPGeneralQ.Charts.ZMod29
import DDPGeneralQ.Charts.ZMod31
import DDPGeneralQ.Charts.ZMod37
import DDPGeneralQ.Charts.ZMod41
import DDPGeneralQ.Charts.ZMod43
import DDPGeneralQ.Charts.ZMod47
import DDPGeneralQ.Charts.ZMod53
import DDPGeneralQ.Charts.ZMod59
import DDPGeneralQ.Charts.ZMod61
import DDPGeneralQ.Charts.ZMod67
import DDPGeneralQ.Charts.ZMod71
import DDPGeneralQ.Charts.ZMod73
import DDPGeneralQ.Charts.ZMod79
import DDPGeneralQ.Charts.GF4Chart
import DDPGeneralQ.Charts.GF8Chart
import DDPGeneralQ.LargePrimes
import Mathlib.Algebra.IsPrimePow
import Mathlib.Tactic.IntervalCases
import Mathlib.Tactic.NormNum.Prime

/-!
# Main theorem

For every `n ≥ 1` with `n % 4 ≠ 2` there is a graph with `144 n^5` vertices, maximum degree at
most `4 n`, in which every two vertices are joined by a walk of length at most 5; that is,
`N(4n, 5) ≥ 144 n^5` in the degree/diameter problem. In particular this holds for every prime
power `n = q ≥ 3`.

The graph is the route-chart lift of the 144-vertex controller of arXiv:2606.15860 over a finite
commutative ring with `n` elements: a product of copies of GF(4), GF(8) and `ZMod p` for odd primes
`p`. The finite facts used are the `decide +kernel` theorems in `DDPGeneralQ/Charts/` and `G_eq` in
`DDPGeneralQ/LargePrimes.lean`; everything else is proved in general.
-/

namespace DDP

theorem good_small_odd_prime (p : ℕ) (hp : p.Prime) (h2 : p ≠ 2) (h79 : p ≤ 79) : Good p := by
  interval_cases p
  all_goals first
    | exact good_3
    | exact good_5
    | exact good_7
    | exact good_11
    | exact good_13
    | exact good_17
    | exact good_19
    | exact good_23
    | exact good_29
    | exact good_31
    | exact good_37
    | exact good_41
    | exact good_43
    | exact good_47
    | exact good_53
    | exact good_59
    | exact good_61
    | exact good_67
    | exact good_71
    | exact good_73
    | exact good_79
    | (exfalso; exact h2 rfl)
    | (exfalso; norm_num at hp)

theorem good_odd_prime (p : ℕ) (hp : p.Prime) (h2 : p ≠ 2) : Good p := by
  by_cases h : p ≤ 79
  · exact good_small_odd_prime p hp h2 h
  · exact good_large_prime p hp (by omega)

theorem good_of_mod_four_ne_two (n : ℕ) (hn : 0 < n) (h : n % 4 ≠ 2) : Good n :=
  good_of_mod_four good_4 good_8 good_odd_prime n hn h

/-- **Main theorem.** `N(4n, 5) ≥ 144 n^5` for every `n ≥ 1` with `n % 4 ≠ 2`. -/
theorem main (n : ℕ) (hn : 0 < n) (h : n % 4 ≠ 2) :
    ∃ (V : Type) (_ : Fintype V) (G : SimpleGraph V) (_ : DecidableRel G.Adj),
      Fintype.card V = 144 * n ^ 5 ∧ (∀ v, G.degree v ≤ 4 * n) ∧
        ∀ u v, ∃ w : G.Walk u v, w.length ≤ 5 := by
  obtain ⟨V, hV, G, hG, hcard, hdeg, hwalk⟩ :=
    exists_graph_of_good Ctrl.controller Ctrl.exactNB5 (good_of_mod_four_ne_two n hn h)
  exact ⟨V, hV, G, hG, by rw [hcard, Fintype.card_fin], hdeg, hwalk⟩

lemma mod_four_ne_two_of_isPrimePow {q : ℕ} (hq : IsPrimePow q) (h3 : 3 ≤ q) : q % 4 ≠ 2 := by
  obtain ⟨p, k, hp, hk, rfl⟩ := (isPrimePow_nat_iff q).mp hq
  rcases hp.eq_two_or_odd' with rfl | hodd
  · have hk2 : 2 ≤ k := by
      by_contra hlt
      have : k = 1 := by omega
      subst this
      omega
    have : 4 ∣ 2 ^ k := by
      have := pow_dvd_pow 2 hk2
      simpa using this
    omega
  · have : (p ^ k) % 2 = 1 := Nat.odd_iff.mp (hodd.pow)
    omega

/-- **Prime powers.** `N(4q, 5) ≥ 144 q^5` for every prime power `q ≥ 3`. -/
theorem main_prime_power (q : ℕ) (hq : IsPrimePow q) (h3 : 3 ≤ q) :
    ∃ (V : Type) (_ : Fintype V) (G : SimpleGraph V) (_ : DecidableRel G.Adj),
      Fintype.card V = 144 * q ^ 5 ∧ (∀ v, G.degree v ≤ 4 * q) ∧
        ∀ u v, ∃ w : G.Walk u v, w.length ≤ 5 :=
  main q (by omega) (mod_four_ne_two_of_isPrimePow hq h3)

end DDP
