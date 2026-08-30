# M3 Consolidated Routing Implementation Evidence

Change ID: 2026-08-28-consolidate-rigorloop-review-gates
Milestone: M3
Stage authority: implement
Subject path: docs/plans/2026-08-29-consolidate-rigorloop-review-gates.md
Subject identity: sha256:0f37ca539a8d2fdc10ad4b982d69c95fe379f04ca4383a78877de34fe1a090f6
Validation result: pass

## Scope completed

M3 replaces the lifecycle CLI's pre-implementation forward graph with the approved consolidated sequence, centralizes source-stage completion checks, integrates package correction routing, synchronizes active automation projections, and makes current package evidence participate in downstream status. Milestone operations remain separate and unchanged.

## Stage-transition matrix

| Completed source | Permitted destination | Completion authority |
| --- | --- | --- |
| proposal | proposal-review | current proposal authoring registration |
| proposal-review | architecture | accepted Proposal Review |
| architecture | spec | current architecture and applicable ADR registrations |
| spec | design-review | current specification registration |
| design-review | plan | current approved design package |
| plan | test-spec | current plan registration |
| test-spec | delivery-review | current test-specification registration |
| delivery-review | implement | current approved delivery package |

Retired and skipped edges fail unchanged. Package settlement leaves `current_stage` and `next_stage` at the review stage until workflow invokes `advance-stage`. Exact replay remains idempotent through the existing lifecycle transaction contract.

## Package correction routing

- A changes-requested package review exposes `route-correction` only for named correction targets.
- `review-required` component artifacts are valid package-correction destinations because package authority, not an individual artifact review, owns progression.
- The owning author records the corrected artifact revision; `return-correction` binds the exact current artifact and its authoring evidence.
- Returned targets are associated with the exact source package review ID and cannot be routed twice for that review.
- A governed correction revision changes the package to `review-required`; package rereview remains mandatory and no component gains partial progression authority.

## Automation and downstream authority

`advance-stage` atomically updates `workflow_state.current_stage`, `workflow_state.next_stage`, and an active `workflow.automation.current_stage`. A contradictory active automation projection fails without mutation.

Status and context reread registered package review evidence and the canonical review-log occurrence. Changed review evidence, a mismatched upstream review ID, or another mixed package projection withholds authority and blocks downstream status. Appending an unrelated review-log entry does not stale earlier package authority because package registrations bind their canonical log occurrence rather than the entire mutable log file.

## Tests added or updated

- `packages/rigorloop/test/lifecycle-stage-advance.test.js`: consolidated adjacent graph, package-authorized advancement, isolated settlement, retired-edge rejection, automation synchronization, and stale/mixed downstream authority.
- `packages/rigorloop/test/lifecycle-correction-route.test.js`: exact package-finding route, authoring return, repeat-target rejection, and package-rereview requirement.
- `packages/rigorloop/test/helpers/lifecycle-package-fixture.js`: preserves multiple canonical package-review log occurrences.

## Validation

- `node --test packages/rigorloop/test/lifecycle-stage-advance.test.js packages/rigorloop/test/lifecycle-correction-route.test.js packages/rigorloop/test/lifecycle-milestone.test.js packages/rigorloop/test/lifecycle-read.test.js` — 41 passed.
- `python scripts/test-workflow-automation.py` — 76 passed.
- `python scripts/test-workflow-automation-policy.py` — 16 passed.
- `python scripts/test-workflow-automation-state.py` — 65 passed.
- `python scripts/test-workflow-code-state.py` — 18 passed.
- `npm test --prefix packages/rigorloop` — 294 passed.
- `python scripts/test-change-metadata-validator.py` — 66 passed.
- `python scripts/validate-review-artifacts.py docs/changes/2026-08-28-consolidate-rigorloop-review-gates` — passed.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-28-consolidate-rigorloop-review-gates/change.yaml` — passed.
- `node packages/rigorloop/dist/bin/rigorloop.js lifecycle validate --change 2026-08-28-consolidate-rigorloop-review-gates --format concise-json` — success at M3.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-08-29-consolidate-rigorloop-review-gates.md --path specs/consolidated-review-gates.md --path docs/adr/ADR-20260828-consolidated-review-package-topology.md` — 4 artifact files validated.
- `git diff --check` — passed.

## Unaffected surfaces

- `scripts/workflow_automation.py`, `scripts/workflow_automation_policy.py`, and `scripts/workflow_automation_state.py` are unchanged. Their existing policy, durable-state, recovery, and code-state suites pass; lifecycle `advance-stage` owns synchronization of the active automation stage projection in this slice. Canonical public target and skill inventory replacement remains M4 and final cutover work remains M6.
- Code Review, milestone completion, final holistic review, explanation, Verify, and PR ownership are unchanged. M3 only makes stale or mixed package evidence visible to their downstream contexts.
- No topology field, activation document, package hash, new top-level CLI family, dependency, or separate completion receipt was added.

## Recovery

Before release cutover, revert the consolidated routing module, graph, package-correction integration, and their tests as one unit. Existing milestone-specific operations and the last complete package settlement remain intact.

## Handoff

M3 implementation is ready for milestone-local Code Review of graph closure, shared completion authority, package correction ownership, automation synchronization, and downstream evidence rejection. This evidence does not claim review, verification, branch, or PR readiness.
