# Code Review PR Preflight R1: Query Change Record Fixture Drift

Review ID: code-review-pr-preflight-r1
Stage: code-review
Round: r1
Reviewer: Independent Codex code-review agent
Target: post-Verify PR-preflight integration failure at `880473c9cd172f872b38cdbcf6c9a4e7e6c629a9`
Reviewed artifact: `scripts/test-query-change-record.py` against the current v3 runtime and immutable-v2 closeout record
Review date: 2026-09-01
Status: changes-requested
Recording status: recorded
Material findings: FV-M6-CR1
Reviewed milestone: M6

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review, `review-invocation-code-review-pr-preflight-r1.yaml`, `review-log.md`, and `review-resolution.md`
- Open blockers: `FV-M6-CR1`
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: `FV-M6-CR1`
- Recording status: recorded
- Recording blocker: none for review evidence; Workflow must perform any lifecycle route with the immutable v2 CLI
- Review record: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/reviews/code-review-pr-preflight-r1.md`
- Review log: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/review-log.md`
- Review resolution: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/review-resolution.md`
- Reviewed milestone: M6
- Milestone closeout: resolution-needed
- Remaining implementation milestones: none; this is a bounded correction to the reviewed candidate
- Required review-resolution: yes
- Finding IDs: `FV-M6-CR1`
- Verify readiness: not-claimed; the prior verdict is invalidated by the failing PR-preflight integration check

## Finding FV-M6-CR1

Finding ID: FV-M6-CR1
Severity: major
Location: `scripts/test-query-change-record.py:181-182,200,246,449,481`
Evidence: `python scripts/test-query-change-record.py` at `880473c9` runs 26 tests and fails three with one error. The stage-owned fixtures and workflow-state projection still select `stage-owned-change-local-v1`, which the current runtime correctly rejects as non-current, and two automation fixtures still bind the retired Verify completion rule `fresh verification passes` instead of the current immutable policy `verification passes and the final explanation is recorded`. A temporary-archive probe changing only those two contract values, two completion strings, and the matching metadata-shape assertion passed all 26 tests. The failure also reproduces inside `bash scripts/ci.sh --mode pr --base 066d973c4e230639aefda753d1f52dea4d730d28 --head HEAD`.
Required outcome: Current-behavior query tests must use v3 and the exact current Verify completion policy while retaining the explicit test that a stage-owned record requires the separately authorized read-only compatibility read. The focused suite and the authoritative PR-mode command must pass before Verify is repeated.
Safe resolution path: In `scripts/test-query-change-record.py` only, change the two governed fixture/input lifecycle contracts to `stage-owned-change-local-v3`, change the two completion rules to `verification passes and the final explanation is recorded`, and update the one metadata-shape expectation to v3. Do not weaken runtime rejection, revive v1/v2 progression, edit the production helper, or alter historical release evidence. Run the focused test, then the exact PR-mode command; obtain targeted rereview of the correction and repeat Verify because its prior decision basis claimed passing integrated evidence.
needs-decision rationale: none; the approved v3-only contract and current policy determine the correction exactly.

## Lifecycle routing conclusion

The finding belongs to implementation/test ownership, not Verify repair. The change remains an immutable v2 bootstrap at `current_stage: verify`, and the bound archived-v2 read-back explicitly permits `route-correction`; the staged current runtime must remain read-only toward this historical v2 record. Workflow should use the exact archived CLI from source snapshot `585c2beecea0ddda0ae11ed8f0b1a53b24310052` to route the open finding from Verify to the bounded implementation correction under M6, using the v2 ordinary correction reason `upstream-proof-gap` rather than any v3-only reason. The current runtime cannot perform this mutation. After the five-line test correction, independent rereview and a fresh Verify are mandatory before PR handoff; the existing Verify report cannot remain authoritative because its integrated-pass premise is disproved.

No lifecycle state was mutated by this review.
