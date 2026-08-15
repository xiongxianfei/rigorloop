# Review Resolution: Architecture Skill Simplification

Closeout status: open

Review closeout: proposal-review-r1

- Reviews covered: `proposal-review-r1`
- Findings resolved: 0
- Unresolved findings: 3
- Current result: proposal revision required before specification

## Resolution overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| `ARSIM-PR1` | accepted | open | Close architecture-assessment result, recording authority, persisted evidence, and compatibility. |
| `ARSIM-PR2` | accepted | open | Define per-target operations, complete manifest identity, partial result, and combined handoff. |
| `ARSIM-PR3` | accepted | open | Give every policy-bearing asset instruction one explicit disposition and owner. |

## Finding details

### proposal-review-r1

#### ARSIM-PR1

Finding ID: ARSIM-PR1
Disposition: accepted
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Reconcile semantic assessment results with current persisted workflow evidence and direct assessment behavior.
Chosen action: Add a closed isolated/workflow-managed assessment matrix and exact semantic-to-persisted mapping without a new state owner.
Rationale: The current workflow describes route-level architecture outcomes while the stage-native verifier consumes specific evidence fields, and the proposal changes direct recording behavior without compatibility treatment.
Required outcome: Define execution mode, input identity, result vocabulary, persisted evidence, ambiguity pause evidence, direct recording authority, and stop behavior.
Safe resolution path: Reuse current workflow evidence for required/not-required, preserve the current ambiguity pause owner, and explicitly preserve or amend direct rationale recording.
Validation target: revised classification, assessment recording, compatibility, risks, scenarios, and acceptance criteria plus independent rereview.
Validation evidence: pending proposal revision.

#### ARSIM-PR2

Finding ID: ARSIM-PR2
Disposition: accepted
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Replace the invocation-wide create/revise operation with a complete mixed-target transaction contract.
Chosen action: Bind an ordered per-target manifest and require complete manifest settlement before combined review handoff.
Rationale: A canonical revision can coexist with new, revised, or superseding ADRs, so one operation value cannot represent the batch.
Required outcome: Define target fields, target-local operation, batch identity, partial results, identical retry, and review eligibility.
Safe resolution path: Use existing authoring evidence to bind the manifest; do not add lifecycle state or atomic rollback.
Validation target: revised transaction, retry, recovery, handoff, architecture impact, scenarios, and acceptance criteria plus independent rereview.
Validation evidence: pending proposal revision.

#### ARSIM-PR3

Finding ID: ARSIM-PR3
Disposition: accepted
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Reconcile current policy-bearing skeleton text with the structural-only asset boundary.
Chosen action: Add an asset-content disposition table and move method semantics to the method reference while retaining necessary structure and literal styles.
Rationale: The current skeleton contains diagram, section-applicability, ADR, and quality-scenario procedure that the proposal also assigns to the new reference.
Required outcome: Classify every instruction as structural, method-owned, literal copied material, necessary compact prompt, or removed duplicate.
Safe resolution path: Preserve official headings, placeholders, link slots, table shapes, and literal styles; move normative method procedure to one reference and prove composed output.
Validation target: revised ownership, rollout, semantic/literal ledgers, scenarios, and acceptance criteria plus independent rereview.
Validation evidence: pending proposal revision.
