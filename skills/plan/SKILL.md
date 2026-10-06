---
name: plan
description: Turn accepted requirements and reviewed System/Architecture Design into a proportionate delivery plan with milestones, dependencies, proof and recovery. Use before multi-component or risky implementation.
---

# Plan

Read the accepted IR/SR basis, applicable ARs, reviewed System/Architecture Design and material constraints. If a needed obligation, logical behavior or architectural owner is missing, return it to its author instead of deciding it through a task assignment.

Create or revise the initiative's stable plan in the project's plan convention, using the packaged plan skeleton when useful. Keep mutable progress and execution outcomes in the current operational handoff. Do not overwrite another initiative's plan.

Define coherent milestones with scope, prerequisites, completion conditions, required proof, actual validation commands and relevant failure/recovery considerations. Allocate requirement and design outcomes to implementation and checks; include cross-milestone interactions. Use only work levels that improve coordination. Feature remains a stakeholder-visible capability, not a delivery work level.

Milestone completion means implementation and required checks are complete for that scope. Specify one whole-change independent Code Review checkpoint after the complete implementation and before distinct final Verify. Do not add mandatory per-milestone review handoffs. Optional interim advice remains optional.

Use the relevant packaged proof methods for concurrency, migration, recovery, negative boundaries or integrated behavior. Select observations that can expose a plausible violation; no one-test-per-requirement rule or requirement-shaped stub is needed. Submit the plan and proof allocation together to delivery-review before implementation reliance.

## Recording boundary

For Change-managed work, read the packaged operational interface reference before relying on or updating current state. Use supported CLI tasks and the inspected opaque revision; skills do not use SQL or edit runtime storage. An isolated invocation keeps its requested scope. Installation alone does not adopt workflow policy.

## Resource map

- READ `references/operational-recording.md` when inspecting or recording Change-managed work.
- READ `references/targeted-recording-v2.schema.json` when constructing a recording request.
- READ `references/rigorloop-records-v4.schema.json` when checking the types used by that request.

- READ `references/boundary-and-negative-verification.md` when that boundary can change the delivery outcome.

- READ `references/boundary-first-method-v1.md` when the project applies its boundary first method v1 criteria to this invocation.

- READ `references/concurrency-and-retry-verification.md` when that boundary can change the delivery outcome.

- READ `references/cross-milestone-integration-verification.md` when that boundary can change the delivery outcome.

- READ `references/failure-and-recovery-verification.md` when that boundary can change the delivery outcome.

- READ `references/manual-and-operational-evidence.md` when that boundary can change the delivery outcome.

- READ `references/migration-and-compatibility-verification.md` when that boundary can change the delivery outcome.

- READ `references/requirement-to-delivery-model.md` when the project applies its requirement to delivery model criteria to this invocation.

- READ `references/review-reliance.md` when the project applies its review reliance criteria to this invocation.

- READ `references/security-and-authority-verification.md` when that boundary can change the delivery outcome.

- READ `references/state-machine-verification.md` when that boundary can change the delivery outcome.

- READ `references/test-maintenance.md` when the project applies its test maintenance criteria to this invocation.

- READ `references/test-quality.md` when the project applies its test quality criteria to this invocation.

- COPY `assets/plan-skeleton.md` when authoring a new delivery plan.
- COPY `assets/milestone.md` when defining a milestone in that plan.

- READ `references/rem-methods-plan-and-assess-verification.md` when planning or interpreting verification against specified obligations.
- READ `references/rem-methods-validate-stakeholder-outcomes.md` when assessing intended-use outcomes separately from specified conformance.
- READ `references/rem-concepts-assurance.md` when reasoning about assurance in the selected scope.
- READ `references/rem-models-README.md` when reasoning about README in the selected scope.
- READ `references/rem-practices-engineer-change-WORKED-EXAMPLE.md` when needing an illustrative application of the canonical methods; examples do not establish execution.

## Expected output

Report the actual scoped outcome, governing basis, changed subjects or recorded judgment, material gaps and the next authorized action. Distinguish progress, review approval, final verification and external publication; claim only outcomes supported by this invocation.
