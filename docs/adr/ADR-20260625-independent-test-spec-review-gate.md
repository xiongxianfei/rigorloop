# ADR-20260625: Independent Test-Spec-Review Gate

## Status

accepted

## Context

The standard workflow currently has `plan-review -> test-spec -> implement`. The test spec exists before implementation and guides proof, but no named independent review owner verifies its adequacy before implementation relies on it.

Adjacent stages cannot own this cleanly: `plan-review` runs before the test spec exists, `implement` should not approve its own proof contract, and `code-review` plus `verify` happen after implementation has consumed the proof map.

## Decision

Add a dedicated `test-spec-review` gate between `test-spec` and `implement`.

The gate reviews proof-map adequacy only. It does not reapprove product requirements, redesign architecture, author tests, implement code, execute final validation, or claim branch readiness.

The active test spec remains `active`. Review approval is recorded in formal review evidence and exposed through deterministic `Review status`, `Immediate next stage`, and `Implementation handoff` fields.

## Alternatives Considered

| Alternative | Reason rejected |
| --- | --- |
| Keep repository-defined review ownership | Leaves proof-map adequacy inconsistent and ambiguous. |
| Fold review into `plan-review` | The test spec does not exist yet. |
| Fold review into `implement` | Removes independence and lets implementation silently repair proof gaps. |
| Rely on `code-review` or `verify` | Finds proof defects after implementation has already relied on the test spec. |

## Consequences

- Formal workflow-managed test specs receive independent review before implementation.
- Implementation gains a new upstream eligibility condition.
- Workflow, skill, validator, and generated-package surfaces need coordinated updates.
- Isolated/manual review remains possible but does not authorize workflow implementation.
- Code-review and verify remain downstream backstops.

## Follow-up

- Implementation planning should decide milestone boundaries for workflow/spec updates, skill and asset creation, validator support, generated adapter proof, and representative review fixtures.
