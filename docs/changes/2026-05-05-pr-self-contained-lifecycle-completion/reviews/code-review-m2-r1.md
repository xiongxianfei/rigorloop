# Code Review M2 R1

Review ID: code-review-m2-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: M2 pre-resolution commit `086bcaa`
Status: changes-requested
Review date: 2026-05-05
Record mode: reconstructed
Original review source: Codex code-review handoff during M2 implementation.
Original review evidence: Review-side direct check showed `validate_repository(..., paths=["docs/plan.md"])` produced zero blockers for the stale Active fixture, then the focused regression `test_plan_index_change_validates_linked_plan_body` failed before the fix.
Created after fixes began: yes; the finding was surfaced before the fix, but this durable review record was written after the accepted fix started.
Loss of fidelity: low; the failing condition, safe resolution, and validation commands are recorded below.

## Scope

Reviewed the M2 lifecycle-validator implementation against the approved PR-self-contained lifecycle completion spec, active test spec, M2 plan scope, committed diff, and selected validation evidence.

## Review inputs

- Diff range: `c2d4e51..086bcaa` for the pre-resolution M2 implementation.
- Review surface: `scripts/artifact_lifecycle_validation.py`, `scripts/test-artifact-lifecycle-validator.py`, `scripts/test-review-artifact-validator.py`, lifecycle fixtures, active plan updates, change metadata, and explain-change evidence.
- Tracked governing branch state: `CONSTITUTION.md`, `AGENTS.md`, `specs/rigorloop-workflow.md`, `specs/rigorloop-workflow.test.md`, `docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md`, `docs/plan.md`, and `docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/change.yaml` were present in the reviewed branch state.
- Architecture / ADR: not required; M2 changes repository validation and workflow evidence without runtime architecture, deployment, persistence, or external integration changes.
- Validation evidence inspected: M2 red/green `python scripts/test-artifact-lifecycle-validator.py`, `python scripts/test-review-artifact-validator.py`, explicit lifecycle validation with expected warnings, selector-selected check IDs, `bash scripts/ci.sh --mode explicit ...`, change metadata validation, and whitespace checks.

## Diff summary

M2 adds plan lifecycle validation for plan index/body agreement, terminal plan readiness wording, duplicate Active/Done index entries, tracked merge-dependent lifecycle-language warnings, and focused review-artifact closeout coverage for `Closeout status: open`.

## Findings

### CR-M2-R1-F1: Plan-index-only validation misses linked plan bodies

Finding ID: CR-M2-R1-F1

Evidence: Review-side proof using the `plan-index-completed-under-active` fixture showed `validate_repository(..., mode="explicit-paths", paths=["docs/plan.md"])` returned zero blocking findings even though `docs/plan.md` listed a `done` plan under `## Active`. The added regression `test_plan_index_change_validates_linked_plan_body` failed before the fix with `expected fixture 'plan-index-completed-under-active' to fail`.

Required outcome: When `docs/plan.md` is in validation scope, the lifecycle validator must inspect the linked plan bodies and block stale plan/index lifecycle state, including a terminal plan still listed under `## Active`.

Safe resolution: Expand the plan lifecycle candidate set from plan-index entries when `docs/plan.md` is the only plan lifecycle surface in scope, keep selected related-plan validation focused when plan bodies are already in scope, and rerun lifecycle regression, review-artifact validation, selected CI, change metadata validation, and whitespace checks.

## Checklist coverage

| Check | Result | Notes |
| --- | --- | --- |
| Spec alignment | concern | M2 covers plan body paths, but the pre-resolution diff does not satisfy `R8j`/`R8ja` when only `docs/plan.md` changes. |
| Test coverage | concern | Existing tests passed because they supplied the plan body path directly; they did not prove index-only validation. |
| Edge cases | concern | The named stale Active/Done edge case is missed for the common index-only edit path. |
| Error handling | pass | Existing missing-status and terminal-readiness failure paths are deterministic once a plan body is inspected. |
| Architecture boundaries | pass | The validator remains the correct owner for plan lifecycle consistency; no selector or hosted CI boundary change is required for this fix. |
| Compatibility | pass | The requested fix only expands validation scope for `docs/plan.md`; existing explicit plan-body validation behavior remains valid. |
| Security/privacy | pass | The reviewed diff handles tracked repository files only and introduces no secrets or external access. |
| Generated output drift | pass | No generated outputs are touched by M2. |
| Unrelated changes | pass | The M2 diff is scoped to lifecycle validation, review-artifact test coverage, fixtures, and change-local evidence. |
| Validation evidence | concern | Selected CI passed on the pre-resolution surface, but the missing index-only proof shows the evidence set was incomplete. |

## Recommended next stage

Enter review-resolution for CR-M2-R1-F1, then rerun `code-review`.
