# Code Review M2 R2: Adapter Metadata Source Commit Validation

Review ID: code-review-m2-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review skill
Target: commit `2c51445`
Status: clean-with-notes
Review date: 2026-05-13

## Scope

Reviewed the M2 rerun fix for `PAAM-M2-CR1` against the approved spec, test spec, active plan, prior code-review finding, review-resolution record, and actual implementation diff.

## Review Inputs

- Diff range: `367d622..2c51445`
- Spec: `specs/public-adapter-artifact-migration-examples-concise-skill-release.md`
- Test spec: `specs/public-adapter-artifact-migration-examples-concise-skill-release.test.md`
- Plan milestone: `docs/plans/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release.md` M2
- Prior review: `docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/code-review-m2-r1.md`
- Review resolution: `docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/review-resolution.md`
- Validation evidence inspected:
  - `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_adapter_artifact_metadata_validation_accepts_schema_and_optional_combined AdapterDistributionTests.test_adapter_artifact_metadata_validation_rejects_bad_results_checksums_and_source_commit_mismatch AdapterDistributionTests.test_v0_1_2_release_validation_checks_archives_and_artifact_metadata AdapterDistributionTests.test_validate_release_cli_passes_changed_surface_inputs AdapterDistributionTests.test_release_verify_script_supports_v0_1_2_archive_metadata_gate`
  - `python scripts/test-adapter-distribution.py`
  - `tmpdir=$(mktemp -d); python scripts/build-adapters.py --version v0.1.2 --output-dir "$tmpdir" >/dev/null; python scripts/validate-release.py --version v0.1.2 --release-output-dir "$tmpdir" --release-commit 5514ef14ce5f310787f464ea78bd777838cb5537`
  - `tmpdir=$(mktemp -d); python scripts/build-adapters.py --version v0.1.2 --output-dir "$tmpdir" >/dev/null; python scripts/validate-release.py --version v0.1.2 --release-output-dir "$tmpdir" --release-commit aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` failed with `release.source_commit mismatch`.
  - `RELEASE_VERIFY_DRY_RUN=1 RELEASE_OUTPUT_DIR=release-output RELEASE_COMMIT=5514ef14ce5f310787f464ea78bd777838cb5537 bash scripts/release-verify.sh v0.1.2`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/change.yaml`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
  - `git diff --check --`

## Diff Summary

The rerun fix adds `release_commit` as an explicit adapter artifact metadata validation input, compares it to `release.source_commit`, threads that input through `validate_release_output`, `scripts/validate-release.py --release-commit`, and the `v0.1.2` release verification path, and adds a negative regression test for source-commit mismatch. The lifecycle records now close `PAAM-M2-CR1` and document the approved `v0.1.2` policy exception that the metadata source commit is the archive source commit `5514ef14ce5f310787f464ea78bd777838cb5537`.

## Findings

No blocking or required-change findings.

## Checklist Coverage

| Check | Result | Notes |
|---|---|---|
| Spec alignment | pass | Spec edge case 9 allows a reviewed policy exception; the resolution record documents that `v0.1.2` metadata names the archive source commit, and validation now rejects mismatches against the supplied commit. |
| Test coverage | pass | The focused regression test now covers source-commit mismatch, and release validation tests pass the accepted source commit explicitly. |
| Edge cases | pass | The named wrong-source-commit failure path is directly exercised with an intentionally wrong commit and fails with `release.source_commit mismatch`. |
| Error handling | pass | Invalid SHA shape still fails, mismatched valid SHA now fails, and release validation also marks `validation.adapter_artifact_metadata` inconsistent when metadata validation fails. |
| Architecture boundaries | pass | Validation remains in repo-owned scripts, uses generated release output, and does not introduce a second metadata source. |
| Compatibility | pass | The fix does not remove tracked `dist/adapters/**/skills` and preserves the `0.1.1` tracked adapter compatibility matrix for `v0.1.2`. |
| Security/privacy | pass | The diff records public commit IDs and archive metadata only; no secrets, credentials, or machine-local private paths are introduced. |
| Derived artifact currency | pass | The adapter artifact metadata comment, review-resolution, plan, and release validation command all agree on the archive source commit policy. |
| Unrelated changes | pass | The diff is scoped to source-commit validation, tests, release-gate wiring, and required lifecycle evidence. |
| Validation evidence | pass | Focused tests, full adapter-distribution tests, accepted and wrong source-commit release validation, dry-run release gate, lifecycle validation, and whitespace checks are recorded. |

## No-Finding Rationale

No material findings were found because the exact failure from `PAAM-M2-CR1` is now covered at the metadata validator boundary, propagated through release validation and the release gate, and proved by both positive and negative validation evidence. The approved policy exception is recorded in tracked review-resolution evidence and the active plan.

## Residual Risks

- `v0.1.2` release validation must pass `RELEASE_COMMIT=5514ef14ce5f310787f464ea78bd777838cb5537` when validating the tracked pre-metadata archive source commit policy.
- M3-M5 remain open and still own install-contract documentation, conditional example/skill cleanup, token-cost evidence, and final release readiness.

## Recommended Next Stage

Close M2 and proceed to `implement` M3.
