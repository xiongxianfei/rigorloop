# Review Resolution: Test-Spec Skill Simplification

## Summary

Closeout status: closed

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`
- Findings resolved: 6
- Unresolved findings: 0
- Current result: proposal revised; independent rereview required

## Resolution overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| `TSSIM-PR1` | accepted | closed | Authoring now ends at `review-required`; peer review owns activation and workflow owns the later settlement gate. |
| `TSSIM-PR2` | accepted | closed | Governed creation now has an authoring-entry-first sequence and exact identical-retry contract. |
| `TSSIM-PR3` | accepted | closed | The skeleton owns headings and insertion positions; smaller assets own repeated body shapes. |
| `TSSIM-PR4` | accepted | closed | Revision now binds prior and new identities, preserves history, stops on active reliance, and requires fresh review. |
| `TSSIM-PR5` | accepted | closed | Stale creation now uses workflow-routed, test-spec-owned bounded abandonment before a new identity starts. |
| `TSSIM-PR6` | accepted | closed | Optional manual verification retains its existing distributed owners with no new contract or asset. |

## Finding details

### proposal-review-r1

#### TSSIM-PR1

Finding ID: TSSIM-PR1
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Close authoring, peer settlement, and workflow settlement ownership.
Chosen action: End `test-spec` authoring at `review-required`, reserve activation for `test-spec-review`, and keep the later implementation settlement gate workflow-owned and non-authoring.
Rationale: Open-ended settlement preparation can cross accepted lifecycle write boundaries.
Required outcome: Define one non-overlapping operation and handoff matrix.
Safe resolution path: Adopt the ownership split recommended by `proposal-review-r1` and prove authoring stop, peer activation, and read-only workflow gate behavior.
Validation target: revised invocation, ownership, expected behavior, scenario, risk, and acceptance sections plus independent proposal rereview.
Validation evidence: `evidence/proposal-revision-r1.md`; revised Invocation and authority model, Authoring/review/workflow ownership matrix, Resource ownership, Expected Behavior Changes, Testing and Verification Strategy, Risks and Mitigations, and Decision Log.

#### TSSIM-PR2

Finding ID: TSSIM-PR2
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Select the governed creation transaction and recovery sequence.
Chosen action: Create the matching `authoring` entry before content mutation and reconcile only the exact change, artifact, path, evidence, and input identity tuple.
Rationale: File and entry writes can be interrupted and must not turn an identical retry into an unrecoverable conflict.
Required outcome: Define exact write order, partial-state reconciliation, collision behavior, and forbidden writes.
Safe resolution path: Adopt the authoring-first identity sequence recommended by `proposal-review-r1` and prove every interruption boundary.
Validation target: revised creation, failure, scenario, rollout, and acceptance sections plus independent proposal rereview.
Validation evidence: `evidence/proposal-revision-r1.md`; revised Governed creation and retry, Static contract scenarios, Rollout and Rollback, Risks and Mitigations, and Decision Log.

#### TSSIM-PR3

Finding ID: TSSIM-PR3
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Close structural ownership and composition across five assets.
Chosen action: Make the skeleton own section order, headings, table headers, and insertion positions while smaller assets own repeated body shapes.
Rationale: The full skeleton and repeated assets currently contain overlapping structural examples.
Required outcome: Define exactly which asset owns section order, headers, repeated body shapes, and creation or revision composition.
Safe resolution path: Adopt the header-versus-body ownership split recommended by `proposal-review-r1` and validate no duplicated structural owner remains.
Validation target: revised structural ownership, scenarios, rollout, and acceptance sections plus independent proposal rereview.
Validation evidence: `evidence/proposal-revision-r1.md`; revised Structural ownership, Static contract scenarios, Rollout and Rollback, Risks and Mitigations, and Decision Log.

### proposal-review-r2

#### TSSIM-PR4

Finding ID: TSSIM-PR4
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Close the governed revision transaction and review-staleness model.
Chosen action: Define revision as a prior-identity-bound authoring transaction that produces a new identity, preserves history, and requires fresh review.
Rationale: Revision is named but lacks a complete state, authority, identity, retry, and reliance contract.
Required outcome: Define legal revision states, write sequence, prior/new identities, fresh review, and active-implementation stop behavior.
Safe resolution path: Adopt the bounded pre-implementation revision transaction recommended by `proposal-review-r2`.
Validation target: revised revision, ownership, scenarios, risks, and acceptance sections plus independent rereview.
Validation evidence: `evidence/proposal-revision-r2.md`; revised Governed test-spec revision, Expected Behavior Changes, Static contract scenarios, Acceptance criteria, Rollout and Rollback, Risks and Mitigations, and Decision Log.

#### TSSIM-PR5

Finding ID: TSSIM-PR5
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Close changed-basis interrupted-authoring recovery.
Chosen action: Report `stale-authoring-attempt`; let workflow authorize and route recovery while only `test-spec` abandons its exact incomplete entry with bounded closeout evidence.
Rationale: An incomplete creation may be neither an identical retry nor a valid revision.
Required outcome: Define stale result, exact closeout owner and write set, and new-identity restart.
Safe resolution path: Use workflow-routed, test-spec-owned bounded abandonment under existing stage-owned authority.
Validation target: revised recovery matrix, ownership, scenarios, risks, rollout, and acceptance sections plus independent rereview.
Validation evidence: `evidence/proposal-revision-r2.md`; revised Stale interrupted authoring, Expected Behavior Changes, Static contract scenarios, Acceptance criteria, Rollout and Rollback, Risks and Mitigations, and Decision Log.

#### TSSIM-PR6

Finding ID: TSSIM-PR6
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Reconcile optional manual verification with existing structural owners.
Chosen action: Preserve optional manual verification through existing proof, test-case, milestone, and skeleton structures and prohibit a new manual-proof contract or asset in this change.
Rationale: The proposal must not imply an unowned repeated structure or introduce a new manual-proof contract accidentally.
Required outcome: Identify current owners and preserve optional Manual QA behavior without a new asset.
Safe resolution path: Retain the proof reference, proof-obligation row, test-case, milestone row, and skeleton responsibilities already approved.
Validation target: revised ownership, non-goals, scenarios, risks, and acceptance sections plus independent rereview.
Validation evidence: `evidence/proposal-revision-r2.md`; revised Non-goals, Optional manual-verification ownership, Static contract scenarios, Acceptance criteria, Risks and Mitigations, and Decision Log.
