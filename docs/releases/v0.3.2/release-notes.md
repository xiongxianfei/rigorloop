# RigorLoop v0.3.2

v0.3.2 publishes the workflow artifact-location map contract and validator coverage update on top of the target-native init release line.

The workflow guide now exposes a project-local artifact registry and human-readable artifact location map. The validator checks required registry entries, plan-index versus plan-body placement, change-pack evidence placement, and drift between workflow skill defaults, the workflow guide, and directly affected stage skills. The published `workflow` skill now states the action-first formal lifecycle recording rule while preserving `docs/plans/YYYY-MM-DD-slug.md` as the canonical detailed plan-body location.

## npm Package

Use target names directly:

```bash
npx @xiongxianfei/rigorloop@latest init codex
npx @xiongxianfei/rigorloop@0.3.2 init codex
npm install -D @xiongxianfei/rigorloop
npx rigorloop init codex
```

`init codex`, `init claude`, and `init opencode` are the only accepted target forms. Default init does not create `rigorloop.yaml` or `rigorloop.lock`; use `--write-state` when you intentionally want RigorLoop-managed state files.

npm is the CLI delivery channel, not the canonical source for workflow rules, skills, schemas, templates, or adapter definitions. Adapter archives remain GitHub release artifacts verified by the CLI and are not bundled in the npm package.

## Adapter Archives

Generated public adapter skill bodies are no longer tracked source. Release archives are the active public adapter install path for `v0.3.2`; `dist/adapters/README.md` documents the adapter install-contract surface.

- `rigorloop-adapter-codex-v0.3.2.zip` installs to `.agents/skills/`.
- `rigorloop-adapter-claude-v0.3.2.zip` installs to `.claude/skills/`.
- `rigorloop-adapter-opencode-v0.3.2.zip` installs to `.opencode/skills/`.

Checksums and adapter artifact metadata are recorded in `docs/reports/adapter-artifacts/releases/v0.3.2.yaml`.

## Release Gate

The repository-owned release gate is:

```bash
bash scripts/release-verify.sh v0.3.2
```

The gate requires packed-package pre-publish smoke for `codex`, `claude`, and `opencode` using real non-dry-run installs. Dry-run output is not install-success proof.

After publication, release evidence must record live registry/download post-publish smoke for every target.
