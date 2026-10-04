# @xiongxianfei/rigorloop

RigorLoop CLI for repository-local AI-assisted software delivery.

This package exposes the `rigorloop` binary for approved CLI workflows such as target initialization and current engineering handoffs. Release archives remain verified GitHub release artifacts; they are not bundled into the npm package. npm is the CLI delivery channel, not the canonical source for workflow rules, skills, schemas, templates, or adapter archives.

## Quick Start

Run directly with `npx`; no install step is required:

```bash
npx @xiongxianfei/rigorloop@latest --help
npx @xiongxianfei/rigorloop@latest version
npx @xiongxianfei/rigorloop@latest init codex
npx @xiongxianfei/rigorloop@latest init claude
```

After the candidate is published, pin its version for reproducible setup:

```bash
npx @xiongxianfei/rigorloop@2.0.0 init codex
```

Install as a project-local development dependency:

```bash
npm install --save-dev @xiongxianfei/rigorloop
npx rigorloop --help
npx rigorloop init codex
```

Install globally only if you want a machine-wide `rigorloop` command:

```bash
npm install --global @xiongxianfei/rigorloop
rigorloop --help
rigorloop init codex
```

## Commands

The successor uses targeted-recording-v2 / rigorloop-records-v4 and project-local SQLite. Skills supply engineering intent and judgments through the CLI; they do not execute SQL. Installation alone does not adopt a workflow, import records or approve work.

Create a tracked `.rigorloop.json` containing `{"schema_version":1,"project_id":"<stable UUID>"}` and ignore `.rigorloop/`. Current requirements, designs and implementation stay in the repository. Operational state lives in `.rigorloop/rigorloop.db`; selected large payloads live under `.rigorloop/artifacts/changes/`. Use a qualified Node 24.15.0+ build within Node 24, with SQLite 3.51.3+; current coordination and safe installation require Linux filesystem primitives.

```sh
rigorloop capabilities --root . --format json
rigorloop change create --root . --change example --input - --format json
rigorloop change context --root . --change example --format json
rigorloop change update --root . --change example --input - --format json
rigorloop review prepare code --root . --change example --input - --format json
rigorloop review show code --root . --change example --format json
rigorloop review record code --root . --change example --input - --format json
rigorloop verification record final --root . --change example --input - --format json
rigorloop verification show final --root . --change example --format json
rigorloop change complete --root . --change example --input - --format json
rigorloop store backup --root . --input - --format json
rigorloop store restore --root . --input - --format json
rigorloop store migrate --root . --input - --format json
```

`--input -` reads one bounded JSON request from stdin. Record mutations use `{schema_version:2, interface:"targeted-recording-v2", contract:"rigorloop-records-v4", change_id, expected_revision, reads, input}`. Creation supplies a null expected revision; updates use the exact current revision. Task inputs are defined in the bundled `dist/schemas/targeted-recording-v2.schema.json`. Read results use schema 4; a save is a storage result, never an inferred approval. Review and Verification IDs are Change-local.

Context supplies the current seven-part engineering handoff and bounded observations. Selected queries expose omissions and unknown support. Replace comparable working information when useful; open obligations and judgments still relied upon retain explicit dispositions and attribution. One formal whole-change Code Review gate precedes distinct final Verify. Completed Changes retain compact historical acceptance rather than tracking future repository drift.

Preview with `--dry-run` reserves nothing. Conflicts require rereading and reconciling the caller's decision. Maintenance uses its separately versioned `store-maintenance-v1` request and explicit store/source observations. Interrupted replacement remains fenced until an explicit finish or rollback can reconcile known bytes. Do not copy a live WAL database manually; use `store backup`. Restore creates a new store incarnation so earlier revision tokens cannot authorize updates.

Earlier filesystem recording commands and targeted-recording-v1 are not supported by this executable. Retain the earlier executable for unconverted work. `store migrate` supports explicit qualified v3 import with complete dispositions and separately retained originals; it never promotes old approvals to the new requirement basis. No bulk deletion of historical files is implied.

### Maintenance input

`dist/schemas/store-maintenance-v1.schema.json` supplies the complete `backup`, `restore` and `migrate` definitions; `rigorloop store TASK --help` resolves its installed location. Every request wraps `input` in `{"schema_version":1,"interface":"store-maintenance-v1","input":...}`.

For example, pipe this JSON to `rigorloop store backup --root . --input - --format json`:

```json
{"schema_version":1,"interface":"store-maintenance-v1","input":{"scope":{"changes":"all"},"output":"../project-backup","actor":{"id":"engineer","role":"human"}}}
```

A selected backup uses `scope.changes: ["change-id"]`. The destination must be absent and outside the live runtime directory. Restore input supplies `backup`, its returned `expected_backup` integrity, `expected_store` (`{"kind":"absent"}` or the current revision from `capabilities`), explicit `replace`, `actor` and `reason`. Run with `--dry-run` to inspect admission before the real request.

For qualified v3 import use `migrate` with `mode: "legacy-import"`, exact source scope and a disposition for every selected record. A preview permits null `expected_source` to obtain the source observation; execution requires that returned digest. Unsupported source contracts stop without conversion. Required originals go to an explicit external `originals_output`.

An interrupted operation is visible through `capabilities`. Resume the same task using `input: {"resume":{"operation_id":"...","expected_observation":"sha256:...","action":"finish"},"actor":{"id":"engineer","role":"human"},"reason":"Inspected recovery state"}`. `rollback` is available only while the inspected state permits it. Resume does not accept `--dry-run`; stale observations and foreign content stop recovery. No successful save or recovery establishes review approval.

### Installation and diagnostics

```sh
rigorloop --help
rigorloop version
rigorloop init codex|claude [--force] [--from-archive <path>] [--dry-run] [--json]
rigorloop init codex --replace-workflow requirement-first-v1 --force
rigorloop logs [--format human|json]
rigorloop logs --invocation <invocation-id> [--format human|json]
```

Every successor archive includes a verified workflow descriptor. Explicit replacement retires only `proposal`, `proposal-review` and `design` under the selected target root and retains originals outside discovery. It installs the verified candidate without sweeping unrelated skills or other targets. Ordinary force cannot retire the old workflow. Init result schema 2 reports actual per-unit effects, including partial failures; retry does not imply rollback. Dry-run reports a preliminary plan without acquiring an archive.

## Local CLI logs and concise results

RigorLoop records privacy-bounded local JSON Lines diagnostics by default and prints console diagnostics at `error` level by default. Routine success is therefore quiet on stderr. Logs rotate at 5 MiB and retain `rigorloop.jsonl` plus four archives in the platform user-state directory; use `rigorloop logs` to locate it and `rigorloop logs --invocation <invocation-id>` for exact lookup.

For installation and general commands, use `--no-file-log` or `RIGORLOOP_FILE_LOG=off` to disable file logging. Set `--file-log-level debug|info|warning|error` and `--console-log-level debug|info|warning|error|off` for one invocation; the matching environment variables are `RIGORLOOP_FILE_LOG_LEVEL` and `RIGORLOOP_CONSOLE_LOG_LEVEL`. `RIGORLOOP_LOG_DIR` accepts only an absolute, non-symlinked safe directory. Operational recording commands, `capabilities` and `store` must be the first argument; they reject these flags, ignore this logging environment and emit only their model-defined results.

General commands support `--json`. Agents can opt into compact results with `--format concise-json` or `--format concise-human`; complete results remain available with `--format detailed-json`. Local logs are diagnostics only and never authorize lifecycle transitions.

## Target Init

Use `rigorloop init codex|claude` to install verified skills into `.agents/skills/` or `.claude/skills/`. Package-bundled trusted metadata identifies the official archive. `--from-archive <path>` uses the same trusted metadata and verification for a local copy; it does not accept a substitute trust root.

Installation checks every candidate skill destination after archive verification. Any existing skill directory or declared file is a conflict, even if empty or identical. It lists the conflicts and installs nothing. Shared parent directories and unrelated skills are preserved.

The installer currently requires Linux with accessible `/proc/self/fd` directory descriptors and a filesystem supporting hard links. If those safety primitives are unavailable, installation stops without replacing existing skills. This requirement applies to fresh installation as well as force replacement.

Use `--force` to replace existing destination skills completely. Local changes and obsolete files within replaced skill directories leave the active installation. Originals remain at reported private paths outside skill discovery for separate inspection and cleanup. Symlinks, unsafe paths and intervening changes still stop installation. Partial failure reports what completed, what failed and what remains untouched; retry performs verification again and existing destinations still require explicit `--force`.

```bash
rigorloop init codex --dry-run --json
rigorloop init claude --from-archive ./rigorloop-adapter-claude-<version>.zip --json
rigorloop init codex --force
```

Dry-run reports preliminary destination checks and unperformed archive verification without downloading, extracting or writing. Installation does not read or write `rigorloop.yaml` or `rigorloop.lock`; their presence and contents do not affect installation. `--write-state` and `--adapter` are retired, and OpenCode is unsupported, including pinned and local-archive requests through this CLI.

Network failures report bounded diagnostics without proxy credentials. Configure Node's `NODE_USE_ENV_PROXY` or `--use-env-proxy` support when needed, or download the matching official archive and use `--from-archive`.

## New Change recording

Use `rigorloop change create --help` for the request envelope and bundled schema location. Submit a v2 request for the v4 record contract with `--root PATH --change ID --input - --format json`. Creation requires explicit authority and an unused Change ID; it grants no engineering judgment. The removed `new-change` scaffold is unsupported.

## Version guidance

This source describes the 2.0.0 candidate. It does not assert that the candidate is published. Pin an actually published version for repeatable installation; historical releases retain their original interface and runtime requirements.

## Source of Truth

npm is the CLI delivery channel. The canonical workflow sources, skills, Designs, schemas, and release records live in the GitHub repository:

```text
https://github.com/xiongxianfei/rigorloop
```

## Upgrading retired authoring skills

The successor supplies `requirement-analysis`, `requirement-review`, `system-design` and `architecture-design`. Use the explicit workflow replacement above to retire `proposal`, `proposal-review` and `design`. Earlier unrelated retired entries are not swept. Historical archives require their matching earlier executable; the successor requires its verified workflow descriptor. Importing old records is a separate, qualified maintenance operation.

## Feature-format support change

Current skills author living Designs with model-owned test intent and Delivery allocation. Feature-spec amendments and companion test-spec/proof-map operations are no longer supported. Existing documents remain readable sources under project authority; installation does not convert or delete them. A project requiring the old output can use another tool or explicitly authorize scoped adoption into living Designs. This compatibility change applies to the next artifact built from these sources, not to previously released archives.
