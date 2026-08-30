# Review Resolution: Governed Repository CLI Architecture

## Summary

Closeout status: open

Review closeout: proposal-review-r1

- Reviews covered: `proposal-review-r1`
- Findings resolved: 0
- Unresolved findings: 3
- Current result: proposal revision and same-stage rereview are required before specification.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| CLIARCH-PR1 | needs-decision | open | Select a technically provable meaning for mandatory CLI enforcement and CI validation. |
| CLIARCH-PR2 | needs-decision | open | Define the complete durable `docs/changes/` publication boundary or justify a narrower target. |
| CLIARCH-PR3 | needs-decision | open | Compare modular single-file architecture with combined multi-file publication and select or split the investment. |

## Finding Details

### proposal-review-r1

#### CLIARCH-PR1

Finding ID: CLIARCH-PR1
Disposition: needs-decision
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: choose invariant enforcement, non-authoritative provenance, or a separately trusted authorization mechanism.
Chosen action: pending proposal-author decision.
Rationale: equivalent committed bytes do not prove whether the CLI or a direct editor produced them.
Required outcome: enforcement and CI claims are technically provable under the stated local trust model.
Follow-up: revise the proposal and run proposal-review-r2.
Validation target: aligned goals, rollout, risks, test strategy, and decision log with no impossible writer-provenance claim.
Validation evidence: pending proposal revision.

#### CLIARCH-PR2

Finding ID: CLIARCH-PR2
Disposition: needs-decision
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: choose the complete governed change-local publication boundary and its explicit exclusions.
Chosen action: pending proposal-author decision.
Rationale: “supported” files do not preserve the stated universal `docs/changes/` direction.
Required outcome: every current durable file family, transient file family, and read-only operation has a clear applicability treatment.
Follow-up: revise the proposal and run proposal-review-r2.
Validation target: closed applicability table, aligned scope budget, and explicit future-file policy.
Validation evidence: pending proposal revision.

#### CLIARCH-PR3

Finding ID: CLIARCH-PR3
Disposition: needs-decision
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: choose a focused modular-single-file direction or justify the combined multi-file publication direction.
Chosen action: pending proposal-author decision after option comparison.
Rationale: internal modularization and persistence-boundary expansion are independently valuable and independently risky.
Required outcome: the strongest lower-risk option is compared using explicit value and risk criteria before selection.
Follow-up: revise the proposal and run proposal-review-r2.
Validation target: revised options, decision rationale, scope budget, and rollout boundary.
Validation evidence: pending proposal revision.
