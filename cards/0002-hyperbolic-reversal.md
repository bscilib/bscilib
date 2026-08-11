---
title: Hyperbolic discounting produces preference reversal, constructively
status: accepted
assumptions:
  - Value is separable in amount and delay
  - Discounting is hyperbolic (Mazur) with rate k > 0
  - Smaller-sooner is strictly preferred at zero front-end delay
source: Mazur, J. E. (1987). An adjusting procedure for studying delayed reinforcement. Catalog entry pending.
statement: Given A_s < A_l, D_s < D_l, and strict preference for the smaller-sooner option at T = 0, there exists a front-end delay T at which preference reverses; exhibit it explicitly.
blocked_on: none
---

## Why this one is interesting

Card 0001 shows that stationarity rules out preference reversal. This card takes
up the complementary case. The discount function most often used to describe
organisms is not stationary, and its failure of stationarity is what the
reversal phenomenon amounts to.

Formalizing it has some content that the informal statement hides. Lean will not
accept an appeal to the limiting behavior of the value ratio as T grows without
bound unless the witness is actually produced. Solving

    A_s * (1 + k * (D_l + T)) = A_l * (1 + k * (D_s + T))

for T gives the crossover point in closed form, and the theorem should return
that T and prove the strict inequality beyond it. As it happens, the exact
crossover delay is more useful to an experimenter than the bare existence claim,
since it is the quantity around which a session would be designed.

## Suggested shape

Two declarations, in order of difficulty. The first is
`theorem hyp_not_stationary (k : ℝ) (hk : 0 < k) : ¬ Stationary (hypDiscount k)`,
which follows from an explicit counterexample and is the cheaper half. The
second is `theorem hyp_preference_reversal`, the constructive statement given
above.

`BSciLib.hypDiscount` is already defined in `BSciLib/Discounting/Basic.lean`
with no `Stationary` instance, so the first declaration has somewhere to land.

## Pairs with

`python/tests/test_metamorphic.py::test_mr2_reversal_exists_hyperbolic`, which
asserts the same thing by search rather than by proof.
