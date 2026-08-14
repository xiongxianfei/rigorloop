# Workflow Automation Target: Verify

- Change: `2026-08-14-proposal-skill-simplification`
- Mechanism: `bounded-review-fix`
- Target stage: `verify`
- Occurrence: singleton
- Bound at: `2026-08-14T11:25:14-07:00`
- Canonical position source: `docs/changes/2026-08-14-proposal-skill-simplification/change.yaml`
- Starting position: approved active test specification; implementation milestone M1 planned
- Completion rule: the first formal verify result is durably recorded
- PR boundary: stop after verify; do not invoke `pr`

The target resumes the existing governed change. It authorizes automatic progression through M1-M3 implementation and code review, required review resolution, final holistic code review, change explanation, and the first formal verify result. It does not authorize pushing, PR creation, publication, release, deployment, merge, destructive Git operations, credentials, or external mutation.
