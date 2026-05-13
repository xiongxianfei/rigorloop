# Public Adapter Artifact Migration Review Resolution

## Scope

This record tracks material findings from formal lifecycle reviews for the public adapter artifact migration, examples relocation, and concise skill release change.

Closeout status: closed
Review closeout: code-review-m2-r1

## Resolution Entries

### proposal-review-r1

No material findings.

### spec-review-r1

No material findings.

### architecture-review-r1

No material findings.

### plan-review-r1

Review closeout: closed

#### PR-001

Finding ID: PR-001
Disposition: accepted
Status: resolved
Owner: plan author
Owning stage: plan
Chosen action: Revise M5 so the token-cost benchmark validation command uses an executable `scripts/run-token-cost-benchmarks.py` invocation, or explicitly add a benchmark-runner CLI change and tests to the implementation scope.
Rationale: The current plan names `--version`, but the runner currently exposes `--release`. A non-executable final validation command would create a predictable late release-readiness failure.
Validation target: M5 names an executable token benchmark command using the public adapter release output or generated temporary public adapter output, and a plan-review rerun confirms the validation command is reliable.
Validation evidence: M5 updated to use `python scripts/run-token-cost-benchmarks.py --release v0.1.2 --suite benchmarks/token-cost/manifest.yaml --tool codex --output-dir <run-output-dir> --skill-source <public-adapter-skill-source>`; `plan-review-r2` approved the revised plan with no material findings.

### plan-review-r2

No material findings.

### code-review-m1-r1

No material findings.

### code-review-m2-r1

Review closeout: closed

#### PAAM-M2-CR1

Finding ID: PAAM-M2-CR1
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M2 review-resolution
Chosen action: Added direct release-source commit validation to adapter artifact metadata validation, exposed `--release-commit` on `scripts/validate-release.py`, passed the release commit through `scripts/release-verify.sh`, and added a negative regression test for source-commit mismatch. Recorded the approved `v0.1.2` policy exception that `release.source_commit` names the archive source commit `5514ef14ce5f310787f464ea78bd777838cb5537` rather than the later commit that tracks the metadata evidence.
Rationale: The archived adapter payload is generated from a source commit that necessarily predates the tracked metadata file describing the archive checksums. Direct validation now compares metadata with the release/source commit input supplied to validation, so mismatches fail unless validation intentionally uses the approved archive-source commit for this release.
Required outcome: Release validation must reject adapter artifact metadata whose `release.source_commit` does not match the release commit under validation, unless a reviewed release policy explicitly permits that mismatch.
Safe resolution: Add direct validation for `release.source_commit` against the release commit input used by validation, add a negative regression test for source-commit mismatch, and either update the metadata to the accepted source commit model or record an approved policy exception if the metadata intentionally points to a pre-metadata archive source commit.
Validation target: Source-commit mismatch regression fails before the fix, passes after the fix, and `python scripts/validate-release.py --version v0.1.2 --release-output-dir <release-output-dir> --release-commit <source-commit>` rejects mismatched source commits.
Validation evidence: `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_adapter_artifact_metadata_validation_accepts_schema_and_optional_combined AdapterDistributionTests.test_adapter_artifact_metadata_validation_rejects_bad_results_checksums_and_source_commit_mismatch AdapterDistributionTests.test_v0_1_2_release_validation_checks_archives_and_artifact_metadata AdapterDistributionTests.test_validate_release_cli_passes_changed_surface_inputs AdapterDistributionTests.test_release_verify_script_supports_v0_1_2_archive_metadata_gate` initially failed before CLI and release-gate plumbing, then passed after the fix.

### code-review-m2-r2

No material findings.

### code-review-m3-r1

No material findings.

### code-review-m4-r1

No material findings.

### code-review-m5-r1

No material findings.
