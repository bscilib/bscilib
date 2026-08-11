# BSciLib: a machine-checked library of behavioral theory

Working plan, drafted 2026-08-10. Expect this to change as we learn what
works.

This document is a companion to `program_roadmap.md` (i.e., the larger program
running from MIABS through a benchmark corpus, an exchange format, and
verification tooling) and to `miabs_v0.1_blueprint.md`. Those documents describe
what is worth building. This one describes where we are starting and what the
next few months look like.

## Where we are starting

The program roadmap sketched the derivation library as a later piece, on the
thought that it would want a stabilized vocabulary underneath it. Starting there
instead seems reasonable right now, for three practical reasons rather than any
principled one.

First, the library gives people something to do immediately. A statement card
takes an afternoon and needs no Lean, so there is a contribution path available
from day one, which a reporting checklist does not offer until it is finished
and adopted.

Second, several of the other artifacts turn out to overlap with it. The
metamorphic relations in `python/tests/test_metamorphic.py` state the same
claims as the Lean theorems in a different representation, so corpus entries and
library results can grow together. The Phase 0 identifiability preprint and
flagship theorem #5 would likewise share their content, once a real motivating
case is in hand.

Third, the Behavioral Process Catalog supplies a backlog. Its 209
equation-bearing entries offer an empirically grounded answer to what belongs in
the library, along with a priority queue, which is the thing a new project
usually lacks.

None of this settles the ordering. If the cards attract few contributors, or the
formalization proves slower than expected, then MIABS and the corpus are still
sitting there and the sequence should change accordingly. Nothing in the plan
below depends on the current order being the right one.

## What can actually be formalized

Behavior science has no axioms, and any attempt to supply some would be an
instance of exactly the premature axiomatization that the program roadmap
already names as its third risk. The library therefore never asserts an
empirical claim. Every declaration in BSciLib is an implication: given
assumptions A1 through A3, consequence C follows.

That constraint turns out to be the whole design, and it plays to what
proof-checking tools are good at. The question that comes up most often in
quantitative behavior analysis is seldom whether a given equation is true. More
often it is what the equation presupposes, and whether the field's derivation of
it carries those presuppositions through to the conclusion. That is a question
in the spirit of reverse mathematics, and it is machine-checkable.

## What motivates the effort

The Behavioral Process Catalog's `TODO.md` records that 15 of its 209
equation-bearing entries carried LaTeX corrupted badly enough that an editorial
panel had to reconstruct them from the surrounding quantitative literature,
because the source papers are pre-1990 JEAB scans with no machine-readable
equation layer. Twelve of those reconstructions still await a human check
against the physical page.

It is worth being careful about what this does and does not show, since the
claim is easy to overstate. Nothing has been lost to science. Any reader can
open those papers and read the equations perfectly well, and the mathematics is
exactly where the authors left it. The narrower difficulty is that the equations
exist only as marks on page images, so no program can parse, search, compare, or
execute them.

In turn, work that would be routine in a field whose models are machine-readable
currently requires a person to retype the mathematics first. Asking whether two
published models make the same predictions under a given schedule, or whether a
model's parameters are identifiable from a particular design, are both
mechanical questions given a machine-readable model and substantial projects
without one. Retyping also introduces errors of its own, as the catalog's
reconstruction pass illustrates. A checked library is one way to build that
missing layer, a result at a time.

## What Lean offers beyond a symbolic algebra system

The Python layer could do some of this work, so it is worth saying what the
proof assistant adds.

First, assumption tracking. Running `#print axioms` on a declaration reports
exactly what the result depends on, and to my knowledge no other tool in common
use gives this directly.

Second, negative results. Claims of the form "these two parameter vectors are
observationally equivalent" and "no data collected on this design can separate
them" are provable in Lean, whereas a fitting routine can only ever be
suggestive about them. Flagship theorem #5 below is a case in point.

Third, protection against silent hypothesis smuggling. A continuity,
monotonicity, or independence assumption that is used in a derivation but never
stated is among the more common defects in published mathematical arguments, and
it becomes impossible to commit.

Fourth, permanence. A checked proof stays valid for as long as the toolchain
builds.

## Architecture

```
bscilib/                          repo root
  lean-toolchain                  pinned Lean version
  lakefile.toml                   depends on Mathlib
  BSciLib.lean                    root import file
  BSciLib/
    Foundations/
      Time.lean                   continuous, discrete, and event-driven time
      Event.lean                  responses, reinforcers, stimuli as abstract types
      Allocation.lean             behavior allocation over alternatives
    Assumptions/                  the reverse-mathematics layer; see below
      Matching.lean               strict, generalized, melioration
      Conservation.lean           constant total behavior
      Discounting.lean            monotone, normalized, stationary, and so on
      Independence.lean           magnitude and delay separability
    Discounting/
      Basic.lean  Reversal.lean
    Choice/
      Matching.lean  Herrnstein.lean
    Identifiability/
      Observational.lean          observational-equivalence definitions
      Discounting.lean            observational equivalence in discounting models
    Respondent/
      RescorlaWagner.lean         (v0.2)
  python/
    bscilib/
      schedules/                  VI, VR, FI, FR, conc, chain; executable
      identifiability/            symbolic rank tests
      corpus/                     metamorphic relations as property tests
    tests/
  cards/                          statement cards; the contribution path without Lean
  docs/                           roadmap, assumption policy, naming conventions
  miabs/                          the MIABS checklist and its generator
  scripts/                        policy lints and setup helpers
```

### The assumption-module pattern

This pattern carries the intellectual weight of the design, so it is worth
spelling out. Rather than asserting the matching law, we declare it as a
structure that a model may or may not satisfy.

```lean
/-- Strict matching (Herrnstein 1961): relative behavior allocation equals
relative reinforcement rate across all concurrently available sources.

Empirical standing: undermatching is the modal empirical result, so this
assumption is usually false as stated. See `Assumptions.GeneralizedMatching`
for the two-parameter weakening. -/
class StrictMatching (M : Model) : Prop where
  matches : ∀ i j, M.allocation i / M.allocation j = M.rate i / M.rate j
```

Theorems then take assumption instances explicitly.

```lean
theorem herrnstein_hyperbola
    [StrictMatching M] [ConstantTotalBehavior M k] (r r_e : ℝ) ... :
    M.allocation target = k * r / (r + r_e) := ...
```

Three consequences follow without further effort.

The first is that nothing is frozen. Adding an assumption module costs nothing
and commits the library to nothing, which keeps the ontology open, as the
program roadmap's third risk requires.

The second is that theoretical even-handedness becomes structural. A molar
assumption module and a molecular one sit side by side in `Assumptions/`, and
theorems declare which they consume. There is no privileged set. This seems a
more durable arrangement than a stated intention to be fair, since it does not
depend on anyone's continued goodwill.

The third is that dependency facts become results. A statement such as
"Herrnstein's hyperbola requires constant total behavior, and under generalized
matching the consequent is not a hyperbola" is publishable, and the library
produces it mechanically.

One policy, enforced by a continuous-integration lint, keeps this honest: no
`axiom` declarations outside `Assumptions/`, and every module there carries a
docstring stating its empirical provenance and known violations.

### Correspondence between Lean and Python

Each claim gets two representations, deliberately.

| Claim | Lean | Python |
|---|---|---|
| Matching is scale-invariant in rate | `matching_scale_invariant` (planned) | `test_mr1_scale_invariance` |
| Stationarity admits no reversal | `no_preference_reversal_of_stationary` | `test_mr2_no_reversal` |

The Lean side establishes the claim for the idealized model, while the Python
side tests it against any candidate agent implementing the interface. A model
that passes the Python property while violating the Lean theorem's hypotheses is
the interesting case, since it suggests the property holds for a reason the
theorem does not capture. The pairing is documented in `python/README.md`, and
in the longer run the corpus entry format should carry both.

## (a) Basics up and running, weeks 1 through 3

None of this is research. It is a walking skeleton: one easy theorem, green
continuous integration, and a published front door, working end to end before
any of the content gets hard.

Week 1 covers the toolchain and skeleton. Initialize the repository with a
`.gitignore` covering `.lake/`, `__pycache__/`, `.hypothesis/`,
`.pytest_cache/`, and `.DS_Store`; note that the starter-kit zip ships several
of those caches, so unpack and clean before the first commit. Install `elan` and
pin `lean-toolchain` to whatever Mathlib's current release uses. Migrate the
four proof-of-concept scripts in `tools/` into `python/bscilib/` behind a
`pyproject.toml`, keeping `make_onepager.py` for MIABS. Then ship one theorem
and nothing else. Three lines of algebra is the right size, because the goal is
to show that the pipeline works before the mathematics starts making demands.

Week 2 covers continuous integration and hygiene. GitHub Actions should run
`lake exe cache get && lake build`, `pytest` for the Python package, and the
policy lints, all as required checks. On licensing, use Apache 2.0 for the Lean
tree so that results can be contributed upstream to Mathlib where appropriate,
MIT for Python, and CC-BY 4.0 for prose. Adopt Mathlib naming conventions rather
than inventing a house style. Add `CITATION.cff` and a Zenodo hookup so that
every tagged release receives a DOI, with contributors listed as authors; the
catalog's leaderboard suggests that credit of this kind does real recruiting
work.

Week 3 covers the front door and the governance furniture. Write a README that
opens with a theorem statement and its axiom footprint rather than with a
mission statement, and write the governance document, code of conduct, issue
templates, and pull-request template now, while they cost nothing and there is
nothing to argue about.

One revision to the original plan is worth recording. I had put browsable API
documentation in week 3. In practice `doc-gen4` documents the entire import
closure, so publishing documentation for three declarations would mean building
documentation for all of Mathlib, which costs hours of continuous integration
and produces a large site in order to render three pages. Turning it on makes
sense once the library has content worth browsing, around theorem #4 in weeks 9
through 10, and it should run on `workflow_dispatch` and on release rather than
on every push. Until then the README serves as the front door.

Exit criteria for this phase: continuous integration green on a fresh clone; one
theorem checked; a stranger able to run `lake build` in under ten minutes.

## (b) GitHub as a community project, weeks 3 through 6

The organization is `github.com/bscilib`, holding `bscilib` (the library), the
Behavioral Process Catalog, and MIABS. One item should precede the catalog's
move. The catalog's published citation (Perez, McNulty, & Cox, 2025,
*Perspectives on Behavior Science*) points at
`david-j-cox.github.io/catalog-of-principles-and-processes`. GitHub does
redirect transferred repositories and their Pages URLs, but a redirect is a
courtesy rather than a guarantee. Registering a custom domain (e.g.,
`bscilib.org`) and pointing Pages at it first would make this the last URL move
that costs anything.

### The two-tier contribution model

There is an obvious objection to a Lean library aimed at behavior analysts,
which is that the number of behavior analysts who write Lean is approximately
zero. The objection is correct, and the two-tier model is the answer to it.

The first tier is the statement card. Anyone can open a pull request adding a
file to `cards/` containing an informal statement, assumptions in prose, a
source (i.e., a catalog entry id or DOI), and a note on why the claim matters.
No Lean is required. This is close to the submit-and-verify workflow that the
catalog has already trained people on.

The second tier is formalization, in which a smaller group turns accepted cards
into Lean. Assistance from language models has made this considerably cheaper
than it was even two years ago, and it is the natural place to put a funded
student.

Cards live at `cards/NNNN-slug.md` with front-matter fields for `title`,
`status`, `assumptions`, `source`, `statement`, `lean_decl` once formalized, and
an optional `blocked_on`. Continuous integration validates the schema. A card
whose `lean_decl` resolves to a real declaration can flip to `formalized`
automatically, and that single check does most of the work that a more elaborate
credit system would.

### Repository furniture

The shared items across the organization are a contributing guide covering the
two tiers and the assumption policy; a code of conduct (Contributor Covenant,
unmodified); a governance document specifying a working group of four to six
with theoretical diversity as a written requirement, an annual revision cycle,
and an explicit statement that correctness is settled by the proof checker
rather than by seniority; issue templates for cards, formalization requests, and
defects; a label set including `good first formalization`, `needs card`,
`needs assumptions`, `blocked on mathlib`, and `catalog-sourced`; GitHub
Discussions rather than Zulip for now, since Zulip suits Mathlib's scale and
would look presumptuous at ours; and a public project board organized around the
flagship theorem list, so that the backlog is legible to anyone who arrives at
the repository.

### Recruiting

Three pools, in this order.

The first is the catalog's existing contributors. They have already done
structured volunteer work on behavioral equations, and they can write cards
immediately.

The second is the Lean and formalization community. They tend to be actively
interested in new application domains and are unusually helpful to newcomers who
arrive with clean statements and a working build. A Zulip post asking for a
sanity check on the assumption structure will likely draw more substantive help
in a week than a grant application would in a year.

The third is mathematical psychology and computational modeling (e.g., SQAB and
the Society for Mathematical Psychology), which is where both halves of the
audience overlap.

Exit criteria for this phase: organization live; catalog moved behind a stable
URL; three external statement cards merged; one external Lean contribution
merged.

## (c) Getting to work: the v0.1 content, weeks 4 through 14

Five flagship theorems, ordered by difficulty. The set is chosen so that each
one demonstrates something different about what the library can do.

The first is that exponential discounting admits no preference reversal. Given
`V(A,D) = A·exp(-kD)`, if `V(A_s, D_s) ≥ V(A_l, D_l)` then the same ordering
holds after adding any common front-end delay. The proof is immediate, since the
added delay multiplies both values by the same factor. It comes first precisely
because it is easy, and it serves as the walking skeleton and the documentation
example.

The second is that hyperbolic discounting produces reversal, constructively.
Given `V(A,D) = A/(1+kD)`, smaller-sooner preference at zero front-end delay,
and the usual ordering of amounts and delays, exhibit an explicit delay at which
preference reverses. The interesting part is that Lean requires the witness
rather than accepting an appeal to limiting behavior. This one pairs with MR-2
in the Python corpus.

The third is that generalized matching is scale-invariant in reinforcement rate.
Given `log(B₁/B₂) = a·log(r₁/r₂) + log b`, scaling both rates by a common factor
leaves the predicted allocation unchanged. This is easy, and its value is as a
demonstration of the Lean and Python correspondence, since the identical claim
already exists as `test_mr1_scale_invariance`.

The fourth is Herrnstein's hyperbola, derived from strict matching together with
constant total behavior. This is the reverse-mathematics showcase and probably
the one worth a paper. Derive `B = kr/(r + r_e)` from the two named assumption
modules, then show what happens when strict matching is weakened to generalized
matching, where the consequent is no longer a hyperbola. The publishable output
is the dependency fact rather than the equation.

The fifth is an observational-equivalence result in a separable discounting
model, and it needs a motivating case before it can be written. The
mathematical content is a collapse of the form

    (A^α · e^(−κD^γ))^(1/α) ≡ A · exp(−κD^γ/α)

from which it follows that rescaling `(α, κ)` by a common factor leaves every
predicted indifference point unchanged, on any design, at any sample size. Two
parameters are therefore not separately recoverable, no matter how much data are
collected.

A result of this shape would be the capstone of v0.1, for two reasons. It is a
negative result that no fitting procedure can establish, since a fit walking a
flat ridge looks like a fit that has converged. And it is the natural centerpiece
for the Phase 0 identifiability preprint, which would make the preprint and the
flagship theorem the same piece of work.

What is missing is a real model to attach it to. The strongest version examines
one of our own published discounting models, so that the paper reads as
self-examination rather than as criticism of others. That means running
StructuralIdentifiability.jl over our actual model forms first and seeing what
it reports, rather than deciding in advance what it will find. Until that
happens, the theorem is a synthetic exercise, and the schedule below reflects
that.

### The catalog as a backlog engine

Beyond serving as a citation, the catalog contributes in four concrete ways.

The 209 equation-bearing entries carry LaTeX plus variable definitions, which
makes them a ready-made formalization queue. Each becomes a draft statement card
with `source: catalog#<id>`, pre-populated with the equation and its
definitions, at status `proposed`. That is a backlog of roughly two hundred
well-scoped units of work, which is the thing open-source projects usually
lack.

This is a nightly-batch job rather than an afternoon's work. Reading an entry
closely enough to extract its assumptions costs real tokens, and the catalog's
own validation runs have already hit session limits twice. The budget should
follow the same pattern that `.validation/` already uses, described below.

The 813 process labels (172 preferred labels after the taxonomy merge) offer a draft
module hierarchy. They should be adopted as file names rather than as an
ontology, since file names commit to nothing.

The `.validation/` machinery itself, with its batched review, checkpointed
progress, human-followup queue, and taxonomy merges, is a working pattern for
autonomous review at scale, and it can be reused to triage the 209 into cards.

Finally, the 12 unverified reconstructed equations are both the motivating
example for talks and the first twelve cards worth a person's attention.

### Nightly card generation and the token budget

The literature sweep is the expensive part of this project and has to be paced.
The catalog's `.validation/` machinery already solves this problem, so it should
be lifted rather than rebuilt: batched cycles, a cursor and done-set on disk, a
nightly window, a cooldown when session limits are hit, and a commit per cycle
so that an interruption costs at most one batch.

On sizing, the catalog's own numbers give 26 cycles and roughly 13.7 million
tokens, or about 530,000 per cycle at 40 entries. Card generation is heavier per
entry than metadata validation, since extracting a claim, separating its
assumptions, and drafting a statement is closer in kind to the three-editor
equation workflow (8 entries per cycle) than to a single reviewer pass. Starting
at 8 to 10 entries per night and adjusting from measured cost seems right. At
that rate the 209 equation-bearing entries take roughly three to four weeks of
nights, which is fine, since nothing downstream waits on the full backlog. Only
the first dozen cards are on the critical path.

Sequence matters more than throughput here. The 12 human-followup entries from
the catalog's `TODO.md` should go first, since they are the entries whose
equations were reconstructed by inference and are therefore both the
highest-value cards and the motivating exhibit.

Two prerequisites, in order. First, finish the catalog's equation track, where 7
of 209 entries remain and the run is currently paused in cooldown. Cards
generated from unvalidated equations would inherit exactly the problem this
project exists to address. Second, and only then, start the card sweep, reusing
`gen_batch.py` and `apply_batch.py` with a card-drafting template in place of
the review template.

The entry track, at 12 of 11,920 entries done, is a separate and much larger
job, and it is not on BSciLib's critical path. It can run at whatever rate the
budget allows.

### The first two papers

The identifiability paper is already planned, and it would carry a
machine-checked proof as its methods contribution. It needs a real motivating
case first; see theorem #5 above. Target PsyArXiv, then *JEAB* or
*Behavioural Processes*.

The position paper would ask what the matching law presupposes, using the
reverse-mathematics framing with theorems #3 and #4 as the demonstration.
*Perspectives on Behavior Science* is the natural venue. This is likely the
paper that does the recruiting, since it should be interesting to a theorist who
will never write a line of Lean.

## Where the program's other pieces stand

| Program piece | Where it sits now |
|---|---|
| Standing, award address, working group | Running in parallel, unchanged |
| Identifiability preprint | Shares its content with flagship theorem #5, so the two get written together |
| MIABS checklist | Drafted already, and circulating the one-pager for criticism costs an email rather than a build. Continues alongside |
| Benchmark corpus | Overlaps with the library's executable half, since the metamorphic relations state the same claims |
| Exchange format, reference simulator | Would grow into `python/bscilib/schedules/` when the schedule semantics are needed |
| Derivation library | Where we are working now |

Read that as a snapshot rather than a decision. Several of these could
reasonably come forward if circumstances suggest it, and the MIABS work in
particular is close enough to done that finishing it may make sense at any
point.

## Risks worth watching

The first risk is that essentially nobody in the target field writes Lean. This
is the largest risk and the reason the two-tier card model is not optional. Part
of the mitigation is social as well as technical: the first external contributor
should probably come from the Lean community rather than from behavior analysis,
so that the repository has a working review culture in place before the
behavioral audience arrives.

The second risk is a category error, namely formalizing empirical claims. The
guard is structural: no `axiom` outside `Assumptions/`, every module documenting
its known violations, and every theorem stated as an implication. If a reviewer
can ever fairly say that we have asserted that behavior obeys some law, the
design has failed.

The third risk is formalizing the wrong things. The temptation runs toward what
is easy in Lean (real analysis) rather than toward what matters (schedule
semantics, which are hard). The catalog-derived backlog is the countermeasure,
since it sets priorities from what the field actually published.

The fourth risk is Mathlib churn. Pin the toolchain, use `lake exe cache get`,
and upgrade on a fixed cadence rather than opportunistically.

The fifth risk, carried over from the program roadmap and now more acute, is the
founder bottleneck. The Lean tree has a bus factor of one on day one. By the
time the position paper is submitted, at least one flagship theorem should have
been formalized by somebody else.

## A twelve-week calendar

| Weeks | Deliverable |
|---|---|
| 1 | Toolchain, repository skeleton, theorem #1, Python package migrated |
| 2 | Continuous integration green, licensing, naming conventions, CITATION and Zenodo |
| 3 | README and governance furniture; organization created |
| 4 | Catalog moved under the organization behind a custom domain; card schema and its validation |
| 5–6 | Theorems #2 and #3; first `good first formalization` issues; Lean Zulip post |
| 7–8 | Run identifiability analysis over our own published discounting models; write theorem #5 against whatever it turns up |
| 9–10 | Theorem #4 and the generalized-matching weakening; turn on `doc-gen4` |
| 11 | Card-generation sweep begins, at 8 to 10 catalog entries per night, the 12 human-followup entries first, running roughly three to four weeks in the background |
| 12 | Identifiability preprint to PsyArXiv; position paper outlined; v0.1 tagged with a DOI and a contributor list |

Exit criteria for v0.1: five theorems checked in continuous integration; the
organization live with the catalog under it; the card pipeline validated end to
end by at least one external contributor; and the preprint posted.
