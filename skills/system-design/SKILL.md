---
name: system-design
description: Define or refine logical Functions and behavior from accepted SRs, including Feature–Function and SR–Function relationships. Use architecture-design for Module responsibility and realization.
---

# System Design

Start from the accepted requirement basis and current system definitions. Determine the logical behavior required: Function purpose, inputs, outputs, states, rules and observable outcomes. Reuse existing Functions and relationships where they already satisfy the obligation.

Use Functional Analysis and the system model reference as needed. Several Functions may satisfy one SR, and one Function may support several obligations. A quality constraint can constrain existing behavior; do not mirror the requirement tree mechanically.

Feature intent remains anchored in requirement analysis. Return changes to stakeholder need or obligation to requirement-analysis. Leave Module allocation, Interfaces, realization and architectural AR derivation to architecture-design. Iterate with that owner when feasibility or interactions expose a gap.

Update the owning repository model and supporting behavior/information explanations. Diagrams explain that design; they do not create separate authoritative copies of entities. Prepare the affected logical behavior together with Architecture Design for one integrated design-review.

## Recording boundary

For Change-managed work, read the packaged operational interface reference before relying on or updating current state. Use supported CLI tasks and the inspected opaque revision; skills do not use SQL or edit runtime storage. An isolated invocation keeps its requested scope. Installation alone does not adopt workflow policy.

## Resource map

- READ `references/operational-recording.md` when inspecting or recording Change-managed work.
- READ `references/targeted-recording-v2.schema.json` when constructing a recording request.
- READ `references/rigorloop-records-v4.schema.json` when checking the types used by that request.

- READ `references/rem-methods-functional-analysis.md` when deriving logical behavior.
- READ `references/rem-models-system-design.md` when editing Functions and relationships.
- READ `references/rem-models-requirements.md` when checking governing SR constraints.

- READ `references/requirement-to-delivery-model.md` when applying its criteria to this responsibility.

- READ `references/test-quality.md` when applying its criteria to this responsibility.

- READ `references/boundary-first-method-v1.md` when applying its criteria to this responsibility.

- READ `references/rem-practices-engineer-change-README.md` when needing an illustrative application of the canonical methods; examples do not establish execution.
- READ `references/rem-practices-engineer-change-WORKED-EXAMPLE.md` when needing an illustrative application of the canonical methods; examples do not establish execution.

## Expected output

Report the actual scoped outcome, governing basis, changed subjects or recorded judgment, material gaps and the next authorized action. Distinguish progress, review approval, final verification and external publication; claim only outcomes supported by this invocation.
