# Code Review M2 R1

Review ID: code-review-m2-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: M2 working tree implementation for `rigorloop new-change`
Status: changes-requested

## Scope

Reviewed M2 write-plan, dry-run, and safe metadata scaffolding implementation against the approved `new-change` spec, active test spec, active plan milestone, actual working tree diff, and recorded validation evidence.

## Review inputs

- Diff surface: `packages/rigorloop/dist/bin/rigorloop.js`, `packages/rigorloop/test/cli.test.js`, `scripts/validate-change-metadata.py`, `scripts/test-change-metadata-validator.py`, active plan and change metadata updates.
- Governing spec: `specs/rigorloop-cli-new-change.md`.
- Test spec: `specs/rigorloop-cli-new-change.test.md`.
- Plan milestone: `docs/plans/2026-05-16-rigorloop-cli-new-change.md` M2.
- Architecture: `docs/architecture/system/architecture.md`.
- Validation evidence inspected:
  - `npm test --prefix packages/rigorloop -- --test-name-pattern 'TNC-009|TNC-010|TNC-011|TNC-012|TNC-013|TNC-014|TNC-015|TNC-016|TNC-020|TNC-021'`.
  - `npm test --prefix packages/rigorloop`.
  - `python scripts/test-change-metadata-validator.py`.
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`.
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path scripts/validate-change-metadata.py --path scripts/test-change-metadata-validator.py --path specs/rigorloop-cli-new-change.md --path specs/rigorloop-cli-new-change.test.md --path docs/plans/2026-05-16-rigorloop-cli-new-change.md --path docs/plan.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`.
  - `git diff --check -- packages/rigorloop scripts/validate-change-metadata.py scripts/test-change-metadata-validator.py specs/rigorloop-cli-new-change.test.md docs/plans/2026-05-16-rigorloop-cli-new-change.md docs/plan.md docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`.

## Diff summary

M2 adds real `new-change` filesystem planning and mutation. The CLI now preflights `docs`, `docs/changes`, the change root, and `change.yaml`; reports JSON actions, artifacts, blockers, and minimal-profile warnings; creates directories before writing metadata; blocks existing `change.yaml` and directory path conflicts; preserves existing project files; and keeps `rigorloop.yaml`, `rigorloop.lock`, adapters, and placeholder Markdown files out of scope. Tests now cover successful standard and minimal scaffolding, empty-project dry-run planning, directory file conflicts, a top-level symlink conflict, existing metadata overwrite blocking, generated metadata validation, and scoped path behavior. The change metadata validator also learns inline `{}` and `[]` literals so generated metadata validates against the repository schema.

## Findings

### CR2-F1 - M2 tests do not directly prove all named write-plan edge cases

Finding ID: CR2-F1
Severity: major
Location: `packages/rigorloop/test/cli.test.js:613` and `packages/rigorloop/test/cli.test.js:659`

Evidence: The active test spec requires `TNC-012` to run both dry-run and actual `new-change` for a project with existing `docs/`, `docs/changes`, and an existing change root, then assert existing directories are reported as existing/skipped and unrelated files are preserved (`specs/rigorloop-cli-new-change.test.md:263`). The current test at `packages/rigorloop/test/cli.test.js:613` only runs the actual command, so it does not directly prove the dry-run write plan reports existing directories before mutation.

The test spec also requires `TNC-014` fixtures with a symlink at `docs`, `docs/changes`, or `docs/changes/<change-id>` where supported (`specs/rigorloop-cli-new-change.test.md:291`). The current test at `packages/rigorloop/test/cli.test.js:659` creates only a symlink at `docs`. The code currently loops over all three planned directories, but the code-review contract requires direct proof for named edge cases; code-shape inference alone is not enough for a clean review conclusion.

Required outcome: M2 must have direct test proof that existing directories are reported correctly in dry-run mode and that symlinks at nested planned directory paths block before mutation.

Safe resolution path: Extend the M2 tests to cover dry-run existing-directory planning and add table-driven symlink cases for `docs`, `docs/changes`, and `docs/changes/<change-id>`. Assert `status: blocked`, exit code `5`, blocker code `path-not-directory`, the conflicting path, and no mutation through the symlink target. Rerun `npm test --prefix packages/rigorloop`, the selected M2 CI command, `git diff --check`, then rerun `code-review`.

## Checklist coverage

| Check | Result | Notes |
|---|---|---|
| Spec alignment | concern | The implementation shape matches the M2 write-plan contract in the reviewed paths, but CR2-F1 leaves named edge cases without direct proof. |
| Test coverage | block | CR2-F1: `TNC-012` and `TNC-014` are only partially implemented relative to the active test spec. |
| Edge cases | block | Named dry-run existing-directory and nested symlink cases lack direct proof. |
| Error handling | concern | File conflicts and the tested top-level symlink conflict block with exit `5`; nested symlink proof is missing. M3 still owns partial write failure after mutation begins. |
| Architecture boundaries | pass | M2 stays inside the existing CLI package and repository validator scripts; no new dependency or network surface was introduced. |
| Compatibility | pass | The metadata validator update is scoped to accepting YAML inline empty map/list literals that generated metadata now uses. |
| Security/privacy | concern | Top-level symlink rejection is proved, but nested symlink rejection needs direct proof because symlink handling protects writes outside the intended root. |
| Derived artifact currency | pass | No generated adapter or skill output is affected by this milestone. |
| Unrelated changes | pass | The M2 implementation diff is limited to CLI behavior, package tests, validator support for generated metadata, and lifecycle handoff artifacts. |
| Validation evidence | concern | Recorded validation is relevant and passing, but it does not cover all named M2 edge cases. |

## Recommended next stage

Stop after this isolated code review. Record review-resolution for `CR2-F1`, fix the M2 tests within the approved scope, return M2 to `review-requested`, and rerun `code-review`.
