# Code Review M3 R2 - CRM-M3-CR1 Re-review

Review ID: code-review-m3-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review
Target: commit `e05a74d`
Status: clean-with-notes

## Review inputs

- Review surface: commit `e05a74d` (`Resolve M3 compact artifact query support`).
- Reviewed milestone: M3. Bounded change-record query helper.
- Governing artifacts: `specs/change-record-catalog-registration-and-bounded-read-model.md`, `specs/change-record-catalog-registration-and-bounded-read-model.test.md`, `docs/adr/ADR-20260522-change-record-catalog-registration-and-bounded-read-model.md`, and `docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md`.
- Prior finding under re-review: `CRM-M3-CR1`.
- Implementation files reviewed: `scripts/query-change-record.py` and `scripts/test-query-change-record.py`.
- Lifecycle evidence reviewed: `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-resolution.md`, `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml`, and the M3 validation notes in the active plan.

## Diff summary

The resolution commit extends query-helper artifact extraction so accepted compact metadata can expose artifact paths through compact `path_vars` entries. The helper now expands compact path variables using the existing compact metadata resolver, selects artifact-bearing keys from an explicit allowlist, rejects unsafe or unresolved artifact paths with stable unsupported-shape diagnostics, and keeps legacy and top-level `artifacts` behavior intact. The query regression suite now covers compact `path_vars` artifact extraction for both `artifacts` and `summary`, excludes expansion-only variables, and proves unsafe or unresolved compact artifact variables fail closed.

## Findings

No blocking or required-change findings.

## Checklist coverage

- Spec alignment: pass. CRM-R29, CRM-R32, CRM-R33, and CRM-R36 require artifact paths to be available from valid legacy and compact metadata shapes; the helper now reads accepted compact `path_vars` artifact metadata rather than returning an empty successful list.
- Test coverage: pass. `scripts/test-query-change-record.py` includes direct regression coverage for compact `path_vars` without top-level `artifacts`, summary inclusion, expansion-only variable exclusion, unsafe path failure, and unresolved-variable failure.
- Edge cases: pass. The named CRM-M3-CR1 edge cases have direct proof: accepted compact fixture output includes compact artifact paths; expansion-only values such as `change_id`, `slug`, and `change_root` are excluded; unsafe and unresolved artifact variables fail closed.
- Error handling: pass. Compact artifact path query failures return `unsupported-shape` diagnostics instead of partial success or silent omission.
- Architecture boundaries: pass. The query helper remains a standalone read helper and reuses compact path-variable resolution without adding validation subcommands or executing validation bundles.
- Compatibility: pass. Top-level legacy/synthetic `artifacts` extraction remains supported, and existing compact metadata validation semantics are unchanged.
- Security/privacy: pass. Query outputs are repo-relative and compact artifact values are checked through the same repo-relative safety boundary used by the helper's existing artifact validation.
- Derived artifact currency: pass. No generated skills or adapters are in scope for M3.
- Unrelated changes: pass. The diff is scoped to query-helper compact artifact extraction, tests, and lifecycle state/evidence updates.
- Validation evidence: pass. Recorded and rerun validation includes `python scripts/test-query-change-record.py`, direct compact fixture `artifacts` and `summary` query proof, active query smoke commands, metadata validator regression, selected CI for query/helper/metadata paths, lifecycle validation, review-artifact structure validation, and whitespace.

## No-finding rationale

The R1 finding was that a valid compact `change.yaml` with artifact paths in `path_vars` could return a successful empty `artifact_paths` list. The resolution adds an explicit compact artifact-key allowlist, expands those keys through the compact metadata resolver, rejects invalid artifact-bearing path variables, and proves both `artifacts` and `summary` return compact artifact paths. The direct compact fixture proof now returns `specs/compact-change-validation-metadata.md` and `specs/compact-change-validation-metadata.test.md` instead of an empty list.

## Handoff

Reviewed milestone: M3. Bounded change-record query helper
Review status: clean-with-notes
Milestone closeout: closed
Required review-resolution: no
Next stage: implement M4
Remaining implementation milestones: M4, M5
Verify readiness: not-claimed
