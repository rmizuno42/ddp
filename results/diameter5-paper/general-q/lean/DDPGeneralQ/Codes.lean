import DDPGeneralQ.Basic

/-!
# List arithmetic on codes, and its agreement with matrices

The finite checks are run on *codes*: elements of a type `K` (natural numbers
modulo `p`, integers, or the elements of a small field) with explicit addition
and multiplication, arranged in lists. An encoding `e : K → R` that respects
the code operations turns code lists into matrices and vectors over `R`.

The lemmas here show, once and for all, that list products of well-formed
5 × 5 code matrices encode the corresponding products over `R`. A check that
`M_w * N = 1` on codes therefore proves the same identity over `R`.
-/

open Matrix

namespace DDP

/-- Arithmetic on codes. -/
structure CodeOps (K : Type) where
  add : K → K → K
  mul : K → K → K
  zero : K
  one : K

variable {K R : Type} [CommRing R]

/-- `e` carries the code operations to the ring operations of `R`. -/
structure CodeOps.Hom (o : CodeOps K) (e : K → R) : Prop where
  map_add : ∀ x y, e (o.add x y) = e x + e y
  map_mul : ∀ x y, e (o.mul x y) = e x * e y
  map_zero : e o.zero = 0
  map_one : e o.one = 1

namespace CodeOps

variable (o : CodeOps K)

/-- Dot product of two code lists. -/
def dot : List K → List K → K
  | x :: xs, y :: ys => o.add (o.mul x y) (dot xs ys)
  | _, _ => o.zero

/-- Matrix–vector product: the dot product of every row with `v`. -/
def mv (M : List (List K)) (v : List K) : List K := M.map fun row => o.dot row v

/-- Column `j` of a code matrix. -/
def col (N : List (List K)) (j : ℕ) : List K := N.map fun row => row.getD j o.zero

/-- Matrix product of 5 × 5 code matrices. -/
def mm (M N : List (List K)) : List (List K) :=
  M.map fun row => (List.range 5).map fun j => o.dot row (o.col N j)

/-- The 5 × 5 code matrix with `d` on the diagonal and `zero` elsewhere. -/
def diag (d : K) : List (List K) :=
  (List.range 5).map fun i => (List.range 5).map fun j => if i = j then d else o.zero

/-- The code matrix whose columns are the given lists. -/
def ofCols (cs : List (List K)) : List (List K) :=
  (List.range 5).map fun i => cs.map fun c => c.getD i o.zero

/-- The matrix over `R` encoded by a code matrix. -/
def toMat (e : K → R) (M : List (List K)) : Matrix (Fin 5) (Fin 5) R :=
  Matrix.of fun i j => e ((M.getD i []).getD j o.zero)

/-- The vector over `R` encoded by a code list. -/
def toVec (e : K → R) (v : List K) : Fin 5 → R := fun i => e (v.getD i o.zero)

end CodeOps

/-- A code matrix with five rows of length five. -/
def WF5 {K : Type} (M : List (List K)) : Prop := M.length = 5 ∧ ∀ row ∈ M, row.length = 5

lemma list_five {α : Type} {l : List α} (h : l.length = 5) :
    ∃ a b c d f : α, l = [a, b, c, d, f] := by
  rcases l with _ | ⟨a, _ | ⟨b, _ | ⟨c, _ | ⟨d, _ | ⟨f, _ | ⟨g, l⟩⟩⟩⟩⟩⟩ <;> simp at h
  exact ⟨a, b, c, d, f, rfl⟩

namespace CodeOps

variable {o : CodeOps K} {e : K → R}

lemma dot_hom (h : o.Hom e) {r v : List K} (hr : r.length = 5) (hv : v.length = 5) :
    e (o.dot r v) = ∑ k : Fin 5, e (r.getD k o.zero) * e (v.getD k o.zero) := by
  obtain ⟨r0, r1, r2, r3, r4, rfl⟩ := list_five hr
  obtain ⟨v0, v1, v2, v3, v4, rfl⟩ := list_five hv
  simp [dot, h.map_add, h.map_mul, h.map_zero, Fin.sum_univ_five, add_assoc]

lemma mv_length (M : List (List K)) (v : List K) : (o.mv M v).length = M.length := by
  simp [mv]

lemma mv_hom (h : o.Hom e) {M : List (List K)} {v : List K} (hM : WF5 M) (hv : v.length = 5) :
    o.toVec e (o.mv M v) = o.toMat e M *ᵥ o.toVec e v := by
  obtain ⟨hlen, hrows⟩ := hM
  obtain ⟨r0, r1, r2, r3, r4, rfl⟩ := list_five hlen
  simp only [List.mem_cons, List.not_mem_nil, or_false, forall_eq_or_imp, forall_eq] at hrows
  obtain ⟨h0, h1, h2, h3, h4⟩ := hrows
  funext i
  fin_cases i <;>
    simp [toVec, toMat, mv, Matrix.mulVec, dotProduct, dot_hom h h0 hv, dot_hom h h1 hv,
      dot_hom h h2 hv, dot_hom h h3 hv, dot_hom h h4 hv]

lemma col_length (N : List (List K)) (j : ℕ) : (o.col N j).length = N.length := by
  simp [col]

lemma mm_hom (h : o.Hom e) {M N : List (List K)} (hM : WF5 M) (hN : WF5 N) :
    o.toMat e (o.mm M N) = o.toMat e M * o.toMat e N := by
  obtain ⟨hlen, hrows⟩ := hM
  obtain ⟨r0, r1, r2, r3, r4, rfl⟩ := list_five hlen
  simp only [List.mem_cons, List.not_mem_nil, or_false, forall_eq_or_imp, forall_eq] at hrows
  obtain ⟨h0, h1, h2, h3, h4⟩ := hrows
  obtain ⟨hNlen, hNrows⟩ := hN
  obtain ⟨n0, n1, n2, n3, n4, rfl⟩ := list_five hNlen
  simp only [List.mem_cons, List.not_mem_nil, or_false, forall_eq_or_imp, forall_eq] at hNrows
  obtain ⟨g0, g1, g2, g3, g4⟩ := hNrows
  have hc : ∀ j, (o.col [n0, n1, n2, n3, n4] j).length = 5 := fun j => by simp [col]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [toMat, mm, Matrix.mul_apply, dot_hom h h0 (hc _), dot_hom h h1 (hc _), dot_hom h h2 (hc _),
      dot_hom h h3 (hc _), dot_hom h h4 (hc _), Fin.sum_univ_five] <;> simp [col]

lemma diag_hom (h : o.Hom e) (d : K) : o.toMat e (o.diag d) = e d • (1 : Matrix (Fin 5) (Fin 5) R) := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [toMat, diag, h.map_zero]

lemma ofCols_hom {c1 c2 c3 c4 c5 : List K} :
    o.toMat e (o.ofCols [c1, c2, c3, c4, c5]) =
      Matrix.of fun i j => (![o.toVec e c1, o.toVec e c2, o.toVec e c3, o.toVec e c4,
        o.toVec e c5] j) i := by
  ext i j
  fin_cases i <;> fin_cases j <;> rfl

end CodeOps

/-! ## Charts given by codes -/

/-- Chart data as codes: four code matrices and four code vectors, indexed by the symbol. -/
structure CodeChart (K : Type) where
  A : List (List (List K))
  b : List (List K)

namespace CodeChart

variable (o : CodeOps K) (cc : CodeChart K)

/-- The code matrix of symbol `t`. -/
def Am (t : Sym) : List (List K) := cc.A.getD t []

/-- The code vector of symbol `t`. -/
def bv (t : Sym) : List K := cc.b.getD t []

/-- The code controllability matrix of the word `t1 … t5` (its columns as in (A.2)). -/
def ctrl (t1 t2 t3 t4 t5 : Sym) : List (List K) :=
  o.ofCols
    [o.mv (cc.Am t5) (o.mv (cc.Am t4) (o.mv (cc.Am t3) (o.mv (cc.Am t2) (cc.bv t1)))),
     o.mv (cc.Am t5) (o.mv (cc.Am t4) (o.mv (cc.Am t3) (cc.bv t2))),
     o.mv (cc.Am t5) (o.mv (cc.Am t4) (cc.bv t3)),
     o.mv (cc.Am t5) (cc.bv t4),
     cc.bv t5]

/-- Well-formedness of the chart codes: every matrix is 5 × 5 and every vector has length 5. -/
def WF : Prop := ∀ t : Sym, WF5 (cc.Am t) ∧ (cc.bv t).length = 5

/-- The inverse relations (A.1) on codes. -/
def InvOK : Prop :=
  ∀ t : Sym, o.mm (cc.Am (inv t)) (cc.Am t) = o.diag o.one ∧
    cc.bv (inv t) = o.mv (cc.Am (inv t)) (cc.bv t)

variable {o cc}

/-- The chart over `R` encoded by chart codes satisfying the inverse relations. -/
def toChart {e : K → R} (h : o.Hom e) (hwf : cc.WF) (hinv : cc.InvOK o) : Chart R where
  A t := o.toMat e (cc.Am t)
  b t := o.toVec e (cc.bv t)
  A_inv t := by
    rw [← CodeOps.mm_hom h (hwf _).1 (hwf _).1, (hinv t).1, CodeOps.diag_hom h, h.map_one, one_smul]
  b_inv t := by
    rw [(hinv t).2, CodeOps.mv_hom h (hwf _).1 (hwf _).2]

lemma toChart_ctrl {e : K → R} (h : o.Hom e) (hwf : cc.WF) (hinv : cc.InvOK o)
    (t1 t2 t3 t4 t5 : Sym) :
    (cc.toChart h hwf hinv).ctrl t1 t2 t3 t4 t5 = o.toMat e (cc.ctrl o t1 t2 t3 t4 t5) := by
  have hl : ∀ (t : Sym) (v : List K), (o.mv (cc.Am t) v).length = 5 := fun t v => by
    rw [CodeOps.mv_length]; exact (hwf t).1.1
  have hv1 : ∀ (t t' : Sym) (v : List K), o.toVec e (o.mv (cc.Am t) (o.mv (cc.Am t') v)) =
      o.toMat e (cc.Am t) *ᵥ o.toVec e (o.mv (cc.Am t') v) :=
    fun t t' v => CodeOps.mv_hom h (hwf t).1 (hl t' v)
  have hv2 : ∀ (t s : Sym), o.toVec e (o.mv (cc.Am t) (cc.bv s)) =
      o.toMat e (cc.Am t) *ᵥ o.toVec e (cc.bv s) :=
    fun t s => CodeOps.mv_hom h (hwf t).1 (hwf s).2
  rw [ctrl, CodeOps.ofCols_hom]
  simp only [hv1, hv2]
  rfl

end CodeChart

end DDP
