# RigorLoop npm Publication Test Spec

## Status

active

## Related spec and plan

- Spec: [RigorLoop npm Publication](rigorloop-npm-publication.md), approved.
- Plan: [RigorLoop npm publication](../docs/plans/2026-05-16-rigorloop-npm-publication.md), active and approved by `plan-review-r2`.
- Proposal: [First public npm release](../docs/proposals/2026-05-16-first-public-npm-release.md), accepted.
- Architecture: [RigorLoop Canonical System Architecture](../docs/architecture/system/architecture.md), approved.
- ADR: [ADR-20260516 RigorLoop npm publication](../docs/adr/ADR-20260516-rigorloop-npm-publication.md), accepted.
- Change metadata: [change.yaml](../docs/changes/2026-05-16-first-public-npm-release/change.yaml).
- Review records:
  - `docs/changes/2026-05-16-first-public-npm-release/reviews/spec-review-r3.md`
  - `docs/changes/2026-05-16-first-public-npm-release/reviews/architecture-review-r1.md`
  - `docs/changes/2026-05-16-first-public-npm-release/reviews/plan-review-r2.md`

## Testing strategy

This release-hardening slice creates a public npm distribution boundary. The proof must cover package metadata, tarball contents, dependency and lifecycle policy, packed-package execution, release workflow gates, publication-mode evidence, release documentation, and post-publication smoke.

- Package unit/contract tests inspect `packages/rigorloop/package.json`, bin target, scripts, dependencies, package-local license, bundled metadata, and CLI version behavior.
- Tarball integration tests run `npm pack --prefix packages/rigorloop`, inspect the resulting `.tgz`, and install it into a temporary project. They must execute the installed `node_modules/.bin/rigorloop`, not the repository-local CLI path.
- Release validation tests extend existing release verification around `scripts/release-verify.sh`, `scripts/validate-release.py`, and release workflow static checks.
- Workflow tests are static or dry-run tests. They must not perform real npm publication in ordinary CI.
- Networked post-publication checks are release/manual smoke. They use the public npm registry and official GitHub release archive only after publication or when release assets are externally observable.
- Tests must not require ordinary contributors to have npm credentials, trusted publisher admin access, or maintainer 2FA.
- Where external state cannot be automated safely, publication evidence under `docs/releases/v0.1.4/npm-publication.md` becomes the audited proof surface.

## Requirement coverage map

| Requirement | Coverage |
| --- | --- |
| R1-R9 | TNP-001, TNP-005, TNP-013, TNP-018, TNP-021 |
| R10-R16 | TNP-002, TNP-006, TNP-022 |
| R17-R27 | TNP-003, TNP-004, TNP-021 |
| R28-R34 | TNP-004 |
| R35-R36f | TNP-008, TNP-009, TNP-010, TNP-011, TNP-012, TNP-014 |
| R37-R47 | TNP-008, TNP-009, TNP-010 |
| R48-R61d | TNP-010, TNP-011, TNP-012, TNP-015, TNP-018 |
| R62-R69 | TNP-006, TNP-007 |
| R69a-R69m | TNP-016, TNP-017, TNP-018 |
| R70-R80 | TNP-013, TNP-014, TNP-015, TNP-019 |
| R81-R85 | TNP-018, TNP-019 |
| S1-S6 | TNP-005, TNP-012, TNP-014, TNP-016, TNP-019, TNP-021 |
| EB1-EB4 | TNP-001, TNP-005, TNP-008, TNP-009 |
| EB5-EB7 | TNP-003, TNP-006, TNP-008, TNP-013 |
| EB8 | TNP-009 |
| EB9-EB12 | TNP-011, TNP-012 |
| EB13-EB14 | TNP-014, TNP-016, TNP-017, TNP-019 |

## Example coverage map

| Example | Coverage |
| --- | --- |
| E1 first public package is installable | TNP-018 |
| E2 pinned npx init uses matching release line | TNP-006, TNP-018 |
| E3 package exposes one executable | TNP-002, TNP-003 |
| E4 package tarball contains only runtime files | TNP-003, TNP-021 |
| E5 packed package smoke proves CLI behavior | TNP-006, TNP-007 |
| E6 first publication bootstrap is recorded | TNP-011, TNP-015 |
| E7 release candidates do not publish npm | TNP-009 |
| E8 bootstrap publishes only a verified tarball | TNP-011, TNP-012, TNP-015 |
| E9 real Codex install smoke closes FU-010 | TNP-016, TNP-017, TNP-019 |

## Edge case coverage

| Edge case | Coverage |
| --- | --- |
| `private: true` remains in package metadata | TNP-001, TNP-008 |
| Package version does not match `v0.1.4` tag | TNP-001, TNP-005, TNP-009 |
| Bundled adapter metadata still points at `v0.1.3` | TNP-005, TNP-016 |
| `files` omits required runtime file | TNP-003 |
| Tarball includes tests, docs, `.codex`, `.agents`, adapter ZIPs, `.tgz`, secrets, or generated adapter bodies | TNP-003, TNP-021 |
| Package has install lifecycle scripts | TNP-004 |
| Runtime dependencies appear without recorded purpose | TNP-004 |
| Packed package binary executes repository-local CLI by accident | TNP-006 |
| JSON-mode packed smoke emits non-JSON stdout | TNP-006 |
| Unsupported tag or release candidate attempts npm publish | TNP-009 |
| Trusted mode and bootstrap mode are both selected | TNP-012 |
| Bootstrap tarball SHA is missing or mismatched | TNP-011 |
| Bootstrap used for a version other than `0.1.4` | TNP-011 |
| Publication evidence remains `pending-publication` | TNP-014, TNP-019 |
| Official GitHub adapter archive not externally observable before npm publication | TNP-017 |
| Actual Codex install smoke fails checksum, size, extraction, or tree hash verification | TNP-016 |
| Public npm package is visible but post-publication smoke fails | TNP-018, TNP-019 |

## Milestone coverage map

| Plan milestone | Coverage |
| --- | --- |
| M1. Package metadata and runtime tarball contract | TNP-001-TNP-005, TNP-021, TNP-022 |
| M2. Package-content validation and packed-package smoke | TNP-003, TNP-006, TNP-007, TNP-020, TNP-021 |
| M3. Release verification and v0.1.4 release evidence | TNP-005, TNP-008, TNP-013-TNP-017, TNP-020 |
| M4. Release workflow and publication mode gates | TNP-009-TNP-012, TNP-015, TNP-020 |
| M5. Documentation, follow-up state, and final local readiness | TNP-013-TNP-015, TNP-019, TNP-020 |
| M6a. Pre-publication PR and merge readiness | TNP-006, TNP-008, TNP-014, TNP-019, final selected CI |
| M6b. Publication execution and evidence closeout | TNP-016-TNP-019, post-publication smoke |

## Test cases

### TNP-001. Package identity is `@xiongxianfei/rigorloop@0.1.4`

- Covers: R1-R8, EB1-EB4, S1
- Level: unit, contract
- Fixture/setup: `packages/rigorloop/package.json`.
- Steps:
  - Read `packages/rigorloop/package.json`.
  - Assert `name` is `@xiongxianfei/rigorloop`.
  - Assert `version` is `0.1.4`.
  - Assert `private` is absent or not `true`.
  - Assert no publish-time mutation script is needed to change `name`, `version`, `private`, `files`, `bin`, dependencies, or lifecycle scripts.
- Expected result: the package tested locally is the package identity intended for npm.
- Failure proves: publication can block or publish a different package than the release gate tested.
- Automation location: `packages/rigorloop/test/cli.test.js` or `scripts/test-npm-package-publication.py`.

### TNP-002. Package exposes exactly one `rigorloop` binary

- Covers: R10-R16, E3
- Level: unit, contract
- Fixture/setup: package metadata and `packages/rigorloop/dist/bin/rigorloop.js`.
- Steps:
  - Assert `bin` has exactly one key: `rigorloop`.
  - Assert `bin.rigorloop` is `dist/bin/rigorloop.js`.
  - Assert the bin target exists.
  - Assert the bin target starts with a Node shebang.
  - Assert package metadata does not expose `create-rigorloop`, `@rigorloop/create`, `@rigorloop/cli`, or any second binary.
- Expected result: public command surface remains one package and one executable.
- Failure proves: the first npm package exposes unsupported commands or cannot launch through npm-installed bin linking.
- Automation location: package CLI tests or npm package publication tests.

### TNP-003. Tarball contains required runtime files and excludes forbidden paths

- Covers: R17-R27, R20, E4, EB5
- Level: integration, contract
- Fixture/setup: run `npm pack --json --prefix packages/rigorloop` and inspect the `.tgz`.
- Steps:
  - Assert required paths exist:
    - `package/package.json`
    - `package/README.md`
    - `package/LICENSE`
    - `package/dist/bin/rigorloop.js`
    - required runtime `dist/lib/**`
    - `package/dist/metadata/adapter-artifacts-v0.1.4.json`
    - `package/dist/metadata/releases.json`
  - Assert forbidden paths are absent:
    - `package/test/**`, `package/tests/**`, `package/__fixtures__/**`
    - `package/docs/**`, `package/release-output/**`
    - `package/.codex/**`, `package/.agents/**`
    - `package/dist/adapters/**`
    - `package/**/*.zip`, `package/**/*.tgz`, `package/**/*.pem`, `package/**/*.key`, `package/**/*.env`
  - Assert no adapter release archive is bundled.
  - Assert no generated public adapter skill bodies are bundled.
- Expected result: package tarball is a minimal runtime delivery artifact.
- Failure proves: npm publication leaks repository internals, secrets, generated skill bodies, or adapter archives.
- Automation location: new tarball validator such as `scripts/validate-npm-package.py` plus regression tests.

### TNP-004. Package dependency and lifecycle-script policy is enforced

- Covers: R28-R34
- Level: unit, contract
- Fixture/setup: `packages/rigorloop/package.json` and negative metadata fixtures.
- Steps:
  - Assert `preinstall`, `install`, and `postinstall` are absent.
  - Assert `prepare` and `prepack` are absent unless a later approved spec revision justifies them.
  - Assert runtime dependencies are empty, or every runtime dependency has a recorded purpose in release evidence/spec revision.
  - Assert package scripts do not require secrets or network access for normal consumer installation.
  - Negative fixture: inject lifecycle scripts and assert package policy validation fails.
- Expected result: installing the package does not execute unnecessary lifecycle code or hidden network/secret behavior.
- Failure proves: publication introduces supply-chain risk during consumer install.
- Automation location: package-content validator tests.

### TNP-005. Version mapping and bundled metadata align to `v0.1.4`

- Covers: R4, R5, R9, S1, EB3, EB4
- Level: unit, integration
- Fixture/setup: package metadata, `dist/metadata/releases.json`, `adapter-artifacts-v0.1.4.json`, `docs/releases/v0.1.4/release.yaml`, and release notes.
- Steps:
  - Assert package version `0.1.4` maps to release tag `v0.1.4`.
  - Assert bundled release index names `adapter-artifacts-v0.1.4.json`.
  - Assert bundled metadata names the `v0.1.4` Codex archive.
  - Assert release metadata and release notes record npm package `0.1.4` to adapter release `v0.1.4`.
  - Negative fixture: package version/tag mismatch fails release validation.
  - Negative fixture: adapter release mismatch fails release validation.
- Expected result: `npx @xiongxianfei/rigorloop@0.1.4 init --adapter codex` cannot accidentally install the wrong release line.
- Failure proves: users can pin a package version that resolves incompatible adapter metadata.
- Automation location: package tests and `scripts/validate-release.py` tests.

### TNP-006. Packed-package smoke executes installed binary

- Covers: R62-R67, R69, E2, E5
- Level: integration, smoke
- Fixture/setup: packed `.tgz`, temporary project, `npm install --prefix <tmp> <tarball>`.
- Steps:
  - Execute `<tmp>/node_modules/.bin/rigorloop --help`.
  - Execute `<tmp>/node_modules/.bin/rigorloop version`.
  - Execute `<tmp>/node_modules/.bin/rigorloop init --adapter codex --dry-run --json`.
  - Execute `<tmp>/node_modules/.bin/rigorloop new-change test-change --title "Test change" --dry-run --json`.
  - Assert the command path is the installed binary, not `packages/rigorloop/dist/bin/rigorloop.js`.
  - Assert `version` reports `@xiongxianfei/rigorloop` and `0.1.4`.
  - Assert JSON-mode stdout is JSON-only.
  - Assert public exit codes follow the existing CLI contract.
- Expected result: the packed package works in the same shape users install from npm.
- Failure proves: repository-local tests passed but the distributed package is broken.
- Automation location: `scripts/test-npm-package-publication.py` or package test suite.

### TNP-007. Optional local archive packed smoke uses release-output fixture when available

- Covers: R68, R69
- Level: integration, smoke
- Fixture/setup: packed package plus local `v0.1.4` Codex archive from `release-output/` when generated by the release gate.
- Steps:
  - Install the packed package into a temporary project.
  - Run installed `rigorloop init --adapter codex --from-archive <path> --json`.
  - Assert success when archive metadata, checksum, size, extraction, and tree hash match.
  - Skip or mark not-run with rationale when the local archive fixture is unavailable.
- Expected result: packed package can install from a local verified archive without npm credentials.
- Failure proves: the local archive path regressed in the published package shape.
- Automation location: packed smoke script; optional release-gate smoke.

### TNP-008. Release gate supports `v0.1.4` and runs npm publication checks

- Covers: R35, R38-R40, R46-R47, R70-R71, EB2, EB5-EB7
- Level: integration, release
- Fixture/setup: `RELEASE_VERIFY_DRY_RUN=1` where appropriate, release output temp dir, release metadata fixtures.
- Steps:
  - Run `bash scripts/release-verify.sh v0.1.4` in dry-run mode and inspect invoked commands.
  - Assert package-content validation is invoked.
  - Assert packed-package smoke is invoked.
  - Assert release validation for `v0.1.4` is invoked.
  - Assert GitHub release archive behavior remains present.
  - Assert npm package tarballs are not treated as adapter archives.
  - Negative fixture: missing release notes or release metadata fails release validation.
- Expected result: `release-verify.sh v0.1.4` is the maintainer-facing gate for npm publication readiness.
- Failure proves: publication can bypass package-content or packed smoke proof.
- Automation location: `scripts/test-adapter-distribution.py`, `scripts/test-npm-package-publication.py`.

### TNP-009. Release workflow publishes npm only for supported stable tags

- Covers: R37, R41-R45, E7, EB8
- Level: static, contract
- Fixture/setup: `.github/workflows/release.yml` and workflow/test fixtures.
- Steps:
  - Assert no separate npm-only workflow is introduced.
  - Assert npm publish job is gated by stable semver tags.
  - Assert `v0.1.4` is accepted.
  - Assert branches, PRs, untagged runs, manual dispatch without approval, unsupported tags, and `v0.1.4-rc.1` do not publish npm.
  - Assert package version must equal tag without leading `v`.
- Expected result: npm publication cannot run from unsupported release contexts.
- Failure proves: a branch, RC, or version mismatch can publish public npm artifacts.
- Automation location: workflow static tests in `scripts/test-adapter-distribution.py` or dedicated publication tests.

### TNP-010. Trusted-publishing mode is correctly gated

- Covers: R36c, R38-R40, R48-R52, R61
- Level: static, manual confirmation
- Fixture/setup: `.github/workflows/release.yml`, publication evidence fixture.
- Steps:
  - Assert trusted-publishing mode uses `.github/workflows/release.yml`.
  - Assert the publish job requests `id-token: write`.
  - Assert the publish job uses npm public registry.
  - Assert release gate, package-content validation, and packed-package smoke run before publish.
  - Manual evidence: record trusted publisher configuration for package `@xiongxianfei/rigorloop`, repository `xiongxianfei/rigorloop`, and workflow `.github/workflows/release.yml`.
  - Manual evidence: record whether npm provenance was generated.
- Expected result: trusted publishing is the normal future path and uses OIDC rather than long-lived tokens.
- Failure proves: npm release trust is not reviewable or repeatable.
- Automation location: workflow static tests plus publication evidence manual checklist.

### TNP-011. Bootstrap mode is one-time and requires exact tarball identity

- Covers: R36d-R36f, R53-R61d, E6, E8, EB9-EB12
- Level: contract, manual confirmation
- Fixture/setup: publication evidence fixtures for bootstrap mode and negative variants.
- Steps:
  - Assert bootstrap is allowed only for `@xiongxianfei/rigorloop@0.1.4`.
  - Assert `release.yml` does not also publish `0.1.4` in bootstrap mode.
  - Assert bootstrap evidence records package name, package version, source commit, release tag, tarball filename, SHA-256, `npm pack` command, package-content validation, packed-package smoke, approving maintainer, publish command, and npm package URL.
  - Negative fixture: missing tarball SHA fails validation.
  - Negative fixture: mismatched tarball SHA fails validation.
  - Negative fixture: bootstrap mode for any later version fails validation.
  - Manual evidence: maintainer 2FA was used for bootstrap publication.
- Expected result: bootstrap can claim the package once without becoming normal release behavior.
- Failure proves: manual publish can bypass release proof or become a reusable shadow path.
- Automation location: release evidence validator/tests plus manual publication checklist.

### TNP-012. Publication mode evidence is exclusive

- Covers: R36-R36b, R36c-R36f, R59, R78a-R78b, S3-S5
- Level: contract
- Fixture/setup: `docs/releases/v0.1.4/npm-publication.md` fixtures.
- Steps:
  - Positive: trusted-publishing evidence selects only `trusted-publishing`.
  - Positive: bootstrap evidence selects only `bootstrap`.
  - Negative: evidence selecting both modes fails validation.
  - Negative: trusted mode with `workflow.published_by_workflow: false` fails validation.
  - Negative: bootstrap mode with `workflow.published_by_workflow: true` fails validation.
- Expected result: publication evidence always identifies one publication authority.
- Failure proves: duplicate or ambiguous publish paths can exist.
- Automation location: `scripts/validate-release.py` tests or dedicated publication evidence validator.

### TNP-013. Release docs and release metadata are publication-ready

- Covers: R9, R70-R76, EB7
- Level: contract
- Fixture/setup: `docs/releases/v0.1.4/release.yaml`, `docs/releases/v0.1.4/release-notes.md`.
- Steps:
  - Assert both files exist before publication readiness.
  - Assert release notes include latest npx command.
  - Assert release notes include pinned `0.1.4` npx command.
  - Assert release notes include local install usage.
  - Assert release notes state npm is CLI delivery, not canonical source.
  - Assert release notes state adapter archives remain GitHub release artifacts and are not bundled in npm.
  - Assert release metadata records npm package to adapter release mapping.
- Expected result: release notes and metadata truthfully describe public install and source-of-truth boundaries.
- Failure proves: public users or maintainers can follow stale or unsafe release instructions.
- Automation location: release validator tests.

### TNP-014. Pending publication evidence blocks FU-010 closeout

- Covers: R77-R80, R78d, R79-R79a, S5-S6, EB13
- Level: contract
- Fixture/setup: `npm-publication.md` fixture with status `pending-publication`.
- Steps:
  - Assert pending evidence may record package name, intended version, source commit, selected publication mode, package-content result, packed smoke result, release verification result, and bootstrap tarball identity when applicable.
  - Assert pending evidence may record ordering gap if GitHub assets are not externally observable.
  - Assert FU-010 remains open while evidence is pending.
  - Negative fixture: FU-010 closed while `npm-publication.md` is pending fails validation.
- Expected result: release preparation evidence cannot be mistaken for publication closeout evidence.
- Failure proves: FU-010 can close before users can actually install and run the package.
- Automation location: release evidence validator plus follow-up register tests.

### TNP-015. Published publication evidence shape is complete

- Covers: R59-R61, R78-R78c, R78a-R78b, E6, E8
- Level: contract, manual confirmation
- Fixture/setup: `npm-publication.md` fixture with status `published`.
- Steps:
  - Assert evidence records package name, published version, npm package URL, source commit, repository tag, publication mode, workflow run or bootstrap evidence, tarball evidence, packed-package smoke, real Codex adapter install smoke, trusted publishing status, provenance status when available, and rollback/deprecation note when applicable.
  - Assert trusted mode records workflow run and trusted publishing fields.
  - Assert bootstrap mode records approving maintainer and publish command.
  - Negative fixture: published evidence missing npm URL fails validation.
  - Negative fixture: published evidence missing real install smoke fails validation.
- Expected result: publication evidence is durable enough to audit FU-010 closeout.
- Failure proves: release evidence cannot support public package or supply-chain claims.
- Automation location: release validator tests plus manual publication checklist.

### TNP-016. Real Codex adapter install smoke proves archive verification

- Covers: R69a-R69k, R78c, E9, EB14, S6
- Level: e2e, smoke
- Fixture/setup: packed or published package installed into a temporary project; official `v0.1.4` Codex archive externally observable or fixture-backed official release output before publication.
- Steps:
  - Run package binary `rigorloop init --adapter codex --json`.
  - Assert command uses the package binary, not repository-local script path.
  - Assert official archive URL is `https://github.com/xiongxianfei/rigorloop/releases/download/v0.1.4/rigorloop-adapter-codex-v0.1.4.zip`.
  - Assert archive SHA-256 verifies.
  - Assert archive size verifies when metadata provides `size_bytes`.
  - Assert extraction stays within `.agents/skills`.
  - Assert installed tree hash verifies.
  - Assert generated files exist under expected Codex install root.
  - Assert JSON status is `success`.
  - Negative fixtures: checksum mismatch, size mismatch, extraction safety failure, and tree hash mismatch fail and keep FU-010 open.
- Expected result: the primary public install path works, not just dry-run command discovery.
- Failure proves: public npm package cannot install verified Codex adapter output.
- Automation location: packed release smoke when assets are available; post-publication manual/e2e smoke.

### TNP-017. Asset-ordering gap is recorded and blocks closeout

- Covers: R69l-R69m, R78d, EB13
- Level: contract, manual confirmation
- Fixture/setup: publication evidence fixture where npm publication occurred before GitHub assets are externally observable.
- Steps:
  - Assert evidence records `adapter_install_smoke.result: pending`.
  - Assert evidence records an ordering gap reason.
  - Assert evidence records `fu_010_closeout_blocked: true`.
  - Assert FU-010 remains open.
  - After assets are observable, rerun actual install smoke and update evidence to pass.
- Expected result: a temporary release ordering gap is visible and cannot silently close FU-010.
- Failure proves: closeout can claim real install proof before the official archive exists.
- Automation location: release evidence validator tests plus manual release checklist.

### TNP-018. Post-publication npm and npx smoke passes

- Covers: R81-R85, E1, E2
- Level: e2e, manual smoke
- Fixture/setup: public npm registry after `@xiongxianfei/rigorloop@0.1.4` publication.
- Steps:
  - Run `npm view @xiongxianfei/rigorloop@0.1.4 version --registry=https://registry.npmjs.org`.
  - Assert output is `0.1.4`.
  - Run `npx @xiongxianfei/rigorloop@0.1.4 --help`.
  - Run `npx @xiongxianfei/rigorloop@0.1.4 version`.
  - Run `npx @xiongxianfei/rigorloop@0.1.4 init --adapter codex --dry-run --json` unless registry propagation or local execution policy prevents it.
  - Record any inability in `npm-publication.md`.
- Expected result: published package is visible and executable through npm/npx.
- Failure proves: npm publication succeeded but public consumption is broken or unproven.
- Automation location: manual post-publication checklist and release evidence.

### TNP-019. FU-010 closes only after tracked final evidence

- Covers: R79-R80, R84-R85, S5, EB10, EB13-EB14
- Level: contract, lifecycle
- Fixture/setup: `docs/follow-ups.md`, `docs/releases/v0.1.4/npm-publication.md`, active plan and plan index.
- Steps:
  - Negative fixture: FU-010 marked done while `npm-publication.md` is missing fails validation.
  - Negative fixture: FU-010 marked done while post-publication smoke failed fails validation.
  - Negative fixture: FU-010 marked done while actual install smoke is pending or failed fails validation.
  - Positive fixture: FU-010 marked done only after public publication evidence and actual install smoke pass.
  - Assert FU-006 through FU-009 remain open.
  - Assert active plan and `docs/plan.md` synchronize final evidence closeout state.
- Expected result: follow-up state matches the durable public release evidence.
- Failure proves: roadmap state can claim publication closeout without proof.
- Automation location: follow-up/release evidence validator tests or selected lifecycle CI.

### TNP-020. Selected validation routes package, release, workflow, and evidence paths

- Covers: plan validation, operational readiness
- Level: unit, CI
- Fixture/setup: `scripts/validation_selection.py` and `scripts/test-select-validation.py`.
- Steps:
  - Assert package paths select package tests.
  - Assert release validation script changes select release validation tests.
  - Assert workflow changes select release/workflow validation.
  - Assert `docs/releases/v0.1.4/**`, `docs/follow-ups.md`, plan, test spec, and change metadata select lifecycle/change/release checks as appropriate.
- Expected result: scoped CI catches changes to package publication surfaces.
- Failure proves: future edits can bypass release-hardening validation.
- Automation location: selector regression tests.

### TNP-021. Security and privacy scan rejects sensitive package contents

- Covers: R22-R25, S2, EB5
- Level: security, contract
- Fixture/setup: tarball fixtures and negative path fixtures.
- Steps:
  - Assert package-content validation rejects `.npmrc`, `.env`, `.pem`, `.key`, archive ZIPs, nested `.tgz`, `.codex`, `.agents`, and release-output paths.
  - Assert package-content validation rejects absolute local paths, usernames, host-specific temp directories, and token-like fixture markers when present in package files.
  - Assert no generated adapter skill bodies are present under `dist/adapters/**`.
- Expected result: npm tarball does not leak secrets or repository-local/generated adapter internals.
- Failure proves: public npm package can leak sensitive or non-runtime content.
- Automation location: tarball validator tests.

### TNP-022. Publication slice does not add new CLI features

- Covers: R15-R16
- Level: regression, integration
- Fixture/setup: local and packed CLI help/version command output.
- Steps:
  - Assert existing supported commands remain help/version, `init --adapter codex`, and `new-change`.
  - Assert help does not advertise `status`, `validate`, workflow YAML, generated workflow docs, or other deferred commands.
  - Assert unknown future commands still fail with the established invalid-usage exit code.
- Expected result: publication hardening does not expand product behavior.
- Failure proves: this slice leaked deferred follow-ups into public CLI behavior.
- Automation location: package CLI tests and packed-package smoke.

## Fixtures and data

- `packages/rigorloop/package.json` as the source package metadata fixture.
- `packages/rigorloop/dist/bin/rigorloop.js` and runtime `dist/lib/**` as bin/runtime fixtures.
- `packages/rigorloop/dist/metadata/releases.json` and `adapter-artifacts-v0.1.4.json` as bundled metadata fixtures.
- Temporary tarballs from `npm pack --json --prefix packages/rigorloop`.
- Temporary install projects created under the system temp directory.
- Negative tarball fixtures with forbidden paths or missing required runtime files.
- Publication evidence fixtures for:
  - `pending-publication`;
  - trusted-publishing `published`;
  - bootstrap `published`;
  - mode conflict;
  - missing tarball SHA;
  - missing actual install smoke;
  - ordering gap.
- Release fixtures under `docs/releases/v0.1.4/`.
- Adapter artifact release output for `v0.1.4` when generated by release validation.

## Mocking and stubbing policy

- Automated tests must not publish to npm.
- Automated tests must not require npm maintainer credentials, npm 2FA, or trusted-publisher admin access.
- Automated workflow tests should inspect YAML or script behavior statically and use dry-run script modes where available.
- `npm pack` and local tarball installation are allowed in automated tests because they do not require registry credentials.
- Live npm registry and live GitHub release checks are reserved for post-publication manual/e2e smoke, except where a release validation command intentionally checks externally observable assets.
- Network archive verification may use fixture-backed official URL fetch seams before publication, but final FU-010 closeout requires real official archive proof or explicitly recorded ordering-gap evidence.
- Tests must not use arbitrary archive URLs in production metadata. Official URL validation remains in force.

## Migration or compatibility tests

- Existing `v0.1.3` release evidence remains historical and must not be rewritten by `v0.1.4` publication tests.
- Existing CLI tests for help/version/init/lockfile/new-change must remain green after package version moves to `0.1.4`.
- Package version and adapter release mapping tests must prove there is no parallel package-publication version line for the first public package.
- Release workflow tests must preserve GitHub release archive creation behavior while adding npm publication gates.

## Observability verification

- JSON-mode packed smoke must prove stdout is JSON-only for `init --adapter codex --dry-run --json` and `new-change ... --dry-run --json`.
- Publication evidence must record the selected publication mode, tarball identity, package-content result, packed-package smoke result, npm URL, post-publication result, and actual Codex install smoke result.
- Release validation output should identify blockers such as missing metadata, forbidden tarball contents, unsupported tag, mode conflict, or pending actual install smoke.

## Security and privacy verification

- Tarball validation must reject secrets and sensitive extensions listed in R22-R25.
- Package policy checks must reject consumer-install lifecycle scripts.
- Trusted-publishing static checks must require OIDC permission in the publish job.
- Bootstrap evidence must include exact tarball SHA-256 and maintainer approval.
- Network install smoke must use official RigorLoop GitHub release archive URLs only.
- No test fixture should require real npm tokens or commit token-like secrets.

## Performance checks

- No release-hardening requirement adds a runtime performance budget.
- Packed-package smoke should remain bounded to a small temporary install and the four required CLI commands.
- Tarball inspection should inspect package file lists directly rather than unpacking or scanning unrelated repository directories.

## Manual QA checklist

Run during M6b or post-publication evidence PR:

```bash
bash scripts/release-verify.sh v0.1.4
npm view @xiongxianfei/rigorloop@0.1.4 --json
npx @xiongxianfei/rigorloop@0.1.4 --help
npx @xiongxianfei/rigorloop@0.1.4 version
npx @xiongxianfei/rigorloop@0.1.4 init --adapter codex --dry-run --json
npx @xiongxianfei/rigorloop@0.1.4 init --adapter codex --json
```

Record in `docs/releases/v0.1.4/npm-publication.md`:

- publication mode;
- npm package URL;
- source commit and release tag;
- workflow run or bootstrap maintainer/publish command;
- tarball filename and SHA-256;
- package-content validation result;
- packed-package smoke result;
- trusted publishing/provenance status;
- actual Codex install smoke result;
- official archive URL;
- checksum, size, extraction, and tree-hash verification result;
- FU-010 closeout status.

## What not to test

- Do not automate real `npm publish` in ordinary package tests or selected CI.
- Do not require ordinary contributors to configure npm trusted publishing.
- Do not test future `status`, `validate`, workflow YAML, generated workflow docs, or other deferred commands.
- Do not bundle adapter archives into npm only to simplify tests.
- Do not rely on snapshots alone for tarball content, publication evidence, or workflow behavior.
- Do not attempt to mutate an already-published npm version as a rollback test.

## Uncovered gaps

None that require returning to spec or architecture.

External proof remains manual/release-owned for npm package ownership, trusted-publisher registry settings, maintainer 2FA, real npm publication, and public registry propagation. Those are covered by publication evidence and M6b manual/e2e smoke rather than ordinary CI.

## Next artifacts

- test-spec-review or maintainer approval.
- implement M1 after test-spec approval.

## Follow-on artifacts

None yet.

## Readiness

Ready for test-spec review or maintainer approval.

Implementation is not ready until this test spec is approved.
