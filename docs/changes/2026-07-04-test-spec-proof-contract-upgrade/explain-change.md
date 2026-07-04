# Explain Change: Test-Spec Proof-Contract Upgrade

## Status

Draft implementation reasoning. Final `explain-change` stage has not run.

## M1 implementation notes

M1 updates the authored `test-spec` skill and assets so future test specs start from the proof-contract structures approved in `specs/test-spec-proof-contract-upgrade.md`.

Changed surfaces:

- `skills/test-spec/SKILL.md` now defines conditional `Input artifact identities`, `Validation commands`, and `Milestone proof map` authoring rules, adds the closed command classification enum, strengthens test-case fields, and preserves the `test-spec-review` route and claim boundary.
- `skills/test-spec/assets/test-spec-skeleton.md` now includes the input identity, validation-command, and milestone proof-map sections.
- `skills/test-spec/assets/test-case.md` now includes `Command IDs`, `Evidence artifact`, and `Required by milestone`.
- `skills/test-spec/assets/validation-command-row.md` and `skills/test-spec/assets/milestone-proof-row.md` provide repeated structures for the new proof-contract rows.
- `scripts/skill_validation.py` and `scripts/test-skill-validator.py` were updated only to keep the existing spec-family asset allowlist aligned with the approved `test-spec` asset inventory amendment.

Manual-proof contracts remain out of scope. No `assets/manual-proof.md` was added, and existing Manual QA checklist behavior remains unchanged.

## M1 validation

- `python scripts/validate-skills.py skills/test-spec/SKILL.md`: passed.
- `python scripts/test-skill-validator.py -k test_spec`: passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/test-spec-proof-contract-upgrade.md --path specs/test-spec-proof-contract-upgrade.test.md --path docs/plans/2026-07-04-test-spec-proof-contract-upgrade.md --path docs/plan.md --path docs/changes/2026-07-04-test-spec-proof-contract-upgrade/change.yaml`: passed.

## M2 implementation notes

M2 adds representative fixture validation for the new test-spec proof-contract shape without turning it into broad historical test-spec enforcement.

Changed surfaces:

- `scripts/skill_validation.py` now exposes `validate_test_spec_proof_contract_fixture`, a static representative-output helper that checks validation-command ledger structure, closed command classifications, planned-command owner and milestone metadata, raw command use without Command IDs, missing ledger entries, milestone proof-map presence for milestone-based plans, and command-free non-milestone rationale.
- `scripts/test-skill-validator.py` now includes representative positive and negative fixture tests for the command ledger and milestone proof-map requirements approved for M2.

## M2 validation

- `python scripts/test-skill-validator.py -k test_spec_proof_contract`: failed before implementation because the representative validator did not exist.
- `python scripts/test-skill-validator.py -k test_spec_proof_contract`: passed after implementation.
- `python scripts/test-skill-validator.py -k test_spec`: passed.
- `python scripts/validate-skills.py skills/test-spec/SKILL.md`: passed.

## M2 review-resolution notes

`code-review-m2-r1` found `TSP-M2-CR1`: the representative valid fixture did not directly prove CI-owned and release-owned command rows required by T4, EC3, and EC4.

Resolution:

- Added `ci-owned` and `release-owned` validation-command rows to the representative valid fixture.
- Referenced those commands from milestone proof-map rows and test cases.
- Updated the missing-milestone-map negative fixture to remove the complete milestone proof-map table structurally.

Validation:

- `python scripts/test-skill-validator.py -k test_spec_proof_contract`: passed.
- `python scripts/test-skill-validator.py -k test_spec`: passed.
- `python scripts/validate-skills.py skills/test-spec/SKILL.md`: passed.

## M3 implementation notes

M3 records preservation and generated-output proof for the completed `test-spec` skill upgrade.

Changed surfaces:

- `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/behavior-preservation.md` records that the `test-spec` role, status model, review route, Manual QA behavior, no-manual-proof boundary, no historical migration boundary, and generated-output handling remain aligned with the approved spec.
- `docs/plans/2026-07-04-test-spec-proof-contract-upgrade.md`, `docs/plan.md`, and `change.yaml` now record M3 validation evidence and the handoff to `code-review M3`.

## M3 validation

- `python scripts/build-skills.py --check`: passed.
- `python scripts/test-build-skills.py`: passed.
- `python scripts/test-adapter-distribution.py`: passed.
- `python scripts/validate-skills.py`: passed.
- `python scripts/validate-change-metadata.py docs/changes/2026-07-04-test-spec-proof-contract-upgrade/change.yaml`: passed.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-07-04-test-spec-proof-contract-upgrade`: passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/test-spec-proof-contract-upgrade.md --path specs/test-spec-proof-contract-upgrade.test.md --path docs/plans/2026-07-04-test-spec-proof-contract-upgrade.md --path docs/plan.md --path docs/changes/2026-07-04-test-spec-proof-contract-upgrade/change.yaml --path docs/changes/2026-07-04-test-spec-proof-contract-upgrade/behavior-preservation.md`: passed.
