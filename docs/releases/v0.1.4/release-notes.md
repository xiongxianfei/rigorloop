# RigorLoop v0.1.4

v0.1.4 prepares the first public npm package for the RigorLoop CLI while preserving GitHub release archives as the adapter delivery surface.

## npm Package

Install the CLI through npm:

```bash
npx @xiongxianfei/rigorloop@latest init --adapter codex
npx @xiongxianfei/rigorloop@0.1.4 init --adapter codex
npm install -D @xiongxianfei/rigorloop
npx rigorloop init --adapter codex
```

npm is the CLI delivery channel, not the canonical source for workflow rules, skills, schemas, templates, or adapter definitions.

Adapter archives remain GitHub release artifacts verified by the CLI and are not bundled in the npm package.

## Adapter Archives

Release archives are the active public adapter install path for `v0.1.4`:

- `rigorloop-adapter-codex-v0.1.4.zip` installs to `.agents/skills/`.
- `rigorloop-adapter-claude-v0.1.4.zip` installs to `.claude/skills/`.
- `rigorloop-adapter-opencode-v0.1.4.zip` installs to `.opencode/skills/`.

Checksums and adapter artifact metadata are recorded in `docs/reports/adapter-artifacts/releases/v0.1.4.yaml`.

The repository-owned release gate is:

```bash
bash scripts/release-verify.sh v0.1.4
```

FU-010 remains open until public npm publication evidence and actual non-dry-run Codex adapter install smoke are recorded.
