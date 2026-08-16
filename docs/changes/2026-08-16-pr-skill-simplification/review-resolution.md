# Review Resolution: PR Skill Simplification

Closeout status: open

Review closeout: proposal-review-r1

## Resolution overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| `PRSIM-PR1` | accepted | closed | The verified subject and handoff revision are separate, with one closed verify-owned evidence tail. |
| `PRSIM-PR2` | accepted | closed | Reuse is non-mutating and refresh requires explicit field or full-replacement authority. |
| `PRSIM-PR3` | accepted | closed | Remote branches use fail-closed states and PR state is reread after push. |
| `PRSIM-PR4` | accepted | open | Close submission-intent side effects and existing PR-state transition authority. |
| `PRSIM-PR5` | accepted | open | Bind readiness to an exact verified base/head pair and directional branch relations. |
| `PRSIM-PR6` | accepted | open | Remove unmanaged Markdown section refresh from the first version. |

## Finding details

### proposal-review-r1

#### PRSIM-PR1

Finding ID: PRSIM-PR1
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Reconcile exact verified revision binding with the required durable final-verification evidence commit.
Chosen action: Represent the verified subject and final handoff revisions separately and permit only a closed verify-owned evidence tail.
Rationale: Final verification must be recorded durably without making its own valid evidence commit appear unverified.
Required outcome: Define the allowed tail, identities, invalidating changes, tail validation, and final remote and PR head binding.
Safe resolution path: Amend the proposal's sequence, result model, scenarios, risks, and acceptance criteria, then obtain independent rereview.
Validation target: revised proposal and approving proposal rereview.
Validation evidence: `docs/changes/2026-08-16-pr-skill-simplification/evidence/proposal-revision-r1.md`; independent rereview remains pending.

### proposal-review-r2

#### PRSIM-PR4

Finding ID: PRSIM-PR4
Disposition: accepted
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Close the cross-product of submission intent, external mutation, and existing PR draft/open state.
Chosen action: Make `prepare-only` externally read-only and separate creation intent from explicit existing-PR state-transition authority.
Rationale: Creation intent does not imply permission to push, refresh, publish a draft, or convert an open PR.
Required outcome: Define push, creation, refresh, and state-transition behavior for every submission intent and existing state.
Safe resolution path: Add independent state-transition authority, a closed side-effect matrix, separate requested and actual result fields, scenarios, and acceptance criteria.
Validation target: revised proposal and independent proposal rereview.
Validation evidence: pending proposal revision and rereview.

#### PRSIM-PR5

Finding ID: PRSIM-PR5
Disposition: accepted
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Bind verification to the exact base as well as the head and eliminate directional ambiguity in remote branch state.
Chosen action: Record the verified base or merge-base identity, recheck it before mutation and after read-back, and use directional ancestry names.
Rationale: An unchanged head does not preserve readiness when the effective PR base changes.
Required outcome: Define the verified base/head tuple, base staleness behavior, directional branch relations, and external-success versus readiness results.
Safe resolution path: Amend the operation identity, sequence, branch-state matrix, scenarios, risks, and acceptance criteria.
Validation target: revised proposal and independent proposal rereview.
Validation evidence: pending proposal revision and rereview.

#### PRSIM-PR6

Finding ID: PRSIM-PR6
Disposition: accepted
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Remove unsafe section-level body rewriting or define a complete ownership and parser contract.
Chosen action: Limit first-version refresh to closed host-native scalar fields and explicitly authorized whole-body replacement.
Rationale: Section mutation without markers, provenance, and a code-fence-aware parser cannot preserve user-authored bytes reliably.
Required outcome: Remove section refresh, preserve existing body bytes by default, and route managed-section behavior to a separate approved contract.
Safe resolution path: Amend refresh authority, the operation matrix, architecture boundary, scenarios, risks, and acceptance criteria.
Validation target: revised proposal and independent proposal rereview.
Validation evidence: pending proposal revision and rereview.

#### PRSIM-PR2

Finding ID: PRSIM-PR2
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Close authority and ownership semantics for modifying an existing PR title or body.
Chosen action: Make reuse non-mutating, require explicit current refresh authority, and fail closed on unknown or mixed content ownership.
Rationale: Matching PR identity does not itself grant permission to overwrite externally edited reviewer context.
Required outcome: Define refresh authority, content comparison, draft preservation, mixed ownership, and forbidden replacement behavior.
Safe resolution path: Amend the operation matrix, authority rules, scenarios, risks, and acceptance criteria without adding a hidden marker system.
Validation target: revised proposal and approving proposal rereview.
Validation evidence: `docs/changes/2026-08-16-pr-skill-simplification/evidence/proposal-revision-r1.md`; independent rereview remains pending.

#### PRSIM-PR3

Finding ID: PRSIM-PR3
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Close remote branch divergence, race, and duplicate-PR behavior.
Chosen action: Add a remote-branch state vocabulary, prohibit force operations, and reread matching PR state after push.
Rationale: A pre-push PR snapshot is stale by the time external mutation begins, and divergence must not be resolved by destructive push behavior.
Required outcome: Define every remote branch state, permitted push, post-push reclassification, concurrent creation reconciliation, and stop result.
Safe resolution path: Amend the sequence, state matrices, retry scenarios, risks, and acceptance criteria, then obtain independent rereview.
Validation target: revised proposal and approving proposal rereview.
Validation evidence: `docs/changes/2026-08-16-pr-skill-simplification/evidence/proposal-revision-r1.md`; independent rereview remains pending.
