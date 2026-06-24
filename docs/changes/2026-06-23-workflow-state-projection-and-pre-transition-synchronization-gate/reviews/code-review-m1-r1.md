# Code Review M1 R1

Review ID: code-review-m1-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: commit 55ffa6c9
Reviewed artifact: M1 implementation diff for workflow-state parser fixtures
Review date: 2026-06-23
Recording status: recorded
Status: changes-requested

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/reviews/code-review-m1-r1.md, docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/review-log.md, docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/review-resolution.md, docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md, docs/plan.md, docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/change.yaml
- Open blockers: WSS-CR1
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: WSS-CR1
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/reviews/code-review-m1-r1.md
- Review log: docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/review-log.md
- Review resolution: docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/review-resolution.md#code-review-m1-r1
- Reviewed milestone: M1. Parser Fixture Harness and Owner-State Tests
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3, M4, M5
- Required review-resolution: yes
- Finding IDs: WSS-CR1
- Verify readiness: not-claimed

## Review inputs

- Diff/review surface: commit `55ffa6c9` (`M1: add workflow-state sync parser fixtures`).
- Tracked governing branch state: committed M1 implementation and governing artifacts at `55ffa6c9`.
- Governing artifacts:
  - `specs/single-source-of-workflow-state.md`
  - `specs/single-source-of-workflow-state.test.md`
  - `docs/architecture/system/architecture.md`
  - `docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md`
- Validation evidence reviewed:
  - `python scripts/test-artifact-lifecycle-validator.py -k workflow_state`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/single-source-of-workflow-state.test.md --path docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md --path docs/plan.md`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/change.yaml`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/`

## Diff summary

M1 adds `scripts/lifecycle_state_sync.py` as a shared parser/comparison helper and wires it into `scripts/artifact_lifecycle_validation.py`. The new test coverage in `scripts/test-artifact-lifecycle-validator.py` exercises structured review-status parsing, final-closeout reason-code validation, plan-index projection comparisons, `change.yaml.change_id` consistency, and `Readiness` live-state restatement rejection.

## Findings

### WSS-CR1: `docs/plan.md` projection drift passes when only the plan index is validated

Finding ID: WSS-CR1
Severity: major
Location: `scripts/artifact_lifecycle_validation.py:1642`
Evidence: The new artifact-lifecycle hook builds `workflow_state_plan_paths` only from changed or related plan-body paths. When `docs/plan.md` is the sole explicit validation path, no plan body is added to `workflow_state_plan_paths`, so `validate_workflow_state_sync()` is not called even though `docs/plan.md` is the projection surface. A direct check using a temporary fixture with `docs/plan.md` `Next stage: implement M2` and the plan owner `Next stage: code-review M2` returned zero blockers for `paths=["docs/plan.md"]`, but returned the expected blocker when the plan body path was also supplied.
Required outcome: `docs/plan.md` projection validation must run when the plan index is in scope, using linked active/blocked structured plan bodies as the authoritative sources for `State`, `Next stage`, and `Change ID`.
Safe resolution path: When `docs/plan.md` is in scope, collect the relevant active/blocked plan rows from the index, resolve linked plan bodies that carry the structured workflow-state marker, and pass those plan paths into the shared state-sync validator. Add a regression test where an index-only explicit-path validation catches a stale `Next stage` projection without requiring the caller to also pass the plan body.
needs-decision rationale: none

## Checklist coverage

| Check | Verdict | Evidence |
| --- | --- | --- |
| Spec alignment | block | WSS-CR1 violates the projection synchronization requirement for `docs/plan.md` when the index itself is the reviewed path. |
| Test coverage | concern | Existing tests cover projection drift only when both `docs/plan.md` and the plan body are passed; they miss the index-only path. |
| Edge cases | block | The named stale projection handoff path fails for index-only validation. |
| Error handling | pass | Parser failures generally fail closed for malformed owner fields and reason codes. |
| Architecture boundaries | pass | The implementation uses a shared module composed through artifact-lifecycle validation, matching the approved architecture. |
| Compatibility | concern | The structured-marker guard preserves legacy plans, but WSS-CR1 leaves an important projection surface unenforced. |
| Security/privacy | pass | No secrets, credentials, auth paths, or sensitive runtime data are introduced. |
| Derived artifact currency | not-applicable | No generated artifacts are changed in M1. |
| Unrelated changes | pass | The M1 code changes are scoped to lifecycle state-sync parser/tests; broader artifact changes are the governing workflow artifacts for this branch. |
| Validation evidence | concern | The reported validation commands are real and relevant, but they do not exercise the index-only failure path. |

## No-finding rationale

Not applicable. WSS-CR1 requires changes before M1 can close.

## Residual risks

Review consistency fixtures and broader stale-token comparison remain planned for later milestones; this review only blocks on the M1 projection-enforcement gap.

## Milestone handoff

M1 moves to `resolution-needed`. The next stage is `review-resolution` for WSS-CR1. Do not start M2 until WSS-CR1 is resolved and M1 passes re-review.
