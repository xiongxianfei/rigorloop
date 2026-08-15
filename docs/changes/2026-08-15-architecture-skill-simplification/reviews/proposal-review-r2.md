# Proposal Review R2: Architecture Skill Simplification

Review ID: proposal-review-r2
Stage: proposal-review
Round: r2
Reviewer: Codex independent proposal-review context
Target: `docs/proposals/2026-08-15-architecture-skill-simplification.md`
Reviewed artifact: commit `d821bfb2`
Review date: 2026-08-15
Recording status: recorded
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: ARSIM-PR4, ARSIM-PR5, ARSIM-PR6
- Open blockers: current assessment binding, durable pre-write manifest evidence, and dependency-safe combined commits require proposal revision
- Proposal readiness: not ready for specification
- Immediate next stage: proposal revision
- Automatic downstream handoff: none
- Claim limitations: this review does not approve the proposal, authorize specification, complete architecture assessment, or continue the workflow

## Overall assessment

The revised proposal retains the right package boundary and resolves the first-round assessment, mixed-target, and asset-ownership concerns. Universal assessment stays self-sufficient, method and governed procedure have coherent conditional owners, and canonical architecture plus ADRs use distinct target identities.

Three transaction contracts remain incomplete. Workflow-managed authoring is not bound to the current architecture-required assessment that authorized it, exact retry assumes a manifest that is not durably persisted before file mutation, and combined canonical/ADR commits lack dependency and intermediate-validity rules.

## Material findings

### ARSIM-PR4 — Major: later authoring is not bound to a current architecture-required assessment

Finding ID: ARSIM-PR4
Severity: major
Location: Classification model; Target manifest and transaction model; Assessment isolation and recording
Evidence: The proposal says `architecture-required` permits later authoring and records workflow-managed assessment receipts, but the governed-authoring prerequisites and manifest do not bind the authoring operation to one current required assessment, exact spec identity, and approving spec-review identity. A later spec or review change, contradictory assessment, or unresolved ambiguity can therefore leave authoring eligibility stale.
Required outcome: Require every workflow-managed authoring manifest to bind one current `architecture-required` assessment receipt with matching spec and approving spec-review identities, no later contradictory assessment, and no unresolved ambiguity; require portable authoring to perform a current inline applicability judgment.
Safe resolution path: Add an `assessment_basis` manifest group, define decision-bearing staleness inputs, and block missing, stale, contradictory, not-required, or ambiguous assessment evidence before mutation.
needs-decision rationale: none; the existing assessment receipt can provide the authority basis without changing the package design.

### ARSIM-PR5 — Major: exact retry lacks a durable prepared manifest before the first write

Finding ID: ARSIM-PR5
Severity: major
Location: Target manifest and transaction model; Multi-file writes, retries, and recovery; Architecture Impact
Evidence: The proposal requires exact manifest-based retry, but its sequence writes package files before complete authoring evidence is recorded. An interruption after the first file write can therefore leave no durable record of the intended manifest, identities, order, or baseline needed to distinguish a valid partial write from unrelated content.
Required outcome: Persist the complete ordered manifest and intended file identities in existing authoring evidence before the first target-file mutation, then record target progress and final disposition on the same evidence surface.
Safe resolution path: Use a prepared write-ahead authoring record, revalidate authority and baselines after preparation, reconcile only files named in that record, and make architecture work required if the existing evidence model cannot represent the protocol without a new schema or owner.
needs-decision rationale: none; the proposal can first require proof that the existing evidence surface supports prepared and progress evidence.

### ARSIM-PR6 — Major: combined canonical and ADR commits lack dependency and intermediate-validity rules

Finding ID: ARSIM-PR6
Severity: major
Location: Target manifest and transaction model; Multi-file writes, retries, and recovery
Evidence: The proposal permits independently committed targets and `partial-blocked`, but an ordered manifest alone does not prevent canonical Markdown from linking to an unwritten diagram or ADR, a predecessor ADR from being superseded before its replacement exists, or a partially committed target from being invalid without its dependents.
Required outcome: Add explicit dependency edges, commit groups, and an independently-valid-after-commit predicate; define canonical-package and ADR supersession write order; preserve only independently valid completed targets after partial failure.
Safe resolution path: Write subordinate diagrams and ADR dependencies before canonical Markdown, treat canonical Markdown as the package commit point, group targets that cannot be safe independently, keep review as the supersession approval owner, and block unsafe partial commits.
needs-decision rationale: none; dependency-aware procedure can remain inside the selected governed-authoring reference when the existing evidence surface can record it.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | Assessment, method, governed mutation, and structural ownership remain concrete. |
| User value | pass | Assessment and portable authoring should load less unrelated procedure. |
| Option diversity | pass | The alternatives remain materially distinct. |
| Decision rationale | pass | Two references follow real method and authority boundaries. |
| Vision fit | pass | The change supports inspectable durable architecture work. |
| Scope control | pass | Runtime machinery, method redesign, and architecture-review optimization remain excluded. |
| Classification model | concern | Authoring eligibility is not yet bound to the current assessment occurrence. |
| Retry and recovery | block | Exact recovery requires a durable prepared manifest before mutation. |
| Combined transaction safety | block | Dependency and intermediate-validity rules are absent. |
| Asset ownership | pass | The first-round structural disposition is now closed. |
| Testing boundary | pass | Static scenarios and package proof remain proportionate. |
| Architecture awareness | concern | `architecture-not-required` depends on capabilities the proposal has not yet required proving. |
| Readiness for spec | changes-requested | ARSIM-PR4 through ARSIM-PR6 require proposal revision. |

## Scope Preservation Review

- Scope-preservation result: pass; the requested optimization, branch, governed proposal, and proposal review remain visible and classified.

## Recommended Proposal Edits

- Recommended edits: bind authoring to current assessment evidence, persist a complete prepared manifest before mutation, add dependency and commit-group semantics, and update architecture impact, scenarios, risks, and acceptance criteria before rereview.

## Specialized-gate group

- Active gate predicates: `initial_intent_table_context`, `scope_budget_context`
- Gate outcomes: pass; initial goals and work items remain explicitly classified
- Trigger ambiguity: none

## Durable-recording group

- Recording status: recorded
- Recording blocker: none
- Record path: `docs/changes/2026-08-15-architecture-skill-simplification/reviews/proposal-review-r2.md`
- Finding-record paths: this detailed review record

## Formal-settlement group

- Review ID: proposal-review-r2
- Review record: `docs/changes/2026-08-15-architecture-skill-simplification/reviews/proposal-review-r2.md`
- Review log: `docs/changes/2026-08-15-architecture-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-15-architecture-skill-simplification/review-resolution.md`
- Proposal settlement: revision-required
- Governed change identity: `2026-08-15-architecture-skill-simplification`
- Formal next-stage eligibility: blocked pending proposal revision and approving rereview

## Recommendation

- Recommendation: revise the proposal to resolve ARSIM-PR4 through ARSIM-PR6, then run a new independent proposal review against the committed revision. No automatic downstream handoff follows this review.
