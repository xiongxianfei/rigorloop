# Proposal Review R1: Proposal Skill Simplification

Review ID: proposal-review-r1
Stage: proposal-review
Round: r1
Reviewer: Codex independent proposal-review context
Target: `docs/proposals/2026-08-14-proposal-skill-simplification.md`
Reviewed artifact: commit `891f937d`
Review date: 2026-08-14
Recording status: recorded
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: PRSIM-PR1, PRSIM-PR2, PRSIM-PR3
- Open blockers: governed-reference selection, recoverable authoring transactions, and specialized-gate applicability require proposal revision
- Proposal readiness: not ready for specification
- Immediate next stage: proposal revision
- Automatic downstream handoff: none
- Claim limitations: this review does not approve the proposal, authorize specification, or continue the workflow

## Overall assessment

The proposal selects the right package boundary: a compact universal proposal contract, one governed authoring reference, one strategic and scope gates reference, and one structural skeleton. The split follows real activation and authority differences rather than arbitrary document size, and the proposal correctly measures loaded assemblies separately from total package size.

The proposal also protects the right universal content: decision quality, option comparison, intent preservation, evidence integrity, claim boundaries, and review handoff remain inline. Its rejection of a runtime classifier, target-agent acceptance, and an additional manual semantic-review gate is proportionate.

Three contracts still need proposal-level closure. The governed trigger requires the authority validation owned by the reference before the reference can load, the create and revise operations cannot recover from their own intermediate states, and the specialized predicates do not preserve the current scope-budget triggers or distinguish the two conditional output groups completely.

## What is strong

### Two references correspond to different authority boundaries

Governed proposal-entry mutation and strategic exception judgment are not variants of one procedure. Keeping them independently loadable prevents portable gated proposals from loading `change.yaml` mutation and prevents ordinary governed proposals from loading unrelated exception procedure.

### Universal proposal quality remains self-sufficient

Problem framing, user value, alternatives, decision rationale, intent preservation, risks, stops, claims, and `proposal-review` handoff remain available before any conditional reference is selected.

### Structural ownership is explicit

The existing skeleton remains the sole owner of headings, ordering, table shapes, and placeholders. The proposal also correctly keeps applicability, meaning, readiness, and lifecycle authority out of the asset.

### Proof and measurement are proportionate

The proposal requires rule and literal inventories, deterministic static scenarios, package parity, and profile measurements without introducing semantic prose scoring, a permanent simplicity validator, or target-agent runtime execution.

## Material findings

### PRSIM-PR1 — Major: governed reference loading requires the validation that the reference owns

Finding ID: PRSIM-PR1
Severity: major
Location: Invocation predicates; Loaded assemblies; Portable and governed operations
Evidence: `governed_proposal_context` becomes true only after confirming one exact governed change, the lifecycle marker, deterministic placement, settled prerequisites, and current proposal-authoring authority. The governed reference is separately assigned authority validation, exact entry resolution, and legal transition checks. The main file must therefore perform much of the conditional procedure before it can decide to load the resource that owns that procedure. This is circular and can force the portable common path to inspect complete governed state.
Required outcome: Separate a positive candidate predicate used only for resource selection from reference-owned authoritative validation, and define deterministic failure behavior when a candidate does not validate.
Safe resolution path: Introduce `governed_proposal_candidate_context`, established by an explicit current change identity, a workflow-managed proposal invocation, or a proposal artifact already pointing to an owning change record. Key the `PA1` assemblies to that candidate. After loading, the reference validates the complete change record, lifecycle marker, exact proposal entry or deterministic creation path, prerequisites, and legal authoring state. A candidate that fails validation stops and never falls back to portable authoring. Conversational mentions of changes or workflows do not establish the candidate.
needs-decision rationale: none; this preserves the selected reference boundary while preventing circular loading.

### PRSIM-PR2 — Major: create and revise transactions cannot recover from their own intermediate states

Finding ID: PRSIM-PR2
Severity: major
Location: Portable and governed operations; Resource ownership; Expected Behavior Changes
Evidence: The operation matrix permits governed creation only when both proposal entry and file are absent, but the current authoring contract sets the matching entry to `authoring` before completing the proposal. An interruption after that write produces an entry-present/file-absent state that the matrix classifies as a conflict, so an identical retry cannot resume. Revision likewise promises retry and concurrency handling without selecting a prior identity, write sequence, evidence basis, commit point, or idempotent final state.
Required outcome: Define complete create and revise transactions, including retry identity, write order, allowed partial states, collision handling, and one idempotent completion state.
Safe resolution path: Use entry-first governed transactions. Creation binds the change ID, artifact ID, normalized intended path, governing input identities, and authoring-evidence path before creating the exact `authoring` entry; an identical entry-only retry may resume, while an unrelated file or mismatched basis stops. Revision additionally binds the prior proposal content identity and authorized reopen or revision evidence before clearing only the current review mapping. Both operations write and validate proposal content, compute the new identity, complete authoring evidence, and transition only the matching entry to `review-required`. Matching completed retries are no-ops; mismatched, ambiguous, or competing writes stop.
needs-decision rationale: none; the proposal already chooses governed retry and concurrency handling, so its recoverable transaction must be executable.

### PRSIM-PR3 — Major: specialized-gate predicates and structural applicability do not preserve the current contract

Finding ID: PRSIM-PR3
Severity: major
Location: Invocation predicates; Structural asset; Scope budget; Semantic preservation and compatibility
Evidence: The proposal defines `scope_budget_context` only as broad or multi-workstream scope needing detailed treatment. The current proposal contract also positively triggers a scope budget for multiple lifecycle families, multiple downstream artifacts, policy or generated-output work, and a proposal-review concern. The proposed simplification itself is policy and generated-output work, so the narrowed wording could remove a current obligation. The proposal also uses `scope_budget_context` for the scope-budget group but describes the initial-intent group with a separate broad or multi-part condition that has no named predicate or closed relationship to the four assemblies.
Required outcome: Preserve or explicitly amend every current positive gate trigger and define independent applicability for the initial-intent and scope-budget structural groups.
Safe resolution path: Add `initial_intent_table_context` for broad or multi-part initial requests. Define `scope_budget_context` with the current positive evidence set: multiple independent work items, multiple lifecycle families, multiple plausible downstream artifacts, policy or generated-output scope, or a current proposal-review concern. Treat semantic applicability as proposal judgment, apply both predicates independently, and load the gates reference when either is true or when vision or standing-artifact predicates are true. Define omission only for a small single-decision proposal with no positive trigger and no silent-narrowing risk.
needs-decision rationale: none; the existing public contract supplies the trigger set.

## Architecture assessment

The expected architecture outcome remains `architecture-not-required`. The change uses the existing package model, canonical source, mapped resources, and generated parity rules, and it adds no runtime, persistence, dependency, transformation, or lifecycle owner. A bounded documentation correction is needed only if current architecture contains a flat `proposal` inventory or an obsolete no-reference statement. A new ADR is warranted only if later work changes the normative package or state model.

## Acceptance criteria to add

| ID | Criterion |
| --- | --- |
| `AC-PRSIM-001` | Governed resource selection uses a candidate predicate distinct from authoritative governed validation. |
| `AC-PRSIM-002` | A governed candidate that fails validation stops and cannot fall back to portable authoring. |
| `AC-PRSIM-003` | Conversational wording alone cannot establish governed candidate or authority. |
| `AC-PRSIM-004` | Governed creation has an identity-bound entry-first transaction and an identical entry-only recovery path. |
| `AC-PRSIM-005` | Governed revision binds the prior content identity and current legal revision authority. |
| `AC-PRSIM-006` | Completed identical retries are idempotent and conflicting partial states fail closed. |
| `AC-PRSIM-007` | Initial-intent-table applicability has its own closed predicate. |
| `AC-PRSIM-008` | Scope-budget applicability preserves every current positive trigger unless the governing contract is amended. |
| `AC-PRSIM-009` | Conditional structural groups are selected independently and inapplicable groups are omitted. |
| `AC-PRSIM-010` | Every real loaded assembly decreases or has one independently reviewed semantic-preservation exception. |
| `AC-PRSIM-011` | No target-agent runtime or separate manual semantic-review acceptance stage is introduced. |
| `AC-PRSIM-012` | Canonical, generated, archived, release-candidate, and installed resources retain required parity. |

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | Common-path overload, conditional procedure, and duplicate structure are concrete and measured. |
| User value | pass | Portable and ordinary proposals should become easier to scan without losing decision rigor. |
| Option diversity | pass | Unchanged, inline compression, one reference, two references, and an executable engine are materially different. |
| Decision rationale | pass | Two references follow distinct activation and authority boundaries. |
| Vision fit | pass | The change supports inspectable and reusable proposal reasoning. |
| Scope control | pass | Runtime machinery, adjacent-skill optimization, historical rewriting, and extra assets are excluded. |
| Trigger model | block | Governed loading requires reference-owned validation before the reference can load. |
| Transaction model | block | Entry-first interruption and revision retries have no executable recovery contract. |
| Specialized gates | block | The current scope-budget trigger set and initial-intent applicability are not closed. |
| Structural ownership | pass | The skeleton remains a structural leaf rather than a policy owner. |
| Testing boundary | pass | Static proof, package parity, and normal review are proportionate; runtime execution is excluded. |
| Measurement | pass | Loaded assemblies and total package size are separated, with no normative percentage. |
| Architecture awareness | pass | `architecture-not-required` is plausible after a bounded inventory check. |
| Readiness for spec | changes-requested | PRSIM-PR1 through PRSIM-PR3 require proposal revision. |

## Scope Preservation Review

- Scope-preservation result: pass; all user goals are classified and the selected work, branch creation, formal review, rigor boundary, and downstream exclusions are visible.

## Recommended Proposal Edits

- Recommended edits: replace the circular governed predicate with candidate selection plus reference-owned validation; add complete create and revise transaction tables; restore the current scope-budget trigger set; and name independent initial-intent structural applicability.

## Specialized-gate group

- Active gate predicates: `scope_budget_context`, `initial_intent_table_context`
- Gate outcomes: pass for current artifact coverage; the proposal contains complete intent and scope-budget tables, but its future skill trigger contract needs the corrections in PRSIM-PR3
- Trigger ambiguity: none for this review invocation

## Durable-recording group

- Recording status: recorded
- Recording blocker: none
- Record path: `docs/changes/2026-08-14-proposal-skill-simplification/reviews/proposal-review-r1.md`
- Finding-record paths: this detailed review record

## Formal-settlement group

- Review ID: proposal-review-r1
- Review record: `docs/changes/2026-08-14-proposal-skill-simplification/reviews/proposal-review-r1.md`
- Review log: `docs/changes/2026-08-14-proposal-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-14-proposal-skill-simplification/review-resolution.md`
- Proposal settlement: revision-required
- Governed change identity: `2026-08-14-proposal-skill-simplification`
- Formal next-stage eligibility: blocked pending proposal revision and approving rereview

## Recommendation

- Recommendation: revise the proposal to resolve PRSIM-PR1 through PRSIM-PR3, then run a new independent proposal review against the frozen revised artifact. No automatic downstream handoff follows this review.
