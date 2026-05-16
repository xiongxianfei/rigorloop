# RigorLoop CLI durable lockfile

- Status: done
- Owner: maintainers
- Start date: 2026-05-16
- Last updated: 2026-05-16
- Related issue or PR: PR #63
- Supersedes: none

## Purpose / big picture

This plan turns the approved durable lockfile contract into reviewable implementation milestones for the existing `@xiongxianfei/rigorloop` CLI package.

The first CLI slice installed the verified Codex adapter and emitted planned lockfile content only. This slice allows `rigorloop init --adapter codex` and `rigorloop init --adapter codex --from-archive <path>` to write deterministic `rigorloop.lock` state after verification succeeds, while preserving the source-of-truth boundary: the lockfile records downstream generated-output state and does not become canonical workflow, skill, schema, release, or adapter metadata.

## Source artifacts

- Proposal: `docs/proposals/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow.md`
- Spec: `specs/rigorloop-cli-lockfile.md`
- Architecture: `docs/architecture/system/architecture.md`
- ADR: `docs/adr/ADR-20260516-rigorloop-cli-lockfile.md`
- Architecture review: `docs/changes/2026-05-15-rigorloop-cli-lockfile/reviews/architecture-review-r1.md`
- Related first CLI plan: `docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md`
- Test spec: `specs/rigorloop-cli-lockfile.test.md`

## Context and orientation

- The CLI implementation currently lives in `packages/rigorloop/dist/bin/rigorloop.js` with helper modules under `packages/rigorloop/dist/lib/`.
- The package currently emits `planned_lockfile` and warning code `lockfile-spec-not-approved`; this slice removes that warning for successful lockfile-writing operations and creates or updates `rigorloop.lock`.
- Existing CLI tests live in `packages/rigorloop/test/cli.test.js` and already include fixture helpers for temporary projects, fixture ZIP archives, bundled metadata, mocked fetch, tree hashing, and command execution.
- The existing archive flow verifies bundled metadata, official archive URLs, local archives, archive size/SHA, extraction safety, symlink absence, and installed tree hash before writing adapter files.
- `rigorloop.yaml` remains the project manifest. `rigorloop.lock` records verified generated-output state and must not record absolute paths, timestamps, usernames, hostnames, tokens, temp directories, or full adapter release metadata.
- `docs/plan.md` is the lifecycle index. This file is the active plan body and owns live milestone state.

## Non-goals

- No `rigorloop new-change`, `rigorloop status`, or `rigorloop validate`.
- No lockfile migration, repair, refresh, or delete command.
- No lockfile writes for Claude Code, opencode, workflow YAML, generated workflow docs, or non-adapter outputs.
- No public npm publication or npm release hardening.
- No new canonical workflow, skill, schema, release, or adapter metadata source.
- No use of `--force` to replace arbitrary lockfile state.
- No preservation of unknown lockfile fields in this first schema slice.

## Requirements covered

- R1-R8: lockfile scope, owner, Codex-only write surface, verification-before-write, dry-run no-write behavior.
- R9-R17h: deterministic UTF-8/LF `schema_version: 1` lockfile document shape.
- R18-R23b: Codex adapter entry fields and first-slice adapter limits.
- R23ba-R23bj: `release-archive` and `local-archive` source semantics.
- R23c-R23k: unknown-field, unsupported-shape, malformed-YAML, and invalid-type handling.
- R24-R33: `rigorloop-tree-hash-v1` lockfile hashing.
- R34-R45e: write plan, create/update, supported entry update, and no arbitrary replacement.
- R46-R53: drift and generated-output conflict behavior.
- R54-R61: JSON, human output, status, exit-class, and error behavior.
- R62-R66: compatibility with first-slice projects and package-local execution.
- AC1-AC13: creation, dry-run, complete shape, deterministic rerun, missing-field rejection, unsupported shape blocking, drift blocking, source-mode recording, and failed-verification no-write behavior.

## Current Handoff Summary

- Current milestone: Lifecycle closeout
- Current milestone state: completed
- Last reviewed milestone: M3
- Review status: code-review-r5 approved M3 with no material findings
- Remaining in-scope implementation milestones: none
- Next stage: none
- Final closeout readiness: completed
- Reason final closeout is or is not ready: M1, M2, and M3 are closed, explain-change is recorded, final local verify passed, PR #63 passed hosted CI and human review, and PR #63 is merged.

## Milestones

### M1. Lockfile schema, parser, serializer, and write-plan contract

- Milestone state: closed
- Goal: add the lockfile data model and deterministic serialization path without changing adapter install success behavior yet.
- Requirements: R1-R17h, R23c-R23k, R34-R35, R40-R45c, R54-R61, AC2-AC7, AC12
- Files/components likely touched: `packages/rigorloop/dist/bin/rigorloop.js`, possibly new `packages/rigorloop/dist/lib/lockfile.js`, `packages/rigorloop/test/cli.test.js`
- Dependencies: approved spec, approved architecture-review, approved test spec
- Tests to add/update:
  - full valid `schema_version: 1` lockfile fixture parses successfully;
  - missing required fields fail with `status: error`, exit code `4`;
  - malformed YAML fails with `status: error`, exit code `4`;
  - unsupported schema version blocks with `status: blocked`, exit code `2`, blocker code `unsupported-lockfile-shape`;
  - unknown top-level or nested fields block before mutation with `unsupported-lockfile-shape`;
  - unsupported adapter, source, or tree hash algorithm blocks before mutation;
  - dry-run reports `planned_lockfile` and does not write `rigorloop.lock`;
  - write plan includes `rigorloop.lock` as planned, skipped, blocked, or unchanged.
- Implementation steps:
  - Add a small lockfile helper that parses strict `schema_version: 1` YAML for the supported shape.
  - Add deterministic lockfile serialization using fixed field order, LF line endings, sorted adapter entries, and no timestamps.
  - Add SHA-256 normalization for `rigorloop.yaml`.
  - Add lockfile action/artifact planning for absent, valid, invalid, unsupported, and unchanged lockfile states.
  - Keep successful actual init from writing the lockfile until M2 wires the verified-write point.
- Validation commands:
  - `npm test --prefix packages/rigorloop`
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path docs/plans/2026-05-16-rigorloop-cli-lockfile.md --path docs/plan.md --path specs/rigorloop-cli-lockfile.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml`
- Expected observable result: tests prove strict shape handling and deterministic planned lockfile output, while the existing adapter install behavior remains otherwise unchanged.
- Commit message: `M1: add rigorloop lockfile schema handling`
- Milestone closeout:
  - validation passed: yes for implementation handoff
  - progress updated: yes
  - decision log updated if needed
  - validation notes updated: yes
  - milestone committed: no; commit not created in this handoff
- Risks: ad hoc YAML parsing can be brittle.
- Rollback/recovery: keep the parser scoped to the strict first-slice shape; if implementation needs broader YAML behavior, record the dependency decision before adding it.

### M2. Successful lockfile creation and update after verified Codex install

- Milestone state: closed
- Goal: write or update `rigorloop.lock` only after Codex adapter install and installed-tree verification succeed.
- Requirements: R4-R8, R18-R23bj, R24-R33, R36-R39, R45a-R45e, R54-R57, R62-R65, AC1-AC5, AC9-AC11, AC13
- Files/components likely touched: `packages/rigorloop/dist/bin/rigorloop.js`, lockfile helper, `packages/rigorloop/test/cli.test.js`
- Dependencies: M1 closed
- Tests to add/update:
  - network install writes `source: release-archive`;
  - local archive install writes `source: local-archive`;
  - local archive lockfile records archive basename, not absolute path;
  - lockfile includes package identity, manifest path/hash, release tag, archive hash, install root, tree hash algorithm, tree hash, and file count;
  - rerun with matching state is deterministic and does not rewrite unrelated supported entries;
  - reinstall through a different source mode updates only the matching Codex entry after verification succeeds;
  - failed metadata, archive, tree-hash, or mutation-safety verification does not create or update `rigorloop.lock`;
  - `lockfile-spec-not-approved` is no longer emitted on successful lockfile-writing operations.
- Implementation steps:
  - Move lockfile write to the verified point after archive inspection, extraction, and installed-tree hash confirmation.
  - Compute lockfile tree hash from the installed filesystem state, not only from archive fixture bytes.
  - Add supported existing-lockfile update behavior for `rigorloop.version`, `manifest.sha256`, and the matching Codex adapter entry.
  - Preserve supported unrelated adapter entries by sorting and serializing them deterministically, while still blocking unsupported adapters.
  - Update JSON actions/artifacts and human output to report created, updated, unchanged, skipped, or blocked lockfile state.
- Validation commands:
  - `npm test --prefix packages/rigorloop`
  - fixture command: `node packages/rigorloop/dist/bin/rigorloop.js init --adapter codex --from-archive <fixture.zip> --json`
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path docs/plans/2026-05-16-rigorloop-cli-lockfile.md --path docs/plan.md --path specs/rigorloop-cli-lockfile.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml`
- Expected observable result: successful non-dry-run Codex init creates or updates `rigorloop.lock` after verification, and failed verification paths leave the lockfile absent or unchanged.
- Commit message: `M2: write lockfile after verified codex init`
- Milestone closeout:
  - validation passed: yes for implementation handoff
  - progress updated: yes
  - decision log updated if needed
  - validation notes updated: yes
  - milestone committed: no; commit not created in this handoff
  - code-review: `code-review-r3` requested changes for `CR3-F1`; fix implemented; `code-review-r4` approved M2 with no material findings
- Risks: lockfile write failure after adapter install can leave generated output installed without recorded lockfile state.
- Rollback/recovery: report the lockfile write failure explicitly, do not claim lockfile success, and require manual rerun or repair under a later approved command if needed.

### M3. Drift and conflict blocking for existing lockfile state

- Milestone state: closed
- Goal: protect existing generated output represented in `rigorloop.lock` before destructive replacement.
- Requirements: R46-R53, R58-R61, R66, AC4, AC7, AC8, AC12, AC13
- Files/components likely touched: `packages/rigorloop/dist/bin/rigorloop.js`, lockfile helper, `packages/rigorloop/test/cli.test.js`
- Dependencies: M2 closed
- Tests to add/update:
  - existing generated output matching recorded tree hash allows unchanged or update behavior;
  - modified generated output reports drift and blocks destructive replacement by default;
  - missing installed root represented in the lockfile reports drift or missing generated output before replacement;
  - install root path existing as a file exits `5`;
  - generated file path existing as a directory exits `5`;
  - drift output includes adapter, installed root, expected tree hash, and actual tree hash when available;
  - unsupported future lockfile shape still blocks before generated-output mutation.
- Implementation steps:
  - Compute current installed tree hash before extraction when an existing supported lockfile records Codex output.
  - Compare current tree hash to the recorded tree hash and block destructive replacement on mismatch.
  - Detect missing roots and file/directory conflicts before extraction.
  - Return stable blocker/error codes and exit classes for drift and mutation conflicts.
  - Keep `--force` from bypassing lockfile drift or arbitrary lockfile replacement in this slice.
- Validation commands:
  - `npm test --prefix packages/rigorloop`
  - drift fixture commands covering modified, missing, and conflicting `.agents/skills` state
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path docs/plans/2026-05-16-rigorloop-cli-lockfile.md --path docs/plan.md --path specs/rigorloop-cli-lockfile.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml`
- Expected observable result: existing generated output cannot be overwritten when it diverges from lockfile-recorded state, and conflict paths use the approved exit-code classes.
- Commit message: `M3: block drifted lockfile adapter output`
- Milestone closeout:
  - validation passed: yes for implementation handoff
  - progress updated: yes
  - decision log updated if needed
  - validation notes updated: yes
  - milestone committed: no; commit not created in this handoff
  - code-review: `code-review-r5` approved M3 with no material findings
- Risks: path-level changed-file reporting can distract from the tree-hash contract.
- Rollback/recovery: require exact tree-hash blocker output first; changed-file lists remain best-effort only when available without weakening the contract.

### Lifecycle closeout

- Milestone state: closed
- Goal: complete downstream evidence after all implementation milestones are closed.
- Requirements: all acceptance criteria AC1-AC13
- Files/components likely touched: active plan, change-local explain-change/verify artifacts, PR handoff text
- Dependencies: M1-M3 closed and required review-resolution closed if any code-review finding is material
- Tests to add/update: none unless final validation exposes a gap
- Implementation steps:
  - Run final selected validation named by the test spec and this plan.
  - Record explain-change evidence.
  - Run verify.
  - Prepare PR handoff only after verify owns branch-ready.
- Validation commands:
  - final selected CI from the test spec
  - `npm test --prefix packages/rigorloop`
  - `git diff --check -- <touched paths>`
- Expected observable result: final closeout evidence exists and plan/index lifecycle state is synchronized before PR handoff.
- Commit message: `Close out rigorloop CLI lockfile`
- Milestone closeout:
  - validation passed: yes
  - progress updated: yes
  - decision log updated if needed: yes
  - validation notes updated: yes
  - milestone committed if needed: PR #63 merged
- Risks: final validation may expose selector coverage gaps for the new package path or lockfile test cases.
- Rollback/recovery: add selector coverage or explicitly route package validation in the test spec and plan before claiming final readiness.

## Validation plan

- Plan-stage validation:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-16-rigorloop-cli-lockfile.md --path docs/plan.md --path specs/rigorloop-cli-lockfile.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path docs/plans/2026-05-16-rigorloop-cli-lockfile.md --path docs/plan.md --path specs/rigorloop-cli-lockfile.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml`
- Implementation-stage validation:
  - `npm test --prefix packages/rigorloop`
  - fixture-based CLI commands for dry-run, network install, local archive install, successful lockfile write, failed verification no-write, unsupported shape blocking, and drift blocking
  - selected CI over package paths, spec/test-spec, plan, and change-local artifacts
- Review and closeout validation:
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-15-rigorloop-cli-lockfile`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-15-rigorloop-cli-lockfile` when material findings exist or review-resolution changes
  - `git diff --check -- <touched paths>`

## Risks and recovery

- YAML parsing and serialization may become too broad. Recovery: keep support limited to the strict schema shape; add a dependency only if the implementation records a decision and tests the public behavior.
- Lockfile write failure after adapter install may create partial success. Recovery: report the lockfile failure explicitly, do not claim lockfile success, and leave repair to a later approved command.
- Existing generated output drift can be destructive if checked too late. Recovery: compute drift before extraction when a supported lockfile entry exists.
- Local archive paths may leak into durable state. Recovery: serialize only the archive basename and test against absolute path leakage.
- Older or future lockfiles may be accidentally rewritten. Recovery: block on unknown shape, unsupported schema, unsupported adapters, unsupported source values, and unsupported tree hash algorithms before mutation.
- Tree hashing could differ across platforms. Recovery: normalize paths to POSIX, normalize generated text bytes, exclude directories/symlinks/metadata, and test deterministic fixtures.

## Dependencies

- Plan-review must approve this plan before test-spec.
- Test spec must map each lockfile `MUST` and acceptance criterion to concrete tests before implementation.
- The implementation builds on the existing first-slice CLI package and Codex adapter verification flow.
- Public npm publication remains blocked by a separate release-hardening slice.
- Future lockfile migration, repair, `status`, `validate`, and non-Codex adapters require later specs.

## Progress

- 2026-05-16: plan created after approved spec, approved architecture update, accepted ADR, and clean architecture-review.
- 2026-05-16: plan-review-r1 approved the plan with no material findings.
- 2026-05-16: test spec created at `specs/rigorloop-cli-lockfile.test.md`; next stage is implement M1.
- 2026-05-16: M1 implementation started.
- 2026-05-16: M1 added strict lockfile schema parsing/serialization, normalized manifest hashing, lockfile write-plan entries, and pre-mutation blocking for invalid or unsupported existing `rigorloop.lock`; M1 package tests passed and the milestone is ready for code-review.
- 2026-05-16: code-review-r1 requested changes for CR1-F1; M1 parser accepts unknown nested mapping fields that must block as unsupported lockfile shape.
- 2026-05-16: CR1-F1 fix implemented by detecting unknown nested mapping keys in known lockfile sections and adapter entries; focused and full package tests passed, and M1 returned to code-review.
- 2026-05-16: code-review-r2 approved M1 with no material findings; CR1-F1 resolved and M1 closed. Next stage is implement M2.
- 2026-05-16: M2 implemented durable lockfile creation/update after verified Codex init, source-mode recording for network/local archive installs, portable local archive lockfile output, warning removal, and no-write behavior on failed verification. M2 package tests passed and the milestone is ready for code-review.
- 2026-05-16: code-review-r3 requested changes for CR3-F1; M2 can write a lockfile whose installed tree hash includes unrelated pre-existing files under `.agents/skills`.
- 2026-05-16: CR3-F1 fix implemented by verifying the installed Codex adapter tree against trusted metadata before lockfile writes and adding regression coverage for extra, modified, partial, exact, and existing-lockfile mismatch cases. M2 returned to code-review.
- 2026-05-16: code-review-r4 approved M2 with no material findings; M2 is closed and the next stage is implement M3.
- 2026-05-16: M3 implemented lockfile-recorded generated output drift preflight, missing-output blocking, and generated output file/directory conflict handling. M3 package tests passed and the milestone is ready for code-review.
- 2026-05-16: code-review-r5 approved M3 with no material findings. All implementation milestones are closed, and the next stage is explain-change.
- 2026-05-16: explain-change recorded the durable rationale for the lockfile implementation. The next stage is verify.
- 2026-05-16: final local verify passed for the durable lockfile change; branch-ready evidence is recorded and the next stage is PR handoff.
- 2026-05-16: PR #63 opened for the durable lockfile change; hosted CI and human review are pending.
- 2026-05-16: PR #63 merged. The durable lockfile plan is complete, and `FU-004` is closed.

## Decision log

- 2026-05-16: split implementation into schema/serialization, verified write/update, and drift/conflict milestones so each review loop has one main failure domain.
- 2026-05-16: keep lockfile parsing strict in the plan; unknown preservation and migration remain future work per spec.

## Surprises and discoveries

- 2026-05-16: Existing first-slice tests still asserted the old planned-lockfile top-level `tree_hash_algorithm`; M1 updated them to assert the approved complete `generated.adapters[]` shape.
- 2026-05-16: M2 code-review found that archive tree verification before extraction is not enough for lockfile durability; post-extraction installed-tree verification must reject unrelated or extra files before writing `rigorloop.lock`.
- 2026-05-16: M3 separates lockfile-recorded drift from first-install tree verification: once `rigorloop.lock` records Codex output, mismatches report `generated-output-drift` or `generated-output-missing` before replacement rather than recreating or rewriting files.

## Validation notes

- 2026-05-16: `npm test --prefix packages/rigorloop -- --test-name-pattern 'TLF-'` passed.
- 2026-05-16: `npm test --prefix packages/rigorloop` passed.
- 2026-05-16: `python scripts/validate-change-metadata.py docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml` passed.
- 2026-05-16: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path packages/rigorloop/dist/bin/rigorloop.js --path packages/rigorloop/dist/lib/lockfile.js --path packages/rigorloop/test/cli.test.js --path docs/plans/2026-05-16-rigorloop-cli-lockfile.md --path docs/plan.md --path specs/rigorloop-cli-lockfile.md --path specs/rigorloop-cli-lockfile.test.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml` passed.
- 2026-05-16: `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path docs/plans/2026-05-16-rigorloop-cli-lockfile.md --path docs/plan.md --path specs/rigorloop-cli-lockfile.md --path specs/rigorloop-cli-lockfile.test.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml` passed.
- 2026-05-16: `npm test --prefix packages/rigorloop -- --test-name-pattern 'TLF-005|TLF-006|TLF-007'` passed for CR1-F1 regression coverage.
- 2026-05-16: `npm test --prefix packages/rigorloop` passed after the CR1-F1 fix.
- 2026-05-16: `npm test --prefix packages/rigorloop -- --test-name-pattern 'TLF-012|TLF-013|TLF-014|TLF-015|T18|T20|T41'` initially failed before M2 implementation because actual init still emitted `lockfile-spec-not-approved` and did not write `rigorloop.lock`.
- 2026-05-16: `npm test --prefix packages/rigorloop` passed after the M2 implementation.
- 2026-05-16: `python scripts/validate-change-metadata.py docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml` passed after the M2 implementation.
- 2026-05-16: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path packages/rigorloop/dist/bin/rigorloop.js --path packages/rigorloop/dist/lib/lockfile.js --path packages/rigorloop/test/cli.test.js --path docs/plans/2026-05-16-rigorloop-cli-lockfile.md --path docs/plan.md --path specs/rigorloop-cli-lockfile.md --path specs/rigorloop-cli-lockfile.test.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml` passed after the M2 implementation.
- 2026-05-16: `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path docs/plans/2026-05-16-rigorloop-cli-lockfile.md --path docs/plan.md --path specs/rigorloop-cli-lockfile.md --path specs/rigorloop-cli-lockfile.test.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml` passed after the M2 implementation.
- 2026-05-16: `git diff --check -- packages/rigorloop/dist/bin/rigorloop.js packages/rigorloop/dist/lib/lockfile.js packages/rigorloop/test/cli.test.js docs/plans/2026-05-16-rigorloop-cli-lockfile.md docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml` passed.
- 2026-05-16: code-review-r3 manual probe created a temp project with `.agents/skills/custom/NOTE.md`; `node packages/rigorloop/dist/bin/rigorloop.js init --adapter codex --json` returned success and wrote a lockfile with `file_count: 24`, proving CR3-F1.
- 2026-05-16: `python scripts/validate-review-artifacts.py docs/changes/2026-05-15-rigorloop-cli-lockfile` passed after recording code-review-r3.
- 2026-05-16: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-15-rigorloop-cli-lockfile/reviews/code-review-r3.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/review-log.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/review-resolution.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml --path docs/plans/2026-05-16-rigorloop-cli-lockfile.md --path docs/plan.md` passed after recording code-review-r3.
- 2026-05-16: `bash scripts/ci.sh --mode explicit --path docs/changes/2026-05-15-rigorloop-cli-lockfile/reviews/code-review-r3.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/review-log.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/review-resolution.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml --path docs/plans/2026-05-16-rigorloop-cli-lockfile.md --path docs/plan.md --path packages/rigorloop --path specs/rigorloop-cli-lockfile.md --path specs/rigorloop-cli-lockfile.test.md` passed after recording code-review-r3.
- 2026-05-16: `npm test --prefix packages/rigorloop -- --test-name-pattern 'CR3-F1|T26 adapter file|TLF-020|TLF-021'` passed after the CR3-F1 fix.
- 2026-05-16: `npm test --prefix packages/rigorloop` passed after the CR3-F1 fix.
- 2026-05-16: `python scripts/validate-review-artifacts.py docs/changes/2026-05-15-rigorloop-cli-lockfile` passed after the CR3-F1 fix.
- 2026-05-16: `python scripts/validate-change-metadata.py docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml` passed after the CR3-F1 fix.
- 2026-05-16: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path packages/rigorloop/dist/bin/rigorloop.js --path packages/rigorloop/dist/lib/lockfile.js --path packages/rigorloop/test/cli.test.js --path specs/rigorloop-cli-lockfile.test.md --path docs/plans/2026-05-16-rigorloop-cli-lockfile.md --path docs/plan.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml --path docs/changes/2026-05-15-rigorloop-cli-lockfile/review-log.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/review-resolution.md` passed after the CR3-F1 fix.
- 2026-05-16: `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path docs/plans/2026-05-16-rigorloop-cli-lockfile.md --path docs/plan.md --path specs/rigorloop-cli-lockfile.md --path specs/rigorloop-cli-lockfile.test.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml --path docs/changes/2026-05-15-rigorloop-cli-lockfile/review-log.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/review-resolution.md` passed after the CR3-F1 fix.
- 2026-05-16: `git diff --check -- packages/rigorloop/dist/bin/rigorloop.js packages/rigorloop/test/cli.test.js specs/rigorloop-cli-lockfile.test.md docs/plans/2026-05-16-rigorloop-cli-lockfile.md docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml docs/changes/2026-05-15-rigorloop-cli-lockfile/review-log.md docs/changes/2026-05-15-rigorloop-cli-lockfile/review-resolution.md` passed after the CR3-F1 fix.
- 2026-05-16: `python scripts/validate-review-artifacts.py docs/changes/2026-05-15-rigorloop-cli-lockfile` passed after recording code-review-r4.
- 2026-05-16: `python scripts/validate-change-metadata.py docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml` passed after recording code-review-r4.
- 2026-05-16: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-15-rigorloop-cli-lockfile/reviews/code-review-r4.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/review-log.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/review-resolution.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml --path docs/plans/2026-05-16-rigorloop-cli-lockfile.md --path docs/plan.md` passed after recording code-review-r4.
- 2026-05-16: `bash scripts/ci.sh --mode explicit --path docs/changes/2026-05-15-rigorloop-cli-lockfile/reviews/code-review-r4.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/review-log.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/review-resolution.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml --path docs/plans/2026-05-16-rigorloop-cli-lockfile.md --path docs/plan.md --path packages/rigorloop --path specs/rigorloop-cli-lockfile.md --path specs/rigorloop-cli-lockfile.test.md` passed after recording code-review-r4.
- 2026-05-16: `npm test --prefix packages/rigorloop -- --test-name-pattern 'TLF-023|TLF-024|TLF-025|TLF-026|TLF-027'` passed after M3 implementation.
- 2026-05-16: `npm test --prefix packages/rigorloop` passed after M3 implementation.
- 2026-05-16: `python scripts/validate-change-metadata.py docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml` passed after M3 implementation.
- 2026-05-16: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path packages/rigorloop/dist/bin/rigorloop.js --path packages/rigorloop/dist/lib/lockfile.js --path packages/rigorloop/test/cli.test.js --path docs/plans/2026-05-16-rigorloop-cli-lockfile.md --path docs/plan.md --path specs/rigorloop-cli-lockfile.md --path specs/rigorloop-cli-lockfile.test.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml` passed after M3 implementation.
- 2026-05-16: `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path docs/plans/2026-05-16-rigorloop-cli-lockfile.md --path docs/plan.md --path specs/rigorloop-cli-lockfile.md --path specs/rigorloop-cli-lockfile.test.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml` passed after M3 implementation.
- 2026-05-16: `git diff --check -- packages/rigorloop/dist/bin/rigorloop.js packages/rigorloop/test/cli.test.js docs/plans/2026-05-16-rigorloop-cli-lockfile.md docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml` passed after M3 implementation.
- 2026-05-16: `python scripts/validate-review-artifacts.py docs/changes/2026-05-15-rigorloop-cli-lockfile` passed after recording code-review-r5.
- 2026-05-16: `python scripts/validate-change-metadata.py docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml` passed after recording code-review-r5.
- 2026-05-16: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-15-rigorloop-cli-lockfile/reviews/code-review-r5.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/review-log.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/review-resolution.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml --path docs/plans/2026-05-16-rigorloop-cli-lockfile.md --path docs/plan.md` passed after recording code-review-r5.
- 2026-05-16: `bash scripts/ci.sh --mode explicit --path docs/changes/2026-05-15-rigorloop-cli-lockfile/reviews/code-review-r5.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/review-log.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/review-resolution.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml --path docs/plans/2026-05-16-rigorloop-cli-lockfile.md --path docs/plan.md --path packages/rigorloop --path specs/rigorloop-cli-lockfile.md --path specs/rigorloop-cli-lockfile.test.md` passed after recording code-review-r5.
- 2026-05-16: `git diff --check -- docs/changes/2026-05-15-rigorloop-cli-lockfile/reviews/code-review-r5.md docs/changes/2026-05-15-rigorloop-cli-lockfile/review-log.md docs/changes/2026-05-15-rigorloop-cli-lockfile/review-resolution.md docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml docs/plans/2026-05-16-rigorloop-cli-lockfile.md` passed after recording code-review-r5.
- 2026-05-16: `python scripts/validate-change-metadata.py docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml` passed after recording explain-change.
- 2026-05-16: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-15-rigorloop-cli-lockfile/explain-change.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml --path docs/plans/2026-05-16-rigorloop-cli-lockfile.md --path docs/plan.md` passed after recording explain-change.
- 2026-05-16: `bash scripts/ci.sh --mode explicit --path docs/changes/2026-05-15-rigorloop-cli-lockfile/explain-change.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml --path docs/plans/2026-05-16-rigorloop-cli-lockfile.md --path docs/plan.md --path packages/rigorloop --path specs/rigorloop-cli-lockfile.md --path specs/rigorloop-cli-lockfile.test.md` passed after recording explain-change.
- 2026-05-16: `git diff --check -- docs/changes/2026-05-15-rigorloop-cli-lockfile/explain-change.md docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml docs/plans/2026-05-16-rigorloop-cli-lockfile.md` passed after recording explain-change.
- 2026-05-16: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-15-rigorloop-cli-lockfile` passed during final verify.
- 2026-05-16: `python scripts/validate-change-metadata.py docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml` passed during final verify.
- 2026-05-16: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path packages/rigorloop/dist/bin/rigorloop.js --path packages/rigorloop/dist/lib/lockfile.js --path packages/rigorloop/test/cli.test.js --path specs/rigorloop-cli-lockfile.md --path specs/rigorloop-cli-lockfile.test.md --path docs/architecture/system/architecture.md --path docs/architecture/system/diagrams/container.mmd --path docs/adr/ADR-20260516-rigorloop-cli-lockfile.md --path docs/follow-ups.md --path docs/learn/sessions/2026-05-15-follow-up-register-activation-and-closeout.md --path docs/plans/2026-05-16-rigorloop-cli-lockfile.md --path docs/plan.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml --path docs/changes/2026-05-15-rigorloop-cli-lockfile/explain-change.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/review-log.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/review-resolution.md` passed during final verify.
- 2026-05-16: `npm test --prefix packages/rigorloop` passed during final verify with 60 tests passing.
- 2026-05-16: final selected CI passed during final verify for package, lockfile specs, architecture, ADR, follow-up register, learn session, plan, change metadata, explain-change, and review artifacts.
- 2026-05-16: final `git diff --check -- <changed paths>` passed during final verify.

## Outcome and retrospective

- Final local verify passed on 2026-05-16. PR #63 passed hosted CI and human review, merged on 2026-05-16, and closed `FU-004`.

## Readiness

- Completed.
