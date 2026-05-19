# Published Skill Design Pilot Behavior Parity Evidence Plan

## Scope

Changed pilot skills:

- `proposal`
- `proposal-review`

M1 defines representative artifacts and parity assertions. M3 must fill actual before/after evidence after pilot skill edits.

## Representative Artifacts

| Fixture | Source | Purpose |
| --- | --- | --- |
| Proposal artifact | `docs/proposals/2026-05-19-rigorloop-published-skill-design-contract.md` | Representative proposal with accepted status, goals, non-goals, scope, rollout, acceptance criteria, decisions, and readiness. |
| Proposal review with material findings | `docs/changes/2026-05-19-rigorloop-published-skill-design-contract/reviews/proposal-review-r1.md` | Representative proposal-review result with material findings and detailed recording obligations. |
| Clean proposal review | `docs/changes/2026-05-19-rigorloop-published-skill-design-contract/reviews/proposal-review-r2.md` | Representative clean review receipt with no material findings. |
| Review resolution | `docs/changes/2026-05-19-rigorloop-published-skill-design-contract/review-resolution.md` | Evidence of material finding disposition and closeout semantics. |
| Review log | `docs/changes/2026-05-19-rigorloop-published-skill-design-contract/review-log.md` | Evidence of review recording and open-finding state. |

## Parity Assertions

M3 must show that the pilot edits do not weaken:

| Area | Required parity evidence |
| --- | --- |
| Material review status | Proposal-review still returns `changes-requested`, `blocked`, `inconclusive`, or `approved` according to material findings and readiness. |
| Finding format | Material findings still include stable ID, severity, location, evidence, required outcome, and safe resolution or needs-decision rationale. |
| Recording obligations | Formal review recording still creates or reports review record, review log, and review resolution status. |
| Stop conditions | Proposal and proposal-review still stop on missing direction, unresolved material findings, missing durable recording, or owner-decision blockers. |
| Validation obligations | Review artifacts and change metadata remain validated with repository-owned scripts. |
| Claim boundaries | Proposal does not claim spec readiness without review; proposal-review does not write the spec, review implementation, claim verify, branch-ready, or PR-ready. |
| Resource loading | Pilot skills do not open optional packaged resources unless a mapped condition applies. |
| Token cost | Static token delta for `proposal` and `proposal-review` follows the zero target, `+5%` rationale tolerance, and `+10%` hard cap. |

## Evidence Rows To Fill In M3

| Skill | Parity area | Before evidence | After evidence | Result |
| --- | --- | --- | --- | --- |
| `proposal` | claim boundaries | Pending M3 | Pending M3 | Pending M3 |
| `proposal` | output skeleton | Pending M3 | Pending M3 | Pending M3 |
| `proposal-review` | material review status | Pending M3 | Pending M3 | Pending M3 |
| `proposal-review` | finding format | Pending M3 | Pending M3 | Pending M3 |
| `proposal-review` | recording obligations | Pending M3 | Pending M3 | Pending M3 |
| `proposal-review` | stop conditions | Pending M3 | Pending M3 | Pending M3 |

## M1 Result

M1 identifies the parity fixtures and assertions. M1 does not change skill behavior, so before/after parity rows remain pending until M3.
