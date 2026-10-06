---
name: verify
description: Assess whether current engineering work, applicable reviews and actual evidence justify a scoped result or final completion. Keep Verify separate from authoring and whole-change Code Review.
---

# Verify

State whether the requested assessment is scoped or final. Read accepted IR/SRs and applicable ARs, reviewed System/Architecture Design, delivery intent, actual implementation/work, open issues and selected current evidence. For final success, require adequate applicable whole-change Code Review and current support for the other mandatory bases. A review for every milestone is not required.

Run the applicable repository checks and any required direct validation; report commands actually executed, results and limitations. Reuse evidence only where its scope and applicability justify it. Trace evidence through implementation/work to governing SR/AR and accepted IR/request basis. Saving records or passing schemas does not satisfy engineering obligations.

Keep correction ownership: implementation defects return to implement, requirement defects to requirement-analysis, and design defects to their responsible designer. Independently reassess materially changed subjects, then reverify. Verify cannot fix code and silently approve that correction. An evidence-collection retry alone does not require another Code Review; contradictory evidence requires assessing its effect on earlier reliance.

Record an explicit Verification assessment, including support and limitations. Current support means recorded dependencies are reconciled; it does not establish unreported repository stability. Renewing a Review does not renew a stale Verification automatically. Failed and inconclusive results remain recordable without a success claim.

Only after successful final assessment, use change complete to retain the compact delivered outcome, actual acceptance basis, limitations and selected useful attachments. Preserve meaningful deferred follow-up; it cannot waive mandatory acceptance. Completion is historical and stops tracking later repository applicability. A later regression is linked new work; an error in the original account gets an explicit completion note.

Continue to the pr skill when external handoff is authorized. Commit, PR, merge and release remain separate actions; a completion save does not authorize them.

## Recording boundary

For Change-managed work, read the packaged operational interface reference before relying on or updating current state. Use supported CLI tasks and the inspected opaque revision; skills do not use SQL or edit runtime storage. An isolated invocation keeps its requested scope. Installation alone does not adopt workflow policy.

## Resource map

- READ `references/operational-recording.md` when inspecting or recording Change-managed work.
- READ `references/targeted-recording-v2.schema.json` when constructing a recording request.
- READ `references/rigorloop-records-v4.schema.json` when checking the types used by that request.

- READ `references/boundary-first-method-v1.md` when the project applies its boundary first method v1 criteria to this invocation.

- READ `references/requirement-to-delivery-model.md` when the project applies its requirement to delivery model criteria to this invocation.

- READ `references/review-reliance.md` when the project applies its review reliance criteria to this invocation.

- READ `references/test-maintenance.md` when the project applies its test maintenance criteria to this invocation.

- READ `references/test-quality.md` when the project applies its test quality criteria to this invocation.

- READ `references/rem-methods-plan-and-assess-verification.md` when planning or interpreting verification against specified obligations.
- READ `references/rem-methods-validate-stakeholder-outcomes.md` when assessing intended-use outcomes separately from specified conformance.
- READ `references/rem-concepts-assurance.md` when reasoning about assurance in the selected scope.
- READ `references/rem-models-README.md` when reasoning about README in the selected scope.
- READ `references/rem-practices-verify-and-validate-slice.md` when needing an illustrative application of the canonical methods; examples do not establish execution.
- READ `references/rem-practices-engineer-change-WORKED-EXAMPLE.md` when needing an illustrative application of the canonical methods; examples do not establish execution.

## Expected output

Report the actual scoped outcome, governing basis, changed subjects or recorded judgment, material gaps and the next authorized action. Distinguish progress, review approval, final verification and external publication; claim only outcomes supported by this invocation.
