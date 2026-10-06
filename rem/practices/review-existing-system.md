# Review an existing system

## Goal and inputs

Assess how an existing implementation corresponds to the applicable requirements and design.
Identify the actual implementation/configuration, current requirement/design basis, requested review scope and available observations.
An implementation inventory alone cannot supply stakeholder intent or approve missing design.

## Procedure

1. Establish which requirements and design definitions govern the scope and identify missing or uncertain authority.
2. Inspect observed entry points, behavior, state ownership and interactions. Distinguish source observations, runtime evidence and proposed interpretation.
3. Compare observed behavior with [Functions](../models/system-design.md) and accountable [architecture boundaries](../models/architecture-boundaries.md). Preserve gaps instead of inventing correspondence to complete a graph.
4. Use [Architecture Design](../methods/architecture-design.md) to propose corrections to responsibility, Interfaces or subordinate realization. Return new or changed needs to [Requirement Analysis](../methods/requirement-analysis.md).
5. Select [views](../methods/architecture-views.md#view-selection-and-tailoring) that expose the material questions and uncertainties.
6. Assess specified obligations through [verification](../methods/plan-and-assess-verification.md); assess stakeholder outcomes through [intended-use validation](../methods/validate-stakeholder-outcomes.md) when relevant to the claim.

## Outputs and limits

Produce attributable correspondences, discrepancies, evidence scope and an owned correction path.
The project's governance supplies review judgment and action authority.
Existing code, a diagram or a proposed mapping cannot by itself establish an accepted requirement, correct allocation or observed stakeholder success.
