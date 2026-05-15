# ADR-20260515-rigorloop-cli-package-and-codex-init: RigorLoop CLI Package and Codex Init Boundary

## Status

accepted

## Context

RigorLoop already separates canonical authored workflow content from generated adapter output. For `v0.1.3` and later, generated public adapter skill bodies are release archives rather than tracked source under `dist/adapters/<adapter>/`.

The approved first-slice CLI spec introduces a new npm package candidate and command surface:

```text
@xiongxianfei/rigorloop
rigorloop --help
rigorloop version
rigorloop init --adapter codex
rigorloop init --adapter codex --dry-run --json
```

The architecture decision is where the CLI package sits relative to canonical repository sources, release archives, bundled metadata, user projects, generated adapter output, and future public npm publishing.

## Decision

Create one CLI package candidate under the repository, published later as `@xiongxianfei/rigorloop` with one binary named `rigorloop`.

The first CLI slice is a scaffold and adapter installer, not a new source of truth. It may package CLI code, small project scaffolds, and official adapter metadata for the package's compatible Codex adapter release. It must not package adapter archives as authored npm source, generated adapter skill bodies as canonical source, or repository-owned validator logic as the public validator authority.

`rigorloop init --adapter codex` installs Codex adapter output from verified release archives:

- network mode uses bundled official adapter metadata shipped with the installed CLI package version, then fetches the official archive URL named by that metadata;
- local mode uses `--from-archive <path>` and verifies the archive against the same bundled adapter metadata;
- both modes verify filename, size, SHA-256, install root, archive traversal safety, and installed tree hash before claiming success;
- both modes install only under `.agents/skills` for the Codex adapter.

The first slice writes `rigorloop.yaml` using the approved first-slice shape and may emit planned lockfile content, but it must not write durable `rigorloop.lock` until a lockfile spec is accepted.

Public npm publication is architecturally blocked until a later release-policy slice accepts package contents, trusted publishing, provenance, workflow controls, dependency policy, lifecycle-script policy, versioning, and rollback behavior.

## Alternatives considered

### Use separate `@rigorloop/cli` and `@rigorloop/create` packages

Rejected for the first slice because one package and one binary make the public command model clearer and reduce first-release package governance.

### Bundle adapter archives inside the npm package

Rejected because adapter archives are generated release artifacts. Bundling them into npm would blur the source-of-truth boundary and enlarge the package surface before release hardening is accepted.

### Require users to pass a separate metadata file for `--from-archive`

Rejected for first-slice UX. Local archive installation keeps one user archive input and verifies it against official metadata bundled with the installed CLI package version.

### Install from `.codex/skills`

Rejected because `.codex/skills` is local runtime state and must never become a public adapter source.

### Write `rigorloop.lock` during the first slice

Rejected because a lockfile is durable source-of-truth state. The first slice may emit planned lockfile content only until a lockfile spec defines ownership, hash computation, and update rules.

## Consequences

- The repository gains a Node/package boundary for the CLI candidate while canonical workflow sources stay in repository-owned paths.
- The CLI package needs bundled adapter metadata that is generated or copied from official release evidence for the matching compatible adapter release, plus a bundled release index hash so the metadata is verified before use.
- Local archive installation can remain offline and simple for users while retaining strong verification.
- Adapter archive verification becomes a security-sensitive command path requiring archive traversal checks, install-root confinement, checksums, size checks, and tree-hash validation.
- The CLI package can be tested from local package artifacts before public npm publication.
- Public npm publishing remains blocked by a separate hardening decision.
- Future `new-change`, `status`, `validate`, durable lockfile writes, other adapters, and workflow YAML canonicality require separate specs or proposals as already recorded.

## Follow-up

- Update the canonical architecture package to include the CLI package, bundled adapter metadata, install flow, and publication boundary.
- Create an architecture-review record for this decision and canonical package update.
- Create a test spec for the approved first-slice CLI requirements after architecture review.
- Keep npm release hardening as a separate follow-up before public publication.
