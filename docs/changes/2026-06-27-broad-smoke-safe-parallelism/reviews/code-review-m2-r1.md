# Code Review M2 R1: Opt-In Parallel Executor

Review ID: code-review-m2-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: M2. Opt-In Parallel Executor and Deterministic Aggregation
Reviewed artifact: commit `671c02b6c7089ea89dc7797dd9bc66f365180fee`
Reviewed commit: `671c02b6c7089ea89dc7797dd9bc66f365180fee`
Review date: 2026-06-27
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Material findings: CR-M2-1

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/code-review-m2-r1.md
- Open blockers: none
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: CR-M2-1
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/code-review-m2-r1.md
- Review log: docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-log.md
- Review resolution: docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-resolution.md#code-review-m2-r1
- Reviewed milestone: M2. Opt-In Parallel Executor and Deterministic Aggregation
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3
- Required review-resolution: yes
- Finding IDs: CR-M2-1
- Verify readiness: not-claimed

## Review Inputs

- Diff/review surface: commit `671c02b6c7089ea89dc7797dd9bc66f365180fee`
- Governing spec: `specs/broad-smoke-safe-parallelism.md`
- Test spec: `specs/broad-smoke-safe-parallelism.test.md`
- Active plan: `docs/plans/2026-06-27-broad-smoke-safe-parallelism.md`
- M2 implementation files: `scripts/ci.sh`, `scripts/test-select-validation.py`, `scripts/validate-broad-smoke-classification.py`
- M2 evidence artifact: `docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-preservation.md`

## Diff Summary

M2 adds an explicit `--jobs > 1` broad-smoke opt-in scheduler, classification
preflight, per-child capture files, deterministic aggregation, all-failure
reporting for captured child results, fixture coverage for opt-in overlap,
sequential compatibility, verbose grouping, missing classification, and multiple
captured failures.

Omitted `--jobs` and `--jobs 1` remain on the existing sequential broad-smoke
path.

## Findings

## Finding CR-M2-1

Finding ID: CR-M2-1
Severity: major
Location: `scripts/ci.sh:277`; `scripts/ci.sh:388`
Evidence: `broad_smoke_wait_oldest_parallel_child` discards background process exit status with `wait "$pid" || true`, and `broad_smoke_aggregate_results` iterates fixed slots but skips any missing child result directory with `continue`. If a scheduler worker exits before writing its result files, broad-smoke can omit that required child from aggregation and still print a successful `[PASS] broad-smoke: <lower count> checks passed ...` line. This violates the spec requirement that scheduler errors and worker crashes exit nonzero, and it can mask a required child that never produced evidence.
Required outcome: Opt-in broad-smoke aggregation must treat every launched required child as expected evidence. A missing, incomplete, or unreadable child result must be reported as a scheduler error and make broad-smoke exit nonzero, with deterministic diagnostics attached to the canonical child slot.
Safe resolution path: Track expected child result slots when scheduling children, make aggregation fail closed for any expected slot with missing result metadata, and add a regression test that simulates a worker crash or missing result file before aggregation.
needs-decision rationale: none
auto_fix_class: bounded
auto_fix_scope: `scripts/ci.sh`, `scripts/test-select-validation.py`, M2 validation evidence, and lifecycle state surfaces.
auto_fix_validation: `python scripts/test-select-validation.py -k broad_smoke`; `python scripts/test-select-validation.py -k jobs`; `bash -n scripts/ci.sh`; selected explicit CI for M2 paths.

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | concern | Opt-in scheduling, output capture, and deterministic aggregation are present, but missing worker-result handling violates scheduler-error fail-closed requirements. |
| Test coverage | concern | Tests cover captured child failures and missing classification, but no test simulates a worker crash or missing child result. |
| Edge cases | concern | EC7 scheduler worker crash is not directly covered and can be masked by missing-result skipping. |
| Error handling | concern | Captured child failures are handled, but missing scheduler evidence is skipped rather than converted into a nonzero scheduler error. |
| Architecture boundaries | pass | The change stays inside `scripts/ci.sh`, repository tests, and change-local evidence; no cache, persistent worker, composition framework, or new protocol is introduced. |
| Compatibility | pass | Omitted `--jobs` and `--jobs 1` remain on the sequential compatibility path. |
| Security/privacy | pass | Per-child output capture uses temporary directories and does not add credential handling or persistence. |
| Derived artifact currency | pass | Preservation evidence and change metadata are updated for M2. |
| Unrelated changes | pass | The diff is scoped to M2 implementation, tests, validator diagnostics, and lifecycle evidence. |
| Validation evidence | pass | Recorded validation covers focused tests, `--jobs 1` real broad-smoke rollback, syntax, lifecycle, metadata, diff hygiene, and selected CI. |

## Handoff

M2 requires review-resolution for `CR-M2-1` before it can close or hand off to M3 implementation. This review does not claim branch readiness, PR readiness, final verification, or hosted CI status.
