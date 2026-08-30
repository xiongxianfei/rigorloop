# M3 Publication Parity

## Result

## Core result

- Skill: implement
- Status: implemented
- Completed scope: Added explicit canonical-build and supported-adapter parity proof for both `proposal` and `proposal-review`, then synchronized the existing v0.4.1 release metadata with current generated archives.
- Artifacts changed: `scripts/test-build-skills.py`, `scripts/test-adapter-distribution.py`, `packages/rigorloop/dist/metadata/adapter-artifacts-v0.4.1.json`, `packages/rigorloop/dist/metadata/releases.json`, `packages/rigorloop/test/cli.test.js`, and `docs/reports/adapter-artifacts/releases/v0.4.1.yaml`.
- Tests added or updated: Local skill build now compares every file in both proposal-stage packages with canonical source; adapter distribution now builds archives and clean-installs both packages for Codex, Claude, and opencode; the existing package metadata mapping expectation now uses the regenerated v0.4.1 tree identity.
- Validation performed: `python scripts/test-build-skills.py`; `python scripts/build-skills.py --check`; `python scripts/test-adapter-distribution.py`; `python scripts/test-npm-package-publication.py`; `python scripts/validate-release.py --version v0.4.1 --release-output-dir <temporary-release-output> --release-commit a9f1220040acd590f50ff0ed2d50f72d0990bcf0`; `bash scripts/release-verify.sh v0.4.1`; `npm test --prefix packages/rigorloop`.
- Validation result: Passed: 8 local-build tests, 152 adapter-distribution tests, 7 packed-package tests, 298 CLI/package tests with 2 skipped, direct Gate C validation, and the complete release wrapper. The first wrapper run correctly blocked on stale v0.4.1 archive metadata; the metadata, index digest, adapter report, and package mapping expectation were synchronized before the successful reruns.
- Open blockers: None.
- Next stage: code-review
- Claim limitations: This evidence does not claim clean review, final verification, branch readiness, PR readiness, or lifecycle closeout.

## Planned milestone

- Change ID: `2026-08-30-simplify-rigorloop-proposal-contract`
- Plan identity: `docs/plans/2026-08-30-simplify-rigorloop-proposal-contract.md`, approved in `delivery-review-r2`.
- Milestone ID: M3
- Milestone state: implementing
- Baseline or change-pack status: Current approved Design and Delivery packages; M1 and M2 are closed.
- Milestone validation evidence: This file.
- Commit status: Included in the M3 implementation commit.
- Code-review handoff: Ready after commit and lifecycle state-sync validation.

## Surface audit

- Canonical `skills/proposal/` and `skills/proposal-review/`: unchanged in M3 because M1 owns their approved content.
- Generated skill mirrors and adapter archives: temporary derived output only; no generated package bodies or repository-local installed copies are tracked.
- Existing missing/stale resource behavior: unchanged and covered by the pre-existing negative build and adapter tests.
- Public release behavior: unchanged; only the current v0.4.1 archive identities and inventory projection were refreshed to match canonical generation.
