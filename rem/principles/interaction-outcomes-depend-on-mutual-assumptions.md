# Interaction outcomes depend on mutual assumptions

Identity: `rem:principle:contracts`.

## Key takeaway

Provider behavior and consumer expectations can each be reasonable and still be incompatible.

## Summary

A contract makes the relevant assumptions and guarantees visible at an interaction boundary. The behavior of the combined system depends on their compatibility, not just on matching operation names or data types.

## Statement and explanation
An acknowledgement may mean accepted, completed, durable or visible. A consumer that relies on a stronger meaning than the provider supplies can fail despite both sides conforming to their own informal expectations. Errors, retries, ordering and units are equally consequential forms of semantic agreement.

## Example
A client retries an operation after a timeout. If timeout leaves completion unknown, retrying may duplicate the effect unless the interaction provides an appropriate identification or recovery mechanism. This is an issue to analyze; this Principle does not prescribe idempotency for every operation or select an implementation.

## Source basis and REM synthesis

[NASA Interface Management](../sources/S17.md) includes interface rationale, assumptions, anomalies and agreements. The acknowledgement and retry examples are REM-authored illustrations of semantic compatibility; the source does not prescribe an idempotency mechanism or REM provider cardinality.

## Scope and limits
More contract detail is not always better. Exposing internal scheduling unnecessarily can restrict future designs. Leaving externally relevant failure behavior implicit can be equally damaging. The useful boundary is determined by what each party needs to rely on.

## Challenge
Ask whether a consumer can explain its decision for each significant outcome, including uncertainty. A signature match or schema pass cannot answer that question on its own.

## Deeper knowledge
[Interface](../concepts/system-and-architecture.md#system-and-architecture-assets); [Architecture Design model](../models/architecture-design.md); [Architecture Design](../methods/architecture-design.md).
