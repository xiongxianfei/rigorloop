# Code Review M3 R1 - Bounded Query Helper

Review ID: code-review-m3-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: commit `ac3be67`
Status: changes-requested

## Review inputs

- Review surface: commit `ac3be67` (`M3: add change record query helper`).
- Reviewed milestone: M3. Bounded change-record query helper.
- Governing artifacts: `specs/change-record-catalog-registration-and-bounded-read-model.md`, `specs/change-record-catalog-registration-and-bounded-read-model.test.md`, `docs/adr/ADR-20260522-change-record-catalog-registration-and-bounded-read-model.md`, and `docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md`.
- Implementation files reviewed: `scripts/query-change-record.py`, `scripts/test-query-change-record.py`, `scripts/validation_selection.py`, and `scripts/test-select-validation.py`.
- Lifecycle evidence reviewed: `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml`, `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/behavior-preservation.md`, `docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md`, and `docs/plan.md`.

## Diff summary

M3 adds `scripts/query-change-record.py` as a standalone JSON query helper with `summary`, `artifacts`, `validation --latest`, and `validation --stage <stage>` commands. It adds `scripts/test-query-change-record.py` with compact and legacy synthetic fixtures, stable diagnostic tests, read-only command-boundary tests, and active change summary proof. It also adds selector routing for query-helper paths through `change_record_query.regression`, records behavior-preservation evidence, and updates the active plan to hand off M3 for code review.

## Findings

### CRM-M3-CR1: Compact artifact paths omit accepted `path_vars` artifact metadata

Finding ID: CRM-M3-CR1
Severity: major

Location: `scripts/query-change-record.py`, `artifact_paths`; `scripts/test-query-change-record.py`, compact fixture setup.

Evidence: CRM-R29 requires owning artifact paths to be available from `change.yaml` artifact/path metadata or the query helper. CRM-R36 requires the query helper to support legacy and compact metadata shapes that remain valid under existing metadata contracts. CRM-T016 also calls for running the helper against supported legacy and compact fixtures. The implementation's `artifact_paths()` reads only top-level `artifacts` values. The query tests create a synthetic compact fixture with top-level `artifacts`, so they do not exercise the repository's accepted compact shape. The existing valid compact fixture `tests/fixtures/change-metadata/compact-valid/change.yaml` stores artifact/path metadata in compact `path_vars` entries such as `spec` and `test_spec`, not in top-level `artifacts`. A direct proof against that valid compact fixture, copied under a normal `docs/changes/<id>/change.yaml` layout, returns:

```json
{
  "query": "artifacts",
  "artifact_paths": []
}
```

That is a supported compact metadata shape returning an empty artifact inventory even though artifact path metadata is present.

Required outcome: The query helper must return canonical artifact paths for accepted compact metadata, including compact `path_vars` artifact entries, or report a stable unsupported-shape diagnostic when it cannot safely query that valid compact shape. It must not return a successful empty artifact list for a supported compact record with artifact path metadata.

Safe resolution path: Extend artifact extraction to include compact artifact path variables using the existing compact metadata artifact key mapping or an equivalent selector-local allowlist aligned with `validate-change-metadata.py`. Add a regression test using an accepted compact fixture shape without top-level `artifacts`, proving `summary` and `artifacts` include compact artifact paths such as `specs/{slug}.md` and `specs/{slug}.test.md` after path-var expansion. Rerun `python scripts/test-query-change-record.py`, `python scripts/test-change-metadata-validator.py`, the active query commands, selected CI for query/helper/metadata paths, lifecycle validation, review-artifact validation, and `git diff --check --`.

## Checklist coverage

- Spec alignment: block. CRM-R29 and CRM-R36 are not satisfied for accepted compact metadata path metadata.
- Test coverage: concern. The new tests cover synthetic compact and legacy fixtures, but they miss the existing compact fixture shape where artifact paths live in `path_vars`.
- Edge cases: concern. CRM-T016's supported compact fixture path is not directly proven.
- Error handling: pass for the reviewed failure modes. Unknown change, unsupported query, missing validation evidence, unknown stage, unsafe artifact path, and read-only behavior have direct tests.
- Architecture boundaries: pass. The helper is standalone and does not add query behavior as a `validate-change-metadata.py` subcommand.
- Compatibility: block. A valid compact metadata shape is queried successfully but returns an incomplete artifact slice.
- Security/privacy: pass for covered paths. Tests cover unsafe absolute artifact paths and deterministic read-only behavior.
- Derived artifact currency: pass. No generated skill or adapter outputs are in M3 scope.
- Unrelated changes: pass. The diff is scoped to the query helper, selector routing for that helper, tests, and lifecycle evidence.
- Validation evidence: concern. The recorded validation is relevant, but it does not include direct proof against the existing compact metadata artifact-path shape.

## Handoff

Reviewed milestone: M3. Bounded change-record query helper
Review status: changes-requested
Milestone closeout: resolution-needed
Required review-resolution: yes
Next stage: review-resolution / implement M3 fix
Remaining implementation milestones: M3, M4, M5
Verify readiness: not-claimed
