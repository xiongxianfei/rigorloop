# Code Review: M4 R6 Current Review Authority and Run Projection

## Review metadata

Review ID: code-review-m4-r6
Stage: code-review
Round: M4 R6
Reviewer: same-session independent-review reset
Target: M4 correction commit `6f5da1f3`
Reviewed artifact: commit `6f5da1f3`
Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
Review mode: isolated direct formal review
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-23
Recording status: recorded
Material findings: BRF-M4-CR13
Immediate next stage: review-resolution M4

Automated review: no
Review gate outcome: stop
Native review status: changes-requested
Independence level: L0
Reviewer context ID: root-m4-r6-review-reset
Context separation mechanism: The direct formal review used an explicit review-phase reset and inspected the production diff and governing clauses before tests, validation summaries, prior findings, or author resolution claims.
Risk tier: elevated
Risk-tier triggers: Executable correction authority, durable historical review state, capability lifecycle, and receipt completion changed.
Risk-tier classifier: Approved review-independence risk-tier contract.
Governing artifacts: `specs/single-bounded-review-fix-workflow-automation.md`; `specs/single-bounded-review-fix-workflow-automation.test.md`; `docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md`; approved workflow architecture and ADR.
Formal criteria: Code-review checklist; BRF-R047-R062, BRF-R066, BRF-R099-R100; M4 T10-T12 and CMD15-CMD20 proof.
Initial packet inventory: scripts/workflow_automation.py@6f5da1f3#sha256:b3820e3a3466e7eddd086018011d45a73c9a4e7854c83e618180e7155c2d3a1b; scripts/workflow_automation_policy.py@6f5da1f3#sha256:d5cac21087c99c8ab4e930fe0a5ac68a2d0024a7d899b368541e07f248a895f2; scripts/workflow_automation_state.py@6f5da1f3#sha256:21c78dcf933daf5b6cc764b6f0a7de892d3d5b18798f3686d36f777cfeefb551; scripts/validate_workflow_automation.py@6f5da1f3#sha256:92b4d7dbaa340f0b464a3930f26ec1c3d882f0040253b96bdb832e8a3a1ca6c8; specs/single-bounded-review-fix-workflow-automation.md@6f5da1f3#sha256:59241a5e4968a0d6ba60f9772eed56ab8b9e79859a0be1c94e7c77840c724070; specs/single-bounded-review-fix-workflow-automation.test.md@6f5da1f3#sha256:e73ac1691966e7f17c1d1342b969681ae660b8a283e2f0130078c564a37e21bd; docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md@6f5da1f3#sha256:a33c9acec5e12261b24b000f4389f5da96fccc2f369ed354c4ccffe8394d8a2f
Initial packet contains prohibited context: no
Prompt template version: code-review-v1
Initial packet hash: sha256:d96cbe544adfec519ccced1e51410402ae5ee679c5618b8a3129d47b1dee2af0
Manifest owner: direct reviewer
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded

Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: `scripts/workflow_automation.py`; `scripts/workflow_automation_policy.py`; `scripts/workflow_automation_state.py`; `scripts/validate_workflow_automation.py`; their changed tests and review evidence
Requirement-fidelity matched path triggers: scripts/*validator*, docs/changes/**/reviews/, docs/changes/**/review-*.md
Requirement-fidelity matched category triggers: autoprogression gates, review-recording contracts, workflow routing contracts, closed enums
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause, property decomposition, production diff, tests, validation evidence, prior findings

Affected behavior: Proposal-review completion proof supplies current review identities to correction-capability selection; durable review projection controls run status and pause reason.
Highest-impact failure modes: Stale authority can route correction; current capability lifecycle can reinterpret historical review state; paused and non-paused routes can retain contradictory reasons; malformed or ambiguous authority can bypass consistency checks.
Changed boundaries: Stage-native proof to state finalizer; finalizer to effective-capability selector; shared projection to durable latest review and run state; persisted state to validator.
Evidence expected: Exact current and stale identity contrasts; ambiguous authority rejection; every pause-reason route; composed review-to-correction-to-rereview proof; durable round-trip validation.
Areas requiring direct inspection: `resolve_active_proposal_correction_capability`; proposal-review finalization; `project_proposal_review_result`; durable latest-review validation; focused proposal-review tests.
Areas intentionally out of scope: M5 implementation/verification integration; M6 public cutover and legacy adapters; final holistic review, verify, PR, and external actions.
Risk classes considered: authorization bypass=applicable; durable-state contradiction=applicable; recovery/idempotency=applicable; compatibility=applicable; review independence=applicable; privacy=not-applicable; deployment=not-applicable
Falsifiable review questions: Can stale or ambiguous authority produce correction-loop? Can consumed or newly created authority change a recorded route? Can a written result fail durable validation? Can any route retain a contradictory pause reason?

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, review log, review resolution, active plan, plan index, and change metadata
- Open blockers: `BRF-M4-CR13` blocks M4 closeout
- Next stage: review-resolution M4
- Review status: changes-requested
- Material findings: `BRF-M4-CR13`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m4-r6.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m4-r6`
- Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M4 resolution and rereview, M5, M6
- Required review-resolution: yes
- Finding IDs: `BRF-M4-CR13`
- Verify readiness: not-claimed

## Invocation manifest

Manifest owner: orchestrator
Review target identity: `6f5da1f30b76b5138ba1dc9d71d8c99566e07c8e`
Initial packet: actual commit diff; tracked active-plan handoff and M4 scope; approved `BRF-R047` through `BRF-R062`; active T10-T12 proof contracts; formal code-review criteria
Forbidden initial context excluded: author reasoning and self-assessment, desired verdict, prior reviewer conclusions and findings, validation summaries, evidence menu, and correction eligibility
Reviewer did not edit reviewed implementation target: true

## Phase receipts

| Phase | Status | Evidence |
| --- | --- | --- |
| neutral-initial-packet | recorded | Commit diff and governing clauses inspected without prior finding content or validation summaries. |
| risk-map-recorded | recorded | Independent risk map below was written before evidence challenge and prior-finding reconciliation. |
| evidence-challenge | recorded | Focused suites passed, but a direct composed review-to-correction probe reproduced a finalization failure absent from the suite. |
| prior-finding-reconciliation | recorded | `BRF-M4-CR11` and `BRF-M4-CR12` were reconciled after the blind-first pass. |
| requirement-fidelity | recorded | The changed surfaces were compared with BRF-R047, BRF-R054, BRF-R066, BRF-R099, BRF-R100, and T10-T12. |

## Independent risk map

### Affected behavior

- Proposal-review completion proof now supplies the review-record and reviewed-proposal identities used to select proposal-correction authority.
- The correction-capability selector now filters executable authority by those two identities.
- The durable latest-review projection now carries review-record identity and an explicit run pause-reason projection.
- Durable validation reconstructs the route from persisted review evidence and current capabilities.
- The pure proposal-review evaluator accepts an optional review-record identity when evaluating correction authority.

### Highest-impact failure modes

1. A stale or unrelated correction capability is selected because only part of its concrete basis is compared with the finalized review.
2. Multiple matching capabilities or a malformed matching capability cause validation to skip route consistency instead of failing closed.
3. The state writer and validator derive the current review identity from different evidence, allowing a written state that cannot be validated or a stale state that appears current.
4. Active or completed routes retain a stale pause reason, or paused routes omit or carry the wrong reason.
5. An optional identity in the pure projection creates a second, weaker route contract that diverges from durable finalization.
6. Adding a required durable review-record identity invalidates supported historical unified state without a compatibility rule.
7. Tests prove only happy-path serialization while missing ambiguous authority, missing identity, malformed basis, and all closed review outcomes.

### Changed boundaries

- Stage-native completion proof → state finalizer.
- State finalizer → effective-capability selector.
- Effective-capability selector → shared proposal-review projection.
- Shared projection → `latest_review_result` and run state.
- Persisted automation state → independent durable validator.

### Evidence expected

- Direct positive proof for one identity-matched correction capability.
- Direct negative proof for stale proposal identity, stale review-record identity, absent authority, invalid budget, and ambiguous matching authority.
- Direct proof for pause-reason presence and exact value on every paused route.
- Direct proof that pause reason is removed or rejected on every active and completed route.
- Round-trip proof that state written by the finalizer passes the independent durable validator.
- Closed-vocabulary and malformed-identity proof that errors cannot bypass consistency checks.

### Direct-inspection areas

- `resolve_active_proposal_correction_capability`.
- Proposal-review branch in `WorkflowAutomationStateStore.finalize_transition`.
- `project_proposal_review_result`.
- `evaluate_proposal_review`.
- Latest-review vocabulary and consistency branches in `validate_workflow_automation`.
- Focused proposal-review and durable-validator regressions.

### Scope boundaries

Intentionally in scope:

- M4 proposal-review routing, proposal-correction authority, durable state, and non-public integration behavior.
- Requirement families `BRF-R047`-`BRF-R062` and test cases T10-T12 where touched by the commit.

Intentionally out of scope:

- M5 implementation/code-review/verification integration.
- M6 public command activation, legacy adapter cutover, generated adapters, and retired-writer removal.
- Final holistic review, verification, and PR readiness.

### Risk-class assessment

| Risk class | Applicability | Reason |
| --- | --- | --- |
| Authorization bypass | applicable | A stale effective capability could permit proposal mutation. |
| Durable-state contradiction | applicable | Latest review evidence and run pause state must be one deterministic projection. |
| Recovery/idempotency | applicable | Persisted review state must remain independently reconstructable after resume. |
| Compatibility/migration | applicable | The durable review-result shape gains a required identity. |
| Review independence | applicable | Correction must remain bound to the formal review occurrence. |
| External-action safety | not directly applicable | This slice does not activate public or external actions. |
| Privacy/secret exposure | not applicable | No credential, telemetry, or user-data surface is changed. |
| Deployment/performance | not applicable | The change is local deterministic state evaluation. |

### Falsifiable review questions

1. Can a capability whose proposal or review-record identity differs by one value still produce `correction-loop`?
2. Can two identity-matched active capabilities cause the validator to return no error?
3. Can a state written by proposal-review finalization fail its own durable validator?
4. Can any approved, exact-target, correction-loop, blocked, inconclusive, or authorization-required route retain a contradictory run pause reason?
5. Can missing or malformed review-record identity suppress route-consistency validation without another blocking error?
6. Does any supported pre-public unified state legitimately omit the newly required review-record identity?

## Diff summary

Commit `6f5da1f3` adds the finalized review-record identity to the shared review projection, requires exact proposal and review-record identities when selecting an active proposal-correction capability, and projects run-level pause-reason presence or absence alongside run status.

The state finalizer and durable validator now use that shared identity-aware selector.
Focused tests add current-versus-stale proposal and review identity cases and route-level pause-reason contrasts.

## Prior-finding reconciliation

| Prior finding | R6 result | Evidence |
| --- | --- | --- |
| `BRF-M4-CR11` | resolved | The selector receives independently verified proposal and formal review-record identities and requires both to equal the active correction capability basis before recording `correction-loop`. Direct stale-proposal and stale-review cases pause. |
| `BRF-M4-CR12` | resolved | The shared projection now owns `run_pause_reason`; the writer removes it from non-paused routes and the validator rejects absent, wrong, or stale values. Direct correction-loop stale-pause proof also fails closed. |

## Findings

## Finding BRF-M4-CR13

Finding ID: BRF-M4-CR13
Severity: major
Location: `scripts/validate_workflow_automation.py:133-185` and `scripts/validate_workflow_automation.py:1420-1488`; composed flow through `scripts/workflow_automation_state.py:944-1029`
Evidence: Durable validation reconstructs the already recorded proposal-review route by selecting a capability that is active **now**. A direct composed probe first recorded a valid identity-matched `correction-loop`, then executed the bound proposal correction. Completion consumed that correction capability before the final state write, so the validator reprojected the historical review as `pause` with `proposal-correction-authorization-required`. The completion write and its fallback paused write both raised `StateContractError`. Proposal bytes were rolled back, but the correction receipt remained `prepared`, the capability remained active, and every retry reaches the same impossible finalization boundary. The reverse transition is also unsafe by construction: granting authority after an authorization-required review would reinterpret the recorded route.
Required outcome: A recorded proposal-review occurrence and routing action must remain a stable historical projection while later authorization and capability lifecycle changes proceed. Current executable-authority selection may govern a new transition, but durable validation must not recompute an earlier review result from mutable current capability status.
Safe resolution path: Separate route-time capability selection from historical review-result validation. Persist the selected correction capability ID and exact basis identities at review finalization, validate that recorded relationship and its receipt without requiring the capability to remain active, and add a composed `proposal-review → correction-loop → proposal correction → fresh proposal-review capability` regression. Add the inverse case proving that later capability creation does not rewrite an earlier authorization-required pause.
needs-decision rationale: none; BRF-R047 records the occurrence, BRF-R054 evaluates authority at routing time, BRF-R066 requires correction to reach rereview, and BRF-R100 requires durable receipt/identity-based resume rather than mutable reinterpretation.

auto_fix_class: none

## Requirement fidelity

| Requirement property | Result | Evidence |
| --- | --- | --- |
| BRF-R047 durable occurrence and route record | block | The validator changes the meaning of the recorded route when capability status changes. |
| BRF-R054 authority checked for later-target correction | pass at review time, block after transition | Exact active authority is selected correctly when review finalizes, but consumption makes the same record invalid. |
| BRF-R055 pause semantics | pass | Blocked, inconclusive, and authorization-required routes carry exact pause state. |
| BRF-R060-BRF-R062 review independence and deterministic proposal correction | pass | Review and correction remain separate, and correction authority is identity- and budget-bound. |
| BRF-R066 correction must require fresh rereview | block | The composed correction cannot finalize and activate its fresh proposal-review capability. |
| BRF-R099 coherent run reporting | block | Run state cannot progress beyond the recorded correction-loop without contradicting durable validation. |
| BRF-R100 tracked identity/receipt resume | block | The prepared receipt is retryable in form but cannot reach a valid terminal write. |
| T10-T12 proof projection | block | Focused review and validator cases omit the composed route-to-correction lifecycle transition. |

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | Stable recorded routing and correction-to-rereview progression fail across a capability lifecycle change. |
| Test coverage | block | Current tests separately prove review routing and proposal correction but do not compose them in one durable run. |
| Edge cases | block | Active-to-consumed and absent-to-active authority transitions can reinterpret historical review state. |
| Error handling | concern | Proposal bytes roll back safely, but both completion and fallback finalization fail and leave a permanently retrying prepared receipt. |
| Architecture boundaries | block | The validator conflates historical occurrence evidence with current executable authority despite the architecture’s evidence/capability separation. |
| Compatibility | pass | Public commands, legacy adapters, schema, and M5/M6 behavior remain unchanged. |
| Security/privacy | concern | No secret or external-action surface changed; current identity matching prevents the reported stale-authority bypass, but lifecycle liveness remains broken. |
| Derived artifact currency | pass | No generated or public adapter output changed. |
| Unrelated changes | pass | Commit `6f5da1f3` is limited to the two R5 corrections, tests, and lifecycle evidence. |
| Validation evidence | block | Focused and broad suites pass but omit the composed transition that deterministically fails. |

## Validation and direct proof

- `python scripts/test-workflow-automation.py -k proposal_review` passed 6 tests.
- `python scripts/test-validate-workflow-automation.py -k proposal_review_result` passed 2 tests.
- Direct correction-loop round-trip, stale-pause, duplicate-authority, and missing-review-identity probes passed.
- Direct composed review-to-correction proof failed during the correction completion write with canonical latest-review, run-status, and run-pause mismatches.
- Failure-state inspection showed proposal rollback succeeded, while the correction receipt remained `prepared`, the correction capability remained `active`, and the run remained `active`; the state itself was valid but could not complete the pending transition.
- Implementation evidence reports the broader engine, policy, state, validator, lifecycle, review, skill, metadata, and broad-smoke suites passing. Those results establish regression breadth but do not cover this composed failure.

## No-finding rationale

Not applicable; this review has one material finding.

## Residual risks

Rereview must prove both directions of authority lifecycle change:

- a recorded correction-loop remains valid after its capability is consumed by successful correction;
- a recorded authorization-required pause is not retroactively changed merely because a capability is later created.

M5, M6, final holistic review, verification, and PR readiness remain outside this review.

## Milestone handoff

- Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `BRF-M4-CR13`
- Remaining in-scope implementation milestones: M4 resolution and rereview, M5, M6
- Next stage: review-resolution M4
- Final closeout readiness: not ready because M4 has one open material finding and M5-M6 remain unimplemented
- Verify readiness: not-claimed
- Isolation: this direct review performs no automatic downstream handoff
