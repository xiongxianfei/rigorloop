# Generated Output Proof: CI-Maintenance Skill Rename and Workflow Authoring

## Scope

This proof covers M3 generated local skill output and temporary public adapter archives for the hard rename from `ci` to `ci-maintenance`.

## Tracked Adapter Metadata

- `dist/adapters/manifest.yaml` lists `ci-maintenance` as the supported adapter skill.
- `dist/adapters/manifest.yaml` no longer lists `ci` as an active skill entry.
- `dist/adapters/README.md` includes adopter-facing migration guidance: direct `ci` invocations should be updated to `ci-maintenance`; this release does not install `ci` as a compatibility alias.

## Generated Local Skill Output

Command:

```bash
python scripts/build-skills.py --check --output-dir /tmp/rigorloop-cim-m3-skills/skills
```

Result: passed.

This proves generated local skill output can be built from canonical `skills/` with the renamed `ci-maintenance` skill and packaged resources.

## Adapter Distribution Regression

Command:

```bash
python scripts/test-adapter-distribution.py
```

Result: passed, 112 tests.

This proves the hard rename and validator update remain compatible with adapter generation, release-validation fixtures, archive packaging, non-Codex front matter transforms, and adapter support-surface expectations.

## Temporary Adapter Archives

Command:

```bash
tmpdir="$(mktemp -d)" && \
python scripts/build-adapters.py --version v0.1.5 --output-dir "$tmpdir" && \
python scripts/validate-adapters.py --root "$tmpdir" --version v0.1.5
```

Output root:

```text
/tmp/tmp.eXBa1HTkJk
```

Result: passed.

Built archives:

```text
/tmp/tmp.eXBa1HTkJk/rigorloop-adapter-codex-v0.1.5.zip
/tmp/tmp.eXBa1HTkJk/rigorloop-adapter-claude-v0.1.5.zip
/tmp/tmp.eXBa1HTkJk/rigorloop-adapter-opencode-v0.1.5.zip
```

## Archive Content Inspection

The generated archives contain the renamed skill and its resources:

```text
rigorloop-adapter-claude-v0.1.5.zip
.claude/skills/ci-maintenance/SKILL.md
.claude/skills/ci-maintenance/assets/github-workflow-skeleton.yml
.claude/skills/ci-maintenance/references/risk-to-check-map.md

rigorloop-adapter-codex-v0.1.5.zip
.agents/skills/ci-maintenance/SKILL.md
.agents/skills/ci-maintenance/assets/github-workflow-skeleton.yml
.agents/skills/ci-maintenance/references/risk-to-check-map.md

rigorloop-adapter-opencode-v0.1.5.zip
.opencode/skills/ci-maintenance/SKILL.md
.opencode/skills/ci-maintenance/assets/github-workflow-skeleton.yml
.opencode/skills/ci-maintenance/references/risk-to-check-map.md
```

The same inspection command searched for `/ci/` archive paths and found no active `ci` skill body.

## Tracked Tree Adapter Check

Command:

```bash
python scripts/build-adapters.py --check --version v0.1.5 --verbose
```

Result: failed with expected tracked-tree archive-era drift.

The command reports missing generated adapter skill bodies under `dist/adapters/{codex,claude,opencode}/...`. This is expected for `v0.1.3` and later because generated public adapter skill bodies are release archives, not tracked source under `dist/adapters/`.

The command also reports the existing `command_aliases` section as unsupported for `v0.1.5`. This change does not modify command-alias behavior; it updates the tracked adapter skill metadata and proves release archives through temporary generated output and `validate-adapters.py --root`.

## Preservation Result

- Canonical generated public adapter proof includes `ci-maintenance`.
- Generated public adapter proof includes `assets/github-workflow-skeleton.yml`.
- Generated public adapter proof includes `references/risk-to-check-map.md`.
- Generated public adapter proof does not expose an active `ci` skill body.
- Adapter proof was generated from canonical skills and temporary output, not hand-edited public adapter package output.
