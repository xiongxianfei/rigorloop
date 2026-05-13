# Code Review M3 R1: Adapter Install Contract and Release Notes

Review ID: code-review-m3-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: commit `968b3ec`
Reviewed artifact: commit `968b3ec`
Status: clean-with-notes
Review date: 2026-05-13
Recording status: recorded

## Scope

Reviewed M3 implementation for the `v0.1.2` adapter install contract, release-note compatibility wording, release-note validation, and `docs/workflows.md` adapter artifact metadata location.

## Review Inputs

- Diff target: `968b3ec` (`M3: document adapter archive install contract`)
- Plan milestone: `docs/plans/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release.md` M3
- Spec requirements: `R3`-`R6`, `R43`-`R51`, `R57`, `R60`, `R70`-`R75`, `R82`-`R85`
- Test spec checks: `T6`, `T7`, `T10`
- Changed implementation surfaces: `dist/adapters/README.md`, `docs/releases/v0.1.2/release-notes.md`, `docs/workflows.md`, `scripts/adapter_distribution.py`, `scripts/test-adapter-distribution.py`

## Validation Evidence Inspected

- `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_public_adapter_readme_documents_metadata_and_install_transition AdapterDistributionTests.test_v0_1_2_release_notes_document_archive_introduction_contract AdapterDistributionTests.test_v0_1_2_release_validation_rejects_notes_without_archives_or_compatibility AdapterDistributionTests.test_workflows_records_adapter_artifact_metadata_location AdapterDistributionTests.test_v0_1_2_release_validation_checks_archives_and_artifact_metadata` passed during this review.
- `tmpdir=$(mktemp -d); python scripts/build-adapters.py --version v0.1.2 --output-dir "$tmpdir" >/dev/null; python scripts/validate-release.py --version v0.1.2 --release-output-dir "$tmpdir" --release-commit 5514ef14ce5f310787f464ea78bd777838cb5537` passed during this review.
- M3 implementation recorded full `python scripts/test-adapter-distribution.py` passing with 88 tests.
- M3 implementation recorded `python scripts/build-adapters.py --version 0.1.1 --check`, `python scripts/validate-adapters.py --version 0.1.1`, dry-run `scripts/release-verify.sh v0.1.2`, and scoped `git diff --check` passing.

## Diff Summary

M3 updates the public adapter README to describe the compatibility-window repository-tree install path, forward release-archive install path, archive naming patterns, install roots, support matrix, metadata/checksum location, and `.codex/skills/` local-runtime boundary. It updates `v0.1.2` release notes with retained `dist/adapters/**/skills` compatibility, per-adapter archives, install roots, metadata location, and release gate command. It adds release-note consistency checks and regression tests, and records the adapter artifact metadata path in the workflow artifact-location table.

## Findings

No material findings.

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | README covers `R43`-`R51`; release notes cover `R82`-`R85`; workflow map covers `R70`-`R71`. |
| Test coverage | pass | Focused M3 tests cover README contract, release-note contract, negative release-note validation, and workflow metadata location. |
| Edge cases | pass | Negative test rejects `v0.1.2` release notes that omit archive and retained compatibility wording. |
| Error handling | pass | `validate_release_output` now reports missing per-adapter archives, retained compatibility wording, metadata path, and release-gate command for `v0.1.2` notes. |
| Architecture boundaries | pass | No generated adapter skill bodies or canonical skill text were hand-edited; release artifacts remain generated output. |
| Compatibility | pass | `v0.1.2` keeps tracked `dist/adapters/**/skills` available and documents archives as the forward install path. |
| Security/privacy | pass | No secrets, credential handling, or sensitive logging paths changed. |
| Derived artifact currency | pass | No canonical skill text changed, so generated adapter refresh was not required; tracked adapter compatibility validation remains on `0.1.1`. |
| Unrelated changes | pass | Diff is limited to install guidance, release notes, workflow map, validation checks, tests, and lifecycle bookkeeping. |
| Validation evidence | pass | Focused tests and release validation were rerun during review; M3 implementation also recorded full adapter distribution tests and dry-run release gate. |

## No-Finding Rationale

The implementation directly satisfies the M3 contract without removing tracked adapter skill bodies or broadening into M4 proof-pack movement or M5 token-cost evidence. The tests prove the user-facing install contract, release-note compatibility window, archive metadata location, and validation failure mode for missing archive/compatibility wording.

## Residual Risks

M4 still needs to settle the retained skill-validator proof pack and any bounded skill wording. M5 still needs token-cost evidence and final release-readiness validation. This review closes only M3.

## Recommended Next Stage

Proceed to `implement M4`.
