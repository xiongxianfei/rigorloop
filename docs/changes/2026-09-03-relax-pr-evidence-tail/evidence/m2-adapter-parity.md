# M2 implementation evidence: PR evidence-tail adapter parity

Milestone: M2
Subject path: docs/plans/2026-09-03-relax-pr-evidence-tail.md
Subject identity: sha256:9b762060e3022f6d0310ad8197ff363c92228c3bb89ff3d92d59935541bf4494
Validation result: passed

## Result

- Skill: implement
- Status: implemented
- Completed scope: deterministic Codex, Claude Code, and opencode candidate parity for the proportional PR suffix contract, coupled Verify wording, and current unpublished v0.5.1 metadata
- Artifacts changed: `scripts/test-adapter-distribution.py`, `packages/rigorloop/dist/metadata/adapter-artifacts-v0.5.1.json`, `packages/rigorloop/dist/metadata/releases.json`, and `packages/rigorloop/test/cli.test.js`
- Open blockers: none
- Next stage: code-review
- Claim limitations: this evidence does not claim Code Review acceptance, final holistic review, final verification, hosted CI, PR readiness, publication, or release readiness

## Test and derivation evidence

The first full adapter-distribution run failed only `test_v0_5_1_bundled_candidate_metadata_matches_generated_route_only_archives`, exposing the expected stale current-candidate archive, tree, size, and release-index identities after canonical bytes changed. The failure printed the complete generator-derived replacement values. Those exact current v0.5.1 values were applied, and the bundled-candidate test passed on rerun.

A direct archive regression now opens every generated adapter archive and proves that:

- the PR package contains the closed `none`, `evidence-only`, and `invalidating` suffix vocabulary;
- any commit count or direct-parent topology is permitted only under the evidence rule;
- the retired one-direct-child wording is absent; and
- the packaged Verify explanation states that final-review and workflow inputs do not become part of Verify result registration.

## Current candidate identities

| Adapter | Archive SHA-256 | Size bytes | Skills tree SHA-256 |
| --- | --- | ---: | --- |
| Codex | `dab13755f45c7a19a5f62f58d1f2abba4043cc1ee82c08f6785201634355abc6` | 197685 | `5b82fdc6409ddf8981969c7cb0b9da9657ad7bb4889324bcd0a3081dfe10128f` |
| Claude Code | `4ee807820e5bc0aadfb159250b8f963778d878f2c318b62910a7c7fc2560188a` | 196927 | `fe067c51da4c00b5608a556e13fbabfa3ab4845771ed30674b89155b6d0fd8cc` |
| opencode | `efa3906651a70a2788df920db672ab456127e6a1d0288229b1d2c6bfec6e0a5c` | 199897 | `fe067c51da4c00b5608a556e13fbabfa3ab4845771ed30674b89155b6d0fd8cc` |

The resulting bundled metadata hash is `6586b8a01a011e6fe8d89af1f8b5dc35c0db63e606c8292aedeff6ad969fab6c`. File counts remain 105 for each skills tree; opencode's ten-command alias tree and hash are unchanged.

## Validation results

- `python scripts/test-build-skills.py` — passed, 8 tests.
- `python scripts/test-adapter-distribution.py` — passed after metadata refresh, 157 tests.
- `python scripts/test-select-validation.py` — passed, 154 tests.
- `npm test --prefix packages/rigorloop` — passed, 375 tests total: 373 passed and 2 intentionally skipped.
- `bash scripts/ci.sh --mode broad-smoke` — passed, 11 checks in 486 seconds.
- `git diff --check` — passed.

## Changed and unaffected surfaces

- Changed: only current unpublished v0.5.1 archive, tree, size, bundled-metadata, and exact CLI fixture identities plus direct generated-contract assertions.
- Unaffected: historical release metadata, release archives, `dist/adapters/README.md`, `dist/adapters/manifest.yaml`, generated adapter bodies, command-alias identities, canonical skill text, lifecycle schemas, and publication state.
- Temporary generator output remained under tool-created temporary roots and was not adopted as authored source.

## Recovery

Revert the M2 metadata, fixture, and direct archive assertions as one unit with the accepted M1 canonical changes if rollback is required. Do not rewrite historical releases or publish a mixed candidate.
