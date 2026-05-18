# Multi-Adapter Init and Proxy-Aware Adapter Download

## Status

accepted

## Problem

RigorLoop publishes public adapter archives for Codex, Claude Code, and opencode, but the CLI init surface is still narrower than the adapter distribution surface.

The current approved CLI contract supports:

```bash
rigorloop init --adapter codex
```

It does not yet support:

```bash
rigorloop init --adapter claude
rigorloop init --adapter opencode
```

The Codex install root should remain `.agents/skills`. The accepted CLI and lockfile specs already record Codex generated output under `.agents/skills`, and the official OpenAI Codex Skills documentation says Codex scans repository skills from `.agents/skills` locations, including `$REPO_ROOT/.agents/skills`. The earlier proposal direction to move Codex output to `.codex/skills` is no longer needed and should not proceed.

Finally, adapter archive download can fail in enterprise or proxied environments. Current CLI download behavior uses Node `fetch`. Node's enterprise-networking guidance says proxy environment variables affect `fetch()` only when supported Node env-proxy support is enabled, and proxy behavior is Node-version dependent. The CLI needs a contract-first path for multi-adapter init and actionable proxy diagnostics without weakening archive verification. Programmatic Undici proxy dispatcher support is deferred from this proposal.

References:

- OpenAI Codex Skills documentation: <https://developers.openai.com/codex/skills>
- Node.js enterprise network configuration: <https://nodejs.org/en/learn/http/enterprise-network-configuration>

## Goals

- Add a contract for `rigorloop init --adapter claude`.
- Add a contract for `rigorloop init --adapter opencode`.
- Preserve Codex installs under `.agents/skills`.
- Define lockfile schema changes for adapter-specific roots and opencode multi-root installs.
- Preserve the existing `rigorloop init --adapter codex` command shape, archive verification, mutation-safety, local archive fallback, and lockfile integrity model.
- Keep adapter archives as GitHub release artifacts verified by CLI-bundled official metadata.
- Preserve `--from-archive` as the reliable offline or controlled-network path.
- Add proxy-aware network download behavior or clear proxy diagnostics that do not expose credentials, private hostnames, or internal proxy URLs.
- Keep network tests hermetic and fixture-backed.
- Require generated adapter temp-output validation from canonical `skills/` when public adapter output changes.
- Preserve generated-output tree-hash verification.
- Avoid making npm package contents the canonical adapter source.
- Avoid a constants-only adapter patch without spec, tests, and compatibility proof.

## Non-goals

- Do not claim Claude Code or opencode init support already exists.
- Do not change public adapter archive packaging in this proposal.
- Do not bundle adapter archives into the npm package.
- Do not change the Codex install root from `.agents/skills` to `.codex/skills`.
- Do not install from unverified local skill directories.
- Do not make `.agents/skills`, `.claude/skills`, or `.opencode/skills` canonical authored skill source.
- Do not bypass archive checksum, size, path traversal, symlink, install-root, or tree-hash verification.
- Do not add `rigorloop status`, `rigorloop validate`, workflow YAML, or generated workflow docs.
- Do not add programmatic Undici proxy dispatcher support in this proposal.
- Do not weaken existing Codex init trust-boundary tests.
- Do not require live GitHub or live proxy access in normal tests.

## Vision fit

fits the current vision

This proposal improves RigorLoop adoption while preserving artifact-first, verification-first delivery. It makes the existing adapter distribution easier to use from the CLI without replacing durable proposals, specs, plans, validation evidence, or review records.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
|---|---|---|
| Keep Codex on `.agents/skills` based on official Codex Skills documentation | in scope | Problem, Goals, Recommended direction, Expected behavior changes |
| Add `init --adapter claude` | in scope | Goals, Expected behavior changes |
| Add `init --adapter opencode` | in scope | Goals, Expected behavior changes |
| Preserve existing Codex command behavior | in scope with install-root compatibility work | Goals, Rollout and rollback, Risks and mitigations |
| Keep release archives verified by CLI metadata | in scope | Goals, Architecture impact |
| Preserve `--from-archive` fallback | in scope | Goals, Expected behavior changes |
| Add proxy-aware diagnostics or support | in scope | Goals, Recommended direction |
| Keep tests hermetic | in scope | Testing and verification strategy |
| Require generated adapter validation | in scope | Generated adapter validation |
| Bound first implementation slice | in scope | First-slice boundary |
| Avoid npm-bundled adapter archives | out of scope | Non-goals |
| Avoid `status`, `validate`, workflow YAML, and generated workflow docs | out of scope | Non-goals |
| Avoid Codex install-root migration | in scope | Codex install-root handling |

## Context

The accepted CLI direction made npm a delivery channel, not the source of truth. The CLI already installs Codex adapter output from verified release archives and verifies official bundled metadata, archive size, SHA-256, install-root confinement, path safety, and installed tree hash.

Current accepted artifacts intentionally limited the first CLI and lockfile slices to Codex:

- `specs/rigorloop-cli-package-and-codex-init.md` defines only `rigorloop init --adapter codex` and records `.agents/skills`.
- `specs/rigorloop-cli-lockfile.md` defines lockfile writes only for Codex and records `.agents/skills`.
- `docs/adr/ADR-20260515-rigorloop-cli-package-and-codex-init.md` keeps Codex extraction under `.agents/skills`.
- `dist/adapters/README.md` currently lists Codex target install root as `.agents/skills/`.
- The official OpenAI Codex Skills documentation says Codex scans repository `.agents/skills` directories from the current working directory up to the repository root.

The intended install-root distinction is:

```text
skills/                  canonical authored source
release archive           verified generated adapter output source
.agents/skills/           Codex repository skill install destination
.claude/skills/           Claude Code runtime install destination
.opencode/skills/         opencode runtime install destination
.opencode/commands/       opencode command-alias install destination
```

The proposal does not make runtime install directories a source of trust.

## Options considered

### Option 1: Patch constants to accept `claude` and `opencode`

Advantages:

- Fastest implementation.

Disadvantages:

- Misses opencode command aliases.
- Risks incomplete lockfile behavior.
- Risks incomplete install-root and overwrite checks.
- Does not address proxy diagnostics or multi-adapter lockfile semantics.
- Changes public CLI behavior without a testable contract.

### Option 2: Only document local archive fallback

Advantages:

- Very small change.
- Helps users blocked by proxy or `fetch` differences.

Disadvantages:

- Does not solve Claude Code or opencode init.
- Does not improve network reliability or diagnostics.

### Option 3: Contract-first multi-adapter init plus proxy-aware download

Advantages:

- Preserves trust boundaries.
- Makes adapter behavior testable.
- Handles enterprise network realities.
- Keeps local archive fallback as a safe escape hatch.
- Keeps Codex aligned with the official `.agents/skills` repository skill location.
- Avoids accidental opencode under-implementation.

Disadvantages:

- Requires spec, test spec, plan, and focused implementation.
- Requires extending accepted CLI, lockfile, and adapter guidance artifacts.
- Slightly larger than a pure documentation fix.

## Recommended direction

Choose Option 3.

Define explicit adapter descriptors for:

```bash
rigorloop init --adapter codex
rigorloop init --adapter claude
rigorloop init --adapter opencode
```

Preserve `.agents/skills` as the Codex install destination, while adding Claude Code and opencode through explicit adapter descriptors. The spec should extend the existing Codex init and lockfile contracts without introducing a Codex install-root migration.

The spec should define canonical descriptor fields for archive filename pattern, expected install roots, archive allowlisted paths, required roots, root hashing, and lockfile serialization. The proposal direction is:

```yaml
codex:
  archive: rigorloop-adapter-codex-<version>.zip
  install_roots:
    skills: .agents/skills

claude:
  archive: rigorloop-adapter-claude-<version>.zip
  install_roots:
    skills: .claude/skills

opencode:
  archive: rigorloop-adapter-opencode-<version>.zip
  install_roots:
    skills: .opencode/skills
    commands: .opencode/commands
```

For proxy behavior, specify diagnostics first and adopt built-in Node env-proxy support only where the current runtime supports it. Programmatic Undici proxy dispatcher support is out of scope for this proposal and should require a later proposal or spec revision if advanced proxy handling becomes necessary.

## Resolved proposal-review decisions

Proposal review resolved the formerly open questions with these decisions:

- Lockfile multi-root support uses `schema_version: 2`.
- Existing Codex entries remain single-root entries using `installed_root`.
- Multi-root adapters use `installed_roots` and `root_hashes`.
- New opencode archives must include command aliases when trusted metadata declares them.
- Older opencode archives without command alias metadata may install with a warning instead of a hard block.
- First-slice proxy handling uses Node built-in env-proxy support and safe diagnostics.
- Programmatic Undici proxy dispatcher support is deferred unless a later proposal or spec revision justifies the extra runtime surface.
- Proxy diagnostics report only safe facts: adapter name, release version, detected proxy environment variable names, Node env-proxy support status, download failure class, trusted public archive URL, and `--from-archive` fallback guidance.

## Multi-adapter CLI init contract

- Public skills use adapter descriptors to populate runtime roots.
- Canonical authored skills remain under `skills/`.
- Adapter output comes from verified release archives or verified local archives matched against CLI-bundled official metadata.
- Customer projects can install adapters without requiring RigorLoop internal docs.
- CLI init enforces archive verification, lockfile integrity, runtime path safety, and multi-root handling.
- Proxy diagnostics report safe facts only and recommend `--from-archive` when download fails.
- Generated adapters are validated from canonical skills; generated adapter output is not hand-edited.

## Codex install-root handling

Codex should remain a single-root adapter installed under `.agents/skills`.

First-slice direction:

- New Codex installs continue to use `.agents/skills`.
- Existing `.agents/skills` lockfile entries remain compatible.
- The proposal does not define or require migration to `.codex/skills`.
- Any future Codex install-root change would require a separate compatibility-sensitive proposal or spec revision.

## Lockfile schema direction

The spec must revise the lockfile contract before non-Codex or multi-root entries are written.

First-slice direction:

- Use `schema_version: 2` for multi-root adapter support.
- Preserve backward-compatible parsing for existing `schema_version: 1` Codex single-root entries.
- Keep Codex entries using the existing `installed_root` field.
- Use `installed_roots` and per-root `root_hashes` for multi-root adapters.
- Preserve archive basename, archive SHA-256, release tag, tree hash algorithm, and file counts.
- Avoid absolute local paths, usernames, hostnames, temporary paths, proxy URLs, credentials, and environment variable values.
- Preserve old-lockfile behavior for existing Codex `.agents/skills` entries.
- Require CLI and validation logic to handle mixed single-root and multi-root entries concurrently.

Preferred multi-root shape:

```yaml
generated:
  adapters:
    - adapter: opencode
      release: "v0.1.6"
      source: release-archive
      archive: "rigorloop-adapter-opencode-v0.1.6.zip"
      archive_sha256: "<sha256>"
      tree_hash_algorithm: rigorloop-tree-hash-v1
      installed_roots:
        skills: ".opencode/skills"
        commands: ".opencode/commands"
      root_hashes:
        skills:
          tree_sha256: "<sha256>"
          file_count: 23
        commands:
          tree_sha256: "<sha256>"
          file_count: 5
```

## Proxy diagnostics

Proxy-aware behavior must be useful without leaking sensitive network details.

When network download fails, the CLI should report:

- adapter name;
- adapter release version;
- detected proxy-related environment variable names only;
- Node env-proxy support status;
- download failure class;
- trusted public archive URL from bundled metadata;
- the `--from-archive` fallback command shape.

The CLI must not report proxy credentials, full proxy URLs, private hostnames, access tokens, or raw environment variable values. If the official archive URL is reported, it should be the public release asset URL selected from trusted metadata, not a user-provided or proxy-rewritten URL.

## Opencode multi-root

opencode is a multi-root adapter:

- `.opencode/skills` contains skill content.
- `.opencode/commands` contains generated command aliases when the verified metadata declares command aliases.

The CLI must not silently install only `.opencode/skills` when metadata declares command aliases.

First-slice direction:

- New opencode archives must include command aliases when trusted metadata declares aliases.
- Missing declared command aliases are a validation failure for new archives.
- Older archives that lack command-alias metadata may install with a warning instead of a hard block.
- CLI descriptor validation flags missing declared aliases before claiming a complete opencode install.

## Generated adapter validation

If canonical public skills or adapter templates change in this initiative, validation must regenerate temporary adapter output from `skills/` and validate it against expected install roots, metadata, archive hashes, and tree hashes.

Generated adapter output must not be hand-edited. Validation should use repository-owned scripts and release metadata rather than treating `.agents/skills`, `.claude/skills`, `.opencode/skills`, or `.opencode/commands` as authored source.

## First-slice boundary

The first implementation slice should begin with an audit of the CLI, metadata, adapter generation, docs, and any public skill text that references install roots or internal RigorLoop paths.

The implementation should update only audited surfaces needed for the approved contract. It should record the touched skill or adapter guidance list and avoid broad public skill rewrites unrelated to init, lockfile, proxy diagnostics, or install-root accuracy.

## Expected behavior changes

- `rigorloop init --adapter codex` continues to install verified Codex adapter output to `.agents/skills`.
- `rigorloop init --adapter claude` installs verified Claude Code adapter output to `.claude/skills`.
- `rigorloop init --adapter opencode` installs verified opencode adapter output to `.opencode/skills` and installs `.opencode/commands` when the verified archive metadata declares command aliases.
- Unsupported adapters still block with the existing invalid-adapter exit behavior.
- `--from-archive` works for all supported adapters and verifies against bundled official metadata without requiring a user-supplied metadata file.
- Network download failures report the attempted official archive URL, adapter name, release version, relevant proxy environment detection, whether Node env-proxy support appears enabled, and a concrete `--from-archive` fallback.
- `rigorloop.yaml` and `rigorloop.lock` record adapter-specific install roots without recording machine-local archive paths.

## Architecture impact

The CLI init flow moves from Codex-only constants to adapter descriptors that define archive identity, expected roots, lockfile shape, and extraction allowlists.

The affected boundaries are:

- CLI adapter selection and validation.
- Bundled official adapter metadata lookup.
- Network and local archive acquisition.
- Archive safety validation and extraction root confinement.
- Generated-output tree hashing.
- `rigorloop.yaml` adapter recording.
- `rigorloop.lock` generated adapter entries.
- Adapter install guidance in `dist/adapters/README.md`.
- The accepted CLI and lockfile specs that currently name only Codex and a single adapter root.

opencode needs multi-root handling because `.opencode/commands` is a generated command-alias surface separate from `.opencode/skills`. The lockfile should use one adapter entry with `installed_roots` and per-root `root_hashes` rather than separate entries for one adapter.

## Testing and verification strategy

Unit and integration tests should cover:

- Codex still accepts `rigorloop init --adapter codex` and continues to use `.agents/skills`.
- Existing `.agents/skills` projects remain compatible.
- Claude Code selects `.claude/skills`.
- opencode selects `.opencode/skills` and `.opencode/commands` when metadata declares command aliases.
- Unsupported adapters still block.
- Wrong archive for the selected adapter fails.
- Local archive mode verifies bundled metadata for all supported adapters.
- Network mode accepts only official release URLs from trusted metadata.
- Proxy failure diagnostics are stable.
- `--from-archive` fallback guidance appears when network fetch fails.
- No `--metadata` user option is required.
- Lockfile entries do not record absolute local archive paths, usernames, hostnames, temporary directories, proxy URLs, or secrets.

Hermetic network tests should use mocked fetch, a local fixture server, fixture archive bytes, and fixture metadata. Normal tests should not depend on live GitHub, a live corporate proxy, or external internet.

Release verification may include real smoke tests for all three adapters when the release environment supports them. If network smoke is unreliable, release verification should require local archive smoke for all supported adapters.

## Rollout and rollback

Roll out through the standard workflow: proposal review, spec, spec review, architecture or ADR if required, plan, test spec, implementation, code review, explanation, verification, PR, and release.

Codex compatibility handling should remain simple:

- new installs use `.agents/skills`;
- existing lockfiles that record `.agents/skills` remain valid;
- no Codex install-root migration is attempted in this proposal.

Rollback should preserve the existing archive verification model. If multi-adapter support is partially rolled back, Codex init should remain verified and unsupported adapters should block clearly rather than install incomplete output.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Codex install-root behavior drifts from official Codex guidance | Keep Codex on `.agents/skills` and cite the official OpenAI Codex Skills documentation in the spec. |
| Runtime install roots are mistaken for canonical source | State that they are verified generated-output destinations; canonical authored source remains `skills/`. |
| opencode command aliases are missed | Treat opencode as a multi-root adapter in the spec. |
| Proxy support becomes flaky | Keep local archive fallback central and test proxy diagnostics hermetically. |
| CLI trusts user-supplied metadata | Continue the bundled official metadata model. |
| Network tests depend on live GitHub | Use fixture-backed mocked network tests. |
| Lockfile records machine-local paths or proxy secrets | Record archive basename and verified tree hashes only; never record proxy URL values. |
| Multi-adapter support becomes too broad | Defer opencode implementation if multi-root lockfile semantics are not approved. |

## Open questions

None that block spec authoring.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
|---|---|---|---|
| 2026-05-18 | Propose contract-first multi-adapter init. | Existing CLI supports only Codex while public archives exist for more adapters. | Constants-only adapter patch. |
| 2026-05-18 | Keep Codex init on `.agents/skills`. | Official OpenAI Codex Skills documentation identifies `.agents/skills` as the repository skill location, and existing RigorLoop specs already use that root. | Move Codex init to `.codex/skills`. |
| 2026-05-18 | Keep local archive fallback central. | It is the reliable path when Node fetch and user network behavior differ. | Require live network success for init. |
| 2026-05-18 | Treat first-slice proxy support as Node built-in env-proxy support plus diagnostics. | Node proxy behavior is version-dependent and must remain testable without adding dispatcher complexity. | Claim universal proxy support from environment variables alone. |
| 2026-05-18 | Treat opencode as a multi-root adapter. | It has skills and command aliases. | Skills-only opencode install. |
| 2026-05-18 | Require pre-implementation specification of multi-root lockfile behavior. | opencode command aliases need root-specific install and hash semantics. | Ad hoc lockfile extension during implementation. |
| 2026-05-18 | Use `schema_version: 2` for multi-root adapter lockfile support. | Older CLI and validation logic should not misinterpret multi-root fields. | Compatible extension to `schema_version: 1`. |
| 2026-05-18 | Keep Codex lockfile entries on the existing single-root `installed_root` field. | Codex remains a single-root `.agents/skills` adapter. | Normalize every adapter to `installed_roots` in the first multi-adapter slice. |
| 2026-05-18 | Require declared opencode command aliases for new archives and warn for older archives without alias metadata. | Prevent silent incomplete opencode installs while preserving older archive compatibility. | Hard-block all old opencode archives. |
| 2026-05-18 | Use Node built-in env-proxy support and safe diagnostics for the first proxy slice. | Avoid first-slice dependency and dispatcher complexity. | Add programmatic Undici proxy dispatcher support immediately. |

## Next artifacts

- `proposal-review`
- `spec` for multi-adapter init, Codex `.agents/skills` preservation, lockfile shape, and proxy diagnostics
- `spec-review`
- architecture or ADR only if the spec changes lockfile schema, proxy trust boundaries, or adapter install-root architecture
- `plan`
- `test-spec`
- implementation and review stages after the contract is approved

## Follow-on artifacts

- Spec: [Multi-Adapter Init and Proxy-Aware Adapter Download](../../specs/multi-adapter-init-and-proxy-aware-download.md)

## Readiness

Accepted and followed by spec authoring.
