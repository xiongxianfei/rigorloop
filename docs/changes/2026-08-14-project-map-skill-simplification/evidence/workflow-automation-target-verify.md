# Workflow Automation Target: Verify

- Command: `$workflow auto: verify`
- Change: `2026-08-14-project-map-skill-simplification`
- Bound at: `2026-08-14T08:28:55-07:00`
- Target stage: `verify`
- Occurrence: singleton
- Canonical position source: `change.yaml#workflow_state.planned_work`
- Current implementation milestone: `M1`
- Starting revision: `ce8c4311`

The target authorizes workflow-managed continuation through M1, M2, M3, their required code reviews and finding resolution, final holistic code review, explanation, and the first formal verify result. It does not authorize PR creation, pushing, publication, release, deployment, merge, credentials, or destructive Git operations.

The direct user decision and approved `test-spec-review-r2` remove MP0 and MP1 as scripted acceptance procedures. Deterministic proof remains required through verify, while ordinary PR review retains later human semantic judgment outside this automation target.
