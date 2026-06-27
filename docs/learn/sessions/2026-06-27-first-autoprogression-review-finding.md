# Learn Session: First Autoprogression Review Finding

## Status

- captured

## Frame

- Trigger: explicit maintainer invocation asking why the first review finding in the autoprogression workflow was found, and what lesson matters most.
- Trigger type: explicit maintainer request / workflow retrospective.
- Scope:
  - `docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/code-review-m1-r1.md`
  - `docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-resolution.md`
  - `docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/code-review-m1-r2.md`
  - `docs/workflows.md`
  - `.agents/skills/code-review/SKILL.md`
  - `.agents/skills/workflow/SKILL.md`
- Evidence in scope:
  - `CR-M1-1`, the undeclared PyYAML dependency in the M1 broad-smoke classification validation path.
  - Review-resolution evidence showing the finding was accepted and resolved by removing the undeclared dependency.
  - Workflow and skill guidance requiring workflow-managed automated code-review to be independent, first-pass, diff-grounded, and routed to review-resolution on `changes-requested`.
- Explicit exclusions:
  - no new workflow policy from this learn session;
  - no claim that all future autoprogression findings will be caught;
  - no topic update without contributor-confirmed durable routing;
  - no PR readiness, branch readiness, or CI status claim.
- Prior learnings reviewed:
  - `docs/learn/README.md`
  - `docs/learn/sessions/2026-06-24-clean-review-outcome-preflight-first.md`
  - `docs/learn/topics/review-artifact-recording.md`
  - `docs/learn/topics/ci-selector-routing.md`
- Session record path: `docs/learn/sessions/2026-06-27-first-autoprogression-review-finding.md`

## Observe

### O1 - The finding was visible because review inspected the actual diff against contributor-runtime assumptions

Evidence:

- `code-review-m1-r1.md` records `CR-M1-1` at `scripts/validate-broad-smoke-classification.py:12` and `scripts/test-select-validation.py:21`.
- The evidence says the new validator and tests imported `yaml`, no existing repository use or dependency manifest declared PyYAML, and the validator had become part of selected-CI routing.
- The required outcome was not vague: M1 validation must not rely on an undeclared third-party parser.

Observation:

The review found the issue because it checked the implementation as runnable repository validation, not only as plausible code. The critical question was: "Can an ordinary contributor execute this selected-CI path from declared repository dependencies?" That question exposed the hidden dependency.

### O2 - Autoprogression helped because it preserved an independent stop point instead of continuing on implementation momentum

Evidence:

- `docs/workflows.md` says workflow-managed automated `code-review` emits a first-pass review record before review-driven fixes begin, and first-pass `changes-requested` continues to `review-resolution`.
- `.agents/skills/code-review/SKILL.md` requires independent-review mode, a first-pass review record, evidence, required outcome, safe resolution path, and milestone-aware handoff.
- `code-review-m1-r1.md` records `Status: changes-requested`, `Next stage: review-resolution`, `Milestone closeout: resolution-needed`, and `Verify readiness: not-claimed`.

Observation:

The automation did not skip review just because M1 validation had passed locally. It created a separate gate where the reviewer could challenge the dependency boundary, block M1 closeout, and force an explicit resolution before M2 began.

### O3 - The finding was useful because it was mechanically actionable and re-reviewed

Evidence:

- `review-resolution.md` records `CR-M1-1` as accepted and resolved.
- The chosen action removed the PyYAML dependency while preserving classification freshness and baseline artifact validation.
- Validation evidence included the classification validator, broad-smoke tests, registered change evidence tests, and a search confirming no YAML imports remained.
- `code-review-m1-r2.md` later closed M1 with no material findings.

Observation:

The finding did not become a vague warning or a chat-only concern. It had a concrete safe fix, validation targets, and a re-review loop. That made it compatible with autoprogression rather than a reason to abandon automation.

### O4 - The most important lesson is about preserving adversarial gates inside automation

Evidence:

- The workflow contract intentionally separates `implement`, `code-review`, `review-resolution`, `explain-change`, and `verify`.
- The finding was not discovered by final broad-smoke or by implementation self-checks. It was found by independent review of the new validation path and dependency assumptions.
- The issue would have undermined contributor validation even though the code could pass in an environment that happened to have PyYAML installed.

Observation:

Autoprogression is only safe when it automates the movement between gates, not the removal of gates. The key value was not speed. The key value was that the automated workflow still forced an independent reviewer to ask whether the new proof surface would work for contributors under declared repository assumptions.

## Classify

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | observation | observation | None | Review record evidence | The dependency issue explains why this specific finding was catchable. |
| O2 | observation | observation | None | Workflow and code-review skill evidence | The existing autoprogression contract already required the independent stop point. |
| O3 | observation | observation | None | Review-resolution and re-review evidence | The finding was resolved through the existing review-resolution loop. |
| O4 | durable-lesson candidate | observation | Potential future workflow/topic update only if confirmed and recurring | Contributor confirmation not yet recorded for routing | This is reusable, but this session has one event plus existing workflow support. Under learn rules, keep it as a session observation rather than adding topic-level guidance from a single finding. |

Contributor confirmation status: not confirmed for routing. The maintainer asked for the lesson, but did not ask to update a topic, skill, spec, or workflow artifact.

## Route

- Observation routing: kept in this session record.
- Durable lesson routing: not created.
- Artifact update routing: not created.
- Decision routing: not created.
- Direction routing: not created.
- Process follow-up routing: not created.

## Direct Answer

We were able to find the first autoprogression review finding because the workflow still had a real independent review gate. M1 had passing validation, but `code-review` inspected the actual diff and asked a different question: whether the newly selected validation path depended on anything the repository had not declared. That exposed the PyYAML import before the change advanced.

The most important lesson is:

```text
Autoprogression is safe only when it preserves adversarial review gates.
It should automate handoff between proof stages, not convert implementation
confidence into review confidence.
```

In practical terms: keep first-pass review independent, diff-grounded, and allowed to stop the workflow. The value of the first finding was not that the bug was exotic; it was that the workflow caught a boring but real contributor-runtime defect before it became part of the validation contract.

## No Durable Topic Rationale

No topic file was updated in this session. The observation supports the existing workflow contract, but a single successful catch is not enough by itself to create new durable topic guidance or policy. If similar autoprogression findings recur, or if the maintainer confirms this should become curated guidance, route a later session to `docs/learn/topics/workflow-stage-order.md` or an action-owning workflow/spec artifact.
