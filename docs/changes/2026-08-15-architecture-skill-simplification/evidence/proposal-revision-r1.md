# Proposal Revision Evidence R1: Architecture Skill Simplification

Stage: proposal
Date: 2026-08-15
Artifact ID: `proposal`
Artifact: `docs/proposals/2026-08-15-architecture-skill-simplification.md`
Revision authority: accepted findings `ARSIM-PR1`, `ARSIM-PR2`, and `ARSIM-PR3` from `proposal-review-r1`
Completion status: complete
Review request: `proposal-review-r2`

## Resolution summary

| Finding | Revision |
| --- | --- |
| `ARSIM-PR1` | Separated isolated and workflow-managed assessment, semantic judgment, route result, completion receipt fields, ambiguity pause, and direct explicit-path recording. |
| `ARSIM-PR2` | Replaced the single create/revise axis with an ordered per-target manifest, four target-local operations, three batch results, exact retry identity, and complete-manifest review eligibility. |
| `ARSIM-PR3` | Added a complete asset-content disposition that retains structure and literal styles while moving method applicability and adequacy rules into the method reference. |

## Compatibility decisions

- Workflow-managed required and not-required assessment receipts retain `Stage: architecture-assessment`, `Applicability: required | not-required`, and exact `Spec identity`.
- `architecture-ambiguous` remains a workflow-owned pause and does not become a completed assessment receipt or new parser value.
- Direct assessment no longer mutates a proposal, spec, plan, PR, or change record implicitly; it may write only to one explicit valid evidence path.
- Combined canonical and ADR authoring uses existing authoring evidence and artifact entries rather than a new persisted batch state.
- The package continues shipping exactly the existing three assets, but policy-bearing skeleton text receives explicit disposition instead of assumed byte preservation.

## Validation

- `python scripts/validate-change-metadata.py docs/changes/2026-08-15-architecture-skill-simplification/change.yaml`
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-08-15-architecture-skill-simplification`
- `python scripts/validate-documentation-prose.py --mode enforce --path docs/proposals/2026-08-15-architecture-skill-simplification.md --path docs/changes/2026-08-15-architecture-skill-simplification/evidence/proposal-revision-r1.md`
- `git diff --check`

The revised proposal is ready for independent same-stage rereview and claims no specification or downstream readiness.
