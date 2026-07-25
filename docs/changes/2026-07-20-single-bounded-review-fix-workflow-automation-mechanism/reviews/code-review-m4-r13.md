# Code Review: M4 R13 Repository-Backed Review Status

## Review metadata

Review ID: code-review-m4-r13
Stage: code-review
Round: M4 R13
Reviewer: fresh blind-first reviewer agent
Target: M4 correction commit `f12a4f3a`
Reviewed artifact: commit `f12a4f3a`
Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
Review mode: isolated direct formal review
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-23
Recording status: recorded
Material findings: BRF-M4-CR20, BRF-M4-CR21
Immediate next stage: review-resolution M4

Automated review: yes
Review gate outcome: stop
Native review status: changes-requested
Independence level: L2
Reviewer context ID: m4-r13-blind-review-agent
Context separation mechanism: A fresh agent received only the target commit, governing artifacts, milestone identity, and formal criteria. Prior reviews, findings, implementation self-assessment, validation summaries, and desired outcome were excluded until the blind-first risk map was returned.
Risk tier: elevated
Risk-tier triggers: Durable review identity, repository-backed status projection, historical occurrence integrity, recovery behavior, and the state-store read/write boundary changed.
Risk-tier classifier: Approved review-independence risk-tier contract.
Governing artifacts: `specs/single-bounded-review-fix-workflow-automation.md`; `specs/single-bounded-review-fix-workflow-automation.test.md`; `docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md`; approved workflow architecture and ADR.
Formal criteria: Code-review checklist; BRF-R006, BRF-R047, BRF-R066, BRF-R073 through BRF-R077, BRF-R099 through BRF-R102; T10, T15, and T22.
Initial packet inventory: scripts/workflow_automation_state.py@f12a4f3a#sha256:a74dd282b6e2af89bdaff7747b6635431e2c07a0646d977c09429a168f9d02cb; scripts/test-workflow-automation-state.py@f12a4f3a#sha256:5ccb4bfd798d6d17235f32176d95a25df661a82816cdb6f770381e25d3f5fb03; scripts/test-query-change-record.py@f12a4f3a#sha256:6e07fa06be23097b91633c0938003ba56f9903552507e5ffb7297e4a1c594503; specs/single-bounded-review-fix-workflow-automation.md@f12a4f3a#sha256:59241a5e4968a0d6ba60f9772eed56ab8b9e79859a0be1c94e7c77840c724070; specs/single-bounded-review-fix-workflow-automation.test.md@f12a4f3a#sha256:e73ac1691966e7f17c1d1342b969681ae660b8a283e2f0130078c564a37e21bd; docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md@f12a4f3a#sha256:5b0e007fb3ee2fbc84a1719ba88cdd99fbf5596bc7e3de93abd113c0c939afa4
Initial packet contains prohibited context: no
Prompt template version: code-review-v1
Initial packet hash: sha256:c4b29ffdf2e8fe7ca452b0756dee03f6ffcbc2f4255957874186d5a720fc4d9b
Manifest owner: workflow reviewer
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded

Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: `scripts/workflow_automation_state.py`; `scripts/test-workflow-automation-state.py`; `scripts/test-query-change-record.py`; M4 review and lifecycle evidence
Requirement-fidelity matched path triggers: scripts/*validator*, docs/changes/**/reviews/, docs/changes/**/review-*.md
Requirement-fidelity matched category triggers: autoprogression gates, review-recording contracts, workflow routing contracts, closed enums
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause, reviewer-authored property decomposition, production diff, tests, validation evidence, prior finding

## Blind-first risk map

Affected behavior: Repository-backed semantic validation for completed proposal-review receipts on canonical state reads and replacements; completed-receipt recovery reuse; historical review validation after later proposal mutation; and query/status rejection through the state-store boundary.

Highest-impact failure modes: Coordinated semantic forgery, historical-state false rejection, recovery regression, query-boundary bypass, multi-occurrence rewind, path/TOCTOU escape, and vocabulary-order masking.

- Coordinated receipt, route, latest-result, run-state, or review-log rewrites remain self-authenticating.
- Append-only review growth, proposal correction, rereview, cancellation, migration, or unrelated receipt reads become unavailable.
- Completed recovery reruns work, accepts partial or stale output, silently rebinds identity, or weakens fail-closed behavior.
- A status/query caller bypasses the repository-backed state boundary.
- Multiple review occurrences bind to the wrong latest result or force old receipts to equal the newest occurrence.
- Path, symlink, or time-of-check/time-of-use behavior admits evidence outside the canonical repository surfaces.
- Semantic validation masks structural unknown-vocabulary errors.

Changed boundaries: State-store reads and writes now consult proposal, formal-review, and review-log files. Historical receipt validation permits later proposal and append-only review-log changes while requiring the bound review record and occurrence to remain exact. Status/query remain non-mutating but gain semantic rejection behavior.

Evidence expected: Coordinated ID/outcome/route/latest tampering; all four outcomes; historical and latest multi-review receipts; corrected proposal plus rereview; append acceptance and occurrence rewrite/deletion rejection; completed/prepared recovery contrasts; status/query byte stability; unknown-value ordering; path containment; and non-proposal receipt isolation.

Areas requiring direct inspection: `_verify_transition_completion`; `_verify_completed_proposal_review_semantics`; `validate_workflow_automation_semantics`; `evaluate_receipt_recovery`; state-store `read`, `replace_automation`, and `status`; recorded-route resolvers; formal-review/log parsers; query loading and error translation; and changed cancellation/log-disappearance tests.

Areas intentionally out of scope: M5 implementation/verification integration, M6 public activation and aliases, public help/final output, migration cutover, generated adapters, external actions, PR readiness, and final verification except where the new read boundary could regress them.

Risk classes considered: Data integrity, recovery/idempotency, compatibility/availability, filesystem/path/TOCTOU safety, observability, validator ordering, test adequacy, and the architecture write boundary are applicable. Credentials, privacy exposure, network mutation, deployment, generated publication, and throughput are not applicable absent contrary evidence.

Falsifiable review questions: Can coordinated durable facts remain accepted against unchanged canonical evidence; can corrected proposals and appended logs preserve valid history; can multiple receipts rewind latest state; can query validate and report different snapshots; can valid recovery reinvoke; can structural unknowns lose precedence; and can non-review receipts become review-coupled?

- Can canonical review facts remain unchanged while coordinated durable review facts are rewritten and accepted?
- Can a corrected proposal retain an auditable old occurrence without satisfying the current clean gate?
- Can log append preserve an old occurrence while rewrite or deletion fails?
- Does each of two completed review receipts bind its own occurrence while only the current receipt owns `latest_review_result`?
- Are successful and rejected status/query operations byte-stable?
- Does valid completed recovery avoid reinvocation while drift pauses or fails closed?
- Do structural unknown values fail before repository semantic errors?
- Do non-proposal completed receipts avoid proposal-review coupling?
- Does replacement reject false semantic state while permitting legitimate correction and rereview?

## Phase receipts

| Phase | Status | Evidence |
| --- | --- | --- |
| neutral-initial-packet | recorded | Target commit, governing artifacts, M4 milestone, and formal criteria only. |
| risk-map-recorded | recorded | Independent reviewer returned the complete blind-first risk map before later evidence or prior findings were released. |
| evidence-menu-released | recorded | Source, tests, architecture boundaries, focused commands, and direct adversarial probes were released after the risk map. |
| evidence-results-released | recorded | Focused suite results and bounded plan validation notes were challenged after direct inspection. |
| prior-findings-released | recorded | R12 and `BRF-M4-CR19` resolution were released only after the blind-first phase. |
| verdict-recorded | recorded | `BRF-M4-CR19` resolved; `BRF-M4-CR20` and `BRF-M4-CR21` recorded as new major findings. |

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, review log, review resolution, active plan, plan index, and change metadata
- Open blockers: `BRF-M4-CR20` and `BRF-M4-CR21` block M4 closeout
- Next stage: review-resolution M4
- Review status: changes-requested
- Material findings: `BRF-M4-CR20`, `BRF-M4-CR21`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m4-r13.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m4-r13`
- Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M4 resolution and rereview, M5, M6
- Required review-resolution: yes
- Finding IDs: `BRF-M4-CR20`, `BRF-M4-CR21`
- Verify readiness: not-claimed

## Review inputs

- Review surface: commit `f12a4f3a` against parent `fb68a457`.
- Tracked governing branch state: approved spec, architecture, ADR, active test spec, and active plan are tracked.
- Governing requirements: BRF-R006, BRF-R047, BRF-R066, BRF-R073 through BRF-R077, and BRF-R099 through BRF-R102.
- Test contract: T10 proposal-review integrity, T15 evidence-first recovery, T22 tracked read-only status, and M4 CMD14-CMD20.
- Conditional evidence: R12 and the `BRF-M4-CR19` resolution were inspected only after the blind-first risk map.

## Diff summary

The commit adds repository-backed semantic validation for every completed proposal-review receipt on canonical state read and replacement. It reuses the same receipt verifier during completed recovery while retaining stricter current-log identity behavior there.

Historical semantic reads permit later proposal bytes and append-only review-log identity changes, but continue to require the bound formal-review record and exact canonical occurrence.

Status inherits validation from `WorkflowAutomationStateStore.read`. The query helper separately parses change metadata, invokes a fresh state-store read as a validation gate, then projects its first parsed document.

Tests add coordinated review-ID and known-outcome rejection for read/status, append-only later-log acceptance, query rejection for a forged tracked file, and real evidence setup for cancellation.

## Prior-finding reconciliation

| Prior finding | R13 result | Evidence |
| --- | --- | --- |
| `BRF-M4-CR19` | resolved | Coordinated review-ID and all three alternative known-outcome rewrites now fail at repository-backed read/status; the query rejects the same tracked forged file; completed recovery remains parser-bound; proposal mutation and append-only later review history remain readable. |

## Findings

## Finding BRF-M4-CR20

Finding ID: BRF-M4-CR20
Severity: major
Location: `scripts/workflow_automation_state.py:697-756`; missing contrast in `scripts/test-workflow-automation-state.py:1176-1233`
Evidence: `validate_workflow_automation_semantics` authenticates every completed proposal-review receipt independently, but validates `latest_review_result` only against whichever `source_transition_id` it already names. It never compares that source with canonical review-log ordering. A direct repository-backed probe created genuine r0 and r1 formal reviews, canonical log entries, and exact completed receipts. Status initially reported r1. Replacing only `latest_review_result` with the structurally and semantically valid projection of transition r0 was accepted, and status then reported r0 as latest. No occurrence or receipt evidence was forged.
Required outcome: Repository-backed semantic validation must require `latest_review_result.source_transition_id` to name the unique most recent canonical proposal-review occurrence represented by completed proposal-review receipts, without treating unrelated appended log entries that lack an automation receipt as the automation latest result.
Safe resolution path: Retain canonical log occurrence order while verifying completed receipts, reject duplicate or ambiguous receipt-to-occurrence bindings, and require the latest-result source to select the last canonical occurrence among verified completed receipts. Add two genuine reviews and two completed receipts with outcome-differentiated routing; accept r1 as latest and reject a coherent rewind to r0 while preserving unrelated append-only log entries.
needs-decision rationale: none; the approved latest-applicable-review, tracked-status, and historical-occurrence contracts already determine the required ordering semantics.
auto_fix_class: none

## Finding BRF-M4-CR21

Finding ID: BRF-M4-CR21
Severity: major
Location: `scripts/query-change-record.py:102-145`, `scripts/query-change-record.py:398-408`; missing split-snapshot contrast in `scripts/test-query-change-record.py:420-453`
Evidence: `load_change_metadata` parses `data`, then `validate_supported_shape` calls `WorkflowAutomationStateStore(metadata_path).read()` but discards the returned validated snapshot. Later `automation_policy(data)` projects the earlier parse. A deterministic direct probe kept a valid tracked completed review in the state store, passed a coordinated forged copy as `data`, and observed `shape_error=None`, projected review ID `proposal-review-forged`, and tracked state-store review ID `proposal-review-r1`. The public path can reach the same split when an atomic metadata replacement occurs between the initial parse and the validating reread.
Required outcome: Query output must project the exact document snapshot that passed repository-backed semantic validation; it must not validate one state-store read and report another parsed document.
Safe resolution path: Make `load_change_metadata` obtain one `WorkflowAutomationStateStore.read()` snapshot for unified automation state and return that snapshot document to all query projections. Refactor shape validation so it does not perform and discard a second semantic read. Add a deterministic split-snapshot/atomic-replacement regression proving query either reports the validated snapshot or fails coherently, with metadata bytes unchanged by the query.
needs-decision rationale: none; the architecture state-adapter boundary and BRF-R006/BRF-R100 already require one coherent tracked read.
auto_fix_class: none

## Requirement fidelity

| Requirement property | Result | Evidence |
| --- | --- | --- |
| BRF-R006 tracked read-only status | block | State-store status is read-only, but query can validate one snapshot and project another. |
| BRF-R047 exact recorded occurrence | block for multi-occurrence projection | Each receipt is exact, but the record named latest can be coherently rewound to an older occurrence. |
| BRF-R066 historical occurrence after proposal mutation | pass | Proposal mutation remains readable historically and does not satisfy live completion identity. |
| BRF-R073/BRF-R074 evidence-first reconciliation | pass | Completed recovery reparses evidence and valid completion does not reinvoke the stage. |
| BRF-R075 retry boundary | pass | Existing retry-policy matrix remains green and unchanged. |
| BRF-R076 completed identity drift | pass | Bound record deletion and identity/projection drift reject or pause. |
| BRF-R077 malformed/unknown state | pass | Capability suppression and malformed state fail closed. |
| BRF-R099 review/gate result | block | A genuine older occurrence can replace the current review/gate/route result. |
| BRF-R100 tracked status and resume | block | Receipt authenticity is enforced, but canonical ordering and single-snapshot query projection are not. |
| BRF-R101/BRF-R102 vocabulary-first validation | pass | Unknown run status reports its structural vocabulary error before missing repository evidence. |
| T10 | block | Single-occurrence outcome behavior passes; latest routing across two real occurrences is unproven and directly fails. |
| T15 | pass | Recovery suite and bound-evidence deletion contrast pass. |
| T22 | block | Read-only byte stability passes, but latest semantic correctness and single-snapshot query reporting fail. |

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | BRF-R047, BRF-R099, BRF-R100, T10, and T22 remain incomplete across latest selection and query snapshot coherence. |
| Test coverage | block | The append test adds a log entry without a second receipt, and the query test validates only one unchanged on-disk forged snapshot. |
| Edge cases | block | Two real receipts can rewind latest state; a query can validate and project different snapshots. |
| Error handling | concern | Malformed and deleted evidence fail safely, but individually valid stale selection and split snapshots do not. |
| Architecture boundaries | block | State-store semantic validation exists, but query discards its validated document and projects an independent parse. |
| Compatibility | pass with concern | Proposal correction and append-only unrelated review growth pass; multi-receipt ordering still needs correction. |
| Security/privacy | concern | No secret or privacy issue; durable audit/status integrity can be stale or forged under the two counterexamples. |
| Derived artifact currency | pass | No generated artifact changed. |
| Unrelated changes | pass | Source and tests are scoped to the review-status correction; lifecycle edits record the milestone. |
| Validation evidence | block for sufficiency | All named suites pass, but neither dispositive contrast is present. |

## Validation and direct proof

- Independently ran 56 state/recovery tests, 20 query tests, 64 automation-validator tests, 15 policy tests, and 7 proposal-review engine tests; all passed.
- Independently ran CMD14, CMD16-CMD20: 156 lifecycle, 8 proposal-correction, 4 authoring, 4 non-public, 103 review-artifact, and 259 skill-validator tests; all passed.
- Python compilation for the three changed Python files and `git diff --check fb68a457 f12a4f3a` passed.
- Direct two-receipt probe: latest r1 accepted; coherent source/result rewind to genuine r0 accepted.
- Direct split-snapshot query probe: valid tracked r1 state plus forged parsed copy returned no shape error and projected the forged ID.
- Direct corrected-proposal history, bound-record deletion, status byte stability, unknown-before-semantic ordering, and capability-stage suppression contrasts behaved safely.
- Broad smoke was not rerun in this review because the focused counterexamples are dispositive.

## No-finding rationale

Not applicable; two material findings remain.

## Independent-review sufficiency receipt

- Target identity: commit `f12a4f3a48790352e850191219a49be1f7f11689` against parent `fb68a457`
- Independence: L2 fresh agent; risk map recorded before prior reviews, resolution, validation summaries, or desired outcome
- Governing artifacts inspected: exact BRF-R006, BRF-R047, BRF-R066, BRF-R073 through BRF-R077, BRF-R099 through BRF-R102, T10, T15, T22, M4 plan section, architecture state-adapter boundary, and ADR recovery boundary
- Risk classes considered: Durable review integrity, multi-occurrence ordering, recovery/idempotency, status coherence, validator ordering, filesystem identity/containment, compatibility, and test adequacy
- Adversarial hypotheses tested: Coordinated ID/outcome rewrite, genuine two-receipt latest rewind, split query snapshots, bound occurrence deletion, proposal correction history, status byte stability, unknown-before-semantic ordering, capability-stage suppression, and append-only later occurrence
- Validation evidence challenged: Focused state, query, validator, engine, policy, lifecycle, review, and skill suites plus bounded plan notes
- Unreviewed or uncertain surfaces: M5/M6 public composition, adapters/cutover, and final verification
- Confidence: high for both deterministic counterexamples
- No-finding rationale: not applicable

## Residual risks

Rereview must directly prove canonical latest selection across multiple genuine receipts and one-snapshot query validation/projection.

M5 and M6 remain out of scope and blocked.

## Milestone handoff

- Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `BRF-M4-CR20` and `BRF-M4-CR21`
- Remaining in-scope implementation milestones: M4 resolution and rereview, M5, M6
- Next stage: review-resolution M4
- Final closeout readiness: not ready
- Reason: implementation-milestones-open, review-findings-open, explain-change-pending, verify-pending, pr-handoff-pending; review-state=open; open-count=2; open-findings=BRF-M4-CR20,BRF-M4-CR21

This direct review remains isolated.

It records the findings and does not automatically apply a fix or enter review-resolution.
