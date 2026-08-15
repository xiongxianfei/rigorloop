# Proposal Review R3: Proposal Skill Simplification

Review ID: proposal-review-r3
Stage: proposal-review
Round: r3
Reviewer: Codex independent proposal-review context
Target: `docs/proposals/2026-08-14-proposal-skill-simplification.md`
Reviewed artifact: commit `af900af7`
Review date: 2026-08-14
Recording status: recorded
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: PRSIM-R3-PR1
- Open blockers: stale-attempt reset write ownership conflicts with the current workflow mutation boundary
- Proposal readiness: not ready for specification
- Immediate next stage: proposal revision
- Automatic downstream handoff: none
- Claim limitations: this review does not approve the proposal, authorize specification, or continue the workflow

## Overall assessment

The second revision resolves all three R2 findings. Portable and governed operations are now separate, changed-basis partial attempts have a closed transaction result and recovery prerequisites, and every specialized predicate has an explicit independently composable destination in the sole skeleton.

One material ownership conflict remains. The proposal says workflow may change the proposal entry and incomplete authoring evidence during reset, while the current governed workflow procedure explicitly limits workflow mutation to `workflow_state`, automation state, and workflow-owned evidence and requires it to preserve `artifact_states` and stage-owned evidence. The proposal cannot both reuse existing workflow authority and assign that new write without an architecture and contract decision.

## What is strong

### Portable operations are independent of lifecycle entries

Portable create and revise now depend only on exact target resolution and file existence. Governed operations separately add entry, identity, authority, retry, and no-fallback behavior.

### Partial transaction outcomes are closed

Current-basis partial transactions resume, stale-basis transactions return `authoring-reset-required`, completed matching transactions are idempotent, and unrelated state is never adopted.

### Every specialized predicate has structural ownership

Vision exception, standing artifact, initial intent, and scope budget each map to an independently composable group in the existing skeleton. Ordinary `Vision fit` and universal intent obligations remain core semantics.

### Package and acceptance boundaries remain proportionate

Two references and one asset remain sufficient. Static scenarios, package parity, profile measurements, and ordinary review provide evidence without target-agent execution or a new semantic validator.

## Material findings

### PRSIM-R3-PR1 — Major: workflow-owned reset contradicts the current workflow write boundary

Finding ID: PRSIM-R3-PR1
Severity: major
Location: Stale governed authoring attempts; Architecture Impact; Scope budget
Evidence: The proposal says workflow may reset or abandon the exact proposal entry and incomplete authoring evidence while claiming this reuses existing reconciliation authority and needs no architecture change. The current `skills/workflow/references/governed-lifecycle-routing.md` mutation boundary permits workflow to update only `workflow_state`, selected automation state, and workflow-owned transition evidence; it explicitly preserves `artifact_states` and stage-owned evidence. `CONSTITUTION.md` likewise assigns authoring skills their own governed artifact and matching authoring-state transitions. No existing reset contract authorizes workflow to mutate proposal-owned entry or evidence.
Required outcome: Select one ownership model and align architecture expectation, scope, and acceptance criteria with it.
Safe resolution path: Prefer preserving the current architecture: workflow owns the reset decision, identity validation, no-reliance proof, and routing authorization, while `proposal` executes the explicitly authorized bounded reset of its own exact `authoring` entry and incomplete proposal-authoring evidence before starting a new transaction. The focused proposal-skill contract must define that narrow authoring-stage recovery. If workflow must perform the write directly, change the architecture result to `architecture-required`, include workflow contract and skill changes in scope, and amend the workflow mutation boundary before implementation.
needs-decision rationale: none; preserving existing stage-owned write ownership is the smaller compatible solution.

## Architecture assessment

Architecture is `architecture-not-required` only under the recommended split in which workflow authorizes and routes recovery while proposal performs its own bounded stage-owned reset. Direct workflow mutation of proposal-owned `artifact_states` or evidence makes architecture work required and expands the change into workflow package ownership.

## Acceptance criteria to add or revise

| ID | Criterion |
| --- | --- |
| `AC-PRSIM-033` | Workflow owns stale-attempt validation, no-reliance proof, reset authorization, and routing but does not mutate proposal-owned entry or evidence. |
| `AC-PRSIM-034` | Proposal may execute only the exact authorized reset of its own incomplete `authoring` entry and proposal-authoring evidence. |
| `AC-PRSIM-035` | Reset authorization is identity-bound, current, single-use or idempotently consumed, and cannot affect another artifact or transaction. |
| `AC-PRSIM-036` | A new proposal operation starts only after the bounded reset validates and receives a new transaction identity. |
| `AC-PRSIM-037` | Direct workflow mutation of proposal-owned state requires architecture and workflow-contract changes before implementation. |

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | Common-path cost and duplicated ownership remain concrete. |
| User value | pass | Portable and ordinary proposal authoring should load less irrelevant procedure. |
| Option diversity | pass | The alternatives remain meaningfully different. |
| Decision rationale | pass | Two references and one skeleton remain proportionate. |
| Vision fit | pass | The direction preserves inspectable, resumable proposal reasoning. |
| Scope control | concern | Direct workflow reset would expand scope into workflow ownership and architecture. |
| Resource selection | pass | Candidate loading and authoritative validation are correctly separated. |
| Portable operation model | pass | Portable operations no longer require lifecycle entries. |
| Transaction recovery | pass with revision | State outcomes are closed, but reset write ownership conflicts with current architecture. |
| Structural ownership | pass | Every specialized predicate has one explicit destination. |
| Governed revision | pass | Downstream reliance requires workflow-owned impact handling before reopen. |
| Missing-resource behavior | pass | Triggered resources fail closed. |
| Semantic preservation | pass | Rule and literal inventories remain separate. |
| Testing boundary | pass | Static proof and package parity are proportionate. |
| Measurement | pass | Loaded assemblies and total package are separate. |
| Architecture awareness | block | The claimed no-impact result conflicts with the selected direct workflow write. |
| Readiness for spec | changes-requested | PRSIM-R3-PR1 requires proposal revision. |

## Scope Preservation Review

- Scope-preservation result: pass; all initial goals remain visible, but recovery ownership must be corrected without silently expanding into workflow redesign.

## Recommended Proposal Edits

- Recommended edits: make workflow the recovery decision and routing owner, make proposal the bounded reset writer for its own stage-owned partial state, add AC-PRSIM-033 through AC-PRSIM-037, and retain `architecture-not-required` only for that ownership-preserving design.

## Specialized-gate group

- Active gate predicates: `scope_budget_context`, `initial_intent_table_context`
- Gate outcomes: pass; current intent and scope classifications remain complete
- Trigger ambiguity: none

## Durable-recording group

- Recording status: recorded
- Recording blocker: none
- Record path: `docs/changes/2026-08-14-proposal-skill-simplification/reviews/proposal-review-r3.md`
- Finding-record paths: this detailed review record

## Formal-settlement group

- Review ID: proposal-review-r3
- Review record: `docs/changes/2026-08-14-proposal-skill-simplification/reviews/proposal-review-r3.md`
- Review log: `docs/changes/2026-08-14-proposal-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-14-proposal-skill-simplification/review-resolution.md`
- Proposal settlement: revision-required
- Governed change identity: `2026-08-14-proposal-skill-simplification`
- Formal next-stage eligibility: blocked pending ownership correction and approving rereview

## Recommendation

- Recommendation: revise recovery write ownership to preserve the existing stage-owned mutation boundary, then run a fresh proposal review. No automatic downstream handoff follows this review.
