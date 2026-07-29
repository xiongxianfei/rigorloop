# CI Maintenance: Change-Local Evidence Routing

Stage: ci-maintenance
Status: updated
Workflow file: not applicable
PR checks: existing change-local lifecycle validation
Boundary checks: existing broad smoke
Risk coverage: milestone evidence under one governed change root
Open blockers: none
Next stage: code-review

## Change

The existing validation selector now classifies exactly
`docs/changes/<change-id>/evidence/<file>` as change-local lifecycle evidence.
It routes the directory to the already-owned artifact lifecycle check.
Deeper unknown paths and unrelated unregistered top-level evidence continue
to fail closed.

This replaces seven per-file manual-routing failures with one stable directory
boundary. It adds no validation command, selector parameter, permission,
external action, or hosted workflow.

Focused command owned by the existing CI contract:

- `python scripts/test-select-validation.py` — 136 passed.

The first complete PR-mode retry then exposed GUIDE-005 as a second retired
projection: it still required live-work and superseded status sections in
`docs/plan.md`. The existing guide validator now requires a navigation index
to stable plan bodies and owning `change.yaml` records instead.

- `python scripts/test-guide-system-validator.py` — 10 passed.
- `python scripts/validate-guide-system.py` — passed.
