# Code Review M3 R2

Review ID: code-review-m3-r2
Stage: code-review
Round: M3 R2
Reviewer: Codex code-review skill
Target: M3 correction commit `a2b5f224`
Reviewed artifact: M3 correction commit `a2b5f224`
Reviewed milestone: M3. Target Binding, Canonical Position, and Capability Evaluation
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-22
Recording status: recorded
Material findings: BRF-M3-CR5, BRF-M3-CR6
Immediate next stage: review-resolution

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, review log, review resolution, active plan, plan index, and change metadata
- Open blockers: none; both findings are actionable within the approved M3 scope
- Next stage: review-resolution M3
- Review status: changes-requested
- Material findings: BRF-M3-CR5, BRF-M3-CR6
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m3-r2.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m3-r2`
- Reviewed milestone: M3. Target Binding, Canonical Position, and Capability Evaluation
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3 resolution needed, M4, M5, M6
- Required review-resolution: yes
- Finding IDs: BRF-M3-CR5, BRF-M3-CR6
- Verify readiness: not-claimed

## Review Inputs

- Diff surface: correction range `1f36c0aa..a2b5f224`.
- Tracked governing branch state: clean worktree at `a2b5f224` before review evidence recording.
- Governing spec: `specs/single-bounded-review-fix-workflow-automation.md`, especially `BRF-R009`-`BRF-R046`, `BRF-R068`-`BRF-R080`.
- Test spec: T4-T9 and T14 in `specs/single-bounded-review-fix-workflow-automation.test.md`.
- Architecture: the accepted capability evaluator, stage-owned completion, canonical synchronization, immutable policy, and sole-writer boundaries in `docs/architecture/system/architecture.md`.
- Active plan: M3 `review-requested` handoff in `docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md`.
- Prior finding dispositions: consulted only after the blind-first risk map and direct code inspection.

## Automated Independent Review Gate

Invocation manifest:

- Review target: commit `a2b5f224`, M3 correction slice.
- Initial packet: target identity, actual correction diff, governing spec/test-spec/architecture/plan, and formal review criteria.
- Excluded from the blind-first decision basis: author correctness claims, desired outcome, correction eligibility, prior reviewer conclusions, and validation summaries.

Phase receipts:

1. `risk-map-recorded`: recorded before consulting prior-finding dispositions or implementation validation summaries.
2. `evidence-challenge-recorded`: focused and full suites were challenged with direct counterexamples rather than treated as sufficient because they passed.
3. `prior-findings-reconciled`: recorded after direct reproductions.
4. `requirement-fidelity-applicable`: the correction implements a multi-surface normative contract across engine, validator, state writer, and tests.

## Risk Map

- Affected behavior: immutable target completion, canonical evidence binding, correction-budget authority, stage-owned completion, canonical synchronization, and durable receipt finalization.
- Highest-impact failures: attacker-selected stopping semantics, stale evidence reaching mutation, exhausted or stale correction authority, capability consumption without stage completion, and a receipt claiming synchronization that never occurred.
- Changed boundaries: policy registry to target binder/validator, canonical resolver to coordinator, capability basis to receipt inputs, stage callback to coordinator, coordinator to sole state writer, and durable receipt validation.
- Expected evidence: every public target mutation rejected, complete basis mismatch prevents callback invocation, proposal and implementation correction budgets bind current identity, fake stage output cannot complete, canonical state is written and reread, and completed receipts require concrete sync evidence.
- Direct-inspection areas: `target_completion_predicate`, `_bind_canonical_evidence`, correction derivation and durable validation, `_validate_stage_result`, `_validate_sync_result`, `coordinate_one_stage`, receipt finalization, and focused fixtures.
- Intentionally out of scope: M4-M6 stage integration, public workflow routing, legacy adapter activation, final holistic review, verification, PR, and external actions.
- Applicable risk classes: workflow correctness, authorization integrity, durable-state integrity, recovery safety, compatibility, and proof sufficiency.
- Non-applicable risk classes: secrets, network access, credentials, generated adapters, and external-system mutation; none are changed by this slice.
- Falsifiable questions: Can an unbound budget identity derive and validate? Can typed callbacks complete without a stage artifact? Can synchronized status validate without sync evidence? Can target or canonical identity tampering reach invocation?

## Diff Summary

The correction centralizes public-target completion predicates, rejects unknown review and transition vocabularies, treats disappeared observed identities as drift, binds the complete capability basis and canonical identity set into receipt inputs, and adds positive correction-budget scope.

It also replaces raw stage outputs with typed stage and synchronization results and persists synchronization evidence in completed receipts. Tests expand completion tampering, canonical mismatch, correction budgets, and failure ordering.

Target completion and canonical input binding are materially improved. Two authority/evidence gaps remain: implementation-correction budget identity is not a required basis property, and callback-returned values still substitute for actual stage-owned completion and canonical reread.

## Prior-Finding Reconciliation

| Prior finding | R2 result | Evidence |
| --- | --- | --- |
| `BRF-M3-CR1` | resolved | `coordinate_one_stage` derives canonical position, copies every basis field into receipt inputs, rejects disappeared observed identities, and direct canonical/supporting-basis mismatch tests prove the callback is not invoked. |
| `BRF-M3-CR2` | resolved | One policy helper supplies binding, resume, and durable target validation; every public target's altered completion predicate is rejected. |
| `BRF-M3-CR3` | failed-remediation | Positive and subset budget checks exist, but implementation-correction basis omits `correction_budget_identity`; an arbitrary unbound identity still derives and validates. |
| `BRF-M3-CR4` | failed-remediation | Typed result shapes exist, but callbacks can still assert completion and synchronization without writing or rereading stage-owned evidence, and durable validation accepts a completed receipt with only sync status. |

## Findings

### BRF-M3-CR5: Implementation-correction budget identity is not bound to its basis

Finding ID: BRF-M3-CR5
- Severity: major
- Status: open
- Location: `scripts/validate_workflow_automation.py:213-220`, `scripts/workflow_automation.py:724-729`, `scripts/validate_workflow_automation.py:909-935`
- Evidence: `CAPABILITY_BASIS_FIELDS[implementation-correction]` omits `correction_budget_identity`. Both derivation and durable validation compare the scope identity only when the optional basis field happens to exist. A direct reproduction omitted the field, supplied `sha256:unbound-budget`, derived an active capability, and received zero durable validation errors. This leaves no authoritative identity proving that the positive budget is the current reviewer-owned budget.
- Required outcome: Every proposal- and implementation-correction capability must require one concrete correction-budget identity in its stage-appropriate basis, and derivation plus durable validation must require exact equality with the bounded scope identity.
- Safe resolution path: Add `correction_budget_identity` to the implementation-correction basis contract, make the comparison unconditional for both correction kinds, and add missing, changed, arbitrary, and matching identity contrasts through derivation and durable validation.
- auto_fix_class: none
- needs-decision rationale: none

### BRF-M3-CR6: Typed callback claims still substitute for stage completion and canonical reread

Finding ID: BRF-M3-CR6
- Severity: major
- Status: open
- Location: `scripts/workflow_automation.py:813-837`, `scripts/workflow_automation.py:978-1015`, `scripts/validate_workflow_automation.py:1205-1245`, `scripts/test-validate-workflow-automation.py:1143-1151`
- Evidence: The coordinator checks only that callback-returned mappings are non-empty and mutually equal. It does not inspect the stage-owned artifact, derive the expected postcondition from policy/canonical state, or reread canonical state after the synchronization callback. A direct reproduction returned fabricated review and synchronization records, created no file other than `change.yaml`, yet finalized the receipt as `completed/synchronized` and consumed the capability. The durable validator's explicit completed-receipt test also passes with `canonical_sync: {status: synchronized}` and no evidence or observed identities. This violates the stage-authority and synchronization requirements in `BRF-R015`, `BRF-R078`, and the architecture runtime steps 11-13.
- Required outcome: Completion must be established from stage-owned evidence against a policy-derived postcondition, followed by synchronization through the canonical owner and an independent reread whose identities and postcondition are persisted and durably validated before capability consumption.
- Safe resolution path: Separate stage invocation from evidence inspection; resolve the owning stage's declared completion evidence from the repository after invocation; run synchronization through the state boundary; reread canonical position/state in the coordinator; compare the reread with the expected transition postcondition; and require completed receipts to contain concrete sync evidence and observed identities. Add fake typed-result, no-artifact, no-sync-write, stale-reread, incomplete completed-receipt, and valid real-fixture contrasts.
- auto_fix_class: none
- needs-decision rationale: none

## Requirement Fidelity

| Requirement properties | Result | Evidence |
| --- | --- | --- |
| `BRF-R009`-`BRF-R017f`: closed targets, occurrence, and completion | pass | Binding, resume, and durable validation use the same immutable completion projection; all public target tampering tests pass. |
| `BRF-R018`-`BRF-R023`: canonical position and mismatch handling | pass | Unknown review/transition values, missing previous identities, canonical/basis mismatches, and callback-not-invoked paths are covered directly. |
| `BRF-R032`-`BRF-R046`: exact current bounded capability basis | block | `BRF-M3-CR5` shows implementation-correction budget identity is optional and therefore cannot prove current budget authority. |
| `BRF-R068`-`BRF-R072`: prepared receipt and completion evidence | block | Preparation ordering is intact, but `BRF-M3-CR6` shows fabricated completion/sync can finalize and consume authority. |
| `BRF-R078`-`BRF-R080`: stage ownership and coordination boundary | block | The coordinator still accepts callback claims in place of inspecting stage-owned evidence and independently rereading canonical state. |
| M3 non-public boundary | pass | No canonical skill, public dispatcher, generated adapter, external action, or M4-M6 integration surface changed. |

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | Two direct reproductions violate current correction authority and stage-owned completion/synchronization boundaries. |
| Test coverage | block | Existing suites pass, but they encode the incomplete contracts: implementation budget identity is always volunteered, fake callbacks count as valid success, and completed sync evidence is optional. |
| Edge cases | block | Missing implementation budget identity, arbitrary scope identity, no stage artifact, no sync write, and evidence-free completed receipts succeed. |
| Error handling | block | Unsafe authority and evidence claims produce successful derivation or completion instead of pause/fail-closed behavior. |
| Architecture boundaries | block | Sole-writer ownership remains intact, but stage-owner and canonical-reread authority are still delegated to unverified callback claims. |
| Compatibility | pass | Public commands, legacy adapters, schema version, and migration behavior are unchanged. |
| Security/privacy | concern | No secret or network surface changed, but authority can be fabricated at an internal trust boundary. |
| Derived artifact currency | pass | No generated or public adapter artifacts are in this correction slice. |
| Unrelated changes | pass | The diff is limited to M3 corrections, tests, and lifecycle evidence. |
| Validation evidence | concern | Ten capability-selected, 18 full engine, and 50 validator tests pass, but direct counterexamples prove the covered assertions are insufficient. |

## Validation and Direct Proof

- `python scripts/test-workflow-automation.py -k target`: 5 tests passed.
- `python scripts/test-workflow-automation.py -k position`: 4 tests passed.
- `python scripts/test-workflow-automation.py -k capability`: 10 tests passed.
- `python scripts/test-workflow-automation.py`: 18 tests passed.
- `python scripts/test-validate-workflow-automation.py`: 50 tests passed.
- `git diff --check 1f36c0aa..a2b5f224` passed.
- Direct budget reproduction: implementation correction omitted the basis budget identity, used an arbitrary scope identity, derived active authority, and produced no durable validation error.
- Direct completion reproduction: fabricated typed review/sync results created no stage-owned file but finalized `completed/synchronized` and consumed authority.
- Direct durable-state proof: the existing completed-receipt fixture passes with synchronized status but without sync evidence or observed identities.
- Validation challenge conclusion: passing suites establish target and canonical-input improvements but do not prove current budget identity or actual stage/canonical completion.

## No-Finding Rationale

Not applicable. This review has two material findings.

## Residual Risks

Canonical evidence is resolved before automation-state writes, not re-resolved immediately before stage invocation; later stage integration must ensure its authoritative artifact reads and synchronization boundary remain race-aware.
M4-M6 routing, public command activation, legacy adapters, final holistic review, verification, and external-action containment remain unreviewed by this milestone-local rereview.

## Milestone Handoff

- Reviewed milestone: M3. Target Binding, Canonical Position, and Capability Evaluation
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `BRF-M3-CR5` and `BRF-M3-CR6`
- Remaining in-scope implementation milestones: M3 resolution needed, M4, M5, M6
- Next stage: review-resolution M3
- Final closeout readiness: not ready because M3 has two open findings and M4-M6, final holistic review, explanation, verification, and PR handoff remain.

## Recommended Next Stage

This direct review remains isolated: no automatic downstream handoff or implementation correction was performed.
Enter `review-resolution` for `BRF-M3-CR5` and `BRF-M3-CR6`, apply targeted M3 fixes, rerun CMD10-CMD14 plus the direct contrasts, return M3 to `review-requested`, and rerun code-review M3.
Do not start M4 while these findings remain open.

