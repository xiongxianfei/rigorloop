# Proposal Review R1: Plan-Review Skill Simplification

Review ID: proposal-review-r1
Stage: proposal-review
Round: r1
Reviewer: Codex independent proposal-review context
Target: `docs/proposals/2026-08-13-plan-review-skill-simplification.md`
Reviewed artifact: commit `6305460b`
Review date: 2026-08-13
Recording status: recorded
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: PRVSIM-PR1, PRVSIM-PR2, PRVSIM-PR3
- Open blockers: governed trigger validation, transaction outcomes, and result-asset recording structure require proposal revision
- Proposal readiness: not ready for specification
- Immediate next stage: proposal revision
- Automatic downstream handoff: none
- Claim limitations: this review does not approve the proposal, authorize specification, or continue the workflow

## Overall assessment

The proposal selects a proportionate package design: a shorter universal `SKILL.md`, one conditional governed procedure reference, the existing boundary-first reference, and the two standard review-family structural assets. It correctly keeps portable formal recording inline, separates initial semantic review from settlement retry, preserves the merged reviewed-plan transaction, and rejects runtime journeys and permanent simplicity gates.

The proposal is also stronger than a file-size-only refactor because it measures portable and governed assemblies separately, treats assets as structural resources, preserves exact lifecycle ownership, and requires semantic and literal disposition evidence. Three contracts still need proposal-level closure before a specification can implement the design without inventing trigger, state, or output behavior.

## Material findings

### PRVSIM-PR1 — Major: the governed reference trigger depends on validation owned by the reference

Finding ID: PRVSIM-PR1
Severity: major
Location: Invocation and operation classification; Loaded-resource profiles; Governed reference ownership
Evidence: The proposal selects `governed-plan-entry` only after resolving one exact current change, lifecycle marker, matching plan entry, legal plan state, authoring evidence or initialization basis, and reviewed revision. It then says the governed reference loads exactly for `governed-plan-entry` and owns complete `change.yaml` inspection, exact entry resolution, legal-state checks, and identity validation. The caller therefore needs the reference to prove the predicate that permits loading the reference. A stale or malformed governed candidate has no closed assembly: treating it as portable could bypass the procedure needed to diagnose it, while treating it as governed assumes authority before validation.
Required outcome: Separate the resource-load trigger from validated settlement authority and define the reclassification sequence for valid, invalid, stale, ambiguous, and absent governed candidates.
Safe resolution path: Introduce `governed_plan_candidate_context` as a load-only predicate established by an explicit change identity, reviewed-plan metadata, or current governed review request. Load the reference on that candidate, then let the reference validate either `governed-plan-entry` or a fail-closed stop. Keep `isolated-recording` for requests with no governed candidate. State that a candidate grants no mutation authority, a failed candidate never falls back to portable settlement, and late discovery loads the reference before dependent judgment, recording-location selection, or status claims.
needs-decision rationale: none; this is a trigger-order defect with a safe ownership-preserving correction.

### PRVSIM-PR2 — Major: review status, transaction result, and handoff are not a closed matrix

Finding ID: PRVSIM-PR2
Severity: major
Location: Invocation and operation classification; Expected Behavior Changes; Governed reference ownership
Evidence: The proposal distinguishes `initial-review` and `settlement-retry`, but it does not define whether `initialization-required` is a review status, lifecycle result, or next action. It also does not close the combinations for approved isolated review, approved governed review with absent state, non-clean governed review, blocked recording, matching settlement retry, invalid retry, or workflow-managed completion. The current skill and merged lifecycle contract require `approved` to remain the semantic review status while the initial governed lifecycle result is `initialization-required`; only the identical retry may produce active settlement and `test-spec` eligibility. Without a matrix, the specification could accidentally report test-spec too early, create another review record during retry, or treat recording failure as a lifecycle result.
Required outcome: Define separate closed values and a complete operation/status/settlement/handoff matrix, including retry recording behavior.
Safe resolution path: Keep review status exactly `approved`, `changes-requested`, `blocked`, or `inconclusive`; add a separate transaction result such as `recorded-isolated`, `initialization-required`, `revision-required`, `blocked`, `settled-active`, or `not-settled`; and define the immediate action for each valid combination. State that settlement retry is legal only for a previously recorded clean review, creates no second semantic review, receipt, finding set, or review-log entry, and mutates only the matching plan entry. An initial approved governed review with absent state must remain `review-required`, report `initialization-required`, and withhold `test-spec` eligibility.
needs-decision rationale: none; the merged lifecycle transaction and current status vocabulary determine the safe matrix.

### PRVSIM-PR3 — Major: the result asset omits mandatory formal-recording path fields

Finding ID: PRVSIM-PR3
Severity: major
Location: Structural assets
Evidence: The proposed core result group contains `recording status` but not `recording blocker`, `review record`, `review log`, or `review resolution`. Every explicit `plan-review` is formal under the proposal, and the formal-review recording contract requires those paths or blocked states in the result. The governed group contains lifecycle identity and settlement fields, but portable formal review still needs durable-recording structure. A specification would have to add fields outside the asset, make them policy-owned by prose, or emit an incomplete result.
Required outcome: Define one recording group applicable to every formal result and close omission versus blocked-data behavior for every asset group.
Safe resolution path: Use five structural groups: core, durable-recording, governed-settlement, boundary-review, and workflow-managed. The durable-recording group always contains recording status, blocker, review record, review log, review resolution, and finding-record paths. Omit only truly inapplicable groups; emit applicable unavailable fields with explicit `blocked` or `unknown` plus the blocker; forbid unfilled placeholders. Keep applicability and field meaning in procedure, not assets.
needs-decision rationale: none; existing formal-review output requirements already require these fields.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | Conditional lifecycle procedure and inline output duplication are concrete and measured. |
| User value | pass | Portable and governed plan review should become easier to scan without weakening rigor. |
| Option diversity | pass | Unchanged, editorial, asset-only, one-reference, fragmented, and runtime options are materially different. |
| Decision rationale | pass | One governed reference plus two assets is proportionate. |
| Vision fit | pass | The direction improves inspectability and preserves durable evidence. |
| Scope control | pass | Adjacent optimization, lifecycle redesign, runtime machinery, and permanent simplicity policy remain excluded. |
| Architecture awareness | pass with revisions | Existing architecture likely suffices; the load-versus-authority boundary needs closure. |
| Testability | block | Static scenarios cannot encode a deterministic trigger and transaction matrix yet. |
| Risk honesty | pass with revisions | Principal risks are named, but circular classification and incomplete result structure need explicit mitigation. |
| Rollout realism | pass | Canonical-first atomic rollout and package parity are appropriate. |
| Readiness for spec | block | PRVSIM-PR1 through PRVSIM-PR3 require proposal revision. |

## Scope Preservation Review

- Scope-preservation result: pass. Every initial user goal remains explicitly classified and in scope. The scope budget covers the skill package, directly coupled validator and contract surfaces, preservation evidence, branch creation, proposal authoring, and formal review without adding another runtime, lifecycle model, or adjacent skill optimization.

## Recommended Proposal Edits

- Add a candidate-context load predicate and validate governed settlement authority only after loading the reference.
- Add a closed matrix separating semantic review status, transaction result, artifact state, recording behavior, immediate action, and workflow handoff.
- Add a durable-recording asset group used by every formal result and retain the four existing conditional structural groups as applicable.

## Recommendation

- Recommendation: revise the proposal to resolve PRVSIM-PR1 through PRVSIM-PR3, then rerun independent `proposal-review` against a frozen revision. No automatic downstream handoff follows this review.

## Specialized-gate group

- Active gate predicates: `scope_budget_context`
- Gate outcomes: pass; the scope budget classifies every core, same-slice, and out-of-scope work item with actionable ownership
- Trigger ambiguity: none

## Durable-recording group

- Recording status: recorded
- Recording blocker: none
- Record path: `docs/changes/2026-08-13-plan-review-skill-simplification/reviews/proposal-review-r1.md`
- Finding-record paths: `docs/changes/2026-08-13-plan-review-skill-simplification/reviews/proposal-review-r1.md`

## Formal-settlement group

- Review ID: proposal-review-r1
- Review record: `docs/changes/2026-08-13-plan-review-skill-simplification/reviews/proposal-review-r1.md`
- Review log: `docs/changes/2026-08-13-plan-review-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-13-plan-review-skill-simplification/review-resolution.md`
- Proposal settlement: revision-required
- Governed change identity: `2026-08-13-plan-review-skill-simplification`
- Formal next-stage eligibility: proposal revision only
