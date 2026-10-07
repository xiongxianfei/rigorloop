# Principle 18: Preserve responsibility ownership through technical realization

## Relationship and why

Logical responsibility and technical realization need not have the same boundaries or rate of change. A responsibility can be realized by several technical units, and a technical unit can contribute to several responsibilities. Explicit realization mappings preserve accountability through those choices instead of letting deployment or code placement silently redefine it.

## REM commitment

Modules and Interfaces remain the durable first-class architecture assets. Material software structures, runtime/process boundaries, persistence mechanisms, deployment choices, interaction mechanisms, and technology selections are governed as subordinate realization information owned by those assets.
The technical model makes component responsibilities, contracts and realization mappings explicit. Its technical structure may be presented within the Logical View; that presentation does not turn components into Modules or transfer accountability. Development explains source/package/build organization, Process explains execution, and Physical explains placement using the same owned design.

## Application

[Architecture realization](../models/architecture-realization.md) owns the subordinate mappings and their consistency; [Realization Design](../methods/realization-design.md) develops them.
