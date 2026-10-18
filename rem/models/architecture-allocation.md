# Allocation

## Allocation

```text
Feature ── realizedBy ──> Function ── primaryModule ──> Module
                                 └── supportingModule ──> Module (0..*)

SR ── derivation ──> AR ── allocatedTo ──> Module
```

Functional allocation and requirement allocation are separate engineering relationships.
Review them together so the assigned behavior, state, policy, data, and interfaces can satisfy the allocated obligations.

## Function allocation cardinality

Every active Function MUST have exactly one accountable primary Module before architecture allocation is considered complete.
A Function MAY involve zero or more supporting Modules.

The primary Module owns the architectural responsibility for the Function.
Supporting Modules may contribute required behavior or services without becoming co-owners of the Function.

Allocate the Function to the lowest Module in the containment hierarchy that can coherently own the complete behavior. Parent Modules receive derived roll-up visibility over descendant allocations but do not become additional owners merely because they contain the accountable Module. A Function MAY be allocated directly to a parent when the behavior genuinely belongs to that broader responsibility boundary.

If no single Module can own the Function coherently, reconsider the Function boundary or Module boundaries rather than leaving responsibility ambiguous.

## AR allocation cardinality

Every active AR MUST be allocated to exactly one Module.

If an allocated obligation genuinely belongs to several Modules, decompose it into separate ARs under the same parent SR so each lower-level obligation has one accountable Module.
Do not assign one AR to several Modules to avoid deciding responsibility.

This convergence does not require every AR to pair one-to-one with a Function.
An AR may govern state, quality, policy, data, or another architectural responsibility.

Allocate the AR to the lowest Module in the containment hierarchy that can coherently own the complete obligation. Parent Modules receive derived roll-up visibility over descendant ARs but are not additional allocated owners. An AR MAY be allocated directly to a parent when the obligation applies to the broader parent boundary itself.
