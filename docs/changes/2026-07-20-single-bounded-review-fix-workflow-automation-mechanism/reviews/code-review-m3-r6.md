# Code Review M3 R6

Review ID: code-review-m3-r6
Stage: code-review
Round: M3 R6
Reviewer: Codex code-review skill with independent blind-first reviewer
Target: M3 correction commit `516f6956`
Reviewed artifact: M3 correction commit `516f6956`
Reviewed milestone: M3. Target Binding, Canonical Position, and Capability Evaluation
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-22
Recording status: recorded
Material findings: BRF-M3-CR11, BRF-M3-CR12
Immediate next stage: review-resolution

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, review log, review resolution, active plan, plan index, and change metadata
- Open blockers: `BRF-M3-CR11` and `BRF-M3-CR12` block M3 closeout; neither requires a product, spec, architecture, or ownership decision
- Next stage: review-resolution M3
- Review status: changes-requested
- Material findings: `BRF-M3-CR11`, `BRF-M3-CR12`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m3-r6.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m3-r6`
- Reviewed milestone: M3. Target Binding, Canonical Position, and Capability Evaluation
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3 resolution needed, M4, M5, M6
- Required review-resolution: yes
- Finding IDs: `BRF-M3-CR11`, `BRF-M3-CR12`
- Verify readiness: not-claimed

## Review Inputs

- Diff surface: correction commit `516f6956` against its first parent.
- Tracked governing branch state: clean worktree at `516f6956` before review evidence recording.
- Governing spec: `BRF-R018`-`BRF-R023`, `BRF-R068`-`BRF-R078`, `BRF-R100`, and the canonical input/output and state invariants.
- Test spec: T6, T14-T16, CMD10-CMD14, and the deterministic temporary-repository proof contract.
- Architecture and ADR: exact `docs/changes/<change-id>/change.yaml#workflow.automation` persistence, sole state-writer ownership, repository-owned completion evidence, and active-plan handoff ownership.
- Active plan: M3 `review-requested` handoff for R6.
- Prior finding dispositions and implementation validation summaries were consulted only after the blind-first risk map, code inspection, and direct adversarial probes.

## Independent Review Gate

Phase receipts:

1. `risk-map-recorded`: recorded before consulting prior findings or implementation validation summaries.
2. `evidence-challenge-recorded`: passing focused tests were challenged with explicit ancestor-root, symlinked-metadata, and contradictory-detail probes.
3. `prior-findings-reconciled`: recorded after both blind-first reproductions.
4. `requirement-fidelity-applicable`: canonical persistence ownership, tracked identity, stage-native evidence, and active-plan state properties were checked across changed production and test surfaces.

## Risk Map

- Affected behavior: state-store construction, repository-root binding, coordinator/finalizer evidence selection, cancellation recovery, and active-plan closeout-reason synchronization.
- Highest-impact failures: constructor-time trust-root rebinding, canonical metadata symlink escape, cross-repository state/evidence consumption, and contradictory live handoff state.
- Changed boundaries: metadata path to canonical repository root, coordinator to state adapter, state adapter to evidence filesystem, and formal review summary to active-plan owner state.
- Expected evidence: one exact root derived from the canonical lexical metadata path, no symlinked canonical metadata components, matching change-directory identity, and deterministic agreement between structured finding state and the complete authoritative reason field.
- Direct-inspection areas: `WorkflowAutomationStateStore.__init__`, `require_repository_root`, `read`, `finalize_transition`, `cancel`, `coordinate_one_stage`, lifecycle state sync, and new negative fixtures.
- Intentionally out of scope: M4-M6 integration, public command cutover, final holistic review, verification, PR, publication, and external actions.
- Applicable risk classes: filesystem trust, cross-repository identity, durable-state integrity, recovery safety, workflow-state ownership, compatibility, and proof sufficiency.
- Non-applicable risk classes: network, credentials, deployment, database, UI, and generated adapters.
- Falsifiable questions: Can construction bind canonical-looking metadata to an ancestor or foreign root? Can a symlink erase the canonical layout before validation? Can the reason detail contradict the structured review summary while its code list remains valid?

## Diff Summary

The correction makes the state store expose one bound root, checks coordinator and finalizer roots against it, infers a root from a resolved canonical-looking path, validates the change-directory identity in that inferred layout, and adds cross-root post-construction tests. It also compares the `review-findings-open` reason code with formal review open-count state and adds two code-list contrast tests.

The post-construction root mismatch is now rejected. The constructor itself still accepts an arbitrary ancestor root and resolves away canonical metadata symlinks before layout validation, so the bound root is not necessarily the repository that lexically owns `docs/changes/<change-id>/change.yaml`. The lifecycle change validates only the code list before the em dash; contradictory bounded detail remains accepted.

## Prior-Finding Reconciliation

| Prior finding | R6 result | Evidence |
| --- | --- | --- |
| `BRF-M3-CR9` | failed-remediation | Post-construction mismatch is fixed, but constructor-time ancestor-root and symlink rebinding still defeat canonical repository ownership; the remaining defect is recorded as `BRF-M3-CR11`. |
| `BRF-M3-CR10` | failed-remediation | Code-list synchronization is fixed, but the authoritative bounded detail can still claim the opposite finding state; the remaining defect is recorded as `BRF-M3-CR12`. |

## Findings

## Finding BRF-M3-CR11

Finding ID: BRF-M3-CR11
Severity: blocker
Location: `scripts/workflow_automation_state.py:603-663`, affecting `scripts/workflow_automation.py:908-984`, finalization, recovery, and cancellation through the bound store root
Evidence: The constructor resolves `metadata_path` before recognizing canonical layout and accepts any explicit ancestor as `repository_root`. Its exact layout and change-directory checks run only when the already-resolved path relative to that selected root starts with `docs/changes`. A direct tracked-repository probe constructed the current canonical store with the repository's parent as root; construction and `read()` succeeded with the wrong bound root. A second temporary-repository probe symlinked `repo-a/docs/changes/example/change.yaml` to `repo-b/change.yaml`; the store resolved away Repo A, bound itself to Repo B, and read the foreign document. The new tests cover a foreign root supplied after normal construction, not adversarial construction itself. This violates the architecture's exact canonical persistence boundary, weakens tracked identity reliance under `BRF-R100`, and leaves the repository-owned completion boundary bypassable.
Required outcome: A canonical metadata path must remain bound to exactly its owning repository root and matching `<change-id>` directory; explicit ancestors, alternate roots, and symlinked metadata or canonical ancestors must fail before read, invocation, recovery, finalization, or mutation.
Safe resolution path: Preserve and validate the lexical metadata path before resolving it; reject symlinks in the metadata path and canonical ancestor chain; derive the exact root from `docs/changes/<change-id>/change.yaml`; require any explicit root to equal that derived root rather than merely contain the file; enforce directory/change-ID equality unconditionally for canonical lexical paths; and add ancestor/common-root, symlinked-file, symlinked-directory, mismatched-ID, and valid explicit-root regressions.
needs-decision rationale: none; the approved architecture already fixes the canonical persistence location and repository-owned state boundary.
auto_fix_class: none

## Finding BRF-M3-CR12

Finding ID: BRF-M3-CR12
Severity: major
Location: `scripts/lifecycle_state_sync.py:1702-1746` and `scripts/test-artifact-lifecycle-validator.py:1160-1191`
Evidence: State sync parses only the comma-separated reason codes before the em dash. With zero open findings and a valid code list that omits `review-findings-open`, the bounded detail `WSS-F1 remains open and later closeout gates remain` produced zero lifecycle blockers. The inverse contradiction is equally representable. The tests mutate only code presence and use semantically matching detail, so they do not prove that the complete authoritative reason agrees with formal review state. This is the exact stale live-state class that `BRF-M3-CR10` required the validator to prevent.
Required outcome: The complete authoritative closeout reason, including bounded detail, must agree deterministically with formal open-finding evidence in both the open and closed states.
Safe resolution path: Define a closed, machine-checkable review-state detail projection instead of broad natural-language inference—for example an exact generated review-finding clause containing the current open count or IDs, or a rule prohibiting review-state claims outside that clause. Validate the projection against formal review evidence and add direct open-evidence/closed-prose plus closed-evidence/open-prose regressions while leaving historical prose outside `Current Handoff Summary` untouched.
needs-decision rationale: none; the accepted prior finding already requires reason-code and open-finding prose synchronization. The correction should implement that bounded contract without reopening product or architecture direction.
auto_fix_class: none

## Requirement Fidelity

| Requirement property | Result | Evidence |
| --- | --- | --- |
| Exact canonical persistence and repository-owned evidence | block | Ancestor-root and symlinked-metadata construction bypass the intended owner. |
| `BRF-R073`-`BRF-R077`: recovery and completion fail closed on invalid evidence | block | Recovery/finalization inherit a constructor-selected root that may not canonically own the metadata. |
| `BRF-R078`: stage-owned evidence authority remains external to automation state | block | Foreign repository evidence may become authoritative through constructor rebinding. |
| `BRF-R100`: resume relies on tracked identities and receipts | block | The supposedly tracked repository root can be an arbitrary ancestor or symlink target. |
| `BRF-R020` and active-plan ownership | block | The authoritative reason detail may contradict formal review evidence. |
| M3 non-public boundary | pass | No public workflow skill, adapter, external action, or M4-M6 integration surface changed. |

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | Canonical ownership and complete handoff-state agreement remain bypassable. |
| Test coverage | block | Constructor adversaries and contradictory detail are absent. |
| Edge cases | block | Ancestor root, metadata symlink, and code-correct/prose-wrong cases succeed. |
| Error handling | block | Both direct probes return success instead of failing closed. |
| Architecture boundaries | block | The exact change-local persistence owner is not enforced at construction. |
| Compatibility | concern | The safe correction must preserve normal canonical construction and explicit valid-root fixture construction. |
| Security/privacy | block | Symlink and ancestor-root trust can cross repository boundaries. |
| Derived artifact currency | pass | No generated output or public adapter changed. |
| Unrelated changes | pass | The commit is limited to M3 correction code, tests, and lifecycle evidence. |
| Validation evidence | concern | Required suites pass, but direct probes expose missing negative coverage. |

## Validation and Direct Proof

- `python scripts/test-workflow-automation.py -k target`: 6 tests passed.
- `python scripts/test-workflow-automation.py -k position`: 4 tests passed.
- `python scripts/test-workflow-automation.py -k capability`: 15 tests passed.
- `python scripts/test-artifact-lifecycle-validator.py -k automation`: 2 tests passed.
- `python scripts/test-artifact-lifecycle-validator.py`: 151 tests passed.
- Focused new root and lifecycle tests passed, confirming the intended narrow cases.
- `git diff --check 516f6956^..516f6956`: passed.
- Direct ancestor-root probe: the current canonical metadata read successfully with the repository parent bound as its root.
- Direct metadata-symlink probe: canonical Repo A metadata resolved to and read Repo B's document.
- Direct contradictory-detail probe: zero open formal findings plus `WSS-F1 remains open` in the authoritative detail produced zero blockers.

## No-Finding Rationale

Not applicable. This review has two material findings.

## Residual Risks

M4 and M5 stage readers must inherit only the eventual exact store-bound repository root. The bounded reason-detail projection must avoid broad prose interpretation and remain limited to the live `Current Handoff Summary` field.

## Milestone Handoff

- Reviewed milestone: M3. Target Binding, Canonical Position, and Capability Evaluation
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `BRF-M3-CR11` and `BRF-M3-CR12`
- Remaining in-scope implementation milestones: M3 resolution needed, M4, M5, M6
- Next stage: review-resolution M3
- Final closeout readiness: not ready because M3 has two open R6 findings and M4-M6, final holistic review, explanation, verification, and PR handoff remain.

## Recommended Next Stage

This direct review remains isolated: no automatic downstream handoff or implementation correction was performed.
Enter `review-resolution` for `BRF-M3-CR11` and `BRF-M3-CR12`, return M3 to `review-requested` after correction, and rerun code-review M3.
Do not start M4 while either finding remains open.
