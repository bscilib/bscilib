/-
Copyright (c) 2026 BSciLib contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: David J. Cox
-/
import BSciLib.Assumptions.Discounting

/-!
# Discount functions

Concrete discount functions. Each is a *definition* together with the
assumption instances it satisfies; theorems about them live elsewhere.

## Main declarations

* `BSciLib.expDiscount`: exponential discounting, `d D = exp (-k * D)`
* `BSciLib.hypDiscount`: hyperbolic discounting (Mazur), `d D = 1 / (1 + k * D)`
-/

namespace BSciLib

open Real

/-- Exponential discounting: `d D = exp (-k * D)` for discount rate `k`.

Source: standard in the intertemporal-choice literature; the normative form
under constant per-unit-time discounting. -/
noncomputable def expDiscount (k : ℝ) : ℝ → ℝ := fun D => exp (-k * D)

instance (k : ℝ) : DiscountWeights (expDiscount k) where
  nonneg _ := exp_nonneg _

instance (k : ℝ) : Stationary (expDiscount k) where
  add D T := by
    simp only [expDiscount, ← exp_add]
    congr 1
    ring

/-- Hyperbolic discounting (Mazur 1987): `d D = 1 / (1 + k * D)`.

Source: catalog entry pending; Mazur, J. E. (1987), *An adjusting procedure for
studying delayed reinforcement*.

No `Stationary` instance is provided here, and for `k ≠ 0` none exists. That
failure is the content of flagship theorem #2 (see
`cards/0002-hyperbolic-reversal.md`), and it is why hyperbolic discounting
predicts preference reversal where exponential discounting does not. -/
noncomputable def hypDiscount (k : ℝ) : ℝ → ℝ := fun D => 1 / (1 + k * D)

end BSciLib
