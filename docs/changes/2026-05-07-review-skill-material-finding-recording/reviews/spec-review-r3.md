# Spec Review R3

Review ID: spec-review-r3
Stage: spec-review
Round: 3
Reviewer: Maintainer spec-review
Target: specs/rigorloop-workflow.md; specs/review-finding-resolution-contract.md; specs/formal-review-recording.md; CONSTITUTION.md; AGENTS.md; docs/workflows.md
Status: changes-requested

## Scope

Reviewed the spec amendments after the `SR2` and `SR3` resolutions, with emphasis on whether older `review-resolution.md` trigger wording still conflicts with the refined material-finding recording split.

## Findings

### SR4: Standalone review-resolution trigger still reintroduces the broad material-finding rule

Finding ID: SR4

Evidence: `specs/rigorloop-workflow.md:589` through `specs/rigorloop-workflow.md:590` still says a standalone `review-resolution.md` artifact must be used when a non-trivial change has material review findings. That broad trigger conflicts with `specs/rigorloop-workflow.md:579`, `specs/formal-review-recording.md:275`, and `docs/workflows.md:101`, which now say `review-resolution.md` and detailed change-local review files are conditional on material findings requiring disposition or another approved trigger rather than on every material finding.

Required outcome: The standalone `review-resolution.md` trigger must use the refined trigger vocabulary and must not teach that every material finding in a non-trivial change automatically requires `review-resolution.md`.

Suggested resolution: Amend `R12c` so the first trigger is "a non-trivial change has material review findings that require disposition, affect closeout, create follow-up work, drive tracked artifact edits, are reconstructed, or are explicitly requested for durable closeout" or equivalent. Cross-check any acceptance criteria or summaries that still say every material finding requires final disposition in `review-resolution.md`, and scope those statements to findings that require disposition or to review-resolution entries once `review-resolution.md` exists.

## Recommendation

Request changes before approving the spec amendments. This finding is material because it affects when `review-resolution.md` is required and could cause test-spec and implementation to encode the old broad trigger.
