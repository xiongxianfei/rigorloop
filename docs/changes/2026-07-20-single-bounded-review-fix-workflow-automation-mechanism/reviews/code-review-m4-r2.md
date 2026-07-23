# Code Review: M4 R2 Transactional Authoring Correction

Review ID: code-review-m4-r2
Stage: code-review
Round: M4 R2
Reviewer: independent blind-review context
Target: M4 correction commit `0136c851`
Reviewed artifact: M4 correction commit `0136c851`
Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-22
Recording status: recorded
Material findings: BRF-M4-CR3, BRF-M4-CR4
Immediate next stage: review-resolution

Automated review: yes
Review gate outcome: stop
Native review status: changes-requested
Independence level: L2
Reviewer context ID: m2-r2-blind-review-reused-as-m4-r2
Context separation mechanism: A separate existing agent context received a neutral packet, recorded the blind-first risk map, and stopped before later evidence release.
Risk tier: elevated
Risk-tier triggers: Authorization, durable state, parser ownership, correction safety, and transaction recovery changed.
Risk-tier classifier: Approved review-independence risk-tier contract.
Governing artifacts: `specs/single-bounded-review-fix-workflow-automation.md`; `specs/single-bounded-review-fix-workflow-automation.test.md`; `docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md`; approved workflow architecture and ADR.
Formal criteria: Code-review checklist; BRF-R047-R062, BRF-R065-R066, BRF-R078-R080, BRF-R087-R090, BRF-R099-R100; M4 T10-T12, T24, T26, and MP1 proof.
Initial packet inventory: scripts/workflow_automation.py@0136c851#sha256:94fff7dd2225fdcd1fc49e390e59df31d3cf015022c73bbab8c71d536fc00a8b; scripts/workflow_automation_state.py@0136c851#sha256:dd0f5432a76512f42401052e1022e3b15793c7a64304cdb3975ca792c168b40b; scripts/artifact_lifecycle_validation.py@0136c851#sha256:b9bd53e6bbef2b23be6cc13b453cac846389099232560368727ddde9e38e8ecb; specs/single-bounded-review-fix-workflow-automation.md@0136c851#sha256:59241a5e4968a0d6ba60f9772eed56ab8b9e79859a0be1c94e7c77840c724070; docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md@0136c851#sha256:f30ff832c71cb26a0722a273feadf7c476cf97f27de59ad40461bd47992a71f1
Initial packet contains prohibited context: no
Prompt template version: code-review-v1
Initial packet hash: sha256:2a66828e69c2f86f60c6bcad0436666bc1f6fc1f60c8dc5e73fa855ca85f1761
Manifest owner: workflow orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded

Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: `scripts/artifact_lifecycle_validation.py`; `scripts/workflow_automation.py`; `scripts/workflow_automation_state.py`; their changed tests and review evidence
Requirement-fidelity matched path triggers: scripts/*validator*, docs/changes/**/reviews/, docs/changes/**/review-*.md
Requirement-fidelity matched category triggers: autoprogression gates, artifact lifecycle validators, closed enums
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause, property decomposition, production diff, tests, validation evidence, prior findings

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, review log, review resolution, active plan, plan index, and change metadata
- Open blockers: `BRF-M4-CR3` and `BRF-M4-CR4` block M4 closeout
- Next stage: review-resolution M4
- Review status: changes-requested
- Material findings: `BRF-M4-CR3`, `BRF-M4-CR4`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m4-r2.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m4-r2`
- Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M4 resolution needed, M5, M6
- Required review-resolution: yes
- Finding IDs: `BRF-M4-CR3`, `BRF-M4-CR4`
- Verify readiness: not-claimed

## Review inputs

- Review surface: correction commit `0136c851` against `b4891139`, with production code inspected before changed tests.
- Tracked governing branch state: commit `0136c851`; only this R2 review evidence was untracked during review.
- Governing requirements: BRF-R047-R062, BRF-R065-R066, BRF-R078-R080, BRF-R087-R090, BRF-R099-R100.
- Test contract: T10-T12, T24, T26, MP1, and CMD14-CMD20.
- Architecture: stage-owned evidence, sole state writer, prepared receipt, exact effective-capability binding, and capability-stable recovery.
- Prior review and resolution: `code-review-m4-r1.md` and its accepted BRF-M4-CR1/CR2 dispositions, released only after the risk map.

## Blind-first risk map

Affected behavior: Proposal-review correction routing; persisted proposal-correction authority; non-public authoring coordination; active-capability reuse; stage-native completion verification; parser-backed artifact and review routing.

Highest-impact failure modes: Caller-fabricated correction evidence; skipped post-mutation convergence proof; incomplete or vacuously valid budgets; stale persisted-capability reuse; consumed authority treated as executable; incomplete lifecycle completion; parser divergence or evidence swap; review gate collapse; stale review reuse; premature public reachability; incomplete receipt recovery.

Changed boundaries: Persisted authority to executable capability; formal review evidence to correction eligibility; prepared receipt to stage mutation and completion; lifecycle parsers to automation proof; consumed capability to routing; non-public harness to public and isolated entry points.

Evidence expected: Tracked-evidence correction fixtures; complete invalid-budget matrix; pre/post-mutation proof; persisted-capability reuse contrasts; stage-native positive and negative proof for every M4 stage; receipt-order and failure-injection traces; identity-stable rereads; four-outcome routing; static public-isolation proof.

Areas requiring direct inspection: `resolve_proposal_correction_authority`; `evaluate_proposal_review`; `evaluate_proposal_correction`; `coordinate_non_public_authoring_stage`; `coordinate_one_stage`; `verify_transition_completion`; `inspect_lifecycle_artifact`; formal-review, lifecycle, handoff, and policy dependencies; changed tests and public call graph.

Areas intentionally out of scope: M5 implementation and verification integration; M6 public cutover and legacy adapter activation; PR, release, deployment, merge, credentials, and external actions except premature reachability; unrelated lifecycle history.

Risk classes considered: Authorization least privilege and single use; independent review and clean-gate fidelity; deterministic correction safety; durable identity provenance; stage-native evidence; repository/path containment; transaction recovery; closed vocabularies; compatibility isolation; observability; multi-surface requirement fidelity.

Falsifiable review questions: Can opaque hash-matching caller data substitute for tracked evidence? Can empty or invalid budgets route to correction? Are post-mutation shrinkage, validation, identity change, historical review, stale gate, and fresh review authority independently proven? Can stale capabilities be reused? Can weak artifact shapes satisfy completion? Can evidence change between verification and routing? Can any non-approved review advance? Can any public or isolated path reach the harness? Are failures durably recoverable?

## Diff summary

The correction adds an internal authoring coordinator, expands stage-native completion from proposal review to all M4 authoring stages, permits reuse of a persisted active capability, exposes lifecycle inspection to the state verifier, and replaces correction booleans with a typed authority resolver.

It also adds one receipt-backed spec fixture, one receipt-backed proposal-correction fixture, a stage-verifier registry equality test, authority hash contrasts, and lifecycle handoff updates.

The composed path remains incomplete at two trust boundaries: non-review receipt recovery still requires review-log evidence, while correction preflight and completion still rely on caller dictionaries and do not prove the required post-mutation convergence or fresh review authority.

## Prior-finding reconciliation

| Prior finding | R2 result | Evidence |
| --- | --- | --- |
| `BRF-M4-CR1` | failed-remediation | A representative spec transition completes, but every completed non-review receipt pauses during recovery, per `BRF-M4-CR3`; the registry-equality test does not prove semantic traversal through every M4 stage. |
| `BRF-M4-CR2` | failed-remediation | Caller booleans were removed, but caller-supplied dictionaries and unverified post-mutation claims still authorize and route correction, per `BRF-M4-CR4`. |

## Findings

## Finding BRF-M4-CR3

Finding ID: BRF-M4-CR3
Severity: major
Location: `scripts/workflow_automation_state.py:348-410`, `scripts/workflow_automation_state.py:548-562`, `scripts/workflow_automation.py:683-695`; coverage gap in `scripts/test-workflow-automation-state.py:79-97` and `scripts/test-workflow-automation.py:1213-1289`
Evidence: Lifecycle, plan, and architecture-assessment completion proofs contain only stage evidence identities. Completed recovery nevertheless unconditionally requires exactly one identity ending in `-log`; only formal-review proofs produce one. A valid completed `spec`, `plan`, `architecture-assessment`, `architecture`, or `test-spec` receipt therefore pauses with `canonical-review-log-identity-drift` instead of returning `completed-evidence-current`. The new all-stage test asserts only registry membership, and the only receipt-backed authoring fixture completes one unrelated copied spec without exercising recovery or the remaining stages. Formal review and assessment routing also reread the raw evidence path after finalization without comparing the reread identity to the receipt-verified identity.
Required outcome: Every M4 stage must have stage-appropriate completion and completed-recovery proof that compares the originally persisted identities without requiring irrelevant review-log evidence, and route selection must use the verifier-normalized proof or recheck the exact persisted identity before parsing.
Safe resolution path: Make completed recovery compare the complete normalized identity map generically, with review-log comparison conditional on a formal-review proof; route from `VerifiedCompletion` or rehash and compare before parsing; add positive completed-recovery and drift/TOCTOU contrasts for authored artifacts, architecture assessment, plan, and every formal review stage; replace registry-only proof with stage-semantic fixtures.
needs-decision rationale: none; the approved receipt recovery and stage-owned evidence contracts determine the correction.
auto_fix_class: none

## Finding BRF-M4-CR4

Finding ID: BRF-M4-CR4
Severity: major
Location: `scripts/workflow_automation.py:280-356`, `scripts/workflow_automation.py:380-508`, `scripts/workflow_automation.py:622-682`, `scripts/validate_workflow_automation.py:951-970`; coverage gap in `scripts/test-workflow-automation.py:1071-1211` and `scripts/test-workflow-automation.py:1291-1417`
Evidence: `resolve_proposal_correction_authority` hashes caller-supplied review ID, finding IDs, classifications, and budget instead of parsing the current formal review and review-resolution artifacts. It returns the caller budget and never proves that `scope.correction_budget` hashes to the stored identity; a valid-state probe changed persisted remaining budget while leaving its identity unchanged, the validator returned no error, and the resolver returned the caller's older budget. `evaluate_proposal_review` also treats an empty authority budget as remaining because `all(...)` is vacuously true. The coordinator calls correction evaluation with `mutation_completed=False`, whose early `authorized` return occurs before deterministic-validation and proposal-identity checks. After mutation the verifier proves only that proposal bytes changed; the coordinator does not re-evaluate convergence, validate historical occurrence or stale-gate state, or derive a fresh proposal-review capability before routing. A direct probe authorized identical proposal identities with deterministic validation false, and the positive fixture supplies `unresolved_after=()` itself while merely appending a newline.
Required outcome: Correction authority and convergence must be derived from current repository-backed formal review, review-resolution, classifier, budget, and proposal evidence; persisted budget content must match its identity; every invalid or empty budget must pause; post-mutation proof must independently establish deterministic validation, strict finding-set shrinkage, changed proposal identity, preserved review history, stale prior gate, and newly derived proposal-review authority.
Safe resolution path: Add repository-path inputs bound to the capability basis and parse them through existing review/review-resolution parsers; recompute structured identities for persisted scope budget and classification/finding evidence; validate the closed budget key/value limits at review routing; split preflight from post-mutation evaluation and run the latter from independently reread outputs; persist stale-gate/history evidence and derive a new review capability before returning the rereview route; add forged caller, stale persisted budget, empty/extra/over-limit budget, false shrinkage/validation, unchanged identity, old-review reuse, and fresh-capability tests.
needs-decision rationale: none; the approved identity-bound capability and correction-convergence requirements already select the safe outcome.
auto_fix_class: none

## Requirement fidelity

| Requirement property | Result | Evidence |
| --- | --- | --- |
| Review occurrence and clean gate remain separate | pass | Four known outcomes and exact/later target distinctions remain explicit; unknown and unchanged-inconclusive paths fail closed. |
| Later `changes-requested` requires current active correction authority and remaining budget | block | Empty authority budget routes to correction, and current persisted budget content is not identity-checked. |
| Driver-owned correction pauses on stale/new/non-shrinking/exhausted/invalid evidence | block | Preflight consumes caller claims; post-mutation shrinkage and deterministic validation are not reread or evaluated. |
| Proposal mutation preserves history, stales the gate, and requires new review capability | block | Only changed proposal bytes and consumed correction capability are proven; no fresh review capability or stale-gate/history proof exists. |
| Stage-owned evidence and tracked receipts govern authoring progression | block | Non-review completed recovery always pauses, and representative lifecycle proof accepts a broad class without end-to-end stage coverage. |
| Direct/public/legacy/bugfix isolation remains intact | pass | No non-test call site reaches the internal harness; public skill and adapter surfaces are unchanged. |
| External actions remain excluded | pass | No PR, push, publication, deployment, credential, or external-system surface changed. |
| BRF-R099 public result projection | deferred, not a finding | The approved proof map assigns final observable result coverage to M6; M4 uses an internal harness result. |

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | BRF-R054, BRF-R065-R066, BRF-R078, and BRF-R100 remain incomplete at executable boundaries. |
| Test coverage | block | Registry equality and two representative transactions do not prove all-stage recovery, canonical correction evidence, or post-mutation convergence. |
| Edge cases | block | Empty budget, stale persisted budget content, false post-mutation claims, non-review completed recovery, and raw-path evidence drift are uncovered. |
| Error handling | block | Valid completed authored receipts pause for a review-log identity they cannot possess. |
| Architecture boundaries | block | Recovery is review-specific instead of stage-native, and correction substitutes caller data for stage-owned review-resolution evidence. |
| Compatibility | pass | Public and legacy routing remain unchanged and unreachable from the M4 harness. |
| Security/privacy | concern | No secrets or external actions changed, but executable authority remains caller-substitutable. |
| Derived artifact currency | pass | No generated adapter or derived public output changed. |
| Unrelated changes | pass | The correction is limited to M4 runtime, tests, and required lifecycle evidence. |
| Validation evidence | concern | CMD14-CMD20 and broad suites pass, but direct counterexamples reproduce both trust-boundary defects. |

## Validation and direct proof

- CMD14-CMD20, the 33 engine tests, 49 state/recovery tests, and 52 automation-validator tests exited successfully.
- Public call-graph inspection found no non-test caller for `coordinate_non_public_authoring_stage`; public workflow and adapter surfaces are unchanged.
- Direct empty-budget evaluation returned `correction-loop`.
- Direct correction evaluation returned `authorized` with false deterministic validation and unchanged proposal identities when `mutation_completed=False`.
- Direct valid-state budget probe changed persisted remaining budget without updating its identity; durable validation returned no errors and the resolver returned caller-supplied older values.
- Source-level recovery proof shows every non-review `VerifiedCompletion` lacks a `-log` identity while completed recovery requires one unconditionally.
- `git diff b4891139..0136c851 --check` passed.

## No-finding rationale

Not applicable; this review has two material findings.

## Residual risks

After correction, rereview should execute a stage-semantic matrix for every M4 stage, inject failures before and after finalization, and prove correction from real tracked review-resolution evidence through fresh proposal-review capability derivation. M5-M6 public composition and final holistic behavior remain out of scope.

## Milestone handoff

- Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `BRF-M4-CR3` and `BRF-M4-CR4`
- Remaining in-scope implementation milestones: M4 resolution needed, M5, M6
- Next stage: review-resolution M4
- Final closeout readiness: not ready because M4 has two open findings and M5-M6, final holistic review, explanation, verification, and PR handoff remain.

## Recommended next stage

This review is recorded before any review-driven fix.
Enter `review-resolution` for `BRF-M4-CR3` and `BRF-M4-CR4`, return M4 to `review-requested` after correction, and rerun code-review M4.
Do not start M5 while either finding remains open.
