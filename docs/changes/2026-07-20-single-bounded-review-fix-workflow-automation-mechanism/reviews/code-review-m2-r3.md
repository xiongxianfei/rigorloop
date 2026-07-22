# Code Review M2 R3

Review ID: code-review-m2-r3
Stage: code-review
Round: M2 R3
Reviewer: Codex code-review skill
Target: M2 correction commit `f9ba90d2`
Reviewed artifact: M2 correction commit `f9ba90d2`
Reviewed milestone: M2. Sole State Writer, Prepared Receipts, and Recovery
Status: clean-with-notes
Review status: clean-with-notes
Review date: 2026-07-22
Recording status: recorded
Material findings: None
Immediate next stage: implement M3

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review receipt, review log, review-resolution summary, active plan, plan index, and change metadata
- Open blockers: none for M2
- Next stage: implement M3
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m2-r3.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: not-required; the prior R2 finding resolution remains closed
- Reviewed milestone: M2. Sole State Writer, Prepared Receipts, and Recovery
- Milestone closeout: closed
- Remaining implementation milestones: M3, M4, M5, M6
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed

## Review Inputs

- Diff surface: commit range `1430d268..f9ba90d2`, with blind-first inspection of the changed state, validator, and test modules before consulting R2 conclusions or implementation validation.
- Tracked governing branch state: clean worktree at `f9ba90d2` before R3 evidence recording.
- Governing spec: `specs/single-bounded-review-fix-workflow-automation.md`, especially `BRF-R068`-`BRF-R077`.
- Test spec: T14 and T15, including deterministic capability-bound receipts and validator-valid proof for every retry policy.
- Architecture and ADR: the accepted sole-writer, canonical state-read, immutable policy, and capability-bound recovery boundaries.
- Active plan: M2 `review-requested` handoff in `docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md`.

## Risk Map

- Affected behavior: persisted transition-key validation and retry-policy recovery proof.
- Highest-impact failures: accepting a stale key after immutable inputs change, projecting malformed state as valid status, retrying under receipt-supplied authority, or proving retry behavior with states canonical validation would reject.
- Changed boundaries: canonical automation validation, direct recovery evaluation, cancellation/status reads, and the three retry-family fixtures.
- Direct proof expected: prepared and completed stale-key rejection, recovery and query rejection without mutation, order-independent key computation, all key-bound inputs changing the key, canonical-read success for each retry family, and policy-mismatch rejection.
- Intentionally out of scope: M3-M6 orchestration, public routing, stage invocation, adapters, final holistic review, and external actions.
- Applicable risk classes: workflow correctness, durable-state integrity, fail-closed recovery, compatibility, and proof validity. Security/privacy and generated-output risks are non-applicable to this correction slice.

## Diff Summary

The correction centralizes deterministic transition-key computation in the canonical automation validator and makes persisted receipt validation recompute the key from nine immutable operation inputs.
The state recovery evaluator performs the same check before receipt-status, capability, policy, evidence, or retry decisions.

State tests now reject stale prepared and completed receipts, direct recovery rejects stale keys, cancellation preserves bytes on stale state, and the query helper reports invalid automation without mutation.
The retry-family proof now builds complete architecture-assessment, proposal-review, and `implement@M2` states, reads each through `WorkflowAutomationStateStore`, and proves both the expected recovery result and mismatch rejection.

## Prior-Finding Reconciliation

| Finding | R3 result | Evidence |
| --- | --- | --- |
| `BRF-M2-CR5` | resolved | Canonical validation recomputes the transition key at `scripts/validate_workflow_automation.py:1115`; recovery rejects mismatches before further evaluation at `scripts/workflow_automation_state.py:200`; prepared/completed read, recovery, cancellation, and query regressions pass. |
| `BRF-M2-CR6` | resolved | `scripts/test-workflow-automation-state.py:201` constructs all three stage-appropriate states, requires canonical read success, and proves the registry-derived retry result plus per-family mismatch rejection. |

## Findings

No blocking or required-change findings.

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | Deterministic receipt identity and policy-bounded recovery now enforce `BRF-R068`-`BRF-R077` at the canonical state boundary. |
| Test coverage | pass | Focused tests cover prepared/completed stale keys, recovery, cancellation, status projection, key ordering, all retry families, and mismatch rejection. |
| Edge cases | pass | Direct R3 proof changed each of the nine key-bound inputs; every change altered the key and failed validation. Unknown policy versions fail earlier at the required closed-vocabulary gate. |
| Error handling | pass | Stale or uncomputable keys fail closed before projection, mutation, or retry; invalid retry projections are rejected by canonical read. |
| Architecture boundaries | pass | One canonical helper is consumed by the validator and sole state adapter; no second writer, policy registry, or workflow cursor was introduced. |
| Compatibility | pass | No public command, legacy adapter, schema version, or migration behavior changed. |
| Security/privacy | pass | The diff adds no secret, network, authentication, logging, credential, or external-action surface. |
| Derived artifact currency | pass | No generated adapter or derived public artifact is in scope. |
| Unrelated changes | pass | The correction is limited to M2 state integrity, proof fixtures, and lifecycle evidence. |
| Validation evidence | pass | R3 independently reran the focused and full validator suites and challenged every transition-key field; recorded implementation broad smoke covers the wider repository surface. |

## No-Finding Rationale

No material finding remains because persisted receipt identity is now checked at every canonical read before status, cancellation, or recovery can act, and recovery independently retains the same fail-closed check.
The corrected retry tests no longer bypass the persistence contract: all three policy families pass canonical state validation before their decisions are asserted, and mismatched projections fail at that same boundary.

## Direct Proof and Validation Challenge

- `python scripts/test-workflow-automation-state.py` passed 30 tests.
- `python scripts/test-validate-workflow-automation.py -k receipt` passed 18 selected tests.
- `python scripts/test-validate-workflow-automation.py` passed 49 tests.
- `python scripts/test-query-change-record.py` passed 19 tests.
- `python scripts/test-change-metadata-validator.py` passed 53 tests.
- Python compilation and `git diff --check 1430d268..f9ba90d2` passed.
- The direct nine-field mutation matrix confirmed every immutable input changes the transition key and causes validation failure.
- The implementation record reports 11 repository broad-smoke checks passed in 408 seconds; R3 independently challenged its adequacy with the focused suites and mutation matrix.

## Clean-Review Sufficiency

- Target identity: commit `f9ba90d2`, M2 correction after R2.
- Independence level: direct isolated review with intentional assumption reset and blind-first code/test inspection.
- Governing artifacts inspected: approved spec, active test spec, accepted architecture and ADR boundaries, active plan, and R2 resolution after the blind-first pass.
- Adversarial hypotheses tested: stale-key survival, canonicalization drift, missing key coverage, retry authority widening, invalid-state proof, status mutation, and unrelated public behavior change.
- Unreviewed surfaces: M3-M6 routing, stage execution, adapters, public activation, final holistic interactions, and release behavior remain later milestones.
- Confidence: high for the M2 state-integrity and recovery boundary.

## Residual Risks

Live command normalization, canonical position resolution, capability derivation, stage invocation, migration adapters, and public activation remain intentionally assigned to M3-M6.
This clean milestone review does not establish final verification or PR readiness.

## Milestone Handoff

- Reviewed milestone: M2. Sole State Writer, Prepared Receipts, and Recovery
- Review status: clean-with-notes
- Milestone state after review: closed
- Required review-resolution: no; all 40 prior findings are resolved
- Remaining in-scope implementation milestones: M3, M4, M5, M6
- Next stage: implement M3
- Final closeout readiness: not ready; four implementation milestones, final holistic review, explanation, verification, and PR handoff remain.

This direct review is isolated and does not start M3 automatically.
