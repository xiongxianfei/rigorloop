# Code Review M1 Round 2

Review ID: code-review-m1-r2
Stage: code-review
Round: 2
Target: commits `4503926f08627dab6de9a4a238c9ea6a1d23ca9b` and `70a5440ca6aeea08cbbccc852b6ff68b574954cd`
Reviewed milestone: M1. Validation model migration and regression tests
Reviewed artifact: commits `4503926` and `70a5440`
Review date: 2026-05-13
Reviewer: Codex code-review
Recording status: recorded
Status: clean-with-notes

## Outcome

- Review status: clean-with-notes
- Material findings: none
- Blocking findings: none
- Review resolution: closed; `CR-M1-1` accepted and resolved

## Review inputs

- Diff/review surface: `git show 4503926 -- scripts/adapter_distribution.py scripts/test-adapter-distribution.py` and `git show 70a5440 -- scripts/release-verify.sh scripts/test-adapter-distribution.py`
- Governing spec: `specs/stop-tracking-generated-public-adapter-skill-bodies.md`
- Test spec: `specs/stop-tracking-generated-public-adapter-skill-bodies.test.md`
- Active plan: `docs/plans/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies.md`
- Prior review: `reviews/code-review-m1-r1.md`
- Review resolution: `review-resolution.md#code-review-m1-r1`
- Validation evidence recorded in the active plan and commit `70a5440`

## Diff summary

M1 adds v0.1.3 release validation support that validates adapter packages through generated release archives and artifact metadata instead of tracked adapter package trees. It introduces v0.1.3-specific tracked adapter support-surface validation, rejects tracked adapter package fragments, keeps v0.1.2 compatibility-window behavior version-gated, and adds regression tests for release-output validation and tracked package-fragment rejection.

The accepted review finding `CR-M1-1` is resolved by updating `scripts/release-verify.sh` so `v0.1.3` is accepted by the maintainer-facing gate, builds adapter release archives, passes `--release-output-dir` and `--release-commit` to `scripts/validate-release.py`, and skips tracked adapter package drift validation for the retired v0.1.3 repository-tree package model. The new dry-run test proves the exact command selection.

## Findings

No blocking or required-change findings.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | `validate_release_output()` recognizes `v0.1.3`, requires adapter archive metadata for v0.1.3, skips tracked adapter package drift checks for `UNTRACKED_PUBLIC_ADAPTER_RELEASES`, and validates tracked support files plus release archives. |
| Test coverage | pass | `test_v0_1_3_release_validation_uses_release_output_not_tracked_adapter_tree`, `test_v0_1_3_release_validation_rejects_tracked_adapter_package_fragments`, and `test_release_verify_script_supports_v0_1_3_archive_only_gate` cover the named M1 behavior. |
| Edge cases | pass | Direct tests cover the positive archive-output path, rejection of tracked package fragments, required archive metadata, and dry-run release-gate command selection. |
| Error handling | pass | Missing support files, tracked package fragments, missing release-output directory, archive validation errors, artifact metadata errors, and release-note errors produce explicit validation errors. |
| Architecture boundaries | pass | The release gate now delegates v0.1.3 adapter package proof to generated release archives while keeping `dist/adapters/README.md` and `manifest.yaml` as tracked support surfaces. |
| Compatibility | pass | v0.1.1 and v0.1.2 behavior remains version-gated; v0.1.2 still uses the compatibility manifest version and tracked adapter checks. |
| Security/privacy | pass | The diff does not introduce secrets or unsafe credential handling; release notes and metadata paths continue through existing security scans. |
| Derived artifact currency | pass | M1 changes validation and release-gate logic only; it does not remove generated adapter package files yet. That removal belongs to M2. |
| Unrelated changes | pass | The reviewed implementation commits are scoped to the approved M1 validation model and its lifecycle evidence. |
| Validation evidence | pass | The plan records passing targeted and full adapter distribution tests, skill validation, generated v0.1.3 archive validation, and v0.1.3 release-verify dry-runs. |

## No-finding rationale

The first-pass review finding was narrow: the direct validator supported v0.1.3, but the maintainer-facing release gate still rejected it. Commit `70a5440` closes that gap and adds direct proof for the exact gate command. The remaining M1 behavior matches the approved boundary: validation is migrated before tracked adapter package removal, v0.1.2 compatibility behavior remains intact, and M2-M4 retain their planned scope.

## Residual risks

- Full `bash scripts/release-verify.sh v0.1.3` against final release evidence is still an M4 gate; M1 only proves the validation model and dry-run release-gate routing.
- `docs/learn/sessions/2026-05-13-release-version-gate.md` is an untracked artifact from a separate learn invocation and is outside this M1 review surface.

## Recommended next stage

Close M1 and proceed to `implement M2`.
