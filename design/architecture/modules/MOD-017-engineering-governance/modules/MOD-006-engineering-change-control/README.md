# Change control

[MOD-006](module.json) interprets Change context, assesses applicable authority and preserves the meaning of controlled transitions. This Process design refines existing Functions and is maintained directly here as understanding changes. It defines intended behavior; installed workflow behavior and storage support remain separately evidenced. [The parent composition](../../README.md#gate-and-work-state-semantics) owns shared gate semantics and review cooperation. [The system composition](../../../../README.md#requirement-first-workflow-composition) owns cooperation across the top-level Modules.

## Responsibility and collaboration

| Participant | Contribution and boundary |
| --- | --- |
| Skill procedures (MOD-012), including route | Select the next bounded activity from attributable context, dependencies and authority; hand work to the responsible author, implementer or assessor. |
| Change control (MOD-006) | Interpret resumption context through FUNC-025, assess authority through FUNC-026 and retain transition meaning through FUNC-023. A suggestion, recorded fact or favorable review creates no permission. |
| Review and verification (MOD-007) | Support claim/evidence applicability and preservation of scoped judgments. The independent reviewer or verifier supplies the actual assessment. |
| Command handling and Work record storage (MOD-010/011) | Admit supported requests and read or publish the selected records with identity checks and truthful persistence outcomes. |

MOD-017 provides [IF-011](../../../../interfaces/IF-011-engineering-work-context-and-workflow-adoption/interface.json) for activity-context interpretation and [IF-009](../../../../interfaces/IF-009-applicable-governed-action-authority/interface.json) for authority assessment. MOD-006 contributes behavior without becoming a second provider. The caller obtains records through the supported command boundary; semantic interpretation does not itself publish records. The participants are responsibilities and actor roles. The sequence below shows one authorized work slice and its recorded handoff; it introduces no separately deployed services or executable API operations.

## Resume and progress

Start with an identified project, Change, selected workflow contract and requested scope. Read the seven-section current handoff: goal/scope/authority, governing basis, progress, open issues and rationale, relevant evidence, review standing, and next action. Inspect the referenced engineering subjects needed for the next decision, not all historical activity. FUNC-025 exposes missing, stale or conflicting context; a checkout without operational history does not prove that no work occurred. FUNC-026 recognizes applicable standing authority without demanding another approval for an already covered action.

<!-- architecture-diagram: resume-and-progress -->

```d2
shape: sequence_diagram
engineer: "Engineer"
route: "Coordination\nroute"
control: "Change control\nMOD-006"
records: "Command handling and\nWork record storage"
owner: "Responsible\nwork owner"
engineer -> route: "Resume the selected Change within this scope"
route -> records: "IF-004: read selected handoff and bounded support"
records -> route: "Return scoped facts, complete selector index and identity"
route -> control: "IF-011: interpret context; IF-009: assess action authority"
control -> route: "Return eligible work, limits and affected blockers"
route -> owner: "Assign one eligible slice within existing authority"
owner -> control: "Recheck exact action, grant and changed conditions"
control -> owner: "Return applicable basis or specific unmet boundary"
owner -> owner: "Perform covered work and required checks"
owner -> route: "Return actual outcomes, changed subjects and blockers"
route -> records: "Record explicit progress against the inspected identity"
records -> route: "Confirm the actual committed result"
route -> engineer: "Report recorded progress and the next permitted handoff"
```

This sequence shows the successful path for one eligible slice. If context is missing or stale, authority is insufficient, or required dependencies are blocked, coordination returns the affected issue to its owner before assigning that work. It does not interpret an unavailable history as proof of no previous work.

Publication outcomes distinguish a rejected stale update from an interrupted attempt. A failed response after durable commitment is not evidence that the update was absent. Retain the actual work outcome, inspect the supported recovery facts and reconcile before further dependent work; do not blindly replay the action or rewrite unrelated records. Exact storage transactions and recovery remain owned by [Work record storage](../../../MOD-018-engineering-operations/modules/MOD-011-operational-record-persistence/README.md).

Once progress is coherently recorded, route selects the next eligible activity within existing authorization. Completed milestone scope and passing required checks can permit the next milestone without a review assignment. Failed checks, known in-scope defects and unresolved dependencies remain substantive blockers for affected work. A complete implementation candidate is handed to the [parent-owned whole-change review interaction](../../README.md#whole-change-review-and-correction). An isolated slice request does not authorize additional implementation.

Update the handoff when a material blocker, evidence basis, review conclusion, authority limit or next action changes, and before transfer. Routine local runs need no permanent records. Current evidence can be replaced where comparable; open issues survive omission. Completed Changes return a compact historical account without ongoing comparison to the repository; later regression becomes linked new work.

## Current handoff ownership

MOD-006 interprets the seven sections through IF-011; MOD-012 obtains their authoritative records through IF-004 and presents references or derived summaries. Neither creates a second editable copy of a source fact. The selected record contract owns the representation and custody; this table assigns semantic authority.

| Section | Authoritative contribution |
| --- | --- |
| Goal, scope and authority | The Change owner's declared goal and authorized scope, with attributable human grants and applicable policy assessed through IF-009. |
| Governing basis | The selected accepted requirement, Design and delivery bases and their exact subject references; definitions remain with their model owners. |
| Progress and remaining work | The responsible work owner's explicit actual outcome and remaining obligations, recorded on the selected work item. |
| Open issues and rationale | The attributable issue owner and explicit disposition; omission from an update does not resolve an issue. |
| Relevant evidence | The observation producer's scope, method, actual result, limitations and source; a planned check is not an executed result. |
| Review standing | The assessment owner's judgment and applicability on identified subjects and basis; route cannot renew them. |
| Next action, reason and owner | The coordinator's bounded proposal derived from the preceding facts; it is neither an approval nor authority to execute. |

Start with the selected Change handoff and its complete selector index. Request only the supporting bases, work, issues, evidence or reviews needed for the impending decision. An oversized aggregate response requires bounded supported selections; omitted records are not absent records. If one needed fact remains unavailable, expose that gap and its affected work instead of reconstructing private storage or replaying all activity. The public command and record contracts own size limits and selection mechanics.

Keep the project, Change, adopted contract and observed record identity with the interpreted result. Supporting reads used together must describe a coherent decision basis; if the record identity changes during acquisition, reread the affected scope before relying on the combination. Record identity does not protect engineering files or external decisions. Inspect the actual referenced subjects and current authority conditions required by the next action. A changed subject returns review applicability to its owner through IF-010; a previous favorable review is not automatically renewed or rejected solely by the coordinator.

Missing, conflicting and unavailable information remain explicit. A supported not-applicable explanation, a planned/not-run check, an assessment with no findings and an approved judgment retain their distinct meanings. No absent section, empty query, checkout or successful save can manufacture those conclusions.

## Applicable authority at resumption

MOD-006 applies FUNC-026 through parent-provided IF-009 to the proposed action, exact subject/state, participant, project, scope and relevant conditions. The decision basis identifies the applicable policy and decision owner, the attributable grant or standing delegation and its limits, and any known completion, revocation, supersession or condition change. Respect higher-priority runtime and direct user instructions under the Constitution; stored text cannot override them. No new grant is inferred from conversation reconstruction, a routing suggestion or an assessment result.

The initial profile reserves beyond-mandate scope expansion, governing-policy changes, reserved project tradeoffs and release decisions for their applicable human authority. External mutation and destruction require explicit applicable authorization. This is an interpretation of the governing policy, not a universal confirmation step. Recognize a valid prior grant across resumed sessions and covered steps, including standing delegation. A new session alone supplies no reason to ask again. Where there is no reserved boundary, identify the applicable mandate and continue within it.

For revoked, superseded, completed, exceeded or conditionally invalid authority, identify the exact affected action and unmet boundary. Continue separately covered independent work when it remains useful and permitted. A nondelegable decision or higher-authority conflict cannot be bypassed by delegation; an authorization cannot waive required independent assessment. A favorable Design review, passing check or permission for another subject cannot substitute for the action's own basis.

The work owner rechecks action identity and material authority conditions immediately before its governed effect. The earlier interpretation is not a reservation or transferable permission token. If relevant facts change, reassess the affected action and withhold it until covered. Existing action-specific execution safeguards remain necessary: state-control retirement requires its maintained exclusion, and release retains exact-candidate checks. An uncertain previous effect requires scoped outcome inspection and reconciliation before retry; neither a still-valid grant nor a new session authorizes blind repetition.

## Updating and retaining the handoff

Before the next dependent decision or transfer, the work owner supplies actual changed subjects, outcome, remaining work and material blockers to coordination. MOD-012 explicitly publishes the corresponding supported record updates through IF-004 against the inspected identity. MOD-006 prepares meaning; MOD-010 admits requests and MOD-011 owns atomic custody. A stale rejected update requires rereading affected facts and recomputing the update, preserving concurrent work. An uncertain response requires supported readback of actual committed effects before a retry. Until reconciliation, identify the uncertain scope in the handoff and do not advertise an unconfirmed result.

A replacement working summary states its comparable scope and basis and retains the result, limitations and support still needed for current reliance. Do not silently narrow away an unresolved issue, contrary observation or required evidence. Open issues need an explicit attributable resolution, withdrawal, supersession or transfer before their detail can be compacted. A transferred obligation retains an identifiable owner and destination. Routine successful checks need no permanent log; no policy here requires recording every action or retaining every former version.

A restored store describes only its retained state and explicitly unavailable later work. Its old grant or approval does not acquire renewed applicability through restoration; current authority and assessment owners resolve any affected reliance before action. An unavailable or malformed governed store cannot become an empty or completed Change or trigger silent portable fallback. [Work record storage](../../../MOD-018-engineering-operations/modules/MOD-011-operational-record-persistence/README.md#database-schema-backup-and-migration) owns SR-074–077 backup, restoration, transfer and migration; this Module interprets their returned facts.

A completed Change exposes its original outcome, reason, accepted scope, acceptance basis and limitations as a compact historical account. Reading it performs no continuous repository-health comparison. An attributable correction preserves original completion meaning; a later regression opens linked new work. Active unresolved obligations and support still relied upon remain available until coherently disposed of, even when routine historical detail is compacted.

## Realization and acceptance walkthroughs

Realize this responsibility through the existing participant-assisted capability guidance: MOD-012 coordinates supported scoped CLI reads/writes, MOD-006 supplies semantic interpretation and action-authority assessment, and independent assessors retain their judgments. The owning skill procedures and IF-004/Records contracts are the intended integration surfaces. No additional service, permission-token store, public command, lifecycle vocabulary or duplicate handoff database is required. Adoption into installed guidance and executable behavior needs its own implementation evidence; the Architecture browser displays the proposed design only.

AR-077 derives the resumption obligation from SR-006 and constrains FUNC-025. AR-078 derives action-bound authority from SR-007 and constrains FUNC-026. Both have one accountable owner, MOD-006. Existing AR-035/038 retain workflow progression and adoption scope; AR-074/075 retain controlled transitions and retirement. The new ARs supply complete resumption and authority obligations without transferring those responsibilities or duplicating custody ARs.

| Walkthrough | Required architectural outcome |
| --- | --- |
| SCN-023: another participant resumes with a valid standing grant and a planned check | Read the seven sections and bounded supporting facts, identify the eligible next owner/action, retain the check as not run and reuse the applicable grant. |
| Large context, changed record identity or unavailable referenced subject | Use complete selectors and bounded reads; refresh the affected inconsistent basis or expose the exact gap. No truncation, empty-history inference or invented approval. |
| Concurrent publication or lost response after commit | Preserve actual work, inspect current committed facts, recompute only the affected update and return confirmed persistence or explicit uncertainty. |
| Summary replacement with an omitted open issue or contrary evidence | Preserve unresolved obligations and current reliance; require explicit attributable disposition before compaction. |
| Restored or completed account | Identify retained history and unavailable later work; no renewed authority/review, invented completion or current-health claim. |
| SCN-024: valid prior authorization across sessions | Bind the same covered action and current conditions to its existing grant without redundant confirmation. |
| Revocation, scope expansion, nondelegable decision or higher-authority conflict | Withhold the affected action and identify its exact decision boundary; preserve independently covered work. |
| Favorable review, unrelated grant or uncertain prior external effect | Keep assessment and permission separate; inspect actual effects before retry and preserve action-specific safeguards. |

These walkthroughs allocate acceptance proof for all eight SR-006 and six SR-007 criteria and their two ARs. They are review cases, not executed implementation verification. The [system composition](../../../../README.md#controlled-work-and-recoverability) relates these outcomes to SR-074–077 maintenance and the direct IR-003 need; coverage and actual execution judgments remain separately recorded.

## State and approval distinctions

| Fact | What it establishes |
| --- | --- |
| Milestone progress and check outcomes | Work actually performed within its scope, remaining work and blockers; no review approval. |
| Advisory findings | Feedback on the inspected subjects; serious defects still require disposition, but advice cannot settle the formal gate. |
| Review attempt | One attributable judgment on exact subjects and governing basis; retain its basis while relied upon; superseded detail may be compacted after issue disposition. |
| Applicable whole-change approval | An assessor-supported conclusion for the complete current candidate, including justified retained coverage after corrections. |
| Verify result | A separate scoped assessment of whether current evidence supports completion. |
| Authority assessment | Whether a specific proposed action is covered by applicable policy and grants; evidence and approval cannot substitute for it. |
| Persistence outcome | What was actually retained or remains to recover; a successful save creates no engineering judgment. |

These facts remain separately attributable. A changed engineering subject or contrary evidence returns approval applicability to the assessment owner. Pure bookkeeping does not automatically restart review. This design does not introduce a single global stage flag or a new lifecycle-state vocabulary; a state diagram is deferred until explicit transition conditions warrant one.

## Verification intent and limits

Inspect a resumed Change with one completed milestone and remaining authorized work: its next assignment must not require a milestone review. Contrast failed checks, exhausted slice authority and unavailable history; each must expose its actual affected boundary without inventing completion or permission. For a concurrent record update, preserve the first actor's facts and require fresh interpretation before retrying publication. For response failure after commitment, distinguish actual stored progress from the uncertain response before continuing. These walkthroughs and the acceptance cases above define the checks for SR-006/007/023 and AR-035/077/078; actual execution results remain separate evidence.

[Operations' existing SCN-078–081 groups](../../../MOD-018-engineering-operations/test-design.md) own integrated progression, advisory, correction and Verify observations. [The parent composition](../../README.md#whole-change-review-and-correction) owns the shared review interaction. FUNC-024 retirement and FUNC-078 adoption keep their existing definitions and [parent adoption/recovery design](../../README.md#adoption-and-recovery); their detailed Process diagrams remain outside this bounded refinement.

## Browser presentation

The existing [Change control Process page](../../../../views/browser/index.html#process/MOD-006) shows Resume and progress as the current design. Its Parent composition section links the parent's review/Verify and correction sequences without duplicating its source or transferring ownership. Revise these owning sources directly when the design changes, then regenerate the browser. The optional local registration selects the D2 block above; the generated browser preserves its source identity and distinguishes design from implementation observations.

## Supporting contracts

These documents retain detailed clauses and proof under this Module; they are not additional REM entities.

- [Delivery Handoff Design](delivery-handoff.md)
- [Plan Design](planning.md)
- [Workflow](workflow.md)
