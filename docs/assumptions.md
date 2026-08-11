# The assumption policy

One commitment shapes the rest of the library, so it is worth stating plainly
and then explaining at some length.

BSciLib does not assert empirical claims. Every theorem is an implication: given
the assumption modules it names, the stated consequence follows.

## Why we work this way

Behavior science has no axioms, and writing some would be a mistake at this
stage. The field has spent decades working out which of its constructs earn
their keep, and freezing a set of primitives into a foundational layer now would
commit the library to answers the field has not reached. The history here is
instructive: response strength was once treated as a foundational term, and a
good deal of subsequent work went into disentangling what that commitment had
quietly assumed.

Fortunately, a checked library does not need axioms about organisms in order to
be useful. The question that comes up most often in quantitative behavior
analysis is rarely whether a given equation is true. More often it is what the
equation presupposes, and whether the published derivation carries those
presuppositions to the stated conclusion. That question is answerable by proof
checking, and it is the question this library is built to answer.

## How the policy is enforced

The mechanical parts are enforced by tooling, so that they do not depend on
anyone remembering them.

First, `axiom` declarations are confined to `BSciLib/Assumptions/`, and
`scripts/lint_axioms.py` fails continuous integration otherwise.

Second, `sorry` is not permitted anywhere in the library. Unfinished claims
belong in `cards/` as statement cards rather than as holes in a proof. The same
lint checks this.

Third, flagship theorems are checked for their axiom footprint by
`scripts/check_axiom_footprint.sh`, which runs `#print axioms` and fails if
anything appears beyond Lean's own `propext`, `Classical.choice`, and
`Quot.sound`.

Fourth, every assumption module carries a docstring stating its empirical
standing and known violations. No linter can check this one, so it is a review
requirement instead. `BSciLib.Stationary` shows the intended pattern: its
docstring says plainly that the assumption is routinely violated (i.e.,
preference reversal under a common front-end delay is among the
better-replicated findings in the discounting literature), and that the module
exists to make dependent results visible rather than because the assumption is
believed to hold.

## Three consequences worth spelling out

The first consequence is that nothing gets frozen. Adding an assumption module
costs nothing and commits the library to nothing, so a new account can be
represented without displacing an existing one.

The second consequence concerns theoretical disputes. A molar assumption module
and a molecular one sit in the same directory, and each theorem declares which
it consumes. No set of assumptions is privileged by the library's structure,
and there is correspondingly little for camps to fight over at the level of the
files themselves. We think this is a more durable arrangement than a stated
intention to be even-handed, since it does not depend on anyone's continued good
behavior.

The third consequence is that dependency facts become results in their own
right. A statement such as "Herrnstein's hyperbola requires constant total
behavior, and under generalized matching the consequent is no longer a
hyperbola" is something the library can establish mechanically, and it may be of
more interest to a theorist than the equation itself.

## On unused hypotheses

If a theorem's statement carries a hypothesis its proof never consumes, we treat
the statement as defective. The result is stronger than advertised, and the
extra hypothesis misleads readers about what the claim actually requires.

Card 0001 is the worked example. The familiar statement that exponential
discounting admits no preference reversal carries three hypotheses the proof
does not need, and removing them turned a claim about a functional form into a
claim about an invariance. That change appears to have experimental
consequences, which is the sort of return that makes the exercise worth the
trouble.

## Writing a new assumption module

```lean
/-- Name of the assumption: a one-line statement in prose.

A longer gloss, if the assumption has a standard name in the literature, or if
its usual informal phrasing differs from the formal one.

Empirical standing: what is actually known, stated plainly. "Routinely
violated" is a perfectly good answer when it is the true one. Known boundary
conditions: preparations, ranges, or species where the assumption is known to
fail. -/
class TheAssumption (M : Model) : Prop where
  /-- A doc-comment on the field as well. -/
  property : ...
```

The paragraph on empirical standing is the part that keeps a reader from
mistaking a module for a claim, and it is the first thing a reviewer will look
for. Writing "routinely violated" where that is accurate costs the library
nothing and tells the reader exactly what they need to know.
