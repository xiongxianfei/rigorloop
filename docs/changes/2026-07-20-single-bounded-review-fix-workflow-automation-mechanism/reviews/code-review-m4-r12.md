# Code Review: M4 R12 Parser-Bound Proposal-Review Recovery

## Review metadata

Review ID: code-review-m4-r12
Stage: code-review
Round: M4 R12
Reviewer: same-session context-reset reviewer
Target: M4 correction commit `cb814d80`
Reviewed artifact: commit `cb814d80`
Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
Review mode: isolated direct formal review
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-23
Recording status: recorded
Material findings: BRF-M4-CR19
Immediate next stage: review-resolution M4

Automated review: yes
Review gate outcome: stop
Native review status: changes-requested
Independence level: L1
Reviewer context ID: m4-r12-same-session-context-reset
Context separation mechanism: The reviewer reset assumptions, inspected the implementation and test diff plus governing clauses first, and recorded the blind-first risk map before consulting validation summaries or prior-finding resolution. Same-session authorship prevents an L2 independence claim.
Risk tier: elevated
Risk-tier triggers: Durable review identity, status projection, stage-owned evidence, completed-receipt integrity, and recovery changed or became jointly binding.
Risk-tier classifier: Approved review-independence risk-tier contract.
Governing artifacts: `CONSTITUTION.md`; `specs/single-bounded-review-fix-workflow-automation.md`; `specs/single-bounded-review-fix-workflow-automation.test.md`; `docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md`; approved workflow architecture and ADR.
Formal criteria: Code-review checklist; BRF-R047, BRF-R073 through BRF-R077, BRF-R099 through BRF-R102; T10, T15, and T22.
Initial packet inventory: scripts/workflow_automation_state.py@cb814d80#sha256:ee682851be1673e171bf36e55c7529ccc042a2fc93e169e0db6c575e5f6929ec; scripts/test-workflow-automation-state.py@cb814d80#sha256:12bdc456cb29edd3510f3f1245c510b445acd9fb7cc33db48ab0be13d0ba4451; specs/single-bounded-review-fix-workflow-automation.md@cb814d80#sha256:59241a5e4968a0d6ba60f9772eed56ab8b9e79859a0be1c94e7c77840c724070; specs/single-bounded-review-fix-workflow-automation.test.md@cb814d80#sha256:e73ac1691966e7f17c1d1342b969681ae660b8a283e2f0130078c564a37e21bd; docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md@cb814d80#sha256:9f141b34a3d804affd7600a7cbb4e5404a932dd9b24471e1b939d0bbcee0b1c7
Initial packet contains prohibited context: no
Prompt template version: code-review-v1
Initial packet hash: sha256:92b6a83dec262c38e3a6b01c32d7e4d63e2e0322f3789ace3e99ea995114b6b2
Manifest owner: workflow reviewer
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded

Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: `scripts/workflow_automation_state.py`; `scripts/test-workflow-automation-state.py`; M4 review and lifecycle evidence
Requirement-fidelity matched path triggers: scripts/*validator*, docs/changes/**/reviews/, docs/changes/**/review-*.md
Requirement-fidelity matched category triggers: autoprogression gates, review-recording contracts, workflow routing contracts, closed enums
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause, reviewer-authored property decomposition, production diff, tests, validation evidence, prior finding

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, review log, review resolution, active plan, plan index, and change metadata
- Open blockers: `BRF-M4-CR18` is a failed remediation at the durable read/status boundary; residual `BRF-M4-CR19` blocks M4 closeout
- Next stage: review-resolution M4
- Review status: changes-requested
- Material findings: `BRF-M4-CR19`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m4-r12.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m4-r12`
- Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M4 resolution and rereview, M5, M6
- Required review-resolution: yes
- Finding IDs: `BRF-M4-CR19`
- Verify readiness: not-claimed

## Review inputs

- Review surface: commit `cb814d80` against parent `62b58696`.
- Tracked governing branch state: approved spec, approved architecture and ADR, active test spec, and active plan are tracked on the reviewed branch.
- Governing requirements: BRF-R047, BRF-R073 through BRF-R077, and BRF-R099 through BRF-R102.
- Test contract: T10 proposal-review integrity, T15 evidence-first recovery, T22 durable status, and the M4 CMD15-CMD20 boundary.
- Conditional evidence: BRF-M4-CR18 resolution was inspected only after the blind-first risk map and direct source inspection.

## Blind-first risk map

Affected behavior: Completed proposal-review receipt recovery, parser-derived evidence projection, recorded route validation, and source-linked latest-result validation.

Highest-impact failure modes: Coordinated persisted fact rewrites remain self-authenticating; valid historical recovery breaks; stage mutation suppresses semantic checks; missing latest result is accepted; or valid recovery pauses.

Changed boundaries: The sole state writer now reuses validator-owned recorded-route resolvers during semantic recovery.

Evidence expected: Clean-recovery contrast; coordinated ID/outcome/identity tampering; route/latest/missing-result tampering; historical review behavior; and capability-stage mismatch rejection.

Areas requiring direct inspection: `VerifiedCompletion`, `_proposal_review_evidence_from_proof`, completed recovery, recorded proposal-review resolvers, state-store read, and status projection.

Areas intentionally out of scope: M5 implementation/verification integration, M6 public routing, compatibility alias cutover, PR readiness, and final verification.

Risk classes considered: Authorization integrity, durable-state integrity, recovery/idempotency, closed-vocabulary failure, lifecycle synchronization, and compatibility containment were applicable. Network behavior, secrets, privacy data, deployment, external actions, and generated publication were not applicable.

Falsifiable review questions: Can parser facts disagree with the persisted envelope while recovery continues? Can route or latest-result state disagree while recovery continues? Can deleting the latest result avoid recovery checks? Can a forged envelope pass canonical read or status projection? Can a changed capability stage suppress proposal-review validation? Does unchanged parser-valid evidence still recover?

## Diff summary

The commit introduces one `_proposal_review_evidence_from_proof` projection and uses it during both finalization and completed recovery.

Completed recovery now compares the parser-derived envelope with `proposal_review_evidence`, reconstructs the receipt route, requires a latest review result, and validates that result against its source receipt.

Three state-test families cover coordinated review ID and known-outcome rewrites, coherent review-record/output/canonical identity rewrites, route and latest-result rewrites, missing latest result, and the clean recovery contrast.

The commit does not change `WorkflowAutomationStateStore.read`, `WorkflowAutomationStateStore.status`, `project_automation_status`, or the rootless durable validator.

## Prior-finding reconciliation

| Prior finding | R12 result | Evidence |
| --- | --- | --- |
| `BRF-M4-CR18` | failed-remediation | Completed recovery is fixed, but the required durable-state boundary remains self-authenticating: the canonical state store accepts the coordinated forged receipt/result and `status()` reports it as unified state. |

## Findings

## Finding BRF-M4-CR19

Finding ID: BRF-M4-CR19
Severity: major
Location: `scripts/workflow_automation_state.py:900-905`, `scripts/workflow_automation_state.py:772-811`, `scripts/workflow_automation_state.py:1228-1232`; missing contrast in `scripts/test-workflow-automation-state.py:890-1081`
Evidence: The new parser comparison exists only inside `evaluate_receipt_recovery`. `WorkflowAutomationStateStore.read()` still invokes only `validate_workflow_automation`, and `status()` projects `latest_review_result` directly from that structurally self-consistent state. A direct repository-backed probe finalized a real proposal review, jointly changed the receipt evidence, route, and latest review ID to `proposal-review-forged`, then rewrote `change.yaml` outside the state adapter. `store.read()` accepted it, `store.status()` returned `source=unified` with the forged result, while `evaluate_receipt_recovery()` correctly paused with `completed-proposal-review-evidence-drift`. Thus the same durable state is reported as valid by status and invalid by resume.
Required outcome: Every repository-backed read or status entrypoint that reports proposal-review semantic state must validate completed proposal-review facts against the tracked formal review artifact and canonical occurrence before returning the result. Rootless structural validation may remain structural, but it must not be the sole gate for a status surface that reports review ID, outcome, clean gate, or routing state.
Safe resolution path: Add one repository-root-backed semantic completed-review validator owned by the state adapter and reuse it from `read`/`status` and completed recovery. Reparse each completed proposal-review record and its canonical occurrence, compare its ID, outcome, reviewed proposal identity, and record identity with the persisted envelope, then validate route/latest projections. Preserve historical receipts without requiring an old review-log byte identity to equal the current append-only log; require the occurrence itself to remain exact. Make `query-change-record` use the repository-backed state/status boundary instead of the pure projection when it reports automation review state. Add direct coordinated-tamper contrasts for store read, status, query, and recovery, plus legitimate multiple-review history.
needs-decision rationale: none; the approved tracked-evidence and status contracts already require one coherent result. The exact historical-log comparison mode must be implemented carefully but does not require a product or architecture decision.
auto_fix_class: none

## Requirement fidelity

| Requirement property | Result | Evidence |
| --- | --- | --- |
| BRF-R047 exact recorded review occurrence | block at status boundary | Status reports a forged review ID that contradicts the tracked formal review. |
| BRF-R073 stage-owned evidence before resume | pass | Recovery re-parses stage evidence before returning. |
| BRF-R074 valid completion reconciles without rerun | pass for clean contrast | The unchanged completed receipt returns `continue completed-evidence-current`. |
| BRF-R076 completed identity mismatch pauses | pass in recovery | Envelope and coherent identity mismatches pause. |
| BRF-R077 partial or unknown evidence fails closed | pass | Missing/malformed projections and stage-native evidence errors pause. |
| BRF-R099 review/gate state in run result | concern | The reported review state can contradict tracked artifacts. |
| BRF-R100 durable status and resume use tracked identities and receipts | block for status coherence | Resume checks tracked artifact bytes; status trusts the mutable receipt/result copies. |
| BRF-R101/BRF-R102 unknown values fail first and have regressions | pass | Existing closed-vocabulary validation remains intact. |
| T10 proposal-review occurrence and route | pass in recovery; block in durable status | Recovery catches coordinated rewrites, but status reports them. |
| T15 evidence-first recovery | pass | The direct parser/envelope contradiction now pauses. |
| T22 status is complete and tracked | block | Status output is read-only but not coherent with the tracked review evidence it reports. |

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | BRF-R100 and T22 remain incomplete at the status boundary. |
| Test coverage | block | Recovery tampering is covered; repository-backed read/status/query tampering and valid multi-review history are not. |
| Edge cases | block | The same forged state produces status success and recovery pause. |
| Error handling | concern | Recovery fails safely, but status exposes contradictory review state without an error. |
| Architecture boundaries | concern | The state adapter owns state access and reconciliation, but semantic validation is invoked only by recovery. |
| Compatibility | concern | A historical multi-review semantic validator must distinguish occurrence validity from append-only review-log byte changes. |
| Security/privacy | concern | No secret/privacy issue; durable authorization and review history can be misreported through status. |
| Derived artifact currency | pass | No generated artifact changed. |
| Unrelated changes | pass | The reviewed commit is scoped to recovery proof binding, tests, and lifecycle evidence. |
| Validation evidence | block for sufficiency | All focused suites pass, but none exercises repository-backed read/status after coordinated semantic tampering. |

## Validation and direct proof

- Independently ran 54 state/recovery tests; passed.
- Independently ran 64 automation-validator tests; passed.
- Independently ran 7 proposal-review engine tests and 15 policy tests; passed.
- `git diff --check cb814d80^ cb814d80` passed.
- Direct repository-backed coordinated-tamper probe: `store.read=accepted`; `status.source=unified`; recovery=`pause:completed-proposal-review-evidence-drift`.
- The implementation’s recorded CMD14-CMD20 and final-source 11-check broad-smoke evidence was challenged but not rerun because the focused status counterexample is dispositive.

## No-finding rationale

Not applicable; one material failed remediation remains.

## Independent-review sufficiency receipt

- Target identity: commit `cb814d80` against parent `62b58696`
- Independence: L1 same-session context reset; no L2 claim
- Governing artifacts inspected: exact BRF-R047, BRF-R073 through BRF-R077, BRF-R099 through BRF-R102, T10, T15, T22, M4 plan section, architecture state-adapter boundary, and BRF-M4-CR18 after the blind-first pass
- Risk classes considered: durable integrity, stage-evidence ownership, recovery, status coherence, closed vocabulary, compatibility, and test adequacy
- Adversarial hypotheses: coordinated ID/outcome rewrite, coherent identity rewrite, route/latest/missing-result rewrite, status-versus-recovery contradiction, and stage suppression
- Direct proof: real repository-backed formal review and log, external durable-state rewrite, state-store read, status projection, and completed recovery
- Validation evidence challenged: focused state, validator, engine, and policy suites plus recorded CMD and broad-smoke evidence
- Unreviewed or uncertain surfaces: M5/M6, public activation, and complete multi-review historical status behavior
- Confidence: high for the reported status-boundary defect
- No-finding rationale: not applicable

## Residual risks

Rereview must prove one repository-backed semantic boundary governs status and recovery without invalidating legitimate historical receipts merely because the append-only review log gained later entries.

M5 and M6 remain out of scope and blocked.

## Milestone handoff

- Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `BRF-M4-CR19`
- Remaining in-scope implementation milestones: M4 resolution and rereview, M5, M6
- Next stage: review-resolution M4
- Final closeout readiness: not ready
- Reason: implementation-milestones-open, review-findings-open, explain-change-pending, verify-pending, pr-handoff-pending; review-state=open; open-count=1; open-findings=BRF-M4-CR19

This direct review remains isolated.

It records the finding and does not automatically apply a fix or enter review-resolution.
