# Proposal Review R1: Plan Skill Simplification

Review ID: proposal-review-r1
Stage: proposal-review
Round: r1
Reviewer: Codex independent proposal-review context
Target: `docs/proposals/2026-08-12-plan-skill-simplification.md`
Reviewed artifact: commit `82bdb96f`
Review date: 2026-08-12
Recording status: recorded
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: PLSIM-PR1, PLSIM-PR2, PLSIM-PR3
- Open blockers: automation ownership, stable milestone completion structure, and deterministic profile accounting require proposal revision
- Proposal readiness: not ready for specification
- Immediate next stage: proposal revision
- Automatic downstream handoff: none
- Claim limitations: this review does not approve the proposal, authorize specification, or continue the workflow

## Overall assessment

The proposal chooses the right broad package design: a compact universal `SKILL.md`, one conditional governed plan-authoring reference, the existing boundary reference, and the existing three structural assets. It correctly protects the exact one-time `planned_work` initialization exception, rejects a runtime engine, separates semantic rules from literal compatibility, and treats loaded-profile reduction rather than main-file reduction as the primary outcome.

The proposal also identifies a real current-contract inconsistency: `assets/milestone.md` carries mutable state while higher-priority lifecycle architecture assigns mutable state to `change.yaml`. Treating that as an atomic contract-and-consumer migration is sound. Three execution contracts still need closure before a specification could implement the design without making new decisions.

## Material findings

### PLSIM-PR1 — Major: the governed reference is assigned automation and handoff responsibilities outside `plan` ownership

Finding ID: PLSIM-PR1
Severity: major
Location: Governed reference ownership; Expected Behavior Changes
Evidence: The proposal assigns the governed reference “workflow-managed authoring-profile evidence and return to `workflow` after `plan-review` handoff preparation.” `plan` authors the plan and may hand it to `plan-review`; it does not execute or complete `plan-review`, own autoprogression receipts, or prepare a post-review return. The existing workflow contract assigns automation state and continuation to `workflow`, while `plan-review` owns its review evidence and settlement. Moving that language into a plan-owned reference risks granting `plan` cross-stage authority during simplification.
Required outcome: Restrict the reference to plan-owned governed authoring procedure and define automation as an execution-authority axis that changes neither loaded resources nor plan-owned writes.
Safe resolution path: State that the same governed reference is used for manual and workflow-managed plan authoring. Under automation, `plan` may consume current same-change authorization and emit only its normal authoring evidence; it then hands the review-required plan to `plan-review`. `workflow` owns automation receipts and continuation, and `plan-review` owns all review evidence and settlement. Remove every suggestion that `plan` returns after, completes, prepares, or records `plan-review` behavior.
needs-decision rationale: none; existing lifecycle ownership determines the correction.

### PLSIM-PR2 — Major: milestone cleanup removes stable completion structure without naming its replacement

Finding ID: PLSIM-PR2
Severity: major
Location: Asset ownership and milestone-state migration
Evidence: The proposal correctly removes mutable `Milestone state` and execution-progress closeout checkboxes, but the target milestone field list does not preserve stable completion criteria, review handoff, or the distinction between implementation and lifecycle-closeout milestones beyond a generic kind. Existing skill-contract parity requires milestone shape, validation evidence, implementation and review handoff, and recording discipline not to weaken. Deleting a mutable progress checklist is safe; deleting stable exit criteria or proof expectations is not.
Required outcome: Define the exact stable milestone structure that replaces the mixed closeout block and explicitly separate plan-time completion criteria from runtime progress.
Safe resolution path: Retain `kind`, `completion criteria`, `required evidence`, and `review handoff` as stable plan fields. Keep actual command outcomes, milestone state, current review status, validation progress, commit completion, blockers, and closeout readiness exclusively in `change.yaml` and stage-owned evidence. Define how a `lifecycle-closeout` milestone differs from an implementation milestone without storing mutable state in the plan.
needs-decision rationale: none; the plan must remain independently executable and reviewable.

### PLSIM-PR3 — Major: loaded-profile measurement is not deterministic because asset applicability is variable

Finding ID: PLSIM-PR3
Severity: major
Location: Invocation classification and resource loading; Simplification measurement
Evidence: The four profiles load “applicable assets,” while the decision-log asset is conditional and the finding asset does not exist. The proposal then requires `PL0-portable` and `PL1-governed` loaded words and bytes to decrease, but it does not define whether measurements include the plan skeleton, one milestone copy, all milestone copies, or the decision-log row. Asset content may be copied into output rather than read as procedure, and variable milestone count makes the baseline non-repeatable. A specification or validator would have to invent the assembly.
Required outcome: Separate procedural loaded-context profiles from structural output-resource measurements and define one deterministic assembly convention.
Safe resolution path: Measure `SKILL.md` plus mapped references only for `PL0`, `PL0B`, `PL1`, and `PL1B`. Report each asset's canonical words and bytes separately, plus the total package. If output-template loading is also measured, define a fixed representative assembly of plan skeleton, one milestone asset, and no decision-log row, with an additional decision-log delta. Do not multiply asset size by milestone count. Require portable and governed procedural profiles to decrease; treat asset changes as separate structural evidence.
needs-decision rationale: none; deterministic measurement is required to prove the proposal's objective.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | Common-path overload, duplicate ownership, and stale milestone-state structure are concrete and measured. |
| User value | pass | Portable and governed planning should become easier to scan without weakening rigor. |
| Option diversity | pass | Unchanged, editorial, asset-only, one-reference, fragmented, and runtime alternatives are materially different. |
| Decision rationale | pass | One governed reference is proportionate. |
| Vision fit | pass | The direction improves human-readable, durable planning evidence. |
| Scope control | pass | Adjacent skill optimization, runtime machinery, and permanent simplicity gates remain excluded. |
| Architecture awareness | pass with revisions | Existing architecture likely suffices, but stage ownership must be kept exact. |
| Testability | block | Profile assembly and stable milestone replacement are not deterministic yet. |
| Risk honesty | concern | Parser migration risk is well covered; cross-stage authority and stable exit-criteria loss need explicit mitigation. |
| Rollout realism | pass with revisions | Atomic parser migration is sound once the exact milestone contract and proof assembly are closed. |
| Readiness for spec | block | PLSIM-PR1 through PLSIM-PR3 require proposal revision. |

## Scope Preservation Review

- Scope-preservation result: pass. Every initial user goal remains visible and in scope. The findings refine the selected plan-skill package and migration; they do not introduce another skill, runtime, asset family, or lifecycle model.

## Recommended Proposal Edits

- Remove plan-owned automation receipt, post-review return, and plan-review preparation language; add a closed execution-authority statement.
- Define a stable milestone completion group containing completion criteria, required evidence, and review handoff while keeping mutable progress out of the plan.
- Define procedural profile measurement independently from structural asset measurement.

## Recommendation

- Recommendation: revise the proposal to resolve PLSIM-PR1 through PLSIM-PR3, then rerun independent `proposal-review` against a frozen revision. No automatic downstream handoff follows this review.

## Durable-recording group

- Recording status: recorded
- Recording blocker: none
- Record path: `docs/changes/2026-08-12-plan-skill-simplification/reviews/proposal-review-r1.md`
- Finding-record paths: `docs/changes/2026-08-12-plan-skill-simplification/reviews/proposal-review-r1.md`

## Formal-settlement group

- Review ID: proposal-review-r1
- Review record: `docs/changes/2026-08-12-plan-skill-simplification/reviews/proposal-review-r1.md`
- Review log: `docs/changes/2026-08-12-plan-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-12-plan-skill-simplification/review-resolution.md`
- Proposal settlement: revision-required
- Governed change identity: `2026-08-12-plan-skill-simplification`
- Formal next-stage eligibility: proposal revision only
