# M1 Preservation Inventories

- Milestone: M1
- Status: implementation complete; review required
- Rules: `ci-maintenance-rule-disposition.yaml`
- Literals: `ci-maintenance-literal-compatibility.yaml`
- Scenarios: `fixtures/scenarios.yaml`
- Baseline: `evidence/profile-size-baseline.md`
- Architecture trigger: absent; all R53 trigger values are recorded as absent.
- Correction: CIMSIM-CR1 expanded the rule ledger to explicit R1-R54 and CIM-R1-CIM-R65 rows and enumerated assembly, result, consumer, and placeholder literals.
- Unchanged with rationale: `skills/ci-maintenance/SKILL.md` and its packaged resources remain byte-identical because M1 freezes ownership before package mutation.

Validation:

- `python scripts/test-skill-validator.py CiMaintenanceSkillSimplificationTests`: required and passing.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-19-ci-maintenance-skill-simplification/change.yaml`: required and passing.
