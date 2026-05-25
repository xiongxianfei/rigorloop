# Workflow Stage Order

This topic is curated learn guidance. Authoritative workflow order remains in
`docs/workflows.md`, `specs/rigorloop-workflow.md`, active plans, and accepted
workflow specs.

## Plan Before Test Spec

- Date: 2026-05-25
- Source session: [Plan Before Test Spec Public Framing](../sessions/2026-05-25-plan-before-test-spec-public-framing.md)
- Primary classification: durable-lesson
- Secondary routes: none

When writing public or contributor-facing traceability copy, put `plan` before
`test-spec`.

Preferred short chain:

```text
proposal -> proposal-review -> spec -> spec-review -> plan -> plan-review ->
test-spec -> implement -> code-review -> explain-change -> verify -> PR
```

Use the conditional architecture and review-resolution stages when the context
needs the full workflow:

```text
proposal -> proposal-review -> spec -> spec-review -> architecture ->
architecture-review -> plan -> plan-review -> test-spec -> implement ->
code-review -> review-resolution when triggered -> ci-maintenance when triggered
-> explain-change -> verify -> PR
```

The reason is practical: the test spec operationalizes the accepted contract
against the chosen execution plan. It depends on milestone order, dependencies,
rollback boundaries, manual proof surfaces, and validation commands. A spec can
be eventually test-spec ready after `spec-review`, but `architecture` and `plan`
still come first when those stages are required.

Avoid phrases that imply generic tests are designed before planning, such as:

```text
proposal -> spec -> tests -> plan
```

Safer public wording:

```text
proposal -> spec -> plan -> test spec -> implementation
```

or:

```text
RigorLoop turns an idea into proposal, spec, plan, test spec, implementation
evidence, review, verification, and PR handoff.
```
