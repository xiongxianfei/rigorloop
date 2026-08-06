# PR Full-Gate Review Resolution Implementation Evidence

Stage: implement
Date: 2026-08-06
Scope: `UBR-PRFG-CR1-001`, `UBR-PRFG-CR1-002`, `UBR-PRFG-CR1-003`
Approved contract: UBR-R021, BND-COMPAT-001, AC-UBR-013, EC11
Approved proof: T24, PRF-007, test-spec-review-r4

## Tests first

- Lifecycle authority: the new T24 regression initially failed because `validate_feature_record` had no repository root and accepted owner-pointer syntax without resolving `change.yaml`.
- Release profiles: the three malformed paths initially returned selector exit 0 and fabricated release versions instead of `release-version-required`.
- Historical opencode: the four older skills-only cases initially exposed `v0.4.0` metadata despite requesting `v0.3.3`.

## Implementation

- The boundary validator now resolves the normalized owning-change pointer inside the repository, rejects missing, symlinked, unreadable, duplicate, or non-stage-owned lifecycle authority, and threads that authority through feature and proof validation.
- The release selector treats `docs/releases/profiles/` as an exclusive namespace and accepts only exact `vMAJOR.MINOR.PATCH.yaml` filenames.
- CLI fixtures now parameterize package, release-tag, metadata-file, archive, and release-index identity. Current package tests remain `v0.4.0`; the four official older skills-only cases use `v0.3.3` and its compatibility marker.
- After code-review R2 reproduced `UBR-PRFG-CR2-001`, lifecycle authority resolution moved ahead of branch acceptance: a stage-owned record now rejects the legacy status form, a genuinely non-stage-owned record retains it, and the direct before-pointer case is explicit.

## Validation

- `python scripts/test-boundary-first-validation.py BoundaryFirstStructuralTests.test_stage_owned_marker_requires_matching_lifecycle_contract` — expected pre-fix TypeError, then pass.
- `python scripts/test-select-validation.py ValidationSelectionTests.test_malformed_release_profile_paths_require_release_version` — expected pre-fix three failures, then pass.
- Focused four historical opencode tests — expected pre-fix `v0.4.0 != v0.3.3`, then pass, 4 tests.
- `python scripts/test-boundary-first-validation.py` — pass, 64 tests.
- `python scripts/test-select-validation.py` — pass, exit 0, 150 tests.
- `npm test --prefix packages/rigorloop` — pass, 117 tests.
- `python scripts/validate-boundary-first.py --check` — pass for active `v0.4.0` and rollback `v0.3.6`.
- `python scripts/test-npm-package-publication.py` — pass, 6 tests.
- `python scripts/validate-release.py --recorded-source-auto --version v0.4.0` — pass from recorded source `c7b0babe6e8c91655c2b98f4092197eef5fabc69`.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-06-usability-first-boundary-release/change.yaml` — pass.
- `python scripts/validate-review-artifacts.py docs/changes/2026-08-06-usability-first-boundary-release --mode structure` — pass, 32 reviews and 32 findings.
- Explicit selector inspection — pass; selected `boundary_first.validate`, `boundary_first.regression`, `artifact_lifecycle.validate`, `selector.regression`, `rigorloop_cli.test`, and `npm_package_publication.test`; no broad smoke required for the implementation slice.
- Selected artifact-lifecycle validation — pass for 9 artifacts with three pre-existing merge-language warnings.
- `git diff --check` — pass.
- R2 reciprocal-authority regression — expected pre-fix failure because the stage-owned status form returned no issue; post-fix targeted T24 passes.
- Post-R2 `python scripts/test-boundary-first-validation.py` — pass, 64 tests including owner-form, stage-owned status rejection, non-stage-owned status retention, before-pointer, missing/different authority, outside-section, and duplicate coverage.
- Post-R2 path-aware feature/test-spec validation — pass for the approved usability-first spec pair.

## Aligned-surface audit

- Governing feature spec and proof map were approved in spec-review R5 and test-spec-review R4.
- The plan and architecture remain unaffected: this correction enforces the approved metadata authority, selector grammar, and historical fixture identity without changing components, release flow, milestones, or public interfaces.
- Current `v0.4.0` package behavior, immutable `v0.3.6` rollback metadata, generated artifacts, and release-owned publication mechanisms remain unchanged.

## Handoff

The correction is ready for independent code-review. This evidence does not claim review approval, verification, branch readiness, PR readiness, publication, or release completion.
