# Requirement-first workflow refactor analysis

This package analyzes the requested whole-system refactor before detailed skill, CLI, or persistence implementation. It is RR analysis and navigation to the draft engineering model, not another proposal approval gate. The [source register](sources.md#src-workflow-requirement-review) identifies the author-assessed requirement basis for downstream design under the explicit project exception. It is not independent approval or workflow activation.

The user subsequently authorized document-based review of this refactor without governed recording and removed the Constitution's mandatory author/reviewer separation rule. The [Constitution exception](../../CONSTITUTION.md#workflow-and-review) governs this work. An author assessment must be identified as such; it does not constitute independent review or change the proposed product workflow's independent-review requirements.

## Request and selected rule

The incoming request replaces Proposal approval with review of the proposed requirement basis, separates Requirement Analysis, System Design and Architecture Design, and preserves one integrated Design Review. The user's explicit clarification selects **one mandatory whole-change Code Review gate after implementation, with optional interim advice**. This supersedes the conflicting per-milestone review clause in the earlier pasted specification. A gate can contain several correction and reassessment attempts.

The proposed dependency order is:

```text
RR → Requirement Analysis → Requirement Review
   → System Design ↔ Architecture Design → integrated Design Review
   → Plan → Delivery Review → Implement → whole-change Code Review
   → Verify → optional authorized PR
```

Iteration returns findings to the responsible author. Milestones organize checked implementation; they do not add approvals. Route coordinates authorized work and cannot create a review judgment.

## Existing IR disposition

| Existing owner | Disposition | Reason |
| --- | --- | --- |
| IR-009, portable guided engineering work | Refine its analysis; add SR-079–083 | The request changes the lifecycle and responsibilities of the existing guided-work capability, rather than introducing a new stakeholder need. |
| IR-004, assessment using applicable evidence | Reuse the IR; refine SR-027–029 | Exact review subjects, judgment scope, independence and renewed applicability apply to the new gates and advisory scope. |
| IR-003, controlled Changes and recovery | Reuse | SR-006/007 and SR-023/024 already cover work context, authority, transitions, provenance and retirement. Workflow adoption must satisfy them. |
| IR-008, explicit engineering commands | Reuse | Supported inspection and recording remain CLI responsibilities. Workflow semantics do not require raw SQL or invented commands. |
| IR-001/002/005 and IR-010 | Reuse within their existing scope | Current definitions, traceability, conformance and distribution remain governed by their existing owners. Packaging consequences require later design, not a new need. |

No new IR is proposed. FEAT-016 and FEAT-017 retain their identities and receive clarified scope. Existing SR-053–055 retain specialist-output, coordination and recording ownership. Shared assessment SRs retain their single IR-004 parent.

## Proposed requirement and Scenario changes

| Obligation | New SR | New supporting Scenarios |
| --- | --- | --- |
| Analyze RR against existing owners and justify reuse, refinement or creation | SR-079 | SCN-075 |
| Independently accept the proposed requirement basis before dependent design, without demanding completed Functions or ARs | SR-080 | SCN-076 |
| Preserve three authoring responsibilities and one integrated design assessment | SR-081 | SCN-077 |
| Continue checked, authorized milestones and assess the complete implementation through one review gate | SR-082 | SCN-078–081 |
| Adopt coordinated replacement contracts while preserving historical meanings and active-work authority | SR-083 | SCN-082 |

The [requirement index](README.md#system-requirements) and [Scenario index](scenarios/README.md) link to the authoritative JSON subjects and their assessable criteria. SCN-078 addresses milestone continuation; SCN-079 advisory review; SCN-080 correction reassessment; SCN-081 distinct final Verify and correction ownership.

The five new SRs constrain existing stakeholder capabilities. They do not claim completed Function design, allocation, AR derivation or implementation. Existing Function and architecture records describe their previously analyzed scope; the new criteria require downstream reconciliation. Earlier Scenario confirmations and review judgments do not extend to these draft subjects.

## Coordinated replacement map

| Current responsibility or surface | Target disposition | Owning obligation |
| --- | --- | --- |
| `proposal` and `proposal-review` establish approved direction | RR intake and Requirement Analysis; Requirement Review accepts the exact proposed requirement basis, including justified reuse | SR-079/080 |
| `design` combines requirements and realization | Requirement Analysis owns IR/SR and stakeholder Feature/Scenario analysis; System Design owns logical Functions; Architecture Design owns responsibility, Interfaces, realization and AR derivation | SR-081 |
| `design-review` depends on approved Proposal direction | One integrated assessment of System and Architecture Design against the accepted requirements | SR-080/081 |
| `plan` and `delivery-review` | Consume accepted requirements and reviewed design; define sequencing, proof and completion without mandatory milestone reviews | SR-081/082 |
| `implement`, `code-review`, `verify` and `route` | Checked milestone continuation, optional advisory findings, one whole-change gate with retained attempts, then distinct Verify; corrections return to their owners | SR-082; SR-027–029/054 |
| Constitution, Workflow and Assessment | Reconcile Proposal-first and milestone-review rules together with responsibility and authority boundaries | SR-083 |
| Skill references, templates and terminology | Replace obsolete handoffs; preserve REM Feature meaning and AR allocation rather than delivery-task meanings; load scoped canonical methods | SR-081/083 |
| CLI records, context, validators and transitions | Distinguish stage readiness, milestone progress, advisory scope, whole-change attempts and Verify; do not fabricate approvals to satisfy old validators | SR-083; SR-055 |
| Generated adapters, catalog, tests and packaging | Regenerate from canonical sources and demonstrate the same adopted contract through supported reading and invocation paths | SR-083; existing IR-010 |
| Active and historical Changes | Record explicit adoption disposition for active work; retain old judgments with their original subjects and authority | SR-083; SR-023/024/029 |

The current [Constitution](../../CONSTITUTION.md), [Workflow](../architecture/modules/MOD-017-engineering-governance/modules/MOD-006-engineering-change-control/workflow.md), [Assessment](../architecture/modules/MOD-017-engineering-governance/modules/MOD-007-engineering-verification-and-assurance/assessment.md), and canonical [skills](../../skills/) still contain the existing product contracts. This draft identifies their required replacement; it does not activate a mixture of old and new routing rules. Future adoption must reconcile all live consumers and retire obsolete internal paths together.

## Storage relationship and remaining work

The [local operational-history analysis](sources.md#src-local-operational-analysis) remains a separately owned delivery responsibility. Git retains the current engineering model; the operational store retains work and judgments; artifacts retain bulky evidence. Under the [adoption dependency refinement](sources.md#src-adoption-dependency-refinement), authoring may precede storage delivery, while activation requires the recording support selected by the governing contract. New projects without earlier records need no historical import. Selected work depending on incompatible earlier records needs qualified migration; its absence blocks affected adoption. No empty replacement store, unrelated historical import or deletion of relied-on work is implied.

The completed document-based Requirement Review assessed the exact IR-009 analysis, SR-079–083, refined SR-027–029 and SR-053–055, FEAT-016/017, and SCN-075–082, together with justified reuse conclusions. Its findings, corrections, subject identities and author-assessment limits are recorded in the linked review. Draft status and structural checks are not this judgment.

After an accepted requirement basis, System and Architecture Design can reconcile Functions, Module accountability, Interfaces, ARs, operational record semantics and adoption boundaries. One integrated Design Review precedes the delivery plan. Implementation then replaces the affected contracts and consumers as a coherent change, with the new v4 operational contract realized directly in SQLite after its backup, restoration and import prerequisites are qualified. Workflow design can proceed before storage implementation; no intermediate v4 filesystem adapter is required.

## Authoring validation

`bash scripts/ci.sh --mode local` passed all eight selected REM checks: requirements, system, architecture, projection, browser, current product inventory, current browser output and browser JavaScript syntax. The browser was regenerated with D2 0.9.0. Documentation prose checks and `git diff --check` passed.

The same CI invocation failed `current_records.validate` with `current-record-discovery-unavailable`, the previously observed CLI discovery failure. Consequently this package has structural validation evidence, not a clean overall CI result or reconciled governed review records. Under the subsequent user-authorized exception, this recording failure does not block document-based analysis or review. The document-based review is complete under that exception; independent approval and governed recording are not claimed.

## Current handoff refinement

The user selected current state first, selective supporting detail and compact historical completion. This refines the existing continuity need in IR-003 and reliable command need in IR-008, with SR-006 as the primary handoff obligation; no new IR or handoff subsystem is needed. IR-004 and IR-009 remain the assessment/workflow owners. SR-029 and SR-043 no longer impose permanent copies of every prior observation or judgment. SR-024 distinguishes disposable working detail from explicitly retained engineering history. SR-023 preserves significant transition/completion meaning without requiring every local action. SR-082/083 retain independent assessment and one whole-change gate while permitting current review accounts.

Reuse SCN-023 for context-free resumption, SCN-029/080 for current applicability and reassessment, SCN-044/046 for explicit updates, and SCN-045 for a later problem linked to historical completion. Refine existing Functions and allocations; current operational representation changes do not make engineering definitions database records. Seven handoff sections are a coherent projection from single-owner facts, not seven mandatory files or independently editable copies.

The adoption package must reconcile future workflow/assessment guidance, validators and installed skills with this meaning. Existing v1/v3 runtime and historical preservation contracts are not silently weakened. Backup and engineering Baseline retention preserve their explicitly retained scope; they do not require archiving every future test run. The immediate output is the reconciled requirement/System/Architecture design and its handoff walkthroughs, not implementation or a new delivery plan.
