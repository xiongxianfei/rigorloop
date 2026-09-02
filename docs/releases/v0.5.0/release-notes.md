# RigorLoop v0.5.0

v0.5.0 activates the `stage-owned-change-local-v3` lifecycle and simplifies final readiness: Verify now owns impact-aware evidence selection and creates the durable change explanation only after verification succeeds.

Highlights:

- Activates v3 as the sole current executable lifecycle contract while keeping historical v1/v2 records readable.
- Retires `explain-change` as a standalone current skill and governed stage.
- Makes Verify reuse still-applicable evidence, rerun stale or explicitly fresh-required evidence, and broaden validation when impact is uncertain.
- Directly closes the implementing v2 change without requiring unrelated historical v2 changes to close.
- Records “Refocus Workflow into the Route Skill” as the first proposal governed by v3. The proposal is approved direction evidence; the `workflow`-to-`route` implementation is not part of this release.

Run the complete local release gate with:

```sh
bash scripts/release-verify.sh v0.5.0
```

## npm package

```bash
npx @xiongxianfei/rigorloop@latest init codex
npx @xiongxianfei/rigorloop@0.5.0 init codex
npx @xiongxianfei/rigorloop@0.5.0 init claude
npx @xiongxianfei/rigorloop@0.5.0 init opencode
npx rigorloop init codex
```

The default init does not create `rigorloop.yaml` or `rigorloop.lock`; add `--write-state` when those project-state files should be written explicitly.

Adapter archives remain GitHub release assets verified by the CLI. Generated adapter skill bodies are not tracked canonical source.

## Adapter archives

- `rigorloop-adapter-codex-v0.5.0.zip` installs to `.agents/skills/`.
- `rigorloop-adapter-claude-v0.5.0.zip` installs to `.claude/skills/`.
- `rigorloop-adapter-opencode-v0.5.0.zip` installs skills to `.opencode/skills/` and command aliases to `.opencode/commands/`.

Checksums and tree identities are recorded in `docs/reports/adapter-artifacts/releases/v0.5.0.yaml` and bundled as `adapter-artifacts-v0.5.0.json`.

## Release proof

Pre-publication readiness requires the repository-owned release gate and packed-package pre-publish smoke for all three targets. Public availability is claimed only after live npm and GitHub evidence plus live registry/download post-publish smoke are recorded.

<!-- rigorloop:generated:start release-transaction surface=release-metadata profile=docs/releases/profiles/v0.5.0.yaml -->
- Release profile: `docs/releases/profiles/v0.5.0.yaml`
- npm package: `@xiongxianfei/rigorloop@0.5.0`
- npm dist-tag: `latest`
- Supported targets: codex, claude, opencode
- Adapter metadata: `adapter-artifacts-v0.5.0.json`
- Pending publication evidence: `docs/releases/v0.5.0/npm-publication.md`
<!-- rigorloop:generated:end release-transaction surface=release-metadata -->
