# Review Resolution: Architecture Skill Simplification

Closeout status: closed

Review closeout: proposal-review-r1

- Reviews covered: `proposal-review-r1`
- Findings resolved: 3
- Unresolved findings: 0
- Current result: revised proposal ready for independent rereview

## Resolution overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| `ARSIM-PR1` | accepted | closed | Separated assessment mode, judgment, route result, current completion fields, ambiguity pause, and direct recording. |
| `ARSIM-PR2` | accepted | closed | Added an ordered per-target manifest, mixed operations, closed batch results, and complete-manifest handoff. |
| `ARSIM-PR3` | accepted | closed | Classified current asset instructions and assigned method semantics to one reference owner. |

## Finding details

### proposal-review-r1

#### ARSIM-PR1

Finding ID: ARSIM-PR1
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Reconcile semantic assessment results with current persisted workflow evidence and direct assessment behavior.
Chosen action: Use separate assessment mode, judgment, and route values; retain current required/not-required completion receipt fields; keep ambiguity as a workflow pause; and allow isolated writes only to an explicit valid path.
Rationale: The current workflow describes route-level architecture outcomes while the stage-native verifier consumes specific evidence fields, and the proposal changes direct recording behavior without compatibility treatment.
Required outcome: Define execution mode, input identity, result vocabulary, persisted evidence, ambiguity pause evidence, direct recording authority, and stop behavior.
Safe resolution path: Reuse current workflow evidence for required/not-required, preserve the current ambiguity pause owner, and explicitly preserve or amend direct rationale recording.
Validation target: revised classification, assessment recording, compatibility, risks, scenarios, and acceptance criteria plus independent rereview.
Validation evidence: `evidence/proposal-revision-r1.md`; revised sections `Classification model`, `Assessment isolation and recording`, `Proposal acceptance criteria`, `Expected Behavior Changes`, `Testing and Verification Strategy`, and `Risks and Mitigations`.

#### ARSIM-PR2

Finding ID: ARSIM-PR2
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Replace the invocation-wide create/revise operation with a complete mixed-target transaction contract.
Chosen action: Bind an ordered per-target manifest with target-local operations, existing authoring evidence, three batch results, exact retry identity, and complete-manifest review handoff.
Rationale: A canonical revision can coexist with new, revised, or superseding ADRs, so one operation value cannot represent the batch.
Required outcome: Define target fields, target-local operation, batch identity, partial results, identical retry, and review eligibility.
Safe resolution path: Use existing authoring evidence to bind the manifest; do not add lifecycle state or atomic rollback.
Validation target: revised transaction, retry, recovery, handoff, architecture impact, scenarios, and acceptance criteria plus independent rereview.
Validation evidence: `evidence/proposal-revision-r1.md`; revised sections `Target manifest and transaction model`, `Multi-file writes, retries, and recovery`, `Proposal acceptance criteria`, `Expected Behavior Changes`, `Architecture Impact`, and `Testing and Verification Strategy`.

#### ARSIM-PR3

Finding ID: ARSIM-PR3
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Reconcile current policy-bearing skeleton text with the structural-only asset boundary.
Chosen action: Retain headings, ordering, placeholders, table shapes, neutral prompts, and literal Mermaid styles; move applicability, adequacy, diagram, ADR, and quality-scenario semantics to the method reference.
Rationale: The current skeleton contains diagram, section-applicability, ADR, and quality-scenario procedure that the proposal also assigns to the new reference.
Required outcome: Classify every instruction as structural, method-owned, literal copied material, necessary compact prompt, or removed duplicate.
Safe resolution path: Preserve official headings, placeholders, link slots, table shapes, and literal styles; move normative method procedure to one reference and prove composed output.
Validation target: revised ownership, rollout, semantic/literal ledgers, scenarios, and acceptance criteria plus independent rereview.
Validation evidence: `evidence/proposal-revision-r1.md`; revised sections `Asset ownership`, `Proposal acceptance criteria`, `Expected Behavior Changes`, `Testing and Verification Strategy`, `Rollout and Rollback`, and `Risks and Mitigations`.
