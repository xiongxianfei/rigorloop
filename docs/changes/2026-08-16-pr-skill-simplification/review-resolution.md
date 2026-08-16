# Review Resolution: PR Skill Simplification

Closeout status: closed

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: proposal-review-r3
Review closeout: proposal-review-r4

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`, `proposal-review-r3`, `proposal-review-r4`
- Findings resolved: 7
- Unresolved findings: 0
- Current result: proposal approved for focused specification and bounded architecture assessment

## Resolution overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| `PRSIM-PR1` | accepted | closed | The verified subject and handoff revision are separate, with one closed verify-owned evidence tail. |
| `PRSIM-PR2` | accepted | closed | Reuse is non-mutating and refresh requires explicit field or full-replacement authority. |
| `PRSIM-PR3` | accepted | closed | Remote branches use fail-closed states and PR state is reread after push. |
| `PRSIM-PR4` | accepted | closed | `prepare-only` is read-only and creation intent is separate from existing PR-state authority. |
| `PRSIM-PR5` | accepted | closed | Readiness binds an exact verified base/head pair and directional branch relations. |
| `PRSIM-PR6` | accepted | closed | First-version refresh is limited to title or authorized whole-body replacement. |
| `PRSIM-PR7` | accepted | closed | `verify` owns the normalized basis through its existing result/report contract and same-slice compatibility proof. |

## Finding details

### proposal-review-r1

#### PRSIM-PR1

Finding ID: PRSIM-PR1
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Reconcile exact verified revision binding with durable final-verification recording.
Chosen action: Represent the verified subject and handoff revisions separately and permit only one closed verify-owned evidence tail.
Rationale: Final verification must be recorded without making its own evidence commit appear unverified.
Required outcome: Define allowed tail identities, invalidating changes, validation, and final remote and PR head binding.
Safe resolution path: Amend the sequence, result model, scenarios, risks, and acceptance criteria.
Validation target: revised proposal and independent rereview.
Validation evidence: `docs/changes/2026-08-16-pr-skill-simplification/evidence/proposal-revision-r1.md` and subsequent `proposal-review-r2`.

#### PRSIM-PR2

Finding ID: PRSIM-PR2
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Close authority and ownership semantics for modifying an existing PR title or body.
Chosen action: Make reuse non-mutating, require explicit refresh authority, and fail closed on unknown content ownership.
Rationale: Matching PR identity does not grant permission to overwrite externally edited context.
Required outcome: Define refresh authority, content comparison, draft preservation, and forbidden replacement behavior.
Safe resolution path: Amend operations, authority, scenarios, risks, and acceptance without hidden markers.
Validation target: revised proposal and independent rereview.
Validation evidence: `docs/changes/2026-08-16-pr-skill-simplification/evidence/proposal-revision-r1.md` and subsequent `proposal-review-r2`.

#### PRSIM-PR3

Finding ID: PRSIM-PR3
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Close remote branch divergence, race, and duplicate-PR behavior.
Chosen action: Add remote-branch states, prohibit force operations, and reread matching PR state after push.
Rationale: Pre-push PR state may be stale, and divergence must not trigger destructive push behavior.
Required outcome: Define branch states, permitted push, post-push reclassification, concurrency, and stops.
Safe resolution path: Amend sequence, matrices, retry scenarios, risks, and acceptance criteria.
Validation target: revised proposal and independent rereview.
Validation evidence: `docs/changes/2026-08-16-pr-skill-simplification/evidence/proposal-revision-r1.md` and subsequent `proposal-review-r2`.

### proposal-review-r2

#### PRSIM-PR4

Finding ID: PRSIM-PR4
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Close submission intent, external mutation, and existing PR-state behavior.
Chosen action: Make `prepare-only` read-only and separate creation intent from explicit existing PR-state authority.
Rationale: Creation intent does not imply push, refresh, publication, or draft-conversion permission.
Required outcome: Define every intent's push, creation, refresh, and state-transition behavior.
Safe resolution path: Add authority axes, side-effect matrix, result fields, scenarios, and acceptance criteria.
Validation target: revised proposal and independent rereview.
Validation evidence: `docs/changes/2026-08-16-pr-skill-simplification/evidence/proposal-revision-r2.md` and subsequent `proposal-review-r3`.

#### PRSIM-PR5

Finding ID: PRSIM-PR5
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Bind verification to the exact base and eliminate directional branch-state ambiguity.
Chosen action: Record the verified base or merge base, recheck it, and use directional ancestry names.
Rationale: An unchanged head does not preserve readiness when the effective PR base changes.
Required outcome: Define the verified tuple, staleness, directional relations, and external-success versus readiness results.
Safe resolution path: Amend identity, sequence, states, scenarios, risks, and acceptance criteria.
Validation target: revised proposal and independent rereview.
Validation evidence: `docs/changes/2026-08-16-pr-skill-simplification/evidence/proposal-revision-r2.md` and subsequent `proposal-review-r3`.

#### PRSIM-PR6

Finding ID: PRSIM-PR6
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Remove unsafe section-level body rewriting or define a complete ownership contract.
Chosen action: Limit refresh to title or explicitly authorized whole-body replacement.
Rationale: Unmanaged section mutation cannot preserve user-authored bytes reliably.
Required outcome: Remove section refresh, preserve body bytes by default, and defer managed sections.
Safe resolution path: Amend refresh authority, operations, architecture, scenarios, risks, and acceptance criteria.
Validation target: revised proposal and independent rereview.
Validation evidence: `docs/changes/2026-08-16-pr-skill-simplification/evidence/proposal-revision-r2.md` and subsequent `proposal-review-r3`.

### proposal-review-r3

#### PRSIM-PR7

Finding ID: PRSIM-PR7
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Close where the exact verified repository, remote, base, merge-base, head, and subject identities are durably authored.
Chosen action: Amend the existing verify evidence contract in the same slice without changing verify ownership of `branch-ready`.
Rationale: Current verify skill text and historical reports do not guarantee one normalized exact base identity that `pr` can safely consume.
Required outcome: Put the verify-evidence amendment in scope, name verify as owner, define legacy compatibility, and stop readiness on missing or ambiguous basis.
Safe resolution path: Update scope, architecture, rollout, preservation inventories, scenarios, and acceptance before rereview.
Validation target: revised proposal and independent proposal rereview.
Validation evidence: `docs/changes/2026-08-16-pr-skill-simplification/evidence/proposal-revision-r3.md`; independent rereview remains pending.

### proposal-review-r4

No material findings. The approving clean rereview confirms that the normalized verify-basis amendment closes `PRSIM-PR7` within the existing evidence owner and that all prior external-action findings remain resolved.
