# Independent parallel tests and concise validation design

Owning change: [independent parallel tests](../changes/2026-09-13-independent-parallel-tests/change.json).

## Challenge

The merged three-model design gives Skill, CLI and Engineering clear product responsibilities, but its validation realization still repeats expensive proof and leaves many suites serial because their isolation has not been assessed. A serial catalog entry does not establish that its individual cases cannot run concurrently. The design needs a clear completion standard for resolving that uncertainty and removing unnecessary work.

The passing [PR #188 CI run](https://github.com/xiongxianfei/rigorloop/actions/runs/34743370429) took 18m54s. The same executor regression suite ran in focused and broad validation, taking 339.54s and 332.29s respectively. Together those exclusive executions consumed about 11m12s. Each repeats full normal, individual sequential and individual parallel comparisons of the three adopted suites. Raising the hosted timeout allowed completion but did not reduce this work.

Duplicate test cases and duplicate execution are separate problems: different cases may provide the same protection, while one useful case may also be scheduled unnecessarily more than once. Both need explicit treatment without losing required regression or integration coverage.

## Goals

1. Refine the design so ownership, distinct proof obligations, case independence and necessary execution are clear and consistent.
2. Remove genuinely duplicate cases and unnecessary repeated execution while preserving every distinct required failure detection and observation boundary.
3. Make retained automated test cases independently runnable and capable of concurrent execution within resource limits; refine or replace remaining cases that depend on shared mutable state or another case.
4. Reduce avoidable validation time while retaining complete discovery, truthful failures and useful diagnostics.

## Scope and non-goals

| User intent | Initial goal treatment | Scope budget treatment | Destination |
| --- | --- | --- | --- |
| Refine the design | in scope | core to this proposal | Engineering Validation owns the refinement; System and Engineering reconcile affected relationships while preserving the three main models. |
| Remove duplicate test cases | in scope | core to this proposal | Assess overlapping protection, consolidate redundant cases, and remove repeated execution of equivalent proof within one invocation. |
| Enable parallel cases and refine remaining serial cases | in scope | core to this proposal | Assess the remaining automated suites and repair case isolation, including their fixtures and nested resource demand. |
| Reconcile affected readers and execution metadata | in scope | same-slice dependency | Keep selection, execution, guidance and product-consumer proof consistent with the refined design. |

The initiative covers current repository-owned automated validation for published skills, the CLI and their engineering tooling, including executor, release, adapter, CLI, workflow, review and documentation suites. The existing 278 adopted cases remain protected. The largest costs are initial candidates for attention, not a limit that silently excludes other remaining serial cases. Delivery will bound the actual current inventory and allocate reviewable implementation slices; unassessed cases cannot disappear into an unspecified follow-up.

This proposal does not authorize test deletion or implementation. It excludes a new Test model, public runner or skill, validation-result caching, distributed CI, a permanent benchmark or test ledger, product-feature changes, and weaker review or release gates. Historical evidence and archived records retain their identities. Live release/publication actions remain separately authorized.

## Governing principle

Every retained test case should prove a distinct required behavior and own the state needed to execute independently.

## Proposed direction

Refine the existing [Validation model](../design/engineering/validation.md), with [Engineering](../design/engineering/engineering.md) and [System](../design/system.md) retaining their integration responsibilities. Distinguish the behavior being proved, the case that proves it, the suite that organizes cases, and the execution needed for a particular validation scope. Clarify when repeated execution contributes distinct protection. Detailed model changes and realization belong to Design, followed by Delivery allocation.

Assess duplication by governing obligation, failure detection, configuration and observation boundary. Consolidate or remove a case only after retained or replacement proof preserves its distinct protection. Similar names, low runtime, age, or passing remaining tests are insufficient. Equivalent proof requested by multiple phases should execute once within that invocation and satisfy each requesting scope. Different inputs, configurations, changed subjects or independently required fresh observations remain distinct work. Every new invocation executes again; this introduces no result cache.

Resolve each remaining serial case through an isolation assessment. Refine setup, cleanup and resource ownership; replace dependencies on other cases with self-contained scenarios; bound nested execution. Tests of ordering, locks, failures and sequential behavior remain valuable and can themselves run concurrently when their resources are isolated. A scenario may contain ordered internal steps. An unassessed case may run conservatively during migration, but that is not the completed design. A case that cannot meet the independence goal must be redesigned or replaced; deletion requires redundant protection or explicitly retired behavior. An unresolved required obligation blocks completion rather than justifying removal or a permanent serial exemption.

Separate case independence from scheduling capacity. A single-worker request, necessary artifact dependency or declared resource budget may serialize otherwise independent work. The intended outcome is safe eligibility for parallel execution and actual use of available capacity, not forced overlap of every operation. Retain useful executor tests while reducing repeated exhaustive comparisons when they add no distinct protection.

## Feasibility

Assessment: feasible to enter Design using the existing catalog, process isolation and worker-budget mechanisms. The current implementation already runs selector, lifecycle and metadata cases independently. The executor comparison helper explicitly exercises normal, sequential and reversed parallel populations. Many remaining serial entries have no isolation assessment, while inspected executor and release fixtures already use temporary resources. These are credible refinement opportunities, not proof that the full remaining inventory is safe today.

The baseline timing above identifies duplicate execution as a concrete source of cost; it does not establish that any two distinct cases are redundant or guarantee a particular speedup. Fresh-process startup, repeated setup, nested workers and actual shared resources may limit gains. Detailed inspection must establish equivalence before consolidation and isolation before parallel adoption. Missing required protection, an inseparable external resource or an unclear owner would block the affected design decision. None currently prevents proposal-level Design work.

## Impact and major trade-offs

This extends case independence beyond the previous initiative's initial three-suite adoption and replaces indefinite serial defaults with an explicit refinement obligation. It can affect many test families and should be delivered in reviewed slices. Isolation can increase setup cost, and careless consolidation could hide boundary-specific regressions. Preserve required negative, recovery and real product-consumer proof before relying on reduced tests or faster execution. Performance observations inform the work; lower test counts and larger timeout limits do not establish success.

## Decision requested

Approve the combined direction: refine the existing design, remove proven duplicate cases and execution, and resolve remaining serial cases so retained automated tests can run independently and concurrently within their resource budgets. Keep all three goals in scope. Proposal approval permits detailed Design and review; it does not approve particular deletions, implementation, adoption or publication.
