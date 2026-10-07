# Principle 4: Model durable architectural structure as hierarchical Modules and Interfaces

## Relationship and why

Responsibility and interaction are complementary: knowing who performs work does not by itself explain the contract through which others depend on it. A hierarchy can refine a broad responsibility into coherent parts while Interfaces make their interactions explicit. This helps readers understand both the boundaries and the cooperation of the architecture.

## REM commitment

Modules express responsibility and may contain Modules that refine broader responsibility; Interfaces express interaction contracts.

## Application

[Architecture boundaries](../models/architecture-boundaries.md) define Module containment and Interface contracts; [Architecture Allocation](../methods/architecture-allocation.md) applies those definitions.
