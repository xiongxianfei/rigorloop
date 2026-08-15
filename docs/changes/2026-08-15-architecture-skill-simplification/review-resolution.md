# Review Resolution: Architecture Skill Simplification

Closeout status: closed

Review closeout: proposal-review-r3
Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: test-spec-review-r1
Review closeout: test-spec-review-r2

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`, `proposal-review-r3`, `spec-review-r1`, `plan-review-r1`, `test-spec-review-r1`, `test-spec-review-r2`
- Findings resolved: 8
- Unresolved findings: 0
- Current result: test-spec-review R2 approved the corrected proof map for implementation handoff

## Resolution overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| `ARSIM-PR1` | accepted | closed | Separated assessment mode, judgment, route result, current completion fields, ambiguity pause, and direct recording. |
| `ARSIM-PR2` | accepted | closed | Added an ordered per-target manifest, mixed operations, closed batch results, and complete-manifest handoff. |
| `ARSIM-PR3` | accepted | closed | Classified current asset instructions and assigned method semantics to one reference owner. |
| `ARSIM-PR4` | accepted | closed | Bound authoring to one current architecture-required assessment and exact decision basis. |
| `ARSIM-PR5` | accepted | closed | Persisted the complete prepared target manifest before file mutation. |
| `ARSIM-PR6` | accepted | closed | Added dependency-aware commit order, groups, and intermediate-validity rules. |
| `ARSIM-TSR1` | accepted | closed | Added explicit AC1-AC10 traceability to stable proof cases, commands, and milestones. |
| `ARSIM-TSR2` | accepted | closed | Replaced the nonexistent module invocation with the existing repository runner and a planned M1 ledger class. |

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

### proposal-review-r2

#### ARSIM-PR4

Finding ID: ARSIM-PR4
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Bind later authoring to one current architecture-required assessment basis.
Chosen action: Add assessment receipt, exact spec, and approving spec-review identities to the target manifest and define staleness and portable applicability checks.
Rationale: Generic authoring authority cannot substitute for the current applicability decision that permits architecture work.
Required outcome: Block missing, stale, contradictory, not-required, or ambiguous assessment evidence before authoring.
Safe resolution path: Reuse current assessment evidence and record its identity in existing authoring evidence.
Validation target: revised assessment basis, manifest, staleness scenarios, and acceptance criteria plus independent rereview.
Validation evidence: `evidence/proposal-revision-r2.md`; revised sections `Assessment basis for authoring`, `Target manifest and transaction model`, `Proposal acceptance criteria`, `Architecture Impact`, and `Testing and Verification Strategy`.

#### ARSIM-PR5

Finding ID: ARSIM-PR5
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Make exact retry possible after an interrupted first target write.
Chosen action: Persist the complete ordered manifest and intended identities in prepared authoring evidence before mutation, then record progress on the same evidence surface.
Rationale: An in-memory manifest cannot distinguish valid partial state from unrelated content after interruption.
Required outcome: Define the prepared write-ahead sequence and conditional architecture consequence if existing evidence cannot support it.
Safe resolution path: Reuse existing authoring evidence when capable; otherwise require architecture work rather than weakening recovery.
Validation target: revised transaction sequence, recovery scenarios, architecture impact, and acceptance criteria plus independent rereview.
Validation evidence: `evidence/proposal-revision-r2.md`; revised sections `Multi-file writes, retries, and recovery`, `Proposal acceptance criteria`, `Architecture Impact`, and `Testing and Verification Strategy`.

#### ARSIM-PR6

Finding ID: ARSIM-PR6
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Ensure every partial canonical and ADR commit leaves a valid intermediate repository state.
Chosen action: Add dependency edges, commit groups, independently valid completion, canonical commit order, and ADR supersession order.
Rationale: Ordered targets alone do not prevent broken links or premature supersession in partial batches.
Required outcome: Commit only when dependencies are complete and preserve only independently valid targets after failure.
Safe resolution path: Keep the procedure in governed authoring and architecture-review as the approval owner.
Validation target: revised manifest, commit sequencing, partial-state matrix, static scenarios, and acceptance criteria plus independent rereview.
Validation evidence: `evidence/proposal-revision-r2.md`; revised sections `Target manifest and transaction model`, `Multi-file writes, retries, and recovery`, `Proposal acceptance criteria`, and `Risks and Mitigations`.

### proposal-review-r3

Review closeout: proposal-review-r3

No material findings; no resolution entry required. The same-stage proposal-review rerun approved the revised proposal and confirmed that all findings through `proposal-review-r2` are closed.

### spec-review-r1

Review closeout: spec-review-r1

No material findings; no resolution entry required. The formal spec review approved the contract and routed the change to bounded architecture assessment.

### plan-review-r1

Review closeout: plan-review-r1

No material findings; no resolution entry required. The formal plan review approved the stable plan and requires identity-bound initialization and settlement retry before test-spec eligibility.

### test-spec-review-r1

#### ARSIM-TSR1

Finding ID: ARSIM-TSR1
Disposition: accepted
Status: closed
Owner: test-spec author
Owning stage: test-spec
Decision owner: none
Decision needed: none; AC1 through AC10 already define the required traceability targets.
Chosen action: Add exact acceptance-criterion mappings to stable cases and commands without changing normative behavior.
Rationale: Requirement coverage alone does not satisfy the formal review contract's separate acceptance-criterion traceability obligation.
Required outcome: Every acceptance criterion maps to direct proof and can be audited from the feature spec through the test spec.
Safe resolution path: Revise only the proof map and its authoring evidence, run structural validation, and submit the committed revision for independent test-spec rereview.
Validation target: AC1-AC10 mapping, boundary validation, documentation prose validation, and change metadata validation.
Validation evidence: `evidence/test-spec-revision-r1.md`; acceptance criterion coverage map; `reviews/test-spec-review-r2.md`; boundary, prose, metadata, and review validation passed.

#### ARSIM-TSR2

Finding ID: ARSIM-TSR2
Disposition: accepted
Status: closed
Owner: test-spec author
Owning stage: test-spec
Decision owner: none
Decision needed: none; the approved plan and repository runner establish the safe command family.
Chosen action: Replace or consolidate CMD1 with an executable repository-owned focused or change-local validation command while preserving M1 timing and zero-test failure.
Rationale: A planned class can be added to the existing runner, but it cannot make the nonexistent underscored module importable without an unplanned runner change.
Required outcome: Every command identity resolves to a valid current or explicitly planned repository surface and remains aligned with the approved plan.
Safe resolution path: Revise only the proof map and its authoring evidence, confirm command resolution, and submit the committed revision for independent test-spec rereview.
Validation target: command path resolution, plan alignment, documentation prose validation, and change metadata validation.
Validation evidence: `evidence/test-spec-revision-r1.md`; corrected CMD1 ledger entry; repository runner help resolution; `reviews/test-spec-review-r2.md`; metadata and review validation passed.

### test-spec-review-r2

Review closeout: test-spec-review-r2

No material findings; no resolution entry required. The independent formal rereview approved the corrected proof map, closed ARSIM-TSR1 and ARSIM-TSR2, and established implementation handoff eligibility without starting implementation.

### code-review-M1-r1

Review closeout: code-review-M1-r1

No material findings; no resolution entry required. The independent milestone review accepted the preservation inventories, focused closed-vocabulary tests, scenarios, and measurement baseline and closed M1 without claiming later package behavior.

### code-review-M2-r1

#### ARSIM-M2-CR1

Finding ID: ARSIM-M2-CR1
Disposition: accepted
Status: closed
Owner: architecture package implementer
Owning stage: implement
Decision owner: none
Decision needed: none; R21, R26-R27, and R38-R42 enumerate the missing contract properties.
Chosen action: Restore the exact prepared-manifest, evidence-state, batch-result, and changed-operation semantics in the governed reference and focused proof.
Rationale: Concision cannot omit identity and recovery properties needed for crash-safe governed writes.
Required outcome: The governed package states every required property and passes CMD3-CMD6.
Safe resolution path: Apply the bounded correction and complete context-reset rereview.
Validation target: governed reference, focused transaction assertions, M2 evidence, and package validation.
Validation evidence: corrected governed reference and focused assertions at `793d3acd`; CMD3-CMD6 passed; `reviews/code-review-m2-r2.md` approved the correction.

### code-review-M2-r2

Review closeout: code-review-M2-r2

No material findings; no resolution entry required. The context-reset rereview confirmed `ARSIM-M2-CR1` resolved and closed M2 without claiming M3 or final verification.

### code-review-M3-r1

Review closeout: code-review-M3-r1

No material findings; no resolution entry required. The independent milestone review accepted the measurements, semantic reconciliation, boundary proof, and canonical-through-installed adapter parity and closed M3.
