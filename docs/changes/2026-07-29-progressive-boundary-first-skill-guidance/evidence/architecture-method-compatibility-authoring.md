# Architecture Method Compatibility Authoring

- Artifact ID: `spec-architecture-package-method`
- Artifact path: `specs/architecture-package-method.md`
- Authoring stage: `spec`
- Completion status: `complete`
- Resulting review-request path: `docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/reviews/spec-review-architecture-method-r1.md`

## Trigger

Architecture-review R3 finding `AR3-001` identified a conflict between
architecture-method R8 and the active stage-owned lifecycle contract. This
supporting amendment will define stable owner-pointer metadata before the
arc42 sequence and keep mutable lifecycle state solely in the owning
`change.yaml` entry.

## Scope

The correction is limited to the conflicting method requirement and the
directly implementing architecture template and published architecture skill
wording. It does not change arc42 section order, C4 guidance, ADR policy, or
architecture review quality criteria.

R8 now requires stable owning-change-record metadata and assigns mutable state
exclusively to the matching `change.yaml` entry. The template and both
architecture skills use the same wording.
The substantively revised legacy spec now carries one stable pointer to this
owning change record instead of embedded mutable status.

Spec-review finding `APM-SR1-001` reopens authoring to align the same contract
for new governed ADRs while preserving unmigrated historical ADR compatibility.

R46-R48, AC7, observability, compatibility, the ADR template, and the public
architecture-review checklist now use stable owner pointers and exact
change-local lifecycle entries for new governed ADRs. Historical unmigrated
ADRs retain explicit legacy compatibility.
