# Code Review M3 R1

Review ID: code-review-m3-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: M3 proposal scope preservation skill and validator updates
Status: changes-requested

## Review Inputs

- Commit: `317a04c M3: preserve initial proposal intent`
- Spec: `specs/token-cost-measurement-baseline-and-proposal-scope-preservation.md`
- Test spec: `specs/token-cost-measurement-baseline-and-proposal-scope-preservation.test.md`
- Plan: `docs/plans/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation.md`
- Change metadata: `docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml`
- Changed files:
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
  - `scripts/test-skill-validator.py`
  - `docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml`
  - `docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/explain-change.md`
  - `docs/plans/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation.md`

## Diff Summary

M3 adds scope-preservation guidance to proposal authoring, adds silent-narrowing checks to proposal-review, and adds narrow regression coverage in `scripts/test-skill-validator.py`.

Generated local skill mirrors and public adapter output are intentionally left stale until M4, which owns generated-output refresh.

## Findings

### TCSP-CR-M3-F1 - Proposal-review expected output still omits `changes-requested`

Finding ID: TCSP-CR-M3-F1
Severity: major

Evidence:

- `specs/token-cost-measurement-baseline-and-proposal-scope-preservation.md` requires proposal-review to return `changes-requested` when an initial goal disappears, a deferred goal lacks follow-up, a rejected goal lacks rationale, or narrowed scope lacks an explanation.
- `skills/proposal-review/SKILL.md` adds the new scope-preservation review rules and says to return `changes-requested` for those cases.
- The same skill's `Expected output` section still says `verdict: approve, revise, or rethink;` and does not name `changes-requested` as an allowed or required result.

Problem:

The implementation adds the required rule in one section while leaving the normal output contract on the older proposal-review verdict vocabulary. That makes the public skill internally inconsistent and can cause reviewers to return `revise` instead of the spec-required `changes-requested` for silent narrowing.

Required outcome:

The proposal-review skill's expected output must align with R8b-R8e and make `changes-requested` available for scope-preservation failures.

Safe resolution:

Update `skills/proposal-review/SKILL.md` so `Expected output` includes `changes-requested` for scope-preservation findings, either by changing the verdict/status vocabulary or by explicitly mapping silent-narrowing failures to `changes-requested`.

Update the static validator test so this alignment is covered directly, then rerun M3 validation.

## Checklist Coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | concern | R8b-R8e require `changes-requested`, but the proposal-review expected output omits it. |
| Test coverage | concern | The new static test checks the new scope-preservation section but does not check the expected-output vocabulary alignment. |
| Edge cases | concern | Silent narrowing is the named edge case; the output contract remains ambiguous for that failure. |
| Error handling | pass | No unsafe runtime error path is introduced by this documentation change. |
| Architecture boundaries | pass | The change stays inside canonical skill and validator surfaces; M4 owns generated output. |
| Compatibility | concern | Existing proposal-review verdict vocabulary remains visible and conflicts with the new required review result. |
| Security/privacy | pass | No secret, telemetry, or raw transcript exposure is added. |
| Derived artifact currency | concern | Generated skill mirrors and adapters are stale, but this is expected M4 scope and is not the blocking finding. |
| Unrelated changes | pass | The reviewed diff is scoped to M3 skill, validator, and milestone evidence updates. |
| Validation evidence | pass | Targeted validation passed; the finding is a manual contract-review issue not caught by current tests. |

## Validation Rerun

- `python scripts/test-skill-validator.py`: pass, 54 tests.
- `python scripts/validate-skills.py`: pass, validated 23 skill files.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml`: pass.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml --path docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/explain-change.md --path docs/plans/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation.md --path skills/proposal-review/SKILL.md --path skills/proposal/SKILL.md`: pass.
- `git diff --check -- HEAD~1..HEAD`: pass.
- `python scripts/build-skills.py --check`: expected fail, stale generated proposal/proposal-review mirrors; M4 owns refresh.
- `python scripts/build-adapters.py --version 0.1.1 --check`: expected fail, stale generated proposal/proposal-review adapter files; M4 owns refresh.

## Recommended Next Stage

Status: changes-requested.

Immediate next repository stage: review-resolution for M3.

Do not start M4 until TCSP-CR-M3-F1 is resolved, targeted validation passes, and M3 returns to code-review.
