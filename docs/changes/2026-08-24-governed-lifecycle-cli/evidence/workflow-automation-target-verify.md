# Workflow Automation Target: Verify

- Change ID: `2026-08-24-governed-lifecycle-cli`
- Mechanism: `bounded-review-fix`
- Requested target: singleton `verify`
- Bound at: `2026-08-24T20:36:54+01:00`
- Canonical starting position: approved `test-spec-review-r1`, active test spec, and planned implementation milestone `M1`
- Completion rule: first formal final verification result is durably recorded
- Permitted progression: ordered implementation milestones with formal code review, final holistic code review, explanation, then verify
- Prohibited progression: PR creation, push, merge, release, deployment, publication, or external mutation
