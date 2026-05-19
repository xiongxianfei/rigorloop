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
| `proposal` | claim boundaries | Baseline skill said proposal hands off to `proposal-review`, does not imply `proposal-review -> spec`, and expected output is a readiness statement for `proposal-review` or blocker state. | Edited skill keeps the handoff behavior and expected output wording, and adds `must_not_claim: proposal-review approval, spec readiness, implementation readiness, verification, branch readiness, or PR readiness.` | pass |
| `proposal` | output skeleton | Baseline skill included a fenced proposal skeleton with status, problem, goals, non-goals, vision fit, context, options, recommendation, behavior changes, architecture impact, testing strategy, rollout, risks, open questions, decision log, next artifacts, follow-on artifacts, and readiness. | Edited skill keeps the same fenced output skeleton and section list unchanged. | pass |
| `proposal-review` | material review status | Baseline skill used closed review statuses `approved`, `changes-requested`, `blocked`, and `inconclusive`; representative `proposal-review-r1.md` returned `changes-requested` for material findings and `proposal-review-r2.md` returned approved with no material findings. | Edited skill keeps the same closed enum and review-status contract. The description and `must_not_claim` addition do not alter status selection. | pass |
| `proposal-review` | finding format | Baseline skill required Finding ID, Severity, Location, Evidence, Required outcome, and Safe resolution path or `needs-decision` rationale. | Edited skill keeps the material-finding section and output skeleton fields unchanged. | pass |
| `proposal-review` | recording obligations | Baseline skill required formal lifecycle review evidence, detailed records for material findings, review log updates, and review-resolution when required. | Edited skill keeps `Isolation and Recording` unchanged and adds only a claim-boundary line to `Workflow role`. | pass |
| `proposal-review` | stop conditions | Baseline skill stopped on material findings, missing recording ability, downstream isolation, and owner-decision blockers. | Edited skill keeps isolation, recording blocker, material-finding, and immediate-next-stage wording unchanged and adds that it must not claim automatic downstream handoff. | pass |

## M3 Token-Cost Evidence

Baseline measured before skill edits:

| Skill | Baseline estimated tokens | After estimated tokens | Delta | Budget result |
| --- | ---: | ---: | ---: | --- |
| `proposal` | 3300 | 3368 | +68 / +2.1% | within +5% rationale tolerance |
| `proposal-review` | 3405 | 3473 | +68 / +2.0% | within +5% rationale tolerance |

Rationale for nonzero delta: the pilot adds description-level near-miss routing and explicit workflow-role claim boundaries required by R29 and R30. The body procedure and output skeletons were left intact to avoid behavior drift.

## M3 Routing Transcript Observation

No runtime routing harness is approved for this slice, and no new live routing transcript is claimed as deterministic selection proof. The edited descriptions now cover the M1 routing table's positive triggers, competing skills, and should-not-trigger classes for both pilot skills. Static validation remains limited to repository-local checks and does not score broad semantic routing quality.

## M1 Result

M1 identifies the parity fixtures and assertions. M1 does not change skill behavior, so before/after parity rows remain pending until M3.
