import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.Combinatorics.SimpleGraph.Finite
import Mathlib.Combinatorics.SimpleGraph.Walk.Operations
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic.Abel

/-!
# Route-chart lift graphs over finite commutative rings

This file formalizes the route-chart lift of arXiv:2606.15860 (§A.4), with
the fibre `F_q^5` replaced by `R^5` for an arbitrary commutative ring `R`.

* Symbols are `Fin 4`: `0 = a`, `1 = a⁻¹`, `2 = b`, `3 = b⁻¹`.
* A controller on a type `C` is given by the four arc maps `σ t : C → C`
  (the head of the arc with symbol `t` leaving a vertex), with
  `σ (inv t) (σ t u) = u`.
* A route chart is a family `A t`, `b t` with `A (inv t) * A t = 1` and
  `b (inv t) = A (inv t) *ᵥ b t` (condition (A.1)).
* The lift graph has vertex set `C × (Fin 5 → R)` and joins `(u, x)` to
  `(σ t u, A t *ᵥ x + l • b t)` for every symbol `t` and every `l : R`.

Main results: every vertex has degree at most `4 * |R|`, and if every
ordered pair of controller vertices is joined by a reduced word of length 5
and every controllability matrix (A.2) of a reduced word has a right inverse,
then every two vertices are joined by a walk of length at most 5.
-/

open Matrix

namespace DDP

/-- Symbols: `0 = a`, `1 = a⁻¹`, `2 = b`, `3 = b⁻¹`. -/
abbrev Sym := Fin 4

/-- The inverse of a symbol. -/
def inv (t : Sym) : Sym := ![1, 0, 3, 2] t

/-- The word `t1 t2 t3 t4 t5` is reduced: no symbol is followed by its inverse. -/
def Reduced (t1 t2 t3 t4 t5 : Sym) : Prop :=
  t2 ≠ inv t1 ∧ t3 ≠ inv t2 ∧ t4 ≠ inv t3 ∧ t5 ≠ inv t4

instance (t1 t2 t3 t4 t5 : Sym) : Decidable (Reduced t1 t2 t3 t4 t5) := by
  unfold Reduced; infer_instance

/-! ## Controllers -/

/-- A controller: four arc maps, the arc with symbol `inv t` reversing the arc with symbol `t`. -/
structure Controller (C : Type) where
  σ : Sym → C → C
  σ_inv : ∀ t u, σ (inv t) (σ t u) = u

/-- Every ordered pair of controller vertices is joined by a reduced word of length exactly 5. -/
def Controller.ExactNB5 {C : Type} (K : Controller C) : Prop :=
  ∀ u v : C, ∃ t1 t2 t3 t4 t5 : Sym, Reduced t1 t2 t3 t4 t5 ∧
    K.σ t5 (K.σ t4 (K.σ t3 (K.σ t2 (K.σ t1 u)))) = v

/-! ## Route charts -/

/-- A route chart on `R^5` (condition (A.1) of arXiv:2606.15860, over a commutative ring). -/
structure Chart (R : Type) [CommRing R] where
  A : Sym → Matrix (Fin 5) (Fin 5) R
  b : Sym → Fin 5 → R
  A_inv : ∀ t, A (inv t) * A t = 1
  b_inv : ∀ t, b (inv t) = A (inv t) *ᵥ b t

namespace Chart

variable {R : Type} [CommRing R]

/-- The controllability matrix (A.2) of the word `t1 t2 t3 t4 t5`: its columns are
`A t5 A t4 A t3 A t2 b t1`, `A t5 A t4 A t3 b t2`, `A t5 A t4 b t3`, `A t5 b t4`, `b t5`. -/
def ctrl (c : Chart R) (t1 t2 t3 t4 t5 : Sym) : Matrix (Fin 5) (Fin 5) R :=
  Matrix.of fun i j =>
    (![c.A t5 *ᵥ (c.A t4 *ᵥ (c.A t3 *ᵥ (c.A t2 *ᵥ c.b t1))),
       c.A t5 *ᵥ (c.A t4 *ᵥ (c.A t3 *ᵥ c.b t2)),
       c.A t5 *ᵥ (c.A t4 *ᵥ c.b t3),
       c.A t5 *ᵥ c.b t4,
       c.b t5] j) i

/-- A chart is universal if the controllability matrix of every reduced word of length 5
has a right inverse. Over a field this is the nonsingularity of (A.2). -/
def Universal (c : Chart R) : Prop :=
  ∀ t1 t2 t3 t4 t5 : Sym, Reduced t1 t2 t3 t4 t5 →
    ∃ N : Matrix (Fin 5) (Fin 5) R, c.ctrl t1 t2 t3 t4 t5 * N = 1

/-- One step of the lift: `x ↦ A t *ᵥ x + l • b t`. -/
def step (c : Chart R) (t : Sym) (l : R) (x : Fin 5 → R) : Fin 5 → R :=
  c.A t *ᵥ x + l • c.b t

lemma ctrl_mulVec (c : Chart R) (t1 t2 t3 t4 t5 : Sym) (l : Fin 5 → R) :
    c.ctrl t1 t2 t3 t4 t5 *ᵥ l =
      l 0 • (c.A t5 *ᵥ (c.A t4 *ᵥ (c.A t3 *ᵥ (c.A t2 *ᵥ c.b t1)))) +
      l 1 • (c.A t5 *ᵥ (c.A t4 *ᵥ (c.A t3 *ᵥ c.b t2))) +
      l 2 • (c.A t5 *ᵥ (c.A t4 *ᵥ c.b t3)) +
      l 3 • (c.A t5 *ᵥ c.b t4) +
      l 4 • c.b t5 := by
  ext i
  simp [ctrl, Matrix.mulVec, dotProduct, Fin.sum_univ_five, mul_comm]

/-- Five steps along `t1 … t5` with scalars `l 0, …, l 4` end at
`A t5 A t4 A t3 A t2 A t1 x + M_w l`. -/
lemma five_steps (c : Chart R) (t1 t2 t3 t4 t5 : Sym) (x l : Fin 5 → R) :
    c.step t5 (l 4) (c.step t4 (l 3) (c.step t3 (l 2) (c.step t2 (l 1) (c.step t1 (l 0) x)))) =
      c.A t5 *ᵥ (c.A t4 *ᵥ (c.A t3 *ᵥ (c.A t2 *ᵥ (c.A t1 *ᵥ x)))) +
        c.ctrl t1 t2 t3 t4 t5 *ᵥ l := by
  rw [ctrl_mulVec]
  simp only [step, Matrix.mulVec_add, Matrix.mulVec_smul]
  abel

lemma step_inv (c : Chart R) (t : Sym) (l : R) (x : Fin 5 → R) :
    c.step (inv t) (-l) (c.step t l x) = x := by
  simp only [step, Matrix.mulVec_add, Matrix.mulVec_smul, Matrix.mulVec_mulVec, c.A_inv,
    Matrix.one_mulVec, ← c.b_inv, neg_smul]
  abel

end Chart

/-! ## The lift graph -/

variable {C R : Type} [CommRing R]

/-- The route-chart lift graph on `C × R^5`. -/
def liftGraph (K : Controller C) (c : Chart R) : SimpleGraph (C × (Fin 5 → R)) where
  Adj p q := p ≠ q ∧ ∃ (t : Sym) (l : R), q.1 = K.σ t p.1 ∧ q.2 = c.step t l p.2
  symm := ⟨by
    rintro p q ⟨hne, t, l, h1, h2⟩
    refine ⟨hne.symm, inv t, -l, ?_, ?_⟩
    · rw [h1, K.σ_inv]
    · rw [h2, c.step_inv]⟩
  loopless := ⟨fun _ h => h.1 rfl⟩

lemma liftGraph_adj (K : Controller C) (c : Chart R) (p q : C × (Fin 5 → R)) :
    (liftGraph K c).Adj p q ↔ p ≠ q ∧ ∃ (t : Sym) (l : R), q.1 = K.σ t p.1 ∧ q.2 = c.step t l p.2 :=
  Iff.rfl

/-- Every vertex of the lift graph has at most `4 |R|` neighbours. -/
theorem liftGraph_degree_le [Fintype C] [DecidableEq C] [Fintype R] [DecidableEq R]
    (K : Controller C) (c : Chart R) [DecidableRel (liftGraph K c).Adj]
    (p : C × (Fin 5 → R)) : (liftGraph K c).degree p ≤ 4 * Fintype.card R := by
  classical
  rw [← SimpleGraph.card_neighborFinset_eq_degree]
  have hsub : (liftGraph K c).neighborFinset p ⊆
      (Finset.univ : Finset (Sym × R)).image (fun tl => (K.σ tl.1 p.1, c.step tl.1 tl.2 p.2)) := by
    intro q hq
    rw [SimpleGraph.mem_neighborFinset, liftGraph_adj] at hq
    obtain ⟨-, t, l, h1, h2⟩ := hq
    exact Finset.mem_image.mpr ⟨(t, l), Finset.mem_univ _, Prod.ext h1.symm h2.symm⟩
  calc ((liftGraph K c).neighborFinset p).card
      ≤ ((Finset.univ : Finset (Sym × R)).image _).card := Finset.card_le_card hsub
    _ ≤ (Finset.univ : Finset (Sym × R)).card := Finset.card_image_le
    _ = 4 * Fintype.card R := by simp [Finset.card_univ, Fintype.card_prod]

/-- Appending a step that is either a stay or an edge. -/
lemma walk_snoc {V : Type} (G : SimpleGraph V) {a b c : V} {n : ℕ}
    (h : ∃ p : G.Walk a b, p.length ≤ n) (hbc : b = c ∨ G.Adj b c) :
    ∃ p : G.Walk a c, p.length ≤ n + 1 := by
  obtain ⟨p, hp⟩ := h
  rcases hbc with rfl | hadj
  · exact ⟨p, by omega⟩
  · exact ⟨p.concat hadj, by rw [SimpleGraph.Walk.length_concat]; omega⟩

lemma lift_step (K : Controller C) (c : Chart R) (t : Sym) (l : R) (p : C × (Fin 5 → R)) :
    p = (K.σ t p.1, c.step t l p.2) ∨ (liftGraph K c).Adj p (K.σ t p.1, c.step t l p.2) := by
  by_cases h : p = (K.σ t p.1, c.step t l p.2)
  · exact Or.inl h
  · exact Or.inr ((liftGraph_adj K c _ _).mpr ⟨h, t, l, rfl, rfl⟩)

/-- **Diameter.** If the controller is exact-NB-5 and the chart is universal, every two vertices
of the lift graph are joined by a walk of length at most 5. -/
theorem liftGraph_walk_le_five (K : Controller C) (hK : K.ExactNB5) (c : Chart R)
    (hc : c.Universal) (p q : C × (Fin 5 → R)) :
    ∃ w : (liftGraph K c).Walk p q, w.length ≤ 5 := by
  obtain ⟨t1, t2, t3, t4, t5, hred, hσ⟩ := hK p.1 q.1
  obtain ⟨N, hN⟩ := hc t1 t2 t3 t4 t5 hred
  set z : Fin 5 → R :=
    q.2 - c.A t5 *ᵥ (c.A t4 *ᵥ (c.A t3 *ᵥ (c.A t2 *ᵥ (c.A t1 *ᵥ p.2))))
  set l : Fin 5 → R := N *ᵥ z
  have hl : c.ctrl t1 t2 t3 t4 t5 *ᵥ l = z := by
    simp only [l, Matrix.mulVec_mulVec, hN, Matrix.one_mulVec]
  -- the six intermediate vertices
  set p1 : C × (Fin 5 → R) := (K.σ t1 p.1, c.step t1 (l 0) p.2)
  set p2 : C × (Fin 5 → R) := (K.σ t2 p1.1, c.step t2 (l 1) p1.2)
  set p3 : C × (Fin 5 → R) := (K.σ t3 p2.1, c.step t3 (l 2) p2.2)
  set p4 : C × (Fin 5 → R) := (K.σ t4 p3.1, c.step t4 (l 3) p3.2)
  set p5 : C × (Fin 5 → R) := (K.σ t5 p4.1, c.step t5 (l 4) p4.2)
  have h5 : p5 = q := by
    refine Prod.ext ?_ ?_
    · exact hσ
    · change c.step t5 (l 4) (c.step t4 (l 3) (c.step t3 (l 2) (c.step t2 (l 1)
          (c.step t1 (l 0) p.2)))) = q.2
      rw [Chart.five_steps, hl]
      simp [z]
  have w0 : ∃ w : (liftGraph K c).Walk p p, w.length ≤ 0 := ⟨SimpleGraph.Walk.nil, le_rfl⟩
  have w1 := walk_snoc _ w0 (lift_step K c t1 (l 0) p)
  have w2 := walk_snoc _ w1 (lift_step K c t2 (l 1) p1)
  have w3 := walk_snoc _ w2 (lift_step K c t3 (l 2) p2)
  have w4 := walk_snoc _ w3 (lift_step K c t4 (l 3) p3)
  have w5 := walk_snoc _ w4 (lift_step K c t5 (l 4) p4)
  obtain ⟨w, hw⟩ := w5
  exact ⟨w.copy rfl h5, by rw [SimpleGraph.Walk.length_copy]; omega⟩

end DDP
