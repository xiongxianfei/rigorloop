# Principle 15: Keep configuration-management technology replaceable while preserving engineering semantics

## Relationship and why

Engineering meaning and the mechanisms used to store or recover it are related but distinct. Tying meaning to one storage technology makes a tool replacement risk becoming an unintended method change. Separating the required preservation properties from their technical realization lets a project change tools while checking that its engineering history remains meaningful and recoverable.

## REM commitment

A tool-independent method requires controlled, recoverable engineering history without prescribing a particular technology.

## Application

[Operational Support](../models/operational-support.md) owns selected representations and maintenance; the [Evolution model](../models/README.md#evolution) owns the history those mechanisms preserve.
