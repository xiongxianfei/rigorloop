# Code Review M3 R4

Review ID: code-review-m3-r4
Stage: code-review
Round: M3 R4
Reviewer: Codex code-review skill
Target: M3 correction commit `32a819e6`
Reviewed artifact: M3 correction commit `32a819e6`
Reviewed milestone: M3. Target Binding, Canonical Position, and Capability Evaluation
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-22
Recording status: recorded
Material findings: BRF-M3-CR8
Immediate next stage: review-resolution

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, review log, review resolution, active plan, plan index, and change metadata
- Open blockers: `BRF-M3-CR8` blocks M3 closeout; no product, spec, architecture, or ownership decision is required
- Next stage: review-resolution M3
- Review status: changes-requested
- Material findings: BRF-M3-CR8
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m3-r4.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m3-r4`
- Reviewed milestone: M3. Target Binding, Canonical Position, and Capability Evaluation
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3 resolution needed, M4, M5, M6
- Required review-resolution: yes
- Finding IDs: BRF-M3-CR8
- Verify readiness: not-claimed

## Review Inputs

- Diff surface: correction commit `32a819e6` against its first parent.
- Tracked governing branch state: clean worktree at `32a819e6` before review evidence recording.
- Governing spec: `BRF-R068`-`BRF-R079`, especially completed-receipt canonical identity drift in `BRF-R076` and stage-owned authority in `BRF-R078`.
- Test spec: T14, T15, T16, CMD10-CMD14, and the deterministic fixture rule requiring symlink escape rejection.
- Architecture: stage-owned completion evidence, canonical-state synchronization, evidence-first recovery, and the sole state-writer boundary.
- Active plan: M3 `review-requested` handoff.
- Prior finding dispositions and implementation validation summaries were consulted only after the blind-first risk map, code inspection, and direct filesystem-boundary reproductions.

## Independent Review Gate

Phase receipts:

1. `risk-map-recorded`: recorded before consulting prior-finding dispositions or implementation validation summaries.
2. `evidence-challenge-recorded`: passing focused suites were challenged with symlink-escape and canonical-identity-drift counterexamples.
3. `prior-findings-reconciled`: recorded after both blind-first reproductions.
4. `requirement-fidelity-applicable`: `BRF-R076`, `BRF-R078`, and the test-spec filesystem contract were checked property-by-property across completion, recovery, cancellation, and fixtures.

## Risk Map

- Affected behavior: formal-review parsing, proposal identity binding, canonical review-log synchronization, state-writer completion, prepared/completed recovery, cancellation, and capability consumption.
- Highest-impact failures: external filesystem evidence satisfying canonical state, canonical evidence changing without identity drift detection, weaker recovery proof, and capability consumption after partial proof.
- Changed boundaries: review parser to state reconciler, repository path resolver to canonical review log, coordinator to sole writer, and prepared/completed receipt recovery.
- Expected evidence: exact parser-valid review and target binding, repository-contained canonical-owner evidence, persisted canonical-owner identity, identical verifier use across completion paths, and fail-closed unsupported stages.
- Direct-inspection areas: `_resolve_completion_artifact`, `verify_transition_completion`, `evaluate_receipt_recovery`, `finalize_transition`, `cancel`, formal review parsers, and regression fixtures.
- Intentionally out of scope: M4-M6 routing, public commands and adapters, final holistic review, verification, PR, and external actions.
- Applicable risk classes: workflow correctness, authorization integrity, filesystem trust boundaries, durable-state integrity, recovery safety, and proof sufficiency.
- Non-applicable risk classes: network, credentials, publication, deployment, and external mutation.
- Falsifiable questions: Can an out-of-repository canonical review log satisfy completion? Can canonical log identity change without a completed-receipt pause? Can recovery or cancellation bypass the semantic verifier? Can an unsupported stage consume authority?

## Diff Summary

The correction exposes repository-owned formal review parsers, validates proposal-review structure and closed outcome, binds the reviewed target to the receipt proposal identity, requires a matching review-log occurrence, enforces semantic verification before the sole writer completes a receipt, and reuses verification for prepared/completed recovery and cancellation. It also adds direct invalid-content, identity, outcome, missing-log, nonexistent-recovery, and valid-parser fixtures.

The parser and target-binding work is effective. The canonical review-log path and identity remain weaker than the review artifact: the log is followed without repository containment, and its identity is neither persisted nor compared during completed recovery.

## Prior-Finding Reconciliation

| Prior finding | R4 result | Evidence |
| --- | --- | --- |
| `BRF-M3-CR7` | failed-remediation | Stage-native parsing and canonical occurrence matching were added, but an external symlink target can still act as the canonical review log and review-log identity drift is not bound to the receipt. |

## Findings

## Finding BRF-M3-CR8

Finding ID: BRF-M3-CR8
Severity: major
Location: `scripts/workflow_automation_state.py:327-343`, `scripts/workflow_automation_state.py:372-396`, `scripts/workflow_automation_state.py:654-681`, `scripts/workflow_automation_state.py:709-734`, `scripts/test-workflow-automation-state.py:94-166`
Evidence: `verify_transition_completion` checks `review_log.is_file()` and parses the path without resolving it against `repository_root` or rejecting a symlink escape. A direct reproduction replaced the in-repository log with a symlink to a parser-valid file outside the temporary repository; `evaluate_receipt_recovery` returned `reconcile-completed`, and `cancel` persisted the receipt as `completed`, the capability as `consumed`, and the run as `cancelled`. A second reproduction completed a valid receipt, changed the canonical review-log bytes, and resumed with the persisted outputs and sync evidence; recovery returned `continue/completed-evidence-current` because `canonical_sync.observed_identities` contains only the review-record identity. This violates `BRF-R076`, `BRF-R078`, architecture runtime steps 12-13, and the test-spec deterministic filesystem rule to reject symlink escape.
Required outcome: Canonical review-log evidence must resolve to its declared repository-owned location, remain inside the repository and change root, and have its independently observed identity persisted and compared during normal completion, prepared recovery, completed recovery, and cancellation before capability consumption.
Safe resolution path: Introduce one canonical-evidence resolver that rejects absolute paths, traversal, and symlink escape for both stage artifacts and canonical-owner records. Extend the verified completion result to carry engine-derived canonical identities, including the review-log identity; have the sole writer persist only that normalized verified proof. Make recovery and cancellation consume the verified normalized proof instead of copying caller mappings. Add direct fixtures for external and in-repository symlink substitution, review-log byte drift after completion, wrong canonical-log occurrence, missing log, and the valid parser-produced path.
needs-decision rationale: none; the approved spec, architecture, and test spec already require repository-owned canonical evidence, identity-drift detection, and symlink-escape rejection.
auto_fix_class: none

## Requirement Fidelity

| Requirement property | Result | Evidence |
| --- | --- | --- |
| `BRF-R073`-`BRF-R075`: evidence-first prepared recovery | block | Prepared recovery accepts a canonical review log whose resolved path is outside the repository. |
| `BRF-R076`: completed canonical/output identity drift pauses | block | Review-log bytes can change while completed recovery returns `continue`. |
| `BRF-R077`: partial or invalid completion fails closed | block | External canonical-owner evidence is treated as valid completion. |
| `BRF-R078`: stage-owned review authority is preserved | block | A non-repository log can supply the canonical occurrence used to consume authority. |
| M3 non-public boundary | pass | No public workflow skill, adapter, external action, or M4-M6 integration surface changed. |

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | Canonical identity drift and external canonical evidence violate `BRF-R076` and `BRF-R078`. |
| Test coverage | block | Named review and recovery contrasts pass, but the test-spec symlink-escape rule and canonical-log identity drift are not exercised. |
| Edge cases | block | External symlink substitution and semantic-preserving canonical byte drift are accepted. |
| Error handling | block | Unsafe canonical evidence completes or continues instead of pausing. |
| Architecture boundaries | block | The canonical-owner read is not repository-contained or identity-bound. |
| Compatibility | pass | Public commands, aliases, state schema, and migration writers are unchanged. |
| Security/privacy | block | Filesystem trust expands outside the repository through a followed symlink. |
| Derived artifact currency | pass | No generated or public adapter outputs are changed. |
| Unrelated changes | pass | The implementation diff remains limited to M3 completion proof, tests, and lifecycle evidence. |
| Validation evidence | concern | Focused suites pass, but direct counterexamples show the filesystem and canonical-identity assertions are incomplete. |

## Validation and Direct Proof

- `python scripts/test-workflow-automation.py -k capability`: 14 selected tests passed.
- `python scripts/test-workflow-automation-state.py`: 33 tests passed.
- `python scripts/test-validate-workflow-automation.py`: 52 tests passed.
- `git diff --check 32a819e6^..32a819e6`: passed.
- Direct symlink reproduction: an external canonical review log produced `reconcile-completed`; cancellation persisted `completed/consumed/cancelled`.
- Direct canonical-identity reproduction: changed review-log bytes produced `continue/completed-evidence-current`; the persisted observed identities contained no review-log identity.
- Validation challenge conclusion: the suites prove formal review parsing and occurrence matching but not repository containment or canonical-owner identity stability.

## No-Finding Rationale

Not applicable. This review has one material failed-remediation finding.

## Residual Risks

M4 and M5 must add stage-relative canonical evidence readers without weakening the containment and identity contract established for proposal review. Unsupported later-stage verifiers correctly remain fail closed and are not reviewed as implemented behavior in this milestone.

## Milestone Handoff

- Reviewed milestone: M3. Target Binding, Canonical Position, and Capability Evaluation
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `BRF-M3-CR8`, which records failed remediation of `BRF-M3-CR7`
- Remaining in-scope implementation milestones: M3 resolution needed, M4, M5, M6
- Next stage: review-resolution M3
- Final closeout readiness: not ready because M3 has one open finding and M4-M6, final holistic review, explanation, verification, and PR handoff remain.

## Recommended Next Stage

This direct review remains isolated: no automatic downstream handoff or implementation correction was performed.
Enter `review-resolution` for `BRF-M3-CR8`, apply the targeted M3 correction, return M3 to `review-requested`, and rerun code-review M3.
Do not start M4 while the finding remains open.
