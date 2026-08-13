# Proposal Review R2: Test-Spec Skill Simplification

Review ID: proposal-review-r2
Stage: proposal-review
Round: r2
Reviewer: independent proposal-review supplied by user
Target: `docs/proposals/2026-08-13-test-spec-skill-simplification.md`
Reviewed artifact: commit `07c9ac8d`
Review date: 2026-08-13
Recording status: recorded
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: TSSIM-PR4, TSSIM-PR5, TSSIM-PR6
- Open blockers: governed revision, stale interrupted-authoring recovery, and manual-verification ownership require proposal revision
- Proposal readiness: not ready for specification
- Immediate next stage: proposal revision
- Automatic downstream handoff: none
- Claim limitations: this review does not approve the proposal, authorize specification, or continue the workflow

## Overall assessment

The proposal retains the correct package direction: a shorter universal `SKILL.md`, one governed authoring reference, both existing boundary-first references, and the existing structural assets. Portable and governed authority, entry-first creation, stage settlement, boundary compatibility, static acceptance, and loaded-profile measurement are well framed.

Three contracts remain incomplete. Revision is named without a full transaction, changed-basis interrupted creation has no valid recovery route, and the proposal does not explicitly reconcile optional manual verification with its structural single-owner claim.

## Material findings

### TSSIM-PR4 — Major: governed revision lacks a complete transaction

Finding ID: TSSIM-PR4
Severity: major
Location: Invocation and authority model; Governed creation and retry; Testing and Verification Strategy
Evidence: The proposal declares `revise-primary-test-spec` but defines only its high-level prerequisites. It does not close legal source states, authorizing evidence, prior review staleness, implementation reliance, write order, retry identity, historical evidence, or the return to fresh review.
Required outcome: Define a complete governed revision transaction with legal states, exact authority, prior/new identities, review invalidation, identical retry, and downstream-reliance stops.
Safe resolution path: Restrict ordinary revision to a current exact test spec with authorized review findings or changed governing inputs. Move only the matching entry to `authoring`, preserve prior review evidence as historical evidence for the old identity, bind revision evidence to the prior identity and new inputs, write and validate the new identity, return to `review-required`, and require fresh `test-spec-review`. Active implementation reliance must stop ordinary revision until workflow routes an approved reopen operation.
needs-decision rationale: none; existing authoring and review-staleness contracts determine the safe boundary.

### TSSIM-PR5 — Major: changed-basis interrupted creation has no recovery route

Finding ID: TSSIM-PR5
Severity: major
Location: Governed creation and retry; Rollout and Rollback; Acceptance criteria
Evidence: A partial creation whose governing basis changes cannot use identical retry, but it may also lack the complete file and identity required for revision. The current instruction to start an authorized revision can therefore strand an `authoring` entry.
Required outcome: Define an exact stale-attempt result, bounded closeout owner, write set, and restart identity without adopting or rewriting the partial attempt.
Safe resolution path: `test-spec` reports `stale-authoring-attempt` and stops. Under existing stage-owned authority, workflow may authorize and route recovery, but only `test-spec` may abandon its exact incomplete artifact entry with stage-owned closeout evidence after proving no review or downstream reliance exists. A later create operation uses a new authoring-evidence path and retry identity. Unrelated entries, review evidence, workflow state, and automation state remain unchanged.
needs-decision rationale: none; workflow-owned mutation would conflict with the accepted stage-owned lifecycle contract, so workflow routes while `test-spec` owns its artifact closeout.

### TSSIM-PR6 — Major: manual-verification structure is not explicitly reconciled with existing owners

Finding ID: TSSIM-PR6
Severity: major
Location: Goals; Universal `SKILL.md` content; Structural ownership; Acceptance criteria
Evidence: The proposal preserves manual-proof IDs and claims the existing assets are sole structural owners, but it does not state where the already-approved manual and hybrid proof fields and optional Manual QA checklist live. This ambiguity could cause ad hoc new structure or an unnecessary new asset.
Required outcome: Identify the existing structural owners for manual and hybrid proof without introducing a new manual-proof contract in this simplification.
Safe resolution path: Preserve current behavior: the proof reference owns automation mode and manual-procedure IDs, the proof-obligation row owns their mapping, `test-case.md` owns `Level`, evidence, and automation-location fields, `milestone-proof-row.md` owns milestone manual-proof IDs, and the skeleton owns the optional Manual QA checklist location. Use `none`, `-`, or `not applicable` when manual verification is not required. Do not add a conditional manual-proof group or sixth asset unless a separate approved contract later standardizes a new repeated record.
needs-decision rationale: none; the approved test-spec proof-contract upgrade explicitly excludes a new manual-proof contract and asset.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | The common-path and ownership problem remains concrete. |
| User value | pass | Both authoring profiles should become easier to scan. |
| Option diversity | pass | Options remain materially distinct. |
| Decision rationale | pass | One governed reference and existing resources remain proportionate. |
| Vision fit | pass | The change improves usable traceability. |
| Scope control | pass | Runtime, adjacent skills, and boundary redesign remain excluded. |
| Architecture awareness | pass | Existing package architecture likely suffices after bounded assessment. |
| Testability | block | Revision and stale-attempt recovery lack complete expected outcomes. |
| Risk honesty | pass with revisions | The new transaction and structural ambiguities need explicit treatment. |
| Rollout realism | pass with revisions | Recovery and historical evidence must be closed before implementation planning. |
| Readiness for spec | block | TSSIM-PR4 through TSSIM-PR6 require proposal revision. |

## Scope Preservation Review

- Scope-preservation result: pass. The proposal retains every initial goal and its scope budget still distinguishes core, same-slice, and excluded work without hidden follow-ups.

## Recommended Proposal Edits

- Add a complete governed revision transaction with fresh review and active-implementation stop behavior.
- Add `stale-authoring-attempt`, test-spec-owned bounded abandonment, and new-identity restart behavior.
- Clarify that current distributed structures already represent optional manual verification and explicitly prohibit a new manual-proof contract or asset in this slice.

## Recommendation

- Recommendation: revise the proposal to resolve TSSIM-PR4 through TSSIM-PR6, then rerun independent `proposal-review` against a frozen revision. No automatic downstream handoff follows this review.

## Specialized-gate group

- Active gate predicates: `scope_budget_context`
- Gate outcomes: pass; all current and excluded work has a valid treatment and reason
- Trigger ambiguity: none

## Durable-recording group

- Recording status: recorded
- Recording blocker: none
- Record path: `docs/changes/2026-08-13-test-spec-skill-simplification/reviews/proposal-review-r2.md`
- Finding-record paths: `docs/changes/2026-08-13-test-spec-skill-simplification/reviews/proposal-review-r2.md`

## Formal-settlement group

- Review ID: proposal-review-r2
- Review record: `docs/changes/2026-08-13-test-spec-skill-simplification/reviews/proposal-review-r2.md`
- Review log: `docs/changes/2026-08-13-test-spec-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-13-test-spec-skill-simplification/review-resolution.md`
- Proposal settlement: revision-required
- Governed change identity: `2026-08-13-test-spec-skill-simplification`
- Formal next-stage eligibility: proposal revision only
