# ADR-20260428-architecture-package-method: C4, arc42, and ADR Architecture Package Method

## Status
accepted

## Context

RigorLoop needs architecture guidance that is consistent, reviewable, and traceable. Existing architecture work can vary between ad hoc diagrams, broad prose documents, and decision notes embedded in larger artifacts. That drift makes it harder for contributors and reviewers to distinguish structure, runtime behavior, deployment impact, cross-cutting concerns, and durable decisions.

The accepted proposal and approved spec require a focused architecture package method based on C4, official arc42 sections, and ADRs. The method also introduces one canonical architecture package, change-local architecture deltas for architecture-significant changes, templates under `templates/`, and Mermaid source diagrams for the first implementation.

## Decision

Adopt C4 plus official arc42 plus ADRs as RigorLoop's default architecture package method.

Use one canonical architecture package under:

```text
docs/architecture/system/architecture.md
docs/architecture/system/diagrams/context.mmd
docs/architecture/system/diagrams/container.mmd
```

Use all 12 official arc42 sections in the canonical `architecture.md`, while keeping content concise and allowing explicit `Not applicable` rationale.

Use C4 system context and container diagrams by default, stored as Mermaid `.mmd` source files in the first implementation.

Use change-local architecture deltas under `docs/changes/<change-id>/architecture.md` only when architecture-significant work needs working design reasoning before accepted content is merged into the canonical package.

Store architecture and ADR scaffolds under `templates/`, and treat `templates/` as canonical authored workflow content.

Keep the first implementation review-based. Add only the narrow existing lifecycle-validator compatibility needed for `docs/architecture/system/architecture.md`; do not add required package-shape enforcement automation in the first implementation.

## Alternatives considered

### Keep current architecture skill guidance and ad hoc diagrams

Rejected because it leaves artifact shape, diagram expectations, runtime reasoning, deployment reasoning, and ADR thresholds inconsistent.

### Use C4 only

Rejected because diagrams alone do not preserve runtime, deployment, cross-cutting, quality, risk, and decision reasoning.

### Use arc42 only

Rejected because the written structure does not itself provide a shared visual language for system and container boundaries.

### Use ADR only

Rejected because decision records preserve why, but they do not explain the whole architecture or current structure.

### Create a new canonical architecture document for every feature

Rejected because it would create competing current architecture sources and make merge-back discipline harder.

## Consequences

- Architecture work has a consistent package shape for non-trivial architecture changes.
- Reviewers can check C4 sufficiency, all arc42 sections, runtime/deployment conditions, cross-cutting concerns, risks, and ADR completeness.
- Feature-specific architecture deltas stay temporary and must merge durable content into the canonical package.
- Important architecture decisions become durable ADRs rather than prose-only notes.
- `templates/` must be added to governance as canonical authored workflow content.
- Existing legacy architecture artifacts need a follow-on normalization artifact before the repository can claim all architecture docs fit the canonical package lifecycle.
- Future enforcement automation must wait until at least one real package has used the method and a later approved contract defines the required checks.

## Follow-up

- Architecture-review approved this ADR with the architecture-method change delta on 2026-04-28.
- Implement the canonical package, templates, workflow pointer, governance updates, skill updates, generated output refresh, and lifecycle-validator compatibility.
- Create the follow-on legacy architecture lifecycle normalization artifact.
