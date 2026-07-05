# Code Review M2 R1

Review ID: code-review-m2-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: M2. Validation and Representative Fixture Coverage
Reviewed artifact: commit 4ad4d47c
Review date: 2026-07-04
Reviewed commit: 4ad4d47c
Status: changes-requested
Review status: changes-requested
Material findings: TSP-M2-CR1
Recording status: recorded
Recording blocker: none
Reviewed milestone: M2
Milestone closeout: resolution-needed
Required review-resolution: yes
Immediate next stage: review-resolution M2
Verify readiness: not-claimed

## Review inputs

- Diff/review surface: commit `4ad4d47c M2: add test-spec proof contract fixtures`.
- Tracked governing branch state: proposal, spec, plan, test spec, M1 implementation/review, and M2 implementation are tracked through commit `4ad4d47c`.
- Governing artifacts: `specs/test-spec-proof-contract-upgrade.md`, `specs/test-spec-proof-contract-upgrade.test.md`, `docs/plans/2026-07-04-test-spec-proof-contract-upgrade.md`, `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/reviews/test-spec-review-r1.md`.
- Validation evidence: M2 validation notes in `docs/plans/2026-07-04-test-spec-proof-contract-upgrade.md` and `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/change.yaml`.

## Diff summary

M2 adds `validate_test_spec_proof_contract_fixture` to `scripts/skill_validation.py` and representative tests in `scripts/test-skill-validator.py`. The new helper validates command-ledger tables, closed command classifications, required command fields, planned command owner/milestone fields, raw command use without Command IDs, milestone proof-map presence for milestone plans, and command-free non-milestone rationale. Lifecycle artifacts record M2 validation and route the milestone to code-review.

## Findings

### TSP-M2-CR1 - M2 fixtures miss CI-owned and release-owned command proof required by T4

Finding ID: TSP-M2-CR1
Severity: major
Location: `scripts/test-skill-validator.py:1677`
Evidence: The approved test spec assigns T4 to M2 and says representative fixtures include test-running, CI-owned, and release-owned commands. T4 covers R8, R11, R12, EC3, and EC4, including command entries that record zero-test behavior and safe-mode/side-effect boundaries. The M2 valid fixture in `valid_test_spec_proof_contract_output` includes only `existing/configured` and `planned-for-implementation` command rows. The negative tests cover missing ledger, missing/unknown classification, incomplete planned command metadata, missing milestone map, and raw commands without Command IDs, but no M2 fixture directly proves `ci-owned` or `release-owned` command rows with evidence ownership and safe-mode boundary metadata.
Required outcome: M2 representative fixture coverage must directly include CI-owned and release-owned validation-command rows with the required command fields, evidence ownership, zero-test behavior, and safe-mode/side-effect boundary metadata.
Safe resolution path: Extend the representative valid fixture, or add focused positive fixtures, with at least one `ci-owned` command and one `release-owned` command. Map them through Command IDs from test cases or milestone proof rows as appropriate, assert the validator accepts them, and rerun `python scripts/test-skill-validator.py -k test_spec_proof_contract`, `python scripts/test-skill-validator.py -k test_spec`, `python scripts/validate-skills.py skills/test-spec/SKILL.md`, change metadata validation, and artifact lifecycle validation. Then return M2 to `review-requested` for code-review rerun.
needs-decision rationale: none

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | concern | R33/R34 fixture families are mostly implemented, but T4 also assigns CI-owned and release-owned command fixture proof to M2. |
| Test coverage | block | TSP-M2-CR1: the representative positive fixtures do not directly cover CI-owned or release-owned command rows named by T4/EC3/EC4. |
| Edge cases | block | EC3 and EC4 require CI-owned and release-owned command proof; the M2 fixtures only use existing/configured and planned-for-implementation commands. |
| Error handling | concern | Missing, unknown, and incomplete metadata failures are covered; side-effect/evidence ownership for CI/release-owned commands lacks direct positive proof. |
| Architecture boundaries | pass | M2 stays inside repository-owned validation scripts and tests. No architecture boundary or dependency is introduced. |
| Compatibility | pass | The helper is a representative fixture validator and is not wired to enforce all historical test specs. |
| Security/privacy | concern | Safe-mode/side-effect boundary metadata is validated generically, but release-owned and CI-owned proof rows are absent. |
| Derived artifact currency | pass | Generated-output proof is correctly deferred to M3. |
| Unrelated changes | pass | The diff is scoped to M2 validation helpers, tests, and lifecycle handoff artifacts. |
| Validation evidence | concern | The recorded commands passed, but the selected tests do not yet exercise the CI-owned/release-owned positive fixture cases required by T4. |

## Recommended next stage

`review-resolution M2` for `TSP-M2-CR1`, then return M2 to implementation for the targeted fixture additions and rerun code-review.

## Milestone handoff

- Reviewed milestone: M2
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes
- Remaining in-scope implementation milestones: M2, M3
- Next stage: review-resolution M2
- Final closeout readiness: not ready; M2 has an open material finding and M3 remains unimplemented.
