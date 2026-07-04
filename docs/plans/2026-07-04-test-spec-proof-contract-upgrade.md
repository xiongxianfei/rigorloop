# Test-Spec Proof-Contract Upgrade Plan

## Status

Plan lifecycle state: active
Terminal disposition: none

- Owner: maintainer
- Change ID: 2026-07-04-test-spec-proof-contract-upgrade
- Start date: 2026-07-04
- Last updated: 2026-07-04
- Related issue or PR: none yet
- Supersedes: none

## Goal

Upgrade the `test-spec` skill contract so future test specs explicitly record command ownership, input identities, milestone proof timing, and command-linked evidence before implementation relies on them.

## Why now

The accepted proposal and approved spec identify a repeated proof-authoring gap: command ownership and milestone proof timing can be discovered by `test-spec-review` after authoring instead of being built into the authoring structure.

## Scope

### In scope

- Update `skills/test-spec/SKILL.md` for input artifact identities, validation commands, milestone proof maps, and strengthened test-case fields.
- Update `skills/test-spec/assets/test-spec-skeleton.md`.
- Update `skills/test-spec/assets/test-case.md`.
- Add `skills/test-spec/assets/validation-command-row.md`.
- Add `skills/test-spec/assets/milestone-proof-row.md`.
- Add validation or representative fixture coverage for command ledger and milestone proof-map structure.
- Record behavior-preservation evidence.
- Prove generated skill and adapter inclusion from canonical sources.

### Out of scope

- Manual-proof contracts and `assets/manual-proof.md`.
- Executing validation commands during `test-spec` authoring.
- Implementing production behavior outside authored skill, asset, validator, fixture, and generated-output proof surfaces.
- Historical migration of existing test specs.
- Hand-editing generated adapter output.

## Constraints

- Follow `specs/test-spec-proof-contract-upgrade.md`.
- Preserve the test-spec artifact status model and `test-spec-review` route.
- Keep policy in `skills/test-spec/SKILL.md`; assets own reusable structure.
- Do not exceed the spec-family asset amendment: only `validation-command-row.md` and `milestone-proof-row.md` are newly authorized for `test-spec`.
- Use repository-owned validation scripts before downstream readiness claims.

## Source artifacts

- Proposal: `docs/proposals/2026-07-04-test-spec-proof-contract-upgrade.md`
- Proposal review: `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/reviews/proposal-review-r1.md`
- Spec: `specs/test-spec-proof-contract-upgrade.md`
- Spec review: `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/reviews/spec-review-r1.md`
- Architecture: not required, recorded in `spec-review-r1`
- Test spec: `specs/test-spec-proof-contract-upgrade.test.md`

## Requirements covered

| Requirement IDs | Plan coverage |
| --- | --- |
| R1-R12 | M1 updates skill policy, skeleton, test-case asset, and command-row asset; M2 adds validation proof. |
| R13-R14 | M1 adds input artifact identity guidance and skeleton structure. |
| R15-R20 | M1 adds milestone proof-map guidance and asset; M2 adds validation proof. |
| R21-R26 | M1 updates and adds assets plus resource-map entries. |
| R27-R29 | M1 preserves Manual QA behavior and excludes manual-proof asset work; M3 behavior-preservation verifies. |
| R30-R32 | M1 preserves status and claim boundaries; M3 behavior-preservation verifies. |
| R33-R34 | M2 adds representative validation coverage. |
| R35 | M3 records generated skill and adapter inclusion proof. |
| R36 | M3 records no historical migration proof. |

## Current Handoff Summary

- Current milestone: M3. Generated Output and Behavior Preservation Proof
- Current milestone state: planned
- Latest review evidence: code-review-m2-r2
- Last reviewed milestone: M2
- Review status: approved; stage=code-review; round=r2
- Remaining in-scope implementation milestones: M3
- Next stage: implement M3
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: lifecycle-gates-open, implementation-milestones-open, milestone-review-pending, explain-change-pending, verify-pending, pr-handoff-pending — plan-review, test-spec, test-spec-review, implementation milestones, code-review, explain-change, verify, and PR handoff have not completed.

## Milestones

### M1. Skill Contract and Asset Structure

- Milestone state: closed
- Goal: update authored `test-spec` guidance and packaged structures for the new proof contract.
- Requirements: R1-R32.
- Likely files:
  - `skills/test-spec/SKILL.md`
  - `skills/test-spec/assets/test-spec-skeleton.md`
  - `skills/test-spec/assets/test-case.md`
  - `skills/test-spec/assets/validation-command-row.md`
  - `skills/test-spec/assets/milestone-proof-row.md`
  - `scripts/skill_validation.py` (aligned allowlist only)
  - `scripts/test-skill-validator.py` (aligned fixture only)
- Implementation steps:
  - Add `Input artifact identities`, `Validation commands`, and `Milestone proof map` guidance.
  - Add command classification and command-ledger rules.
  - Strengthen test-case format with Command IDs, evidence artifact, and required milestone.
  - Update resource map with the new assets.
  - Preserve Manual QA behavior and exclude manual-proof contracts.
- Validation:
  - `python scripts/validate-skills.py skills/test-spec/SKILL.md`
  - `python scripts/test-skill-validator.py -k test_spec`
- Rollback: revert `skills/test-spec/` edits from this milestone.
  Also revert the aligned spec-family asset allowlist fixture edits in `scripts/skill_validation.py` and `scripts/test-skill-validator.py`.

### M2. Validation and Representative Fixture Coverage

- Milestone state: closed
- Goal: add deterministic proof for command ledger, command classification, planned command ownership, milestone proof map, and command ID references.
- Requirements: R7, R33, R34.
- Likely files:
  - `scripts/skill_validation.py`
  - `scripts/test-skill-validator.py`
  - fixture files under existing skill-validator or artifact-lifecycle fixture locations as selected during implementation
- Implementation steps:
  - Add asset/resource-map shape checks for the new sections and assets.
  - Add representative positive and negative fixtures for command ledger and milestone proof-map requirements.
  - Avoid broad semantic scoring.
- Validation:
  - `python scripts/test-skill-validator.py -k test_spec`
  - `python scripts/validate-skills.py skills/test-spec/SKILL.md`
- Rollback: revert validator and fixture additions from this milestone.

### M3. Generated Output and Behavior Preservation Proof

- Milestone state: planned
- Goal: prove generated output includes the revised skill and assets and that protected behavior is preserved.
- Requirements: R27-R32, R35, R36.
- Likely files:
  - `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/behavior-preservation.md`
  - generated-output evidence under the change root, if needed
  - generated mirrors or temporary adapter outputs only through repository-owned scripts
- Implementation steps:
  - Record behavior-preservation evidence for role, status model, review route, Manual QA behavior, historical migration boundary, and no generated hand edits.
  - Build or check generated skills.
  - Validate adapter output includes mapped assets from canonical sources.
- Validation:
  - `python scripts/build-skills.py --check`
  - `python scripts/test-build-skills.py`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-skills.py`
- Rollback: revert generated-proof artifacts and any generated-output changes produced by repository-owned scripts.

## Validation plan

- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/test-spec-proof-contract-upgrade.md --path docs/plans/2026-07-04-test-spec-proof-contract-upgrade.md --path docs/plan.md --path docs/changes/2026-07-04-test-spec-proof-contract-upgrade/change.yaml`
- `python scripts/validate-change-metadata.py docs/changes/2026-07-04-test-spec-proof-contract-upgrade/change.yaml`
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-07-04-test-spec-proof-contract-upgrade`
- Milestone-specific validation commands listed above.
- Final selected validation will be refined by the matching test spec.

## Risks and recovery

- Risk: proof-contract sections make small test specs too heavy.
  - Recovery: preserve explicit not-applicable rationale paths for command-free and non-milestone specs.
- Risk: assets drift from skill policy.
  - Recovery: validate resource-map entries and asset field shape.
- Risk: generated output drifts from canonical assets.
  - Recovery: run repository-owned build and adapter validation scripts; do not hand-edit generated output.
- Risk: manual-proof scope leaks back in.
  - Recovery: enforce AC9/R28 and record any manual-proof work as a separate proposal.

## Dependencies

- Approved spec `specs/test-spec-proof-contract-upgrade.md`.
- Clean `spec-review-r1`.
- Plan-review before test-spec authoring.
- Test-spec and test-spec-review before implementation.

## Progress

- 2026-07-04: plan created after accepted proposal and approved spec.
- 2026-07-04: plan-review-r1 approved the plan with no material findings; next stage is test-spec.
- 2026-07-04: test spec authored and marked active; next stage is test-spec-review.
- 2026-07-04: test-spec-review-r1 approved the active test spec with no material findings; implementation handoff is allowed for M1.
- 2026-07-04: M1 implementation started; scope is limited to authored `test-spec` skill text and packaged assets.
- 2026-07-04: M1 updated `test-spec` skill policy, skeleton, test-case asset, validation-command row asset, milestone-proof row asset, and the aligned spec-family asset allowlist needed for validation.
- 2026-07-04: M1 targeted validation passed; milestone is ready for `code-review`.
- 2026-07-04: code-review-m1-r1 completed clean-with-notes; M1 closed and next stage is implement M2.
- 2026-07-04: M2 implementation started; scope is representative fixture validation for command ledger, command classifications, planned command metadata, milestone proof-map presence, and Command ID references.
- 2026-07-04: M2 added representative proof-contract fixture validation for valid ledgers, missing ledger entries, missing and unknown classifications, incomplete planned commands, missing milestone proof maps, raw commands without Command IDs, and command-free non-milestone rationale.
- 2026-07-04: M2 targeted validation passed; milestone is ready for `code-review`.
- 2026-07-04: code-review-m2-r1 requested changes for `TSP-M2-CR1`; M2 needs review-resolution and targeted fixture additions before rereview.
- 2026-07-04: `TSP-M2-CR1` accepted and resolved by adding CI-owned and release-owned representative command fixture rows; M2 is ready for code-review rerun.
- 2026-07-04: code-review-m2-r2 completed clean-with-notes; M2 closed and next stage is implement M3.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-07-04 | Use three implementation milestones. | The change has separate skill/asset, validation, and generated-output proof concerns. | One oversized implementation milestone. |
| 2026-07-04 | Keep manual-proof work out of all milestones. | The accepted proposal and approved spec exclude manual-proof contracts. | Add `assets/manual-proof.md` opportunistically. |
| 2026-07-04 | Align the spec-family asset allowlist in M1. | `validate-skills.py` blocks the new approved `test-spec` assets until the allowlist recognizes them. | Defer the allowlist to M2 and leave M1 validation failing. |

## Surprises and discoveries

- `python scripts/validate-skills.py skills/test-spec/SKILL.md` initially failed because `scripts/skill_validation.py` still allowed only the old three `test-spec` assets. The allowlist and its positive fixture were updated narrowly for the two approved new assets.

## Validation notes

- 2026-07-04: `python scripts/validate-skills.py skills/test-spec/SKILL.md` passed.
- 2026-07-04: `python scripts/test-skill-validator.py -k test_spec` passed.
- 2026-07-04: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/test-spec-proof-contract-upgrade.md --path specs/test-spec-proof-contract-upgrade.test.md --path docs/plans/2026-07-04-test-spec-proof-contract-upgrade.md --path docs/plan.md --path docs/changes/2026-07-04-test-spec-proof-contract-upgrade/change.yaml` passed.
- 2026-07-04: `code-review-m1-r1` found no material findings; no material review-resolution required for M1.
- 2026-07-04: `python scripts/test-skill-validator.py -k test_spec_proof_contract` failed before implementation because `validate_test_spec_proof_contract_fixture` did not exist.
- 2026-07-04: `python scripts/test-skill-validator.py -k test_spec_proof_contract` passed after adding the representative proof-contract fixture validator.
- 2026-07-04: `python scripts/test-skill-validator.py -k test_spec` passed.
- 2026-07-04: `python scripts/validate-skills.py skills/test-spec/SKILL.md` passed.
- 2026-07-04: `code-review-m2-r1` found `TSP-M2-CR1`; CI-owned and release-owned positive fixture proof is missing.
- 2026-07-04: `python scripts/test-skill-validator.py -k test_spec_proof_contract` passed after resolving `TSP-M2-CR1`.
- 2026-07-04: `python scripts/test-skill-validator.py -k test_spec` passed after resolving `TSP-M2-CR1`.
- 2026-07-04: `python scripts/validate-skills.py skills/test-spec/SKILL.md` passed after resolving `TSP-M2-CR1`.
- 2026-07-04: `python scripts/test-skill-validator.py -k test_spec_proof_contract` passed during code-review-m2-r2.
- 2026-07-04: `code-review-m2-r2` found no material findings; M2 closed.

## Outcome and retrospective

- Pending downstream lifecycle completion.

## Readiness

- See `Current Handoff Summary`.
