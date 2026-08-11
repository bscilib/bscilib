# Contributing to BSciLib

Thanks for considering it. This document describes how contributions work,
what review looks for, and which conventions we follow. If anything here is
unclear, an issue asking about it is a perfectly good first contribution.

## Two ways in

The first way is a statement card, and it requires no Lean. Open a pull request
adding a file to `cards/` that contains a claim, the assumptions it needs, and
where it came from. [`cards/README.md`](cards/README.md) has the format, and
copying an existing card is the easiest way to start. Cards are how the library
learns what belongs in it.

The second way is formalization, which turns an accepted card into a Lean
declaration, sets that card's `lean_decl` field, and flips its status to
`formalized`. Issues tagged `good first formalization` have been scoped for a
first contribution.

Neither path requires permission to begin. If you would like feedback before
finishing, opening a draft pull request early is welcome.

## The commitment that shapes everything else

Every theorem in BSciLib is an implication. The library does not assert that any
organism behaves in any particular way. Assumptions belong in
`BSciLib/Assumptions/`, named and documented with what is known about them
empirically, including the cases where they are known to fail.
[`docs/assumptions.md`](docs/assumptions.md) explains the reasoning behind this
policy at more length.

Continuous integration checks the mechanical part: no `axiom` outside
`Assumptions/`, no `sorry` anywhere in the library, and a verified axiom
footprint on flagship results.

## What review is for

Whether a proof is correct has already been settled by the time a reviewer sees
it, since the Lean kernel does not accept invalid proofs. Review therefore
attends to three other things.

First, are the assumptions honestly described? A module's docstring should say
what is actually known about the assumption, including where the evidence runs
against it.

Second, is the statement at the right level of generality? If a hypothesis
appears in the statement but is never used in the proof, we remove it, because
the theorem is stronger than it appears and the extra hypothesis misleads
readers about what the result requires. This is our most common review comment
and, we think, the most useful one.

Third, is the declaration easy to find and to read? That covers Mathlib naming
conventions, a docstring on every public declaration, and a citation for the
source.

One note on how disagreements get settled here. Once continuous integration
passes and the assumptions are honestly stated, seniority carries no weight in
whether a contribution is merged.

## Style

We follow Mathlib's conventions rather than inventing our own, so that anyone
who has worked in Lean already knows our house style. The
[style guide](https://leanprover-community.github.io/contribute/style.html) and
[naming convention](https://leanprover-community.github.io/contribute/naming.html)
are the references. Briefly: `snake_case` theorem names that describe the
statement; `UpperCamelCase` for types and classes; a docstring on every public
declaration; and the copyright header on every file.

Please cite sources in docstrings. Catalog entry ids work well, since they
already carry the equation and its variable definitions.

## Checks to run before pushing

    lake build
    python3 scripts/lint_axioms.py
    ./scripts/check_axiom_footprint.sh
    python3 scripts/validate_cards.py
    cd python && pytest -q

## Getting help

GitHub Discussions is the place for questions about design, scope, or whether
something belongs in the library. For questions about Lean itself, the
[Lean Zulip](https://leanprover.zulipchat.com/) is a friendly and unusually
patient place for newcomers, particularly if you arrive with a clear statement
of what you are trying to prove.
