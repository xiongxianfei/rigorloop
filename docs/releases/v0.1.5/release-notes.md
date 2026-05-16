# RigorLoop v0.1.5

v0.1.5 publishes the RigorLoop CLI through the trusted GitHub Actions npm publication path while preserving GitHub release archives as the adapter delivery surface.

## npm Package

Install the CLI through npm:

```bash
npx @xiongxianfei/rigorloop@latest init --adapter codex
npx @xiongxianfei/rigorloop@0.1.5 init --adapter codex
npm install -D @xiongxianfei/rigorloop
npx rigorloop init --adapter codex
```

npm is the CLI delivery channel, not the canonical source for workflow rules, skills, schemas, templates, or adapter definitions.

Adapter archives remain GitHub release artifacts verified by the CLI and are not bundled in the npm package.

## Adapter Archives

Generated public adapter skill bodies are no longer tracked source. Release archives are the active public adapter install path for `v0.1.5`; `dist/adapters/README.md` documents the adapter install-contract surface.

- `rigorloop-adapter-codex-v0.1.5.zip` installs to `.agents/skills/`.
- `rigorloop-adapter-claude-v0.1.5.zip` installs to `.claude/skills/`.
- `rigorloop-adapter-opencode-v0.1.5.zip` installs to `.opencode/skills/`.

Checksums and adapter artifact metadata are recorded in `docs/reports/adapter-artifacts/releases/v0.1.5.yaml`.

The repository-owned release gate is:

```bash
bash scripts/release-verify.sh v0.1.5
```

Post-publication evidence is tracked in `docs/releases/v0.1.5/npm-publication.md`.
