# Explain Change: Plan Review to Test Spec Workflow Transition

## Outcome

The unified workflow coordinator now represents and authorizes the complete pre-implementation sequence:

```text
plan -> plan-review -> test-spec -> test-spec-review -> implement M1
```

This repairs an implementation gap in the coordinator. The approved workflow contract and contributor-facing workflow guide already require this ordering, so no contract amendment is needed.

## Root Cause

The canonical artifact sequence stopped at `plan`, and active-plan resolution treated the first planned milestone as though `test-spec-review` had already completed. As a result, durable evidence for `plan-review` was rejected as an unknown position, while a plan whose next stage was `test-spec` was rejected because the resolver expected `implement M1`.

## Fix

- Extend the canonical pre-implementation sequence through `test-spec-review`.
- Treat `plan-review` and `test-spec-review` as review positions.
- Reject test-spec evidence unless plan-review evidence is approved.
- Resolve planned-milestone handoffs to their immediately preceding canonical positions. The recognized handoffs are `plan-review`, `test-spec`, `test-spec-review`, and `implement M1`.

No authorization class, mutation scope, external-action policy, or post-implementation routing behavior changed.

## Regression Proof

Tests were added before the production fix and reproduced both failures:

- artifact evidence could not reach the three post-plan positions;
- an active plan could not represent post-plan authoring handoffs.

A transaction-level regression also proves that approved plan-review evidence permits a bounded test-spec authoring capability. The transaction consumes that capability, records `plan-review` as the source position, and routes to `test-spec-review`.

Passing validation:

```text
python scripts/test-workflow-automation.py
python scripts/test-workflow-automation-state.py
python scripts/test-validate-workflow-automation.py
```

The runs passed 76, 60, and 68 tests respectively.

## Scope And Remaining Work

This repair is limited to the coordinator and its regression tests. It does not itself advance the active boundary-first artifacts. That workflow resumes separately through the repaired public coordinator so its durable transition receipts and authorization boundaries remain authoritative.
