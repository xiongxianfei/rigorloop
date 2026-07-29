# Review Resolution: Progressive Boundary-First Skill Guidance

## Summary

Closeout status: open

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: proposal-review-r3
Review closeout: architecture-review-r1
Review closeout: architecture-review-r2
Review closeout: plan-review-r1
Review closeout: plan-review-r2
Review closeout: test-spec-review-r1
Review closeout: test-spec-review-r2
Review closeout: code-review-m1-r1
Review closeout: code-review-m1-r2
Review closeout: code-review-m1-r3
Review closeout: code-review-m1-r4
Review closeout: code-review-m1-r5
Review closeout: code-review-m1-r6
Review closeout: code-review-m1-r7
Review closeout: code-review-m1-r8
Review closeout: code-review-m2-r1
Review closeout: code-review-m2-r2
Review closeout: code-review-m2-r3
Review closeout: code-review-m2-r4
Review closeout: code-review-m3-r1

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`,
  `proposal-review-r3`, `architecture-review-r1`,
  `architecture-review-r2`, `plan-review-r1`, `plan-review-r2`,
  `test-spec-review-r1`, `test-spec-review-r2`, `code-review-m1-r1`,
  `code-review-m1-r2`, `code-review-m1-r3`, `code-review-m1-r4`,
  `code-review-m2-r1`, `code-review-m2-r2`, `code-review-m2-r3`,
  `code-review-m2-r4`, `code-review-m3-r1`
- Findings resolved: 25
- Unresolved findings: 0
- Current result: M3 code-review R1 is clean-with-notes; M3 is closed and M4 may begin.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| PBS-PR1 | accepted | resolved | Selector removal now follows contract review while the existing-contract bug fix remains independent. |
| PBS-PR2 | accepted | resolved | Proposal-review R3 confirms one test specification is authored after the reviewed plan and settled through `test-spec-review`. |
| PBS-AR1 | accepted | resolved | ADR-20260729 defines the exact closed projection-manifest schema and the canonical package identifies it as the sole resource matrix. |
| PBS-AR2 | accepted | resolved | The architecture separates tracked activation state and rollback from derived package, archive, and clean-install proof. |
| PBS-TSR1 | accepted | resolved | M2 directly proves its compatibility-guidance state matrix and includes every plan-required M2 command; M4 retains composed activation and rollback proof. |
| CR-M1-R1-001 | accepted | resolved | Exact resource tuples and canonical versions now fail closed. |
| CR-M1-R1-002 | accepted | resolved | The four-question compact scan is restored to the compact core. |
| CR-M1-R1-003 | accepted | resolved | Catchable interruption restores present and absent targets before propagation. |
| CR-M1-R1-004 | accepted | resolved | Manifest and family-source identity is preserved through public consumers. |
| CR-M1-R2-001 | accepted | resolved | Canonical and skill-local recursive inventory rejects alternate and nested additions. |
| CR-M1-R2-002 | accepted | resolved | Projection and activation diagnostics preserve structured resource identity. |
| CR-M1-R3-001 | accepted | resolved | Catchable interruption restores target state before propagation. |
| CR-M1-R3-002 | accepted | resolved | Projection derives from the manifest without a parallel tuple matrix. |
| CR-M1-R3-003 | accepted | resolved | Missing-manifest diagnostics are structured through CLI and activation. |
| CR-M1-R4-001 | accepted | resolved | Skill validation translates manifest failures without traceback or private roots. |
| CR-M1-R4-002 | accepted | resolved | Manifest scalars are represented by one-way identities. |
| CR-M1-R5-001 | accepted | resolved | Canonical resource-version values use one-way diagnostic identities. |
| CR-M1-R5-002 | accepted | resolved | Symlink inventory is scoped to governed boundary resources. |
| CR-M1-R6-001 | accepted | resolved | Drift through the final stability barrier restores targets; success binds the reported snapshot identity. |
| CR-M1-R7-001 | rejected | resolved | The approved contract does not require exclusion of non-cooperative writes after the linearization read. |
| CR-M1-R7-002 | accepted | resolved | Descriptor-relative no-follow writes prevent outside mutation and recovery aggregates unsafe paths. |
| CR-M1-R7-003 | accepted | resolved | Identity diagnostics name affected stable resource layers. |
| CR-M2-R1-001 | accepted | resolved | Independent decision derivation, complete identity coverage, and shipped-guidance bindings replace self-assertion. |
| CR-M2-R2-001 | accepted | resolved | Closed sets, boolean types, stable property IDs, and unknown/removal mutations now fail closed for valid-shaped rows. |
| CR-M2-R3-001 | accepted | resolved | Unknown identities and malformed rows fail before dependent logic; valid rows remain order-independent. |

## Finding Details

### code-review-m2-r1

#### CR-M2-R1-001 - Semantic scenario proof does not validate scenario decisions

Finding ID: CR-M2-R1-001
Disposition: accepted
Status: resolved
Owner: M2 implementation
Owning stage: review-resolution
Chosen action: Add an independent test oracle, complete the distinct scenario matrix, bind cases to shipped guidance, and prove contradictory mutations fail.
Rationale: Fixture-authored expected values cannot prove their own semantic correctness.
Validation target: code-review-m2-r2
Validation evidence: Code-review M2 R2 confirmed contradictory outcomes, routes, missing identities, missing skills, and missing guidance now fail.

### code-review-m2-r2

#### CR-M2-R2-001 - Semantic oracle accepts unknown vocabulary and removable partitions

Finding ID: CR-M2-R2-001
Disposition: accepted
Status: resolved
Owner: M2 implementation
Owning stage: review-resolution
Chosen action: Validate every closed input and output vocabulary and boolean type before evaluation, enforce stable property coverage, and add unknown-value and removal mutations.
Rationale: A proof oracle must fail closed before semantic consistency checks.
Validation target: code-review-m2-r3
Validation evidence: Code-review M2 R3 confirmed declared vocabularies, booleans, and required property removals fail; malformed row identity remains separately tracked.

### code-review-m2-r3

#### CR-M2-R3-001 - Case identity and malformed rows do not fail closed

Finding ID: CR-M2-R3-001
Disposition: accepted
Status: resolved
Owner: M2 implementation
Owning stage: review-resolution
Chosen action: Validate row shape, case and skill identity, and types before all dependent logic, then aggregate only validated rows.
Rationale: Closed-vocabulary validators must reject unknowns before consistency evaluation and must not crash on malformed input.
Validation target: code-review-m2-r4
Validation evidence: Code-review M2 R4 confirmed every malformed category returns bounded errors without oracle invocation and the complete M2 suite passes.

### code-review-m2-r4

No new findings. Both independent reviewers issued clean-with-notes receipts.

### code-review-m3-r1

No findings. Both independent reviewers confirmed exact path-owned routing.

### code-review-m1-r1

#### CR-M1-R1-001 - Exact resource authority is not closed

Finding ID: CR-M1-R1-001
Disposition: accepted
Status: resolved
Owner: M1 implementation
Owning stage: review-resolution
Chosen action: Validate the manifest against one immutable exact resource contract and validate every canonical resource version before projection.
Rationale: Generic containment and known-consumer membership do not prove the ADR-exact ownership matrix.
Validation target: code-review-m1-r2
Validation evidence: Code-review M1 R2 confirmed exact tuple and canonical version mutations fail closed.

#### CR-M1-R1-002 - Compact core omits the compact scan

Finding ID: CR-M1-R1-002
Disposition: accepted
Status: resolved
Owner: M1 implementation
Owning stage: review-resolution
Chosen action: Add the exact PBS-R007 questions to the compact core, reproject, and refresh identities.
Rationale: PBS-R012 assigns compact scan semantics to the compact resource independently of M2 stage-local invocation.
Validation target: code-review-m1-r2
Validation evidence: Code-review M1 R2 confirmed the compact core and all ten projections contain the exact scan.

#### CR-M1-R1-003 - Interrupted writes leave a mixed tree

Finding ID: CR-M1-R1-003
Disposition: accepted
Status: resolved
Owner: M1 implementation
Owning stage: review-resolution
Chosen action: Snapshot target state after preflight, restore on handled write failure, and prove early, middle, final, and retry paths.
Rationale: T2 requires an interrupted-write proof, while current code proves only invalid-input preflight.
Validation target: code-review-m1-r4
Validation evidence: Code-review M1 R3 reproduced partial mutation on `KeyboardInterrupt`; broader recovery proof remains pending.

#### CR-M1-R1-004 - Activation diagnostics erase manifest failure identity

Finding ID: CR-M1-R1-004
Disposition: accepted
Status: resolved
Owner: M1 implementation
Owning stage: review-resolution
Chosen action: Use structured projection errors and retain source check, path, expectation, and reason through activation validation.
Rationale: PBS-R037 requires the actual affected resource and blocking reason.
Validation target: code-review-m1-r4
Validation evidence: Code-review M1 R3 confirmed family-source identity but reproduced missing-manifest fallback; complete public diagnostic proof remains pending.

### code-review-m1-r2

#### CR-M1-R2-001 - Alternate-version resources escape inventory validation

Finding ID: CR-M1-R2-001
Disposition: accepted
Status: resolved
Owner: M1 implementation
Owning stage: review-resolution
Chosen action: Inventory every `boundary-first-*.md` resource in canonical and governed reference roots and reject non-manifest paths.
Rationale: A version-specific glob cannot prove additional or mixed-version closure.
Validation target: code-review-m1-r3
Validation evidence: Code-review M1 R3 confirmed recursive canonical and skill-local inventory rejects alternate and nested additions.

#### CR-M1-R2-002 - Structured diagnostics remain incomplete on sibling paths

Finding ID: CR-M1-R2-002
Disposition: accepted
Status: resolved
Owner: M1 implementation
Owning stage: review-resolution
Chosen action: Structure missing-source and path errors, use one bounded CLI formatter, and prove activation and CLI family-resource failures.
Rationale: Fixing one manifest-version case does not satisfy PBS-R037 across public and sibling validation paths.
Validation target: code-review-m1-r3
Validation target: code-review-m1-r4
Validation evidence: Family-resource and missing-manifest CLI and activation diagnostics pass in the 24-test projection and 61-test activation suites; independent R4 confirmation remains pending.

### code-review-m1-r3

#### CR-M1-R3-001 - Catchable interruption leaves a mixed projection tree

Finding ID: CR-M1-R3-001
Disposition: accepted
Status: resolved
Owner: M1 implementation
Owning stage: review-resolution
Chosen action: Restore snapshots for catchable in-process interruptions before preserving the original exception.
Rationale: T2 requires coherent recovery from an interrupted projection, not only `OSError`.
Validation target: code-review-m1-r4
Validation evidence: Both pre-existing and initially absent target-set interruption cases restore exactly, re-raise `KeyboardInterrupt`, and retry successfully in the 24-test projection suite; independent R4 confirmation remains pending.

#### CR-M1-R3-002 - Projection code retains a parallel resource inventory

Finding ID: CR-M1-R3-002
Disposition: accepted
Status: resolved
Owner: M1 implementation
Owning stage: review-resolution
Chosen action: Remove the duplicated source, target, and consumer matrix and validate manifest structure through independent invariants.
Rationale: The ADR assigns sole declarative projection authority to the manifest.
Validation target: code-review-m1-r4
Validation evidence: The source-level no-parallel-matrix regression and approved manifest-identity mutations pass in the 24-test projection suite; independent R4 confirmation remains pending.

#### CR-M1-R3-003 - Missing-manifest diagnostics lose path and expectation

Finding ID: CR-M1-R3-003
Disposition: accepted
Status: resolved
Owner: M1 implementation
Owning stage: review-resolution
Chosen action: Raise a structured missing-manifest error and prove exact CLI and activation propagation.
Rationale: PBS-R037 applies to required manifest absence as well as family resources.
Validation target: code-review-m1-r4
Validation evidence: Missing-manifest CLI and activation regressions preserve exact path and expected condition in the 24-test projection and 61-test activation suites; independent R4 confirmation remains pending.

### code-review-m1-r4

#### CR-M1-R4-001 - Skill validation leaks malformed-manifest exceptions

Finding ID: CR-M1-R4-001
Disposition: accepted
Status: resolved
Owner: M1 implementation
Owning stage: review-resolution
Chosen action: Translate projection contract failures into bounded skill-validation errors and prove missing and malformed CLI paths.
Rationale: PBS-R037 applies consistently across public validator consumers.
Validation target: code-review-m1-r5
Validation evidence: Missing and unknown-schema isolated skill-validation CLI cases return code 1 with structured repository-relative errors, no traceback, and no temporary root; independent R5 confirmation remains pending.

#### CR-M1-R4-002 - Manifest diagnostics expose untrusted scalar values

Finding ID: CR-M1-R4-002
Disposition: accepted
Status: resolved
Owner: M1 implementation
Owning stage: review-resolution
Chosen action: Remove untrusted values from diagnostic messages and consistently redact the offending-value field.
Rationale: Actionable diagnostics do not require disclosure of the rejected payload.
Validation target: code-review-m1-r5
Validation evidence: Secret-bearing consumer fixtures preserve stable identities while excluding the scalar from projection CLI and activation serialization; independent R5 confirmation remains pending.

### code-review-m1-r5

#### CR-M1-R5-001 - Canonical resource diagnostics disclose untrusted version scalars

Finding ID: CR-M1-R5-001
Disposition: accepted
Status: resolved
Owner: M1 implementation
Owning stage: review-resolution
Chosen action: Hash canonical version offending values and prove public and activation paths.
Rationale: Resource contents are untrusted diagnostic input.
Validation target: code-review-m1-r6
Validation evidence: Secret-bearing canonical version fixtures preserve stable check, path, reason, and expected version while emitting only a SHA-256 offending identity through CLI and activation; independent R6 confirmation remains pending.

#### CR-M1-R5-002 - Projection inventory rejects unrelated symlinked resources

Finding ID: CR-M1-R5-002
Disposition: accepted
Status: resolved
Owner: M1 implementation
Owning stage: review-resolution
Chosen action: Restrict recursive symlink discovery to the boundary resource namespace while retaining governed path ancestor checks.
Rationale: The boundary validator must not claim unrelated packaged resources.
Validation target: code-review-m1-r6
Validation evidence: Unrelated skill-local and canonical reference symlinks pass, while existing governed and boundary-resource symlink cases fail closed in the 26-test projection suite; independent R6 confirmation remains pending.

### code-review-m1-r6

#### CR-M1-R6-001 - Projection can return success for an already-stale transaction

Finding ID: CR-M1-R6-001
Disposition: accepted
Status: resolved
Owner: M1 implementation
Owning stage: review-resolution
Chosen action: Snapshot canonical inputs and enforce a final stability barrier, restoring write targets on drift.
Rationale: Cached-byte target checks cannot prove currency against inputs that change during the transaction.
Validation target: code-review-m1-r7
Validation evidence: Twelve manifest/resource and early/middle/final mutation cases reject success, restore prior targets, and retry deterministically. Success reports the snapshot identities; later non-cooperative drift is rejected by activation or the next check as required by PBS-R033, PBS-R034, and BND-TEMPORAL-001.

### code-review-m1-r7

#### CR-M1-R7-001 - Final-read race is treated as an unbounded concurrency guarantee

Finding ID: CR-M1-R7-001
Disposition: rejected
Status: resolved
Owner: workflow orchestrator
Owning stage: review-resolution
Chosen action: Keep success defined by the reported immutable input snapshot and retain downstream drift rejection.
Rationale: PBS-R033 requires incomplete or divergent states to fail closed, PBS-R034 governs atomic activation, and BND-TEMPORAL-001 says drift blocks activation. None requires a global lock against non-cooperative writes occurring after the projector's final read.
Validation target: code-review-m1-r8
Validation evidence: Static contract interpretation plus existing snapshot-identity, drift, activation, and retry tests.

#### CR-M1-R7-002 - Target topology drift can escape containment or abort recovery

Finding ID: CR-M1-R7-002
Disposition: accepted
Status: resolved
Owner: M1 implementation
Owning stage: review-resolution
Chosen action: Use descriptor-relative no-follow target operations and aggregate restoration path failures.
Rationale: Repository containment applies even under a target-parent swap.
Validation target: code-review-m1-r8
Validation evidence: A target-parent swap cannot write outside; restoration continues for every unaffected target and reports `BFR-PROJECTION-RESTORE` for the unsafe path in the 28-test projection suite; independent R8 confirmation remains pending.

#### CR-M1-R7-003 - Exact-manifest diagnostics omit the affected resource layer

Finding ID: CR-M1-R7-003
Disposition: accepted
Status: resolved
Owner: M1 implementation
Owning stage: review-resolution
Chosen action: Add opaque per-layer diagnostic identities and report differing stable resource IDs.
Rationale: PBS-R037 requires the affected resource layer without requiring disclosure of rejected values.
Validation target: code-review-m1-r8
Validation evidence: Exact compact, feature-authoring, and proof tuple mutations identify the affected stable layer while retaining one-way offending identities in the 28-test projection suite; independent R8 confirmation remains pending.

### code-review-m1-r8

Status: approved
Material findings: none
Resolution required: no new findings
Evidence: reviews/code-review-m1-r8.md

### proposal-review-r1

#### PBS-PR1 - Selector removal precedes its contract gate

Finding ID: PBS-PR1
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Separate the already-approved embedded-status bug fix from the new selector policy, and place selector removal plus boundary-guidance implementation after amended feature and test specifications, spec review, architecture assessment, plan review, and proof-map review.
Rationale: The stage-owned lifecycle specification already governs the embedded-status correction, while selector routing is a new contributor-visible behavior that requires contract-first review.
Validation target: proposal-review-r2
Validation evidence: Proposal-review R2 confirmed that selector removal is separated from the existing-contract bug fix and remains behind contract review.

### proposal-review-r2

#### PBS-PR2 - Test-spec timing and review ownership are duplicated

Finding ID: PBS-PR2
Disposition: accepted
Status: resolved
Owner: proposal author
Chosen action: Use one stage-owned sequence in which feature contracts settle through `spec-review`, architecture settles through `architecture-review`, the plan settles through `plan-review`, and one test specification is then authored and settled through `test-spec-review` before implementation.
Owning stage: proposal
Rationale: This follows the approved workflow, prevents duplicate proof-map work, and keeps each review stage within its artifact authority.
Expected proof: A revised proposal and proposal-review R3 confirm one test-spec artifact, correct review ownership, and the approved artifact order.
Validation evidence: Proposal-review R3 confirmed the corrected artifact order, one test-spec artifact, and stage-owned review authority.

### architecture-review-r1

#### PBS-AR1 - Projection manifest shape is not exact

Finding ID: PBS-AR1
Disposition: accepted
Status: resolved
Owner: architecture author
Owning stage: architecture
Chosen action: Add the exact closed top-level and resource-entry schema,
resource IDs, paths, consumer ordering, duplicate rules, and unknown-field
behavior to the ADR and matching canonical architecture.
Rationale: The approved spec and spec-review explicitly delegate this closed
data contract to architecture, and downstream planning and proof need one
implementable vocabulary.
Validation target: architecture-review-r2
Validation evidence: Architecture-review R2 confirms the exact top-level and
entry keys, values, resource IDs, paths, order, consumers, duplicate rules,
unsafe-path rules, and unknown-field behavior are complete and testable.

#### PBS-AR2 - Commit-level rollback includes ephemeral outputs

Finding ID: PBS-AR2
Disposition: accepted
Status: resolved
Owner: architecture author
Owning stage: architecture
Chosen action: Separate the exact tracked activation transaction from
generated, packed, and installed proof; define pre-activation rollback as
tracked revert plus derived-output regeneration or discard.
Rationale: Generated packages and clean target installs are derived validation
surfaces under repository governance and cannot be Git-reverted as commit
contents.
Validation target: architecture-review-r2
Validation evidence: Architecture-review R2 confirms the tracked activation
transaction, derived proof set, atomic acceptance boundary, pre-activation
recovery, and immutable post-activation rollback are distinct and
implementable.

### test-spec-review-r1

#### PBS-TSR1 - M2 compatibility and command proof is deferred or omitted

Finding ID: PBS-TSR1
Disposition: accepted
Status: resolved
Owner: test-spec author
Owning stage: test-spec
Chosen action: Add direct M2 proof for pending, active-candidate,
grandfathered non-substantive, and substantive revision guidance; bind
`BND-COMPAT-001` and `INT-004` to M2 evidence as well as later M4
composition; and add CMD2 to the M2 proof row.
Rationale: The approved plan changes this guidance in M2 and names the
projection check as an M2 command, so proof cannot be deferred entirely to
M4.
Validation target: test-spec-review-r2
Validation evidence: Test-spec-review R2 confirms T4, PRF-014, PRF-020,
PRF-022, PRF-023, and the M2 milestone row close the finding without changing
the contract or scenario count.

## Shared Validation Evidence

| Validation area | Result | Notes |
| --- | --- | --- |
| Proposal review | changes-requested | `PBS-PR1` records the contract-first sequencing defect. |
| Proposal review R2 | changes-requested | `PBS-PR1` is resolved; `PBS-PR2` records the remaining artifact-order defect. |
| Proposal review R3 | approved | `PBS-PR1` and `PBS-PR2` are resolved; no material findings remain. |
| Architecture review R1 | changes-requested | `PBS-AR1` and `PBS-AR2` are recorded and remain open pending architecture revision. |
| Architecture review R2 | approved | `PBS-AR1` and `PBS-AR2` are resolved; no material findings remain. |
| Plan review R1 | blocked | No plan-content finding was recorded; the plan remains `authoring` because primary-plan registration requires workflow-owned `planned_work`. |
| Plan review R2 | approved | One-time plan initialization resolves the lifecycle precondition; the plan is ready for test-spec. |
| Test-spec review R1 | changes-requested | `PBS-TSR1` records the M2 proof-timing and command-ledger mismatch. |
| Test-spec review R2 | approved | `PBS-TSR1` is resolved; the proof map permits isolated M1 implementation handoff. |

## Clean review receipts

### proposal-review-r3

Status: approved
Material findings: none
Resolution required: no
Evidence: reviews/proposal-review-r3.md

### spec-review-r1

Status: approved
Material findings: none
Resolution required: no
Evidence: reviews/spec-review-r1.md

### architecture-review-r2

Status: approved
Material findings: none
Resolution required: no new findings; reconciles `PBS-AR1` and `PBS-AR2`
Evidence: reviews/architecture-review-r2.md

### plan-review-r1

Status: blocked
Material findings: none
Resolution required: no finding disposition; lifecycle precondition resolved
by planned-work initialization and confirmed by plan-review R2
Evidence: reviews/plan-review-r1.md

### plan-review-r2

Status: approved
Material findings: none
Resolution required: no
Evidence: reviews/plan-review-r2.md

### test-spec-review-r1

Status: changes-requested
Material findings: PBS-TSR1
Resolution required: accepted and resolved by test-spec-review R2
Evidence: reviews/test-spec-review-r1.md

### test-spec-review-r2

Status: approved
Material findings: none
Resolution required: no new findings; confirms `PBS-TSR1` resolution
Evidence: reviews/test-spec-review-r2.md

## Closeout Checklist

- [x] Every material finding has a disposition.
- [x] Every accepted finding has a chosen action.
- [x] Every rejected finding has rationale.
- [x] Every deferred finding has follow-up or explicit no-follow-up rationale.
- [x] Every `needs-decision` finding is resolved or blocks closeout.
- [ ] Validation evidence is recorded for all accepted findings.
- [x] Closeout status is correct.
