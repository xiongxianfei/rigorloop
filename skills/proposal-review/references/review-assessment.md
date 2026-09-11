# Review assessment application

This guidance applies the project's explicitly adopted Review and Closeout policy. The project's governing policy remains authoritative. Select the project contract before using this guidance; installing a skill does not adopt policy or migrate historical records. Historical identities, judgments and approvals retain their original meaning as archival evidence; this does not retain runtime support for retired stored formats.

## Establish the assessment

Identify kind, exact subjects, governing basis and claim limits. Keep Proposal, Design, Delivery, milestone Code Review, final whole-change Code Review and bounded advisory scopes distinct. Read the complete required subject and expand omitted context when it affects the judgment; do not load unrelated specialist methods.

For independent approval, identify actual contributors and concrete separation: the reviewer did not author the reviewed contribution. A fresh turn, role label, assumption reset, passing checks or author self-assessment is not independence. Missing provenance prevents reliance on independent approval. Retain supported findings.

Use the invoked skill's specialist criteria. Proposal approval supports authorized Design only; Design approval supports authorized planning only; Delivery approval supports authorized implementation only. Milestone approval covers that slice; final Code Review supports Verify's separate assessment. Advisory conclusions neither settle a broader package nor initiate the governed lifecycle.

## Select one overall judgment

Apply the first matching condition to the required scope, retaining every supported material finding:

| Condition, in priority order | Judgment |
| --- | --- |
| Missing necessary authority or owner decision prevents an adequately scoped judgment or correction | `blocked`; name the decision and owner |
| Otherwise, missing or unreliable required evidence leaves a material part of the assessment unassessable | `inconclusive`; identify missing basis and retain bounded supported findings |
| Otherwise, an evidenced required correction has a defined outcome and safe resolution path | `changes-requested`; identify corrections and owners |
| Required scope is adequately assessed and criteria are satisfied without required corrections or unresolved necessary decisions | `approved`; optional advisory improvements may remain |

A retry defect plus an undecided necessary compatibility policy is blocked with the defect retained. A concrete defect in one inspected member plus another materially unassessable required member is inconclusive with that defect retained. An unrelated future decision does not block the current scope. Optional style suggestions do not defeat approval. Do not narrow scope after discovering missing evidence to manufacture approval. Specialist pass/concern/block dimensions and severity explain evidence; they do not override this overall rule or create new stored values.

## Record and return

Before downstream reliance, durably record the judgment, actual subjects, rationale and limitations through the selected contract. Distinguish judgment, recording success, applicability and authorized continuation. Failed recording blocks reliance on unrecorded approval; it does not erase supported findings. Structurally valid non-approval and correction records remain recordable; the CLI does not select the judgment.

For each material concern, keep its ID stable and maintain accurate reporter, subjects/location, evidence, required outcome and correction ownership. V3 findings have editable current fields; explain corrections through evidence, required outcome and resolution without adding origin, history or paragraph records. Existing IDs cannot be removed or renamed; withdraw a mistaken finding explicitly through resolution. V2 findings and change-level blockers retain their immutable origin and supporting judgment. Optional improvements are labeled advisory, not open required fixes. Use existing narrative fields for severity and specialist attribution where the contract has no dedicated field.

Send corrections to the owning author or implementation activity. Record the finding before review-driven edits; never edit and approve the same contribution. Corrected work is review-ready. The reporter assesses disposition with proof and rationale; later approval does not silently dispose concerns. Deferral needs authorized residual risk, accountable owner, tracked follow-up and satisfaction of mandatory acceptance conditions; it cannot waive final review. A reviewer cannot close Verify's blocker.

Record formal reviews even for isolated requests. Isolation controls continuation, not evidence. Return the result and responsible next action within existing authority; recording a judgment grants no permission for unrelated work or external actions.

## Contract-selected assessment explanation

For v3 Review, supply a nonempty summary and assessment_scope, at least one complete rationale string, and an explicit limitations array. Keep judgment, findings, actors and exact subjects in their authoritative fields; do not repeat their lists or status in explanation. Multiline reasons are allowed. Existing v2 reviews retain their required body; never infer or mechanically convert old approvals into named fields.

Use review.record for a complete assessment. Use review.set only to replace named explanation fields; omitted fields and findings stay unchanged. A save does not approve, restore applicability, provide independent review or authorize continuation. Correcting a typo does not automatically require implementation tests; a meaning-changing limitation requires the assessor to reconsider reliance and explicitly record applicability or reassessment. Changed subjects, judgment, actors or evidence basis require a complete assessment. Use a batch when related explicit corrections must publish together. Read complete review context before reliance: show --fields reports a selection, even when retrieval is complete.
