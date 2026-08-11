# Proposal Revision Evidence R2: Proposal-Review Skill Simplification

Stage: proposal
Date: 2026-08-11
Artifact: `docs/proposals/2026-08-11-proposal-review-skill-simplification.md`
Prior review: `docs/changes/2026-08-11-proposal-review-skill-simplification/reviews/proposal-review-r1.md`

## Revision scope

The revision resolves `PRSIM-PR1` without changing the selected two-reference package design.

It also corrects two existing proposal-contract omissions discovered during the author-owned revision: the `Vision fit` section now starts with the exact closed-vocabulary value, and the broad public-skill and validation-policy change now includes explicit initial-intent and scope-budget tables.

## Finding resolution

| Finding ID | Disposition | Revision evidence |
| --- | --- | --- |
| `PRSIM-PR1` | accepted | The conditional proposal-gates section now defines observable positive and forbidden evidence for `vision_exception_context`, `standing_artifact_context`, and `scope_budget_context`; combined predicates load one reference and apply every active gate; late-discovered evidence triggers loading before status selection; unresolved ambiguity blocks approval. |

## Additional contract corrections

- `Vision fit` now uses `fits the current vision` as its first non-empty line.
- `Initial intent preservation` classifies every initial user goal with the closed treatment vocabulary.
- `Scope budget` classifies the core package change, same-slice contract and proof dependencies, architecture assessment, and excluded cross-skill or runtime work.
- Static scenarios now include positive, forbidden, combined, late-trigger, and ambiguity cases.

## Validation target

The revised proposal, review resolution, change metadata, artifact lifecycle, review-artifact structure, Markdown readability contract, and diff hygiene must pass before independent R2 review.

## Authoring result

The proposal is ready for independent `proposal-review` R2. It does not claim acceptance, specification completion, implementation readiness, final verification, branch readiness, or PR readiness.
