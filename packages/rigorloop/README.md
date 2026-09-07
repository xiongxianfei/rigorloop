# @xiongxianfei/rigorloop

RigorLoop CLI for repository-local AI-assisted software delivery.

This package exposes the `rigorloop` binary for approved CLI workflows such as
target initialization and change metadata scaffolding. Release archives remain
verified GitHub release artifacts; they are not bundled into the npm package.
npm is the CLI delivery channel, not the canonical source for workflow rules,
skills, schemas, templates, or adapter archives.

## Quick Start

Run directly with `npx`; no install step is required:

```bash
npx @xiongxianfei/rigorloop@latest --help
npx @xiongxianfei/rigorloop@latest version
npx @xiongxianfei/rigorloop@latest init codex
npx @xiongxianfei/rigorloop@latest init claude
npx @xiongxianfei/rigorloop@latest init opencode
```

Use a pinned version when you want reproducible setup:

```bash
npx @xiongxianfei/rigorloop@0.5.1 init codex
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

### Explicit workflow recording

This distribution supports `explicit-recording-v1` for explicitly selected new changes in projects that adopt the matching Workflow/CLI models and stage guidance. Installation alone does not adopt the workflow. Historical roots retain their contracts; `new-change`, `workflow-context`, `compact` and `lifecycle` retain their historical purposes and are not new-record registration or progression commands.

```bash
rigorloop record-store inspect --root /path/to/project --change example --format json
rigorloop record-store check --root /path/to/project --change example --input - --format json
rigorloop record-store record --root /path/to/project --change example --input - --format json
rigorloop record-store recover --root /path/to/project --change example --transaction TRANSACTION --expected-recovery DIGEST --action restore --format json
```

`check` and `record` read one UTF-8 JSON request from stdin. The request contains exactly `schema_version: 1`, `contract: explicit-recording-v1`, `change_id`, `expected_revision`, `writes: [{path, expected_identity, content}]` and `reads: [{path, expected_identity}]`. Obtain current revision and identities from inspect; null means absence, not permission to overwrite. `content` is the complete replacement string. Include the actual current hashes of decision-basis files in reads. Inspect/check do not write. Record saves only supplied decisions and never advances a stage or approves work.

The package includes `dist/schemas/explicit-recording-v1.schema.json` and `dist/templates/explicit-recording/records.json`. The latter provides example metadata for change, review, evidence, decisions and successful Verify records. Replace example identities, subjects, actors and decisions with actual evidence. It is not a complete record request and must not be recorded unchanged. In particular, never create a Verify report from the template until successful Verify establishes its claims. A normal initial request writes only `docs/changes/<id>/change.yaml`, with empty registry/applicability arrays; add conditional records only when needed and register them together.

Encode YAML-named records as JSON objects plus a final LF. Markdown records contain `---`, a JSON metadata object, `---`, then nonempty reasoning, with each delimiter on its own line and a final LF. Register supporting records and their explicit applicability in the change record. The CLI preserves supplied bytes; it does not serialize or merge them for you. Create `docs/changes/` in the project before initial recording. The selected change directory must be absent; an existing directory without a manifest cannot be adopted.

All outcomes claim `storage-only`. Text and JSON preserve the same meanings: success is exit 0, rejected input 2, conflict 3, busy 4 and recovery-required 5. Conflict requires rereading and reassessing. Recovery uses the returned transaction and recovery identity; explicitly select `restore` or `complete`. Do not manually edit records during recording or recovery: external exact-target edits after the final identity check can be overwritten. Stale reviews, failed proof and inconsistent completion are observations; actors must block reliance and record corrections explicitly.

Rollback before any new-contract writes restores prior CLI/guidance without changing records. After new records exist, stop invoking write commands and retain this compatible reader while fixing forward; do not use an old writer, delete records or rewrite the contract to simulate rollback. There is no automatic migration, rollback command or extra configuration layer.

### Other command families

```bash
rigorloop --help
rigorloop version
rigorloop init codex|claude|opencode [--write-state] [--from-archive <path>] [--dry-run] [--json]
rigorloop new-change <change-id> --title <title> [--dry-run] [--json]
rigorloop workflow-context [--change <id>] [--format human|json]
rigorloop compact project --change <id> --view <view> [--requested-operation <operation>] [--format human|json]
rigorloop compact apply (--request <path|-> | --request-json <json>) [--format human|json]
rigorloop compact recover --change <id> [--action restore-prior|accept-candidate --expected-recovery-identity <sha256>] [--format human|json]
rigorloop lifecycle status|context <stage>|validate [--change <id>] [--format human|json|concise-human|concise-json|detailed-json]
rigorloop lifecycle <operation> --request <path> [--dry-run] [--format human|json|concise-human|concise-json|detailed-json]
rigorloop logs path [--format human|json]
rigorloop logs show <invocation-id> [--format human|json]
```

Registered historical lifecycle mutations use request files and their existing operations. Existing version-1 coordination remains readable under that contract. Compact operations instead accept transient arguments, standard input, or disposable request files; successful requests are not governed artifacts. The CLI validates expected revision, exact identities, semantic operation shape, and resulting consistency, but it does not grant caller permission.

`workflow-context` is read-only. Without `--change` it reports the effective workflow configuration and up to 32 sorted active-change candidates without selecting one; count and truncation fields show when exact `--change` selection is required. With an exact change ID it reports deterministic lifecycle, artifact, package, milestone, blocker, operation, and bounded automation facts. Collections are capped at 32 entries and expose count/truncation metadata where caller-controlled size can vary. Compact formal reviews use one stable current review path per target; round-suffixed paths remain historical-contract behavior. An optional repository-root `rigorloop.workflow.yaml` may override supported bundled artifact locations; invalid or unsafe configuration fails closed.

The `compact` command exposes the candidate `compact-current-state-v1` boundary without activating compact change creation. `project` returns bounded current views and can evaluate one requested operation separately from overall progression. `apply` accepts the same transient semantic request as an argument, standard input, or disposable file; the transport does not become governed state. `recover` reconciles an interrupted compact transaction from private local recovery state. The compact record and recovery path work without Git history, without PR access, and without local logs. Legacy changes remain on their registered lifecycle contract and reject compact writes or migration.

## Local CLI logs and concise results

RigorLoop records privacy-bounded local JSON Lines diagnostics by default and prints console diagnostics at `error` level by default. Routine success is therefore quiet on stderr. Logs rotate at 5 MiB and retain `rigorloop.jsonl` plus four archives in the platform user-state directory; use `rigorloop logs path` to locate it and `rigorloop logs show <invocation-id>` for exact lookup.

For historical commands, use `--no-file-log` or `RIGORLOOP_FILE_LOG=off` to disable file logging. Set `--file-log-level debug|info|warning|error` and `--console-log-level debug|info|warning|error|off` for one invocation; the matching environment variables are `RIGORLOOP_FILE_LOG_LEVEL` and `RIGORLOOP_CONSOLE_LOG_LEVEL`. `RIGORLOOP_LOG_DIR` accepts only an absolute, non-symlinked safe directory. The separate `record-store` namespace must be the first argument; it rejects these flags, ignores this logging environment and emits only its model-defined result.

Existing v0.4.x output defaults and `--json` remain unchanged. Agents can opt into compact results with `--format concise-json` or `--format concise-human`; complete results remain available with `--format detailed-json`. Local logs are diagnostics only and never authorize lifecycle transitions.

## Target Init

Version 0.5.1 is an unpublished candidate. Its bundled metadata describes route-only candidate archives and makes no claim that those archives or the npm package are publicly available yet. For an exact lockfile-managed install, rerun `init` with `--write-state` to replace `workflow` with `route`; unmanaged or drifted installs remain blocked with state-specific recovery guidance. Persisted `workflow.automation` state remains compatible.

After v0.5.1 is published, initialize target support from its verified official release archive:

```bash
npx @xiongxianfei/rigorloop@0.5.1 init codex --json
npx @xiongxianfei/rigorloop@0.5.1 init claude --json
npx @xiongxianfei/rigorloop@0.5.1 init opencode --json
```

Preview the write plan without mutating files:

```bash
npx @xiongxianfei/rigorloop@0.5.1 init opencode --dry-run --json
```

Use `--from-archive` with a matching generated candidate during local validation, or with the official archive after publication:

```bash
npx @xiongxianfei/rigorloop@0.5.1 init codex --from-archive ./rigorloop-adapter-codex-v0.5.1.zip --json
npx @xiongxianfei/rigorloop@0.5.1 init claude --from-archive ./rigorloop-adapter-claude-v0.5.1.zip --json
npx @xiongxianfei/rigorloop@0.5.1 init opencode --from-archive ./rigorloop-adapter-opencode-v0.5.1.zip --json
```

Default init installs verified target support without writing `rigorloop.yaml` or `rigorloop.lock`. Use `--write-state` when you want RigorLoop-managed project state files. The command verifies the selected archive before extraction and verifies the installed tree before reporting success. Runtime roots are target-specific:

```text
codex:   .agents/skills
claude:  .claude/skills
opencode: .opencode/skills and .opencode/commands when command aliases are declared
```

Network installs use Node `fetch()`. If download fails in a proxied environment, JSON output reports bounded diagnostics such as target name, release version, trusted archive URL, detected proxy environment variable names, Node env-proxy status, and failure class. It does not print proxy credentials or raw proxy values. On Node versions that support env-proxy, enable it with `NODE_USE_ENV_PROXY=1`, `NODE_OPTIONS=--use-env-proxy`, or `node --use-env-proxy`; otherwise use the `--from-archive` fallback.

## Change Metadata Scaffold

Create a new change metadata scaffold:

```bash
npx @xiongxianfei/rigorloop@0.5.1 new-change my-change --title "Describe the change" --json
```

Preview the scaffold first:

```bash
npx @xiongxianfei/rigorloop@0.5.1 new-change my-change --title "Describe the change" --dry-run --json
```

`new-change` creates `docs/changes/<change-id>/change.yaml`. It does not claim that proposal, spec, review, verification, or PR readiness is complete.

## Version Guidance

Use `@latest` for manual exploration. Use an explicit version such as `@0.3.5` for CI, onboarding docs, and repeatable agent setup.

## Source of Truth

npm is the CLI delivery channel. The canonical workflow sources, skills, specs, schemas, and release records live in the GitHub repository:

```text
https://github.com/xiongxianfei/rigorloop
```
