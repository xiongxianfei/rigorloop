# Code Review M3 R1: Performance Result and Promotion Decision

Review ID: code-review-m3-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: M3. Performance Result, Default-Promotion Decision, and Closeout Evidence
Reviewed artifact: commit `b73f495baa90cc5e4235e95a6fc51f3189c6845f`
Reviewed commit: `b73f495baa90cc5e4235e95a6fc51f3189c6845f`
Review date: 2026-06-27
Recording status: recorded
Status: clean-with-notes
Review status: clean-with-notes
Material findings: none

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/code-review-m3-r1.md
- Open blockers: none
- Next stage: code-review
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/code-review-m3-r1.md
- Review log: docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-log.md
- Review resolution: docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-resolution.md#code-review-m3-r1
- Reviewed milestone: M3. Performance Result, Default-Promotion Decision, and Closeout Evidence
- Milestone closeout: closed
- Remaining implementation milestones: none
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed

## Review Inputs

- Diff/review surface: commit `b73f495baa90cc5e4235e95a6fc51f3189c6845f`
- Governing spec: `specs/broad-smoke-safe-parallelism.md`
- Test spec: `specs/broad-smoke-safe-parallelism.test.md`
- Active plan: `docs/plans/2026-06-27-broad-smoke-safe-parallelism.md`
- M3 implementation files: `scripts/ci.sh`, `scripts/test-select-validation.py`
- M3 evidence artifacts: `docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-result.yaml`, `docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-preservation.md`

## Diff Summary

M3 adds optional opt-in result evidence writing through
`RIGORLOOP_BROAD_SMOKE_RESULT_JSON`, records the measured `--jobs 4`
broad-smoke result, records rollback `--jobs 1` evidence after the writer
change, and explicitly defers default promotion. The measured single local run
finished in `332s`, `42061ms` / `11.24%` faster than the M1 baseline, below the
30% median target.

No default broad-smoke behavior is changed in M3.

## Findings

No material findings.

## No-Finding Rationale

The result artifact has the required jobs, phase, duration, output-size, delta,
preservation, variance, low-confidence, sequential-only, and promotion-decision
fields. It sanitizes adapter temp-root command text and records the single-run
limitation clearly. The decision to remain opt-in is consistent with the
approved spec because the measured reduction is below target, the evidence is a
single local run, and dominant checks remain sequential-only.

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | Runtime evidence is recorded, default promotion is deferred, rollback remains `--jobs 1`, and cache/composition/final-verify boundaries remain unchanged. |
| Test coverage | pass | `result_evidence`, `broad_smoke`, and `jobs` tests cover result artifact writing, child phases, delta shape, opt-in scheduling, and rollback behavior. |
| Edge cases | pass | Slower/partial improvement handling is covered by the recorded opt-in decision and sequential-only rationale. |
| Error handling | pass | M2 scheduler error handling remains covered; M3 writer is optional and inert unless the result path environment variable is set. |
| Architecture boundaries | pass | No cache, persistent worker, composition framework, new protocol, or default-promotion registry is introduced. |
| Compatibility | pass | Default broad-smoke remains sequential; explicit `--jobs 1` passed after M3. |
| Security/privacy | pass | The result artifact sanitizes adapter temp paths and records no credentials or secrets. |
| Derived artifact currency | pass | Result, preservation, plan, and change metadata are synchronized and validated. |
| Unrelated changes | pass | The diff is scoped to M3 evidence writing, tests, result artifacts, and lifecycle state. |
| Validation evidence | pass | Recorded evidence includes focused tests, real `--jobs 4` result run, real `--jobs 1` rollback run, JSON validation, lifecycle validation, diff hygiene, and selected CI. |

## Handoff

M3 is closed. All implementation milestones are closed, so the next workflow gate is final holistic cross-milestone code-review before explain-change or verify. This review does not claim branch readiness, PR readiness, final verification, or hosted CI status.
