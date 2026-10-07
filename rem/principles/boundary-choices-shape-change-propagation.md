# Boundary choices shape change propagation

Identity: `rem:principle:change-propagation`.

## Key takeaway

When several components depend on the same changeable design detail, changing it can require coordinated revisions.

## Summary

A boundary can limit change propagation by preventing consumers from relying on decisions they do not need to know. The benefit depends on which decisions are likely to change and on whether the exposed contract is sufficient. Small size or hierarchical nesting alone does not create that benefit.

## Statement and explanation
Knowledge of a representation, calling convention or storage policy creates a dependency. Hiding that detail behind a useful contract can allow its replacement without changing every consumer. The contract itself still couples the parties and can become a change boundary.

## Example
A reader that depends only on a release-retrieval contract need not know whether the data are sharded or compressed. If it also reads the provider’s internal manifest format, the nominal interface boundary no longer contains that dependency.

## Source basis and REM synthesis

[Parnas](../sources/S10.md) compares decomposition around processing steps with hiding change-sensitive design decisions. This supports reasoning about change propagation, not a universal Module size, nesting depth or benefit from every extra abstraction.

## Scope and tradeoffs
An extra abstraction can add indirection, latency and maintenance work. If the hidden detail is actually shared semantics that consumers must understand, suppressing it produces ambiguity rather than useful encapsulation. A project should compare concrete change scenarios, not only draw cleaner boxes.

## What would weaken an application
The proposed boundary does not contain the expected change; consumers still need the internal detail; or the new coordination cost dominates its benefit. These are reasons to revisit the design, not to insist that the Principle implies one decomposition.

## Deeper knowledge
[Architecture Design model](../models/architecture-design.md); [Architecture Allocation](../methods/architecture-allocation.md); [Architecture Design](../methods/architecture-design.md).
