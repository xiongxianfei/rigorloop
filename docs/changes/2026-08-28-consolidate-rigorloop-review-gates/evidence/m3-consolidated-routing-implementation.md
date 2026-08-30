# M3 Consolidated Routing Implementation Evidence

Change ID: 2026-08-28-consolidate-rigorloop-review-gates
Milestone: M3
Stage authority: implement
Subject path: docs/plans/2026-08-29-consolidate-rigorloop-review-gates.md
Subject identity: sha256:0f37ca539a8d2fdc10ad4b982d69c95fe379f04ca4383a78877de34fe1a090f6
Validation result: pass

## Scope completed

M3 replaces both lifecycle routing implementations with the approved consolidated sequence, centralizes source-stage completion checks, integrates package correction routing, synchronizes active automation projections, and exposes one compact downstream package-authority assessment. Milestone operations remain separate and unchanged.

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

The JavaScript lifecycle and Python automation policy now use the same sequence: `proposal-review -> architecture -> spec -> design-review -> plan -> test-spec -> delivery-review -> implement`. Retired public review stages are rejected by the active Python vocabulary, while historical automation mechanism names remain readable until cutover.

Status and downstream context expose one compact assessment for both packages. Each package reports only `state` (`missing`, `historical-only`, `partial`, `stale`, `mixed`, or `current`) and `authority`; the assessment reports `enforcement: cutover-pending`. This makes invalid authority explicit without adding document hashes, aggregate revisions, activation metadata, or a retroactive blocker. M6 will activate the same assessment atomically after legacy-dependent work is closed, as required by CRG-R35 through CRG-R40.

Python stage-native completion now validates combined reviews against safe current member paths, the explicit package member map, upstream review ID, registered package-review decision, and canonical review-log occurrence. It records compact member facts in the completion proof and does not introduce a package hash or aggregate revision.

## Tests added or updated

- `packages/rigorloop/test/lifecycle-stage-advance.test.js`: consolidated adjacent graph, package-authorized advancement, isolated settlement, retired-edge rejection, automation synchronization, and stale/mixed downstream authority.
- `packages/rigorloop/test/lifecycle-correction-route.test.js`: exact package-finding route, authoring return, repeat-target rejection, and package-rereview requirement.
- `packages/rigorloop/test/lifecycle-read.test.js`: missing, historical-only, and partial authority projections plus pre-cutover non-enforcement.
- `packages/rigorloop/test/helpers/lifecycle-package-fixture.js`: preserves multiple canonical package-review log occurrences.
- `scripts/test-workflow-automation-policy.py`, `scripts/test-workflow-automation-state.py`, and `scripts/test-workflow-automation.py`: exact consolidated vocabulary, graph, positioning, routing, and retired-stage rejection.
- `packages/rigorloop/test/fixtures/observability/v0.4.x-output-compatibility-v1.json`: approved lifecycle status/context evolution governed by CRG-R41.
- `packages/rigorloop/test/lifecycle-evidence.test.js`: finding-resolution recording reads disposition and ownership from the requested finding section rather than the first finding in a shared resolution file.

## Validation

- `node --test packages/rigorloop/test/lifecycle-stage-advance.test.js packages/rigorloop/test/lifecycle-correction-route.test.js packages/rigorloop/test/lifecycle-milestone.test.js packages/rigorloop/test/lifecycle-read.test.js` — 43 passed.
- `python scripts/test-workflow-automation.py` — 76 passed.
- `python scripts/test-workflow-automation-policy.py` — 17 passed.
- `python scripts/test-workflow-automation-state.py` — 68 passed.
- `python scripts/test-workflow-code-state.py` — 18 passed.
- `npm test --prefix packages/rigorloop` — 297 passed.
- `python scripts/test-change-metadata-validator.py` — 66 passed.
- `python scripts/validate-review-artifacts.py docs/changes/2026-08-28-consolidate-rigorloop-review-gates` — passed.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-28-consolidate-rigorloop-review-gates/change.yaml` — passed.
- `node packages/rigorloop/dist/bin/rigorloop.js lifecycle validate --change 2026-08-28-consolidate-rigorloop-review-gates --format concise-json` — success at M3.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-08-29-consolidate-rigorloop-review-gates.md --path specs/consolidated-review-gates.md --path docs/adr/ADR-20260828-consolidated-review-package-topology.md` — 4 artifact files validated.
- `git diff --check` — passed.

## Unaffected surfaces

- Historical automation record names and legacy change-stage vocabulary remain readable until the atomic M6 cutover; they grant no new consolidated authority.
- Code Review, milestone completion, final holistic review, explanation, Verify, and PR ownership are unchanged. M3 exposes invalid package authority to downstream contexts; M6 owns activation of the blocker.
- No topology field, activation document, package hash, new top-level CLI family, dependency, or separate completion receipt was added.

## Recovery

Before release cutover, revert the consolidated routing module, graph, package-correction integration, and their tests as one unit. Existing milestone-specific operations and the last complete package settlement remain intact.

## Handoff

M3 implementation is ready for milestone-local Code Review of graph closure, shared completion authority, package correction ownership, automation synchronization, and downstream evidence rejection. This evidence does not claim review, verification, branch, or PR readiness.
