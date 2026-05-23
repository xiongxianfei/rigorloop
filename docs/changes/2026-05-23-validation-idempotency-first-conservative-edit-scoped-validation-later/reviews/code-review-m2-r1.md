# Code Review M2 R1 - Validation Idempotency and Cache-Hit Safety

Review ID: code-review-m2-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: M2 commit `43f7776`
Reviewed milestone: M2. Explicit-path lifecycle cache integration and cache-hit evidence
Reviewed artifact: scripts/validation_cache.py; scripts/validate-artifact-lifecycle.py
Review date: 2026-05-23
Recording status: recorded
Status: changes-requested

## Result

- Skill: code-review
- Review status: changes-requested
- Material findings: VIC-CR-M2-R1-F1, VIC-CR-M2-R1-F2
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/reviews/code-review-m2-r1.md`
- Review log: `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/review-log.md`
- Review resolution: `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/review-resolution.md#code-review-m2-r1`
- Reviewed milestone: M2. Explicit-path lifecycle cache integration and cache-hit evidence
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2 pending review-resolution; M3 and M4 planned
- Required review-resolution: yes
- Verify readiness: not-claimed

## Review Inputs

- Diff/review surface: commit `43f7776` against `e00d7b9`, with focus on `scripts/validation_cache.py`, `scripts/validate-artifact-lifecycle.py`, M2 tests, and lifecycle artifact updates.
- Tracked governing branch state: proposal, approved spec, ADR, active plan, test spec, M1 review records, review log, and review-resolution are present in the branch.
- Governing artifacts: `specs/validation-idempotency-and-cache-hit-safety.md`, `specs/validation-idempotency-and-cache-hit-safety.test.md`, `docs/adr/ADR-20260523-validation-idempotency-cache-hit-safety.md`, and `docs/plans/2026-05-23-validation-idempotency-cache-hit-safety.md`.
- Validation evidence inspected: M2 plan validation notes and change metadata entries for `python scripts/test-validation-cache.py`, `python scripts/test-artifact-lifecycle-validator.py`, `python scripts/test-select-validation.py`, change metadata validation, artifact lifecycle validation, selected CI, and `git diff --check --`.

## Diff Summary

M2 adds opt-in local cache integration to `scripts/validate-artifact-lifecycle.py` for `--mode explicit-paths`, adds local cache record persistence and cache-hit lookup helpers in `scripts/validation_cache.py`, writes single-entry formal cache-hit evidence when explicitly requested, adds regression tests for lifecycle cache identity and second-run cache hits, ignores `.rigorloop-validation-cache/`, and records behavior-preservation and lifecycle state updates.

## Findings

### VIC-CR-M2-R1-F1: Local cache hits do not require a valid cache key or validator ID

Finding ID: VIC-CR-M2-R1-F1
Severity: major
Location: `scripts/validation_cache.py:61`, `scripts/validation_cache.py:355`, `scripts/validation_cache.py:381`

Evidence: `LocalCacheRecord` gives `cache_key` a default empty string and `validator_id` a default value, so `load_local_cache_records` can accept an older or malformed record that omits those fields. `local_cache_entry_eligible` then checks result, repository, branch, worktree, change ID, command hash, input-surface hash, implementation hash, and policy hash, but it never checks that the stored cache key matches the currently computed cache key or that the stored `validator_id` is `artifact-lifecycle`. The M2 cache-hit path in `validate-artifact-lifecycle.py` trusts any eligible record returned by `find_local_cache_hit`.

Spec `R11` requires the validator to run if any cache-key component is unknown, missing, malformed, unsupported, or changed. The first-slice cache key also includes the validator ID and command family in `build_lifecycle_cache_identity`, but those fields are not enforced during local cache hit eligibility. This means a malformed local cache record can still skip actual validation if the compared hashes match.

Required outcome: Local cache hit eligibility must fail closed when the stored cache key is missing or differs from the current computed key, and when the stored validator ID is missing, malformed, unsupported, or different from the first-slice validator ID.

Safe resolution path: Add `cache_key`, `validator_id`, and, if kept in the identity, `command_family` to the local cache eligibility context or compare them before accepting a hit. Treat missing or mismatched values as cache-ineligible and run the validator. Add direct tests for missing `cache_key`, mismatched `cache_key`, unsupported `validator_id`, and matching valid records.

### VIC-CR-M2-R1-F2: Formal cache-hit evidence writing overwrites existing cache-hit records

Finding ID: VIC-CR-M2-R1-F2
Severity: major
Location: `scripts/validation_cache.py:458`

Evidence: `write_cache_hit_evidence` writes `_render_cache_hit_evidence(...)` directly to `validation-cache-evidence.yaml` with `target.write_text(...)`. `_render_cache_hit_evidence` always renders one `cache_hits` entry. There is no read-merge-write path, no preservation of existing cache-hit records, and no test for adding a second cache-hit ID to an existing evidence file.

Spec `R32` requires formal cache-hit evidence whenever a cache hit is cited in formal workflow validation, and `R36` through `R44` define each cache-hit record inside the evidence file. The active plan M2 implementation step says to add a path for writing or updating `validation-cache-evidence.yaml`. Replacing the whole file on each write can silently erase an earlier formal cache-hit claim, leaving skipped validations no longer reviewable from change-local evidence.

Required outcome: Writing a cache-hit evidence record must preserve existing cache-hit records unless the same stable cache-hit ID is intentionally replaced.

Safe resolution path: Update `write_cache_hit_evidence` to load the existing `schema_version: 1` evidence file when present, preserve unrelated `cache_hits`, replace only a matching `id`, and then write the merged file. Add tests that write two distinct cache-hit IDs and prove both remain, plus a same-ID update test if replacement is supported.

## Checklist Coverage

| Check | Result | Notes |
| --- | --- | --- |
| Spec alignment | concern | Runtime cache integration is limited to explicit-path lifecycle validation, but malformed cache records can still be accepted contrary to `R11`, and formal evidence updates can erase earlier required evidence. |
| Test coverage | concern | Tests cover the happy-path second-run cache hit, failed prior result, input/helper/policy invalidation, and single-entry evidence shape, but they do not cover missing/mismatched cache keys, unsupported stored validator IDs, or preserving multiple formal cache-hit records. |
| Edge cases | concern | Named malformed/uncertain cache-key and formal evidence reviewability edge cases are not fully proven. |
| Error handling | concern | Cache identity construction failures fall back to actual validation, but loaded local cache records are not rejected when key identity fields are missing or mismatched. |
| Architecture boundaries | pass | Cache execution remains in the CLI/helper layer, and `artifact_lifecycle_validation.validate_repository` actual-run semantics are not changed. |
| Compatibility | pass | Cache use is opt-in, unsupported modes run normally, CI disables cache lookup, and `.rigorloop-validation-cache/` is ignored. |
| Security/privacy | concern | The formal evidence writer avoids worktree paths in the tested single-record case, but evidence overwrite can remove the reviewable trail required for skipped validation claims. |
| Derived artifact currency | pass | No generated outputs are changed. |
| Unrelated changes | pass | The diff is scoped to M2 cache integration, tests, and lifecycle evidence updates. |
| Validation evidence | concern | Recorded validation is relevant for covered behavior, but it does not prove malformed local cache records are rejected or that multiple formal cache-hit records remain reviewable. |

## No-Finding Rationale

Not applicable. Two material findings require review-resolution before M2 can close.

## Milestone Handoff

- Reviewed milestone: M2. Explicit-path lifecycle cache integration and cache-hit evidence.
- Review status: changes-requested.
- Milestone state after review: resolution-needed.
- Required review-resolution: yes, for `VIC-CR-M2-R1-F1` and `VIC-CR-M2-R1-F2`.
- Remaining in-scope implementation milestones: M2 pending review-resolution; M3 and M4 remain planned.
- Next stage: review-resolution for M2.
- Final closeout readiness: not ready; M2 is unresolved, M3 and M4 are not implemented or reviewed, final validation has not run, explain-change and verify are not recorded, and PR handoff is not prepared.
