# Code Review M3 R7

Review ID: code-review-m3-r7
Stage: code-review
Round: M3 R7
Reviewer: Codex code-review skill in isolated direct-review mode
Target: M3 correction commit `31eba592`
Reviewed artifact: M3 correction commit `31eba592`
Reviewed milestone: M3. Target Binding, Canonical Position, and Capability Evaluation
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-22
Recording status: recorded
Material findings: BRF-M3-CR13, BRF-M3-CR14
Immediate next stage: review-resolution

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, review log, review resolution, active plan, plan index, and change metadata
- Open blockers: `BRF-M3-CR13` and `BRF-M3-CR14` block M3 closeout; neither requires a product, spec, architecture, or ownership decision
- Next stage: review-resolution M3
- Review status: changes-requested
- Material findings: `BRF-M3-CR13`, `BRF-M3-CR14`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m3-r7.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m3-r7`
- Reviewed milestone: M3. Target Binding, Canonical Position, and Capability Evaluation
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3 resolution needed, M4, M5, M6
- Required review-resolution: yes
- Finding IDs: `BRF-M3-CR13`, `BRF-M3-CR14`
- Verify readiness: not-claimed

## Review Inputs

- Diff surface: correction commit `31eba592` against its first parent.
- Tracked governing branch state: clean worktree at `31eba592` before review evidence recording.
- Governing spec: `BRF-R018`-`BRF-R023`, `BRF-R068`-`BRF-R078`, `BRF-R100`, and canonical state/input/output invariants.
- Test spec: T6, T14-T16, CMD10-CMD14, and deterministic temporary-repository proof requirements.
- Architecture and ADR: exact change-local persistence ownership, sole state-writer ownership, repository-owned completion evidence, and active-plan handoff ownership.
- Active plan: M3 `review-requested` handoff for R7.
- Prior finding dispositions: `BRF-M3-CR11` and `BRF-M3-CR12` in `review-resolution.md`.

## Review Mode and Risk Map

This was an isolated direct review. It does not claim the workflow-managed automated-review manifest or automatic downstream handoff.

- Affected behavior: canonical state-store construction, filesystem ownership binding, live closeout-detail parsing, and lifecycle state synchronization.
- Highest-impact failures: a lexical path escaping through an unchecked ancestor symlink, and a valid review-state prefix being contradicted by a second structured state claim.
- Changed boundaries: absolute metadata path to repository root, state adapter to filesystem, and formal review evidence to the live plan handoff.
- Expected evidence: rejection of every symlink in the lexical canonical ancestor chain and one unambiguous review-state projection with no second state vocabulary in the remainder.
- Direct-inspection areas: `WorkflowAutomationStateStore.__init__`, `require_repository_root`, finalization root use, `_review_state_detail_errors`, and the added regressions.
- Intentionally out of scope: M4-M6, public command routing, final holistic review, verification, PR, publication, and external actions.
- Applicable risk classes: filesystem trust, cross-repository identity, durable-state integrity, workflow-state ownership, compatibility, and proof sufficiency.
- Non-applicable risk classes: network, credentials, deployment, database, UI, and generated adapters.
- Falsifiable questions: Can a symlink before the derived root still redirect canonical metadata? Can the detail remainder restate `review-state` or another open-state vocabulary without rejection?

## Diff Summary

The correction preserves the lexical metadata path long enough to derive the canonical root, rejects a non-exact explicit root, rejects symlinks at the derived root and below it, removes the finalizer root override, and retains change-directory identity checking. It also introduces an exact review-state prefix and compares its state, count, and IDs with formal review evidence while screening the remaining detail for the word `finding` and finding-shaped IDs.

The intended focused cases pass, but both corrected boundaries remain bypassable. Path checking starts at the derived root, so a symlink in an earlier absolute-path ancestor is followed during `resolve()`. The detail remainder screening is vocabulary-based and does not reject a second `review-state` or equivalent open-state field, so the authoritative detail can still contradict the validated prefix.

## Prior-Finding Reconciliation

| Prior finding | R7 result | Evidence |
| --- | --- | --- |
| `BRF-M3-CR11` | failed-remediation | File, change-directory, and derived-root symlinks are rejected, but an earlier lexical ancestor symlink is accepted and becomes the resolved canonical root; the remaining defect is `BRF-M3-CR13`. |
| `BRF-M3-CR12` | failed-remediation | Count, ID, and selected prose contrasts are rejected, but a second structured `review-state` or unrecognized open-state claim in the remainder is accepted; the remaining defect is `BRF-M3-CR14`. |

## Findings

## Finding BRF-M3-CR13

Finding ID: BRF-M3-CR13
Severity: blocker
Location: `scripts/workflow_automation_state.py:603-651`, especially the symlink walk at lines 618-630; coverage gap in `scripts/test-workflow-automation-state.py:218-325`
Evidence: The constructor checks `lexical_root.is_symlink()` and then components below `lexical_root`, but it never checks absolute lexical ancestors above the derived root. A direct temporary-repository probe created `<temp>/linked-parent -> <temp>/real-parent` and opened `<temp>/linked-parent/repo/docs/changes/example/change.yaml`. Construction succeeded and bound `repository_root` to `<temp>/real-parent/repo`. This still resolves away lexical ownership evidence even though the R6 required outcome explicitly includes symlinked canonical ancestors.
Required outcome: Canonical metadata construction must reject a symlink anywhere in the lexical canonical path chain whose resolution can change the owning repository identity, before reading or binding the store root.
Safe resolution path: Validate the absolute lexical path component-by-component from its anchor through `change.yaml` without following symlinks, or establish an equivalent descriptor-based no-follow boundary. Add a regression with a symlink above the derived repository-root segment while preserving a normal absolute canonical path.
needs-decision rationale: none; the accepted R6 finding already requires rejection of symlinked canonical ancestors.
auto_fix_class: none

## Finding BRF-M3-CR14

Finding ID: BRF-M3-CR14
Severity: major
Location: `scripts/lifecycle_state_sync.py:68-77` and `scripts/lifecycle_state_sync.py:327-377`; coverage gap in `scripts/test-artifact-lifecycle-validator.py:1193-1232`
Evidence: `contains_independent_claim()` recognizes only `finding(s)` and finding-shaped uppercase IDs. With one formal open finding, the fully valid prefix followed by `review-state=closed; nothing remains open` produced zero lifecycle blockers. With zero formal findings, the unstructured detail `review-state=open; open-count=1; open-items=WSS item; later gates remain` also produced zero blockers. Both probes exercised the full artifact lifecycle validator, not only the helper.
Required outcome: The bounded detail must have exactly one authoritative review-state projection and must not permit the remainder to restate or contradict review state through structured state keys or alternate review-state vocabulary.
Safe resolution path: Reserve the review-state namespace rather than trying to infer arbitrary prose. Reject `review-state`, `open-count`, `open-findings`, and any other approved structured review-state keys outside the single leading projection; keep the remainder explicitly non-authoritative. Add direct second-projection and zero-open/unstructured-state regressions.
needs-decision rationale: none; this is the same deterministic complete-reason agreement required by the accepted R6 finding.
auto_fix_class: none

## Requirement Fidelity

| Requirement property | Result | Evidence |
| --- | --- | --- |
| Exact canonical persistence and repository-owned evidence | block | An ancestor symlink outside the derived-root segment still changes the resolved owner. |
| `BRF-R073`-`BRF-R077`: recovery and completion fail closed on invalid evidence | block | All later operations inherit the incorrectly rebound root. |
| `BRF-R078`: stage-owned evidence authority remains external to automation state | block | Filesystem authority can still cross the intended lexical repository boundary. |
| `BRF-R100`: resume relies on tracked identities and receipts | block | The bound root can originate from a symlinked ancestor not represented in the canonical identity. |
| `BRF-R020` and active-plan ownership | block | The authoritative detail can contain a second contradictory review-state assertion. |
| M3 non-public boundary | pass | No public skill, adapter, M4-M6 integration, or external-action surface changed. |

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | Canonical ownership and complete live-state agreement remain bypassable. |
| Test coverage | block | Earlier-ancestor symlink and second-state-claim contrasts are absent. |
| Edge cases | block | Both direct adversarial cases complete without blockers. |
| Error handling | block | Invalid trust and contradictory state are accepted instead of failing closed. |
| Architecture boundaries | block | The exact change-local persistence owner can still be rebound before store construction completes. |
| Compatibility | concern | The next correction must preserve normal absolute canonical paths and non-review-related bounded detail. |
| Security/privacy | block | Filesystem path traversal through an ancestor symlink can cross repository identity. |
| Derived artifact currency | pass | No generated output or public adapter changed. |
| Unrelated changes | pass | Commit `31eba592` is limited to the two R6 corrections, their tests, and lifecycle evidence. |
| Validation evidence | concern | Focused suites pass, but the two direct negative probes expose missing proof. |

## Validation and Direct Proof

- `python scripts/test-workflow-automation-state.py`: 47 tests passed.
- `python scripts/test-artifact-lifecycle-validator.py`: 153 tests passed.
- `python scripts/test-workflow-automation.py -k target`: 6 tests passed.
- `python scripts/test-workflow-automation.py -k position`: 4 tests passed.
- `python scripts/test-workflow-automation.py -k capability`: 15 tests passed.
- `git diff --check 31eba592^..31eba592`: passed.
- Direct ancestor-symlink probe: construction accepted a canonical-looking path below a symlinked parent and rebound the store to the resolved real repository.
- Direct full-validator open-state probe: a valid `review-state=open` prefix followed by `review-state=closed` produced zero blockers.
- Direct full-validator closed-state probe: zero open formal findings plus an unstructured `review-state=open; open-count=1` detail produced zero blockers.

## No-Finding Rationale

Not applicable. This review has two material findings.

## Residual Risks

The next filesystem correction should define whether protection is lexical component rejection or descriptor-based no-follow validation and test the exact chosen boundary. The closeout-detail correction should reserve structured state keys and avoid broad natural-language interpretation.

## Milestone Handoff

- Reviewed milestone: M3. Target Binding, Canonical Position, and Capability Evaluation
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `BRF-M3-CR13` and `BRF-M3-CR14`
- Remaining in-scope implementation milestones: M3 resolution needed, M4, M5, M6
- Next stage: review-resolution M3
- Final closeout readiness: not ready because M3 has two open R7 findings and M4-M6, final holistic review, explanation, verification, and PR handoff remain.

## Recommended Next Stage

This direct review remains isolated: no automatic downstream handoff or implementation correction was performed.
Enter `review-resolution` for `BRF-M3-CR13` and `BRF-M3-CR14`, return M3 to `review-requested` after correction, and rerun code-review M3.
Do not start M4 while either finding remains open.
