import DDPGeneralQ.Codes
import DDPGeneralQ.Good

/-!
# Boolean checks and what they prove

Each finite fact is reduced to a Boolean function on code data, evaluated by
the kernel (`decide +kernel`). The lemmas in this file state what a passing
check proves:

* `CodeChart.checkB`: the codes are well formed and satisfy the inverse
  relations (A.1), so they define a chart.
* `CodeChart.univB`: for every reduced word, the supplied code matrix is a
  right inverse of the code controllability matrix; the chart is universal.
* `CodeChart.adjB`: for every reduced word, the code controllability matrix
  times the supplied matrix is `d • 1` for a supplied code `d` (an adjugate
  certificate).
* `ctrlB`: for every ordered pair of controller vertices, the supplied word
  is reduced and leads from the first vertex to the second.
-/

open Matrix

namespace DDP

/-- Boolean version of `Reduced`. -/
def reducedB (t1 t2 t3 t4 t5 : Sym) : Bool :=
  t2 != inv t1 && t3 != inv t2 && t4 != inv t3 && t5 != inv t4

lemma reduced_of_reducedB {t1 t2 t3 t4 t5 : Sym} (h : reducedB t1 t2 t3 t4 t5 = true) :
    Reduced t1 t2 t3 t4 t5 := by
  simpa [reducedB, Reduced, and_assoc] using h

lemma reducedB_of_reduced {t1 t2 t3 t4 t5 : Sym} (h : Reduced t1 t2 t3 t4 t5) :
    reducedB t1 t2 t3 t4 t5 = true := by
  simpa [reducedB, Reduced, and_assoc] using h

/-- The index of a word in the certificate lists: `t1 + 4 t2 + 16 t3 + 64 t4 + 256 t5`. -/
def wordCode (t1 t2 t3 t4 t5 : Sym) : ℕ :=
  t1.val + 4 * t2.val + 16 * t3.val + 64 * t4.val + 256 * t5.val

/-- A Boolean predicate holds for all words of length 5. -/
def allWords (f : Sym → Sym → Sym → Sym → Sym → Bool) : Bool :=
  (List.finRange 4).all fun t1 => (List.finRange 4).all fun t2 => (List.finRange 4).all fun t3 =>
    (List.finRange 4).all fun t4 => (List.finRange 4).all fun t5 => f t1 t2 t3 t4 t5

lemma allWords_spec {f : Sym → Sym → Sym → Sym → Sym → Bool} (h : allWords f = true)
    (t1 t2 t3 t4 t5 : Sym) : f t1 t2 t3 t4 t5 = true := by
  simp only [allWords, List.all_eq_true, List.mem_finRange, forall_const] at h
  exact h t1 t2 t3 t4 t5

/-- Boolean version of `WF5`. -/
def wf5B {K : Type} (M : List (List K)) : Bool := M.length == 5 && M.all fun r => r.length == 5

lemma wf5_of_wf5B {K : Type} {M : List (List K)} (h : wf5B M = true) : WF5 M := by
  simp only [wf5B, Bool.and_eq_true, beq_iff_eq, List.all_eq_true] at h
  exact ⟨h.1, h.2⟩

lemma wf5_ofCols {K : Type} (o : CodeOps K) {cs : List (List K)} (h : cs.length = 5) :
    WF5 (o.ofCols cs) := by
  refine ⟨by simp [CodeOps.ofCols], fun row hrow => ?_⟩
  simp only [CodeOps.ofCols, List.mem_map, List.mem_range] at hrow
  obtain ⟨i, -, rfl⟩ := hrow
  simp [h]

namespace CodeChart

variable {K R : Type} [CommRing R] [DecidableEq K] (o : CodeOps K) (cc : CodeChart K)

/-- The codes are well formed and satisfy the inverse relations (A.1). -/
def checkB : Bool :=
  (List.finRange 4).all fun t => wf5B (cc.Am t) && (cc.bv t).length == 5 &&
    decide (o.mm (cc.Am (inv t)) (cc.Am t) = o.diag o.one) &&
    decide (cc.bv (inv t) = o.mv (cc.Am (inv t)) (cc.bv t))

variable {o cc}

lemma wf_of_checkB (h : cc.checkB o = true) : cc.WF := by
  intro t
  simp only [checkB, List.all_eq_true, List.mem_finRange, forall_const, Bool.and_eq_true,
    beq_iff_eq, decide_eq_true_eq] at h
  exact ⟨wf5_of_wf5B (h t).1.1.1, (h t).1.1.2⟩

lemma invOK_of_checkB (h : cc.checkB o = true) : cc.InvOK o := by
  intro t
  simp only [checkB, List.all_eq_true, List.mem_finRange, forall_const, Bool.and_eq_true,
    beq_iff_eq, decide_eq_true_eq] at h
  exact ⟨(h t).1.2, (h t).2⟩

lemma ctrl_wf (t1 t2 t3 t4 t5 : Sym) : WF5 (cc.ctrl o t1 t2 t3 t4 t5) :=
  wf5_ofCols o rfl

variable (o cc)

/-- For every reduced word, `certs[code]` is a right inverse of the code controllability matrix. -/
def univB (certs : List (List (List K))) : Bool :=
  allWords fun t1 t2 t3 t4 t5 => !(reducedB t1 t2 t3 t4 t5) ||
    (wf5B (certs.getD (wordCode t1 t2 t3 t4 t5) []) &&
      decide (o.mm (cc.ctrl o t1 t2 t3 t4 t5) (certs.getD (wordCode t1 t2 t3 t4 t5) []) =
        o.diag o.one))

/-- For every reduced word, the code controllability matrix times `adjs[code]` is
`dets[code]` times the identity. -/
def adjB (dets : List K) (adjs : List (List (List K))) : Bool :=
  allWords fun t1 t2 t3 t4 t5 => !(reducedB t1 t2 t3 t4 t5) ||
    (wf5B (adjs.getD (wordCode t1 t2 t3 t4 t5) []) &&
      decide (o.mm (cc.ctrl o t1 t2 t3 t4 t5) (adjs.getD (wordCode t1 t2 t3 t4 t5) []) =
        o.diag (dets.getD (wordCode t1 t2 t3 t4 t5) o.zero)))

variable {o cc}

theorem universal_of_univB {e : K → R} (h : o.Hom e) (hc : cc.checkB o = true)
    {certs : List (List (List K))} (hu : cc.univB o certs = true) :
    (cc.toChart h (wf_of_checkB hc) (invOK_of_checkB hc)).Universal := by
  intro t1 t2 t3 t4 t5 hr
  have hw := allWords_spec hu t1 t2 t3 t4 t5
  simp only [reducedB_of_reduced hr, Bool.not_true, Bool.false_or, Bool.and_eq_true,
    decide_eq_true_eq] at hw
  obtain ⟨hwf, heq⟩ := hw
  refine ⟨o.toMat e (certs.getD (wordCode t1 t2 t3 t4 t5) []), ?_⟩
  rw [toChart_ctrl, ← CodeOps.mm_hom h (ctrl_wf _ _ _ _ _) (wf5_of_wf5B hwf), heq,
    CodeOps.diag_hom h, h.map_one, one_smul]

theorem ctrl_mul_adj {e : K → R} (h : o.Hom e) (hc : cc.checkB o = true)
    {dets : List K} {adjs : List (List (List K))} (hu : cc.adjB o dets adjs = true)
    {t1 t2 t3 t4 t5 : Sym} (hr : Reduced t1 t2 t3 t4 t5) :
    (cc.toChart h (wf_of_checkB hc) (invOK_of_checkB hc)).ctrl t1 t2 t3 t4 t5 *
        o.toMat e (adjs.getD (wordCode t1 t2 t3 t4 t5) []) =
      e (dets.getD (wordCode t1 t2 t3 t4 t5) o.zero) • (1 : Matrix (Fin 5) (Fin 5) R) := by
  have hw := allWords_spec hu t1 t2 t3 t4 t5
  simp only [reducedB_of_reduced hr, Bool.not_true, Bool.false_or, Bool.and_eq_true,
    decide_eq_true_eq] at hw
  obtain ⟨hwf, heq⟩ := hw
  rw [toChart_ctrl, ← CodeOps.mm_hom h (ctrl_wf _ _ _ _ _) (wf5_of_wf5B hwf), heq,
    CodeOps.diag_hom h]

/-- An adjugate certificate whose determinant codes map to units gives a universal chart. -/
theorem universal_of_adjB {e : K → R} (h : o.Hom e) (hc : cc.checkB o = true)
    {dets : List K} {adjs : List (List (List K))} (hu : cc.adjB o dets adjs = true)
    (hd : ∀ t1 t2 t3 t4 t5 : Sym, Reduced t1 t2 t3 t4 t5 →
      IsUnit (e (dets.getD (wordCode t1 t2 t3 t4 t5) o.zero))) :
    (cc.toChart h (wf_of_checkB hc) (invOK_of_checkB hc)).Universal := by
  intro t1 t2 t3 t4 t5 hr
  obtain ⟨u, hu'⟩ := hd t1 t2 t3 t4 t5 hr
  refine ⟨(↑u⁻¹ : R) • o.toMat e (adjs.getD (wordCode t1 t2 t3 t4 t5) []), ?_⟩
  rw [Matrix.mul_smul, ctrl_mul_adj h hc hu hr, ← hu', smul_smul, Units.inv_mul, one_smul]

end CodeChart

/-! ## The controller check -/

/-- The symbol at position `i` (from 0) of a word code. -/
def digit (c i : ℕ) : Sym := ⟨(c / 4 ^ i) % 4, Nat.mod_lt _ (by norm_num)⟩

/-- For every ordered pair `(u, v)` of controller vertices, the word with code `cert u v` is
reduced and leads from `u` to `v`. -/
def ctrlB {n : ℕ} (σ : Sym → Fin n → Fin n) (cert : ℕ → ℕ → ℕ) : Bool :=
  (List.finRange n).all fun u => (List.finRange n).all fun v =>
    reducedB (digit (cert u v) 0) (digit (cert u v) 1) (digit (cert u v) 2) (digit (cert u v) 3)
        (digit (cert u v) 4) &&
      σ (digit (cert u v) 4) (σ (digit (cert u v) 3) (σ (digit (cert u v) 2)
        (σ (digit (cert u v) 1) (σ (digit (cert u v) 0) u)))) == v

theorem exactNB5_of_ctrlB {n : ℕ} (K : Controller (Fin n)) {cert : ℕ → ℕ → ℕ}
    (h : ctrlB K.σ cert = true) : K.ExactNB5 := by
  intro u v
  simp only [ctrlB, List.all_eq_true, List.mem_finRange, forall_const, Bool.and_eq_true,
    beq_iff_eq] at h
  obtain ⟨hr, hv⟩ := h u v
  exact ⟨_, _, _, _, _, reduced_of_reducedB hr, hv⟩

end DDP
