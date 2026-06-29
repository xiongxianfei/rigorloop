# RigorLoop v0.3.4

v0.3.4 packages the accumulated workflow, validation, and skill updates since v0.3.3 on top of the target-native init release line.

This release keeps the public CLI command surface stable while refreshing the bundled adapter metadata and public adapter archives. It includes the current canonical skills, workflow guidance, validation scripts, and package metadata needed for repeatable `init codex`, `init claude`, and `init opencode` installs.

## npm Package

Use target names directly:

```bash
npx @xiongxianfei/rigorloop@latest init codex
npx @xiongxianfei/rigorloop@0.3.4 init codex
npm install -D @xiongxianfei/rigorloop
npx rigorloop init codex
```

`init codex`, `init claude`, and `init opencode` are the only accepted target forms. Default init does not create `rigorloop.yaml` or `rigorloop.lock`; use `--write-state` when you intentionally want RigorLoop-managed state files.

npm is the CLI delivery channel, not the canonical source for workflow rules, skills, schemas, templates, or adapter definitions. Adapter archives remain GitHub release artifacts verified by the CLI and are not bundled in the npm package.

## Adapter Archives

Generated public adapter skill bodies are no longer tracked source. Release archives are the active public adapter install path for `v0.3.4`; `dist/adapters/README.md` documents the adapter install-contract surface.

- `rigorloop-adapter-codex-v0.3.4.zip` installs to `.agents/skills/`.
- `rigorloop-adapter-claude-v0.3.4.zip` installs to `.claude/skills/`.
- `rigorloop-adapter-opencode-v0.3.4.zip` installs skills to `.opencode/skills/` and command aliases to `.opencode/commands/`.

Checksums and adapter artifact metadata are recorded in `docs/reports/adapter-artifacts/releases/v0.3.4.yaml`.

## Release Gate

The repository-owned release gate is:

```bash
bash scripts/release-verify.sh v0.3.4
```

The gate requires packed-package pre-publish smoke for `codex`, `claude`, and `opencode` using real non-dry-run installs. Dry-run output is not install-success proof.

After publication, release evidence must record live registry/download post-publish smoke for every target.
