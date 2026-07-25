# Code Review: M4 R7 Historical Route Binding

## Review metadata

Review ID: code-review-m4-r7
Stage: code-review
Round: M4 R7
Reviewer: same-session independent-review reset
Target: M4 correction commit `2d4b3b56`
Reviewed artifact: commit `2d4b3b56`
Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
Review mode: isolated direct formal review
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-23
Recording status: recorded
Material findings: BRF-M4-CR14
Immediate next stage: review-resolution M4

Automated review: no
Review gate outcome: stop
Native review status: changes-requested
Independence level: L0
Reviewer context ID: root-m4-r7-review-reset
Context separation mechanism: The direct formal review used an explicit review-phase reset and inspected the committed production diff and governing clauses before validation results and prior-finding reconciliation.
Risk tier: elevated
Risk-tier triggers: Executable correction authority, durable historical review state, and receipt-to-route identity binding changed.
Risk-tier classifier: Approved review-independence risk-tier contract.
Governing artifacts: `specs/single-bounded-review-fix-workflow-automation.md`; `specs/single-bounded-review-fix-workflow-automation.test.md`; `docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md`; approved workflow architecture and ADR.
Formal criteria: Code-review checklist; BRF-R047, BRF-R054, BRF-R066, BRF-R069, BRF-R076, BRF-R099, BRF-R100; M4 T10-T12 and CMD15-CMD20 proof.
Initial packet inventory: scripts/validate_workflow_automation.py@2d4b3b56#sha256:5d4d46bae1597c7ad21433081817a7c91e69712f4f1da7f7e12c1d0c17040a55; scripts/workflow_automation_state.py@2d4b3b56#sha256:21c78dcf933daf5b6cc764b6f0a7de892d3d5b18798f3686d36f777cfeefb551; scripts/test-workflow-automation.py@2d4b3b56#sha256:ff808d2bedf7de7b027cb065dd0cf2a569c9e510d87c98851e8482f81d14a27c; specs/single-bounded-review-fix-workflow-automation.md@2d4b3b56#sha256:59241a5e4968a0d6ba60f9772eed56ab8b9e79859a0be1c94e7c77840c724070; specs/single-bounded-review-fix-workflow-automation.test.md@2d4b3b56#sha256:e73ac1691966e7f17c1d1342b969681ae660b8a283e2f0130078c564a37e21bd; docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md@2d4b3b56#sha256:c6f4b48987aba244ad7e0c8853b613d9ff37de6135da08253f97aa2245b10ce5
Initial packet contains prohibited context: no
Prompt template version: code-review-v1
Initial packet hash: sha256:778e9a1e7bad1bd130e23934a413cfbd5df1019525d1f5ca4fa1dea46291b6da
Manifest owner: direct reviewer
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded

Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: `scripts/validate_workflow_automation.py`; `scripts/workflow_automation_state.py`; `scripts/test-workflow-automation.py`; their change-local review evidence
Requirement-fidelity matched path triggers: scripts/*validator*, docs/changes/**/reviews/, docs/changes/**/review-*.md
Requirement-fidelity matched category triggers: autoprogression gates, review-recording contracts, workflow routing contracts, closed enums
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause, property decomposition, production diff, tests, validation evidence, prior findings

Affected behavior: Durable proposal-review validation now reads the recorded correction capability and searches for one completed proposal-review receipt after current capability status changes.
Highest-impact failure modes: A later capability can be retroactively presented as route-time authority; a recorded route can be rebound to a receipt that proves only occurrence; valid historical routing can become ambiguous; and route-time authorization can be bypassed by internally consistent state rewriting.
Changed boundaries: Proposal-review finalizer to `latest_review_result`; historical result to correction capability; historical result to completed proposal-review receipt; validator to run status and pause reason.
Evidence expected: Active-to-consumed stability; absent-to-active stability; retroactive route-rewrite rejection; exact receipt-to-route binding; stale capability and receipt rejection.
Areas requiring direct inspection: `resolve_recorded_proposal_correction_capability`; proposal-review finalization; completed receipt fields; inverse route-stability test; durable projection comparison.
Areas intentionally out of scope: M5 implementation and verification integration; M6 public cutover and compatibility adapters; final holistic review, verify, PR, and external actions.
Risk classes considered: authorization bypass=applicable; durable-state contradiction=applicable; recovery/idempotency=applicable; compatibility=applicable; review independence=applicable; privacy=not-applicable; deployment=not-applicable
Falsifiable review questions: Does the matching receipt identify the selected correction capability? Can later authority plus a rewritten result validate as correction-loop? Does durable validation use persisted route evidence rather than the route action to choose its own proof?

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, review log, review resolution, active plan, plan index, and change metadata
- Open blockers: `BRF-M4-CR14` blocks M4 closeout
- Next stage: review-resolution M4
- Review status: changes-requested
- Material findings: `BRF-M4-CR14`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m4-r7.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m4-r7`
- Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M4 resolution and rereview, M5, M6
- Required review-resolution: yes
- Finding IDs: `BRF-M4-CR14`
- Verify readiness: not-claimed

## Invocation manifest

Manifest owner: orchestrator
Review target identity: `2d4b3b56a414add2d74a28a7775d218510831dec`
Initial packet: actual commit diff; tracked active-plan handoff and M4 scope; approved BRF-R047, BRF-R054, BRF-R066, BRF-R069, BRF-R076, BRF-R099, and BRF-R100 clauses; active T10-T12 proof contracts; formal code-review criteria
Forbidden initial context excluded: author reasoning and self-assessment, desired verdict, prior reviewer conclusions and findings, validation summaries, evidence menu, and correction eligibility
Reviewer did not edit reviewed implementation target: true

## Phase receipts

| Phase | Status | Evidence |
| --- | --- | --- |
| neutral-initial-packet | recorded | Commit diff and governing clauses were inspected before validation evidence and prior-finding reconciliation. |
| risk-map-recorded | recorded | The independent risk map below was recorded before focused test results and R6 reconciliation. |
| evidence-challenge | recorded | Focused suites passed, but a direct state transition proved that a later capability can validate a retroactively rewritten correction-loop route. |
| prior-finding-reconciliation | recorded | `BRF-M4-CR13` fixed active-to-consumed liveness but its inverse historical-integrity remediation is incomplete; the residual defect is recorded separately as `BRF-M4-CR14`. |
| requirement-fidelity | recorded | The diff was compared with BRF-R047, BRF-R054, BRF-R066, BRF-R069, BRF-R076, BRF-R099, BRF-R100, T10, and T11. |

## Independent risk map

### Affected behavior

- Historical proposal-review routes no longer depend on current correction-capability status.
- A correction-loop route now references a correction capability from `latest_review_result`.
- Durable validation searches for a completed proposal-review receipt with matching proposal and review-record identities.
- The recorded route controls run status, pause reason, and whether correction authority appears to have existed.

### Highest-impact failure modes

1. Later-created correction authority is accepted as if it had existed when the review route was recorded.
2. The result's routing action selects the proof used to validate itself.
3. A completed review receipt proves review occurrence but not the selected correction capability or explicit absence of authority.
4. Receipt search by shared identities binds the latest result to the wrong occurrence.
5. A tampered correction-loop route passes durable validation and bypasses BRF-R054's route-time active-authority condition.

### Changed boundaries

- Proposal-review finalization to durable result.
- Durable result to correction capability.
- Durable result to completed review receipt.
- Durable projection to run status and pause reason.

### Evidence expected

- Composed active-to-consumed correction and fresh-rereview proof.
- Absent-to-active route stability without result mutation.
- Negative proof for later authority plus retroactive route mutation.
- Exact source transition or receipt binding for the selected capability or explicit absence.
- Missing, stale, mismatched, and ambiguous binding rejection.

### Direct-inspection areas

- `scripts/validate_workflow_automation.py:190-277`.
- `scripts/workflow_automation_state.py:970-1016`.
- `scripts/test-workflow-automation.py:1490-1610`.
- Receipt fields established by BRF-R069.

### Scope boundaries

M4 internal proposal review, correction authority, durable state, and recovery are in scope.
M5, M6, public routing, compatibility cutover, generated adapters, external actions, final verification, and PR readiness are out of scope.

### Risk-class assessment

| Risk class | Applicability | Reason |
| --- | --- | --- |
| Authorization bypass | applicable | Durable state can claim correction authority existed at routing time. |
| Durable-state contradiction | applicable | A historical pause can be rewritten to an accepted correction-loop. |
| Recovery/idempotency | applicable | Resume depends on trustworthy immutable route evidence. |
| Compatibility/migration | applicable | Any added receipt binding must preserve current pre-public unified state semantics. |
| Review independence | applicable | Correction must remain bound to the exact formal review occurrence. |
| External-action safety | not directly applicable | The M4 harness remains non-public and performs no external action. |
| Privacy/secret exposure | not applicable | No credential, telemetry, or user-data path changed. |
| Deployment/performance | not applicable | The changed behavior is local state validation. |

### Falsifiable review questions

1. Does the matching completed receipt contain the selected correction capability ID?
2. Can later matching authority plus a changed result and run status pass validation?
3. Can the validator distinguish route-time absence from later capability creation?
4. Does the inverse regression mutate the route or only assert it remains unchanged?

## Diff summary

Commit `2d4b3b56` adds historical correction-capability validation, requires one completed proposal-review receipt with matching proposal and review identities, composes review through correction and fresh rereview authority, and adds an inverse test where later capability creation leaves an authorization-required pause unchanged.

The lifecycle artifacts resolve `BRF-M4-CR13` and request M4 R7 review.

## Prior-finding reconciliation

| Prior finding | R7 result | Evidence |
| --- | --- | --- |
| `BRF-M4-CR13` | failed-remediation with residual defect recorded as `BRF-M4-CR14` | Active-to-consumed correction now finalizes and creates fresh rereview authority. However, the inverse proof only leaves the route unchanged; a direct rewrite to `correction-loop` after adding later authority returns no validation errors because the receipt does not bind the selected correction capability. |

## Findings

## Finding BRF-M4-CR14

Finding ID: BRF-M4-CR14
Severity: major
Location: `scripts/validate_workflow_automation.py:190-277`; `scripts/workflow_automation_state.py:988-1016`; `scripts/test-workflow-automation.py:1549-1610`
Evidence: `resolve_recorded_proposal_correction_capability` trusts `review_result.routing_action` to decide whether a correction capability should exist, then checks that capability against proposal/review identities and any matching completed proposal-review receipt. That receipt records the review capability and occurrence evidence, but never the correction capability selected by `resolve_active_proposal_correction_capability`. A direct probe recorded an authorization-required pause with no correction capability, added a matching capability later, changed the result to `correction-loop`, added that capability ID, changed the run to active, and received `[]` from `validate_workflow_automation`. The seven focused proposal-review tests and two focused validator tests still pass because the inverse regression does not challenge a rewritten route.
Required outcome: Durable validation must prove the exact route decision recorded at proposal-review finalization, including the selected correction capability ID or explicit absence, without allowing later authority or self-selected routing action to manufacture that proof.
Safe resolution path: Persist an immutable route binding during proposal-review receipt finalization, reference its exact source transition from `latest_review_result`, and include the outcome, target, proposal identity, review-record identity, and selected correction capability ID or explicit absence. Validate the result against that exact receipt binding rather than searching by shared identities. Add a regression where an authorization-required pause receives later matching authority and is then rewritten to `correction-loop`; validation must fail. Preserve the active-to-consumed composed regression.
needs-decision rationale: none; this is a bounded completion of the accepted BRF-R047, BRF-R054, BRF-R066, BRF-R069, BRF-R076, BRF-R099, and BRF-R100 contracts.

auto_fix_class: none

## Requirement fidelity

| Requirement property | Result | Evidence |
| --- | --- | --- |
| BRF-R047 durable occurrence and routing action | block | The stored routing action can be changed after the occurrence and then accepted without occurrence-bound route proof. |
| BRF-R054 active authority at route time | block | A capability created after an authorization-required route can be presented as if it authorized correction at review finalization. |
| BRF-R066 preserve history and force rereview | pass for active-to-consumed liveness | The composed correction now consumes authority and activates one fresh proposal-review capability. |
| BRF-R069 complete capability-bound receipts | block for route evidence | The review receipt identifies its review capability but not the correction capability or explicit absence used by the route projection. |
| BRF-R076 completed receipt/canonical-state consistency | block | Receipt occurrence evidence does not determine the route now accepted as canonical state. |
| BRF-R099 coherent result reporting | block | A rewritten run/result pair can appear internally coherent despite lacking route-time authority. |
| BRF-R100 tracked identity/receipt resume | block | Resume cannot distinguish route-time absence from later-created matching authority. |
| T10-T11 proof | block | Existing tests cover stable unmodified history, not retroactive route fabrication. |

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | BRF-R054 route-time authority is not durably provable. |
| Test coverage | block | The named inverse regression omits route mutation after later authority appears. |
| Edge cases | block | Later authority plus retroactive route rewrite validates successfully. |
| Error handling | concern | Missing, stale, or absent bindings fail, but a fabricated internally consistent binding passes. |
| Architecture boundaries | block | The receipt/result boundary does not durably bind the route decision made by the state finalizer. |
| Compatibility | pass with follow-up | Public routing, legacy adapters, and M5/M6 behavior remain unchanged; the fix must stay compatible with current pre-public unified state. |
| Security/privacy | block for authorization integrity | No secrets are affected, but durable state can bypass the active-at-routing-time authority invariant. |
| Derived artifact currency | pass | No generated output changed. |
| Unrelated changes | pass | The commit is limited to M4 validator/tests and required lifecycle evidence. |
| Validation evidence | block for sufficiency | Focused and broad suites passed but omitted the reproduced retroactive rewrite. |

## Validation and direct proof

- `python scripts/test-workflow-automation.py -k proposal_review` passed 7 tests.
- `python scripts/test-validate-workflow-automation.py -k proposal_review_result` passed 2 tests.
- A direct temporary-state probe first confirmed later capability creation leaves the stored pause valid, then changed the result to `correction-loop` and the run to active; `validate_workflow_automation` returned no errors.
- Source inspection confirmed the completed proposal-review receipt records the review capability and occurrence identities but not the correction capability selected at finalization or explicit absence.

## No-finding rationale

Not applicable; this review has one material finding.

## Residual risks

Rereview must prove all three contrasts:

- authorized correction-loop remains valid after its capability is consumed;
- authorization-required pause remains valid after later authority appears;
- later authority cannot be used to rewrite that historical pause into correction-loop.

M5, M6, final holistic review, verification, and PR readiness remain outside this review.

## Milestone handoff

- Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `BRF-M4-CR14`
- Remaining in-scope implementation milestones: M4 resolution and rereview, M5, M6
- Next stage: review-resolution M4
- Final closeout readiness: not ready because M4 has one open material finding and M5-M6 remain unimplemented
- Verify readiness: not-claimed
- Isolation: this direct review performs no automatic downstream handoff
