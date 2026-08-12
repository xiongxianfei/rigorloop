# Proposal Revision R3 Evidence: Spec-Review Skill Simplification

## Scope

This revision addresses `SRSIM-R2-PR1`, `SRSIM-R2-PR2`, and `SRSIM-R2-PR3` from `proposal-review-r2` while retaining the selected package shape.

## Changes

- Removed recording mode as an independent classification axis and derived recording directly from review kind.
- Defined explicit formal-review triggers and strict non-formal feedback conditions.
- Made a durable-record request promote the invocation to isolated formal review and removed the unsupported non-formal durable profile.
- Bound isolated review placement to `specs/formal-review-recording.md` requirements `R31a` through `R31n`.
- Bound minimal-root shape and recording results to `R4h` through `R4l` and `R24` through `R26`.
- Enumerated the clean and material isolated write sets and prohibited governed settlement, plan, routing, lifecycle, and automation mutations.
- Made reduced loaded words and bytes for `SR1-isolated-formal` a normative success condition.
- Required one loaded owner per duplicate cluster and separate reporting for feedback, boundary, governed-manual, governed-automated, and total-package profiles.

## Scope preservation

The revision adds no reference, asset, runtime, lifecycle schema, recording model, boundary activation owner, permanent simplicity validator, or target-agent acceptance system.

## Readiness

The revised proposal is ready for independent `proposal-review`. It does not claim proposal approval, specification readiness, implementation readiness, verification, branch readiness, or PR readiness.

## Validation

- Review-artifact structure validation passed for the complete change root.
- Change-metadata validation passed for `change.yaml`.
- Explicit-path lifecycle consistency validation passed for the revised artifact pack.
- Markdown readability validation passed with audit-only warnings.
- `git diff --check` passed.
