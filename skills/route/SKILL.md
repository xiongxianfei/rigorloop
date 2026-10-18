---
name: route
description: Resume authorized engineering work from current context; coordinate usable requirements/design, implementation, final independent review and verification.
---

# Route

Read the selected Change's goal, authority, requirement/design basis, work, issues, evidence and next action. Resolve an ambiguous target rather than scanning private storage. Missing or conflicting meaning is a gap; a missing intermediate approval is not.

```text
RR → requirement-analysis → system-design ↔ architecture-design
   → proportionate plan → implement → whole-change code-review → verify
   → authorized PR when requested
```

The responsible author selects usable requirement and design bases within existing authority. Work on logical behavior and architecture in one iterative loop. Requirement, integrated Design and Delivery Reviews are optional specialist assessments; invoke them when requested or useful for a material uncertainty. Do not introduce approval pauses or duplicate reports solely because the activity changes.

Return a defect to the owner of its meaning: obligations to requirement-analysis, behavior to system-design, responsibility/Interfaces/ARs to architecture-design, sequencing/proof allocation to plan, and implementation to implement or bugfix. Material unresolved decisions, missing authority, failed required checks and open findings still constrain dependent work. Continue authorized work when those dependencies are settled.

Explore is optional when the option space is materially unclear. Research is optional when a material decision depends on an uncertain fact. Use both when research questions could materially change the option comparison, and neither when direction and decision-relevant facts are sufficiently clear. An explicit invocation produces the specialist artifact; an incidental fact check does not create a discovery artifact. The owning stage must explicitly adopt consequential conclusions. Discovery does not approve work and does not advance lifecycle state.

After complete implementation, obtain one independent whole-change Code Review covering the current requirements, design, delivery intent, implementation and evidence. Corrections and proportionate reassessment stay within that gate; distinct final Verify follows. Optional advice cannot replace either. Preserve explicit formal-review dependencies and unresolved findings rather than treating an optional gate as permission to ignore contrary evidence.

Update records at meaningful transitions and handoffs, not after each action. Use the actual current revision; after response loss, inspect before retrying. Isolated requests remain scoped. Continue through PR only when already authorized; approval of engineering work grants no merge or release permission.

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
