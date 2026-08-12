# Proposal Review R5: Spec-Review Skill Simplification

Review ID: proposal-review-r5
Stage: proposal-review
Round: r5
Reviewer: Codex independent proposal-review context
Target: `docs/proposals/2026-08-12-spec-review-skill-simplification.md`
Reviewed artifact: commit `505d05b5`
Review date: 2026-08-12
Recording status: recorded
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: SRSIM-R5-PR1
- Open blockers: the always-loaded recording reference cannot provide the claimed progressive-disclosure benefit
- Proposal readiness: not ready for specification
- Immediate next stage: proposal revision
- Automatic downstream handoff: none
- Claim limitations: no specification, implementation, verification, branch, or PR readiness is claimed

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | Loaded-context cost and duplicated ownership are concrete and measured. |
| User value | pass | The proposal correctly targets the actual isolated formal-review profile. |
| Option diversity | pass | The alternatives include no change, compression, boundary-only extraction, reference splits, and a runtime engine. |
| Decision rationale | concern | Option 3 still assumes recording is conditional after the proposal makes it universal. |
| Vision fit | pass | The direction preserves inspectable and durable evidence. |
| Scope control | pass | Initial intent and directly coupled work remain visible and bounded. |
| Architecture awareness | pass | A bounded assessment with expected `architecture-not-required` remains proportionate. |
| Testability | pass | The proposal now defines deterministic profiles, writes, outputs, and measurements. |
| Risk honesty | block | The selected package cannot satisfy its primary context-reduction mechanism as written. |
| Rollout realism | pass | Atomic resource rollout, parity, and rollback remain adequate. |
| Readiness for spec | block | SRSIM-R5-PR1 requires a package-ownership revision. |

## Scope Preservation Review

- Scope-preservation result: pass; every initial goal remains classified and no hidden follow-up or silent narrowing was found.

## Specialized-gate group

- Active gate predicates: `scope_budget_context`
- Gate outcomes: pass; work items have closed treatments and remain within the selected skill/package scope.
- Trigger ambiguity: none

## Durable-recording group

- Recording status: recorded
- Recording blocker: none
- Record path: `docs/changes/2026-08-12-spec-review-skill-simplification/reviews/proposal-review-r5.md`
- Finding-record paths: `docs/changes/2026-08-12-spec-review-skill-simplification/reviews/proposal-review-r5.md`

## Formal-settlement group

- Review ID: proposal-review-r5
- Review record: `docs/changes/2026-08-12-spec-review-skill-simplification/reviews/proposal-review-r5.md`
- Review log: `docs/changes/2026-08-12-spec-review-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-12-spec-review-skill-simplification/review-resolution.md`
- Proposal settlement: `revision-required`
- Governed change identity: `2026-08-12-spec-review-skill-simplification`
- Formal next-stage eligibility: proposal revision only

## Material finding

### SRSIM-R5-PR1 — Major: the selected reference is universal after removal of non-formal profiles

Finding ID: SRSIM-R5-PR1
Severity: major
Location: Option 3; Closed loaded-resource profiles; Recording-and-settlement reference ownership; Preservation and measurement
Evidence: The proposal now defines every `spec-review` invocation as formal and requires every profile to load `spec-review-recording-and-settlement.md`. That reference contains isolated recording, governed settlement, and governed automation procedure. Moving universal recording mechanics from `SKILL.md` into an always-loaded reference changes navigation and ownership but does not progressively disclose them, while isolated reviews also load governed settlement and automation text that they cannot use. The proposal simultaneously requires `SR1-isolated-formal` words and bytes to decrease, but its selected package split does not identify which content is actually removed from that loaded assembly rather than relocated.
Required outcome: Align the resource boundary with a genuinely conditional authority boundary and explain how the isolated formal profile becomes smaller.
Safe resolution path: Keep concise universal recording procedure inline in `SKILL.md`, rename the new reference to a governed settlement-and-automation procedure, and load it only for `settlement_mode: governed-spec-entry`. Keep detailed formal-review placement and artifact rules governed by `specs/formal-review-recording.md` through compact inline references rather than duplicating them. Use resource profiles for isolated formal, governed formal, and their boundary variants; require isolated formal reduction from deduplication and removal of governed-only procedure. If the proposal instead keeps the always-loaded reference, reframe the change as ownership/readability improvement and drop the loaded-context reduction claim, but that would no longer satisfy the current primary goal.
needs-decision rationale: none

## Recommended Proposal Edits

- Change the new resource from recording-and-settlement to governed settlement-and-automation.
- Keep only concise universal recording obligations and portable execution steps inline.
- Load the governed reference only for same-change governed settlement; automation remains a branch within that reference.
- Define isolated, governed, isolated-boundary, and governed-boundary resource assemblies.
- Recalculate primary-profile reduction from content actually absent from isolated formal review.

## Recommendation

- Recommendation: changes-requested; revise the resource boundary and rerun proposal review against a frozen revision.
