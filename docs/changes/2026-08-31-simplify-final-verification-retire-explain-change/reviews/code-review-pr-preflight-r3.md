# Code Review PR Preflight R3: Workflow Code-State Tail Fixture Drift

Review ID: code-review-pr-preflight-r3
Stage: code-review
Round: r3
Reviewer: Independent Codex code-review agent
Target: post-correction PR-preflight failure at `2e1bd067`
Reviewed artifact: `scripts/test-workflow-code-state.py` against the current v3 evidence-tail gate in `scripts/workflow_automation.py`
Review date: 2026-09-01
Status: changes-requested
Recording status: recorded
Material findings: FV-M6-CR2
Reviewed milestone: M6

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review, `review-invocation-code-review-pr-preflight-r3.yaml`, `review-log.md`, `review-resolution.md`, and the top review projection in `change.yaml`
- Open blockers: `FV-M6-CR2`
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: `FV-M6-CR2`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/reviews/code-review-pr-preflight-r3.md`
- Review log: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/review-log.md`
- Review resolution: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/review-resolution.md`
- Reviewed milestone: M6
- Milestone closeout: resolution-needed
- Remaining implementation milestones: none; this is another bounded current-test correction
- Required review-resolution: yes
- Finding IDs: `FV-M6-CR2`
- Verify readiness: not-claimed; the focused workflow-code-state suite is failing

## Finding FV-M6-CR2

Finding ID: FV-M6-CR2
Severity: major
Location: `scripts/test-workflow-code-state.py:27-55,213-289,292-329`
Evidence: `python scripts/test-workflow-code-state.py` at `2e1bd067` runs 19 tests and reports two failures plus one error. The v3 gate in `scripts/workflow_automation.py:406-423` correctly accepts only `tail_state == "review-recorded"` with a final-review revision and no explanation or handoff revision. The tests still expect the default gate to reject that valid v3 review-only tail and accept the historical review→explanation tail. The first failure masks one additional stale default-call expectation later in the same test. A temporary-archive probe changing only five gate assertions across those three tests passed all 19 tests.
Required outcome: The workflow-code-state tests must prove that a review-recorded, explanation-free tail is complete for v3 Verify, while a historical review→explanation snapshot remains readable but is rejected as v3 Verify authority. The default gate must be tested as v3, and the production gate/provider must remain unchanged.
Safe resolution path: In `scripts/test-workflow-code-state.py` only, make both review-only gate calls succeed; make the default legacy-complete call and both ordered review→explanation snapshot gate calls expect `AutomationContractError` with `incomplete`; optionally rename the two snapshot tests so their names distinguish historical readability from v3 authority. Do not delete the historical snapshot construction, weaken provider parsing, restore an explanation prerequisite, or change `scripts/workflow_automation.py` or `scripts/workflow_code_state.py`. Run the 19-test focused suite and structural validation, then return the exact test-only diff for targeted rereview.
needs-decision rationale: none; FV-R1, FV-R3, FV-R28, the approved architecture, and the current production gate already determine the expected outcomes.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | Tests invert the approved v3 review-only pre-Verify tail and historical explanation non-authority. |
| Test coverage | block | Three tests fail; one masks a fourth stale assertion in the same case. |
| Edge cases | pass | The existing fixtures already model both review-only and historical explanation tails. |
| Error handling | pass | Production fails closed for non-v3 or explanation-bearing tails. |
| Architecture boundaries | pass | Production keeps explanation generation inside successful Verify; only tests are stale. |
| Compatibility | concern | Historical tail parsing is correctly retained, but its test wrongly grants current v3 authority. |
| Security/privacy | pass | No security, privacy, secret, or permission surface is involved. |
| Derived artifact currency | pass | No generated or published artifact is implicated. |
| Unrelated changes | pass | The required correction is confined to focused test assertions and truthful test names. |
| Validation evidence | block | Focused suite is red until the stale expectations are corrected. |

## Validation performed

- `python scripts/test-workflow-code-state.py` — failed as reported: 19 tests, two failures, one error.
- Direct production inspection of `require_complete_ordered_evidence_tail` — current v3 gate matches the approved review-only tail contract.
- Temporary-archive assertion-only probe — passed all 19 focused tests after changing five gate expectations; production files were untouched.

No broad-smoke or PR-mode command was run.

## Handoff

This isolated review records the finding but performs no implementation correction or automatic downstream handoff. FV-M6-CR2 needs no owner decision; the record exists before correction. Workflow owns any lifecycle coordination, and this review leaves routing unchanged.
