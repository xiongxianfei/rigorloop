# Code Review M4 R1: Skill-Validator Fixture Retention

Review ID: code-review-m4-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: commit `bd4e4ce`
Reviewed artifact: commit `bd4e4ce`
Status: clean-with-notes
Review date: 2026-05-13
Recording status: recorded

## Scope

Reviewed M4 implementation for the skill-validator proof-pack settlement and bounded skill wording decision.

## Review Inputs

- Diff target: `bd4e4ce` (`M4: settle skill-validator example surface`)
- Plan milestone: `docs/plans/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release.md` M4
- Spec requirements: `R64`-`R75`
- Test spec checks: `T8`, `T9`, `T11`
- Changed implementation surfaces: `docs/changes/0001-skill-validator/README.md`, `scripts/test-skill-validator.py`, `scripts/test-artifact-lifecycle-validator.py`, plan/index/change metadata

## Validation Evidence Inspected

- `python scripts/test-skill-validator.py SkillValidatorFixtureTests.test_project_artifact_location_m1_retained_fixture_has_durable_rationale` passed during this review.
- `python scripts/test-artifact-lifecycle-validator.py ArtifactLifecycleValidatorFixtureTests.test_retained_skill_validator_fixture_readme_documents_non_active_status` passed during this review.
- `python scripts/test-select-validation.py ValidationSelectionTests.test_retained_skill_validator_fixture_rationale_has_deterministic_routing` passed during this review.
- `tmpdir=$(mktemp -d); python scripts/build-adapters.py --version v0.1.2 --output-dir "$tmpdir" >/dev/null; python scripts/validate-release.py --version v0.1.2 --release-output-dir "$tmpdir" --release-commit 5514ef14ce5f310787f464ea78bd777838cb5537` passed during this review.
- M4 implementation recorded full selector, artifact-lifecycle, and skill-validator test suites passing.

## Diff Summary

M4 keeps `docs/changes/0001-skill-validator/` in place and adds an explicit `v0.1.2` retention decision saying the retained fixture path does not block the archive-introduction release. The implementation strengthens existing tests so both the skill-validator static proof and artifact-lifecycle proof require the release non-blocking rationale. It does not move the proof pack, change selector routing, change canonical skill text, or regenerate public adapter output.

## Findings

No material findings.

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | Retention with explicit rationale satisfies `R68`; the rationale states retention does not block `v0.1.2`, satisfying `R69`. |
| Test coverage | pass | Focused tests require retained-fixture, historical proof-pack, non-active-root, future example target, and release non-blocking wording. |
| Edge cases | pass | The conditional move path is not taken; selector routing for the retained README remains deterministic. |
| Error handling | pass | Release validation was rerun with generated `v0.1.2` archive output and does not fail solely because the retained fixture remains. |
| Architecture boundaries | pass | The change preserves authored sources and avoids moving historical fixtures into examples without updating all references. |
| Compatibility | pass | Existing references to `docs/changes/0001-skill-validator/` remain valid during this release slice. |
| Security/privacy | pass | No secrets, credentials, auth behavior, or private data surfaces changed. |
| Derived artifact currency | pass | No canonical skill text changed, so generated adapter refresh was not required. |
| Unrelated changes | pass | Diff is limited to retained-fixture rationale, direct tests, and lifecycle bookkeeping. |
| Validation evidence | pass | Focused tests and release validation were rerun during review; implementation recorded full relevant suites. |

## No-Finding Rationale

The approved contract allowed either a safe move or retention with rationale. The diff chose the safer retained-fixture path after reference inventory and records why the old path remains. Direct tests prove the rationale exists, lifecycle routing remains stable, and release validation still passes with the retained path.

## Residual Risks

M5 still needs token-cost reports and final release-readiness evidence. This review closes only M4.

## Recommended Next Stage

Proceed to `implement M5`.
