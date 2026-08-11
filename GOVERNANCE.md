# Governance

This document is deliberately written early, while the project has one
contributor and a handful of theorems. Agreeing on how decisions get made is
inexpensive before there is anything to disagree about, and considerably more
expensive afterward.

## Working group

BSciLib is governed by a working group of four to six members.

Theoretical diversity is a requirement of membership rather than an aspiration.
The working group should at all times include at least one member who works
within molar accounts, at least one who works within molecular accounts, and at
least one member who is publicly skeptical of the formalization program itself.

The skeptic's seat deserves a word of explanation, since it may look like
decoration. It is not. If these artifacts come to be read as one theoretical
camp's instrument, they will be dismissed in review regardless of their
technical merit, and a skeptic's objections are the cheapest available way to
find out where that risk lies. Should a departure leave any of those three
perspectives unrepresented, filling that seat takes priority over other
recruitment.

## How decisions get made

Whether a proof is correct is not a governance question. The Lean kernel settles
it, and no vote or maintainer preference overrides `lake build`. Governance
covers the questions the kernel cannot answer.

| Decision | How it is made |
|---|---|
| Merging a pull request | Any maintainer, once continuous integration passes and the review standards in `CONTRIBUTING.md` are met |
| Accepting or rejecting a statement card | Working group, by rough consensus |
| Adding or changing what an assumption module claims about its empirical standing | Working group, by rough consensus |
| Changing the assumption policy in `docs/assumptions.md` | Unanimous working group |
| Tagged releases and their author lists | Working group |

Rough consensus means that no sustained objection remains after discussion,
rather than a count of votes. Objections are recorded in the relevant card or
issue whether or not they carry the day.

The third row deserves note, because it is the most consequential kind of edit
the library admits. Changing what an assumption module says about its own
empirical standing changes how every downstream result should be read, and such
changes therefore warrant more discussion than a new theorem does.

## Rejections are kept

A rejected statement card stays in `cards/` with a status of `rejected` and a
note giving the reasoning. Keeping a record of what the working group declined
to include, and why, is useful to the project and gives a straightforward answer
to anyone who later asks why a particular idea is absent.

## Revision

The working group reviews the assumption policy, the card lifecycle, and this
document annually. Every tagged release receives a DOI and lists contributors as
authors.

## What we are not doing yet

There is no society, trademark, membership, or fee associated with BSciLib, and
we do not intend to create one in the near term. Forming institutions before
there is a community to institutionalize tends to read as a claim to ownership
of a shared research area, which would work against what the project is trying
to do. This is worth revisiting once the exchange-format work is underway.

## Succession

By the time BSciLib reaches its second tagged release, we would like at least
one flagship theorem to have been formalized by someone other than the founding
maintainer, and at least one artifact in the organization to have a lead who is
not the founding maintainer. Dependence on a single person is the most likely
way for a project of this kind to stall, and these two markers are how we plan
to notice the problem while it is still easy to fix.
