# Code Review PR Preflight R7: Workflow Automation State Fixture Drift

Review ID: code-review-pr-preflight-r7
Stage: code-review
Round: r7
Reviewer: Independent Codex code-review agent
Target: PR-preflight failure at `ef5c22d5`
Reviewed artifact: `scripts/test-workflow-automation-state.py` against current v3-only automation-state production
Review date: 2026-09-01
Status: changes-requested
Recording status: recorded
Material findings: FV-M6-CR4
Reviewed milestone: M6

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review, `review-invocation-code-review-pr-preflight-r7.yaml`, `review-log.md`, `review-resolution.md`, and the top review projection in `change.yaml`
- Open blockers: `FV-M6-CR4`
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: `FV-M6-CR4`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/reviews/code-review-pr-preflight-r7.md`
- Review log: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/review-log.md`
- Review resolution: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/review-resolution.md`
- Reviewed milestone: M6
- Milestone closeout: resolution-needed
- Remaining implementation milestones: none; this is a bounded current-state test correction
- Required review-resolution: yes
- Finding IDs: `FV-M6-CR4`
- Verify readiness: not-claimed; the focused automation-state suite is failing

## Finding FV-M6-CR4

Finding ID: FV-M6-CR4
Severity: major
Location: `scripts/test-workflow-automation-state.py:120-142,329-391,422-475,2584-2636`
Evidence: `python scripts/test-workflow-automation-state.py` at `ef5c22d5` runs 70 tests and fails five. The stage-native registry expectation still includes retired Test Spec and Explain Change; the package-review helper defaults to v1 and therefore builds delivery members with a Test Spec while current production expects plan-only v3 Delivery; three positive/negative delivery tests fail at the earlier member mismatch; and the first nonterminal migration still expects v1 even though production migrates to `STAGE_OWNED_CONTRACT` v3. The helper's current migration target also retains retired Verify completion wording. A consolidated in-memory test-only correction of those six current-policy sites passed all 70 tests.
Required outcome: Current automation-state tests must expect the exact v3 stage-native registry, default package-review fixtures to v3 with plan-only Delivery membership, use the current Verify completion rule for newly migrated state, and expect migration to v3. Explicit historical v1/v2 package/read cases and their contract-specific artifacts must remain intact.
Safe resolution path: Modify only `scripts/test-workflow-automation-state.py`: remove Test Spec and Explain Change from the current registry expectation; change `package_review_completion_fixture` default to v3; select plan-plus-Test-Spec only for explicit v1 and plan-only for v2/v3 delivery fixtures; update the first current migration target to `verification passes and the final explanation is recorded`; and expect the migrated lifecycle contract to be v3. Keep the explicit v2 plan-only package test, explicit v1 Test Spec artifact branch, retired Explain Change rejection test, historical side-effect-free reads, terminal historical non-migration, and historical source target used by the drift-rejection test. Run all 70 focused tests, rescan the file to classify remaining v1/v2/retired-stage references, run structural validation, and return for targeted rereview.
needs-decision rationale: none; FV-R4-FV-R7, FV-R28, FV-R35, FV-R37, and current production already distinguish current v3 execution from historical readability.

## Historical-reference classification

The remaining explicit non-v3 references are intentional and must not be bulk replaced: `test_v2_delivery_review_completion_binds_the_primary_plan_only` proves the historical v2 plan-only package shape; the v1 artifact-state branch constructs historical Test Spec membership; the Explain Change route case proves retired-stage rejection; historical read/migration negative tests preserve absent/terminal legacy behavior; and the old completion string in `test_migration_rejects_target_or_stop_reason_drift` is source historical state whose drift must be rejected. Only `current_parts()` represents the new current migration target and needs current wording.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | Current fixture defaults and registry expectation still encode retired v1 stages. |
| Test coverage | block | Five failures stop current package and migration assertions at stale earlier mismatches. |
| Edge cases | pass | Explicit v1/v2 and historical read/migration cases already exist and should be preserved. |
| Error handling | pass | Production rejects retired stages and enforces current package members. |
| Architecture boundaries | pass | Production state/migration owners are coherent; only tests are stale. |
| Compatibility | concern | Current defaults are conflated with historical v1/v2 cases. |
| Security/privacy | pass | No security, privacy, secret, or permission surface is involved. |
| Derived artifact currency | pass | No generated or published artifact is affected. |
| Unrelated changes | pass | Required correction is confined to one focused test file. |
| Validation evidence | block | Focused suite remains red until all stale current-policy sites are corrected together. |

## Validation performed

- `python scripts/test-workflow-automation-state.py` — failed: 70 tests, five failures.
- Full-file current/historical reference scan — identified six stale-current sites and preserved the explicit historical cases listed above.
- Direct production inspection — current registry omits retired stages; `STAGE_OWNED_CONTRACT` is v3; Delivery is plan-only.
- In-memory consolidated test-only probe — passed all 70 tests with production untouched.

No broad-smoke or PR-mode command was run.

## Handoff

This isolated review records FV-M6-CR4 before correction and performs no automatic downstream handoff. No owner decision is needed. Workflow owns lifecycle coordination; this review leaves routing unchanged.
