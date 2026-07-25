# Code Review: M4 R9 Historical Proposal-Review Receipt Integrity

## Review metadata

Review ID: code-review-m4-r9
Stage: code-review
Round: M4 R9
Reviewer: same-session independent-review reset
Target: M4 correction commit `ddb30e4d`
Reviewed artifact: commit `ddb30e4d`
Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
Review mode: isolated direct formal review
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-23
Recording status: recorded
Material findings: BRF-M4-CR16
Immediate next stage: review-resolution M4

Automated review: no
Review gate outcome: stop
Native review status: changes-requested
Independence level: L0
Reviewer context ID: root-m4-r9-review-reset
Context separation mechanism: The direct formal review inspected the committed production and test diff and governing clauses, then recorded a blind-first risk map before reading validation summaries or the R8 finding.
Risk tier: elevated
Risk-tier triggers: Durable review-route evidence, correction-authority identity, receipt immutability, cancellation reconciliation, and fail-closed validation changed or became jointly binding.
Risk-tier classifier: Approved review-independence risk-tier contract.
Governing artifacts: `specs/single-bounded-review-fix-workflow-automation.md`; `specs/single-bounded-review-fix-workflow-automation.test.md`; `docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md`; approved workflow architecture and ADR.
Formal criteria: Code-review checklist; BRF-R007a, BRF-R007b, BRF-R047, BRF-R054, BRF-R069, BRF-R076, BRF-R100, BRF-R101, and BRF-R102; T10, T11, and T16 proof.
Initial packet inventory: scripts/workflow_automation_state.py@ddb30e4d#sha256:1579b076766d08e40bcb5a8c77c272b30554b6c0a041f48a3f6449dfc8efc32e; scripts/validate_workflow_automation.py@ddb30e4d#sha256:6fabd56eed7d468cb8a77bdbaaf81135b84479e9287ad920d85f37f7243e5b15; scripts/test-workflow-automation-state.py@ddb30e4d#sha256:83e970569188c0bb94f61d7cdb31ea6751e89ef118c2c19973a9a56d635710a4; scripts/test-validate-workflow-automation.py@ddb30e4d#sha256:a98c9e8475b73237a7e86d47fc7029124baac909350c251a38cb1eae554f39c3; specs/single-bounded-review-fix-workflow-automation.md@ddb30e4d#sha256:59241a5e4968a0d6ba60f9772eed56ab8b9e79859a0be1c94e7c77840c724070; specs/single-bounded-review-fix-workflow-automation.test.md@ddb30e4d#sha256:e73ac1691966e7f17c1d1342b969681ae660b8a283e2f0130078c564a37e21bd; docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md@ddb30e4d#sha256:740a4fccff5239dcad3a26e142590626b4cd18bee33dba4a085140e5739dd2a5
Initial packet contains prohibited context: no
Prompt template version: code-review-v1
Initial packet hash: sha256:a8592c34a7afe10b691935a00eb0436a1c24b35b4f07a8853e910c9546113162
Manifest owner: direct reviewer
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded

Affected behavior: Proposal-review completion is shared across normal and cancellation paths; completed receipts gain route evidence; cancelled runs preserve the stage result while terminating authority; durable validation attempts to require route and occurrence evidence.
Highest-impact failure modes: Cancellation loses or rebinds correction authority; cancelled-run handling masks route inconsistencies; a non-latest completed review receipt retains malformed historical evidence; active authority survives shutdown; or terminal immutability freezes invalid state.
Changed boundaries: Sole state writer to shared review projection; completed receipt to route binding; latest result to exact source transition; cancelled run to historical review outcome; validator to every completed proposal-review receipt.
Evidence expected: Exact approved and correction-loop route binding; explicit capability absence; missing and malformed historical route rejection; exact source identity; parent and capability shutdown; stale-pause rejection; and immutable terminal receipts.
Areas requiring direct inspection: `_project_completed_proposal_review`; cancellation ordering; `resolve_recorded_proposal_correction_capability`; the completed-receipt validation loop; cancelled-run projection exception; cancellation and validator regressions.
Areas intentionally out of scope: M5, M6, public command activation, compatibility cutover, generated adapters, external actions, final verification, and PR readiness.
Risk classes considered: authorization bypass=applicable; durable-state contradiction=applicable; recovery/idempotency=applicable; compatibility=applicable; review independence=applicable; privacy=not-applicable; deployment=not-applicable
Falsifiable review questions: Can any completed proposal-review receipt contain malformed route data and still validate? Can cancellation lose or rebind correction capability identity? Can a cancelled run retain active authority or stale pause state? Can normal finalization regress because of the extracted helper?

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
- Open blockers: `BRF-M4-CR16` blocks M4 closeout
- Next stage: review-resolution M4
- Review status: changes-requested
- Material findings: `BRF-M4-CR16`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m4-r9.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m4-r9`
- Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M4 resolution and rereview, M5, M6
- Required review-resolution: yes
- Finding IDs: `BRF-M4-CR16`
- Verify readiness: not-claimed

## Invocation manifest

Manifest owner: direct reviewer
Review target identity: `ddb30e4dc81076ba38ee35129b47b0fb58375554`
Initial packet: actual source and test diff; tracked M4 handoff; approved BRF-R007a, BRF-R007b, BRF-R047, BRF-R054, BRF-R069, BRF-R076, BRF-R100, BRF-R101, and BRF-R102 clauses; T10, T11, and T16 proof contracts; formal code-review criteria
Forbidden initial context excluded: author reasoning and self-assessment, desired verdict, prior reviewer conclusions and findings, validation summaries, evidence menu, and correction eligibility
Reviewer did not edit reviewed implementation target: true

## Phase receipts

| Phase | Status | Evidence |
| --- | --- | --- |
| neutral-initial-packet | recorded | Commit source/test diff and governing clauses were inspected before validation summaries and R8 reconciliation. |
| risk-map-recorded | recorded | Historical receipt integrity, cancellation authority binding, and cancelled-run projection were recorded before evidence results. |
| evidence-challenge | recorded | A direct two-receipt probe replaced the older completed proposal-review route with an empty object; canonical validation returned no errors. |
| prior-finding-reconciliation | recorded | `BRF-M4-CR15` is resolved for normal and cancellation writer paths. The historical non-latest validation gap is a new finding, `BRF-M4-CR16`. |
| requirement-fidelity | recorded | The implementation was compared with BRF-R007a, BRF-R007b, BRF-R047, BRF-R054, BRF-R069, BRF-R076, BRF-R100, BRF-R101, BRF-R102, T10, T11, and T16. |
| verdict-recorded | recorded | One actionable major finding requires bounded M4 review-resolution and rereview. |

## Independent risk map

### Affected behavior

- Normal and cancellation proposal-review completion use one state-writer projection.
- Every new completed proposal-review receipt receives a route binding.
- `latest_review_result` references one exact completed source transition.
- Cancellation overlays terminal orchestration state after recording stage evidence.
- The validator recognizes completed proposal-review receipts by their bound capability.

### Highest-impact failure modes

1. Cancellation records a route after correction authority has already been revoked.
2. Cancellation loses explicit absence or silently selects later authority.
3. The cancelled-run exception skips canonical route validation.
4. A completed historical receipt not referenced by the latest result retains malformed route evidence.
5. Terminal receipt immutability freezes state that the validator failed to reject.

### Changed boundaries

- Verified completion proof to shared proposal-review projector.
- Shared projector to normal finalization and cancellation.
- Completed receipt to immutable route binding.
- Latest review result to exact source receipt.
- Cancelled run to preserved review outcome and terminated authority.
- Validator to the set of completed proposal-review receipts.

### Evidence expected

- Route evidence parity across normal and cancellation completion.
- Selected correction capability or explicit absence recorded before shutdown.
- Every completed receipt independently validates route fields and stage-native identities.
- Latest occurrence points to an exact completed source.
- Cancellation revokes active parents, invalidates remaining capabilities, clears stale pause state, and stays idempotent.
- Finalized receipts cannot be rewritten through the sole writer.

### Direct-inspection areas

- `scripts/workflow_automation_state.py:126-180`.
- `scripts/workflow_automation_state.py:904-1155`.
- `scripts/validate_workflow_automation.py:133-320`.
- `scripts/validate_workflow_automation.py:1550-1710`.
- `scripts/test-workflow-automation-state.py:1044-1230`.
- `scripts/test-validate-workflow-automation.py:515-615`.

### Scope boundaries

M4 internal proposal review, correction authority, durable state, recovery, cancellation reconciliation, and their validators are in scope.
M5, M6, public routing, compatibility cutover, generated adapters, external actions, final verification, and PR readiness are out of scope.

### Risk-class assessment

| Risk class | Applicability | Reason |
| --- | --- | --- |
| Authorization bypass | applicable | Route history must preserve selected correction capability or explicit absence. |
| Durable-state contradiction | applicable | A completed non-latest review receipt can carry malformed route evidence without rejection. |
| Recovery/idempotency | applicable | Cancellation reconciles prepared work and makes the run terminal. |
| Compatibility/migration | applicable | The correction must not alter public or legacy writer behavior before M6. |
| Review independence | applicable | Durable routing must remain tied to the exact formal review occurrence. |
| External-action safety | not directly applicable | The M4 harness and cancellation remain repository-local. |
| Privacy/secret exposure | not applicable | No credential, telemetry, or user-data path changed. |
| Deployment/performance | not applicable | The change is local validation and state persistence. |

### Falsifiable review questions

1. Can any completed proposal-review receipt contain malformed route data and still validate?
2. Does cancellation bind route authority before revoking parent and child authority?
3. Does canonical validation continue checking latest review evidence for cancelled runs?
4. Can active authority or stale pause state survive cancellation?
5. Does helper extraction preserve normal finalization outcome routing?

## Diff summary

Commit `ddb30e4d` factors complete proposal-review projection into one state-writer helper used by normal finalization and cancellation reconciliation. Cancellation records the verifier-derived route before applying terminal run state, clears stale pause state, revokes parents, and invalidates remaining capabilities.

The validator now rejects a completed proposal-review receipt when its route field is absent or not an object, requires a source-linked latest occurrence when any completed proposal-review receipt exists, permits the canonical review result to coexist with a cancelled run, and validates cancellation evidence and authority shutdown.

Tests add the previously missing cancellation assertions, terminal immutability proof, missing route/latest-result rejection, and cancelled-run consistency cases.

## Prior-finding reconciliation

| Prior finding | R9 result | Evidence |
| --- | --- | --- |
| `BRF-M4-CR15` | resolved | Both normal finalization and cancellation invoke `_project_completed_proposal_review` before terminal cancellation. The targeted cancellation test proves route presence, exact source linkage, explicit correction-capability absence, parent revocation, stale-pause removal, final cancellation, and terminal receipt immutability. Missing route and missing latest occurrence now fail for the single completed receipt case. |
| Historical completed-receipt integrity | new-finding `BRF-M4-CR16` | The validator checks only that every completed proposal-review route is an object. Exact route/evidence validation remains limited to the receipt referenced by `latest_review_result`. |

## Findings

## Finding BRF-M4-CR16

Finding ID: BRF-M4-CR16
Severity: major
Location: `scripts/validate_workflow_automation.py:1554-1578`; `scripts/validate_workflow_automation.py:1635-1708`; `scripts/test-validate-workflow-automation.py:518-558`
Evidence: `completed_proposal_review_receipts` rejects only a missing or non-object `proposal_review_route`. Exact route, target, proposal identity, review-record identity, outcome, routing action, and correction-capability validation occurs later only through `latest_review_result.source_transition_id`. A direct probe created two structurally valid completed proposal-review receipts, retained `latest_review_result` on `transition-001`, changed `transition-002.proposal_review_route` to `{}`, recomputed its immutable transition key, and observed `validate_workflow_automation(state) == []`. The added regression covers only the single latest receipt, so it cannot expose this historical-receipt bypass.
Required outcome: Every completed proposal-review receipt, including receipts not referenced by `latest_review_result`, must independently prove an exact canonical route binding to its own target, proposal input identity, canonical review-record identity, outcome, routing action, and selected correction capability or explicit absence. Unknown route vocabulary must fail before cross-field consistency.
Safe resolution path: Add one receipt-level proposal-review route validator and reuse it from latest-result validation. Extend closed-vocabulary validation to route outcome and routing action. For every completed proposal-review receipt, reconstruct the canonical route projection from its own immutable receipt target and evidence, compare the exact route binding, and validate any recorded correction capability against that review basis without requiring current active status. Add two-receipt regressions for an empty route, wrong target, wrong proposal/review identity, unknown outcome/action, missing or mismatched correction capability, and a valid historical receipt; retain the cancellation, explicit-absence, consumed-capability, and terminal-immutability contrasts.
needs-decision rationale: none; this is a bounded completion of BRF-R047, BRF-R054, BRF-R076, BRF-R100, BRF-R101, and BRF-R102 inside the approved M4 validator and test boundary.

auto_fix_class: none

## Requirement fidelity

| Requirement property | Result | Evidence |
| --- | --- | --- |
| BRF-R007a reconcile before cancellation | pass | Cancellation verifies and projects stage completion before applying terminal run state. |
| BRF-R007b revoke/invalidate and preserve evidence | pass | Cancelled-run validation rejects active parents/capabilities and the state writer preserves completed receipt evidence. |
| BRF-R047 complete durable review occurrence | block for historical receipts | A non-latest completed receipt may retain an empty route and still validate. |
| BRF-R054 route-time correction authority | block for historical receipts | Non-latest correction-capability selection or explicit absence is not independently checked. |
| BRF-R069 complete receipt contract | pass for named base fields | All named base receipt fields remain validated; the defect is in the proposal-review route extension. |
| BRF-R076 completed receipt consistency | block | Canonical validation accepts a malformed completed historical route. |
| BRF-R100 tracked receipt-based status/resume | block | Tracked non-latest receipt evidence is not sufficient to reconstruct or reject its route. |
| BRF-R101 unknown values before consistency | block for historical route values | Route outcome/action vocabulary is not independently validated for non-latest receipts. |
| BRF-R102 unknown-value regression | block | No historical route unknown-value regression exists. |
| T10 proposal-review outcome and routing | block for historical receipts | Outcome/route proof covers the current result but not every retained completed occurrence. |
| T11 correction authority | pass for the current latest result | Active-to-consumed and later-authority contrasts remain covered for the current source receipt. |
| T16 cancellation | pass for the reviewed path | Prepared review completion now records route/result evidence before terminal cancellation. |

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | BRF-R047, BRF-R076, BRF-R100, and BRF-R101 are incomplete for non-latest completed review receipts. |
| Test coverage | block | The new tests cover one current receipt but no retained historical receipt contrast. |
| Edge cases | block | A valid current receipt can mask an empty historical route object. |
| Error handling | block | Canonical validation returns no errors for malformed historical evidence. |
| Architecture boundaries | pass | The sole writer and validator ownership boundaries remain respected. |
| Compatibility | pass with bounded correction | Public commands, legacy adapters, schemas, M5/M6, and external actions are unchanged. |
| Security/privacy | concern for authorization integrity | No secret exposure exists, but historical correction-authority evidence can be erased without detection. |
| Derived artifact currency | pass | No generated output is part of the reviewed implementation. |
| Unrelated changes | pass | The diff is limited to M4 state, validation, tests, and lifecycle evidence. |
| Validation evidence | block for sufficiency | Focused and broad suites pass, but the direct two-receipt tamper is absent and succeeds. |

## Validation and direct proof

- `python scripts/test-workflow-automation-state.py -k cancel`: 7 tests passed.
- `python scripts/test-validate-workflow-automation.py -k proposal_review`: 6 tests passed.
- Direct two-receipt historical-route probe: `transition-002.proposal_review_route = {}` produced `[]` validation errors while `latest_review_result` remained bound to valid `transition-001`.
- Source inspection confirms receipt-set validation checks only route object presence; exact binding uses only the latest source transition.
- Recorded broad-smoke and full-suite evidence was inspected after the risk map. It does not include the two-receipt historical tamper case.

## No-finding rationale

Not applicable; this review has one material finding.

## Residual risks

Rereview must prove every retained completed proposal-review receipt independently preserves route and authority history without interpreting current capability status as route-time authority.

Direct cancellation with an active correction capability should be added as a contrast while the receipt-level validator is factored, because the current cancellation regression proves explicit absence only.

M5, M6, final holistic review, verification, and PR readiness remain outside this review.

## Milestone handoff

- Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `BRF-M4-CR16`
- Remaining in-scope implementation milestones: M4 resolution and rereview, M5, M6
- Next stage: review-resolution M4
- Final closeout readiness: not ready because M4 has one open material finding and M5-M6 remain unimplemented
- Verify readiness: not-claimed
- Isolation: this direct review performs no automatic downstream handoff
