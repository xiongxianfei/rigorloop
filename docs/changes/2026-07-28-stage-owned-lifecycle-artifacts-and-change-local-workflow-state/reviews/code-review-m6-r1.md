# Code Review M6 R1

Review ID: code-review-m6-r1
Stage: code-review
Round: M6 R1
Reviewer: Codex code-review skill
Target: commit e3b421fa, M6 activation slice
Reviewed artifact: commit e3b421fa
Review date: 2026-07-29
Status: changes-requested
Material findings: SLA-CR-M6-1
Reviewed milestone: M6. Atomic workflow-skill activation
Recording status: recorded

## First-pass risk map

| Risk | Verdict |
| --- | --- |
| A second activation source exists | pass |
| Existing historical reads create the marker | pass |
| Current change fails the new shape | pass |
| Generated adapters diverge after cutover | pass |
| Exact public activation default lacks regression proof | finding |

## Finding SLA-CR-M6-1

Finding ID: SLA-CR-M6-1
Severity: medium
Location: `scripts/test-skill-validator.py`

Evidence: the workflow skill creates the exact current marker and states the
one-time migration/read-only boundary, but focused skill tests do not pin
those activation clauses.

Required outcome: add a focused assertion for the exact marker, default
creation, one-time pre-mutation migration, and side-effect-free historical
inspection.

Safe resolution: extend the existing stage-owned skill-contract test class;
do not add an activation selector or another validator.

## Outcome

M6 remains in resolution until the focused skill test passes.
