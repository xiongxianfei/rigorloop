# Code Review M3 R1

Review ID: code-review-m3-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: M3. Release gate command integration and dry-run rehearsal evidence
Status: clean-with-notes
Reviewed artifact: docs/plans/2026-05-23-release-process-contract.md
Review date: 2026-05-23
Recording status: recorded

## Review inputs

- Diff/review surface:
  - `scripts/release-verify.sh`
  - `scripts/validate-release-ci.py`
  - `scripts/test-adapter-distribution.py`
  - `docs/changes/2026-05-23-release-process-contract/release-process-dry-run.md`
  - `docs/plans/2026-05-23-release-process-contract.md`
  - `docs/plan.md`
  - `docs/changes/2026-05-23-release-process-contract/change.yaml`
- Governing spec: `specs/release-process-contract.md`
- Test spec: `specs/release-process-contract.test.md`
- Plan milestone: `docs/plans/2026-05-23-release-process-contract.md#M3. Release gate command integration and dry-run rehearsal evidence`
- Validation evidence recorded by implement:
  - `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.5`
  - `python scripts/validate-release-ci.py --version v0.1.5`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/test-npm-package-publication.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-23-release-process-contract/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/release-process-contract.test.md --path docs/plans/2026-05-23-release-process-contract.md --path docs/plan.md --path docs/changes/2026-05-23-release-process-contract/change.yaml`
  - `git diff --check -- scripts/release-verify.sh scripts/validate-release.py scripts/validate-release-ci.py scripts/test-adapter-distribution.py scripts/test-npm-package-publication.py docs/plans/2026-05-23-release-process-contract.md docs/plan.md docs/changes/2026-05-23-release-process-contract`
- Reviewer spot checks:
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-23-release-process-contract`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-23-release-process-contract/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/release-process-contract.test.md --path docs/plans/2026-05-23-release-process-contract.md --path docs/plan.md --path docs/changes/2026-05-23-release-process-contract/change.yaml`

## Diff summary

M3 connects the standing release-process contract to the existing release gate without publishing anything:

- `scripts/release-verify.sh` now prints a standing release-process gate summary before the release checks, including generated-output currency, package preview/packed install smoke, publish-path policy, post-publish registry verification, and dry-run no-publish behavior.
- `scripts/test-adapter-distribution.py` adds a dry-run regression for `v0.1.5` proving the standing gate text, npm package check, adapter archive build, release metadata validation, and no-publish dry-run message.
- `scripts/validate-release-ci.py` now rebuilds historical adapter release archives from the source commit recorded in adapter artifact metadata before validating current release metadata, so later repository source changes do not invalidate historical checksum proof.
- `docs/changes/2026-05-23-release-process-contract/release-process-dry-run.md` records a non-release rehearsal and explicitly states that no package, tag, dist-tag, registry state, release evidence record, or public artifact changed.
- Plan and change metadata were updated to request M3 review and record validation evidence.

## Findings

No blocking or required-change findings.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | M3 addresses REL-R14 through REL-R27 by making the standing gate explicit and REL-R42 through REL-R56 by naming publish-path and registry-verification expectations without performing a publish. |
| Test coverage | pass | `scripts/test-adapter-distribution.py` directly tests the dry-run gate output and `validate-release-ci.py --version v0.1.5` recorded-source behavior. |
| Edge cases | pass | The dry-run evidence records that it is not release evidence for a real package version, and the CI wrapper covers the historical-source checksum edge case discovered during M3 validation. |
| Error handling | pass | `validate-release-ci.py` returns nonzero status on git archive, archive build, or release validation errors and prints validation diagnostics without masking failures. |
| Architecture boundaries | pass | The implementation reuses `scripts/release-verify.sh`, `scripts/validate-release-ci.py`, and `validate_release_output`; it does not add a new release CLI or a dedicated release-evidence validator. |
| Compatibility | pass | Existing release targets remain routed through the existing release verification script. Historical adapter validation is strengthened by using the recorded source commit for generated release archives. |
| Security/privacy | pass | The dry-run evidence redacts temp paths and release commit details, records no credentials, and the wrapper uses a temporary source tree with a path-containment check before extraction. |
| Derived artifact currency | pass | The dry-run output and tests name repository-owned generated-output checks, adapter archive generation, and release metadata validation as the proof path. |
| Unrelated changes | pass | The reviewed M3 diff is scoped to release gate output, CI release validation, regression tests, dry-run evidence, and lifecycle bookkeeping. |
| Validation evidence | pass | Implement recorded and reviewer spot-checked targeted validation, metadata validation, lifecycle validation, and patch hygiene. |

## No-finding rationale

The implementation satisfies the M3 plan slice without expanding into real publication or broad release automation. The release gate can now be rehearsed in dry-run mode with explicit standing-process boundaries, and the change-local dry-run evidence makes the publication boundary unambiguous. The `validate-release-ci.py` change is within M3 scope because the approved validation command for M3 must remain executable for `v0.1.5`; rebuilding historical adapter archives from the recorded source commit is the narrow fix that preserves historical release metadata rather than rewriting it.

## Residual risks

- `scripts/release-verify.sh` still names registry verification as a required post-publish boundary but does not execute live registry checks in dry-run mode. That is expected for M3 because no npm publish operation occurs in this milestone.
- M4 still needs lifecycle closeout, final rationale, and final verification after M3 review closes.

## Handoff

- Reviewed milestone: M3. Release gate command integration and dry-run rehearsal evidence
- Review status: clean-with-notes
- Milestone closeout: close M3 and hand off to implement M4
- Remaining implementation milestones: M4
- Required review-resolution: no
