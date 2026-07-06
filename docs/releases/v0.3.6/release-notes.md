# RigorLoop v0.3.6

v0.3.6 packages the workflow guide skeleton asset, markdown readability validation, semantic source-line documentation guardrails, and release metadata refreshes accumulated after v0.3.5.

This release keeps the public CLI command surface stable while refreshing bundled adapter metadata and public adapter archives. It includes the current canonical skills, workflow guidance, validation scripts, and package metadata needed for repeatable `init codex`, `init claude`, and `init opencode` installs.

Highlights:

- Added the workflow guide skeleton asset so customer-project workflow guides can be scaffolded from a maintained template.
- Added markdown readability validation and guidance for source-line formatting.
- Preserved target-native init behavior while refreshing release metadata and adapter artifacts for the current canonical skill set.

Run the release gate with:

```sh
bash scripts/release-verify.sh v0.3.6
```

## npm Package

Use target names directly:

```bash
npx @xiongxianfei/rigorloop@latest init codex
npx @xiongxianfei/rigorloop@0.3.6 init codex
npm install -D @xiongxianfei/rigorloop
npx rigorloop init codex
```

`init codex`, `init claude`, and `init opencode` are the only accepted target forms. Default init does not create `rigorloop.yaml` or `rigorloop.lock`; use `--write-state` when you intentionally want RigorLoop-managed state files.

npm is the CLI delivery channel, not the canonical source for workflow rules, skills, schemas, templates, or adapter definitions. Adapter archives remain GitHub release artifacts verified by the CLI and are not bundled in the npm package.

## Adapter Archives

Generated public adapter skill bodies are no longer tracked source. Release archives are the active public adapter install path for `v0.3.6`; `dist/adapters/README.md` documents the adapter install-contract surface.

- `rigorloop-adapter-codex-v0.3.6.zip` installs to `.agents/skills/`.
- `rigorloop-adapter-claude-v0.3.6.zip` installs to `.claude/skills/`.
- `rigorloop-adapter-opencode-v0.3.6.zip` installs skills to `.opencode/skills/` and command aliases to `.opencode/commands/`.

Checksums and adapter artifact metadata are recorded in `docs/reports/adapter-artifacts/releases/v0.3.6.yaml`.

## Release Gate

The repository-owned release gate is:

```bash
bash scripts/release-verify.sh v0.3.6
```

The gate requires packed-package pre-publish smoke for `codex`, `claude`, and `opencode` using real non-dry-run installs. Dry-run output is not install-success proof.

After publication, release evidence must record live registry/download post-publish smoke for every target.

<!-- rigorloop:generated:start release-transaction surface=release-metadata profile=docs/releases/profiles/v0.3.6.yaml -->
- Release profile: `docs/releases/profiles/v0.3.6.yaml`
- npm package: `@xiongxianfei/rigorloop@0.3.6`
- Supported targets: codex, claude, opencode
- Adapter metadata: `adapter-artifacts-v0.3.6.json`
- Pending publication evidence: `docs/releases/v0.3.6/npm-publication.md`
<!-- rigorloop:generated:end release-transaction surface=release-metadata -->
