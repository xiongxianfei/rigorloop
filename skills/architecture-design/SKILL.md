---
name: architecture-design
description: Refine accountable Modules, Interfaces, state ownership, realization and allocated requirements together with logical behavior.
---

# Architecture Design

Start with selected requirements, logical Functions and affected existing architecture. Reuse responsibility boundaries and stable identities where meaning continues; a new file or technology does not automatically create a Module.

In the same working loop as System Design, define changed Function allocation, Interfaces, interactions, state/data authority and material realization choices. Derive ARs only when architectural accountability is meaningful: one parent SR and one accountable Module; delivery tasks are not ARs. Record consequential choices, rationale and unresolved assumptions with their current owner.

Challenge the proposed behavior and architecture using representative normal, failure and boundary situations. Return missing obligations to requirement-analysis and behavior gaps to system-design. Resolve material unknowns before dependent work rather than covering them with an approval label.

Select views that answer actual questions about the affected scope. A sequence, state or dependency diagram can be sufficient; document omitted/combined concerns concisely under the owning view-selection rules. Reuse generated model views, keep stakeholder Scenarios black-box and place internal participation in derived views. Do not create a complete diagram set merely to fill a template.

Update the affected authoritative models and their consumers, then select the usable combined design for proportionate planning. Optional integrated Design Review assesses the complete affected composition; it is not a mandatory intermediate approval. Final whole-change review includes requirements, architecture, implementation and proof.

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
- READ `references/rem-practices-engineer-a-change.md` when needing an illustrative application of the canonical methods; examples do not establish execution.
- READ `references/rem-practices-WORKED-EXAMPLE.md` when needing an illustrative application of the canonical methods; examples do not establish execution.

- READ `references/rem-models-operational-support.md` when applying shared definition clarity, semantic authority, representation or maintenance rules.

- READ `references/rem-practices-make-an-architecture-decision.md` when comparing architecture alternatives, evidence and reopening conditions.

## Expected output

Report the actual scoped outcome, governing basis, changed subjects or recorded judgment, material gaps and the next authorized action. Distinguish progress, review approval, final verification and external publication; claim only outcomes supported by this invocation.
