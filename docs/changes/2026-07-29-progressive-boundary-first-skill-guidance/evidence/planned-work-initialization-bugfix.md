# Planned-Work Initialization Bug Fix

Evidence ID: planned-work-initialization-bugfix
Stage: bugfix
Owning change:
`docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/change.yaml`

## Reproduction

Registering the new primary plan and running:

```text
python scripts/validate-change-metadata.py docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/change.yaml
```

failed with:

```text
workflow_state.planned_work: presence must match primary plan registration
```

The plan skill prohibited every `workflow_state` write, but the metadata
contract required `planned_work` at the same time as primary-plan
registration.

## Root cause

The state shape was correct, but write ownership omitted the actor responsible
for its initial value.
Plan already owns the stable ordered milestone definitions, so the smallest
deterministic fix is one-time initialization by plan.

## Fix

- Plan initializes missing primary-plan `planned_work` exactly once.
- Every implementation milestone starts as `planned`.
- The first implementation milestone is current.
- Every implementation milestone is initially remaining.
- Latest review is `not-started`.
- Final closeout is `not-ready`.
- Plan never replaces or updates existing `planned_work`.
- Workflow owns every later transition.

The governing specification, test specification, constitution, repository
instructions, workflow guide, architecture, accepted ADR, and published
`plan` and `workflow` skills now state the same narrow exception.

## Regression coverage

- `scripts/test-skill-validator.py` checks reciprocal plan/workflow ownership.
- `scripts/test-change-metadata-validator.py` checks that a primary plan
  without initialization fails and the deterministic initial shape passes.

## Validation

- `python scripts/test-change-metadata-validator.py`
  passed 61 tests.
- `python scripts/test-skill-validator.py`
  passed 272 tests with 16 documented skips.
- `python scripts/validate-skills.py`
  passed for 24 canonical skills.
- `python scripts/build-skills.py --check`
  passed using temporary generated output.
- `python scripts/validate-change-metadata.py docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/change.yaml`
  passed after initialization.
- Current-plan explicit artifact-lifecycle validation passed with two
  pre-existing nonblocking lifecycle-language warnings.
- Boundary-first validation passed for the amended lifecycle spec and test
  spec.
- Guide-system validation and `git diff --check` passed.

Broader explicit lifecycle validation of the older stage-owned artifact
package still reports baseline ownership debt in its referenced historical
proposal and multiply registered canonical architecture.
This fix does not claim that unrelated historical package debt is resolved.
