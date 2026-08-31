# M5 v2 activation evidence

## Result

Milestone: M5
Validation result: passed

## Outcome

M5 atomically activates `stage-owned-change-local-v2` for new governed changes, freezes the exact prior-contract inventory, removes standalone test-spec from canonical and adapter publication surfaces, and preserves manifest-bound v1 continuation after Delivery Review.

## Activation identity and compatibility

- Activating source revision: `2ad3568ee15673ccbccc99474ecdd90b258a15f8`.
- Frozen prior inventory: 149 records in raw UTF-8 change-ID order: 33 explicit v1 and 116 legacy-unversioned.
- Activation prerequisite: passed with no missing, extra, reordered, duplicated, class-mismatched, pre-gate, or retired-live-stage dependency.
- Historical handling: records and evidence were not rewritten. The governed CLI validates all 33 explicit contract records and reports only the two approved baseline warnings.
- Recovery boundary: this activation commit is the complete pre-first-v2 rollback unit. No governed v2 record existed when the inventory was frozen. Once a v2 record is committed, the active manifest and v2 classifier reject silent prior-contract fallback; recovery must be a forward compatible correction.

## Test-first record

Before production changes, focused tests failed because new-change still emitted v1, legacy approved plan/test-spec reviews did not satisfy activation prerequisites, canonical and adapter inventories still contained test-spec, and active workflow guidance still described preactivation. The same focused surfaces pass after the implementation.

## Implemented surfaces

- New-change now emits v2 and the output compatibility fixture records that approved fact evolution.
- The active lifecycle manifest binds every prior record exactly, while repository validation fails on inventory drift.
- Current workflow, governance, README, skill-contract, skill packages, and adapter metadata use the plan-centered route.
- `skills/test-spec/` and all current OpenCode/test-spec adapter entrypoints are removed.
- Manifest-bound v1 changes remain readable and may continue only from their already-approved post-delivery packages.
- Plan-owned specialist verification references remain packaged conditionally for every supported adapter.

## Validation

- `node --test packages/rigorloop/test/cli.test.js packages/rigorloop/test/lifecycle-contract.test.js packages/rigorloop/test/lifecycle-read.test.js packages/rigorloop/test/lifecycle-stage-advance.test.js packages/rigorloop/test/lifecycle-transaction.test.js` — passed, 189 tests.
- `npm test --prefix packages/rigorloop` — passed, 310 tests; 2 skipped.
- `python scripts/test-change-metadata-validator.py` — passed, 82 tests.
- `python scripts/test-artifact-lifecycle-validator.py` — passed.
- `python scripts/test-workflow-automation.py && python scripts/test-workflow-automation-policy.py && python scripts/test-workflow-automation-state.py` — passed.
- `python scripts/test-review-artifact-validator.py` — passed.
- `python scripts/test-skill-validator.py` — passed, 376 tests.
- `python scripts/test-build-skills.py && python scripts/build-skills.py --check` — passed, including temporary generated-skill parity.
- `python scripts/test-adapter-distribution.py` — passed, 154 tests in 380 seconds, including supported archive and clean-install checks.
- `python scripts/validate-documentation-prose.py --mode audit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path specs/rigorloop-workflow.md` — passed with 0 errors and 48 pre-existing/source-format warnings assessed as non-blocking.
- `python scripts/test-lifecycle-cli-conformance.py` — passed, 6 invalid and 10 protected fixtures.
- `python scripts/test-governed-lifecycle-cli-validator.py` — passed, 8 tests.
- `python scripts/validate-governed-lifecycle-cli.py` — passed; activation errors 0, failures 0, retired progression dependencies 0, 33 explicit records validated, 2 approved baseline warnings.
- `bash scripts/ci.sh --mode broad-smoke` — passed, 11 checks in 434 seconds.
- `git diff --check` — passed.

## Unaffected with rationale

- Historical test-spec artifacts and formal review evidence are unchanged because they remain immutable compatibility records.
- Code Review, Explain Change, Verify, and PR ownership are unchanged; M5 changes their inputs only where the contract selects the v2 plan package.
- No generated adapter skill bodies were hand-edited; tracked adapter support metadata changed and temporary archive generation proved parity.

## Handoff

The complete M5 activation slice is ready for final implementation-milestone Code Review. M6 lifecycle closeout remains out of this implementation milestone.
