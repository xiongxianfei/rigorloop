# RigorLoop v0.4.0

v0.4.0 makes boundary-first reasoning automatic and concise across the ten
governed lifecycle skills. Users no longer need to name the method explicitly:
each stage covers the material behavior boundaries admitted by its contract and
observed interfaces, while ordinary work stays focused instead of expanding
into an exhaustive scenario matrix.

This release also simplifies activation to a checked-revision contract. Local
validation reads one declarative pending or active snapshot and does not depend
on tags, remotes, network access, or Git history. The unpublished custom
candidate and atomic-publication experiment is removed; public delivery remains
owned by the existing routine release workflow and trusted tag publication.

Highlights:

- Applies concise, stage-owned boundary coverage automatically in workflow,
  specification, planning, testing, implementation, review, and verification.
- Preserves deeper analysis when a governing contract, material risk, or user
  request requires it, without inventing unrelated scenarios.
- Replaces transition-history activation with deterministic current-file
  validation and a one-time internal historical-inventory derivation function.
- Retires the custom activation candidate and publisher scripts while retaining
  ordinary validation, release preparation, full verification, and closeout.
- Packages equivalent mapped boundary resources for Codex, Claude, and
  opencode, with `v0.3.6` retained as the immutable rollback release.

Run the complete local release gate with:

```sh
bash scripts/release-verify.sh v0.4.0
```

## npm package

Use the stable target-native commands:

```bash
npx @xiongxianfei/rigorloop@latest init codex
npx @xiongxianfei/rigorloop@0.4.0 init codex
npx @xiongxianfei/rigorloop@0.4.0 init claude
npx @xiongxianfei/rigorloop@0.4.0 init opencode
npm install -D @xiongxianfei/rigorloop
npx rigorloop init codex
```

Adapter archives remain GitHub release assets verified by the CLI; generated
adapter skill bodies are not tracked canonical source.

Default init does not create `rigorloop.yaml` or `rigorloop.lock`. Use
`--write-state` only when you explicitly want RigorLoop-managed state files.

## Adapter archives

- `rigorloop-adapter-codex-v0.4.0.zip` installs to `.agents/skills/`.
- `rigorloop-adapter-claude-v0.4.0.zip` installs to `.claude/skills/`.
- `rigorloop-adapter-opencode-v0.4.0.zip` installs skills to
  `.opencode/skills/` and command aliases to `.opencode/commands/`.

Checksums and tree identities are recorded in
`docs/reports/adapter-artifacts/releases/v0.4.0.yaml` and bundled as
`adapter-artifacts-v0.4.0.json`.

## Release proof

Pre-publish readiness requires packed-package pre-publish smoke with real
non-dry-run installs for all three targets; dry-run output is not installation
proof. After publication, closeout requires live registry/download post-publish smoke
for each target before public availability is claimed.

<!-- rigorloop:generated:start release-transaction surface=release-metadata profile=docs/releases/profiles/v0.4.0.yaml -->
- Release profile: `docs/releases/profiles/v0.4.0.yaml`
- npm package: `@xiongxianfei/rigorloop@0.4.0`
- npm dist-tag: `latest`
- Supported targets: codex, claude, opencode
- Adapter metadata: `adapter-artifacts-v0.4.0.json`
- Pending publication evidence: `docs/releases/v0.4.0/npm-publication.md`
<!-- rigorloop:generated:end release-transaction surface=release-metadata -->
