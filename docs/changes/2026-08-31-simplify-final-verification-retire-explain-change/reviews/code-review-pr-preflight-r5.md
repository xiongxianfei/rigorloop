# Code Review PR Preflight R5: Workflow Automation Policy Fixture Drift

Review ID: code-review-pr-preflight-r5
Stage: code-review
Round: r5
Reviewer: Independent Codex code-review agent
Target: PR-preflight failure at `0dd08612`
Reviewed artifact: `scripts/test-workflow-automation-policy.py` against the v3-only policy projection in `scripts/workflow_automation_policy.py`
Review date: 2026-09-01
Status: changes-requested
Recording status: recorded
Material findings: FV-M6-CR3
Reviewed milestone: M6

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review, `review-invocation-code-review-pr-preflight-r5.yaml`, `review-log.md`, `review-resolution.md`, and the top review projection in `change.yaml`
- Open blockers: `FV-M6-CR3`
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: `FV-M6-CR3`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/reviews/code-review-pr-preflight-r5.md`
- Review log: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/review-log.md`
- Review resolution: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/review-resolution.md`
- Reviewed milestone: M6
- Milestone closeout: resolution-needed
- Remaining implementation milestones: none; this is a bounded current-policy test correction
- Required review-resolution: yes
- Finding IDs: `FV-M6-CR3`
- Verify readiness: not-claimed; the focused policy suite is failing

## Finding FV-M6-CR3

Finding ID: FV-M6-CR3
Severity: major
Location: `scripts/test-workflow-automation-policy.py:39-86,115-132,460-472`
Evidence: `python scripts/test-workflow-automation-policy.py` at `0dd08612` runs 20 tests and errors four times. Current tests reference removed `WorkflowStage.TEST_SPEC` and `WorkflowStage.EXPLAIN_CHANGE` members, still expect selector/evaluator success for `stage-owned-change-local-v2`, include Test Spec in the exact public sequence, and classify Explain Change as an internal final occurrence. Production correctly defines a nine-stage v3-only public sequence, omits both retired enum values, and rejects every non-v3 contract with `unknown_value`. An in-memory consolidated test-only probe replacing all four stale policy groups passed all 20 tests.
Required outcome: The policy tests must prove the exact v3-only public sequence, absence and constructor rejection of retired Test Spec and Explain Change values, final occurrence only for the current final holistic review and Verify policies, and fail-closed rejection of v1, v2, and unknown contracts by all three selectors plus `evaluate_transition`.
Safe resolution path: Modify only `scripts/test-workflow-automation-policy.py`: replace removed enum-member membership checks with value-set absence and `WorkflowStage(retired)` rejection; replace the v2-success test with a loop proving v1/v2/future rejection through `public_target_stages_for_contract`, `stage_policy_by_stage_for_contract`, `transition_rules_for_contract`, and `evaluate_transition`; assert the exact current nine-stage sequence without Test Spec; and remove Explain Change from internal occurrence expectations. Keep production policy code unchanged. Run the focused 20-test suite, scan the file again for retired enum/non-v3 success references, run structural validation, and return for targeted rereview.
needs-decision rationale: none; FV-R1, FV-R5, FV-R6, FV-R35, FV-R37, and the approved v3-only architecture determine the expected policy exactly.

## Consolidated sibling scan

The direct sibling scan found no additional correction target. `scripts/test-workflow-automation.py` uses v2 only in explicit `unknown_value` rejection tests, retains v1 only as historical state input, and uses historical explanation paths only to prove rejection from current verification basis. Validator and classification tests elsewhere intentionally exercise historical v1/v2 readability and are not current-policy selector tests. Editing them would erase required compatibility proof rather than consolidate this defect.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | Tests still encode retired stages and v2 execution despite the sole-current-v3 contract. |
| Test coverage | block | Four errors prevent the policy suite from exercising its remaining assertions. |
| Edge cases | concern | Unknown contracts are tested, but v1/v2 are incorrectly treated as executable in this file. |
| Error handling | pass | Production selector/evaluator functions fail closed on non-v3 values. |
| Architecture boundaries | pass | Production policy is coherent; the stale surface is test-only. |
| Compatibility | concern | Tests confuse historical readability with current policy execution. |
| Security/privacy | pass | No security, privacy, secret, or permission surface is involved. |
| Derived artifact currency | pass | No generated or published output is affected. |
| Unrelated changes | pass | The required correction is confined to one focused policy test file. |
| Validation evidence | block | The focused suite remains red until all stale policy groups are corrected together. |

## Validation performed

- `python scripts/test-workflow-automation-policy.py` — failed: 20 tests, four errors.
- Direct production inspection — current enums, stage tuple, selectors, and evaluator implement the approved v3-only policy and reject non-v3 contracts.
- Direct `rg` sibling scan — no additional stale current-policy success assertion; sibling v1/v2/explanation references are deliberate negative or historical tests.
- In-memory consolidated test-only probe — passed all 20 tests with production untouched.

No broad-smoke or PR-mode command was run.

## Handoff

This isolated review records FV-M6-CR3 before correction and performs no automatic downstream handoff. No owner decision is needed. Workflow owns lifecycle coordination; this review leaves routing unchanged.
