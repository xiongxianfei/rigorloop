# M2 Package Implementation

- Milestone: M2
- Result: implementation-complete; ready for code review
- Canonical common path: `skills/plan-review/SKILL.md`
- Governed procedure: `skills/plan-review/references/governed-plan-review-settlement.md`
- Structural assets: `assets/review-result-skeleton.md` and `assets/material-finding.md`

The common path retains universal plan judgment, recording safety, evidence discipline, boundary scanning, statuses, stops, claims, and handoff. Candidate validation, the initial-review transaction, identity-bound settlement retry, recovery, and workflow-managed procedure have one conditional owner. Output labels live only in the two mapped assets.

Tests were added before the resources existed and initially failed on the missing reference and assets. The implementation then satisfied the focused package, transaction, output, boundary, recording, readability, independence, and lifecycle contracts.

## Validation

- `python scripts/validate-skills.py skills/plan-review/SKILL.md`: passed.
- `python scripts/test-skill-validator.py`: passed, 323 tests with 16 skipped.
- `python scripts/test-build-skills.py`: passed, 7 tests.
- `python scripts/build-skills.py --check`: passed.

## Compatibility treatment

Tests that previously expected output fields inline now inspect their structural asset owner. The plan-review automation-manifest test now inspects the governed reference rather than preserving conditional procedure in the common path. Shared boundary, recording, evidence-efficiency, independence, lifecycle-settlement, and closed-vocabulary contracts remain enforced.

## Claim limitations

M2 does not claim final package parity, completed measurements, holistic review, verification, branch readiness, or PR readiness. Those belong to M3 and later gates.
