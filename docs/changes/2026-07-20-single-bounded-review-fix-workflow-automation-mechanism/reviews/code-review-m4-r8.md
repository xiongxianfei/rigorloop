# Code Review: M4 R8 Route Binding Across Terminalization Paths

## Review metadata

Review ID: code-review-m4-r8
Stage: code-review
Round: M4 R8
Reviewer: same-session independent-review reset
Target: M4 correction commit `4340d3d0`
Reviewed artifact: commit `4340d3d0`
Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
Review mode: isolated direct formal review
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-23
Recording status: recorded
Material findings: BRF-M4-CR15
Immediate next stage: review-resolution M4

Automated review: no
Review gate outcome: stop
Native review status: changes-requested
Independence level: L0
Reviewer context ID: root-m4-r8-review-reset
Context separation mechanism: The direct formal review used an explicit review-phase reset and inspected the committed production diff and governing clauses before validation summaries and prior-finding reconciliation.
Risk tier: elevated
Risk-tier triggers: Executable correction authority, durable review-route evidence, receipt immutability, and cancellation reconciliation changed or became jointly binding.
Risk-tier classifier: Approved review-independence risk-tier contract.
Governing artifacts: `specs/single-bounded-review-fix-workflow-automation.md`; `specs/single-bounded-review-fix-workflow-automation.test.md`; `docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md`; approved workflow architecture and ADR.
Formal criteria: Code-review checklist; BRF-R007a, BRF-R047, BRF-R054, BRF-R069, BRF-R076, BRF-R100; T10, T11, and T16 proof.
Initial packet inventory: scripts/workflow_automation_state.py@4340d3d0#sha256:2c27bd1beb9214097ff3688e34392416a254ff5cb49dc6685157b64eefbf6439; scripts/validate_workflow_automation.py@4340d3d0#sha256:241378c1358ae2883b243e2e5fbe3d341dc684713dc64e1c423dff4dcaa62ba2; scripts/test-workflow-automation-state.py@4340d3d0#sha256:7c654894260c87ce0859b9730ae171e6ba4b5e13814c7ed6f467f7d044570a38; specs/single-bounded-review-fix-workflow-automation.md@4340d3d0#sha256:59241a5e4968a0d6ba60f9772eed56ab8b9e79859a0be1c94e7c77840c724070; specs/single-bounded-review-fix-workflow-automation.test.md@4340d3d0#sha256:e73ac1691966e7f17c1d1342b969681ae660b8a283e2f0130078c564a37e21bd; docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md@4340d3d0#sha256:77bd2a7647f673c57a63476a19a11dc3196b60e0b56b77e0841d5bb139ac2783
Initial packet contains prohibited context: no
Prompt template version: code-review-v1
Initial packet hash: sha256:019dbfd7167b39f5b286211062a175bcba7c4b23126574346b18cdba5fc55729
Manifest owner: direct reviewer
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded

Affected behavior: Proposal-review finalization now binds route evidence to one completed receipt, all terminal receipts are immutable, and cancellation may reconcile prepared completion before terminalizing the run.
Highest-impact failure modes: Wrong historical receipt binding; later authority fabrication; alternate terminalization without route evidence; and immutable incomplete receipts.
Changed boundaries: Proposal-review finalizer to receipt; receipt to latest result; validator to exact source transition; state replacement to terminal immutability; cancellation reconciliation to completed receipt.
Evidence expected: Exact source mismatch, explicit absence, active-to-consumed liveness, retroactive rewrite rejection, receipt tampering, and proposal-review completion through normal and cancellation paths.
Areas requiring direct inspection: `resolve_recorded_proposal_correction_capability`; proposal-review finalization; `replace_automation`; cancellation reconciliation; validator presence conditions; cancellation tests.
Areas intentionally out of scope: M5, M6, public routing, compatibility cutover, generated adapters, external actions, final verification, and PR readiness.
Risk classes considered: authorization bypass=applicable; durable-state contradiction=applicable; recovery/idempotency=applicable; compatibility=applicable; review independence=applicable; privacy=not-applicable; deployment=not-applicable
Falsifiable review questions: Can any supported path complete proposal review without route binding? Does cancellation preserve verifier-derived route facts? Does validation reject an incomplete completed occurrence? Can terminal immutability freeze the omission?

Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: `scripts/workflow_automation_state.py`; `scripts/validate_workflow_automation.py`; proposal-review and cancellation tests; their change-local review evidence
Requirement-fidelity matched path triggers: scripts/*validator*, docs/changes/**/reviews/, docs/changes/**/review-*.md
Requirement-fidelity matched category triggers: autoprogression gates, review-recording contracts, workflow routing contracts, closed enums
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause, property decomposition, production diff, tests, validation evidence, prior findings

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, review log, review resolution, active plan, plan index, and change metadata
- Open blockers: `BRF-M4-CR15` blocks M4 closeout
- Next stage: review-resolution M4
- Review status: changes-requested
- Material findings: `BRF-M4-CR15`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m4-r8.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m4-r8`
- Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M4 resolution and rereview, M5, M6
- Required review-resolution: yes
- Finding IDs: `BRF-M4-CR15`
- Verify readiness: not-claimed

## Invocation manifest

Manifest owner: direct reviewer
Review target identity: `4340d3d086adf26d6a768ed0972e3971c262e2e5`
Initial packet: actual commit diff; tracked M4 handoff; approved BRF-R007a, BRF-R047, BRF-R054, BRF-R069, BRF-R076, and BRF-R100 clauses; T10, T11, and T16 proof contracts; formal code-review criteria
Forbidden initial context excluded: author reasoning and self-assessment, desired verdict, prior reviewer conclusions and findings, validation summaries, evidence menu, and correction eligibility
Reviewer did not edit reviewed implementation target: true

## Phase receipts

| Phase | Status | Evidence |
| --- | --- | --- |
| neutral-initial-packet | recorded | Commit diff and governing clauses were inspected before validation summaries and R7 reconciliation. |
| risk-map-recorded | recorded | Alternate terminalization, especially cancellation reconciliation, was identified as the highest-risk boundary before evidence results were consulted. |
| evidence-challenge | recorded | A direct temporary-state probe reconciled a valid prepared proposal-review during cancellation and produced a completed receipt with no route binding or latest review result; canonical validation returned no errors. |
| prior-finding-reconciliation | recorded | `BRF-M4-CR14` is a failed remediation across the complete terminalization surface; normal finalization is fixed, but cancellation reconciliation bypasses and permanently freezes incomplete route evidence. |
| requirement-fidelity | recorded | The implementation was compared with BRF-R007a, BRF-R047, BRF-R054, BRF-R069, BRF-R076, BRF-R100, T10, T11, and T16. |
| verdict-recorded | recorded | One actionable major finding requires bounded M4 review-resolution and rereview. |

## Independent risk map

### Affected behavior

- Normal proposal-review finalization records an occurrence-bound route on the completed receipt.
- `latest_review_result` references the source transition used by durable validation.
- Every terminal receipt becomes immutable at the sole writer.
- Cancellation can reconcile a prepared stage completion before making the run terminal.

### Highest-impact failure modes

1. A route result references the wrong historical review receipt.
2. Later authority manufactures a correction-loop route.
3. A coherent result-and-receipt rewrite bypasses static validation.
4. Resume or cancellation terminalizes proposal review without the new route binding.
5. Terminal immutability permanently freezes incomplete occurrence evidence.

### Changed boundaries

- Proposal-review finalization to completed receipt.
- Completed receipt to latest review result.
- State validator to exact source transition.
- Generic state replacement to finalized-receipt immutability.
- Cancellation reconciliation to completed receipt and terminal run.

### Evidence expected

- Exact source-transition mismatch rejection.
- Explicit correction-capability absence and selected-capability identity.
- Active-to-consumed correction liveness.
- Retroactive route rewrite rejection after later authority appears.
- Receipt tamper rejection at validation and write boundaries.
- Proposal-review completion through normal finalization, resume, and cancellation reconciliation.

### Direct-inspection areas

- `scripts/validate_workflow_automation.py:190-320`.
- `scripts/validate_workflow_automation.py:926-956`.
- `scripts/validate_workflow_automation.py:1560-1630`.
- `scripts/workflow_automation_state.py:794-830`.
- `scripts/workflow_automation_state.py:985-1046`.
- `scripts/workflow_automation_state.py:1064-1115`.
- `scripts/test-workflow-automation-state.py:1122-1148`.

### Scope boundaries

M4 internal proposal review, correction authority, durable state, recovery, and cancellation reconciliation are in scope.
M5, M6, public routing, compatibility cutover, generated adapters, external actions, final verification, and PR readiness are out of scope.

### Risk-class assessment

| Risk class | Applicability | Reason |
| --- | --- | --- |
| Authorization bypass | applicable | Missing explicit absence can erase proof that correction authority was unavailable at route time. |
| Durable-state contradiction | applicable | A completed proposal-review receipt may lack the route evidence required by the new validator model. |
| Recovery/idempotency | applicable | Cancellation reconciliation is a supported completion path and now freezes terminal receipts. |
| Compatibility/migration | applicable | The correction must preserve pre-public unified-state and legacy-read behavior. |
| Review independence | applicable | Every route must remain bound to the exact formal review occurrence. |
| External-action safety | not directly applicable | The M4 harness remains non-public and cancellation is repository-local. |
| Privacy/secret exposure | not applicable | No credential, telemetry, or user-data path changed. |
| Deployment/performance | not applicable | The changed behavior is local state validation and persistence. |

### Falsifiable review questions

1. Can any supported path make a proposal-review receipt `completed` without `proposal_review_route`?
2. Does cancellation reconciliation preserve the same verifier-derived route facts as normal finalization?
3. Does canonical validation reject a completed proposal-review occurrence with no source-linked latest result?
4. Can terminal immutability prevent later repair of an incomplete receipt?

## Diff summary

Commit `4340d3d0` adds a shared route-binding projection, writes that binding during normal proposal-review finalization, records `source_transition_id` on the latest result, validates the exact completed source receipt, rejects later-authority result rewrites, and makes every finalized receipt immutable in `replace_automation`.

The added tests cover normal route finalization, active-to-consumed correction, later-authority rewrite rejection, route-binding mismatch, wrong source identity, and coherent terminal-receipt rewrite rejection at the writer boundary.

## Prior-finding reconciliation

| Prior finding | R8 result | Evidence |
| --- | --- | --- |
| `BRF-M4-CR14` | failed-remediation with residual defect recorded as `BRF-M4-CR15` | Normal `finalize_transition` now records and validates the exact route binding. The separate cancellation reconciliation path still changes a proposal-review receipt from prepared to completed without either the route binding or latest review occurrence; validation accepts it, and terminal immutability prevents later repair. |

## Findings

## Finding BRF-M4-CR15

Finding ID: BRF-M4-CR15
Severity: major
Location: `scripts/workflow_automation_state.py:1064-1115`; `scripts/validate_workflow_automation.py:926-956,1560-1630`; `scripts/test-workflow-automation-state.py:1122-1148`
Evidence: `cancel()` reconciles valid prepared completion by directly setting the receipt to `completed`, persisting verifier outputs and canonical identities, and consuming its capability. Unlike normal `finalize_transition`, it does not project `proposal_review_route` or `latest_review_result`. The validator checks source binding only when `latest_review_result` already exists, so it does not reject the omission. A direct temporary-state probe used the existing valid proposal-review completion fixture, invoked cancellation, and observed `cancel_status=cancelled`, `receipt_status=completed`, `has_route_binding=False`, `has_latest_review_result=False`, and `validation_errors=[]`. The new terminal-receipt immutability rule then prevents the incomplete completed receipt from being repaired through the sole writer.
Required outcome: Every supported path that reconciles a proposal-review occurrence to `completed` must atomically preserve its exact verifier-derived outcome, target, proposal identity, review-record identity, selected correction capability or explicit absence, and source-transition relationship, while cancellation still reaches its required terminal run state.
Safe resolution path: Factor proposal-review completion projection into one state-writer helper used by normal finalization and cancellation reconciliation; persist the route binding and source-linked review occurrence before applying cancellation. Extend durable validation so a completed proposal-review receipt cannot exist without its route binding and exact occurrence linkage. Define the canceled-run exception explicitly so a valid recorded review route can coexist with terminal cancellation without being mistaken for the current run-routing status. Add a regression to `test_cancel_reconciles_valid_prepared_completion_then_cancels` that proves the exact binding, rejects missing binding/result state, preserves receipt immutability, revokes authority, and leaves `run.status: cancelled`.
needs-decision rationale: none; this is a bounded completion of the accepted BRF-R007a, BRF-R047, BRF-R054, BRF-R069, BRF-R076, and BRF-R100 contracts.

auto_fix_class: none

## Requirement fidelity

| Requirement property | Result | Evidence |
| --- | --- | --- |
| BRF-R007a reconcile before cancellation | block | Reconciliation records stage output but omits required proposal-review occurrence routing facts. |
| BRF-R047 complete durable review occurrence | block | Cancellation completion records no route action, clean-gate state, or source-linked latest result. |
| BRF-R054 explicit route-time correction authority | block | Cancellation loses the selected capability or explicit-absence evidence. |
| BRF-R069 complete receipt evidence | block for the accepted route-binding extension | The completed receipt lacks the route binding added to normal finalization. |
| BRF-R076 completed receipt consistency and recovery | block | The incomplete receipt is accepted and then made immutable. |
| BRF-R100 tracked receipt-based resume | block | Tracked state cannot distinguish a fully projected review occurrence from cancellation's partial terminalization. |
| T10-T11 route and correction proof | pass for normal finalization | Normal finalization covers exact source, explicit absence, later authority, and active-to-consumed cases. |
| T16 prepared-work cancellation proof | block | The existing test asserts status, consumption, and log identity but not proposal-review route preservation. |

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | BRF-R007a and BRF-R047 are not jointly satisfied on cancellation reconciliation. |
| Test coverage | block | The named T16 fixture exercises the failing path but omits the new route-integrity assertions. |
| Edge cases | block | A prepared proposal-review that finishes concurrently with cancellation produces incomplete terminal evidence. |
| Error handling | block | Canonical validation returns no errors for the incomplete completed receipt. |
| Architecture boundaries | concern | The sole writer is respected, but duplicated completion logic lets cancellation bypass the shared route projection. |
| Compatibility | pass with follow-up | Public commands, legacy aliases, M5/M6, and external actions are unchanged; the fix should remain internal to the existing state boundary. |
| Security/privacy | block for authorization integrity | No secret exposure exists, but explicit absence of correction authority is lost. |
| Derived artifact currency | pass | No generated output is part of the reviewed patch. |
| Unrelated changes | pass | The commit is limited to M4 routing integrity, tests, and lifecycle evidence. |
| Validation evidence | block for sufficiency | Focused and broad suites passed, but the existing cancellation test did not assert the new invariant. |

## Validation and direct proof

- Direct cancellation probe: valid prepared proposal-review completion reconciled to a cancelled run with a completed receipt, no `proposal_review_route`, no `latest_review_result`, and zero validator errors.
- Source inspection confirms normal finalization uses `proposal_review_route_binding`, while `cancel()` has separate direct receipt mutation.
- `test_cancel_reconciles_valid_prepared_completion_then_cancels` covers the exact path but asserts only terminal status, capability consumption, and canonical review-log identity.
- Recorded validation evidence shows the implementation suites and broad smoke passed; this does not cover the missing T16 route-integrity assertion.

## No-finding rationale

Not applicable; this review has one material finding.

## Residual risks

Rereview must prove route evidence parity across normal finalization and cancellation reconciliation without weakening cancellation terminality or finalized-receipt immutability.

M5, M6, final holistic review, verification, and PR readiness remain outside this review.

## Milestone handoff

- Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `BRF-M4-CR15`
- Remaining in-scope implementation milestones: M4 resolution and rereview, M5, M6
- Next stage: review-resolution M4
- Final closeout readiness: not ready because M4 has one open material finding and M5-M6 remain unimplemented
- Verify readiness: not-claimed
- Isolation: this direct review performs no automatic downstream handoff
