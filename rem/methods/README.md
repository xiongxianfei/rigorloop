# REM methods

Methods are repeatable procedures for producing and refining engineering information.
They use the [principles](../principles/README.md) as explanatory guidance while applying the selected rules defined by the [models](../models/README.md).

| Method | Use | Result |
| --- | --- | --- |
| [5W2H](5w2h.md) | Analyze each IR, SR, and AR and expose missing information | Attributed answers, explicit unknowns, and a bounded understanding of the need or obligation |
| [Requirement Analysis](requirement-analysis.md) | Reconcile RR input with current needs, reuse/refine/create IRs, derive/refine SRs, and formulate ARs when architecture provides allocation context | Clear normative requirements with explicit parentage, provenance, disposition, and assessment intent |
| [Scenario Analysis](scenario-analysis.md) | Develop governed stakeholder-visible situations and confirm the durable Feature | First-class Scenarios, a durable Feature, and candidate obligations/behavior |
| [Functional Analysis](functional-analysis.md) | Confirm logical Functions from SR obligations and reconcile Feature realization | Durable Functions with clear logical boundaries and explicit SR/Feature traceability |
| [Architecture Allocation](architecture-allocation.md) | Establish/refine Module hierarchy, allocate Functions, derive/refine and allocate ARs at the lowest coherent accountable Modules, and identify/expose logical Interfaces | Accountable hierarchical architectural responsibility with reconciled requirement/behavior allocation and explicit encapsulation |
| [Architecture Design](architecture-design.md) | Develop the complete hierarchical logical architecture and its material physical/software realization | Semantic Module containment, Interface/exposure, state/data ownership, material subordinate realization information, explicit deferrals, and derived review views |
| [4+1 Architecture Views](architecture-views.md) | Generate and assess standard architecture projections for comprehension and cross-view validation | Traceable Logical, Process, Development, Physical, and Scenario presentations with assessed semantic fidelity and intended reading tasks |
| [Verification](plan-and-assess-verification.md) | Assess specified obligations | Identified criteria, plan, actual observations and scoped judgment |
| [Intended-use validation](validate-stakeholder-outcomes.md) | Assess stakeholder outcomes in representative use | Attributable outcome evidence, limitations and corrective work |

5W2H is required at every requirement level in the selected requirement-authoring method.
Every question needs an answer, an explicit unknown, or justified non-applicability at that level.
The statement expresses the authoritative need or obligation; analysis explains all seven dimensions.

Methods do not own Concept definitions or Model cardinalities.
They link to the authoritative knowledge and explain how engineers produce information that satisfies it.

## Applying methods together

[Engineer a change](../practices/engineer-a-change.md#stage-map-and-entry-routes) owns the iterative application sequence from RR reconciliation through design, realization, assessment and Baseline evolution.
[Practices](../practices/README.md) provide other goal-oriented reading paths without redefining individual methods.

## Using a method

Distinguish stakeholder statements, observed facts, derived conclusions, assumptions, and unresolved questions.
Record enough reasoning to review the result without reconstructing the original conversation.
Do not treat a completed worksheet as approval, implementation, or evidence of requirement satisfaction.
