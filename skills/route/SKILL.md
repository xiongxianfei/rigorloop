---
name: route
description: Resume and coordinate authorized engineering work from current CLI context. Select the responsible skill, preserve authority limits and continue through the applicable requirement-first workflow.
---

# Route

Use the selected Change's current handoff to identify goal, authority, governing basis, work, open issues, evidence, review standing and next action. Resolve an ambiguous Change selection rather than scanning private storage or guessing from filenames. Missing or contradictory support remains a gap.

The standard dependency chain is:

```text
RR → requirement-analysis → requirement-review
   → system-design ↔ architecture-design → design-review
   → plan → delivery-review → implement
   → whole-change code-review → verify → authorized PR
```

Route chooses work; the specialist owns its definitions or judgments. Requirement changes return to requirement-analysis, logical behavior to system-design, allocation/Interface/AR defects to architecture-design, sequencing/proof allocation to plan, and implementation defects to implement or bugfix. Explore is optional when the option space is materially unclear. Research is optional when a material decision depends on an uncertain fact. Use both when research questions could materially change the option comparison, and neither when direction and decision-relevant facts are sufficiently clear. An explicit invocation produces the specialist artifact. An incidental fact check does not create a discovery artifact. The owning stage must explicitly adopt any consequential conclusion; discovery does not approve work and does not advance lifecycle state.

Within the user's authorization, continue across milestones whose work and required checks are complete. Milestones require no reviewer assignment, review record or clean-review label. Known in-scope defects, failed required checks, unresolved dependencies and exhausted authority still block affected work. An isolated request ends at its authorized slice.

When the complete delivered scope is ready, request one independent whole-change Code Review gate. Interim advice is optional and cannot approve the gate. Corrections and proportionate reassessment remain inside that same gate. Final Verify is separate. A save, route decision, installation or schema pass grants no engineering approval or external permission.

Update the handoff at consequential changes and before transfer, not after every action. Preserve unresolved obligations and actual judgment ownership. After response loss, inspect current state before reconciling another request; do not replay stale intent. Continue to PR when already authorized and all required work is ready; do not invent another permission checkpoint.

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
