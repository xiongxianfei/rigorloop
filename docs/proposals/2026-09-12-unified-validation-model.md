# Build One Validation Model and Retire Superseded Machinery

## Challenge

RigorLoop defines test quality in the Test model while validation selection, execution, parallelism and caching remain distributed across legacy specifications, architecture, ADRs and scripts. Contributors must assemble one validation story from several owners and historical layers. Adding another model without consolidating those responsibilities and removing their superseded sources would increase the burden.

The user selected one Validation model combining test quality and execution, independent test cases that can run concurrently, and no validation cache. The initiative must also leave a clearer, smaller repository by removing obsolete designs, scripts and supporting material.

## Goals

Establish one current Validation owner for proof-quality and maintenance criteria, applicable-check selection, execution and truthful result reporting. Preserve necessary engineering meaning while replacing the separate Test owner and selected legacy validation contracts.

Make test cases independent by default and support bounded parallel execution of independent work. Remove validation-result caching and its exclusive machinery. Complete actual source and implementation cleanup alongside adoption, so contributors can understand and use validation without reconstructing current rules from superseded documents.

## Scope and non-goals

| User intent or dependency | Initial goal treatment | Scope budget treatment | Boundary |
| --- | --- | --- | --- |
| One Validation model combining Test and execution | in scope | core to this proposal | Transfer necessary Test criteria and selected validation selection, execution and reporting responsibilities into one owner. |
| Independent tests and parallel execution | in scope | core to this proposal | Establish case isolation and order independence; apply bounded concurrency to independent cases and checks, with explicit necessary resource constraints. |
| No validation cache | in scope | core to this proposal | Retire validation-result lookup, persistence, execution skipping and exclusively supporting code, guidance and checks. |
| Remove old designs, scripts and related clutter | in scope | core to this proposal | Remove superseded sources and obsolete machinery within the affected Test/validation responsibility, including exclusive fixtures, metadata and wrappers where justified. |
| Reconcile current consumers | in scope | same-slice dependency | Update affected governance, System, skills, references, selectors, CI and package consumers so adoption leaves no competing current contract. |
| Unrelated repository cleanup | out of scope | out of scope | No blanket deletion of old files, unrelated model consolidation or redesign of other product responsibilities. |

Product models retain required behavior and domain invariants. Delivery retains concrete verification allocation. Review and Closeout retains independent assessment, evidence applicability and approval authority; Workflow, Record Format and CLI retain coordination, representation and recording mechanics. Release and Distribution retain their operation-specific requirements and permissions.

No new lifecycle gate, public skill, hosted execution service, general scheduling platform, permanent per-test ledger or replacement cache is selected. Dependency-download caches and hashes used for package integrity or safe persistence are outside validation-cache retirement. Publication and customer policy activation remain separately authorized.

## Governing principle

Keep one necessary validation contract, with independent proof, simple execution and no superseded machinery.

## Proposed direction

### Consolidate proof quality and execution

Create one living Validation model that reconciles test derivation, meaningful assertions, protective value and maintenance with explainable selection, execution and result reporting. Tests are one validation mechanism alongside structural, static and package-integrity checks. The model consumes product obligations without redefining them or granting approval through a passing command.

Transfer the necessary Test requirements and selected legacy operational obligations through an exact ownership and source-disposition map. Preserve requirement identities and meaningful decisions where still applicable; explicitly reconcile changed or retired obligations. Avoid copying entire historical documents into a larger model. Model approval alone does not adopt the transfer.

### Make independence support parallel execution

Test cases should own their mutable setup and cleanup and remain runnable without another case's prior execution or outcome. Shared immutable fixtures are compatible with this direction. An integration scenario may contain ordered steps while remaining independent of other scenarios.

Independent cases and validation checks should normally be eligible for bounded concurrent execution. Necessary exclusive resources or dependencies require explicit constraints rather than accidental ordering. Existing suites need scoped isolation assessment and correction; the proposal does not assert that every current case is already safe to run concurrently. Preserve failure visibility, meaningful diagnostics and accurate completion reporting under concurrency and interruption. Design resolves the execution boundaries and resource policy without introducing a second competing runner by default.

### Remove caching and simplify the maintained surface

Retire the existing validation cache as part of this initiative. Validation commands execute their selected checks without automatic cache-based substitution. Responsible assessors may still judge existing evidence applicable under Review and Closeout; that judgment does not require an execution cache or turn prior results into fresh execution.

Remove the superseded Test Design, selected legacy validation design sources and obsolete scripts once necessary content and actual consumers have coherent replacements or explicit retirement decisions. Include exclusive tests, fixtures, configuration, wrappers and documentation in that assessment. Retain useful existing mechanisms and shared safeguards; a filename's age or a passing reduced suite does not prove redundancy.

Do not replace removed files automatically with archive copies, redirects, dormant compatibility branches or a new maintenance catalogue. Mixed sources retain only their necessary remainder. Preserve historical record bytes, identities and judgments. Where a removed source was relied upon, preserve the basis necessary for current reliance or explicitly cease that reliance without retargeting old approvals.

Cleanup is required delivery scope, not an optional follow-up after creating the model. Design identifies exact source and consumer boundaries; Delivery allocates reviewable adoption slices and proportionate proof. Completion requires an implemented, reviewed replacement, justified removal of superseded machinery, and successful Verify. Any necessary retained remainder has an explicit owner and reason.

## Feasibility

**Assessment: feasible as a coordinated model consolidation and implementation cleanup.** The [Test model](../design/test/test.md) already defines test derivation and protective-value criteria. [System](../design/system/system.md#candidate-models-and-legacy-source-ownership) identifies the remaining validation execution sources. Existing [selection](../../specs/test-layering-and-change-scoped-validation.md), [preflight](../../specs/validation-execution-performance-and-preflight.md) and [parallelism](../../specs/broad-smoke-safe-parallelism.md) contracts supply concrete starting points rather than requiring a new execution system.

The [selector implementation](../../scripts/validation_selection.py) already carries parallel-safety metadata. The [lifecycle validator](../../scripts/validate-artifact-lifecycle.py) actively consumes the [cache helper](../../scripts/validation_cache.py), so cache removal requires coordinated caller and contract changes. The [cache contract](../../specs/validation-idempotency-and-cache-hit-safety.md) already separates cache hits from final actual-run proof. These facts support the direction but do not establish a complete dependency inventory or safe parallelism for every case.

Design must resolve exact source dispositions, live command consumers, shared mutable resources and necessary compatibility changes. Unknown protection must be investigated rather than silently removed. No measured runtime improvement or deletion count is claimed. Current owners and code were inspected directly because the project map predates the current v3-only runtime boundary.

## Impact and major trade-offs

A combined owner reduces fragmented guidance but requires disciplined separation of proof criteria, execution mechanics and external assessment authority inside the model. This explicitly changes the earlier direction that retained Test separately and treated Validation Execution as an optional future owner; historical approvals do not cover the new subjects.

Removing caching may increase repeated unchanged execution. Independence and bounded concurrency can reduce avoidable waiting, but no performance gain is promised before measurement. Updating real callers and preserving useful failure detection may require more work than simply deleting old scripts. A smaller maintained repository is the intended outcome, with necessary behavior and evidence preserved rather than a deletion quota or mandatory benchmark programme.

## Decision requested

Approve one Validation model combining the current Test responsibility with selected validation selection, execution and reporting responsibilities; independent tests and bounded parallel execution; retirement of validation-result caching; and coordinated removal of superseded designs, scripts and exclusive supporting material in the same initiative.

The next assessment is independent Proposal Review, followed by exact Design reconciliation and delivery planning. This proposal does not itself remove current owners or scripts, approve implementation, or claim completed adoption.
