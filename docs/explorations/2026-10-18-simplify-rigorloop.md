# Simplify RigorLoop

## Topic and decision supported

Help the maintainer reduce the effort needed to understand, use and maintain RigorLoop while retaining trustworthy changes. This is advice, not adoption of a new workflow.

## Inputs examined

Current checkout at `486cb998`: [Vision](../../VISION.md), [Constitution](https://github.com/xiongxianfei/rigorloop/blob/dc55c7f7a565ff0e61735fcea6b8c2bef2ef5f72/CONSTITUTION.md), [entry instructions](../../AGENTS.md), [composition](../../design/architecture/composition.md), [ownership](../../design/support/ownership.md), [workflow](../../design/architecture/modules/MOD-017-engineering-governance/modules/MOD-006-engineering-change-control/workflow.md), [assessment](../../design/architecture/modules/MOD-017-engineering-governance/modules/MOD-007-engineering-verification-and-assurance/assessment.md), [plan navigation](../plan.md), and [guidance projector](../../scripts/project-operational-guidance.py). Counts below use tracked files and whitespace-separated Markdown words; they are inventory observations, not measurements of reader effort.

## Facts, assumptions, and unknowns

### Established facts

- `docs/plans/` contains 197 Markdown files; `docs/proposals/` contains 171. Together they contain approximately 1.26 million words. Their presence does not establish that they are obsolete.
- `design/` contains 76 Markdown files with approximately 247,000 words. `rem/` contains 78 with approximately 52,000 words. JSON and generated views are additional surfaces.
- There are 20 authored skill entrypoints. The projector copies operational guidance, schemas and selected REM material into skill resources; package duplication is partly deliberate, not separate authored authority.
- The standard workflow has Requirement, integrated Design, Delivery and whole-change Code Review, followed by distinct final Verify. Requirement reuse still requires Requirement Review.
- Existing policy already permits scoped reads, evidence reuse and recording only consequential transitions. It also permits retiring historical material after resolving current dependencies and preservation obligations.

### Important assumptions

The desired improvement is less reading, coordination and maintenance for ordinary work, while preserving correctness, resumability and meaningful review. File count alone is not the objective.

### Material unknowns

We have not measured typical time spent reading, recording, waiting for decisions or running checks. We have not established which older plans still support current decisions or whether resource duplication materially slows installation or execution.

## Options

### A — Reduce clutter under the existing workflow

Retire completed narratives after checking dependencies; shorten entry guides; consolidate repeated rule explanations under existing owners; load specialist detail only when needed; record once at a meaningful handoff. Retain all current approval gates and runtime contracts.

This is the least disruptive direction and helps navigation. It cannot remove the coordination cost of mandatory upstream reviews for otherwise straightforward work.

### B — Simplify the workflow as well as its presentation

Apply A, then amend the policy so one ordinary change proceeds through understanding the request, implementation with evidence, independent review and a concise verification closeout. Reuse current requirement/design owners without manufacturing new documents. Require separate upstream decisions when changed obligations, architectural boundaries, migration, security or unresolved uncertainty justify them. Keep one workflow with conditional work, rather than multiple named modes.

Keep canonical engineering definitions and operational evidence separate, but provide one concise Change summary. Expose a primary task entrypoint and make specialist skills available on demand. Retain SQLite initially; hide transport envelopes and revision mechanics behind task-oriented commands rather than replacing storage during this simplification.

This addresses coordination as well as reading. It requires explicit reconciliation of the Constitution, workflow, assessment, skills, schemas where affected and meaningful tests. Current mandatory gates remain effective until that change is adopted.

## Decision criteria and comparison

| Criterion | A: cleanup | B: workflow simplification |
| --- | --- | --- |
| Reading and navigation | Improves | Improves |
| Routine review/handoff effort | Mostly unchanged | Can decrease |
| Adoption and implementation cost | Lower; dependency audit still required | Higher; changes governing policy |
| Main failure risk | Cosmetic cleanup leaves underlying friction | Overbroad exemptions omit a necessary decision |

## Questions requiring research

Before implementation, inspect a small set of actual changes: a prose correction, a bounded defect fix and a change to an external contract. Identify which artifacts, reviews and checks changed a decision or caught a defect. This is a bounded local assessment; no new benchmark service or evaluation platform is needed.

## Remaining uncertainty

No speedup or safe deletion quota has been established. Generated package resources may still need complete local copies for offline consumers. Historical approval must not be rewritten, and tests protecting current behavior cannot be removed merely because they are expensive.

## Recommended handoff

Recommend B, beginning with a bounded A cleanup. Prioritize the daily entry path and repetitive coordination before adding more REM coverage. Put durable lessons and still-applicable decisions under current owners; retire their superseded narratives through Git after dependency reconciliation. Generate copies for consumers without treating them as additional authored material.

Use the three representative changes to compare required reading, artifacts edited, manual recording, avoidable user interruptions and review usefulness. Preserve a reviewer's ability to explain what changed, why, what evidence supports it and what remains unresolved. Set improvement targets from those observations rather than inventing a percentage reduction.

The maintainer decides the direction; requirement-analysis and the workflow/assessment owners reconcile any selected policy changes. This exploration changes no current gate, requirement, executable or approval.

## Selected direction

The maintainer subsequently selected removal of intermediate approvals while retaining final independent review and verification. The [bounded implementation plan](../plans/2026-10-18-remove-intermediate-approvals.md) applies that choice. Historical cleanup and broader product simplification remain recommendations, not part of this implementation.
