---
name: implement
description: >
  Implement a reviewed milestone using strict test-driven development. Use after spec, architecture, plan, and test-spec are ready, or in the fast lane after an explicit spec and test checklist exist.
argument-hint: [plan path, milestone ID, feature name, or implementation request]
---

# Test-driven implementation

You are implementing the smallest approved slice with tests first.

Do not expand scope. Do not silently alter the spec. Do not declare success without verification evidence.

For planned initiatives, `implement` owns keeping the active plan body current during execution. Update the plan body's progress, decisions, discoveries, and validation notes as work advances instead of leaving those details to later stages.

## Inputs to read

Read before editing:

- `AGENTS.md`
- `CONSTITUTION.md` if present
- concrete execution plan
- feature spec
- test spec
- architecture doc and ADRs when relevant
- code and tests listed in the milestone
- existing patterns in neighboring files
- CI or validation commands relevant to the milestone

## Implementation loop

For each milestone:

1. Confirm milestone scope and requirements covered.
2. Identify the tests from the test spec.
3. Write or update the tests first.
4. Run the narrowest relevant test command.
5. Confirm new tests fail for the expected reason when feasible.
6. Implement the minimum production code needed to pass.
7. Run the narrow tests again.
8. Refactor only within milestone scope.
9. Run milestone validation commands.
10. Update the active plan body’s progress, decisions, surprises, and validation notes.
11. When the milestone is complete, create a milestone closeout commit using the subject format `M<n>: <completed milestone outcome>` and include milestone validation in the commit body or referenced evidence.
12. Stop before the next milestone unless the user asked to continue.

## TDD rules

- Tests first for new behavior.
- Regression test first for bugs.
- Minimal implementation to make tests pass.
- Refactor after green, not before.
- Delete or rewrite tests that pass for the wrong reason.
- Do not write broad mocks that bypass the behavior under test.

## Scope rules

- Implement only approved requirements and milestone tasks.
- Do not add unrelated refactors.
- Do not change public behavior not covered by the spec.
- If code reveals a spec or architecture gap, stop and update the artifact or document the blocker.
- If validation fails, fix or report before moving on.
- Do not mark a milestone complete without the milestone commit.
- Do not assume every completed milestone needs its own PR; multiple completed milestones may continue in the same PR when that is the clearest review unit.

## Plan update requirements

Update the concrete plan with:

- milestone progress;
- decisions made during implementation;
- surprises and discoveries;
- validation commands run;
- validation results;
- known follow-ups or deferred work.
- for planned initiatives, keep `docs/plan.md` as lifecycle bookkeeping rather than a milestone journal;
- if lifecycle state changes during implementation, update both `docs/plan.md` and the plan body, or record why only a merge-dependent `Done` transition remains pending.

## Expected output

- milestone implemented;
- tests added or updated first;
- validation commands and results;
- files changed;
- plan updates made;
- blockers or spec gaps;
- readiness statement for `code-review` or next milestone.
