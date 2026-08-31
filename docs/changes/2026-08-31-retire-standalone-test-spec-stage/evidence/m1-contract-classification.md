## Result

Milestone: M1
Validation result: passed

## Core result

- Skill: implement
- Status: implemented
- Completed scope: Added the inactive lifecycle-contract activation model, deterministic v2/v1/legacy classification, exact prior-contract manifest matching, fail-closed vocabulary and ordering checks, reader diagnostics, and explicit v1 new-change scaffolding.
- Artifacts changed: `specs/lifecycle-contract-activation.yaml`; `schemas/lifecycle-contract-activation.schema.json`; `schemas/change.schema.json`; lifecycle contract, reader, and new-change modules; shared Node/Python fixtures and focused regressions.
- Tests added or updated: TS-001, TS-002, and TS-015 coverage for explicit v2, manifest-matched v1 and legacy-unversioned records, missing and mismatched membership, duplicate and raw-UTF-8-unsorted entries, unknown contract/class/activation-state values, active test-spec state under v2, heuristic-independence, reader diagnostics, and v1 scaffold preservation.
- Validation performed: CMD-01, CMD-03, CMD-04, and `git diff --check`.
- Validation result: CMD-01 passed 186 Node tests; CMD-03 passed 73 Python tests; CMD-04 passed 162 Python tests; whitespace validation passed.
- Open blockers: none.
- Next stage: code-review.
- Claim limitations: v2 routing, v2 package authority, lifecycle migration, activation, rollback, skill retirement, and adapter publication remain outside M1. The tracked manifest remains `preactivation`, has no activating revision or compatibility entries, and grants no v2 authority.

## Planned milestone

- Change ID: `2026-08-31-retire-standalone-test-spec-stage`
- Plan identity: `docs/plans/2026-08-31-retire-standalone-test-spec-stage.md`, sha256 `727b5a71f1d5ce001876cde59f195536c9671b4743e50a70ef95cf437ccc9938`.
- Milestone ID: M1.
- Milestone state: implementation complete; ready for the guarded `review-requested` transition.
- Baseline or change-pack status: Delivery Review package `delivery-review-r3` is current and granted; lifecycle initialization selected M1 and preserved the approved package identities.
- Milestone validation evidence: this file.
- Commit status: pending the lifecycle handoff mutation so the implementation and exact review-requested state can share one branch commit.
- Code-review handoff: review schema closure, identical Node/Python classification, raw UTF-8 manifest determinism, bounded prior compatibility, inactive v2 behavior, and explicit v1 new-change output.

## Test-first record

The first focused run failed because the classifier exports and Python compatibility functions did not yet exist, the reader exposed no compatibility classification, and an active manifest did not constrain prior records. After those paths passed, the complete CMD-01 run exposed that `new-change` was still unversioned. The scaffold was corrected to emit a v1 draft at `proposal`, and CMD-01 then passed in full.

No in-place migration operation was added. Existing prior records keep their registered contract; the optional migration decision remains deferred by the approved architecture and plan.
