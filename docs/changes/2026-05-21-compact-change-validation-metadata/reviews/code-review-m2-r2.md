# Code Review M2 R2 - Compact Change Validation Metadata

Review ID: code-review-m2-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review
Target: M2. Path Variables, Lifecycle Stages, And Transcript References
Reviewed artifact: commit `76e9f87` (`Resolve M2 bundle command safety review finding`)
Review date: 2026-05-21
Status: clean-with-notes
Recording status: recorded

## Review inputs

- Diff/review surface: commit `76e9f87`, including `scripts/validate-change-metadata.py`, `scripts/test-change-metadata-validator.py`, compact unsafe-command fixtures, and review-resolution/plan/change-metadata updates for CVM-M2-CR1.
- Prior material finding: `CVM-M2-CR1` from `reviews/code-review-m2-r1.md`.
- Governing artifacts:
  - `specs/compact-change-validation-metadata.md`
  - `specs/compact-change-validation-metadata.test.md`
  - `docs/plans/2026-05-21-compact-change-validation-metadata.md`
- Validation evidence recorded for the fix:
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compact-valid/change.yaml`
  - `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/valid-basic/change.yaml`
  - expected-failure direct checks for unsafe local path, credential-bearing URL, and secret-like bundle commands
  - `python -m py_compile scripts/validate-change-metadata.py scripts/change_metadata_semantics.py`
  - `git diff --check --`
  - active change metadata, review-artifact closeout, and lifecycle explicit-path validation after resolution recording

## Diff summary

The CVM-M2-CR1 resolution adds string-level safety validation for compact `validation_bundles.<id>.command` values without executing those commands. The validator now rejects credential-bearing URLs, secret-like command values, home-directory tokens, Windows absolute paths, and path-like tokens that resolve to unsafe repository paths. The fix wires this safety check into compact bundle definition validation, keeps valid repo-relative commands with compact path variables accepted, and adds fixture-backed coverage for unsafe local path, credential URL, and secret-like bundle command failures.

## Findings

No blocking or required-change findings.

## Checklist coverage

| Check | Verdict | Evidence |
| --- | --- | --- |
| Spec alignment | pass | The fix closes the M2 security/privacy gap by validating compact bundle command strings for unsafe local paths, credential-bearing URLs, and secret-like values while preserving the accepted compact bundle model. |
| Test coverage | pass | `scripts/test-change-metadata-validator.py` includes fixture checks for unsafe bundle-command local paths, credential-bearing URLs, and secret-like values, plus helper coverage for `$HOME` and Windows absolute command tokens. |
| Edge cases | pass | Valid repo-relative commands and compact path-variable references remain accepted through the updated `compact-valid` fixture. |
| Error handling | pass | Diagnostics name the bundle field path and unsafe category, such as `validation_bundles.unsafe_credentials.command contains credential-bearing URL`, without echoing credential-bearing command strings. |
| Architecture boundaries | pass | The implementation remains in the existing change-metadata validator and fixture suite, with no new dependency, command execution path, or selector behavior change. |
| Compatibility | pass | Legacy valid metadata and compact valid metadata both passed the recorded direct validation commands. |
| Security/privacy | pass | The new command safety check is lexical only, rejects the unsafe classes required by CVM-M2-CR1, and does not execute bundle commands. |
| Derived artifact currency | pass | Review-resolution, review-log, active plan, and change metadata were updated for the M2 review-resolution handoff before rerun review. |
| Unrelated changes | pass | Unstaged lifecycle title-case validator edits and untracked learn artifacts remain outside this M2 rerun review surface. |
| Validation evidence | pass | The recorded M2 rerun evidence covers the targeted validator suite, valid compact/legacy fixtures, expected-failure unsafe command fixtures, syntax compilation, whitespace, active metadata, review-artifact closeout, and lifecycle validation. |

## No-finding rationale

The rerun directly addresses CVM-M2-CR1 without broadening M2. The fix validates bundle-command strings as command templates rather than treating the entire command as a path, avoids command execution, provides stable non-leaking diagnostics, and preserves ordinary repo-relative validation commands. The remaining compact evidence-consistency work is still correctly assigned to M3.

## Residual risks

- M3 remains responsible for path-set reconstruction, summary derivation, duplicate stage checks, skipped/not-run blocker handling, review-artifact count cross-checking, and compactness proof.
- This review does not claim final branch, verify, CI, or PR readiness.

## Milestone handoff

- Reviewed milestone: M2. Path Variables, Lifecycle Stages, And Transcript References
- Review status: clean-with-notes
- Milestone closeout: close M2
- Remaining implementation milestones: M3
- Required review-resolution: no
- Next stage: implement M3
