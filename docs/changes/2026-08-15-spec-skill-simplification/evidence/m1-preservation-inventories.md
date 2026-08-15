# M1 Preservation Inventories

- Change: `2026-08-15-spec-skill-simplification`
- Plan: `docs/plans/2026-08-15-spec-skill-simplification.md` at reviewed revision `933c90f4`
- Milestone: M1
- Implementation profile: `IP2-planned-armed`
- Result: implementation evidence complete; code review required

## Completed scope

M1 records 28 semantic rule clusters, 50 exact literal dependencies, 34 deterministic scenarios, two unknown-value fixtures, and the pre-refactor profile and package baseline. The semantic ledger assigns every current or approved replacement rule cluster one disposition and destination. The literal ledger separately distinguishes normative, parser/package, incidental, historical, and obsolete contracts without freezing ordinary prose.

## Tests and proof first

The invalid fixtures use unknown disposition and classification values. CMD1 validates those closed vocabularies before required-field and consistency checks, then validates all real rows, unique IDs, and scenario identities.

## Authored and aligned surfaces

| Surface | Result |
| --- | --- |
| Semantic-rule ledger | Added with one destination per behavioral cluster. |
| Literal-compatibility ledger | Added separately with exact consumers and treatment. |
| Scenario fixtures | Added for profiles, signals, operations, transactions, retries, recovery, partial content, boundary structure, resources, measurement, parity, and acceptance. |
| Profile baseline | Added with canonical identities, words, bytes, both procedural assemblies, skeleton, and total package. |
| `skills/spec/SKILL.md` | Unaffected with rationale: M1 freezes ownership before canonical edits. |
| `skills/spec/references/` | Unaffected with rationale: reference creation and any approved structural adjustment belong to M2. |
| `skills/spec/assets/spec-skeleton.md` | Unaffected with rationale: the conditional insertion point belongs to M2 after baseline review. |
| Permanent validator families | Unaffected with rationale: M1 evidence is change-local and uses the planned standard-library command. |

## Validation

- CMD1: passed after correction with `rules=28 literals=50 scenarios=34 unknown_values=rejected-first`.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-15-spec-skill-simplification/change.yaml`: passed.
- `python scripts/test-skill-validator.py MarkdownReadabilityGuidanceTests`: passed four tests.
- `python scripts/validate-documentation-prose.py --mode audit --path docs/changes/2026-08-15-spec-skill-simplification/evidence/profile-size-baseline.md --path docs/changes/2026-08-15-spec-skill-simplification/evidence/m1-preservation-inventories.md`: passed with no errors or warnings.
- `git diff --check`: passed.

## Handoff

M1 is implementation-complete evidence only. It now routes to formal milestone code review and does not claim milestone closure, later package behavior, generated-resource currency, verification, branch readiness, or PR readiness.

## Accepted correction SPSIM-M1-CR1

The initial-loading rule now has one inline owner, while the compact method and feature-record procedures retain separate reference-owned rows. Every exact universal skeleton heading now has an independent literal classification. No canonical skill, boundary reference, skeleton, spec, plan, workflow contract, validator, or package surface changed.
