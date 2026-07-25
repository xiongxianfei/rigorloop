# Code Review M4 R1

Review ID: code-review-m4-r1
Stage: code-review
Round: M4 R1
Reviewer: Codex code-review skill in isolated direct-review mode
Target: M4 implementation commit `0b0cd798`
Reviewed artifact: M4 implementation commit `0b0cd798`
Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-22
Recording status: recorded
Material findings: BRF-M4-CR1, BRF-M4-CR2
Immediate next stage: review-resolution

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, review log, review resolution, active plan, plan index, and change metadata
- Open blockers: `BRF-M4-CR1` and `BRF-M4-CR2` block M4 closeout; neither requires a product, spec, architecture, or ownership decision
- Next stage: review-resolution M4
- Review status: changes-requested
- Material findings: `BRF-M4-CR1`, `BRF-M4-CR2`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m4-r1.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m4-r1`
- Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M4 resolution needed, M5, M6
- Required review-resolution: yes
- Finding IDs: `BRF-M4-CR1`, `BRF-M4-CR2`
- Verify readiness: not-claimed

## Review Inputs

- Diff surface: implementation commit `0b0cd798` against its first parent.
- Tracked governing branch state: clean worktree at `0b0cd798` before review evidence recording.
- Governing spec: `BRF-R047`-`BRF-R062`, `BRF-R065`-`BRF-R066`, `BRF-R078`-`BRF-R080`, `BRF-R087`-`BRF-R090`, and `BRF-R099`-`BRF-R100`.
- Test spec: T10-T12, T24, T26, MP1, and CMD14-CMD20.
- Architecture and ADR: stage-owning skill coordination, effective-capability authority, prepared receipts, stage-native completion, and the non-public M4 boundary.
- Active plan: M4 `review-requested` handoff and its named validation commands.

## Review Mode and Risk Map

This was an isolated direct review with an intentional assumption reset and diff-first inspection. It does not claim a workflow-managed automated-review manifest or automatic downstream handoff.

- Affected behavior: proposal-review outcome routing, proposal correction, conditional authoring progression, and non-public isolation through `test-spec-review`.
- Highest-impact failures: review occurrence conflated with approval, correction without identity-bound authority, correction after finding-class drift, authoring stages advanced without stage-owned evidence, and partial M4 routing becoming publicly reachable.
- Changed boundaries: formal review evidence to clean-gate routing, effective correction capability to proposal mutation, and stage-policy results to downstream authoring transitions.
- Expected evidence: one receipt-backed non-public path derives the exact capability, invokes a stage owner, verifies stage-native completion, synchronizes canonical state, and cannot be entered by public, direct-skill, bugfix, or legacy contexts.
- Direct-inspection areas: new M4 evaluators, `coordinate_one_stage`, `verify_transition_completion`, M4 call sites, and CMD15-CMD18 tests.
- Intentionally out of scope: M5 implementation/review/verification integration, M6 public activation, final holistic review, verification, PR, release, deployment, and external actions.
- Applicable risk classes: authorization integrity, review independence, workflow-state integrity, correction convergence, compatibility, and proof sufficiency.
- Non-applicable risk classes: network, credentials, deployment, database, UI, and generated adapter content.
- Falsifiable questions: Can any non-test caller execute the M4 path? Can downstream authoring complete through the state verifier? Can caller booleans or strings manufacture correction authority? Can omission of prior finding classifications permit a changed class?

## Diff Summary

The commit adds three immutable decision records and four helper/evaluator functions for proposal review, proposal correction, and authoring routing. It adds selector-addressable tests for proposal-review outcomes, target mutation, correction guardrails, architecture applicability, and non-public invocation contexts. It also updates M4 plan and validation evidence.

The new M4 functions are not connected to `coordinate_one_stage`, the state adapter, or a non-test invocation path. The state-native completion verifier still supports only `proposal-review`, so `spec`, `spec-review`, architecture, plan, and test-spec transitions cannot complete through the receipt-backed engine. Correction decisions also accept unbound caller assertions instead of the exact persisted capability, review, finding-classification, budget, validation, and artifact identities.

## Findings

## Finding BRF-M4-CR1

Finding ID: BRF-M4-CR1
Severity: major
Location: `scripts/workflow_automation.py:243-523`, `scripts/workflow_automation_state.py:48-50` and `scripts/workflow_automation_state.py:276-297`; coverage gap in `scripts/test-workflow-automation.py:969-1222`
Evidence: Repository call-site inspection finds `evaluate_non_public_authoring_route` and `evaluate_proposal_correction` only at their definitions and in tests. `verify_transition_completion` maps only `proposal-review`; every other M4 authoring stage returns `stage-native-verifier-unavailable`. CMD15-CMD18 pass because they call pure decision helpers and never prepare/finalize a transition, invoke a stage owner, verify a spec/architecture/plan/test-spec artifact, or synchronize canonical state. This does not satisfy the M4 plan step to connect proposal correction and post-proposal authoring policies to stage-native completion evidence, T10-T12/T26 integration steps, or `BRF-R078` and `BRF-R100`.
Required outcome: M4 must provide one explicitly non-public, receipt-backed integration path that resolves current tracked evidence, derives the exact effective capability, invokes the stage-owning operation, verifies stage-native completion for every M4 stage through `test-spec-review`, synchronizes canonical state, and routes from the verified result without exposing public or legacy entry.
Safe resolution path: Extend the state-native verifier with stage-specific artifact/review proof for `spec`, `spec-review`, `architecture-assessment`, `architecture`, `architecture-review`, `plan`, `plan-review`, `test-spec`, and `test-spec-review`; compose those verifiers through `coordinate_one_stage`; replace helper-only CMD15-CMD18 positives with temporary-repository integration fixtures that assert prepared receipt, stage invocation, canonical synchronization, consumed capability, exact target stopping, conditional not-applicable evidence, and public/direct/legacy rejection.
needs-decision rationale: none; the approved spec, architecture, plan, and test spec already select this integration boundary.
auto_fix_class: none

## Finding BRF-M4-CR2

Finding ID: BRF-M4-CR2
Severity: major
Location: `scripts/workflow_automation.py:258-337` and `scripts/workflow_automation.py:353-434`; coverage gap in `scripts/test-workflow-automation.py:999-1009` and `scripts/test-workflow-automation.py:1058-1135`
Evidence: `evaluate_proposal_review` enters `correction-loop` from caller-supplied booleans without an effective-capability ID or persisted capability lookup. `evaluate_proposal_correction` accepts caller-supplied `capability_kind`, `capability_status`, review identities, budget, paths, validation result, and before/after proposal identities. The reviewed classification map is optional. A direct probe omitting it returned `rereview-required` for a current `mechanical` classification, so a changed review classification is undetectable unless the caller volunteers the old value. The same probe manufactured a correction-loop route with `correction_capability_active=True` and `correction_budget_remaining=True` and no durable authority or receipt. This violates `BRF-R054`, `BRF-R062`, `BRF-R065`, `BRF-R066`, and the tracked-identity requirement in `BRF-R100`.
Required outcome: Proposal correction routing and completion must derive authority and all safety evidence from the exact active persisted effective capability and its current parent/basis, plus the current formal review and review-resolution records; omission, drift, or caller substitution of any classification, finding set, budget identity, path scope, validation evidence, or proposal identity must pause or fail closed.
Safe resolution path: Replace boolean/string authority inputs with a capability ID resolved through canonical state; require the reviewed and current finding classifications as identity-bound evidence; bind remaining budget to the capability's `correction_budget_identity`; derive paths and proposal identities from rehashed repository artifacts; record mutation through a prepared receipt; invalidate the old proposal review and require a newly derived proposal-review capability. Add omission, forged-active-status, changed-class, stale-budget-identity, forged-validation, forged-after-identity, and old-review continuation regressions.
needs-decision rationale: none; the two-level authority and correction-convergence contracts already determine the safe implementation.
auto_fix_class: none

## Requirement Fidelity

| Requirement property | Result | Evidence |
| --- | --- | --- |
| Proposal-review occurrence and clean gate remain separate | pass | The four closed outcomes and exact/later target distinctions are represented directly. |
| Unknown and unchanged-inconclusive proposal review fail closed | pass | Targeted CMD15 tests raise before a valid occurrence or rerun. |
| Proposal correction uses current identity-bound authority and evidence | block | Caller assertions can manufacture authority and omit the reviewed classification map. |
| Stage owners and stage-native evidence govern authoring progression | block | M4 evaluators have no production call site and post-proposal stages have no completion verifier. |
| Conditional architecture behavior is deterministic | concern | Pure routing results are correct, but no receipt/result integration proves the recorded not-applicable transition required by T26. |
| Direct, bugfix, public, and legacy entry remain isolated | pass with limitation | The public skill diff is empty and context tests pause, but they do not exercise a composed stateful invocation path. |
| Public activation and external actions remain excluded | pass | No skill, adapter, network, credential, PR, or external-action surface changed. |

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | `BRF-R054`, `BRF-R065`-`BRF-R066`, `BRF-R078`, and `BRF-R100` are not enforced at an executable integration boundary. |
| Test coverage | block | CMD15-CMD18 pass helper-only tests and do not execute the required receipt-backed stage chain. |
| Edge cases | block | Omitted prior classifications and caller-manufactured correction authority return an allowed route. |
| Error handling | concern | Unknown later review outcomes pause safely, but no stateful path proves fail-closed recovery for M4 stages. |
| Architecture boundaries | block | The coordinator/state-verifier boundary is bypassed rather than extended for M4. |
| Compatibility | pass | Public and legacy skill/adapter surfaces are unchanged. |
| Security/privacy | concern | No secrets or external actions were added, but executable authorization is modeled as caller assertions rather than canonical capability evidence. |
| Derived artifact currency | pass | No generated or derived adapter output changed. |
| Unrelated changes | pass | Commit `0b0cd798` is scoped to M4 code, tests, and lifecycle evidence. |
| Validation evidence | concern | CMD14-CMD20 pass, but direct call-site and adversarial probes show the selected tests do not prove M4 integration or authority binding. |

## Validation and Direct Proof

- CMD15 passed 3 selected tests.
- CMD16 passed 1 selected test.
- CMD17 passed 3 selected tests.
- CMD18 passed 2 selected tests.
- CMD19 passed 103 review-artifact tests.
- CMD20 passed 259 skill tests.
- CMD14 passed 156 lifecycle tests.
- Call-site inspection found no non-test caller for the M4 correction or authoring-route evaluators.
- The state verifier returned an unavailable verifier path for every stage absent from its proposal-review-only map.
- Direct correction probe without `reviewed_finding_classifications` returned `rereview-required`.
- Direct proposal-review probe with caller booleans and no durable capability returned `correction-loop`.
- `git diff 0b0cd798^ 0b0cd798 -- skills/ docs/workflows.md dist/adapters/manifest.yaml` was empty, confirming no public cutover occurred.

## MP1 Result

MP1 does not pass for M4. The existing proposal-review coordinator test proves same-pass target mutation is rejected, and the public skill is unchanged. However, there is no composed non-public M4 invocation path to inspect for durable review evidence and isolated run behavior across post-proposal authoring. The helper-only context test cannot establish that a real invocation creates no run for direct/bugfix calls or advances a run only for authorized workflow-managed calls.

## No-Finding Rationale

Not applicable. This review has two material findings.

## Residual Risks

After resolving the two findings, rereview should challenge unknown post-proposal review outcomes, exact review targets with non-approval outcomes, stale latest-review selection, not-applicable receipt evidence, and interrupted stage completion. M5-M6 and final holistic behavior remain out of scope for this milestone review.

## Milestone Handoff

- Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `BRF-M4-CR1` and `BRF-M4-CR2`
- Remaining in-scope implementation milestones: M4 resolution needed, M5, M6
- Next stage: review-resolution M4
- Final closeout readiness: not ready because M4 has two open findings and M5-M6, final holistic review, explanation, verification, and PR handoff remain.

## Recommended Next Stage

This direct review remains isolated: no automatic downstream handoff or implementation correction was performed.
Enter `review-resolution` for `BRF-M4-CR1` and `BRF-M4-CR2`, return M4 to `review-requested` after correction, and rerun code-review M4.
Do not start M5 while either finding remains open.
