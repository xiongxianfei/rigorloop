---
name: implement
description: Realize accepted requirements and reviewed design in authorized, testable milestones. Maintain current evidence and hand off the complete implementation for independent whole-change Code Review.
---

# Implement

Read the governing requirements/design, material decisions, delivery plan and verification allocation before changing implementation. Use concrete proof first when feasible; reproduce defects and test the affected behavior. Run existing relevant checks and address known in-scope defects before claiming implementation complete.

Keep changes bounded and complete across affected producers, consumers and generated resources. Preserve unrelated work. Discoveries that change obligations return to requirement-analysis; logical behavior to system-design; allocation or Interface design to architecture-design; delivery sequencing to plan. Do not hide a changed requirement in code or test expectations.

Complete milestones with their required checks and report actual progress. Continue remaining eligible implementation when already authorized; no milestone reviewer or clean-review record is required. Optional advisory reviews can expose defects, but they do not settle milestones or replace whole-change approval. A request for one isolated slice grants no wider continuation.

Maintain selected current evidence, actionable blockers, rationale and the next action at meaningful transitions. Comparable working evidence can be replaced; preserve unresolved obligations and support still relied upon. Do not record every command or preserve every test log.

When the complete delivered scope is ready, hand all relevant code, tests, configuration, migrations, generated resources, instructions and documentation to an independent whole-change reviewer. Implementation completion is a substantive claim about that scope, not review approval or final Verify. Own the corrections and relevant checks; return the revised candidate for proportionate reassessment within the same gate.

## Recording boundary

For Change-managed work, read the packaged operational interface reference before relying on or updating current state. Use supported CLI tasks and the inspected opaque revision; skills do not use SQL or edit runtime storage. An isolated invocation keeps its requested scope. Installation alone does not adopt workflow policy.

## Resource map

- READ `references/operational-recording.md` when inspecting or recording Change-managed work.
- READ `references/targeted-recording-v2.schema.json` when constructing a recording request.
- READ `references/rigorloop-records-v4.schema.json` when checking the types used by that request.

- READ `references/boundary-first-method-v1.md` when the project applies its boundary first method v1 criteria to this invocation.

- READ `references/review-reliance.md` when the project applies its review reliance criteria to this invocation.

- READ `references/test-maintenance.md` when the project applies its test maintenance criteria to this invocation.

- READ `references/test-quality.md` when the project applies its test quality criteria to this invocation.

## Expected output

Report the actual scoped outcome, governing basis, changed subjects or recorded judgment, material gaps and the next authorized action. Distinguish progress, review approval, final verification and external publication; claim only outcomes supported by this invocation.
