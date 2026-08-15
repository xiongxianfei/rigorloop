# Review Resolution: Spec Skill Simplification

Closeout status: closed

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`, `proposal-review-r3`, `spec-review-r1`, `plan-review-r1`, `test-spec-review-r1`, `code-review-M1-r1`, `code-review-M1-r2`, `code-review-M2-r1`, `code-review-M2-r2`, `code-review-M3-r1`, `code-review-final-r1`
- Findings resolved: 7
- Unresolved findings: 0
- Current result: final holistic code-review R1 is clean and approved explanation

## Resolution overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| `SPSIM-PR1` | accepted | closed | Replaced workflow reset authorization with a bounded spec-owned same-entry restart contract. |
| `SPSIM-PR2` | accepted | closed | Added one conditional skeleton insertion point and a closed boundary-block applicability contract. |
| `SPSIM-R2-PR1` | accepted | closed | Added tri-state governed-signal classification with no invalid-signal portable fallback. |
| `SPSIM-R2-PR2` | accepted | closed | Required explicit restart authority and deterministic preservation of matching nonempty partial content. |
| `SPSIM-R2-PR3` | accepted | closed | Closed boundary-block transition, removal, malformed-state, and grandfathered-adoption behavior. |
| `SPSIM-M1-CR1` | accepted | closed | Completed one-owner semantic destinations and exact skeleton-heading classifications. |
| `SPSIM-M2-CR1` | accepted | closed | Made every governed transaction identity and preservation boundary explicit. |
| `SPSIM-M2-CR2` | accepted | closed | Restored the incomplete retained-inline semantic rules compactly. |

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

### test-spec-review-r1

Review closeout: test-spec-review-r1

No material findings; no resolution entry required. The formal test-spec review approved the proof map and established implementation handoff eligibility without starting implementation.

### code-review-M1-r1

Review closeout: code-review-M1-r1

#### SPSIM-M1-CR1

Finding ID: SPSIM-M1-CR1
Disposition: accepted
Status: closed
Owner: implementation author
Owning stage: implement M1
Decision owner: none
Decision needed: none; the accepted correction is deterministic under R57 and R59.
Chosen action: Split the composite semantic ownership and classify every remaining exact skeleton heading.
Rationale: The inventories must be exhaustive and independently reviewable before canonical skill prose moves.
Required outcome: One destination per semantic rule cluster and one classification per exact consumed skeleton heading.
Safe resolution path: Apply the reviewer-declared mechanical correction only to the three affected M1 evidence files, rerun named validation, and return M1 for rereview.
Validation target: CMD1, documentation prose validation, change metadata validation, and `git diff --check`.
Validation evidence: `evidence/m1-preservation-inventories.md`; corrected ledgers; CMD1 passed with 28 rules, 50 literals, and 34 scenarios; `reviews/code-review-m1-r2.md`.

### code-review-M1-r2

Review closeout: code-review-M1-r2

No material findings; no resolution entry required. The context-reset rereview confirmed the accepted correction, closed M1, and established M2 implementation eligibility.

### code-review-M2-r1

Review closeout: code-review-M2-r1

#### SPSIM-M2-CR1

Finding ID: SPSIM-M2-CR1
Disposition: accepted
Status: closed
Owner: implementation author
Owning stage: implement M2
Decision owner: none
Decision needed: none; R21-R42 define the required correction.
Chosen action: Expand the governed reference and focused assertions to name every mandatory identity, prerequisite, evidence field, preservation rule, and stop boundary.
Rationale: Generic phrases do not form a deterministic identity-bound transaction contract.
Required outcome: Complete explicit governed semantics while both loaded profiles remain below baseline.
Safe resolution path: Change only the governed reference, focused tests, and M2 evidence, rerun M2 validation, and return for rereview.
Validation target: focused and broad skill tests, canonical validation, build checks, profile measurement, and diff checking.
Validation evidence: corrected governed reference and focused assertions; M2 validation passed; `reviews/code-review-m2-r2.md`.

#### SPSIM-M2-CR2

Finding ID: SPSIM-M2-CR2
Disposition: accepted
Status: closed
Owner: implementation author
Owning stage: implement M2
Decision owner: none
Decision needed: none; the M1 rule ledger defines the missing inline semantics.
Chosen action: Restore complete proposal settlement, unrelated-target, normative scope, and superseded-replacement rules in compact common-path prose.
Rationale: Simplification may relocate or deduplicate behavior but cannot silently delete retained universal rules.
Required outcome: Every affected retained-inline rule is directly recoverable from `SKILL.md` without restoring duplicated sections.
Safe resolution path: Change only `SKILL.md`, focused tests, and M2 evidence, rerun M2 validation, and return for rereview.
Validation target: focused and broad skill tests, readability validation, profile measurement, and rule-ledger inspection.
Validation evidence: corrected `SKILL.md` and focused assertions; profile evidence and M2 validation passed; `reviews/code-review-m2-r2.md`.

### code-review-M2-r2

Review closeout: code-review-M2-r2

No material findings; no resolution entry required. The context-reset rereview confirmed both accepted corrections, closed M2, and established M3 implementation eligibility.

### code-review-M3-r1

Review closeout: code-review-M3-r1

No material findings; no resolution entry required. The review confirmed measurements, preservation, and package parity, closed M3, and established final holistic review eligibility.

### code-review-final-r1

Review closeout: code-review-final-r1

No material findings; no resolution entry required. The final holistic review reconciled the complete branch, all milestones, corrections, requirements, tests, package proof, and lifecycle evidence and established explanation eligibility.
