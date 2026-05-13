# RigorLoop v0.1.3

v0.1.3 completes the adapter install migration started by v0.1.2. Generated public adapter skill bodies are no longer tracked source, and release archives are the active public adapter install path.

Use `dist/adapters/README.md` as the install-contract surface. It points ordinary users to GitHub release archives and records the target install roots for each supported adapter.

Required adapter archives:

- `rigorloop-adapter-codex-v0.1.3.zip`
- `rigorloop-adapter-claude-v0.1.3.zip`
- `rigorloop-adapter-opencode-v0.1.3.zip`

Adapter artifact metadata and checksums are recorded in `docs/reports/adapter-artifacts/releases/v0.1.3.yaml`.

The maintainer-facing release gate is:

```bash
bash scripts/release-verify.sh v0.1.3
```

Compatibility note: v0.1.2 kept repository-tree adapter skill bodies during the compatibility window. v0.1.3 and later install public adapters from release archives.
