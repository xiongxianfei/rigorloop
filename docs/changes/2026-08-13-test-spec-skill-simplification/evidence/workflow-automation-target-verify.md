# Workflow Automation Target: Verify

- Command: `$workflow auto: verify`
- Bound at: 2026-08-13T13:05:57-07:00
- Change: `2026-08-13-test-spec-skill-simplification`
- Canonical position source: `change.yaml`
- Starting position: implementation milestone M1
- Target: first formal `verify` result
- Mechanism: `bounded-review-fix`

The run may execute and review milestones M1 through M3, complete final holistic code review, create the durable change explanation, and enter formal verification. It stops at the first recorded verify result. It does not open a pull request, push, publish, release, deploy, merge, use credentials, or mutate external systems.
