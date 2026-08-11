# Workflow Automation Target: Verify

- Mechanism: `bounded-review-fix`
- Change: `2026-08-11-test-spec-review-skill-simplification`
- Target stage: `verify`
- Occurrence: singleton final verification
- Bound at: `2026-08-11T20:19:07Z`
- Canonical position source: `docs/changes/2026-08-11-test-spec-review-skill-simplification/change.yaml`
- Starting position: approved `test-spec-review-r2`; implementation milestone `M1` planned
- Completion rule: final verification result is recorded
- External authority: none; the run cannot open a PR, push, publish, release, deploy, merge, or mutate external state

The new target replaces the completed `test-spec-review` automation target after its exact occurrence was reached and recorded.
It authorizes repository-local continuation through all mandatory implementation, review, rationale, and verification gates required before the final verification result.
