# Architecture Assessment: Implement Skill Simplification

Assessment: architecture-not-required

## Rationale

The approved specification adds two mapped references and one mapped structural asset to the existing `implement` skill root, but it does not change the repository's published-skill package model.
Canonical skill source remains under `skills/`; `READ` and `COPY` retain their existing resource-class meanings; references remain packaged procedure rather than independent lifecycle owners; assets remain structural leaves; and canonical, generated, packed, and installed resources retain the existing relative-path and raw-byte parity chain.

The change introduces no runtime, persistent state, service, API, dependency, deployment topology, security boundary, adapter install-root rule, validation gate family, or lifecycle owner.
The approved feature specification fully owns the `implement`-specific profile predicates, reference responsibilities, result groups, preservation ledgers, and failure behavior.

The current architecture already states the general package and resource-integrity decisions needed by this change, including canonical source ownership, Resource-map verb classes, mapped-resource containment, package parity, assets as structural leaves, references as packaged procedure, deterministic acceptance, and rollback to one complete package revision.
No architecture document or ADR change is necessary.

## Reassessment triggers

Reassess as `architecture-required` if implementation or later review proposes any of the following:

- a new package ownership model or independent reference authority;
- a new runtime, service, persistent store, dependency, selector, scheduler, or validation gate family;
- transformed rather than raw-byte-parity resource packaging;
- an adapter install-root or publication-flow change;
- an architecture document change needed to make the package model accurate.

## Result

Proceed directly to `plan` and `plan-review`.
No architecture or architecture-review artifact is required for the approved scope.
