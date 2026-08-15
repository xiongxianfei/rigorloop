# Proposal Revision R1 Evidence: Spec Skill Simplification

Stage: proposal
Date: 2026-08-15
Artifact ID: `proposal`
Artifact: `docs/proposals/2026-08-15-spec-skill-simplification.md`
Revision basis: `proposal-review-r1`
Completion status: complete

## Findings addressed

| Finding ID | Resolution | Proposal surfaces |
| --- | --- | --- |
| `SPSIM-PR1` | Replaced the unsupported workflow reset-authorization handshake with a spec-owned `restart-stale-authoring` operation over the same incomplete entry, including exact prerequisites, identities, bounded writes, partial-content treatment, final state, stops, and architecture fallback. | Goals, recovery state matrix, ownership, validation, acceptance criteria, architecture, expected behavior, tests, risks, open questions, and decision log |
| `SPSIM-PR2` | Added one conditional insertion point after error behavior and before compatibility, kept the formal block in the feature-authoring reference, and closed emission, preservation, omission, and unresolved-data behavior independently from resource loading. | Goals, structural composition matrix, ownership, validation, acceptance criteria, expected behavior, tests, risks, and decision log |

## Validation

- The revised proposal retains the selected one-governed-reference package and both mandatory boundary-first resources.
- The review findings have explicit proposal-level decisions and no unresolved owner choice.
- The revision adds no lifecycle state, persistent authorization, workflow write owner, target-agent acceptance system, or new structural asset.
- The proposal remains bounded to `spec` and directly coupled contract, fixture, validator, skeleton, and package surfaces.
- The proposal is ready for a new independent `proposal-review` and claims no downstream readiness.
