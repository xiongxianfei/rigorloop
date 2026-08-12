# Proposal Revision R5 Evidence: Spec-Review Skill Simplification

## Scope

This revision addresses `SRSIM-R4-PR1` by removing non-formal feedback from the `spec-review` contract.

## Changes

- Defined every `spec-review` invocation as formal lifecycle review with required durable recording.
- Routed explicitly informal critique or discussion outside `spec-review` to conversational assistance or an applicable ideation skill.
- Removed `SR0-feedback`, `SR0B-feedback-boundary`, the feedback core, dual-core rules, and their measurements and fixtures.
- Reduced resource loading to `SR1-formal` and `SR1B-formal-boundary`.
- Kept one formal result core, one required recording group, and governed-settlement, boundary-review, and automated-review conditional groups.
- Reconciled the decision log and retained `SR1-isolated-formal` as the normative simplification surface.

## Scope preservation

The revision reduces proposal complexity and adds no asset, reference, runtime, lifecycle schema, recording model, boundary owner, validator family, or target-agent acceptance system.

## Readiness

The revised proposal is ready for independent `proposal-review`. It does not claim proposal approval, specification readiness, implementation readiness, verification, branch readiness, or PR readiness.

## Validation

- Review-artifact structure validation passed for the complete change root.
- Change-metadata validation passed for `change.yaml`.
- Explicit-path lifecycle consistency validation passed for the revised artifact pack.
- Markdown readability validation passed with audit-only warnings.
- `git diff --check` passed.
