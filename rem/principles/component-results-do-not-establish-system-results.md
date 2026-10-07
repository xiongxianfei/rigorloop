# Component results do not establish system results

Identity: `rem:principle:integration`.

## Key takeaway

Each part can satisfy its local obligations while their interaction fails the larger outcome.

## Summary

Local obligations cover only the conditions assigned to them. Timing, shared state, incompatible assumptions and failure propagation arise at interactions. A decomposition argument therefore needs a composition argument before the whole outcome is justified.

## Statement and mechanism
The conjunction of local results implies an end-to-end result only when the relevant connections, conditions and interactions are also justified. Missing an interaction condition leaves a gap, even if every local test passes.

## Example
A Builder creates complete release content and a Store can retain it. Neither fact alone establishes that a Reader cannot observe the pointer to that content before it is complete. Publication visibility is an integration concern unless a contract and mechanism settle it.

## Source basis and REM synthesis

[NASA Product Integration](../references/nasa-2016-systems-engineering-handbook.md#product-integration) treats subsystem/environment interactions and adverse emergent behavior as integration concerns. The need for a composition argument and the publication example are REM's explanatory application of that concern.

## Scope and limits
The explanatory relationship is useful whenever responsibility is distributed. It does not prohibit compositional proof: a valid proof with adequate assumptions can establish the whole. Nor does it require repeating every component test at system level. The assessment should target the missing interaction argument.

## Counter-signal
A claim that “all child requirements pass, therefore the parent passes” without explaining the interactions remains unsupported. Conversely, evidence that an interface guarantee closes the identified gap can justify reducing redundant testing.

## Applications
[Architecture Design model](../models/architecture-design.md); [Assurance model](../models/README.md#assurance); [Architecture Allocation](../methods/architecture-allocation.md); [Verify and validate a slice](../practices/verify-and-validate-a-bounded-slice.md).
