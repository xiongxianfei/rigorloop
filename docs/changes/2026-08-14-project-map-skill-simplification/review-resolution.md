# Review Resolution: Project-Map Skill Simplification

## Summary

Closeout status: open

Review closeout: proposal-review-r2

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`
- Findings resolved: 3
- Unresolved findings: 3
- Current result: proposal revision required

## Resolution overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| `PMAPSIM-PR1` | accepted | closed | Reference loading now uses map-coordination evidence and every operation has an explicit write and recovery boundary. |
| `PMAPSIM-PR2` | accepted | closed | Minimum dirty-baseline truthfulness remains inline while maintenance comparison stays conditional. |
| `PMAPSIM-PR3` | accepted | closed | New results use exact operation and scope fields with a read-old/write-new compatibility migration. |
| `PMAPSIM-R2-PR1` | needs-decision | open | Proposal author must bind operations to resolved target state and isolate audit correction. |
| `PMAPSIM-R2-PR2` | needs-decision | open | Proposal author must define the coordination preflight and actual procedural assemblies. |
| `PMAPSIM-R2-PR3` | needs-decision | open | Proposal author must close area-creation prerequisites, commit ordering, and recovery. |

## Finding details

### proposal-review-r1

#### PMAPSIM-R2-PR1

Finding ID: PMAPSIM-R2-PR1
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Close reference loading when root creation discovers multi-map coordination and define every operation's allowed write set.
Chosen action: Add `map_coordination_context`, late reference loading, and closed write and recovery boundaries for root creation, area creation, refresh, and audit.
Rationale: Root creation can encounter procedure owned only by a reference that its declared profile does not load.
Required outcome: Add an evidence-based coordination predicate, late-load behavior, explicit write boundaries, and interruption handling.
Safe resolution path: Adopt `map_coordination_context` and the operation-specific boundaries recommended by `proposal-review-r1`.
Validation target: revised classification, resource ownership, expected behavior, scenarios, risks, rollout, and acceptance criteria plus independent proposal rereview.
Validation evidence: `evidence/proposal-revision-r1.md`; revised Closed classification model, Conditional-reference ownership, Expected Behavior Changes, Proposal acceptance criteria, Testing and Verification Strategy, Risks and Mitigations, and Decision Log sections.

#### PMAPSIM-R2-PR2

Finding ID: PMAPSIM-R2-PR2
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Separate universal dirty-baseline truthfulness from maintenance-specific comparison.
Chosen action: Keep the complete minimum dirty-baseline reporting contract inline and reserve prior/current comparison and correction procedure for the conditional reference.
Rationale: Root creation must describe inspected uncommitted evidence even when the maintenance reference is not loaded.
Required outcome: Keep the complete minimum baseline-reporting contract inline and move only maintenance comparison to the reference.
Safe resolution path: Adopt the ownership split recommended by `proposal-review-r1` and prove it for all profiles.
Validation target: revised ownership, scenarios, rule ledger, risks, and acceptance criteria plus independent proposal rereview.
Validation evidence: `evidence/proposal-revision-r1.md`; revised Universal ownership, Conditional-reference ownership, Proposal acceptance criteria, Testing and Verification Strategy, Risks and Mitigations, and Decision Log sections.

#### PMAPSIM-R2-PR3

Finding ID: PMAPSIM-R2-PR3
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Select the exact operation/scope result contract and compatibility migration.
Chosen action: Emit `Operation` and `Map scope` for new results, remove legacy `Mode` from new output, and use a deterministic read-old/write-new compatibility mapping.
Rationale: The current `Mode` literal is a published and validator-consumed contract, while the proposal selects a different classification without closing its emitted shape.
Required outcome: Define exact new fields, legacy mappings, ambiguity stops, and literal-consumer migration.
Safe resolution path: Adopt `Operation` and `Map scope` as the write-new result contract and migrate real consumers atomically as recommended by `proposal-review-r1`.
Validation target: revised expected behavior, compatibility, testing, rollout, and acceptance criteria plus independent proposal rereview.
Validation evidence: `evidence/proposal-revision-r1.md`; revised Result compatibility, Expected Behavior Changes, Proposal acceptance criteria, Testing and Verification Strategy, Rollout and Rollback, and Decision Log sections.

### proposal-review-r2

#### PMAPSIM-PR1

Finding ID: PMAPSIM-PR1
Disposition: needs-decision
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Bind each operation to resolved target existence and keep audit permanently read-only.
Chosen action: pending proposal revision
Rationale: Create can currently replace an existing map and bypass maintenance procedure, while audit correction is not reclassified.
Required outcome: Define a closed operation and target-state matrix and a separate refresh after audit findings.
Safe resolution path: Adopt the operation semantics recommended by `proposal-review-r2`.
Validation target: revised classification, write boundaries, expected behavior, scenarios, risks, and acceptance criteria plus independent proposal rereview.
Validation evidence: pending

#### PMAPSIM-PR2

Finding ID: PMAPSIM-PR2
Disposition: needs-decision
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Define the minimum evidence for no coordination and distinguish semantic profiles from loaded assemblies.
Chosen action: pending proposal revision
Rationale: A false-negative preflight can omit known area maps, while the same semantic profile currently represents two resource packages.
Required outcome: Close the bounded coordination preflight, ambiguity behavior, and measured assembly model.
Safe resolution path: Adopt the ownership-surface preflight and PMA0/PMA1 assembly split recommended by `proposal-review-r2`.
Validation target: revised classification, loading, measurement, scenarios, risks, and acceptance criteria plus independent proposal rereview.
Validation evidence: pending

#### PMAPSIM-PR3

Finding ID: PMAPSIM-PR3
Disposition: needs-decision
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Select one complete area-creation transaction and recovery model.
Chosen action: pending proposal revision
Rationale: Identity binding without prerequisites, order, commit point, or partial-state outcomes is not executable or safely retryable.
Required outcome: Require an existing root, bind the full transaction basis, write registration last, and classify every partial state.
Safe resolution path: Adopt the transaction sequence and recovery matrix recommended by `proposal-review-r2`.
Validation target: revised write boundaries, testing, rollout, risks, and acceptance criteria plus independent proposal rereview.
Validation evidence: pending
