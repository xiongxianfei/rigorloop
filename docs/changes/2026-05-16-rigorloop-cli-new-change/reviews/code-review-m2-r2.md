# Code Review M2 R2

Review ID: code-review-m2-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review skill
Target: M2 working tree implementation for `rigorloop new-change`
Status: clean-with-notes

## Scope

Reviewed the M2 rerun after `CR2-F1` resolution. The review focused on write-plan, dry-run, and safe metadata scaffolding behavior plus direct proof for the previously missing named edge cases.

## Review inputs

- Diff surface: `packages/rigorloop/dist/bin/rigorloop.js`, `packages/rigorloop/test/cli.test.js`, `scripts/validate-change-metadata.py`, `scripts/test-change-metadata-validator.py`, active plan and change metadata updates.
- Governing spec: `specs/rigorloop-cli-new-change.md`.
- Test spec: `specs/rigorloop-cli-new-change.test.md`.
- Plan milestone: `docs/plans/2026-05-16-rigorloop-cli-new-change.md` M2.
- Architecture: `docs/architecture/system/architecture.md`.
- Review-resolution evidence: `docs/changes/2026-05-16-rigorloop-cli-new-change/review-resolution.md`.
- Validation evidence inspected:
  - `npm test --prefix packages/rigorloop -- --test-name-pattern 'TNC-012|TNC-014'`.
  - `npm test --prefix packages/rigorloop`.
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-16-rigorloop-cli-new-change`.
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`.
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path scripts/validate-change-metadata.py --path scripts/test-change-metadata-validator.py --path specs/rigorloop-cli-new-change.md --path specs/rigorloop-cli-new-change.test.md --path docs/plans/2026-05-16-rigorloop-cli-new-change.md --path docs/plan.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`.
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path scripts/validate-change-metadata.py --path scripts/test-change-metadata-validator.py --path specs/rigorloop-cli-new-change.md --path specs/rigorloop-cli-new-change.test.md --path docs/plans/2026-05-16-rigorloop-cli-new-change.md --path docs/plan.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml --path docs/changes/2026-05-16-rigorloop-cli-new-change/review-log.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/review-resolution.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/code-review-m2-r1.md`.
  - `git diff --check -- packages/rigorloop scripts/validate-change-metadata.py scripts/test-change-metadata-validator.py specs/rigorloop-cli-new-change.test.md docs/plans/2026-05-16-rigorloop-cli-new-change.md docs/plan.md docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`.

## Diff summary

The M2 implementation remains scoped to `new-change` scaffolding and validator support for generated inline empty YAML collections. The `CR2-F1` resolution changed only the M2 proof surface: `TNC-012` now runs dry-run before actual scaffolding and asserts existing directory actions are reported as `existing`, `change.yaml` remains planned, unrelated files are preserved, and no mutation occurs before actual execution. `TNC-014` now uses table-driven symlink fixtures for `docs`, `docs/changes`, and `docs/changes/<change-id>`, asserting blocked status, exit code `5`, `path-not-directory`, and no writes through the symlink target.

## Findings

No blocking or required-change findings.

## Checklist coverage

| Check | Result | Notes |
|---|---|---|
| Spec alignment | pass | M2 covers `R20-R26`, `R38-R56`, `R57-R70`, and `R71-R76` without creating Markdown placeholders, project manifests, lockfiles, adapters, network access, or readiness claims. |
| Test coverage | pass | `TNC-009` through `TNC-016`, `TNC-020`, and `TNC-021` cover successful scaffolding, dry-run planning, no-overwrite behavior, scoped non-goals, schema validation, and proportional path scope. |
| Edge cases | pass | `TNC-012` directly proves dry-run and actual existing-directory handling; `TNC-013` covers file conflicts at each planned directory; `TNC-014` covers symlink conflicts at each planned directory path. |
| Error handling | pass | Mutation conflicts return blocked/exit `5` in the M2-covered paths. Partial write failure after mutation begins remains explicitly assigned to M3. |
| Architecture boundaries | pass | The implementation stays in the existing CLI package and repository-owned validator scripts, with no new dependency or packaging boundary change. |
| Compatibility | pass | The change metadata validator update accepts inline `{}` and `[]` so generated metadata satisfies the existing schema validator. |
| Security/privacy | pass | Symlink tests prove the command does not write through planned-directory symlinks; generated metadata tests avoid local paths, tokens, and environment data. |
| Derived artifact currency | pass | No generated adapter or skill output is affected by M2. |
| Unrelated changes | pass | The reviewed implementation surface is limited to CLI behavior, package tests, validator support for generated metadata, and lifecycle state. |
| Validation evidence | pass | Package tests, selected CI, review artifact validation, change metadata validation, and diff check are recorded in the active plan and change metadata. |

## No-Finding Rationale

`CR2-F1` is resolved by direct tests at `packages/rigorloop/test/cli.test.js:613` and `packages/rigorloop/test/cli.test.js:673`, which now match the named edge cases in `TNC-012` and `TNC-014`. The production implementation still uses `lstat`-based preflight and deterministic action ordering, and the package-level validation evidence covers both the new tests and the wider existing CLI surface.

## Residual Risks

M3 remains open for partial write failure behavior, output polish, and final command integration. M2 closeout does not imply final plan closeout or PR readiness.

## Recommended next stage

Close M2 and hand off to `implement` for M3.
