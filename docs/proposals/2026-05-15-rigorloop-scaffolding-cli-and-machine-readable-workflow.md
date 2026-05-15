# RigorLoop Scaffolding CLI and Machine-Readable Workflow

## Status

accepted

## Problem

RigorLoop has a strong artifact-first workflow contract, but adoption still requires too much manual repository knowledge. Users must copy adapter files, create change artifacts by hand, know the workflow order before they can benefit from it, and run several repository-specific validation scripts instead of one user-facing command.

The project already separates canonical authored content from generated adapter output. That boundary is correct, but the install and validation experience does not yet make the boundary easy for humans, CI, or agents to use safely.

## Goals

- Provide a small, reproducible CLI for initializing projects, creating change artifact packs, inspecting workflow state, and running validation.
- Keep canonical workflow content, skills, schemas, templates, and adapter definitions in the repository.
- Treat npm as a delivery channel, not as the source of truth.
- Add stable human and machine-readable command output.
- Preserve RigorLoop's claim-boundary discipline: implementation, review, verification, and PR readiness remain owned by their proper workflow stages.
- Introduce a machine-readable workflow definition that can drive validators, generated documentation, diagrams, and adapter handoff snippets over time.
- Make generated adapter and workflow output drift-detectable through hashes or frozen validation.

## Non-goals

- Do not replace the existing standard workflow with a lighter shortcut path.
- Do not make npm packages the canonical source for skills, workflow rules, schemas, or adapters.
- Do not let file existence imply proposal acceptance, branch readiness, PR-body readiness, or PR-open readiness.
- Do not port every Python validator to TypeScript in the first slice.
- Do not require network access, secrets, or hosted services for normal validation.
- Do not hand-edit generated adapter package output.
- Do not implement the full CLI, workflow schema, generated docs, and release hardening in one review slice.

## Vision fit

fits the current vision

This proposal strengthens RigorLoop's commitment to trustworthy, reconstructable AI-assisted delivery. The CLI reduces adoption friction while keeping durable artifacts, explicit contracts, validation evidence, and review boundaries as the center of the product.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
|---|---|---|
| Publish a small reproducible scaffolding CLI through npm | in scope | Goals, Recommended direction, Expected behavior changes |
| Keep canonical workflow, skills, schemas, and adapters in the repository | in scope | Goals, Recommended direction, Architecture impact |
| Support `init`, `new-change`, `status`, and `validate` first | in scope | Recommended direction, Expected behavior changes |
| Add machine-readable workflow state in a later milestone | in scope | Recommended direction, Architecture impact |
| Use stable `--json`, `--quiet`, `--debug`, `--no-color`, and CI-friendly behavior | in scope | Expected behavior changes, Testing and verification strategy |
| Add manifest and lockfile for reproducibility and drift detection | deferred follow-up until the lockfile authority is specified | Lockfile boundary, `docs/follow-ups.md` |
| Harden npm publishing with provenance and supply-chain controls | required follow-up before public npm publication | Publishing boundary, `docs/follow-ups.md` |
| Use one package, `@xiongxianfei/rigorloop`, with one `rigorloop` binary | in scope | Recommended decisions, Publishing boundary, Decision log |
| Support `init --adapter codex` as the first useful adapter path | in scope | First accepted slice, Adapter asset boundary |
| Split broad work into several slices | deferred follow-up | `docs/follow-ups.md` |
| Clearly put slices into `follow-ups.md` | in scope | Follow-on artifacts, `docs/follow-ups.md` |

## Context

RigorLoop currently exposes its workflow through repository artifacts, stage skills, schemas, and scripts. The source-of-truth model is intentional:

- canonical authored workflow content lives in `docs/`, `specs/`, `skills/`, `schemas/`, `scripts/`, and `templates/`;
- `skills/` is the only authored skill source;
- generated public adapter skill bodies are release archives for `v0.1.3` and later, not tracked source under `dist/adapters/`;
- repository validation logic lives in repo-owned scripts, with GitHub Actions acting as thin wrappers.

This makes RigorLoop reviewable, but it leaves first-time setup and day-to-day validation awkward. A user-facing CLI can wrap the existing repository-owned scripts and scaffolds without changing the canonical source boundaries.

The user-provided comparison with OpenSpec, GitHub Spec Kit, BMAD, Agent Package Manager, CLI design guidance, and npm initializer behavior points to a common pattern: strong projects give users a reproducible lifecycle, not just a package.

## Options considered

### Option 1: Keep the current copy-and-script model

Advantages:

- Minimal new tooling.
- No new package surface or npm release risk.
- Existing scripts remain the only validation entry points.

Disadvantages:

- Adoption remains dependent on users knowing internal repository structure.
- Adapter installation stays manual.
- Agents and CI lack a single stable command contract.
- Validation remains fragmented across several commands.

### Option 2: Publish generated adapter packages only

Advantages:

- Improves adapter installation without designing a larger CLI.
- Keeps workflow validation mostly unchanged.
- Lower initial implementation scope than a full lifecycle CLI.

Disadvantages:

- Does not help create change artifacts, inspect workflow state, or run validation.
- Risks making generated package output feel like the source of truth.
- Leaves workflow state and claim boundaries difficult for tools to inspect.

### Option 3: Add a small CLI facade first, then machine-readable workflow generation

Advantages:

- Replaces manual setup with repeatable commands.
- Gives humans, agents, and CI one stable interface.
- Allows existing Python validators to remain authoritative while the public interface stabilizes.
- Preserves canonical authored content in the repository.
- Creates a path to generate docs, diagrams, validators, and adapter snippets from a workflow file later.

Disadvantages:

- Adds npm package and release-process responsibilities.
- Requires careful lockfile and overwrite behavior to avoid damaging user projects.
- Needs phased delivery to avoid one large hard-to-review change.

### Option 4: Build the workflow state machine first, then the CLI

Advantages:

- Starts with the strongest canonical model.
- Could reduce duplicated workflow logic before public command design.

Disadvantages:

- Delays the most visible adoption improvement.
- Requires changing workflow docs and validators before command behavior is proven.
- Risks designing an abstract workflow model without feedback from actual CLI use.

## Recommended direction

Choose Option 3.

Add a small npm-delivered CLI as the public facade while keeping canonical sources in this repository. The first command surface should be:

```text
rigorloop init
rigorloop new-change
rigorloop status
rigorloop validate
```

That command surface is the target product direction, not the first implementation slice.

The CLI should eventually support one-time execution through `npx`, initializer usage through `npm create`, and pinned project usage through a local dev dependency. It should wrap existing repository-owned validation scripts only after the validator execution model is specified.

The CLI can eventually create and maintain:

```text
rigorloop.yaml
rigorloop.lock
docs/changes/<change-id>/change.yaml
selected adapter files
required project directories
```

After the CLI facade is stable, add:

```text
workflow/rigorloop.workflow.yaml
schemas/workflow.schema.json
rigorloop workflow render
rigorloop validate --workflow --frozen
```

That second phase should make stage order, obligations, transitions, blockers, produced artifacts, consumed artifacts, owned claims, forbidden claims, validator bindings, and adapter mappings machine-readable.

## Recommended decisions

| Question | Recommended answer |
|---|---|
| Package names and npm namespace | Use one package: `@xiongxianfei/rigorloop`. The package is accepted as available based on `npm view @xiongxianfei/rigorloop --registry=https://registry.npmjs.org` returning `E404` / not found during proposal review. Expose one executable: `rigorloop`. Do not create `@rigorloop/cli`, `@rigorloop/create`, or `create-rigorloop` in the first slice. |
| Public command UX | Support `npx @xiongxianfei/rigorloop@latest init --adapter codex` for quick starts, `npx @xiongxianfei/rigorloop@0.1.3 init --adapter codex` for reproducible setup and docs, and `rigorloop init --adapter codex` after local or global install. |
| First published package contents | Publish the CLI only: entry point, help, version, `init --adapter codex`, `init --adapter codex --dry-run --json`, basic `rigorloop.yaml` generation, non-destructive write planning, stable JSON output, and release-archive install logic. Do not bundle all adapter archives in the npm package. |
| Stable JSON contract | Use one envelope for all commands with `schema_version`, `command`, `package`, `cwd`, `status`, `summary`, `actions`, `artifacts`, `blockers`, `warnings`, `errors`, and `diagnostics`. |
| Exit-code policy | Use a small stable set: `0` for success or warning, `2` for blocked, `3` for validation failed, `4` for invalid usage or config, `5` for mutation conflict or overwrite refusal, and `1` for internal or unexpected error. |
| Lockfile hash model | Use `rigorloop-tree-hash-v1`: SHA-256 over a canonical manifest of normalized relative paths and normalized file hashes. The first public package may emit planned lockfile content but must not write durable `rigorloop.lock` until a lockfile spec is accepted. |
| First `rigorloop.yaml` validation command names | Use `selected`, `ci`, `change_metadata`, `review_artifacts`, `artifact_lifecycle`, and `skills`. |
| Validators to wrap first | Wrap ordinary workflow artifact validation first: selected-path validation, change metadata, review artifacts, artifact lifecycle, and skill validation only where canonical skills are present. Keep release, adapter archive, token-cost, security, broad-smoke, and workflow frozen checks as direct advanced commands initially. |
| Workflow YAML canonicality | Treat `workflow/rigorloop.workflow.yaml` as a candidate machine-readable workflow definition until generated docs, frozen drift validation, conflict rules, release validation, and migration rules are approved and implemented. |
| `rigorloop init` adapter assets | First useful slice supports at least `--adapter codex`. Pinned package versions install the matching Codex adapter release archive by default; `latest` installs the latest compatible adapter archive. Offline mode uses `--from-archive`. Never install from `.codex/skills`. |
| Release metadata before network download | Require version, source repository, source commit, release tag, published date, adapter name, archive URL, SHA-256, size, install root, metadata URL/hash, tree hash fields, and validation result. |
| `rigorloop validate` wrapping model | Use a facade over repository-owned or project-configured validators first. Do not port validators to TypeScript first and do not make npm the canonical validator source. |

## First accepted slice

The first accepted slice is the one-package CLI strategy plus a useful Codex init path.

The recommended first implementation target after spec and architecture approval is:

```text
@xiongxianfei/rigorloop package skeleton
rigorloop binary
rigorloop --help
rigorloop version
rigorloop init --adapter codex
rigorloop init --adapter codex --dry-run --json
basic rigorloop.yaml generation
non-destructive write plan
verified Codex adapter release archive installation
```

The first slice may prepare the public package, but public npm publication remains blocked until the publishing boundary is satisfied.

Out of scope for the first implementation slice:

- `@rigorloop/cli`;
- `@rigorloop/create`;
- `create-rigorloop`;
- `rigorloop new-change`;
- `rigorloop status`;
- `rigorloop validate`;
- durable `rigorloop.lock` writes before an accepted lockfile spec;
- bundled adapter archives in the npm package;
- adapters other than Codex;
- machine-readable workflow YAML;
- generated workflow docs or diagrams;
- frozen drift checks;
- npm release hardening implementation.

The first slice should prove command discovery, option parsing, dry-run planning output, local fixture execution, non-destructive mutation planning, release archive metadata verification, checksum verification, and refusal to overwrite user files without an explicit safe path.

## Publishing boundary

The first implementation may create package structure and local CLI tests without publishing to npm.

Public npm publishing is blocked until a release-policy slice defines:

- package names and ownership;
- package contents;
- `bin` entries;
- lockfile and provenance expectations;
- release workflow controls;
- dependency policy;
- lifecycle-script policy;
- versioning and rollback behavior.

The package strategy is:

```json
{
  "name": "@xiongxianfei/rigorloop",
  "bin": {
    "rigorloop": "dist/bin/rigorloop.js"
  }
}
```

The first slice should not create `@rigorloop/cli`, `@rigorloop/create`, or `create-rigorloop`.

The proposal accepts `@xiongxianfei/rigorloop` as available based on the proposal-review npm lookup returning `E404` / not found. The spec should still record the final package ownership and publication controls before public npm publication.

Supply-chain hardening is not optional once public npm publication is in scope for a release.

## Adapter asset boundary

`rigorloop init --adapter codex` is part of the first useful CLI slice.

The CLI package should not bundle all adapter archives. Adapter archives remain GitHub release artifacts with metadata and checksums. The CLI may download or install them, but npm remains only the delivery channel for the CLI.

Default behavior:

- `npx @xiongxianfei/rigorloop@0.1.3 init --adapter codex` installs the matching `v0.1.3` Codex adapter release archive.
- `npx @xiongxianfei/rigorloop@latest init --adapter codex` installs the latest compatible Codex adapter archive.
- `rigorloop init --adapter codex --from-archive ./rigorloop-adapter-codex-v0.1.3.zip` installs from an explicit local archive for offline or controlled environments.

Install rules:

- verify release metadata before download or install;
- verify archive SHA-256 before install;
- fail on missing metadata, unknown adapter, checksum mismatch, incompatible release version, or overwrite conflict;
- emit planned installed file hashes and planned lockfile content until lockfile support is approved;
- never install from `.codex/skills`;
- never treat npm package contents as canonical skill source.

Required release metadata shape:

```yaml
schema_version: 1

release:
  version: v0.1.3
  source_repository: xiongxianfei/rigorloop
  source_commit: "<sha>"
  release_tag: v0.1.3
  published_at: "YYYY-MM-DD"

metadata:
  url: "https://github.com/xiongxianfei/rigorloop/releases/download/v0.1.3/adapter-artifacts-v0.1.3.yaml"
  sha256: "<sha256>"

artifacts:
  - adapter: codex
    archive: rigorloop-adapter-codex-v0.1.3.zip
    url: "https://github.com/xiongxianfei/rigorloop/releases/download/v0.1.3/rigorloop-adapter-codex-v0.1.3.zip"
    sha256: "<sha256>"
    size_bytes: 12345
    install_root: ".agents/skills"
    tree_hash_algorithm: rigorloop-tree-hash-v1
    tree_sha256: "<sha256>"

validation:
  command: "python scripts/validate-adapters.py --root <release-output-dir> --version v0.1.3"
  result: pass
```

Networked download rules:

- require an explicit adapter name;
- resolve package version to matching release version by default;
- fetch metadata from the official release source;
- verify metadata hash when provided;
- verify archive SHA-256;
- verify `size_bytes` when provided;
- extract only inside the expected install root;
- refuse path traversal in archive entries;
- refuse overwrite of user files unless `--force`;
- compute `tree_sha256` after extraction;
- write planned or installed files to JSON output.

Failure handling:

| Failure | Result |
|---|---|
| metadata missing | `blocked` |
| adapter unknown | `blocked` |
| checksum mismatch | `error` |
| archive path traversal | `error` |
| release version mismatch | `blocked` |
| overwrite conflict | exit code `5` |

This boundary prevents npm package contents from accidentally becoming the source of truth for adapters.

## Lockfile boundary

The first CLI spec must define whether `rigorloop.lock` records:

- RigorLoop package version;
- workflow schema version;
- adapter archive or generated file hashes;
- installed adapter names;
- template versions;
- validation command versions;
- project profile.

Until a lockfile spec is accepted, implementation may create safe scaffold files covered by the init spec and may emit planned lockfile content, but it must not write a durable `rigorloop.lock` outside fixture tests.

First package behavior:

- `--dry-run` prints planned writes and planned lockfile content;
- `--json` includes `planned_lockfile`;
- actual `init` may create safe scaffold files covered by the init spec;
- actual `init` must not write `rigorloop.lock` until the lockfile spec is approved.

If adapter installation cannot be implemented safely without a durable lockfile, actual adapter install should be blocked until the lockfile spec is approved while dry-run remains allowed.

Example blocked result:

```json
{
  "status": "blocked",
  "blockers": [
    {
      "code": "lockfile-spec-required",
      "message": "Adapter installation requires an approved lockfile contract before writing generated output."
    }
  ]
}
```

Example planned lockfile JSON field:

```json
{
  "planned_lockfile": {
    "schema_version": 1,
    "tree_hash_algorithm": "rigorloop-tree-hash-v1",
    "generated": {
      "adapters": [
        {
          "adapter": "codex",
          "source": "release-archive",
          "archive": "rigorloop-adapter-codex-v0.1.3.zip",
          "archive_sha256": "<planned>",
          "installed_root": ".agents/skills",
          "tree_sha256": "<planned-after-install>"
        }
      ]
    }
  },
  "warnings": [
    {
      "code": "lockfile-spec-not-approved",
      "message": "rigorloop.lock was not written because the lockfile contract is not approved."
    }
  ]
}
```

The lockfile tree hash algorithm is `rigorloop-tree-hash-v1`.

Inputs:

- hash a generated output directory after generation or installation, such as `.agents/skills/`, `.claude/skills/`, `.opencode/skills/`, or generated workflow output directories;
- include regular files only;
- exclude directories, symlinks, `mtime`, `ctime`, owner, group, absolute paths, the lockfile itself, and temporary files;
- defer symlink support to a future algorithm version such as `rigorloop-tree-hash-v2`.

Path normalization:

- path is relative to the generated output root;
- use POSIX `/`;
- no leading `./`;
- no trailing slash;
- UTF-8 path string;
- sort paths lexicographically by normalized path.

File-byte normalization:

- for text generated by RigorLoop, use UTF-8, normalize CRLF and CR to LF, remove UTF-8 BOM if present, and do not trim whitespace or normalize Markdown semantically;
- for binary files, hash raw bytes;
- if a directory mixes text and binary, the generator should mark which files are text-normalized.

File hash:

```text
file_sha256 = sha256(normalized_file_bytes)
```

Tree manifest:

```text
rigorloop-tree-hash-v1\n
<relative_path>\t<file_sha256>\n
<relative_path>\t<file_sha256>\n
...
```

Tree hash:

```text
tree_sha256 = sha256(utf8(canonical_manifest))
```

Lockfile entry shape:

```yaml
generated:
  adapters:
    - adapter: codex
      source: release-archive
      archive: rigorloop-adapter-codex-v0.1.3.zip
      archive_sha256: "<sha256>"
      installed_root: ".agents/skills"
      tree_hash_algorithm: rigorloop-tree-hash-v1
      tree_sha256: "<sha256>"
      file_count: 23
```

## Machine-readable workflow boundary

This proposal does not make `workflow/rigorloop.workflow.yaml` canonical.

The current canonical workflow contract remains the existing accepted specs and workflow guidance. A later proposal or spec must decide:

- whether workflow YAML becomes canonical;
- what it supersedes;
- how generated docs and validators are checked;
- how frozen drift validation works;
- how conflicts with `docs/workflows.md` and workflow specs are resolved.

The preferred migration rule is that spec approval can authorize building the workflow YAML, but canonicality should move only after generated docs, frozen drift validation, conflict rules, release validation, and migration rules exist.

## CLI command contract boundary

The first CLI spec must define the public command contract before any command ships beyond local proof behavior:

- global exit-code policy;
- JSON envelope shape;
- error object shape;
- command result status values;
- `--no-color`, `--quiet`, and `--debug` behavior;
- stdout and stderr split;
- CI behavior;
- whether JSON output is stable across patch releases.

The recommended JSON envelope is:

```json
{
  "schema_version": 1,
  "command": "init",
  "package": {
    "name": "@xiongxianfei/rigorloop",
    "version": "0.1.0"
  },
  "cwd": "/path/to/project",
  "status": "success",
  "summary": "",
  "actions": [],
  "artifacts": [],
  "blockers": [],
  "warnings": [],
  "errors": [],
  "diagnostics": {}
}
```

Stable status values are `success`, `warning`, `blocked`, and `error`.

The first CLI spec should also define the stable shapes for `actions`, `artifacts`, `blockers`, `warnings`, and `errors`, including codes, messages, paths when applicable, and recommended next actions for blockers.

## Mutation safety

Mutation commands default to non-destructive behavior.

They should:

- support `--dry-run`;
- refuse to overwrite existing non-generated files by default;
- report planned writes before applying them when `--json` is requested;
- support explicit `--force` only for documented generated outputs;
- create backups or require confirmation before replacing generated files;
- never delete user files in the first implementation slice.

## Validator wrapping boundary

`rigorloop validate` should not be implemented until the spec or architecture decides how the CLI locates or includes validators.

Possible models are:

- CLI package bundles repository validator scripts as package resources;
- CLI requires a local RigorLoop checkout path in `rigorloop.yaml`;
- CLI shells out only to project-local validators and starts with scaffold-only behavior;
- CLI uses a generated validation manifest and defers direct validator wrapping.

The recommended first model is a facade over repository-owned or project-configured validators. `rigorloop validate` should read `rigorloop.yaml`, discover configured validation commands, call those commands, normalize output into the stable JSON envelope, and map child exit codes to stable CLI exit codes. Downstream projects without configured validators should receive a `blocked` result rather than a false pass.

The first `rigorloop.yaml` validation config should use these stable command names:

```yaml
schema_version: 1

validation:
  commands:
    selected:
      command: "bash scripts/ci.sh --mode explicit"
    ci:
      command: "bash scripts/ci.sh --mode local"
    change_metadata:
      command: "python scripts/validate-change-metadata.py"
    review_artifacts:
      command: "python scripts/validate-review-artifacts.py"
    artifact_lifecycle:
      command: "python scripts/validate-artifact-lifecycle.py"
    skills:
      command: "python scripts/validate-skills.py"
```

Command-name meanings:

| Name | Purpose |
|---|---|
| `selected` | Run path-selected targeted checks. |
| `ci` | Run the project's ordinary local CI command. |
| `change_metadata` | Validate `docs/changes/<change-id>/change.yaml`. |
| `review_artifacts` | Validate review records, review logs, and review-resolution shape. |
| `artifact_lifecycle` | Validate proposal, spec, plan, ADR, and lifecycle status rules. |
| `skills` | Validate canonical skill files when the project authors skills. |

Until that model is settled, the first slice should avoid public `validate` behavior.

## Expected behavior changes

After the relevant slices are specified and implemented, users should be able to initialize RigorLoop in an existing project without manually copying adapter files:

```bash
npx @xiongxianfei/rigorloop@latest init --adapter codex
npx @xiongxianfei/rigorloop@0.1.3 init --adapter codex
rigorloop init --adapter codex
rigorloop init --dry-run --json
```

Users should eventually be able to create a change artifact pack without manually remembering required paths:

```bash
rigorloop new-change adapter-install-cli --type workflow
rigorloop new-change docs-typo --type docs --profile minimal
```

Users, agents, and CI should eventually be able to inspect state and validate with stable command shapes:

```bash
rigorloop status --json
rigorloop validate --change adapter-install-cli --ci --json
```

Mutation commands should support dry-run, backup, explicit target directories, force behavior, and actionable errors. Validation commands should return meaningful non-zero exit codes and should not require network access or secrets.

Status output should report blockers and missing artifacts without overclaiming readiness. In particular, `verify` remains the owner of branch readiness, and `pr` remains the owner of PR-body and PR-open readiness.

The first published package should contain CLI scaffolding only. Adapter archives, all generated skills, full validator bundles, workflow YAML canonical generators, and npm publish automation should stay out of the first package.

Documentation should prominently use:

```bash
# Quick start
npx @xiongxianfei/rigorloop@latest init --adapter codex

# Reproducible setup
npx @xiongxianfei/rigorloop@0.1.3 init --adapter codex

# After installation
rigorloop init --adapter codex
```

CI and agent docs should prefer the pinned version:

```bash
npx @xiongxianfei/rigorloop@0.1.3 init --adapter codex --json
```

## Architecture impact

The change affects several repository boundaries:

- `packages/rigorloop/` can own the public `@xiongxianfei/rigorloop` package and `rigorloop` command facade.
- `templates/project/` and `templates/change/` can hold scaffolds for manifests and change artifact packs.
- `schemas/workflow.schema.json` can define the machine-readable workflow contract only after a follow-on spec approves that boundary.
- `workflow/rigorloop.workflow.yaml` can become an authored workflow state-machine source only after a follow-on spec decides canonicality and conflict behavior.
- Existing Python scripts under `scripts/` should remain repository-owned validation implementations until a later consolidation decision.
- `dist/adapters/README.md` and `dist/adapters/manifest.yaml` remain the tracked adapter support surface; generated adapter skill bodies remain release output.

The proposal is compatibility-sensitive because it introduces public commands, package names, manifest and lockfile formats, and generated-output drift behavior. Follow-on spec and architecture work should define the command JSON contracts, lockfile semantics, overwrite rules, adapter asset model, validator wrapping model, schema versioning, and release pipeline boundaries before implementation of those surfaces.

## Testing and verification strategy

Follow-on specs should define tests at these levels:

- CLI unit tests for option parsing, exit codes, JSON output, color suppression, quiet/debug behavior, and actionable errors.
- Temporary-fixture integration tests for `init --adapter codex`, then later `new-change`, `status`, and `validate` as each command is specified.
- Adapter archive metadata tests for missing metadata, unknown adapter, checksum mismatch, incompatible release version, and overwrite conflict.
- Drift tests proving generated adapter files and lockfile hashes detect unexpected modification.
- Schema validation tests for `rigorloop.yaml`, `rigorloop.lock`, `change.yaml`, and later `workflow/rigorloop.workflow.yaml`.
- Regression tests proving status and validation do not infer branch-ready or PR-ready from file existence.
- Release verification for npm package contents, bin entries, provenance expectations, and absence of unnecessary lifecycle scripts before public npm publication.

The smallest useful first verification path should test the package skeleton, `--help`, `version`, and `init --dry-run` planning output in local fixtures. Existing repository-owned validation scripts remain the proof surface for repository behavior until validator wrapping is specified.

## Rollout and rollback

Roll out in slices:

1. Stabilize package architecture and CLI command contracts without public npm publication.
2. Implement the package skeleton, local command execution, `--help`, `version`, and `init --adapter codex` with `--dry-run --json`.
3. Specify and implement real `init` mutation behavior, including verified Codex adapter release archive installation and the lockfile model if lockfile support is included.
4. Specify and implement `new-change`, then `status`, then `validate`.
5. Add the workflow schema and semantic validator only after a follow-on spec settles canonicality.
6. Add generated workflow docs and frozen drift checks.
7. Harden npm publishing before any public npm publication.

Rollback should be straightforward while the CLI is additive and unpublished: users can keep using existing repository scripts and documented adapter install guidance. If a later published package version is flawed, publish a fixed version and keep project-local pinned dev dependency guidance so CI does not silently move with `latest`.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| npm distribution introduces supply-chain risk. | Block public npm publication until trusted publishing, provenance, 2FA, protected release workflows, CODEOWNERS, minimal dependencies, and lifecycle-script policy are specified. |
| CLI convenience weakens workflow rigor. | Treat missing artifacts and unresolved blockers as explicit state; preserve stage-owned readiness claims. |
| Generated package output becomes mistaken for source of truth. | Keep canonical authored content in repository paths and make package output reproducible from those sources. |
| Python and Node validation diverge. | Defer `rigorloop validate` until the validator wrapping model is specified; consolidate only after contracts are stable. |
| Workflow YAML becomes too rigid or silently canonical. | Keep workflow YAML non-canonical in this proposal; model mandatory, conditional, on-demand, and periodic obligations only after the follow-on spec settles canonicality. |
| Broad scope becomes hard to review. | Split the initiative into deferred follow-up slices recorded in `docs/follow-ups.md`. |
| Lockfile overwrite behavior damages user changes. | Defer durable lockfile writes until authority and overwrite behavior are specified; default to non-destructive writes, backup before overwrite, dry-run support, and explicit `--force`. |

## Open questions

None that block proposal review.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
|---|---|---|---|
| 2026-05-15 | Recommend a small npm-delivered CLI facade before the machine-readable workflow generator. | It gives users immediate adoption value while preserving repository-owned canonical sources and existing validators. | Current copy-and-script model; generated adapter packages only; workflow schema before CLI. |
| 2026-05-15 | Defer implementation slices into `docs/follow-ups.md`. | The requested scope is broad and should not become an implementation plan inside the proposal. | Encoding all milestones as proposal body tasks. |
| 2026-05-15 | Limit the first accepted implementation slice to one package, one binary, `--help`, `version`, and `init --adapter codex` with dry-run JSON support. | The public UX should be clear enough to be useful while still excluding the broader command surface. | Treating `new-change`, `status`, `validate`, lockfile writes, workflow YAML, and full adapter coverage as one first slice. |
| 2026-05-15 | Block public npm publishing until release-policy and supply-chain controls are specified. | Publishing makes package contents and provenance part of the release contract. | Deferring npm hardening while still allowing publication. |
| 2026-05-15 | Use one package, `@xiongxianfei/rigorloop`, with one binary, `rigorloop`. | The public commands are clearer through `npx @xiongxianfei/rigorloop@<version> ...` and avoid extra initializer packages in the first slice. | `@rigorloop/cli`, `@rigorloop/create`, and `create-rigorloop` in the first slice. |
| 2026-05-15 | Keep adapter archives out of the npm package, but let `init --adapter codex` install a verified Codex release archive. | Adapter archives are release artifacts; the CLI can install them without making npm the canonical skill source. | Bundling adapter archives or all generated skills into the first npm package; installing from `.codex/skills`. |
| 2026-05-15 | Use a facade model for validation and keep repository-owned validators authoritative initially. | This preserves existing Python and shell validators while giving users stable command output later. | Porting validators to TypeScript first; making npm the canonical validator source. |
| 2026-05-15 | Use `rigorloop-tree-hash-v1` for generated output tree hashes. | A canonical manifest over normalized relative paths and normalized file hashes gives deterministic drift detection across platforms. | Ad hoc directory hashing; hashes that include mtimes, owners, absolute paths, or symlinks. |
| 2026-05-15 | Use `selected`, `ci`, `change_metadata`, `review_artifacts`, `artifact_lifecycle`, and `skills` as first validation command names. | The names map cleanly to current repository validator families while leaving release and advanced checks direct initially. | Vague command names or wrapping release, adapter archive, token-cost, security, and broad-smoke checks first. |
| 2026-05-15 | Require verified release metadata before network adapter download. | Adapter install must prove official source, version, checksum, size, install root, tree hash, and validation result before writing files. | Silent download, checksum-only install, or fallback to unverified sources. |
| 2026-05-15 | Emit planned lockfile content only until a lockfile spec is accepted. | A lockfile is durable source-of-truth state and should not be written before its ownership, hash, and update contract are approved. | Letting the first public package improvise durable `rigorloop.lock` writes. |

## Next artifacts

- Proposal review for this direction-setting and compatibility-sensitive change.
- Feature spec for CLI package architecture, command contracts, JSON and exit-code behavior, mutation safety, and the first local proof command set.
- Architecture package or ADR for Node package boundaries, validator wrapping, adapter asset model, generated output ownership, and release security controls.
- Execution plan split into reviewable implementation slices after proposal/spec/architecture settlement.
- Test spec mapping command contracts, schema rules, drift detection, and release hardening to concrete tests.

## Follow-on artifacts

- `docs/follow-ups.md` entries `FU-002` through `FU-010` record the proposed slices for later ownership and planning after this proposal is accepted.
- `specs/rigorloop-cli-package-and-codex-init.md` defines the first Codex init CLI slice.

## Readiness

Accepted by `proposal-review-r1`; ready for first-slice spec review.

This proposal does not claim implementation readiness, branch readiness, PR-body readiness, or PR-open readiness.
