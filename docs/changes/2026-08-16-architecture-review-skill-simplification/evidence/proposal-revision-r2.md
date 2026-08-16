# Proposal Revision Evidence R2: Architecture Review Skill Simplification

- Stage: proposal
- Date: 2026-08-16
- Artifact ID: `proposal`
- Artifact: `docs/proposals/2026-08-16-architecture-review-skill-simplification.md`
- Prior proposal identity: `sha256:3806497d00f0016f45224b2ea6f0cf18fd4e64f612a47368d084d3901b3ae75a`
- Revised proposal identity: `sha256:2e2e1a457e1691784667f065e1202fbfd3d6eb51f9d7ef3c1bea2bca529b16cf`
- Revision authority: accepted findings `ARRSIM-R2-PR1`, `ARRSIM-R2-PR2`, and `ARRSIM-R2-PR3` from `proposal-review-r2`
- Completion status: complete
- Review request: `proposal-review-r3`

## Resolution summary

| Finding | Revision |
| --- | --- |
| `ARRSIM-R2-PR1` | Separated review subject, governing basis, and settlement targets; defined subjects for every surface; and made every decision-bearing identity part of staleness and retry checks. |
| `ARRSIM-R2-PR2` | Retained one overall semantic status while adding finding-scoped and blocker-scoped target dispositions, unchanged `review-required` behavior, and non-settling `inconclusive` behavior. |
| `ARRSIM-R2-PR3` | Required a complete prepared settlement manifest on existing formal-review evidence before target writes, with pre-state, disposition, expected state, progress, write order, and exact recovery. |

## Architecture condition

The expected result remains provisionally `architecture-not-required` only if existing formal-review evidence can represent the complete governing basis, target dispositions, expected states, and per-target settlement progress. A new persisted transaction record, schema, lifecycle state, or write owner changes the downstream result to `architecture-required`.

## Validation intent

- Every formal surface has one exact subject; record-only surfaces have no settlement targets.
- Judgment reuse requires unchanged subject, governing basis, targets, status, review ID, and round.
- A non-approved occurrence approves no target and mutates only targets supported by finding-scoped or blocker-scoped evidence.
- `inconclusive` and review-occurrence blockers perform no target settlement by default.
- The prepared manifest is durable before mutation and exact retry never reconstructs intent from mutable current state.
- The proposal is ready for independent same-stage rereview and claims no specification or downstream readiness.

## Commands

- `python scripts/validate-change-metadata.py docs/changes/2026-08-16-architecture-review-skill-simplification/change.yaml`
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-08-16-architecture-review-skill-simplification`
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-08-16-architecture-review-skill-simplification`
- `python scripts/validate-documentation-prose.py --mode enforce --path docs/proposals/2026-08-16-architecture-review-skill-simplification.md --path docs/changes/2026-08-16-architecture-review-skill-simplification/reviews/proposal-review-r2.md --path docs/changes/2026-08-16-architecture-review-skill-simplification/reviews/proposal-review-r3.md --path docs/changes/2026-08-16-architecture-review-skill-simplification/evidence/proposal-revision-r1.md --path docs/changes/2026-08-16-architecture-review-skill-simplification/evidence/proposal-revision-r2.md --path docs/changes/2026-08-16-architecture-review-skill-simplification/review-log.md --path docs/changes/2026-08-16-architecture-review-skill-simplification/review-resolution.md`
- `python scripts/validate-markdown-readability.py docs/proposals/2026-08-16-architecture-review-skill-simplification.md docs/changes/2026-08-16-architecture-review-skill-simplification/reviews/proposal-review-r2.md docs/changes/2026-08-16-architecture-review-skill-simplification/reviews/proposal-review-r3.md docs/changes/2026-08-16-architecture-review-skill-simplification/evidence/proposal-revision-r1.md docs/changes/2026-08-16-architecture-review-skill-simplification/evidence/proposal-revision-r2.md docs/changes/2026-08-16-architecture-review-skill-simplification/review-log.md docs/changes/2026-08-16-architecture-review-skill-simplification/review-resolution.md`
- `python scripts/test-documentation-prose-validator.py`
- `python scripts/test-markdown-readability-validator.py`
- `git diff --check`
