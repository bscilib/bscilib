/-
Copyright (c) 2026 BSciLib contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: David J. Cox
-/
import Mathlib.Analysis.SpecialFunctions.Exp

/-!
# Assumption modules for discounting

Nothing in this file asserts that any organism discounts in any particular way.
Each declaration names a property that a discount function may or may not have,
so that theorems downstream can state exactly which properties they use. The
reasoning behind this arrangement is in `docs/assumptions.md`.

## Main declarations

* `BSciLib.DiscountWeights`: nonnegative delay weights
* `BSciLib.Stationary`: the delay-additive (memoryless) property
-/

namespace BSciLib

/-- The discounted value of amount `A` available after delay `D`, under a
discount function `d` mapping delays to weights.

This is the separable value form, in which amount and delay contribute
multiplicatively. Separability is itself an assumption, and it is false for
models in which delay interacts with magnitude. We have written it into this
definition rather than leaving it implicit, so that any theorem stated in terms
of `value` visibly inherits it. Models without separability should define their
own value function rather than an instance here. -/
def value (d : ℝ → ℝ) (A D : ℝ) : ℝ := A * d D

/-- Nonnegative weights: a discount function never assigns negative weight to a
delay.

Empirical standing: uncontroversial for the delay-discounting preparations this
library currently covers. Boundary condition worth noting: models that allow
negative value for delayed aversive outcomes carry the sign on the amount rather
than on the weight, and so still satisfy this. -/
class DiscountWeights (d : ℝ → ℝ) : Prop where
  /-- Weights are nonnegative at every delay. -/
  nonneg : ∀ D : ℝ, 0 ≤ d D

/-- Stationarity: the weight of a total delay factors into the weights of its
parts, so that `d (D + T) = d D * d T`.

Stated differently, the discount applied over an interval does not depend on
when that interval begins (i.e., the memoryless property). This is the
assumption that does the work in `no_preference_reversal_of_stationary`.
Exponential discounting satisfies it; hyperbolic discounting does not.

Empirical standing: routinely violated. Preference reversal under a common
front-end delay is among the better-replicated findings in the discounting
literature, and such a reversal is precisely a violation of this assumption. The
module exists so that results depending on stationarity are easy to identify,
rather than because the assumption is thought to hold generally. -/
class Stationary (d : ℝ → ℝ) : Prop where
  /-- Delay weights are multiplicative over addition of delays. -/
  add : ∀ D T : ℝ, d (D + T) = d D * d T

end BSciLib
