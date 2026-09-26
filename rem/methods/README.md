# REM methods

Methods are repeatable procedures for producing and refining engineering information.
They apply the [principles](../principles/README.md) to the structures defined by the [models](../models/README.md).

| Method | Use | Result |
| --- | --- | --- |
| [5W2H](5w2h.md) | Analyze each IR, SR, and AR and expose missing information | Attributed answers, explicit unknowns, and a bounded understanding of the need or obligation |
| [Requirement Analysis](requirement-analysis.md) | Develop and name IRs, derive SRs, confirm Functions, and later allocate ARs | Clear requirements and confirmed logical behavior with explicit boundaries |
| [Scenario Analysis](scenario-analysis.md) | Create and govern black-box stakeholder Scenarios for an IR, confirm the durable Feature, and expose candidate system obligations | First-class Scenarios with stable identity/lifecycle, a confirmed Feature, and traceable inputs to SR analysis |

5W2H is required at every requirement level in the selected requirement-authoring method.
Every question needs an answer, an explicit unknown, or justified non-applicability at that level.
The statement expresses the authoritative need or obligation; analysis explains all seven dimensions, including the problem and desired outcome under What.
The method does not prescribe a file format or a separate analysis document.
Other methods can be added when their purpose, inputs, steps, outputs, and limits are clear.

## Engineering cycle

1. Analyze the initial need with [5W2H](5w2h.md) and establish an IR.
2. Apply [Scenario Analysis](scenario-analysis.md) to create or refine governed stakeholder-visible Scenarios and confirm the durable Feature.
3. Derive system obligations as SRs and confirm the required logical Functions.
4. Allocate Functions to architectural Modules.
5. Derive ARs from SRs and allocate their lower-level obligations to architectural responsibility.
6. Define or change Interfaces.
7. Realize the architecture in code, configuration, or other implementation.
8. Apply Verification to the Requirements.
9. Capture actual Evidence.
10. Review the complete engineering result and the conclusions supported by that evidence.
11. Establish the new Baseline through the project's controlled-change process.

The cycle is iterative, not a one-way waterfall.
Architecture may expose missing obligations, implementation may expose missing behavior, and verification may require design correction.
Return to the responsible definition and reconcile affected relationships when that occurs.

## Using a method

Distinguish stakeholder statements, observed facts, derived conclusions, assumptions, and unresolved questions.
Record the reasoning needed to review the result without reconstructing the original conversation.
Do not treat a completed worksheet as approval, implementation, or evidence of requirement satisfaction.
