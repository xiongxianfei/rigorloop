# Clean Install Proof

## Status

active

## Scope

This proof records the post-change M5 reusable clean-install regression gate for
the published-skill resource-integrity architecture pilot.

The proof uses locally packed release-candidate archives built from current
canonical source. It does not use live registry installation, dry-run output, an
unpackaged source directory, or hand-edited generated output.

## Command Source

The reusable gate is:

```sh
python scripts/validate-adapters.py --version v0.3.2 --root /tmp/rigorloop-sri-install-release-output --clean-install-smoke --skill architecture
```

The command first validates the packed adapter archives under
`/tmp/rigorloop-sri-install-release-output`, then creates a temporary local CLI
release-candidate metadata bundle matching those archives, installs each archive
into an empty temporary project through:

```sh
node <temporary-cli>/bin/rigorloop.js init <target> --from-archive <archive> --json
```

and compares installed mapped architecture resources by skill-root relative path
and raw-byte SHA-256.

## Packed Candidates

Built with:

```sh
python scripts/build-adapters.py --version v0.3.2 --output-dir /tmp/rigorloop-sri-install-release-output
```

Archives inspected:

| Target | Archive |
| --- | --- |
| codex | `/tmp/rigorloop-sri-install-release-output/rigorloop-adapter-codex-v0.3.2.zip` |
| claude | `/tmp/rigorloop-sri-install-release-output/rigorloop-adapter-claude-v0.3.2.zip` |
| opencode | `/tmp/rigorloop-sri-install-release-output/rigorloop-adapter-opencode-v0.3.2.zip` |

Archive parity prerequisite passed with:

```sh
python scripts/validate-adapters.py --version v0.3.2 --root /tmp/rigorloop-sri-install-release-output
```

## Installed Roots

The clean-install smoke installs into empty temporary projects. Temporary
project paths are intentionally disposable; the stable target-specific installed
skill roots are:

| Target | Installed architecture skill root |
| --- | --- |
| codex | `.agents/skills/architecture/` |
| claude | `.claude/skills/architecture/` |
| opencode | `.opencode/skills/architecture/` |

## Mapped Resource Identity

The normalized architecture `Resource map` owns these resources:

| Relative path beneath skill root | Raw SHA-256 |
| --- | --- |
| `assets/architecture-skeleton.md` | `fb284a2940c731ef44a371511338a8d61ab27e87d997e7320bdf2076a98e3d84` |
| `assets/adr-skeleton.md` | `67bb852acb50e4804c3d4e5ad0241c175d2b6a0b8453a21ec9eb185cc098f1ad` |
| `assets/diagram-styles.mmd` | `020be16bb4b01f1eb1a1605562ffd6b31af9e5ba2ee12b1a1e1735acb6378a56` |

The clean-install gate compares those same relative paths and raw hashes under
each target installed architecture skill root.

## Result

```text
validated generated adapter archives and clean installs for version v0.3.2 under /tmp/rigorloop-sri-install-release-output (architecture)
```

## Regression Coverage

`python scripts/test-adapter-distribution.py` includes M5 coverage proving:

- local archive clean install succeeds for a mapped-resource fixture through the
  real `rigorloop init --from-archive` path;
- non-mutating command output is not accepted as clean-install proof;
- stale installed mapped-resource bytes fail raw-byte SHA-256 parity;
- `--clean-install-smoke` without `--root` is rejected so an unpackaged source
  directory cannot substitute for locally packed archives.
