# Code Review M3 R2

Review ID: code-review-m3-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review skill
Target: M3 rereview after CR-RFA-M3-1 fix
Status: changes-requested

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/reviews/code-review-m3-r2.md; docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/review-log.md; docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/review-resolution.md; docs/plans/2026-06-30-bounded-review-fix-autoprogression-in-chat.md; docs/plan.md; docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/change.yaml
- Open blockers: none
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: CR-RFA-M3-2
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/reviews/code-review-m3-r2.md
- Review log: docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/review-log.md
- Review resolution: docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/review-resolution.md#code-review-m3-r2
- Reviewed milestone: M3. Auto-Safe Classification, Review-Resolution, and Rereview Evidence
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3, M4, M5
- Required review-resolution: yes
- Finding IDs: CR-RFA-M3-2
- Verify readiness: not-claimed

## Review inputs

- Diff/review surface: commit `75e0d15d` resolving CR-RFA-M3-1, especially `scripts/review_artifact_validation.py`, `scripts/test-review-artifact-validator.py`, current review-resolution state, active plan handoff, plan index, and change metadata.
- Tracked governing branch state: `specs/review-fix-autoprogression.md`, `specs/review-fix-autoprogression.test.md`, `docs/plans/2026-06-30-bounded-review-fix-autoprogression-in-chat.md`, and `docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/change.yaml` are present in tracked branch state.
- Governing artifacts inspected: `specs/review-fix-autoprogression.md` requirements `R23`-`R38`, `R41`-`R43`; `specs/review-fix-autoprogression.test.md` `T6`, `T7`, `T8`, and `T9`; active plan M3 section; CR-RFA-M3-1 disposition.
- Validation evidence reviewed/rerun: `python scripts/test-review-artifact-validator.py -k review_fix` passed; `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-25-independent-test-spec-review-gate` failed with review-fix marker errors on a non-review-fix resolution entry.

## Diff summary

The CR-RFA-M3-1 fix adds tests for missing and unsupported `Review-fix auto-resolution` marker values and changes review-resolution validation to invoke review-fix auto-resolution checks when any field in `REVIEW_FIX_AUTO_RESOLUTION_FIELDS` is present. The targeted `review_fix` test selector passes.

## Findings

### CR-RFA-M3-2 - Review-fix trigger treats generic resolution fields as review-fix-specific

Finding ID: CR-RFA-M3-2
Severity: major
Location: `scripts/review_artifact_validation.py:108`
Evidence: `REVIEW_FIX_AUTO_RESOLUTION_FIELDS` includes generic material-resolution fields such as `Files changed`, `Target artifact`, and `Stop reason`. `_validate_resolution_entry_structure` invokes review-fix validation when any of those fields are present. Running `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-25-independent-test-spec-review-gate` now fails on `docs/changes/2026-06-25-independent-test-spec-review-gate/review-resolution.md:38` because that historical non-review-fix disposition contains `Files changed:` at line 50, producing missing `Review-fix auto-resolution`, missing `Driver classification`, and missing `Review-fix auto-applied` errors.
Required outcome: Review-fix validation must fail closed for review-fix-specific fields without treating generic material-resolution fields as review-fix markers.
Safe resolution path: Narrow the trigger set used by `_validate_resolution_entry_structure` to unambiguous review-fix marker fields, or otherwise distinguish optional review-fix block fields from generic resolution fields before invoking `_validate_review_fix_auto_resolution_entry`. Add a regression test with a non-review-fix accepted disposition that includes `Files changed:` and must remain valid, while preserving the missing-marker and unsupported-marker review-fix tests added for CR-RFA-M3-1. Rerun the targeted review-fix tests and validation for the historical affected change root.
needs-decision rationale: none

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | `R42` requires fail-closed validator behavior for review-fix fields, but the implementation broadens the trigger to generic resolution fields and rejects valid non-review-fix dispositions. |
| Test coverage | block | The new tests cover missing and unsupported review-fix markers, but no compatibility regression covers a normal material finding disposition with `Files changed:`. |
| Edge cases | block | Historical non-review-fix resolution entries are a concrete edge case for validator compatibility and now fail structure validation. |
| Error handling | concern | The validator emits deterministic errors, but they are attached to the wrong artifact class. |
| Architecture boundaries | pass | The change remains scoped to review artifact validation and tests. |
| Compatibility | block | `docs/changes/2026-06-25-independent-test-spec-review-gate/review-resolution.md` is an existing non-review-fix artifact that now fails structure validation solely because it has `Files changed:`. |
| Security/privacy | pass | The diff adds no secret handling, credential output, network behavior, or unsafe logging. |
| Derived artifact currency | pass | No generated adapter or public package output is touched by this fix. |
| Unrelated changes | pass | The reviewed diff is scoped to M3 validation behavior, focused tests, and lifecycle handoff updates. |
| Validation evidence | block | Targeted `review_fix` tests pass, but validation of an existing affected review-resolution root fails. |

## No-finding rationale

Not applicable. The review found one material implementation defect.

## Direct-proof gaps

- Direct proof is missing for preserving existing non-review-fix material disposition entries that use generic fields also listed in the review-fix template.

## Milestone handoff state

- Reviewed milestone: M3. Auto-Safe Classification, Review-Resolution, and Rereview Evidence
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes
- Remaining in-scope implementation milestones: M3, M4, M5
- Next stage: review-resolution for CR-RFA-M3-2, then implementation fix and rerun code-review for M3
- Final closeout readiness: not ready
- Verify readiness: not-claimed
