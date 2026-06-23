# Code Review M4 R1 - Workflow Guidance, Active Audit, and Projection Normalization

Review ID: code-review-m4-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: commit `361456cc`
Status: changes-requested

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/reviews/code-review-m4-r1.md, docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/review-log.md, docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/review-resolution.md, docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md, docs/plan.md, docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/change.yaml
- Open blockers: WSS-CR4
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: WSS-CR4
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/reviews/code-review-m4-r1.md
- Review log: docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/review-log.md
- Review resolution: docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/review-resolution.md#code-review-m4-r1
- Reviewed milestone: M4. Workflow Guidance, Active Audit, and Projection Normalization
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M4, M5
- Required review-resolution: yes
- Finding IDs: WSS-CR4
- Verify readiness: not-claimed

## Review inputs

- Diff/review surface: commit `361456cc` (`M4: bind workflow state-sync guidance`).
- Tracked governing branch state: committed M4 implementation and governing artifacts at `361456cc`.
- Governing artifacts:
  - `specs/single-source-of-workflow-state.md`
  - `specs/single-source-of-workflow-state.test.md`
  - `docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md`
- Validation evidence reviewed:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py -k workflow_state_sync_gate_is_binding_guidance`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/workflows.md --path docs/plan.md --path docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md --path skills/workflow/SKILL.md --path skills/plan/SKILL.md --path skills/implement/SKILL.md --path skills/code-review/SKILL.md --path skills/verify/SKILL.md --path skills/pr/SKILL.md --path docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/change.yaml`
  - Active/blocked audit reproduction: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md --path docs/plans/2026-06-23-evidence-bound-incremental-project-map.md --path docs/plans/2026-06-23-published-skill-resource-integrity-architecture-pilot.md --path docs/plans/2026-06-18-workflow-skill-artifact-location-map.md`

## Diff summary

M4 adds binding state-sync wording to `docs/workflows.md` and the workflow, plan, implement, code-review, verify, and PR skills. It adds a static skill regression test for that wording, records M4 validation evidence in change metadata and the active plan, updates the active plan/index to route M4 to code review, and adds a missing plan-body `Change ID` field to the active Evidence-Bound Project Map plan.

## Findings

### WSS-CR4: Active/blocked enforcement scope is deferred while the all-active gate still fails

Finding ID: WSS-CR4
Severity: major
Location: `docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md:402`
Evidence: M4's plan requires active and blocked plan files to be audited and exact owner/projection fields added for enforcement (`docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md:216`, `:234`, `:239`-`:240`). The governing spec says first enforcement scope MUST include active and blocked plans (`specs/single-source-of-workflow-state.md:345`), and T19 requires live projection synchronization for active and blocked plans plus a failure for active applicable plans lacking `Current Handoff Summary` (`specs/single-source-of-workflow-state.test.md:528`-`:537`). The implementation instead records that the all-active audit exposed legacy active-plan debt and a cross-plan change-metadata association blocker, then keeps it outside the slice (`docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md:402`). Re-running the all-active audit command fails with `BLOCK docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml [workflow-state]: change.yaml change_id must match plan-body Change ID for docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md`.
Required outcome: M4 must not hand off as review-complete while active/blocked enforcement scope is known not to pass. The implementation must either make the active/blocked audit gate pass for the active index scope or record a valid current blocker instead of claiming M4 review readiness.
Safe resolution path: Fix the active/blocked enforcement path so active plan rows and their owning change metadata are associated correctly, add or update fixture coverage for the multi-active-plan case, normalize any active/blocked projection-source fields required by the contract, and rerun the all-active audit command. If the intended behavior is to grandfather active legacy plans, revise the approved spec/plan first; do not leave R81/T19 silently bypassed.
needs-decision rationale: none

## Checklist coverage

| Check | Verdict | Evidence |
| --- | --- | --- |
| Spec alignment | block | WSS-CR4 violates R81/T19 by deferring active/blocked enforcement after the all-active gate fails. |
| Test coverage | block | The new static skill test covers binding guidance wording, but no M4 fixture or regression proves the active/blocked audit can pass with multiple active plans. |
| Edge cases | block | The multi-active-plan audit path is a named M4 rollout edge and currently fails. |
| Error handling | concern | The implementation records a cross-plan validation blocker as outside the slice instead of converting it into a resolved gate or current blocker. |
| Architecture boundaries | pass | Guidance remains in workflow docs/skills and does not introduce a competing state owner. |
| Compatibility | concern | Legacy active-plan compatibility is asserted in the plan notes, but R81 requires active and blocked plans in first enforcement scope. |
| Security/privacy | pass | The diff is documentation, tests, and metadata only; no secrets or runtime auth surfaces are touched. |
| Derived artifact currency | concern | The current initiative's owner/index projections sync, but the full active index projection set does not validate. |
| Unrelated changes | pass | The Evidence-Bound plan edit is a one-line projection-source normalization tied to the active/blocked audit. |
| Validation evidence | block | Targeted M4 checks pass, but the all-active audit command fails and is the direct proof for this finding. |

## No-finding rationale

Not applicable. WSS-CR4 requires changes before M4 can close.

## Residual risks

The failure is the same family as earlier projection-enforcement findings: a narrower validation path passes while the broader projection surface that the contract names still fails.

## Milestone handoff

Reviewed milestone: M4. Workflow Guidance, Active Audit, and Projection Normalization
Review status: changes-requested
Milestone closeout: resolution-needed
Required review-resolution: yes
Next stage: review-resolution
Remaining implementation milestones: M4, M5
Verify readiness: not-claimed
