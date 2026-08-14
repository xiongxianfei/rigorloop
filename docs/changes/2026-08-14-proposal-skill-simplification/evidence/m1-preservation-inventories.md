# M1 Preservation Inventories

- Change: `2026-08-14-proposal-skill-simplification`
- Plan: `docs/plans/2026-08-14-proposal-skill-simplification.md` at reviewed revision `0f1a25e8`
- Milestone: M1
- Implementation profile: `IP2-planned-armed`
- Result: implementation evidence complete; code review required

## Completed scope

M1 records 25 semantic rule clusters, 29 literal dependencies, 25 deterministic scenarios, two unknown-value fixtures, and the pre-refactor profile and package baseline. The semantic ledger assigns every current rule cluster one disposition and destination. The literal ledger separately distinguishes normative and parser/package contracts without freezing incidental prose.

## Tests and proof first

The invalid fixtures use unknown disposition and classification values. CMD1 validates the closed vocabularies before required-field and consistency checks, then validates all real rows, unique IDs, and scenario identities.

## Authored and aligned surfaces

| Surface | Result |
| --- | --- |
| Semantic-rule ledger | Added with one destination per behavior cluster. |
| Literal-compatibility ledger | Added separately with exact consumers and treatment. |
| Scenario fixtures | Added for assemblies, operations, transactions, recovery, predicates, resources, measurement, parity, and acceptance boundaries. |
| Profile baseline | Added with canonical identities, words, bytes, assemblies, skeleton, and total package. |
| `skills/proposal/SKILL.md` | Unaffected with rationale: M1 freezes ownership before canonical edits. |
| `skills/proposal/assets/proposal-skeleton.md` | Unaffected with rationale: structural changes belong to M2 after baseline review. |
| Permanent validator families | Unaffected with rationale: M1 evidence is change-local and reuses standard-library validation. |

## Validation

- CMD1: passed; `rules=25 literals=29 scenarios=25 unknown_values=rejected-first`.
- Change metadata validation: passed.
- Documentation prose validation: passed with no errors or warnings for M1 Markdown evidence.
- Git diff check: passed.

## Handoff

M1 is implementation-complete evidence only. It is ready for formal milestone code review and does not claim milestone closure, later package behavior, generated-resource currency, verification, branch readiness, or PR readiness.
