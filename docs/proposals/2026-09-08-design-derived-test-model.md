# Design-Derived Test Model

Owning change: [2026-09-08-design-derived-test-model](../changes/2026-09-08-design-derived-test-model/change.json)

## Challenge

Tests should explain which design obligation they protect and which meaningful defect they would detect. Generating cases from implementation details, adding similar cases without a distinct purpose, or preserving obsolete expectations can increase maintenance cost without increasing confidence.

RigorLoop already requires requirement-to-proof allocation and boundary-focused verification. The missing direction is a coherent Test model that makes those expectations usable across test creation, review, maintenance, and removal. This proposal responds to the requested improvement; it does not claim that a repository-wide audit has demonstrated which existing cases are useless.

## Goals

Derive test objectives and expected outcomes from approved Design requirements, invariants, boundaries, interactions, and compatibility obligations. Make each retained test or coherent test group explain its contribution to confidence. Stop speculative case proliferation and remove or consolidate tests whose value is demonstrably absent or redundant, while preserving meaningful regression and failure-path protection.

## Scope and non-goals

| Work | Treatment | Boundary |
| --- | --- | --- |
| Test model policy for deriving, evaluating, and maintaining tests | core to this proposal | One authoritative model Design; exact responsibility boundaries are Design work |
| Alignment of Design, planning, implementation, review, and Verify consumers | same-slice dependency | Identify affected instructions, templates, examples, and packaged guidance; preserve specialist ownership |
| Audit and justified cleanup of existing tests | separate implementation slice | Included in the initiative; Delivery must name bounded suites and coverage-preservation evidence before deletion |
| Repository-wide conversion of all historical tests and records | out of scope | No automatic migration or blanket deletion |

The current step establishes direction before detailed Design. Both design-derived test creation and removal of unnecessary tests remain in scope. Exact cleanup targets and completion bounds require an inventory; this proposal does not promise that every existing suite will be rewritten.

No new lifecycle gate, mandatory public skill, record type, schema version, CLI readiness decision, test-count target, or coverage-percentage target is selected. Historical contracts retain their meaning. Published guidance must be usable without RigorLoop's internal Design checkout or internal requirement identifiers.

## Governing principle

> Every test should protect a justified engineering obligation; every removal should explain why that protection remains sufficient or is no longer required.

## Proposed direction

Establish a Test model with one authoritative living Design document. It should own shared criteria for test purpose, derivation, protective value, and maintenance. The Test model defines test-quality and maintenance criteria; responsible specialist reviewers and Verify apply those criteria to the actual plan, tests, and evidence. It does not independently approve a suite, declare evidence current, or waive a review obligation. Product and component Designs remain the source of required behavior; Delivery allocates verification; implementation owns concrete test mechanics. Review and Closeout retains assessment authority policy, independence, judgment meaning, evidence applicability, and closeout consequences. Workflow coordinates these responsibilities, and Record Format and CLI retain representation and mechanics.

Use a traceable relationship from the governing Design or explicit engineering obligation through a test objective and observable expected outcome to concrete proof. Allow many-to-many mapping and coherent groups instead of requiring an administrative record for every test function. Assertions should distinguish correct behavior from a plausible violation, rather than simply mirror the current implementation.

Select cases for distinct outcomes or material hazards, including rejection, state transitions, retries, recovery, authority boundaries, compatibility, and cross-component interactions when applicable. A documented regression or discovered hazard can reveal a Design gap; route that gap to its owner rather than discarding the test or treating observed behavior as the approved contract. Property-based and randomized testing remain valid when they exercise a justified invariant with interpretable failure evidence.

Evaluate existing tests for retention, strengthening, consolidation, replacement, or removal. A removal must account for the obligation, the distinct failure it detects, remaining proof, and any intentionally retired behavior. Similar names, lack of requirement labels, execution cost, or a passing suite alone do not establish redundancy. Uncertain protection calls for investigation. Do not delete a failing test merely to make validation pass.

Design should define the ownership map, sufficient rationale for test changes, and a small set of representative acceptance examples. Consumer alignment must replace competing policy definitions rather than add another universal manual. Concrete cleanup and any automation follow approved Design and Delivery allocation.

## Feasibility

**Assessment: Feasible as a policy model and coordinated consumer refactor; cleanup scope requires an inventory.**

The existing [plan quality contract](../../skills/plan/SKILL.md) already maps requirements to verification groups and concrete proof, requires meaningful negative and integrated cases, and rejects Cartesian scenario inventories. Its [boundary verification guidance](../../skills/plan/references/boundary-and-negative-verification.md) derives cases from outcome partitions and rejection invariants. [Review and Closeout](../design/review-closeout/review-closeout.md) already owns the policy for assessing evidence sufficiency and applicability; the responsible specialist reviewers and Verify make the actual assessments. These provide a credible basis for clarification and extraction.

Before implementation, Design must reconcile those owners and distinguish current policy from historical contracts. Delivery must identify concrete cleanup candidates and how their retained protection will be assessed. No specific test has yet been established as safe to remove, and no runtime or token saving is claimed.

## Impact and major trade-offs

Explicit purpose can reduce redundant tests and make failures easier to interpret, but excessive traceability could become another maintenance burden. Group-level rationale and selective guidance should keep the work proportional. Cleanup also carries a risk of losing undocumented regression knowledge, so it needs semantic review of what each candidate protects, not just count or runtime comparisons.

## Decision requested

Approve designing a Test model that makes test creation and maintenance follow Design obligations and supports evidence-backed removal of unnecessary tests. Include coordinated consumer alignment and a bounded existing-suite cleanup in downstream planning.

Approval authorizes detailed Design. It does not approve specific deletions, final ownership relocation, exact document layout, implementation, migration, or activation. Independent Proposal Review remains required before governed Design progression.
