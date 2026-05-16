# Code Review M3 R1

Review ID: code-review-m3-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: M3 working tree implementation for `rigorloop new-change`
Status: clean-with-notes

## Scope

Reviewed M3 partial failure behavior, output polish, and final integration for the `rigorloop new-change` first slice.

## Review inputs

- Diff surface: `packages/rigorloop/dist/bin/rigorloop.js`, `packages/rigorloop/dist/lib/new-change-filesystem.js`, `packages/rigorloop/test/cli.test.js`, active plan and change metadata updates.
- Governing spec: `specs/rigorloop-cli-new-change.md`.
- Test spec: `specs/rigorloop-cli-new-change.test.md`.
- Plan milestone: `docs/plans/2026-05-16-rigorloop-cli-new-change.md` M3.
- Architecture: `docs/architecture/system/architecture.md`.
- Validation evidence inspected:
  - `npm test --prefix packages/rigorloop -- --test-name-pattern 'TNC-017|TNC-018|TNC-019'`.
  - `npm test --prefix packages/rigorloop`.
  - `python scripts/test-select-validation.py`.
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path packages/rigorloop --path specs/rigorloop-cli-new-change.md --path specs/rigorloop-cli-new-change.test.md --path docs/plans/2026-05-16-rigorloop-cli-new-change.md --path docs/plan.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`.
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path specs/rigorloop-cli-new-change.md --path specs/rigorloop-cli-new-change.test.md --path docs/plans/2026-05-16-rigorloop-cli-new-change.md --path docs/plan.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`.
  - `git diff --check -- packages/rigorloop specs/rigorloop-cli-new-change.test.md docs/plans/2026-05-16-rigorloop-cli-new-change.md docs/plan.md docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`.

## Diff summary

M3 factors `new-change` filesystem planning and mutation into `packages/rigorloop/dist/lib/new-change-filesystem.js`, preserving the CLI command surface while making partial write failures deterministic to test. The helper reports completed directory actions as `done`, failed file actions as `failed`, returns `status: error`, maps the process exit class to internal error, and marks the scaffold artifact as `failed` when `change.yaml` cannot be written. The CLI now delegates `new-change` execution to that helper and still routes process exits through `exitCodeForResult`.

The tests add direct M3 coverage for non-atomic partial write failure, human output, JSON quiet/debug behavior, color suppression, unknown-option no-mutation behavior, and running `new-change` in a non-Git temporary directory. Existing package tests continue to cover `version`, `init`, archive verification, lockfile behavior, and earlier `new-change` milestones.

## Findings

No blocking or required-change findings.

## Checklist coverage

| Check | Result | Notes |
|---|---|---|
| Spec alignment | pass | M3 covers `R56a-R56k`, `R57-R70`, and `R71-R76`; partial write failures are observable and output modes follow the shared CLI contract. |
| Test coverage | pass | `TNC-017`, `TNC-018`, and `TNC-019` cover the M3 cases, and the full package test suite passed. |
| Edge cases | pass | Partial write failure, unknown options without mutation, non-Git project execution, no-color, quiet, and debug paths have direct proof. |
| Error handling | pass | `write-failed` results return `status: error`, exit class `internal`, exit code `1`, failed action state, and an `errors[]` entry naming the failed path. |
| Architecture boundaries | pass | The helper is package-local, introduces no dependency, and does not expose public runtime override hooks. |
| Compatibility | pass | Existing `init`, lockfile, archive, and earlier `new-change` tests remain green in the full package suite. |
| Security/privacy | pass | No secrets, environment values, Git/PR state, or network behavior are added; non-Git local execution is tested. |
| Derived artifact currency | pass | No generated adapter or skill output is affected by M3. |
| Unrelated changes | pass | The reviewed M3 diff is limited to CLI helper extraction, tests, and lifecycle handoff artifacts. |
| Validation evidence | pass | Plan-recorded validation covers narrow M3 tests, full package tests, selector regression, change metadata, artifact lifecycle, selected CI, and diff check. |

## No-Finding Rationale

The M3 helper seam directly satisfies the test spec's deterministic partial failure requirement without relying on platform-specific permissions. The CLI delegates to the helper and keeps the public JSON envelope and exit-code helper intact. The new tests exercise the M3 behavior directly, and the full package test suite plus selected CI show no regression in existing command surfaces.

## Residual Risks

Implementation milestones are closed, but final lifecycle closeout is still pending. This review does not claim explain-change, verify, PR readiness, hosted CI, or branch readiness.

## Recommended next stage

Close M3 and enter downstream closeout with `explain-change`.
