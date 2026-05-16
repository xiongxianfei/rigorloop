# Code Review R6 - M4 CR5-F1 Rerun

Review ID: code-review-r6
Stage: code-review
Round: 6
Reviewer: Codex code-review
Target: M4 release workflow and publication mode gates rerun after `CR5-F1`
Reviewed artifact: scripts/adapter_distribution.py; scripts/validate-release.py; scripts/test-adapter-distribution.py; docs/plans/2026-05-16-rigorloop-npm-publication.md; docs/changes/2026-05-16-first-public-npm-release/change.yaml; docs/changes/2026-05-16-first-public-npm-release/review-resolution.md
Review date: 2026-05-16
Recording status: recorded
Status: clean-with-notes

## Result

- Skill: code-review
- Status: completed
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-16-first-public-npm-release/reviews/code-review-r6.md`
- Review log: `docs/changes/2026-05-16-first-public-npm-release/review-log.md`
- Review resolution: not-required
- Artifacts changed: review record and lifecycle handoff only
- Open blockers: none for M4
- Next stage: implement M5 Documentation, Follow-Up State, And Final Local Readiness
- Reviewed milestone: M4. Release Workflow And Publication Mode Gates
- Milestone closeout: M4 can close
- Remaining implementation milestones: M5
- Required review-resolution: none
- Finding IDs: none
- Verify readiness: not ready; M5 remains open and publication evidence is not final

## Review status

clean-with-notes

## Review inputs

- Diff/review surface: `scripts/adapter_distribution.py`, `scripts/validate-release.py`, `scripts/test-adapter-distribution.py`, `.github/workflows/release.yml`, and lifecycle artifacts for M4.
- Governing artifacts: `specs/rigorloop-npm-publication.md`, `specs/rigorloop-npm-publication.test.md`, `docs/adr/ADR-20260516-rigorloop-npm-publication.md`, and `docs/plans/2026-05-16-rigorloop-npm-publication.md`.
- Prior finding: `CR5-F1` in `code-review-r5`.
- Validation evidence: plan validation notes and `change.yaml` entries for focused CR5-F1 tests, full adapter distribution tests, selector tests, `release-verify.sh v0.1.4`, artifact lifecycle validation, selected CI, review artifact validation, and diff check.

## Diff summary

The rerun fix adds byte-level bootstrap tarball identity validation. `scripts/adapter_distribution.py` computes the actual SHA-256 of the named packed tarball when `npm_tarball_root` is supplied and rejects mismatches or missing tarball files. `scripts/validate-release.py` exposes this as `--npm-tarball-root`. `scripts/test-adapter-distribution.py` adds direct fixtures for malformed SHA, mismatched SHA, missing tarball file, and matching tarball success.

The release workflow gating added earlier in M4 remains unchanged: future trusted-publishing releases use the existing `release.yml` publish job, while `v0.1.4` bootstrap is skipped by workflow publication.

## Findings

No blocking or required-change findings.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | R61c and SP8 require bootstrap publication to block when tarball SHA-256 differs from recorded evidence. `_validate_bootstrap_tarball_identity` now compares `tarball.sha256` with `_sha256_file(tarball_path)` when a tarball root is provided. |
| Test coverage | pass | TNP-011 requires a mismatched tarball SHA negative fixture. `test_v0_1_4_release_validation_rejects_mismatched_bootstrap_tarball_sha` records one SHA and writes different tarball bytes; matching and missing-file fixtures are also present. |
| Edge cases | pass | Direct tests cover malformed/missing SHA, mismatched SHA, missing tarball file, matching tarball bytes, and CLI argument forwarding for `--npm-tarball-root`. |
| Error handling | pass | The validator reports malformed SHA before byte comparison, missing tarball file by filename, and mismatch with recorded and actual hashes. Pending-publication evidence remains non-blocking when no tarball root is supplied. |
| Architecture boundaries | pass | The change stays in release evidence validation and release CLI surfaces; it does not alter runtime adapter install trust boundaries or npm package contents. |
| Compatibility | pass | `validate_release_output` receives an optional parameter with a default of `None`; existing callers remain compatible. |
| Security/privacy | pass | Bootstrap mode no longer accepts a well-formed but wrong SHA as artifact identity proof. No tokens, `.npmrc`, private keys, or package secret surfaces were introduced. |
| Derived artifact currency | pass | No generated public adapter skill bodies were edited for this rerun. Release validation still builds and validates v0.1.4 adapter archives. |
| Unrelated changes | pass | The CR5-F1 rerun diff is scoped to release evidence validation, release CLI argument plumbing, tests, and lifecycle state. |
| Validation evidence | pass | Recorded commands include focused CR5-F1 tests, full `python scripts/test-adapter-distribution.py`, `python scripts/test-select-validation.py`, `bash scripts/release-verify.sh v0.1.4`, selected CI, lifecycle validation, review artifact validation, and `git diff --check`. |

## No-finding rationale

The prior blocker was that a well-formed but incorrect `tarball.sha256` could pass bootstrap publication evidence validation. The rerun adds direct byte comparison against the tarball named in evidence and proves the mismatch path with a deterministic fixture. The fix also keeps the approved scaffold behavior intact because byte comparison is only attempted when the validator is given a tarball root.

## Residual risks

- CI cannot prove npm account settings, maintainer 2FA, or actual registry publication before M6b. Those remain evidence and publication-execution responsibilities, not M4 implementation blockers.
- M5 remains open, so the initiative is not ready for final verify, PR handoff, or publication.
