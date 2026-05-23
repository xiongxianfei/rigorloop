# Code Review M3 R1 - Validation Idempotency and Cache-Hit Safety

Review ID: code-review-m3-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: M3 commit `2769e2c`
Reviewed milestone: M3. Compact metadata evidence-kind and closeout enforcement
Reviewed artifact: scripts/validate-change-metadata.py; scripts/artifact_lifecycle_validation.py
Review date: 2026-05-23
Recording status: recorded
Status: approved

## Result

- Skill: code-review
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/reviews/code-review-m3-r1.md`
- Review log: `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/review-log.md`
- Review resolution: not-required
- Reviewed milestone: M3. Compact metadata evidence-kind and closeout enforcement
- Milestone closeout: closed
- Remaining implementation milestones: M4 planned
- Required review-resolution: no
- Verify readiness: not-claimed

## Review Inputs

- Diff/review surface: commit `2769e2c` against `7d20d2a`, with focus on `scripts/validate-change-metadata.py`, `scripts/artifact_lifecycle_validation.py`, M3 tests, compact metadata fixtures, and lifecycle artifact updates.
- Tracked governing branch state: proposal, approved spec, ADR, active plan, test spec, review log, review-resolution, M1 and M2 review records, and M3 implementation commit are present in the branch.
- Governing artifacts: `specs/validation-idempotency-and-cache-hit-safety.md`, `specs/validation-idempotency-and-cache-hit-safety.test.md`, `docs/adr/ADR-20260523-validation-idempotency-cache-hit-safety.md`, and `docs/plans/2026-05-23-validation-idempotency-cache-hit-safety.md`.
- Validation evidence inspected and rerun: targeted M3 reviewer checks for compact invalid fixtures, compact M3 valid fixtures, lifecycle cache-only closeout rejection, and direct metadata validation of legacy valid plus cache-hit-plus-closeout fixtures.

## Diff Summary

M3 adds compact `validation_events[].evidence_kind` validation for the first-slice evidence kinds and required result pairings, adds `evidence_ref` safety and anchor checks, rejects unsupported cache-evidence fields in legacy validation metadata, and makes compact closeout events with `cache-hit-inner-loop` invalid. The artifact lifecycle validator now tracks change metadata files in scope and rejects compact closeout records that rely only on cache-hit evidence. The test fixtures cover valid supporting cache-hit evidence plus actual-run closeout, invalid evidence-kind/result pairings, unsafe or unresolved evidence refs, cache-only closeout, and legacy cache-field misuse.

## Findings

No blocking or required-change findings.

## Checklist Coverage

| Check | Result | Notes |
| --- | --- | --- |
| Spec alignment | pass | The implementation addresses R50-R59 and R101-R116 by allowing cache hits only as inner-loop/supporting evidence, enforcing evidence-kind/result pairings, rejecting cache-only closeout, and preserving legacy compatibility except for unsupported cache evidence fields. |
| Test coverage | pass | M3 adds fixtures and assertions for VIC-T023 through VIC-T027: valid supporting cache evidence plus actual-run closeout, invalid evidence-kind/result pairings, unsafe and unresolved evidence refs, cache-only closeout, and legacy metadata field misuse. |
| Edge cases | pass | Reviewer-run proof covered invalid compact cases, valid M3 compact cases, lifecycle cache-only closeout rejection, and legacy valid metadata. |
| Error handling | pass | Invalid compact metadata returns stable diagnostics; malformed or unsafe evidence refs fail validation rather than being accepted as reviewable evidence. |
| Architecture boundaries | pass | Change metadata owns compact event shape and evidence references; artifact lifecycle owns the closeout guard for cache-only lifecycle evidence. |
| Compatibility | pass | Existing legacy metadata remains valid unless it attempts to use the unsupported new cache evidence fields. |
| Security/privacy | pass | Evidence refs are repository-relative and unsafe absolute, home, URL, hostname, credential-bearing, and Windows absolute paths are rejected by metadata path validation. |
| Derived artifact currency | pass | No generated artifacts are changed. |
| Unrelated changes | pass | The diff is scoped to M3 validators, fixtures, tests, behavior-preservation evidence, and lifecycle state updates. |
| Validation evidence | pass | Implementation validation and reviewer-run checks cover the named M3 behavior and selected CI for touched validator/test paths. |

## No-Finding Rationale

The M3 implementation satisfies the approved first-slice closeout enforcement contract without introducing Workstream B or broad validator selection changes. The new compact metadata checks reject cache-only closeout and invalid evidence states, while the lifecycle validator independently rejects compact closeout records backed only by cache-hit evidence. The direct tests prove the named valid and invalid paths, including legacy compatibility.

## Residual Risks

- M3 uses compact validation event stage IDs containing `closeout` as the first-slice closeout signal because the approved metadata contract does not add a separate closeout boolean field.
- Workstream A measurement and selector/routing evidence remain planned for M4.

## Milestone Handoff

- Reviewed milestone: M3. Compact metadata evidence-kind and closeout enforcement.
- Review status: clean-with-notes.
- Milestone state after review: closed.
- Required review-resolution: no.
- Remaining in-scope implementation milestones: M4 remains planned.
- Next stage: implement M4.
- Final closeout readiness: not ready; M4 is not implemented or reviewed, final validation has not run, explain-change and verify are not recorded, and PR handoff is not prepared.
