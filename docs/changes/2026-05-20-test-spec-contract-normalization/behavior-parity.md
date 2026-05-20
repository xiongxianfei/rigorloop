# Behavior Parity: Test-Spec Contract Normalization

## Scope

This evidence covers the representative `test-spec` input named by T37:

- accepted [Test-Spec Contract Normalization proposal](../../proposals/2026-05-20-test-spec-contract-normalization.md);
- approved [Skill Contract](../../../specs/skill-contract.md);
- active [Test-Spec Contract Normalization Plan](../../plans/2026-05-20-test-spec-contract-normalization.md).

The parity target is structural and contractual: `test-spec` must produce the same kind of test specification with the same required sections, test-case format, coverage maps, stop conditions, and output obligations after normalization.

## Representative Output Comparison

| Artifact surface | Before normalization | After normalization | Parity result |
| --- | --- | --- | --- |
| Frontmatter routing description | Routes test-spec generation from an approved feature spec and execution plan. | Unchanged text. | preserved |
| Stop conditions | Two blockers in `Rules`: unreviewed/unstable spec unless isolated output is requested and limitation recorded; `not-ready`/`not-assessed` spec-review outcome. | Same two blockers surfaced in `Stop conditions`; removed from `Rules` to avoid duplicate authority. | preserved |
| Required section set | 19 required sections. | Same 19 required sections, unchanged in the numbered list and reflected in the skeleton. | preserved |
| Test-case format | `T1. Title` plus Covers, Level, Fixture/setup, Steps, Expected result, Failure proves, Automation location. | Same format preserved in the original format block and reflected in the skeleton. | preserved |
| Requirement coverage map | Every requirement ID maps to tests or explicit manual verification. | Same obligation preserved in required sections, coverage rules, and skeleton. | preserved |
| Example coverage map | Every example maps to a test when feasible. | Same obligation preserved in required sections and skeleton. | preserved |
| Edge case coverage | Required section plus coverage obligations for boundary and error behavior. | Same obligation preserved in required sections, coverage rules, and skeleton. | preserved |
| Coverage rules | `MUST`, error behavior, migration/compatibility, architecture boundaries, and bug regression coverage. | Rule text unchanged. | preserved |
| Durable test-spec states | `draft`, `active`, `abandoned`, `superseded`, `archived`; no durable `reviewed` or long-lived `complete`. | State rule unchanged and reflected in skeleton status placeholder. | preserved |
| Artifact placement lookup | Same lookup order and stop-on-ambiguity behavior. | Same lookup order; wording adjusted to remain project-portable under normalized readability validation. | preserved |

## Representative Test-Spec Shape

For the representative proposal/spec/plan input, the generated test spec is still expected to contain:

1. Status
2. Related spec and plan
3. Testing strategy
4. Requirement coverage map
5. Example coverage map
6. Edge case coverage
7. Test cases
8. Fixtures and data
9. Mocking/stubbing policy
10. Migration or compatibility tests
11. Observability verification
12. Security/privacy verification
13. Performance checks
14. Manual QA checklist
15. What not to test and why
16. Uncovered gaps
17. Next artifacts
18. Follow-on artifacts
19. Readiness

The skeleton uses the same section names. No material output change is introduced.

## Validation Evidence

- `python scripts/validate-skills.py skills/test-spec/SKILL.md` passed after adding readability metadata and structure.
- `python scripts/test-skill-validator.py` passed after preserving the static artifact-lookup wording expected by existing repository validation.

## Parity Statement

The normalization changes how the skill exposes its contract to readers, not what the skill asks the agent to produce. The representative input remains governed by the same required sections, coverage maps, test-case format, stop conditions, and readiness wording obligations.
