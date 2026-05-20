# Spec-Family Assets Generated Output Proof

## Status

active

This artifact records M5 generated-output proof for the spec-family assets
progressive-disclosure change. M6 refreshed the proof after removing trivial
row assets.

## Commands

| Check | Command | Result |
| --- | --- | --- |
| Generated skill mirror check | `python scripts/build-skills.py --check` | passed; validated generated skills from canonical `skills/` using temporary output `/tmp/rigorloop-skills-check-jmip6gcc/skills` |
| Temporary adapter archives | `python scripts/build-adapters.py --version v0.1.5 --output-dir /tmp/rigorloop-m6-adapters-ohAnao` | passed; built Codex, Claude, and opencode adapter archives |
| Temporary adapter validation | `python scripts/validate-adapters.py --root /tmp/rigorloop-m6-adapters-ohAnao --version v0.1.5` | passed |
| Temporary adapter archive inspection | Python `zipfile` inspection against `/tmp/rigorloop-m6-adapters-ohAnao` | passed; every current mapped asset is present and removed row assets are absent |
| Tracked-tree adapter check | `python scripts/build-adapters.py --check --version v0.1.5 --verbose` | deferred; tracked expanded adapter package files are intentionally not present for `v0.1.3` and later |

## Generated Skill Mirror Assets

The generated skill mirror check validates these current mapped assets:

```text
spec/assets/spec-skeleton.md
spec-review/assets/review-finding.md
spec-review/assets/review-result-skeleton.md
test-spec/assets/coverage-map-row.md
test-spec/assets/test-case.md
test-spec/assets/test-spec-skeleton.md
```

## Temporary Adapter Archive Assets

The temporary `v0.1.5` adapter archives under
`/tmp/rigorloop-m6-adapters-ohAnao` contain the mapped assets under each
adapter root:

| Adapter archive | Asset root |
| --- | --- |
| `rigorloop-adapter-codex-v0.1.5.zip` | `.agents/skills/` |
| `rigorloop-adapter-claude-v0.1.5.zip` | `.claude/skills/` |
| `rigorloop-adapter-opencode-v0.1.5.zip` | `.opencode/skills/` |

Each archive contains:

```text
spec/assets/spec-skeleton.md
spec-review/assets/review-finding.md
spec-review/assets/review-result-skeleton.md
test-spec/assets/coverage-map-row.md
test-spec/assets/test-case.md
test-spec/assets/test-spec-skeleton.md
```

The removed row assets are absent from the refreshed temporary adapter archives:

```text
spec/assets/acceptance-criterion-row.md
spec/assets/decision-log-row.md
spec/assets/requirement-row.md
test-spec/assets/edge-case-row.md
```

## Tracked-Tree Adapter Deferral

`python scripts/build-adapters.py --check --version v0.1.5 --verbose` failed
against `dist/adapters/` because tracked expanded adapter package files are not
present. This is the known tracked-tree adapter debt allowed by `SFA-R36` after
temporary generated proof passes.

The failure did not block M5 because:

- generated skill mirror proof passed;
- temporary adapter archive generation passed;
- temporary adapter validation passed;
- temporary archive inspection found every mapped spec-family asset;
- no generated adapter body or asset was hand-edited.

The tracked support surface remains `dist/adapters/README.md` and
`dist/adapters/manifest.yaml`; generated public adapter skill bodies are release
archives for `v0.1.3` and later.
