/-
Copyright (c) 2026 BSciLib contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: David J. Cox
-/
import BSciLib.Discounting.Basic

/-!
# Preference reversal under a common front-end delay

This file contains flagship theorem #1 (see
`cards/0001-exponential-no-reversal.md`).

The result usually stated as "exponential discounting admits no preference
reversal" turns out not to require exponential discounting. It requires
`Stationary` and `DiscountWeights`, and nothing further: not continuity, not
monotonicity, not a positive discount rate, and not that the front-end delay `T`
is nonnegative. Stating the theorem at that level of generality is the point of
the exercise. `exp_no_preference_reversal` then follows in one line, and the
empirical question shifts from whether an organism discounts exponentially to
whether its discount function is stationary.

## Main results

* `BSciLib.no_preference_reversal_of_stationary`
* `BSciLib.exp_no_preference_reversal`
-/

namespace BSciLib

/-- No preference reversal under stationarity.

If the larger-later option `(A_l, D_l)` is not preferred to the smaller-sooner
option `(A_s, D_s)`, then adding a common front-end delay `T` to both cannot
make it preferred.

In words: a delay applied equally to both alternatives leaves the ordering
alone. The proof uses exactly two assumptions, `Stationary` and
`DiscountWeights`, and holds for every real `T` rather than only for
nonnegative ones. -/
theorem no_preference_reversal_of_stationary (d : ℝ → ℝ)
    [Stationary d] [DiscountWeights d] {A_s D_s A_l D_l : ℝ}
    (h : value d A_l D_l ≤ value d A_s D_s) (T : ℝ) :
    value d A_l (D_l + T) ≤ value d A_s (D_s + T) := by
  simp only [value, Stationary.add] at h ⊢
  calc A_l * (d D_l * d T)
      = A_l * d D_l * d T := by ring
    _ ≤ A_s * d D_s * d T := mul_le_mul_of_nonneg_right h (DiscountWeights.nonneg T)
    _ = A_s * (d D_s * d T) := by ring

/-- Exponential discounting admits no preference reversal.

A corollary of `no_preference_reversal_of_stationary`. The exponential form
enters only through its `Stationary` instance. -/
theorem exp_no_preference_reversal (k : ℝ) {A_s D_s A_l D_l : ℝ}
    (h : value (expDiscount k) A_l D_l ≤ value (expDiscount k) A_s D_s) (T : ℝ) :
    value (expDiscount k) A_l (D_l + T) ≤ value (expDiscount k) A_s (D_s + T) :=
  no_preference_reversal_of_stationary _ h T

end BSciLib
