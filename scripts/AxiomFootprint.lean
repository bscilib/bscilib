/-
Copyright (c) 2026 BSciLib contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: David J. Cox
-/
import BSciLib

/-!
# Axiom footprint of the flagship results

CI runs this file with `lake env lean` and fails the build if the output
mentions any axiom outside Lean's three standard ones (`propext`,
`Classical.choice`, `Quot.sound`). See `scripts/check_axiom_footprint.sh`.

Every flagship theorem gets a line here. The output is also the honest answer
to "what does this result depend on," which is the question the library exists
to answer.
-/

-- Flagship #1: no preference reversal under stationarity, and its corollary.
#print axioms BSciLib.no_preference_reversal_of_stationary
#print axioms BSciLib.exp_no_preference_reversal
