# Code Review M3 R5

Review ID: code-review-m3-r5
Stage: code-review
Round: M3 R5
Reviewer: Codex code-review skill with independent blind-first reviewer
Target: M3 correction commit `b4f64f32`
Reviewed artifact: M3 correction commit `b4f64f32`
Reviewed milestone: M3. Target Binding, Canonical Position, and Capability Evaluation
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-22
Recording status: recorded
Material findings: BRF-M3-CR9, BRF-M3-CR10
Immediate next stage: review-resolution

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, review log, review resolution, active plan, plan index, and change metadata
- Open blockers: `BRF-M3-CR9` and `BRF-M3-CR10` block M3 closeout; neither requires a product, spec, architecture, or ownership decision
- Next stage: review-resolution M3
- Review status: changes-requested
- Material findings: `BRF-M3-CR9`, `BRF-M3-CR10`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m3-r5.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m3-r5`
- Reviewed milestone: M3. Target Binding, Canonical Position, and Capability Evaluation
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3 resolution needed, M4, M5, M6
- Required review-resolution: yes
- Finding IDs: `BRF-M3-CR9`, `BRF-M3-CR10`
- Verify readiness: not-claimed

## Review Inputs

- Diff surface: correction commit `b4f64f32` against its first parent.
- Tracked governing branch state: clean worktree at `b4f64f32` before review evidence recording.
- Governing spec: `BRF-R073`-`BRF-R078`, `BRF-R100`, and the isolation and state-ownership contracts.
- Test spec: T14-T16, CMD10-CMD14, and the deterministic filesystem rule requiring symlink-escape rejection and fresh temporary roots.
- Architecture: the sole state-writer boundary, repository-owned change-local evidence, stage-owned completion evidence, and evidence-first recovery.
- Active plan: M3 `review-requested` handoff.
- Prior finding dispositions and implementation validation summaries were consulted only after the independent risk map, code inspection, and cross-repository reproduction.

## Independent Review Gate

Phase receipts:

1. `risk-map-recorded`: recorded before consulting prior-finding dispositions or implementation validation summaries.
2. `evidence-challenge-recorded`: passing suites were challenged with independent-root, additional symlink, and canonical-state consistency probes.
3. `prior-findings-reconciled`: recorded after the blind-first cross-repository reproduction.
4. `requirement-fidelity-applicable`: `BRF-R073`-`BRF-R078`, `BRF-R100`, and the test-spec filesystem contract were checked across completion, recovery, cancellation, and handoff state.

## Risk Map

- Affected behavior: repository file resolution, proposal-review completion proof, completed receipt recovery, cancellation reconciliation, canonical state persistence, and M3 handoff state.
- Highest-impact failures: evidence from the wrong repository consuming capability authority, caller-selected trust roots, stale canonical identities, recovery proof rebinding, and contradictory canonical workflow state.
- Changed boundaries: coordinator to state store, state store to repository filesystem, formal review parser to canonical review log, and review resolution to active-plan handoff.
- Expected evidence: one root bound to the canonical state store, no-symlink contained paths under that root, verifier-derived identities, drift rejection, and synchronized review/handoff surfaces.
- Direct-inspection areas: `coordinate_one_stage`, `_resolve_repository_file`, `verify_transition_completion`, `evaluate_receipt_recovery`, `finalize_transition`, `cancel`, state fixtures, and `Current Handoff Summary`.
- Intentionally out of scope: M4-M6 stage integration, public command cutover, final holistic review, verification, PR, publication, and external actions.
- Applicable risk classes: authorization integrity, filesystem trust, durable-state integrity, recovery safety, workflow state ownership, and proof sufficiency.
- Non-applicable risk classes: network, credentials, deployment, publication, and external mutation.
- Falsifiable questions: Can Store A consume evidence from Repository B? Can a caller select a root independently of the canonical metadata? Do all symlink forms pause? Does completed log drift pause? Do handoff and review-resolution surfaces agree?

## Diff Summary

The correction introduces a no-symlink repository-file resolver, extends stage-native verification to return normalized completion proof, persists review-record and review-log identities, compares completed proof against current canonical evidence, and makes cancellation persist verified proof instead of caller mappings. It adds direct external and in-repository log-symlink, occurrence, drift, valid recovery, fabricated identity, and cancellation regressions.

The intended symlink and identity-drift corrections work. The filesystem trust root remains caller-selectable and independent of the state store, so equivalent evidence in an unrelated repository can still complete Store A's receipt. The implementation handoff also left the active plan's authoritative reason inconsistent with the closed review-resolution state.

## Prior-Finding Reconciliation

| Prior finding | R5 result | Evidence |
| --- | --- | --- |
| `BRF-M3-CR8` | failed-remediation | Its exact symlink and canonical-log drift cases are resolved, but its repository-owned-evidence requirement remains bypassable through an unbound caller-selected `repository_root`; the remaining defect is recorded as `BRF-M3-CR9`. |

## Findings

## Finding BRF-M3-CR9

Finding ID: BRF-M3-CR9
Severity: major
Location: `scripts/workflow_automation.py:908-965`, `scripts/workflow_automation.py:1094-1114`, `scripts/workflow_automation_state.py:603-605`, `scripts/workflow_automation_state.py:727-773`, `scripts/test-workflow-automation-state.py:483-748`
Evidence: `coordinate_one_stage` accepts `store` and `repository_root` independently and forwards the caller root to `finalize_transition`. The state writer verifies completed evidence against `(repository_root or self.repository_root)` without proving that the selected root owns the store's `change.yaml`. A direct reproduction created Store A, copied its parser-valid proposal/review/log evidence into unrelated temporary Repository B, removed Store A's `docs/`, and finalized Store A with `repository_root=B`; the result persisted the receipt as `completed` and the effective capability as `consumed`. The 40 state/recovery tests cover path-level symlinks and drift inside one fixture root but contain no mismatched store/root case. This violates `BRF-R078`, `BRF-R100`, the repository-owned evidence boundary, and the architecture's sole-writer/canonical-evidence contract.
Required outcome: Completion, prepared/completed recovery, and cancellation must evaluate evidence only against the repository canonically owning the persisted `change.yaml`, and a mismatched or unbound root must fail before invocation, finalization, or authority consumption.
Safe resolution path: Bind one canonical repository root to `WorkflowAutomationStateStore`; validate that the metadata path belongs to the expected `docs/changes/<change-id>/change.yaml` location under that root; remove the per-finalization trust-root override or require exact equality before any write or invocation; use the bound root for completion, recovery, and cancellation; and add a two-repository negative regression covering direct finalization and coordinator preflight.
needs-decision rationale: none; the approved spec and architecture already require repository-owned tracked evidence and one state-writer boundary.
auto_fix_class: none

## Finding BRF-M3-CR10

Finding ID: BRF-M3-CR10
Severity: major
Location: `docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md:102-112`, `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md:5-31`, `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md:359-369`, `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/change.yaml:925-937`
Evidence: The active plan's authoritative `Current Handoff Summary` says `review-findings-open` and states that M3 has one failed-remediation R4 finding, while the same tracked commit records `Closeout status: closed`, zero unresolved findings, `Open findings: None`, and `review.status: resolved`. The plan is the post-plan canonical workflow-position owner, so this is a state-sync contradiction even though structural lifecycle validation passes.
Required outcome: The active plan's handoff reason must agree with review resolution, review log, and change metadata at every state-changing handoff, then reflect the R5 findings after this review is recorded.
Safe resolution path: Synchronize the M3 handoff summary and plan index from the actual R5 review state, add or strengthen a regression that compares reason tokens/open-finding prose with structured review state, and rerun the artifact lifecycle state-sync gate before M3 rereview.
needs-decision rationale: none; canonical state ownership and handoff synchronization are already settled.
auto_fix_class: none

## Requirement Fidelity

| Requirement property | Result | Evidence |
| --- | --- | --- |
| `BRF-R073`-`BRF-R075`: prepared recovery uses stage-owned evidence | block | The verifier can use stage-shaped evidence from a repository unrelated to the canonical state store. |
| `BRF-R076`: completed canonical/output drift pauses | pass | Direct log-byte drift now pauses and unchanged verifier-derived proof continues. |
| `BRF-R077`: partial or invalid completion fails closed | block | A mismatched repository root is not treated as invalid completion evidence. |
| `BRF-R078`: stage-owned review authority is preserved | block | Caller-selected Repository B can supply the occurrence that consumes Store A's capability. |
| `BRF-R100`: resume relies on tracked identities and receipts | block | Identity checks are scoped to a caller root not bound to the tracked state record. |
| Active-plan workflow-state ownership | block | The authoritative handoff reason contradicts the tracked review state. |
| M3 non-public boundary | pass | No public workflow skill, adapter, external action, or M4-M6 integration surface changed. |

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | Wrong-repository evidence can satisfy completion and consume authority. |
| Test coverage | block | No cross-repository store/root mismatch regression exists. |
| Edge cases | block | Path-level symlinks are covered, but the independent-root boundary is not. |
| Error handling | block | A mismatched root completes instead of pausing or failing closed. |
| Architecture boundaries | block | The state writer is not bound to the repository containing its canonical metadata. |
| Compatibility | pass | Public commands, aliases, schema, and migration writers are unchanged. |
| Security/privacy | block | The filesystem trust root remains caller-selectable. |
| Derived artifact currency | pass | No generated or public adapter outputs changed. |
| Unrelated changes | pass | The diff is limited to M3 completion proof, tests, and lifecycle evidence. |
| Validation evidence | concern | Focused and broad suites pass, but direct cross-root proof and handoff comparison reveal missing coverage. |

## Validation and Direct Proof

- `python scripts/test-workflow-automation.py -k capability`: 14 selected tests passed.
- `python scripts/test-workflow-automation-state.py`: 40 tests passed.
- `python scripts/test-validate-workflow-automation.py`: 52 tests passed.
- `git diff --check b4f64f32^..b4f64f32`: passed.
- Independent reviewer also reran CMD10 with 6 tests, CMD11 with 4 tests, CMD13 with 2 tests, and full CMD14 successfully.
- Direct cross-repository reproduction: Store A finalized `completed` and consumed its capability using evidence located only in unrelated Repository B after Store A's evidence tree was removed.
- Direct additional symlink probes: review-record and reviewed-target symlinks paused, confirming that the remaining gap is root binding rather than the fixed path-component check.
- Validation challenge conclusion: current tests prove containment relative to a supplied root, but do not prove that the supplied root is the canonical repository for the state being mutated.

## No-Finding Rationale

Not applicable. This review has two material findings.

## Residual Risks

M4 and M5 must reuse the eventual store-bound canonical evidence root for their stage-relative readers. Unsupported later-stage verifiers remain fail closed and were not reviewed as implemented behavior in M3.

## Milestone Handoff

- Reviewed milestone: M3. Target Binding, Canonical Position, and Capability Evaluation
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `BRF-M3-CR9` and `BRF-M3-CR10`; `BRF-M3-CR9` records failed remediation of the repository-owned portion of `BRF-M3-CR8`
- Remaining in-scope implementation milestones: M3 resolution needed, M4, M5, M6
- Next stage: review-resolution M3
- Final closeout readiness: not ready because M3 has two open findings and M4-M6, final holistic review, explanation, verification, and PR handoff remain.

## Recommended Next Stage

This direct review remains isolated: no automatic downstream handoff or implementation correction was performed.
Enter `review-resolution` for `BRF-M3-CR9` and `BRF-M3-CR10`, return M3 to `review-requested`, and rerun code-review M3.
Do not start M4 while either finding remains open.
