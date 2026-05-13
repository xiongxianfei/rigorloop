# Code Review M2 R1: Adapter Artifact Release Metadata

Review ID: code-review-m2-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: commit `a4efaca`
Status: changes-requested
Review date: 2026-05-13

## Scope

Reviewed M2 adapter artifact metadata and checksum validation against the approved spec, test spec, architecture, active plan, and actual implementation diff.

## Review Inputs

- Diff range: `5514ef1..a4efaca`
- Spec: `specs/public-adapter-artifact-migration-examples-concise-skill-release.md`
- Test spec: `specs/public-adapter-artifact-migration-examples-concise-skill-release.test.md`
- Architecture: `docs/architecture/system/architecture.md`
- Plan milestone: `docs/plans/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release.md` M2
- Change metadata and review artifacts: `docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/`
- Validation evidence inspected:
  - `python scripts/test-adapter-distribution.py` passed with 85 tests in the implementation evidence.
  - `tmpdir=$(mktemp -d); python scripts/build-adapters.py --version v0.1.2 --output-dir "$tmpdir"; python scripts/validate-release.py --version v0.1.2 --release-output-dir "$tmpdir"` passed during implementation and again during review.
  - `RELEASE_VERIFY_DRY_RUN=1 RELEASE_OUTPUT_DIR=release-output bash scripts/release-verify.sh v0.1.2` passed during implementation.
  - `git diff --check --` passed during implementation.

## Diff Summary

M2 adds adapter artifact metadata parsing and checksum validation, tracks `docs/reports/adapter-artifacts/releases/v0.1.2.yaml`, wires `validate-release.py --release-output-dir`, adds `v0.1.2` support to `release-verify.sh`, and creates minimal `docs/releases/v0.1.2/` metadata and notes so release validation can check generated archives and adapter artifact metadata.

## Findings

### PAAM-M2-CR1 - Source commit mismatch is accepted instead of rejected

Finding ID: PAAM-M2-CR1
Severity: major
Location: `scripts/adapter_distribution.py`; `docs/reports/adapter-artifacts/releases/v0.1.2.yaml`
Evidence: `validate_adapter_artifact_metadata` only validates that `release.source_commit` matches a SHA-shaped regex at `scripts/adapter_distribution.py:2064`, and never compares it to the release commit under validation. The tracked metadata records `source_commit: 5514ef14ce5f310787f464ea78bd777838cb5537` at `docs/reports/adapter-artifacts/releases/v0.1.2.yaml:5`, while the reviewed M2 commit is `a4efaca61f7c84a8f1fc7c2976bf7428a07e7d53`. Despite that mismatch, `python scripts/validate-release.py --version v0.1.2 --release-output-dir <tmpdir>` passed during review.
Required outcome: Release validation must reject adapter artifact metadata whose `release.source_commit` does not match the release commit under validation, unless a reviewed release policy explicitly permits that mismatch.
Safe resolution: Add direct validation for `release.source_commit` against the release commit input used by validation, add a negative regression test for source-commit mismatch, and either update the metadata to the accepted source commit model or record an approved policy exception if the metadata intentionally points to a pre-metadata archive source commit.

## Checklist Coverage

| Check | Result | Notes |
|---|---|---|
| Spec alignment | block | T5 and spec edge case 9 require source-commit mismatch rejection; the implementation accepts a mismatch. |
| Test coverage | concern | New tests cover schema, required adapters, bad results, checksum mismatch, missing metadata, CLI routing, and release gate invocation, but not the required wrong-source-commit negative case. |
| Edge cases | block | Spec edge case 9 is not implemented. |
| Error handling | pass | Missing metadata, bad artifact result, checksum mismatch, missing archives, and missing release-output directory are handled. |
| Architecture boundaries | pass | Validation remains in repo-owned scripts and uses generated release output instead of committed archives. |
| Compatibility | pass | M2 keeps tracked `dist/adapters/**/skills` on the compatibility path and validates tracked adapter output with the `0.1.1` support matrix. |
| Security/privacy | pass | No secrets or local private paths were found in the reviewed diff. |
| Derived artifact currency | concern | Archive checksum evidence validates, but source-commit evidence is not bound to the release commit. |
| Unrelated changes | pass | The diff is scoped to M2 validation, metadata, release gate wiring, minimal release evidence, and lifecycle state. |
| Validation evidence | concern | The recorded validation commands are relevant, but they do not cover the required source-commit mismatch failure. |

## No-Finding Rationale

Not applicable. The review found one material required-change finding.

## Residual Risks

- M3 still owns refinement of install-contract docs and release-note wording.
- M5 still owns token-cost evidence and final release readiness.

## Recommended Next Stage

Enter `review-resolution` for `PAAM-M2-CR1`, then return M2 to `code-review` after the fix and targeted validation pass.
