# Proposal Revision R2 Evidence: Spec Skill Simplification

Stage: proposal
Date: 2026-08-15
Artifact ID: `proposal`
Artifact: `docs/proposals/2026-08-15-spec-skill-simplification.md`
Revision basis: `proposal-review-r2`
Completion status: complete

## Findings addressed

| Finding ID | Resolution | Proposal surfaces |
| --- | --- | --- |
| `SPSIM-R2-PR1` | Added tri-state governed-signal classification, counted every structured ownership field as a signal, required all present identities to agree, and prohibited invalid-signal or failed-authority fallback to portable authoring. | Invocation profiles, ownership, resource failure, validation, acceptance criteria, expected behavior, tests, risks, and decision log |
| `SPSIM-R2-PR2` | Separated diagnostic stale detection from explicitly authorized restart, required authority and attempt identities in authoring evidence, made partial-content handling deterministic, preserved every matching nonempty file byte-for-byte, and closed the restart write set and final state. | Same-entry restart, ownership, validation, acceptance criteria, architecture, expected behavior, tests, risks, open questions, and decision log |
| `SPSIM-R2-PR3` | Added closed boundary-block and anchor states, an exhaustive transition matrix, implicit-removal prohibition, explicit deactivation authority, stable-ID handling, and grandfathered insertion or full-rewrite rules. | Structural composition, validation, acceptance criteria, expected behavior, tests, risks, and decision log |

## Validation

- The selected one-governed-reference package and both mandatory boundary-first resources remain unchanged.
- Every round-2 finding has an explicit proposal-level decision and deterministic failure behavior.
- Restart continues using the existing `authoring` entry and authoring-evidence model without a new schema, lifecycle state, persistent authorization subsystem, or write owner.
- The proposal remains bounded to `spec` and directly coupled contract, fixture, validator, skeleton, and package surfaces.
- The proposal is ready for a new independent `proposal-review` and claims no downstream readiness.
