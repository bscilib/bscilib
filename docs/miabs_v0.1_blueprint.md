# MIABS v0.1: blueprint and working draft

MIABS stands for Minimum Information About a Behavioral Simulation. This
document contains the working draft of a one-page reporting checklist for any
published simulation of operant or respondent processes, along with the
reasoning behind each design decision.

The checklist costs an author roughly twenty minutes, costs a journal nothing to
recommend, and creates the vocabulary that every later artifact (i.e., the
corpus, the exchange format, and the verification layers) will inherit. The name
echoes MIAME deliberately, since MIAME's trajectory from community draft to
journal recommendation to de facto requirement within about three years is the
playbook we are following.

## Design constraints

Five constraints are settled up front, on the understanding that they can be
argued about later.

The first is that the checklist fits on one page. If it does not fit, items get
cut rather than shrunk. The moment it begins to look like bureaucracy, adoption
becomes unlikely.

The second is that the checklist reports rather than prescribes. Every item asks
authors to state something, never to do something. Asking an author to state
their timing resolution is uncontroversial; requiring a resolution of 10 ms or
finer starts an argument. Prescription can arrive later, through the corpus, as
evidence rather than by fiat.

The third is that the vocabulary stays theory-neutral. Items should be
answerable in the same way by a momentary-maximizing agent, a molar optimizer, a
Rescorla-Wagner network, and an LLM-driven artificial organism. Any item that
presupposes a framework gets rewritten or cut.

The fourth is that each item earns its place with a failure story. An item is
included only where its absence has demonstrably produced a replication failure,
a hidden confound, or an uninterpretable result. This serves as the working
group's admission test for items, and as our answer to any reviewer asking why a
given item is present.

The fifth is that the document is versioned and provisional. Version 0.1 is
explicitly a draft for public comment, with semantic versioning, a DOI per
version, and archiving on OSF. Humility in the framing should buy some latitude
in the content.

## The draft checklist

Instructions to authors: for each applicable item, state the information in the
manuscript or supplement, or state why it does not apply. "Not applicable" is
always an acceptable answer; silence is not.

### A. Model specification

A1. State every equation or update rule governing the simulated organism,
including all auxiliary assumptions (e.g., response emission mechanism, choice
rule, noise model), rather than only the focal theoretical equation.

A2. List every free parameter with its permissible range, units, and
interpretation, and identify which are fitted, fixed, or derived.

A3. Distinguish observable quantities (e.g., rates, allocations, latencies,
IRTs) from latent state variables (e.g., associative values, memory traces,
activation levels), and state which quantities the predictions are expressed in.

A4. State initial conditions for all state variables, and how they were chosen.

### B. Environment specification

B1. Specify each contingency completely: schedule type and parameters;
interval-timer semantics (i.e., arranged versus obtained, and whether timers
pause, reset, or run during reinforcement); reinforcer parameters (e.g.,
magnitude, duration, delay); and changeover requirements where applicable.

B2. Specify stimulus conditions and their mapping to contingencies, including
any programmed stimulus-consequence relations in respondent preparations (e.g.,
CS and US durations, ISI, ITI distributions).

B3. State session structure: session length or termination criterion, number of
sessions, and any phase transitions along with their criteria.

### C. Temporal structure

C1. State whether time is continuous, discrete, or event-driven. If discrete,
state the time step and either justify that results are insensitive to it or
report the sensitivity.

C2. State how simultaneous events are resolved (e.g., a response coinciding with
an interval timer elapsing), and the order of operations within a time step.

### D. Stochasticity and reproducibility

D1. Identify every source of randomness in the organism and the environment,
with distributions.

D2. Report random seeds, the number of simulated subjects or replicates, and how
variability across replicates is summarized.

D3. Provide runnable code and exact dependency versions sufficient to regenerate
every figure, or state why not.

### E. Parameterization and fitting

E1. State the objective function, fitting algorithm, convergence criteria, and
starting-value strategy.

E2. Report evidence that fitted parameters are recoverable. At minimum, report a
parameter-recovery study (i.e., fit the model to data it generated); where the
model form permits, report a structural identifiability analysis. Report any
confounded or unidentifiable parameters.

E3. If models are compared, state the comparison metric and how model complexity
is accounted for.

### F. Validation scope

F1. List the behavioral phenomena the simulation is claimed to reproduce, with
the qualitative signature of each (i.e., direction, ordering, or functional
form, rather than merely "matches the data").

F2. State known boundary conditions, meaning preparations, schedule ranges, or
phenomena where the model is known or expected to fail.

F3. Distinguish results the model was designed or tuned to produce from results
that emerged without tuning.

### G. Availability

G1. Deposit code, specification files, and generated data in a persistent
repository with a DOI, and state the license.

## Why these items

Every item traces to a documented failure mode, and the abbreviated versions
follow. Items A2 and E2 address parameter confounds discovered only during
fitting, for which structural identifiability tooling makes the check nearly
free. A worked exhibit for this item is still needed; see the note in
`failure_stories.md`. Item A3 addresses latent
constructs smuggled into predictions, which institutionalizes the
response-strength lesson as a reporting requirement rather than as a
prohibition. Items B1 and C2 address hand-rolled VI implementations that diverge
precisely at timer-response coincidences and at the arranged-versus-obtained
distinction, which is plausibly the largest silent source of cross-laboratory
simulation disagreement. Item C1 addresses time-step sensitivity presented as a
theoretical effect. Items D2 and D3 address the ordinary irreproducibility that
the audit paper will attempt to quantify. Item F3 addresses the
overfitting-as-discovery pattern that model comparison sections rarely disclose.

The full failure-story dossier should be kept as a living appendix, since it
serves as the working group's evidence base and as the answer to any reviewer
asking why a particular item is present.

## Build sequence

In week 1, draft against reality. Take the item list above and apply it to three
papers: one of our own simulations, one established paper we admire, and one
recent paper chosen blind. Every item that all three satisfy trivially gets
examined for cutting, and every item all three fail gets its failure story
written. Revise the wording until each item is answerable in one or two
sentences.

In weeks 2 and 3, build the self-audit companion. Run
StructuralIdentifiability.jl on our own discounting models and report what it
finds. If it turns up a confound, that produces the E2 exemplar and the Phase 0
preprint at the same time, so that the checklist and its supporting evidence
ship together.

In week 4, recruit by requesting criticism. Send the one-pager to the five
working-group candidates with a single ask: what is wrong with this, and what is
missing? Incorporate their comments, credit them, and iterate. Their edits are
their buy-in.

In weeks 5 through 8, publish the public draft. Post MIABS v0.1 and the
failure-story appendix on OSF with a DOI and an open comment period. At the same
time, submit the SQAB symposium proposal built around it, and begin the position
paper for *Perspectives on Behavior Science* carrying the argument, with the
checklist itself targeted at *JEAB* as the instrument.

In months 3 through 6, write the audit paper. Apply v0.1 to 20 to 30 published
simulations and report per-item compliance. This is the citation engine and the
motivation section for every future grant.

The deliverables ledger for the first quarter therefore contains the one-page
checklist as PDF and web page; the failure-story appendix; the identifiability
preprint; the OSF project with its DOI; the symposium proposal; and five
annotated responses from working-group candidates.

## What v0.1 deliberately omits

Three things are left out on purpose, and each has a destination.

Required formats or tools are deferred to the Phase 3 exchange format, once the
corpus reveals what needs expressing.

Pass-or-fail thresholds for phenomena are deferred to the Phase 2 benchmark
corpus, where prescription can arrive as evidence.

Ontological commitments, meaning any statement of what counts as a reinforcer,
an operant, or a stimulus class, are deferred until the derivations and the
corpus reveal which primitives recur. The checklist asks authors to define their
terms; it does not define them.

That restraint is the political core of the design. Version 0.1 asks the field
for nothing beyond sentences that a careful author should already have written.
