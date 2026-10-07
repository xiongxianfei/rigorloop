# Principle 20: Preserve encapsulation through Module hierarchy

## Relationship and why

A parent responsibility is meaningful only if its boundary continues to govern how its parts are used from outside. Child collaboration and implementation placement do not automatically expose a contract across that boundary or determine who owns it. Keeping containment, contract ownership and realization distinct supports local refinement without silently transferring accountability.

## REM commitment

Parent Modules are real architectural responsibility boundaries. Child Modules refine their parent responsibility; allocations target the lowest coherent accountable Module; descendant allocations roll up for comprehension without duplicating ownership; and a child-provided Interface remains internal to its containing boundary unless explicitly exposed through each parent boundary it crosses.
Assign Interface ownership to the Module accountable for the contract and assign its realizing behavior separately. A parent may own a contract realized through child responsibilities; implementation location alone does not determine its provider.

## Application

[Architecture boundaries](../models/architecture-boundaries.md) own containment, encapsulation, contract ownership and exposure; [architecture allocation](../models/architecture-allocation.md) owns accountable allocation and roll-up interpretation.
