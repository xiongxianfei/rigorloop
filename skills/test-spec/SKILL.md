---
name: test-spec
description: >
  Generate a traceable test specification from an approved feature spec and execution plan before writing test code or production code. Use to map requirements, examples, edge cases, architecture boundaries, and milestones into concrete tests.
argument-hint: [feature spec path, plan path, or feature name]
---

# Test spec authoring

You are designing the proof before implementation.

The test spec defines how the team will know the implementation satisfies the behavioral contract.

## Inputs to read

Read:

- approved or reviewed feature spec;
- spec-review findings;
- architecture doc and ADRs when relevant;
- concrete execution plan;
- `AGENTS.md` and `.codex/CONSTITUTION.md` if present;
- existing test conventions, fixtures, helpers, and CI commands;
- related tests for similar behavior.

## Output path

Prefer:

```text
specs/slug.test.md
```

## Required sections

1. **Status**: draft, reviewed, active, complete.
2. **Related spec and plan**.
3. **Testing strategy**: unit, integration, end-to-end, smoke, manual, contract, migration.
4. **Requirement coverage map**: every requirement ID maps to one or more tests or explicit manual verification.
5. **Example coverage map**: every example maps to a test when feasible.
6. **Edge case coverage**.
7. **Test cases** with stable IDs.
8. **Fixtures and data**.
9. **Mocking/stubbing policy**.
10. **Migration or compatibility tests** when relevant.
11. **Observability verification** when logs, metrics, traces, or audit events are required.
12. **Security/privacy verification** when relevant.
13. **Performance checks** when relevant.
14. **Manual QA checklist** when automation is insufficient.
15. **What not to test** and why.
16. **Uncovered gaps** that must return to spec or architecture.

## Test case format

Use:

```text
T1. Title
- Covers: R1, R3, E2
- Level: unit | integration | e2e | smoke | manual
- Fixture/setup:
- Steps:
- Expected result:
- Failure proves:
- Automation location:
```

## Coverage rules

- Every `MUST` requirement needs coverage.
- Every error behavior needs coverage.
- Every migration or compatibility claim needs coverage or explicit manual verification.
- Every architectural boundary that could break wiring needs an integration or contract test.
- Bugs require a regression test that fails before the fix when feasible.

## Rules

- Do not generate tests from an unreviewed or unstable spec unless using the fast lane and documenting the risk.
- Do not invent behavior not specified.
- Do not mark a requirement covered by a test that does not assert it.
- Do not rely only on snapshots for behavioral requirements.
- Do not skip integration tests where the risk is at a boundary.
- Do not hide untestable requirements; send them back to `spec-review`.

## Expected output

- test spec path;
- grouped test cases;
- requirement-to-test coverage map;
- fixtures and commands;
- explicit exclusions;
- uncovered gaps, if any;
- readiness statement for `implement`.
