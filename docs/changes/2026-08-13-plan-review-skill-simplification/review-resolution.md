# Review Resolution: Plan-Review Skill Simplification

## Summary

Closeout status: open

Review closeout: proposal-review-r1

- Reviews covered: `proposal-review-r1`
- Findings resolved: 0
- Unresolved findings: 3
- Current result: proposal revision required

## Resolution overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| `PRVSIM-PR1` | needs-decision | open | Proposal author must separate candidate-trigger loading from validated governed authority. |
| `PRVSIM-PR2` | needs-decision | open | Proposal author must close semantic status, transaction result, recording, and handoff combinations. |
| `PRVSIM-PR3` | needs-decision | open | Proposal author must add mandatory durable-recording fields to the result-asset model. |

## Finding details

### proposal-review-r1

#### PRVSIM-PR1

Finding ID: PRVSIM-PR1
Disposition: needs-decision
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Close the resource-trigger and authority-validation sequence.
Chosen action: pending proposal revision
Rationale: Exact governed validation cannot be both the load predicate and the procedure owned by the loaded reference.
Required outcome: Define candidate-context loading followed by fail-closed governed validation without portable fallback.
Safe resolution path: Adopt the candidate-trigger sequence recommended by `proposal-review-r1` and prove valid, stale, absent, ambiguous, and late-discovery scenarios.
Validation target: revised invocation classification, profile, reference ownership, stop, and scenario sections plus independent proposal rereview.
Validation evidence: pending

#### PRVSIM-PR2

Finding ID: PRVSIM-PR2
Disposition: needs-decision
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Close the review-status, transaction-result, settlement, and handoff matrix.
Chosen action: pending proposal revision
Rationale: `approved`, `initialization-required`, active settlement, and test-spec eligibility are distinct claims with different owners.
Required outcome: Define every valid initial-review and settlement-retry outcome, write set, recording effect, and next action.
Safe resolution path: Adopt the closed matrix recommended by `proposal-review-r1`, including no duplicate record or semantic rereview during retry.
Validation target: revised operation, expected behavior, asset, acceptance, and static scenario sections plus independent proposal rereview.
Validation evidence: pending

#### PRVSIM-PR3

Finding ID: PRVSIM-PR3
Disposition: needs-decision
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Close formal recording structure in the result asset.
Chosen action: pending proposal revision
Rationale: Every explicit plan review requires recording paths or a blocked recording result, including portable review.
Required outcome: Add a durable-recording group and exact applicability, omission, blocked-data, and placeholder behavior.
Safe resolution path: Adopt the five-group asset model recommended by `proposal-review-r1` and align it with existing review-family validation.
Validation target: revised structural asset, result, validator, and scenario sections plus independent proposal rereview.
Validation evidence: pending
