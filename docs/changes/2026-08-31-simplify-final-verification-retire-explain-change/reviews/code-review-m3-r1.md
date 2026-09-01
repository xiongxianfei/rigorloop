# Code Review M3 R1: V3 Routing, Correction Ownership, and PR Consumption

Review ID: code-review-m3-r1
Stage: code-review
Round: r1
Reviewer: Independent Codex code-review agent
Target: M3 implementation commit `e0530499`
Reviewed artifact: committed implementation diff `f2c69a20b89399b12b41ee7565113a32bd4dd30e..e0530499`; handoff commit `eb673483` contains review-requested state only
Review date: 2026-09-01
Status: changes-requested
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review, `review-invocation-code-review-m3-r1.yaml`, `review-log.md`, and `review-resolution.md`
- Open blockers: `FV-M3-CR1`, `FV-M3-CR2`
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: `FV-M3-CR1`, `FV-M3-CR2`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/reviews/code-review-m3-r1.md`
- Review log: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/review-log.md`
- Review resolution: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/review-resolution.md`
- Reviewed milestone: M3
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3, M4, M5
- Required review-resolution: yes
- Finding IDs: `FV-M3-CR1`, `FV-M3-CR2`
- Verify readiness: not-claimed

## Scope and authority

Reviewed the exact committed M3 product diff against approved Design Review `design-review-r1`, Delivery Review `delivery-review-r1`, M3 TG-10 through TG-14, FV-R1 through FV-R3 and FV-R23 through FV-R34, plus BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001, INT-002, and INT-003. The review inspected the complete changed runtime, automation, policy, state, protocol, test, and evidence surfaces and expanded into existing correction operations and canonical code-state semantics because M3's new helpers must compose with those boundaries.

The formal review is isolated from implementation repair. It records findings and review evidence only; Workflow owns correction routing and lifecycle mutation.

## Actual-diff summary

- Adds an inactive v3 policy graph that removes `test-spec` and `explain-change` and adds final holistic Code Review directly to Verify.
- Makes verification readiness contract-keyed and removes the standalone explanation input for v3.
- Adds closed Verify-finding-to-owner maps in JavaScript and Python.
- Adds exact Verify-report-to-PR handoff evaluators with report, basis, explanation, and authoritative-reference equality checks.
- Extends automation/state tests for v3 phase boundaries, unknown contracts, direct Verify routing, and unchanged v1/v2 behavior.
- Leaves the activation manifest preactivation and makes no current public v3 route authoritative.

## Material findings

## Finding FV-M3-CR1

Finding ID: FV-M3-CR1
Severity: major
Location: `scripts/workflow_automation.py:413-423`; `scripts/workflow_code_state.py:579-636`; `scripts/test-workflow-code-state.py:25-40`
Evidence: The v3 branch of `require_complete_ordered_evidence_tail` accepts both `review-recorded` and legacy `complete`. In the canonical code-state model, `complete` specifically means a second post-review `explanation_recording_revision` was found, validated as the standalone explanation commit, and selected as `handoff_revision`. A reviewer probe constructed that exact S -> R -> E state and the v3 readiness guard accepted it. The only new v3 test proves `review-recorded` succeeds; it does not reject `complete`. This allows the retired explain-change evidence tail to remain admissible to v3 Verify, contrary to FV-R1, FV-R2, FV-R28, FV-R31-FV-R34, TG-10, TG-12, BND-STATE-001, BND-TEMPORAL-001, and INT-003.
Required outcome: V3 verification readiness must accept exactly the final-review-recorded S -> R pre-Verify state and reject any legacy explanation commit or other second pre-Verify evidence commit; v1/v2 must retain their exact S -> R -> E requirement.
Safe resolution path: Require `tail_state == "review-recorded"`, require `explanation_recording_revision` and `handoff_revision` to be absent for v3, and add direct resolver plus repository-backed tests showing S -> R passes, S -> R -> E fails for v3, and the same S -> R -> E tail remains required for v1/v2.
needs-decision rationale: none; the approved graph and ADR already fix the v3 S -> R -> V identity.

## Finding FV-M3-CR2

Finding ID: FV-M3-CR2
Severity: major
Location: `packages/rigorloop/dist/lib/lifecycle-contract.js:171-179,386-394,559-561`; `packages/rigorloop/dist/lib/lifecycle-operations.js:464-505`; `scripts/workflow_automation_policy.py:634-652`
Evidence: M3 adds closed owner lookup helpers, but no production routing path calls either helper. Repository search finds only the two definitions and their unit tests. The existing lifecycle `route-correction` operation still admits only proposal/spec/architecture/design-review/plan/test-spec destinations, so four approved Verify owners (`implement`, `code-review`, `ci-maintenance`, and `external-evidence-acquisition`) cannot be selected by that supported transaction at all. The tests prove a dictionary lookup, not TG-11's owner-correction route, rereview, or external-acquisition behavior. Consequently a Verify finding can be named but cannot enter the required exact owner flow through the implemented graph. This violates FV-R23-FV-R25, FV-R30, TG-11, TG-12, BND-AUTH-001, BND-RECOVERY-001, and INT-002.
Required outcome: Every closed Verify finding kind must compose with one executable Workflow-owned correction route to its exact non-Verify owner, with the required rereview/return boundary and fail-closed unknown handling; Verify must remain unable to mutate or repair.
Safe resolution path: Integrate the owner classifier into the contract-keyed Workflow/lifecycle correction transaction, extend the permitted destination and external-acquisition representation deliberately for v3, and add public/request-path tests for all seven owners, unknown kinds, wrong owners, Verify-as-owner, return/rereview, and no-mutation-on-rejection while retaining exact v1/v2 behavior.
needs-decision rationale: none; owner identities and Workflow/Verify authority are already approved. If external evidence acquisition cannot be represented by the existing stage model, route that representation gap to the owning Design boundary rather than silently leaving it as an unused string.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | The visible v3 graph omits explain-change, but readiness still accepts an E tail and owner correction is not executable. |
| Test coverage | block | All planned suites pass, but TG-10/TG-12 lack negative S-R-E proof and TG-11 tests only lookup tables. |
| Edge cases | block | Legacy complete-tail reuse and four unrepresentable correction owners change v3 recovery outcomes. |
| Error handling | concern | Unknown finding kinds fail in helpers, but the helpers do not guard an actual routing transaction. |
| Architecture boundaries | block | The temporal S-R-V boundary and Workflow-owned correction boundary are not closed. |
| Compatibility | pass | Current v1/v2 suites remain green and v3 remains preactivation. |
| Security/privacy | pass | No credential, network, secret-output, or repository-path expansion was introduced. |
| Derived artifact currency | pass | Changed JavaScript/Python helpers and their tests agree; publication and activation remain later milestones. |
| Unrelated changes | pass | The diff is scoped to M3 routing, protocol, automation, tests, and evidence. |
| Validation evidence | concern | All named commands pass, but direct probes and consumer tracing disprove two completion claims. |

## Validation performed

- `node --test packages/rigorloop/test/lifecycle-contract.test.js packages/rigorloop/test/lifecycle-read.test.js packages/rigorloop/test/lifecycle-stage-advance.test.js packages/rigorloop/test/lifecycle-correction-route.test.js packages/rigorloop/test/lifecycle-transaction.test.js` — 84 passed, 2 skipped.
- `python scripts/test-workflow-automation.py` — 78 passed.
- `python scripts/test-workflow-automation-policy.py` — 20 passed.
- `python scripts/test-workflow-automation-state.py` — 70 passed.
- `python scripts/test-workflow-code-state.py` — 19 passed.
- `python scripts/test-review-artifact-validator.py` — 110 passed.
- `git diff --check f2c69a20b89399b12b41ee7565113a32bd4dd30e..e0530499` — passed.
- Reviewer S-R-E probe — v3 accepted a canonical `complete` state carrying `explanation_recording_revision=E` and `handoff_revision=E`.
- Production consumer trace — both correction-owner helpers have no caller outside tests; lifecycle correction destination validation excludes four mapped owners.

## No automatic handoff

This review records findings before repair. There is no automatic downstream handoff, no implementation edit, and no PR or Verify readiness claim. Neither finding needs a new product decision; both have bounded corrections under approved M3 authority, subject to an upstream Design correction only if external-evidence acquisition lacks an agreed lifecycle representation.

## Handoff

- Reviewed milestone: M3
- Review status: changes-requested
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3, M4, M5
- Required review-resolution: yes
- Recommended next stage: Workflow records `FV-M3-CR1` and `FV-M3-CR2`, routes the correction to M3 implementation ownership, and returns the complete corrected M3 diff for Code Review M3 R2.
- Final closeout readiness: not ready; M3 has two material findings and M4-M5 remain planned.
