# Proposal Review R2: Plan-Review Skill Simplification

Review ID: proposal-review-r2
Stage: proposal-review
Round: r2
Reviewer: User-supplied independent proposal-review result normalized by Codex
Target: `docs/proposals/2026-08-13-plan-review-skill-simplification.md`
Reviewed artifact: commit `4c06850c`
Review date: 2026-08-13
Recording status: recorded
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: PRVSIM-PR4, PRVSIM-PR5, PRVSIM-PR6
- Open blockers: the retry state machine, judgment applicability, and settlement final state require proposal revision
- Proposal readiness: not ready for specification
- Immediate next stage: proposal revision
- Automatic downstream handoff: none
- Claim limitations: this review does not approve the proposal, authorize specification, or continue the workflow

## Identity normalization

The supplied review reused `PRVSIM-PR1` through `PRVSIM-PR3` for findings that differ from the already recorded first-round findings. This durable record assigns `PRVSIM-PR4` through `PRVSIM-PR6` so every material finding keeps one stable identity and the review ledger does not conflate separate defects.

## Overall assessment

The proposal retains the correct package boundary: a compact universal `SKILL.md`, one governed review-and-settlement reference, the existing boundary-first reference, and two review-family structural assets. Candidate loading, transaction-result separation, formal recording, profile measurement, and target-runtime exclusions are now well formed.

Three lifecycle details remain insufficiently closed. Operation selection does not exhaust pending, contradictory, ambiguous, and already-settled states; the result asset still requires a semantic status when a retry performs no judgment; and optional authoring-evidence deletion prevents one deterministic, idempotent settlement final state.

## Material findings

### PRVSIM-PR4 — Major: the reviewed-plan operation state machine is not exhaustive

Finding ID: PRVSIM-PR4
Severity: major
Location: Invocation and operation classification; closed outcome matrix; governed reference ownership
Evidence: `settlement-retry` currently requires matching initialization evidence merely to classify the operation, so a second invocation after an exact clean review but before initialization can be misclassified as another initial review. The proposal also leaves already-active entries, duplicate matching reviews, `planned_work` without a clean review, stale plan identity, open resolution, and non-clean status effects without one deterministic result.
Required outcome: Select the operation from the complete transaction state, prevent duplicate semantic review while initialization is pending, and define every pending, matching, active, stale, contradictory, ambiguous, and non-clean outcome.
Safe resolution path: Make `initial-review` valid only when no exact current clean review exists and required initial state is present. Once one exact clean review exists, select `settlement-retry`; return `initialization-required` when `planned_work` is absent, settle a matching `review-required` entry, return idempotent success for an already-active matching entry, and block mismatched, ambiguous, stale, open-resolution, or contradictory state. Map `changes-requested`, `blocked`, `inconclusive`, and blocked recording to distinct deterministic entry and transaction results.
needs-decision rationale: none; the approved review-first initialization transaction determines the safe state machine.

### PRVSIM-PR5 — Major: the result asset requires semantic status when no judgment occurred

Finding ID: PRVSIM-PR5
Severity: major
Location: Structural assets; settlement-retry output
Evidence: The universal core group requires `review status` and material findings for every invocation, while invalid retries create no new semantic review and may not resolve one prior judgment safely. Reporting `blocked` would manufacture a new semantic verdict, while reporting `approved` would claim unsafe judgment reuse.
Required outcome: Separate universal operation output from a conditionally applicable semantic-judgment group.
Safe resolution path: Put operation, transaction result, blockers, action or handoff, and claim limitations in the universal group. Emit a judgment group only when the invocation performed a semantic review or safely reused one exact prior review. Keep recording, governed settlement, boundary, and workflow-managed groups separate; an invalid retry reports a blocked transaction and omits judgment unless one exact prior judgment was safely resolved.
needs-decision rationale: none; review status describes semantic judgment and cannot truthfully serve as transaction-execution status.

### PRVSIM-PR6 — Major: optional evidence removal prevents deterministic settlement

Finding ID: PRVSIM-PR6
Severity: major
Location: Governed reference ownership; settlement retry; recovery
Evidence: The governed reference may optionally remove authoring evidence during settlement. Two successful implementations can therefore leave different durable states, and recovery cannot distinguish a partial deletion from an allowed retained-evidence result.
Required outcome: Select one settlement final state, one identity-checked write sequence, and one interruption-reconciliation policy.
Safe resolution path: Retain authoring, review, and initialization evidence as immutable historical evidence. Validate all identities and conflicts, return idempotent success when the matching entry is already active, otherwise compare-and-set only the exact matching `review-required` entry to `active`, validate the resulting record, and reconcile interruption from the same identities without rereview or duplicate records.
needs-decision rationale: none; retaining evidence is the smallest deterministic policy and preserves traceability.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | Portable judgment is meaningfully separated from governed transaction procedure. |
| User value | pass | The selected package should reduce portable and governed context without weakening rigor. |
| Option diversity | pass | The alternatives remain materially distinct. |
| Decision rationale | pass | One governed reference and two structural assets remain proportionate. |
| Vision fit | pass | The direction improves inspectability and durable evidence. |
| Scope control | pass | The change remains bounded to `plan-review` and directly coupled package surfaces. |
| Transaction state model | block | Duplicate, pending, already-settled, ambiguous, and non-clean cases are incomplete. |
| Output semantics | block | The core requires a review status when no semantic judgment occurred. |
| Idempotency and recovery | concern | Optional evidence deletion prevents one deterministic final state. |
| Testing boundary | pass | Static scenarios and semantic review remain proportionate. |
| Readiness for spec | block | PRVSIM-PR4 through PRVSIM-PR6 require proposal revision. |

## Scope Preservation Review

- Scope-preservation result: pass. The findings close transaction semantics inside the selected package and do not add another runtime, lifecycle owner, resource family, or adjacent skill optimization.

## Recommendation

- Recommendation: revise the proposal to resolve PRVSIM-PR4 through PRVSIM-PR6, then rerun independent `proposal-review` against a frozen revision. No automatic downstream handoff follows this review.

## Specialized-gate group

- Active gate predicates: `scope_budget_context`
- Gate outcomes: pass; the new findings refine same-slice transaction safety without expanding the approved scope budget
- Trigger ambiguity: none

## Durable-recording group

- Recording status: recorded
- Recording blocker: none
- Record path: `docs/changes/2026-08-13-plan-review-skill-simplification/reviews/proposal-review-r2.md`
- Finding-record paths: `docs/changes/2026-08-13-plan-review-skill-simplification/reviews/proposal-review-r2.md`

## Formal-settlement group

- Review ID: proposal-review-r2
- Review record: `docs/changes/2026-08-13-plan-review-skill-simplification/reviews/proposal-review-r2.md`
- Review log: `docs/changes/2026-08-13-plan-review-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-13-plan-review-skill-simplification/review-resolution.md`
- Proposal settlement: revision-required
- Governed change identity: `2026-08-13-plan-review-skill-simplification`
- Formal next-stage eligibility: proposal revision only
