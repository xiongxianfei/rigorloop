# Code Review M2 R1

Review ID: code-review-m2-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: commit `cacf1b1`
Status: changes-requested

## Review inputs

- Review surface: commit `cacf1b1` (`M2: add script output contract tests`).
- Governing artifacts: `specs/script-output-optimization.md`, `specs/script-output-optimization.test.md`, and M2 in `docs/plans/2026-05-21-script-output-optimization.md`.
- Implementation evidence: `scripts/test-select-validation.py`, `docs/changes/2026-05-21-script-output-optimization/behavior-preservation.md`, active plan validation notes, and `change.yaml`.
- Validation evidence recorded for M2: `python scripts/test-select-validation.py`, lifecycle validation, change metadata validation, selector inspection, diff check, and selected CI.

## Diff summary

M2 adds `ScriptOutputContractTests` and `ScriptOutputFixtureTests` to `scripts/test-select-validation.py`. The new tests exercise the script through subprocess invocations for default success, default failure, verbose, quiet, conflicting flags, zero-test behavior, rerun behavior, and JSON deferral. The plan and behavior-preservation evidence were updated to record the M2 test-suite extension.

No output formatter implementation was added in M2.

## Findings

### SRO-M2-CR1: Contract tests are masked as expected failures

Finding ID: SRO-M2-CR1
Severity: major
Location: `scripts/test-select-validation.py:150`

Evidence: The formatter-dependent M2 tests are decorated with `@unittest.expectedFailure` at lines 150, 161, 184, 194, 206, 222, and 232. As a result, `python scripts/test-select-validation.py` exits successfully while the old runner still violates default success, default failure, quiet success/failure, conflicting flag, zero-test, and reliable rerun expectations. The approved M2 plan says the expected observable result is that tests "fail for the old noisy default output and pass only when the approved output contract and preservation checks are satisfied." TSRO-002 through TSRO-008 define these as executable integration tests with failure proving contract violations, not as permanently green expected-failure markers.

Required outcome: M2 must provide contract tests or proof commands that fail against the old output contract and become ordinary passing validation once M3 implements the formatter. Normal validation for M3 must not be able to pass while any required formatter behavior remains hidden as an expected failure.

Safe resolution path: Remove `@unittest.expectedFailure` from contract tests that are intended to become acceptance tests, or move the intentionally failing pre-M3 proof into a separate explicit red-test command/artifact that is not counted as passing validation. If a temporary expected-failure mechanism is kept, add an executable guard that fails M2/M3 validation when any required output-contract case remains expected-failing after implementation.

## Checklist coverage

- Spec alignment: concern. The M2 tests cover approved behavior names, but expected-failure decorators mask unmet requirements in the normal test command.
- Test coverage: concern. Several tests assert the right contract shape but do not fail the suite while the implementation is wrong.
- Edge cases: concern. Quiet mode, conflict flags, zero-test safety, and reliable rerun behavior are represented but expected-failing, so validation can stay green with those edge cases unmet.
- Error handling: concern. Combined output flag handling is expected-failing rather than enforced by a failing proof.
- Architecture boundaries: pass. M2 changes tests and lifecycle evidence only; no production formatter or wrapper architecture changed.
- Compatibility: pass. No production behavior changed in M2.
- Security/privacy: pass. Test fixtures use static test names and messages; no sensitive values are introduced.
- Derived artifact currency: pass. No generated artifacts were changed.
- Unrelated changes: pass. The diff is scoped to M2 test additions and lifecycle evidence for the same initiative.
- Validation evidence: concern. Recorded validation passes, but it passes with seven expected failures that correspond to required output-contract behavior.

## No-finding rationale

Not applicable; one material finding was found.

## Handoff

Reviewed milestone: M2. Output contract tests
Review status: changes-requested
Milestone closeout: resolution-needed
Required review-resolution: yes
Next stage: review-resolution for `SRO-M2-CR1`
Remaining implementation milestones: M2 resolution, M3, M4 when triggered, M5
Verify readiness: not-claimed
