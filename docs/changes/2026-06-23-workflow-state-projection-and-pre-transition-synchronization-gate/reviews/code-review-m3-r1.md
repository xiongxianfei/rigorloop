# Code Review M3 R1 - Review Evidence and Change Metadata Consistency

Review ID: code-review-m3-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: commit `8946e67c`
Status: changes-requested

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/reviews/code-review-m3-r1.md, docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/review-log.md, docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/review-resolution.md, docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md, docs/plan.md, docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/change.yaml
- Open blockers: WSS-CR2
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: WSS-CR2
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/reviews/code-review-m3-r1.md
- Review log: docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/review-log.md
- Review resolution: docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/review-resolution.md#code-review-m3-r1
- Reviewed milestone: M3. Review Evidence and Change Metadata Consistency
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3, M4, M5
- Required review-resolution: yes
- Finding IDs: WSS-CR2
- Verify readiness: not-claimed

## Review inputs

- Diff/review surface: commit `8946e67c` (`M3: enforce review evidence state consistency`).
- Tracked governing branch state: committed M3 implementation and governing artifacts at `8946e67c`.
- Governing artifacts:
  - `specs/single-source-of-workflow-state.md`
  - `specs/single-source-of-workflow-state.test.md`
  - `docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md`
- Validation evidence reviewed:
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md --path docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/change.yaml --path docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/review-log.md --path docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/review-resolution.md`

## Diff summary

M3 adds `ReviewEvidenceSummary` derivation from review records, `review-log.md`, and `review-resolution.md`; uses the summary to check `change.yaml` review counts; rejects `review.next_stage` and `review.next-stage`; and blocks workflow owner states that claim `review-requested` while the derived summary still has open findings. It also adds tests for open-finding owner-state blocking, change metadata count drift, and next-stage-like review metadata.

## Findings

### WSS-CR2: Closed summary counts can hide findings that fail required closeout evidence

Finding ID: WSS-CR2
Severity: major
Location: `scripts/review_artifact_validation.py:241`
Evidence: `summarize_review_evidence()` subtracts every `review-resolution.md` entry from `open_ids` whenever the file has `Closeout status: closed`, using only structure-mode parsing. It does not require the closeout checks that R65 names: final disposition-specific closeout requirements, required validation evidence, and no later reopening. A direct fixture with `review-log.md` listing `Open findings: WSS-F1`, `review-resolution.md` set to `Closeout status: closed` but missing `Validation evidence`, and `change.yaml` claiming `unresolved_items: 0`, `closed_findings: 1`, `open_findings: 0` passed `python scripts/validate-change-metadata.py <fixture>/change.yaml`. The same fixture failed `python scripts/validate-review-artifacts.py --mode closeout <fixture>` with `accepted finding missing validation evidence` and stale open-finding closeout errors.
Required outcome: Derived review summaries and owner-state blocking must treat a material finding as open until the review-resolution entry satisfies the same closeout requirements used by review-artifact closeout validation, including required validation evidence and no later reopening.
Safe resolution path: Derive open and closed finding IDs through shared review-artifact closeout semantics rather than only `Closeout status: closed`. Add regression tests where a closed-status resolution entry without required validation evidence still keeps the finding open for `change.yaml` counts and lifecycle owner-state checks; add the positive paired fixture only after closeout validation succeeds.
needs-decision rationale: none

## Checklist coverage

| Check | Verdict | Evidence |
| --- | --- | --- |
| Spec alignment | block | WSS-CR2 violates R65 and T17 by closing a finding for derived metadata without required validation evidence. |
| Test coverage | block | Added tests cover open log counts and a happy closed-resolution count, but not the required negative fixture for closed status with missing closeout evidence. |
| Edge cases | block | The named T17 case for resolved findings requiring final dispositions, validation evidence, and no reopening is not enforced by the new summary helper. |
| Error handling | concern | The helper ignores parse/closeout findings from review-artifact validation while producing authoritative counts. |
| Architecture boundaries | pass | The implementation reuses the review artifact parser and keeps checks composed through existing validators. |
| Compatibility | pass | The change remains repository-local and does not migrate historical plans. |
| Security/privacy | pass | The diff reads local Markdown/YAML only and does not expose secrets or alter auth-sensitive behavior. |
| Derived artifact currency | block | `change.yaml` derived closed/open counts can agree with the helper while contradicting review-resolution closeout requirements. |
| Unrelated changes | pass | The implementation diff is scoped to M3 code, tests, and lifecycle/review artifacts. |
| Validation evidence | concern | Recorded validation is real, but it does not include the missing closeout-evidence negative case. |

## No-finding rationale

Not applicable. WSS-CR2 requires changes before M3 can close.

## Residual risks

The same summary path feeds lifecycle owner-state blocking in `scripts/lifecycle_state_sync.py`, so WSS-CR2 can also allow `review-requested` owner state while review-resolution closeout evidence is incomplete.

## Milestone handoff

Reviewed milestone: M3. Review Evidence and Change Metadata Consistency
Review status: changes-requested
Milestone closeout: resolution-needed
Required review-resolution: yes
Next stage: review-resolution
Remaining implementation milestones: M3, M4, M5
Verify readiness: not-claimed
