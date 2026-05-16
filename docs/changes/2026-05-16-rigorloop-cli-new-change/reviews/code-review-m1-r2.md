# Code Review M1 R2

Review ID: code-review-m1-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review skill
Target: M1 working tree implementation after `CR1-F1` resolution
Status: clean-with-notes

## Scope

Reviewed the M1 rerun after the accepted `CR1-F1` fix against the approved `new-change` spec, active test spec, active plan milestone, actual working tree diff, and recorded validation evidence.

## Review inputs

- Diff surface: `packages/rigorloop/dist/bin/rigorloop.js`, `packages/rigorloop/dist/lib/new-change.js`, `packages/rigorloop/test/cli.test.js`, active plan, plan index, change metadata, review log, review-resolution, and code-review records.
- Prior finding: `CR1-F1` in `docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/code-review-m1-r1.md`.
- Resolution record: `docs/changes/2026-05-16-rigorloop-cli-new-change/review-resolution.md#code-review-m1-r1`.
- Governing spec: `specs/rigorloop-cli-new-change.md`.
- Test spec: `specs/rigorloop-cli-new-change.test.md`.
- Plan milestone: `docs/plans/2026-05-16-rigorloop-cli-new-change.md` M1.
- Architecture: `docs/architecture/system/architecture.md`.
- Validation evidence inspected:
  - `npm test --prefix packages/rigorloop -- --test-name-pattern 'TNC-006'` failed before the renderer fix and passed after the fix.
  - `npm test --prefix packages/rigorloop`.
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-16-rigorloop-cli-new-change`.
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`.
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path specs/rigorloop-cli-new-change.md --path specs/rigorloop-cli-new-change.test.md --path docs/plans/2026-05-16-rigorloop-cli-new-change.md --path docs/plan.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`.
  - `git diff --check -- packages/rigorloop specs/rigorloop-cli-new-change.test.md docs/plans/2026-05-16-rigorloop-cli-new-change.md docs/plan.md docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`.

## Diff summary

M1 adds the package-local `new-change` helper module, command dispatch, help output, invalid-usage handling, and no-write dry-run JSON metadata planning. The rerun specifically verifies that `renderChangeMetadata` now emits `review.unresolved_items: 0` and that `TNC-006` directly asserts the deterministic `changed_files` to `review` block includes the numeric field. Review-resolution, review log, active plan, and change metadata now show `CR1-F1` resolved and M1 ready for rerun review.

## Findings

No blocking or required-change findings.

## Checklist coverage

| Check | Result | Notes |
|---|---|---|
| Spec alignment | pass | M1 covers command discovery, option validation, deterministic metadata rendering, JSON envelope behavior, and no-write dry-run planning. The `review.unresolved_items: 0` requirement from R30 is now implemented. |
| Test coverage | pass | `TNC-002` through `TNC-008` cover required M1 behavior; `TNC-006` now directly proves `review.unresolved_items: 0`. |
| Edge cases | pass | M1 unsafe IDs, classification domains, risk/profile values, missing required inputs, YAML quoting, and no-write dry-run behavior have direct tests. Filesystem mutation edge cases remain in M2/M3 by plan. |
| Error handling | pass | Invalid usage returns JSON `status: error`, exit code `4`, and field-specific error codes for reviewed M1 paths. |
| Architecture boundaries | pass | The helper remains package-local, with no new dependency, network behavior, persistence surface, adapter behavior, lockfile behavior, or workflow-YAML work. |
| Compatibility | pass | Existing `init`, lockfile, and archive package tests remain green, and fixture package copying includes the new helper module. |
| Security/privacy | pass | Validators reject unsafe path-like identifiers and classification tokens; generated metadata tests check local path and sensitive-marker omission. |
| Derived artifact currency | pass | No generated adapter or skill output is affected by M1. |
| Unrelated changes | pass | The reviewed implementation diff is scoped to M1 CLI/test behavior and the required lifecycle review artifacts. |
| Validation evidence | pass | Recorded package tests, review-artifact validation, change metadata validation, selected CI, and diff check are relevant to the reviewed paths. |

## No-finding rationale

The only M1 rerun finding from `code-review-m1-r1` was the missing `review.unresolved_items: 0` field. The renderer now emits that numeric field under `review`, and the deterministic metadata test proves the required block order and value. The rest of the M1 surface remains limited to validation, deterministic metadata generation, and dry-run JSON output, while actual filesystem mutation stays deferred to M2.

## Residual risks

M2 must replace the temporary non-dry-run blocked path with the approved write-plan and mutation behavior. This is already captured by the active plan and is not a blocker for closing M1.

## Recommended next stage

Close M1 and proceed to `implement M2`.
