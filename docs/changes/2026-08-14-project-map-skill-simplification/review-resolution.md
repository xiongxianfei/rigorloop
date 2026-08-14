# Review Resolution: Project-Map Skill Simplification

## Summary

Closeout status: closed

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: proposal-review-r3
Review closeout: spec-review-r1
Review closeout: architecture-review-r1
Review closeout: plan-review-r1
Review closeout: test-spec-review-r1
Review closeout: test-spec-review-r2

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`, `proposal-review-r3`, `spec-review-r1`, `architecture-review-r1`, `plan-review-r1`, `test-spec-review-r1`, `test-spec-review-r2`
- Findings resolved: 7
- Unresolved findings: 0
- Current result: revised test spec approved and active; implementation handoff allowed

## Resolution overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| `PMAPSIM-PR1` | accepted | closed | Reference loading now uses map-coordination evidence and every operation has an explicit write and recovery boundary. |
| `PMAPSIM-PR2` | accepted | closed | Minimum dirty-baseline truthfulness remains inline while maintenance comparison stays conditional. |
| `PMAPSIM-PR3` | accepted | closed | New results use exact operation and scope fields with a read-old/write-new compatibility migration. |
| `PMAPSIM-R2-PR1` | accepted | closed | Operations now depend on resolved target state, and audit correction begins a new refresh. |
| `PMAPSIM-R2-PR2` | accepted | closed | A bounded seven-surface preflight selects between two explicit procedural assemblies. |
| `PMAPSIM-R2-PR3` | accepted | closed | Area creation now requires a valid root and uses one root-registration-last recoverable transaction. |
| `PMAPTSR-PR1` | rejected | closed | Manual semantic judgment is assigned to ordinary PR review rather than represented as a scripted test-spec acceptance procedure. |

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
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Bind each operation to resolved target existence and keep audit permanently read-only.
Chosen action: Permit create only for absent targets, require refresh for existing targets and full rewrites, and make post-audit correction a separately resolved refresh.
Rationale: Create can currently replace an existing map and bypass maintenance procedure, while audit correction is not reclassified.
Required outcome: Define a closed operation and target-state matrix and a separate refresh after audit findings.
Safe resolution path: Adopt the operation semantics recommended by `proposal-review-r2`.
Validation target: revised classification, write boundaries, expected behavior, scenarios, risks, and acceptance criteria plus independent proposal rereview.
Validation evidence: `evidence/proposal-revision-r2.md`; revised Operation selection, write boundaries, Expected Behavior Changes, Proposal acceptance criteria, Testing and Verification Strategy, Risks and Mitigations, and Decision Log sections.

#### PMAPSIM-PR2

Finding ID: PMAPSIM-PR2
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Define the minimum evidence for no coordination and distinguish semantic profiles from loaded assemblies.
Chosen action: Add the seven known coordination surfaces and distinguish six semantic classifications from `PMA0` and `PMA1` procedural assemblies.
Rationale: A false-negative preflight can omit known area maps, while the same semantic profile currently represents two resource packages.
Required outcome: Close the bounded coordination preflight, ambiguity behavior, and measured assembly model.
Safe resolution path: Adopt the ownership-surface preflight and PMA0/PMA1 assembly split recommended by `proposal-review-r2`.
Validation target: revised classification, loading, measurement, scenarios, risks, and acceptance criteria plus independent proposal rereview.
Validation evidence: `evidence/proposal-revision-r2.md`; revised classification, coordination preflight, assembly, measurement, acceptance, scenario, risk, and decision sections.

#### PMAPSIM-PR3

Finding ID: PMAPSIM-PR3
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Select one complete area-creation transaction and recovery model.
Chosen action: Require an existing valid root, bind the complete transaction basis, write registration last, and classify every partial state.
Rationale: Identity binding without prerequisites, order, commit point, or partial-state outcomes is not executable or safely retryable.
Required outcome: Require an existing root, bind the full transaction basis, write registration last, and classify every partial state.
Safe resolution path: Adopt the transaction sequence and recovery matrix recommended by `proposal-review-r2`.
Validation target: revised write boundaries, testing, rollout, risks, and acceptance criteria plus independent proposal rereview.
Validation evidence: `evidence/proposal-revision-r2.md`; revised Area-map creation transaction, write boundaries, Expected Behavior Changes, Proposal acceptance criteria, Testing and Verification Strategy, Risks and Mitigations, and Decision Log sections.

### proposal-review-r3

Review closeout: proposal-review-r3

No material findings; no resolution entry required. The same-stage proposal-review rerun approved the revised proposal and closed all findings through `proposal-review-r2`.

### spec-review-r1

Review closeout: spec-review-r1

No material findings; no resolution entry required. The specification is approved and conditionally ready for eventual test-spec authoring after the required bounded architecture update and execution planning settle.

### architecture-review-r1

Review closeout: architecture-review-r1

No material findings; no resolution entry required. The canonical architecture update is approved and ready for execution planning.

### plan-review-r1

Review closeout: plan-review-r1

No material findings; no resolution entry required. The plan judgment was approved, `planned_work` was initialized from the exact reviewed basis, and the identical settlement retry activated the matching plan entry without semantic rereview.

### test-spec-review-r1

#### PMAPTSR-PR1

Finding ID: PMAPTSR-PR1
Disposition: rejected
Status: closed
Owner: test-spec author
Owning stage: test-spec
Decision owner: test-spec author
Decision needed: Decide whether semantic judgment is a scripted test-spec proof obligation or ordinary PR reviewer responsibility.
Chosen action: Remove MP0 and MP1 from test acceptance, convert every affected proof row to deterministic evidence, and leave final human semantic judgment to ordinary PR review.
Rationale: The user explicitly assigned this judgment to PR reviewers and rejected a separate manual semantic-review procedure. Automated ledgers, scenarios, representative outputs, measurements, and package checks remain the pre-implementation proof surface.
Required outcome: No proof or milestone row depends on MP0 or MP1, deterministic evidence remains complete, and the test spec does not claim that later PR review has occurred.
Safe resolution path: Remove the manual procedures and their hybrid mappings, validate the resulting proof map, and submit the exact revised test-spec identity for independent rereview.
Validation target: Deterministic proof mappings, milestone proof mappings, boundary validation, and independent test-spec rereview.
Validation evidence: `evidence/test-spec-revision-r1.md`; revised testing strategy, proof map, milestone proof map, T16, T17, Manual QA checklist, and exclusions.

### test-spec-review-r2

Review closeout: test-spec-review-r2

No material findings; no resolution entry required. The rereview verified the rejection and closure of `PMAPTSR-PR1`, confirmed that deterministic proof remains complete without manual semantic-review procedures, approved the revised proof map, and settled the matching test-spec artifact.
