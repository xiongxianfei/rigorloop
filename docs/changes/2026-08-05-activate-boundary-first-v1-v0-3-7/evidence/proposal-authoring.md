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

## Evidence used

- Current GitHub Releases, npm registry version, and Git tags.
- The merged progressive boundary-first specification and activation state.
- The current release profile and release-transaction tooling.
- The canonical architecture package and project workflow guidance.

## Validation target

Proposal review should challenge release identity, activation/rollback
coherence, external-action containment, scope, and whether existing
architecture is sufficient.
