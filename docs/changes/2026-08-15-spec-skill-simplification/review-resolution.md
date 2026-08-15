# Review Resolution: Spec Skill Simplification

Closeout status: closed

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`, `proposal-review-r3`, `spec-review-r1`, `plan-review-r1`
- Findings resolved: 5
- Unresolved findings: 0
- Current result: proposal-review R3 approved the revised proposal with no material findings

## Resolution overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| `SPSIM-PR1` | accepted | closed | Replaced workflow reset authorization with a bounded spec-owned same-entry restart contract. |
| `SPSIM-PR2` | accepted | closed | Added one conditional skeleton insertion point and a closed boundary-block applicability contract. |
| `SPSIM-R2-PR1` | accepted | closed | Added tri-state governed-signal classification with no invalid-signal portable fallback. |
| `SPSIM-R2-PR2` | accepted | closed | Required explicit restart authority and deterministic preservation of matching nonempty partial content. |
| `SPSIM-R2-PR3` | accepted | closed | Closed boundary-block transition, removal, malformed-state, and grandfathered-adoption behavior. |

## Finding details

### proposal-review-r1

Review closeout: proposal-review-r1

#### SPSIM-PR1

Finding ID: SPSIM-PR1
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Replace the unowned reset-authorization assumption with an executable recovery contract.
Chosen action: Use a spec-owned `restart-stale-authoring` operation over the same incomplete entry and keep workflow limited to detection and routing.
Rationale: Proposal-specific reset authorization and test-spec-specific same-entry restart do not automatically grant a recovery mechanism to `spec`.
Required outcome: Define exact owner, authority, operation, identity, partial-content treatment, permitted writes, resulting state, and architecture effect.
Safe resolution path: Adopt the same-entry restart recommended by `proposal-review-r1` or explicitly broaden the governing workflow contract with architecture reassessment.
Validation target: revised recovery, ownership, architecture, scenarios, risks, and acceptance criteria plus independent rereview.
Validation evidence: `evidence/proposal-revision-r1.md`; revised sections `Same-entry stale-authoring restart`, `Ownership model`, `Validation and acceptance boundary`, `Proposal acceptance criteria`, `Architecture assessment`, `Testing and Verification Strategy`, and `Risks and Mitigations`.

#### SPSIM-PR2

Finding ID: SPSIM-PR2
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Close the interface between ordinary skeleton structure and the formal boundary-record block.
Chosen action: Add one conditional insertion point while preserving the feature-authoring reference as the block owner.
Rationale: Initial resource loading does not determine output applicability or the block's location in the ordinary spec structure.
Required outcome: Define exact insertion location, applicability, omission, unresolved-data behavior, and non-duplication.
Safe resolution path: Adopt the conditional insertion point and applicability matrix recommended by `proposal-review-r1`.
Validation target: revised structural ownership, behavior, missing-resource rules, scenarios, risks, and acceptance criteria plus independent rereview.
Validation evidence: `evidence/proposal-revision-r1.md`; revised sections `Structural composition and boundary-block applicability`, `Ownership model`, `Validation and acceptance boundary`, `Proposal acceptance criteria`, `Expected Behavior Changes`, `Testing and Verification Strategy`, and `Risks and Mitigations`.

### proposal-review-r2

Review closeout: proposal-review-r2

#### SPSIM-R2-PR1

Finding ID: SPSIM-R2-PR1
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Prevent malformed, duplicated, stale, escaped, missing-root, or conflicting governed indicators from falling through to portable authoring.
Chosen action: Add a closed tri-state governed-signal classifier and permit portable authoring only for `no-governed-signal`.
Rationale: Any structured ownership indicator is an attempted governed claim even when invalid and must fail closed.
Required outcome: Classify absent, single-candidate, and invalid-or-ambiguous signal states and require all present identities to resolve to the same change.
Safe resolution path: Adopt the round-2 tri-state classifier and explicit no-fallback rules.
Validation target: revised classification, profile table, failure behavior, scenarios, risks, and acceptance criteria plus rereview.
Validation evidence: `evidence/proposal-revision-r2.md`; revised sections `Invocation profiles and resource loading`, `Ownership model`, `Required-resource failure behavior`, `Validation and acceptance boundary`, `Proposal acceptance criteria`, `Expected Behavior Changes`, `Testing and Verification Strategy`, and `Risks and Mitigations`.

#### SPSIM-R2-PR2

Finding ID: SPSIM-R2-PR2
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Separate stale detection from authorized restart and make partial-content handling deterministic.
Chosen action: Require an explicit user request or same-change workflow handoff and preserve every matching nonempty partial file byte-for-byte before replacement.
Rationale: Detection alone cannot authorize destructive replacement, and subjective evidentiary-value judgments cannot protect user-authored bytes consistently.
Required outcome: Define restart authority, evidence fields, partial-content states, write set, stops, and final `authoring` state.
Safe resolution path: Adopt the round-2 restart authorization and content-disposition matrices using existing authoring evidence.
Validation target: revised recovery, ownership, architecture, scenarios, risks, and acceptance criteria plus rereview.
Validation evidence: `evidence/proposal-revision-r2.md`; revised sections `Same-entry stale-authoring restart`, `Ownership model`, `Validation and acceptance boundary`, `Proposal acceptance criteria`, `Architecture assessment`, `Architecture Impact`, `Testing and Verification Strategy`, `Risks and Mitigations`, and `Open Questions`.

#### SPSIM-R2-PR3

Finding ID: SPSIM-R2-PR3
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Make boundary-block presence, applicability, removal, malformed structure, and grandfathered structural adoption exhaustive.
Chosen action: Add closed block-state and anchor-state values, preserve complete blocks absent explicit deactivation, and require valid anchors or an authorized full rewrite for adoption.
Rationale: Resource loading, current block state, applicability, revision class, and structural anchors are independent inputs and cannot be collapsed into overlapping rows.
Required outcome: Define one result for every state combination and fail closed on partial, duplicated, misplaced, or unresolved structure.
Safe resolution path: Adopt the round-2 transition and grandfathered-adoption matrix while retaining current structural owners.
Validation target: revised composition, compatibility, scenarios, risks, and acceptance criteria plus rereview.
Validation evidence: `evidence/proposal-revision-r2.md`; revised sections `Structural composition and boundary-block applicability`, `Validation and acceptance boundary`, `Proposal acceptance criteria`, `Expected Behavior Changes`, `Testing and Verification Strategy`, and `Risks and Mitigations`.

### proposal-review-r3

Review closeout: proposal-review-r3

No material findings; no resolution entry required. The same-stage proposal-review rerun approved the revised proposal and confirmed that all findings through `proposal-review-r2` are closed.

### spec-review-r1

Review closeout: spec-review-r1

No material findings; no resolution entry required. The formal spec review approved the contract and routed the change to bounded architecture assessment.

### plan-review-r1

Review closeout: plan-review-r1

No material findings; no resolution entry required. The formal plan review approved the stable execution plan, and the identity-bound initialization and settlement retry activated the exact reviewed revision.
