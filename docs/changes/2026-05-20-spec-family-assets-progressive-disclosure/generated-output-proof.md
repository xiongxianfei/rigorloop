# Spec-Family Assets Generated Output Proof

## Status

active

This artifact records M5 generated-output proof for the spec-family assets
progressive-disclosure change.

## Commands

| Check | Command | Result |
| --- | --- | --- |
| Generated skill mirror check | `python scripts/build-skills.py --check` | passed; validated generated skills from canonical `skills/` using temporary output `/tmp/rigorloop-skills-check-8xybv0pr/skills` |
| Generated skill mirror output | `python scripts/build-skills.py --output-dir /tmp/rigorloop-m5-skills-mirror` | passed; generated skill mirror output under `/tmp/rigorloop-m5-skills-mirror` |
| Temporary adapter archives | `python scripts/build-adapters.py --version v0.1.5 --output-dir /tmp/rigorloop-m5-adapters-db7QUP` | passed; built Codex, Claude, and opencode adapter archives |
| Temporary adapter validation | `python scripts/validate-adapters.py --root /tmp/rigorloop-m5-adapters-db7QUP --version v0.1.5` | passed |
| Tracked-tree adapter check | `python scripts/build-adapters.py --check --version v0.1.5 --verbose` | deferred; tracked expanded adapter package files are intentionally not present for `v0.1.3` and later |

## Generated Skill Mirror Assets

The generated skill mirror under `/tmp/rigorloop-m5-skills-mirror` contains:

```text
spec/assets/acceptance-criterion-row.md
spec/assets/decision-log-row.md
spec/assets/requirement-row.md
spec/assets/spec-skeleton.md
spec-review/assets/review-finding.md
spec-review/assets/review-result-skeleton.md
test-spec/assets/coverage-map-row.md
test-spec/assets/edge-case-row.md
test-spec/assets/test-case.md
test-spec/assets/test-spec-skeleton.md
```

## Temporary Adapter Archive Assets

The temporary `v0.1.5` adapter archives contain the mapped assets under each
adapter root:

| Adapter archive | Asset root |
| --- | --- |
| `rigorloop-adapter-codex-v0.1.5.zip` | `.agents/skills/` |
| `rigorloop-adapter-claude-v0.1.5.zip` | `.claude/skills/` |
| `rigorloop-adapter-opencode-v0.1.5.zip` | `.opencode/skills/` |

Each archive contains:

```text
spec/assets/acceptance-criterion-row.md
spec/assets/decision-log-row.md
spec/assets/requirement-row.md
spec/assets/spec-skeleton.md
spec-review/assets/review-finding.md
spec-review/assets/review-result-skeleton.md
test-spec/assets/coverage-map-row.md
test-spec/assets/edge-case-row.md
test-spec/assets/test-case.md
test-spec/assets/test-spec-skeleton.md
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
