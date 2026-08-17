# M3 learn package and parity proof

## Canonical and structural proof

Passed:

- `python scripts/validate-skills.py skills/learn/SKILL.md`
- `python scripts/test-skill-validator.py LearnSkillSimplificationTests`
- `python scripts/test-skill-validator.py`
- `python scripts/test-build-skills.py`
- `python scripts/build-skills.py --check`
- `python scripts/validate-boundary-first.py --check --path specs/learn-skill-simplification.md`
- `python scripts/validate-change-metadata.py docs/changes/2026-08-16-learn-skill-simplification/change.yaml`
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-08-16-learn-skill-simplification`

Observed results include 397 skill-validator tests passing with 16 skipped, seven build-skill tests passing, canonical validation passing, boundary validation passing, valid change metadata, and closed review evidence.

## Adapter distribution proof

The first captured `python scripts/test-adapter-distribution.py` run executed all 150 tests and failed four release-validation fixtures because the new root skill used Codex-specific `$learn` syntax, causing `learn` to be classified as non-portable. M3 replaced that literal with adapter-neutral direct-invocation wording and added a regression assertion that the published skill contains no `$learn` token.

After correction, the four previously failing release-validation cases passed in a focused rerun. The complete corrected rerun then passed all 150 adapter-distribution tests in 379.297 seconds with exit status 0. This covers temporary generated output, adapter archives, release metadata and candidates, mapped-resource hashes, and clean-install fixtures for Codex, Claude, and opencode.

Final command result: `python scripts/test-adapter-distribution.py` — 150 passed, 0 failed.

## Package inventory

The canonical package contains exactly:

- `skills/learn/SKILL.md`
- `skills/learn/references/session-method.md`

It contains no asset, template, script, executable engine, or additional reference. Existing repository generators consume the canonical package; no generated public adapter output was hand-edited.

## Acceptance boundary

All checks are deterministic repository-owned static, fixture, lifecycle, build, archive, release-candidate, and install proof. No target-agent runtime or live external operation executes.
