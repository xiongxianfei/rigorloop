# Simplify published skills using current Designs

## Challenge

RigorLoop skills must help an agent understand its responsibility, find applicable guidance and complete a bounded task correctly. Repeated instructions, overlapping sections and detailed conditional procedures in the main entrypoint can make that task harder to follow and maintain.

The current [Skill Design](../design/skill/skill.md#conditional-resources) already calls for useful operating entrypoints, explicit resource triggers and sufficient specialist guidance. An initial inventory found 19 entrypoints totaling 3,291 lines; `implement` and `code-review` contain 285 and 291 lines respectively. These counts identify inspection candidates, not proven defects or efficiency savings. The opportunity is to reconcile published guidance with current Designs and remove unnecessary reading and interpretation work while preserving required behavior.

## Goals

- Make each skill's purpose, inputs, procedure, outputs and handoff easy to understand and execute.
- Simplify instructions against their current owning Designs, preserving specialist judgment, evidence obligations, authority boundaries and failure handling.
- Keep conditional guidance discoverable and complete without loading irrelevant procedures.
- Cover the published skill inventory, retaining already-compliant guidance with a reason instead of requiring edits everywhere.
- Preserve standalone customer-project use and coherent generated and installed packages.

## Scope and non-goals

The initiative covers authored entrypoints and supporting resources under `skills/`, together with directly affected shared sources, validation and packaging consumers. All goals above remain in scope; the pilot bounds initial delivery, not the overall inventory commitment.

| Work item | Treatment | Reason and destination |
| --- | --- | --- |
| Inventory skills and map guidance to current owning Designs | core to this proposal | Establish justified changes and explicit no-change dispositions across the inventory. |
| Simplify `implement` and `code-review` | first-slice candidate | Exercise implementation and assessment responsibilities with substantial entrypoints; Design confirms suitability and Delivery allocates the slice. |
| Reconcile affected shared guidance, resource maps and validation/package consumers | same-slice dependency | A simplified skill must retain a complete, consistent supported execution path. |
| Apply justified improvements to remaining skills | separate implementation slice | Keep the full inventory in this initiative; the owning delivery plan allocates coherent batches. |
| Change workflow policy, review gates, permissions, public invocations or stored-record formats | out of scope | Such changes need their own direction decision. |
| Restore token-cost tooling, impose length quotas or introduce a universal skill template | out of scope | These do not establish clarity or correct task execution. |
| Publish a release or install into user environments | out of scope | Packaging validation does not grant external handoff or installation authority. |

## Governing principle

Make the required task easier to understand and perform while preserving every applicable obligation.

## Proposed direction

Use current owning Designs as the behavioral basis for assessing each skill. Retain necessary instructions, simplify wording and ordering, remove superseded or redundant procedure, and place substantial conditional detail behind explicit resource triggers. Keep the main entrypoint sufficient to select and perform its core task, including its essential limits and handoff.

Use references for applicable methods and detailed procedures, and assets for usable output structures. Preserve specialist differences and consistent local reminders where they prevent mistakes. Installed packages must supply their required guidance without depending on RigorLoop's internal Design repository.

For each affected obligation, establish its surviving location or justified removal; distinguish obsolete prose from still-supported portable behavior. The existing proposal-family treatment in [Skill's solution strategy](../design/skill/skill.md#solution-strategy) provides a scoped precedent, not approval for other skills. Reconcile the affected Designs and consumers before implementation. Any discovered need to change required behavior returns to its owner for a direction decision.

Judge success by clear task execution, complete applicable guidance and preserved outcomes across supported invocation contexts. Detailed resource factoring, batch allocation and proof selection belong to Design and Delivery.

## Feasibility

Assessment: feasible within the current product architecture. [Skill](../design/skill/skill.md#evidence-access-and-proportional-effort) already supports concise entrypoints and conditional loading; [Assessment](../design/skill/assessment.md) requires specialist reasoning and portable guidance; [Packaging](../design/engineering/packaging.md) supplies existing generation and resource-integrity boundaries. No new runtime or distribution model is needed.

The principal uncertainty is how much guidance is actually redundant once standalone, governed and conditional paths are considered. The inventory and pilot must establish that before broader edits. Moving text alone does not demonstrate better usability, and current wording checks may require reconciliation while preserving their behavioral protection. No blocker to beginning Design is known; this proposal does not claim an inventory-wide audit or measured savings.

## Decision requested

Approve simplification of the published skill inventory against current Designs, with `implement` and `code-review` as first-slice candidates and the compatibility bounds above. Submit this direction to independent Proposal Review, then reconcile affected Designs and prepare reviewed delivery allocation. Proposal approval does not authorize implementation, publication or changes to existing behavioral obligations.
