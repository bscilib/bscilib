# BSciLib

BSciLib is a library of behavioral theory written so that a computer can check
it. Status: v0.1, early, and openly under construction.

Quantitative behavior analysis has accumulated a substantial body of
derivations over the past six decades (e.g., the matching law and its
generalizations, discounting models, behavioral momentum, associative learning
rules). Those derivations live in papers, stated in prose and equations, and the
reasoning that carries assumptions to conclusions lives in the reader's head.
The purpose of this library is to write some of that reasoning down in a form
that a proof checker can verify, so that the assumptions each result depends on
become explicit, searchable, and easy to argue about.

## A worked example

Consider a result many of us learned as a fact about exponential discounting.

```lean
theorem no_preference_reversal_of_stationary (d : ℝ → ℝ)
    [Stationary d] [DiscountWeights d] {A_s D_s A_l D_l : ℝ}
    (h : value d A_l D_l ≤ value d A_s D_s) (T : ℝ) :
    value d A_l (D_l + T) ≤ value d A_s (D_s + T)
```

In words: if the larger-later option is not preferred to the smaller-sooner
option, then adding the same front-end delay to both alternatives cannot make
the larger-later option preferred.

Writing this out with every hypothesis made explicit had a small surprise in it.
The exponential form turned out to be unnecessary. The proof uses exactly two
properties: stationarity (i.e., the weight of a total delay factors into the
weights of its parts, so that d(D + T) = d(D) × d(T)) and nonnegative weights.
Continuity, monotonicity, a positive discount rate, and the usual restriction to
nonnegative front-end delays all go unused.

That reframing may carry a practical upshot. Asking whether an organism
discounts exponentially is a question about functional form, and it is answered
by fitting curves. Asking whether an organism's discount function is stationary
is a question about an invariance, and it is answered by a front-end delay
manipulation. In turn, the second question appears both cheaper to ask and
closer to the assumption actually doing the work.

Lean also reports what a result rests on. For the theorem above:

```
'BSciLib.no_preference_reversal_of_stationary' depends on axioms:
  [propext, Classical.choice, Quot.sound]
```

Those three are Lean's own logical foundations and nothing else. Producing
observations of this kind across the field's quantitative literature is what the
library is for.

## The one commitment

BSciLib does not assert empirical claims. Every theorem is an implication: given
the assumption modules it names, the stated consequence follows.

We take this stance for a practical reason. Behavior science has no axioms, and
supplying some now would freeze an ontology long before the field has settled on
one. Assumptions therefore live in `BSciLib/Assumptions/`, each documented with
what is known about it empirically, including where it fails. Stationarity is a
good illustration: preference reversal under a common front-end delay is one of
the better-replicated findings in the discounting literature, so the assumption
is routinely violated. The module exists to make results that depend on it
visible, not because anyone believes it holds generally.

Continuous integration enforces the mechanical part of this policy. No `axiom`
outside `Assumptions/`, no `sorry` anywhere, and a checked axiom footprint on
every flagship result. A fuller discussion is in
[`docs/assumptions.md`](docs/assumptions.md).

## Layout

| Path | Contents |
|---|---|
| `BSciLib/` | The Lean library (Apache 2.0, matching Mathlib) |
| `BSciLib/Assumptions/` | Named, documented assumption modules |
| `python/` | The executable half: identifiability checks, metamorphic tests, and eventually schedule semantics (MIT) |
| `cards/` | Statement cards, the contribution path that requires no Lean |
| `docs/` | Roadmap, assumption policy, contributing notes |
| `miabs/` | The MIABS reporting checklist and its generator (CC-BY 4.0) |

## Build

    curl -sSfL https://elan.lean-lang.org/elan-init.sh | sh
    lake exe cache get     # prebuilt Mathlib; this step saves hours
    lake build

    cd python && pip install -e ".[test]" && pytest

## Contributing

There are two ways in, and the first one needs no Lean at all.

The first is a statement card: write down a claim you think belongs in the
library, name the assumptions it needs, and cite where it came from. Most people
who know what belongs in a library of behavioral theory do not write Lean, and
most people who write Lean do not know what belongs in a library of behavioral
theory. Cards are how the two groups talk to each other. See
[`cards/README.md`](cards/README.md), and please do not worry about getting the
format perfect on the first try.

The second is formalization, which turns an accepted card into a checked
theorem. Issues tagged `good first formalization` are scoped so that a first
contribution can be finished in a sitting.

If a card proves hard to write because the assumptions are difficult to pin
down, that is worth reporting rather than a sign of trouble on your end. Such
cases tell us something about how the result is stated in the literature, and
they are among the most useful things a contributor can send. Further detail is
in [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Where this came from

BSciLib is one piece of a larger program that also includes a reporting standard
for behavioral simulations (MIABS) and a planned benchmark corpus of behavioral
phenomena. That program is described in
[`docs/program_roadmap.md`](docs/program_roadmap.md), and
[`docs/bscilib_roadmap.md`](docs/bscilib_roadmap.md) describes what we are
working on at the moment and why we started here.

A sibling project, the
[Behavioral Process Catalog](https://github.com/david-j-cox/catalog-of-principles-and-processes),
indexes 11,920 articles from JEAB, Behavioural Processes, and JEP: Animal
Learning & Cognition; 209 of those entries carry equations. While assembling
them, 15 equations came through the extraction pipeline corrupted badly enough
that an editorial pass had to reconstruct them, and 12 of those reconstructions
are still awaiting a check against the original pages.

To be clear about what that does and does not show. Any reader can open those
papers and read the equations without difficulty, so nothing has been lost to
science. The narrower problem is that the equations exist only as marks on
scanned page images, with no machine-readable layer underneath. In turn, work
that would be routine in a field whose models are machine-readable (e.g., asking
whether two published models make the same predictions under a given schedule,
or whether a model's parameters are identifiable from a given design) currently
requires someone to retype the mathematics first, and retyping introduces errors
of its own. A checked library is one way to build that layer, a result at a
time.

## An invitation

If you work on quantitative accounts of behavior and have ever wondered exactly
which assumptions a familiar derivation requires, you already have the expertise
this project runs on. Objections are as welcome as contributions, and a
well-argued case that some piece of this is misguided will improve the library
more than another theorem would. We would be glad to have you along.

## License

Lean tree: Apache 2.0, matching Mathlib so that results can be contributed
upstream where appropriate. Python: MIT. Prose and checklist: CC-BY 4.0.
