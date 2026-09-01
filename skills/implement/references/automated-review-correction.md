# Automated review and correction

Load this procedure only after `SKILL.md` establishes valid `IP2-planned-armed` authority.
The `implement` skill package remains the policy owner; this reference owns only workflow-managed automated review and bounded correction procedure.

## Load conditions

Armed implementation automation is valid only inside a current planned workflow-managed milestone.

Require:

- valid `planned_milestone_context` for the same change and milestone;
- current durable workflow authorization;
- the current automated review or correction mode;
- matching, non-stale change, plan, and milestone identity.

Do not infer authorization from conversational wording, prior runs, or a stale receipt.
Do not load this reference for `IP0-isolated` or `IP1-planned`.

## Armed authority

Implementation authority may execute the current approved milestone and reviewer-declared bounded corrections.
It does not authorize `verify`, `pr`, publication, release, deployment, credentials, or external mutation.

Keep milestone state and handoff procedure owned by `planned-milestone-implementation.md`.
This reference may cite that procedure but must not redefine it.

## Independent review packet

When handing workflow-managed implementation work to automated `code-review`, hand off to the independent adversarial review gate.
Provide tracked artifacts, the actual diff, governing contracts, and neutral routing metadata.

The orchestrator creates the neutral invocation manifest before review.
Begin blind-first and record an independent risk map before releasing validation summaries or implementation evidence.

Do not provide these forbidden initial-context items:

- author hidden reasoning;
- author chain-of-thought;
- author self-assessment;
- claims that the change is correct;
- desired review outcome;
- autoprogression round budget;
- message that approval is needed to continue;
- auto-fix budget;
- auto-fix eligibility;
- implementation-stage safety narrative;
- prior reviewer conclusion;
- prior finding content;
- validation-result summaries;
- evidence menu.

Do not expose auto-fix classification to review discovery; findings and verdict are recorded before fixability is classified.

## Requirement-fidelity routing

When handing workflow-managed implementation work to automated `code-review`, include neutral routing metadata for requirement-fidelity applicability.
Do not present implementation and validator agreement as sufficient proof of spec fidelity.
When both contracts apply, downstream continuation requires both the independent-review receipt and the requirement-fidelity receipt.

Requirement-fidelity review begins from the relevant spec clause, decomposes its properties, and checks every required surface before validation agreement is considered.

## Correction and rereview

Record the first-pass review before any correction.
Only reviewer-declared `mechanical` or `declared-safe` findings may enter automatic correction.

A declared-safe recipe must name inputs, outputs, allowed and forbidden paths, acceptance criteria, and required commands without requiring an owner decision.
Do not infer fix safety from size or apparent obviousness.

Each correction remains on the same milestone, changes only declared paths, reruns named proof, records before/after finding sets, and returns to independent rereview.
Pause when a finding is unclassified, requires substantive governing-artifact changes, touches forbidden paths, introduces a new finding class, fails to shrink the unresolved set, or exceeds the authorized correction bound.

## Promotion and pause

Clean milestone promotion requires the normalized review outcome, independence manifest, phase receipts, clean sufficiency receipt, applicable fidelity receipt, risk-tier gates, and no unresolved findings.

Before Phase C can enter `verify`, require final holistic code-review evidence for the complete cross-milestone diff.

Pause on missing or stale identity, missing promotion evidence, blocked or inconclusive review, owner decisions, non-shrinking correction, validation failure, user pause/cancel, or any request to cross the PR boundary.
Never change the reviewer's native verdict to continue automation.
