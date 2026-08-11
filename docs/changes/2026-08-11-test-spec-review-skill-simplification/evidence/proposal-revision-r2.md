# Proposal Revision Evidence R2: Test-Spec-Review Skill Simplification

Stage: proposal
Date: 2026-08-11

- Artifact: `docs/proposals/2026-08-11-test-spec-review-skill-simplification.md`
- Prior review: `docs/changes/2026-08-11-test-spec-review-skill-simplification/reviews/proposal-review-r1.md`

## Revision scope

The revision resolves `TSRSIM-PR1` without changing the selected compact-package direction.
It separates durable recording applicability from formal lifecycle settlement authority.

## Finding resolution

| Finding ID | Disposition | Revision |
| --- | --- | --- |
| `TSRSIM-PR1` | accepted | Added `durable_recording_context`, renamed the conditional resource to recording-and-settlement, defined phase-aware loading, required isolated material and blocking records or blocked-recording output, preserved isolated handoff, and added complete static scenarios. |

## Behavioral preservation

- Isolated clean advisory review remains short and does not create lifecycle evidence unless explicitly requested.
- Every isolated material finding loads recording procedure before final output and receives durable evidence or an explicit recording blocker.
- Isolated blocking outcomes receive the detailed record and disposition artifacts required by their governing trigger.
- Loading recording procedure never converts an isolated review into formal lifecycle review and never authorizes implementation handoff.
- Formal lifecycle review and isolated handoff are classified independently, so a direct formal review records and settles its artifact but does not automatically continue.
- Formal review continues to load recording and settlement procedure before review and settles only the matching test-spec artifact entry.
- Boundary-first resource loading, universal proof semantics, status routing, claim boundaries, and target-runtime exclusions are unchanged.

## Validation target

- Proposal trigger, assembly, ownership, missing-resource, scenario, rollout, risk, and decision sections.
- Closed prior finding in `review-resolution.md` and `review-log.md`.
- Change metadata, review-artifact structure and closeout, artifact lifecycle, documentation prose, and diff integrity.
- Independent proposal-review R2.
