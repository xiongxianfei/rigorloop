# REM methods

Methods are repeatable procedures for producing and refining engineering information.
They apply the [principles](../principles/README.md) to the structures defined by the [models](../models/README.md).

| Method | Use | Result |
| --- | --- | --- |
| [5W2H](5w2h.md) | Analyze each IR, SR, and AR and expose missing information | Attributed answers, explicit unknowns, and a bounded understanding of the need or obligation |
| [Requirement Analysis](requirement-analysis.md) | Reconcile RR input with current needs, reuse/refine/create IRs, derive/refine SRs, and formulate ARs when architecture provides allocation context | Clear normative requirements with explicit parentage, provenance, disposition, and assessment intent |
| [Scenario Analysis](scenario-analysis.md) | Develop governed stakeholder-visible situations and confirm the durable Feature | First-class Scenarios, a durable Feature, and candidate obligations/behavior |
| [Functional Analysis](functional-analysis.md) | Confirm logical Functions from SR obligations and reconcile Feature realization | Durable Functions with clear logical boundaries and explicit SR/Feature traceability |
| [Architecture Allocation](architecture-allocation.md) | Establish/refine Module hierarchy, allocate Functions, derive/refine and allocate ARs at the lowest coherent accountable Modules, and identify/expose logical Interfaces | Accountable hierarchical architectural responsibility with reconciled requirement/behavior allocation and explicit encapsulation |
| [Architecture Design](architecture-design.md) | Develop the complete hierarchical logical architecture and its material physical/software realization | Semantic Module containment, Interface/exposure, state/data ownership, material subordinate realization information, explicit deferrals, and derived review views |
| [4+1 Architecture Views](architecture-views.md) | Generate and assess standard architecture projections for comprehension and cross-view validation | Traceable Logical, Process, Development, Physical, and Scenario presentations with assessed semantic fidelity and intended reading tasks |

5W2H is required at every requirement level in the selected requirement-authoring method.
Every question needs an answer, an explicit unknown, or justified non-applicability at that level.
The statement expresses the authoritative need or obligation; analysis explains all seven dimensions.

Methods do not own Concept definitions or Model cardinalities.
They link to the authoritative knowledge and explain how engineers produce information that satisfies it.

## Engineering cycle

1. Treat the incoming request, proposal, issue, incident, observation, or equivalent source as RR input. Reconcile it with current IRs, SRs, Scenarios, Features, and known constraints before creating new durable requirements.
2. Establish or refine the justified IRs with [5W2H](5w2h.md), preserving RR provenance and explicit no-change, conflict, or unresolved dispositions where applicable.
3. Apply [Scenario Analysis](scenario-analysis.md) to confirm the durable Feature and first-class stakeholder Scenarios for the affected need.
4. Derive or refine system obligations as SRs through [Requirement Analysis](requirement-analysis.md).
5. Use [Functional Analysis](functional-analysis.md) to reuse, refine, or confirm the logical Functions required by the SRs and reconcile Feature realization.
6. Establish or refine the Module responsibility hierarchy and use [Architecture Allocation](architecture-allocation.md) to allocate each Function to one primary Module, normally the lowest coherent accountable Module.
7. With those architectural boundaries available, derive or refine justified ARs from SRs and allocate each AR to exactly one accountable Module; reconcile AR and Function allocation without duplicating ownership on ancestors.
8. Define or refine architecturally significant Interfaces, explicitly expose descendant-provided contracts through parent boundaries when needed, and establish significant state/data ownership.
9. Use [Architecture Design](architecture-design.md#design-the-physicalsoftware-realization) to define only material software, runtime, persistence, deployment, Interface-realization, and technology decisions as subordinate Module/Interface information.
10. Use [4+1 Architecture Views](architecture-views.md) to derive and render Logical, Process, Development, Physical, and Scenario projections, assess their meaning and intended reading tasks, and reconcile findings with their responsible owners.
11. Realize the architecture in code, configuration, infrastructure, and other implementation artifacts.
12. Apply Verification to the Requirements and capture actual Evidence.
13. Review the complete engineering result and the conclusions supported by that evidence as required by the project's governance; REM does not prescribe concrete review-stage names or cadence.
14. Establish the new Baseline through the project's controlled-change process.

The cycle is iterative, not a one-way waterfall.
Architecture may expose missing obligations, implementation may expose missing behavior, and verification may require design correction.
Return to the authoritative Concept, Model, Requirement, or Method output that owns the discovered issue and reconcile downstream relationships.

## Using a method

Distinguish stakeholder statements, observed facts, derived conclusions, assumptions, and unresolved questions.
Record enough reasoning to review the result without reconstructing the original conversation.
Do not treat a completed worksheet as approval, implementation, or evidence of requirement satisfaction.
