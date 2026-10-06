---
name: architecture-design
description: Define Module responsibilities, Interfaces, Function allocation, state authority, realization and derived ARs. Compose appropriate 4+1 views for integrated design review.
---

# Architecture Design

Consume accepted IR/SRs, logical Functions and existing architecture. Refine accountable Module boundaries before choosing convenient file or tool groupings. Preserve stable Module/Interface identities when only names change, use clear responsibility names, and make parent/child responsibility and boundary exposure explicit.

Allocate Functions to accountable Modules; define Interfaces, interactions and state/data authority. Derive ARs from SRs once architectural accountability is meaningful. Keep ARs under their owning SR in the requirement model, with one accountable Module; a delivery task is not an AR or a second authoritative obligation. Parent visibility does not duplicate descendant ownership.

Define material technology choices and rationale in the owning architecture realization. Distinguish intended design from observed implementation. A selected database or runtime realizes logical responsibility; it is not automatically a new REM Module.

Generate and inspect relevant Logical, Process, Development, Physical and Scenario views from their owning model data. Keep governed Scenarios black-box; internal participation belongs in derived Scenario views. Use concise dependency, sequence or state diagrams when they clarify the question. A Development view explains intended code organization and dependencies; it can name meaningful directories/files without merely cataloguing today's checkout. Reuse repository data and existing generators rather than maintaining duplicate diagrams or tables.

Return missing system obligations to requirement-analysis and incoherent logical behavior to system-design. Submit the combined affected design and AR allocation to one integrated design-review. Views and successful schema checks cannot approve the design.

## Recording boundary

For Change-managed work, read the packaged operational interface reference before relying on or updating current state. Use supported CLI tasks and the inspected opaque revision; skills do not use SQL or edit runtime storage. An isolated invocation keeps its requested scope. Installation alone does not adopt workflow policy.

## Resource map

- READ `references/operational-recording.md` when inspecting or recording Change-managed work.
- READ `references/targeted-recording-v2.schema.json` when constructing a recording request.
- READ `references/rigorloop-records-v4.schema.json` when checking the types used by that request.

- READ `references/rem-methods-architecture-design.md` when refining accountable architecture.
- READ `references/rem-methods-architecture-allocation.md` when allocating Functions and deriving ARs.
- READ `references/rem-methods-architecture-views.md` when selecting and inspecting views.
- READ `references/rem-models-architecture-design.md` when editing Modules, Interfaces or realization.
- READ `references/rem-models-requirements.md` when editing ARs.
- READ `references/rem-methods-5w2h.md` when analyzing allocated obligations.

- READ `references/requirement-to-delivery-model.md` when applying its criteria to this responsibility.

- READ `references/test-quality.md` when applying its criteria to this responsibility.

- READ `references/boundary-first-method-v1.md` when applying its criteria to this responsibility.

- READ `references/rem-methods-realization-design.md` when reasoning about realization design in the selected scope.
- READ `references/rem-methods-view-presentation.md` when reasoning about view presentation in the selected scope.
- READ `references/rem-methods-views-logical.md` when assessing logical architecture concerns.
- READ `references/rem-methods-views-process.md` when assessing process architecture concerns.
- READ `references/rem-methods-views-development.md` when assessing development architecture concerns.
- READ `references/rem-methods-views-physical.md` when assessing physical architecture concerns.
- READ `references/rem-methods-views-scenario.md` when assessing scenario architecture concerns.
- READ `references/rem-models-architecture-allocation.md` when reasoning about architecture allocation in the selected scope.
- READ `references/rem-models-architecture-boundaries.md` when reasoning about architecture boundaries in the selected scope.
- READ `references/rem-models-architecture-realization.md` when reasoning about architecture realization in the selected scope.
- READ `references/rem-practices-engineer-change-README.md` when needing an illustrative application of the canonical methods; examples do not establish execution.
- READ `references/rem-practices-engineer-change-WORKED-EXAMPLE.md` when needing an illustrative application of the canonical methods; examples do not establish execution.

## Expected output

Report the actual scoped outcome, governing basis, changed subjects or recorded judgment, material gaps and the next authorized action. Distinguish progress, review approval, final verification and external publication; claim only outcomes supported by this invocation.
