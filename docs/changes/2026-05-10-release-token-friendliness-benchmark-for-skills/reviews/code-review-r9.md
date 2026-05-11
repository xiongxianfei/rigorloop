# Code Review R9

Review ID: code-review-r9
Stage: code-review
Round: 9
Reviewer: Codex code-review
Target: M5 release validation integration
Status: changes-requested
Date: 2026-05-11

## Review Inputs

- Diff range: `2c498cf..449f1df`
- Review surface: release-level token-cost validation delegation, `release-verify.sh` invocation, release metadata, workflow guidance, tests, and M5 lifecycle handoff state.
- Spec: `specs/release-token-friendliness-benchmark-for-skills.md`
- Test spec: `specs/release-token-friendliness-benchmark-for-skills.test.md`
- Plan milestone: `docs/plans/2026-05-11-release-token-friendliness-benchmark-for-skills.md`, M5.
- Architecture: `docs/architecture/system/architecture.md`
- Validation evidence recorded in the active plan and change metadata.
- Governance: `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`

## Diff Summary

M5 adds release-level Token-Friendliness validation for governed `v0.1.1` releases. `scripts/adapter_distribution.py` now requires `validation.token_cost_report` for `v0.1.1`, checks `docs/reports/token-cost/releases/v0.1.1.yaml`, and invokes `scripts/validate-token-cost-report.py`. `scripts/release-verify.sh` now runs the token-cost validator for `v0.1.1` and keeps earlier release targets out of the new token-cost gate. `scripts/test-adapter-distribution.py` adds focused coverage for missing token-cost metadata on `v0.1.1`, historical release scope, repository `v0.1.1` release validation, and dry-run release verifier command inclusion.

## Findings

### RTF-CR8 - Release validation integration lacks direct proof that invalid token-cost metadata blocks

Finding ID: RTF-CR8
Severity: major

Evidence:

- The approved test spec requires invalid governed release fixtures and an assertion that governed missing or invalid token-cost evidence blocks release validation in `specs/release-token-friendliness-benchmark-for-skills.test.md:392` and `specs/release-token-friendliness-benchmark-for-skills.test.md:396`.
- The M5 tests added in `scripts/test-adapter-distribution.py:1454` cover a missing token-cost report, and `scripts/test-adapter-distribution.py:1557` covers the repository's valid `v0.1.1` metadata.
- No M5 test forces `scripts/validate-release.py` or `validate_release_output()` through the nonzero token-cost validator path for invalid YAML, invalid waiver, missing run evidence, inconsistent runner metadata, or a validator failure.

Problem:

The release integration can still regress from "delegate and propagate token-cost validator failures" to "only require a file to exist" without an integration test catching it. Standalone validator tests prove the token-cost schema validator rejects invalid metadata, but T16 specifically requires release validation integration proof that invalid governed token-cost evidence blocks through the release gate.

Required outcome:

Add release-level integration coverage that proves governed invalid token-cost metadata fails release validation through the token-cost validator delegation path.

Safe resolution:

Add a focused M5 test that creates otherwise-valid `v0.1.1` release artifacts, points `token_cost_report_root` at a fixture containing invalid token-cost metadata, and asserts `validate_release_output("v0.1.1", ...)` returns `token-cost report validation failed` or the specific propagated validator error. A small fixture with a malformed or evidence-invalid token-cost report is enough; the test does not need to duplicate every standalone validator negative case.

## Checklist Coverage

| Check | Result | Notes |
|---|---|---|
| Spec alignment | concern | The implementation delegates token-cost validation for governed `v0.1.1`, but M5 test evidence does not yet prove invalid governed token-cost evidence blocks as required by T16. |
| Test coverage | block | Missing direct integration proof for invalid token-cost metadata propagation through release validation. |
| Edge cases | concern | Missing report and historical-release scope are covered, but invalid metadata and validator-failure paths are not covered at release-integration level. |
| Error handling | concern | `_validate_token_cost_report()` has a nonzero-subprocess error path, but no integration test exercises it. |
| Architecture boundaries | pass | Release validation delegates to the token-cost validator instead of moving schema ownership into release validation. |
| Compatibility | pass | Historical `v0.1.0` release validation is covered by fixture-backed tests and release verifier dry-run evidence. |
| Security/privacy | pass | The change does not add raw benchmark data logging or local path exposure beyond validator error messages. |
| Derived artifact currency | pass | No generated adapter output or generated Codex skill mirrors are hand-edited. |
| Unrelated changes | pass | The diff is scoped to M5 release validation integration, release workflow guidance, and lifecycle metadata. |
| Validation evidence | concern | Recorded validation is credible for the implemented happy path, missing-report path, and historical-release exception, but not for invalid governed evidence propagation. |

## No-Finding Rationale

Not applicable. One required-change finding blocks M5 closeout.

## Residual Risks

- Until RTF-CR8 is fixed, invalid token-cost metadata behavior depends on code inspection rather than the release-integration tests required by T16.

## Recommended Next Stage

Move M5 to `resolution-needed`, resolve RTF-CR8 in implementation, then rerun `code-review M5`.
