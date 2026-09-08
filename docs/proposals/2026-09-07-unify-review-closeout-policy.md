# Unify Review and Closeout Policy Ownership

## Challenge

RigorLoop's review and closeout rules are distributed across the Workflow model, review skills, routing and verification guidance, and delivery-plan templates. These surfaces need related information, but it is not consistently clear which owns a policy and which applies it.

The [Code Review skill](../../skills/code-review/SKILL.md) already requires final holistic review of the complete final diff and cross-milestone interactions. The [plan skill](../../skills/plan/SKILL.md) also requires final whole-change review dependencies. Nevertheless, the delivery plan described in the incoming request does not explicitly name that assessment before final Verify. That particular plan was not identified in the request; it is reported motivation, not independently verified evidence. The problem is therefore not simply a missing review capability: an existing obligation can be lost between policy, planning, execution, and closeout.

Similar ownership questions affect independence, review scope, judgment versus applicability, finding disposition, correction routing, and the meaning of successful Verify. Adding another copy of each rule to every skill would increase maintenance and agent context without establishing one authority.

## Goals

Establish one authoritative owner for shared review and closeout policy; make every review's scope and consequence explicit; preserve fresh independent whole-change Code Review before successful final Verify; and align planning, routing, review, and verification without adding lifecycle gates or CLI-owned readiness enforcement.

Reduce duplicated instructions while retaining the stage-specific reasoning and sufficient evidence needed for each assessment. Token savings are an intended benefit, not a measured result.

## Scope and non-goals

In scope are Proposal Review, Design Review, Delivery Review, milestone and final Code Review, final Verify, and their policy dependencies in Workflow, plan, route, and downstream handoff guidance. The change includes affected canonical skill instructions, conditional references, templates, examples, governing references, and generated adapter packages. Generated package changes must flow from canonical sources through the existing packaging process; release archives are not new tracked skill sources.

This proposal does not merge the specialized review skills, introduce a new review stage, replace final Code Review with Verify, remove existing review obligations, require standalone advisory requests to execute the full governed lifecycle, or make the CLI decide readiness. It does not require completion of the separate spec/architecture-to-design skill refactor.

Record Format remains the owner of stored representation, and CLI remains the owner of mechanical inspection, construction, validation, and persistence. No new record type, schema version, approval service, history ledger, or automatic migration is selected by this proposal. Release, PR creation, publication, and destructive-action authority remain separately owned.

### Initial intent treatment

| Goal or concern | Treatment | Destination |
| --- | --- | --- |
| One owner for shared review and closeout obligations | in scope | Review and Closeout model within Workflow |
| Explicit review scope, consequence, independence, applicability, and disposition | in scope | Shared policy applied by specialist skills |
| Fresh final whole-change Code Review before successful Verify | in scope | Mandatory closeout checkpoint identified in delivery planning |
| Preserve specialization and reduce duplicated instructions and context | in scope | Coordinated consumer alignment with selective loading |
| Separate judgment, recording, applicability, and continuation; keep corrections recordable | in scope | Actor-owned decisions with CLI mechanical authority |
| Align canonical guidance and generated packages without customer dependence on internal design files | in scope | Portable packaged operational guidance |
| Add gates, merge skills, replace Code Review with Verify, or restore CLI readiness enforcement | rejected option | These alternatives weaken the selected responsibility boundaries |
| Require the separate Design skill refactor or select schemas, migration, or publication | out of scope | Those decisions retain their separate owners |

### Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Review and Closeout policy ownership and affected Workflow revision | core to this proposal | Establish one authoritative definition and its coordination boundary |
| Final whole-change review obligation and plan closeout checkpoint | core to this proposal | Prevent an existing assessment obligation from disappearing during delivery |
| Proposal, Design, Delivery, and Code Review skills; Verify, plan, route, and handoff consumers | same-slice dependency | Every affected policy consumer must agree before adoption |
| Conditional references, templates, examples, governing references, and generated adapter packages | same-slice dependency | Policy extraction must remain usable and coherent in installed skills |
| Current-rule ownership mapping and historical applicability analysis | same-slice dependency | Preserve existing obligations and the meaning of prior approvals |
| Record Format or CLI changes | same-slice dependency | Only a concrete representation or mechanical-interface gap found in Design justifies a change; otherwise retain these surfaces |
| Separate spec/architecture-to-design skill refactor | out of scope | This direction does not depend on completing that initiative |
| New record types, schema versions, approval services, history ledgers, automatic migration, and external publication | out of scope | No such decision or authority is selected here |

These classifications describe adoption dependencies, not implementation sequencing. Design determines exact affected surfaces; Delivery allocates reviewable milestones without silently deferring an affected consumer.

## Governing principle

> Define each review and closeout obligation once, apply it through the responsible specialist skill, and record its judgment without confusing it with permission to perform unrelated work.

## Proposed direction

Establish a **Review and Closeout** model as a bounded policy responsibility within the Workflow domain, with one authoritative Design document. It is not another runtime component, lifecycle stage, or public review skill.

The new model should own shared assessment requirements: required review scopes, independence, the meaning and limits of judgments, applicability after changes, finding and blocker disposition responsibilities, rereview expectations, and the conditions for justified final closeout. Workflow should reference these obligations when coordinating activities instead of maintaining a second definition.

Keep Proposal Review, Design Review, Delivery Review, and Code Review specialized. Each skill applies the shared policy while retaining the methods appropriate to its subject. Verify remains a distinct final evidence/coherence assessment, not a replacement code reviewer.

Every governed change must receive a fresh independent whole-change Code Review after all implementation milestones and their required corrections are complete, and before successful final Verify. Prior milestone judgments may inform the final assessment but do not substitute for it. The delivery plan must identify this as a closeout checkpoint rather than implementation work.

Corrections return to the owning author or implementation activity. Revised engineering subjects require the appropriate independent reassessment. Recording a review, blocker, evidence result, or final explanation must not automatically invalidate the engineering assessment merely because storage bookkeeping changed; relevant new evidence must still be considered before reliance.

Separate substantive judgment, durable recording, current applicability, and workflow continuation. A successful CLI save grants none of the other conclusions. Structurally valid blockers and corrections remain recordable even when review or Verify cannot justify progression.

Align the existing skills and templates with the owning model. Common operational guidance may be shared and packaged for installed skills, but it must not become a second policy owner or require customer projects to contain RigorLoop's internal design repository. Keep normal reading proportional to the invoked assessment.

## Feasibility

**Assessment: Feasible as a coordinated policy extraction and consumer refactor; exact relocation and compatibility need Design work.**

The [Workflow model](../design/workflow/workflow.md), [Code Review skill](../../skills/code-review/SKILL.md), and [plan skill](../../skills/plan/SKILL.md) already express decision ownership, independence, current-subject assessment, correction paths, and final review obligations. The [Verify skill](../../skills/verify/SKILL.md) retains success-only closeout. Much of the work is identifying authoritative ownership and reconciling consumers, not inventing another review mechanism. The reported delivery-plan omission is not necessary to establish this feasibility basis.

Before adoption, Design must map each affected current rule to its retained or replacement owner and distinguish historical-contract behavior from the selected current policy. Stable references and existing approvals must not silently acquire new meaning.

The minimum Design package is the new Review and Closeout model plus the affected Workflow revision. [Record Format](../design/record-format/record-format.md) and [CLI](../design/cli/cli.md) require changes only when that analysis identifies a concrete representation or mechanical-interface gap. A policy extraction alone does not justify a schema or command change. No known factual blocker prevents responsible Design; unresolved ownership, compatibility, or packaging contradictions would block adoption until their owning stage resolves them.

## Impact and major trade-offs

A separate policy model adds one design surface, but can reduce competing definitions across many skills. That benefit depends on removing redundant normative ownership and replacing it with explicit references, rather than copying the rules into a fourth place.

Shared guidance can reduce repeated context, but a large universal review manual could make every invocation more expensive. Stage-specific methods and selective loading must remain usable in published packages.

Fresh final whole-change review creates deliberate assessment cost for every governed change, including small changes. Its depth may scale with the change, but milestone reviews alone do not waive it. This policy does not require every validation command to rerun when its evidence remains applicable under the governing contract.

## Decision requested

Approve reorganizing all review-stage and closeout policy around one authoritative Review and Closeout model within the Workflow domain, while retaining specialized skills, independent assessment, the existing gate sequence, and CLI storage-only authority.

Approval includes mandatory fresh independent whole-change Code Review after implementation and before successful final Verify, plus coordinated alignment of planning, review, routing, verification, and handoff consumers.

**Approval authorizes detailed Design of ownership, shared policy, and consumer changes. It does not approve exact file layout, requirement renumbering, serialized fields, command changes, historical supersession, automatic migration, implementation, or activation.**
