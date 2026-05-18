# @xiongxianfei/rigorloop

RigorLoop CLI for repository-local AI-assisted software delivery.

This package exposes the `rigorloop` binary for approved CLI workflows such as adapter initialization and change metadata scaffolding. Adapter archives remain verified GitHub release artifacts; they are not bundled into the npm package.

## Quick Start

Run directly with `npx`; no install step is required:

```bash
npx @xiongxianfei/rigorloop@latest --help
npx @xiongxianfei/rigorloop@latest version
npx @xiongxianfei/rigorloop@latest init --adapter codex
npx @xiongxianfei/rigorloop@latest init --adapter claude
npx @xiongxianfei/rigorloop@latest init --adapter opencode
```

Use a pinned version when you want reproducible setup:

```bash
npx @xiongxianfei/rigorloop@0.1.5 init --adapter codex
```

Install as a project-local development dependency:

```bash
npm install --save-dev @xiongxianfei/rigorloop
npx rigorloop --help
npx rigorloop init --adapter codex
```

Install globally only if you want a machine-wide `rigorloop` command:

```bash
npm install --global @xiongxianfei/rigorloop
rigorloop --help
rigorloop init --adapter codex
```

## Commands

```bash
rigorloop --help
rigorloop version
rigorloop init --adapter codex|claude|opencode [--from-archive <path>] [--dry-run] [--json]
rigorloop new-change <change-id> --title <title> [--dry-run] [--json]
```

## Adapter Install

Initialize an adapter from the verified official release archive:

```bash
npx @xiongxianfei/rigorloop@0.1.5 init --adapter codex --json
npx @xiongxianfei/rigorloop@0.1.5 init --adapter claude --json
npx @xiongxianfei/rigorloop@0.1.5 init --adapter opencode --json
```

Preview the write plan without mutating files:

```bash
npx @xiongxianfei/rigorloop@0.1.5 init --adapter opencode --dry-run --json
```

Use `--from-archive` when you already downloaded the matching official archive, or when Node `fetch()` cannot reach GitHub from your network:

```bash
npx @xiongxianfei/rigorloop@0.1.5 init --adapter codex --from-archive ./rigorloop-adapter-codex-v0.1.5.zip --json
npx @xiongxianfei/rigorloop@0.1.5 init --adapter claude --from-archive ./rigorloop-adapter-claude-v0.1.5.zip --json
npx @xiongxianfei/rigorloop@0.1.5 init --adapter opencode --from-archive ./rigorloop-adapter-opencode-v0.1.5.zip --json
```

The install command writes repository-local RigorLoop files, verifies the selected archive before extraction, and verifies the installed tree before reporting success. Runtime roots are adapter-specific:

```text
codex:   .agents/skills
claude:  .claude/skills
opencode: .opencode/skills and .opencode/commands when command aliases are declared
```

Network installs use Node `fetch()`. If download fails in a proxied environment, JSON output reports bounded diagnostics such as adapter name, release version, trusted archive URL, detected proxy environment variable names, Node env-proxy status, and failure class. It does not print proxy credentials or raw proxy values. On Node versions that support env-proxy, enable it with `NODE_USE_ENV_PROXY=1`, `NODE_OPTIONS=--use-env-proxy`, or `node --use-env-proxy`; otherwise use the `--from-archive` fallback.

## Change Metadata Scaffold

Create a new change metadata scaffold:

```bash
npx @xiongxianfei/rigorloop@0.1.5 new-change my-change --title "Describe the change" --json
```

Preview the scaffold first:

```bash
npx @xiongxianfei/rigorloop@0.1.5 new-change my-change --title "Describe the change" --dry-run --json
```

`new-change` creates `docs/changes/<change-id>/change.yaml`. It does not claim that proposal, spec, review, verification, or PR readiness is complete.

## Version Guidance

Use `@latest` for manual exploration. Use an explicit version such as `@0.1.5` for CI, onboarding docs, and repeatable agent setup.

## Source of Truth

npm is the CLI delivery channel. The canonical workflow sources, skills, specs, schemas, and release records live in the GitHub repository:

```text
https://github.com/xiongxianfei/rigorloop
```
