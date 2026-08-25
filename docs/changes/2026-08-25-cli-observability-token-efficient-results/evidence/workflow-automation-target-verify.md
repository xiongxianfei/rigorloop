# Workflow Automation Target: Verify

- Command: `$workflow auto: verify`
- Mechanism: `bounded-review-fix`
- Change: `2026-08-25-cli-observability-token-efficient-results`
- Target stage: `verify`
- Occurrence: singleton final verification
- Bound at: `2026-08-25T11:51:54+01:00`
- Canonical position source: `docs/changes/2026-08-25-cli-observability-token-efficient-results/change.yaml`
- Starting position: approved `test-spec-review-r3`; implementation milestone `M1` planned
- Completion rule: final verification result is durably recorded
- External authority: none; the run cannot open a PR, push, publish, release, deploy, merge, access credentials, or perform destructive Git operations

The new target replaces the completed `test-spec-review` automation target after its exact occurrence was reached and recorded. It authorizes repository-local continuation through implementation milestones M1 through M4, milestone-local reviews and bounded corrections, final holistic code review, change explanation, and formal verification. It stops at the recorded verification result.
