# Code Review M2 R1 - Compact Change Validation Metadata

Review ID: code-review-m2-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: M2. Path Variables, Lifecycle Stages, And Transcript References
Reviewed artifact: commit `57a6994` (`M2: add compact path and lifecycle validation`)
Review date: 2026-05-21
Status: changes-requested
Recording status: recorded

## Review inputs

- Diff/review surface: commit `57a6994`, including `scripts/validate-change-metadata.py`, `scripts/test-change-metadata-validator.py`, compact fixtures, and M2 plan/change metadata updates.
- Tracked governing branch state: committed proposal, approved spec, approved test spec, active plan, M1 review closeout, and M2 implementation evidence through `57a6994`.
- Governing artifacts:
  - `specs/compact-change-validation-metadata.md`
  - `specs/compact-change-validation-metadata.test.md`
  - `docs/plans/2026-05-21-compact-change-validation-metadata.md`
- Validation evidence:
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compact-valid/change.yaml`
  - `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/valid-basic/change.yaml`
  - expected-failure direct checks for unresolved variables, missing transcript references, and unknown lifecycle stages
  - `python -m py_compile scripts/validate-change-metadata.py scripts/change_metadata_semantics.py`
  - `git diff --check --`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-compact-change-validation-metadata`
  - lifecycle explicit-path validation for the active change artifacts

## Diff summary

M2 adds compact path-variable resolution, derived `slug`, closed `{var}` interpolation with doubled-brace literals, unsafe path detection, lifecycle-stage enum checks, first-exists filesystem checks, event path validation, optional transcript-reference validation, and fixture coverage for the M2 failure cases. It keeps legacy metadata on the existing schema path and leaves reconstruction, summary derivation, and count cross-checking for M3.

## Findings

### CVM-M2-CR1 - Bundle command safety is not validated

Finding ID: CVM-M2-CR1
Severity: major
Location: `scripts/validate-change-metadata.py` compact bundle validation; `scripts/test-change-metadata-validator.py` M2 fixture coverage
Evidence: The approved spec's security/privacy section says validators MUST reject machine-local paths and credential-bearing references in path variables, bundle commands, event paths, and transcript references. The M2 plan also names bundle commands in the path safety implementation step. In the implementation, `validate_compact_bundle_definitions` checks only that `command` is a non-empty string and that optional fields are strings; it never calls `validate_repo_relative_path` or an equivalent bundle-command safety check. The M2 tests cover unsafe path variables and transcript references, but there is no compact fixture proving an unsafe bundle command is rejected.
Required outcome: Compact validation must reject unsafe bundle command strings that contain machine-local paths, hostnames, credentials, proxy URLs, or secret-like values, without executing the commands or changing command selection behavior.
Safe resolution path: Add a focused invalid compact fixture with an unsafe `validation_bundles.<id>.command` value, add it to `scripts/test-change-metadata-validator.py`, and extend compact bundle validation to apply the approved safety checks to command strings.

## Checklist coverage

| Check | Verdict | Evidence |
| --- | --- | --- |
| Spec alignment | block | M2 implements most path/lifecycle requirements, but misses the spec security/privacy rule for bundle command safety. |
| Test coverage | block | M2 adds broad fixture coverage for path variables, lifecycle stages, canonical paths, and transcripts, but no test proves unsafe bundle commands fail. |
| Edge cases | concern | Named M2 edge cases are mostly covered; bundle-command unsafe values are an untested in-scope edge case from the security/privacy boundary. |
| Error handling | pass | Existing invalid compact fixtures produce actionable validator messages for unresolved variables, lifecycle stages, missing transcript files, and first-exists failures. |
| Architecture boundaries | pass | The implementation stays inside existing validator, test, and fixture surfaces with no new dependency or runtime component. |
| Compatibility | pass | Legacy valid metadata still validates through the legacy schema/semantic path. |
| Security/privacy | block | Bundle commands can currently contain machine-local or credential-bearing values without compact validation rejecting them. |
| Derived artifact currency | pass | No generated artifacts are involved; plan and change metadata were updated for M2 handoff. |
| Unrelated changes | pass | Reviewed commit `57a6994` contains M2 validator/test/fixture/lifecycle evidence only. Unstaged lifecycle title-case edits and untracked learn artifacts remain outside this review surface. |
| Validation evidence | concern | The recorded validation commands are relevant, but they do not exercise the unsafe bundle-command case. |

## No-finding rationale

Not applicable; the review found one material M2 issue.

## Residual risks

- M3 remains responsible for path-set reconstruction, summary derivation, duplicate stage checks, skipped/not-run blocker handling, review-artifact count cross-checking, and compactness proof.
- This review does not claim final branch, verify, CI, or PR readiness.

## Milestone handoff

- Reviewed milestone: M2. Path Variables, Lifecycle Stages, And Transcript References
- Review status: changes-requested
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2 fixes, then M3
- Required review-resolution: yes
- Next stage: review-resolution for CVM-M2-CR1
