# RigorLoop v0.2.0

v0.2.0 publishes the release-process contract and the current RigorLoop CLI through the trusted GitHub Actions npm publication path while preserving GitHub release archives as the adapter delivery surface.

## Install

```bash
npx @xiongxianfei/rigorloop@latest init --adapter codex
npx @xiongxianfei/rigorloop@0.2.0 init --adapter codex
npm install -D @xiongxianfei/rigorloop
npx rigorloop init --adapter codex
```

npm is the CLI delivery channel, not the canonical source for workflow rules, skills, schemas, templates, or adapter definitions.

Adapter archives remain GitHub release artifacts verified by the CLI and are not bundled in the npm package.

Generated public adapter skill bodies are no longer tracked source. Release archives are the active public adapter install path for `v0.2.0`; `dist/adapters/README.md` documents the adapter install-contract surface.

- `rigorloop-adapter-codex-v0.2.0.zip` installs to `.agents/skills/`.
- `rigorloop-adapter-claude-v0.2.0.zip` installs to `.claude/skills/`.
- `rigorloop-adapter-opencode-v0.2.0.zip` installs to `.opencode/skills/`.

Checksums and adapter artifact metadata are recorded in `docs/reports/adapter-artifacts/releases/v0.2.0.yaml`.

## Verification

```bash
bash scripts/release-verify.sh v0.2.0
```

Post-publication evidence is tracked in `docs/releases/v0.2.0.md`.
