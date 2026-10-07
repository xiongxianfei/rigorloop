---
name: design-review
description: Independently assess System Design and Architecture Design together against the accepted requirement basis, including Functions, allocation, Interfaces, ARs and realization.
---

# Design Review

Review the complete affected design composition: accepted obligations, required logical behavior, accountable Modules, Interfaces, derived ARs, state/data authority and material realization. Supporting views reveal interactions and gaps; they are projections of the owning design, not separate approval targets that must each receive a gate.

Check that the combined design can satisfy the accepted IR/SRs and relevant constraints. Inspect scope, feasibility, boundary behavior, failures, compatibility, supporting rationale and acceptance intent. Reuse existing applicable definitions where sufficient. Distinguish a reviewed target design from current implementation observations.

Return need/scope/obligation defects to requirement-analysis, Function/behavior defects to system-design, and responsibility/Interface/AR/realization defects to architecture-design. Delivery sequencing and concrete proof allocation belong to plan; do not take them over to fill a design gap.

Record the exact reviewed subjects, accepted governing basis, actual independent reviewer, findings and judgment under the design purpose. Do not edit the authors' definitions and approve the repaired result. Assess corrections in proportion to their effects while retaining adequate integrated coverage. One integrated design-review covers the two authoring responsibilities.

## Recording boundary

For Change-managed work, read the packaged operational interface reference before relying on or updating current state. Use supported CLI tasks and the inspected opaque revision; skills do not use SQL or edit runtime storage. An isolated invocation keeps its requested scope. Installation alone does not adopt workflow policy.

## Resource map

- READ `references/operational-recording.md` when inspecting or recording Change-managed work.
- READ `references/targeted-recording-v2.schema.json` when constructing a recording request.
- READ `references/rigorloop-records-v4.schema.json` when checking the types used by that request.

- READ `references/rem-models-system-design.md` when reviewing logical behavior.
- READ `references/rem-models-architecture-design.md` when reviewing architectural responsibility and realization.
- READ `references/rem-models-requirements.md` when reviewing AR and governing requirement consistency.
- READ `references/rem-methods-architecture-views.md` when assessing view fidelity and coverage.

- READ `references/boundary-first-method-v1.md` when the project applies its boundary first method v1 criteria to this invocation.

- READ `references/requirement-to-delivery-model.md` when the project applies its requirement to delivery model criteria to this invocation.

- READ `references/review-assessment.md` when the project applies its review assessment criteria to this invocation.

- READ `references/review-reliance.md` when the project applies its review reliance criteria to this invocation.

- READ `references/test-quality.md` when the project applies its test quality criteria to this invocation.

- READ `references/rem-models-architecture-allocation.md` when reasoning about architecture allocation in the selected scope.
- READ `references/rem-models-architecture-boundaries.md` when reasoning about architecture boundaries in the selected scope.
- READ `references/rem-models-architecture-realization.md` when reasoning about architecture realization in the selected scope.
- READ `references/rem-methods-view-presentation.md` when reasoning about view presentation in the selected scope.
- READ `references/rem-methods-views-logical.md` when assessing logical architecture concerns.
- READ `references/rem-methods-views-process.md` when assessing process architecture concerns.
- READ `references/rem-methods-views-development.md` when assessing development architecture concerns.
- READ `references/rem-methods-views-physical.md` when assessing physical architecture concerns.
- READ `references/rem-methods-views-scenario.md` when assessing scenario architecture concerns.

- READ `references/rem-models-operational-support.md` when applying shared definition clarity, semantic authority, representation or maintenance rules.

## Expected output

Report the actual scoped outcome, governing basis, changed subjects or recorded judgment, material gaps and the next authorized action. Distinguish progress, review approval, final verification and external publication; claim only outcomes supported by this invocation.
