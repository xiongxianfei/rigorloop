# Review Resolution: Proposal Skill Simplification

Closeout status: open

Review closeout: proposal-review-r1

- Reviews covered: `proposal-review-r1`
- Findings resolved: 0
- Unresolved findings: 3
- Current result: proposal revision required before specification

## Resolution overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| `PRSIM-PR1` | accepted | open | Separate governed candidate selection from reference-owned authority validation. |
| `PRSIM-PR2` | accepted | open | Define identity-bound create and revise transactions with deterministic retry behavior. |
| `PRSIM-PR3` | accepted | open | Preserve the complete specialized-trigger contract and independent conditional-group applicability. |

## Finding details

### proposal-review-r1

#### PRSIM-PR1

Finding ID: PRSIM-PR1
Disposition: accepted
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Remove circular governed-reference selection without weakening authority validation.
Chosen action: Add a candidate predicate for loading and keep complete authority validation inside the governed reference.
Rationale: The main file cannot require reference-owned validation before deciding to load that reference.
Required outcome: Define candidate evidence, authoritative validation, invalid-candidate stops, and no portable fallback.
Safe resolution path: Adopt the candidate and validation split recommended by `proposal-review-r1`.
Validation target: revised invocation predicates, assemblies, operations, scenarios, risks, and acceptance criteria plus independent rereview.
Validation evidence: pending proposal revision.

#### PRSIM-PR2

Finding ID: PRSIM-PR2
Disposition: accepted
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Make governed creation and revision recoverable after interruption.
Chosen action: Define entry-first identity-bound transactions, allowed partial states, commit points, and idempotent completion.
Rationale: The current operation matrix classifies an entry-only state created by its own transaction as a conflict.
Required outcome: Close create and revise write order, retry identity, partial-state recovery, collision, and concurrency behavior.
Safe resolution path: Adopt the transaction model recommended by `proposal-review-r1`.
Validation target: revised operations, ownership, expected behavior, scenarios, rollout, risks, and acceptance criteria plus independent rereview.
Validation evidence: pending proposal revision.

#### PRSIM-PR3

Finding ID: PRSIM-PR3
Disposition: accepted
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Preserve current scope-budget triggers and close conditional output applicability.
Chosen action: Add `initial_intent_table_context` and restore every current positive `scope_budget_context` trigger.
Rationale: Broad or multi-workstream wording alone omits existing policy, generated-output, lifecycle-family, downstream-artifact, and review-concern triggers.
Required outcome: Define both predicates, their evidence, independent composition, omission rule, and gates-reference loading.
Safe resolution path: Adopt the trigger and structural-applicability model recommended by `proposal-review-r1`.
Validation target: revised invocation predicates, structural asset, semantic preservation, scenarios, risks, and acceptance criteria plus independent rereview.
Validation evidence: pending proposal revision.
