# Complete model test design, aligned proof and execution cost

## Challenge

Contributors lack a sufficiently explicit procedure for deciding which supported behaviors, requirements and failure scenarios need proof. The existing shared rules establish useful principles, but applying them consistently across models still requires interpretation. Existing acceptance sections and passing suites do not establish that all important outcomes have adequate observations, representative fixtures and realized protection.

The [focused testing proposal](2026-09-17-model-test-design.md) selected separate catalogs for Release, Skill and Authoring and bounded executable refinements. The user's next objective extends coverage to every model, aligns actual tests and fixtures with that intent, and makes the execution cost of each test visible. Existing per-case timing provides a foundation, but reporting across execution modes and complete population accounting need reconciliation.

## Goals

- Make requirement and scenario selection repeatable and reviewable, with clear reasons for selected proof and explicit remaining gaps.
- Complete proportionate living test designs for every current model and section-owned responsibility, including parent interactions.
- Align executable cases, semantic review procedures and fixtures with those designs while preserving distinct required protection.
- Make every executable case's measured runtime attributable and useful for finding expensive setup and execution without weakening proof.

## Scope and non-goals

| User intent or necessary dependency | Intent treatment | Scope budget treatment | Owning destination |
| --- | --- | --- | --- |
| Clarify which features, requirements and scenarios need testing | in scope | core to this proposal | System's shared rules and model authorship guidance. |
| Complete test design for all models | in scope | core to this proposal | All current model owners, including section-owned responsibilities and parent composition. |
| Align actual tests and fixtures | in scope | separate implementation slice | Existing capability-owned suites, fixtures and review procedures, allocated against settled designs. |
| Measure the time each test costs | in scope | separate implementation slice | Validation's existing execution and reporting responsibilities. |
| Reconcile guidance, discovery, document admission and reporting consumers | in scope | same-slice dependency | Affected authored skills, templates, validators, selectors and generated consumers. |

The baseline is the current [System hierarchy](../design/system.md#responsibility-inventory), including the 24 document models declared in [model layout](../../scripts/lib/validation/model_layout.py). Adequate existing coverage remains usable; every owner is assessed, without requiring every document to gain a separate catalog. The complete scope includes Python and native Node cases, generated cases, inline and file-based fixtures, and supporting resource helpers.

This direction includes closing required realization gaps and assessing applicable semantic proof. A procedure requiring a future release or incident retains its applicability and cannot be represented as already executed. Any proposed narrowing or deferred required proof needs an explicit owner decision and limits the completion claim.

Non-goals are new product features, compatibility retirement, a replacement runner, JSON-driven execution, a universal mandatory case schema, a permanent per-function ledger, validation-result caching, a historical benchmark service, or new failing runtime thresholds. No model, case-count or code-coverage quota is selected. Publication and external service mutations are outside this initiative.

## Governing principle

Account for every supported obligation with sufficient proof, and spend additional testing effort where distinct failures create material risk.

## Proposed direction

Make the shared selection method explicit: identify supported outcomes and current requirements, describe plausible violations and their consequences, select meaningful scenarios, and choose the smallest observation boundary that establishes the required result. Risk determines depth and priority; execution cost informs efficient realization. Neither silently waives mandatory proof. Parent interactions and known regressions supplement requirement accounting.

Keep a reviewable relationship between the governing obligation, failure being detected, scenario, independent expected outcome, fixture strategy and existing or proposed realization. Permit many-to-many relationships between requirements, scenarios and executable cases. Group equivalent variations while retaining distinct authority, persistence, temporal and recovery observations. Use concrete independent walkthroughs where semantic judgment is required.

Complete and independently review the model designs before relying on them to reshape the suites. Then reconcile cases, fixtures, discovery and consumers in bounded owner slices. Establish retained or replacement protection before consolidating or removing tests. Keep design completeness, implemented proof, observed results and independent assessment distinguishable.

Build timing visibility on existing native discovery and execution. Account for the complete supported executable population across its actual callers, report attributable case costs and expensive groups, and distinguish total elapsed time from summed parallel work. Establish a baseline before suite changes and compare relevant measurements afterward with their execution conditions and limitations. Detailed report interfaces, measurement boundaries and delivery allocation belong to Design and Plan.

## Feasibility

Assessment: feasible using existing owners and tooling, with the amount of missing proof still to be established by the full coverage audit. [Shared rules](../design/test-design/rules.md) and [living test-design guidance](../design/skill/authoring/design.md#living-test-design) already support model ownership, meaningful scenarios, independent expectations and proportionate semantic methods. The three existing catalog packages provide examples and explicitly expose realization gaps.

The [executor](../../scripts/lib/validation/validation_execution.py) already records per-case elapsed time and supports optional broad-smoke JSON output. Common reporting for other execution modes and complete discovery accounting can extend that foundation; broad-smoke alone does not represent every suite. No new runner or external service is needed. Structural validation cannot establish semantic adequacy, and process-level timings do not isolate fixture or test-body cost. These constraints must remain explicit in the owning Designs. No known blocker prevents starting Design; uncertain coverage size must be resolved before committing to delivery estimates or claiming complete alignment.

## Impact and major trade-offs

Full-model coverage is materially broader than the earlier three-package adoption and needs independently reviewable delivery slices. Durable selection rationale and realization links add maintenance, so retain concise inline designs where sufficient and avoid duplicating native method inventories. Changes to the shared method require reconciliation of published guidance and its consumers. Runtime visibility may reveal expensive but necessary proof; improvements must preserve its observation boundary and isolation. Additional reporting must retain truthful failure, skipped and unstarted-work accounting.

## Decision requested

Approve the complete direction: explicit test-selection guidance, reviewed test design across all current model responsibilities, aligned cases and fixtures, and attributable runtime reporting through the existing executor. Preserve all four outcomes through downstream Design and delivery allocation. This proposal requests direction approval for subsequent Design; it does not establish review approval, implementation readiness or completed proof.
