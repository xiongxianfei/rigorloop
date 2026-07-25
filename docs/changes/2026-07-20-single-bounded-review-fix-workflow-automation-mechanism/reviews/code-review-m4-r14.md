# Code Review: M4 R14 Canonical Ordering and Query Snapshot Rereview

## Review metadata

Review ID: code-review-m4-r14
Stage: code-review
Round: M4 R14
Reviewer: fresh blind-first reviewer agent
Target: M4 correction commit `61112030`
Reviewed artifact: commit `61112030`
Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
Review mode: isolated direct formal review
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-23
Recording status: recorded
Material findings: BRF-M4-CR22, BRF-M4-CR23
Immediate next stage: review-resolution M4

Automated review: yes
Review gate outcome: stop
Native review status: changes-requested
Independence level: L2
Reviewer context ID: m4-r14-final-blind-review-agent
Context separation mechanism: Two contaminated risk-map attempts were discarded before evidence release. A third fresh agent received only the exact four-file target, bounded governing clauses, architecture and ADR boundaries, and neutral M4 scope. Prior reviews, findings, validation summaries, implementation self-assessment, desired outcome, and budgets were excluded until its clean blind-first risk map and evidence challenge were complete.
Risk tier: elevated
Risk-tier triggers: Canonical review chronology, aggregate durable-state validation, completed recovery, tracked query snapshot selection, and the state-adapter read boundary changed.
Risk-tier classifier: Approved review-independence risk-tier contract.
Governing artifacts: `specs/single-bounded-review-fix-workflow-automation.md`; `specs/single-bounded-review-fix-workflow-automation.test.md`; approved workflow architecture and ADR; M4 milestone scope.
Formal criteria: Code-review checklist; BRF-R006, BRF-R047, BRF-R066, BRF-R073 through BRF-R077, BRF-R099 through BRF-R102; T10, T15, and T22.
Initial packet inventory: scripts/workflow_automation_state.py@61112030#sha256:c4511c56bb6237bc751d79d573f473cb551b6977c59a3fdc66bebd4b246f27a1; scripts/query-change-record.py@61112030#sha256:bb5e81d05a74214c21358fef1b15cb574f7d71a71670062356a37b49654b554a; scripts/test-workflow-automation-state.py@61112030#sha256:d82e30fbe0cf718eb9523c2c7ff4698cf1c46e75738091f6f61beb08e924ed6d; scripts/test-query-change-record.py@61112030#sha256:96dd71d0f5d695edaf837e9bd4681b070daa4ff5ec855f13c0cc7c9923a3c6cc; specs/single-bounded-review-fix-workflow-automation.md@61112030#sha256:59241a5e4968a0d6ba60f9772eed56ab8b9e79859a0be1c94e7c77840c724070; specs/single-bounded-review-fix-workflow-automation.test.md@61112030#sha256:e73ac1691966e7f17c1d1342b969681ae660b8a283e2f0130078c564a37e21bd; docs/architecture/system/architecture.md@61112030#sha256:3ad5871a99f96f86e7beed58137a6eab7fdf235a0a36dd5c25f3ea6899e9dca8; docs/adr/ADR-20260721-single-bounded-review-fix-workflow-automation.md@61112030#sha256:72f84faada32301b58221e008f7bd90d198bc002e51ffa868e5210b1299bd538
Initial packet contains prohibited context: no
Prompt template version: code-review-v1
Initial packet hash: sha256:827a7b31b216333bef51ec9b07bd132f26413121c93df92dacadde91547fe3f8
Manifest owner: workflow reviewer
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded

Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: `scripts/workflow_automation_state.py`; `scripts/query-change-record.py`; `scripts/test-workflow-automation-state.py`; `scripts/test-query-change-record.py`
Requirement-fidelity matched path triggers: scripts/*validator*, docs/changes/**/reviews/
Requirement-fidelity matched category triggers: autoprogression gates, review-recording contracts, workflow routing contracts
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause, reviewer-authored property decomposition, production diff, tests, validation evidence, prior findings

## Blind-first risk map

Affected behavior: Proposal-review proof now carries canonical log occurrence identity, aggregate semantics selects the latest completed review, completed recovery checks aggregate state, and unified query reporting conditionally crosses the state-adapter boundary.

- proposal-review completion proof now carries canonical review-log path and parsed occurrence index;
- aggregate semantics select the latest completed proposal-review receipt by occurrence index;
- duplicate occurrence bindings and cross-log completed receipts fail;
- completed recovery evaluates aggregate proposal-review semantics;
- query loading switches to the state-store document only when its first generic parse already contains unified automation.

Highest-impact failure modes: Parser grouping can replace canonical chronology, a stale first query parse can bypass unified tracked state, aggregate recovery can trust the wrong latest result, and supported compatibility shapes can lose fail-closed behavior.

- parser ordering differs from canonical source chronology;
- stale or invalid unified state is bypassed when the first query parse lacks automation;
- append-only history or completed recovery becomes spuriously unavailable;
- duplicate bindings or structural vocabulary failures lose fail-closed behavior;
- a query validates and reports different durable snapshots.

Changed boundaries: Review-log parse order now determines durable latest-review state; per-receipt proof participates in aggregate history validation; completed recovery depends on global projection; and query state-adapter use depends on the first parsed snapshot.

- review-log parse order now determines durable latest-review state;
- per-receipt verification now participates in aggregate history validation;
- completed recovery depends on global proposal-review projection;
- unified query reporting crosses the state-adapter validation boundary conditionally.

Evidence expected: Cross-format chronological receipts, rewind and duplicate negatives, append compatibility, recovery no-reinvoke proof, both valid and invalid query race directions, structural precedence, and byte stability.

- two genuine chronological review receipts across every accepted log representation;
- coherent rewind and duplicate binding negatives;
- append-only unrepresented later occurrence compatibility;
- recovery pause and no-reinvoke proof;
- both query race directions for valid and invalid unified state;
- structural-error precedence and byte stability.

Areas requiring direct inspection: `_verify_transition_completion`, `validate_workflow_automation_semantics`, `evaluate_receipt_recovery`, `parse_formal_review_log`, `load_change_metadata`, and state/query regressions.

- `_verify_transition_completion`;
- `validate_workflow_automation_semantics`;
- `evaluate_receipt_recovery`;
- `parse_formal_review_log`;
- `load_change_metadata`;
- state and query regression fixtures.

Areas intentionally out of scope: M5 implementation and verification integration, M6 public routing and aliases, external actions, final holistic review, verification, and PR readiness.

- M5 implementation and verification integration;
- M6 public routing and aliases;
- external actions, final holistic review, verification, and PR readiness.

Risk classes considered: Durable state and audit integrity, canonical chronology, snapshot and time-of-check/time-of-use coherence, recovery and idempotency, observability, compatibility, and fail-closed validation.

- durable state and audit integrity;
- canonical chronology;
- snapshot and time-of-check/time-of-use coherence;
- recovery and idempotency;
- observability, compatibility, and fail-closed validation.

Non-applicable risk classes:

- credentials, privacy, network mutation, deployment, publication, and generated adapters.

Falsifiable review questions: Does the parser preserve source chronology across accepted formats; can a stale no-automation parse bypass unified state; do duplicate and rewind states fail; does recovery avoid reinvocation; and do structural unknowns fail first?

- Does the review-log parser preserve source chronology across detailed entries and clean-receipt tables?
- Can the first query parse omit automation while the tracked file contains valid or invalid unified state?
- Do duplicate occurrences and coherent rewind fail?
- Does valid completion reconcile without reinvocation?
- Do structural unknown values fail before semantic consistency?

Requirement-property decomposition covered BRF-R006, BRF-R047, BRF-R066, BRF-R073 through BRF-R077, BRF-R099 through BRF-R102, T10, T15, and T22 across state proof, aggregate semantics, recovery, query/status, and tests.

## Phase receipts

| Phase | Status | Evidence |
| --- | --- | --- |
| neutral-initial-packet | recorded | Exact four-file target, bounded governing clauses, architecture and ADR passages, and neutral M4 scope only. |
| risk-map-recorded | recorded | The final fresh reviewer recorded the blind-first risk map before validation results or prior findings. |
| evidence-menu-released | recorded | Target source and tests, bounded parser/state helpers, and targeted commands were released after the risk map. |
| evidence-results-released | recorded | The reviewer reran focused suites and independently probed both query race directions, mixed log ordering, recovery, and structural precedence. |
| prior-findings-released | recorded | R13, `BRF-M4-CR20`, `BRF-M4-CR21`, their accepted resolution, and reported validation were released only after evidence challenge. |
| verdict-recorded | recorded | Both prior findings were classified failed-remediation; residual findings `BRF-M4-CR22` and `BRF-M4-CR23` were recorded. |

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, review log, review resolution, active plan, plan index, and change metadata
- Open blockers: `BRF-M4-CR22` and `BRF-M4-CR23` block M4 closeout
- Next stage: review-resolution M4
- Review status: changes-requested
- Material findings: `BRF-M4-CR22`, `BRF-M4-CR23`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m4-r14.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m4-r14`
- Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M4 resolution and rereview, M5, M6
- Required review-resolution: yes
- Finding IDs: `BRF-M4-CR22`, `BRF-M4-CR23`
- Verify readiness: not-claimed

## Review inputs

- Review surface: commit `611120301433d4089cb6b716f65ac55992c758f2` against parent `23962931b9d0330adc36c11b1ec3ca2540eea046`.
- Tracked governing branch state: approved specification, architecture, ADR, active test specification, and active plan are tracked.
- Governing requirements: BRF-R006, BRF-R047, BRF-R066, BRF-R073 through BRF-R077, and BRF-R099 through BRF-R102.
- Test contract: T10 proposal-review integrity, T15 evidence-first recovery, and T22 tracked read-only status.
- Conditional evidence: R13 and its accepted resolution were inspected only after the clean blind-first risk map and independent evidence challenge.

## Diff summary

The correction carries canonical review-log path and parsed occurrence index in proposal-review completion proof, rejects duplicate completed-receipt occurrence bindings, selects the maximum represented occurrence index as the latest result, and applies aggregate review semantics during completed recovery.

The query helper replaces its first generic parsed document with the state-store document only when that first parse already contains unified automation.

Tests add homogeneous detailed-entry rewind and duplicate-binding proof and a query proof whose first forged parse already contains unified automation.

## Prior-finding reconciliation

| Prior finding | R14 result | Residual finding | Evidence |
| --- | --- | --- | --- |
| `BRF-M4-CR20` | failed-remediation | `BRF-M4-CR22` | Accepted mixed-format review logs are returned in parser grouping order rather than source order, so `max(index)` can identify an older clean-table occurrence as latest. |
| `BRF-M4-CR21` | failed-remediation | `BRF-M4-CR23` | State-store reread remains conditional on the first generic parse already containing automation; a stale no-automation parse bypasses newer valid or invalid tracked unified state. |

## Findings

## Finding BRF-M4-CR22

Finding ID: BRF-M4-CR22
Severity: major
Location: `scripts/workflow_automation_state.py:560-591`, `scripts/workflow_automation_state.py:704-824`, and `scripts/review_artifact_validation.py:2460-2645`; missing mixed-format contrast in `scripts/test-workflow-automation-state.py:1235-1461`
Evidence: `_verify_transition_completion` records an occurrence index from the sequence returned by `parse_formal_review_log`, and aggregate semantics selects `max(index)`. The repository parser accepts detailed blocks and clean-receipt table rows but parses every detailed block first and appends every table row afterward, irrespective of source position. An accepted log with older r1 as a clean table row followed by newer r2 as a detailed entry parsed as r2 then r1 with no findings, making the older occurrence appear latest. The 57-test state suite uses homogeneous detailed entries and does not exercise this supported representation boundary.
Required outcome: `latest_review_result.source_transition_id` must select the unique chronologically most recent canonical proposal-review occurrence represented by completed receipts across every accepted review-log representation. Parser grouping by record format must not determine chronology.
Safe resolution path: Derive chronology from canonical source position, such as `ReviewLogEntry.line`, or return one source-position-sorted parser sequence. Retain exact receipt matching and duplicate rejection. Add both mixed-format source orders and prove newer acceptance, older rewind rejection, duplicate rejection, and unrelated unrepresented append compatibility. Rerun state, review-parser, query, validator, engine, and lifecycle suites.
needs-decision rationale: none; the accepted R13 outcome already requires canonical latest occurrence ordering.
auto_fix_class: none

## Finding BRF-M4-CR23

Finding ID: BRF-M4-CR23
Severity: major
Location: `scripts/query-change-record.py:99-148`; missing no-automation-first contrasts in `scripts/test-query-change-record.py:464-500`
Evidence: `load_change_metadata` performs the repository-backed state-store read only when the first generic parsed document already contains `workflow.automation`. A stale no-automation first parse returned no error and omitted automation while the tracked file contained valid unified state. The same stale parse returned no error when the tracked unified state was structurally or semantically invalid. The reviewer and orchestrator reproduced the bypass independently, and metadata bytes remained unchanged. The added test covers only the unified-first branch.
Required outcome: Every query result must derive from one exact repository-backed document snapshot that receives all applicable structural and semantic validation. State-adapter use must not depend on a potentially stale first parse.
Safe resolution path: Make one canonical snapshot authoritative for every query projection; run artifact, validation, legacy/compact, and automation checks against that same document; preserve malformed-generic versus invalid-automation diagnostics; add all four unified-first/no-automation-first valid/invalid race contrasts with byte-stability assertions; retain legacy and compact compatibility.
needs-decision rationale: none; BRF-R006, BRF-R100, T22, and the accepted R13 outcome already require one coherent tracked snapshot.
auto_fix_class: none

## Requirement fidelity

| Requirement property | Result | Evidence |
| --- | --- | --- |
| BRF-R006 read-only current status | block | Byte stability passes, but a stale no-automation parse can omit current unified state. |
| BRF-R047 exact occurrence, gate, and route | block | Individual receipts are exact, but accepted mixed log shapes can invert the selected latest occurrence. |
| BRF-R066 historical occurrence and rereview | concern | History remains readable, but supported mixed-format chronology can select the wrong rereview. |
| BRF-R073 and BRF-R074 evidence-first no-reinvoke recovery | pass | Valid completion evidence is inspected and reconciled without invoking the stage. |
| BRF-R075 policy-bounded retry | pass | The retry-policy matrix remains green. |
| BRF-R076 completed mismatch pause | block for chronology | Identity drift pauses, but mixed-format ordering can classify stale latest state as current. |
| BRF-R077 unsafe state fail-closed | pass | Multiple in-flight, partial output, invalid state, and structural errors retain fail-closed behavior. |
| BRF-R099 and BRF-R100 tracked result and resume | block | Mixed chronology and stale no-automation query projection can report or accept the wrong tracked state. |
| BRF-R101 and BRF-R102 vocabulary handling | pass | Structural unknown values still fail before semantic consistency; no new closed vocabulary was introduced. |
| T10 | block | Homogeneous detailed entries pass; accepted mixed-format chronology fails. |
| T15 | concern | Core recovery proof passes but aggregate latest projection inherits the chronology defect. |
| T22 | block | Read-only behavior passes while exact tracked snapshot reporting fails in the no-automation-first direction. |

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | BRF-R047, BRF-R076, BRF-R100, T10, and T22 remain incomplete. |
| Test coverage | block | Mixed-format chronology and both no-automation-first cases are absent. |
| Edge cases | block | Two independently reproduced boundary cases bypass the claimed corrections. |
| Error handling | block | Invalid tracked unified state can be silently bypassed. |
| Architecture boundaries | block | Query state-adapter use is conditional on a stale parse; chronology uses parser grouping rather than source position. |
| Compatibility | concern | Homogeneous logs and normal legacy/compact cases pass; mixed accepted logs and concurrent transition into unified state do not. |
| Security/privacy | concern | No secret or privacy regression; durable audit and status integrity remain vulnerable to stale projection. |
| Derived artifact currency | pass | No generated artifact is in the reviewed implementation slice. |
| Unrelated changes | pass | The diff is scoped to the two accepted R13 corrections and tests. |
| Validation evidence | block for sufficiency | All reported suites pass, but neither residual counterexample is represented. |

## Validation and direct proof

- Independently ran 57 state, 21 query, and 64 automation-validator tests; all passed.
- `git diff --check 23962931..61112030` passed for the exact four-file target.
- Reported correction evidence covers 772 selected tests, Python compilation, explicit lifecycle validation, and 12 broad-smoke checks.
- Mixed-format parser proof returned newer detailed r2 before older clean-table r1 with no structural findings.
- No-automation-first query probes bypassed both valid and invalid tracked unified state.
- Duplicate binding, homogeneous rewind, append-only unrepresented occurrence, recovery no-reinvoke/pause, query byte stability, and structural-error precedence behaved safely in their covered shapes.
- Passing suites are credible for selected fixtures but insufficient for the missing representation and branch contrasts.

## Residual risks

`project_automation_status` omits `run.pause_reason` and exposes only `stop_reason`. This appears pre-existing and overlaps M6 public status work, so it is recorded as a residual non-finding rather than expanding this R14 correction review.

## Independent-review sufficiency receipt

- Target identity: commit `611120301433d4089cb6b716f65ac55992c758f2` against parent `23962931b9d0330adc36c11b1ec3ca2540eea046`
- Independence: L2 fresh reviewer; two contaminated attempts discarded; final risk map recorded before prior reviews, findings, or validation summaries
- Governing artifacts inspected: exact BRF-R006, BRF-R047, BRF-R066, BRF-R073 through BRF-R077, BRF-R099 through BRF-R102, T10, T15, T22, and bounded architecture and ADR state/recovery passages
- Risk classes considered: canonical chronology, tracked-state integrity, snapshot coherence, recovery/idempotency, observability, compatibility, path boundary, and requirement compression
- Direct proofs: mixed accepted log ordering, both query race directions with valid and invalid unified state, duplicate binding, homogeneous rewind, append-only history, recovery no-reinvoke/pause, byte stability, and structural precedence
- Unreviewed surfaces: M5, M6, public routing, external actions, final holistic interactions, verification, and PR readiness
- Confidence: high for both findings
- Gate outcome: stop

## Requirement-fidelity receipt

- Applicability: applicable
- Triggered categories: automation state, formal review occurrence, state-adapter read boundary, recovery, status/query, and tests
- Spec-first packet order: satisfied
- Multi-surface property matrix: state proof, aggregate semantics, recovery, query/status, and tests
- Requirement compression detected: yes
- Material findings: `BRF-M4-CR22`, `BRF-M4-CR23`
- Gate outcome: block

## No-finding rationale

Not applicable; two material findings remain.

## Milestone handoff

- Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `BRF-M4-CR22` and `BRF-M4-CR23`
- Remaining in-scope implementation milestones: M4 resolution and rereview, M5, M6
- Next stage: review-resolution M4
- Automatic downstream handoff: stopped
- Final closeout readiness: not ready
- Reason: two major failed-remediation residual findings remain; M4 cannot close and M5/M6 remain blocked
- Verify readiness: not claimed
