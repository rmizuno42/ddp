import DDPGeneralQ.Basic
import Mathlib.Data.Fintype.Prod
import Mathlib.Data.Fintype.Pi
import Mathlib.Data.Nat.Prime.Basic

/-!
# Charts over products of rings, and the orders `n` that are reached

`Good n` says that some commutative ring with `n` elements carries a universal
route chart. It is closed under products, so it suffices to know `Good 4`,
`Good 8` and `Good p` for the odd primes `p`; then `Good n` holds for every
`n ≥ 1` with `n % 4 ≠ 2`. Together with an exact-NB-5 controller on `C`, a
universal chart over a ring with `n` elements gives a graph with
`|C| * n^5` vertices, maximum degree at most `4 n`, and every two vertices
joined by a walk of length at most 5.
-/

open Matrix

namespace DDP

attribute [ext] Chart

namespace Chart

variable {R S : Type} [CommRing R] [CommRing S]

lemma mulVec_map (f : R →+* S) (M : Matrix (Fin 5) (Fin 5) R) (v : Fin 5 → R) :
    f ∘ (M *ᵥ v) = M.map f *ᵥ (f ∘ v) :=
  funext fun i => RingHom.map_mulVec f M v i

/-- Transport of a chart along a ring homomorphism. -/
def map (f : R →+* S) (c : Chart R) : Chart S where
  A t := (c.A t).map f
  b t := f ∘ c.b t
  A_inv t := by rw [← Matrix.map_mul, c.A_inv, Matrix.map_one f f.map_zero f.map_one]
  b_inv t := by rw [c.b_inv t, mulVec_map]

lemma ctrl_map (f : R →+* S) (c : Chart R) (t1 t2 t3 t4 t5 : Sym) :
    (c.map f).ctrl t1 t2 t3 t4 t5 = (c.ctrl t1 t2 t3 t4 t5).map f := by
  ext i j
  fin_cases j <;> simp [ctrl, map, ← mulVec_map]

/-- A universal chart stays universal under a ring homomorphism. -/
lemma Universal.map {c : Chart R} (hc : c.Universal) (f : R →+* S) : (c.map f).Universal := by
  intro t1 t2 t3 t4 t5 hr
  obtain ⟨N, hN⟩ := hc t1 t2 t3 t4 t5 hr
  refine ⟨N.map f, ?_⟩
  rw [ctrl_map, ← Matrix.map_mul, hN, Matrix.map_one f f.map_zero f.map_one]

/-- If every controllability matrix of a reduced word has a unit determinant, the chart is
universal. -/
lemma universal_of_isUnit_det (c : Chart R)
    (h : ∀ t1 t2 t3 t4 t5 : Sym, Reduced t1 t2 t3 t4 t5 → IsUnit (c.ctrl t1 t2 t3 t4 t5).det) :
    c.Universal := fun t1 t2 t3 t4 t5 hr =>
  ⟨(c.ctrl t1 t2 t3 t4 t5)⁻¹, Matrix.mul_nonsing_inv _ (h t1 t2 t3 t4 t5 hr)⟩

/-- The product of two charts, a chart over the product ring. -/
def prod (c : Chart R) (d : Chart S) : Chart (R × S) where
  A t := Matrix.of fun i j => (c.A t i j, d.A t i j)
  b t := fun i => (c.b t i, d.b t i)
  A_inv t := by
    ext i j
    · simpa [Matrix.mul_apply, Matrix.one_apply, apply_ite Prod.fst, Prod.fst_sum] using
        congrFun (congrFun (c.A_inv t) i) j
    · simpa [Matrix.mul_apply, Matrix.one_apply, apply_ite Prod.snd, Prod.snd_sum] using
        congrFun (congrFun (d.A_inv t) i) j
  b_inv t := by
    ext i
    · simpa [Matrix.mulVec, dotProduct, Prod.fst_sum] using congrFun (c.b_inv t) i
    · simpa [Matrix.mulVec, dotProduct, Prod.snd_sum] using congrFun (d.b_inv t) i

lemma prod_map_fst (c : Chart R) (d : Chart S) : (c.prod d).map (RingHom.fst R S) = c := by
  ext t i j <;> rfl

lemma prod_map_snd (c : Chart R) (d : Chart S) : (c.prod d).map (RingHom.snd R S) = d := by
  ext t i j <;> rfl

lemma matrix_eq_of_fst_snd {M N : Matrix (Fin 5) (Fin 5) (R × S)}
    (h1 : M.map (RingHom.fst R S) = N.map (RingHom.fst R S))
    (h2 : M.map (RingHom.snd R S) = N.map (RingHom.snd R S)) : M = N := by
  ext i j
  · exact congrFun (congrFun h1 i) j
  · exact congrFun (congrFun h2 i) j

lemma Universal.prod {c : Chart R} {d : Chart S} (hc : c.Universal) (hd : d.Universal) :
    (c.prod d).Universal := by
  intro t1 t2 t3 t4 t5 hr
  obtain ⟨N1, h1⟩ := hc t1 t2 t3 t4 t5 hr
  obtain ⟨N2, h2⟩ := hd t1 t2 t3 t4 t5 hr
  refine ⟨Matrix.of fun i j => (N1 i j, N2 i j), matrix_eq_of_fst_snd ?_ ?_⟩
  · have hN : (Matrix.of fun i j => (N1 i j, N2 i j)).map (RingHom.fst R S) = N1 := by
      ext i j; rfl
    rw [Matrix.map_mul, ← ctrl_map, prod_map_fst, Matrix.map_one _ rfl rfl, hN, h1]
  · have hN : (Matrix.of fun i j => (N1 i j, N2 i j)).map (RingHom.snd R S) = N2 := by
      ext i j; rfl
    rw [Matrix.map_mul, ← ctrl_map, prod_map_snd, Matrix.map_one _ rfl rfl, hN, h2]

end Chart

/-- `Good n`: some commutative ring with `n` elements carries a universal route chart. -/
def Good (n : ℕ) : Prop :=
  ∃ (R : Type) (_ : CommRing R) (_ : Fintype R), Fintype.card R = n ∧ ∃ c : Chart R, c.Universal

lemma Good.mul {m n : ℕ} (hm : Good m) (hn : Good n) : Good (m * n) := by
  obtain ⟨R, _, _, hR, c, hc⟩ := hm
  obtain ⟨S, _, _, hS, d, hd⟩ := hn
  exact ⟨R × S, inferInstance, inferInstance, by rw [Fintype.card_prod, hR, hS], c.prod d, hc.prod hd⟩

/-- The zero ring carries a (trivially universal) chart. -/
lemma good_one : Good 1 := by
  refine ⟨PUnit, inferInstance, inferInstance, rfl, ⟨fun _ => 1, fun _ => 0, ?_, ?_⟩, ?_⟩
  · intro t; ext i j
  · intro t; ext i
  · intro t1 t2 t3 t4 t5 _
    exact ⟨1, by ext i j⟩

/-- From `Good 4`, `Good 8` and `Good p` for all odd primes, `Good n` for every `n ≥ 1`
with `n % 4 ≠ 2`. -/
theorem good_of_mod_four (h4 : Good 4) (h8 : Good 8) (hp : ∀ p, p.Prime → p ≠ 2 → Good p) :
    ∀ n, 0 < n → n % 4 ≠ 2 → Good n := by
  intro n
  induction n using Nat.strong_induction_on with
  | _ n ih =>
    intro hn hmod
    by_cases h1 : n = 1
    · subst h1; exact good_one
    by_cases hodd : n % 2 = 1
    · have hpr : n.minFac.Prime := Nat.minFac_prime h1
      obtain ⟨k, hk⟩ := Nat.minFac_dvd n
      have hp2 : n.minFac ≠ 2 := by
        intro h2
        have : 2 ∣ n := h2 ▸ Nat.minFac_dvd n
        omega
      have hk0 : 0 < k := by
        rcases Nat.eq_zero_or_pos k with h0 | h0
        · rw [h0, mul_zero] at hk; omega
        · exact h0
      have hklt : k < n := by
        have := hpr.two_le
        calc k < 2 * k := by omega
          _ ≤ n.minFac * k := Nat.mul_le_mul_right k this
          _ = n := hk.symm
      have hkodd : k % 2 = 1 := by
        have hn' : Odd n := Nat.odd_iff.mpr hodd
        rw [hk] at hn'
        exact Nat.odd_iff.mp (Nat.odd_mul.mp hn').2
      rw [hk]
      exact (hp _ hpr hp2).mul (ih k hklt hk0 (by omega))
    · obtain ⟨k, hk⟩ : 4 ∣ n := Nat.dvd_of_mod_eq_zero (by omega)
      by_cases hk2 : k % 4 = 2
      · have h8k : n = 8 * (k / 2) := by omega
        rw [h8k]
        exact h8.mul (ih (k / 2) (by omega) (by omega) (by omega))
      · rw [hk]
        exact h4.mul (ih k (by omega) (by omega) hk2)

/-- A universal chart over a ring with `n` elements and an exact-NB-5 controller on `C` give a
graph on `|C| n^5` vertices with maximum degree at most `4 n` and diameter at most 5. -/
theorem exists_graph_of_good {C : Type} [Fintype C] [DecidableEq C] (K : Controller C)
    (hK : K.ExactNB5) {n : ℕ} (hn : Good n) :
    ∃ (V : Type) (_ : Fintype V) (G : SimpleGraph V) (_ : DecidableRel G.Adj),
      Fintype.card V = Fintype.card C * n ^ 5 ∧ (∀ v, G.degree v ≤ 4 * n) ∧
        ∀ u v, ∃ w : G.Walk u v, w.length ≤ 5 := by
  classical
  obtain ⟨R, _, _, hR, c, hc⟩ := hn
  refine ⟨C × (Fin 5 → R), inferInstance, liftGraph K c, inferInstance, ?_, ?_, ?_⟩
  · simp [Fintype.card_prod, hR]
  · intro v
    have := liftGraph_degree_le K c v
    rwa [hR] at this
  · exact liftGraph_walk_le_five K hK c hc

end DDP
