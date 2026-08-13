# Workflow Automation Target: Verify

- Skill: `workflow`
- Mechanism: `bounded-review-fix`
- Target stage: `verify`
- Occurrence: singleton final verification
- Bound change: `2026-08-12-plan-skill-simplification`
- Canonical position at authorization: clean recorded `test-spec-review-r1`; next stage `implement` for milestone `M1`
- Implementation authority: the three approved implementation milestones and reviewer-declared bounded corrections only
- Stop boundary: complete final `verify` result; do not enter `pr`
- External authority: no push, PR, publication, release, deployment, merge, credential access, or destructive Git operation
- Authorization result: active
