# Proposal Revision Evidence R1: Architecture Review Skill Simplification

- Stage: proposal
- Date: 2026-08-16
- Artifact ID: `proposal`
- Artifact: `docs/proposals/2026-08-16-architecture-review-skill-simplification.md`
- Prior proposal identity: `sha256:19987383c3cf5da56e92a883ac34bd7bb255a171c595768e251954884689a4b8`
- Revised proposal identity: `sha256:3806497d00f0016f45224b2ea6f0cf18fd4e64f612a47368d084d3901b3ae75a`
- Revision authority: accepted findings `ARRSIM-PR1`, `ARRSIM-PR2`, and `ARRSIM-PR3` from `proposal-review-r1`
- Completion status: complete
- Review request: `proposal-review-r2`

## Resolution summary

| Finding | Revision |
| --- | --- |
| `ARRSIM-PR1` | Classified the exact shared isolation and recording subsection as a normative cross-skill literal, preserved it inline, and limited the new recording reference to architecture-review-specific mechanics. |
| `ARRSIM-PR2` | Replaced open settlement and automation axes with six valid recording, artifact-settlement, and execution combinations plus an exhaustive side-effect and handoff matrix. |
| `ARRSIM-PR3` | Made no-impact and proposal/spec-gap surfaces unconditionally review-evidence-only, restricted settlement to exact existing canonical architecture and ADR targets, and closed target-state mapping and physical retry. |

## Architecture condition

The expected result remains `architecture-not-required` only if existing authoring evidence already records the intended accepted state for each governed ADR and existing formal-review evidence supports exact physical retry. The proposal adds no rationale artifact, schema, lifecycle state, persistence surface, or write owner.

## Validation

- The shared `## Isolation and Recording` block remains a byte-identical inline compatibility requirement and is not assigned to the new reference.
- Every permitted authority combination has explicit recording, settlement, automation-evidence, isolation, and handoff behavior; every unlisted combination stops.
- No-impact rationale and proposal/spec-gap review cannot create or settle lifecycle targets.
- Governed settlement is limited to exact existing canonical architecture and ADR entries at `review-required` with matching identities and authoring evidence.
- Interrupted settlement permits exact physical retry but no partial semantic approval or downstream eligibility.
- The revised proposal is ready for independent same-stage rereview and claims no specification or downstream readiness.

## Commands

- `python scripts/validate-change-metadata.py docs/changes/2026-08-16-architecture-review-skill-simplification/change.yaml`
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-08-16-architecture-review-skill-simplification`
- `python scripts/validate-documentation-prose.py --mode enforce --path docs/proposals/2026-08-16-architecture-review-skill-simplification.md --path docs/changes/2026-08-16-architecture-review-skill-simplification/evidence/proposal-revision-r1.md --path docs/changes/2026-08-16-architecture-review-skill-simplification/review-resolution.md`
- `python scripts/validate-markdown-readability.py docs/proposals/2026-08-16-architecture-review-skill-simplification.md docs/changes/2026-08-16-architecture-review-skill-simplification/evidence/proposal-revision-r1.md docs/changes/2026-08-16-architecture-review-skill-simplification/review-resolution.md`
- `python scripts/test-documentation-prose-validator.py`
- `python scripts/test-markdown-readability-validator.py`
- `git diff --check`
