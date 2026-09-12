# Test Model Design

Model validation contract: model-document-v1

Owning change: [2026-09-08-design-derived-test-model](../../changes/2026-09-08-design-derived-test-model/change.json)

## Introduction and Goals

The Test model defines shared criteria for deriving tests, evaluating their protective value, and maintaining them. Its purpose is to make tests explain the engineering obligations and meaningful failures they cover, and to support removal of unnecessary tests without silently losing protection. Test count, assertion count, coverage percentage and execution time are observations, not definitions of quality.

This is a bounded policy responsibility within Workflow. It is not a test runner, suite approval service, lifecycle stage or public skill. The [approved direction](../../proposals/2026-09-08-design-derived-test-model.md) includes both future test creation and a bounded audit and cleanup of existing tests. This Design supplies criteria; it does not identify any existing test as safe to delete.

## Architecture Constraints

Product/component Design owns required behavior. This model cannot infer requirements from implementation or grant compatibility retirement. [Review and Closeout](../review-closeout/review-closeout.md#requirements) owns assessment authority policy, independence, judgment meaning, evidence applicability and closeout consequences. Responsible specialist reviewers and Verify make the actual assessments. [Workflow](../workflow/workflow.md) owns coordination and model-document conventions; Record Format and CLI retain stored representation and mechanics.

The original adoption change used rigorloop-records-v2; its records remain historical provenance. Current recording follows Record Format’s v3-only contract. The model-validation marker above versions document structure independently of stored records. No schema change, CLI judgment selector, automated deletion, history ledger, migration, new gate or mandatory separate test specification is introduced. Public guidance must not require internal model IDs, repository-maintainer details or an internal Design checkout.

## Context and Scope

| Responsibility | Owner | Boundary |
| --- | --- | --- |
| Required behavior, invariants, interfaces and supported compatibility | Product/component Design | Tests may expose a gap but cannot decide its intended outcome |
| Test purpose, derivation, protective-value and maintenance criteria | Test model | No suite approval, evidence-current declaration or review waiver |
| Objectives allocated to milestones and integrated work, commands and evidence expectations | Delivery planning | Uses criteria; does not redefine behavior or assessment policy |
| Concrete fixtures, assertions, instrumentation and test changes | Implementation or authorized correction activity | Supplies proof and maintenance rationale; cannot approve its own changes |
| Design testability, delivery allocation, actual tests and final evidence | Design Review, Delivery Review, Code Review and Verify within their scopes | Apply criteria and record their own conclusions under Review and Closeout |
| Independence, judgments, applicability, concern disposition and closeout | Review and Closeout | Retains RC-SR-01–18 without relocation in this package |
| Routing, storage and execution infrastructure | Workflow, Record Format, CLI and existing runners respectively | No semantic quality decision delegated to structural validation |

The criteria apply to an invoked assessment's scope, including unit, integration, system, regression, property-based and generated-output tests. They also help distinguish automated tests from allowed manual or static proof. Adoption does not require a standalone advisory invocation to run the full lifecycle. Historical tests remain interpretable under their governing contracts; absence of modern trace labels is not a deletion reason.

## Solution Strategy

Follow a many-to-many chain: governing obligation → test objective → representative condition and expected observation → concrete proof → observed evidence. Keep the smallest sufficient explanation at the existing owning surface. Group several cases when their common purpose is clear; distinguish cases when their failure detection or boundary differs.

Assess protection by asking what plausible violation the proof would expose and what it would miss. Select cases for materially distinct outcomes, boundaries or hazards. Compare removal candidates against remaining proof using those same criteria, rather than comparing test names or counting assertions. Separate a test's intended protection from evidence that it actually ran and from an assessor's decision to rely on it.

## Requirements

| ID | Required behavior |
| --- | --- |
| TEST-SR-01 | Each new or substantively changed test or coherent group MUST have an identifiable governing Design obligation or explicit engineering obligation, objective, relevant condition, expected observable outcome and plausible violation it is intended to detect. References MAY be group-level and many-to-many; a new record or ID per test function MUST NOT be required. |
| TEST-SR-02 | Expected outcomes MUST come from the governing contract or an explicitly justified engineering obligation, not solely from current implementation output. A discovered regression or hazard with missing or conflicting behavioral authority MUST retain its reproduction and route the intended outcome to the Design owner; missing traceability alone MUST NOT justify deletion or fabrication of a requirement. |
| TEST-SR-03 | Case selection MUST cover representative outcome partitions, relevant boundaries and material hazards for the scoped obligation. A case added beyond existing protection MUST identify a distinct outcome, path, state, timing, authority, failure/recovery, compatibility or environmental contribution, or a justified diagnostic contribution that materially helps identify the protected failure. The rationale MUST explain that contribution; a different test name or repeated assertion alone does not establish diagnostic value. Mechanical Cartesian expansion and numerical coverage targets MUST NOT substitute for this reasoning. |
| TEST-SR-04 | Proof MUST observe the contract outcome at a boundary capable of exposing the claimed violation, including required absence of side effects. Mocks or helpers that bypass the behavior under assessment MUST NOT be cited as proof of that behavior. Lower-level and integrated tests MAY both be retained when their detection scope or diagnostic contribution differs. |
| TEST-SR-05 | Assertions and setup MUST distinguish correct behavior from the intended violation. Expected results computed by the same potentially faulty production logic, assertions that cannot fail on the claimed defect, and snapshots accepted without examining required outcomes MUST NOT be treated as sufficient protection. Review uses a concrete counterexample or inspected failure mechanism; mutation testing is optional, not universally required. |
| TEST-SR-06 | Property-based or randomized tests MUST identify their invariant, valid generated domain, relevant failure observation and enough failure data to investigate or reproduce a counterexample. A seed alone is insufficient when relevant environment or external state is uncontrolled. Random generation with a justified property MUST NOT be rejected merely because its inputs were not enumerated in Design. |
| TEST-SR-07 | Test maintenance MUST distinguish retain, strengthen, consolidate, replace and remove actions and state the affected obligation and protection impact for the changed scope. Runtime cost, naming similarity, age, missing labels, line coverage or a passing remaining suite alone MUST NOT establish redundancy. An unchanged legacy suite need not be retroactively annotated before unrelated work can proceed. |
| TEST-SR-08 | Removal or consolidation MUST identify the candidate scope, its existing failure detection and boundary, the retained or replacement proof, and why no required distinct protection is lost. Replacement proof MUST be established and assessed before relying on the reduced suite. An intentionally retired obligation requires an explicit governing owner decision and scope; removing its test cannot itself retire behavior. |
| TEST-SR-09 | When a candidate's protection is unknown, maintenance MUST preserve it while investigating or strengthening its basis; uncertainty MUST NOT be relabelled uselessness. A failing or flaky test MUST have its cause and contract relevance assessed, not be removed or skipped solely to obtain green validation. Any permitted quarantine requires an authorized owner, tracked follow-up, affected claim limits and alternative protection or explicit residual-risk treatment under the governing contract. |
| TEST-SR-10 | Test changes MUST identify impacts on fixtures, alternate callers, supported versions, runner discovery, selectors and generated outputs where those affect protection. Validation MUST demonstrate that selected checks are actually discovered and exercise the changed obligations; fewer failures caused by accidental loss of selection MUST NOT count as successful cleanup. |
| TEST-SR-11 | This model's criteria MUST be applied by the responsible specialist within its actual scope. Test-model criteria, structural validity or test success MUST NOT independently approve a suite, declare evidence applicable, choose an overall review judgment or waive an assessment. Those decisions and consequences remain governed by Review and Closeout RC-SR-01–18. |
| TEST-SR-12 | Delivery MUST allocate every affected obligation and material combined hazard to milestone or change-level proof and identify bounded cleanup targets and completion criteria before implementation. Execution MUST retain enough actual-result and maintenance rationale in existing plan, review and evidence surfaces to support the claimed protection; an additional test ledger or per-function receipt MUST NOT be mandatory. |
| TEST-SR-13 | Consumer adoption MUST map each affected shared criterion to one owner, preserve specialist methods and historical contracts, and provide selectively loaded portable guidance. Internal requirement IDs and repository-maintainer mechanics MUST remain in governance/contributor traceability, not published skill instructions. Installation, drafting or structural validation MUST NOT activate the policy or authorize deletion. |
| TEST-SR-14 | For the selected necessary-design consolidation, validation scope MUST follow affected obligations and actual readers/dependencies. Distinguish a useful retained check, a check required for this change, and a fresh execution. Apply the bounded retirement contract below when a check or exclusive assertion changes. Unknown impact MUST trigger investigation and broader relevant proof; existing mandatory or freshness requirements remain effective unless their owner explicitly amends them. No new ledger, benchmark or validation subsystem is required for source cleanup. |

## Building Block View

There are four conceptual inputs, with no new serialized entities: the governing obligation; the test objective and observable outcome; concrete proof and its execution conditions; and the maintenance rationale when protection changes. Existing Design requirement references and plan verification groups organize these relationships. Test names, comments, focused review rationale or group-level documentation can make a test's purpose clear without repeating the full Design.

For a maintenance change, the rationale answers: what is changing; what obligation it protects; what distinct failure it detects; what remaining proof covers that failure at the relevant boundary; and what evidence or retirement decision supports the change. The implementation evidence carries the actual result; the review carries the assessment. The Record Format evidence summary and review narrative can express these facts today, so no representation or CLI revision is selected.

C4 runtime/container diagrams are not applicable: this policy introduces no executable component or deployment boundary. The responsibility table and traceability chain above describe its complete architecture. Decisions remain embedded in this model under Workflow's one-file convention; no separate specification or ADR is created.

## Runtime View

### New or changed behavior

The Design owner defines the outcome and acceptance boundary. Planning selects objectives and allocates direct and integrated proof where each can be established. Implementation chooses concrete cases, fixtures and assertions, preferably establishing a failing reproduction before a correction. Code Review assesses the actual tests and diff; Verify assesses final evidence and coherence under Review and Closeout. A gap in intended behavior returns to Design; an allocation gap returns to planning; a weak assertion returns to implementation. These are applications of existing stages, not new transitions.

### Existing-suite cleanup

Start from the Delivery-approved suites and candidate categories. Inspect the test, setup, assertions, called production boundary and governing obligation. Retain a useful test; strengthen one whose intended protection is weak; consolidate repeated mechanics while preserving meaningful cases; replace unsuitable proof with established equivalent or stronger proof; or remove a test whose protection is otherwise preserved or whose obligation was explicitly retired. Record uncertainty as an investigation outcome rather than forcing a deletion count.

For replacement or consolidation, demonstrate the retained cases' relevant detection before removing the old path. A failing-before/passing-after reproduction or focused mutation can help when feasible; otherwise inspect the exact counterexample mechanism and execute relevant proof. This is bounded evidence, not a requirement to inject every conceivable defect. Review judges whether the basis suffices. Restoring removed tests is the recovery path if the claimed equivalence fails; suppressing the contradictory result is not recovery.

### Necessary-design consolidation: proportionate proof

TEST-SR-14 applies only to the source cleanup selected in System's necessary-design consolidation map and its necessary consumer corrections. It does not reclassify all repository checks, alter hosted CI, or extend the earlier stored-format retirement. Review and Closeout RC-SR-15 continues to own evidence reuse; CLI runtime containment, identity, structural and transaction checks still execute on actual writes and recovery. A documentation-only scope does not waive fresh independent final Code Review or distinct Verify.

The following is the complete retained contract for any script/check affected by this selected cleanup. Original source references are qualified by `published-skill-first-repository-simplification.md`; the earlier stored-format amendment in Workflow remains separately scoped. Unselected work retains its existing obligations.

| Actual requirement | Applicable population | Existing equivalent or selected amendment |
| --- | --- | --- |
| Identify the protected product/package/governance/release failure, why deterministic proof is appropriate, responsible owner, simpler existing owner considered, invocation conditions, actionable repair and retirement condition. | New or changed checks and exclusive assertions in this consolidation; not an annotation audit of unchanged suites. | R14's engineering meaning retained. The existing plan and current evidence/decision records carry coherent groups; a second retirement-ledger entry is not required for this slice. |
| Inspect accepted/rejected cases and map every distinct contractual failure to retained proof at its real boundary or an explicit obligation-retirement decision. Preserve and investigate unknown, undocumented or contradictory protection. | Any selected check removal or replacement. | R17/R18/R20 retained through TEST-SR-02/04/08/09/10. Filenames, favorable metrics and a reduced-suite pass cannot establish equivalence. |
| Establish retained detection before removing a replacement candidate. Compare representative old and retained proof where available and relevant; record differences, missing evidence, disposition and a recoverable source/code boundary. | Replacement/consolidation of selected checks protecting surviving obligations. | R19 amended for this slice: applicable recorded old results may be reused under RC-SR-15. Missing old proof requires sufficient direct evidence of the surviving failure boundary, not an invented equivalence claim. Review assesses sufficiency. |
| Record an explicit owner-approved retirement and establish surviving safe rejection, compatibility and shared-safety protection. No replacement must reproduce behavior that was deliberately retired. | An obsolete source-location/wording assertion or exclusive mechanism whose obligation is actually retired by this package. | R19/R20: obligation retirement is distinct from equivalent replacement. Deleting prose alone does not retire a supported guarantee. No individual runtime test is selected for removal by this Design. |
| Record actual source/check removals, retained exceptions and ownership changes. Report timing, command-count or other savings only when measured; absent measurements are disclosed. | Completion evidence for this selected cleanup. | R22 amended: no mandatory runtime/token benchmark or rerun solely to measure savings. Protection and usable current meaning, not a count, establish success. |

For source-only edits, Delivery allocates model/document structure, changed references, actual reader impact and semantic preservation assessment. Package checks apply when packaged bytes, generation inputs, manifests or candidate identities are affected; runtime checks apply when executable behavior or selection changes. An extension such as `.md` does not decide impact. Source-only cleanup needs no package generation merely to re-demonstrate an unchanged boundary. Existing command names and interface/result identifiers are retained even where guidance uses skill checks, package checks and release checks.

A selected obsolete source-path assertion can be replaced with an assertion of the current owner's actual obligation. A useful regression with no effect from this cleanup remains intact and need not rerun solely because a review occurred. A source mistakenly treated as prose but consumed by a loader instead triggers that loader's proof. These demonstrate TEST-SR-08/10/14 at Input domain, Composition/path and Compatibility/migration; changed check configuration invalidating a previous pass demonstrates Temporal/retry under TEST-SR-14 and RC-SR-15. Delivery allocates exact proof without creating an exhaustive case catalogue.

This package adds no public skill procedure: existing selective Test maintenance guidance already covers protected failure, uncertainty and group-level evidence, while the scoped source-retention decision is contributor governance. Any newly discovered conflicting published instruction returns to Design before consumer edits; it is not permission to change all skills.

### Representative applications

| Situation | Application of criteria |
| --- | --- |
| Two unit tests use different ordinary values from the same partition and detect the same violation | Consolidation is a candidate; inspect fixtures and boundary differences and establish retained detection before removing either case (TEST-SR-03/08) |
| Helper test and public-command test assert the same rejection text | Retain both if the public case additionally protects dispatch, parsing or absence of persistence; helper proof does not establish the public boundary (TEST-SR-04/08) |
| Retry can duplicate an operation, but a legacy regression lacks an SR label | Preserve the reproduction; identify the existing idempotence obligation or obtain the Design owner's intended outcome (TEST-SR-02/09) |
| A snapshot merely tracks an internal arrangement | Determine whether order or representation is contractual; replace with outcome assertions if they preserve all relevant protection (TEST-SR-05/08) |
| A randomized round-trip check finds a minimal counterexample | Keep the property and useful regression with domain/environment basis; duplication depends on distinct protection, not shared origin (TEST-SR-03/06) |
| A large suite passes after a selector drops a test directory | Treat discovery loss as a proof gap; the pass does not establish protection of that directory (TEST-SR-10/11) |
| An obsolete-version test is slow | Check supported-version authority first; runtime cost does not retire compatibility (TEST-SR-07/08) |
| A flaky concurrency case is the only evidence for a race invariant | Investigate isolation and timing; any authorized quarantine exposes the coverage gap and follow-up instead of claiming full protection (TEST-SR-09/11) |

These synthetic examples illustrate requirements, not audited repository findings or deletion approvals.

## Deployment View

The adoption package is this Test model and the affected Workflow revision. Review and Closeout, Record Format and CLI remain unchanged governing dependencies. No runtime or stored contract gap has been identified. Any later gap requires an explicit Design amendment and assessment of its impact before implementation.

### Consumer ownership and adoption inventory

This inventory selects responsibility and rule areas. Delivery expands each row through transitive references/assets into exact files and records an affected or justified unaffected disposition before implementation. A newly discovered conflicting policy clause returns to Design; Delivery cannot settle a different policy by editing a consumer. Existing historical text keeps its contract-qualified meaning.

| Current source and rule area | Treatment for adopted work | Retained owner / Test criteria |
| --- | --- | --- |
| [Constitution](../../../CONSTITUTION.md), Spec-driven and Test-driven rules; [AGENTS](../../../AGENTS.md), spec/test conventions, implementation and verification expectations | Reference shared criteria while retaining governing precedence, regression-proof obligations and required closed-vocabulary negative tests | Governance remains superior; TEST-SR-01/02/03/12/13 |
| Workflow, Model validation and proof mapping | Retain document shape, stable IDs and allocation convention; reference Test quality criteria explicitly | Workflow keeps structure/coordination; TEST-SR-11/12 |
| [Plan](../../../skills/plan/SKILL.md), Plan quality contract and Boundary-first method; [plan scaffold](../../../skills/plan/assets/plan-skeleton.md) verification groups | Apply shared purpose and proportionality criteria; add bounded maintenance rationale and cleanup scope where triggered | Plan keeps ordering, allocation, commands and evidence expectations; TEST-SR-01/03/07/08/12 |
| [Plan boundary method](../../../skills/plan/references/boundary-and-negative-verification.md) and [integrated verification](../../../skills/plan/references/cross-milestone-integration-verification.md), plus triggered specialist verification references | Retain partition and domain-specific methods; shared contribution/boundary criteria have this owner rather than competing definitions | Plan applies TEST-SR-03/04/06/10; integrated tests and final review remain distinct |
| [Spec](../../../skills/spec/SKILL.md), [architecture](../../../skills/architecture/SKILL.md), [Design Review](../../../skills/design-review/SKILL.md), boundary and testability guidance | Preserve behavioral authorship and assessment; use criteria for observable acceptance and discovered gaps | Design owns outcomes; reviewers apply TEST-SR-01/02/11 |
| [Implement](../../../skills/implement/SKILL.md), proof-first and boundary guidance; [bugfix](../../../skills/bugfix/SKILL.md), reproduction and correction | Apply test validity and maintenance criteria to concrete tests and test removals | Implementation owns mechanics; TEST-SR-01–10 |
| [Delivery Review](../../../skills/delivery-review/SKILL.md), Review contract and correction routing | Apply criteria to allocation, integrated protection and cleanup bounds; retain one specialist judgment | Delivery Review under RC; TEST-SR-03/04/08/11/12 |
| [Code Review](../../../skills/code-review/SKILL.md), First-pass checklist, Direct proof and Boundary-first method | Assess actual assertions, mocks, distinct protection and removal rationale | Code Review under RC; TEST-SR-04–11 |
| [Verify](../../../skills/verify/SKILL.md), evidence access, dimensions and execution; [route](../../../skills/route/SKILL.md), boundary scan and corrections | Use criteria when judging changed tests and route gaps to their actual owner; retain RC evidence applicability and closeout policy | Verify/route within their scopes; TEST-SR-10/11/12 |
| [CI maintenance](../../../skills/ci-maintenance/SKILL.md), authoritative commands and bounded repair | Preserve command authority; ensure runner/selector changes do not masquerade as test cleanup | Existing CI owner; TEST-SR-09/10/11 |
| [Workflow specification](../../../specs/rigorloop-workflow.md), adopted-profile guidance; [skill contract](../../../specs/skill-contract.md) and [system architecture](../../architecture/system/architecture.md), ownership descriptions | Reference this owner for criteria only; no global rewrite of historical rules or new stage | Governance and Workflow retained; TEST-SR-11/13 |
| [Boundary method](../../../specs/references/boundary-first-method-v1.md) and its feature/proof companions; packaged copies and shared source guidance | Preserve historical boundary serialization/IDs and specialist methods; explicitly scope current shared criteria to adopted work | Existing format owner; TEST-SR-01/03/04/13 |
| Canonical shared guidance, consuming skill resource maps/assets, supported adapter archives and existing package parity validation | Package only relevant criteria; keep internal maps here, regenerate via existing builders, and validate discovered consumers | Contributor implementation mechanism; TEST-SR-13 |

Review and Closeout's references to specialist evidence adequacy continue to mean actual assessment. Its RC-SR-15 owns sufficient/current evidence and reuse, not a rival test-generation method. No RC requirement or judgment vocabulary is relocated. No Record Format or CLI model revision is selected.

### Adoption, cleanup bounds and recovery

Adoption requires approved Design, Delivery allocation and coordinated consumer changes with existing required reviews and Verify. A bounded audit/cleanup remains required initiative work: Delivery names suites, selection reasons, candidate evaluation scope and completion outcomes, including retained or uncertain candidates. No minimum deletion count applies; a completed audit with no justified deletion must explain that result rather than invent removals. Unexamined suites remain outside the cleanup claim.

Installation does not activate customer policy. Historical tests and records are not bulk-converted; defects found in their supported contracts remain real obligations. Portable application text states the criteria without internal IDs or checkout paths, and loads maintenance guidance only when tests are being changed or assessed for removal. No universal testing manual is loaded on every invocation.

Before adoption, rollback discards the candidate guidance changes. After adoption, a policy rollback requires an explicit governing decision and coherent consumer alignment. Test restoration is bounded engineering correction with current proof and applicable review; reverting guidance does not automatically restore removed tests or the old evidence basis. No records are deleted as rollback.

## Crosscutting Concepts

### Quality criteria versus assessment

Here, test adequacy means criteria for fit between an obligation and the protection offered by tests. A conclusion that a particular plan, suite or evidence set is sufficient belongs to its specialist assessor. RC-SR-03 selects overall judgment when defects, missing authority and incomplete evidence overlap. RC-SR-05–07/15 govern applicability after test, environment or bookkeeping changes. This model neither overrides those rules nor requires every command to rerun simply because a new review occurs.

### Boundary scan and acceptance scenarios

| Dimension | Requirement basis | Distinct outcome to demonstrate |
| --- | --- | --- |
| Input domain | TEST-SR-01, TEST-SR-03, TEST-SR-06, TEST-SR-14 | Representative partitions and justified generated inputs contribute explicit protection without exhaustive combinations. |
| State/lifecycle | TEST-SR-07, TEST-SR-08, TEST-SR-09 | Distinguish retention, strengthening, replacement and removal; unknown protection is preserved and investigated. |
| Identity/authority | TEST-SR-02, TEST-SR-08, TEST-SR-11 | A test or passing result cannot define missing behavior, retire compatibility or grant approval. |
| Composition/path | TEST-SR-04, TEST-SR-05, TEST-SR-10, TEST-SR-14 | Helper proof cannot substitute for public-path behavior; a selector omission cannot produce a valid coverage claim. |
| Temporal/retry | TEST-SR-03, TEST-SR-06, TEST-SR-09, TEST-SR-14 | Retry and race protection remains distinct; generated failures expose reproducible or investigable conditions. |
| Failure/recovery | TEST-SR-05, TEST-SR-08, TEST-SR-09 | Detect vacuous assertions and lost replacement protection; failed/flaky tests are investigated rather than suppressed for green output. |
| Compatibility/migration | TEST-SR-02, TEST-SR-08, TEST-SR-13, TEST-SR-14 | Unlabelled historical tests remain valid candidates for retention; retirement needs explicit authority and adoption preserves old records. |
| External/environment | TEST-SR-06, TEST-SR-10, TEST-SR-12, TEST-SR-13 | Environment and discovery limits bound evidence claims; portable skills apply criteria without internal Design files. |

Material combined hazards are consolidation plus public-path loss (TEST-SR-04/08/10), a flaky sole regression plus missing behavior authority (TEST-SR-02/09/11), and faster validation plus accidentally omitted discovery (TEST-SR-07/10/11). Delivery maps every requirement, scenario row and these combined hazards to checks and evidence; structural validators cannot determine semantic sufficiency.

## Architecture Decisions

| ID | Decision and rationale | Rejected alternative and consequence |
| --- | --- | --- |
| TEST-DEC-01 | One policy model defines shared criteria; existing specialists make judgments | A suite-approval component or new gate would duplicate Review and Closeout |
| TEST-DEC-02 | Many-to-many, group-level traceability through existing artifacts | Per-function records and one-test-per-requirement rules create bookkeeping and distort useful test structure |
| TEST-DEC-03 | Protection-preserving maintenance without a deletion quota | Count, speed or line-coverage targets can reward lost detection and conceal undocumented obligations |
| TEST-DEC-04 | Properties and discovered regressions are legitimate inputs with an owned behavior decision | Requiring every concrete input to appear in Design would suppress useful discovery; deriving expected outcomes from code would reverse authority |
| TEST-DEC-06 | Necessary-design cleanup uses actual reader impact and existing evidence surfaces; TEST-SR-14 makes only its directly necessary procedural exceptions. | Blanket reruns and a new check catalogue duplicate work; blanket skipping hides dependencies. Unknown impact broadens investigation, and surviving failure detection remains required. |
| TEST-DEC-05 | Retain existing storage, commands and document validation | A dedicated test ledger or semantic CLI selector adds mechanics without establishing engineering judgment |

## Quality Requirements

| Quality | Observable acceptance | Requirement basis |
| --- | --- | --- |
| Traceability | A reviewer identifies the obligation, outcome and failure contribution from the test/group's current basis | TEST-SR-01/02/12 |
| Detection | A concrete violating example explains why the selected assertion and boundary can expose the defect | TEST-SR-04/05 |
| Safe simplification | A removal's distinct protection is covered by established remaining proof or explicitly retired authority | TEST-SR-07/08/09/10 |
| Proportionality | Cases and records have distinct purpose; useful randomized and integrated tests are preserved without compulsory exhaustive enumeration | TEST-SR-03/06/12 |
| Portable ownership | Installed consumers apply criteria with sufficient local context and no internal identifiers; judgments remain with specialists | TEST-SR-11/13 |

## Risks and Technical Debt

Undocumented regression knowledge may make some candidates expensive to classify. Preserve uncertain protection rather than force cleanup. A test that appears redundant at one level may cover a different dispatch or environment boundary; the maintenance analysis must inspect that difference. Mocks and snapshots are neither inherently valid nor inherently useless. Criterion-level traceability can still become verbose; Delivery and reviewers should use coherent groups where they preserve the reasoning.

The existing-suite inventory, exact consumer diffs, measured cost changes and actual protection-preservation evidence remain Delivery/implementation work. This Design makes no repository test-quality audit claim. Required governance checks, including unknown-value regressions for closed vocabularies, remain obligations and cannot be waived as redundant through this policy.

## Glossary

Obligation: approved behavior or explicit engineering responsibility. Test objective: what protection the proof seeks to establish. Protective value: the justified failure detection and relevant diagnostic contribution of a test or group. Oracle: the independently grounded expected observation used to distinguish correct behavior. Redundancy: absence of a required distinct contribution after comparing boundaries and remaining protection. Evidence applicability: the separately assessed ability to rely on a result under Review and Closeout.

## Drafting basis and authority

The user's continuation authorizes detailed Design after [independent Proposal Review](../../changes/2026-09-08-design-derived-test-model/reviews/proposal-review.json). The review package comprises this model and the Workflow revision that references its responsibility. No other model is amended. The existing four model files and canonical linked guidance supplied direct orientation; no project-map inference is needed for this policy-only authoring scope. This document does not approve itself, start implementation or delete tests.

## Next artifacts

Independent Design Review of the exact Test and Workflow package, including ownership, consumer mapping, acceptance and historical preservation. Delivery planning follows approved Design and authorized continuation and allocates both consumer alignment and bounded test cleanup.

## Follow-on artifacts

None yet.
