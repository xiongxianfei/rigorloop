# First Public npm Release for `@xiongxianfei/rigorloop`

## Status

accepted

## Problem

RigorLoop now has an implemented CLI package candidate with the one-package public shape, Codex init, durable lockfile support, and `new-change` scaffolding. Users still cannot install it from npm:

```text
npm view @xiongxianfei/rigorloop --registry=https://registry.npmjs.org
-> E404 Not Found
```

That blocks the intended public quick-start path:

```bash
npx @xiongxianfei/rigorloop@latest init --adapter codex
```

The accepted CLI proposal explicitly blocked public npm publication until package ownership, package contents, `bin` entries, provenance, release workflow controls, dependency policy, lifecycle-script policy, versioning, rollback behavior, and publish validation are defined. `FU-010` records that release hardening as required before publication.

Continuing into `status`, `validate`, workflow YAML, or generated workflow docs would add feature depth, but it would not solve the adoption bottleneck. The next direction-setting slice should make the existing CLI safely publishable.

## Goals

- Publish the first public npm version of `@xiongxianfei/rigorloop`.
- Keep one package and one executable:
  - package: `@xiongxianfei/rigorloop`;
  - binary: `rigorloop`.
- Support the already-approved public user flows:
  - `npx @xiongxianfei/rigorloop@latest init --adapter codex`;
  - `npx @xiongxianfei/rigorloop@<version> init --adapter codex`;
  - `rigorloop init --adapter codex`;
  - `rigorloop new-change <change-id> --title "..."`
- Preserve the source-of-truth boundary: npm is a delivery channel, not the canonical source for skills, workflow rules, schemas, templates, or adapters.
- Publish only the CLI package, not bundled adapter archives.
- Keep adapter archives as GitHub release artifacts verified by the CLI.
- Define release-policy artifacts for trusted publishing, provenance, package contents, dependency policy, lifecycle-script policy, versioning, rollback, and publish validation.
- Review package tarball contents before publication.
- Add automated package tarball content checks before publication.
- Define the first-publication bootstrap path, publish gate, version mapping, and publication evidence surface before spec implementation.
- Keep first public publication from weakening RigorLoop workflow claim boundaries.

## Non-goals

- Do not implement `rigorloop status`.
- Do not implement `rigorloop validate`.
- Do not add machine-readable workflow YAML.
- Do not add generated workflow docs, diagrams, or frozen workflow drift checks.
- Do not create `@rigorloop/cli`, `@rigorloop/create`, or `create-rigorloop`.
- Do not bundle adapter archives into the npm package.
- Do not make npm package contents canonical source for skills, schemas, templates, workflow rules, or adapters.
- Do not publish before trusted publishing or an explicitly approved fallback publish path is ready.
- Do not change workflow stage order.
- Do not add new CLI feature behavior beyond what is necessary for safe public package publication.
- Do not close `FU-006` through `FU-009`.

## Vision fit

fits the current vision

Publishing the CLI makes RigorLoop easier to adopt while preserving artifact-first delivery. The package should make existing rigor easier to access, not replace durable proposals, specs, plans, validation evidence, or review records.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
|---|---|---|
| Publish the first public `@xiongxianfei/rigorloop` npm package safely | in scope | Goals, Recommended direction |
| Support `npx @xiongxianfei/rigorloop@latest init --adapter codex` | in scope | Goals, Expected behavior changes |
| Support pinned `npx @xiongxianfei/rigorloop@<version>` usage | in scope | Goals, Release versioning |
| Support installed `rigorloop init --adapter codex` usage | in scope | Goals, Expected behavior changes |
| Keep one package and one binary | in scope | Goals, Package contract |
| Preserve npm as delivery only, not source of truth | in scope | Goals, Architecture impact |
| Publish CLI only and avoid bundled adapter archives | in scope | Package contract, Risks and mitigations |
| Add trusted publishing, provenance, package contents, dependency, lifecycle-script, versioning, rollback, and publish validation policy | in scope | Publishing security boundary, Testing and verification strategy |
| Do not implement `status`, `validate`, workflow YAML, or generated workflow docs | deferred follow-up | Non-goals, Follow-up handling |
| Close `FU-010` only after successful publication evidence | in scope | Acceptance criteria, Follow-on artifacts |
| Define first-publish bootstrap, publish trigger, version mapping, tarball checks, package policy, `private: true`, and evidence path before spec/plan | in scope | First publication scope, Publishing security boundary, Publish gate ownership, Version mapping, Package policy checks, Publication evidence |

## Context

The accepted CLI proposal chose one public npm package:

```text
@xiongxianfei/rigorloop
```

with one executable:

```text
rigorloop
```

The implemented package candidate currently has that package name and binary in `packages/rigorloop/package.json`, plus a `files` allowlist. It still has `"private": true`, which npm documents as causing npm to refuse publication. The existing `.github/workflows/release.yml` creates GitHub releases and uploads release-output assets, but it does not publish the npm package and does not request OIDC `id-token: write` permission.

npm's package metadata docs identify `name` and `version` as the critical publication identity fields, describe `bin` as the executable-linking mechanism, describe `files` as the package inclusion allowlist, and note that omitting `files` defaults to broad inclusion. They also document that `"private": true` prevents publication. The trusted publishing docs describe OIDC-based npm publishing from supported CI systems and call out `id-token: write` as the critical GitHub Actions permission for OIDC tokens.

References:

- npm `package.json` docs: <https://docs.npmjs.com/cli/v11/configuring-npm/package-json/>
- npm trusted publishing docs: <https://docs.npmjs.com/trusted-publishers/>
- npm `npm trust` docs: <https://docs.npmjs.com/cli/v11/commands/npm-trust/>

## Options considered

### Option 1: Keep the package unpublished and continue feature work

Advantages:

- Avoids immediate npm supply-chain and release-process risk.
- Allows `status`, `validate`, and workflow YAML to mature before public exposure.

Disadvantages:

- Users still cannot run the intended public quick start.
- Adoption remains tied to repository checkout or local tarball workflows.
- Additional feature depth does not prove public package safety.

### Option 2: Publish manually with a maintainer token

Advantages:

- Fastest route to an npm package.
- Lower GitHub Actions workflow scope.

Disadvantages:

- Introduces long-lived token handling unless tightly constrained.
- Weakens the supply-chain hardening boundary recorded in `FU-010`.
- Makes provenance and repeatability harder to review.
- Creates an emergency path as the default path.

### Option 3: Add trusted publishing and package-content hardening first

Advantages:

- Solves the adoption blocker while respecting the accepted publication boundary.
- Uses a reviewable release workflow and package-content proof.
- Avoids long-lived publish tokens for the normal path.
- Keeps package contents, dependencies, lifecycle scripts, and rollback policy explicit before publication.

Disadvantages:

- Requires npm trusted publisher setup outside repository code.
- Requires release workflow changes and packed-package smoke tests before publish.
- Defers other CLI follow-ups for one more slice.

### Option 4: Bundle adapter archives in npm to make install fully offline

Advantages:

- Could reduce network dependency during `init --adapter codex`.
- Makes package install self-contained for the adapter archive.

Disadvantages:

- Conflicts with the accepted adapter artifact model.
- Risks making npm package contents appear canonical for generated adapter output.
- Enlarges the package and release surface.
- Reopens a boundary already settled by the CLI and lockfile slices.

## Recommended direction

Choose Option 3.

Create a focused release-hardening slice for first public npm publication. The first public package should expose the current approved CLI behavior without adding new command surfaces:

```text
@xiongxianfei/rigorloop
  bin: rigorloop
  commands: help, version, init --adapter codex, new-change
```

Normal publication should use GitHub Actions trusted publishing with npm OIDC. The package tarball should be allowlisted and smoke-tested before publication. Adapter archives should remain GitHub release artifacts; the npm package should ship only the CLI code and bundled metadata needed to verify adapter installs.

## First publication scope

This proposal publishes the existing approved CLI behavior only.

In scope:

- package hardening;
- package-content checks;
- trusted-publishing setup;
- packed-package smoke tests;
- release notes and publication evidence;
- first public npm publish.

Out of scope:

- `status`;
- `validate`;
- workflow YAML;
- generated workflow docs;
- new adapter packaging behavior;
- new CLI feature behavior.

## Package contract

The public package should keep:

```json
{
  "name": "@xiongxianfei/rigorloop",
  "bin": {
    "rigorloop": "dist/bin/rigorloop.js"
  }
}
```

The publication slice should define an intentional package-content allowlist. The expected runtime contents are:

```text
package.json
README.md
LICENSE or package-local license evidence
dist/bin/rigorloop.js
dist/lib/**
dist/metadata/**
```

The package should exclude:

```text
.git/
node_modules/
tests unless intentionally published
docs lifecycle artifacts unless intentionally published
release-output/
temporary files
local fixtures not needed by runtime
adapter archives
.codex/
dist/adapters/** generated skill bodies
```

The first publication slice should remove `"private": true` from `packages/rigorloop/package.json` after release-hardening controls are implemented and before publication. The tested package should be the same package that is published; publish-time mutation of `package.json` should be avoided unless a later spec explicitly defines and tests that transformation.

The package should include a package-local license file:

```text
packages/rigorloop/LICENSE
```

The package should also keep the `license` field in `packages/rigorloop/package.json`. The npm tarball should be self-contained for ordinary package inspection rather than relying only on repository-root license inclusion behavior.

## Publishing security boundary

Preferred publication path:

```text
GitHub Actions trusted publishing with npm OIDC
```

The release-hardening spec should define:

- npm ownership or maintainer access for `@xiongxianfei/rigorloop`;
- trusted publisher configuration for the GitHub repository and exact publish workflow;
- `id-token: write` on the publish job;
- release trigger policy, likely protected release tags or a release workflow approved by maintainers;
- action pinning or approved action-version policy;
- package-content proof before publish;
- required validation before publish;
- provenance expectations;
- no token-based publication in the normal path;
- emergency fallback criteria, if token publication is retained at all.

## First-publication bootstrap

The publication spec must define how `@xiongxianfei/rigorloop` is first claimed on npm. The accepted first-publication direction assumes a one-time manual bootstrap publish is likely required for `@xiongxianfei/rigorloop@0.1.4`, followed immediately by trusted publishing configuration.

Preferred path:

- configure trusted publishing before the first public publish, if npm supports that flow for this package;
- publish through the configured GitHub Actions trusted publisher.

Fallback path:

- allow a one-time maintainer bootstrap publish for `@xiongxianfei/rigorloop@0.1.4` only if trusted publishing cannot be configured for an unpublished package;
- require maintainer 2FA, the same package-content checks, packed-package smoke tests, and explicit approval;
- after bootstrap publication, configure trusted publishing and restrict token publishing before the next release.

The fallback is not the normal release path.

## Publish gate ownership

The maintainer-facing release readiness gate should remain:

```bash
bash scripts/release-verify.sh <version>
```

or a release workflow that invokes it before `npm publish`.

The existing `.github/workflows/release.yml` should own publication rather than adding a parallel workflow. An npm publish job may run only after release verification, package-content checks, packed-package smoke tests, and maintainer approval have passed.

For the first public npm release, the approved trigger is the protected stable tag:

```text
v0.1.4
```

For later stable npm releases, the publish trigger may generalize to stable semver tags:

```text
vX.Y.Z
```

The workflow should not publish on branches, pull requests, release candidates such as `vX.Y.Z-rc.N`, workflow runs without a tag, or manual dispatch without matching release approval. If the workflow uses a broad tag glob such as `v*.*.*`, the release script or workflow must still enforce the stable semver pattern and verify that `packages/rigorloop/package.json` version equals the tag without the leading `v`.

## Dependency and lifecycle-script policy

The first public package should prefer zero runtime dependencies.

If runtime dependencies are introduced, each should have a specific runtime reason and be reviewed as part of the publication spec. The package should avoid `preinstall`, `install`, `postinstall`, `prepare`, `prepack`, or consumer-install-time build behavior unless a later accepted release policy justifies it.

Build or packaging steps should happen before publication and should be verified through package smoke tests, not during consumer install.

## Package policy checks

The release-hardening spec and test-spec should make package policy enforceable:

- no `preinstall`, `install`, or `postinstall` scripts;
- no `prepare` or `prepack` script unless explicitly justified by the spec;
- no runtime dependencies unless each dependency has a recorded runtime purpose;
- no dependency install or build step during consumer install;
- no package scripts that require secrets or network access for normal install;
- exactly one public binary target, `rigorloop`.

## Version mapping

For the first public npm release, use one release line:

```text
repository tag: v0.1.4
npm package: @xiongxianfei/rigorloop@0.1.4
compatible adapter release: v0.1.4
```

Do not create a separate package-publication version. The first public package version should match the repository release tag and compatible adapter release version so pinned user commands stay simple:

```bash
npx @xiongxianfei/rigorloop@0.1.4 init --adapter codex
```

The spec must record:

- npm package version;
- compatible adapter release tag;
- bundled metadata version;
- GitHub release archive names;
- whether `latest` resolves to the same adapter release as the package version.

If a later release ever differs package and adapter versions, that mapping must be explicit in package metadata and release notes before publication.

Documentation should prefer pinned examples for CI and agents:

```bash
npx @xiongxianfei/rigorloop@<published-version> init --adapter codex
```

and allow `latest` for human quick starts:

```bash
npx @xiongxianfei/rigorloop@latest init --adapter codex
```

## Expected behavior changes

After the slice is complete and publication succeeds:

- `npm view @xiongxianfei/rigorloop` returns the published package metadata.
- Users can install or execute the CLI from npm.
- The package exposes exactly one executable, `rigorloop`.
- `rigorloop --help` and `rigorloop version` work from an installed package.
- `init --adapter codex` and `new-change` work from the packed and published package.
- Package contents are small, intentional, and reviewed.
- Adapter archives remain external verified release artifacts, not npm package contents.
- `FU-010` can close after publication evidence is recorded.
- `FU-006` through `FU-009` remain open.

## Architecture impact

The change affects release and packaging boundaries rather than core workflow behavior:

- `packages/rigorloop/package.json` becomes a public package contract instead of only a package candidate.
- `.github/workflows/release.yml` or a new publish workflow becomes part of the release trust boundary.
- Release validation may gain package-content and packed-package smoke checks.
- Release notes gain npm install and `npx` examples.
- `docs/follow-ups.md` remains the deferred-work register, with `FU-010` closing only after publication evidence.

The canonical source boundary should remain unchanged:

- authored workflow and skills stay in repository source surfaces;
- adapter archives stay GitHub release artifacts;
- npm ships the CLI delivery mechanism and trusted metadata needed for verification.

## Testing and verification strategy

The spec and test-spec should cover:

- package metadata correctness;
- exactly one public binary;
- package-content allowlist and automated tarball inspection;
- expected runtime files in the tarball;
- absence of adapter archives in the npm tarball;
- absence of `.codex/`, `dist/adapters/**/skills`, docs lifecycle artifacts, tests, fixtures, release-output, local temp files, secrets, and local paths in the tarball;
- dependency and lifecycle-script policy;
- `npm pack --dry-run` evidence;
- install smoke from the packed tarball;
- `rigorloop --help`;
- `rigorloop version`;
- `rigorloop init --adapter codex --dry-run --json`;
- `rigorloop init --adapter codex --from-archive ...` when a release archive fixture is available;
- `rigorloop new-change <id> --title "..." --dry-run --json`;
- stable JSON and exit-code behavior from the packed package;
- trusted publishing workflow shape, permissions, trigger, and provenance expectations.

The later plan should reuse repository-owned validation scripts where possible and add package-release checks only where current validation lacks the proof surface.

## Rollout and rollback

Rollout should proceed in these stages:

1. Proposal review accepts the public npm publication direction.
2. Spec defines package contract, release policy, trusted publishing, package content, version mapping, rollback, and validation.
3. Architecture or ADR records the release trust boundary if review requires a long-lived design artifact.
4. Plan and test-spec define reviewable implementation milestones.
5. Implementation adds package-content checks, packed-package smoke tests, release workflow changes, release notes, and publication evidence.
6. Maintainer configures npm trusted publisher outside the repository.
7. Release workflow publishes the package.
8. `FU-010` closes after public npm evidence is recorded.

Publication evidence should be recorded under:

```text
docs/releases/<version>/npm-publication.md
```

or in a release metadata section with the same fields. Required evidence fields:

- package name;
- published version;
- npm package URL;
- source commit;
- publish workflow run;
- package tarball evidence path;
- packed-package smoke result;
- trusted publishing or provenance status;
- rollback or deprecation note, if applicable.

Rollback for a bad package should prefer:

- publish a fixed patch version;
- document the bad version and recommended fixed version;
- avoid relying on mutable `latest` in CI and agent examples;
- deprecate the bad npm version when appropriate.

If trusted publishing setup fails, do not publish. Record the blocker and either finish trusted publishing setup or approve a narrow emergency fallback in the spec.

If package-content proof finds unintended files, do not publish. Tighten the package allowlist and rerun pack proof.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| npm package becomes mistaken for source of truth | State in package docs and release notes that canonical sources remain in the repository and npm is CLI delivery only. |
| Supply-chain risk | Use trusted publishing/OIDC, restricted release triggers, package-content proof, minimal dependencies, and no unnecessary lifecycle scripts. |
| Package includes unintended files | Use a strict `files` allowlist plus `npm pack --dry-run` and tarball inspection tests. |
| `latest` changes break users | Document pinned versions for reproducible setup, CI, and agents. |
| Adapter archives are bundled accidentally | Add package-content checks that fail on adapter ZIPs or generated adapter package output. |
| Feature scope expands into `status`, `validate`, workflow YAML, or generated docs | Keep this proposal publication-only and leave `FU-006` through `FU-009` open. |
| Trusted publisher configuration cannot be represented fully in git | Record the required out-of-repo setup and proof evidence before publishing. |
| Manual token fallback becomes the normal path | Treat token publishing as disallowed unless an accepted spec defines an emergency-only fallback. |

## Open questions

No proposal-level questions remain open.

The spec still needs to define operational details for the accepted decisions, including exact package-content validation, packed-package smoke command shape, one-time bootstrap evidence, trusted-publisher post-bootstrap proof, and release workflow changes.

## Acceptance criteria

- `@xiongxianfei/rigorloop` package ownership or maintainer access is confirmed.
- The first public npm version is `@xiongxianfei/rigorloop@0.1.4`, published from repository tag `v0.1.4`.
- `package.json` exposes exactly one public binary: `rigorloop`.
- Package contents are allowlisted and reviewed.
- `packages/rigorloop/LICENSE` exists and is included in the package tarball.
- `npm pack --dry-run` output is recorded and contains no unexpected files.
- Automated package tarball inspection proves expected runtime files are present and forbidden files are absent.
- Runtime dependency list is empty or justified.
- No unnecessary install lifecycle scripts exist.
- Trusted publishing or an approved fallback publish path is configured.
- First publication uses a one-time maintainer bootstrap only if trusted publishing cannot be configured before package creation.
- Trusted publishing is configured after bootstrap and required for later releases.
- The publish workflow uses OIDC for trusted publishing.
- Existing `.github/workflows/release.yml` owns npm publication after release verification.
- Publish workflow is restricted to the approved stable release trigger.
- The release gate runs `bash scripts/release-verify.sh <version>` or an equivalent release workflow that invokes it before `npm publish`.
- `private: true` is removed from the package before publication without untested publish-time mutation.
- Package-to-adapter release version mapping is recorded before publication.
- Packed-package install smoke passes.
- `rigorloop --help`, `rigorloop version`, `init --adapter codex`, and `new-change` smoke tests pass from the packed package.
- Adapter archives are not bundled into the npm package.
- Release notes explain how to install and run the package.
- Publication evidence is recorded under `docs/releases/<version>/npm-publication.md` or an equivalent release metadata section.
- `FU-006` through `FU-009` remain deferred.
- `FU-010` closes only after successful public publication evidence is recorded.

## Follow-up handling

Do not open or implement these before first publication unless a blocker proves they are required:

```text
FU-006: rigorloop status
FU-007: rigorloop validate
FU-008: workflow YAML
FU-009: generated workflow docs / frozen checks
```

After first publication, choose the next CLI follow-up based on user feedback, dependency order, and adoption value.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
|---|---|---|---|
| 2026-05-16 | Prioritize first public npm publication over `FU-006` through `FU-009`. | Users need an installable CLI before additional command depth creates much adoption value. | Implementing `status`, `validate`, workflow YAML, or generated docs first. |
| 2026-05-16 | Keep one package: `@xiongxianfei/rigorloop`. | This matches the accepted CLI direction and keeps user commands simple. | `@rigorloop/cli`, `@rigorloop/create`, `create-rigorloop`. |
| 2026-05-16 | Do not bundle adapter archives in npm. | Adapter archives remain verified release artifacts; npm is CLI delivery only. | Shipping adapter ZIPs inside the package. |
| 2026-05-16 | Prefer trusted publishing with npm OIDC. | Public npm publication creates a supply-chain and compatibility surface. | Manual publish with a long-lived npm token as the normal path. |
| 2026-05-16 | Require the spec to define first-publication bootstrap, publish gate, version mapping, tarball checks, package policy, `private: true` removal, and publication evidence. | Proposal review found these trust details must be settled before spec/plan. | Leaving trusted publishing, versioning, tarball review, or evidence shape as generic implementation choices. |
| 2026-05-16 | Publish first as `@xiongxianfei/rigorloop@0.1.4` from repository tag `v0.1.4`. | One version line keeps package, repository release, and adapter metadata simple for pinned user commands. | Separate package-publication version. |
| 2026-05-16 | Use the existing `.github/workflows/release.yml` as the npm publication workflow. | One release workflow is easier to reason about and configure as the trusted publisher. | A parallel npm-only workflow for the first publication. |
| 2026-05-16 | Allow one-time manual bootstrap only if trusted publishing cannot claim an unpublished package, then require trusted publishing for future releases. | Keeps first publication practical without making token/manual publication the normal path. | Permanent token-based publishing or blocking first publish indefinitely. |
| 2026-05-16 | Add `packages/rigorloop/LICENSE`. | The package tarball should be self-contained and easy to audit. | Relying only on repository-root license inclusion behavior. |

## Next artifacts

```text
proposal-review
spec for npm publication hardening and package contract
architecture or ADR only if release trust boundary review requires it
plan
test-spec
implement
code-review
explain-change
verify
publish
```

## Follow-on artifacts

- `docs/changes/2026-05-16-first-public-npm-release/reviews/proposal-review-r1.md` approved the proposal with no material findings.

## Readiness

Accepted and ready for spec.

## Core invariant

```text
First make RigorLoop installable.

One package.
One binary.
Minimal package contents.
Trusted publishing.
Adapters remain verified release artifacts.
Future commands wait until users can install the CLI.
```
