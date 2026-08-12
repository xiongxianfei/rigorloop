# Proposal Revision R6 Evidence: Spec-Review Skill Simplification

## Scope

This revision addresses `SRSIM-R5-PR1` by moving the conditional resource boundary from universal recording to governed settlement and automation.

## Changes

- Renamed the proposed resource to `governed-spec-review-settlement.md`.
- Kept concise universal recording selection, artifact choice, synchronization, retry, and blocked behavior inline for every formal review.
- Limited the new reference to same-change `change.yaml` settlement, governed retries, automation evidence, pause, and return-to-workflow procedure.
- Defined isolated, isolated-boundary, governed, and governed-boundary resource profiles.
- Kept automation as an authority branch within the governed resource assembly.
- Required isolated-profile reduction to come from duplicate removal and exclusion of governed-only procedure.
- Added failure and preservation scenarios for isolated recording and missing governed procedure after successful recording.

## Scope preservation

The revision changes one proposed resource boundary and adds no reference, asset, runtime, lifecycle schema, recording model, boundary owner, validator family, or target-agent acceptance system.

## Readiness

The revised proposal is ready for independent `proposal-review`. It does not claim proposal approval, specification readiness, implementation readiness, verification, branch readiness, or PR readiness.

## Validation

- Review-artifact structure validation passed for the complete change root.
- Change-metadata validation passed for `change.yaml`.
- Explicit-path lifecycle consistency validation passed for the revised artifact pack.
- Markdown readability validation passed with audit-only warnings.
- `git diff --check` passed.
