# Code Review M3 R2: Correction Routing and Compatibility

Review ID: code-review-m3-r2
Stage: code-review
Round: r2
Reviewer: Independent Codex code-review agent
Target: corrected M3 implementation commit `128e70c6`; lifecycle return commit `27fb4c7e` contains Workflow-owned rereview state only
Reviewed artifact: complete M3 implementation `f2c69a20b89399b12b41ee7565113a32bd4dd30e..128e70c6` and correction `2c5ed673..128e70c6`
Review date: 2026-09-01
Status: changes-requested
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review, `review-invocation-code-review-m3-r2.yaml`, `review-log.md`, and `review-resolution.md`
- Open blockers: `FV-M3-CR2`, `FV-M3-CR3`
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: `FV-M3-CR3`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/reviews/code-review-m3-r2.md`
- Review log: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/review-log.md`
- Review resolution: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/review-resolution.md`
- Reviewed milestone: M3
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3, M4, M5
- Required review-resolution: yes
- Finding IDs: `FV-M3-CR3`
- Verify readiness: not-claimed

## Scope and authority

This rereview independently inspected the original M3 implementation and the complete correction through `128e70c6` against approved Design Review `design-review-r1`, Delivery Review `delivery-review-r1`, M3 TG-10 through TG-14, FV-R1 through FV-R3 and FV-R23 through FV-R34, plus the applicable state, authority, temporal, recovery, and compatibility boundaries. It traced both prior findings through the actual lifecycle request validator, transaction evaluator, stored correction state, return operation, automation consumer, and v1/v2 compatibility surface. The Workflow-owned return commit was read only to confirm the authorized R2 state.

The implementation remained untouched during review.

## R1 finding reconciliation

| Finding | R2 classification | Evidence |
| --- | --- | --- |
| `FV-M3-CR1` | resolved | V3 now requires exactly `review-recorded`, rejects any explanation or handoff revision, and directly rejects the legacy `complete` S-R-E object. The same S-R-E object remains accepted by the v1/v2 default guard. |
| `FV-M3-CR2` | failed-remediation | The owner classifier now has executable consumers, but v3 artifact-owner returns bypass their declared Design or Delivery rereview and the expanded verification-only reason vocabulary leaks into v2 routing. |

## Continuing material finding

`FV-M3-CR2` remains open because its original required outcome is not yet satisfied. R2 records the failed remediation evidence under the new stable occurrence identity `FV-M3-CR3`.

Finding ID: FV-M3-CR3
Severity: major
Location: `packages/rigorloop/dist/lib/lifecycle-contract.js:144-180,381-393,506-548`; `packages/rigorloop/dist/lib/lifecycle-operations.js:488-611`; `packages/rigorloop/test/lifecycle-correction-route.test.js:650-705`
Evidence: First, verification-only reasons were added to the global request vocabulary, while the evaluator restricts their meaning only when the contract is v3 and the source is Verify. A public-request reproduction using an exact v2 change accepted and routed `reason: implementation-defect` from Verify to spec. This changes v2 correction behavior instead of keeping the new reason vocabulary v3-only. Second, a v3 system-requirement correction can declare `return_stage: design-review`, update and register the spec with authoring-only evidence, then call `return-correction`; the artifact-return branch ignores `route.return_stage`, restores the snapshot source, and returned directly to Verify without a Design Review result. The plan-allocation route has the corresponding Delivery Review escape. The committed seven-owner test calls `evaluateLifecycleOperation` directly for route creation only; it does not exercise the public CLI transaction, return operation, no-mutation failures, or v2 reason isolation. This violates the remaining FV-R23-FV-R25/FV-R30 outcome, TG-11/TG-12, BND-AUTH-001, BND-RECOVERY-001, BND-COMPAT-001, and INT-002.
Required outcome: All seven v3 finding kinds must route through the public transaction to exactly one non-Verify owner and complete their required review boundary before Verify can be re-entered; wrong, unknown, and Verify-owned routes must fail without mutation; verification-only reasons and destinations must not become valid v1/v2 semantics.
Safe resolution path: Make verification correction reason validity contract- and source-keyed in the transaction, preserve the preexisting v1/v2 reason set, and make spec/architecture/plan returns stop at their declared consolidated review stage until a current approved Design or Delivery package authorizes return to Verify. Add public CLI/request-path tests for all seven route-and-return flows, wrong/unknown/Verify-owner no-mutation cases, and explicit v1/v2 rejection of every verification-only reason.
needs-decision rationale: none; the approved owner, rereview, and compatibility boundaries already determine the required behavior.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | CR1 is resolved, but two CR2 recovery and compatibility outcomes remain incorrect. |
| Test coverage | block | Named suites pass; the new matrix stops at the internal route evaluator and misses public return and v2 leakage. |
| Edge cases | block | Artifact-owner rereview and contract-version reason isolation change outcomes. |
| Error handling | concern | Unknown and wrong owners fail in the v3 evaluator, but verification-only reasons are not rejected for v2. |
| Architecture boundaries | block | Workflow can re-enter Verify without the required Design or Delivery rereview. |
| Compatibility | block | Active v2 admits a newly introduced verification-only correction reason. |
| Security/privacy | pass | No credential, secret, network, or path-authority expansion was found. |
| Derived artifact currency | pass | Node and Python owner maps agree; publication and activation remain later milestones. |
| Unrelated changes | pass | The implementation correction is scoped to CR1/CR2 and its evidence. |
| Validation evidence | concern | Broad commands pass, but the direct composed probes falsify the claimed closure. |

## Validation performed

- `node --test packages/rigorloop/test/lifecycle-contract.test.js packages/rigorloop/test/lifecycle-read.test.js packages/rigorloop/test/lifecycle-stage-advance.test.js packages/rigorloop/test/lifecycle-correction-route.test.js packages/rigorloop/test/lifecycle-transaction.test.js` — 86 passed, 2 historical skips.
- `python scripts/test-workflow-automation.py` — 78 passed.
- `python scripts/test-workflow-automation-policy.py` — 20 passed.
- `python scripts/test-workflow-automation-state.py` — 70 passed.
- `python scripts/test-workflow-code-state.py` — 19 passed.
- `python scripts/test-review-artifact-validator.py` — 110 passed.
- V3 tail probe — exact S-R succeeds; legacy S-R-E fails for v3 and remains accepted by the legacy guard.
- V2 public-request/evaluator probe — `implementation-defect` validated and produced `status: routed` under `stage-owned-change-local-v2`.
- V3 artifact-return probe — `system-requirement-gap` declared Design Review but produced `status: returned` with actual stage Verify and no Design Review recorded.

## No automatic handoff

M3 cannot close through `complete-milestone` because `FV-M3-CR2` and failed-remediation finding `FV-M3-CR3` remain material. This review records the failed remediation before any further correction. Workflow must route the bounded M3 correction and return the complete slice for R3.

## Handoff

- Reviewed milestone: M3
- Review status: changes-requested
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3, M4, M5
- Required review-resolution: yes
- Recommended next stage: Workflow routes `FV-M3-CR2` and `FV-M3-CR3` to M3 implementation ownership, then requests Code Review M3 R3.
- Final closeout readiness: not ready; M3 remains open and M4-M5 remain planned.
