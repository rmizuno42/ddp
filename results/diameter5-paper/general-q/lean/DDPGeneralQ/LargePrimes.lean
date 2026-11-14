import DDPGeneralQ.Charts.IntChart1
import DDPGeneralQ.Charts.IntChart2
import DDPGeneralQ.Charts.IntChart3
import DDPGeneralQ.Charts.IntChart4
import DDPGeneralQ.Charts.IntChart5
import DDPGeneralQ.Charts.IntChart6
import Mathlib.Data.List.Prime

/-!
# Every prime `p > 79` admits a universal chart over `ZMod p`

Each of the six integer charts comes with, for every reduced word, a
determinant `d_w` and an adjugate certificate. If `p` divides none of the
`d_w` of one chart, that chart reduced modulo `p` is universal
(`good_of_intChart`). The greatest common divisor `G` of the six products
`∏_w |d_w|` factors over the primes up to 79 (`G_eq`), so a prime `p > 79`
cannot divide all six products.
-/

namespace DDP

/-- The product of the absolute values of a list of integers. -/
def prodAbs (l : List ℤ) : ℕ := (l.map Int.natAbs).prod

lemma wordCode_lt (t1 t2 t3 t4 t5 : Sym) : wordCode t1 t2 t3 t4 t5 < 1024 := by
  unfold wordCode
  have := t1.isLt; have := t2.isLt; have := t3.isLt; have := t4.isLt; have := t5.isLt
  omega

/-- A prime dividing no certified determinant of an integer chart gives `Good p`. -/
theorem good_of_not_dvd_prodAbs (p : ℕ) (hp : p.Prime) (cc : CodeChart ℤ) (dets : List ℤ)
    (adjs : List (List (List ℤ))) (hc : cc.checkB intOps = true)
    (hu : cc.adjB intOps dets adjs = true) (hlen : dets.length = 1024)
    (hnd : ¬ p ∣ prodAbs dets) : Good p := by
  haveI := Fact.mk hp
  refine good_of_intChart p cc dets adjs hc hu ?_
  intro t1 t2 t3 t4 t5 _ hdvd
  apply hnd
  have hlt : wordCode t1 t2 t3 t4 t5 < dets.length := by rw [hlen]; exact wordCode_lt _ _ _ _ _
  have hmem : dets.getD (wordCode t1 t2 t3 t4 t5) 0 ∈ dets := by
    rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hlt, Option.getD_some]
    exact List.getElem_mem hlt
  have h1 : p ∣ (dets.getD (wordCode t1 t2 t3 t4 t5) 0).natAbs := Int.natCast_dvd.mp hdvd
  exact h1.trans (List.dvd_prod (List.mem_map_of_mem hmem))

/-- The greatest common divisor of the six products of certified determinants. -/
def G : ℕ :=
  Nat.gcd (prodAbs IntChart1.dets) (Nat.gcd (prodAbs IntChart2.dets)
    (Nat.gcd (prodAbs IntChart3.dets) (Nat.gcd (prodAbs IntChart4.dets)
      (Nat.gcd (prodAbs IntChart5.dets) (prodAbs IntChart6.dets)))))

/-- The prime factorization of `G` (computed by `scripts/gen_lean_data.py`). -/
def gFactors : List (ℕ × ℕ) :=
  [(2, 338), (3, 146), (5, 74), (7, 34), (11, 24), (13, 22), (17, 10), (19, 12), (23, 10),
   (29, 2), (31, 2), (37, 4), (41, 2), (47, 2), (53, 2), (59, 4), (61, 2), (67, 2), (71, 2),
   (73, 2), (79, 4)]

theorem G_eq : G = (gFactors.map fun qe => qe.1 ^ qe.2).prod := by decide +kernel

lemma gFactors_small : ∀ qe ∈ gFactors, 0 < qe.1 ∧ qe.1 ≤ 79 := by decide

lemma not_dvd_G {p : ℕ} (hp : p.Prime) (h : 79 < p) : ¬ p ∣ G := by
  rw [G_eq]
  intro hd
  obtain ⟨a, ha, hpa⟩ := (Prime.dvd_prod_iff hp.prime).mp hd
  obtain ⟨qe, hqe, rfl⟩ := List.mem_map.mp ha
  have hq : p ∣ qe.1 := hp.dvd_of_dvd_pow hpa
  have hs := gFactors_small qe hqe
  have := Nat.le_of_dvd hs.1 hq
  omega

/-- Every prime `p > 79` admits a universal chart over `ZMod p`. -/
theorem good_large_prime (p : ℕ) (hp : p.Prime) (h : 79 < p) : Good p := by
  by_cases h1 : p ∣ prodAbs IntChart1.dets
  swap
  · exact good_of_not_dvd_prodAbs p hp _ _ _ IntChart1.check IntChart1.adj IntChart1.dets_length h1
  by_cases h2 : p ∣ prodAbs IntChart2.dets
  swap
  · exact good_of_not_dvd_prodAbs p hp _ _ _ IntChart2.check IntChart2.adj IntChart2.dets_length h2
  by_cases h3 : p ∣ prodAbs IntChart3.dets
  swap
  · exact good_of_not_dvd_prodAbs p hp _ _ _ IntChart3.check IntChart3.adj IntChart3.dets_length h3
  by_cases h4 : p ∣ prodAbs IntChart4.dets
  swap
  · exact good_of_not_dvd_prodAbs p hp _ _ _ IntChart4.check IntChart4.adj IntChart4.dets_length h4
  by_cases h5 : p ∣ prodAbs IntChart5.dets
  swap
  · exact good_of_not_dvd_prodAbs p hp _ _ _ IntChart5.check IntChart5.adj IntChart5.dets_length h5
  by_cases h6 : p ∣ prodAbs IntChart6.dets
  swap
  · exact good_of_not_dvd_prodAbs p hp _ _ _ IntChart6.check IntChart6.adj IntChart6.dets_length h6
  -- Unfold `G` first so that the divisibility statement matches syntactically; otherwise
  -- elaboration may try to evaluate the large products.
  have hG : p ∣ G := by
    unfold G
    exact Nat.dvd_gcd h1 (Nat.dvd_gcd h2 (Nat.dvd_gcd h3 (Nat.dvd_gcd h4 (Nat.dvd_gcd h5 h6))))
  exact absurd hG (not_dvd_G hp h)

end DDP
