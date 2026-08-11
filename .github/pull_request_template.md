<!-- Please delete the sections that do not apply. -->

## What this changes

## If this adds or changes a theorem

- [ ] Every hypothesis in the statement is used by the proof. (If one is not,
      please remove it. The theorem is stronger than it appears, and the extra
      hypothesis misleads readers about what the result requires.)
- [ ] Public declarations have docstrings, with sources cited.
- [ ] Any new assumption lives in `BSciLib/Assumptions/`, and its docstring
      states its empirical standing and known violations.
- [ ] `lake build`, `scripts/lint_axioms.py`, and
      `scripts/check_axiom_footprint.sh` pass locally.

## If this adds or changes a statement card

- [ ] `python3 scripts/validate_cards.py` passes.
- [ ] The status reflects reality (`lean_decl` is set if and only if the status
      is `formalized`).

## Anything you found hard

Optional, and genuinely useful, particularly if an assumption resisted being
pinned down or the literature states the claim in more than one way.
