# Code Review M2 R2

Review ID: code-review-m2-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review
Target: M2. Release evidence routing and checklist validation fixtures
Status: clean-with-notes
Reviewed artifact: docs/plans/2026-05-23-release-process-contract.md
Review date: 2026-05-23
Recording status: recorded

## Review inputs

- Diff/review surface:
  - `scripts/validation_selection.py`
  - `scripts/test-select-validation.py`
  - `scripts/artifact_lifecycle_validation.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - `docs/plans/2026-05-23-release-process-contract.md`
  - `docs/plan.md`
  - `docs/changes/2026-05-23-release-process-contract/change.yaml`
  - `docs/changes/2026-05-23-release-process-contract/review-log.md`
  - `docs/changes/2026-05-23-release-process-contract/review-resolution.md`
- Prior finding under re-review: `CR-M2-1`
- Governing spec: `specs/release-process-contract.md`
- Test spec: `specs/release-process-contract.test.md`
- Plan milestone: `docs/plans/2026-05-23-release-process-contract.md#M2. Release evidence routing and checklist validation fixtures`
- Validation evidence recorded by implement/review-resolution:
  - `python scripts/select-validation.py --mode explicit --path docs/releases/v1.2.3.md`
  - `python scripts/select-validation.py --mode explicit --path docs/releases/README.md --path docs/releases/index.md`
  - `python scripts/select-validation.py --mode explicit --path docs/releases/v0.1.5/release.yaml`
  - `python scripts/test-select-validation.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/release-process-contract.test.md --path docs/plans/2026-05-23-release-process-contract.md --path docs/plan.md --path docs/changes/2026-05-23-release-process-contract/change.yaml`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-23-release-process-contract/change.yaml`
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-23-release-process-contract`
  - `git diff --check --`
- Reviewer spot checks:
  - `python scripts/select-validation.py --mode explicit --path docs/releases/v1.2.3.md`
  - `python scripts/select-validation.py --mode explicit --path docs/releases/v0.1.5/release.yaml`

## Diff summary

The CR-M2-1 resolution changes selector routing for flat release evidence files:

- `scripts/validation_selection.py` now detects flat release evidence paths with `_is_flat_release_evidence_path`.
- Flat evidence paths such as `docs/releases/v1.2.3.md` select `artifact_lifecycle.validate` for the evidence file instead of relying only on `release.validate`.
- Directory-style release metadata such as `docs/releases/v0.1.5/release.yaml` still selects `release.validate` and keeps its existing broad-smoke trigger.
- `scripts/test-select-validation.py` now asserts `artifact_lifecycle.validate` directly for the flat release evidence route.
- Review-resolution, plan, and change metadata were updated to record CR-M2-1 as resolved and request M2 re-review.

## Findings

No blocking or required-change findings.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | M2 now satisfies the required route split: flat release evidence selects lifecycle/checklist validation, while directory-style release metadata remains under release validation. |
| Test coverage | pass | `scripts/test-select-validation.py` asserts `artifact_lifecycle.validate` for `docs/releases/v1.2.3.md`; `scripts/test-artifact-lifecycle-validator.py` covers the checklist behavior directly. |
| Edge cases | pass | Direct selector proof shows `manual-routing-required` and `release-version-required` are absent for the flat evidence path, and directory metadata routing remains unchanged. |
| Error handling | pass | Invalid release evidence remains handled by the lifecycle checklist; selector routing now ensures the checklist is selected for the flat evidence path. |
| Architecture boundaries | pass | The fix keeps first-slice validation lightweight and does not introduce a separate release-evidence validator. |
| Compatibility | pass | Existing release-directory behavior for `docs/releases/v0.1.5/release.yaml` still selects `release.validate` and broad smoke. |
| Security/privacy | pass | The checklist route that owns forbidden secret/private-machine marker detection is now selected for the flat evidence file. |
| Derived artifact currency | not applicable | No generated outputs are changed by M2. |
| Unrelated changes | pass | The re-review diff is scoped to selector routing/tests and lifecycle bookkeeping for CR-M2-1. |
| Validation evidence | pass | Targeted selector proof, selector regression tests, lifecycle validator tests, metadata validation, artifact lifecycle validation, and patch hygiene were recorded. |

## No-finding rationale

CR-M2-1 is resolved. A changed `docs/releases/v1.2.3.md` now selects:

```text
artifact_lifecycle.validate -> python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/releases/v1.2.3.md
```

The same spot check shows no `manual-routing-required` or `release-version-required` blockers. A separate directory-style release metadata spot check shows `docs/releases/v0.1.5/release.yaml` still selects `release.validate`, preserving existing release-directory behavior.

## Residual risks

- The release evidence checklist remains intentionally lightweight for this first slice; M3 still owns release-gate command integration and dry-run rehearsal.

## Handoff

- Reviewed milestone: M2. Release evidence routing and checklist validation fixtures
- Review status: clean-with-notes
- Milestone closeout: close M2 and hand off to implement M3
- Remaining implementation milestones: M3, M4
- Required review-resolution: no
