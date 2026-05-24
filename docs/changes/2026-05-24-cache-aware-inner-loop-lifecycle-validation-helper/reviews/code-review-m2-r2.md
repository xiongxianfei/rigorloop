# Code Review M2 R2

Review ID: code-review-m2-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review
Target: M2 inner-loop helper runtime and formal cache-hit evidence
Status: clean-with-notes

## Result

- Skill: code-review
- Status: completed
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/reviews/code-review-m2-r2.md`
- Review log: `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-log.md`
- Review resolution: `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-resolution.md`
- Reviewed milestone: M2
- Milestone closeout: closed
- Remaining implementation milestones: M3, M4, M5, M6
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed
- Next stage: implement M3

## Review Inputs

- Reviewed implementation commits: `0cf8130` (`M2: add inner-loop lifecycle helper mode`), `9211b37` (`review-resolution: fix M2 helper evidence test`)
- Prior review: `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/reviews/code-review-m2-r1.md`
- Review-resolution entry: `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-resolution.md#code-review-m2-r1`
- Plan: `docs/plans/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md`
- Spec: `specs/validation-idempotency-and-cache-hit-safety.md`
- Test spec: `specs/validation-idempotency-and-cache-hit-safety.test.md`
- Implementation files: `scripts/validate-artifact-lifecycle.py`, `scripts/validation_cache.py`
- Test files: `scripts/test-artifact-lifecycle-validator.py`, `scripts/test-validation-cache.py`
- Validation evidence: M2 and review-resolution validation notes in the active plan and `change.yaml`

## Diff Summary

M2 makes the inner-loop helper cache-aware by default, while preserving direct `explicit-paths` actual-run behavior unless the existing cache flags are explicitly supplied. Helper misses and disabled cache identity now print distinct miss/fallback output and run actual lifecycle validation. Helper cache hits infer a change-local evidence path only when a safe change root is available, and formal evidence records both displayed helper argv and canonical direct cache argv.

The review-resolution fix narrowed the ad hoc no-evidence test so it asserts no new formal evidence files are created by the ad hoc helper run, without assuming the repository contains no legitimate formal cache-hit evidence files.

## Findings

No blocking or required-change findings.

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | Helper default cache use covers R134; miss/disabled fallback covers R139-R143; formal evidence path inference and no ad hoc write cover R145-R149. Direct `explicit-paths` remains actual-run unless opt-in cache flags are supplied, preserving R136-R137. |
| Test coverage | pass | `scripts/test-artifact-lifecycle-validator.py` covers no-long-flags helper cache hit, miss fallback output, safe formal evidence write, and ad hoc no-new-evidence behavior. `scripts/test-validation-cache.py` covers displayed/canonical argv evidence shape. |
| Edge cases | pass | The accepted R1 finding is fixed: ad hoc no-evidence coverage now tolerates existing legitimate evidence files and checks for no new evidence writes. |
| Error handling | pass | Cache identity errors and local cache misses fall back to actual validation; helper output names the fallback, while direct cache-disabled behavior remains unchanged. |
| Architecture boundaries | pass | The implementation stays inside the existing lifecycle validator and validation-cache modules with no wrapper script or broader validator cache eligibility. |
| Compatibility | pass | Existing formal evidence loading remains backward-compatible by filling displayed/canonical argv from legacy `command.argv` when needed. |
| Security/privacy | pass | Formal evidence path safety remains enforced through `write_cache_hit_evidence`; tracked evidence continues to omit worktree absolute path identity. |
| Derived artifact currency | pass | No generated artifacts are touched. |
| Unrelated changes | pass | The reviewed diff is scoped to M2 runtime/evidence behavior, focused tests, and lifecycle handoff artifacts. |
| Validation evidence | pass | `python scripts/test-validation-cache.py` and `python scripts/test-artifact-lifecycle-validator.py` passed after the review-resolution fix; artifact/metadata validation and `git diff --check --` are recorded in the plan and change metadata. |

## No-Finding Rationale

The M2 implementation now satisfies the helper runtime and formal evidence slice without expanding cache eligibility, changing direct closeout validation, or relying on a repository-empty evidence state. Remaining closeout rejection, selector routing, measurement, and final closeout work are explicitly assigned to later milestones.

## Residual Risks

M2 does not implement closeout rejection, selector routing, or measurement. Those remain planned work for M3-M5 and are not closed by this review.
