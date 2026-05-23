# Code Review M2 R1

Review ID: code-review-m2-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: M2. Release evidence routing and checklist validation fixtures
Status: changes-requested
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
- Governing spec: `specs/release-process-contract.md`
- Test spec: `specs/release-process-contract.test.md`
- Plan milestone: `docs/plans/2026-05-23-release-process-contract.md#M2. Release evidence routing and checklist validation fixtures`
- Validation evidence recorded by implement:
  - `python scripts/test-select-validation.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/release-process-contract.test.md --path docs/plans/2026-05-23-release-process-contract.md --path docs/plan.md --path docs/changes/2026-05-23-release-process-contract/change.yaml`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-23-release-process-contract/change.yaml`
  - `git diff --check -- scripts/validation_selection.py scripts/test-select-validation.py scripts/artifact_lifecycle_contracts.py scripts/artifact_lifecycle_validation.py scripts/test-artifact-lifecycle-validator.py specs/release-process-contract.test.md docs/plans/2026-05-23-release-process-contract.md docs/plan.md docs/changes/2026-05-23-release-process-contract`
- Reviewer spot checks:
  - `python scripts/select-validation.py --mode explicit --path docs/releases/v1.2.3.md`
  - `python scripts/select-validation.py --mode explicit --path docs/releases/README.md --path docs/releases/index.md`

## Diff summary

M2 extends release path handling and adds lightweight checklist validation:

- `scripts/validation_selection.py` infers a release version from `docs/releases/v<version>.md` and routes `docs/releases/README.md` and `docs/releases/index.md` as workflow guidance.
- `scripts/test-select-validation.py` adds selector coverage for the flat release evidence path and release guidance paths.
- `scripts/artifact_lifecycle_validation.py` recognizes `docs/releases/v<version>.md` as a related artifact in lifecycle validation and adds release-evidence checklist checks for required sections, fields, routine gate pass states, registry verification, emergency deferrals, and forbidden secret/private-machine markers.
- `scripts/test-artifact-lifecycle-validator.py` adds positive and negative release evidence fixtures for routine evidence, failed package preview, valid emergency deferral, missing emergency owner, non-deferrable registry verification deferral, and secret-bearing content.
- Plan, plan index, and change metadata were updated to record the M2 implementation handoff.

## Findings

### CR-M2-1

Finding ID: CR-M2-1
Severity: major
Location:
- `scripts/validation_selection.py:934`
- `scripts/validation_selection.py:946`
- `scripts/test-select-validation.py:1282`

Evidence:

The new flat release evidence path is categorized as `release`, but release-category handling selects only `release.validate`:

```text
python scripts/select-validation.py --mode explicit --path docs/releases/v1.2.3.md
```

returned:

```text
selected_checks:
- id: release.validate
  command: python scripts/validate-release-ci.py --version v1.2.3
```

No `artifact_lifecycle.validate` check is selected for `docs/releases/v1.2.3.md`, even though the M2 checklist implementation lives in `scripts/artifact_lifecycle_validation.py`. The selector regression test also asserts only `release.validate` for `docs/releases/v1.2.3.md`.

This conflicts with the M2 goal to ensure `docs/releases/v<version>.md` routes deterministically and that checklist validation can reject missing or unsafe release evidence. It also misses TREL-008's expected result that the path selects the intended release validation/checklist route.

Required outcome:

Changing `docs/releases/v<version>.md` must select the release-evidence checklist validation path that can reject missing or unsafe evidence. The selector test must assert that route directly, not only that `manual-routing-required` and `release-version-required` are absent.

Safe resolution path:

Add selector handling for flat `docs/releases/v<version>.md` evidence files that selects `artifact_lifecycle.validate` for the evidence path, while preserving existing release-directory routing for `docs/releases/<version>/release.yaml`, release notes, and npm publication evidence. Update `scripts/test-select-validation.py` to assert the checklist validation route for `docs/releases/v1.2.3.md`. Keep `release.validate` for historical release-directory artifacts if that remains the current release validation contract.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | concern | The lifecycle checklist code covers required release evidence structure and emergency safety cases, but selector routing does not select that checklist for the new evidence path. |
| Test coverage | concern | Lifecycle validator tests cover the checklist directly, but selector tests assert only `release.validate` for `docs/releases/v1.2.3.md`; they do not prove selected checklist execution for TREL-008. |
| Edge cases | pass | Direct lifecycle fixtures cover routine missing package preview, valid emergency deferral, missing emergency owner, registry-verification deferral, and forbidden secret/private markers. |
| Error handling | pass | Checklist diagnostics fail closed for missing required sections/fields, failed routine gate items, non-deferrable emergency items, and forbidden evidence markers. |
| Architecture boundaries | pass | The implementation keeps a lightweight lifecycle/checklist check and does not introduce a broad dedicated release-evidence validator. |
| Compatibility | pass | Existing release-directory routing remains under `release.validate`; release guidance README/index paths no longer require a package version. |
| Security/privacy | pass | The new forbidden-content fixtures cover token-like and private machine-state markers. |
| Derived artifact currency | not applicable | M2 does not change generated outputs. |
| Unrelated changes | pass | The M2 diff is scoped to selector routing, lifecycle checklist validation, tests, and lifecycle bookkeeping. |
| Validation evidence | concern | The named test suites pass, but the selected-check spot check shows the new evidence path bypasses the implemented checklist. |

## No-finding rationale

Not applicable. This review found one required-change finding.

## Residual risks

- The first-slice checklist is intentionally lightweight and does not yet validate every release evidence rule from the full test spec. That is acceptable for M2 only if the selector actually routes release evidence into the lightweight checklist.

## Handoff

- Reviewed milestone: M2. Release evidence routing and checklist validation fixtures
- Review status: changes-requested
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2 resolution/re-review, M3, M4
- Required review-resolution: yes
- Next stage: review-resolution for CR-M2-1
