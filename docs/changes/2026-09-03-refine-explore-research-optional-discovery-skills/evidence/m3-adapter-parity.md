# M3 implementation evidence: Generated adapter and candidate parity

Milestone: M3
Subject path: docs/plans/2026-09-03-refine-explore-research-optional-discovery-skills.md
Subject identity: sha256:24f3acd041bdd46b56a5a45007f71ee38d9244d4ed07f48d2317718484d3c3fb
Validation result: passed

## Result

## Core result

- Skill: implement
- Status: implemented
- Completed scope: M3 discovery-specific archive and clean-install parity proof, deterministic v0.4.0 candidate generation, unpublished v0.5.1 bundled candidate identity synchronization, npm trust-index synchronization, and historical-release preservation
- Artifacts changed: `scripts/test-adapter-distribution.py`, `packages/rigorloop/dist/metadata/adapter-artifacts-v0.5.1.json`, `packages/rigorloop/dist/metadata/releases.json`, and `packages/rigorloop/test/cli.test.js`
- Tests added or updated: one three-adapter discovery archive/clean-install parity test and the current-candidate npm identity assertion
- Validation performed: focused parity and correction tests, complete adapter distribution, build-skill, skill-validator, token-cost, npm package, candidate archive, clean-install, generated-skill, historical-hash, whitespace, and broad-smoke checks
- Validation result: all required M3 commands and correction checks pass
- Open blockers: none
- Next stage: code-review
- Claim limitations: temporary candidates were not published or committed as adapter bodies; this evidence does not claim final branch, PR, release, deployment, or hosted-CI readiness

## Planned milestone

- Change ID: 2026-09-03-refine-explore-research-optional-discovery-skills
- Plan identity: `docs/plans/2026-09-03-refine-explore-research-optional-discovery-skills.md`, `sha256:24f3acd041bdd46b56a5a45007f48d2317718484d3c3fb`
- Milestone ID: M3
- Milestone state: implementation in progress; ready for review-requested transition
- Baseline or change-pack status: complete for canonical-to-archive-to-clean-install parity and the current unpublished package candidate
- Milestone validation evidence: this file and the command results below
- Commit status: M3 handoff commit subject `M3: propagate optional discovery packages to adapters`
- Code-review handoff: review adapter inventory, exact resource bytes, public-text hygiene, candidate metadata identities, clean-install proof, failure coverage, temporary-output cleanup, and historical preservation

## Test and correction evidence

The new discovery-specific test built v0.4.0 archives for Codex, Claude Code, and opencode; validated every archive; performed clean installs selecting exactly Explore and Research; checked all eight mapped resources; compared each packaged `discovery-support.md` with the canonical raw bytes; checked standalone artifact paths; and rejected maintainer-only source or adapter wording. It passed immediately, demonstrating that the existing generic generator and installer already support the new resources and need no speculative production change.

The first complete adapter suite then passed 156 tests and failed one current-candidate identity check: bundled unpublished v0.5.1 metadata still described 97-file archives while current canonical generation produced 105 files. The v0.5.1 metadata, its release-index hash, and the corresponding npm test assertion were updated from freshly generated deterministic identities. The two focused adapter tests passed, the focused npm assertion passed, and the complete suites then passed.

## Validation results

- `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_optional_discovery_packages_have_archive_and_clean_install_parity` — passed across three supported adapters.
- `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_v0_5_1_bundled_candidate_metadata_matches_generated_route_only_archives AdapterDistributionTests.test_optional_discovery_packages_have_archive_and_clean_install_parity` — passed after candidate synchronization.
- `python scripts/test-adapter-distribution.py` — passed, 157 tests in 394.542 seconds on the corrected tree.
- `python scripts/test-build-skills.py` — passed, 8 tests.
- `python scripts/test-skill-validator.py` — passed, 362 tests.
- `python scripts/test-token-cost-measurement.py` — passed, 25 tests.
- `python scripts/build-skills.py --check` — passed using temporary generated output.
- `python scripts/build-adapters.py --version v0.4.0 --output-dir <fresh-mktemp>` — built all three deterministic candidate archives.
- `python scripts/validate-adapters.py --root <fresh-mktemp> --version v0.4.0 --clean-install-smoke --skill explore --skill research` — passed archive and clean-install parity for all supported adapters.
- `npm test --prefix packages/rigorloop` — passed, 373 tests with 2 intentional skips.
- `bash scripts/ci.sh --mode broad-smoke` — passed, 12 checks in 477 seconds.
- `git diff --check` — passed.

## Distribution and historical integrity

- Each adapter retains separate `explore` and `research` skill roots and all package-local assets and references.
- Archive validation compares every mapped resource hash with canonical source; clean-install validation repeats that comparison after installation into empty target projects.
- The shared discovery policy is byte-identical in canonical source, both skill-local packages, archives, and clean installs.
- Missing, stale, escaped, malformed, unknown-inventory, extra-resource, and failed-install cases remain covered by the existing fail-closed adapter suite; generator output is built in temporary roots and gains no publication authority.
- The changed v0.5.1 record is explicitly `local-release-candidate`; its metadata now records 105 skill files and its index records metadata SHA-256 `894ebde3c8b920e7d8ffc8e2ba6918dd74a60ab98d7182dbaf7587f7a4fed3ad`.
- Historical v0.5.0 metadata remains byte-identical at SHA-256 `74f2d940ce8ef358092609884e9377d0a3955c731e7f437ca63d995862227885`; no earlier release metadata or archive was changed.
- `dist/adapters/manifest.yaml` and `dist/adapters/README.md` need no edit because both skill names and the generic all-resource packaging contract already cover this change.

## Recovery

The exact v0.4.0 validation directory was moved to the system trash after validation. Rollback removes the discovery parity test and restores only the unpublished v0.5.1 candidate metadata, its index hash, and its matching test assertion; historical release identities and canonical M1/M2 behavior remain independent.
