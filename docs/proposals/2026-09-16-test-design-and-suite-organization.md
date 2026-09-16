# Refine test design and organize the complete test suite

## Challenge

The current [Validation Design](../design/engineering/validation.md) establishes ownership, meaningful failure detection and independent execution, but contributors still need clearer guidance for structuring test modules, scenarios, fixtures and helpers. The implementation applies those principles unevenly: locating a protected behavior or understanding its setup can require navigating large files with several responsibilities.

At inspected revision `1195dfb261176d500e319662e2ffad5429cb63be`, [test-skill-validator.py](../../tests/skill/test-skill-validator.py) contains 5,617 lines spanning validator inputs, resource contracts, portability, individual skill guidance and workflow checks. Its use of test classes has not prevented this accumulation. Size identifies a maintenance concern; it does not establish that a case is redundant or that its protection may be removed. Moving code between files alone would leave weak assertions and unnecessary coupling unresolved.

## Goals

- Make the existing testing Design concrete enough to guide everyday test authoring, organization and review, with practical examples.
- Assess the complete repository and package test population, reorganizing groups where ownership, readability or isolation needs improvement.
- Preserve useful failure detection while strengthening weak tests and justifying any consolidation or retirement.
- Keep scenarios independently understandable and runnable, with proportionate fixture and helper reuse.
- Finish with an explicit disposition for every inventoried group, including justified retention of groups that already meet the refined Design.

## Scope and non-goals

The inventory includes Skill, Validation, Packaging and Release tests, package-owned CLI, Records and Installation tests, generated or parameterized cases, imported suites, fixtures and test helpers. Include tests reached through repository commands and CI even when they are outside the obvious test directories. The complete population receives assessment; assessment does not require rewriting every case.

| Initial user intent | Treatment | Destination |
| --- | --- | --- |
| Refine the test Design with more detail | in scope | Extend Validation's existing ownership with practical authoring and organization guidance. |
| Reorganize all test cases | in scope | Assess the entire inventory and change every group that needs improvement; retain suitable groups explicitly. |
| Decide how test scripts should use object-oriented structure | in scope | Select lightweight classes where useful and composition for shared setup, preserving existing frameworks. |
| Improve quality as well as file organization | in scope | Assess protected failures, assertions, fixtures and dependencies alongside placement. |

| Work item | Scope budget treatment | Boundary |
| --- | --- | --- |
| Detailed testing guidance and complete inventory assessment | core to this proposal | Use the existing Design, plan and evidence owners; no separate test specification or permanent per-case ledger. |
| Oversized Skill suite | first-slice candidate | A concrete starting point for the later delivery allocation; completing it cannot close the full initiative. |
| Remaining Validation, Packaging, Release and package tests | separate implementation slice | All populations remain required scope; Delivery determines coherent grouping and order. |
| Fixture/helper ownership, discovery, selectors and direct/CI callers | same-slice dependency | Reconcile consumers whenever a selected reorganization affects them. |
| Contributor guidance and affected published test guidance | same-slice dependency | Reconcile only guidance affected by the refined contract, through canonical sources and applicable packaging procedures. |
| Framework replacement, new runner, changed product behavior or release policy | out of scope | Preserve Python unittest, native Node tests and the existing execution system. |
| Fixed file-size limits, deletion quotas or an automated semantic-quality gate | out of scope | Judge clarity and protected outcomes; do not substitute counts or phrase presence for adequacy. |

The [test organization plan](../plans/2026-09-14-validation-test-organization.md) and [risk-driven test redesign plan](../plans/2026-09-15-risk-driven-test-redesign.md) provide prior allocation and useful context. The [complete skill refinement proposal](2026-09-15-refine-skills-and-retire-stale-support.md) also overlaps test relevance assessment. Design and Delivery must reconcile those scopes with the current implementation, retain useful completed work and identify remaining obligations without overwriting historical judgments or treating a prior pilot as complete suite organization.

## Governing principle

Organize tests so a contributor can understand, run and maintain the protection of a required behavior without weakening it.

## Proposed direction

Refine the existing Validation Design to explain cohesive module and class responsibilities, when to split groups, naming, fixture ownership, helper reuse, scenario readability and test maintenance. Include examples that connect a required behavior and plausible defect to a sufficient observation boundary and an independently justified expected result. Preserve the distinction between executable or structural proof and independent assessment of instruction quality.

Use lightweight test classes where they clarify related scenarios and lifecycle management. Prefer composition for sharing setup and resource operations, with simple functions for ordinary fixture data. Avoid making deep inheritance, broad mixin assemblies or a universal test framework the organizing principle. Detailed helper interfaces and the exact file layout belong to Design.

Assess each inventoried group against its current obligations. Retain suitable groups; separate mixed responsibilities; strengthen weak assertions; and consolidate or retire cases only when their distinct protection is adequately replaced, already retained elsewhere or no longer required by the owning contract. Keep uncertain cases until their contribution is resolved. File length and repeated setup are assessment signals, not automatic removal criteria.

Carry the complete scope through independently reviewed delivery slices. Preserve required discovery, individual execution, CI selection, isolation and observable failure detection as tests and consumers change. Delivery owns the concrete migration sequence and proof allocation. Completion requires accounted-for inventory coverage and resolved protection decisions across all included populations.

## Feasibility

Assessment: feasible within the current repository structure and test frameworks. Validation already owns the quality and maintenance principles; [Skill contract tests](../../tests/skill/skill_contract_tests.py) demonstrate smaller behavior groups, and [release fixture helpers](../../tests/engineering/release/release_fixture_helpers.py) demonstrate reusable setup without coupling to another test class's lifecycle. These are implementation precedents, not a completed adequacy assessment.

The material constraints are discovery and selector compatibility, imported or generated populations, realistic filesystem/process/package behavior, and uncertainty about the purpose of older assertions. Initial source inspection establishes the need and available approach, not a complete inventory or runtime baseline. No blocker to beginning Design is known. Missing consumer information or unproven replacement protection blocks the affected later migration or removal until resolved.

## Impact and major trade-offs

The work adds review and migration effort across the whole suite. Smaller cohesive groups should make ownership and failures easier to understand, but excessive abstraction could hide scenario intent and excessive splitting could fragment related behavior. Detailed Design must balance those costs. Existing useful structure should remain where it meets the contract.

The proposal commits to complete assessment and preserved protection, with no promised reduction in test count, line count or runtime. Any affected contributor or published guidance must remain consistent with its owning Design. Product capabilities, review authority and external release permissions remain outside this initiative's change scope.

## Decision requested

Approve refinement of the existing testing Design and assessment and necessary reorganization of the complete test inventory, using the scope and preservation principles above. Carry this direction through independent Proposal Review, affected Design reconciliation and reviewed delivery allocation. Approval selects the direction; exact source moves, case removals, helper designs and verification commands require their downstream owners. This proposal does not establish implementation or final verification readiness.
