# M4 package-readiness evidence

## Candidate identity

| Identity | Value |
| --- | --- |
| Reviewed M4 implementation commit | `72259213` |
| Reviewed M4 implementation tree | `79e643526a6ed836b5aee17f07062ef407062004` |
| Reviewed M4 implementation diff SHA-256 (`19d49e1e..72259213`) | `f5ed5e4a91c2395b23cc90518259a154cb9dbad217e396d68bb7692cbcb7c1a8` |
| R1 fixed-code commit | `941c7632d89ddd9bf21b53c5f91bc082355b8647` |
| R1 fixed-code tree | `1f80f5eb09234274dfd4fd8f43df8ec869071006` |
| R1 fixed-code diff SHA-256 (`7e8f5d5b..941c7632`) | `9a2456a1293596ad04a67cd343ff97c3af454e5b9d91184a6729783469ac6687` |
| R2 resolved candidate commit | `43adcec9bdd5ab0881f54aebf131ac540b1efdb7` |
| R2 resolved candidate tree | `401b9e5a2b0fcffc8c9a4178ddc9db864928ad67` |
| R2 resolved diff SHA-256 (`52fbd3e3..43adcec9`) | `10a91b0557e262847cbbea177e9b667aa5a71a148e83c700da3fcc42d05a46f7` |
| Resource manifest SHA-256 | `6741b88ec84c392f5c41829203d24bb2044a526f7662cf2d01063358bfae4113` |
| Canonical source inventory SHA-256 | `bb128c838accb20a8232b769b615bedf9d4b4c827eb0b90011a2f7f3ad7ccbf3` |
| Projection-set SHA-256 | `68c6f88c313f706e7011a0e6b7b6625b82464bd3287c15d4fc5b3b7a3a004329` |
| Projection count | 14 |
| Adapter support version | `v0.1.5`, read from `dist/adapters/manifest.yaml` |
| Repository activation state | `pending` |

The source inventory digest covers the three canonical paths and their raw-byte
hashes. The projection digest covers the 14 manifest-keyed logical skill paths.
The implementation and fix commits bind the code candidate; this later evidence
commit records the derived results. No active claim is made.

## Before-and-after loading measurements

Measurements record current raw canonical resource bytes. They are baselines, not budgets or pass/fail thresholds.

The tracked pre-split baseline is commit `9d16bbe2`. Each governed skill mapped
the same 8,318-byte resource with SHA-256
`e65a42359f45d3a0104963386a12aa7a136cdbe18b954d9a62beef044fde134d`.
Its conditional read rules reconstruct the representative initial and expanded
counts below. The current counts come from the closed loading fixture.

| Skill family | Pre-split mapped / initial / expanded | Current mapped / initial / expanded |
| --- | --- | --- |
| Routing and downstream | 1 / 8,318; 1 / 8,318; 1 / 8,318 | 1 / 6,346; 0 / 0; 1 / 6,346 |
| Feature authoring and review | 1 / 8,318; 1 / 8,318; 1 / 8,318 | 2 / 8,670; 2 / 8,670; 2 / 8,670 |
| Proof authoring and review | 1 / 8,318; 1 / 8,318; 1 / 8,318 | 2 / 8,651; 2 / 8,651; 2 / 8,651 |

| Canonical or projected inventory | Pre-split | Current |
| --- | --- | --- |
| Canonical files / bytes | 1 / 8,318 | 3 / 10,975 |
| Manifest-keyed projections / bytes | 10 / 83,180 | 14 / 72,718 |

The comparison uses the same governed stage operation on both sides. At the
pre-split commit, every named stage conditionally reads its one full reference
for that operation. In the current routing/downstream profile, the stage begins
from approved artifact slices and expands to compact guidance only for a
missing, stale, unknown, ambiguous, conflicting, escaped, or insufficient ID.
Feature and proof owners load both of their mapped resources initially.

The closed loading fixture covers all ten governed skills. Unknown schema, skill, resource, or manifest mapping fails before measurement.

## Derived package proof

- Canonical resources match all 14 skill-local projections. Per-resource source
  identities are compact core `4268fbe8...760f6f`, feature authoring
  `962180f3...df7fe`, and proof `ec8e8239...6cc4d`.
- Generated skill output is rebuilt and checked only in a temporary directory.
- Codex, Claude, and opencode `v0.1.5` archives were built in a temporary release-output directory.
- Clean-install smoke validated all ten governed skills for every supported adapter.
- Archive inspection compares every consumer-mapped compact, feature-authoring, and proof resource to canonical raw bytes.
- Layer-specific compact, feature-authoring, and proof mutations each fail with the exact mapped path and canonical/archive hashes.
- Runtime fallback is not used as package evidence; archive and installed bytes are inspected directly.
- No external runtime or hosted service is required by this proof, so no unavailable external-tool result was converted into success.

For cross-layer comparison, adapter-specific roots are normalized back to the
same manifest-keyed logical skill paths before hashing. Every value below covers
14 resources and equals projection digest
`68c6f88c313f706e7011a0e6b7b6625b82464bd3287c15d4fc5b3b7a3a004329`.

| Adapter | Generated | Archive | Clean install |
| --- | --- | --- | --- |
| Codex | 14 / `68c6f88c...004329` | 14 / `68c6f88c...004329` | 14 / `68c6f88c...004329` |
| Claude | 14 / `68c6f88c...004329` | 14 / `68c6f88c...004329` | 14 / `68c6f88c...004329` |
| opencode | 14 / `68c6f88c...004329` | 14 / `68c6f88c...004329` | 14 / `68c6f88c...004329` |

The package proof asserts the exact 14-resource digest independently in each
temporary generated adapter tree, each archive, and each captured clean install.
It also requires every governed skill's portability report to include all three
supported adapters.

Clean-install validation also compares the complete installed
`boundary-first-*.md` inventory with the manifest-derived expected set for each
selected skill. Injected unowned compact, feature-authoring, and proof resources
are rejected for Codex, Claude, and opencode respectively; unrelated packaged
assets remain permitted. An explicitly requested skill cannot be filtered by a
portability report: deleting Claude's requested `workflow` tree fails the
clean-install check.

## Activation and rollback proof

The 63-test boundary suite proves:

- the repository-live pending record passes and remains pending;
- isolated active manifests require the complete parent inventory, adjacent immutable activating and rollback releases, current adapter metadata, and coherent projection identities;
- older, missing, mixed, incomplete, or rewritten rollback metadata fails without mutation;
- mixed projection bytes fail even when their inventory digest is recomputed;
- the active validation CLI emits the authoritative immutable rollback selection.

The 28-test projection suite proves repeated projection identity, handled interruption restoration, input-drift restoration, descriptor-contained recovery, and deterministic retry. Before activation, reverting the tracked candidate and discarding temporary derived output restores one coherent pending bundle; no accepted artifact is rewritten.

## Validation

| Command | Result |
| --- | --- |
| `python scripts/test-boundary-first-reference.py` | pass, 28 tests |
| `python scripts/test-boundary-first-validation.py` | pass, 63 tests |
| `python scripts/validate-boundary-first.py --check` | pass, state `pending` |
| `python scripts/test-skill-validator.py` | pass, 282 tests with 16 documented skips |
| `python scripts/validate-skills.py` | pass, 24 skills |
| `python scripts/build-skills.py --check` | pass with temporary output |
| `python scripts/test-adapter-distribution.py` | pass, 137 tests |
| Planned `build-adapters.py` plus `validate-adapters.py --clean-install-smoke` command | pass for all ten governed skills and three adapters |
| `bash scripts/ci.sh --mode broad-smoke` | pass, 12 checks in 400 seconds |
| `git diff --check` | pass |

## Containment

Generated skills, archives, and installed trees remained temporary and untracked. The live activation manifest was not edited and remains `pending`.
