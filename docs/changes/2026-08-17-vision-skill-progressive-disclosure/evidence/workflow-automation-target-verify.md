# Workflow Automation Target: Verify

Date: 2026-08-17
Change: `2026-08-17-vision-skill-progressive-disclosure`
Mechanism: `bounded-review-fix`
Target: `verify`
Occurrence: singleton
Canonical position source: `docs/changes/2026-08-17-vision-skill-progressive-disclosure/change.yaml`

The user explicitly authorized workflow-managed progression from the approved test specification through implementation milestones, milestone-local code review, final holistic code review, explanation, and the first final `verify` result. The automation remains bound to this change and stops at that result or earlier on a material finding outside an eligible bounded correction, blocked recording, owner decision, invalid transition, failed required validation, or another workflow stop condition.

This authorization does not extend beyond verify to push, PR mutation, release, deployment, merge, destructive Git operations, credentials, publication, or target-agent runtime execution.
