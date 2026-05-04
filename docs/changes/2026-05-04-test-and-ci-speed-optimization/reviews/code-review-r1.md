# Code Review R1

Review ID: code-review-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: M1 commit `db751f1c305cb15827da850755fe164b3598d7bf`
Status: changes-requested
Review date: 2026-05-04

## Scope

Reviewed the M1 implementation for test and CI speed optimization against the approved spec, active test spec, active implementation plan, change-local evidence, architecture boundary, actual committed diff, and recorded validation evidence.

## Review inputs

- Diff range: `HEAD^..HEAD` at `db751f1c305cb15827da850755fe164b3598d7bf`.
- Review surface: `scripts/validation_selection.py`, `scripts/ci.sh`, `scripts/test-select-validation.py`, the active spec/test-spec/plan, proposal, plan index, change metadata, and M1 explain-change evidence.
- Tracked governing branch state: `CONSTITUTION.md`, `AGENTS.md`, `specs/test-and-ci-speed-optimization.md`, `specs/test-and-ci-speed-optimization.test.md`, `docs/plans/2026-05-04-test-and-ci-speed-optimization.md`, `docs/plan.md`, and `docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml` are present in the reviewed branch state.
- Architecture / ADR: no architecture update required because M1 preserves the existing selector, check catalog, wrapper, and hosted CI boundaries.
- Validation evidence: M1 red/green `python scripts/test-select-validation.py`, change metadata validation, selector-selected inspection, wrapper-selected validation including `broad_smoke.repo`, and `git diff --check` are recorded in the active plan and change metadata.

## Diff summary

M1 adds explicit `parallel_safe` catalog metadata, marks only the six reviewed regression check IDs as parallel-safe, exposes `is_parallel_safe_check`, and adds wrapper parsing for `--jobs`, `--timeout`, `--fail-fast`, and `--verbose` without changing selected-check execution semantics. Focused tests cover the allowlist, valid execution flags that do not leak to the selector, and invalid numeric flags failing before selector-selected checks can start.

## Findings

### CR1-F1: Plan index still says M1 is next after M1 is complete

Finding ID: CR1-F1

Evidence: `docs/plan.md` describes the active test-and-CI plan as having "implementation M1 is next", but the plan body records `[x] M1 complete`, "M1 is complete; M2 has not started", and "Ready for the next implementation milestone, M2." The repository workflow requires active plan state to reflect what happened and treats stale lifecycle state between `docs/plan.md` and the plan body as blocking PR readiness.

Required outcome: Update the `docs/plan.md` active-plan entry so it no longer presents M1 as the next step; it should reflect that M1 is complete and M2 is next or not mention milestone progress at that level.

Safe resolution: Edit the single `docs/plan.md` entry for this initiative, then rerun change metadata validation, lifecycle/selector-selected validation for the touched artifacts, review-artifact structure validation, and whitespace/diff checks.

## Checklist coverage

| Check | Result | Notes |
| --- | --- | --- |
| Spec alignment | pass | M1 implements the planned subset of `R2`, `R3`, `R4`, `R5`, `R7`, `R10`, `R16`, and `R20` without implementing deferred scheduler semantics. |
| Test coverage | pass | Focused tests cover catalog metadata, valid wrapper flags, and invalid numeric wrapper flags before selector invocation. |
| Edge cases | pass | M1 invalid `--jobs` and `--timeout` values are covered; scheduler, timeout, signal, and output edge cases are explicitly deferred to M2/M3. |
| Error handling | pass | Invalid numeric flags exit before selector invocation and before selected commands can run. |
| Architecture boundaries | pass | Per-check metadata stays in the catalog; wrapper defaults and invocation flags stay in `scripts/ci.sh`; hosted CI remains unchanged. |
| Compatibility | pass | Existing wrapper modes and selector-facing arguments keep their current meaning. |
| Security/privacy | pass | No secrets, credentials, network behavior, or new external resource use are introduced. |
| Generated output drift | pass | No generated outputs are touched by this M1 slice. |
| Unrelated changes | concern | Code changes are scoped, but CR1-F1 leaves touched lifecycle index wording stale for the completed milestone. |
| Validation evidence | pass | Recorded focused, selector-selected, wrapper-selected, metadata, broad-smoke delegation, and whitespace evidence is relevant to M1. |

## Recommended next stage

Enter review-resolution for CR1-F1, then rerun `code-review`.
