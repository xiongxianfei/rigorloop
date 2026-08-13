# Proposal Review R3: Plan Skill Simplification

Review ID: proposal-review-r3
Stage: proposal-review
Round: r3
Reviewer: Codex independent proposal-review context
Target: `docs/proposals/2026-08-12-plan-skill-simplification.md`
Reviewed artifact: commit `31386949`
Review date: 2026-08-13
Recording status: recorded
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: PLSIM-PR7, PLSIM-PR8, PLSIM-PR9
- Open blockers: settlement sequencing, plan identity, and architecture disposition require proposal revision
- Proposal readiness: not ready for specification
- Immediate next stage: proposal revision
- Automatic downstream handoff: none
- Claim limitations: this review does not approve the proposal, authorize specification, or continue the workflow

## Overall assessment

The proposal now closes the three second-round issues at the conceptual level. Governed authority is separate from create/revise operation, `planned_work` is derived only from a clean review-settled baseline, and milestone format migration is explicitly read-old/write-new. The package shape, structural assets, resource profiles, ownership boundaries, and proof model remain proportionate.

The remaining gaps arise from composing the new initialization timing with the current state contract. The current validator requires `planned_work` whenever a primary plan is registered, the formal review contract settles after writing review evidence, and the governing ADR explicitly assigns initialization at new-plan registration while rejecting governed-document hashes. The proposal selects a different order but does not yet define the legal intermediate states, the settlement retry protocol, or an identity representation compatible with that architecture.

## Material findings

### PLSIM-PR7 — Major: post-review initialization has no legal intermediate-state and settlement sequence

Finding ID: PLSIM-PR7
Severity: major
Location: Governed reference ownership; Plan baseline settlement and replan; Rollout and Rollback
Evidence: The proposal says plan authoring registers a primary plan without `planned_work`, plan-review “settles the exact plan identity,” and only afterward workflow coordinates the plan-owned initializer. Current `change_metadata_semantics.py` requires primary-plan registration and `planned_work` presence to match exactly. Current review procedure writes review evidence and then settles the artifact entry. The proposal does not define when a registered review-required plan without `planned_work` is valid, whether clean review evidence may exist without settlement, when initialization runs, or how settlement resumes if initialization succeeds or fails.
Required outcome: Define one closed evidence-first initialization and settlement protocol plus the exact temporary schema invariants it requires.
Safe resolution path: Allow a primary plan without `planned_work` only while its entry is `authoring` or `review-required`. Plan-review writes a clean durable review record for the exact plan revision but leaves settlement incomplete. Workflow-managed execution may coordinate the plan-owned initializer; isolated review reports `initialization-required` without auto-continuation. The initializer validates the clean record, writes missing `planned_work`, and returns. Plan-review then retries the identical settlement without rerunning judgment and moves only the plan entry to `active`. Allow the temporary combination of `review-required` plus initialized `planned_work` only when the matching clean review record is present and settlement retry is pending. Initialization failure leaves the plan `review-required`, records the blocker, and cannot route to implementation.
needs-decision rationale: none; the selected post-review model needs a deterministic transaction boundary.

### PLSIM-PR8 — Major: plan “content identity” is undefined and conflicts with the governing no-hash architecture

Finding ID: PLSIM-PR8
Severity: major
Location: Invocation classification and resource loading; Governed reference ownership; Plan baseline settlement and replan
Evidence: Creation “computes its content identity,” revision requires a “current matching artifact identity,” and initialization binds an “approved plan identity,” but the proposal defines neither representation nor durable location. `artifact_states` currently identifies an artifact through stable ID, kind, role, and normalized path; review evidence identifies the reviewed revision through its record and commit. ADR-20260729 explicitly rejects governed-document hashes. A specification cannot tell whether the proposal requires a new hash, schema field, Git identity, or only the existing artifact and review evidence.
Required outcome: Select an identity model compatible with the existing stage-owned contract or explicitly amend the no-hash decision.
Safe resolution path: Avoid a new content hash. Use stable artifact identity as the tuple of artifact ID, kind, role, and normalized path. Use the approving review mapping and its durable review record's exact reviewed commit or revision as the baseline revision identity. Creation finalizes the stable plan entry after writing the intended path; plan-review supplies revision identity. The initializer verifies that the current plan matches the reviewed revision using existing review evidence and repository state, without adding a `content_identity` field. If a hash is instead required, make that an explicit architecture decision and schema change rather than an implementation detail.
needs-decision rationale: none; identity is a public lifecycle and compatibility boundary.

### PLSIM-PR9 — Major: `architecture-not-required` contradicts the selected lifecycle-order change

Finding ID: PLSIM-PR9
Severity: major
Location: Architecture Impact
Evidence: The proposal expects `architecture-not-required`, but it changes the validity invariant for registered primary plans, splits clean plan-review evidence from settlement, introduces a plan-owned initialization callback between review evidence and settlement, and moves initialization away from new-plan registration. `docs/architecture/system/architecture.md` states in several normative sections that plan initializes missing planned work for a new primary plan. ADR-20260729 makes the same ordering part of its decision and rejects hashes. This is not only package content or documentation inventory drift.
Required outcome: Change the architecture expectation to an architecture update and determine whether the existing ADR is amended or superseded.
Safe resolution path: Require updates to the canonical architecture sections and state-transition views covering plan registration, review evidence, initialization, settlement, routing, and retry. Amend ADR-20260729 or create a narrowly scoped successor ADR because the decision's initialization ordering and valid state combinations change. Keep `change.yaml` as the architecture-assessment status owner, but do not preselect `architecture-not-required`.
needs-decision rationale: none; the governing architecture explicitly owns the behavior being changed.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | Common-path overload and obsolete state duplication are concrete. |
| User value | pass | Both portable and governed plans should become easier to use. |
| Option diversity | pass | The alternatives remain materially distinct. |
| Decision rationale | pass | One governed reference and three assets remain appropriate. |
| Vision fit | pass | The change strengthens durable, reviewable planning. |
| Scope control | pass | Direct contract, schema, parser, and architecture updates are now necessarily in scope. |
| Architecture awareness | block | The stated assessment expectation contradicts the selected lifecycle transition change. |
| Testability | block | Intermediate state, settlement retry, and identity are not closed. |
| Risk honesty | concern | Read-old/write-new risk is covered; transaction and identity risks are not yet explicit. |
| Rollout realism | concern | Atomic rollout is plausible after legal state combinations and recovery are defined. |
| Readiness for spec | block | PLSIM-PR7 through PLSIM-PR9 require proposal revision. |

## Scope Preservation Review

- Scope-preservation result: pass. Every initial user goal remains in scope. The findings require direct architecture and lifecycle-contract work already implied by the selected post-review initialization decision; they do not introduce an unrelated product or runtime.

## Recommended Proposal Edits

- Add a closed review-evidence, initialization, and settlement-retry sequence with legal temporary state combinations and failure behavior.
- Define stable artifact identity and reviewed revision identity using existing entry and review evidence, or explicitly select a hash/schema architecture change.
- Replace the expected `architecture-not-required` result with required architecture and ADR amendment work.

## Recommendation

- Recommendation: revise the proposal to resolve PLSIM-PR7 through PLSIM-PR9, then rerun independent `proposal-review` against a frozen revision. No automatic downstream handoff follows this review.

## Specialized-gate group

- Active gate predicates: scope_budget_context
- Gate outcomes: scope budget remains complete, but architecture and lifecycle amendments must remain same-slice dependencies
- Trigger ambiguity: none

## Durable-recording group

- Recording status: recorded
- Recording blocker: none
- Record path: `docs/changes/2026-08-12-plan-skill-simplification/reviews/proposal-review-r3.md`
- Finding-record paths: `docs/changes/2026-08-12-plan-skill-simplification/reviews/proposal-review-r3.md`

## Formal-settlement group

- Review ID: proposal-review-r3
- Review record: `docs/changes/2026-08-12-plan-skill-simplification/reviews/proposal-review-r3.md`
- Review log: `docs/changes/2026-08-12-plan-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-12-plan-skill-simplification/review-resolution.md`
- Proposal settlement: revision-required
- Governed change identity: `2026-08-12-plan-skill-simplification`
- Formal next-stage eligibility: proposal revision only
