# Proposal-Family Assets Generated Output Proof

## Status

active

This artifact records M4 generated-output, token-cost, P, cold-read, and
no-hand-edit evidence for proposal-family assets progressive disclosure.

## Commands

| Check | Command | Result |
| --- | --- | --- |
| Generated skill mirror check | `python scripts/build-skills.py --check --output-dir /tmp/rigorloop-pfa-m4-skills-final-wybuIX/skills` | passed; generated mirror validation found all proposal-family assets |
| Temporary adapter archives | `python scripts/build-adapters.py --version v0.1.5 --output-dir /tmp/rigorloop-pfa-m4-adapters-final-bT9gTu` | passed; built Codex, Claude, and opencode adapter archives |
| Temporary adapter validation | `python scripts/validate-adapters.py --root /tmp/rigorloop-pfa-m4-adapters-final-bT9gTu --version v0.1.5` | passed |
| Temporary adapter archive inspection | Python `zipfile` inspection against `/tmp/rigorloop-pfa-m4-adapters-final-bT9gTu` | passed; every mapped proposal-family asset is present in every adapter archive |
| Tracked-tree adapter check | `python scripts/build-adapters.py --check --version v0.1.5 --verbose` | deferred; tracked expanded adapter package files are intentionally absent for `v0.1.3` and later |
| Token measurement | `python scripts/measure-skill-tokens.py` | passed; measured 23 skills, 250084 bytes, and 62509 estimated tokens |

## Generated Skill Mirror Assets

The generated skill mirror under
`/tmp/rigorloop-pfa-m4-skills-final-wybuIX/skills` contains:

```text
proposal/assets/proposal-skeleton.md
proposal-review/assets/material-finding.md
proposal-review/assets/review-result-skeleton.md
```

## Temporary Adapter Archive Assets

The temporary `v0.1.5` adapter archives under
`/tmp/rigorloop-pfa-m4-adapters-final-bT9gTu` contain the mapped assets under
each adapter root:

| Adapter archive | Asset root |
| --- | --- |
| `rigorloop-adapter-codex-v0.1.5.zip` | `.agents/skills/` |
| `rigorloop-adapter-claude-v0.1.5.zip` | `.claude/skills/` |
| `rigorloop-adapter-opencode-v0.1.5.zip` | `.opencode/skills/` |

Each archive contains:

```text
proposal/assets/proposal-skeleton.md
proposal-review/assets/review-result-skeleton.md
proposal-review/assets/material-finding.md
```

## Tracked-Tree Adapter Deferral

`python scripts/build-adapters.py --check --version v0.1.5 --verbose` failed
against `dist/adapters/` with `total=112`, `missing=111`, and
`manifest-error=1`.

The failure is deferred because:

- generated skill mirror proof passed;
- temporary adapter archive generation passed;
- temporary adapter validation passed;
- temporary archive inspection found every mapped proposal-family asset;
- no generated adapter body or asset was hand-edited.

The tracked support surface remains `dist/adapters/README.md` and
`dist/adapters/manifest.yaml`; generated public adapter skill bodies are release
archives for `v0.1.3` and later.

## Token Evidence

Baseline commit: `386ff42834e9489ad17a9194b863f40d5332e0af`.

| Skill package | Baseline common-path tokens | Current common-path tokens | Common-path delta | Current asset tokens | Current packaged total delta |
| --- | ---: | ---: | ---: | ---: | ---: |
| `proposal` | 3368 | 3308 | -60 | 225 | +165 |
| `proposal-review` | 3473 | 3469 | -4 | 365 | +361 |

Detailed current measurements:

```text
skills/proposal/SKILL.md: 13232 bytes, 284 lines, 3308 estimated tokens
skills/proposal/assets/proposal-skeleton.md: 899 bytes, 78 lines, 225 estimated tokens
skills/proposal-review/SKILL.md: 13875 bytes, 317 lines, 3469 estimated tokens
skills/proposal-review/assets/review-result-skeleton.md: 999 bytes, 37 lines, 250 estimated tokens
skills/proposal-review/assets/material-finding.md: 457 bytes, 14 lines, 115 estimated tokens
```

The package footprint grows while the common-path `SKILL.md` bodies shrink. As
with the plan skeleton, `proposal-skeleton.md` is justified by common-path
readability and maintainability, not total-token reduction.

## P Evidence

P is recorded as a reviewer-visible usage estimate, not runtime telemetry.

| Asset | P estimate | Context |
| --- | --- | --- |
| `proposal/assets/proposal-skeleton.md` | high | Most `proposal` invocations create a fresh proposal artifact, so the asset is commonly copied. |
| `proposal-review/assets/review-result-skeleton.md` | high | A formal `proposal-review` invocation produces a result artifact. |
| `proposal-review/assets/material-finding.md` | conditional | Loaded once per material finding; clean reviews do not need it. |

## Cold-Read Evidence

Installed skill output is sufficient to understand asset usage:

- `proposal/SKILL.md` maps `COPY assets/proposal-skeleton.md` to creating a
  new proposal artifact, names required proposal sections and triggered
  conditional sections as fill structures, and says not to emit unfilled
  placeholders.
- `proposal-review/SKILL.md` maps `COPY assets/review-result-skeleton.md` to
  producing the proposal-review result artifact and maps
  `COPY assets/material-finding.md` once per material finding.
- Both skills keep rules, enums, review dimensions, recording obligations,
  lifecycle boundaries, validation, and handoff behavior in `SKILL.md`.

## No-Placeholder Evidence

The packaged assets intentionally contain placeholders because they are
copy-and-fill templates. Final representative lifecycle and review artifacts
for this change do not contain unfilled asset placeholders. M4 generated no new
proposal or proposal-review result artifact from the templates.

## No-Hand-Edit Evidence

No generated public adapter body or generated adapter asset was edited. M4 used
temporary generated mirrors and temporary adapter archives only; canonical edits
remain under `skills/` and change-local lifecycle artifacts.
