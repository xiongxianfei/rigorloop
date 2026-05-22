# Code Review M5 R1 - Plan Archive Validation Routing

Review ID: code-review-m5-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: M5. Selection and CI routing
Reviewed artifact: commit `ffa9826`
Review date: 2026-05-22
Status: clean-with-notes
Recording status: recorded

## Review inputs

- Diff/review surface: `ffa9826 M5: route plan archive validation`
- Plan: `docs/plans/2026-05-22-bounded-plan-index-and-completed-plan-archive.md`
- Spec: `specs/plan-index-lifecycle-ownership.md`
- Test spec: `specs/plan-index-lifecycle-ownership.test.md`
- Implementation files: `scripts/validation_selection.py`, `scripts/test-select-validation.py`
- Validation evidence recorded in the plan and change metadata
- Direct review probes for `docs/plan.md`, `docs/plan-archive.md`, and `docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/plan-index-migration.md`

## Diff summary

M5 teaches the validation selector about the new plan archive surface and migration proof. `docs/plan.md` and `docs/plan-archive.md` are now paired plan-index surfaces that select `artifact_lifecycle.validate` with both paths. `docs/changes/<change-id>/plan-index-migration.md` is now a supported change-local lifecycle artifact that selects lifecycle validation with the migration proof, its governing `change.yaml`, and both plan index surfaces. Selector regression tests cover the standalone archive route, migration-proof route, representative category table, and broader workflow surface set.

## Findings

No material findings.

## Checklist coverage

| Check | Verdict | Evidence |
| --- | --- | --- |
| Spec alignment | pass | `R15` requires terminal-plan conservation whenever `docs/plan.md` or `docs/plan-archive.md` changes; standalone selector probes for both surfaces select `artifact_lifecycle.validate` with `docs/plan.md` and `docs/plan-archive.md`. |
| Test coverage | pass | `ValidationSelectionTests.test_plan_index_surfaces_select_lifecycle_validation_with_both_surfaces` and `test_plan_index_migration_proof_routes_with_metadata_and_index_surfaces` prove the new routes directly. The full `python scripts/test-select-validation.py` suite passed. |
| Edge cases | pass | Standalone `docs/plan.md`, standalone `docs/plan-archive.md`, and standalone migration-proof edits were probed. The migration-proof route includes its governing `change.yaml` plus both plan index surfaces. |
| Error handling | pass | Existing selector blocking behavior for unclassified paths is unchanged; the new plan-index routes remove a previous manual block only for known contract surfaces. |
| Architecture boundaries | pass | The change stays inside selector classification/routing and selector tests; no lifecycle validator behavior or CI scheduler behavior is changed. |
| Compatibility | pass | Existing representative category and workflow-refactor selector tests were updated to include `docs/plan-archive.md` while preserving expected checks for unrelated categories. |
| Security/privacy | pass | The diff adds deterministic path classification and tests only; no secrets, credentials, private paths, network calls, or unsafe logging are introduced. |
| Derived artifact currency | pass | No generated skill or adapter output is touched. |
| Unrelated changes | pass | The diff is scoped to selector code, selector tests, and M5 handoff/evidence artifacts. |
| Validation evidence | pass | Targeted selector tests, full selector regression, `py_compile`, selector CLI proof, selected CI explicit mode, change metadata validation, artifact lifecycle validation, and `git diff --check --` passed. |

## No-finding rationale

The implementation satisfies the M5 scope: archive/index surface edits now select lifecycle validation, migration-proof edits select lifecycle validation with the proof, governing metadata, and both index surfaces, and unrelated selector behavior remains covered by existing regression tests. The CI wrapper did not need code changes because the explicit selected-CI run executes the selected `artifact_lifecycle.validate` and `selector.regression` checks.

## Residual risks

Final lifecycle closeout and final broad validation remain M6 work. This review does not claim branch readiness, PR readiness, final verification, or CI status.

## Handoff

Close M5 and proceed to M6 implementation. This review does not claim branch readiness, PR readiness, final verification, or CI status.
