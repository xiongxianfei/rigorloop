# RigorLoop CLI New Change

- Status: active
- Owner: maintainers
- Start date: 2026-05-16
- Last updated: 2026-05-16
- Related issue or PR: PR #64
- Supersedes: none

## Purpose / big picture

This plan turns the approved `rigorloop new-change` contract into a reviewable implementation path for the existing `@xiongxianfei/rigorloop` package. The command scaffolds draft change-local metadata at `docs/changes/<change-id>/change.yaml` so users do not need to memorize the first-release change metadata shape.

The command is intentionally a scaffold only. It must not create durable Markdown reasoning placeholders, review records, validation claims, PR-readiness claims, project manifests, lockfiles, adapters, or network traffic.

## Source artifacts

- Proposal: `docs/proposals/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow.md`
- Spec: `specs/rigorloop-cli-new-change.md`
- Spec-review: `docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/spec-review-r2.md`
- Architecture: `docs/architecture/system/architecture.md`
- Architecture-review: `docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/architecture-review-r1.md`
- Related CLI package spec: `specs/rigorloop-cli-package-and-codex-init.md`
- Related lockfile spec: `specs/rigorloop-cli-lockfile.md`
- Test spec: `specs/rigorloop-cli-new-change.test.md`

## Context and orientation

- CLI entry point: `packages/rigorloop/dist/bin/rigorloop.js`
- Shared exit-code helper: `packages/rigorloop/dist/lib/command-result.js`
- Existing CLI tests: `packages/rigorloop/test/cli.test.js`
- Package metadata: `packages/rigorloop/package.json`
- Change metadata schema: `schemas/change.schema.json`
- Change metadata validator: `scripts/validate-change-metadata.py`
- Selected CI wrapper: `scripts/ci.sh`

The package currently has no source/build split. Implementation work should edit the tracked `dist/` package files directly unless a later approved plan changes the package layout.

`new-change` should reuse the existing CLI envelope, exit classes, JSON-only stdout rule, and human/quiet/debug/no-color conventions. It should add focused helpers only when they make option validation, metadata generation, write-plan construction, or partial-failure tests clearer.

## Non-goals

- No `rigorloop status`.
- No `rigorloop validate`.
- No adapter install behavior.
- No network access.
- No `rigorloop.yaml` or `rigorloop.lock` writes.
- No `explain-change.md`, review records, review logs, review-resolution, verify reports, proposals, specs, plans, architecture files, ADRs, or PR-body files.
- No `--force`.
- No public npm publication or release hardening.
- No workflow YAML canonicality or generated workflow docs.
- No claim that a scaffolded change has proposal acceptance, review completion, verification, branch readiness, PR readiness, or workflow completion.

## Requirements covered

- R1-R12: command surface, required title, implemented command help, profile and usage handling.
- R13-R19: change-id and safe path rules.
- R20-R26: generated artifact pack boundary and first-slice non-goals.
- R27-R37: deterministic `change.yaml` shape, schema compatibility, YAML safety, and privacy.
- R38-R43: deferred placeholder/template boundary.
- R44-R56k: non-destructive write plan, symlink/overwrite blocking, deterministic mutation order, and partial-failure behavior.
- R57-R70: JSON envelope, exit codes, action/blocker/error shapes, and output modes.
- R71-R76: lifecycle claim boundary, idempotent blocking, no Git/PR inspection, and no `rigorloop.yaml` requirement.

## Current Handoff Summary

- Current milestone: Lifecycle closeout
- Current milestone state: pr-opened
- Last reviewed milestone: M3
- Review status: code-review-m3-r1 clean-with-notes; M3 closed
- Remaining in-scope implementation milestones: none
- Next stage: hosted CI and human review for PR #64
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: implementation milestones are closed, explain-change is recorded, final local verify passed, and PR #64 is open; hosted CI, human review, and merge remain pending.

## Milestones

### M1. Command contract helpers and metadata generation

- Milestone state: closed
- Goal: Add the pure `new-change` contract layer without filesystem mutation.
- Requirements: R1-R12, R13-R19, R27-R37, R57-R70, R71-R76
- Files/components likely touched:
  - `packages/rigorloop/dist/bin/rigorloop.js`
  - optional `packages/rigorloop/dist/lib/new-change.js`
  - `packages/rigorloop/test/cli.test.js`
- Dependencies:
  - Approved spec and architecture.
  - Plan-review approval.
  - Matching test spec approval.
- Tests to add/update:
  - `rigorloop --help` includes `new-change` only after implementation.
  - Missing `<change-id>` returns exit `4` with `missing-change-id`.
  - Missing `--title` returns exit `4` with `missing-title`.
  - Valid and invalid change IDs.
  - Valid and invalid `--type` values, including uppercase, whitespace, path separators, URL-encoded path separators, control characters, and over-length values.
  - Valid and invalid `--risk` values.
  - Unsupported profile returns exit `4`.
  - Generated metadata content uses deterministic field order, empty arrays/maps, `review.status: pending`, and no artifact readiness claims.
  - YAML scalar escaping preserves document shape for titles with punctuation or quotes.
- Implementation steps:
  - Extend argument parsing or command dispatch for `new-change`.
  - Add validation helpers for change ID, classification, risk, profile, title, and unsupported options.
  - Add deterministic `change.yaml` content generation.
  - Add JSON result construction for invalid usage and pure dry-run planning inputs.
  - Keep all helper behavior local to the package; do not introduce dependencies unless a later approved artifact authorizes them.
- Validation commands:
  - `npm test --prefix packages/rigorloop`
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path specs/rigorloop-cli-new-change.md --path specs/rigorloop-cli-new-change.test.md --path docs/plans/2026-05-16-rigorloop-cli-new-change.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`
  - `git diff --check -- packages/rigorloop specs/rigorloop-cli-new-change.test.md docs/plans/2026-05-16-rigorloop-cli-new-change.md docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`
- Expected observable result: Invalid command usage is deterministic, pure metadata generation is test-covered, and no filesystem mutation behavior is claimed complete yet.
- Commit message: `M1: add new-change command contract helpers`
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [ ] milestone committed
- Risks:
  - Option parsing may conflict with existing `init` flags.
  - YAML escaping could be under-specified by tests if only simple titles are covered.
- Rollback/recovery:
  - Revert the `new-change` command dispatch and helper tests without touching existing `init` behavior.

Code-review handoff:

- `code-review-m1-r1` status: changes-requested.
- Resolved finding: `CR1-F1` - generated metadata now includes required `review.unresolved_items: 0`.
- `code-review-m1-r2` status: clean-with-notes.
- Required next action: implement M2.

### M2. Write plan, dry-run, and safe metadata scaffolding

- Milestone state: closed
- Goal: Implement complete write-plan reporting and successful dry-run/actual `change.yaml` scaffolding.
- Requirements: R20-R26, R38-R56, R57-R70, R71-R76
- Files/components likely touched:
  - `packages/rigorloop/dist/bin/rigorloop.js`
  - optional `packages/rigorloop/dist/lib/new-change.js`
  - `packages/rigorloop/test/cli.test.js`
  - `scripts/validate-change-metadata.py`
  - `scripts/test-change-metadata-validator.py`
- Dependencies:
  - M1 closed.
- Tests to add/update:
  - Dry-run JSON reports `docs`, `docs/changes`, `docs/changes/<change-id>`, and `docs/changes/<change-id>/change.yaml` in deterministic order and writes nothing.
  - Existing required directories are reported as existing/skipped.
  - Actual standard profile creates only `change.yaml`.
  - Actual minimal profile creates only `change.yaml` and returns warning `durable-reasoning-not-scaffolded`.
  - `artifacts` is empty for both profiles.
  - `explain-change.md` is never planned or created.
  - Existing `change.yaml` blocks with exit `5`.
  - `docs`, `docs/changes`, and change root file conflicts block with exit `5`.
  - Symlink at any planned directory path blocks with exit `5` and `path-not-directory`.
  - Existing `rigorloop.yaml` is not required.
  - `rigorloop.yaml` and `rigorloop.lock` are not written or modified.
  - No network fetch is attempted.
- Implementation steps:
  - Build path-plan helpers that use `lstat` semantics for symlink detection.
  - Apply directory actions before file actions and only after all preflight blockers are known.
  - Keep action statuses consistent between dry-run and actual mutation.
  - Write UTF-8 LF `change.yaml`.
  - Ensure successful human and JSON output name the change root and metadata path.
- Validation commands:
  - `npm test --prefix packages/rigorloop`
  - `python scripts/validate-change-metadata.py <fixture-created-change-yaml>` when a stable fixture path is available from tests or a manual temp smoke run.
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path specs/rigorloop-cli-new-change.md --path specs/rigorloop-cli-new-change.test.md --path docs/plans/2026-05-16-rigorloop-cli-new-change.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`
  - `git diff --check -- packages/rigorloop specs/rigorloop-cli-new-change.test.md docs/plans/2026-05-16-rigorloop-cli-new-change.md docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`
- Expected observable result: Users can run `rigorloop new-change <change-id> --title <title>` safely, with complete dry-run output and non-destructive actual scaffolding.
- Commit message: `M2: implement safe new-change scaffolding`
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [ ] milestone committed
- Risks:
  - Recursive directory creation could hide unplanned parent mutations.
  - Symlink handling can be wrong if implementation relies only on `stat`.
  - Existing `init` tests may be disturbed by shared parser changes.
- Rollback/recovery:
  - Keep `new-change` changes isolated from existing `init` functions so the command can be disabled without reverting lockfile or adapter behavior.

Code-review handoff:

- `code-review-m2-r1` status: changes-requested.
- Resolved finding: `CR2-F1` - M2 tests now directly prove dry-run existing-directory planning and nested planned-directory symlink conflicts.
- `code-review-m2-r2` status: clean-with-notes.
- Required next action: implement M3.

### M3. Partial failure behavior, output polish, and final integration

- Milestone state: closed
- Goal: Prove the observable non-atomic partial-failure contract and finish command integration.
- Requirements: R56a-R56k, R57-R70, R71-R76
- Files/components likely touched:
  - `packages/rigorloop/dist/bin/rigorloop.js`
  - optional `packages/rigorloop/dist/lib/new-change.js`
  - `packages/rigorloop/test/cli.test.js`
  - `packages/rigorloop/README.md` only if existing package docs advertise command surfaces
- Dependencies:
  - M2 closed.
- Tests to add/update:
  - Unit-level or helper-level partial write failure test where directory actions complete and `change.yaml` write fails; JSON actions mark completed directories `done`, file action `failed`, status `error`, exit `1`, and no success claim.
  - Human output remains concise and does not emit JSON fragments.
  - `--quiet`, `--debug`, `--no-color`, and `NO_COLOR` behavior matches the existing CLI contract for `new-change`.
  - Unknown options remain invalid usage and do not mutate.
  - Existing `init`, lockfile, and archive tests remain green.
- Implementation steps:
  - If needed, factor mutation execution behind package-local helper seams so partial failure can be tested deterministically without public environment overrides.
  - Map classified write failures through `exit_class: internal` unless the failure was classified before writing as mutation conflict.
  - Ensure all result paths use `exitCodeForResult`.
  - Update package README help examples only if stale after command implementation.
  - Update active plan progress and validation notes before code-review handoff.
- Validation commands:
  - `npm test --prefix packages/rigorloop`
  - `python scripts/test-select-validation.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path packages/rigorloop --path specs/rigorloop-cli-new-change.md --path specs/rigorloop-cli-new-change.test.md --path docs/plans/2026-05-16-rigorloop-cli-new-change.md --path docs/plan.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path specs/rigorloop-cli-new-change.md --path specs/rigorloop-cli-new-change.test.md --path docs/plans/2026-05-16-rigorloop-cli-new-change.md --path docs/plan.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`
  - `git diff --check -- packages/rigorloop specs/rigorloop-cli-new-change.test.md docs/plans/2026-05-16-rigorloop-cli-new-change.md docs/plan.md docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`
- Expected observable result: The full `new-change` first slice is implemented, test-covered, and ready for milestone code-review.
- Commit message: `M3: finish new-change failure handling`
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [ ] milestone committed
- Risks:
  - Partial-failure tests can become flaky if they depend on operating-system permissions. Prefer helper-level deterministic failure injection rather than chmod-only tests.
  - Output polish can accidentally broaden claims beyond scaffolding. Keep wording tied to planned or created metadata only.
- Rollback/recovery:
  - Revert M3 helper seam and final output polish while preserving M1/M2 behavior if final edge-case proof exposes a design issue.

Code-review handoff:

- M3 implementation status: review-requested.
- Partial write failure is covered by package-local helper seam `runNewChangePlan`.
- Output mode coverage added for human, `--json --quiet`, `--json --debug`, `--no-color`, `NO_COLOR`, and unknown-option no-mutation behavior.
- `code-review-m3-r1` status: clean-with-notes.
- Required next action: run explain-change.

### Lifecycle closeout

- Milestone state: in-progress
- Goal: Complete downstream non-implementation gates after all implementation milestones close.
- Requirements: all requirements named above, plus workflow closeout requirements.
- Files/components likely touched:
  - `docs/plans/2026-05-16-rigorloop-cli-new-change.md`
  - `docs/plan.md`
  - `docs/changes/2026-05-16-rigorloop-cli-new-change/explain-change.md`
  - PR handoff text
- Dependencies:
  - M1, M2, and M3 closed.
  - Code-review completed with no open findings.
- Tests to add/update:
  - None; this is downstream validation and handoff only.
- Implementation steps:
  - Run `explain-change`.
  - Run `verify`.
  - Prepare PR handoff.
  - Update plan lifecycle state only when the corresponding evidence exists.
- Validation commands:
  - Commands required by `verify` and the active test spec.
- Expected observable result: The branch has durable rationale, final verification evidence, synchronized plan state, and PR-ready handoff.
- Commit message: `closeout: prepare new-change PR handoff`
- Milestone closeout:
  - [x] final validation passed
  - [x] plan state synchronized
  - [x] explain-change recorded
  - [x] verify evidence recorded
  - [ ] PR handoff prepared
- Risks:
  - Plan state could be marked done before downstream gates complete.
- Rollback/recovery:
  - Keep plan active until the missing closeout evidence is produced.

## Validation plan

Before implementation:

- `python scripts/validate-change-metadata.py docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`
- `python scripts/validate-review-artifacts.py docs/changes/2026-05-16-rigorloop-cli-new-change`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/rigorloop-cli-new-change.md --path docs/architecture/system/architecture.md --path docs/architecture/system/diagrams/container.mmd --path docs/plans/2026-05-16-rigorloop-cli-new-change.md --path docs/plan.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml --path docs/changes/2026-05-16-rigorloop-cli-new-change/review-log.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/review-resolution.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/spec-review-r1.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/spec-review-r2.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/architecture-review-r1.md`
- `bash scripts/ci.sh --mode explicit --path specs/rigorloop-cli-new-change.md --path docs/architecture/system/architecture.md --path docs/architecture/system/diagrams/container.mmd --path docs/follow-ups.md --path docs/plan.md --path docs/plans/2026-05-16-rigorloop-cli-lockfile.md --path docs/plans/2026-05-16-rigorloop-cli-new-change.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml --path docs/changes/2026-05-16-rigorloop-cli-new-change/review-log.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/review-resolution.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/spec-review-r1.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/spec-review-r2.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/architecture-review-r1.md`
- `git diff --check -- specs/rigorloop-cli-new-change.md docs/architecture/system/architecture.md docs/architecture/system/diagrams/container.mmd docs/follow-ups.md docs/plan.md docs/plans/2026-05-16-rigorloop-cli-lockfile.md docs/plans/2026-05-16-rigorloop-cli-new-change.md docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml docs/changes/2026-05-16-rigorloop-cli-new-change/review-log.md docs/changes/2026-05-16-rigorloop-cli-new-change/review-resolution.md docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/spec-review-r1.md docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/spec-review-r2.md docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/architecture-review-r1.md`

During implementation, each milestone runs `npm test --prefix packages/rigorloop` first, then the selected CI command for the touched paths. Final verification repeats the broader selected CI and any test-spec-required command.

## Risks and recovery

- Hidden mutation risk: write-plan actions must name every directory and file before mutation. Recovery is to block or revert the command slice before broadening behavior.
- Lifecycle claim risk: generated metadata must leave evidence arrays empty and omit `explain-change.md`. Recovery is to remove placeholder files or artifact mappings and rerun tests.
- Partial write risk: first slice does not promise rollback. Recovery is to report completed and failed actions, keep wording honest, and leave repair commands for a later spec.
- Parser coupling risk: shared flag parsing for `init` and `new-change` can regress existing commands. Recovery is to isolate `new-change` parsing helpers and keep all existing CLI tests green.
- Test reliability risk: permission-based partial-failure tests can be platform-sensitive. Recovery is to use helper-level deterministic failure injection.

## Dependencies

- `plan-review` must approve this plan before test-spec.
- `test-spec` must be created and approved before implementation.
- Existing CLI init and lockfile behavior must remain green.
- No new npm dependency is planned.
- Public npm publication remains out of scope.

## Progress

- [x] 2026-05-16: Spec approved by `spec-review-r2`.
- [x] 2026-05-16: Canonical architecture update approved by `architecture-review-r1`.
- [x] 2026-05-16: Execution plan created.
- [x] 2026-05-16: Plan-review completed with no material findings.
- [x] 2026-05-16: Test spec created and activated.
- [x] 2026-05-16: M1 implemented and handed to code-review.
- [x] 2026-05-16: M1 code-review found `CR1-F1`; milestone moved to resolution-needed.
- [x] 2026-05-16: M1 review-resolution completed for `CR1-F1`; milestone returned to code-review.
- [x] 2026-05-16: M1 code-review rerun closed with `clean-with-notes`.
- [x] 2026-05-16: M2 implemented and handed to code-review.
- [x] 2026-05-16: M2 code-review found `CR2-F1`; milestone moved to resolution-needed.
- [x] 2026-05-16: M2 review-resolution completed for `CR2-F1`; milestone returned to code-review.
- [x] 2026-05-16: M2 code-review rerun closed with `clean-with-notes`.
- [x] 2026-05-16: M3 implemented and handed to code-review.
- [x] 2026-05-16: M3 code-review closed with `clean-with-notes`.
- [x] 2026-05-16: Explain-change recorded.
- [x] 2026-05-16: Verify passed; branch-ready for PR handoff.
- [x] 2026-05-16: PR #64 opened for review.

## Decision log

- 2026-05-16: Split implementation into three milestones so pure command validation, filesystem mutation safety, and partial-failure proof can be reviewed separately.
- 2026-05-16: Keep implementation inside the existing package candidate and edit tracked `dist/` files directly because the package currently has no source/build split.
- 2026-05-16: Prefer helper-level deterministic partial-failure tests over permission-dependent filesystem tests.
- 2026-05-16: Implement M1 with a package-local `new-change` helper module for validation and metadata rendering, keeping actual filesystem mutation blocked until M2.
- 2026-05-16: Keep the approved inline `artifacts: {}` and empty-array `[]` generated metadata shape, and update the repository validator parser to recognize those YAML literals so generated metadata satisfies the existing schema validator.
- 2026-05-16: For M3, factor new-change filesystem planning/application into `dist/lib/new-change-filesystem.js` so partial write failures can be tested deterministically without public runtime overrides or permission-dependent tests.
- 2026-05-16: Leave `packages/rigorloop/README.md` unchanged because it is generic package-candidate text and does not advertise command examples that became stale after `new-change`.

## Surprises and discoveries

- 2026-05-16: Existing fixture-package tests copy individual `dist/lib` helper files, so `new-change.js` must be copied into fixture packages to keep existing init tests green.
- 2026-05-16: The change metadata validator previously treated inline `{}` and `[]` as strings, so M2 added parser support and regression coverage for those literals.
- 2026-05-16: M2 code-review found a direct-proof coverage gap for dry-run existing-directory planning and nested planned-directory symlink conflicts.
- 2026-05-16: `CR2-F1` required test-only changes; the existing implementation already handled the newly covered dry-run and nested symlink cases.
- 2026-05-16: The M3 helper seam did not require changing the public command contract; it only made the mutation path directly testable.

## Validation notes

- 2026-05-16: Plan authoring validation passed:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-16-rigorloop-cli-new-change`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/rigorloop-cli-new-change.md --path docs/architecture/system/architecture.md --path docs/architecture/system/diagrams/container.mmd --path docs/plans/2026-05-16-rigorloop-cli-new-change.md --path docs/plan.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml --path docs/changes/2026-05-16-rigorloop-cli-new-change/review-log.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/review-resolution.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/spec-review-r1.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/spec-review-r2.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/architecture-review-r1.md`
  - `bash scripts/ci.sh --mode explicit --path specs/rigorloop-cli-new-change.md --path docs/architecture/system/architecture.md --path docs/architecture/system/diagrams/container.mmd --path docs/follow-ups.md --path docs/plan.md --path docs/plans/2026-05-16-rigorloop-cli-lockfile.md --path docs/plans/2026-05-16-rigorloop-cli-new-change.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml --path docs/changes/2026-05-16-rigorloop-cli-new-change/review-log.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/review-resolution.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/spec-review-r1.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/spec-review-r2.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/architecture-review-r1.md`
  - `git diff --check -- specs/rigorloop-cli-new-change.md docs/architecture/system/architecture.md docs/architecture/system/diagrams/container.mmd docs/follow-ups.md docs/plan.md docs/plans/2026-05-16-rigorloop-cli-lockfile.md docs/plans/2026-05-16-rigorloop-cli-new-change.md docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml docs/changes/2026-05-16-rigorloop-cli-new-change/review-log.md docs/changes/2026-05-16-rigorloop-cli-new-change/review-resolution.md docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/spec-review-r1.md docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/spec-review-r2.md docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/architecture-review-r1.md`
- 2026-05-16: Test-spec authoring validation passed:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-16-rigorloop-cli-new-change`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/rigorloop-cli-new-change.md --path specs/rigorloop-cli-new-change.test.md --path docs/architecture/system/architecture.md --path docs/architecture/system/diagrams/container.mmd --path docs/plans/2026-05-16-rigorloop-cli-new-change.md --path docs/plan.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml --path docs/changes/2026-05-16-rigorloop-cli-new-change/review-log.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/review-resolution.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/spec-review-r1.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/spec-review-r2.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/architecture-review-r1.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/plan-review-r1.md`
  - `bash scripts/ci.sh --mode explicit --path specs/rigorloop-cli-new-change.md --path specs/rigorloop-cli-new-change.test.md --path docs/architecture/system/architecture.md --path docs/architecture/system/diagrams/container.mmd --path docs/follow-ups.md --path docs/plan.md --path docs/plans/2026-05-16-rigorloop-cli-lockfile.md --path docs/plans/2026-05-16-rigorloop-cli-new-change.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml --path docs/changes/2026-05-16-rigorloop-cli-new-change/review-log.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/review-resolution.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/spec-review-r1.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/spec-review-r2.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/architecture-review-r1.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/plan-review-r1.md`
  - `git diff --check -- specs/rigorloop-cli-new-change.md specs/rigorloop-cli-new-change.test.md docs/architecture/system/architecture.md docs/architecture/system/diagrams/container.mmd docs/follow-ups.md docs/plan.md docs/plans/2026-05-16-rigorloop-cli-lockfile.md docs/plans/2026-05-16-rigorloop-cli-new-change.md docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml docs/changes/2026-05-16-rigorloop-cli-new-change/review-log.md docs/changes/2026-05-16-rigorloop-cli-new-change/review-resolution.md docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/spec-review-r1.md docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/spec-review-r2.md docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/architecture-review-r1.md docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/plan-review-r1.md`
- 2026-05-16: M1 tests-first proof failed for the expected reason before implementation:
  - `npm test --prefix packages/rigorloop -- --test-name-pattern 'TNC|T2'` failed with `ERR_MODULE_NOT_FOUND` for `dist/lib/new-change.js`.
- 2026-05-16: M1 package validation passed after implementation:
  - `npm test --prefix packages/rigorloop -- --test-name-pattern 'TNC-00|T2 help'`
  - `npm test --prefix packages/rigorloop`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path specs/rigorloop-cli-new-change.md --path specs/rigorloop-cli-new-change.test.md --path docs/plans/2026-05-16-rigorloop-cli-new-change.md --path docs/plan.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`
  - `git diff --check -- packages/rigorloop specs/rigorloop-cli-new-change.test.md docs/plans/2026-05-16-rigorloop-cli-new-change.md docs/plan.md docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`
- 2026-05-16: M1 code-review recorded `code-review-m1-r1` with `CR1-F1`; review recording validation passed:
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-16-rigorloop-cli-new-change`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path packages/rigorloop --path specs/rigorloop-cli-new-change.md --path specs/rigorloop-cli-new-change.test.md --path docs/plans/2026-05-16-rigorloop-cli-new-change.md --path docs/plan.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml --path docs/changes/2026-05-16-rigorloop-cli-new-change/review-log.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/review-resolution.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/code-review-m1-r1.md`
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path specs/rigorloop-cli-new-change.md --path specs/rigorloop-cli-new-change.test.md --path docs/plans/2026-05-16-rigorloop-cli-new-change.md --path docs/plan.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml --path docs/changes/2026-05-16-rigorloop-cli-new-change/review-log.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/review-resolution.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/code-review-m1-r1.md`
  - `git diff --check -- packages/rigorloop specs/rigorloop-cli-new-change.test.md docs/plans/2026-05-16-rigorloop-cli-new-change.md docs/plan.md docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml docs/changes/2026-05-16-rigorloop-cli-new-change/review-log.md docs/changes/2026-05-16-rigorloop-cli-new-change/review-resolution.md docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/code-review-m1-r1.md`
- 2026-05-16: `CR1-F1` fix was test-first:
  - `npm test --prefix packages/rigorloop -- --test-name-pattern 'TNC-006'` failed before the renderer fix because `review.unresolved_items: 0` was missing.
  - `npm test --prefix packages/rigorloop -- --test-name-pattern 'TNC-006'` passed after the renderer fix.
- 2026-05-16: `CR1-F1` fix validation passed:
  - `npm test --prefix packages/rigorloop`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-16-rigorloop-cli-new-change`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path specs/rigorloop-cli-new-change.md --path specs/rigorloop-cli-new-change.test.md --path docs/plans/2026-05-16-rigorloop-cli-new-change.md --path docs/plan.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`
  - `git diff --check -- packages/rigorloop specs/rigorloop-cli-new-change.test.md docs/plans/2026-05-16-rigorloop-cli-new-change.md docs/plan.md docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`
- 2026-05-16: M1 code-review rerun recorded `code-review-m1-r2` with `clean-with-notes`; no material findings.
- 2026-05-16: M2 tests-first proof failed for the expected reason before implementation:
  - `npm test --prefix packages/rigorloop -- --test-name-pattern 'TNC-009|TNC-010|TNC-011|TNC-012|TNC-013|TNC-014|TNC-015|TNC-016|TNC-020|TNC-021'` failed because non-dry-run still blocked and dry-run did not report actions.
  - `python scripts/test-change-metadata-validator.py` failed after adding inline-empty-collection regression coverage because the validator parsed `{}` and `[]` as strings.
- 2026-05-16: M2 validation passed:
  - `npm test --prefix packages/rigorloop -- --test-name-pattern 'TNC-009|TNC-010|TNC-011|TNC-012|TNC-013|TNC-014|TNC-015|TNC-016|TNC-020|TNC-021'`
  - `npm test --prefix packages/rigorloop`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path scripts/validate-change-metadata.py --path scripts/test-change-metadata-validator.py --path specs/rigorloop-cli-new-change.md --path specs/rigorloop-cli-new-change.test.md --path docs/plans/2026-05-16-rigorloop-cli-new-change.md --path docs/plan.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`
  - `git diff --check -- packages/rigorloop scripts/validate-change-metadata.py scripts/test-change-metadata-validator.py specs/rigorloop-cli-new-change.test.md docs/plans/2026-05-16-rigorloop-cli-new-change.md docs/plan.md docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`
- 2026-05-16: Final CR2-F1 state-sync selected CI passed after recording the review-resolution and handoff state:
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path scripts/validate-change-metadata.py --path scripts/test-change-metadata-validator.py --path specs/rigorloop-cli-new-change.md --path specs/rigorloop-cli-new-change.test.md --path docs/plans/2026-05-16-rigorloop-cli-new-change.md --path docs/plan.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml --path docs/changes/2026-05-16-rigorloop-cli-new-change/review-log.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/review-resolution.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/code-review-m2-r1.md`
- 2026-05-16: M2 code-review rerun recorded `code-review-m2-r2` with `clean-with-notes`; validation passed before recording:
  - `npm test --prefix packages/rigorloop`
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path scripts/validate-change-metadata.py --path scripts/test-change-metadata-validator.py --path specs/rigorloop-cli-new-change.md --path specs/rigorloop-cli-new-change.test.md --path docs/plans/2026-05-16-rigorloop-cli-new-change.md --path docs/plan.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml --path docs/changes/2026-05-16-rigorloop-cli-new-change/review-log.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/review-resolution.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/code-review-m2-r1.md`
- 2026-05-16: M2 code-review rerun recording validation passed:
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-16-rigorloop-cli-new-change`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path scripts/validate-change-metadata.py --path scripts/test-change-metadata-validator.py --path specs/rigorloop-cli-new-change.md --path specs/rigorloop-cli-new-change.test.md --path docs/plans/2026-05-16-rigorloop-cli-new-change.md --path docs/plan.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml --path docs/changes/2026-05-16-rigorloop-cli-new-change/review-log.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/review-resolution.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/code-review-m2-r2.md`
- 2026-05-16: M3 tests-first proof failed for the expected reason before implementation:
  - `npm test --prefix packages/rigorloop -- --test-name-pattern 'TNC-017|TNC-018|TNC-019'` failed with `ERR_MODULE_NOT_FOUND` for `dist/lib/new-change-filesystem.js`.
- 2026-05-16: M3 package validation passed after implementation:
  - `npm test --prefix packages/rigorloop -- --test-name-pattern 'TNC-017|TNC-018|TNC-019'`
  - `npm test --prefix packages/rigorloop`
- 2026-05-16: M3 selected validation passed:
  - `python scripts/test-select-validation.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path packages/rigorloop --path specs/rigorloop-cli-new-change.md --path specs/rigorloop-cli-new-change.test.md --path docs/plans/2026-05-16-rigorloop-cli-new-change.md --path docs/plan.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path specs/rigorloop-cli-new-change.md --path specs/rigorloop-cli-new-change.test.md --path docs/plans/2026-05-16-rigorloop-cli-new-change.md --path docs/plan.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`
  - `git diff --check -- packages/rigorloop specs/rigorloop-cli-new-change.test.md docs/plans/2026-05-16-rigorloop-cli-new-change.md docs/plan.md docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`
- 2026-05-16: M3 code-review recorded `code-review-m3-r1` with `clean-with-notes`; recording validation passed:
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-16-rigorloop-cli-new-change`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path specs/rigorloop-cli-new-change.md --path specs/rigorloop-cli-new-change.test.md --path docs/plans/2026-05-16-rigorloop-cli-new-change.md --path docs/plan.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml --path docs/changes/2026-05-16-rigorloop-cli-new-change/review-log.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/review-resolution.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/code-review-m3-r1.md`
  - `git diff --check -- packages/rigorloop specs/rigorloop-cli-new-change.test.md docs/plans/2026-05-16-rigorloop-cli-new-change.md docs/plan.md docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml docs/changes/2026-05-16-rigorloop-cli-new-change/review-log.md docs/changes/2026-05-16-rigorloop-cli-new-change/review-resolution.md docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/code-review-m3-r1.md`
- 2026-05-16: explain-change recorded the durable rationale for the `new-change` implementation. The next stage is verify.
- 2026-05-16: explain-change recording validation passed:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-16-rigorloop-cli-new-change`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path packages/rigorloop --path specs/rigorloop-cli-new-change.md --path specs/rigorloop-cli-new-change.test.md --path docs/follow-ups.md --path docs/plans/2026-05-16-rigorloop-cli-new-change.md --path docs/plan.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml --path docs/changes/2026-05-16-rigorloop-cli-new-change/explain-change.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/review-log.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/review-resolution.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/code-review-m3-r1.md`
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path scripts/validate-change-metadata.py --path scripts/test-change-metadata-validator.py --path specs/rigorloop-cli-new-change.md --path specs/rigorloop-cli-new-change.test.md --path docs/architecture/system/architecture.md --path docs/architecture/system/diagrams/container.mmd --path docs/follow-ups.md --path docs/plan.md --path docs/plans/2026-05-16-rigorloop-cli-lockfile.md --path docs/plans/2026-05-16-rigorloop-cli-new-change.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml --path docs/changes/2026-05-16-rigorloop-cli-new-change/explain-change.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/review-log.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/review-resolution.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/code-review-m3-r1.md`
  - `git diff --check -- packages/rigorloop scripts/validate-change-metadata.py scripts/test-change-metadata-validator.py specs/rigorloop-cli-new-change.md specs/rigorloop-cli-new-change.test.md docs/architecture/system/architecture.md docs/architecture/system/diagrams/container.mmd docs/follow-ups.md docs/plan.md docs/plans/2026-05-16-rigorloop-cli-lockfile.md docs/plans/2026-05-16-rigorloop-cli-new-change.md docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml docs/changes/2026-05-16-rigorloop-cli-new-change/explain-change.md docs/changes/2026-05-16-rigorloop-cli-new-change/review-log.md docs/changes/2026-05-16-rigorloop-cli-new-change/review-resolution.md docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/code-review-m3-r1.md`
- 2026-05-16: final local verify passed and established branch-ready for PR handoff:
  - `npm test --prefix packages/rigorloop`
  - `python scripts/test-select-validation.py`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-16-rigorloop-cli-new-change`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path packages/rigorloop --path scripts/validate-change-metadata.py --path scripts/test-change-metadata-validator.py --path specs/rigorloop-cli-new-change.md --path specs/rigorloop-cli-new-change.test.md --path docs/architecture/system/architecture.md --path docs/architecture/system/diagrams/container.mmd --path docs/follow-ups.md --path docs/plan.md --path docs/plans/2026-05-16-rigorloop-cli-lockfile.md --path docs/plans/2026-05-16-rigorloop-cli-new-change.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml --path docs/changes/2026-05-16-rigorloop-cli-new-change/explain-change.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/review-log.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/review-resolution.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/spec-review-r1.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/spec-review-r2.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/architecture-review-r1.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/plan-review-r1.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/code-review-m1-r1.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/code-review-m1-r2.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/code-review-m2-r1.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/code-review-m2-r2.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/code-review-m3-r1.md`
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path scripts/validate-change-metadata.py --path scripts/test-change-metadata-validator.py --path specs/rigorloop-cli-new-change.md --path specs/rigorloop-cli-new-change.test.md --path docs/architecture/system/architecture.md --path docs/architecture/system/diagrams/container.mmd --path docs/follow-ups.md --path docs/plan.md --path docs/plans/2026-05-16-rigorloop-cli-lockfile.md --path docs/plans/2026-05-16-rigorloop-cli-new-change.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml --path docs/changes/2026-05-16-rigorloop-cli-new-change/explain-change.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/review-log.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/review-resolution.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/spec-review-r1.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/spec-review-r2.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/architecture-review-r1.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/plan-review-r1.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/code-review-m1-r1.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/code-review-m1-r2.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/code-review-m2-r1.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/code-review-m2-r2.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/code-review-m3-r1.md --broad-smoke`
  - `git diff --check -- packages/rigorloop scripts/validate-change-metadata.py scripts/test-change-metadata-validator.py specs/rigorloop-cli-new-change.md specs/rigorloop-cli-new-change.test.md docs/architecture/system/architecture.md docs/architecture/system/diagrams/container.mmd docs/follow-ups.md docs/plan.md docs/plans/2026-05-16-rigorloop-cli-lockfile.md docs/plans/2026-05-16-rigorloop-cli-new-change.md docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml docs/changes/2026-05-16-rigorloop-cli-new-change/explain-change.md docs/changes/2026-05-16-rigorloop-cli-new-change/review-log.md docs/changes/2026-05-16-rigorloop-cli-new-change/review-resolution.md docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/spec-review-r1.md docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/spec-review-r2.md docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/architecture-review-r1.md docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/plan-review-r1.md docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/code-review-m1-r1.md docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/code-review-m1-r2.md docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/code-review-m2-r1.md docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/code-review-m2-r2.md docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/code-review-m3-r1.md`
- 2026-05-16: PR #64 opened for review; hosted CI and human review are pending.
- 2026-05-16: M2 code-review recorded `code-review-m2-r1` with `CR2-F1`; review recording validation passed:
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-16-rigorloop-cli-new-change`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path packages/rigorloop --path scripts/validate-change-metadata.py --path scripts/test-change-metadata-validator.py --path specs/rigorloop-cli-new-change.md --path specs/rigorloop-cli-new-change.test.md --path docs/plans/2026-05-16-rigorloop-cli-new-change.md --path docs/plan.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml --path docs/changes/2026-05-16-rigorloop-cli-new-change/review-log.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/review-resolution.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/code-review-m2-r1.md`
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path scripts/validate-change-metadata.py --path scripts/test-change-metadata-validator.py --path specs/rigorloop-cli-new-change.md --path specs/rigorloop-cli-new-change.test.md --path docs/plans/2026-05-16-rigorloop-cli-new-change.md --path docs/plan.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml --path docs/changes/2026-05-16-rigorloop-cli-new-change/review-log.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/review-resolution.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/code-review-m2-r1.md`
  - `git diff --check -- packages/rigorloop scripts/validate-change-metadata.py scripts/test-change-metadata-validator.py specs/rigorloop-cli-new-change.test.md docs/plans/2026-05-16-rigorloop-cli-new-change.md docs/plan.md docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml docs/changes/2026-05-16-rigorloop-cli-new-change/review-log.md docs/changes/2026-05-16-rigorloop-cli-new-change/review-resolution.md docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/code-review-m2-r1.md`
- 2026-05-16: `CR2-F1` resolution validation passed:
  - `npm test --prefix packages/rigorloop -- --test-name-pattern 'TNC-012|TNC-014'`
  - `npm test --prefix packages/rigorloop`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-16-rigorloop-cli-new-change`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path scripts/validate-change-metadata.py --path scripts/test-change-metadata-validator.py --path specs/rigorloop-cli-new-change.md --path specs/rigorloop-cli-new-change.test.md --path docs/plans/2026-05-16-rigorloop-cli-new-change.md --path docs/plan.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`
  - `git diff --check -- packages/rigorloop scripts/validate-change-metadata.py scripts/test-change-metadata-validator.py specs/rigorloop-cli-new-change.test.md docs/plans/2026-05-16-rigorloop-cli-new-change.md docs/plan.md docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`

## Outcome and retrospective

- Implementation milestones are closed, durable change rationale is recorded, final local verify passed, and PR #64 is open. Hosted CI, human review, and merge remain pending.

## Readiness

- See `Current Handoff Summary`.
- This plan is active with PR #64 open. It is not final closeout until hosted CI, human review, and merge complete.
