---
title: Exponential discounting admits no preference reversal under a common front-end delay
status: formalized
assumptions:
  - Value is separable in amount and delay (value A D = A * d D)
  - The discount function is stationary, so that d (D + T) = d D * d T
  - Discount weights are nonnegative
source: A standard result in intertemporal choice; see Mazur (1987) for the contrasting hyperbolic case. Catalog entry pending.
statement: If the larger-later option is not preferred to the smaller-sooner option, then adding a common delay T to both cannot make it preferred.
lean_decl: BSciLib.exp_no_preference_reversal
---

## Why this is card 0001

This is close to the easiest true thing in the domain, which makes it a good
first formalization. It exercises the whole pipeline (i.e., an assumption
module, a theorem, the axiom-footprint check, and continuous integration) while
the mathematics stays out of the way.

## What formalizing it changed

The claim is usually stated as a fact about exponential discounting. Once the
hypotheses were written out explicitly, the exponential form turned out to be
unnecessary. The proof uses stationarity and nonnegative weights, and it uses
nothing else. Continuity, monotonicity, and a positive discount rate are all
unused, as is the usual restriction to nonnegative front-end delays T.

The library therefore states the general result as
`BSciLib.no_preference_reversal_of_stationary`, with
`BSciLib.exp_no_preference_reversal` following in one line.

That reframing may have some experimental value. Asking whether exponential
discounting describes a given organism is a question about a functional form,
and it is answered by fitting curves. Asking whether that organism's discount
function is stationary is a question about an invariance, and it is answered by
a front-end delay manipulation. In turn, the second question appears cheaper to
ask and sits closer to the assumption doing the work in the derivation. The
library produced that observation more or less mechanically, by declining to let
an unused hypothesis remain in the statement.

## Follow-ups

Card 0002 takes up the contrasting case, in which hyperbolic discounting
violates stationarity and reversal follows.

One further question seems worth pursuing. Is stationarity together with
continuity enough to force the exponential form? This is the Cauchy functional
equation, and Mathlib may already have the pieces needed to answer it. A
converse of that kind would be a genuinely interesting entry, since it would
say how much of the exponential model is doing independent work.
