# Code Review M2 R1

Review ID: code-review-m2-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: M2 inner-loop helper runtime and formal cache-hit evidence
Status: changes-requested

## Result

- Skill: code-review
- Status: completed
- Review status: changes-requested
- Material findings: VIC-IH-CR-M2-001
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/reviews/code-review-m2-r1.md`
- Review log: `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-log.md`
- Review resolution: `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-resolution.md`
- Reviewed milestone: M2
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3, M4, M5, M6
- Required review-resolution: yes
- Finding IDs: VIC-IH-CR-M2-001
- Verify readiness: not-claimed
- Next stage: review-resolution for M2

## Review Inputs

- Reviewed commit: `0cf8130` (`M2: add inner-loop lifecycle helper mode`)
- Plan: `docs/plans/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md`
- Spec: `specs/validation-idempotency-and-cache-hit-safety.md`
- Test spec: `specs/validation-idempotency-and-cache-hit-safety.test.md`
- Implementation files: `scripts/validate-artifact-lifecycle.py`, `scripts/validation_cache.py`
- Test files: `scripts/test-artifact-lifecycle-validator.py`, `scripts/test-validation-cache.py`
- Validation evidence: M2 validation notes in the active plan and `change.yaml`

## Diff Summary

M2 makes `--mode explicit-paths-inner-loop` cache-aware by default in inner-loop context, keeps CI and direct `explicit-paths` out of automatic cache use, emits cache-miss fallback output for helper misses, and infers formal helper evidence paths only when a safe change root is available. It also extends formal cache-hit evidence rendering/loading with `command_family`, `evidence_kind`, `displayed_command_argv`, and `canonical_cache_argv`, while retaining the legacy `command.argv` shape for compatibility.

The test update adds helper cache-hit coverage without long flags, helper cache-miss fallback output, inferable formal evidence writes, ad hoc no-evidence behavior, and displayed/canonical argv evidence rendering.

## Findings

### VIC-IH-CR-M2-001

Finding ID: VIC-IH-CR-M2-001
Severity: major
Location: `scripts/test-artifact-lifecycle-validator.py:1932`

Evidence: `test_cli_helper_mode_ad_hoc_cache_hit_writes_no_formal_evidence` verifies ad hoc helper behavior by globbing every `docs/changes/*/validation-cache-evidence.yaml` file in the repository and asserting the list is empty. The approved spec requires formal helper cache hits to write or merge `docs/changes/<change-id>/validation-cache-evidence.yaml` when a safe workflow context exists (R145), and M2 itself implements that formal evidence writer. Once any legitimate tracked cache evidence file exists for this or another change, this ad hoc test fails even if the helper correctly writes no evidence for the ad hoc command under test.

Required outcome: The ad hoc no-evidence test must prove the helper does not create new formal evidence for the ad hoc invocation without assuming the whole repository has no formal cache-hit evidence files.

Safe resolution path: Snapshot the set of repository `validation-cache-evidence.yaml` files before the ad hoc helper invocation and assert the set is unchanged afterward, or assert only that the ad hoc command's inferred/specific evidence path is absent. Keep the cache hit output assertion so the test still proves ad hoc hits print status.

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | concern | Runtime helper behavior matches R134-R146 in code, but the ad hoc test conflicts with the formal evidence contract by assuming no formal cache evidence can exist anywhere. |
| Test coverage | block | The ad hoc no-evidence test is over-broad and will fail in a valid repository state containing formal cache-hit evidence. |
| Edge cases | pass | Helper miss fallback, helper cache hit, inferable change-root evidence, and ad hoc no-evidence behavior are all directly tested, subject to VIC-IH-CR-M2-001's assertion scope. |
| Error handling | pass | Cache identity errors and misses fall back to actual validation with distinct helper output; direct cache behavior remains stderr-based for disabled cache identity. |
| Architecture boundaries | pass | The implementation stays within the existing lifecycle validator and validation-cache modules; no wrapper script or new persistence boundary is introduced. |
| Compatibility | pass | Direct `explicit-paths` still requires explicit cache flags for cache use, and direct no-cache invocation remains actual-run validation. |
| Security/privacy | pass | Formal evidence writes remain repository-relative through `write_cache_hit_evidence`, and worktree identity is not rendered into tracked evidence. |
| Derived artifact currency | pass | No generated artifacts are touched. |
| Unrelated changes | pass | The diff is scoped to M2 runtime/evidence code, focused tests, and lifecycle handoff metadata. |
| Validation evidence | pass | The recorded commands passed, including `python scripts/test-validation-cache.py`, `python scripts/test-artifact-lifecycle-validator.py`, helper/direct lifecycle validation, review-artifact validation, change-metadata validation, and `git diff --check --`. |

## No-Finding Rationale

Not applicable; one material finding requires review-resolution before M2 can close.

## Residual Risks

Closeout rejection, selector routing, and measurement are intentionally deferred to M3-M5 and remain open implementation work rather than defects in M2.
