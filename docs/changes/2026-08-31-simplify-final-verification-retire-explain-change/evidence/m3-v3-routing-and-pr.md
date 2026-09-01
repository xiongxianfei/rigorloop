<!-- Template: implementation-result-skeleton-v1 -->
<!-- Skill: implement -->
<!-- Template status: normative -->

## Result

Milestone: M3
Validation result: passed

## Core result

- Skill: implement
- Status: implemented
- Completed scope: Added the inactive contract-keyed v3 final route, removed the standalone explanation prerequisite only from v3 verification readiness, defined closed Verify-finding ownership, and required PR handoff to consume the exact current successful Verify explanation, basis, and authoritative evidence references.
- Artifacts changed: packaged lifecycle and final-verification runtime modules, Python automation/policy/state/protocol modules, and focused Node/Python tests.
- Tests added or updated: v3 graph isolation, forbidden explain-change routing, review-only pre-Verify tail, exact correction owners, unknown-value rejection, exact Verify-to-PR consumption, stale basis, competing rationale, and newly referenced authority.
- Validation performed: every M3 plan command, focused final-verification protocol tests, Python report/PR parity tests, and `git diff --check`.
- Validation result: passed.
- Open blockers: none.
- Next stage: code-review.
- Claim limitations: v3 remains inactive and grants no public lifecycle authority; M3 does not update published skills or governance, remove `skills/explain-change/`, switch the default contract, prepare a PR, or alter exact v1/v2 continuation behavior.

## Planned milestone

- Change ID: `2026-08-31-simplify-final-verification-retire-explain-change`
- Plan: `docs/plans/2026-08-31-simplify-final-verification-retire-explain-change.md`
- Milestone ID: M3.
- Baseline: M1 and M2 are closed with clean Code Review; the final-verification activation manifest remains `preactivation`.
- Code-review handoff: review graph closure, v1/v2 isolation, exact owner attribution, read-only Verify behavior, evidence-tail identity, and exact PR consumption.

## Test-first and implementation record

- Contract tests were added for the v3 policy graph, forbidden `explain-change`, correction ownership, and exact PR consumption alongside implementation.
- The first focused policy run failed because the new internal transition incorrectly treated `pr` as a `WorkflowStage`; PR is a terminal `WorkflowPosition`. The transition target set was corrected to `verify`, after which the complete policy and automation suites passed.
- Verification readiness now selects its basis by lifecycle contract. V1 and v2 still require `explanation_inputs_identity` and the ordered final-review-to-explanation tail. V3 requires the final-review recording but has no standalone explanation input or commit.
- The public lifecycle classifier remains inactive for v3. The internal graph and fixture routes are available for package assembly and testing without changing active v2 behavior.

## Routing, ownership, and PR evidence

- TG-10: the v3 policy inventory removes both `test-spec` and `explain-change`; final holistic Code Review routes directly to Verify. An attempted v3 `explain-change` integration stage fails closed. Existing v1/v2 policy and automation tests remain unchanged and pass.
- TG-11: a failed Verify route remains paused and exposes no automatic repair. `system-requirement-gap`, `technical-realization-gap`, `verification-allocation-gap`, `implementation-defect`, `stale-or-incomplete-review`, `ci-or-environment-gap`, and `external-evidence-gap` map respectively to spec, architecture, plan, implement, code-review, ci-maintenance, and external evidence acquisition. Verify is never an owner.
- TG-12: v3 verification readiness accepts the current final-review recording as the pre-Verify evidence tail and excludes `explanation_inputs_identity`; v1/v2 still reject that partial tail and retain the standalone explanation prerequisite.
- TG-13: failed verification does not advance to PR and the route model keeps `automatic_repair` false. Successful v3 verification reaches only the PR boundary and performs no external action.
- TG-14: PR readiness recomputes and parses the complete Verify report, requires the exact registered report digest and verified subject, compares the complete current basis and explanation, and accepts exactly the authoritative report, Delivery plan, and proof paths already present in Verify. Drift, incomplete tails, stale subjects, changed basis, rewritten rationale, duplicates, missing references, and new authoritative references do not grant readiness.

## Validation evidence

- `node --test packages/rigorloop/test/lifecycle-contract.test.js packages/rigorloop/test/lifecycle-read.test.js packages/rigorloop/test/lifecycle-stage-advance.test.js packages/rigorloop/test/lifecycle-correction-route.test.js packages/rigorloop/test/lifecycle-transaction.test.js` — passed, 86 tests with 2 historical skips.
- `python scripts/test-workflow-automation.py` — passed, 78 tests.
- `python scripts/test-workflow-automation-policy.py` — passed, 20 tests.
- `python scripts/test-workflow-automation-state.py` — passed, 70 tests.
- `python scripts/test-workflow-code-state.py` — passed, 19 tests.
- `python scripts/test-review-artifact-validator.py` — passed, 110 tests.
- `node --test packages/rigorloop/test/final-verification-protocol.test.js` — passed, 10 tests.
- `python scripts/test-change-metadata-validator.py` — passed, 106 tests.
- `git diff --check` — passed.

## Review handoff

Review the v3 policy as an inactive candidate, not as current public authority. Confirm that there is no v3 explanation target or prerequisite, that all correction kinds fail closed to one non-Verify owner, that v1/v2 semantics did not change, and that PR cannot substitute prose or introduce an authority not already present in the current successful Verify result.
