---
name: code-review
description: Independently assess the complete delivered Change, or provide explicitly requested interim advice. One whole-change gate precedes final Verify; corrections are reassessed within that gate.
---

# Code Review

Identify scope first: formal whole-change review or optional advisory assessment. An advisory review reports findings and advice about inspected subjects, carries no formal judgment, and cannot advance the lifecycle or replace whole-change review. Serious findings still require owned action.

For the mandatory gate, assess the complete delivered scope against accepted IR/SRs, applicable ARs, reviewed System/Architecture Design and accepted delivery intent. Include relevant code, tests, configuration, migration/recovery behavior, generated outputs, skill instructions and documentation, including cross-milestone and cross-Module interactions. The scope is not merely the latest milestone.

Use a reviewer who did not author the implementation being approved. Record actual contributors and the basis for independence; role labels and hashes cannot establish it. Inspect the actual diff and sufficient context, evidence and failure behavior to judge the current result. Do not silently repair the reviewed subjects and approve your own repairs.

Record findings with scope, required outcome, accountable owner and relevant evidence. Route implementation defects to implement, wrong requirements to requirement-analysis, logical behavior to system-design, and allocation/Interface defects to architecture-design. Findings survive omission and a later clean submission until explicitly dispositioned.

After corrections, inspect changed subjects and affected interactions, determine what earlier coverage remains applicable, and maintain adequate whole-change coverage. Do not automatically reread every unchanged file or rerun unaffected tests. Broader or uncertain effects justify broader reassessment. Earlier approval retains its original meaning; current reliance requires an explicit supported disposition.

Use the code-purpose Review to record the actual assessment and applicability. One gate may contain several attempts. Do not settle milestone state or create a second gate for a single milestone. Hand applicable whole-change approval to distinct final Verify.

## Recording boundary

For Change-managed work, read the packaged operational interface reference before relying on or updating current state. Use supported CLI tasks and the inspected opaque revision; skills do not use SQL or edit runtime storage. An isolated invocation keeps its requested scope. Installation alone does not adopt workflow policy.

## Resource map

- READ `references/operational-recording.md` when inspecting or recording Change-managed work.
- READ `references/targeted-recording-v2.schema.json` when constructing a recording request.
- READ `references/rigorloop-records-v4.schema.json` when checking the types used by that request.

- READ `references/boundary-first-method-v1.md` when the project applies its boundary first method v1 criteria to this invocation.

- READ `references/requirement-to-delivery-model.md` when the project applies its requirement to delivery model criteria to this invocation.

- READ `references/review-assessment.md` when the project applies its review assessment criteria to this invocation.

- READ `references/review-reliance.md` when the project applies its review reliance criteria to this invocation.

- READ `references/test-maintenance.md` when the project applies its test maintenance criteria to this invocation.

- READ `references/test-quality.md` when the project applies its test quality criteria to this invocation.

## Expected output

Report the actual scoped outcome, governing basis, changed subjects or recorded judgment, material gaps and the next authorized action. Distinguish progress, review approval, final verification and external publication; claim only outcomes supported by this invocation.
