# Workflow Automation Target: Verify

- Change: `2026-08-15-architecture-skill-simplification`
- Mechanism: `bounded-review-fix`
- Target stage: `verify`
- Target occurrence: singleton
- Bound at: `2026-08-15T15:49:36-07:00`
- Canonical position source: `docs/changes/2026-08-15-architecture-skill-simplification/change.yaml`
- Starting position: approved active test specification and planned implementation milestone M1
- Completion rule: first formal verify result is durably recorded

The run may execute the approved M1 through M3 implementation and review sequence, required review resolution, final holistic review, explanation, and verification. It must stop at verification and may not open or prepare a pull request, push, publish, release, deploy, merge, or mutate external systems.
