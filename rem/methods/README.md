# REM methods

Methods are repeatable procedures for producing and refining engineering information.
They apply the [principles](../principles/README.md) to the structures defined by the [models](../models/README.md).

| Method | Use | Result |
| --- | --- | --- |
| [5W2H](5w2h.md) | Analyze each IR, SR, and AR and expose missing information | Attributed answers, explicit unknowns, and a bounded understanding of the need or obligation |
| [Requirement Analysis](requirement-analysis.md) | Establish IRs, derive SRs, and derive ARs | Clear normative requirements with explicit parentage and assessment intent |
| [Scenario Analysis](scenario-analysis.md) | Develop governed stakeholder-visible situations and confirm the durable Feature | First-class Scenarios, a durable Feature, and candidate obligations/behavior |
| [Functional Analysis](functional-analysis.md) | Confirm logical Functions from SR obligations and reconcile Feature realization | Durable Functions with clear logical boundaries and explicit SR/Feature traceability |
| [Architecture Allocation](architecture-allocation.md) | Allocate Functions and ARs to Modules and identify logical Interfaces | Accountable logical architectural responsibility with reconciled requirement/behavior allocation |
| [Architecture Design](architecture-design.md) | Develop the complete logical architecture and its material physical/software realization | Semantic Module/Interface outputs, state/data ownership, material subordinate realization information, explicit deferrals, and derived review views |

5W2H is required at every requirement level in the selected requirement-authoring method.
Every question needs an answer, an explicit unknown, or justified non-applicability at that level.
The statement expresses the authoritative need or obligation; analysis explains all seven dimensions.

Methods do not own Concept definitions or Model cardinalities.
They link to the authoritative knowledge and explain how engineers produce information that satisfies it.

## Engineering cycle

1. Analyze the initial need with [5W2H](5w2h.md) and establish an IR.
2. Apply [Scenario Analysis](scenario-analysis.md) to confirm the durable Feature and first-class stakeholder Scenarios.
3. Derive system obligations as SRs through [Requirement Analysis](requirement-analysis.md).
4. Use [Functional Analysis](functional-analysis.md) to confirm the logical Functions required by the SRs and realize the Feature.
5. Establish or refine Module responsibility and use [Architecture Allocation](architecture-allocation.md) to allocate each Function to one primary Module.
6. Derive ARs from SRs and allocate each AR to exactly one accountable Module; reconcile AR and Function allocation.
7. Define or refine architecturally significant Interfaces and establish significant state/data ownership.
8. Use [Architecture Design](architecture-design.md#design-the-physicalsoftware-realization) to define only material software, runtime, persistence, deployment, Interface-realization, and technology decisions as subordinate Module/Interface information.
9. Realize the architecture in code, configuration, infrastructure, and other implementation artifacts.
10. Apply Verification to the Requirements and capture actual Evidence.
11. Review the complete engineering result and the conclusions supported by that evidence.
12. Establish the new Baseline through the project's controlled-change process.

The cycle is iterative, not a one-way waterfall.
Architecture may expose missing obligations, implementation may expose missing behavior, and verification may require design correction.
Return to the authoritative Concept, Model, Requirement, or Method output that owns the discovered issue and reconcile downstream relationships.

## Using a method

Distinguish stakeholder statements, observed facts, derived conclusions, assumptions, and unresolved questions.
Record enough reasoning to review the result without reconstructing the original conversation.
Do not treat a completed worksheet as approval, implementation, or evidence of requirement satisfaction.
