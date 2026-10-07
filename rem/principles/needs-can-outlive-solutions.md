# Needs can outlive particular solutions

Identity: `rem:principle:needs`.

## Key takeaway

A change to a solution need not be a change to the reason the solution exists.

## Summary

A stakeholder outcome and a mechanism intended to achieve it are different claims. When several mechanisms can serve the same outcome, the outcome can remain relevant after a mechanism is replaced. This explains why separating intent from realization can preserve useful reasoning through change.

## Statement and explanation
Where the outcome is not itself defined by a required implementation, a need can remain valid across different designs. Coupling its expression to a replaceable mechanism obscures which part of the reasoning has changed.

For example, “recover the reviewed release” can remain a goal whether the implementation uses files, a database or a service. This does not mean all mechanisms satisfy the same durability, cost or integrity conditions. Those conditions have to be made explicit before a choice is justified.

## Source basis and REM synthesis

[NASA requirements rationale](../sources/S01.md) distinguishes reasons, assumptions and implementation constraints. [Zave and Jackson](../sources/S12.md) distinguish requirements, specifications and domain knowledge. The enduring-need explanation is REM's synthesis; neither source prescribes its IR/SR/AR hierarchy.

## Applications and limits
The relationship supports examining a raw request, comparing alternate realizations and deciding whether a change concerns a need or only its implementation. It does not establish a three-level hierarchy. A regulated component, purchased interface or compatibility mandate can make a specific solution an actual constraint; its authority then belongs in the reasoning.

## Challenge or counter-signal
If the benefit depends on the specified mechanism itself, treating that mechanism as freely replaceable is wrong. Ask the stakeholder whether the value remains when an alternative mechanism is substituted; do not infer agreement from semantic similarity.

## Deeper knowledge
[Requirement model](../models/requirements.md); [Requirement Analysis](../methods/requirement-analysis.md); [Realization Design](../methods/realization-design.md).
