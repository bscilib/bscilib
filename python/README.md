# bscilib (Python)

This package is the executable half of BSciLib. The Lean tree proves theorems
about idealized models, and this package tests the same claims against candidate
models that actually run.

| Module | Contents |
|---|---|
| `bscilib.identifiability` | Symbolic structural-identifiability checks (i.e., sensitivity rank, with naming of any parameter confounds found) |
| `bscilib.corpus` | Metamorphic relations, written as property-based tests |
| `bscilib.schedules` | Schedule semantics for VI, VR, FI, FR, concurrent, and chained arrangements (not yet started) |

## Install

    pip install -e ".[test]"

## Run

    pytest                                   # metamorphic corpus
    python -m bscilib.identifiability.poc    # confound-detection demo

## Correspondence with the Lean tree

Each metamorphic relation here should name the Lean theorem it mirrors, and each
Lean theorem should name its counterpart here. The pairing is deliberate. Lean
establishes the claim for the idealized model, while Hypothesis searches for
violations in a working implementation.

| Claim | Lean | Python |
|---|---|---|
| Stationary discounting admits no preference reversal | `BSciLib.no_preference_reversal_of_stationary` | `tests/test_metamorphic.py::test_mr2_*` |
| Matching is scale-invariant in reinforcement rate | not yet formalized (card 0003) | `tests/test_metamorphic.py::test_mr1_*` |

## License

MIT. The Lean tree is Apache 2.0, matching Mathlib.
