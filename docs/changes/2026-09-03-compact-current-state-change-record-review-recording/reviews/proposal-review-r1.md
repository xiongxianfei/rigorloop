# Proposal Review: Adopt a Compact Current-State Change Record

Review ID: proposal-review-r1
Stage: proposal-review
Round: 1
Reviewer: Codex independent proposal-review context
Target: `docs/proposals/2026-09-03-compact-current-state-change-record.md`

Reviewed artifact: `docs/proposals/2026-09-03-compact-current-state-change-record.md` at `sha256:3fe0849041c2256633a6d2f1661da936f0517aed1862b15b82e2c1a42bb126f8`
Reviewed artifact path: docs/proposals/2026-09-03-compact-current-state-change-record.md
Reviewed artifact identity: sha256:3fe0849041c2256633a6d2f1661da936f0517aed1862b15b82e2c1a42bb126f8
Review date: 2026-09-03
Recording mode: advisory-durable
Automation mode: manual
Assembly: PRR1G-recorded-context-gated
Recording status: recorded
Status: changes-requested
Material findings: CCSR-PR1

## Result

- Skill: proposal-review
- Review status: changes-requested
- Vision alignment: aligned
- Material findings: CCSR-PR1
- Open blockers: the promised Git-history retention boundary is incompatible with supported squash or rewritten merge history
- Proposal readiness: not ready for Design authority until CCSR-PR1 is resolved and the revised proposal receives same-stage rereview
- Immediate next stage: isolated stop; proposal revision followed by proposal-review-r2
- Automatic downstream handoff: none
- Claim limitations: this advisory review records judgment only; it does not settle the portable proposal, activate a governed change, authorize Design, or establish implementation, verification, branch, or PR readiness

## Overall Assessment

The proposal identifies a material resumability and context-cost problem, preserves independent review and current evidence, and presents a concrete direction without prematurely defining schemas, commands, concurrency controls, or proof allocation. Its target working set, retention classes, prospective adoption boundary, and explicit cross-contract cutover make the scope understandable despite its breadth. The direction aligns with RigorLoop's commitment to durable, reviewable, resumable work because current findings, constraining decisions, evidence, and final readiness remain tracked.

One retention claim prevents approval. The proposal repeatedly says Git history preserves superseded review rounds and procedural chronology, but the governing workflow permits squash, rebase, or other history rewriting that can collapse intermediate commit boundaries after merge. The proposal may intentionally decline to guarantee superseded non-material procedure after merge, require preservation-compatible history, or name another durable source. That choice changes the approved audit and retention boundary and therefore belongs in the proposal rather than being left implicit for Design.

## Finding CCSR-PR1

Finding ID: CCSR-PR1

Severity: major

Location: `Goals` line 18; `Proposed direction` lines 92, 96, and 104; `Impact and major trade-offs` line 120; `Decision requested` line 140

Evidence: the proposal states that Git history preserves prior review rounds and procedural chronology. `specs/rigorloop-workflow.md` states that repositories which squash, rebase, or otherwise rewrite commit history may collapse milestone commit boundaries after merge and guarantees visibility during branch and pull-request review, not preservation under every default-branch merge strategy. `docs/architecture/2026-04-19-rigorloop-first-release-repository-architecture.md` records the same constraint. Stable-path updates are therefore not guaranteed to retain superseded rounds in repository history after merge.

Required outcome: make the proposal's retention guarantee compatible with supported merge behavior by deciding whether superseded procedural chronology is required after merge, best-effort only, or durably retained through another named surface.

Safe resolution path: preferably state that the authoritative current state, open findings, material decisions, and current evidence are the guaranteed durable resume set, while superseded non-material rounds and transport chronology are best-effort Git or PR history and may be lost under history rewriting. Alternatively, require preservation-compatible commit and merge policy or retain required chronology in another bounded durable surface, then update Goals, Proposed direction, trade-offs, feasibility, and the requested decision consistently.

needs-decision rationale: the proposal owner must choose the post-merge retention guarantee because weakening it, constraining merge policy, or adding another durable surface are materially different directions.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Challenge | pass | The proposal frames overlapping current and historical records as a resumability and context-cost problem before selecting a solution. |
| Goals | concern | The outcomes answer the challenge, but the Git-history goal currently promises retention that supported merge strategies do not guarantee. |
| Scope | pass | Initial intent and the scope budget classify the working set, affected contract families, downstream mechanics, historical compatibility, and excluded systems. |
| Governing principle | pass | The principle is short, implementation-independent, and consistent with retaining only decision-relevant current state. |
| Direction | block | The compact model is concrete, but its superseded-history retention boundary is internally dependent on an unsupported guarantee. |
| Feasibility | concern | Consolidation is credible, and the broad replacement constraint is candid; feasibility must be restated after choosing the post-merge retention guarantee. |
| Material impact | pass | Context reduction, loss of working-tree chronology, stable-record contention, materiality judgment, mixed-model risk, migration, and rollback are disclosed. |
| Vision alignment | pass | The direction retains tracked current judgments, decisions, evidence, and handoff state and does not require a hosted service. |
| Downstream authority | pass | Exact schemas, commands, concurrency, freshness, migration mechanics, sequencing, and verification design remain with Design or Delivery. |
| Requested decision | block | Item 9 requests Git-history retention without reconciling supported history rewriting. |

## Scope Preservation Review

- Scope-preservation result: pass. Every material user goal is visible in Goals, the initial-intent table, the scope budget, or the requested decision; excluded and downstream-owned work is explicit, and no requested workstream is silently narrowed.

## Recommended Proposal Edits

- Recommended edits: resolve CCSR-PR1 consistently across the Git-history goal, stable-review and evidence language, trade-off disclosure, feasibility assessment, and requested decision. Preserve the compact current-state direction and all current-state guarantees.

## Recommendation

- Recommendation: changes-requested. Keep the compact current-state model, decide the exact post-merge guarantee for superseded procedural history, revise the proposal without prematurely defining storage mechanics, and run proposal-review-r2. No automatic downstream handoff follows.

## Specialized-gate group

- Active gate predicates: `scope_budget_context`
- Gate outcomes: pass; all major workstreams use recognized scope-budget treatments with reasons and explicit downstream ownership
- Trigger ambiguity: none

## Durable-recording group

- Recording status: recorded
- Recording blocker: none
- Record path: `docs/changes/2026-09-03-compact-current-state-change-record-review-recording/reviews/proposal-review-r1.md`
- Finding-record paths: this detailed review record and `review-resolution.md#proposal-review-r1`
