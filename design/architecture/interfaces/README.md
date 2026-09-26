# Interfaces

An Interface defines an explicit interaction contract between architectural elements.
It describes what providers and consumers can rely on at their boundary.

The intended collection uses one `IF-<id>.json` file per Interface.
Names and contract descriptions belong in the entity content, independently of its stable identity.
No Interface records are present yet.

Define operations or messages, inputs and outputs, failure behavior, and compatibility rules.
Include protocol, ordering, and state constraints when they affect the contract.
The contract may describe an internal interaction; it need not be a network API.

[Modules](../modules/README.md) identify the Interfaces they provide and consume.
Derive provider and consumer views from those Module-owned references rather than repeating their membership here.
