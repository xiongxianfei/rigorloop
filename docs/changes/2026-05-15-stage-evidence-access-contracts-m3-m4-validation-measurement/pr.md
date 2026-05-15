# PR: Stage evidence access M3/M4 validation and measurement

## Summary

- Add the M3/M4 lifecycle slice for stage evidence access contract follow-through.
- Record that M3 found the existing concept-based static checks sufficient, so no new validator assertions were needed.
- Record the M4 static skill token measurement as unchanged from the M2 merged baseline: 23 skills, 235521 bytes, and 58868 estimated tokens.
- Close stale M2 lifecycle state after PR #60 merged with hosted CI success.

## Why

- The accepted stage evidence access contract work split execution into M1/M2 guidance changes, then M3 static validation and M4 measurement.
- This PR completes the M3/M4 follow-through without reopening skill wording, adding runtime enforcement, creating hard token gates, or expanding into dynamic benchmarks.

## Spec / plan / architecture

- Proposal: `docs/proposals/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor.md`
- Spec: `specs/stage-evidence-access-contracts-for-cost-bounded-rigor.md`
- Test spec: `specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md`
- Architecture / ADRs: not required; this is validation and measurement evidence only.
- Plan: `docs/plans/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement.md`
- Explain-change: `docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/explain-change.md`
- Verify: `docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/verify-report.md`

## What changed

- Added the active M3/M4 plan and change metadata.
- Updated the active test spec with M3/M4 proof cases `T15` and `T16`.
- Recorded plan-review, code-review M3, and code-review M4 evidence.
- Recorded explain-change and final local verify evidence.
- Updated `docs/plan.md` and the M2 plan/change metadata to keep lifecycle state synchronized.

## Tests and verification

- [x] `python scripts/select-validation.py --mode explicit ...` - passed; `broad_smoke_required: false`
- [x] `python scripts/test-skill-validator.py` - passed
- [x] `python scripts/measure-skill-tokens.py` - passed; 23 skills, 235521 bytes, 58868 estimated tokens
- [x] `python scripts/validate-skills.py` - passed
- [x] `python scripts/test-build-skills.py` - passed
- [x] `python scripts/build-skills.py --check` - passed
- [x] `python scripts/validate-review-artifacts.py docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/` - passed
- [x] `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` - passed
- [x] `python scripts/test-change-metadata-validator.py` - passed
- [x] `python scripts/validate-change-metadata.py docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/change.yaml docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml` - passed
- [x] `git diff --check -- ...` - passed
- [ ] CI - pending; hosted CI for this branch has not been observed yet.

## Requirement coverage

- `R30` -> `T6`, `T15` -> M3 audit records existing concept checks as sufficient; `test-skill-validator.py` passed.
- `R31` -> `T6`, `T15` -> M3 audit maps evidence access, default evidence, conditional evidence, reason recording, bounded evidence, and full-file escape concepts to existing checks.
- `R32` -> `T4`, `T9`, `T14`, `T15`, `T16` -> diff stays in lifecycle/test-spec/review/explain/verify evidence and does not add runtime enforcement, hard token gates, release changes, adapter changes, generated-output source changes, or dynamic benchmarks.
- `R33` -> `T10`, `T16` -> static measurement is recorded as diagnostic and unchanged from the M2 baseline.
- `R34` -> `T9`, `T11`, `T15`, `T16` -> formal review and validation evidence remains intact; no material findings were recorded.

## Review resolution summary

- Accepted: 0
- Rejected: 0
- Deferred: 0
- Partially accepted: 0
- Needs decision: 0
- Review-resolution: not required; plan-review, code-review M3, and code-review M4 recorded no material findings.

## Risks and rollback

- Risk: static token measurement does not prove dynamic prompt or command-output savings.
- Mitigation: dynamic benchmarks remain deferred until a later approved plan/test spec requires them.
- Rollback: revert the M3/M4 lifecycle and test-spec follow-through commits; no runtime, release, adapter, or generated-output behavior is changed.

## Reviewer notes

- The key review question is whether the no-change M3 validator rationale is sufficient and whether the M4 measurement is correctly treated as diagnostic-only.
- Hosted CI is pending after PR creation; do not treat local verification as hosted CI evidence.

## Follow-ups

- None required for this PR.
- Future approved work may extend evidence-access concept checks if more skills adopt the contract.
