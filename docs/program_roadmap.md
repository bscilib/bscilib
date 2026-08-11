# A formal infrastructure for behavior science: build roadmap

Working title for the program: Open Behavioral Modeling Initiative. This is a
placeholder, and naming it late, once the first artifacts exist, seems wiser
than naming it now.

A note on how to read this document alongside its companion. The phases below
describe the program's substance, meaning the pieces of infrastructure worth
building and what each one is for. The order in which they get built is a
separate and softer question, and `bscilib_roadmap.md` records where we are
starting at the moment. The numbering here reflects an early view of the
sequence rather than a commitment to it.

## The goal

Within a decade, no simulation of operant or respondent processes would be
published in a flagship behavioral journal without three things: (a) a complete
machine-readable specification; (b) evidence of parameter recoverability; and
(c) reported performance against a shared benchmark corpus. Verification layers
beyond those three should remain opt-in badges rather than gates.

The strategic posture throughout is to ship tools rather than proposals. Each
phase must produce something citable and useful to a laboratory that has never
heard of the larger program. Ratification follows adoption, and it seems
unlikely ever to precede it.

## Phase 0: standing (now through the end of 2026)

The goal of this phase is to establish the intellectual frame and the political
capital before any infrastructure exists. Four items.

The first is the close of the award address. The existing thesis, that
measurement constraints rather than the organism bounded what the field could
ask, extends one register upward: for artificial organisms, representational
constraints now bound what is askable. Two minutes at the end is enough. This
plants the flag with the audience whose participation matters most, under the
cover of an award rather than a proposal.

The second is the self-audit preprint. Run structural identifiability analysis
(e.g., StructuralIdentifiability.jl or SIAN) on our own discounting models
first, plus one or two established models from the literature. The framing matters here: these are
tools that reveal problems in models we all use, including mine. Delivered that
way, the demonstration that the tooling has teeth reads as an invitation rather
than an indictment. Target PsyArXiv within the quarter, then the *Journal of the
Experimental Analysis of Behavior* or *Behavioural Processes*.

The third is working-group recruitment. Four to five people, chosen for visible
theoretical diversity: at least one committed molar theorist, one molecular, one
quantitative modeler outside my immediate network, and one credible skeptic of
the whole enterprise. The skeptic's seat is not decoration. Their objections
will improve the checklist, and their eventual signature would be the strongest
endorsement available. Recruit by asking for criticism of a draft rather than
for membership in a movement.

The fourth is a SQAB symposium proposal for the 2027 meeting. A symposium rather
than a paper, since the goal is a room in which the checklist gets argued about,
which tends to convert attendees into stakeholders.

Exit criteria: preprint posted; three of five working-group seats filled;
symposium accepted.

## Phase 1: MIABS, the reporting checklist (2026 through 2027)

The goal of this phase is the least expensive artifact that changes behavior,
namely a one-page minimum-information standard modeled on MIAME.

MIABS stands for Minimum Information About a Behavioral Simulation. The name
signals its lineage deliberately, since MIAME's trajectory (i.e., published in
2001 and required by major journals within roughly three years) is the playbook.
The full blueprint is in `miabs_v0.1_blueprint.md`.

Three moves matter in this phase beyond the drafting itself.

The first is the retrospective audit paper. Apply MIABS to the last 20 to 30
published behavioral simulations, including our own, and report compliance rates
item by item. This does three things at once. It tests whether the items
discriminate among papers; it generates the reproducibility-gap citation that
subsequent grants and papers will need; and it demonstrates the checklist on
real papers, so that editors can see for themselves how low the cost is.

The second is journal outreach, in rough order of likely receptivity: *JEAB*,
which has the quantitative constituency and SQAB-adjacent editors;
*Behavioural Processes*; *Perspectives on Behavior Science* for the position
paper; and *JABA* last, given its applied audience and different incentives. The
ask should stay soft, recommending the checklist for authors rather than
requiring it. A requirement makes sense only after the corpus exists.

The third is a versioning and governance stub. MIABS v0.1 is explicitly
provisional, revised annually by the working group, and archived on OSF with a
DOI for each version. Inexpensive governance now should prevent ownership
disputes later.

Exit criteria: MIABS v1.0 published with working-group authorship; one journal
listing it in author guidelines; audit paper submitted.

## Phase 2: the benchmark corpus (2027 through 2028)

The goal of this phase is the artifact most likely to generate citations,
contributors, and an admission test for artificial organisms.

The corpus is a versioned, curated repository of behavioral phenomena. Each
entry contains three things: (a) a reference dataset or the specification that
generates it; (b) the qualitative signature that any adequate model must
reproduce, stated as metamorphic relations where possible (i.e., invariances and
directional predictions that hold without ground truth); and (c) provenance
along with known boundary conditions.

An initial set of 12 to 15 entries might cover generalized matching on single
and concurrent schedules; the Herrnstein hyperbola; delay discounting with
preference reversal; magnitude and sign effects in discounting; the partial
reinforcement extinction effect; behavioral contrast; resurgence; ABA and ABC
renewal; behavioral momentum, in the sense of resistance-to-change ordering;
acquisition and extinction curves under Rescorla-Wagner-style respondent
preparations; blocking; spontaneous recovery; and schedule-typical response
patterning (e.g., the FI scallop and the FR break-run).

Three design decisions carry most of the weight. First, each entry is a test,
executable against a common interface, taking a model in and returning
pass, fail, or partial, with the metamorphic relations checked by property-based
testing in the style of Hypothesis or QuickCheck. Second, the curation protocol
should follow BioModels, where an entry is not accepted until an independent
party regenerates its reference figures from the deposited specification.
Curation rather than formalism is what made BioModels useful. Third,
contribution counts as authorship, since corpus versions receive citable DOIs
and contributor lists, and that is the recruitment engine.

Exit criteria: corpus v1.0 with at least 12 curated entries; at least three
external laboratories having run a model against it; and a paper asking how well
existing models perform, using the corpus as the instrument.

## Phase 3: exchange format and reference simulator (2028 through 2030)

The goal of this phase is the SBML move, namely a machine-readable specification
language for behavioral experiments and models, together with the library that
makes adopting it free. It comes here rather than earlier because the format
should be shaped by what Phases 1 and 2 reveal that people actually need to
express.

The first piece is a schedule and contingency specification language. A
declarative format, likely JSON-schema'd or a small domain-specific language,
covering schedule algebra (e.g., VI, VR, FI, FR, conc, chain, tand, mult, and
mixed); timing resolution and event semantics, including the timer-response
coincidence cases where hand-rolled implementations diverge; stimulus mappings;
and session structure. This is the layer at which a specification is
simultaneously documentation and executable.

The second piece is a reference implementation, provisionally libBehav, which
parses the format, runs the schedule, and emits standardized event streams.
Written once and tested exhaustively, it would mean that no graduate student
ever hand-rolls a VI schedule again. The reference implementation is also where
formal verification can enter quietly, since the schedule engine can receive
TLA+ or Dafny treatment internally while users simply inherit the correctness.

The third piece is MIABS v2, which would then require deposition of the
specification file. That closes the loop, since the checklist item asking for a
complete schedule specification would by then have both a standard format and a
free tool behind it.

Exit criteria: format specification v1.0; a reference library with Python and
Julia bindings; at least five published papers depositing specification files;
and one journal making deposition a requirement for simulation papers.

## Phase 4: verification layers (2030 onward, opt-in throughout)

The goal of this phase is the heavier machinery, offered as badges for those who
want them rather than as gates.

The first layer is identifiability certification: a pipeline wrapping
StructuralIdentifiability.jl, SIAN, and SMT backends (e.g., Z3 or dReal for
closed-form models), which accepts a model in the exchange format and returns a
machine-checked identifiability report. The Phase 0 preprint would by then have
become routine infrastructure.

The second layer is observational-equivalence proofs, which give SMT-backed
answers to whether two models generate identical predictions under a given
schedule class. Tooling of this kind could turn some molar and molecular
disputes from rhetorical exchanges into dependency graphs.

The third layer is verified hybrid-systems models, in the sense of KeYmaera X
treatment of free-operant preparations. Continuous-time behavior punctuated by
discrete reinforcer deliveries is a formalism that fits the subject matter well,
and it is the natural home for the dynamical-systems program.

The fourth layer is the derivation library, meaning the proof-assistant work of
formalizing roughly 30 core quantitative derivations relative to explicit
assumption modules, in the spirit of reverse mathematics. This is the piece we
have started on first; see `bscilib_roadmap.md`.

## Governance

The working group should number four to six, with theoretical diversity as a
written requirement rather than an aspiration, and should revise the artifacts
annually. All artifacts carry CC-BY or MIT licenses. OSF and GitHub serve as the
institutional home until adoption justifies anything heavier, and SQAB serves as
the annual venue. Forming a society or seeking a trademark before Phase 3 seems
unwise, since premature institutionalization tends to read as a claim to
ownership of a shared research area.

## Risks

The first and most likely failure is that the program ends up with twelve users.
Every design decision should therefore be evaluated against whether it lowers
the cost of the first hundred adoptions. Where correctness and adoptability
conflict before Phase 4, adoptability should win.

The second risk is capture by one theoretical camp. If the artifacts come to be
read as one camp's instrument, they will be dismissed in review regardless of
their merit. The skeptic's seat and the molar-molecular pairing are the
inoculation.

The third risk is premature axiomatization. No ontology should be frozen until
the derivations and the corpus have revealed which primitives recur. The 1965
counterfactual, in which response strength is baked into a foundational layer as
a primitive, remains the cautionary case.

The fourth risk is the founder bottleneck. By Phase 2, at least one artifact
needs a lead who is not me.

The fifth risk is the funding gap. Phases 0 and 1 are inexpensive enough to run
on nights and weekends. Phase 2 likely wants a grant (e.g., NSF methodology or
cyberinfrastructure lines, or SQAB and ABAI seed money), and Phase 3 likely
wants a funded postdoc. In turn, the corpus grant should be written during Phase
1, using the audit paper as its motivation section.

## Sequencing

One plausible compression of the sequence runs: preprint and award-address
close; working group; MIABS v0.1; SQAB symposium; audit paper; MIABS v1.0 in
author guidelines; corpus; grant; exchange format; verification badges;
derivation library.

The constraint that shapes any ordering is recruitment. Everything before the
corpus is achievable by one person with standing, and everything after it
requires the community that the early artifacts bring in. In turn, the practical
question at any given moment is which artifact is most likely to recruit that
community next, and the answer may reasonably change as we learn more. We have
started with the derivation library because its two-tier contribution path
gives people something to do immediately, but that is a working judgment rather
than a finding.
