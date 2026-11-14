import DDPGeneralQ.Checks
import Mathlib.Data.ZMod.Basic
import Mathlib.Algebra.Field.ZMod
import Mathlib.Tactic.DeriveFintype

/-!
# Code arithmetic for `ZMod p`, for the integers, and for GF(4) and GF(8)

* `natModOps p`: natural numbers with addition and multiplication modulo `p`,
  encoding `ZMod p` through `Nat.cast`.
* `intOps`: integer arithmetic, encoding any commutative ring through `Int.cast`.
* `GF4`, `GF8`: the fields with 4 and 8 elements, defined by addition and
  multiplication tables on `Fin 4` and `Fin 8` (polynomial bases with moduli
  `X^2 + X + 1` and `X^3 + X^2 + 1`; the element with index `Σ c_i 2^i` is
  `Σ c_i X^i`). Their commutative-ring axioms are checked by `decide`. Only
  the ring structure is used.
-/

namespace DDP

/-- Natural numbers with arithmetic modulo `p`. -/
def natModOps (p : ℕ) : CodeOps ℕ := ⟨fun x y => (x + y) % p, fun x y => (x * y) % p, 0, 1 % p⟩

lemma natModOps_hom (p : ℕ) : (natModOps p).Hom (fun n : ℕ => (n : ZMod p)) where
  map_add x y := by simp [natModOps, ZMod.natCast_mod]
  map_mul x y := by simp [natModOps, ZMod.natCast_mod]
  map_zero := by simp [natModOps]
  map_one := by simp [natModOps, ZMod.natCast_mod]

/-- Integer arithmetic. -/
def intOps : CodeOps ℤ := ⟨(· + ·), (· * ·), 0, 1⟩

lemma intOps_hom {R : Type} [CommRing R] : intOps.Hom (fun n : ℤ => (n : R)) where
  map_add x y := by simp [intOps]
  map_mul x y := by simp [intOps]
  map_zero := by simp [intOps]
  map_one := by simp [intOps]

/-! ## GF(4) -/

/-- The field with four elements, as a table on `Fin 4`. -/
structure GF4 where
  v : Fin 4
  deriving DecidableEq, Fintype

namespace GF4

def addTab : List (List ℕ) := [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]
def mulTab : List (List ℕ) := [[0, 0, 0, 0], [0, 1, 2, 3], [0, 2, 3, 1], [0, 3, 1, 2]]

def addN (x y : ℕ) : ℕ := ((addTab.getD (x % 4) []).getD (y % 4) 0) % 4
def mulN (x y : ℕ) : ℕ := ((mulTab.getD (x % 4) []).getD (y % 4) 0) % 4

/-- The element with index `n % 4`. -/
def ofNat (n : ℕ) : GF4 := ⟨⟨n % 4, Nat.mod_lt _ (by norm_num)⟩⟩

instance : Zero GF4 := ⟨ofNat 0⟩
instance : One GF4 := ⟨ofNat 1⟩
instance : Add GF4 := ⟨fun x y => ofNat (addN x.v y.v)⟩
instance : Mul GF4 := ⟨fun x y => ofNat (mulN x.v y.v)⟩
instance : Neg GF4 := ⟨fun x => x⟩

instance : CommRing GF4 where
  add := (· + ·)
  mul := (· * ·)
  zero := 0
  one := 1
  neg := Neg.neg
  nsmul := nsmulRec
  zsmul := zsmulRec
  add_assoc := by decide
  zero_add := by decide
  add_zero := by decide
  add_comm := by decide
  left_distrib := by decide
  right_distrib := by decide
  zero_mul := by decide
  mul_zero := by decide
  mul_assoc := by decide
  one_mul := by decide
  mul_one := by decide
  neg_add_cancel := by decide
  mul_comm := by decide

lemma card : Fintype.card GF4 = 4 := by decide

/-- Code arithmetic for GF(4): naturals read modulo 4. -/
def ops : CodeOps ℕ := ⟨addN, mulN, 0, 1⟩

lemma ops_hom : ops.Hom ofNat where
  map_add x y := by
    show ofNat (addN x y) = ofNat (addN (x % 4) (y % 4))
    simp [addN]
  map_mul x y := by
    show ofNat (mulN x y) = ofNat (mulN (x % 4) (y % 4))
    simp [mulN]
  map_zero := rfl
  map_one := rfl

end GF4

/-! ## GF(8) -/

/-- The field with eight elements, as a table on `Fin 8`. -/
structure GF8 where
  v : Fin 8
  deriving DecidableEq, Fintype

namespace GF8

def addTab : List (List ℕ) :=
  [[0, 1, 2, 3, 4, 5, 6, 7], [1, 0, 3, 2, 5, 4, 7, 6], [2, 3, 0, 1, 6, 7, 4, 5],
   [3, 2, 1, 0, 7, 6, 5, 4], [4, 5, 6, 7, 0, 1, 2, 3], [5, 4, 7, 6, 1, 0, 3, 2],
   [6, 7, 4, 5, 2, 3, 0, 1], [7, 6, 5, 4, 3, 2, 1, 0]]
def mulTab : List (List ℕ) :=
  [[0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 2, 3, 4, 5, 6, 7], [0, 2, 4, 6, 5, 7, 1, 3],
   [0, 3, 6, 5, 1, 2, 7, 4], [0, 4, 5, 1, 7, 3, 2, 6], [0, 5, 7, 2, 3, 6, 4, 1],
   [0, 6, 1, 7, 2, 4, 3, 5], [0, 7, 3, 4, 6, 1, 5, 2]]

def addN (x y : ℕ) : ℕ := ((addTab.getD (x % 8) []).getD (y % 8) 0) % 8
def mulN (x y : ℕ) : ℕ := ((mulTab.getD (x % 8) []).getD (y % 8) 0) % 8

/-- The element with index `n % 8`. -/
def ofNat (n : ℕ) : GF8 := ⟨⟨n % 8, Nat.mod_lt _ (by norm_num)⟩⟩

instance : Zero GF8 := ⟨ofNat 0⟩
instance : One GF8 := ⟨ofNat 1⟩
instance : Add GF8 := ⟨fun x y => ofNat (addN x.v y.v)⟩
instance : Mul GF8 := ⟨fun x y => ofNat (mulN x.v y.v)⟩
instance : Neg GF8 := ⟨fun x => x⟩

instance : CommRing GF8 where
  add := (· + ·)
  mul := (· * ·)
  zero := 0
  one := 1
  neg := Neg.neg
  nsmul := nsmulRec
  zsmul := zsmulRec
  add_assoc := by decide
  zero_add := by decide
  add_zero := by decide
  add_comm := by decide
  left_distrib := by decide
  right_distrib := by decide
  zero_mul := by decide
  mul_zero := by decide
  mul_assoc := by decide
  one_mul := by decide
  mul_one := by decide
  neg_add_cancel := by decide
  mul_comm := by decide

lemma card : Fintype.card GF8 = 8 := by decide

/-- Code arithmetic for GF(8): naturals read modulo 8. -/
def ops : CodeOps ℕ := ⟨addN, mulN, 0, 1⟩

lemma ops_hom : ops.Hom ofNat where
  map_add x y := by
    show ofNat (addN x y) = ofNat (addN (x % 8) (y % 8))
    simp [addN]
  map_mul x y := by
    show ofNat (mulN x y) = ofNat (mulN (x % 8) (y % 8))
    simp [mulN]
  map_zero := rfl
  map_one := rfl

end GF8

/-! ## From passing checks to `Good` -/

/-- A chart over `ZMod p` given by codes modulo `p`, with right-inverse certificates. -/
theorem good_of_natMod (p : ℕ) [NeZero p] (cc : CodeChart ℕ) (certs : List (List (List ℕ)))
    (hc : cc.checkB (natModOps p) = true) (hu : cc.univB (natModOps p) certs = true) : Good p :=
  ⟨ZMod p, inferInstance, inferInstance, ZMod.card p,
    cc.toChart (natModOps_hom p) (CodeChart.wf_of_checkB hc) (CodeChart.invOK_of_checkB hc),
    CodeChart.universal_of_univB (natModOps_hom p) hc hu⟩

theorem good_four (cc : CodeChart ℕ) (certs : List (List (List ℕ)))
    (hc : cc.checkB GF4.ops = true) (hu : cc.univB GF4.ops certs = true) : Good 4 :=
  ⟨GF4, inferInstance, inferInstance, GF4.card,
    cc.toChart GF4.ops_hom (CodeChart.wf_of_checkB hc) (CodeChart.invOK_of_checkB hc),
    CodeChart.universal_of_univB GF4.ops_hom hc hu⟩

theorem good_eight (cc : CodeChart ℕ) (certs : List (List (List ℕ)))
    (hc : cc.checkB GF8.ops = true) (hu : cc.univB GF8.ops certs = true) : Good 8 :=
  ⟨GF8, inferInstance, inferInstance, GF8.card,
    cc.toChart GF8.ops_hom (CodeChart.wf_of_checkB hc) (CodeChart.invOK_of_checkB hc),
    CodeChart.universal_of_univB GF8.ops_hom hc hu⟩

/-- An integer chart with adjugate certificates gives a universal chart over `ZMod p` for every
prime `p` dividing none of the certified determinants. -/
theorem good_of_intChart (p : ℕ) [hp : Fact p.Prime] (cc : CodeChart ℤ) (dets : List ℤ)
    (adjs : List (List (List ℤ))) (hc : cc.checkB intOps = true)
    (hu : cc.adjB intOps dets adjs = true)
    (hd : ∀ t1 t2 t3 t4 t5 : Sym, Reduced t1 t2 t3 t4 t5 →
      ¬ (p : ℤ) ∣ dets.getD (wordCode t1 t2 t3 t4 t5) 0) : Good p :=
  ⟨ZMod p, inferInstance, inferInstance, ZMod.card p,
    cc.toChart intOps_hom (CodeChart.wf_of_checkB hc) (CodeChart.invOK_of_checkB hc),
    CodeChart.universal_of_adjB intOps_hom hc hu fun t1 t2 t3 t4 t5 hr => by
      have h0 : ((dets.getD (wordCode t1 t2 t3 t4 t5) 0 : ℤ) : ZMod p) ≠ 0 := by
        rw [Ne, ZMod.intCast_zmod_eq_zero_iff_dvd]
        exact hd t1 t2 t3 t4 t5 hr
      exact @Ne.isUnit (ZMod p) _ _ h0⟩

end DDP
