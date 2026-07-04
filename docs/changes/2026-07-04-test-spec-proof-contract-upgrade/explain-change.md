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
