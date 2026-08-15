# Proposal Revision R3 Evidence: Proposal Skill Simplification

Stage: proposal
Date: 2026-08-14
Artifact ID: `proposal`
Artifact: `docs/proposals/2026-08-14-proposal-skill-simplification.md`
Revision basis: `proposal-review-r3`
Completion status: complete

## Finding addressed

| Finding ID | Resolution | Proposal surfaces |
| --- | --- | --- |
| `PRSIM-R3-PR1` | Split stale-attempt recovery into workflow-owned validation, no-reliance proof, authorization, and routing plus proposal-owned reset execution for the exact authorized incomplete state. | Stale governed authoring attempts, resource ownership, expected behavior, architecture impact, tests, acceptance criteria, risks, scope budget, and decision log |

## Validation

- Workflow does not mutate proposal-owned lifecycle state or proposal-authored evidence.
- Proposal cannot reset a stale attempt without current identity-bound workflow authorization.
- Reset scope excludes review history, other artifacts, workflow state, automation state, and downstream artifacts.
- Identical completed reset consumption is idempotent; stale, mismatched, relied-upon, ambiguous, or competing state stops.
- A new authoring operation begins only after validated reset completion and receives a new transaction identity and evidence path.
- The proposal retains `architecture-not-required` because it preserves existing stage-owned mutation and workflow-routing boundaries.
- The proposal is ready for a fresh independent proposal review and claims no downstream readiness.
