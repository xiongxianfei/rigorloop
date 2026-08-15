# M1 Preservation Inventories

- Change: `2026-08-15-architecture-skill-simplification`
- Plan: `docs/plans/2026-08-15-architecture-skill-simplification.md` at reviewed revision `0145d6b9`
- Milestone: M1
- Implementation profile: `IP2-planned-armed`
- Result: implementation evidence complete; code review required

## Completed scope

M1 records 20 semantic rule clusters, 20 compatibility-sensitive literals, four asset treatments covering exactly three assets, 18 deterministic scenarios, two unknown-value fixtures, and the pre-refactor profile and package baseline. Unknown owner and literal-classification values are rejected before row consistency is considered.

## Authored and aligned surfaces

| Surface | Result |
| --- | --- |
| Rule ledger | Added with one owner, destination, requirement set, and proof set per cluster. |
| Literal ledger | Added separately with exact classifications and dispositions. |
| Asset ledger | Added with structural, literal-style, and method-owned treatment. |
| Scenario fixtures | Added for classifications, assessment basis, preparation, dependencies, recovery, assets, measurement, parity, and architecture escalation. |
| Profile baseline | Added with canonical identities, words, bytes, procedural assemblies, copied assets, and total package. |
| `skills/architecture/` | Unaffected with rationale: canonical edits belong to M2 after M1 review. |

## Validation

- `python scripts/test-skill-validator.py ArchitectureSkillSimplificationLedgerTests`: passed four tests.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-15-architecture-skill-simplification/change.yaml`: passed before implementation and remains workflow-owned.
- `git diff --check`: passed.

## Handoff

M1 is implementation-complete evidence only. It is ready for formal milestone code review and does not claim milestone closure, package behavior, verification, or branch readiness.
