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
npx @xiongxianfei/rigorloop@0.5.0 init codex
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

```bash
rigorloop --help
rigorloop version
rigorloop init codex|claude|opencode [--write-state] [--from-archive <path>] [--dry-run] [--json]
rigorloop new-change <change-id> --title <title> [--dry-run] [--json]
rigorloop lifecycle status|context <stage>|validate [--change <id>] [--format human|json|concise-human|concise-json|detailed-json]
rigorloop lifecycle <operation> --request <path> [--dry-run] [--format human|json|concise-human|concise-json|detailed-json]
rigorloop logs path [--format human|json]
rigorloop logs show <invocation-id> [--format human|json]
```

Governed lifecycle mutations use request files so operation intent and the expected lifecycle revision remain reviewable. Existing version-1 coordination remains readable; run the explicit `migrate` operation before `route-correction`, `return-correction`, or `withdraw-artifact-registration`. Authoring skills continue to use `record-artifact-revision`; workflow alone owns correction routing, return, and safe duplicate-registration withdrawal.

## Local CLI logs and concise results

RigorLoop records privacy-bounded local JSON Lines diagnostics by default and prints console diagnostics at `error` level by default. Routine success is therefore quiet on stderr. Logs rotate at 5 MiB and retain `rigorloop.jsonl` plus four archives in the platform user-state directory; use `rigorloop logs path` to locate it and `rigorloop logs show <invocation-id>` for exact lookup.

Use `--no-file-log` or `RIGORLOOP_FILE_LOG=off` to disable file logging. Set `--file-log-level debug|info|warning|error` and `--console-log-level debug|info|warning|error|off` for one invocation; the matching environment variables are `RIGORLOOP_FILE_LOG_LEVEL` and `RIGORLOOP_CONSOLE_LOG_LEVEL`. `RIGORLOOP_LOG_DIR` accepts only an absolute, non-symlinked safe directory.

Existing v0.4.x output defaults and `--json` remain unchanged. Agents can opt into compact results with `--format concise-json` or `--format concise-human`; complete results remain available with `--format detailed-json`. Local logs are diagnostics only and never authorize lifecycle transitions.

## Target Init

Initialize target support from the verified official release archive:

```bash
npx @xiongxianfei/rigorloop@0.5.0 init codex --json
npx @xiongxianfei/rigorloop@0.5.0 init claude --json
npx @xiongxianfei/rigorloop@0.5.0 init opencode --json
```

Preview the write plan without mutating files:

```bash
npx @xiongxianfei/rigorloop@0.5.0 init opencode --dry-run --json
```

Use `--from-archive` when you already downloaded the matching official archive, or when Node `fetch()` cannot reach GitHub from your network:

```bash
npx @xiongxianfei/rigorloop@0.5.0 init codex --from-archive ./rigorloop-adapter-codex-v0.5.0.zip --json
npx @xiongxianfei/rigorloop@0.5.0 init claude --from-archive ./rigorloop-adapter-claude-v0.5.0.zip --json
npx @xiongxianfei/rigorloop@0.5.0 init opencode --from-archive ./rigorloop-adapter-opencode-v0.5.0.zip --json
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
npx @xiongxianfei/rigorloop@0.5.0 new-change my-change --title "Describe the change" --json
```

Preview the scaffold first:

```bash
npx @xiongxianfei/rigorloop@0.5.0 new-change my-change --title "Describe the change" --dry-run --json
```

`new-change` creates `docs/changes/<change-id>/change.yaml`. It does not claim that proposal, spec, review, verification, or PR readiness is complete.

## Version Guidance

Use `@latest` for manual exploration. Use an explicit version such as `@0.3.5` for CI, onboarding docs, and repeatable agent setup.

## Source of Truth

npm is the CLI delivery channel. The canonical workflow sources, skills, specs, schemas, and release records live in the GitHub repository:

```text
https://github.com/xiongxianfei/rigorloop
```
