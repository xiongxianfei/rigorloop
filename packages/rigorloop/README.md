# @xiongxianfei/rigorloop

RigorLoop CLI for repository-local AI-assisted software delivery.

This package exposes the `rigorloop` binary for approved CLI workflows such as Codex adapter initialization and change metadata scaffolding. Adapter archives remain verified GitHub release artifacts; they are not bundled into the npm package.

## Quick Start

Run directly with `npx`; no install step is required:

```bash
npx @xiongxianfei/rigorloop@latest --help
npx @xiongxianfei/rigorloop@latest version
npx @xiongxianfei/rigorloop@latest init --adapter codex
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
rigorloop init --adapter codex [--dry-run] [--json]
rigorloop new-change <change-id> --title <title> [--dry-run] [--json]
```

## Codex Adapter Install

Initialize the Codex adapter:

```bash
npx @xiongxianfei/rigorloop@0.1.5 init --adapter codex --json
```

Preview the write plan without mutating files:

```bash
npx @xiongxianfei/rigorloop@0.1.5 init --adapter codex --dry-run --json
```

The install command writes repository-local RigorLoop files and installs Codex skills under `.agents/skills/`. The CLI verifies the official GitHub release archive before extraction and verifies the installed tree before reporting success.

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
