# Version Sync Proof

## Purpose

Record the current stable CLI version sources before README and npm-facing
Quick Start examples are updated.

## Sources checked

### GitHub latest stable release

- Command: `gh release view --repo xiongxianfei/rigorloop --json tagName,isDraft,isPrerelease,publishedAt,url`
- Result:
  - `tagName`: `v0.2.0`
  - `isDraft`: `false`
  - `isPrerelease`: `false`
  - `publishedAt`: `2026-05-23T15:46:54Z`
  - `url`: `https://github.com/xiongxianfei/rigorloop/releases/tag/v0.2.0`

### npm package version

- Command: `npm view @xiongxianfei/rigorloop version`
- Result: `0.2.0`

## Decision

- Source agreement: yes
- Chosen pinned version: `@0.2.0`
- Owner decision needed: no
- Blocker: none

Quick-trial examples should use `@latest`. Reproducible onboarding examples
should use `@0.2.0` unless a later release supersedes this proof before the
README/package implementation milestone runs.

## Stale-version sweep baseline

- Command: `rg -n "@xiongxianfei/rigorloop@0\\.1\\.5" README.md packages/rigorloop/README.md packages/rigorloop/package.json docs/ || true`
- Current-use stale examples found:
  - `README.md:42`
  - `README.md:87`
  - `packages/rigorloop/README.md:22`
  - `packages/rigorloop/README.md:55`
  - `packages/rigorloop/README.md:56`
  - `packages/rigorloop/README.md:57`
  - `packages/rigorloop/README.md:63`
  - `packages/rigorloop/README.md:69`
  - `packages/rigorloop/README.md:70`
  - `packages/rigorloop/README.md:71`
  - `packages/rigorloop/README.md:89`
  - `packages/rigorloop/README.md:95`
- Historical examples found and allowed to remain if clearly historical:
  - `docs/releases/v0.1.5/release-notes.md:11`
  - `docs/releases/v0.1.5/npm-publication.md:5`
  - `docs/releases/v0.1.5/npm-publication.md:54`
  - `docs/learn/sessions/2026-05-16-v015-publication-time-retrospective.md:9`

## Follow-up for M2 and M3

M2 and M3 must update current-use README and package README examples from
`@0.1.5` to `@0.2.0` or `@latest` according to the approved Quick Start
contract. Historical release and retrospective references may remain if they are
clearly historical.

## M2 README version result

- Root README current-use stale examples: resolved.
- Root README quick-trial commands:
  - `npx @xiongxianfei/rigorloop@latest --help`
  - `npx @xiongxianfei/rigorloop@latest init --adapter codex`
- Root README reproducible pinned commands:
  - `npx @xiongxianfei/rigorloop@0.2.0 init --adapter codex`
  - `npx @xiongxianfei/rigorloop@0.2.0 init --adapter codex --json`
- M2 stale-version command: `rg -n "@xiongxianfei/rigorloop@0\\.1\\.5" README.md docs/ packages/ || true`
- M2 stale-version result:
  - No `@0.1.5` matches remain in `README.md`.
  - `packages/rigorloop/README.md` still contains current-use `@0.1.5`
    examples; those are owned by M3.
  - Historical release and retrospective references remain in `docs/releases/`
    and `docs/learn/`.

## M3 package README version result

- Package README current-use stale examples: resolved.
- Package README quick-trial commands:
  - `npx @xiongxianfei/rigorloop@latest --help`
  - `npx @xiongxianfei/rigorloop@latest version`
  - `npx @xiongxianfei/rigorloop@latest init --adapter codex`
  - `npx @xiongxianfei/rigorloop@latest init --adapter claude`
  - `npx @xiongxianfei/rigorloop@latest init --adapter opencode`
- Package README reproducible pinned commands now use `@0.2.0`.
- Matching local archive examples now use `rigorloop-adapter-<adapter>-v0.2.0.zip`.
- M3 stale-version command: `rg -n "@xiongxianfei/rigorloop@0\\.1\\.5" README.md packages/rigorloop/README.md packages/rigorloop/package.json docs/ || true`
- M3 stale-version result:
  - No `@0.1.5` matches remain in current README, package README, or package
    metadata surfaces.
  - Historical release and retrospective references remain in `docs/releases/`
    and `docs/learn/`.
