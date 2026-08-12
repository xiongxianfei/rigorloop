# Proposal Revision R4 Evidence: Spec-Review Skill Simplification

## Scope

This revision addresses `SRSIM-R3-PR1` without changing the selected package shape.

## Changes

- Replaced the universal result core with mutually exclusive non-formal feedback and formal review core groups inside the existing result asset.
- Limited the feedback core to scope, observations, limitations, and an optional suggested next action.
- Kept review status, findings, blockers, readiness, recording, settlement, automation, and handoff fields exclusive to formal profiles.
- Required exactly one core group, complete omission of inapplicable groups, and no `not-applicable` lifecycle placeholders.
- Added positive and negative static scenarios for feedback, formal review, both-core output, and feedback containing forbidden formal fields.

## Scope preservation

The revision adds no asset, reference, runtime, lifecycle schema, recording model, boundary owner, validator family, or target-agent acceptance system.

## Readiness

The revised proposal is ready for independent `proposal-review`. It does not claim proposal approval, specification readiness, implementation readiness, verification, branch readiness, or PR readiness.

## Validation

- Review-artifact structure validation passed for the complete change root.
- Change-metadata validation passed for `change.yaml`.
- Explicit-path lifecycle consistency validation passed for the revised artifact pack.
- Markdown readability validation passed with audit-only warnings.
- `git diff --check` passed.
