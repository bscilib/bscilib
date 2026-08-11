# Statement cards

A statement card describes a claim that you think belongs in BSciLib, written in
prose, with its assumptions named and its source cited. Writing one requires no
Lean.

Cards are the main way to contribute. Most people who know what belongs in a
library of behavioral theory do not write Lean, and most people who write Lean
do not know what belongs in a library of behavioral theory. Cards give the two
groups a way to work together.

## Writing one

Copy `0001-exponential-no-reversal.md`, give it the next number, and edit it.
The front matter uses the following fields.

| Field | Meaning |
|---|---|
| `title` | One line, in plain English |
| `status` | `proposed`, `accepted`, `formalized`, or `rejected` |
| `assumptions` | What the claim needs in order to hold. Prose is fine; naming them is what matters |
| `source` | A catalog entry id, DOI, or citation. "Folk knowledge, never stated in print" is an acceptable answer, and an interesting one |
| `statement` | The claim itself, as precisely as you can put it |
| `lean_decl` | Set only once the card has been formalized; the fully-qualified declaration name |
| `blocked_on` | Optional; other card ids or gaps in Mathlib |

Running `python3 scripts/validate_cards.py` checks the format, and continuous
integration runs the same check on every pull request. Please do not let the
format slow you down. A card with good content and imperfect front matter is
easy to fix in review.

## Lifecycle

A card begins as `proposed`, meaning someone thinks it may belong. It becomes
`accepted` once the working group agrees that it belongs, at which point it is
open for formalization. It becomes `formalized` when a Lean declaration exists
and `lean_decl` points at it. Cards that the working group decides against are
marked `rejected` and kept, with a note explaining the reasoning.

## A note on difficulty

Cards that are hard to write are among the most valuable things this process
produces. If you cannot pin down what a claim assumes, or you find that
different papers state it in incompatible ways, that tells us something about
how the result sits in the literature. Please describe the difficulty in the
body of the card and submit it anyway.

## What makes a card useful

Three qualities help. First, the assumptions are separable, so that a reader
could weaken one and ask what breaks. Second, the claim is an implication rather
than an empirical assertion; "organisms discount hyperbolically" is not a card,
whereas "if discounting is hyperbolic with k > 0, then preference reversal
occurs for some front-end delay" is. Third, the source is real and checkable.
Catalog ids work particularly well here, since they already carry the equation
and its variable definitions.
