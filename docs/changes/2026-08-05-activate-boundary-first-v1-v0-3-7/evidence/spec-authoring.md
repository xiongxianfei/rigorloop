# Specification Authoring Evidence

- Artifact ID: `spec`
- Artifact path: `specs/boundary-first-v1-v0-3-7-activation-release.md`
- Authoring stage: `spec`
- Completion status: complete
- Next review: `spec-review-r1`

## Authoring result

The specification defines the `v0.3.7` activation contract without reopening
the boundary model. It adds one named, side-effect-free candidate mode; retains
strict default and release-context validation; separates reviewed base,
transition, and final-head identities; requires a self-contained tagged tree;
and defines atomic two-ref publication, drift handling, and immutable rollback.

The formal boundary record covers all eight core dimensions and selects only
six composed hazards needed to distinguish candidate authority, commit
identity, atomic publication, strict-gate composition, partial failure, and
rollback. It does not generate a Cartesian scenario inventory.

## Validation target

Spec review should challenge normative completeness, compatibility with the
standing release and activation contracts, feasibility of tagged-tree
self-containment, proof of post-transition path restrictions, atomic-ref
failure behavior, and whether every public or failure outcome is testable.
