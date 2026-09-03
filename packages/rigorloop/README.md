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

```bash
rigorloop --help
rigorloop version
rigorloop init codex|claude|opencode [--write-state] [--from-archive <path>] [--dry-run] [--json]
rigorloop new-change <change-id> --title <title> [--dry-run] [--json]
rigorloop workflow-context [--change <id>] [--format human|json]
rigorloop lifecycle status|context <stage>|validate [--change <id>] [--format human|json|concise-human|concise-json|detailed-json]
rigorloop lifecycle <operation> --request <path> [--dry-run] [--format human|json|concise-human|concise-json|detailed-json]
rigorloop logs path [--format human|json]
rigorloop logs show <invocation-id> [--format human|json]
```

Governed lifecycle mutations use request files so operation intent and the expected lifecycle revision remain reviewable. Existing version-1 coordination remains readable; run the explicit `migrate` operation before `route-correction`, `return-correction`, or `withdraw-artifact-registration`. Authoring skills continue to use `record-artifact-revision`; route alone owns correction routing, return, and safe duplicate-registration withdrawal through the stable lifecycle `workflow` authority role.

`workflow-context` is read-only. Without `--change` it reports the effective workflow configuration and up to 32 sorted active-change candidates without selecting one; count and truncation fields show when exact `--change` selection is required. With an exact change ID it reports deterministic lifecycle, artifact, package, milestone, blocker, operation, and bounded automation facts. Collections are capped at 32 entries and expose count/truncation metadata where caller-controlled size can vary. Formal review locations retain separate proposal-review, design-review, delivery-review, and code-review ownership; their templates identify `<review-round>` as a required authoring input instead of assigning the shared review directory to one owner. An optional repository-root `rigorloop.workflow.yaml` may override supported bundled artifact locations; invalid or unsafe configuration fails closed.

## Local CLI logs and concise results

RigorLoop records privacy-bounded local JSON Lines diagnostics by default and prints console diagnostics at `error` level by default. Routine success is therefore quiet on stderr. Logs rotate at 5 MiB and retain `rigorloop.jsonl` plus four archives in the platform user-state directory; use `rigorloop logs path` to locate it and `rigorloop logs show <invocation-id>` for exact lookup.

Use `--no-file-log` or `RIGORLOOP_FILE_LOG=off` to disable file logging. Set `--file-log-level debug|info|warning|error` and `--console-log-level debug|info|warning|error|off` for one invocation; the matching environment variables are `RIGORLOOP_FILE_LOG_LEVEL` and `RIGORLOOP_CONSOLE_LOG_LEVEL`. `RIGORLOOP_LOG_DIR` accepts only an absolute, non-symlinked safe directory.

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
