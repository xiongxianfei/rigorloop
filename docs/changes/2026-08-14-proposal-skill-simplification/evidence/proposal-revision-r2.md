# Proposal Revision R2 Evidence: Proposal Skill Simplification

Stage: proposal
Date: 2026-08-14
Artifact ID: `proposal`
Artifact: `docs/proposals/2026-08-14-proposal-skill-simplification.md`
Revision basis: `proposal-review-r2`
Completion status: complete

## Findings addressed

| Finding ID | Resolution | Proposal surfaces |
| --- | --- | --- |
| `PRSIM-R2-PR1` | Split portable path-and-file operation resolution from governed entry, identity, authority, and retry resolution. | Portable and governed operations, expected behavior, tests, acceptance criteria, risks, and decision log |
| `PRSIM-R2-PR2` | Added `authoring-reset-required`, proposal no-mutation behavior, workflow-owned reconciliation prerequisites, bounded writes, new-attempt identity, and the architecture escalation condition. | Stale governed authoring attempts, architecture impact, expected behavior, tests, acceptance criteria, risks, and decision log |
| `PRSIM-R2-PR3` | Added vision-exception and standing-artifact groups and made all four specialized groups independently composable in the sole skeleton. | Structural asset, expected behavior, tests, acceptance criteria, risks, and decision log |

## Validation

- The two-reference package and one-asset ownership direction remain unchanged.
- Portable authoring no longer depends on lifecycle entries.
- Stale transaction recovery adds no lifecycle state, persistence record, or proposal-owned reset authority.
- Every specialized predicate has one explicit structural destination.
- The proposal is ready for a new independent proposal review and claims no downstream readiness.
