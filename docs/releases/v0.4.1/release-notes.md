# RigorLoop v0.4.1

v0.4.1 makes the most frequently used RigorLoop skills more concise and easier to navigate while preserving their review, recording, lifecycle, validation, and claim boundaries.

Highlights:

- Simplifies the common paths for `code-review`, `implement`, `workflow`, `verify`, `test-spec-review`, `proposal-review`, and `spec-review`.
- Loads governed lifecycle, automation, recording, settlement, and final-readiness procedure only when the invocation has the matching authority or requested outcome.
- Keeps universal safety, evidence truthfulness, stop conditions, status vocabulary, claim limits, and handoff behavior available in each skill's main file.
- Uses mapped references and existing structural assets as single owners instead of duplicating conditional procedure and output layouts.
- Preserves Codex, Claude, and opencode archive, generated-resource, and clean-install parity.

Some complete skill packages are larger because conditional procedure now has one explicit owner. The ordinary invocation profiles are smaller; the release evidence reports common-path and total-package changes separately rather than presenting relocation as deletion.

Run the complete local release gate with:

```sh
bash scripts/release-verify.sh v0.4.1
```

## npm package

```bash
npx @xiongxianfei/rigorloop@latest init codex
npx @xiongxianfei/rigorloop@0.4.1 init codex
npx @xiongxianfei/rigorloop@0.4.1 init claude
npx @xiongxianfei/rigorloop@0.4.1 init opencode
npx rigorloop init codex
```

The default init does not create `rigorloop.yaml` or `rigorloop.lock`; add `--write-state` when those project-state files should be written explicitly.

Adapter archives remain GitHub release assets verified by the CLI. Generated adapter skill bodies are not tracked canonical source.

## Adapter archives

- `rigorloop-adapter-codex-v0.4.1.zip` installs to `.agents/skills/`.
- `rigorloop-adapter-claude-v0.4.1.zip` installs to `.claude/skills/`.
- `rigorloop-adapter-opencode-v0.4.1.zip` installs skills to `.opencode/skills/` and command aliases to `.opencode/commands/`.

Checksums and tree identities are recorded in `docs/reports/adapter-artifacts/releases/v0.4.1.yaml` and bundled as `adapter-artifacts-v0.4.1.json`.

## Release proof

Pre-publication readiness requires the repository-owned release gate and packed-package pre-publish smoke for all three targets. Public availability is claimed only after live npm and GitHub evidence plus live registry/download post-publish smoke are recorded.

<!-- rigorloop:generated:start release-transaction surface=release-metadata profile=docs/releases/profiles/v0.4.1.yaml -->
- Release profile: `docs/releases/profiles/v0.4.1.yaml`
- npm package: `@xiongxianfei/rigorloop@0.4.1`
- npm dist-tag: `latest`
- Supported targets: codex, claude, opencode
- Adapter metadata: `adapter-artifacts-v0.4.1.json`
- Pending publication evidence: `docs/releases/v0.4.1/npm-publication.md`
<!-- rigorloop:generated:end release-transaction surface=release-metadata -->
