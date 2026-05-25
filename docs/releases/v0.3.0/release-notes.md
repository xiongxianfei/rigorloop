# RigorLoop v0.3.0

v0.3.0 publishes the target-native init command contract and removes public `--adapter` syntax.

## npm Package

Use target names directly:

```bash
npx @xiongxianfei/rigorloop@latest init codex
npx @xiongxianfei/rigorloop@0.3.0 init codex
npm install -D @xiongxianfei/rigorloop
npx rigorloop init codex
```

`init codex`, `init claude`, and `init opencode` are the only accepted target forms. Default init does not create `rigorloop.yaml` or `rigorloop.lock`; use `--write-state` when you intentionally want RigorLoop-managed state files.

npm is the CLI delivery channel, not the canonical source for workflow rules, skills, schemas, templates, or adapter definitions. Adapter archives remain GitHub release artifacts verified by the CLI and are not bundled in the npm package.

## Adapter Archives

Generated public adapter skill bodies are no longer tracked source. Release archives are the active public adapter install path for `v0.3.0`; `dist/adapters/README.md` documents the adapter install-contract surface.

- `rigorloop-adapter-codex-v0.3.0.zip` installs to `.agents/skills/`.
- `rigorloop-adapter-claude-v0.3.0.zip` installs to `.claude/skills/`.
- `rigorloop-adapter-opencode-v0.3.0.zip` installs to `.opencode/skills/`.

Checksums and adapter artifact metadata are recorded in `docs/reports/adapter-artifacts/releases/v0.3.0.yaml`.

## Release Gate

The repository-owned release gate is:

```bash
bash scripts/release-verify.sh v0.3.0
```

The gate requires packed-package pre-publish smoke for `codex`, `claude`, and `opencode` using real non-dry-run installs. Dry-run output is not install-success proof.

After publication, release evidence must record live registry/download post-publish smoke for every target.
