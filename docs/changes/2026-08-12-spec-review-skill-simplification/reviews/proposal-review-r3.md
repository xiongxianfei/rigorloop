# Proposal Review R3: Spec-Review Skill Simplification

Review ID: proposal-review-r3
Stage: proposal-review
Round: r3
Reviewer: Codex independent proposal-review context
Target: `docs/proposals/2026-08-12-spec-review-skill-simplification.md`
Reviewed artifact: commit `a4188594`
Review date: 2026-08-12
Recording status: recorded
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: SRSIM-R3-PR1
- Open blockers: the non-formal result shape contradicts the non-formal status prohibition
- Proposal readiness: not ready for specification
- Immediate next stage: proposal revision
- Automatic downstream handoff: none
- Claim limitations: no specification, implementation, verification, branch, or PR readiness is claimed

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | The loaded-context and duplicate-ownership problem is concrete and measured. |
| User value | pass | The proposal now measures the real direct formal-review profile. |
| Option diversity | pass | Package, compression, fragmentation, and runtime alternatives are materially distinct. |
| Decision rationale | pass | One new recording reference remains proportionate. |
| Vision fit | pass | The direction preserves durable, inspectable evidence while reducing review cost. |
| Scope control | pass | Initial goals and same-slice dependencies remain explicit. |
| Architecture awareness | pass | A bounded assessment with expected `architecture-not-required` is proportionate. |
| Testability | concern | One result-shape contradiction prevents a closed non-formal fixture. |
| Risk honesty | pass | Primary profile reduction, package growth, authority, and compatibility risks are now explicit. |
| Rollout realism | pass | Atomic rollout, parity, and rollback remain adequate. |
| Readiness for spec | block | SRSIM-R3-PR1 must be resolved. |

## Scope Preservation Review

- Scope-preservation result: pass; all initial goals remain visible and no hidden follow-up or silent narrowing was found.

## Specialized-gate group

- Active gate predicates: `scope_budget_context`
- Gate outcomes: pass; work items have closed treatments and directly coupled work remains bounded.
- Trigger ambiguity: none

## Durable-recording group

- Recording status: recorded
- Recording blocker: none
- Record path: `docs/changes/2026-08-12-spec-review-skill-simplification/reviews/proposal-review-r3.md`
- Finding-record paths: `docs/changes/2026-08-12-spec-review-skill-simplification/reviews/proposal-review-r3.md`

## Formal-settlement group

- Review ID: proposal-review-r3
- Review record: `docs/changes/2026-08-12-spec-review-skill-simplification/reviews/proposal-review-r3.md`
- Review log: `docs/changes/2026-08-12-spec-review-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-12-spec-review-skill-simplification/review-resolution.md`
- Proposal settlement: `revision-required`
- Governed change identity: `2026-08-12-spec-review-skill-simplification`
- Formal next-stage eligibility: proposal revision only

## Material finding

### SRSIM-R3-PR1 — Major: the universal result group requires a status forbidden by the non-formal profile

Finding ID: SRSIM-R3-PR1
Severity: major
Location: Review classification and recording; Asset ownership
Evidence: `non-formal-feedback` is forbidden from emitting lifecycle review status, approval, or readiness claims, while the result asset's core group applies to every result and requires `review status`, `eventual test-spec readiness`, and formal next-stage fields. The proposal supplies no non-formal values or alternate structural applicability, so `SR0-feedback` cannot fill the sole result asset without violating either classification or asset rules.
Required outcome: Close the non-formal result contract so feedback never emits formal lifecycle fields and every selected asset group remains fillable without invented values.
Safe resolution path: Make the existing result asset's formal core apply only to `formal-lifecycle`; define a compact non-formal feedback group with feedback scope, observations, limitations, and optional suggested next action, or explicitly route non-formal feedback outside the formal result asset if the governing asset contract permits it. Keep status, readiness, settlement, and recording fields exclusive to formal groups, preserve one asset, and add static fixtures for both profiles.
needs-decision rationale: none

## Recommended Proposal Edits

- Replace “Core result — every result” with closed non-formal and formal core applicability.
- Keep one existing result asset, omit all formal-only groups for `SR0`, and forbid placeholder or `not-applicable` lifecycle values.
- Add a static fixture proving non-formal feedback has no review status, readiness, settlement, or recording fields.

## Recommendation

- Recommendation: changes-requested; resolve SRSIM-R3-PR1 and rerun proposal review against a frozen revision.
