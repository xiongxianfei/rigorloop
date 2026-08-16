# Workflow Automation Target: Verify

- Date: 2026-08-16
- Change: `2026-08-16-pr-skill-simplification`
- Mechanism: `bounded-review-fix`
- Target: `verify`
- Occurrence: singleton final verification
- Canonical position source: `docs/changes/2026-08-16-pr-skill-simplification/change.yaml`

The user explicitly authorized workflow-managed progression from the approved test specification through implementation milestones, milestone-local code reviews, required review resolution and rereview, final holistic code review, change explanation, and the first final `verify` result.

The run remains bound to this exact change and active plan. It stops at final verification or earlier on a material finding that is not eligible for bounded correction, owner decision, failed required validation, stale identity, scope expansion, architecture escalation, unavailable required resource, or another workflow stop condition.

This authorization does not extend to PR creation or refresh, push, publication, release, deployment, merge, destructive Git operations, credentials, live external acceptance, or target-agent runtime execution.
