# Review Resolution: PR Skill Simplification

Closeout status: open

## Resolution overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| `PRSIM-PR1` | accepted | open | Revise the verification binding to distinguish the tested subject from a bounded verify-owned handoff tail. |
| `PRSIM-PR2` | accepted | open | Separate idempotent reuse from explicitly authorized refresh and protect unknown existing content ownership. |
| `PRSIM-PR3` | accepted | open | Add remote-branch states and post-push matching-PR reconciliation without force operations. |

## Finding details

### proposal-review-r1

#### PRSIM-PR1

Finding ID: PRSIM-PR1
Disposition: accepted
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Reconcile exact verified revision binding with the required durable final-verification evidence commit.
Chosen action: Represent the verified subject and final handoff revisions separately and permit only a closed verify-owned evidence tail.
Rationale: Final verification must be recorded durably without making its own valid evidence commit appear unverified.
Required outcome: Define the allowed tail, identities, invalidating changes, tail validation, and final remote and PR head binding.
Safe resolution path: Amend the proposal's sequence, result model, scenarios, risks, and acceptance criteria, then obtain independent rereview.
Validation target: revised proposal and approving proposal rereview.
Validation evidence: pending proposal revision and rereview.

#### PRSIM-PR2

Finding ID: PRSIM-PR2
Disposition: accepted
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Close authority and ownership semantics for modifying an existing PR title or body.
Chosen action: Make reuse non-mutating, require explicit current refresh authority, and fail closed on unknown or mixed content ownership.
Rationale: Matching PR identity does not itself grant permission to overwrite externally edited reviewer context.
Required outcome: Define refresh authority, content comparison, draft preservation, mixed ownership, and forbidden replacement behavior.
Safe resolution path: Amend the operation matrix, authority rules, scenarios, risks, and acceptance criteria without adding a hidden marker system.
Validation target: revised proposal and approving proposal rereview.
Validation evidence: pending proposal revision and rereview.

#### PRSIM-PR3

Finding ID: PRSIM-PR3
Disposition: accepted
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Close remote branch divergence, race, and duplicate-PR behavior.
Chosen action: Add a remote-branch state vocabulary, prohibit force operations, and reread matching PR state after push.
Rationale: A pre-push PR snapshot is stale by the time external mutation begins, and divergence must not be resolved by destructive push behavior.
Required outcome: Define every remote branch state, permitted push, post-push reclassification, concurrent creation reconciliation, and stop result.
Safe resolution path: Amend the sequence, state matrices, retry scenarios, risks, and acceptance criteria, then obtain independent rereview.
Validation target: revised proposal and approving proposal rereview.
Validation evidence: pending proposal revision and rereview.
