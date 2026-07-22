# Code Review M3 R1

Review ID: code-review-m3-r1
Stage: code-review
Round: M3 R1
Reviewer: Codex code-review skill
Target: M3 commit `b9a661c0`
Reviewed artifact: M3 commit `b9a661c0`
Reviewed milestone: M3. Target Binding, Canonical Position, and Capability Evaluation
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-22
Recording status: recorded
Material findings: BRF-M3-CR1, BRF-M3-CR2, BRF-M3-CR3, BRF-M3-CR4
Immediate next stage: review-resolution

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m3-r1.md`, `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`, `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md`, `docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md`, `docs/plan.md`, `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/change.yaml`
- Open blockers: none
- Next stage: review-resolution M3
- Review status: changes-requested
- Material findings: BRF-M3-CR1, BRF-M3-CR2, BRF-M3-CR3, BRF-M3-CR4
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m3-r1.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m3-r1`
- Reviewed milestone: M3. Target Binding, Canonical Position, and Capability Evaluation
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3 resolution needed, M4, M5, M6
- Required review-resolution: yes
- Finding IDs: BRF-M3-CR1, BRF-M3-CR2, BRF-M3-CR3, BRF-M3-CR4
- Verify readiness: not-claimed

## Review Inputs

- Diff range: `f7bdcec8..b9a661c0`.
- Review surface: the new non-public coordinator and tests, lifecycle-parser integration tests, and M3 lifecycle handoff evidence.
- Governing spec: `specs/single-bounded-review-fix-workflow-automation.md`, especially `BRF-R009`-`BRF-R046`, `BRF-R068`-`BRF-R072`, and `BRF-R078`-`BRF-R080`.
- Test spec: `specs/single-bounded-review-fix-workflow-automation.test.md`, especially T4-T9 and T14.
- Architecture and ADR: the approved canonical-position, exact capability, sole-writer, prepared-receipt, stage-owned evidence, and canonical-synchronization boundaries.
- Plan milestone: `docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md` M3 and its tracked `review-requested` handoff.
- Validation evidence inspected after direct review: CMD10-CMD14, state/validator regressions, compilation, lifecycle checks, and broad-smoke evidence recorded by implementation.

## Risk Map

Before consulting the recorded validation summary, the review prioritized five falsifiable risks: persisted targets could retain a syntactically concrete but semantically wrong completion predicate; canonical evidence could be caller-asserted rather than bound to the invoked stage; correction authority could ignore the parent's budget; stage output could be mistaken for canonical synchronization; and the non-public boundary could accidentally alter public routing. Direct inspection focused on target resume and validation, pre-plan evidence and drift comparison, capability scope derivation, coordinator preflight/finalization, public skill diffs, and the exact M3 test matrix. Stage-native authoring and implementation integration remain intentionally assigned to M4 and M5.

## Diff Summary

M3 adds a non-public workflow coordinator, current and legacy command normalization, structured target binding, active-plan parsing, pre-plan and post-plan position resolution, parent authorization creation, capability derivation/invalidation, prepared-receipt coordination, and focused target/position/capability tests. Public skills and legacy writers remain unchanged. The main structural boundaries are present, but target completion is not policy-bound after initial construction, canonical evidence is not bound to coordinator invocation, correction budgets are not enforced during capability derivation, and the coordinator synthesizes successful canonical synchronization from any non-empty output.

## Findings

### BRF-M3-CR1: Canonical evidence and capability identities are not bound to stage invocation

Finding ID: BRF-M3-CR1
- Severity: major
- Status: open
- Location: `scripts/workflow_automation.py:303-351`, `scripts/workflow_automation.py:391-421`, `scripts/workflow_automation.py:704-829`, `scripts/test-workflow-automation.py:204-286`, `scripts/test-workflow-automation.py:502-605`
- Evidence: Pre-plan resolution never evaluates `transition_identities`; an empty tuple and an arbitrary `sha256:unknown-transition` produce the same `proposal-review` position. Drift comparison checks only identities still present in the new result, so a previously observed `spec` identity may disappear while resolution silently regresses to `proposal-review`. The coordinator accepts caller-supplied `from_position` and `input_identities` without resolving canonical position or comparing input identities with capability basis. A direct reproduction used basis proposal `sha256:basis-proposal` and receipt input proposal `sha256:different-proposal`; the callback was invoked and the transition completed. This violates `BRF-R018`, `BRF-R019`, `BRF-R023`, `BRF-R037`, and T6.
- Required outcome: Every stage invocation must use one freshly resolved canonical position and current identity set, bind required receipt inputs to the capability basis and authoritative evidence, reject missing or changed previously observed identities, and incorporate the applicable closed transition evidence rather than accepting an unused tuple.
- Safe resolution path: Introduce a typed canonical-position evaluation input to `coordinate_one_stage`, resolve it immediately before capability/receipt persistence, compare the complete observed identity set and stage-required inputs with the capability basis, and reject additions, disappearance, or mismatch. Replace opaque `transition_identities` with validated transition evidence or remove it only if the governing contract is amended. Add direct missing-identity, mismatched-basis, stale-review, unknown-outcome, transition-evidence, and callback-not-invoked regressions.
- auto_fix_class: none
- needs-decision rationale: none

### BRF-M3-CR2: Persisted target completion predicates are not checked against stage policy

Finding ID: BRF-M3-CR2
- Severity: major
- Status: open
- Location: `scripts/workflow_automation.py:265-293`, `scripts/validate_workflow_automation.py:695-715`, `scripts/test-workflow-automation.py:137-203`
- Evidence: `bind_target` initially projects `StagePolicy.completion_rule`, but `resume_target` accepts any non-empty completion mapping and `_validate_target` checks only that the mapping is concrete. A direct reproduction replaced proposal-review completion with `{'rule': 'attacker-chosen'}`; `resume_target` returned it unchanged and `validate_workflow_automation` returned no errors. `persist_target` therefore can durably accept a completion predicate that no approved stage policy defines. This violates `BRF-R009`, `BRF-R017a`, and T4.
- Required outcome: Every new, resumed, parent, run, and receipt target must carry the exact completion predicate projected for its stage and occurrence; semantic drift must fail before persistence or execution.
- Safe resolution path: Centralize one `expected_target_completion(stage, occurrence)` projection, use it in binding, resume, and durable validation, and compare the complete predicate rather than only non-emptiness. Add one mutation contrast per public stage plus repeated-stage milestone/plan identity controls.
- auto_fix_class: none
- needs-decision rationale: none

### BRF-M3-CR3: Capability derivation ignores correction-budget scope and exhaustion

Finding ID: BRF-M3-CR3
- Severity: major
- Status: open
- Location: `scripts/workflow_automation.py:465-548`, `scripts/workflow_automation.py:581-677`, `scripts/test-workflow-automation.py:288-484`
- Evidence: Parent creation stores a correction budget, but `derive_effective_capability` accepts no requested or remaining budget, does not compare budget scope, and emits no budget constraint in the capability. A direct reproduction created proposal-correction authority with `max_cycles: 0` and `max_findings: 0`; an active proposal-correction capability was still derived. The M3 tests exercise only proposal-review and post-proposal-authoring derivation and contain no expanded/exhausted correction-budget contrast. This violates the correction-budget subset property in `BRF-R035` and T8's explicit expanded-budget case.
- Required outcome: Correction capabilities must bind a concrete current budget state no broader than the parent, and exhausted or expanded budgets must prevent active derivation.
- Safe resolution path: Add a typed correction-budget scope/current-state input to correction capability derivation, persist the bound constraint or identity required for deterministic evaluation, compare every limit with the parent, and reject zero/exhausted/expanded or identity-mismatched states. Add proposal- and implementation-correction positive, reduced-budget, expanded-budget, exhausted-budget, and changed-budget-identity tests.
- auto_fix_class: none
- needs-decision rationale: none

### BRF-M3-CR4: Arbitrary output is finalized as completed and canonically synchronized

Finding ID: BRF-M3-CR4
- Severity: major
- Status: open
- Location: `scripts/workflow_automation.py:818-850`, `scripts/test-workflow-automation.py:502-567`
- Evidence: After `invoke_stage` returns any non-empty list, the coordinator unconditionally finalizes the receipt as `completed`, sets `canonical_sync.status` to `synchronized`, and consumes the capability. It never inspects stage-owned completion evidence, checks `expected_postcondition`, or performs/validates canonical state synchronization. A direct reproduction returned `['not-a-review-record-or-identity']`; the result was `completed`, canonical sync became `synchronized`, and no error was raised. This contradicts `BRF-R015`, `BRF-R068`-`BRF-R069`, the architecture's stage-owned completion and synchronization boundary, and T14's recoverable-evidence intent.
- Required outcome: The coordinator must not claim completion or synchronization until typed stage-owned completion evidence satisfies the expected postcondition and canonical state has actually been synchronized and re-read.
- Safe resolution path: Replace the raw output list with a typed stage result that separates output evidence from canonical-sync evidence, validate both against the stage policy and expected postcondition, and finalize `completed` only after a successful canonical re-read. Otherwise retain/finalize the receipt as `paused` or `failed` according to policy without consuming authority. Add arbitrary-output, missing-postcondition, failed-sync, stale-plan, valid-sync, and capability-consumption ordering tests.
- auto_fix_class: none
- needs-decision rationale: none

## Requirement Fidelity

| Requirement properties | Result | Evidence |
| --- | --- | --- |
| `BRF-R009`-`BRF-R017f` closed structured targets and repeated binding | block | Repeated occurrence binding is directly covered, but `BRF-M3-CR2` shows completion predicates are mutable and accepted. |
| `BRF-R018`-`BRF-R023` canonical position and ownership handoff | block | Plan parsing and basic stale identity tests pass, but `BRF-M3-CR1` shows transition evidence is ignored and missing/mismatched identities can reach invocation. |
| `BRF-R024`-`BRF-R031` bounded non-executable parent authority | pass | Parent-only execution, risk-class separation, external prohibition, policy version, and verification-basis timing are enforced in the reviewed surface. |
| `BRF-R032`-`BRF-R046` exact capability basis and subset authority | block | Path/category/risk conflicts are checked, but `BRF-M3-CR1` and `BRF-M3-CR3` show identity and correction-budget scope are not bound. |
| `BRF-R068`-`BRF-R072` capability-bound prepared receipt | block | The receipt is prepared before callback invocation and one in-flight receipt is enforced, but `BRF-M3-CR4` fabricates completed/synchronized state from unverified output. |
| `BRF-R078`-`BRF-R080` stage ownership and non-public internal support | concern | Public routing remains unchanged, but `BRF-M3-CR4` lets the coordinator claim a stage-owned postcondition without stage-owned evidence. |

## Checklist Coverage

| Check | Result | Notes |
| --- | --- | --- |
| Spec alignment | block | Four direct reproductions violate structured-target, canonical-identity, capability-budget, and completion-synchronization requirements. |
| Test coverage | block | CMD10-CMD14 pass, but they do not encode the reproduced completion tamper, missing identity, transition-registry, exhausted-budget, or false-sync cases. |
| Edge cases | block | Unknown review outcome, disappeared observed identity, arbitrary transition identity, exhausted correction budget, and arbitrary output are accepted. |
| Error handling | block | The unsafe inputs produce success rather than a pause or fail-closed result. |
| Architecture boundaries | block | The sole writer is respected, but canonical resolver and coordinator are disconnected and completion/synchronization authority is collapsed into a raw callback result. |
| Compatibility | pass | Public workflow skills and legacy writers are unchanged; current legacy parsing remains non-public adapter input. |
| Security/privacy | concern | No secrets or external actions were introduced, but caller-controlled authority/evidence values can bypass intended authorization constraints. |
| Derived artifact currency | pass | No generated adapter or derived public skill output changed in M3. |
| Unrelated changes | pass | The diff is scoped to the M3 coordinator, tests, lifecycle integration, and handoff artifacts. |
| Validation evidence | concern | Recorded and rerun suites are credible for covered cases, but direct adversarial reproductions demonstrate material coverage insufficiency. |

## No-Finding Rationale

Not applicable. This review has four material findings.

## Residual Risks

The pure evidence inputs do not yet establish how later M4/M5 stage adapters will obtain authoritative identities. The findings do not require public routing or stage-native integration to move earlier; they require the M3 engine boundary to reject unverifiable or inconsistent inputs before those later adapters depend on it.

## Validation and Direct Proof

- The implementation-recorded CMD10-CMD14, state/validator regressions, lifecycle validation, compilation, and broad-smoke evidence were inspected after the blind-first pass.
- Direct target reproduction: an attacker-chosen completion predicate passed `resume_target` and full automation validation with zero errors.
- Direct canonical-state reproductions: an unknown proposal-review outcome resolved successfully; a previously observed `spec` identity disappeared without mismatch; empty and arbitrary transition identities produced the same position.
- Direct authority reproduction: mismatched proposal identities between capability basis and receipt input still invoked the callback.
- Direct budget reproduction: a zero-cycle, zero-finding correction parent derived an active proposal-correction capability.
- Direct completion reproduction: arbitrary non-identity output finalized the receipt as `completed` with `canonical_sync.status: synchronized`.

## Milestone Handoff

- Reviewed milestone: M3. Target Binding, Canonical Position, and Capability Evaluation
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `BRF-M3-CR1` through `BRF-M3-CR4`
- Remaining in-scope implementation milestones: M3 resolution needed, M4, M5, M6
- Next stage: review-resolution M3
- Final closeout readiness: not ready because M3 has four open findings and M4-M6, final holistic review, explanation, verification, and PR handoff remain.

## Recommended Next Stage

This direct review remains isolated: no automatic downstream handoff or implementation correction was performed. Enter `review-resolution` for `BRF-M3-CR1` through `BRF-M3-CR4`, apply targeted M3 fixes, rerun CMD10-CMD14 plus the direct contrasts, return M3 to `review-requested`, and rerun `code-review M3`. Do not start M4 while these findings remain open.
