# ADR-20260516-rigorloop-npm-publication: First Public npm Publication Boundary

## Status

accepted

## Context

The RigorLoop CLI package exists as a repository package candidate named `@xiongxianfei/rigorloop` with one `rigorloop` binary. Earlier CLI architecture intentionally blocked public npm publication until a release-policy slice defined package contents, trusted publishing, provenance, workflow controls, dependency and lifecycle-script policy, versioning, rollback, and publication evidence.

The approved npm publication spec defines the first public package line:

```text
repository tag: v0.1.4
npm package: @xiongxianfei/rigorloop@0.1.4
compatible adapter release: v0.1.4
```

This is a durable release and supply-chain boundary because it adds a public npm registry distribution path while preserving GitHub release archives as the adapter install surface and repository-authored files as canonical workflow and skill sources.

## Decision

Allow the first public npm publication of `@xiongxianfei/rigorloop@0.1.4` only through the approved release-hardening boundary.

The npm package is a CLI delivery artifact. It may include the `rigorloop` binary, runtime CLI libraries, package-local README and license files, and bundled official adapter metadata for the compatible `v0.1.4` Codex adapter release. It must not include adapter ZIP archives, generated public adapter skill bodies, repository lifecycle artifacts, tests, local fixtures, secrets, `.codex`, `.agents`, or generated adapter package trees.

Publication uses exactly one mode:

- `trusted-publishing`: `.github/workflows/release.yml` owns npm publication through npm trusted publishing/OIDC after release verification, package-content validation, and packed-package smoke.
- `bootstrap`: allowed only for the first `@xiongxianfei/rigorloop@0.1.4` publication if trusted publishing cannot be configured before the package exists. In this mode, release readiness is still owned by `release.yml` or `bash scripts/release-verify.sh v0.1.4`, but npm publication is a one-time maintainer manual publish of the exact packed tarball recorded in publication evidence.

Publication evidence under `docs/releases/v0.1.4/npm-publication.md` owns the closeout proof. It records package identity, source commit, selected publication mode, tarball filename and SHA-256, package-content validation, packed-package smoke, trusted publishing or bootstrap details, npm package URL, and real Codex adapter install smoke.

FU-010 may close only after the package is publicly published and actual non-dry-run `init --adapter codex --json` succeeds from the packed or published package against the official `v0.1.4` Codex release archive. Dry-run smoke is not enough.

## Alternatives considered

### Continue without publishing npm

Rejected because it keeps the intended public quick-start path unavailable and delays adoption after the CLI, lockfile, and `new-change` slices are already implemented.

### Publish manually as the normal path

Rejected because manual publication as the steady-state path weakens repeatability, provenance, and release workflow reviewability. Manual bootstrap is retained only for the first package claim if npm cannot configure trusted publishing before package creation.

### Use a separate npm-only workflow

Rejected for the first public release because one release workflow keeps release readiness, package-content proof, packed-package smoke, and publication evidence easier to audit.

### Bundle adapter archives in npm

Rejected because adapter archives are generated GitHub release artifacts. Bundling them into npm would blur the source-of-truth boundary and enlarge the package surface.

## Consequences

- The npm registry becomes a public distribution boundary for the CLI package, not a canonical source boundary.
- `release.yml`, `release-verify.sh`, package-content validation, packed-package smoke, and publication evidence become part of the first public CLI release architecture.
- Bootstrap publication is allowed only as a one-time package-claim path and must not become a reusable release path.
- The package tarball needs deterministic allowlist validation and forbidden-path checks before publication.
- Packed-package smoke must exercise the installed package binary rather than repository-local scripts.
- Actual Codex adapter installation must be proven from the packed or published package before FU-010 closes.
- Trusted publishing must be configured after bootstrap before any later npm publication.
- Bad npm versions are corrected by fixed patch releases and documentation or deprecation; published versions are not mutated in place.

## Follow-up

- Update the canonical architecture package to include npm registry publication, publication modes, package-content validation, and real install smoke.
- Create architecture-review evidence for this ADR and canonical package update.
- Create the execution plan and test spec for the approved npm publication slice after architecture-review.
