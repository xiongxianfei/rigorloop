# Code Review M1 R1 - Compact Change Validation Metadata

Review ID: code-review-m1-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: M1. Compact Shape Recognition And Legacy Compatibility
Reviewed artifact: commit `87c5cd4` (`M1: add compact metadata shape recognition`)
Review date: 2026-05-21
Status: clean-with-notes
Recording status: recorded

## Review inputs

- Diff/review surface: `git show --stat --oneline HEAD`, `git show --name-only --format=fuller HEAD`, and targeted `git show --unified=80 -- scripts/validate-change-metadata.py scripts/test-change-metadata-validator.py`.
- Tracked governing branch state: commit `87c5cd4` includes the proposal, approved spec, active test spec, active plan, change metadata, M1 implementation, and M1 fixtures.
- Governing artifacts:
  - `specs/compact-change-validation-metadata.md`
  - `specs/compact-change-validation-metadata.test.md`
  - `docs/plans/2026-05-21-compact-change-validation-metadata.md`
- Validation evidence:
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/valid-basic/change.yaml`
  - `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compact-valid/change.yaml`
  - `git diff --check --`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-compact-change-validation-metadata`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-21-compact-change-validation-metadata.md --path specs/compact-change-validation-metadata.md --path specs/compact-change-validation-metadata.test.md --path docs/plans/2026-05-21-compact-change-validation-metadata.md --path docs/plan.md --path docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml --path docs/changes/2026-05-21-compact-change-validation-metadata/review-log.md --path docs/changes/2026-05-21-compact-change-validation-metadata/review-resolution.md`
  - `python -m py_compile scripts/validate-change-metadata.py scripts/change_metadata_semantics.py`

## Diff summary

M1 adds compact `schema_version: 2` recognition to `scripts/validate-change-metadata.py`, routing compact files through compact semantic checks while preserving the legacy schema path for non-compact files. The compact branch validates required compact sections, rejects mixed legacy `validation` entries, checks bundle definitions and event bundle references, enforces event result enum values, requires integer structured counts, and requires non-empty `fail`/`blocked` failure details.

The test suite adds a compact valid fixture plus invalid fixtures for missing compact sections, mixed shape, undefined bundle references, invalid result enum values, non-integer counts, and missing `fail`/`blocked` details. The active plan records that these tests failed before implementation and passed after the compact branch landed.

## Findings

No blocking or required-change findings.

## Checklist coverage

| Check | Verdict | Evidence |
| --- | --- | --- |
| Spec alignment | pass | M1 covers approved requirements R1-R7, R25-R28, R33-R42, R57-R58, and R62 within the planned first slice. Later path, summary, count-cross-check, reconstruction, and compactness behavior remains assigned to M2/M3. |
| Test coverage | pass | `scripts/test-change-metadata-validator.py` now covers `TCVM-001` through `TCVM-005` M1 behavior with compact valid and invalid fixtures, while retaining legacy fixture tests. |
| Edge cases | pass | M1 named failures are directly covered: missing compact required sections, mixed shape, undefined bundle, invalid result, non-integer count, and missing fail/blocked details. |
| Error handling | pass | Invalid compact files return actionable path-specific errors such as `validation_events[0].result: expected one of` and `validation_events[0].failures: required when result is fail`. |
| Architecture boundaries | pass | The implementation stays inside existing validator/test/fixture surfaces and does not add a new architecture component or dependency. |
| Compatibility | pass | Non-compact files still flow through the existing JSON-schema and semantic checks; legacy valid fixtures and shipped example validation passed. |
| Security/privacy | pass | M1 does not introduce secret-handling paths, command execution, network access, or new external dependencies. Path safety is intentionally scoped to M2. |
| Derived artifact currency | pass | No generated artifacts are touched. Plan, change metadata, review log, and lifecycle evidence are updated for the M1 handoff. |
| Unrelated changes | pass | The reviewed commit contains the compact-metadata lifecycle artifacts and M1 validator/test/fixture changes. Separate title-case lifecycle-validator edits remain unstaged and outside this review surface. |
| Validation evidence | pass | The milestone validation commands named in the plan and commit body passed, including focused validator tests, direct legacy/compact fixture validation, metadata validation, review-artifact closeout validation, lifecycle validation, syntax compilation, and whitespace checks. |

## No-finding rationale

The implementation is correctly bounded to M1. It adds explicit compact-version branching without weakening the legacy path, and the new fixture tests prove the M1 contract through the public validator CLI. The deliberately deferred behavior from the approved plan, including path interpolation, lifecycle first-exists checks, transcript validation, exact reconstruction, summary derivation, review-artifact count cross-checking, and compactness proof, remains out of this milestone and is tracked in M2/M3.

## Residual risks

- Compact details beyond M1 remain unimplemented by design and must not be treated as complete until M2 and M3 close.
- `failures` detail shape is only checked for non-empty presence in M1 because the approved M1 scope requires required-detail enforcement, while deeper blocker/summary semantics are assigned to later milestones.

## Milestone handoff

- Reviewed milestone: M1. Compact Shape Recognition And Legacy Compatibility
- Review status: clean-with-notes
- Milestone closeout: close M1
- Remaining implementation milestones: M2, M3
- Required review-resolution: no
- Next stage: implement M2
