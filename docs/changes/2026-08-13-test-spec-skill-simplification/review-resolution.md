# Review Resolution: Test-Spec Skill Simplification

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
| `TSSIM-PR1` | needs-decision | open | Proposal author must separate authoring, review settlement, and workflow settlement ownership. |
| `TSSIM-PR2` | needs-decision | open | Proposal author must define interruption-safe creation and identical retry. |
| `TSSIM-PR3` | needs-decision | open | Proposal author must close full-skeleton and repeated-asset composition ownership. |

## Finding details

### proposal-review-r1

#### TSSIM-PR1

Finding ID: TSSIM-PR1
Disposition: needs-decision
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Close authoring, peer settlement, and workflow settlement ownership.
Chosen action: pending proposal revision
Rationale: Open-ended settlement preparation can cross accepted lifecycle write boundaries.
Required outcome: Define one non-overlapping operation and handoff matrix.
Safe resolution path: Adopt the ownership split recommended by `proposal-review-r1` and prove authoring stop, peer activation, and read-only workflow gate behavior.
Validation target: revised invocation, ownership, expected behavior, scenario, risk, and acceptance sections plus independent proposal rereview.
Validation evidence: pending

#### TSSIM-PR2

Finding ID: TSSIM-PR2
Disposition: needs-decision
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Select the governed creation transaction and recovery sequence.
Chosen action: pending proposal revision
Rationale: File and entry writes can be interrupted and must not turn an identical retry into an unrecoverable conflict.
Required outcome: Define exact write order, partial-state reconciliation, collision behavior, and forbidden writes.
Safe resolution path: Adopt the authoring-first identity sequence recommended by `proposal-review-r1` and prove every interruption boundary.
Validation target: revised creation, failure, scenario, rollout, and acceptance sections plus independent proposal rereview.
Validation evidence: pending

#### TSSIM-PR3

Finding ID: TSSIM-PR3
Disposition: needs-decision
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Close structural ownership and composition across five assets.
Chosen action: pending proposal revision
Rationale: The full skeleton and repeated assets currently contain overlapping structural examples.
Required outcome: Define exactly which asset owns section order, headers, repeated body shapes, and creation or revision composition.
Safe resolution path: Adopt the header-versus-body ownership split recommended by `proposal-review-r1` and validate no duplicated structural owner remains.
Validation target: revised structural ownership, scenarios, rollout, and acceptance sections plus independent proposal rereview.
Validation evidence: pending
