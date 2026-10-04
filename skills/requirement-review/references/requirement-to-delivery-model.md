# Requirements and delivery

RR is incoming request material. Requirement Analysis reuses, refines or creates IRs/SRs against the current model; approval of a proposal does not create an IR. An IR expresses stakeholder need. A Feature is a durable stakeholder-visible capability, and a governed Scenario is a concrete black-box use. SRs state assessable system obligations. Requirements may be accepted for design before Functions and AR allocations are complete.

System Design defines logical Functions and behavior. Architecture Design allocates responsibility to Modules, defines Interfaces and realization, and derives ARs beneath their governing SRs. An AR is an architectural obligation with an accountable Module, not a delivery task. Preserve stable IDs, one authoritative definition and applicable rationale.

Delivery planning allocates accepted obligations and reviewed design to useful milestones/work items, dependencies and proof. It does not use Feature as a work-decomposition level or require one work item per requirement. A milestone completes its work and required checks; it needs no review approval to permit the next authorized milestone.

The trace is RR → accepted IR/SR → logical and architectural design, including applicable ARs → delivery work → implementation → evidence. Read it backward when assessing support. One independent whole-change Code Review gate precedes separate final Verify. Optional advice cannot replace it; corrections are reassessed within that gate. Current operational records preserve the useful handoff and selected support, while repository definitions retain current engineering meaning.
