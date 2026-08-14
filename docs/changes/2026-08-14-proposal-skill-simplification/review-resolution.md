# Review Resolution: Proposal Skill Simplification

Closeout status: open

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: proposal-review-r3
Review closeout: proposal-review-r4
Review closeout: spec-review-r1
Review closeout: plan-review-r1
Review closeout: test-spec-review-r1
Review closeout: code-review-M1-r1

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`, `proposal-review-r3`, `proposal-review-r4`, `spec-review-r1`, `plan-review-r1`, `test-spec-review-r1`, `code-review-M1-r1`
- Findings resolved: 7
- Unresolved findings: 1
- Current result: M1 code review requested one mechanically eligible correction before rereview

### test-spec-review-r1

Review closeout: test-spec-review-r1

No material findings; no resolution entry required. The formal review approved the complete proof map and implementation handoff, and bounded automation stopped at its target without starting implementation.

### plan-review-r1

No material findings. The clean review approved `docs/plans/2026-08-14-proposal-skill-simplification.md` at commit `0f1a25e8`; `planned_work` was initialized from that exact basis, and the identical settlement retry activated the plan without semantic rereview.

### spec-review-r1

No material findings. The clean review approved `specs/proposal-skill-simplification.md` at commit `494d1811` and permitted workflow-owned architecture assessment.

## Resolution overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| `PRSIM-PR1` | accepted | closed | Governed candidate selection is separate from reference-owned authority validation. |
| `PRSIM-PR2` | accepted | closed | Creation and revision now use identity-bound entry-first transactions with deterministic retry behavior. |
| `PRSIM-PR3` | accepted | closed | The complete specialized-trigger contract and independent conditional-group applicability are explicit. |
| `PRSIM-R2-PR1` | accepted | closed | Portable file-based operations are separate from governed entry-based operations. |
| `PRSIM-R2-PR2` | accepted | closed | Workflow-owned stale-attempt reconciliation is bounded and adds no persistent state. |
| `PRSIM-R2-PR3` | accepted | closed | Every specialized predicate has an explicit structural destination. |
| `PRSIM-R3-PR1` | accepted | closed | Workflow authorizes recovery without mutating proposal state; proposal executes only the exact authorized reset of its own incomplete state. |
| `PRSIM-M1-CR1` | accepted | open | Split two composite enum literal rows into one independently classified row per exact consumed value. |

## Finding details

### code-review-M1-r1

#### PRSIM-M1-CR1

Finding ID: PRSIM-M1-CR1

Disposition: accepted

Status: open

Owner: implement M1

Owning stage: implement

Decision owner: none; deterministic correction

Decision needed: none

Chosen action: Split the composite initial-goal and scope-budget enum rows into twelve exact literal rows and update the evidence count.

Rationale: Exact compatibility dependencies must be independently classified; a comma-joined value that does not occur in the source is not an exact literal.

Required outcome: Every consumed enum value has its own literal ID, exact value, consumer set, classification, semantics, disposition, and replacement field.

Safe resolution path: Apply the reviewer-declared mechanical change only to the literal ledger and M1 evidence, rerun CMD1 and named repository checks, then perform a context-reset rereview.

Validation target: literal count increases from 29 to 39, CMD1 passes, and reviewer confirms the two composite strings are absent.

Validation evidence: pending correction and rereview.

### proposal-review-r4

No material findings. The clean rereview approved the proposal at commit `f3313ead` and confirmed closure of `PRSIM-R3-PR1` without changing stage-owned mutation boundaries.

### proposal-review-r1

#### PRSIM-PR1

Finding ID: PRSIM-PR1
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Remove circular governed-reference selection without weakening authority validation.
Chosen action: Add a candidate predicate for loading and keep complete authority validation inside the governed reference.
Rationale: The main file cannot require reference-owned validation before deciding to load that reference.
Required outcome: Define candidate evidence, authoritative validation, invalid-candidate stops, and no portable fallback.
Safe resolution path: Adopt the candidate and validation split recommended by `proposal-review-r1`.
Validation target: revised invocation predicates, assemblies, operations, scenarios, risks, and acceptance criteria plus independent rereview.
Validation evidence: `evidence/proposal-revision-r1.md`; revised Invocation predicates, Loaded assemblies, Expected Behavior Changes, Proposal acceptance criteria, Risks and Mitigations, and Decision Log sections.

#### PRSIM-PR2

Finding ID: PRSIM-PR2
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Make governed creation and revision recoverable after interruption.
Chosen action: Define entry-first identity-bound transactions, allowed partial states, commit points, and idempotent completion.
Rationale: The current operation matrix classifies an entry-only state created by its own transaction as a conflict.
Required outcome: Close create and revise write order, retry identity, partial-state recovery, collision, and concurrency behavior.
Safe resolution path: Adopt the transaction model recommended by `proposal-review-r1`.
Validation target: revised operations, ownership, expected behavior, scenarios, rollout, risks, and acceptance criteria plus independent rereview.
Validation evidence: `evidence/proposal-revision-r1.md`; revised Portable and governed operations, Governed creation transaction, Governed revision transaction, Expected Behavior Changes, Testing and Verification Strategy, Proposal acceptance criteria, Risks and Mitigations, and Decision Log sections.

#### PRSIM-PR3

Finding ID: PRSIM-PR3
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Preserve current scope-budget triggers and close conditional output applicability.
Chosen action: Add `initial_intent_table_context` and restore every current positive `scope_budget_context` trigger.
Rationale: Broad or multi-workstream wording alone omits existing policy, generated-output, lifecycle-family, downstream-artifact, and review-concern triggers.
Required outcome: Define both predicates, their evidence, independent composition, omission rule, and gates-reference loading.
Safe resolution path: Adopt the trigger and structural-applicability model recommended by `proposal-review-r1`.
Validation target: revised invocation predicates, structural asset, semantic preservation, scenarios, risks, and acceptance criteria plus independent rereview.
Validation evidence: `evidence/proposal-revision-r1.md`; revised Invocation predicates, Structural asset, Expected Behavior Changes, Testing and Verification Strategy, Proposal acceptance criteria, Risks and Mitigations, and Decision Log sections.

### proposal-review-r2

#### PRSIM-R2-PR1

Finding ID: PRSIM-R2-PR1
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Separate portable file-based operation resolution from governed lifecycle entry resolution.
Chosen action: Add independent portable and governed matrices and retain no-fallback behavior for failed governed candidates.
Rationale: Portable revision cannot require a proposal entry that portable authoring does not own.
Required outcome: Close file-state behavior for portable create and revise and entry-plus-identity behavior for governed operations.
Safe resolution path: Adopt the operation split recommended by `proposal-review-r2`.
Validation target: revised operation classification, expected behavior, fixtures, risks, and acceptance criteria plus independent rereview.
Validation evidence: `evidence/proposal-revision-r2.md`; revised Portable and governed operations, Expected Behavior Changes, Testing and Verification Strategy, Proposal acceptance criteria, Risks and Mitigations, and Decision Log sections.

#### PRSIM-R2-PR2

Finding ID: PRSIM-R2-PR2
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Provide bounded recovery for stale governed authoring attempts.
Chosen action: Add `authoring-reset-required` and assign exact reset or abandonment to workflow under no-reliance prerequisites.
Rationale: A stale durable `authoring` entry can prevent both retry and a new operation.
Required outcome: Define detection, no-mutation behavior, workflow reset prerequisites, bounded write set, and new-attempt identity.
Safe resolution path: Adopt the recovery ownership recommended by `proposal-review-r2` without adding persistent reset state.
Validation target: revised transaction recovery, architecture impact, expected behavior, fixtures, risks, and acceptance criteria plus independent rereview.
Validation evidence: `evidence/proposal-revision-r2.md`; revised Stale governed authoring attempts, Architecture Impact, Expected Behavior Changes, Testing and Verification Strategy, Proposal acceptance criteria, Risks and Mitigations, and Decision Log sections.

#### PRSIM-R2-PR3

Finding ID: PRSIM-R2-PR3
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Map all specialized predicates to the sole structural asset.
Chosen action: Add vision-exception and standing-artifact groups and make all four groups independently composable.
Rationale: A sole structural owner cannot leave two triggered result shapes ad hoc.
Required outcome: Define each group's destination, structural fields, composition, omission, and blocked-data behavior.
Safe resolution path: Extend the existing skeleton as recommended by `proposal-review-r2`; do not add assets.
Validation target: revised structural ownership, expected behavior, fixtures, risks, and acceptance criteria plus independent rereview.
Validation evidence: `evidence/proposal-revision-r2.md`; revised Structural asset, Expected Behavior Changes, Testing and Verification Strategy, Proposal acceptance criteria, Risks and Mitigations, and Decision Log sections.

### proposal-review-r3

#### PRSIM-R3-PR1

Finding ID: PRSIM-R3-PR1
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Align stale-attempt reset writes with existing stage-owned artifact-state ownership.
Chosen action: Keep workflow as validation, authorization, and routing owner while proposal executes the bounded reset of its own exact partial state.
Rationale: Current workflow procedure must preserve `artifact_states` and stage-owned evidence, so direct workflow reset would require architecture and contract changes.
Required outcome: Define the authorization/reset handshake, bound proposal writes, update architecture rationale and scope, and add acceptance criteria.
Safe resolution path: Adopt the ownership-preserving split recommended by `proposal-review-r3`.
Validation target: revised stale recovery, resource ownership, architecture impact, tests, acceptance criteria, risks, scope budget, and decision log plus independent rereview.
Validation evidence: `evidence/proposal-revision-r3.md`; revised Stale governed authoring attempts, Resource ownership, Expected Behavior Changes, Architecture Impact, Testing and Verification Strategy, Proposal acceptance criteria, Risks and Mitigations, Scope budget, and Decision Log sections.
