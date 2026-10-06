<!-- Generated from rem/practices/engineer-change/README.md; source SHA-256 dbc0af525271cd02dccdf45e9f624f72b27f9ff618bfed16579f5cea593759d4. Edit the owning REM source. -->

# Engineer a change through REM

## Goal and entry

Turn an incoming need into coherent requirements, design, realization and assessed outcomes.
Identify the system boundary, applicable current definitions and Baseline, source of the request, stakeholders and action authority.
Use [Requirement Analysis](https://github.com/xiongxianfei/rigorloop/blob/main/rem/methods/requirement-analysis.md) to decide whether the request warrants reuse, refinement, a new requirement, deferral or no change.

## Engineering cycle

1. Reconcile the RR against current requirements, Scenarios, Features and constraints, preserving the source and disposition.
2. Establish or refine justified IRs with all seven [5W2H](rem-methods-5w2h.md) questions. Apply the existing [open-question rule](https://github.com/xiongxianfei/rigorloop/blob/main/rem/methods/requirement-analysis.md#keep-one-consequential-open-question) without concealing uncertainty.
3. Use [Scenario Analysis](https://github.com/xiongxianfei/rigorloop/blob/main/rem/methods/scenario-analysis.md) to confirm durable Features and governed black-box Scenarios for the affected need.
4. Derive or refine assessable SRs with exactly one parent IR each through Requirement Analysis. Requirement acceptance is distinct from completed design.
5. Use [Functional Analysis](https://github.com/xiongxianfei/rigorloop/blob/main/rem/methods/functional-analysis.md) to confirm the Functions required by SRs and reconcile Feature realization; retain the existing Function-coverage obligation for design completeness.
6. Establish coherent Module hierarchy and use [Architecture Allocation](rem-methods-architecture-allocation.md) to assign each Function one accountable primary Module.
7. Derive justified ARs under their single parent SR and allocate each to exactly one accountable Module; reconcile behavior and obligation allocations without duplicating ancestor ownership.
8. Define significant Interfaces, explicit descendant exposure and state/data ownership using [Architecture Design](rem-methods-architecture-design.md).
9. Use [realization design](rem-methods-realization-design.md) for material software, runtime, persistence, deployment, interaction and technology choices under their Module/Interface owners.
10. Select and assess [architecture views](rem-methods-architecture-views.md#view-selection-and-tailoring) for the relevant questions, preserving source meaning and recording concern coverage.
11. Plan [verification](https://github.com/xiongxianfei/rigorloop/blob/main/rem/methods/plan-and-assess-verification.md) and [intended-use validation](https://github.com/xiongxianfei/rigorloop/blob/main/rem/methods/validate-stakeholder-outcomes.md) early enough to affect design, then realize and assess the authorized scope.
12. Review the engineering result and evidence under the project's governance, resolve or explicitly disposition remaining obligations, and establish the new Baseline through controlled change.

The cycle is iterative.
Architecture can expose a missing obligation, implementation can expose missing behavior, and assessment can require a correction to the need or solution.
Return to the responsible owner and reconcile affected relationships; the sequence does not authorize otherwise unapproved work.

## Exit and application

State the actual result: justified no change, a reviewable requirement/design basis, a realized slice awaiting evidence, or an assessed outcome under the project's governance.
Preserve current definitions, applicable rationale, unresolved obligations and evidence scope.
A completed worksheet or example establishes neither approval nor requirement satisfaction.
Concrete stage names, review cadence, storage and publication permissions remain project decisions under [Operational Support](https://github.com/xiongxianfei/rigorloop/blob/main/rem/models/operational-support.md).

Read the [worked example](rem-practices-engineer-change-WORKED-EXAMPLE.md) to see the retained cardinalities, view selection and two distinct assessment plans applied together.
