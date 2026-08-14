# Proposal Revision R1 Evidence: Proposal Skill Simplification

Stage: proposal
Date: 2026-08-14
Artifact ID: `proposal`
Artifact: `docs/proposals/2026-08-14-proposal-skill-simplification.md`
Revision basis: `proposal-review-r1`
Completion status: complete

## Findings addressed

| Finding ID | Resolution | Proposal surfaces |
| --- | --- | --- |
| `PRSIM-PR1` | Added `governed_proposal_candidate_context`, reference-owned `governed_proposal_authority`, invalid-candidate stops, and no portable fallback. | Invocation predicates, assemblies, expected behavior, acceptance criteria, risks, and decision log |
| `PRSIM-PR2` | Added entry-first create and revise transactions, bound identities, commit points, partial-state recovery, conflicts, and idempotent completion. | Operations, expected behavior, testing, acceptance criteria, risks, and decision log |
| `PRSIM-PR3` | Added `initial_intent_table_context`, restored every current scope-budget trigger, and made both structural groups independently applicable. | Invocation predicates, structural asset, expected behavior, testing, acceptance criteria, risks, and decision log |

## Validation

- The revised proposal retains the two-reference package and one structural asset selected by the original direction.
- The review findings have explicit proposal-level decisions and no unresolved owner choice.
- The proposal remains bounded to `proposal` and directly coupled contract, fixture, validator-registration, and package surfaces.
- The proposal is ready for a new independent `proposal-review` and claims no downstream readiness.
