# Code Review M2 R1 - Plan Index Archive Validator Contract

Review ID: code-review-m2-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: M2. Validator contract and fixtures
Reviewed artifact: commit `e04c13d`
Review date: 2026-05-22
Status: changes-requested
Recording status: recorded

## Review inputs

- Diff/review surface: `e04c13d M2: validate plan index archive contract`
- Plan: `docs/plans/2026-05-22-bounded-plan-index-and-completed-plan-archive.md`
- Spec: `specs/plan-index-lifecycle-ownership.md`
- Test spec: `specs/plan-index-lifecycle-ownership.test.md`
- Validation evidence recorded in the active plan and commit message
- Changed validator: `scripts/artifact_lifecycle_validation.py`
- Changed tests: `scripts/test-artifact-lifecycle-validator.py`

## Diff summary

M2 adds explicit plan lifecycle marker parsing, plan index/archive surface parsing, structural checks for `docs/plan.md`, terminal conservation, recent Done cap enforcement, terminal entry link checks, archive-only nonterminal rejection, and active supersession field checks. It also adds fixture-driven validator tests and change-local implementation evidence.

## Result

- Skill: code-review
- Review status: changes-requested
- Material findings: BPIX-M2-CR1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/reviews/code-review-m2-r1.md`
- Review log: `docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/review-log.md`
- Review resolution: `docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/review-resolution.md#code-review-m2-r1`
- Reviewed milestone: M2. Validator contract and fixtures
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3, M4, M5, M6
- Required review-resolution: yes

## Findings

### BPIX-M2-CR1 - Terminal marker changes can bypass terminal conservation

Finding ID: BPIX-M2-CR1
- Severity: major
- Location: `scripts/artifact_lifecycle_validation.py`
- Evidence: `_validate_terminal_plan_conservation` is only called when `_plan_index_surface_in_scope(root_resolved, scope)` is true. `_plan_index_surface_in_scope` only returns true for `docs/plan.md` or `docs/plan-archive.md` paths. A direct validation probe with only `docs/plans/2026-05-03-done-plan.md` in scope, containing `Plan lifecycle state: done` and no Done/archive entry, returned no blockers.
- Required outcome: A plan body entering or carrying an explicit terminal lifecycle state must trigger terminal conservation validation when that plan file is in validation scope, not only when `docs/plan.md` or `docs/plan-archive.md` changes.
- Safe resolution path: Add a failing fixture/test for a plan body scoped alone with `Plan lifecycle state: done` missing from both Done surfaces. Then update the conservation trigger so it runs when either plan index surfaces are in scope or any scoped plan body has an explicit terminal lifecycle marker. Keep legacy prose-only status exempt from terminal inference.

## Checklist coverage

| Check | Verdict | Evidence |
| --- | --- | --- |
| Spec alignment | block | `R15a` requires every explicit terminal plan to appear exactly once across recent/archive, and performance guidance says terminal conservation should run for relevant plan bodies. The implementation gates conservation only on index/archive scope. |
| Test coverage | concern | Tests cover missing terminal entries when plan index/archive surfaces are validated, but not when the changed path is only a terminal plan body. |
| Edge cases | block | The plan-body terminal marker edge case can silently pass with missing Done/archive placement. |
| Error handling | pass | Marker value, contradictory disposition, duplicate/missing terminal entry, archive-only nonterminal, and supersession structural errors have direct tests in index/archive scope. |
| Architecture boundaries | pass | No runtime architecture or ADR boundary is touched. |
| Compatibility | concern | Existing legacy prose-only behavior is preserved, but explicit marker adoption can still leave stale index/archive state if only the plan file changes. |
| Security/privacy | pass | No secrets, host-only state, or hidden lifecycle state introduced. |
| Derived artifact currency | pass | No generated artifact output is changed in M2. |
| Unrelated changes | pass | Diff is scoped to the approved proposal/spec/test-spec/plan artifacts, validator, tests, and change-local evidence. |
| Validation evidence | concern | Recorded validation is relevant, but it does not include direct proof for plan-body-only terminal conservation. |

## No-finding rationale

Not applicable. One material finding requires resolution before M2 can close.

## Residual risks

The migration milestone should not start until BPIX-M2-CR1 is fixed, validated, and re-reviewed.

## Handoff

Route to review-resolution for BPIX-M2-CR1. Keep M2 on the same milestone with state `resolution-needed`.
