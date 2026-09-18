# Delivery Handoff Design

Model validation contract: model-document-v1

## Responsibility and scope

Delivery Handoff owns the existing `pr` capability’s scoped behavior, output and failure boundaries. Its detailed procedure below preserves the current specialist contract.

Parent: [Skill](skill.md). [Skill](skill.md) retains shared invocation, evidence-access, resource and portability rules. [Workflow](workflow.md) coordinates authorized activity; [Assessment](assessment.md) owns independent judgment and reliance. This decomposition changes no public invocation, stored format or external permission.

## Requirements

| ID | Required behavior |
| --- | --- |
| HAND-SR-01 | Delivery Handoff MUST distinguish prepare-only, open and draft intent; preparation MUST cause no external mutation and a blocked open/draft MUST NOT be reported as successful preparation. |
| HAND-SR-02 | External actions MUST be bound to current verified subjects and explicit authority; branch relation, existing PR, refresh and state-transition constraints MUST be checked before each action. |
| HAND-SR-03 | Retry and result claims MUST reflect exact observed remote/PR/CI state, preserve successful partial effects and stop on ambiguity or drift without force-push, merge or release publication. |
| HAND-SR-04 | Current PR body guidance MUST cite successful Verify as the owner of final change rationale and MUST NOT require a separate Explain-change artifact. Existing core and conditional traceability groups remain; required architecture/decision context may link to its living Design owner without inventing a standalone ADR. This presentation change grants no readiness or mutation authority. |

## Architecture Overview

```mermaid
flowchart LR
    User["User: submission and mutation authority"] -->|"requested intent"| Resolve
    Verify["Assessment: exact current Verify basis"] -->|"verified subjects and limits"| Resolve
    subgraph Owned["Delivery Handoff"]
        Resolve["Resolve intent, identity and readiness"] -->|"actual diff and evidence"| Prepare["Prepare PR title and body"]
        Prepare -->|"authorized open, draft or refresh"| Publish["Recheck and perform bounded mutation"]
        Publish -->|"actual effects"| Readback["Observe exact PR and CI state"]
    end
    Publish -->|"ordinary push under authority"| Remote["Git remote"]
    Publish -->|"authorized PR mutation"| Host["PR host"]
    Remote -->|"observed head relation"| Resolve
    Host -->|"PR identity, state and run/head"| Readback
    Prepare -->|"prepare-only: no external write"| Result["Result with limits"]
    Readback -->|"observed outcome"| Result
```

The overview identifies the owned responsibility and external authority/evidence boundaries. Detailed behavior is in the contract sections below; output does not imply adoption or approval.

| View | Necessity and reason | Owning detail |
| --- | --- | --- |
| Context | Necessary: verified local subjects, Git remote and PR host have separate authority and observation boundaries. | [Context view](#context-view). |
| Building Block | No separate diagram: classification and the specialist operation form one method; no separate internal subsystem is selected. | [Specialist contract](#specialist-contract). |
| Runtime | Necessary: authority, resource failures and partial or blocked outcomes must remain distinct from successful handoff. | [Runtime view](#runtime-view). |
| Deployment | No separate diagram: this is published guidance, not a separately deployed service. External host mutation is governed by the PR contract below. | [Skill Deployment](skill.md#deployment-view). |


## Specialist contract

PR distinguishes `open`, `draft` and `prepare-only`; explicit pr defaults to open. Preparation has no external mutation. Exact verified repository/remote/base/merge-base/head/subject identities from Verify are required before opening; evidence-tail compatibility follows Assessment's current contract. Resolve actual diff, clean handoff, current remote base, directional head relationship and matching PR. Only absent or ancestor remote heads permit an ordinary push; ahead/diverged/ambiguous state stops. Recheck before push and before host mutation, then read back exact PR/head/base/title/body/state before a result claim. Adequate open/draft PRs are reused; refresh and state conversion each need their own matching authority. Closed/merged/ambiguous matches do not permit reopening or duplicate creation. Retry reconciles observed state. Successful external writes remain reported even if later identity drift blocks readiness. Hosted CI success needs the exact observed run/head. PR does not force-push, merge, publish releases, alter governing state or substitute for Verify.

## Interface vocabulary and outputs

The following public domains retain their existing meanings. Unknown values reject before consistency checks; recognized values still require the operation’s authority and prerequisites.

| Capability / independent axis | Supported values |
| --- | --- |
| PR submission | open, draft, prepare-only |
| PR refresh authority | none, explicit-title-refresh, explicit-full-replacement, workflow-title-refresh |
| PR state-transition authority | none, publish-existing-draft, convert-existing-open-to-draft |
| PR remote branch relation | absent, same, remote-ancestor-of-local, local-ancestor-of-remote, diverged, ambiguous |
| PR state | absent, open, draft, closed, merged, ambiguous |
| PR operation result | opened, draft-opened, updated, reused, prepared-not-opened, blocked |
| PR hosted-CI state | passed, failed, pending, unavailable, unobserved, not-applicable |
| PR evidence suffix | none, evidence-only, invalidating |

PR reports requested intent, actual operation, actual_external_mutation or none, actual PR state or none, pr-body-ready, pr-open-ready, hosted-CI state, blockers, read-back URL and claim limits. Preparation returns prepared-not-opened with no external mutation. Requested open/draft cannot silently become successful preparation on a blocker. Existing draft/open state is preserved without independent transition authority. Refresh supports only an authorized title or whole-body replacement; no managed-section parser or implied content ownership is introduced. Core PR body groups remain Summary, Why, What changed, Tests and verification, Risks and rollback, Reviewer notes and Follow-ups; governed traceability and material-impact groups are conditional. Required unresolved data blocks opening; no placeholder is emitted.

Governed-signal classification remains shared with Bugfix under [Skill’s shared interface vocabulary](skill.md#specialist-interface-vocabulary-and-outputs). The [bounded PR CI-repair exception](skill.md#bounded-pr-ci-repair) remains owned by CI maintenance; this model consumes its exact result and Assessment’s continued-reliance judgment without granting repair or external authority. Delivery Handoff covers the PR capability; release publication remains with Engineering Release.

### Current rationale and artifact labels

The [complete refinement round](../../proposals/2026-09-15-refine-skills-and-retire-stale-support.md) removes the obsolete `Explain-change` path prompt from `skills/pr/assets/pr-body-skeleton.md`. The lifecycle group names the successful Verify report and its change rationale once. Architecture and decision context links to the actual governing Design or explicitly retained project source; it must not suggest that a separate architecture document or ADR is a prerequisite. Keep the core body groups and applicable requirement, review, migration, security and release evidence. Retained customer sources remain usable under their own authority.

This corrects presentation under Assessment's existing explanation ownership. It introduces no additional artifact, parser, body schema, section-refresh authority or readiness field. Missing successful Verify or its required Git basis still blocks opening. Historical PR bodies and assessment identities remain unchanged. Skill owns the PR entrypoint's presentation and conditional read-only resource; this model continues to own the external action and output behavior. Existing views require no new node or edge.

## Context view

```mermaid
flowchart LR
    Authority["User and project authority"] -->|"permitted submission and mutation"| Handoff["Delivery Handoff"]
    Assessment["Assessment and Verify"] -->|"current subject basis"| Handoff
    Handoff -->|"authorized ordinary push"| Git["Git remote"]
    Handoff -->|"authorized PR operation"| Host["PR host"]
    Git -->|"exact observed remote head"| Handoff
    Host -->|"read-back PR and CI run/head"| Handoff
```

A host observation cannot substitute for the required Verify basis. Local preparation alone grants neither push nor host-mutation authority. Release publication remains outside this boundary.

## Runtime view

```mermaid
flowchart TB
    Input["Resolve requested operation and current evidence"] --> Ready{"Target, authority and resources sufficient?"}
    Ready -->|"no"| Stop["Report owned blocker; preserve existing work"]
    Ready -->|"yes"| Act["Prepare; perform only individually authorized external actions"]
    Act --> Changed{"Basis changed or partial failure?"}
    Changed -->|"yes"| Partial["Report exact effects and required reassessment or recovery"]
    Changed -->|"no"| Output["Return artifact, conclusions and limits to owner"]
```

The specialist contract determines the permitted action and retry, including read-only or preparation-only operations. A successful artifact write does not grant downstream execution. Reconcile changed basis before dependent work and report partial effects truthfully.

### Boundary scan and acceptance scenarios

| Dimension | Requirement basis | Distinct outcome to demonstrate |
| --- | --- | --- |
| Input domain | HAND-SR-01, HAND-SR-02, HAND-SR-03 | Unknown or ambiguous submission/branch/PR states reject before mutation eligibility. |
| State/lifecycle | HAND-SR-01, HAND-SR-02, HAND-SR-03 | Prepare-only changes no external state; adequate existing PRs retain their actual state. |
| Identity/authority | HAND-SR-01, HAND-SR-02, HAND-SR-03 | Missing current Verify identity or refresh/state-transition authority blocks the corresponding action. |
| Composition/path | HAND-SR-01, HAND-SR-02, HAND-SR-03, HAND-SR-04 | A completed bounded CI repair is consumed only under Assessment’s still-applicable decision basis. A governed body points to the successful Verify rationale without demanding a second explanation artifact or an unnecessary standalone ADR. |
| Temporal/retry | HAND-SR-01, HAND-SR-02, HAND-SR-03 | Recheck head/base and authorization before push and host mutation; retries reconcile the observed PR. |
| Failure/recovery | HAND-SR-01, HAND-SR-02, HAND-SR-03 | A successful external write followed by identity drift is reported as a partial effect, not erased. |
| Compatibility/migration | HAND-SR-01, HAND-SR-02, HAND-SR-03, HAND-SR-04 | Closed/merged matches do not authorize reopening or duplicate creation; evidence suffix compatibility remains Assessment-owned. A governed body points to the successful Verify rationale without demanding a second explanation artifact or an unnecessary standalone ADR. |
| External/environment | HAND-SR-01, HAND-SR-02, HAND-SR-03 | Hosted success requires the exact observed run/head; unavailable host state cannot be fabricated. |

### Test design

Apply [System's selection and proof rules](../test-design/rules.md#select-requirements-and-proof). HAND-SR-01–04 require truthful preparation, independently authorized mutation, exact current verification/remote evidence and useful PR rationale. Select decision tables for intent/authority/branch relationships and ordered walkthroughs for drift and lost-response recovery. Unauthorized pushes, duplicate PRs and false readiness are distinct failures; a body-content assertion cannot protect them.

| Behavior group and requirement basis | Concrete fixture and faulty candidate | Action and independently expected observation |
| --- | --- | --- |
| Intent and independent authorities — HAND-SR-01, HAND-SR-02 | A valid verified packet permits prepare-only; another requests open with an existing adequate draft and no transition authority. Contrast compliant prepared/reused results with candidates pushing during preparation, publishing the draft automatically or reporting blocked open as successful preparation. Independent variants introduce an unknown declared axis value. | Inspect intended actions, authority and result. Preparation makes no external write and reports prepared-not-opened. Requested intent stays visible when blocked; refresh and state conversion require their own matching authority. Unknown values reject before consistency decisions. A title-only refresh preserves literal body bytes; no section parser or inferred content ownership is permitted. |
| Verification basis and evidence suffix — HAND-SR-02 | Supply a current successful Verify with exact repository, remote, base, merge-base, head and verified-subject identities. Compare unchanged and attributable evidence-only descendant handoffs with mixed implementation/evidence, cross-change, stale, non-ancestor and prose-only variants. The faulty candidate reconstructs a missing basis from current Git or accepts filenames as evidence authority. | Review the cumulative diff and Assessment's exact applicability account. Open only from the required current basis; invalidating or ambiguous suffixes return to their owner for review/Verify. Preparation cannot manufacture readiness. A bounded CI-repair result remains subject to Assessment's continued-reliance decision and grants no new external authority. |
| Directional branches and exact PR selection — HAND-SR-02, HAND-SR-03 | A controlled observation packet supplies absent, same, remote-ancestor, local-ancestor, diverged or ambiguous remote-head relationships and absent, adequate open/draft, closed/merged or multiple matching PRs. The faulty candidate fast-forwards in the wrong direction, force-pushes, reopens or creates a duplicate. | Derive allowed actions from independently drawn commit relations and exact repository/head/base PR matches. Absent/remote-ancestor permits authorized ordinary push, same needs none, and ahead/diverged/ambiguous blocks. Reuse adequate open/draft with state preserved; closed/merged or ambiguous matches stop. No merge, remote overwrite or release publication occurs. |
| Recheck, partial success and retry — HAND-SR-02, HAND-SR-03 | Start with permitted push and absent PR. In separate variants change base before push, change PR body/state before host mutation, or lose the response after successful PR creation. The faulty candidate continues from the old basis, erases its successful push from the report or creates a second PR on retry. | Trace each recheck and supplied read-back. Reclassify before the affected action, preserve observed successful partial effects and set readiness false after invalidating drift. Retry reconciles the exact remote/PR state before any mutation. Final URL/head/base/title/body/state claims require matching read-back, not an assumed successful response. |
| Body rationale, resources and hosted CI — HAND-SR-03, HAND-SR-04 | A successful Verify report supplies final rationale; living Designs own architecture context. The compliant body retains core/applicable traceability and impact groups. Faulty candidates demand Explain-change or a standalone ADR, leave placeholders, or call a local pass or an old-head hosted run current CI success. | Inspect body completeness, exact evidence links and observed run/head. Required unresolved content blocks opening; no duplicate rationale artifact is required. Hosted success needs current exact-head evidence; pending, failed, unavailable and unobserved remain distinct, with not-applicable justified. Missing governed reference or body asset stops the dependent readiness/body/mutation action without reconstruction. |

Use fresh synthetic local/remote/host packets with explicit authorities, independently specified commit graphs, literal PR body bytes, stable remote observations and event order. Each compliant and faulty candidate includes its proposed external effects and report. No real network or external mutation is needed to review these decisions; controlled host facts cannot establish an actual hosted CI or PR result. Any future executable realization claiming Git or host interaction must exercise the actual claimed boundary under its own authority and report its environment limits. HAND-SR-04's earlier presentation refinement survives as the current body/rationale requirement; it does not require replaying the historical rollout or rewriting earlier PR bodies and judgments.

Existing [PR guidance tests](../../../tests/skill/skill_pr_guidance_tests.py) check package/resource inventory, body headings and phrases describing vocabularies, directionality, authorization, rechecks, retry and hosted-CI limits. Their `test_closed_vocabularies_reject_unknown_values_first` asserts that the values and instruction are present; it does not execute an unknown-value rejection. These are existing structural observations. All five semantic groups remain proposed independent review of current [PR guidance](../../../skills/pr/SKILL.md), triggered resources and concrete candidate decisions. Delivery must allocate packets and record assessed outcomes; no current external-action proof is claimed. [Assessment](assessment.md) owns verification/reliance judgment, while the [Skill parent handoff scenario](test-design/cases/capability-composition.json) owns the wider capability interaction. The existing context/runtime views already show the required actors and external boundaries, so no new view is required.

## Architecture Decisions

| ID | Decision and rationale | Alternatives and consequences |
| --- | --- | --- |
| HAND-DEC-02 | Name Verify as the sole current final-rationale artifact in the PR asset and accept architecture context from its actual Design owner. | Retaining a separate Explain-change prompt can invent work for a retired stage. Removing rationale or evidence requirements would weaken review; this change removes only the obsolete duplicate artifact expectation. |
| HAND-DEC-01 | Give Delivery Handoff one explicit current owner while retaining shared Skill policy and the specialist’s existing authority boundaries. | Keeping unrelated support duties together obscures responsibility. Duplicating their details in Skill would create competing owners; scoped extraction requires reconciled navigation and review. |

## Quality and limits

Review outcomes against actual inputs, authority and observable effects; structural checks alone do not establish adequacy. Preserve historical subjects, existing public vocabulary and required resource behavior. Unresolved material authority or evidence gaps stop dependent claims rather than inventing a successful outcome.
