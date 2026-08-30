# M5 lifecycle and adapter parity implementation

Change ID: 2026-08-28-consolidate-rigorloop-review-gates
Milestone: M5
Stage authority: implement
Subject path: docs/plans/2026-08-29-consolidate-rigorloop-review-gates.md
Validation result: pass

## Scope completed

- Added one explicit post-cutover adapter skill inventory derived from the full canonical skill vocabulary while retaining the four historical review skills as canonical readable source.
- Generated archives now contain `design-review` and `delivery-review` and omit `spec-review`, `architecture-review`, `plan-review`, and `test-spec-review` for Codex, Claude Code, and OpenCode.
- Updated OpenCode's curated command inventory to the consolidated authoring and review sequence.
- Made canonical adapter generation fail before output when a canonical skill is missing from or unexpectedly added to the declared inventory.
- Added exact archive-inventory, retired-file drift, and unknown-inventory regressions.
- Regenerated the tracked adapter manifest through the repository generator. No generated adapter skill body or release archive is tracked.

## Existing validator ownership

- `change_metadata_semantics.py` already owns package kinds, statuses, authority, explicit member maps, finding scopes, affected artifacts, correction targets, and unknown-value-first checks from M2.
- `review_artifact_validation.py` already owns package review shape, exact visible members, outcome vocabulary, finding scope, and member attribution from M2.
- `artifact_lifecycle_validation.py` and the lifecycle CLI already own stage and lifecycle consistency from M2 and M3.
- M5 therefore adds no duplicate validator CLI and makes no structural validator claim feasibility, design coherence, proof adequacy, implementation fidelity, or readiness.

## Generated inventory

- Published skills per adapter: 22.
- New package-review skills: `design-review`, `delivery-review`.
- Retired progression skills present in archives: none.
- OpenCode command aliases: 11.
- Tracked manifest: exact generator output for `v0.1.5`.

## Validation

- `python scripts/test-change-metadata-validator.py`: passed; 66 tests.
- `python scripts/test-artifact-lifecycle-validator.py`: passed; 170 tests.
- `python scripts/test-review-artifact-validator.py`: passed; 104 tests.
- `python scripts/test-adapter-distribution.py`: all 154 tests passed across the fail-fast rerun partitions, including the four focused M5 inventory, archive, drift, and unknown-value tests.
- `python scripts/build-adapters.py --version v0.4.1 --output-dir release-output/v0.4.1`: built all three temporary archives.
- `python scripts/validate-adapters.py --root release-output/v0.4.1 --version v0.4.1`: passed.
- Generated archive SHA-256 values:
  - Claude Code: `59b5cecd3f6992fe1caaf25a1bd45ff773e8db1b1fd066689a3441945b8be3ec`.
  - Codex: `a5d622251906bed39602d5b1a3aa7a7bb4b955314692f1b038922d1345a281fb`.
  - OpenCode: `ed0784558b53a41773da4e89f5f5ea1bd0c1846617d7437f8b2c62d3f16d744c`.
- Tracked-manifest comparison against `render_manifest_yaml("v0.1.5", collect_skill_reports())`: passed.
- `git diff --check`: passed.

## Review handoff

M5 is ready for independent Code Review of explicit inventory ownership, fail-closed canonical drift, retired-entrypoint exclusion, OpenCode alias parity, archive reproducibility, and preservation of historical canonical source. This evidence does not activate the consolidated workflow, claim Code Review approval, or close the milestone.
