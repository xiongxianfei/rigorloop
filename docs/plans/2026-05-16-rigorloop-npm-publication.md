# RigorLoop npm publication

- Status: active
- Owner: maintainer
- Start date: 2026-05-16
- Last updated: 2026-05-16
- Related issue or PR: PR #65 (`https://github.com/xiongxianfei/rigorloop/pull/65`)
- Supersedes: none

## Goal

Publish the first public npm package `@xiongxianfei/rigorloop@0.1.4` from repository tag `v0.1.4` without adding new CLI feature behavior, weakening adapter release verification, or turning npm package contents into canonical source.

## Why now

The CLI package, Codex init, durable lockfile, and `new-change` scaffolding slices are merged. Users still cannot install the intended public package through npm. FU-010 is now the release-hardening blocker that must close before public npm publication; FU-006 through FU-009 remain deferred.

## Source Artifacts

- Proposal: [First public npm release](../proposals/2026-05-16-first-public-npm-release.md)
- Spec: [RigorLoop npm Publication](../../specs/rigorloop-npm-publication.md)
- Architecture: [Canonical system architecture](../architecture/system/architecture.md)
- ADR: [ADR-20260516 RigorLoop npm publication](../adr/ADR-20260516-rigorloop-npm-publication.md)
- Change metadata: [change.yaml](../changes/2026-05-16-first-public-npm-release/change.yaml)
- Test spec: [RigorLoop npm Publication Test Spec](../../specs/rigorloop-npm-publication.test.md), active and approved by maintainer

## Context And Orientation

The npm package lives under `packages/rigorloop`. It currently exposes one `rigorloop` binary, but its package metadata is still a candidate shape: version `0.1.3`, `private: true`, and no package-local `LICENSE`.

The runtime CLI code is shipped from `packages/rigorloop/dist/`. Adapter archives are not npm package contents. The CLI verifies Codex adapter archives using bundled metadata under `packages/rigorloop/dist/metadata/` and downloads official GitHub release archive URLs only.

The existing release workflow is `.github/workflows/release.yml`. It currently runs `bash scripts/release-verify.sh "$GITHUB_REF_NAME"` and creates GitHub releases, but it does not publish npm, run packed-package smoke, or request npm trusted-publishing OIDC permissions.

The maintainer release gate is `bash scripts/release-verify.sh <tag>`. It currently accepts releases through `v0.1.3`, builds adapter release archives for `v0.1.2` and `v0.1.3`, and delegates release metadata validation to `scripts/validate-release.py`.

Publication evidence must be recorded at `docs/releases/v0.1.4/npm-publication.md`. FU-010 may close only after public publication and real non-dry-run Codex adapter install proof from the packed or published package. Dry-run smoke is not enough.

## Scope

### In Scope

- Prepare `packages/rigorloop` for `@xiongxianfei/rigorloop@0.1.4` publication.
- Add deterministic package-content validation for the npm tarball.
- Add packed-package smoke that executes the installed package binary.
- Extend release verification and release workflow gates for `v0.1.4`.
- Support exactly one publication mode per version: trusted publishing or bootstrap.
- Add release notes, release metadata, and publication evidence surfaces for `v0.1.4`.
- Prove or record the required real Codex adapter install smoke before FU-010 closeout.

### Out Of Scope

- No `rigorloop status`.
- No `rigorloop validate`.
- No workflow YAML canonicality.
- No generated workflow docs or frozen workflow drift checks.
- No new adapter packaging behavior.
- No adapter ZIP archives bundled into npm.
- No new CLI feature behavior beyond publication hardening and release validation.

## Requirements Covered

- Release identity: R1-R9.
- Public binary surface: R10-R16.
- Package content allowlist and forbidden paths: R17-R27.
- Dependency and lifecycle-script policy: R28-R34.
- Release gate and workflow publication modes: R35-R47.
- Trusted publishing and bootstrap constraints: R48-R61d.
- Packed-package smoke: R62-R69.
- Real Codex adapter install proof: R69a-R69m.
- Release artifacts and publication evidence: R70-R80.
- Post-publication verification: R81-R85.
- Invariants and error boundaries: S1-S6 and EB1-EB14.

## Current Handoff Summary

- Current milestone: M6b. Publication Execution And Evidence Closeout
- Current milestone state: planned
- Last reviewed milestone: M5. Documentation, Follow-Up State, And Final Local Readiness
- Review status: M6a repository-local readiness proof reviewed clean; no material findings
- Remaining in-scope implementation milestones: none
- Lifecycle-closeout milestones: M6a, M6b
- Next stage: create `v0.1.4` tag from merged commit `8221134e08674040b05145241b20fbfcf0c530cf`, then run selected publication mode
- Final closeout readiness: not ready
- Reason final closeout is not ready: M6b is not complete, npm publication has not happened, and FU-010 cannot close without public publication evidence plus real Codex adapter install proof.

## Milestones

### M1. Package Metadata And Runtime Tarball Contract

- Milestone state: closed
- Goal: make the package metadata match the first public release identity and define the runtime allowlist at package level.
- Requirements: R1-R27, R28-R34, EB1-EB5.
- Files/components likely touched:
  - `packages/rigorloop/package.json`
  - `packages/rigorloop/LICENSE`
  - `packages/rigorloop/README.md`
  - `packages/rigorloop/dist/metadata/adapter-artifacts-v0.1.4.json`
  - `packages/rigorloop/dist/metadata/releases.json`
  - `packages/rigorloop/test/cli.test.js`
- Dependencies: approved spec and architecture; no npm credentials required.
- Tests to add/update:
  - package version is `0.1.4`;
  - package has no `private: true`;
  - exactly one `bin` entry maps `rigorloop` to `dist/bin/rigorloop.js`;
  - package-local `LICENSE` exists;
  - `files` includes runtime surfaces and excludes adapter archives and generated adapter bodies;
  - forbidden lifecycle scripts and unjustified runtime dependencies are rejected.
- Implementation steps:
  - Update package identity to `0.1.4`.
  - Remove candidate-only publication blockers after package-policy tests exist.
  - Add package-local license and ensure README wording no longer says public npm publication remains blocked once controls are in place.
  - Update bundled metadata filenames and release-index mapping for `v0.1.4`.
- Validation commands:
  - `npm test --prefix packages/rigorloop`
  - `git diff --check -- packages/rigorloop`
- Expected observable result: package metadata is publishable only as `@xiongxianfei/rigorloop@0.1.4` and still exposes one binary.
- Commit message: `M1: prepare rigorloop package metadata for npm publication`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] hand off to code-review for M1
  - [x] material findings resolved or explicitly dispositioned
  - [x] milestone state updated before starting M2
  - [x] progress, decision log, and validation notes updated
- Risks:
  - Version references in tests and lockfile fixtures may still expect `0.1.3`.
  - Metadata may reference `v0.1.4` release assets that are not generated yet.
- Rollback/recovery:
  - Revert package identity changes before publication if validation exposes incompatible metadata.
  - Keep metadata changes scoped so `v0.1.3` release evidence remains historical.

Implementation notes:

- 2026-05-16: M1 implementation started after test spec approval. Same-slice target is package metadata, package-local license, package allowlist policy assertions, and bundled metadata mapping for `v0.1.4`; package-content tarball inspection remains M2.
- 2026-05-16: M1 implementation updated package metadata to `0.1.4`, removed `private: true`, added package-local license coverage, tightened package policy tests, and switched bundled release metadata lookup to `v0.1.4`. Full tarball inspection and packed-package smoke remain M2.
- 2026-05-16: M1 code-review completed clean with no material findings in `docs/changes/2026-05-16-first-public-npm-release/reviews/code-review-r1.md`.

### M2. Package-Content Validation And Packed-Package Smoke

- Milestone state: closed
- Goal: add deterministic proof that the package tarball contains only intentional runtime files and works when installed from the packed tarball.
- Requirements: R17-R27, R62-R69, EB5-EB6.
- Files/components likely touched:
  - `scripts/validate-npm-package.py` or an equivalent package-content validator
  - `scripts/test-npm-package-publication.py` or package-local tests
  - `scripts/validation_selection.py`
  - `scripts/test-select-validation.py`
  - `packages/rigorloop/test/cli.test.js`
  - `specs/rigorloop-npm-publication.test.md` after test-spec stage creates it
- Dependencies: M1 package metadata and allowlist.
- Tests to add/update:
  - tarball includes required runtime files;
  - tarball rejects forbidden paths, adapter ZIPs, `.tgz`, secrets, `.codex`, `.agents`, tests, fixtures, docs, and `dist/adapters/**`;
  - packed tarball install exposes `rigorloop`;
  - installed binary supports `--help`, `version`, `init --adapter codex --dry-run --json`, and `new-change ... --dry-run --json`;
  - JSON-mode output remains JSON-only and exit codes remain stable.
- Implementation steps:
  - Add tarball inspection that reads `npm pack --json` or the packed `.tgz` manifest directly.
  - Add smoke helper that installs the generated tarball into a temporary project and executes `node_modules/.bin/rigorloop`.
  - Wire the package-content and smoke checks into selected validation.
- Validation commands:
  - `npm test --prefix packages/rigorloop`
  - `npm pack --dry-run --prefix packages/rigorloop`
  - `npm pack --prefix packages/rigorloop`
  - packed install smoke command from the test-spec
  - `python scripts/test-select-validation.py`
  - `git diff --check -- packages/rigorloop scripts`
- Expected observable result: a maintainer can inspect and test the exact package shape before npm publication.
- Commit message: `M2: add npm tarball validation and packed smoke`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] hand off to code-review for M2
  - [x] material findings resolved or explicitly dispositioned
  - [x] milestone state updated before starting M3
  - [x] progress, decision log, and validation notes updated
- Risks:
  - `npm pack` output can include npm-required files even when not explicitly listed in `files`.
  - Packed smoke can be brittle if it depends on registry or network behavior.
- Rollback/recovery:
  - Keep packed smoke local to tarball install for M2; move real network adapter install proof to M5/M6.

Implementation notes:

- 2026-05-16: M2 implementation started after clean M1 code-review. Same-slice target is deterministic tarball inspection, package policy validation, packed-package smoke from an installed tarball, and selector/CI routing for the new npm publication check.
- 2026-05-16: M2 implementation added `scripts/npm_package_validation.py`, `scripts/validate-npm-package.py`, and `scripts/test-npm-package-publication.py`. The tests inspect the actual packed `.tgz`, reject forbidden tarball paths, validate package lifecycle/dependency policy, install the packed tarball into a temporary project, and execute the installed `node_modules/.bin/rigorloop` for help/version/init/new-change dry-run smoke.
- 2026-05-16: M2 wired `npm_package_publication.test` into the validation selector for `packages/rigorloop/**` and npm-package validation scripts, so selected CI runs both package CLI tests and packed-package publication tests for package changes.
- 2026-05-16: M2 code-review recorded CR2-F1. The validator misses root-level forbidden archive and secret-like files because Python `fnmatch` does not treat `**` as zero-or-more directories.
- 2026-05-16: CR2-F1 fixed by adding direct root-level and nested forbidden path tests and replacing glob-dependent tarball path matching with explicit normalized package-relative checks for archives, secret-like files, local state, and generated adapter output.
- 2026-05-16: M2 code-review rerun completed clean with no material findings in `docs/changes/2026-05-16-first-public-npm-release/reviews/code-review-r3.md`; M2 is closed and the next stage is M3 implementation.

### M3. Release Verification And v0.1.4 Release Evidence

- Milestone state: closed
- Goal: make the repository release gate understand `v0.1.4`, including npm package checks, release notes, release metadata, adapter archive output, and real-install evidence requirements.
- Requirements: R4, R9, R35, R69a-R69m, R70-R80, R81-R85, S1-S6, EB7, EB13-EB14.
- Files/components likely touched:
  - `scripts/release-verify.sh`
  - `scripts/validate-release.py`
  - `scripts/test-adapter-distribution.py`
  - `docs/releases/v0.1.4/release.yaml`
  - `docs/releases/v0.1.4/release-notes.md`
  - `docs/releases/v0.1.4/npm-publication.md`
  - `docs/reports/adapter-artifacts/releases/v0.1.4.yaml`
  - `packages/rigorloop/dist/metadata/adapter-artifacts-v0.1.4.json`
  - `packages/rigorloop/dist/metadata/releases.json`
- Dependencies: M1 metadata and M2 package validation.
- Tests to add/update:
  - `release-verify.sh v0.1.4` invokes required release checks;
  - release metadata records npm version to adapter release mapping;
  - release notes contain quick-start, pinned, and local install npm usage;
  - publication evidence has the required shape and blocks FU-010 closeout while actual install smoke is pending;
  - actual install smoke records pass only after real non-dry-run Codex install verifies official archive URL, SHA-256, size when present, extraction root, tree hash, and generated files.
- Implementation steps:
  - Add `v0.1.4` as a supported release target.
  - Ensure adapter archive generation/validation emits the `v0.1.4` Codex archive and metadata needed by the CLI.
  - Add release evidence templates with clear pending fields before publication.
  - Add release validation that distinguishes publication-complete from FU-010-closeout-complete when real install smoke is pending.
- Validation commands:
  - `bash scripts/release-verify.sh v0.1.4`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-release.py --version v0.1.4 --release-output-dir <release-output-dir> --release-commit <commit>`
  - `git diff --check -- scripts docs/releases packages/rigorloop/dist/metadata`
- Expected observable result: `v0.1.4` release readiness includes both adapter archive proof and npm publication evidence requirements.
- Commit message: `M3: add v0.1.4 release verification and evidence`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] hand off to code-review for M3
  - [x] material findings resolved or explicitly dispositioned
  - [x] milestone state updated before starting M4
  - [x] progress, decision log, and validation notes updated
- Risks:
  - Official GitHub release assets may not be externally observable until after release creation.
  - Publication evidence must not falsely close FU-010 before actual install smoke passes.
- Rollback/recovery:
  - Use the ordering-gap path from the spec and keep FU-010 open when assets or npm publication are pending.

Implementation notes:

- 2026-05-16: M3 implementation added `v0.1.4` to the release target map and release gate, including npm package publication validation and packed-package smoke through `python scripts/test-npm-package-publication.py`.
- 2026-05-16: M3 added `docs/releases/v0.1.4/release.yaml`, `release-notes.md`, and `npm-publication.md` in `pending-publication` state. The evidence records bootstrap as the selected pre-publication mode, `npm.published: false`, and `adapter_install_smoke.result: pending` with `fu_010_closeout_blocked: true`, so FU-010 remains open.
- 2026-05-16: M3 added `docs/reports/adapter-artifacts/releases/v0.1.4.yaml`, updated `dist/adapters/manifest.yaml` to `v0.1.4`, and refreshed bundled Codex metadata SHA/size/tree-hash values for the generated `v0.1.4` Codex archive.
- 2026-05-16: M3 code-review completed clean with no material findings in `docs/changes/2026-05-16-first-public-npm-release/reviews/code-review-r4.md`; M3 is closed and the next stage is M4 implementation.

### M4. Release Workflow And Publication Mode Gates

- Milestone state: closed
- Goal: update release automation so npm publication uses exactly one mode and trusted publishing is the normal future path without duplicate publication risk.
- Requirements: R35-R61d, EB1-EB12.
- Files/components likely touched:
  - `.github/workflows/release.yml`
  - `scripts/release-verify.sh`
  - release validation scripts/tests from M2/M3
  - `docs/releases/v0.1.4/npm-publication.md`
- Dependencies: M2 package smoke and M3 release validation.
- Tests to add/update:
  - stable `v0.1.4` tag may run npm publication gates;
  - release-candidate tags, branch events, PR events, unsupported tags, and version/tag mismatches do not publish npm;
  - trusted-publishing mode uses `id-token: write` only in the publish job and uses the npm public registry;
  - bootstrap mode records `published_by_workflow: false` and prevents the workflow from publishing the same version;
  - bootstrap requires complete tarball identity evidence and blocks on missing or mismatched SHA-256.
- Implementation steps:
  - Add workflow gating for stable semver npm publication.
  - Add publish job or publish-ready job according to selected mode handling without introducing a separate npm-only workflow.
  - Keep GitHub release archive behavior intact.
  - Add clear bootstrap instructions/evidence checks for the one-time first package claim.
- Validation commands:
  - `python scripts/test-adapter-distribution.py`
  - `bash scripts/release-verify.sh v0.1.4`
  - `bash scripts/ci.sh --mode explicit --path .github/workflows/release.yml --path scripts/release-verify.sh --path scripts/validate-release.py`
  - `git diff --check -- .github/workflows/release.yml scripts docs/releases/v0.1.4/npm-publication.md`
- Expected observable result: maintainers have one release workflow, one selected publication mode, and no duplicate npm publish path.
- Commit message: `M4: gate npm publication through release workflow policy`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] hand off to code-review for M4
  - [x] material findings resolved or explicitly dispositioned
  - [x] milestone state updated before starting M5
  - [x] progress, decision log, and validation notes updated
- Risks:
  - Trusted publishing may not be configurable before first package creation.
  - CI cannot prove npm account settings directly.
- Rollback/recovery:
  - Use bootstrap mode only for `0.1.4` when trusted publishing setup is unavailable before package creation.
  - Keep publication evidence blocking FU-010 until trusted publishing follow-up proof is recorded after bootstrap.

Implementation notes:

- 2026-05-16: M4 implementation started after clean M3 code-review. Same-slice target is release workflow gating, trusted-publishing job shape, v0.1.4 bootstrap non-publication by workflow, and stricter published bootstrap tarball identity validation.
- 2026-05-16: Added failing-first M4 tests for trusted npm workflow gating and published bootstrap identity. The tests initially failed because `release.yml` had no trusted npm publish job and published bootstrap evidence did not require a tarball SHA-256.
- 2026-05-16: M4 added a `publish-npm-trusted` job to `.github/workflows/release.yml` for future trusted-publishing releases. The job is skipped for `v0.1.4` bootstrap mode, rejects non-stable tags and package/tag version mismatches before publishing, requests `id-token: write` only in the publish job, uses the npm public registry, reruns `release-verify.sh`, and publishes `./packages/rigorloop` with provenance.
- 2026-05-16: M4 tightened published bootstrap evidence validation so bootstrap publication requires a concrete 64-hex tarball SHA-256 alongside approving maintainer and publish command proof.
- 2026-05-16: M4 code-review recorded `CR5-F1`. Published bootstrap evidence validation checks SHA shape but does not yet compare the recorded SHA-256 to actual packed tarball bytes, so M4 remains in `resolution-needed`.
- 2026-05-16: `CR5-F1` fixed. Bootstrap publication evidence validation now compares recorded `tarball.sha256` with the actual tarball bytes when the validator receives `--npm-tarball-root`, rejects mismatches and missing tarball files, and keeps pending-publication scaffold behavior non-blocking.
- 2026-05-16: M4 code-review rerun completed clean with no material findings in `docs/changes/2026-05-16-first-public-npm-release/reviews/code-review-r6.md`; M4 is closed and the next stage is M5 implementation.
- 2026-05-16: M5 implementation started after clean M4 code-review rerun. Same-slice target is durable explanation, current follow-up state, pending publication evidence, final local validation, and handoff to M5 code-review without claiming publication or FU-010 closeout.
- 2026-05-16: M5 added durable change rationale in `docs/changes/2026-05-16-first-public-npm-release/explain-change.md`, updated FU-010 to point at the active publication plan and final `npm-publication.md` evidence gate, and kept `docs/releases/v0.1.4/npm-publication.md` in `pending-publication` state. FU-006 through FU-009 remain open and deferred.
- 2026-05-16: M5 code-review completed clean with no material findings in `docs/changes/2026-05-16-first-public-npm-release/reviews/code-review-r7.md`; M5 is closed and the next stage is M6a pre-publication PR and merge readiness.

### M5. Documentation, Follow-Up State, And Final Local Readiness

- Milestone state: closed
- Goal: finish repository-side documentation and lifecycle state needed before publication execution.
- Requirements: R70-R85, R79-R80.
- Files/components likely touched:
  - `docs/releases/v0.1.4/release-notes.md`
  - `docs/releases/v0.1.4/release.yaml`
  - `docs/releases/v0.1.4/npm-publication.md`
  - `docs/follow-ups.md`
  - `docs/changes/2026-05-16-first-public-npm-release/change.yaml`
  - `docs/changes/2026-05-16-first-public-npm-release/explain-change.md`
  - this plan
- Dependencies: M1-M4 closed.
- Tests to add/update:
  - release notes contain all npm usage examples and source-of-truth boundary text;
  - publication evidence remains pending before actual publication;
  - FU-010 remains open until publication and actual install proof are recorded;
  - FU-006 through FU-009 remain open.
- Implementation steps:
  - Record durable explanation for the implemented release-hardening changes.
  - Run final repository-side verification before publication execution.
  - Keep the active plan and `docs/plan.md` synchronized with publication-pending state.
- Validation commands:
  - `npm test --prefix packages/rigorloop`
  - `bash scripts/release-verify.sh v0.1.4`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-first-public-npm-release/change.yaml`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-16-first-public-npm-release`
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path scripts/release-verify.sh --path scripts/validate-release.py --path .github/workflows/release.yml --path docs/releases/v0.1.4/release.yaml --path docs/releases/v0.1.4/release-notes.md --path docs/releases/v0.1.4/npm-publication.md --path docs/follow-ups.md --path specs/rigorloop-npm-publication.md --path docs/plans/2026-05-16-rigorloop-npm-publication.md --path docs/plan.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml`
  - `git diff --check -- packages/rigorloop scripts .github docs/releases/v0.1.4 docs/follow-ups.md docs/plans/2026-05-16-rigorloop-npm-publication.md docs/plan.md docs/changes/2026-05-16-first-public-npm-release`
- Expected observable result: the repository is ready for the publication execution gate, but the plan is not final-closed until publication evidence and real install proof exist.
- Commit message: `M5: prepare npm publication evidence and release docs`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] hand off to code-review for M5
  - [x] material findings resolved or explicitly dispositioned
  - [x] all implementation milestones closed
  - [x] progress, decision log, and validation notes updated
- Risks:
  - Publication evidence may need maintainer-only data that cannot exist before actual publish.
- Rollback/recovery:
  - Leave evidence fields pending and keep FU-010 open until maintainer publication completes.

### M6a. Pre-Publication PR And Merge Readiness

- Milestone state: closed
- Type: lifecycle-closeout
- Goal: close the repository implementation PR and make the `v0.1.4` release tag safe to create from the merged commit.
- Requirements: R35-R80, EB1-EB12.
- Dependencies: M1-M5 closed and all material review findings resolved.
- Closeout steps:
  - Complete explain-change for repository implementation changes.
  - Run verify for repository implementation changes.
  - Prepare PR handoff for the implementation branch.
  - Ensure package-content checks and packed-package smoke pass.
  - Ensure `docs/releases/v0.1.4/release.yaml` and `docs/releases/v0.1.4/release-notes.md` exist.
  - Ensure `docs/releases/v0.1.4/npm-publication.md` exists as a `pending-publication` evidence scaffold.
  - Ensure exactly one publication mode is selected: `trusted-publishing` or `bootstrap`.
  - Merge the implementation PR before creating the `v0.1.4` tag.
- Must not claim:
  - npm package is published;
  - npm package URL exists;
  - post-publication npx smoke passed;
  - FU-010 is closed.
- Validation commands:
  - `npm test --prefix packages/rigorloop`
  - `bash scripts/release-verify.sh v0.1.4`
  - `npm pack --dry-run --prefix packages/rigorloop`
  - `npm pack --prefix packages/rigorloop`
  - packed-package smoke command from the test spec
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-first-public-npm-release/change.yaml`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-16-first-public-npm-release`
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path scripts/release-verify.sh --path scripts/validate-release.py --path .github/workflows/release.yml --path docs/releases/v0.1.4/release.yaml --path docs/releases/v0.1.4/release-notes.md --path docs/releases/v0.1.4/npm-publication.md --path docs/follow-ups.md --path specs/rigorloop-npm-publication.md --path docs/plans/2026-05-16-rigorloop-npm-publication.md --path docs/plan.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml`
  - `git diff --check -- packages/rigorloop scripts .github docs/releases/v0.1.4 docs/follow-ups.md docs/plans/2026-05-16-rigorloop-npm-publication.md docs/plan.md docs/changes/2026-05-16-first-public-npm-release`
- Expected observable result: the implementation PR is merged, and maintainers may create `v0.1.4` from the merged commit. FU-010 remains open.
- Closeout checklist:
  - [x] M1-M5 closed
  - [x] explain-change completed
  - [x] verify completed
  - [x] PR handoff completed
  - [x] implementation PR merged
  - [x] `v0.1.4` tag authorized only from the merged commit
- Risks:
  - A tag created before merge could run stale release automation.
  - Pending publication evidence could be mistaken for final FU-010 closeout evidence.
- Rollback/recovery:
  - Do not tag until M6a is complete.
  - Keep `npm-publication.md` in `pending-publication` state until npm publication and real install smoke complete.

M6a notes:

- 2026-05-16: Repository-local M6a readiness proof passed: package tests, release verification, explicit npm pack/package validation, selected CI, and diff check. M6a remains open because verify, PR handoff, and implementation PR merge are separate closeout steps.
- 2026-05-16: M6a repository-local readiness proof code-review completed clean with no material findings in `docs/changes/2026-05-16-first-public-npm-release/reviews/code-review-r8.md`. M6a remains open for verify, PR handoff, implementation PR merge, and tag authorization.
- 2026-05-16: M6a verify completed for repository implementation changes. Branch-ready local verification passed, and M6a remains open for PR handoff, implementation PR merge, and tag authorization.
- 2026-05-16: PR handoff completed by opening PR #65: `https://github.com/xiongxianfei/rigorloop/pull/65`. M6a remains open for hosted CI/human review, implementation PR merge, and tag authorization from the merged commit.
- 2026-05-16: PR #65 passed hosted `ci` and merged at 2026-05-16T19:34:06Z with merge commit `8221134e08674040b05145241b20fbfcf0c530cf`. M6a is closed. Maintainers may create `v0.1.4` from the merged commit and proceed to M6b publication execution.

### M6b. Publication Execution And Evidence Closeout

- Milestone state: planned
- Type: lifecycle-closeout
- Goal: publish the package, prove the real public install path, commit final evidence, and close FU-010 only after tracked validation passes.
- Requirements: R36-R61d, R69a-R69m, R77-R85, EB9-EB14.
- Dependencies: M6a closed, implementation PR merged, `v0.1.4` tag created from the merged commit, maintainer npm access, official GitHub release assets, and selected publication mode.
- Publication steps:
  - Run the selected publication mode.
  - In trusted-publishing mode, `.github/workflows/release.yml` owns npm publication execution from the approved tag.
  - In bootstrap mode, `release.yml` owns release readiness but not npm publication execution for `0.1.4`; the maintainer manually publishes only the exact verified tarball from the merged commit, and `release.yml` must not also publish `@xiongxianfei/rigorloop@0.1.4`.
  - Publish `@xiongxianfei/rigorloop@0.1.4`.
  - Run post-publication `npm view`.
  - Run post-publication `npx @xiongxianfei/rigorloop@0.1.4 ...` smoke.
  - Run actual non-dry-run `init --adapter codex --json` in a temporary project.
  - Record npm publication evidence.
  - Record real Codex install smoke evidence.
  - Update `docs/releases/v0.1.4/npm-publication.md` to `published`.
  - Update `docs/follow-ups.md` to close FU-010 only after publication and actual install proof pass.
  - Update this plan and `docs/plan.md`.
  - Commit the evidence through a post-publication evidence PR unless repository governance explicitly approves another tracked commit path.
- Validation commands:
  - `bash scripts/release-verify.sh v0.1.4`
  - `npm view @xiongxianfei/rigorloop@0.1.4 --json`
  - `npx @xiongxianfei/rigorloop@0.1.4 --help`
  - `npx @xiongxianfei/rigorloop@0.1.4 version`
  - `npx @xiongxianfei/rigorloop@0.1.4 init --adapter codex --dry-run --json`
  - `npx @xiongxianfei/rigorloop@0.1.4 init --adapter codex --json`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/releases/v0.1.4/release.yaml --path docs/releases/v0.1.4/release-notes.md --path docs/releases/v0.1.4/npm-publication.md --path docs/follow-ups.md --path docs/plans/2026-05-16-rigorloop-npm-publication.md --path docs/plan.md`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-first-public-npm-release/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path docs/releases/v0.1.4/npm-publication.md --path docs/follow-ups.md --path docs/plans/2026-05-16-rigorloop-npm-publication.md --path docs/plan.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml`
  - `git diff --check -- docs/releases/v0.1.4/npm-publication.md docs/follow-ups.md docs/plans/2026-05-16-rigorloop-npm-publication.md docs/plan.md docs/changes/2026-05-16-first-public-npm-release/change.yaml`
- Expected observable result: `@xiongxianfei/rigorloop@0.1.4` is public, executable through npm/npx, proven to install the official Codex adapter archive, and FU-010 closes only after final evidence is tracked and validated.
- Closeout checklist:
  - [ ] publication mode evidence complete
  - [ ] public npm package visible
  - [ ] post-publication npm smoke passed or documented under the spec's allowed limits
  - [ ] actual Codex adapter install smoke passed
  - [ ] final evidence committed through the post-publication evidence PR or explicitly approved tracked commit path
  - [ ] FU-010 closed; FU-006 through FU-009 remain open
- Risks:
  - npm registry propagation can delay `npx` or `npm view` checks.
  - A bad package version cannot be overwritten.
  - Official GitHub adapter assets might not be externally observable before npm publication.
- Rollback/recovery:
  - Publish a fixed patch version and document/deprecate the bad version.
  - If official assets are temporarily unavailable, record the ordering gap and keep FU-010 open.

## Validation Plan

Run the smallest relevant checks during each milestone, then expand to the release gate and selected CI before handoff.

## Release Execution Boundary

Publication MUST use this order:

1. Complete implementation milestones.
2. Complete explain-change and verify for repository changes.
3. Merge the implementation PR.
4. Create `v0.1.4` tag from the merged commit.
5. Run the selected publication mode from that tag, or publish the exact verified bootstrap tarball from that merged commit.
6. Run post-publication checks.
7. Run actual Codex install smoke.
8. Commit publication evidence and FU-010 closeout through a post-publication evidence PR, unless repository governance explicitly approves another tracked commit path.
9. Close FU-010 only after the evidence update is tracked and validated.

In trusted-publishing mode, `release.yml` owns npm publication execution.

In bootstrap mode, `release.yml` owns release readiness but not npm publication execution for `0.1.4`; the maintainer publishes only the exact verified tarball, and `release.yml` must not also publish `@xiongxianfei/rigorloop@0.1.4`.

`docs/releases/v0.1.4/npm-publication.md` has two planned states:

- `pending-publication`: allowed before publication, with package name, intended version, source commit, selected publication mode, package-content validation result, packed-package smoke result, release verification result, and bootstrap tarball filename/SHA-256 when bootstrap is selected.
- `published`: required before FU-010 closes, with npm package URL, publication timestamp, publication mode, source commit, release tag, publish workflow run or bootstrap maintainer/publish command, npm view result, npx smoke result, actual Codex install smoke result, official archive URL verification, archive checksum verification, tree hash verification, and FU-010 closeout status.

FU-010 cannot close while `npm-publication.md` remains `pending-publication`.

Baseline planning validation:

```bash
python scripts/validate-change-metadata.py docs/changes/2026-05-16-first-public-npm-release/change.yaml
python scripts/validate-artifact-lifecycle.py --mode explicit-paths \
  --path docs/plans/2026-05-16-rigorloop-npm-publication.md \
  --path docs/plan.md \
  --path specs/rigorloop-npm-publication.md \
  --path docs/architecture/system/architecture.md \
  --path docs/adr/ADR-20260516-rigorloop-npm-publication.md \
  --path docs/changes/2026-05-16-first-public-npm-release/change.yaml
bash scripts/ci.sh --mode explicit \
  --path docs/plans/2026-05-16-rigorloop-npm-publication.md \
  --path docs/plan.md \
  --path specs/rigorloop-npm-publication.md \
  --path docs/architecture/system/architecture.md \
  --path docs/adr/ADR-20260516-rigorloop-npm-publication.md \
  --path docs/changes/2026-05-16-first-public-npm-release/change.yaml
git diff --check -- \
  docs/plans/2026-05-16-rigorloop-npm-publication.md \
  docs/plan.md \
  docs/changes/2026-05-16-first-public-npm-release/change.yaml
```

Implementation validation expands by milestone:

```bash
npm test --prefix packages/rigorloop
npm pack --dry-run --prefix packages/rigorloop
npm pack --prefix packages/rigorloop
bash scripts/release-verify.sh v0.1.4
python scripts/test-select-validation.py
python scripts/test-adapter-distribution.py
python scripts/validate-review-artifacts.py docs/changes/2026-05-16-first-public-npm-release
```

Post-publication validation:

```bash
npm view @xiongxianfei/rigorloop@0.1.4 version --registry=https://registry.npmjs.org
npx @xiongxianfei/rigorloop@0.1.4 --help
npx @xiongxianfei/rigorloop@0.1.4 version
npx @xiongxianfei/rigorloop@0.1.4 init --adapter codex --dry-run --json
npx @xiongxianfei/rigorloop@0.1.4 init --adapter codex --json
```

## Dependencies

- npm maintainer access for `@xiongxianfei/rigorloop`.
- Trusted publishing support for the package and `.github/workflows/release.yml`, or bootstrap conditions for first package creation.
- GitHub release tag `v0.1.4` and official adapter release assets.
- Release-output generation for the Codex adapter archive and metadata.
- Network access for the real install smoke and post-publication npm checks.
- Test-spec approval before implementation.

## Risks And Recovery

- Unintended package contents: fail package-content validation before publication and tighten the `files` allowlist.
- Duplicate publish path: require publication evidence to select exactly one mode and block workflow publication in bootstrap mode.
- Wrong package/tag/adapter version mapping: block release verification until package version, tag, release metadata, and bundled metadata align.
- First-publish trusted-publishing bootstrap ambiguity: use bootstrap only for `0.1.4` when trusted publishing cannot be configured before package creation, then require trusted publishing before the next npm release.
- Bad published package: publish a fixed patch version, document/deprecate the bad version, and avoid relying on mutable `latest` for reproducible setup.
- Real install smoke blocked by asset ordering: record the ordering gap, keep FU-010 open, and complete actual install proof after assets are observable.

## Progress

- [x] 2026-05-16: Proposal accepted for first public npm release.
- [x] 2026-05-16: Spec approved after three spec-review passes.
- [x] 2026-05-16: Architecture package and ADR accepted after architecture-review.
- [x] 2026-05-16: Plan created.
- [x] 2026-05-16: Plan-review completed by `plan-review-r2`.
- [x] 2026-05-16: Test spec created.
- [x] 2026-05-16: Test spec approved by maintainer.
- [x] 2026-05-16: M1 code-review completed clean with no material findings.
- [x] M1 closed.
- [x] 2026-05-16: M2 code-review rerun completed clean with no material findings.
- [x] M2 closed.
- [x] 2026-05-16: M3 code-review completed clean with no material findings.
- [x] M3 closed.
- [x] M4 `CR5-F1` accepted and fixed.
- [x] M4 code-review rerun completed clean.
- [x] M4 closed.
- [x] M5 code-review completed clean.
- [x] M5 closed.
- [x] M6a repository-local validation completed.
- [x] M6a repository-local readiness proof reviewed clean.
- [x] M6a verify completed.
- [x] M6a PR handoff completed by opening PR #65.
- [x] M6a pre-publication PR and merge readiness completed.
- [ ] M6b publication execution and evidence closeout completed.

## Decision Log

- 2026-05-16: Use repository tag `v0.1.4`, npm package `@xiongxianfei/rigorloop@0.1.4`, and compatible adapter release `v0.1.4` to avoid parallel version lines.
- 2026-05-16: Keep one package and one `rigorloop` binary; do not add `create-rigorloop`, `@rigorloop/cli`, or a second package.
- 2026-05-16: Use the existing `release.yml` as the trusted-publishing workflow; do not add a separate npm-only workflow for the first release.
- 2026-05-16: Allow one-time bootstrap only for the first `0.1.4` package claim when trusted publishing cannot be configured before the package exists.
- 2026-05-16: Treat actual non-dry-run Codex adapter install proof as required for FU-010 closeout, not replaceable by dry-run smoke.
- 2026-05-16: Use `release.yml` for future trusted npm publishing, but skip npm workflow publication for `v0.1.4` because the selected first-publication evidence mode is bootstrap.

## Surprises And Discoveries

- 2026-05-16: M1 can align package/runtime metadata names to `v0.1.4`, but the actual `v0.1.4` adapter archive generation and public release evidence remain M3/M5 scope. The M1 bundled metadata is a package mapping surface, not FU-010 closeout proof.
- 2026-05-16: The M5 plan validation command originally used `--path docs/releases/v0.1.4`, but the selector requires concrete release files to infer `v0.1.4`. The plan now records explicit `release.yaml`, `release-notes.md`, and `npm-publication.md` paths for selected CI.

## Validation Notes

- 2026-05-16: Planning-stage validation passed:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-first-public-npm-release/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-16-rigorloop-npm-publication.md --path docs/plan.md --path specs/rigorloop-npm-publication.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260516-rigorloop-npm-publication.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path docs/plans/2026-05-16-rigorloop-npm-publication.md --path docs/plan.md --path specs/rigorloop-npm-publication.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260516-rigorloop-npm-publication.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml`
  - `git diff --check -- docs/plans/2026-05-16-rigorloop-npm-publication.md docs/plan.md docs/changes/2026-05-16-first-public-npm-release/change.yaml`
- 2026-05-16: Test-spec authoring validation passed:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-first-public-npm-release/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/rigorloop-npm-publication.test.md --path specs/rigorloop-npm-publication.md --path docs/plans/2026-05-16-rigorloop-npm-publication.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path specs/rigorloop-npm-publication.test.md --path specs/rigorloop-npm-publication.md --path docs/plans/2026-05-16-rigorloop-npm-publication.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml`
  - `git diff --check -- specs/rigorloop-npm-publication.test.md docs/plans/2026-05-16-rigorloop-npm-publication.md docs/changes/2026-05-16-first-public-npm-release/change.yaml`
- 2026-05-16: M1 implementation validation passed:
  - `npm test --prefix packages/rigorloop -- --test-name-pattern "T1 package metadata|TNP-005"` first failed for expected pre-implementation reasons, then passed after package and metadata changes.
  - `npm test --prefix packages/rigorloop`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-first-public-npm-release/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path packages/rigorloop/package.json --path packages/rigorloop/README.md --path packages/rigorloop/LICENSE --path packages/rigorloop/dist/bin/rigorloop.js --path packages/rigorloop/dist/metadata/releases.json --path packages/rigorloop/dist/metadata/adapter-artifacts-v0.1.4.json --path packages/rigorloop/test/cli.test.js --path docs/plans/2026-05-16-rigorloop-npm-publication.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml --path specs/rigorloop-npm-publication.md --path specs/rigorloop-npm-publication.test.md`
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path docs/plans/2026-05-16-rigorloop-npm-publication.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml --path specs/rigorloop-npm-publication.md --path specs/rigorloop-npm-publication.test.md`
  - `git diff --check -- packages/rigorloop`
- 2026-05-16: M1 code-review recorded:
  - `docs/changes/2026-05-16-first-public-npm-release/reviews/code-review-r1.md`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-16-first-public-npm-release`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-first-public-npm-release/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-16-first-public-npm-release/reviews/code-review-r1.md --path docs/changes/2026-05-16-first-public-npm-release/review-log.md --path docs/changes/2026-05-16-first-public-npm-release/review-resolution.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml --path docs/plans/2026-05-16-rigorloop-npm-publication.md --path packages/rigorloop/package.json --path packages/rigorloop/test/cli.test.js --path packages/rigorloop/dist/metadata/releases.json --path packages/rigorloop/dist/metadata/adapter-artifacts-v0.1.4.json`
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path docs/plans/2026-05-16-rigorloop-npm-publication.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml --path docs/changes/2026-05-16-first-public-npm-release/review-log.md --path docs/changes/2026-05-16-first-public-npm-release/review-resolution.md --path docs/changes/2026-05-16-first-public-npm-release/reviews/code-review-r1.md --path specs/rigorloop-npm-publication.md --path specs/rigorloop-npm-publication.test.md`
  - `git diff --check -- packages/rigorloop docs/plans/2026-05-16-rigorloop-npm-publication.md docs/changes/2026-05-16-first-public-npm-release`
- 2026-05-16: M2 implementation validation passed:
  - `python scripts/test-npm-package-publication.py` first failed before `scripts/npm_package_validation.py` existed, then passed after adding validator and smoke coverage.
  - `tmp=$(mktemp -d); npm pack --dry-run --prefix packages/rigorloop ./packages/rigorloop --json > "$tmp/dry-run.json"; npm pack --prefix packages/rigorloop --pack-destination "$tmp" ./packages/rigorloop; python scripts/validate-npm-package.py --package-root packages/rigorloop --tarball "$tmp/xiongxianfei-rigorloop-0.1.4.tgz"`
  - `npm test --prefix packages/rigorloop`
  - `python scripts/test-select-validation.py`
  - `python scripts/test-npm-package-publication.py`
  - `python scripts/test-npm-package-publication.py` after CR2-F1 fix
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-first-public-npm-release/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path scripts/npm_package_validation.py --path scripts/validate-npm-package.py --path scripts/test-npm-package-publication.py --path scripts/validation_selection.py --path scripts/test-select-validation.py --path packages/rigorloop/package.json --path packages/rigorloop/README.md --path packages/rigorloop/LICENSE --path packages/rigorloop/dist/bin/rigorloop.js --path packages/rigorloop/dist/metadata/releases.json --path packages/rigorloop/dist/metadata/adapter-artifacts-v0.1.4.json --path packages/rigorloop/test/cli.test.js --path docs/plans/2026-05-16-rigorloop-npm-publication.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml --path specs/rigorloop-npm-publication.md --path specs/rigorloop-npm-publication.test.md`
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path scripts/npm_package_validation.py --path scripts/validate-npm-package.py --path scripts/test-npm-package-publication.py --path scripts/validation_selection.py --path scripts/test-select-validation.py --path docs/plans/2026-05-16-rigorloop-npm-publication.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml --path specs/rigorloop-npm-publication.md --path specs/rigorloop-npm-publication.test.md`
  - `git diff --check -- packages/rigorloop scripts docs/plans/2026-05-16-rigorloop-npm-publication.md docs/changes/2026-05-16-first-public-npm-release`
- 2026-05-16: M2 code-review rerun validation passed:
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-16-first-public-npm-release`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-first-public-npm-release/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-16-first-public-npm-release/reviews/code-review-r3.md --path docs/changes/2026-05-16-first-public-npm-release/review-log.md --path docs/changes/2026-05-16-first-public-npm-release/review-resolution.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml --path docs/plans/2026-05-16-rigorloop-npm-publication.md --path scripts/npm_package_validation.py --path scripts/test-npm-package-publication.py`
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path scripts/npm_package_validation.py --path scripts/validate-npm-package.py --path scripts/test-npm-package-publication.py --path scripts/validation_selection.py --path scripts/test-select-validation.py --path docs/plans/2026-05-16-rigorloop-npm-publication.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml --path docs/changes/2026-05-16-first-public-npm-release/review-log.md --path docs/changes/2026-05-16-first-public-npm-release/review-resolution.md --path docs/changes/2026-05-16-first-public-npm-release/reviews/code-review-r3.md --path specs/rigorloop-npm-publication.md --path specs/rigorloop-npm-publication.test.md`
  - `git diff --check -- packages/rigorloop scripts docs/plans/2026-05-16-rigorloop-npm-publication.md docs/changes/2026-05-16-first-public-npm-release specs/rigorloop-npm-publication.md specs/rigorloop-npm-publication.test.md`
- 2026-05-16: M3 implementation validation passed:
  - `python scripts/test-adapter-distribution.py` first failed for expected pre-implementation `v0.1.4` release-target and evidence-validation gaps, then passed after adding the release gate and evidence validation.
  - `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_v0_1_3_release_validation_uses_release_output_not_tracked_adapter_tree AdapterDistributionTests.test_v0_1_4_release_validation_accepts_pending_publication_evidence AdapterDistributionTests.test_v0_1_4_release_validation_requires_publication_evidence_and_closeout_blocker AdapterDistributionTests.test_release_verify_script_supports_v0_1_4_npm_publication_gate`
  - `bash scripts/release-verify.sh v0.1.4` first failed because `dist/adapters/manifest.yaml` still recorded `v0.1.3`, then passed after updating the manifest to `v0.1.4`.
  - `npm test --prefix packages/rigorloop`
  - `python scripts/test-npm-package-publication.py`
  - `python scripts/test-select-validation.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-first-public-npm-release/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path scripts/adapter_distribution.py --path scripts/release-verify.sh --path scripts/test-adapter-distribution.py --path docs/releases/v0.1.4/release.yaml --path docs/releases/v0.1.4/release-notes.md --path docs/releases/v0.1.4/npm-publication.md --path docs/reports/adapter-artifacts/releases/v0.1.4.yaml --path packages/rigorloop/dist/metadata/adapter-artifacts-v0.1.4.json --path packages/rigorloop/dist/metadata/releases.json --path docs/plans/2026-05-16-rigorloop-npm-publication.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path scripts/adapter_distribution.py --path scripts/release-verify.sh --path scripts/test-adapter-distribution.py --path scripts/validate-release.py --path docs/releases/v0.1.4/release.yaml --path docs/releases/v0.1.4/release-notes.md --path docs/releases/v0.1.4/npm-publication.md --path docs/reports/adapter-artifacts/releases/v0.1.4.yaml --path packages/rigorloop/dist/metadata/adapter-artifacts-v0.1.4.json --path packages/rigorloop/dist/metadata/releases.json --path dist/adapters/manifest.yaml --path docs/plans/2026-05-16-rigorloop-npm-publication.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml --path specs/rigorloop-npm-publication.md --path specs/rigorloop-npm-publication.test.md`
- 2026-05-16: M3 code-review recording validation passed:
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-16-first-public-npm-release`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-first-public-npm-release/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-16-first-public-npm-release/reviews/code-review-r4.md --path docs/changes/2026-05-16-first-public-npm-release/review-log.md --path docs/changes/2026-05-16-first-public-npm-release/review-resolution.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml --path docs/plans/2026-05-16-rigorloop-npm-publication.md`
  - `bash scripts/ci.sh --mode explicit --path docs/changes/2026-05-16-first-public-npm-release/reviews/code-review-r4.md --path docs/changes/2026-05-16-first-public-npm-release/review-log.md --path docs/changes/2026-05-16-first-public-npm-release/review-resolution.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml --path docs/plans/2026-05-16-rigorloop-npm-publication.md --path specs/rigorloop-npm-publication.md --path specs/rigorloop-npm-publication.test.md`
  - `git diff --check -- docs/changes/2026-05-16-first-public-npm-release docs/plans/2026-05-16-rigorloop-npm-publication.md`
- 2026-05-16: M4 implementation validation passed:
  - `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_release_workflow_gates_npm_publication_modes AdapterDistributionTests.test_v0_1_4_release_validation_rejects_incomplete_published_bootstrap_identity AdapterDistributionTests.test_v0_1_4_release_validation_accepts_complete_published_bootstrap_identity` first failed for expected pre-implementation workflow and evidence-validation gaps, then passed after the M4 changes.
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/test-select-validation.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-first-public-npm-release/change.yaml`
  - `bash scripts/release-verify.sh v0.1.4`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path .github/workflows/release.yml --path scripts/adapter_distribution.py --path scripts/test-adapter-distribution.py --path docs/plans/2026-05-16-rigorloop-npm-publication.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path .github/workflows/release.yml --path scripts/adapter_distribution.py --path scripts/test-adapter-distribution.py --path scripts/release-verify.sh --path scripts/validate-release.py --path docs/releases/v0.1.4/npm-publication.md --path docs/plans/2026-05-16-rigorloop-npm-publication.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml --path specs/rigorloop-npm-publication.md --path specs/rigorloop-npm-publication.test.md`
  - `git diff --check -- .github/workflows/release.yml scripts/adapter_distribution.py scripts/test-adapter-distribution.py docs/plans/2026-05-16-rigorloop-npm-publication.md docs/changes/2026-05-16-first-public-npm-release/change.yaml`
- 2026-05-16: M4 code-review recorded:
  - `docs/changes/2026-05-16-first-public-npm-release/reviews/code-review-r5.md`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-16-first-public-npm-release`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-first-public-npm-release/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-16-first-public-npm-release/reviews/code-review-r5.md --path docs/changes/2026-05-16-first-public-npm-release/review-log.md --path docs/changes/2026-05-16-first-public-npm-release/review-resolution.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml --path docs/plans/2026-05-16-rigorloop-npm-publication.md`
  - `bash scripts/ci.sh --mode explicit --path docs/changes/2026-05-16-first-public-npm-release/reviews/code-review-r5.md --path docs/changes/2026-05-16-first-public-npm-release/review-log.md --path docs/changes/2026-05-16-first-public-npm-release/review-resolution.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml --path docs/plans/2026-05-16-rigorloop-npm-publication.md --path .github/workflows/release.yml --path scripts/adapter_distribution.py --path scripts/test-adapter-distribution.py --path specs/rigorloop-npm-publication.md --path specs/rigorloop-npm-publication.test.md`
  - `git diff --check -- docs/changes/2026-05-16-first-public-npm-release docs/plans/2026-05-16-rigorloop-npm-publication.md`
- 2026-05-16: `CR5-F1` implementation validation passed:
  - `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_validate_release_cli_passes_changed_surface_inputs AdapterDistributionTests.test_v0_1_4_release_validation_rejects_incomplete_published_bootstrap_identity AdapterDistributionTests.test_v0_1_4_release_validation_rejects_mismatched_bootstrap_tarball_sha AdapterDistributionTests.test_v0_1_4_release_validation_rejects_missing_bootstrap_tarball_file AdapterDistributionTests.test_v0_1_4_release_validation_accepts_complete_published_bootstrap_identity`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/test-select-validation.py`
  - `bash scripts/release-verify.sh v0.1.4`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-first-public-npm-release/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path .github/workflows/release.yml --path scripts/adapter_distribution.py --path scripts/test-adapter-distribution.py --path scripts/validate-release.py --path docs/plans/2026-05-16-rigorloop-npm-publication.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml --path docs/changes/2026-05-16-first-public-npm-release/review-resolution.md`
  - `bash scripts/ci.sh --mode explicit --path .github/workflows/release.yml --path scripts/adapter_distribution.py --path scripts/test-adapter-distribution.py --path scripts/validate-release.py --path docs/plans/2026-05-16-rigorloop-npm-publication.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml --path docs/changes/2026-05-16-first-public-npm-release/review-resolution.md --path specs/rigorloop-npm-publication.md --path specs/rigorloop-npm-publication.test.md`
- 2026-05-16: M4 code-review rerun recording validation passed:
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-16-first-public-npm-release`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-first-public-npm-release/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-16-first-public-npm-release/reviews/code-review-r6.md --path docs/changes/2026-05-16-first-public-npm-release/review-log.md --path docs/changes/2026-05-16-first-public-npm-release/review-resolution.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml --path docs/plans/2026-05-16-rigorloop-npm-publication.md`
  - `bash scripts/ci.sh --mode explicit --path docs/changes/2026-05-16-first-public-npm-release/reviews/code-review-r6.md --path docs/changes/2026-05-16-first-public-npm-release/review-log.md --path docs/changes/2026-05-16-first-public-npm-release/review-resolution.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml --path docs/plans/2026-05-16-rigorloop-npm-publication.md --path .github/workflows/release.yml --path scripts/adapter_distribution.py --path scripts/test-adapter-distribution.py --path scripts/validate-release.py --path specs/rigorloop-npm-publication.md --path specs/rigorloop-npm-publication.test.md`
- 2026-05-16: M5 implementation validation passed:
  - `npm test --prefix packages/rigorloop`
  - `bash scripts/release-verify.sh v0.1.4`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-first-public-npm-release/change.yaml`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-16-first-public-npm-release`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/releases/v0.1.4/release.yaml --path docs/releases/v0.1.4/release-notes.md --path docs/releases/v0.1.4/npm-publication.md --path docs/follow-ups.md --path docs/plan.md --path docs/plans/2026-05-16-rigorloop-npm-publication.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml --path docs/changes/2026-05-16-first-public-npm-release/explain-change.md`
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path scripts/release-verify.sh --path scripts/validate-release.py --path .github/workflows/release.yml --path docs/releases/v0.1.4/release.yaml --path docs/releases/v0.1.4/release-notes.md --path docs/releases/v0.1.4/npm-publication.md --path docs/follow-ups.md --path specs/rigorloop-npm-publication.md --path docs/plans/2026-05-16-rigorloop-npm-publication.md --path docs/plan.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml`
  - `git diff --check -- packages/rigorloop scripts .github docs/releases/v0.1.4 docs/follow-ups.md docs/plans/2026-05-16-rigorloop-npm-publication.md docs/plan.md docs/changes/2026-05-16-first-public-npm-release`
- 2026-05-16: M5 code-review recording validation passed:
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-16-first-public-npm-release`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-first-public-npm-release/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-16-first-public-npm-release/reviews/code-review-r7.md --path docs/changes/2026-05-16-first-public-npm-release/review-log.md --path docs/changes/2026-05-16-first-public-npm-release/review-resolution.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml --path docs/plans/2026-05-16-rigorloop-npm-publication.md --path docs/changes/2026-05-16-first-public-npm-release/explain-change.md --path docs/follow-ups.md`
  - `bash scripts/ci.sh --mode explicit --path docs/changes/2026-05-16-first-public-npm-release/reviews/code-review-r7.md --path docs/changes/2026-05-16-first-public-npm-release/review-log.md --path docs/changes/2026-05-16-first-public-npm-release/review-resolution.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml --path docs/changes/2026-05-16-first-public-npm-release/explain-change.md --path docs/plans/2026-05-16-rigorloop-npm-publication.md --path docs/follow-ups.md --path specs/rigorloop-npm-publication.md --path specs/rigorloop-npm-publication.test.md`
  - `git diff --check -- docs/changes/2026-05-16-first-public-npm-release docs/plans/2026-05-16-rigorloop-npm-publication.md docs/follow-ups.md`
- 2026-05-16: M6a repository-local readiness validation passed:
  - `npm test --prefix packages/rigorloop`
  - `bash scripts/release-verify.sh v0.1.4`
  - `tmp=$(mktemp -d); npm pack --dry-run --prefix packages/rigorloop ./packages/rigorloop --json > "$tmp/dry-run.json"; npm pack --prefix packages/rigorloop --pack-destination "$tmp" ./packages/rigorloop; python scripts/validate-npm-package.py --package-root packages/rigorloop --tarball "$tmp/xiongxianfei-rigorloop-0.1.4.tgz"`
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path scripts/release-verify.sh --path scripts/validate-release.py --path .github/workflows/release.yml --path docs/releases/v0.1.4/release.yaml --path docs/releases/v0.1.4/release-notes.md --path docs/releases/v0.1.4/npm-publication.md --path docs/follow-ups.md --path specs/rigorloop-npm-publication.md --path docs/plans/2026-05-16-rigorloop-npm-publication.md --path docs/plan.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml`
  - `git diff --check -- packages/rigorloop scripts .github docs/releases/v0.1.4 docs/follow-ups.md docs/plans/2026-05-16-rigorloop-npm-publication.md docs/plan.md docs/changes/2026-05-16-first-public-npm-release`
- 2026-05-16: M6a plan/update validation passed:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-first-public-npm-release/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-16-rigorloop-npm-publication.md --path docs/plan.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml --path docs/changes/2026-05-16-first-public-npm-release/explain-change.md --path docs/releases/v0.1.4/npm-publication.md --path docs/follow-ups.md`
  - `bash scripts/ci.sh --mode explicit --path docs/plans/2026-05-16-rigorloop-npm-publication.md --path docs/plan.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml --path docs/changes/2026-05-16-first-public-npm-release/explain-change.md --path docs/releases/v0.1.4/npm-publication.md --path docs/follow-ups.md --path specs/rigorloop-npm-publication.md`
  - `git diff --check -- packages/rigorloop scripts .github docs/releases/v0.1.4 docs/follow-ups.md docs/plans/2026-05-16-rigorloop-npm-publication.md docs/plan.md docs/changes/2026-05-16-first-public-npm-release`
- 2026-05-16: M6a repository-local readiness proof code-review recording validation passed:
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-16-first-public-npm-release`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-first-public-npm-release/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-16-first-public-npm-release/reviews/code-review-r8.md --path docs/changes/2026-05-16-first-public-npm-release/review-log.md --path docs/changes/2026-05-16-first-public-npm-release/review-resolution.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml --path docs/plans/2026-05-16-rigorloop-npm-publication.md --path docs/changes/2026-05-16-first-public-npm-release/explain-change.md --path docs/follow-ups.md`
  - `bash scripts/ci.sh --mode explicit --path docs/changes/2026-05-16-first-public-npm-release/reviews/code-review-r8.md --path docs/changes/2026-05-16-first-public-npm-release/review-log.md --path docs/changes/2026-05-16-first-public-npm-release/review-resolution.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml --path docs/changes/2026-05-16-first-public-npm-release/explain-change.md --path docs/plans/2026-05-16-rigorloop-npm-publication.md --path docs/follow-ups.md --path specs/rigorloop-npm-publication.md`
  - `git diff --check -- docs/changes/2026-05-16-first-public-npm-release docs/plans/2026-05-16-rigorloop-npm-publication.md docs/follow-ups.md`
- 2026-05-16: M6a verify validation passed:
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-16-first-public-npm-release`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-first-public-npm-release/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-16-rigorloop-npm-publication.md --path docs/plan.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml --path docs/changes/2026-05-16-first-public-npm-release/explain-change.md --path docs/changes/2026-05-16-first-public-npm-release/review-log.md --path docs/changes/2026-05-16-first-public-npm-release/review-resolution.md --path docs/releases/v0.1.4/release.yaml --path docs/releases/v0.1.4/release-notes.md --path docs/releases/v0.1.4/npm-publication.md --path docs/follow-ups.md`
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path scripts/release-verify.sh --path scripts/validate-release.py --path .github/workflows/release.yml --path docs/releases/v0.1.4/release.yaml --path docs/releases/v0.1.4/release-notes.md --path docs/releases/v0.1.4/npm-publication.md --path docs/follow-ups.md --path specs/rigorloop-npm-publication.md --path specs/rigorloop-npm-publication.test.md --path docs/adr/ADR-20260516-rigorloop-npm-publication.md --path docs/plans/2026-05-16-rigorloop-npm-publication.md --path docs/plan.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml`
  - `bash scripts/release-verify.sh v0.1.4`
  - `git diff --check -- packages/rigorloop scripts .github docs/releases/v0.1.4 docs/follow-ups.md docs/plans/2026-05-16-rigorloop-npm-publication.md docs/plan.md docs/changes/2026-05-16-first-public-npm-release specs/rigorloop-npm-publication.md specs/rigorloop-npm-publication.test.md docs/adr/ADR-20260516-rigorloop-npm-publication.md`
- 2026-05-16: PR #65 opened at `https://github.com/xiongxianfei/rigorloop/pull/65`. Hosted CI is pending and is not claimed as passed.
- 2026-05-16: M6a PR #65 merge state confirmed:
  - `gh pr view 65 --json state,mergedAt,mergeCommit,url,headRefName,baseRefName,statusCheckRollup` reported `state: MERGED`, merge commit `8221134e08674040b05145241b20fbfcf0c530cf`, and hosted `ci` conclusion `SUCCESS`.
  - `git switch main && git pull --ff-only` fast-forwarded local `main` to `8221134e08674040b05145241b20fbfcf0c530cf`.
- 2026-05-16: M6a merge-state lifecycle validation passed:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-16-first-public-npm-release/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-16-rigorloop-npm-publication.md --path docs/plan.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml --path docs/releases/v0.1.4/npm-publication.md --path docs/follow-ups.md`
  - `bash scripts/ci.sh --mode explicit --path docs/plans/2026-05-16-rigorloop-npm-publication.md --path docs/plan.md --path docs/changes/2026-05-16-first-public-npm-release/change.yaml --path docs/releases/v0.1.4/npm-publication.md --path docs/follow-ups.md`
  - `git diff --check -- docs/plans/2026-05-16-rigorloop-npm-publication.md docs/changes/2026-05-16-first-public-npm-release/change.yaml`

## Outcome And Retrospective

- Not yet complete. This plan remains active until implementation milestones, publication execution, FU-010 closeout evidence, final verification, and PR handoff are complete.

## Readiness

- Ready for M6b publication execution from merged commit `8221134e08674040b05145241b20fbfcf0c530cf`.
- Not ready for final FU-010 closeout or post-publication evidence closeout until M6b publication evidence and actual install smoke pass.

## Follow-Ups

- FU-010 remains active until publication evidence and actual install smoke pass.
- FU-006 `rigorloop status`, FU-007 `rigorloop validate`, FU-008 workflow YAML, and FU-009 generated workflow docs remain deferred.
