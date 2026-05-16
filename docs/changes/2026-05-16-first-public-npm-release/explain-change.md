# Explain Change - First Public npm Release

## Summary

This change prepares the repository for the first public npm publication of `@xiongxianfei/rigorloop@0.1.4`.

It does not publish the package, close FU-010, or add deferred CLI features such as `status`, `validate`, workflow YAML, or generated workflow docs.

## Why This Changed

The accepted proposal and approved npm publication spec make public package availability the next useful slice after the CLI, Codex init, lockfile, and `new-change` work. Users need an installable package before later command surfaces add much value.

The governing boundary is:

- one package: `@xiongxianfei/rigorloop`;
- one binary: `rigorloop`;
- npm is a CLI delivery channel, not canonical workflow or adapter source;
- adapter archives remain GitHub release artifacts verified by the CLI;
- FU-010 closes only after public npm publication evidence and actual non-dry-run Codex adapter install proof.

## What Changed

### Package Contract

`packages/rigorloop` was prepared for `0.1.4` publication:

- package identity is `@xiongxianfei/rigorloop@0.1.4`;
- the package exposes one `rigorloop` binary;
- the package-local `LICENSE` is present;
- package metadata no longer uses `private: true`;
- bundled adapter metadata points at the `v0.1.4` release mapping.

This satisfies the first-publication package identity and single-binary contract without introducing a second package or new CLI behavior.

### Package Content Validation

The npm package validation path was added so maintainers can inspect the actual packed tarball before publication.

The validator checks required runtime contents and rejects forbidden content such as adapter archives, nested or root-level archive files, secret-like files, local state, generated adapter skill bodies, tests, fixtures, and unintended docs. Packed-package smoke installs the generated tarball into a temporary project and runs the package binary for approved dry-run command checks.

This prevents accidental publication of repository internals or generated adapter output while keeping adapter archives outside npm.

### Release Evidence

`docs/releases/v0.1.4/` now contains:

- `release.yaml`;
- `release-notes.md`;
- `npm-publication.md`.

The release notes include the public npm usage examples and source-of-truth boundary language. The publication evidence file is intentionally still `Status: pending-publication`; it records the selected bootstrap path and blocks FU-010 until actual publication and install proof are recorded.

### Release Verification

`scripts/release-verify.sh v0.1.4` now ties together:

- canonical skill validation;
- adapter archive generation;
- adapter artifact metadata validation;
- npm package-content and packed-package smoke;
- v0.1.4 release metadata validation;
- npm publication evidence validation.

The release validator also checks bootstrap tarball identity when the packed tarball root is provided. A recorded SHA-256 must match the actual tarball bytes before bootstrap publication evidence can support a publish.

### Publication Mode

The existing `.github/workflows/release.yml` owns future trusted npm publishing through GitHub Actions OIDC. The workflow publish job is skipped for `v0.1.4`, because the first package claim may use the one-time bootstrap path if trusted publishing cannot be configured before package creation.

This keeps one release workflow while preventing duplicate publication of `@xiongxianfei/rigorloop@0.1.4`.

## Why This Shape

The slice intentionally separates repository readiness from external publication:

1. Repository implementation prepares package metadata, release validation, workflow gates, release notes, and pending evidence.
2. A later publication execution step creates the `v0.1.4` tag and publishes the exact verified package.
3. A post-publication evidence update records npm visibility, `npx` smoke, and actual Codex adapter install proof.

That sequencing avoids claiming public availability before npm and GitHub release assets are externally observable.

## Validation Evidence

Validation recorded during implementation includes:

- `npm test --prefix packages/rigorloop`;
- `python scripts/test-npm-package-publication.py`;
- `python scripts/test-adapter-distribution.py`;
- `python scripts/test-select-validation.py`;
- `bash scripts/release-verify.sh v0.1.4`;
- `python scripts/validate-change-metadata.py docs/changes/2026-05-16-first-public-npm-release/change.yaml`;
- `python scripts/validate-review-artifacts.py docs/changes/2026-05-16-first-public-npm-release`;
- selected `bash scripts/ci.sh --mode explicit ...`;
- scoped `git diff --check -- ...`.

## Remaining Work

FU-010 remains open. It can close only after:

- the package is publicly published;
- npm package URL evidence exists;
- post-publication npm or npx smoke passes;
- actual non-dry-run `init --adapter codex --json` passes from the packed or published package;
- `docs/releases/v0.1.4/npm-publication.md` is updated from `pending-publication` to final evidence;
- the evidence update is tracked and validated.

FU-006 through FU-009 remain open and deferred.
