# M3 Publication Parity

## Result

## Core result

- Skill: implement
- Status: implemented
- Completed scope: Added explicit canonical-build and supported-adapter parity proof for both `proposal` and `proposal-review`, while preserving the published v0.4.1 release identity.
- Artifacts changed: `scripts/test-build-skills.py` and `scripts/test-adapter-distribution.py`.
- Tests added or updated: Local skill build now compares every file in both proposal-stage packages with canonical source; adapter distribution now builds temporary archives and clean-installs both packages for Codex, Claude, and opencode.
- Validation performed: `python scripts/test-build-skills.py`; `python scripts/build-skills.py --check`; `python scripts/test-adapter-distribution.py`; `python scripts/validate-release.py --version v0.4.1 --recorded-source-auto`; `git diff --check`.
- Validation result: Passed: 8 local-build tests, 152 adapter-distribution tests, and recorded-source validation for the immutable published v0.4.1 evidence. The initial current-source release wrapper exposed the historical/current identity conflict; Delivery Review R3 reassigned current temporary parity to CMD-07 and historical validation to CMD-08, and the published metadata changes were reverted.
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
- Public release behavior and v0.4.1 evidence: unchanged and validated through the recorded-source profile.
