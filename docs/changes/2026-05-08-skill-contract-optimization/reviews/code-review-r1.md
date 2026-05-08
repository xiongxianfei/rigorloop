# Code Review R1: Skill Contract Optimization M1

Review ID: code-review-r1
Stage: code-review
Round: 1
Reviewer: Codex
Target: M1 commit `00def68`
Status: changes-requested

## Review inputs

- Diff range: `00def68`
- Review surface: M1 commit diff and tracked worktree after commit
- Tracked governing branch state: proposal, approved spec, active test spec, active plan, change metadata, and M1 implementation commit are tracked on `proposal/2026-05-08-skill-optimization`
- Spec: `specs/skill-contract.md`
- Test spec: `specs/skill-contract.test.md`
- Plan milestone: `docs/plans/2026-05-08-skill-contract-optimization.md` M1
- Architecture / ADR: none required by plan
- Validation evidence: plan validation notes for M1 plus reviewer reruns where recorded in chat

## Diff summary

M1 adds the accepted proposal, approved `specs/skill-contract.md`, active `specs/skill-contract.test.md`, the execution plan, change-local review artifacts, the plan-index entry, and passable static validator scaffolding in `scripts/test-skill-validator.py`.

## Findings

### CR1-F1 - First-slice test-spec coverage check is too weak for short skill names

Finding ID: CR1-F1
Severity: major

Evidence: `scripts/test-skill-validator.py` checks each first-slice skill against the test spec with `self.assertIn(skill_name, test_spec)`. For short skill names such as `pr`, this can pass from unrelated words such as `proposal`, so the assertion does not prove that the test spec names the first-slice skill. The same test already uses exact canonical paths for the spec and should use similarly bounded text for the test spec.

Required outcome: The validator must use exact, reviewable first-slice skill evidence for the test spec instead of bare substring checks.

Safe resolution path: Change the test-spec assertion to check bounded tokens such as backticked skill names from the T3 first-slice list, or another exact first-slice list representation, then rerun the M1 validation commands.

## Checklist coverage

| Check | Result | Notes |
|---|---|---|
| Spec alignment | concern | M1 mostly follows the approved spec source split and first-slice scope, but CR1-F1 leaves one validator assertion weaker than the static-proof intent. |
| Test coverage | concern | `python scripts/test-skill-validator.py` passes, but CR1-F1 shows a false-positive risk in the new first-slice scope check. |
| Edge cases | concern | The short-name edge case for `pr` is not handled by the bare substring assertion. |
| Error handling | pass | The M1 changes do not add runtime error paths. |
| Architecture boundaries | pass | No architecture artifact was required; canonical and generated boundaries remain documented. |
| Compatibility | pass | No standalone `ci-maintenance` or `review-resolution` skill is introduced. |
| Security/privacy | pass | No secrets, tokens, credentials, or private runtime values are present in the reviewed diff. |
| Generated output drift | pass | M1 intentionally does not edit canonical skills or generated outputs; generated-output refresh remains an M4 gate. |
| Unrelated changes | pass | The diff is scoped to the skill-contract initiative artifacts and validator scaffolding. |
| Validation evidence | concern | Targeted commands are recorded and pass, but the passing validator result is insufficient for CR1-F1 until the assertion is tightened. |

## No-finding rationale

No additional required-change findings were found because the M1 diff establishes the approved source-of-truth split, creates the active static test spec, keeps first-slice normalization scoped, preserves generated-output boundaries, and records targeted validation evidence.

## Recommended next stage

`review-resolution M1` for CR1-F1, then implement the accepted fix for M1 and rerun `code-review M1`.
