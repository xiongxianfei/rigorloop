# M1 Preservation Inventories

- Change: `2026-08-16-architecture-review-skill-simplification`
- Plan: `docs/plans/2026-08-16-architecture-review-skill-simplification.md` at reviewed revision `fdaed65e`
- Milestone: M1
- Implementation profile: `IP2-planned-armed`
- Result: implementation evidence complete; code review required

## Completed scope

M1 records 20 semantic rule clusters, 20 compatibility-sensitive literals, 26 deterministic scenarios, two unknown-value fixtures, one prepared formal-review manifest capability fixture, and the pre-refactor profile baseline. Unknown owner and literal-classification values are rejected before row consistency is considered.

The manifest fixture proves that existing detailed Markdown review evidence can carry subject identity, governing-basis identity, target pre-state, disposition, expected post-state, and per-target settlement progress. No new parsed schema, lifecycle state, persistent transaction artifact, or write owner is required.

## Authored and aligned surfaces

| Surface | Result |
| --- | --- |
| Rule ledger | Added with one owner, destination, requirement set, and proof set per cluster. |
| Literal ledger | Added separately with exact classifications and dispositions, including the cross-skill shared literal. |
| Scenario fixtures | Added for assemblies, authority, subjects, dispositions, recording, preparation, recovery, compatibility, measurement, parity, and architecture escalation. |
| Evidence-capability fixture | Added a prepared settlement record using the existing formal-review evidence surface. |
| Profile baseline | Added canonical identity, words, bytes, all four pre-extraction assemblies, and total package. |
| `skills/architecture-review/` | Unaffected with rationale: canonical edits belong to M2 after M1 review. |

## Validation

- Initial `python scripts/test-skill-validator.py ArchitectureReviewSkillSimplificationLedgerTests`: failed four tests because the planned ledgers, scenarios, manifest, and baseline did not yet exist.
- Final `python scripts/test-skill-validator.py ArchitectureReviewSkillSimplificationLedgerTests`: passed four tests.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-16-architecture-review-skill-simplification/change.yaml`: passed.
- `python scripts/validate-documentation-prose.py --mode enforce --path docs/changes/2026-08-16-architecture-review-skill-simplification/evidence/profile-size-baseline.md --path docs/changes/2026-08-16-architecture-review-skill-simplification/evidence/m1-preservation-inventories.md`: passed with zero errors and zero warnings.
- `git diff --check`: passed.

## Handoff

M1 is implementation-complete evidence only. It is ready for formal milestone code review and does not claim milestone closure, package behavior, verification, or branch readiness.
