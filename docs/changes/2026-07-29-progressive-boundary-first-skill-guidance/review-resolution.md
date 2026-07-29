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
Review pending closeout: code-review-m1-r1

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`,
  `proposal-review-r3`, `architecture-review-r1`,
  `architecture-review-r2`, `plan-review-r1`, `plan-review-r2`,
  `test-spec-review-r1`, `test-spec-review-r2`, `code-review-m1-r1`
- Findings resolved: 5
- Unresolved findings: 4
- Current result: M1 code-review R1 requests four in-scope corrections before rereview.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| PBS-PR1 | accepted | resolved | Selector removal now follows contract review while the existing-contract bug fix remains independent. |
| PBS-PR2 | accepted | resolved | Proposal-review R3 confirms one test specification is authored after the reviewed plan and settled through `test-spec-review`. |
| PBS-AR1 | accepted | resolved | ADR-20260729 defines the exact closed projection-manifest schema and the canonical package identifies it as the sole resource matrix. |
| PBS-AR2 | accepted | resolved | The architecture separates tracked activation state and rollback from derived package, archive, and clean-install proof. |
| PBS-TSR1 | accepted | resolved | M2 directly proves its compatibility-guidance state matrix and includes every plan-required M2 command; M4 retains composed activation and rollback proof. |
| CR-M1-R1-001 | accepted | open | Close exact resource tuples and canonical resource versions before projection. |
| CR-M1-R1-002 | accepted | open | Restore the four-question compact scan to the compact core. |
| CR-M1-R1-003 | accepted | open | Restore prior target state after a handled projection write failure. |
| CR-M1-R1-004 | accepted | open | Preserve structured manifest failure identity through activation validation. |

## Finding Details

### code-review-m1-r1

#### CR-M1-R1-001 - Exact resource authority is not closed

Finding ID: CR-M1-R1-001
Disposition: accepted
Status: open
Owner: M1 implementation
Owning stage: review-resolution
Chosen action: Validate the manifest against one immutable exact resource contract and validate every canonical resource version before projection.
Rationale: Generic containment and known-consumer membership do not prove the ADR-exact ownership matrix.
Validation target: code-review-m1-r2
Validation evidence: pending

#### CR-M1-R1-002 - Compact core omits the compact scan

Finding ID: CR-M1-R1-002
Disposition: accepted
Status: open
Owner: M1 implementation
Owning stage: review-resolution
Chosen action: Add the exact PBS-R007 questions to the compact core, reproject, and refresh identities.
Rationale: PBS-R012 assigns compact scan semantics to the compact resource independently of M2 stage-local invocation.
Validation target: code-review-m1-r2
Validation evidence: pending

#### CR-M1-R1-003 - Interrupted writes leave a mixed tree

Finding ID: CR-M1-R1-003
Disposition: accepted
Status: open
Owner: M1 implementation
Owning stage: review-resolution
Chosen action: Snapshot target state after preflight, restore on handled write failure, and prove early, middle, final, and retry paths.
Rationale: T2 requires an interrupted-write proof, while current code proves only invalid-input preflight.
Validation target: code-review-m1-r2
Validation evidence: pending

#### CR-M1-R1-004 - Activation diagnostics erase manifest failure identity

Finding ID: CR-M1-R1-004
Disposition: accepted
Status: open
Owner: M1 implementation
Owning stage: review-resolution
Chosen action: Use structured projection errors and retain source check, path, expectation, and reason through activation validation.
Rationale: PBS-R037 requires the actual affected resource and blocking reason.
Validation target: code-review-m1-r2
Validation evidence: pending

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
