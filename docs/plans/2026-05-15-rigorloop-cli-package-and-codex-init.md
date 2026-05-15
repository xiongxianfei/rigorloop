# RigorLoop CLI package and Codex init

- Status: active
- Owner: maintainers
- Start date: 2026-05-15
- Last updated: 2026-05-15
- Related issue or PR: PR #62 (`https://github.com/xiongxianfei/rigorloop/pull/62`)
- Supersedes: none

## Purpose / big picture

This plan turns the approved first-slice CLI contract into reviewable implementation milestones. The slice creates the `@xiongxianfei/rigorloop` package candidate, exposes the `rigorloop` binary, supports help/version, and implements `init --adapter codex` with non-destructive scaffolding, verified Codex release archive installation, stable JSON output, and planned lockfile content only.

The plan intentionally does not implement the broader CLI roadmap. It keeps the CLI as a facade and installer while repository-owned specs, skills, schemas, scripts, templates, release archives, and metadata remain the canonical sources.

## Source artifacts

- Proposal: `docs/proposals/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow.md`
- Spec: `specs/rigorloop-cli-package-and-codex-init.md`
- Architecture: `docs/architecture/system/architecture.md`
- ADR: `docs/adr/ADR-20260515-rigorloop-cli-package-and-codex-init.md`
- Test spec: `specs/rigorloop-cli-package-and-codex-init.test.md`
- Review evidence: `docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-log.md`

## Context and orientation

- There is no existing root `package.json`; the CLI package is a new package boundary, expected under `packages/rigorloop/` unless implementation discovers a better repository-local convention before code is written.
- Existing repository validation is Python and shell driven under `scripts/`; this slice does not port repository validators or add `rigorloop validate`.
- Public adapter bodies are release archives for `v0.1.3` and later. The CLI installs Codex from verified release archives and never from `.codex/skills`.
- The first package may include CLI code, small scaffold templates, and bundled official metadata for the compatible Codex adapter release. It must not bundle adapter archives as authored npm source.
- Actual public npm publication is out of scope until a separate release-hardening artifact is accepted.
- The active plan body owns live milestone state for this planned initiative; `docs/plan.md` is only the lifecycle index.

## Non-goals

- No `rigorloop new-change`, `rigorloop status`, or `rigorloop validate`.
- No durable `rigorloop.lock` writes.
- No workflow YAML canonicality, workflow rendering, generated workflow docs, or frozen drift checks.
- No npm trusted publishing or public npm publication.
- No Claude Code or opencode adapter install.
- No adapter archive generation.
- No TypeScript port of existing Python validators.
- No readiness claims for implementation, review, verification, or PR stages.

## Requirements covered

- R1-R8: package name, one binary, in-scope command surface, unknown-command and unsupported-adapter behavior.
- R9-R20: stable JSON envelope, status values, exit codes, quiet/debug/no-color behavior, stdout/stderr split.
- R21-R29a: `init` inputs, Codex-only adapter, target behavior, network/local archive modes, version-to-release mapping.
- R30-R37c: first-slice `rigorloop.yaml` generation and validation-command restraint.
- R38-R48: non-destructive mutation planning, dry-run behavior, overwrite refusal, extraction safety, partial-failure reporting.
- R49-R61c: release metadata, bundled metadata, archive verification, error/blocker mapping.
- R62-R67: planned lockfile output only.
- R68-R75: `rigorloop-tree-hash-v1`.
- R76-R79: publication and source-of-truth boundaries.

## Current Handoff Summary

- Current milestone: Lifecycle closeout
- Current milestone state: pr-opened
- Last reviewed milestone: M3. Codex adapter metadata, archive verification, extraction, and tree hash
- Review status: code-review-r9 clean-with-notes; `CR8-F1` closed
- Remaining in-scope implementation milestones: none
- Next stage: hosted CI and review on PR #62
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: implementation milestones are closed, explain-change is recorded, verify passed, and PR #62 is open; hosted CI and human review have not completed.

## Milestones

### M1. Package skeleton, command discovery, and command contract core

- Milestone state: closed
- Goal: add the package boundary and reusable CLI result contract without project mutation.
- Requirements: R1-R20, R76-R79
- Files/components likely touched: `packages/rigorloop/package.json`, `packages/rigorloop/src/**`, package build config, CLI unit tests, root ignore/config files only if required by the package toolchain
- Dependencies: approved spec and architecture; plan-review; test spec
- Tests to add/update: package metadata/bin tests, help output tests, version output tests, unknown-command tests, JSON envelope tests, no-color/quiet/debug behavior tests
- Implementation steps:
  - Add the `@xiongxianfei/rigorloop` package skeleton with one `rigorloop` bin.
  - Implement package name/version discovery from package metadata.
  - Implement command dispatch for `--help`, `version`, and `init` placeholder routing.
  - Implement shared human/JSON result envelope, stable statuses, exit-code mapping, and output-channel rules.
  - Add tests that run the built or source CLI through a local package execution path.
- Validation commands:
  - package test command selected by the package toolchain
  - `node <built-or-source-cli> --help`
  - `node <built-or-source-cli> version`
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md`
- Expected observable result: help and version work locally, unsupported commands/adapters fail with the specified contract, and no init mutation occurs yet.
- Commit message: `M1: add rigorloop CLI package skeleton`
- Milestone closeout:
  - validation passed: yes
  - progress updated: yes
  - decision log updated if needed
  - validation notes updated: yes
  - milestone committed: yes
- Risks: package toolchain selection may introduce dependency or repo-layout churn.
- Rollback/recovery: remove the new package directory and package-specific config; keep lifecycle artifacts intact.

### M2. Init dry-run, write planning, and `rigorloop.yaml` scaffold

- Milestone state: closed
- Goal: implement non-destructive `init --adapter codex` planning and first-slice manifest generation before adapter extraction.
- Requirements: R21-R48, R62-R67
- Files/components likely touched: `packages/rigorloop/src/init/**`, scaffold/template files under the package, CLI tests and fixtures
- Dependencies: M1 closed
- Tests to add/update: dry-run JSON no-write tests, human dry-run tests, `rigorloop.yaml` minimum shape tests, existing manifest valid/incompatible behavior tests, overwrite refusal tests, planned lockfile presence tests, `rigorloop.lock` absence tests
- Implementation steps:
  - Parse `init --adapter codex`, `--dry-run`, `--json`, `--from-archive`, `--quiet`, `--debug`, and `--no-color` as defined by the spec.
  - Build a write plan for `rigorloop.yaml`, `.agents/skills`, adapter install artifacts, and planned lockfile content.
  - Generate first-slice `rigorloop.yaml` for release-archive and local-archive source modes.
  - Enforce dry-run no-write behavior.
  - Refuse existing user-file conflicts and keep `--force` constrained to generated outputs only.
  - Ensure actual scaffold writes do not create or modify `rigorloop.lock`.
- Validation commands:
  - package test command selected by the package toolchain
  - fixture command for `rigorloop init --adapter codex --dry-run --json`
  - fixture command for actual init scaffold without adapter extraction if implementation splits scaffold from archive install internally
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md`
- Expected observable result: dry-run reports planned scaffold and planned lockfile content without writing files; actual scaffold writes only allowed files and never writes `rigorloop.lock`.
- Commit message: `M2: add codex init planning and manifest scaffold`
- Milestone closeout:
  - validation passed: yes
  - progress updated: yes
  - decision log updated if needed: yes
  - validation notes updated: yes
  - milestone committed: yes
- Risks: partial write handling can be ambiguous if scaffold writing and adapter install share one transaction.
- Rollback/recovery: keep init writes isolated to fixture directories during tests; for real target failure, report partial write class and never delete user files automatically.

### M3. Codex adapter metadata, archive verification, extraction, and tree hash

- Milestone state: closed
- Goal: complete verified Codex adapter installation from bundled official metadata, using either default network archive download or a local archive verified against that metadata.
- Requirements: R24-R29a, R49-R61c, R68-R75
- Files/components likely touched: `packages/rigorloop/src/adapters/**`, bundled metadata under the package, package tests and archive fixtures, possibly release metadata fixtures copied from existing release evidence
- Dependencies: M2 closed; official or fixture metadata for the compatible Codex adapter release
- Tests to add/update: bundled metadata success and absence tests, metadata rejection tests, local archive success test, checksum mismatch, size mismatch, tree-hash mismatch, path traversal, symlink rejection, wrong install root, validation result not pass, bundled metadata unavailable, release-version incompatible
- Implementation steps:
  - Add bundled official metadata lookup for the package's compatible Codex release.
  - Implement bundled metadata verification and network archive fetch behind the explicit `init --adapter codex` path.
  - Implement local archive mode with `--from-archive <path>` and no user-facing `--metadata` flag.
  - Verify source repository, adapter name, install root, validation result, filename, size, SHA-256, path safety, and symlink absence before extraction.
  - Extract only under `.agents/skills` after conflict checks.
  - Implement `rigorloop-tree-hash-v1` and compare the installed tree hash when metadata provides it.
  - Report verification failures with the spec's blocked/error status and exit-code mapping.
- Validation commands:
  - package test command selected by the package toolchain
  - fixture command for `rigorloop init --adapter codex --from-archive <matching-fixture.zip> --json`
  - fixture commands for checksum, size, tree-hash, traversal, symlink, and metadata-unavailable failures
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md`
- Expected observable result: verified Codex archive install creates `rigorloop.yaml` and `.agents/skills/**`, refuses unsafe archives and user-file conflicts, emits planned lockfile content, and leaves `rigorloop.lock` untouched.
- Commit message: `M3: install verified codex adapter archives`
- Milestone closeout:
  - validation passed: yes
  - progress updated: yes
  - decision log updated if needed: yes
  - validation notes updated: yes
  - milestone committed: yes
- Risks: network-dependent tests can become flaky; archive fixtures can become too large or accidental generated source.
- Rollback/recovery: make network behavior mockable or fixture-backed in tests; keep archive fixtures minimal; if real install fails after scaffold writes, report partial state and require manual cleanup rather than deleting user files.

### Lifecycle closeout

- Milestone state: in-progress
- Goal: complete downstream evidence after all implementation milestones are closed.
- Requirements: all acceptance criteria AC1-AC11
- Files/components likely touched: active plan, change-local explain-change/verify artifacts, PR handoff text
- Dependencies: M1-M3 closed and required review-resolution closed if any code-review finding is material
- Tests to add/update: none unless final validation exposes a gap
- Implementation steps:
  - Run final selected validation named by the test spec and plan.
  - Record explain-change evidence.
  - Run verify.
  - Prepare PR handoff only after verify owns branch-ready.
- Validation commands:
  - final selected CI from the test spec
  - any package-level full test command required by the test spec
  - `git diff --check -- <touched paths>`
- Expected observable result: final closeout evidence exists and plan/index lifecycle state is synchronized before PR handoff.
- Commit message: `Close out rigorloop CLI codex init`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed if needed
- Risks: final validation may reveal selector coverage gaps for the new package path.
- Rollback/recovery: add selector coverage or explicitly route package validation in the test spec and plan before claiming final readiness.

## Validation plan

- Plan-stage validation:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml`
- Implementation-stage validation:
  - package test command chosen in M1 and recorded in the test spec
  - fixture-based CLI commands for help, version, dry-run JSON, actual init, overwrite refusal, metadata failures, archive failures, and no-lockfile behavior
  - selected CI over package paths, spec/test-spec, plan, and change-local artifacts
- Review and closeout validation:
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow` when material findings exist or review-resolution changes
  - `git diff --check -- <touched paths>`

## Risks and recovery

- New Node package tooling could add dependency or formatting churn. Recovery: keep package-local config minimal and justify any dependency in implementation notes.
- Archive extraction is security-sensitive. Recovery: implement path/symlink rejection before extraction and cover it with fixtures before success-path install.
- `rigorloop.lock` could become accidental durable truth. Recovery: test that actual init never creates or modifies it and keep planned lockfile content only in output.
- Public npm publication could be implied by package creation. Recovery: keep publication scripts/workflows out of scope and preserve the release-hardening blocker in docs.
- The validation selector may not understand `packages/rigorloop/**`. Recovery: add explicit package validation routing only if required by the approved test spec or implementation validation.

## Dependencies

- Plan-review must approve this plan before test-spec.
- Test spec must map every spec `MUST` to concrete tests before implementation.
- Public npm publication depends on a separate release-hardening proposal/spec and is not a dependency for this implementation.
- Durable lockfile writes depend on a separate lockfile spec and are not a dependency for this implementation.
- Official Codex adapter metadata for the compatible release must be available as bundled metadata or fixture metadata before M3 can close.

## Progress

- [x] 2026-05-15: accepted proposal, approved spec, approved architecture package update, and accepted ADR are available.
- [x] 2026-05-15: clean architecture-review receipt recorded with no material findings.
- [x] 2026-05-15: execution plan created.
- [x] 2026-05-15: plan-stage artifact lifecycle, change metadata, diff whitespace, and selected CI validation passed.
- [x] 2026-05-15: plan-review approved the plan with no material findings.
- [x] 2026-05-15: test spec created.
- [x] 2026-05-15: test spec approved by user for implementation reliance.
- [x] 2026-05-15: M1 implementation started.
- [x] 2026-05-15: M1 tests were written before the CLI entrypoint and failed on missing `dist/bin/rigorloop.js`.
- [x] 2026-05-15: M1 implementation completed and selected validation passed.
- [x] 2026-05-15: M1 handed to code-review.
- [x] 2026-05-15: M1 handoff commit prepared.
- [x] 2026-05-15: code-review-r1 requested changes for M1 finding `CR1-F1`.
- [x] 2026-05-15: `CR1-F1` accepted and fixed by adding a command-result exit-class mapper and table-driven T11 coverage for exit codes `0`, `2`, `3`, `4`, `5`, and `1`.
- [x] 2026-05-15: code-review-r2 closed M1 with no material findings.
- [x] M1 implemented and reviewed.
- [x] 2026-05-15: M2 implementation started.
- [x] 2026-05-15: M2 tests were written before implementation and failed against the M1 placeholder for missing planned manifest/lockfile output, actual scaffold writes, archive path validation, existing manifest handling, and no-lockfile behavior.
- [x] 2026-05-15: M2 implementation completed with dry-run planning, actual manifest/install-root scaffold writes, local archive path validation, existing manifest handling, overwrite refusal, planned lockfile output only, and no adapter extraction.
- [x] 2026-05-15: M2 handed to code-review.
- [x] 2026-05-15: M2 handoff commit prepared.
- [x] 2026-05-15: code-review-r4 requested changes for M2 finding `CR4-F1`.
- [x] 2026-05-15: `CR4-F1` accepted and fixed by making `.agents` and `.agents/skills` first-class planned directory actions before mutation.
- [x] 2026-05-15: M2 handed back to code-review rerun.
- [x] 2026-05-15: code-review-r5 closed M2 with no material findings.
- [x] M2 implemented and reviewed.
- [x] 2026-05-15: M3 implementation started.
- [x] 2026-05-15: M3 tests were expanded before implementation and failed against the M2 scaffold-only CLI for missing archive metadata lookup, archive verification, extraction, tree-hash validation, and metadata failure handling.
- [x] 2026-05-15: M3 implementation completed with package-bundled Codex metadata, default network archive support, local archive verification without `--metadata`, ZIP path/symlink safety checks, SHA/size/tree-hash validation, adapter extraction, planned lockfile hashes, and no durable `rigorloop.lock` writes.
- [x] 2026-05-15: M3 handed to code-review.
- [x] 2026-05-15: M3 handoff commit prepared.
- [x] 2026-05-15: code-review-r6 requested changes for M3 findings `CR6-F1` and `CR6-F2`.
- [x] 2026-05-15: `CR6-F1` and `CR6-F2` accepted and fixed by removing production runtime metadata source overrides, adding a package-bundled release index, and verifying network metadata bytes before parsing.
- [x] 2026-05-15: M3 handed back to code-review rerun.
- [x] 2026-05-15: code-review-r7 requested changes for M3 finding `CR7-F1`.
- [x] 2026-05-15: `CR7-F1` accepted and fixed by using package-bundled official adapter metadata as the trust root for default network install and local archive install.
- [x] 2026-05-15: code-review-r8 requested changes for M3 finding `CR8-F1`.
- [x] 2026-05-15: `CR8-F1` accepted and fixed by validating that network install fetches only the exact official GitHub release archive URL.
- [x] 2026-05-15: code-review-r9 closed M3 with no material findings.
- [x] M3 implemented and reviewed.
- [x] 2026-05-15: Explain-change recorded at `docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/explain-change.md`.
- [x] 2026-05-15: Verify completed at `docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/verify-report.md`; branch-ready evidence recorded for PR handoff.
- [x] 2026-05-15: PR handoff completed by opening PR #62: `https://github.com/xiongxianfei/rigorloop/pull/62`.

## Decision log

- 2026-05-15: split implementation into package contract, init planning, and verified archive install so command shape can be reviewed before security-sensitive archive extraction.
- 2026-05-15: keep lifecycle closeout separate from implementation milestones because explain-change, verify, and PR readiness are downstream gates rather than implementation work.
- 2026-05-15: make M1 the first implementation handoff after test-spec so package command contract is proven before filesystem mutation and archive extraction work.
- 2026-05-15: use `specs/rigorloop-cli-package-and-codex-init.test.md` as the active proof surface for M1 implementation.
- 2026-05-15: add a narrow selector category and `rigorloop_cli.test` selected check for `packages/rigorloop/**` because selected CI must not fail open or require manual routing for the new package path.
- 2026-05-15: accept `CR1-F1` for M1; the shared exit-code layer must be fixed before M1 can close.
- 2026-05-15: resolve `CR1-F1` with a package-local command-result helper so exit codes are mapped from `exit_class`/failure kind instead of public status alone.
- 2026-05-15: keep M2 actual init to scaffold creation only: it writes `rigorloop.yaml` and `.agents/skills`, reports planned lockfile content, and leaves archive metadata verification/extraction to M3.
- 2026-05-15: accept `CR4-F1` from code-review-r4; the M2 write plan must list `.agents` and `.agents/skills` as separate directory actions, and actual init must only create planned pending directories.
- 2026-05-15: use package-bundled JSON metadata for the v0.1.3 Codex local-archive path while keeping generated adapter archives outside the npm package.
- 2026-05-15: allow the existing v0.1.3 Codex archive's top-level `AGENTS.md` support file to be ignored rather than extracted; every installed path still remains under `.agents/skills`, and every other outside-root entry remains a verification error.
- 2026-05-15: code-review-r6 found that runtime metadata source overrides and missing metadata-hash verification must be resolved before M3 can close.
- 2026-05-15: resolve `CR6-F1` by moving fixture metadata injection into temporary fixture package layouts and removing production `RIGORLOOP_RELEASE_METADATA_URL` / `RIGORLOOP_METADATA_FILE` lookup.
- 2026-05-15: initially resolved `CR6-F2` with `dist/metadata/releases.json` as the package-bundled trust root for network metadata URL and SHA-256; `CR7-F1` then revised the first-slice model to use bundled metadata as the trust root for both install paths.
- 2026-05-15: code-review-r7 found that the tracked bundled release index points at a `v0.1.3` metadata asset URL that currently returns 404, so M3 cannot close until the official metadata source exists or the approved network install contract is revised.
- 2026-05-15: resolve `CR7-F1` by making bundled official adapter metadata the metadata trust root for both default network install and local archive install; default network install now downloads only the official archive URL named by trusted bundled metadata.
- 2026-05-15: code-review-r8 found that default network install does not enforce that the archive URL named by bundled metadata is an official `xiongxianfei/rigorloop` GitHub release archive URL.
- 2026-05-15: resolve `CR8-F1` by validating the exact official GitHub release archive URL before default network install fetches archive bytes.
- 2026-05-15: code-review-r9 closed M3 with no material findings; all implementation milestones are now closed.

## Surprises and discoveries

- 2026-05-15: `packages/rigorloop` was initially unclassified by the validation selector. The active plan anticipated this risk; M1 added deterministic selector routing to run the package test command.
- 2026-05-15: the existing `v0.1.3` Codex adapter archive includes a top-level `AGENTS.md` support document in addition to `.agents/skills/**`; M3 treats that exact support file as non-installed archive metadata so the command remains compatible with the published archive without mutating outside the install root.

## Validation notes

- 2026-05-15: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml` passed.
- 2026-05-15: `python scripts/validate-change-metadata.py docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml` passed.
- 2026-05-15: `git diff --check -- docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md docs/plan.md docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml` passed.
- 2026-05-15: `bash scripts/ci.sh --mode explicit --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml` passed.
- 2026-05-15: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/rigorloop-cli-package-and-codex-init.test.md --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml` passed.
- 2026-05-15: `python scripts/validate-change-metadata.py docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml` passed after test-spec authoring.
- 2026-05-15: `git diff --check -- specs/rigorloop-cli-package-and-codex-init.test.md docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml` passed.
- 2026-05-15: `bash scripts/ci.sh --mode explicit --path specs/rigorloop-cli-package-and-codex-init.test.md --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml` passed.
- 2026-05-15: `npm test --prefix packages/rigorloop` failed before implementation because `packages/rigorloop/dist/bin/rigorloop.js` did not exist.
- 2026-05-15: `npm test --prefix packages/rigorloop` passed after implementing the M1 CLI skeleton.
- 2026-05-15: `node packages/rigorloop/dist/bin/rigorloop.js --help` passed.
- 2026-05-15: `node packages/rigorloop/dist/bin/rigorloop.js version` passed.
- 2026-05-15: `node packages/rigorloop/dist/bin/rigorloop.js init --adapter codex --dry-run --json` passed.
- 2026-05-15: `python scripts/test-select-validation.py` passed after adding `packages/rigorloop` selector routing.
- 2026-05-15: `python scripts/select-validation.py --mode explicit --path packages/rigorloop --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md --path specs/rigorloop-cli-package-and-codex-init.test.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml --path scripts/validation_selection.py --path scripts/test-select-validation.py` returned `status: ok` and selected `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `selector.regression`, and `rigorloop_cli.test`.
- 2026-05-15: `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md --path specs/rigorloop-cli-package-and-codex-init.test.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml --path scripts/validation_selection.py --path scripts/test-select-validation.py` passed.
- 2026-05-15: `code-review-r1` recorded `CR1-F1`; validation pending after review recording.
- 2026-05-15: `npm test --prefix packages/rigorloop` passed after the `CR1-F1` fix.
- 2026-05-15: `python scripts/test-select-validation.py` passed after the `CR1-F1` fix.
- 2026-05-15: `git diff --check --` passed after the `CR1-F1` fix.
- 2026-05-15: `python scripts/validate-review-artifacts.py docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow` passed after `CR1-F1` resolution recording.
- 2026-05-15: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow` passed after `CR1-F1` resolution recording.
- 2026-05-15: `python scripts/validate-change-metadata.py docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml` passed after `CR1-F1` resolution recording.
- 2026-05-15: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-log.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-resolution.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/reviews/code-review-r1.md --path docs/plan.md --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path specs/rigorloop-cli-package-and-codex-init.test.md` passed after `CR1-F1` resolution recording.
- 2026-05-15: `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path scripts/validation_selection.py --path scripts/test-select-validation.py --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md --path specs/rigorloop-cli-package-and-codex-init.test.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-log.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-resolution.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/reviews/code-review-r1.md` passed after `CR1-F1` resolution recording.
- 2026-05-15: `code-review-r2` recorded clean-with-notes for the `CR1-F1` fix and closed M1.
- 2026-05-15: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-log.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-resolution.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/reviews/code-review-r1.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/reviews/code-review-r2.md --path docs/plan.md --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path specs/rigorloop-cli-package-and-codex-init.test.md` passed after code-review-r2 recording.
- 2026-05-15: `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path scripts/validation_selection.py --path scripts/test-select-validation.py --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md --path specs/rigorloop-cli-package-and-codex-init.test.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-log.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-resolution.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/reviews/code-review-r1.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/reviews/code-review-r2.md` passed after code-review-r2 recording.
- 2026-05-15: `npm test --prefix packages/rigorloop` failed after M2 tests were added and before implementation because the M1 placeholder lacked planned manifest/lockfile output, actual init scaffold writes, and local archive path handling.
- 2026-05-15: `npm test --prefix packages/rigorloop` passed after implementing M2.
- 2026-05-15: `node packages/rigorloop/dist/bin/rigorloop.js --help` passed after M2.
- 2026-05-15: `node packages/rigorloop/dist/bin/rigorloop.js version` passed after M2.
- 2026-05-15: temporary-project smoke for `node /home/xiongxianfei/data/20260419-rigorloop/packages/rigorloop/dist/bin/rigorloop.js init --adapter codex --dry-run --json` passed and left the project empty.
- 2026-05-15: temporary-project smoke for actual `node /home/xiongxianfei/data/20260419-rigorloop/packages/rigorloop/dist/bin/rigorloop.js init --adapter codex --json` passed and created `rigorloop.yaml` plus `.agents/skills` without `rigorloop.lock`.
- 2026-05-15: temporary-project smoke for missing `--from-archive ./missing.zip` returned exit `4`, error code `invalid-archive-path`, and no files written.
- 2026-05-15: temporary-project smoke for `.agents` user-file conflict with `--force` returned exit `5`, blocker code `overwrite-refused`, and preserved the user file.
- 2026-05-15: `python scripts/test-select-validation.py` passed after M2.
- 2026-05-15: `python scripts/validate-change-metadata.py docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml` passed after M2.
- 2026-05-15: `git diff --check --` passed after M2.
- 2026-05-15: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path packages/rigorloop/dist/bin/rigorloop.js --path packages/rigorloop/test/cli.test.js --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml --path specs/rigorloop-cli-package-and-codex-init.test.md` passed after M2.
- 2026-05-15: `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md --path specs/rigorloop-cli-package-and-codex-init.test.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml` passed after M2.
- 2026-05-15: `python scripts/validate-review-artifacts.py docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow` passed after code-review-r4 recording.
- 2026-05-15: `python scripts/validate-change-metadata.py docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml` passed after code-review-r4 recording.
- 2026-05-15: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-log.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-resolution.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/reviews/code-review-r4.md --path docs/plan.md --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path specs/rigorloop-cli-package-and-codex-init.test.md` passed after code-review-r4 recording.
- 2026-05-15: `bash scripts/ci.sh --mode explicit --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-log.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-resolution.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/reviews/code-review-r4.md --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md --path specs/rigorloop-cli-package-and-codex-init.test.md` passed after code-review-r4 recording.
- 2026-05-15: `git diff --check --` passed after code-review-r4 recording.
- 2026-05-15: `npm test --prefix packages/rigorloop` failed after adding `CR4-F1` regression tests because the M2 planner omitted `.agents` and listed `rigorloop.yaml` before directory actions.
- 2026-05-15: `npm test --prefix packages/rigorloop` passed after the `CR4-F1` fix.
- 2026-05-15: `python scripts/test-select-validation.py` passed after the `CR4-F1` fix.
- 2026-05-15: `python scripts/validate-review-artifacts.py docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow` passed after `CR4-F1` resolution recording.
- 2026-05-15: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow` passed after `CR4-F1` resolution recording.
- 2026-05-15: `python scripts/validate-change-metadata.py docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml` passed after the `CR4-F1` fix.
- 2026-05-15: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path packages/rigorloop/dist/bin/rigorloop.js --path packages/rigorloop/test/cli.test.js --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml --path specs/rigorloop-cli-package-and-codex-init.test.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-log.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-resolution.md` passed after the `CR4-F1` fix.
- 2026-05-15: `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md --path specs/rigorloop-cli-package-and-codex-init.test.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-log.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-resolution.md` passed after the `CR4-F1` fix.
- 2026-05-15: `git diff --check --` passed after the `CR4-F1` fix.
- 2026-05-15: code-review-r5 recorded clean-with-notes for the `CR4-F1` fix and closed M2.
- 2026-05-15: `python scripts/validate-review-artifacts.py docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow` passed after code-review-r5 recording.
- 2026-05-15: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow` passed after code-review-r5 recording.
- 2026-05-15: `python scripts/validate-change-metadata.py docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml` passed after code-review-r5 recording.
- 2026-05-15: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-log.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-resolution.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/reviews/code-review-r5.md --path docs/plan.md --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path specs/rigorloop-cli-package-and-codex-init.test.md` passed after code-review-r5 recording.
- 2026-05-15: `bash scripts/ci.sh --mode explicit --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-log.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-resolution.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/reviews/code-review-r5.md --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md --path specs/rigorloop-cli-package-and-codex-init.test.md` passed after code-review-r5 recording.
- 2026-05-15: `git diff --check --` passed after code-review-r5 recording.
- 2026-05-15: `npm test --prefix packages/rigorloop` passed after M3 implementation.
- 2026-05-15: temporary-project smoke for the real `v0.1.3` Codex archive with `node /home/xiongxianfei/data/20260419-rigorloop/packages/rigorloop/dist/bin/rigorloop.js init --adapter codex --from-archive ./rigorloop-adapter-codex-v0.1.3.zip --json` passed, installed verified adapter files, and left `rigorloop.lock` unwritten.
- 2026-05-15: `python scripts/test-select-validation.py` passed after M3 implementation.
- 2026-05-15: `python scripts/validate-change-metadata.py docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml` passed after M3 implementation.
- 2026-05-15: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path packages/rigorloop/dist/bin/rigorloop.js --path packages/rigorloop/test/cli.test.js --path packages/rigorloop/dist/metadata/adapter-artifacts-v0.1.3.json --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml --path specs/rigorloop-cli-package-and-codex-init.test.md` passed after M3 implementation.
- 2026-05-15: `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md --path specs/rigorloop-cli-package-and-codex-init.test.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml` passed after M3 implementation.
- 2026-05-15: `git diff --check --` passed after M3 implementation.
- 2026-05-15: `code-review-r6` recorded changes-requested for M3 findings `CR6-F1` and `CR6-F2`; post-recording validation pending.
- 2026-05-15: `python scripts/validate-review-artifacts.py docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow` passed after code-review-r6 recording.
- 2026-05-15: `python scripts/validate-change-metadata.py docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml` passed after code-review-r6 recording.
- 2026-05-15: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-log.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-resolution.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/reviews/code-review-r6.md --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md --path specs/rigorloop-cli-package-and-codex-init.test.md` passed after code-review-r6 recording.
- 2026-05-15: `bash scripts/ci.sh --mode explicit --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-log.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-resolution.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/reviews/code-review-r6.md --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md --path specs/rigorloop-cli-package-and-codex-init.test.md` passed after code-review-r6 recording.
- 2026-05-15: `git diff --check --` passed after code-review-r6 recording.
- 2026-05-15: `npm test --prefix packages/rigorloop` failed before the `CR6-F1`/`CR6-F2` fix because new tests proved runtime metadata source overrides still worked and metadata hash mismatch was not verified.
- 2026-05-15: `npm test --prefix packages/rigorloop` passed after the `CR6-F1`/`CR6-F2` fix.
- 2026-05-15: temporary-project smoke for the real `v0.1.3` Codex archive with `node /home/xiongxianfei/data/20260419-rigorloop/packages/rigorloop/dist/bin/rigorloop.js init --adapter codex --from-archive ./rigorloop-adapter-codex-v0.1.3.zip --json` passed after the `CR6-F1`/`CR6-F2` fix.
- 2026-05-15: `python scripts/test-select-validation.py` passed after the `CR6-F1`/`CR6-F2` fix.
- 2026-05-15: `python scripts/validate-review-artifacts.py docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow` passed after the `CR6-F1`/`CR6-F2` fix.
- 2026-05-15: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow` passed after the `CR6-F1`/`CR6-F2` fix.
- 2026-05-15: `python scripts/validate-change-metadata.py docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml` passed after the `CR6-F1`/`CR6-F2` fix.
- 2026-05-15: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path packages/rigorloop/dist/bin/rigorloop.js --path packages/rigorloop/test/cli.test.js --path packages/rigorloop/dist/metadata/adapter-artifacts-v0.1.3.json --path packages/rigorloop/dist/metadata/releases.json --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml --path specs/rigorloop-cli-package-and-codex-init.test.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-log.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-resolution.md` passed after the `CR6-F1`/`CR6-F2` fix.
- 2026-05-15: `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md --path specs/rigorloop-cli-package-and-codex-init.test.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-log.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-resolution.md` passed after the `CR6-F1`/`CR6-F2` fix.
- 2026-05-15: `git diff --check --` passed after the `CR6-F1`/`CR6-F2` fix.
- 2026-05-15: direct code-review check for `https://github.com/xiongxianfei/rigorloop/releases/download/v0.1.3/adapter-artifacts-v0.1.3.json` returned HTTP 404.
- 2026-05-15: direct code-review check of the GitHub release API for `v0.1.3` listed the three adapter ZIP assets but no `adapter-artifacts-v0.1.3.json` metadata asset.
- 2026-05-15: `npm test --prefix packages/rigorloop` passed after the `CR7-F1` fix.
- 2026-05-15: real default network install smoke with `node packages/rigorloop/dist/bin/rigorloop.js init --adapter codex --json` passed after the `CR7-F1` fix and installed verified Codex adapter files without writing `rigorloop.lock`.
- 2026-05-15: real local archive smoke with `node packages/rigorloop/dist/bin/rigorloop.js init --adapter codex --from-archive ./rigorloop-adapter-codex-v0.1.3.zip --json` passed after the `CR7-F1` fix and installed verified Codex adapter files without writing `rigorloop.lock`.
- 2026-05-15: `python scripts/test-select-validation.py` passed after the `CR7-F1` fix.
- 2026-05-15: `python scripts/validate-review-artifacts.py docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow` passed after the `CR7-F1` fix.
- 2026-05-15: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow` passed after the `CR7-F1` fix.
- 2026-05-15: `python scripts/validate-change-metadata.py docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml` passed after the `CR7-F1` fix.
- 2026-05-15: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path packages/rigorloop/dist/bin/rigorloop.js --path packages/rigorloop/test/cli.test.js --path packages/rigorloop/dist/metadata/adapter-artifacts-v0.1.3.json --path packages/rigorloop/dist/metadata/releases.json --path specs/rigorloop-cli-package-and-codex-init.md --path specs/rigorloop-cli-package-and-codex-init.test.md --path docs/adr/ADR-20260515-rigorloop-cli-package-and-codex-init.md --path docs/architecture/system/architecture.md --path docs/architecture/system/diagrams/context.mmd --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-log.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-resolution.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/reviews/code-review-r7.md` passed after the `CR7-F1` fix.
- 2026-05-15: `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path specs/rigorloop-cli-package-and-codex-init.md --path specs/rigorloop-cli-package-and-codex-init.test.md --path docs/adr/ADR-20260515-rigorloop-cli-package-and-codex-init.md --path docs/architecture/system/architecture.md --path docs/architecture/system/diagrams/context.mmd --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-log.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-resolution.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/reviews/code-review-r7.md` passed after the `CR7-F1` fix.
- 2026-05-15: `git diff --check --` passed after the `CR7-F1` fix.
- 2026-05-15: `npm test --prefix packages/rigorloop` passed after the `CR8-F1` fix.
- 2026-05-15: real default network install smoke with `node packages/rigorloop/dist/bin/rigorloop.js init --adapter codex --json` passed after the `CR8-F1` fix and installed verified Codex adapter files without writing `rigorloop.lock`.
- 2026-05-15: real local archive smoke with `node packages/rigorloop/dist/bin/rigorloop.js init --adapter codex --from-archive ./rigorloop-adapter-codex-v0.1.3.zip --json` passed after the `CR8-F1` fix and installed verified Codex adapter files without writing `rigorloop.lock`.
- 2026-05-15: `python scripts/test-select-validation.py` passed after the `CR8-F1` fix.
- 2026-05-15: `python scripts/validate-review-artifacts.py docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow` passed after the `CR8-F1` fix.
- 2026-05-15: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow` passed after the `CR8-F1` fix.
- 2026-05-15: `python scripts/validate-change-metadata.py docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml` passed after the `CR8-F1` fix.
- 2026-05-15: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path packages/rigorloop/dist/bin/rigorloop.js --path packages/rigorloop/dist/lib/official-archive-url.js --path packages/rigorloop/test/cli.test.js --path packages/rigorloop/dist/metadata/adapter-artifacts-v0.1.3.json --path packages/rigorloop/dist/metadata/releases.json --path specs/rigorloop-cli-package-and-codex-init.md --path specs/rigorloop-cli-package-and-codex-init.test.md --path docs/adr/ADR-20260515-rigorloop-cli-package-and-codex-init.md --path docs/architecture/system/architecture.md --path docs/architecture/system/diagrams/context.mmd --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-log.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-resolution.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/reviews/code-review-r8.md` passed after the `CR8-F1` fix.
- 2026-05-15: `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path specs/rigorloop-cli-package-and-codex-init.md --path specs/rigorloop-cli-package-and-codex-init.test.md --path docs/adr/ADR-20260515-rigorloop-cli-package-and-codex-init.md --path docs/architecture/system/architecture.md --path docs/architecture/system/diagrams/context.mmd --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-log.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-resolution.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/reviews/code-review-r8.md` passed after the `CR8-F1` fix.
- 2026-05-15: `git diff --check --` passed after the `CR8-F1` fix.
- 2026-05-15: `python scripts/validate-review-artifacts.py docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow` passed after code-review-r9 recording.
- 2026-05-15: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow` passed after code-review-r9 recording.
- 2026-05-15: `python scripts/validate-change-metadata.py docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml` passed after code-review-r9 recording.
- 2026-05-15: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path packages/rigorloop/dist/bin/rigorloop.js --path packages/rigorloop/dist/lib/official-archive-url.js --path packages/rigorloop/test/cli.test.js --path packages/rigorloop/dist/metadata/adapter-artifacts-v0.1.3.json --path packages/rigorloop/dist/metadata/releases.json --path specs/rigorloop-cli-package-and-codex-init.md --path specs/rigorloop-cli-package-and-codex-init.test.md --path docs/adr/ADR-20260515-rigorloop-cli-package-and-codex-init.md --path docs/architecture/system/architecture.md --path docs/architecture/system/diagrams/context.mmd --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-log.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-resolution.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/reviews/code-review-r9.md` passed after code-review-r9 recording.
- 2026-05-15: `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path specs/rigorloop-cli-package-and-codex-init.md --path specs/rigorloop-cli-package-and-codex-init.test.md --path docs/adr/ADR-20260515-rigorloop-cli-package-and-codex-init.md --path docs/architecture/system/architecture.md --path docs/architecture/system/diagrams/context.mmd --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-log.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-resolution.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/reviews/code-review-r9.md` passed after code-review-r9 recording.
- 2026-05-15: `git diff --check --` passed after code-review-r9 recording.
- 2026-05-15: `python scripts/validate-change-metadata.py docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml` passed after explain-change recording.
- 2026-05-15: `python scripts/validate-review-artifacts.py docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow` and closeout mode passed after explain-change recording.
- 2026-05-15: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path packages/rigorloop/dist/bin/rigorloop.js --path packages/rigorloop/dist/lib/official-archive-url.js --path packages/rigorloop/test/cli.test.js --path packages/rigorloop/dist/metadata/adapter-artifacts-v0.1.3.json --path packages/rigorloop/dist/metadata/releases.json --path specs/rigorloop-cli-package-and-codex-init.md --path specs/rigorloop-cli-package-and-codex-init.test.md --path docs/adr/ADR-20260515-rigorloop-cli-package-and-codex-init.md --path docs/architecture/system/architecture.md --path docs/architecture/system/diagrams/context.mmd --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/explain-change.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-log.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-resolution.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/reviews/code-review-r9.md` passed after explain-change recording.
- 2026-05-15: `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path specs/rigorloop-cli-package-and-codex-init.md --path specs/rigorloop-cli-package-and-codex-init.test.md --path docs/adr/ADR-20260515-rigorloop-cli-package-and-codex-init.md --path docs/architecture/system/architecture.md --path docs/architecture/system/diagrams/context.mmd --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/explain-change.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-log.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-resolution.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/reviews/code-review-r9.md` passed after explain-change recording.
- 2026-05-15: `git diff --check --` passed after explain-change recording.
- 2026-05-15: final verify passed with `npm test --prefix packages/rigorloop`, `python scripts/test-select-validation.py`, real default network install smoke, real local archive install smoke, change metadata validation, review artifact validation and closeout validation, explicit-path artifact lifecycle validation, selected CI, and `git diff --check --`.
- 2026-05-15: post-verify-report validation passed with change metadata validation, review artifact validation and closeout validation, explicit-path artifact lifecycle validation including `verify-report.md`, selected CI including `skills.regression`, `selector.regression`, and `rigorloop_cli.test`, and `git diff --check --`.

## Outcome and retrospective

- Implementation milestones M1-M3 are complete and reviewed. Explain-change is recorded. Verify passed. PR #62 is open; hosted CI and human review remain pending.

## Readiness

- See `Current Handoff Summary`.
- This plan is ready for hosted CI and human review on PR #62.
- It is not complete until PR review, hosted CI, and merge/closeout complete.

## Follow-ups

- Lockfile durable write behavior remains deferred to a lockfile spec.
- Public npm publication remains deferred to release hardening.
- `new-change`, `status`, `validate`, non-Codex adapters, workflow YAML canonicality, generated workflow docs, and frozen drift checks remain deferred follow-up slices.
