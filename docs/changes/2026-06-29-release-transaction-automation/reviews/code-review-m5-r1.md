# Code Review M5 R1

Review ID: code-review-m5-r1
Stage: code-review
Round: M5 R1
Reviewer: Codex code-review skill
Target: M5 commit `3e30bece`
Reviewed artifact: M5 commit `3e30bece`
Reviewed milestone: M5. Full release gate parity and timing evidence
Status: changes-requested
Review status: changes-requested
Review date: 2026-06-29
Recording status: recorded
Material findings: CR-RTA-M5-F1
Immediate next stage: review-resolution

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: docs/changes/2026-06-29-release-transaction-automation/reviews/code-review-m5-r1.md, docs/changes/2026-06-29-release-transaction-automation/review-log.md, docs/changes/2026-06-29-release-transaction-automation/review-resolution.md, docs/plans/2026-06-29-release-transaction-automation.md, docs/plan.md, docs/changes/2026-06-29-release-transaction-automation/change.yaml
- Open blockers: none
- Next stage: review-resolution M5
- Review status: changes-requested
- Material findings: CR-RTA-M5-F1
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-29-release-transaction-automation/reviews/code-review-m5-r1.md
- Review log: docs/changes/2026-06-29-release-transaction-automation/review-log.md
- Review resolution: docs/changes/2026-06-29-release-transaction-automation/review-resolution.md#code-review-m5-r1
- Reviewed milestone: M5. Full release gate parity and timing evidence
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M5 resolution needed, M6
- Required review-resolution: yes
- Finding IDs: CR-RTA-M5-F1
- Verify readiness: not-claimed

## Review Inputs

- Diff range: `HEAD^..HEAD` at `3e30bece`.
- Review surface: `scripts/release_transaction.py`, `scripts/test-release-transaction.py`, `scripts/release-verify.sh`, active plan M5 state, and change metadata validation evidence.
- Governing spec: `specs/release-transaction-automation.md` requirements `R28` through `R30` and `R39` through `R42`.
- Test spec: `specs/release-transaction-automation.test.md` `RTA-T016`, `RTA-T017`, and `RTA-T022`.
- Plan milestone: `docs/plans/2026-06-29-release-transaction-automation.md` M5.
- Validation evidence inspected: M5 plan and change metadata entries for focused release transaction tests, `release-verify.sh` dry-run, Python compilation, selector validation, selected adapter/release regression, `validate-release.py --help`, lifecycle validation, review artifact validation, and whitespace validation.
- Validation spot checks during review: static call-site inspection for `validate_release_timing_evidence`, `validate-release.py`, and `release-verify.sh`.

## Diff Summary

M5 registers `v0.3.5` in `release-verify.sh`, adds timing evidence constants and a `validate_release_timing_evidence` helper, generates a `timing.yaml` skeleton from `prepare-release`, and adds release workflow parity validation. The tests prove the helper behavior, release-verify dry-run command preservation, and static workflow parity.

## Findings

### CR-RTA-M5-F1: Timing evidence validation is not wired into profile-required release validation

Finding ID: CR-RTA-M5-F1
Severity: major
Status: open
Location: `scripts/validate-release.py:100`
Evidence: The spec requires missing timing evidence to fail when the profile requires timing at `specs/release-transaction-automation.md:143` through `specs/release-transaction-automation.md:145`. The approved test spec says timing evidence must be validated "through profile-required release validation" and lists `scripts/validate-release.py` timing tests as the automation location at `specs/release-transaction-automation.test.md:558` through `specs/release-transaction-automation.test.md:566`. M5 adds `validate_release_timing_evidence` in `scripts/release_transaction.py:367` through `scripts/release_transaction.py:453`, but `scripts/validate-release.py:100` through `scripts/validate-release.py:106` still delegates only to `adapter_distribution.validate_release_output`, and `scripts/release-verify.sh:102` through `scripts/release-verify.sh:106` still invokes only `python scripts/validate-release.py ...` for release validation. The new timing tests call the helper directly at `scripts/test-release-transaction.py:936`, `scripts/test-release-transaction.py:947`, `scripts/test-release-transaction.py:957`, and following timing cases, so they prove helper behavior but not the profile-required release validation path. The active M5 plan also records `scripts/validate-release.py` as intentionally unchanged, leaving no maintainer-facing release command that fails when required timing evidence is missing.
Required outcome: Wire timing evidence validation into the repository-owned release validation path used by the full release gate, or revise the approved spec/test spec before claiming M5 closeout.
Safe resolution path: Import and call `validate_release_timing_evidence` from `scripts/validate-release.py` for releases with a release profile that requires timing, append timing errors to the existing release validation errors, print timing warnings without failing duration-over-target cases, and add command-level regression proof that a profile-required release validation fails when `docs/releases/<tag>/timing.yaml` is missing. Preserve historical releases without release profiles unless the profile explicitly requires timing.
needs-decision rationale: none

## Checklist Coverage

| Check | Result | Notes |
| --- | --- | --- |
| Spec alignment | block | `R40` is not satisfied through a release command or validation path; timing failures are helper-only. |
| Test coverage | block | Timing tests directly call `validate_release_timing_evidence`, but `RTA-T022` requires profile-required release validation proof. |
| Edge cases | concern | Missing timing, unknown phases/results, and over-target durations are covered at helper level, but missing timing can still avoid the full release validation command. |
| Error handling | concern | Helper diagnostics are actionable, but they are not surfaced by `validate-release.py` or `release-verify.sh`. |
| Architecture boundaries | pass | The implementation stays within release transaction helpers, tests, and the existing release gate script. |
| Compatibility | concern | `v0.3.5` registration preserves the existing command set, but the new timing requirement is not enforced by the compatibility surface used by maintainers. |
| Security/privacy | pass | No secrets, publication, or network-sensitive behavior is introduced. |
| Derived artifact currency | pass | `prepare-release` generates timing skeleton output and idempotency was updated. |
| Unrelated changes | pass | The diff is scoped to M5 release gate/timing behavior and lifecycle metadata. |
| Validation evidence | concern | Focused tests and dry-run gate checks pass, but they do not exercise timing validation through `validate-release.py`. |

## No-Finding Rationale

Not applicable. This review has one material finding.

## Residual Risks

M6 remains unimplemented and unreviewed. Selector validation still reports manual routing for release transaction scripts; this review does not treat that known selector limitation as the M5 blocker.

## Validation

- Reviewed implementation evidence: `python scripts/test-release-transaction.py` passed with 60 tests.
- Reviewed implementation evidence: `RELEASE_VERIFY_DRY_RUN=1 RELEASE_OUTPUT_DIR=/tmp/rigorloop-release-output RELEASE_COMMIT=fixture-commit bash scripts/release-verify.sh v0.3.5` passed.
- Reviewed implementation evidence: selected adapter/release regression passed.
- Review inspection found no `validate_release_timing_evidence` call from `scripts/validate-release.py` or `scripts/release-verify.sh`.

## Recommended Next Stage

Enter `review-resolution M5`, wire timing evidence validation into the release validation path, add command-level timing regression proof, rerun M5 validation, and return M5 to code review.
