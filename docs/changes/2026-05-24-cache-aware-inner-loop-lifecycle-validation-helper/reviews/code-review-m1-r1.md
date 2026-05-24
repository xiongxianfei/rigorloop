# Code Review M1 R1

Review ID: code-review-m1-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: M1 helper mode and canonical identity tests
Status: clean-with-notes

## Result

- Skill: code-review
- Status: completed
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/reviews/code-review-m1-r1.md`
- Review log: `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-log.md`
- Review resolution: `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-resolution.md`
- Reviewed milestone: M1
- Milestone closeout: closed
- Remaining implementation milestones: M2, M3, M4, M5, M6
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed
- Next stage: implement M2

## Review Inputs

- Reviewed commit: `e94ac7d` (`M1: add helper cache identity normalization`)
- Plan: `docs/plans/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md`
- Spec: `specs/validation-idempotency-and-cache-hit-safety.md`
- Test spec: `specs/validation-idempotency-and-cache-hit-safety.test.md`
- Architecture: `docs/architecture/system/architecture.md`
- ADR: `docs/adr/ADR-20260523-validation-idempotency-cache-hit-safety.md`
- Implementation files: `scripts/validation_cache.py`, `scripts/validate-artifact-lifecycle.py`
- Test files: `scripts/test-validation-cache.py`, `scripts/test-artifact-lifecycle-validator.py`
- Validation evidence: M1 validation notes in the active plan and `change.yaml`

## Diff Summary

M1 adds `explicit-paths-inner-loop` as a lifecycle validator mode, maps that mode to direct `explicit-paths` for underlying validation execution, and extends validation-cache identity so helper invocations use canonical direct `explicit-paths` argv for cache keys while preserving displayed helper argv on the identity object.

The test update covers helper command-family eligibility, canonical direct argv normalization, displayed helper argv preservation, path-order-sensitive cache identity, direct actual-run cache identity reuse, helper CLI acceptance, and helper path requirements.

## Findings

No blocking or required-change findings.

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | `evaluate_command_family` now accepts only direct `explicit-paths` and helper `explicit-paths-inner-loop` for the existing explicit-path lifecycle command family, matching R1-R3 and AC48-AC49. |
| Test coverage | pass | `scripts/test-validation-cache.py` adds direct proof for helper canonical identity, displayed argv, path-order invalidation, and direct-run identity reuse; `scripts/test-artifact-lifecycle-validator.py` adds helper CLI acceptance and missing-path behavior. |
| Edge cases | pass | Path order remains identity-significant, unsupported validators remain excluded, and helper mode with no `--path` fails through the same explicit-path requirement. |
| Error handling | pass | Unsupported modes still return ineligible command-family results; helper execution delegates to the existing explicit-path validation path rather than adding a new unchecked validator path. |
| Architecture boundaries | pass | The change stays inside the existing validator and validation-cache modules; no wrapper script or new persistence boundary is introduced. |
| Compatibility | pass | Direct `--mode explicit-paths` behavior and cache-hit tests continue to pass; direct closeout actual-run semantics are not changed in M1. |
| Security/privacy | pass | Existing path normalization and unsafe path rejection remain unchanged; no new tracked evidence writer or local-machine data surface is added in M1. |
| Derived artifact currency | pass | No generated artifacts are touched. |
| Unrelated changes | pass | Code changes are scoped to lifecycle validator mode handling, cache identity primitives, and their tests. |
| Validation evidence | pass | `python scripts/test-validation-cache.py`, `python scripts/test-artifact-lifecycle-validator.py`, review-artifact validation, change-metadata validation, artifact lifecycle validation, and `git diff --check --` passed. |

## No-Finding Rationale

The implementation satisfies the M1 slice without expanding cache use at runtime. Helper invocations can now be represented as the same canonical explicit-path cache identity as direct actual runs, and tests prove the displayed helper command is preserved separately for later evidence work. Runtime cache-default behavior, formal helper evidence writing, closeout rejection, selector routing, and measurement remain correctly deferred to later milestones.

## Residual Risks

M1 intentionally does not make helper invocations cache-aware by default and does not write formal helper evidence. Those are M2/M3 responsibilities and remain open implementation work, not defects in this slice.
