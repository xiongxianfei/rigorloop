# RigorLoop npm Publication

## Status

approved

## Related proposal

- [First Public npm Release for `@xiongxianfei/rigorloop`](../docs/proposals/2026-05-16-first-public-npm-release.md)

## Goal and context

This spec defines the first public npm publication contract for the RigorLoop CLI package.

The first public npm release publishes:

```text
repository tag: v0.1.4
npm package: @xiongxianfei/rigorloop@0.1.4
compatible adapter release: v0.1.4
```

The purpose is to make the already-approved CLI behavior installable through npm without adding new command behavior. The package remains a delivery channel. Canonical workflow content, skills, schemas, templates, and adapter definitions remain repository-owned source surfaces, and generated adapter archives remain GitHub release artifacts verified by the CLI.

This spec builds on the approved CLI package, Codex init, lockfile, and new-change contracts. It replaces the previous "public npm publication remains blocked" state for the `v0.1.4` release only after every requirement in this spec is satisfied.

## Glossary

- `CLI package`: the package under `packages/rigorloop`, published as `@xiongxianfei/rigorloop`.
- `public npm package`: the package visible on the public npm registry.
- `first public npm release`: `@xiongxianfei/rigorloop@0.1.4` published from repository tag `v0.1.4`.
- `release workflow`: `.github/workflows/release.yml`.
- `release gate`: the repository-owned release readiness command `bash scripts/release-verify.sh <version>`.
- `package tarball`: the `.tgz` artifact produced by `npm pack --prefix packages/rigorloop`.
- `packed-package smoke`: tests that install the packed `.tgz` into a temporary project and run the published-shape CLI.
- `trusted publishing`: npm OIDC publication from GitHub Actions configured for the package and release workflow.
- `bootstrap publish`: one-time manual publication used only if trusted publishing cannot be configured before the package exists.
- `publication mode`: the mutually exclusive path used to publish a package version: `trusted-publishing` or `bootstrap`.
- `publication evidence`: the durable release artifact that records npm publication proof.
- `adapter release`: the GitHub release whose adapter archives and metadata are compatible with the npm package version.

## Examples first

### Example E1: first public package is installable

Given repository tag `v0.1.4` has passed the release gate
And `@xiongxianfei/rigorloop@0.1.4` has been published
When a user runs `npm view @xiongxianfei/rigorloop@0.1.4 version`
Then npm returns `0.1.4`.

### Example E2: pinned npx init uses the matching release line

Given `@xiongxianfei/rigorloop@0.1.4` is published
When a user runs:

```bash
npx @xiongxianfei/rigorloop@0.1.4 init --adapter codex --dry-run --json
```

Then the command runs the `0.1.4` package
And adapter compatibility resolves to `v0.1.4`
And stdout uses the existing CLI JSON envelope.

### Example E3: package exposes one executable

Given the package tarball has been packed from `packages/rigorloop`
When the tarball is inspected
Then `package.json` contains exactly one `bin` entry:

```json
{
  "rigorloop": "dist/bin/rigorloop.js"
}
```

And no other public binary is exposed.

### Example E4: package tarball contains only runtime files

Given `npm pack --prefix packages/rigorloop` produces a package tarball
When package-content validation inspects the tarball
Then it includes package metadata, README, LICENSE, runtime `dist/bin`, runtime `dist/lib`, and runtime `dist/metadata`
And it does not include tests, change artifacts, release-output, `.codex`, adapter ZIPs, or generated adapter skill bodies.

### Example E5: packed package smoke proves CLI behavior

Given the package tarball has passed content validation
When it is installed into a temporary project
Then the installed `rigorloop` binary supports:

```bash
rigorloop --help
rigorloop version
rigorloop init --adapter codex --dry-run --json
rigorloop new-change test-change --title "Test change" --dry-run --json
```

And each command exits with the existing public exit-code contract.

### Example E6: first publication bootstrap is recorded

Given npm does not allow trusted-publisher configuration before the package exists
When the maintainer performs the one-time bootstrap publish for `@xiongxianfei/rigorloop@0.1.4`
Then the same release gate, package-content validation, and packed-package smoke must pass before publish
And publication evidence records bootstrap publication and trusted publishing configuration for future releases.

### Example E7: release candidates do not publish npm

Given a tag such as `v0.1.4-rc.1`
When the release workflow runs
Then GitHub release behavior may follow existing release-candidate rules
But npm publication must not run.

### Example E8: bootstrap publishes only a verified tarball

Given npm trusted publishing cannot be configured before `@xiongxianfei/rigorloop` exists
And release verification, package-content validation, and packed-package smoke passed for `v0.1.4`
When the maintainer uses bootstrap mode
Then the maintainer may publish only the exact tarball recorded in publication evidence
And publication evidence records the tarball filename, SHA-256, source commit, package version, pack command, smoke result, approving maintainer, publish command, and npm package URL.

### Example E9: real Codex install smoke closes FU-010

Given `@xiongxianfei/rigorloop@0.1.4` is packed or published
And the official `v0.1.4` Codex adapter archive is externally observable
When verification runs:

```bash
rigorloop init --adapter codex --json
```

from the packed or published package in a temporary project
Then the command performs the real non-dry-run install path
And archive checksum, archive size, safe extraction, and installed tree hash verification pass
And FU-010 may close only after that proof is recorded.

## Requirements

### Release identity

R1. The first public npm release MUST publish package `@xiongxianfei/rigorloop`.

R2. The first public npm package version MUST be `0.1.4`.

R3. The first public npm package MUST be published from repository tag `v0.1.4`.

R4. The first public npm package MUST map to compatible adapter release `v0.1.4`.

R5. The first public npm package MUST NOT use a separate package-publication version line.

R6. `packages/rigorloop/package.json` MUST use:

```json
{
  "name": "@xiongxianfei/rigorloop",
  "version": "0.1.4"
}
```

R7. `packages/rigorloop/package.json` MUST NOT contain `"private": true` for the published package.

R8. The package tested by the release gate MUST be the same package published to npm. The release process MUST NOT mutate package identity, package version, `private`, `files`, `bin`, runtime dependencies, or lifecycle scripts only at publish time.

R9. Release metadata and release notes for `v0.1.4` MUST record that npm package `@xiongxianfei/rigorloop@0.1.4` maps to adapter release `v0.1.4`.

### Package command surface

R10. The public package MUST expose exactly one binary named `rigorloop`.

R11. The `bin` field MUST map `rigorloop` to `dist/bin/rigorloop.js`.

R12. The `bin` target file MUST exist in the package tarball.

R13. The `bin` target file MUST start with a Node shebang so npm-installed command execution can launch it through Node.

R14. The package MUST NOT expose `create-rigorloop`, `@rigorloop/create`, `@rigorloop/cli`, or any second binary.

R15. The public package MUST support only the CLI behavior already approved by the existing CLI specs: help/version, `init --adapter codex`, durable lockfile writes after verified init, and `new-change`.

R16. This spec MUST NOT add new CLI command behavior.

### Package contents

R17. `packages/rigorloop/package.json` MUST use a package-content allowlist through `files`.

R18. The `files` allowlist MUST include runtime `dist/`, `package.json`, `README.md`, and `LICENSE`.

R19. The package tarball MUST include these logical package paths:

```text
package/package.json
package/README.md
package/LICENSE
package/dist/bin/rigorloop.js
package/dist/lib/command-result.js
package/dist/lib/lockfile.js
package/dist/lib/new-change-filesystem.js
package/dist/lib/new-change.js
package/dist/lib/official-archive-url.js
package/dist/metadata/adapter-artifacts-v0.1.4.json
package/dist/metadata/releases.json
```

R20. `packages/rigorloop/LICENSE` MUST exist and MUST be included in the package tarball.

R21. `packages/rigorloop/package.json` MUST include a valid SPDX `license` field.

R22. The package tarball MUST NOT include any path matching:

```text
package/test/**
package/tests/**
package/__fixtures__/**
package/docs/**
package/release-output/**
package/.codex/**
package/.agents/**
package/dist/adapters/**
package/**/*.zip
package/**/*.tgz
package/**/*.pem
package/**/*.key
package/**/*.env
```

R23. The package tarball MUST NOT include generated public adapter skill bodies.

R24. The package tarball MUST NOT include adapter release archives.

R25. The package tarball MUST NOT include secrets, npm tokens, `.npmrc`, machine-local paths, usernames, host-specific directories, or temporary files.

R26. Package-content validation MUST fail before publication if any required file is missing or any forbidden path is present.

R27. `npm pack --dry-run --prefix packages/rigorloop` output MUST be recorded as release evidence or package-content evidence before publication.

### Package policy

R28. The first public package SHOULD have zero runtime dependencies.

R29. If runtime dependencies are added, each dependency MUST have a recorded runtime purpose in the spec revision or release evidence before publication.

R30. The package MUST NOT define `preinstall`, `install`, or `postinstall` scripts.

R31. The package MUST NOT define `prepare` or `prepack` scripts unless a later approved spec revision explicitly justifies and tests that behavior.

R32. The package MUST NOT perform dependency installation, builds, network access, or secret access during consumer installation.

R33. Package scripts MUST NOT require secrets or network access for normal installation.

R34. `publishConfig` MAY be used to constrain public registry and provenance behavior, but it MUST NOT weaken this spec's package-content, dependency, lifecycle-script, or trigger requirements.

### Release gate and workflow

R35. The maintainer-facing release gate for npm publication MUST be:

```bash
bash scripts/release-verify.sh v0.1.4
```

R36. The first public npm publication MUST use exactly one publication mode:

- `trusted-publishing`
- `bootstrap`

R36a. Publication evidence MUST record the selected publication mode.

R36b. The release process MUST NOT publish the same package version through both publication modes.

R36c. If the selected mode is `trusted-publishing`, the existing release workflow `.github/workflows/release.yml` MUST own npm publication for this slice.

R36d. If the selected mode is `bootstrap`, `.github/workflows/release.yml` MUST NOT also publish `@xiongxianfei/rigorloop@0.1.4`.

R36e. In bootstrap mode, `.github/workflows/release.yml` or `bash scripts/release-verify.sh v0.1.4` owns release readiness, but not npm publication.

R36f. In bootstrap mode, npm publication is a one-time manual publish of the exact verified tarball recorded in publication evidence.

R37. A separate npm-only publish workflow MUST NOT be introduced for the first public release.

R38. In trusted-publishing mode, the release workflow MUST run the release gate before npm publication.

R39. In trusted-publishing mode, the release workflow MUST run package-content validation before npm publication.

R40. In trusted-publishing mode, the release workflow MUST run packed-package smoke before npm publication.

R41. The release workflow MUST NOT publish npm for branches, pull requests, release-candidate tags, untagged workflow runs, or manual dispatch without matching release approval.

R42. The first npm publication trigger MUST be the stable tag `v0.1.4`.

R43. Later stable npm publication triggers MAY generalize to tags matching `^v[0-9]+\.[0-9]+\.[0-9]+$`.

R44. The release workflow or release script MUST reject npm publication unless the tag matches `^v[0-9]+\.[0-9]+\.[0-9]+$`.

R45. The release workflow or release script MUST reject npm publication unless `packages/rigorloop/package.json` version equals the tag without leading `v`.

R46. The release workflow MUST retain existing GitHub release behavior for release archives and release notes.

R47. The release workflow MUST not upload npm package tarballs as adapter archives or treat npm package tarballs as adapter install artifacts.

### Trusted publishing and bootstrap

R48. Trusted publishing with GitHub Actions OIDC MUST be the normal publication path after the one-time bootstrap.

R49. The release workflow publish job for trusted publishing MUST request `id-token: write`.

R50. The release workflow publish job for trusted publishing MUST use the npm public registry.

R51. Trusted publishing configuration MUST identify the package `@xiongxianfei/rigorloop`, the GitHub repository `xiongxianfei/rigorloop`, and the exact workflow file `.github/workflows/release.yml`.

R52. If npm trusted publishing can be configured before first publication, `@xiongxianfei/rigorloop@0.1.4` MUST be published through trusted publishing.

R53. If npm trusted publishing cannot be configured before first publication because the package does not yet exist, one-time manual bootstrap publication MAY be used for `@xiongxianfei/rigorloop@0.1.4` only.

R54. Bootstrap publication MUST require maintainer 2FA.

R55. Bootstrap publication MUST run the same release gate, package-content validation, and packed-package smoke required for trusted publication before `npm publish`.

R56. Bootstrap publication MUST publish exactly `@xiongxianfei/rigorloop@0.1.4`.

R57. Bootstrap publication MUST NOT become the normal path for later releases.

R58. After bootstrap publication, trusted publishing MUST be configured before the next npm release.

R59. Publication evidence MUST record whether `0.1.4` used trusted publishing or bootstrap publication.

R60. If bootstrap publication is used, publication evidence MUST record the follow-up proof that trusted publishing was configured after bootstrap or record a blocker preventing FU-010 closeout.

R61. When trusted publishing is used from the public repository, publication evidence MUST record whether npm provenance was generated.

R61a. A bootstrap publication MAY publish only a verified packed tarball whose identity is recorded before publication.

R61b. Bootstrap tarball identity MUST include:

- package name;
- package version;
- source commit;
- release tag;
- tarball filename;
- tarball SHA-256;
- `npm pack` command;
- package-content validation result;
- packed-package smoke result;
- approving maintainer;
- publish command;
- npm package URL after publication.

R61c. If bootstrap tarball identity is missing or the tarball SHA-256 differs from recorded evidence, bootstrap publication MUST block.

R61d. The maintainer MAY manually run `npm publish <tarball>` in bootstrap mode only for the exact packed tarball recorded by R61a through R61c.

### Packed-package smoke

R62. Packed-package smoke MUST install the generated `.tgz` into a temporary project before publication.

R63. Packed-package smoke MUST execute the installed `rigorloop` binary, not the repository-local script path.

R64. Packed-package smoke MUST verify:

```bash
rigorloop --help
rigorloop version
rigorloop init --adapter codex --dry-run --json
rigorloop new-change test-change --title "Test change" --dry-run --json
```

R65. Packed-package smoke MUST verify that `rigorloop version` reports `@xiongxianfei/rigorloop` and `0.1.4`.

R66. Packed-package smoke MUST verify that JSON-mode command output remains JSON-only.

R67. Packed-package smoke MUST verify that public exit codes remain consistent with the existing CLI contract.

R68. Packed-package smoke SHOULD include `rigorloop init --adapter codex --from-archive <path>` when a `v0.1.4` Codex release archive fixture or release-output artifact is available locally.

R69. Packed-package smoke MUST NOT require ordinary contributors to have npm publication credentials.

### Real Codex adapter install proof

R69a. Before FU-010 closes, verification MUST run an actual non-dry-run Codex adapter install from the packed or published package in a temporary project.

R69b. The actual install smoke command MUST run the package binary from the packed or published package, not the repository-local script path.

R69c. The actual install smoke MUST run:

```bash
rigorloop init --adapter codex --json
```

or the equivalent `npx @xiongxianfei/rigorloop@0.1.4 init --adapter codex --json` after publication.

R69d. Actual install smoke MUST prove that the official `v0.1.4` Codex adapter archive named by bundled metadata is reachable at the official GitHub release URL.

R69e. Actual install smoke MUST prove archive SHA-256 verification passed.

R69f. Actual install smoke MUST prove archive size verification passed when bundled metadata provides `size_bytes`.

R69g. Actual install smoke MUST prove archive extraction stayed inside the expected install root.

R69h. Actual install smoke MUST prove installed tree hash verification passed.

R69i. Actual install smoke MUST prove generated files exist under the expected Codex install root.

R69j. Actual install smoke MUST exit with public status `success`.

R69k. Dry-run smoke MUST NOT satisfy the real Codex adapter install proof required for FU-010 closeout.

R69l. If official `v0.1.4` adapter release assets are externally observable before npm publication, actual install smoke MUST pass before npm publication.

R69m. If npm publication happens before the GitHub release assets are externally observable, publication evidence MUST record the temporary ordering gap, and FU-010 MUST remain open until actual install smoke passes from the packed or published package.

### Release artifacts and documentation

R70. `docs/releases/v0.1.4/release.yaml` MUST exist before publication.

R71. `docs/releases/v0.1.4/release-notes.md` MUST exist before publication.

R72. `docs/releases/v0.1.4/release-notes.md` MUST include quick-start npm usage:

```bash
npx @xiongxianfei/rigorloop@latest init --adapter codex
```

R73. `docs/releases/v0.1.4/release-notes.md` MUST include pinned npm usage:

```bash
npx @xiongxianfei/rigorloop@0.1.4 init --adapter codex
```

R74. `docs/releases/v0.1.4/release-notes.md` MUST include local install usage:

```bash
npm install -D @xiongxianfei/rigorloop
npx rigorloop init --adapter codex
```

R75. Release notes MUST state that npm is the CLI delivery channel and not the canonical source for workflow rules, skills, schemas, templates, or adapter definitions.

R76. Release notes MUST state that adapter archives remain GitHub release artifacts verified by the CLI and are not bundled in the npm package.

R77. Publication evidence MUST be recorded at:

```text
docs/releases/v0.1.4/npm-publication.md
```

R78. Publication evidence MUST include:

- package name;
- published version;
- npm package URL;
- source commit;
- repository tag;
- publication mode;
- publish workflow run or bootstrap evidence;
- package tarball evidence path or summary;
- packed-package smoke result;
- real Codex adapter install smoke result;
- trusted publishing status;
- provenance status when available;
- rollback or deprecation note, if applicable.

R78a. Publication evidence for the package tarball MUST include:

```yaml
publication:
  package: "@xiongxianfei/rigorloop"
  version: "0.1.4"
  release_tag: "v0.1.4"
  source_commit: "<sha>"
  mode: "trusted-publishing" # or "bootstrap"

workflow:
  release_workflow: ".github/workflows/release.yml"
  published_by_workflow: true # false in bootstrap mode
  unsupported_tags_rejected: true

tarball:
  filename: "xiongxianfei-rigorloop-0.1.4.tgz"
  sha256: "<sha256>"
  pack_command: "npm pack --prefix packages/rigorloop"
  content_check: pass
  smoke_result: pass

trusted_publishing:
  configured: true
  workflow: ".github/workflows/release.yml"
  id_token_write: true

bootstrap:
  used: false
  approving_maintainer: null
  publish_command: null

npm:
  published: true
  package_url: "https://www.npmjs.com/package/@xiongxianfei/rigorloop"
```

R78b. If bootstrap mode is used, publication evidence MUST set `publication.mode` to `bootstrap`, `bootstrap.used` to `true`, and record `bootstrap.approving_maintainer` and `bootstrap.publish_command`.

R78c. Publication evidence for actual Codex adapter install smoke MUST include:

```yaml
adapter_install_smoke:
  required_before_fu_close: true
  required_before_publish: "when official release assets are externally observable"
  command: "npx @xiongxianfei/rigorloop@0.1.4 init --adapter codex --json"
  temp_project: "<path-or-redacted-temp-path>"
  package_source: "published-npm" # or "packed-tarball"
  adapter: "codex"
  official_archive_url: "https://github.com/xiongxianfei/rigorloop/releases/download/v0.1.4/rigorloop-adapter-codex-v0.1.4.zip"
  archive_sha256_verified: true
  tree_hash_verified: true
  result: pass
  ran_at: "YYYY-MM-DDTHH:MM:SSZ"
```

R78d. If an ordering gap prevents actual install smoke before publication, publication evidence MUST record:

```yaml
adapter_install_smoke:
  result: pending
  ordering_gap: "npm package published before GitHub release assets were externally observable"
  fu_010_closeout_blocked: true
```

R79. FU-010 MUST NOT be closed until publication evidence exists and records successful public publication.

R79a. FU-010 MUST NOT be closed until actual non-dry-run `init --adapter codex --json` smoke passes from the packed or published package.

R80. FU-006 through FU-009 MUST remain open after this release unless separately accepted follow-ups close them.

### Post-publication verification

R81. After publication, verification MUST confirm:

```bash
npm view @xiongxianfei/rigorloop@0.1.4 version --registry=https://registry.npmjs.org
```

returns `0.1.4`.

R82. After publication, verification MUST confirm the package can be executed through npm or npx for at least `rigorloop --help` and `rigorloop version`.

R83. After publication, verification SHOULD confirm:

```bash
npx @xiongxianfei/rigorloop@0.1.4 init --adapter codex --dry-run --json
```

unless network, registry propagation, or local execution policy prevents it. Any inability MUST be recorded in publication evidence.

R84. If publication succeeds but post-publication verification fails, FU-010 MUST remain open until a fixed patch version is published or the failure is explicitly resolved.

R85. After publication, verification MUST confirm actual non-dry-run `init --adapter codex --json` from the published package unless the ordering-gap rule in R69m applies.

## Inputs and outputs

### Inputs

- repository tag `v0.1.4`;
- `packages/rigorloop/package.json`;
- runtime package files under `packages/rigorloop/dist/`;
- package-local `packages/rigorloop/LICENSE`;
- release metadata and release notes under `docs/releases/v0.1.4/`;
- adapter artifact metadata for `v0.1.4`;
- release workflow `.github/workflows/release.yml`;
- npm maintainer or trusted-publisher credentials/configuration.

### Outputs

- public npm package `@xiongxianfei/rigorloop@0.1.4`;
- package tarball evidence from `npm pack`;
- packed-package smoke evidence;
- GitHub release assets for adapter archives;
- publication evidence at `docs/releases/v0.1.4/npm-publication.md`;
- updated follow-up state only after publication evidence supports closeout.

## State and invariants

S1. Repository release tag, npm package version, bundled adapter metadata, and compatible adapter release MUST stay aligned for `v0.1.4`.

S2. The package tarball is a delivery artifact; it MUST NOT become a canonical authored source surface.

S3. The release gate owns readiness. `npm publish` MUST NOT be treated as a standalone proof of release readiness.

S4. Bootstrap publication is one-time release infrastructure setup, not a reusable release path.

S5. Publication evidence owns FU-010 closeout proof.

S6. Dry-run CLI smoke proves command availability, but it does not prove the real Codex adapter installation path.

## Error and boundary behavior

EB1. If the npm package name cannot be published or maintainer access is unavailable, publication MUST block before tag publication or npm publish.

EB2. If `private: true` remains in `packages/rigorloop/package.json`, publication MUST block.

EB3. If package version and tag mismatch, publication MUST block.

EB4. If package version and adapter release mapping mismatch, publication MUST block.

EB5. If package-content validation finds missing required files or forbidden files, publication MUST block.

EB6. If packed-package smoke fails, publication MUST block.

EB7. If release notes or release metadata are missing, publication MUST block.

EB8. If the workflow is triggered by an unsupported tag or non-tag event, npm publication MUST be skipped or blocked.

EB9. If trusted publishing is unavailable for first publish, bootstrap MAY proceed only when the bootstrap conditions in this spec are satisfied.

EB10. If bootstrap succeeds but trusted publishing cannot be configured afterward, FU-010 MUST remain open and publication evidence MUST record the blocker.

EB11. If a bad npm version is published, rollback MUST use a fixed patch release and documentation or deprecation of the bad version. The release process MUST NOT rely on mutating the bad package version in place.

EB12. If bootstrap tarball identity is missing or its SHA-256 does not match the tarball being published, bootstrap publication MUST block.

EB13. If actual Codex adapter install smoke is pending because GitHub release assets are not externally observable, npm publication MAY be complete but FU-010 closeout MUST remain blocked.

EB14. If actual Codex adapter install smoke fails due to missing official archive, checksum mismatch, size mismatch, extraction safety failure, or installed tree hash mismatch, FU-010 MUST remain open until the failure is fixed.

## Compatibility and migration

C1. Existing repository-checkout usage remains valid.

C2. Existing GitHub release adapter archive installation remains valid.

C3. Existing CLI command contracts for `init`, lockfile writes, and `new-change` remain authoritative and are not redefined by this spec.

C4. Documentation for CI and agents SHOULD prefer pinned npm versions rather than `latest`.

C5. Public npm publication MUST NOT change workflow stage order, review requirements, validation requirements, or PR-readiness claims.

C6. Future package versions MAY use trusted publishing only, but any change to version mapping or release trigger policy requires a later spec revision or follow-up.

## Observability

O1. Release validation output MUST identify package-content validation and packed-package smoke status.

O2. Publication evidence MUST record enough information to reconstruct how the package was built, checked, and published.

O3. If trusted publishing is used, publication evidence MUST record trusted publishing status and provenance status.

O4. If bootstrap publication is used, publication evidence MUST record bootstrap use and post-bootstrap trusted-publisher setup status.

O5. Release notes MUST make npm install and `npx` usage visible to users.

O6. Publication evidence MUST record actual Codex adapter install smoke status and any ordering gap that blocks FU-010 closeout.

## Security and privacy

SP1. Secrets, npm tokens, `.npmrc`, private keys, and credential files MUST NOT appear in the package tarball.

SP2. The normal publication path MUST use trusted publishing after bootstrap.

SP3. Long-lived npm tokens MUST NOT be committed, printed, or required for normal release workflow execution.

SP4. Bootstrap publication MUST require maintainer 2FA and explicit approval.

SP5. Package scripts MUST NOT perform install-time network access or secret access.

SP6. The release workflow MUST not publish npm packages from untrusted pull request code.

SP7. The tarball MUST not expose machine-local paths, usernames, or host-specific temporary files.

SP8. Bootstrap mode MUST NOT publish an unrecorded tarball or a tarball whose SHA-256 differs from recorded evidence.

## Accessibility and UX

No graphical UI is involved.

UX1. Release notes MUST include both quick-start and pinned usage examples.

UX2. Pinned examples MUST use `0.1.4` for the first public npm release.

UX3. User-facing docs MUST not imply that npm package files are canonical workflow or adapter source.

## Performance expectations

P1. Package-content validation and packed-package smoke SHOULD complete within ordinary release CI timeouts.

P2. The npm package SHOULD remain small enough that `npx @xiongxianfei/rigorloop@0.1.4 --help` does not require downloading adapter archives as part of package installation.

P3. Adapter archives MUST NOT be bundled into the package to keep package install size bounded.

## Edge cases

EC1. Tag is `v0.1.4-rc.1`: release may be created according to existing release-candidate behavior, but npm publication must not run.

EC2. Tag is `v0.1.4` but package version is `0.1.3`: publication blocks.

EC3. Package tarball includes `package/test/cli.test.js`: publication blocks.

EC4. Package tarball includes `package/dist/adapters/codex/.agents/skills/proposal/SKILL.md`: publication blocks.

EC5. Package tarball includes `package/rigorloop-adapter-codex-v0.1.4.zip`: publication blocks.

EC6. Package tarball omits `package/dist/metadata/adapter-artifacts-v0.1.4.json`: publication blocks.

EC7. Package tarball omits `package/LICENSE`: publication blocks.

EC8. `package.json` defines `postinstall`: publication blocks.

EC9. Trusted publishing cannot be configured before first package creation: one-time bootstrap may proceed only with required validation and 2FA evidence.

EC10. Bootstrap publication succeeds but trusted publisher setup is not completed: package remains published, but FU-010 remains open and the blocker is recorded.

EC11. npm registry propagation delays make post-publication `npx` smoke temporarily fail: publication evidence records the delay and follow-up verification is required before FU-010 closes.

EC12. `npm publish` succeeds but GitHub release creation fails: publication evidence records partial release state, and release owner must publish corrected evidence or a fixed release before closeout.

EC13. Bootstrap mode is selected and `.github/workflows/release.yml` also attempts to publish `@xiongxianfei/rigorloop@0.1.4`: publication blocks or the duplicate publish job is skipped, and publication evidence records one selected mode.

EC14. Bootstrap tarball SHA-256 is missing or mismatched: publication blocks.

EC15. Dry-run `init --adapter codex --json` passes but actual non-dry-run install smoke has not run: FU-010 remains open.

EC16. Official `v0.1.4` Codex release archive is missing or not externally observable after npm publication: FU-010 remains open until the archive is available and actual install smoke passes.

EC17. Actual Codex install smoke detects archive checksum mismatch or installed tree hash mismatch: FU-010 remains open until a fixed package or fixed release artifact is published.

## Non-goals

- Do not implement `rigorloop status`.
- Do not implement `rigorloop validate`.
- Do not add workflow YAML canonicality.
- Do not add generated workflow docs, diagrams, or frozen workflow drift checks.
- Do not create `@rigorloop/cli`, `@rigorloop/create`, or `create-rigorloop`.
- Do not bundle adapter archives into the npm package.
- Do not change the adapter archive source-of-truth model.
- Do not redefine CLI JSON, exit-code, lockfile, or `new-change` contracts except where packed-package smoke verifies existing behavior.
- Do not define future non-`vX.Y.Z` publication channels.
- Do not close FU-006 through FU-009.

## Acceptance criteria

- AC1. `packages/rigorloop/package.json` names `@xiongxianfei/rigorloop`, version `0.1.4`, has one `rigorloop` binary, and has no `private: true`.
- AC2. `packages/rigorloop/LICENSE` exists and is present in the packed tarball.
- AC3. Package policy validation proves forbidden lifecycle scripts are absent and runtime dependencies are absent or justified.
- AC4. Package-content validation proves the tarball includes all required runtime files and excludes all forbidden paths.
- AC5. `npm pack --dry-run --prefix packages/rigorloop` evidence is recorded.
- AC6. Packed-package smoke passes from a temporary install.
- AC7. `bash scripts/release-verify.sh v0.1.4` includes or invokes package-content and packed-package smoke checks before publication.
- AC8. Publication evidence proves exactly one publication mode.
- AC8a. Publication evidence records exactly one selected mode: `trusted-publishing` or `bootstrap`.
- AC8b. If mode is `trusted-publishing`, evidence proves `.github/workflows/release.yml` owns npm publication, uses the approved release trigger, and rejects unsupported tags.
- AC8c. If mode is `bootstrap`, evidence proves `.github/workflows/release.yml` did not publish `@xiongxianfei/rigorloop@0.1.4`.
- AC8d. If mode is `bootstrap`, evidence records the exact tarball filename, SHA-256, source commit, release tag, package version, pack command, package-content validation result, packed-package smoke result, approving maintainer, publish command, and npm package URL.
- AC8e. Bootstrap mode is allowed only for the first publication of `@xiongxianfei/rigorloop@0.1.4` when trusted publishing cannot be configured before package creation.
- AC9. The release workflow uses `id-token: write` for trusted publishing after bootstrap.
- AC10. The first public package is published as `@xiongxianfei/rigorloop@0.1.4` from tag `v0.1.4`.
- AC11. Publication evidence exists at `docs/releases/v0.1.4/npm-publication.md`.
- AC12. Post-publication verification confirms npm registry metadata for `@xiongxianfei/rigorloop@0.1.4`.
- AC13. Release notes include quick-start, pinned, and local install examples.
- AC14. Adapter archives are not bundled in the npm package.
- AC15. FU-010 is closed only after successful publication evidence and actual non-dry-run Codex adapter install smoke; FU-006 through FU-009 remain open.
- AC16. The publication evidence declares exactly one publication mode.
- AC17. Bootstrap mode, if used, records the exact verified tarball identity before publication.
- AC18. Dry-run smoke alone cannot close FU-010.
- AC19. Official Codex archive URL, checksum verification, extraction, and installed tree hash verification are recorded for actual install smoke.

## Open questions

None.

## Next artifacts

```text
architecture or ADR only if the release trust boundary review requires it
plan
plan-review
test-spec
implement
code-review
explain-change
verify
publish
```

## Follow-on artifacts

- Spec-review approved in `docs/changes/2026-05-16-first-public-npm-release/reviews/spec-review-r3.md`.
- Architecture/ADR authored in `docs/architecture/system/architecture.md` and `docs/adr/ADR-20260516-rigorloop-npm-publication.md`.

## Readiness

Approved for downstream architecture, plan, test-spec, and implementation work.
