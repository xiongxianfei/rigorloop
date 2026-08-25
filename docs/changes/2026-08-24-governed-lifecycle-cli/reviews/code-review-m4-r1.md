# Code Review M4 R1: Evidence and Settlement Operations

Review ID: code-review-m4-r1
Stage: code-review
Round: r1
Reviewer: Codex same-context direct reviewer
Target: M4 commits `99f96dcc..6d271e3c`
Reviewed milestone: M4
Reviewed artifact: commit `6d271e3c`
Review date: 2026-08-24
Status: clean-with-notes
Review status: clean-with-notes
Material findings: none
Recording status: recorded
Governing artifacts: `specs/governed-lifecycle-cli.md`; `docs/adr/ADR-20260824-governed-lifecycle-cli-transaction-boundary.md`; `docs/plans/2026-08-24-governed-lifecycle-cli.md`; `specs/governed-lifecycle-cli.test.md`
Formal criteria: direct-code-review-v1; evidence-authority-review-v1

## Result

- Skill: code-review
- Status: completed
- Open blockers: none within M4
- Next stage: implement M5
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Reviewed milestone: M4
- Milestone closeout: closed by direct user continuation
- Remaining implementation milestones: M5, M6, M7
- Required review-resolution: no
- Verify readiness: not-claimed

## Review

Requests cannot set lifecycle state directly. Review, validation, and resolution registration require existing stage-owned evidence that names exact current subjects and closed semantic fields. Registrations retain hashes inside `change.yaml`, and settlement rechecks artifact, evidence, log, findings, and authority before deriving state. Stale envelopes fail before mutation, current exact repeats are idempotent, and dry runs leave bytes unchanged.

The review challenged multi-occurrence review logs and corrected the initial whole-ledger finding lookup; validation now scopes to the exact detailed entry or clean-receipt row. The final package suite passes 152 tests, with 103 review-validator and 170 artifact-lifecycle-validator tests also passing.

## Limitation note

This same-context direct review follows the user's recorded instruction and makes no independent-review or second-review claim.
