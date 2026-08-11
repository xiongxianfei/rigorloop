# Architecture Assessment

Assessment: architecture-required

## Rationale

The approved spec formalizes the published `code-review` boundary as a package composed from canonical `SKILL.md`, mapped references, and mapped assets. It also introduces a long-lived conditional-policy resource, constrains which rules remain inline, and requires canonical, generated, packed, and installed package integrity with atomic rollback.

These decisions cross authored-source, packaged-resource, generated-adapter, installer-materialization, validation, and workflow-policy boundaries. Architecture must identify package ownership, conditional loading, resource projection, validation responsibility, failure propagation, and rollback without creating a new runtime or validator family.

The existing published-skill resource-integrity architecture can be specialized rather than replaced. A new ADR is not required unless architecture authoring discovers an unresolved, hard-to-reverse decision not already governed by the approved published-skill package architecture.

## Result

Proceed through `architecture` and `architecture-review` before planning.
