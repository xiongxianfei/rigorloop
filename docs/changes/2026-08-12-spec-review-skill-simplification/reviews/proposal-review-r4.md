# Proposal Review R4: Spec-Review Skill Simplification

Review ID: proposal-review-r4
Stage: proposal-review
Round: r4
Reviewer: Codex independent proposal-review context
Target: `docs/proposals/2026-08-12-spec-review-skill-simplification.md`
Reviewed artifact: commit `1486d726`
Review date: 2026-08-12
Recording status: recorded
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: SRSIM-R4-PR1
- Open blockers: boundary output applicability for the non-formal boundary profile is not closed
- Proposal readiness: not ready for specification
- Immediate next stage: proposal revision
- Automatic downstream handoff: none
- Claim limitations: no specification, implementation, verification, branch, or PR readiness is claimed

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | The loaded-context and duplicate-ownership problem is concrete and measured. |
| User value | pass | The proposal targets the actual isolated formal-review context cost. |
| Option diversity | pass | The alternatives remain materially distinct. |
| Decision rationale | pass | One recording reference and the existing boundary resources remain proportionate. |
| Vision fit | pass | The direction improves inspectability without weakening durable evidence. |
| Scope control | pass | Initial intent and same-slice dependencies remain explicit. |
| Architecture awareness | pass | The bounded assessment and expected `architecture-not-required` outcome remain appropriate. |
| Testability | concern | `SR0B` has no unambiguous output assembly. |
| Risk honesty | pass | Context, package, compatibility, and authority risks are explicit. |
| Rollout realism | pass | Atomic rollout, parity, and rollback remain adequate. |
| Readiness for spec | block | SRSIM-R4-PR1 requires proposal revision. |

## Scope Preservation Review

- Scope-preservation result: pass; all initial goals remain visible and no hidden follow-up or silent narrowing was found.

## Specialized-gate group

- Active gate predicates: `scope_budget_context`
- Gate outcomes: pass; work items retain closed treatments and bounded ownership.
- Trigger ambiguity: none

## Durable-recording group

- Recording status: recorded
- Recording blocker: none
- Record path: `docs/changes/2026-08-12-spec-review-skill-simplification/reviews/proposal-review-r4.md`
- Finding-record paths: `docs/changes/2026-08-12-spec-review-skill-simplification/reviews/proposal-review-r4.md`

## Formal-settlement group

- Review ID: proposal-review-r4
- Review record: `docs/changes/2026-08-12-spec-review-skill-simplification/reviews/proposal-review-r4.md`
- Review log: `docs/changes/2026-08-12-spec-review-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-12-spec-review-skill-simplification/review-resolution.md`
- Proposal settlement: `revision-required`
- Governed change identity: `2026-08-12-spec-review-skill-simplification`
- Formal next-stage eligibility: proposal revision only

## Material finding

### SRSIM-R4-PR1 — Major: the feedback-boundary profile has contradictory output applicability

Finding ID: SRSIM-R4-PR1
Severity: major
Location: Closed loaded-resource profiles; Asset ownership; Decision Log
Evidence: `SR0B-feedback-boundary` is a valid non-formal profile that loads boundary resources. The asset section calls all four conditional groups formal, says the boundary-review group applies whenever checked boundary activation applies, and then says `SR0` omits every formal-only field while only `SR1` adds boundary-review. The older decision-log row also still describes four conditional groups around one universal core. The proposal therefore does not determine whether `SR0B` emits the boundary group, omits boundary output, or maps boundary evidence into feedback observations.
Required outcome: Define one exact output assembly for `SR0B-feedback-boundary` and reconcile the boundary group and decision log with the two-core model.
Safe resolution path: Keep the boundary-review group formal-only. State that `SR0B` uses boundary resources to inform the feedback core's observations and limitations without emitting activation, formal boundary outcome, readiness, or settlement fields. Make the boundary-review group apply only to `formal-lifecycle` with checked activation, add positive and forbidden-field fixtures for `SR0B`, and mark the older universal-core decision as superseded or replace it with the current two-core decision.
needs-decision rationale: none

## Recommended Proposal Edits

- Define `SR0B` output as the non-formal feedback core populated by boundary-informed observations and limitations.
- Restrict the boundary-review group to formal lifecycle review with checked boundary activation.
- Add an invalid `SR0B` fixture containing formal boundary outcome or lifecycle fields.
- Reconcile the stale universal-core decision-log row.

## Recommendation

- Recommendation: changes-requested; resolve SRSIM-R4-PR1 and rerun proposal review against a frozen revision.
