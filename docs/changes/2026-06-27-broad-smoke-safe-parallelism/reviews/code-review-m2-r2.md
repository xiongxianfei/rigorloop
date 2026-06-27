# Code Review M2 R2: Opt-In Parallel Executor

Review ID: code-review-m2-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review skill
Target: M2. Opt-In Parallel Executor and Deterministic Aggregation
Reviewed artifact: commit `ed859260fbb8fe64835ed5960050d69f958d2792`
Reviewed commit: `ed859260fbb8fe64835ed5960050d69f958d2792`
Review date: 2026-06-27
Recording status: recorded
Status: clean-with-notes
Review status: clean-with-notes
Material findings: none

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/code-review-m2-r2.md
- Open blockers: none
- Next stage: implement
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/code-review-m2-r2.md
- Review log: docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-log.md
- Review resolution: docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-resolution.md#code-review-m2-r2
- Reviewed milestone: M2. Opt-In Parallel Executor and Deterministic Aggregation
- Milestone closeout: closed
- Remaining implementation milestones: M3
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed

## Review Inputs

- Diff/review surface: commit `ed859260fbb8fe64835ed5960050d69f958d2792`
- Prior review: `docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/code-review-m2-r1.md`
- Review resolution: `docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-resolution.md#code-review-m2-r1`
- Governing spec: `specs/broad-smoke-safe-parallelism.md`
- Test spec: `specs/broad-smoke-safe-parallelism.test.md`
- Active plan: `docs/plans/2026-06-27-broad-smoke-safe-parallelism.md`
- M2 implementation files: `scripts/ci.sh`, `scripts/test-select-validation.py`, `scripts/validate-broad-smoke-classification.py`
- M2 evidence artifact: `docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-preservation.md`

## Diff Summary

The R2 review surface resolves `CR-M2-1` by registering each opt-in broad-smoke
child result slot before launch and treating missing or incomplete result
metadata as a deterministic scheduler failure. The regression fixture now
simulates a background worker crash and verifies the broad-smoke wrapper exits
nonzero with scheduler diagnostics instead of omitting the child from aggregate
evidence.

The opt-in scheduler remains limited to explicit `--jobs > 1`; omitted `--jobs`
and `--jobs 1` still use the sequential compatibility path.

## Findings

No material findings.

## No-Finding Rationale

`CR-M2-1` is resolved. The aggregation path no longer depends on child result
directories appearing only after successful worker completion: expected slots
are created before launch, incomplete slots are converted to scheduler failures,
and the new `worker_crash` regression proves the missing-result path exits
nonzero with diagnostics. The M2 implementation satisfies the opt-in,
classification-preflight, sequential-fallback, deterministic-output, grouped
verbose, all-failures, and rollback requirements within the approved scope.

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | Explicit `--jobs > 1` enables first-slice opt-in scheduling; omitted `--jobs` and `--jobs 1` remain sequential; scheduler errors now fail closed. |
| Test coverage | pass | Tests cover opt-in overlap, omitted jobs, `--jobs 1`, verbose grouping, missing classification, multiple failures, and worker crash scheduler diagnostics. |
| Edge cases | pass | EC5, EC6, EC7, EC8, and EC9 have direct fixture coverage in `scripts/test-select-validation.py`. |
| Error handling | pass | Missing classification fails before launch, captured child failures aggregate in canonical order, and incomplete worker result metadata exits nonzero as a scheduler error. |
| Architecture boundaries | pass | The change stays inside the CI wrapper, tests, validator diagnostics, and change-local evidence; no cache, persistent worker, composition framework, or new protocol is introduced. |
| Compatibility | pass | Sequential rollback remains available via omitted `--jobs` and explicit `--jobs 1`; real `--jobs 1` broad-smoke passed after M2. |
| Security/privacy | pass | Per-child capture uses temporary directories and does not introduce credential persistence or external network behavior. |
| Derived artifact currency | pass | Plan, review-resolution, review-log, and change metadata are synchronized and validated. |
| Unrelated changes | pass | The diff is scoped to M2 implementation, tests, review resolution, and lifecycle state. |
| Validation evidence | pass | Recorded validation includes focused broad-smoke/jobs tests, worker-crash regression, syntax check, classification validation, review closeout checks, lifecycle validation, diff hygiene, selected CI, and real `--jobs 1` broad-smoke rollback. |

## Handoff

M2 is closed. The approved auto-through workflow may proceed to M3 implementation. This review does not claim branch readiness, PR readiness, final verification, or hosted CI status.
