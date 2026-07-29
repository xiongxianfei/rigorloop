# Stage-Owned Change Query Compatibility Code Review R1

Review ID: code-review-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: unstaged diff in `scripts/query-change-record.py`, `scripts/test-query-change-record.py`, and `scripts/workflow_automation_state.py`
Reviewed artifact: stage-owned query compatibility implementation
Review date: 2026-07-29
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Material findings: SOQ-CR1, SOQ-CR2
Blocking findings: none

## Review inputs

- Governing contracts: `specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md` and `specs/change-record-catalog-registration-and-bounded-read-model.md`.
- Proof maps: the corresponding stage-owned lifecycle and bounded-read test specifications.
- Review surface: the complete unstaged implementation and regression-test diff.
- Validation evidence: the focused query, metadata, workflow-state, workflow-engine, policy, and automation-validator suites reported by implementation.

## Diff summary

The patch adds explicit read-only loading and bounded summary projections for
`stage-owned-change-local-v1`.
It keeps legacy mutation methods on their existing state-store path and adds
positive and unknown-value regression coverage.

## Findings

### Finding SOQ-CR1

Finding ID: SOQ-CR1
Severity: major
Location: `scripts/workflow_automation_state.py:1784`
Evidence: The stage-owned branch returns at line 1795 before the canonical-directory identity check beginning at line 1796. A direct fixture stored `change_id: 2026-07-29-foreign-change` under `docs/changes/2026-07-29-stage-owned-query/change.yaml`; the query exited `0` and reported the requested directory ID as valid.
Required outcome: Stage-owned compatibility reads must reject a stored `change_id` that differs from the canonical change directory before returning a snapshot.
Safe resolution path: Move or share the canonical change-ID check before the stage-owned return, retain the historical legacy exception only where intended, and add a targeted mismatch regression.
needs-decision rationale: none

### Finding SOQ-CR2

Finding ID: SOQ-CR2
Severity: major
Location: `scripts/query-change-record.py:279`
Evidence: The stage-owned projection assigns `unresolved_items: 0` solely from `workflow_state.planned_work.latest_review.status: approved`. The retained bounded-read contract assigns finding status to `review-log.md` and `review-resolution.md`; the positive fixture creates neither file but still reports zero unresolved findings.
Required outcome: The bounded summary must not claim review-finding closeout from routing state alone.
Safe resolution path: Preserve `unresolved_items: null` unless authoritative review-ledger evidence is actually read and validated; keep the evidence pointers for escalation.
needs-decision rationale: none

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | concern | Stage-owned reading is added, but SOQ-CR2 crosses the retained review-ledger ownership boundary. |
| Test coverage | concern | Positive and unknown-value cases exist; canonical identity and no-overclaim cases are missing. |
| Edge cases | block | BND-INPUT-001 and BND-AUTH-001 identity substitution is directly reproducible. |
| Error handling | concern | Unknown lifecycle values fail closed, but a mismatched canonical identity succeeds. |
| Architecture boundaries | pass | No new service, persistence mechanism, or write interception is introduced. |
| Compatibility | concern | The explicit read-only flag protects legacy writers, but its early return bypasses shared compatibility validation. |
| Security/privacy | pass | Output remains repository-relative and no command or external action is executed. |
| Derived artifact currency | pass | No generated surface changes. |
| Unrelated changes | pass | The implementation diff is limited to the query, state reader, and regression tests. |
| Validation evidence | concern | Selected suites pass, but neither material failure mode is asserted. |

## Handoff

This direct review is isolated.
No automatic downstream handoff or implementation fix is authorized.
Resolve SOQ-CR1 and SOQ-CR2 through `review-resolution`, then rerun
`code-review`.
