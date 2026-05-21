# Code Review M3 R1

Review ID: code-review-m3-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: commit `72a4452`
Status: changes-requested

## Review inputs

- Review surface: commit `72a4452` (`M3: shape test-select-validation output`).
- Governing artifacts: `specs/script-output-optimization.md`, `specs/script-output-optimization.test.md`, and M3 in `docs/plans/2026-05-21-script-output-optimization.md`.
- Implementation evidence: `scripts/test-select-validation.py`, `docs/changes/2026-05-21-script-output-optimization/behavior-preservation.md`, `script-output-audit.md`, `output-contract-red-test.md`, active plan validation notes, and `change.yaml`.
- Validation evidence recorded for M3: output-contract command, default/verbose/quiet/conflict/JSON/zero-test/failure checks, selected-test hash proof, artifact lifecycle validation, change metadata validation, selector inspection, diff check, and selected CI.

## Diff summary

M3 adds a script-local unittest runner adapter in `scripts/test-select-validation.py`. The adapter parses `--verbose`, `--quiet`, `-k`, and explicit test names; rejects conflicting output flags; captures result data for compact default and quiet output; preserves full unittest output in verbose mode; fails zero-test runs; emits reliable scoped rerun commands; and leaves `--json` unsupported. It also updates M3 audit and behavior-preservation evidence plus plan and change metadata state.

## Findings

### SRO-M3-CR1: Output-contract tests are still excluded from ordinary post-M3 validation

Finding ID: SRO-M3-CR1
Severity: major
Location: `scripts/test-select-validation.py:2970`

Evidence: `load_tests` still filters `ScriptOutputContractTests` out of ordinary discovery at lines 2970-2979. The M3 evidence records `python scripts/test-select-validation.py` passing `63` tests, while `python scripts/test-select-validation.py ScriptOutputContractTests` is a separate command that runs the `10` output-contract cases. That means the normal selector regression command can pass without executing the required default success, default failure, quiet, conflict, zero-test, rerun, and JSON-deferral acceptance tests in `ScriptOutputContractTests`. The approved test spec says the automation location for TSRO-002 through TSRO-009 is `python scripts/test-select-validation.py`, and the M2 review-resolution required M3 validation not to be able to pass while required output-contract cases remain outside ordinary passing validation.

Required outcome: After M3, ordinary validation must exercise the required output-contract acceptance cases, or an equivalent ordinary validation guard must fail when any required output-contract case fails. The default selected CI path must not be able to pass while `ScriptOutputContractTests` fails.

Safe resolution path: Remove or revise the `load_tests` filter now that the formatter exists, then update the expected ordinary test count and behavior-preservation evidence. If keeping the class excluded is intentional, add a default-suite test that invokes `ScriptOutputContractTests` and fails ordinary validation on any output-contract failure, and record why that is equivalent. Rerun `python scripts/test-select-validation.py`, the explicit output-contract command if retained, selected CI, lifecycle validation, change metadata validation, and diff check.

## Checklist coverage

- Spec alignment: concern. Output behavior itself matches the named contract in direct validation, but the ordinary validation path does not execute the required output-contract tests.
- Test coverage: concern. TSRO-002 through TSRO-009 pass when run explicitly, but are excluded from `python scripts/test-select-validation.py`.
- Edge cases: concern. Quiet, conflict-flag, zero-test, rerun, and JSON-deferral edge cases are not covered by the default selector regression path after M3.
- Error handling: pass for implemented behavior. Direct evidence shows combined flags fail before tests run, zero-test fails, and loader failures omit misleading scoped reruns.
- Architecture boundaries: pass. The diff is scoped to the approved first-slice runner and change-local evidence; `scripts/ci.sh` remains untouched.
- Compatibility: concern. The post-M3 regression command can miss output-contract regressions unless the acceptance tests join ordinary validation.
- Security/privacy: pass. Failure formatting includes test names, messages, and repository-relative file locations; no secrets or environment dumps are introduced.
- Derived artifact currency: pass. No generated artifacts are changed.
- Unrelated changes: pass. The diff is scoped to M3 implementation and lifecycle evidence.
- Validation evidence: concern. Recorded validation is relevant, but it relies on a separate explicit command for required output-contract cases that ordinary selected CI does not run.

## No-finding rationale

Not applicable; one material finding was found.

## Handoff

Reviewed milestone: M3. Test-select-validation output shaping
Review status: changes-requested
Milestone closeout: resolution-needed
Required review-resolution: yes
Next stage: review-resolution for `SRO-M3-CR1`
Remaining implementation milestones: M3 resolution, M4 when triggered, M5
Verify readiness: not-claimed
