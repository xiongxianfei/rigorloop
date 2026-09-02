# M1 Implementation Evidence: Read-only Workflow Context

Milestone: M1
Subject path: docs/plans/2026-09-02-refocus-workflow-into-route.md
Subject identity: sha256:825e74a85b56a43db8f8a47191882794d95dd27cf65ffe0e968358b7203b162d
Validation result: passed

## Result

## Core result

- Skill: implement
- Status: implemented
- Completed scope: Added the public read-only `rigorloop workflow-context` command, one normalized project/change result model, bundled v3 artifact-location defaults, a closed optional `rigorloop.workflow.yaml` parser, safe repository-relative template resolution, bounded lifecycle and automation projections, human and JSON rendering, and direct failure and non-mutation proof.
- Artifacts changed: `packages/rigorloop/dist/bin/rigorloop.js`; `packages/rigorloop/dist/lib/workflow-context.js`; `packages/rigorloop/dist/lib/lifecycle-read.js`; `packages/rigorloop/dist/lib/cli-observability.js`; `packages/rigorloop/test/workflow-context.test.js`; `packages/rigorloop/test/cli-invocation-observability.test.js`; `packages/rigorloop/README.md`; `schemas/rigorloop-workflow-v1.schema.json`.
- Tests added or updated: Project and exact-change phases; zero, one, and several active candidates; exact lifecycle/package/milestone/artifact/operation projection; bounded automation; valid overrides; unknown schema, keys, kinds, and variables; unresolved variables; repository escape; duplicate paths; symlink traversal; human/JSON parity; public invocation; diagnostic classification; invalid arguments; path redaction; byte-identical governed state.
- Validation performed: focused workflow-context test; plan-selected Node test set; complete package test suite; change-metadata validator tests; JSON schema parse; direct repository invocation; `git diff --check`.
- Validation result: all required commands passed. The focused final run passed 41 tests; the plan-selected run passed 162 tests; the complete package run passed 347 tests with 2 pre-existing skips; change-metadata validation passed 107 tests; schema parsing, direct invocation, and whitespace validation passed.
- Open blockers: none.
- Next stage: code-review.
- Claim limitations: M1 does not rename the public skill, remove `docs/workflows.md`, migrate current governance, generate adapters, publish a release, close the milestone, establish branch readiness, or establish final verification readiness.

## Planned milestone

- Change ID: `2026-09-02-refocus-workflow-into-route`.
- Plan identity: `docs/plans/2026-09-02-refocus-workflow-into-route.md`, sha256 `825e74a85b56a43db8f8a47191882794d95dd27cf65ffe0e968358b7203b162d`.
- Milestone ID: M1.
- Milestone state: implementation complete and ready for the guarded `review-requested` transition.
- Baseline or change-pack status: exact Design package `design-review-r1` and Delivery package `delivery-review-r1` remain current and granted; M1 is the first nonterminal implementation milestone.
- Milestone validation evidence: this file.
- Commit status: prepared for the required `M1: add read-only workflow context` review target commit after the workflow-owned review-requested transition is recorded.
- Code-review handoff: Review CLI structural-only authority, configuration closure and precedence, repository containment, privacy-bounded output, shared lifecycle interpretation, public rendering, retry/non-mutation proof, and the exclusion of M2/M3 behavior.

## Test-first record

The first focused test run failed because `packages/rigorloop/dist/lib/workflow-context.js` did not exist. The implementation was then added until the new project, change, configuration, path, privacy, rendering, and read-only tests passed. A later audit added direct command-family observability coverage and redaction proof for an invalid registered absolute path.

## Boundary and interaction proof

- TG-01 and BND-INPUT-001: project phase reports bounded zero, one, or many candidates and never selects one; several candidates return `RL_CONTEXT_SELECTION_AMBIGUOUS`.
- TG-02, BND-STATE-001, and BND-AUTH-001: change phase composes the existing lifecycle interpreter and returns the exact revision, stage, registered artifacts, review packages, milestone state, blockers, permitted operations, and bounded automation without selecting semantic ownership.
- TG-03, BND-INPUT-001, BND-RECOVERY-001, and INT-002: bundled defaults plus a tracked override use closed versions, keys, kinds, entry fields, owners, and variables; invalid, incomplete, duplicate, escaped, absolute, or symlink-dependent locations fail closed with no guide or guessed fallback.
- TG-04 and BND-ENV-001: human and JSON views originate from one result object; emitted paths are repository-relative, automation fields are allowlisted, and invalid registered paths are redacted.
- TG-05, BND-TEMPORAL-001, BND-RECOVERY-001, and INT-005: reads accept no mutation request and direct tests compare governed bytes across success, ambiguity, and rejected input. Exact change output carries the current lifecycle revision, so later mutation creates a distinct context identity.

## Unaffected surfaces

- `skills/workflow/`, its guide resources, and `docs/workflows.md` are unchanged because their coherent rename and retirement belong to M2.
- Current governance, workflow contracts, project map, guide validators, and validation-selection behavior are unchanged because M2 owns their atomic source-of-truth cutover.
- Adapter manifests, generators, installers, archives, and release checks are unchanged because M3 owns generated and distribution parity.
- Lifecycle mutations, stage ownership, correction routing, stored `workflow` authority, and `workflow.automation` persistence are unchanged; M1 only reuses and projects the current read model.

## Commands and results

```text
node --test packages/rigorloop/test/workflow-context.test.js
PASS: 14 tests

node --test packages/rigorloop/test/cli.test.js packages/rigorloop/test/lifecycle-read.test.js packages/rigorloop/test/result-renderer.test.js packages/rigorloop/test/workflow-context.test.js
PASS: 162 tests

node --test packages/rigorloop/test/cli-invocation-observability.test.js packages/rigorloop/test/workflow-context.test.js
PASS: 41 tests

npm test --prefix packages/rigorloop
PASS: 347 passed, 2 skipped, 0 failed

python scripts/test-change-metadata-validator.py
PASS: 107 tests

python -m json.tool schemas/rigorloop-workflow-v1.schema.json
PASS

node packages/rigorloop/dist/bin/rigorloop.js workflow-context --change 2026-09-02-refocus-workflow-into-route --format json --no-file-log
PASS: exact M1 context returned; lifecycle revision and current stage present

git diff --check
PASS
```
