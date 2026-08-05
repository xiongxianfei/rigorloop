# Specification Authoring Evidence

- Artifact ID: `spec`
- Artifact path: `specs/boundary-first-v1-v0-3-7-activation-release.md`
- Authoring stage: `spec`
- Completion status: complete
- Next review: `spec-review-r3`

## Authoring result

The specification defines the `v0.4.0` activation contract without reopening
the boundary model. It adds one named, side-effect-free candidate mode; retains
strict default and release-context validation; separates publication base `P`,
grandfathering baseline `B`, transition `T`, and reviewed head `H`; requires a
self-contained tagged tree; and defines atomic two-ref publication, drift
handling, and immutable rollback.

Revision R2 resolves spec-review R1 by classifying the public behavior as minor
release `v0.4.0`, distinguishing `P` from `B`, requiring invalid unpublished
transition histories to be superseded by a fresh branch from current `P`, and
assigning the missing self-containment, strict-composition, changed-path, and
replacement hazards to the existing compact boundary model.

Revision R3 resolves the implementation-review identity conflict by separating
the candidate-validation head `R`, its immediate evidence-bearing child `C`,
and the final reviewed publication head `H`. Candidate evidence records the
already-existing producer `R`; publication derives and revalidates live `H`.
This removes the impossible requirement for a commit to contain its own identity
while retaining first-parent provenance, post-transition drift checks, and
atomic publication of `H` with the release tag at `T`.

The formal boundary record covers all eight core dimensions and selects only
seven composed hazards needed to distinguish candidate authority, commit
identity, atomic publication, strict-gate composition, invalid-candidate
replacement, partial failure, and rollback. It does not generate a Cartesian
scenario inventory.

## Validation target

Spec review should challenge normative completeness, compatibility with the
standing release and activation contracts, feasibility of tagged-tree
self-containment, proof of the non-circular `R -> C ... H` evidence chain,
post-transition path restrictions, atomic-ref
failure behavior, and whether every public or failure outcome is testable.
