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
route -> records: "Read current work, evidence and record identity"
records -> route: "Return attributable context and current identity"
route -> control: "Interpret context, inspected subjects and authority"
control -> route: "Return eligible work, limits and affected blockers"
route -> owner: "Assign one eligible slice within existing authority"
owner -> owner: "Perform the work and required checks"
owner -> route: "Return actual outcomes, changed subjects and blockers"
route -> records: "Record explicit progress against the inspected identity"
records -> route: "Confirm the actual committed result"
route -> engineer: "Report recorded progress and the next permitted handoff"
```

This sequence shows the successful path for one eligible slice. If context is missing or stale, authority is insufficient, or required dependencies are blocked, coordination returns the affected issue to its owner before assigning that work. It does not interpret an unavailable history as proof of no previous work.

Publication outcomes distinguish a rejected stale update from an interrupted attempt. A failed response after durable commitment is not evidence that the update was absent. Retain the actual work outcome, inspect the supported recovery facts and reconcile before further dependent work; do not blindly replay the action or rewrite unrelated records. Exact storage transactions and recovery remain owned by [Work record storage](../../../MOD-018-engineering-operations/modules/MOD-011-operational-record-persistence/README.md).

Once progress is coherently recorded, route selects the next eligible activity within existing authorization. Completed milestone scope and passing required checks can permit the next milestone without a review assignment. Failed checks, known in-scope defects and unresolved dependencies remain substantive blockers for affected work. A complete implementation candidate is handed to the [parent-owned whole-change review interaction](../../README.md#whole-change-review-and-correction). An isolated slice request does not authorize additional implementation.

Update the handoff when a material blocker, evidence basis, review conclusion, authority limit or next action changes, and before transfer. Routine local runs need no permanent records. Current evidence can be replaced where comparable; open issues survive omission. Completed Changes return a compact historical account without ongoing comparison to the repository; later regression becomes linked new work.

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

Inspect a resumed Change with one completed milestone and remaining authorized work: its next assignment must not require a milestone review. Contrast failed checks, exhausted slice authority and unavailable history; each must expose its actual affected boundary without inventing completion or permission. For a concurrent record update, preserve the first actor's facts and require fresh interpretation before retrying publication. For response failure after commitment, distinguish actual stored progress from the uncertain response before continuing. These walkthroughs define the checks for SR-006/007/023 and AR-035; actual execution results remain separate evidence.

[Operations' existing SCN-078–081 groups](../../../MOD-018-engineering-operations/test-design.md) own integrated progression, advisory, correction and Verify observations. [The parent composition](../../README.md#whole-change-review-and-correction) owns the shared review interaction. FUNC-024 retirement and FUNC-078 adoption keep their existing definitions and [parent adoption/recovery design](../../README.md#adoption-and-recovery); their detailed Process diagrams remain outside this bounded refinement.

## Browser presentation

The existing [Change control Process page](../../../../views/browser/index.html#process/MOD-006) shows Resume and progress as the current design. Its Parent composition section links the parent's review/Verify and correction sequences without duplicating its source or transferring ownership. Revise these owning sources directly when the design changes, then regenerate the browser. The optional local registration selects the D2 block above; the generated browser preserves its source identity and distinguishes design from implementation observations.
