# Plan Design

Owner: [MOD-006 Change control](module.json). This is supporting contract detail, not a separate REM entity. Source-qualified clause IDs retain their existing meaning.

Model validation contract: model-document-v1

Test scenarios and expected observations are defined in the single [system test design](../../../../../support/test-design/system-test-design.md).

## Introduction and Goals

Plan turns settled engineering requirements and realization into safe implementation milestones and explicit verification allocation. It owns stable execution intent and the narrow initialization of missing work from an exact selected plan. Workflow owns subsequent work coordination and mutable progress.

## Context and Scope

[Skill](../../../MOD-018-engineering-operations/modules/MOD-012-published-engineering-capability-guidance/capability-contract.md) owns common capability, resource and evidence-access rules. [Authoring](../MOD-008-engineering-authoring-guidance/authoring.md) owns composition; [Workflow](workflow.md) owns progression and [Assessment](../MOD-007-engineering-verification-and-assurance/assessment.md) owns independent judgments. Published skills realize these contracts; model extraction does not rename invocations, change stored formats or grant execution authority.

## Requirements

| ID | Required behavior |
| --- | --- |
| PLAN-SR-01 | Plan MUST consume the current system test design and allocate settled requirements and architectural boundaries to milestones with dependencies, scope, executable proof, commands, completion conditions, evidence and recovery. Lasting group rationale, targets, scenarios and fixture strategy remain in the system test design; the plan MUST NOT become their sole owner. |
| PLAN-SR-02 | Plan MUST allocate integrated proof where local checks cannot establish the required behavior and MUST include one independent whole-change review gate after implementation, with no mandatory milestone review; passing tests MUST NOT substitute for that gate. |
| PLAN-SR-03 | Plan and navigation MUST contain stable intent and pointers; actual results, current work status, blockers and routing MUST remain with their owning records. |
| PLAN-SR-04 | Create, revise and initialize operations MUST resolve exact current targets and authority; malformed or conflicting governed signals MUST stop without portable fallback or cross-owner mutation. |
| PLAN-SR-05 | Initialization MUST add missing work only from the exact current owner-selected plan and MUST NOT duplicate, replace, repair or update existing work. |
| PLAN-SR-06 | Required conditional resources and the two current plan assets MUST preserve their structure, metadata, fingerprints and package parity; missing resources and unknown operations MUST reject. |
| PLAN-SR-07 | Retries, changed milestones and competing writes MUST preserve existing evidence and require current authority and reassessment; historical plan intent MUST NOT reconstruct current workflow state. |
| PLAN-SR-08 | The Plan entrypoint MUST expose its task, authority, invocation classification and resource selection before detailed recording construction. Its reviewed equivalent layout MUST preserve PLAN-SR-01–07 and applicable common Skill obligations through a complete core procedure, explicitly triggered local methods and usable output assets; fewer lines or relocated text alone MUST NOT establish improvement. |

## Architecture Overview

```mermaid
flowchart LR
    Basis["Settled Design and project authority"] -->|"requirements and constraints"| Allocate
    subgraph Owned["Plan"]
        Allocate["Allocate delivery and verification"] -->|"stable milestones and proof"| Output["Plan and navigation"]
        Init["Initialize authorized missing work"]
    end
    Output -->|"selected plan and authority"| Init
    Output -.->|"optional assessment"| Review["Delivery Review"]
    Init -->|"bounded work additions"| Records["CLI and Records"]
```

The overview names the owned method and its external inputs and consumers. Detailed behavior is defined in the sections below; arrows to review identify submitted subjects, not automatic approvals.

| View | Necessity and reason | Owning detail |
| --- | --- | --- |
| Context | Necessary: user authority, upstream basis and independent assessment are separate boundaries. | [Context view](#context-view) |
| Building Block | No separate diagram: this method has no independent internal subsystem; its procedure and output structure provide the required decomposition. | Specialist procedure and output sections below. |
| Runtime | Necessary: classification, authoring, failure and handoff have distinct authority effects. | [Runtime view](#runtime-view) |
| Deployment | No separate deployment: the capability is packaged guidance, not a separately deployed service; source, archive and installation boundaries are unchanged. | [Skill Deployment](../../../MOD-018-engineering-operations/modules/MOD-012-published-engineering-capability-guidance/capability-contract.md#deployment-view) and [Packaging](../../../MOD-019-product-delivery/modules/MOD-013-product-package-production/packaging.md). |

## Delivery allocation

Plan owns concrete verification allocation: milestone completion conditions, commands, input prerequisites, proof timing, evidence expectations and side-effect permissions. Allocate integrated checks where local proof cannot establish cross-component, cross-milestone, compatibility, concurrency, recovery, security or authority behavior. Implementation supplies tests and observed results. [Engineering authoring](../MOD-008-engineering-authoring-guidance/design-authoring.md#authoring-responsibilities) owns the requirement-to-work relationship; [System](../../../../composition.md#living-test-design-composition) owns shared proof-quality rules; [Validation](../../../../../support/validation.md) owns check execution; [Assessment](../MOD-007-engineering-verification-and-assurance/assessment.md) owns Delivery Review and final evidence judgments. No one-to-one mapping to test functions or separate test-spec stage is required.

Under SKL-SR-04/08/10/24/27, planning preserves stable execution intent: each milestone identifies its ID and kind, goal, governing requirements and architecture, affected components, dependencies, implementation scope, tests and proof, validation commands and expected results, completion criteria, required evidence, review handoff, risks and rollback or recovery. Include a commit boundary when applicable. Plans contain no current milestone state, command outcomes, validation progress, blockers, review status, routing or closeout progress. Navigation points to the plan and owning change; it never becomes another state owner.

Apply [Conditional resources](../../../MOD-018-engineering-operations/modules/MOD-012-published-engineering-capability-guidance/capability-contract.md#conditional-resources). `operational-recording.md` applies the current CLI procedure; boundary and specialist proof methods retain their own triggers. The plan and milestone structural assets own labels and layout, never state or authority. Direct and Change-managed work retain explicit scope; boundary proof guidance loads only when applicable.

Planning distinguishes creating, revising and initializing work from an selected plan. Creation requires one selected change, settled prerequisites, authoring authority, a normalized intended path and no conflicting file or registration; no prior plan identity is needed for an absent target. Revision requires the exact matching current plan and registration. Ambiguous targets, conflicting primary candidates, stale authority or file/registration asymmetry stop before mutation. Portable planning writes only its plan and navigation, without governed state. Manual and workflow-managed invocations share the same authoring boundary; loading resources grants no authority, and Route owns later coordination.

The initialization exception allows Plan to add missing implementation work from the exact current plan selected within applicable authority. Confirm valid milestone definitions, settled dependencies and absent work before explicit `change update` entries. Do not replace or repair existing work through initialization; conflicting results return to Route. A retry cannot duplicate work or treat changed evidence as authorization. Delivery Review is optional and does not gate initialization; material unresolved decisions and missing authority still prevent dependent work.

Current [Records](../../../MOD-018-engineering-operations/modules/MOD-011-operational-record-persistence/record-contract.md) and [CLI](../../../MOD-018-engineering-operations/modules/MOD-010-engineering-command-interface/command-contract.md) own identities, registration, revision conflicts and recovery; [Workflow](workflow.md) owns continuation and subsequent work decisions. Settled changes to milestone ID, order, kind, completion criteria or required evidence require authorized replanning. Historical plan prose cannot reconstruct current work or override change-local state. Preserve old plans and judgments under their original contracts; reading stable historical intent does not enable retired record formats.

Preserve proof of exact creation/revision targets, unknown operations, stale selected basis or authority, absent versus existing work, interrupted or competing writes, no cross-owner mutation, stable plan output and missing triggered resources.

## Authoring presentation

The current `plan` skill establishes scope, authority, accepted requirements/design and conditional resources before recording. Direct invocation authors only its authorized plan. Change-managed invocation uses current CLI context and supported request schemas. Missing required resources stop dependent action. A small plan is sufficient when it covers delivery, dependencies, proof and recovery; no presentation profile or separate proposal artifact is required.

## Living test design and execution allocation

Consume [Engineering authoring](../MOD-008-engineering-authoring-guidance/design-authoring.md#proportionate-design-and-proof), [System TEST-SR-21–23](../../../../composition.md#requirements) and the [shared selection procedure](../../../../../support/test-design/rules.md#select-requirements-and-proof). A plan references the central system scenarios and Validation’s current coverage gaps, then allocates implementation slices, concrete commands, input prerequisites, proof timing, evidence and recovery. For each affected supported requirement and material interaction, identify the selected scenario or explicit gap, the observation capable of exposing its violation and its concrete execution or independent assessment allocation. Risk guides depth and sequencing; timing measurements guide efficient realization without dropping required proof. Existing semantic procedures require real subject/output assessment, not an invented executable command. A plan can introduce a justified additional test and must route a missing behavioral decision to Design. It must not duplicate the central test design, invent coverage from a planned filename or require a private-function case quota.

Changing supported behavior, coverage ownership or intended observations requires the owning Design update; changing execution timing/commands without altering those obligations stays in Delivery. At completion the model's realization links reflect actual test groups, while observed results stay in records. Review this transfer explicitly when tests move or consolidate. The plan and its two assets retain their existing format and fields; reconcile their instructions and consumers with these responsibilities without creating another normative test-spec asset. The earlier focused application selected Release, Skill and Authoring. The separately approved complete-model direction now applies this method across the current model inventory; it does not extend that earlier approval or authorize compatibility retirement.

## Plan assets

The two plan assets are `plan-skeleton.md` and `milestone.md`. The full skeleton owns section order and placeholders; the milestone asset owns repeated delivery structure. Important rationale belongs to its model or current operational decision record; the historical decision-log-row asset is retired. COPY entries state when to use each and what to fill. Do not duplicate the full structure in the skill or add a separate handoff-summary asset. Handoff contains one stable owning-record pointer, with mutable state under Workflow/Records. Index links are relative clickable links.

Each asset carries template/version, skill, normative status, structural fingerprint and maintained-alongside metadata. Deterministic checks recompute fingerprints and compare full-skeleton section expectations; structural drift requires reverting or a version/fingerprint update. Assets contain usable structure, never hidden policy or normal customer dependencies on repository internals. Current proof covers valid fill, missing fields, structure drift and package parity. Fixed pilot populations, token-reduction percentages and compulsory historical-plan counts are completed experiment constraints, not future acceptance gates.


## Context view

```mermaid
flowchart LR
    Design["Settled Design package"] -->|"requirements, realization and acceptance intent"| Plan["Plan authoring"]
    System["System test policy"] -->|"proof quality criteria"| Plan
    Authority["Project authority and current change"] -->|"exact target and allowed action"| Plan
    Plan -.->|"optional assessment"| Review["Delivery Review"]
    Plan -->|"authorized initialization only"| Records["CLI and Records: missing work"]
```

## Runtime view

```mermaid
flowchart TB
    Input["Resolve settled basis and exact target"] --> Resources{"Authority and triggered resources complete?"}
    Resources -->|"no"| Owner
    Resources -->|"yes"| Action{"Authorized operation?"}
    Action -->|"unknown or unauthorized"| Owner
    Action -->|"create or revise"| Allocate["Allocate milestones, proof, commands and recovery"]
    Allocate --> Gap{"Behavior or authority gap?"}
    Gap -->|"yes"| Owner["Return gap to owning stage"]
    Gap -->|"no"| Save["Save stable plan and authorized evidence"]
    Save --> Continue["Authorized implementation; optional delivery advice"]
    Action -->|"initialize selected plan"| Current{"Exact selected plan, authority and work absent?"}
    Current -->|"no"| Route["Return to Route without replacing work"]
    Current -->|"yes"| Init["Add selected missing work once"]
```

These branches describe separate authorized invocations. A successful save does not execute the next branch. Creation/revision does not itself initialize work; explicit authorized initialization cannot alter existing work or derive authority from a save. Integrated proof and final whole-change review are separately allocated under Assessment and System’s testing policy, with execution supplied by Validation.

## Acceptance intent

The following outcomes refine SKL-SR-04/08/10/24/27–29 for Plan. SKL-DEC-06 below retains the stable decision for the narrow initialization exception. Plan assets retain their existing metadata and fingerprint contract; extraction does not change their published format or create new asset families.

### Boundary scan and acceptance scenarios

| Dimension | Requirement basis | Distinct outcome to demonstrate |
| --- | --- | --- |
| Input domain | PLAN-SR-01, PLAN-SR-06, PLAN-SR-08 | Missing milestone fields or unknown operation values reject; valid assets produce complete output without placeholders. Core task and selection precede detailed recording construction. |
| State/lifecycle | PLAN-SR-03, PLAN-SR-05 | An authored plan contains stable intent; initialization with existing work leaves it unchanged and returns to Route. |
| Identity/authority | PLAN-SR-04, PLAN-SR-05 | A plan outside the selected scope or with unresolved dependencies cannot initialize work; exact current selection, authority and absence are checked. |
| Composition/path | PLAN-SR-01, PLAN-SR-02, PLAN-SR-08 | A cross-component requirement receives integrated proof and a separate final review checkpoint with necessary prerequisites. Actual Design output and current review basis remain sufficient Plan inputs; complete Plan output remains sufficient Delivery Review input. |
| Temporal/retry | PLAN-SR-05, PLAN-SR-07 | Retry after lost response does not duplicate work; changed milestone definitions require authorized replanning. |
| Failure/recovery | PLAN-SR-04, PLAN-SR-06, PLAN-SR-07, PLAN-SR-08 | File/registration asymmetry or interrupted recording stops dependent mutation and preserves recovery evidence. Missing or invalid selected procedure stops dependent action; heading removal cannot bypass recording checks or restore retired placement. |
| Compatibility/migration | PLAN-SR-03, PLAN-SR-06, PLAN-SR-07 | Existing plan assets retain their fingerprints and historical plans keep original judgments without enabling retired storage. |
| External/environment | PLAN-SR-01, PLAN-SR-02, PLAN-SR-06 | Commands with external side effects have explicit permission and environment prerequisites; unavailable proof remains visibly unallocated or blocked. |

## Architecture Decisions

| ID | Decision and rationale | Alternatives and consequences |
| --- | --- | --- |
| SKL-DEC-06 | Initialize missing work only from the exact current plan selected within authority. Plan derives initial work, Assessment owns optional review and Route coordinates subsequent work. | Initializing an unsettled or unauthorized plan can freeze incorrect work. An intermediate review is not a universal prerequisite. Reviewer-owned initialization mixes judgment with authoring; coordinator-owned derivation duplicates plan semantics. Allowing ordinary plan revision to replace existing work risks losing progress. Current Records/CLI own identities and recovery; the historical no-hash alternative and two-phase settlement protocol are superseded. |
| PLAN-DEC-01 | Extract delivery allocation and Plan assets into one specialist owner under Authoring; preserve SKL-DEC-06 initialization limits. | A second verification-only plan would split sequencing from proof. Keeping both together supports review while Workflow retains current state. |
| PLAN-DEC-02 | Select the bounded Plan layout and move complete recording construction into its existing governed reference. Retain the Design package with explicit rationale and assess the actual author/reviewer handoffs. | Keeping recording before task selection retains unnecessary reading; a new reference duplicates an existing owner. Applying the same layout to Design adds no established benefit. Required selection, output and authority remain visible and complete. |

## Quality and risks

Requirements and representative outcomes guide review; structural validation does not establish semantic adequacy. Incomplete authority or a material upstream conflict stops dependent work with an explicit owner. Shared policy changes require reconciliation with the named owners, and moved documents retain historical approvals only for their original subjects.
