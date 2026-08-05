# Proposal Authoring Evidence

- Artifact ID: `proposal`
- Artifact path: `docs/proposals/2026-08-05-activate-boundary-first-v1-v0-3-7.md`
- Authoring stage: `proposal`
- Completion status: `complete`
- Next review: `proposal-review-r1`

## Authoring result

The proposal selects a routine stable `v0.3.7` activation release, preserves
`v0.3.6` as the immutable rollback target, reuses the existing profile-driven
release transaction, and keeps automatic workflow continuation outside tag and
publication actions.

The proposal preserves the user's request to proceed while keeping scope to
activation, versioned release preparation, package parity, publication, and
public closeout. It rejects another boundary model or release mechanism.

The R1 revision accepts `BFA-PR1-001`. It adds a narrow candidate-validation
mode for the reviewed pre-tag commit, preserves strict immutable-tag validation
for release context, and requires an unchanged-parent compare-and-swap plus
atomic fast-forward/tag push so the published tag resolves to the exact
reviewed pending-to-active transition. Candidate evidence never claims that an
absent tag is an active release.

The R2 revision accepts `BFA-PR2-001`. It separates the final reviewed branch
head from the earlier pending-to-active transition commit, requires both to
remain on one first-parent chain, tags only the transition commit, fast-forwards
`main` to the final reviewed head, and requires the tagged transition tree to
contain every input needed by strict release verification.

## Evidence used

- Current GitHub Releases, npm registry version, and Git tags.
- The merged progressive boundary-first specification and activation state.
- The current release profile and release-transaction tooling.
- The canonical architecture package and project workflow guidance.

## Validation target

Proposal review R3 should confirm `BFA-PR2-001` is resolved and challenge the
two-identity first-parent model, tagged-tree self-containment,
fast-forward/base-drift handling, atomic publication, rollback coherence, and
the narrowed release-tooling scope.
