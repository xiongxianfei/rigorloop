# Origin and realization answer different questions

Identity: `rem:principle:origins`.

## Key takeaway

Knowing what implements an obligation does not tell us why that obligation was introduced.

## Summary

An obligation has a formation history and a downstream engineering history. One explains stakeholder contributions and decisions; the other explains design, implementation and assessment. Retaining only the final requirement and its code links can leave the original purpose unrecoverable.

## Statement and explanation
The relations that justify a requirement are not the same as the relations that realize it. A link from code to an SR answers a different question from a link from that SR to a customer report and a reconciliation decision.

## Example
Two complaints may lead to one timeout requirement. The implementation link shows where timeout behavior lives. Only the origin-side account reveals that one complaint concerned loss of control and another concerned unnecessary waiting. Changing the timeout can affect those concerns differently.

## Source basis and REM synthesis

[Gotel and Finkelstein](../references/gotel-finkelstein-1994-requirements-traceability-problem.md#located-contribution) distinguish traceability before and after requirements enter a specification. The separate questions about formation and realization follow that distinction. REM selects its own traceability relationships and retention rules.

## Scope and limits
The relationship supports maintaining reasons for reuse, rejection or modification of incoming requests. It does not imply retaining every chat message indefinitely or assigning every input a governed object. Sensitivity, privacy, retention cost and actual retrieval needs remain project considerations.

## Counter-signal
A trace chain that cannot answer the stakeholder question, or that points only to repeated summaries of one source, is weak origin evidence even when all links resolve.

## Applications
[Traceability](../concepts/assurance.md#assurance-and-traceability); [Requirement Analysis](../methods/requirement-analysis.md); [Engineer a change](../practices/engineer-a-change.md). Exact edge types and cardinalities remain governed by the current [Requirement model](../models/requirements.md) and [Model composition](../models/README.md).
