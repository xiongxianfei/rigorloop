# Code Review: M4 R10 Stage-Native Historical Review Integrity

## Review metadata

Review ID: code-review-m4-r10
Stage: code-review
Round: M4 R10
Reviewer: separate blind-review agent
Target: M4 correction commit `3d014149`
Reviewed artifact: commit `3d014149`
Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
Review mode: isolated direct formal review
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-23
Recording status: recorded
Material findings: BRF-M4-CR17
Immediate next stage: review-resolution M4

Automated review: yes
Review gate outcome: stop
Native review status: changes-requested
Independence level: L2
Reviewer context ID: m4-r10-blind-review-agent
Context separation mechanism: A fresh reviewer agent received a neutral packet, recorded and returned its blind-first risk map, and did not receive validation summaries, prior review conclusions, prior findings, or implementation-resolution claims until the risk-map phase was accepted.
Risk tier: elevated
Risk-tier triggers: Durable review identity, review outcome, correction routing, completed-receipt integrity, cancellation evidence, and fail-closed validation changed or became jointly binding.
Risk-tier classifier: Approved review-independence risk-tier contract.
Governing artifacts: `specs/single-bounded-review-fix-workflow-automation.md`; `specs/single-bounded-review-fix-workflow-automation.test.md`; `docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md`; approved workflow architecture and ADR.
Formal criteria: Code-review checklist; BRF-R047, BRF-R054, BRF-R076, BRF-R100, BRF-R101, and BRF-R102; T10, T11, and T16 proof.
Initial packet inventory: scripts/validate_workflow_automation.py@3d014149#sha256:45d8f328a903472fa10ed9e8a23b24252451244186982eafa724b89a26beb6c4; scripts/test-validate-workflow-automation.py@3d014149#sha256:b6d1ee20e5449ea3201510acde72e4ee7bd38cfe992e484d1be018c4b5855c79; specs/single-bounded-review-fix-workflow-automation.md@3d014149#sha256:59241a5e4968a0d6ba60f9772eed56ab8b9e79859a0be1c94e7c77840c724070; specs/single-bounded-review-fix-workflow-automation.test.md@3d014149#sha256:e73ac1691966e7f17c1d1342b969681ae660b8a283e2f0130078c564a37e21bd; docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md@3d014149#sha256:9d608d74c351fe5250890e10a5eaecf70407b28ac835a67828dff8a6cb1cb6cb
Initial packet contains prohibited context: no
Prompt template version: code-review-v1
Initial packet hash: sha256:401512a308b8e12e6cb790e32128b7e43b199363fed90dd3507b06f983976299
Manifest owner: workflow orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded

Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: `scripts/validate_workflow_automation.py`; `scripts/test-validate-workflow-automation.py`; their M4 review evidence
Requirement-fidelity matched path triggers: scripts/*validator*, docs/changes/**/reviews/, docs/changes/**/review-*.md
Requirement-fidelity matched category triggers: autoprogression gates, review-recording contracts, workflow routing contracts, closed enums
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause, reviewer-authored property decomposition, production diff, tests, validation evidence, prior findings

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, review log, review resolution, active plan, plan index, and change metadata
- Open blockers: `BRF-M4-CR17` blocks M4 closeout
- Next stage: review-resolution M4
- Review status: changes-requested
- Material findings: `BRF-M4-CR17`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m4-r10.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m4-r10`
- Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M4 resolution and rereview, M5, M6
- Required review-resolution: yes
- Finding IDs: `BRF-M4-CR17`
- Verify readiness: not-claimed

## Review inputs

- Review surface: commit `3d014149` against parent `a70399d7`, with governing clauses and the production diff inspected before changed tests, validation summaries, and prior findings.
- Tracked governing branch state: commit `3d014149`; R10 review evidence was added only after the verdict.
- Governing requirements: BRF-R047, BRF-R054, BRF-R076, BRF-R100, BRF-R101, and BRF-R102.
- Test contract: T10, T11, T16, and the M4 CMD15-CMD20 proof boundary.
- Architecture: stage-owned completion evidence, the sole state-writer boundary, effective-capability identity, and tracked receipt-based recovery.
- Prior review and resolution: `code-review-m4-r9.md` and the BRF-M4-CR16 disposition, released only after the risk map.

## Blind-first risk map

Affected behavior: Validation of every completed proposal-review receipt; reconstruction of historical route, gate, target, and correction authority; latest-result source linkage; cancellation authority shutdown; and fail-closed route vocabularies.

Highest-impact failure modes: A historical receipt evades classification; route-owned fields validate against themselves instead of stage-native evidence; a known outcome is rewritten with a matching action; correction authority is substituted or becomes invalid after legitimate consumption; output identity disagrees with canonical review identity; or cancellation retains active authority.

Changed boundaries: `resolve_recorded_proposal_correction_capability` to the reusable receipt validator; route vocabulary to closed-set validation; completed-receipt enumeration to per-receipt reconstruction; and receipt route to effective-capability history.

Evidence expected: Two-receipt route tamper tests; independent review ID and outcome evidence; output-to-canonical identity equality; consumed and invalidated correction history; missing or mismatched capability rejection; unknown-value precedence; and cancellation authority shutdown.

Areas requiring direct inspection: `resolve_recorded_proposal_review_receipt`; completed receipt classification; `project_proposal_review_result`; `proposal_review_route_binding`; receipt output/canonical-sync validation; the historical receipt fixtures; and cancellation contrasts.

Areas intentionally out of scope: M5, M6, public command activation, legacy cutover, schemas, generated adapters, external actions, final verification, and PR readiness.

Risk classes considered: Durable-state integrity, authorization/capability binding, recovery and cancellation, closed-vocabulary validation, compatibility with persisted histories, negative-boundary coverage, and scope isolation were applicable. Secrets, privacy, network access, deployment, UI, and performance beyond linear receipt scanning were not applicable.

Falsifiable review questions: Can a non-latest route field be rewritten with zero errors? Can changing capability kind or stage evade classification? Can unknown route values bypass vocabulary checks? Can later authority rewrite historical correction? Can a consumed or invalidated recorded capability remain auditable? Can route review ID differ from stage evidence? Can output identity disagree with canonical review identity?

## Diff summary

Commit `3d014149` adds a reusable completed proposal-review receipt validator and invokes it for every recognized completed proposal-review receipt. It binds proposal identity to receipt inputs, review-record identity to canonical-sync observations, target to the receipt target, and correction-loop authority to one exact historical capability basis. It also adds closed-vocabulary checks for route outcome and routing action.

The tests add two-receipt historical fixtures, empty/target/identity tamper cases, unknown-value precedence, consumed and invalidated correction-capability history, missing and mismatched capability rejection, and active-correction cancellation shutdown.

The correction closes several concrete historical-route gaps, but the canonical projection still takes `review_id` and known `outcome` directly from the route being validated. Output evidence identity also remains independent from the canonical review evidence identity. Those self-consistent contradictions are accepted.

## Prior-finding reconciliation

| Prior finding | R10 result | Evidence |
| --- | --- | --- |
| `BRF-M4-CR16` | failed-remediation | Empty or missing routes, wrong target, route proposal/review identity contradictions, unknown outcome/action, and missing or mismatched correction capability now fail. The core requirement that every receipt independently prove exact stage-native route facts remains incomplete because review ID and known outcome are route-owned, and output identity can disagree with canonical review identity. The residual defect is `BRF-M4-CR17`. |

## Findings

## Finding BRF-M4-CR17

Finding ID: BRF-M4-CR17
Severity: major
Location: `scripts/validate_workflow_automation.py:280-324`; `scripts/validate_workflow_automation.py:1614-1639`; coverage gap in `scripts/test-validate-workflow-automation.py:700-800`
Evidence: The validator independently compares the route's reviewed proposal identity with `input_identities.proposal` and its review-record identity with `canonical_sync.observed_identities.proposal-review`. It then takes `review_id` and `outcome` from the route itself, passes those values to `project_proposal_review_result`, and compares the resulting route with the same source route. Direct two-receipt probes retained a valid latest receipt, changed only the historical `review_id`, and returned zero errors. Replacing `approved` with the known `changes-requested` outcome while preserving its canonical exact-target action also returned zero errors. Coordinately rewriting the latest route/result review ID or known outcome also returned zero errors. A separate probe changed the historical receipt output identity while leaving canonical-sync evidence and observed review identity unchanged; validation again returned zero errors. The tests mutate empty route, target, proposal identity, review-record identity, and unknown values, but do not mutate a non-empty review ID, substitute another known outcome with its canonical action, or contradict output and canonical identities. The 61-test validator suite passes while all three direct contradictions remain accepted.
Required outcome: Every completed proposal-review receipt must bind review ID, selected known outcome, and review output identity to independently observed stage-native completion evidence. A fabricated review ID, alternative known outcome with an otherwise canonical route, or output identity that disagrees with canonical review evidence must fail validation.
Safe resolution path: Use the existing stage-native proposal-review parser and evidence owner to persist or re-read independently integrity-bound completion facts for review ID and outcome, then compare the route with those facts. Require the proposal-review output evidence identity to equal its canonical-sync evidence and observed review identity. Add two-receipt regressions for fabricated review ID, every alternative known outcome with its otherwise canonical route, and output/canonical identity disagreement while retaining the existing empty, target, identity, unknown-value, correction-capability, and cancellation contrasts.
needs-decision rationale: none; the approved durable occurrence, completed-receipt consistency, and tracked-evidence requirements already require fail-closed behavior. Choosing the durable independent evidence representation versus parser-backed revalidation is implementation design within M4 review-resolution.
auto_fix_class: none

## Requirement fidelity

| Requirement property | Result | Evidence |
| --- | --- | --- |
| BRF-R047 records exact review ID and one closed outcome | block | Both values are taken from the route being validated and can be changed to other valid values without contradiction. |
| BRF-R054 correction requires route-time authority | concern | Recorded correction capability identity and basis are checked after correction-loop selection, but a known outcome rewrite can change whether correction was selected or absent. |
| BRF-R076 completed output and canonical state remain consistent | block | A historical review output identity can disagree with canonical-sync evidence and still validate. |
| BRF-R100 status and resume rely on tracked identities and receipts | block | Tracked route values are not independently reproducible from tracked stage-native facts. |
| BRF-R101 unknown values fail before consistency | pass | Receipt-route outcome and routing-action vocabularies are checked before semantic validation. |
| BRF-R102 unknown regressions accompany closed validators | pass | Direct historical unknown-outcome and unknown-action tests are present. |
| T10 exhaustive proposal-review route semantics | block for historical integrity | Ordinary route matrices pass, but a retained known outcome can be rewritten self-consistently. |
| T11 correction authority is bounded | concern | Historical capability identity and basis checks pass once correction-loop is selected, but the outcome that selects the loop remains mutable. |
| T16 cancellation preserves evidence and shuts down authority | pass for the tested path | Cancellation rejects active correction capability and accepts the invalidated state; the residual route-integrity defect still applies to cancelled history. |

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | BRF-R047, BRF-R076, and BRF-R100 remain incomplete for historical route facts. |
| Test coverage | block | Fabricated review ID, alternative known outcome, and output/canonical identity contradictions are absent. |
| Edge cases | block | Self-consistent route tampering bypasses validation. |
| Error handling | block | Contradictory completed receipt evidence produces no error. |
| Architecture boundaries | concern | The validator stays within the approved Python boundary but does not consume or persist the stage-native facts originally derived by the state writer. |
| Compatibility | pass | Public, legacy-adapter, migration, and M5/M6 behavior are unchanged. |
| Security/privacy | concern | No secret or privacy surface changed; historical authorization meaning remains mutable. |
| Derived artifact currency | pass | No generated artifact was changed. |
| Unrelated changes | pass | The implementation diff is scoped to validator behavior, tests, and required lifecycle evidence. |
| Validation evidence | block for sufficiency | The selected suites pass but omit the direct counterexamples. |

## Validation and direct proof

- Independently reran all 61 workflow-automation validator tests; they passed.
- Independently reran `git diff --check 3d014149^ 3d014149`; it passed.
- The separate reviewer reran 7 proposal-review, 8 proposal-correction, 7 cancellation, and 15 policy tests; they passed.
- Direct historical review-ID rewrite returned zero errors.
- Direct historical and latest known-outcome rewrites returned zero errors.
- The separate reviewer projected each of the four known outcomes with fabricated review IDs; all validated.
- Direct historical output/canonical identity disagreement returned zero errors.
- The released 11-check broad-smoke evidence was challenged but not independently rerun during review.

## No-finding rationale

Not applicable; this review has one material finding.

## Residual risks

Rereview should prove independent review ID and outcome binding for every completed receipt, exact output-to-canonical identity equality, all four known historical outcome contrasts, retained correction-authority lifecycle behavior, unknown-value precedence, and cancellation shutdown. M5 and M6 remain out of scope.

## Milestone handoff

- Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `BRF-M4-CR17`
- Remaining in-scope implementation milestones: M4 resolution and rereview, M5, M6
- Next stage: review-resolution M4
- Final closeout readiness: not ready
- Reason: implementation-milestones-open, review-findings-open, explain-change-pending, verify-pending, pr-handoff-pending; review-state=open; open-count=1; open-findings=BRF-M4-CR17

This direct review remains isolated. It records the finding and does not automatically apply a fix or enter review-resolution.
