# Code Review M2 R2

Review ID: code-review-m2-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review skill
Target: M2 resolution for `SRO-M2-CR1` at commit `eb84928`
Status: clean-with-notes

## Review inputs

- Review surface: current working tree after `SRO-M2-CR1` resolution.
- Governing artifacts: `specs/script-output-optimization.md`, `specs/script-output-optimization.test.md`, and `docs/plans/2026-05-21-script-output-optimization.md` M2.
- Resolution evidence: `scripts/test-select-validation.py`, `docs/changes/2026-05-21-script-output-optimization/output-contract-red-test.md`, `behavior-preservation.md`, `review-resolution.md`, and `change.yaml`.
- Validation evidence recorded in the active plan and change metadata for the M2 resolution.

## Diff summary

The M2 resolution removes `@unittest.expectedFailure` masking from `ScriptOutputContractTests`, excludes that red-test class from ordinary validation through `load_tests`, and adds a default-suite guard that fails if required output-contract tests are marked as expected failures. It also records the explicit red-test proof in `output-contract-red-test.md` and updates behavior-preservation, review-resolution, plan, and change metadata evidence.

## Findings

No blocking or required-change findings.

## Checklist coverage

- Spec alignment: pass. The M2 tests cover default success/failure, verbose, quiet, conflicting flags, zero-test safety, reliable-only rerun commands, and JSON deferral as required by the approved spec and test spec.
- Test-proof integrity: pass. Required output-contract tests are no longer hidden as expected failures. Ordinary M2 validation excludes them intentionally, while `python scripts/test-select-validation.py ScriptOutputContractTests` remains the explicit pre-M3 red-test proof.
- Guard coverage: pass. `ValidationSelectionTests.test_output_contract_red_tests_are_unmasked_and_separate` runs in ordinary validation and checks the contract test class for `@unittest.expectedFailure`.
- Red-test evidence: pass. `output-contract-red-test.md` records the explicit command, expected pre-M3 nonzero result, observed `FAILED (failures=9)`, failing TSRO coverage, passing TSRO coverage, and post-M3 expectation.
- Behavior preservation: pass. The resolution does not implement formatter behavior, selection changes, quiet/verbose behavior, rerun behavior, JSON behavior, or CI wrapper behavior. M3 remains responsible for making the explicit red-test command pass.
- Architecture boundaries: pass. The change stays inside the approved first-slice test/evidence surface and does not touch generated artifacts or `scripts/ci.sh`.
- Validation evidence: pass. The active plan and change metadata record ordinary M2 validation, explicit red-test proof, metadata validation, review-artifact validation, lifecycle validation, diff check, selector/manual-routing evidence, and selected CI.

## No-finding rationale

`SRO-M2-CR1` required output-contract violations to remain visible instead of being converted into green expected failures. The resolution separates ordinary M2 validation from explicit red-test proof, adds a guard against reintroducing expected-failure masking, and records the exact failing formatter cases that M3 must make pass. This satisfies the required outcome without expanding M2 into formatter implementation.

## Residual risks

M3 through M5 remain open. This review closes M2 only and does not prove the runner output contract, CI wrapper preservation, final verification, branch readiness, or PR readiness.

## Handoff

Reviewed milestone: M2. Output contract tests
Review status: clean-with-notes
Milestone closeout: closed
Required review-resolution: no
Next stage: implement M3
Remaining implementation milestones: M3, M4 when triggered, M5
Verify readiness: not-claimed
