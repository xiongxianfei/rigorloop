# Code Review M3 R3

Review ID: code-review-m3-r3
Stage: code-review
Round: M3 R3
Reviewer: Codex code-review skill
Target: M3 correction commit `0942c710`
Reviewed artifact: M3 correction commit `0942c710`
Reviewed milestone: M3. Target Binding, Canonical Position, and Capability Evaluation
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-22
Recording status: recorded
Material findings: BRF-M3-CR7
Immediate next stage: review-resolution

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, review log, review resolution, active plan, plan index, and change metadata
- Open blockers: `BRF-M3-CR7` blocks M3 closeout; no owner/spec/architecture decision is required for its approved safe resolution
- Next stage: review-resolution M3
- Review status: changes-requested
- Material findings: BRF-M3-CR7
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m3-r3.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m3-r3`
- Reviewed milestone: M3. Target Binding, Canonical Position, and Capability Evaluation
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3 resolution needed, M4, M5, M6
- Required review-resolution: yes
- Finding IDs: BRF-M3-CR7
- Verify readiness: not-claimed

## Review Inputs

- Diff surface: correction commit `0942c710` against its first parent.
- Tracked governing branch state: clean worktree at `0942c710` before review evidence recording.
- Governing spec: `BRF-R032`-`BRF-R046`, `BRF-R068`-`BRF-R079`, `EC10`, and the stage completion predicates in `specs/single-bounded-review-fix-workflow-automation.md`.
- Test spec: T8, T14, T15, CMD10-CMD14, and the fixture rule requiring stage-native evidence rather than path existence in `specs/single-bounded-review-fix-workflow-automation.test.md`.
- Architecture: stage-owned completion, canonical synchronization, lifecycle/review parser reuse, and sole-writer boundaries in `docs/architecture/system/architecture.md`.
- Active plan: M3 `review-requested` handoff in `docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md`.
- Prior finding dispositions: consulted only after the blind-first risk map, code inspection, and direct arbitrary-artifact reproduction.

## Independent Review Gate

Phase receipts:

1. `risk-map-recorded`: recorded before consulting prior-finding dispositions and implementation validation summaries.
2. `evidence-challenge-recorded`: passing focused suites were challenged with semantic-artifact and recovery counterexamples.
3. `prior-findings-reconciled`: recorded after the blind-first direct reproductions.
4. `requirement-fidelity-applicable`: the correction spans coordinator, durable validator, state recovery, and test surfaces governed by one stage-owned evidence contract.

## Risk Map

- Affected behavior: correction-budget identity, policy-derived completion, stage evidence inspection, canonical synchronization, durable receipt validation, recovery, cancellation, and capability consumption.
- Highest-impact failures: non-stage artifacts satisfying completion, callback echoes substituting for canonical synchronization, nonexistent recovery evidence consuming authority, and scope escape.
- Changed boundaries: stage callback to coordinator, coordinator to repository evidence, coordinator to sole writer, and durable receipt validation to recovery/cancellation.
- Expected evidence: stage-native parsers reject semantically invalid artifacts; canonical state is independently reread; recovery cannot reconcile nonexistent or malformed evidence; correction identities remain exact.
- Direct-inspection areas: `_validate_artifact_evidence`, `_validate_stage_result`, `_validate_sync_result`, `coordinate_one_stage`, `evaluate_receipt_recovery`, `cancel`, completed-receipt validation, and focused fixtures.
- Intentionally out of scope: M4-M6 stage integration, public routing, adapter cutover, final holistic review, verification, PR, and external actions.
- Applicable risk classes: workflow correctness, authorization integrity, durable-state integrity, recovery safety, proof sufficiency, and compatibility.
- Non-applicable risk classes: secrets, credentials, network access, external mutation, and generated adapters; none are changed by this slice.
- Falsifiable questions: Can arbitrary in-scope bytes complete a formal review? Can synchronization simply echo stage output? Can recovery reconcile a nonexistent artifact? Can unbound correction budget identity still derive?

## Diff Summary

The correction makes implementation-correction budget identity mandatory, derives receipt postconditions from immutable policy, introduces typed artifact references, hashes in-scope repository files before completion, and requires completed receipts to carry synchronization evidence and observed identities.

The budget correction is complete. The completion correction remains semantic only by label: the engine verifies file location and bytes but never invokes the stage-owned parser or checks the stage completion predicate. Recovery and cancellation also retain the older caller-supplied evidence path and can consume capability authority without any artifact existing.

## Prior-Finding Reconciliation

| Prior finding | R3 result | Evidence |
| --- | --- | --- |
| `BRF-M3-CR5` | resolved | Implementation-correction now includes `correction_budget_identity` in `CAPABILITY_BASIS_FIELDS`; derivation and durable validation compare it unconditionally, with missing and mismatch contrasts. |
| `BRF-M3-CR6` | failed-remediation | File hashing rejects absent and stale files, but arbitrary in-scope bytes still satisfy `proposal-review`; synchronization may echo the same mapping, and recovery accepts nonexistent evidence without invoking any stage-owned validator. |

## Findings

## Finding BRF-M3-CR7

Finding ID: BRF-M3-CR7
Severity: major
Location: `scripts/workflow_automation.py:826-904`, `scripts/workflow_automation.py:1063-1110`, `scripts/workflow_automation_state.py:183-258`, `scripts/workflow_automation_state.py:493-521`, `scripts/test-workflow-automation-state.py:200-214`
Evidence: `_validate_artifact_evidence` proves only repository-relative path, capability scope, file existence, and SHA-256 equality. `_validate_stage_result` then treats the presence of the policy evidence key as completion, while `_validate_sync_result` accepts a callback that returns the same evidence mapping; neither invokes a stage-native review/lifecycle parser nor rereads the canonical owner. A direct reproduction wrote `not-a-review.txt` containing arbitrary bytes with no formal review fields or outcome, labeled it `proposal-review`, echoed it from the sync callback, and received `completed/synchronized` with the capability `consumed`. A second reproduction passed a nonexistent artifact reference to `evaluate_receipt_recovery`; it returned `reconcile-completed`, and `cancel` persisted the receipt as completed and capability as consumed while the file remained absent. The existing recovery test at `scripts/test-workflow-automation-state.py:200-214` explicitly expects raw output plus status-only synchronization to reconcile. This violates `BRF-R073`, `BRF-R074`, `BRF-R078`, architecture runtime steps 12-13, and the test-spec rule that path existence is not completion evidence.
Required outcome: Completion and recovery must use stage-native semantic evidence and an independent canonical-owner reread before a receipt becomes completed or a capability becomes consumed. A typed path/hash reference may locate evidence, but it cannot itself establish the stage completion predicate.
Safe resolution path: Add one policy-owned evidence verifier/reader contract per stage that reuses the repository's existing review, lifecycle, plan, and verification parsers. Have the coordinator invoke that verifier after stage execution, synchronize through the canonical owner, then independently re-resolve canonical state and compare the policy completion predicate. Route prepared-receipt recovery and cancellation through the same verifier instead of accepting caller-supplied mappings. Add direct contrasts for arbitrary bytes, structurally invalid formal review, outcome/identity mismatch, no canonical write, stale canonical reread, nonexistent recovery artifact, and one valid parser-produced fixture.
needs-decision rationale: none; the approved spec, architecture, and test spec already select stage-owned semantic evidence and canonical parser reuse.
auto_fix_class: none

## Requirement Fidelity

| Requirement properties | Result | Evidence |
| --- | --- | --- |
| `BRF-R032`-`BRF-R046`: exact bounded capability basis | pass | Correction-budget basis identity is mandatory and exactly matches bounded scope. |
| `BRF-R068`-`BRF-R072`: prepared receipt ordering and binding | pass | Prepared receipt and effective capability binding remain intact. |
| `BRF-R073`-`BRF-R077`: evidence-first recovery | block | Nonexistent caller-supplied evidence is classified as valid completion and consumed during cancellation. |
| `BRF-R078`-`BRF-R079`: stage-owned authority and completion | block | The coordinator treats a path/hash plus policy label as completion without stage-native semantic validation. |
| M3 non-public boundary | pass | No public workflow skill, adapter, external action, or M4-M6 integration surface changed. |

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | Direct coordinator and recovery reproductions violate stage-owned completion and evidence-first reconciliation requirements. |
| Test coverage | block | Missing/stale path tests pass, but arbitrary semantic content, canonical no-write, and nonexistent recovery evidence are not rejected; one current recovery test preserves status-only behavior. |
| Edge cases | block | Arbitrary in-scope bytes and nonexistent recovery artifacts consume authority. |
| Error handling | block | Unsafe evidence returns successful completion/reconciliation rather than pause or fail closed. |
| Architecture boundaries | block | Stage-owner and canonical-owner authority remain replaced by callback labels and mappings. |
| Compatibility | concern | Completed-receipt shape is tightened, but recovery still accepts the retired weaker evidence shape, producing two inconsistent completion contracts. |
| Security/privacy | concern | No secret surface changed, but an internal authorization boundary can be bypassed with fabricated evidence. |
| Derived artifact currency | pass | No generated or public adapter artifacts are changed. |
| Unrelated changes | pass | The diff is limited to M3 corrections, tests, and lifecycle evidence. |
| Validation evidence | concern | Ten capability, 30 state, and 52 validator tests pass, but direct counterexamples demonstrate insufficient assertions. |

## Validation and Direct Proof

- `python scripts/test-workflow-automation.py -k capability`: 10 selected tests passed.
- `python scripts/test-workflow-automation-state.py`: 30 tests passed.
- `python scripts/test-validate-workflow-automation.py`: 52 tests passed.
- `git diff --check 0942c710^..0942c710`: passed.
- Direct semantic-artifact reproduction: arbitrary non-review bytes completed proposal review and consumed capability authority.
- Direct recovery reproduction: a nonexistent artifact returned `reconcile-completed`; cancellation persisted completed/consumed state while the artifact did not exist.
- Validation challenge conclusion: the suites prove path and identity checks but not stage-native completion or canonical synchronization.

## No-Finding Rationale

Not applicable. This review has one material failed-remediation finding.

## Residual Risks

The evidence verification contract must remain stage-relative: proposal review, plan state, implementation validation, milestone review, and verification do not share one interchangeable parser or completion predicate. M4-M6 routing and final holistic behavior remain unreviewed by this milestone-local rereview.

## Milestone Handoff

- Reviewed milestone: M3. Target Binding, Canonical Position, and Capability Evaluation
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `BRF-M3-CR7`, which records the failed remediation of `BRF-M3-CR6`
- Remaining in-scope implementation milestones: M3 resolution needed, M4, M5, M6
- Next stage: review-resolution M3
- Final closeout readiness: not ready because M3 has one open finding and M4-M6, final holistic review, explanation, verification, and PR handoff remain.

## Recommended Next Stage

This direct review remains isolated: no automatic downstream handoff or implementation correction was performed.
Enter `review-resolution` for `BRF-M3-CR7`, apply the targeted M3 correction, return M3 to `review-requested`, and rerun code-review M3.
Do not start M4 while the finding remains open.
