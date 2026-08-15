# Proposal Review R2: Proposal Skill Simplification

Review ID: proposal-review-r2
Stage: proposal-review
Round: r2
Reviewer: independent proposal-review supplied by the user
Target: `docs/proposals/2026-08-14-proposal-skill-simplification.md`
Reviewed artifact: commit `48e949a3`
Review date: 2026-08-14
Recording status: recorded
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: PRSIM-R2-PR1, PRSIM-R2-PR2, PRSIM-R2-PR3
- Open blockers: portable operation resolution, stale-attempt recovery ownership, and specialized structural destinations require proposal revision
- Proposal readiness: not ready for specification
- Immediate next stage: proposal revision
- Automatic downstream handoff: none
- Claim limitations: this review does not approve the proposal, authorize specification, or continue the workflow

## Overall assessment

The proposal retains the right package shape: a compact universal `SKILL.md`, one governed-authoring reference, one strategic and scope gates reference, and one structural proposal skeleton. Candidate selection and reference-owned authority validation are now properly separated, governed transactions are identity-bound, and missing resources fail safely.

Three contracts remain incomplete. Portable authoring is described through a lifecycle entry it does not own, stale changed-basis authoring attempts have no bounded recovery owner, and vision-exception and standing-artifact predicates have no explicit structural destinations in the sole output asset.

## What is strong

### Conditional procedure follows distinct ownership boundaries

The governed reference owns exact lifecycle-authorized mutation, while the strategic reference owns judgment-heavy exceptional gates. Neither reference becomes an independent lifecycle owner.

### Governed creation and revision are identity-bound

Both operations have explicit identities, commit points, retry behavior, and conflict stops. Revision also requires a legal reopen or revision basis.

### Missing resources fail safely

The proposal stops before dependent reads, writes, or judgment and forbids remembered reconstruction of missing conditional procedure.

### Acceptance avoids disproportionate machinery

Static contract scenarios, existing validation, package parity, and ordinary review replace target-agent execution, transcript grading, and an extra manual acceptance stage.

## Material findings

### PRSIM-R2-PR1 — Major: the shared operation matrix conflicts with portable authoring

Finding ID: PRSIM-R2-PR1
Severity: major
Location: Portable and governed operations
Evidence: The shared matrix requires a proposal entry for revision, but portable authoring explicitly writes only the proposal artifact and neither requires nor mutates `change.yaml`. A normal portable revision therefore cannot satisfy the written operation prerequisite.
Required outcome: Resolve portable create and revise from exact target path and file existence, and apply proposal-entry and identity requirements only to governed operations.
Safe resolution path: Add separate portable and governed matrices. Portable create requires an absent exact file, portable revise requires an existing exact file, and ambiguous targets stop. Governed operations additionally use the entry, identity, authority, and retry conditions. A valid structured owning-change pointer may create a governed candidate, but incidental prose may not.
needs-decision rationale: none; operation and lifecycle authority are already independent in the selected design.

### PRSIM-R2-PR2 — Major: stale interrupted authoring has no recovery owner

Finding ID: PRSIM-R2-PR2
Severity: major
Location: Governed creation transaction; Governed revision transaction; Architecture Impact
Evidence: A changed path, governing basis, prior identity, or authorization causes `proposal` to stop, but the stale `authoring` entry and incomplete evidence may still occupy the proposal identity. The original attempt cannot resume and a new attempt cannot start, while no owner may currently reset or abandon the partial state.
Required outcome: Define `authoring-reset-required`, assign exact reset or abandonment to `workflow`, and bound the recovery prerequisites and write set.
Safe resolution path: `proposal` detects and reports the stale attempt without adoption, overwrite, reset, or new transaction. Workflow may reset only the exact `authoring` attempt after proving no review or downstream reliance and no competing transaction. A later proposal operation uses a new evidence path, transaction identity, and current governing basis. Architecture remains not required only if this reuses existing workflow reconciliation authority without new persisted state or ownership.
needs-decision rationale: none; workflow already owns lifecycle routing and reconciliation outside proposal authoring writes.

### PRSIM-R2-PR3 — Major: two specialized predicates lack structural destinations

Finding ID: PRSIM-R2-PR3
Severity: major
Location: Invocation predicates; Structural asset
Evidence: The proposal defines vision-exception, standing-artifact, initial-intent, and scope-budget predicates, but the skeleton receives conditional groups only for initial intent and scope budget. The durable shape for a vision exception or standing-artifact bootstrap decision is therefore unspecified despite the skeleton being the sole structural owner.
Required outcome: Map every specialized predicate to one independently composable conditional group in the existing skeleton.
Safe resolution path: Add `Vision exception or revision` and `Standing artifact dependency or bootstrap` groups alongside the existing intent and scope groups. Keep ordinary `Vision fit` core. The strategic reference owns applicability and meaning; the skeleton owns labels, ordering, fields, and placeholders. Applicable unresolved groups report an explicit blocker, while inapplicable groups are omitted.
needs-decision rationale: none; one skeleton remains sufficient and avoids both ad hoc structure and unnecessary assets.

## Architecture assessment

The expected result remains `architecture-not-required` if stale-attempt recovery reuses existing workflow-owned reconciliation without adding a lifecycle state, persistence record, or write owner. A documentation correction is needed only for stale flat-package inventory. Architecture becomes required if specification introduces new persisted reset state or new lifecycle ownership.

## Acceptance criteria to add

| ID | Criterion |
| --- | --- |
| `AC-PRSIM-019` | Portable operation resolution does not require a proposal entry. |
| `AC-PRSIM-020` | Portable create requires an absent exact target and portable revise requires an existing exact target. |
| `AC-PRSIM-021` | Governed operation resolution additionally uses proposal entry, content identity, and authority. |
| `AC-PRSIM-022` | A governed candidate that fails validation never falls back to portable revision. |
| `AC-PRSIM-023` | A changed-basis partial authoring attempt returns `authoring-reset-required`. |
| `AC-PRSIM-024` | Proposal cannot reset, abandon, adopt, or silently replace a stale attempt. |
| `AC-PRSIM-025` | Workflow reset is bounded to one exact incomplete transaction and proves no review or downstream reliance. |
| `AC-PRSIM-026` | A new attempt after reset receives a new transaction identity and evidence path. |
| `AC-PRSIM-027` | Every specialized predicate has one explicit structural destination. |
| `AC-PRSIM-028` | Vision-exception and standing-artifact groups are independently composable with intent and scope groups. |
| `AC-PRSIM-029` | Applicable unresolved groups report blockers rather than being omitted. |
| `AC-PRSIM-030` | A downstream-relied-upon proposal requires workflow-owned reopening and impact handling before revision. |
| `AC-PRSIM-031` | No target-agent runtime executes during acceptance. |
| `AC-PRSIM-032` | Canonical through installed resources retain required parity. |

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | Universal quality, governed mutation, exceptional gates, and structural duplication are concrete. |
| User value | pass | Portable and ordinary proposals should load less irrelevant procedure. |
| Option diversity | pass | The alternatives are meaningfully different. |
| Decision rationale | pass | Two references and one skeleton remain the right boundary. |
| Vision fit | pass | The direction supports inspectable and resumable proposal reasoning. |
| Scope control | pass | The change remains bounded to proposal and directly coupled package surfaces. |
| Resource selection | pass | Candidate loading and authority validation are separate. |
| Portable operation model | block | Portable revision currently requires a lifecycle entry it cannot own. |
| Transaction recovery | block | Changed-basis partial authoring has no bounded reset route. |
| Structural ownership | block | Two specialized predicates have no explicit output structure. |
| Governed revision | concern | Downstream reliance needs an explicit workflow-owned reopen prerequisite. |
| Missing-resource behavior | pass | Triggered resources fail closed. |
| Semantic preservation | pass | Separate rule and literal ledgers remain appropriate. |
| Testing boundary | pass | Static proof, package parity, and ordinary review are proportionate. |
| Measurement | pass | Loaded assemblies and total package are separate. |
| Architecture awareness | pass with revision | Architecture-not-required depends on reuse of existing workflow reconciliation. |
| Readiness for spec | changes-requested | PRSIM-R2-PR1 through PRSIM-R2-PR3 require revision. |

## Scope Preservation Review

- Scope-preservation result: pass; the user-selected optimization, branch, proposal, review, rigor boundary, and downstream exclusions remain visible.

## Recommended Proposal Edits

- Recommended edits: separate portable and governed operation matrices, add workflow-owned stale-attempt reconciliation, map all four specialized predicates to skeleton groups, and add AC-PRSIM-019 through AC-PRSIM-032.

## Specialized-gate group

- Active gate predicates: `scope_budget_context`, `initial_intent_table_context`
- Gate outcomes: pass for current artifact coverage; the future structural destination contract requires PRSIM-R2-PR3
- Trigger ambiguity: none for this review invocation

## Durable-recording group

- Recording status: recorded
- Recording blocker: none
- Record path: `docs/changes/2026-08-14-proposal-skill-simplification/reviews/proposal-review-r2.md`
- Finding-record paths: this detailed review record

## Formal-settlement group

- Review ID: proposal-review-r2
- Review record: `docs/changes/2026-08-14-proposal-skill-simplification/reviews/proposal-review-r2.md`
- Review log: `docs/changes/2026-08-14-proposal-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-14-proposal-skill-simplification/review-resolution.md`
- Proposal settlement: revision-required
- Governed change identity: `2026-08-14-proposal-skill-simplification`
- Formal next-stage eligibility: blocked pending proposal revision and approving rereview

## Recommendation

- Recommendation: revise the proposal to resolve PRSIM-R2-PR1 through PRSIM-R2-PR3, then run a fresh independent proposal review against the frozen revision. No automatic downstream handoff follows this review.
