# Proposal Review: Learn Skill Simplification

Review ID: proposal-review-r2
Stage: proposal-review
Round: r2
Reviewer: external review supplied by contributor and reconstructed by Codex
Target: `docs/proposals/2026-08-16-learn-skill-simplification.md`

Reviewed artifact: `docs/proposals/2026-08-16-learn-skill-simplification.md` at commit `24cdadda`
Review date: 2026-08-16
Recording status: recorded
Reconstruction status: reconstructed from contributor-supplied review
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: LRNSIM-PR4, LRNSIM-PR5, LRNSIM-PR6
- Open blockers: actual trigger-assessment usage, interruption semantics, and later derivative-route reconciliation require proposal decisions
- Proposal readiness: not ready for specification
- Immediate next stage: proposal revision
- Automatic downstream handoff: none
- Claim limitations: this reconstructed review does not approve the proposal, authorize specification, or continue the workflow

The supplied review reused `LRNSIM-PR1`, `LRNSIM-PR2`, and `LRNSIM-PR3`, which already identify findings in `proposal-review-r1`. This durable reconstruction assigns the unique IDs `LRNSIM-PR4`, `LRNSIM-PR5`, and `LRNSIM-PR6` while preserving the supplied findings' meaning and order.

## Overall assessment

The compact universal skill, one session-method reference, and absence of templates or scripts remain a strong package direction. The authority split between contributor confirmation and destination mutation is also sound. The revised proposal now separates session recording from derivative completion and binds session attempts more safely than the current skill.

The review identifies three remaining decisions. The proposed trigger-assessment operation has no demonstrated repository caller. The proposal promises exact interrupted-session resume without durable phase and effect progress. Pending owner routes have no later learn-owned method for recording completed destinations. Those concerns are valid, but their resolution must remain proportionate to a skill-package simplification rather than silently adding a transaction engine.

### LRNSIM-PR4 — Major: trigger assessment lacks an observed caller

Finding ID: LRNSIM-PR4
Severity: major
Location: `Recommended Direction`, `Expected Behavior Changes`, measurement profiles, and `AC-LRNSIM-002`–`003`
Evidence: `assess-learn-trigger` remains a public operation even though the proposal defers proof of an actual caller until later inventory. Repository guidance describes pre-session closeout as behavior of the trigger-owning surface when no session runs, but does not currently invoke `learn` solely to perform a formal assessment. The operation also lacks an exact owner, trigger-occurrence, scope, and evidence-basis request envelope.
Required outcome: Decide before specification whether trigger assessment is a real supported learn operation; retain it only with an observed repository caller and an exact request contract.
Safe resolution path: Complete a bounded inventory now. If no caller exists, remove the operation and LR0 usage claim, let trigger owners decide whether to invoke learn, and keep explicit learn invocations session-based. If a caller exists, identify it and close the read-only envelope.
needs-decision rationale: none; the inventory can determine the first-version choice.

### LRNSIM-PR5 — Major: exact resume lacks durable phase progress

Finding ID: LRNSIM-PR5
Severity: major
Location: `Session identity and retry`, architecture impact, scenarios, and `AC-LRNSIM-008`–`010`
Evidence: The proposal promises resume at the first incomplete phase and idempotent completion without defining durable phase completion, contributor-confirmation progress, prepared topic effects, or whether a side effect occurred before interruption. Markdown section presence cannot safely prove phase completion. Exact crash recovery would require more persistent execution state than the proposal currently acknowledges.
Required outcome: Either define durable phase and side-effect progress before claiming exact resume, or explicitly narrow the first version to fail-closed interruption handling without automatic resume.
Safe resolution path: Prefer the bounded first version: create a unique session record at Frame, perform ordinary identity and concurrent-write checks, make no automatic arbitrary-interruption resume claim, and stop for explicit repair or a new linked session when partial state is ambiguous. Treat transaction-grade recovery as separate architecture-bearing work if later evidence justifies it.
needs-decision rationale: none; the proposal may choose the proportionate fail-closed alternative.

### LRNSIM-PR6 — Major: later owner results lack bounded reconciliation

Finding ID: LRNSIM-PR6
Severity: major
Location: derivative settlement model, same-turn continuation, session-completion behavior, and acceptance criteria
Evidence: A completed session may retain multiple pending owner-bound routes, but the proposal defines no later operation for recording exact owner-produced artifacts. Rerunning the completed session is described as an idempotent no-op, destination owners do not own the learn record, and one aggregate routing value cannot express mixed per-route outcomes.
Required outcome: Define a bounded way to record later owner results per route without giving learn destination-mutation authority or turning it into a general workflow engine.
Safe resolution path: Give each derivative route a stable identity derived from its observation and route kind. Add a narrow explicit `record-learn-route-result` operation that updates only the exact session link and status when an owner-produced artifact or permitted durable follow-up identity is supplied. Do not query, poll, classify again, derive an aggregate workflow state, or mutate destination surfaces.
needs-decision rationale: none; a link-recording operation is sufficient for the existing R8 traceability obligation.

## Architecture assessment

The expected result remains `architecture-not-required` only if the proposal removes transaction-grade phase recovery and keeps later route recording as a bounded update to the existing session document. A new machine-readable session state model, transaction artifact, cross-stage coordinator, polling system, or persistence owner requires architecture work.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | Common-path and authority problems remain concrete. |
| User value | pass | The package can become easier to scan without weakening evidence quality. |
| Option diversity | pass | The proposal compares flat, compressed, referenced, fragmented, and executable designs. |
| Decision rationale | pass with revisions | The reference remains reasonable, but the claimed lightweight profile must be evidence-backed. |
| Vision fit | pass | Durable human-confirmed learning remains aligned. |
| Scope control | concern | Transaction and reconciliation detail risks expanding beyond package simplification. |
| Trigger-assessment operation | block | No actual caller or request envelope is established. |
| Session interruption | block | Exact resume lacks durable phase and effect progress. |
| Derivative traceability | block | Later owner results cannot be recorded per route. |
| Cross-owner authority | pass | Learn does not gain destination mutation authority. |
| Testing boundary | pass | Static scenarios and package proof remain appropriate. |
| Architecture awareness | concern | No-architecture depends on selecting bounded fail-closed recovery. |
| Readiness for spec | changes-requested | LRNSIM-PR4 through LRNSIM-PR6 require revision. |

## Scope Preservation Review

- Scope-preservation result: pass; the initial optimization, evidence, confirmation, no-template, and deterministic proof goals remain visible.

## Recommended Proposal Edits

- Remove unproven trigger assessment and its measured profile.
- Replace exact arbitrary-interruption resume with explicit fail-closed partial-state behavior.
- Add only a narrow per-route result-link operation required for session traceability.
- Keep transaction-grade recovery and automated reconciliation outside this proposal.

## Recommendation

- Recommendation: revise the proposal, then perform independent proposal rereview. No automatic downstream handoff follows this review.

## Specialized-gate group

- Active gate predicates: `scope_budget_context`
- Gate outcomes: pass with required narrowing; the transaction/reconciliation expansion must be explicitly excluded or separately proposed
- Trigger ambiguity: none

## Durable-recording group

- Recording status: recorded
- Recording blocker: none
- Record path: `docs/changes/2026-08-16-learn-skill-simplification/reviews/proposal-review-r2.md`
- Finding-record paths: this detailed review record

## Formal-settlement group

- Review ID: proposal-review-r2
- Review record: `docs/changes/2026-08-16-learn-skill-simplification/reviews/proposal-review-r2.md`
- Review log: `docs/changes/2026-08-16-learn-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-16-learn-skill-simplification/review-resolution.md`
- Proposal settlement: revision-required
- Governed change identity: `2026-08-16-learn-skill-simplification`
- Formal next-stage eligibility: blocked pending proposal revision and approving rereview
