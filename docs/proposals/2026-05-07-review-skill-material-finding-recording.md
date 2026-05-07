# Review Skill Material Finding Recording

## Status

accepted

## Problem

The current review guidance makes it too easy to confuse two separate workflow concerns:

- whether a direct or review-only request automatically continues into downstream work;
- whether a material review finding is preserved as durable evidence.

The first concern is isolation. The second concern is recording. They should not share the same switch.

The gap recurred in `docs/learn/sessions/2026-05-06-isolated-review-material-finding-records.md`: an isolated `proposal-review` produced a material finding, the finding drove a proposal edit, and the first-pass finding was not recorded under `docs/changes/` until the contributor asked for retrospective reconstruction.

This is not only a `proposal-review` problem. The same wording pattern appears across `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, and `code-review`: direct or review-only invocations stay isolated, while detailed-record language is scoped around workflow-managed formal lifecycle reviews. That leaves agents room to over-apply "isolated" as "no durable record" even when the review finding changes tracked artifacts.

## Goals

- Decouple isolated review handoff behavior from material-finding recording behavior.
- Make the material finding, not the workflow context, the durable-record trigger.
- Apply the clarification consistently across all formal review skills: `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, and `code-review`.
- Preserve the current rule that direct or review-only requests do not automatically continue downstream.
- Preserve lightweight artifact-local settlement for clean reviews with no material findings.
- Define a minimal, proportional record shape for material review cases.
- Make the resolution step enforce the record: a tracked artifact revision in response to a material finding is incomplete until that finding is durably recorded.
- Make every new `review-resolution.md` human-readable and useful, not merely structurally valid.

## Non-goals

- Do not make isolated reviews auto-continue into spec, implementation, review-resolution, verify, explain-change, or PR.
- Do not require detailed review files for clean reviews with no material findings when no detailed-record trigger applies.
- Do not create a dedicated `pr-review` stage.
- Do not copy every maintainer PR comment into `docs/changes/`.
- Do not replace artifact-local proposal, spec, architecture, plan, or code-review status.
- Do not add semantic automation that decides whether a review finding is correct.
- Do not add semantic validator flagging for tracked artifact edits that reference unresolved review findings in the first slice.
- Do not introduce a generation step for sharing the review skill subsection.
- Do not treat the initial review-record root as sufficient final handoff for non-trivial work.
- Do not require `review-resolution.md` for no-material detailed records unless another approved review-resolution trigger applies.
- Do not make `review-resolution.md` a transcript of every review comment.
- Do not sacrifice existing validator-readable fields for prettier Markdown.
- Do not migrate historical review records except when a touched or relied-on change needs reconstruction.

## Vision fit

fits the current vision

This proposal strengthens RigorLoop's core promise that reviewers can reconstruct change purpose, requirements, validation evidence, and review concerns from durable tracked artifacts without relying on chat history.

## Context

`CONSTITUTION.md` already says each material review finding must include evidence, required outcome, and a safe resolution path or `needs-decision` rationale before it drives fixes. It also says workflow-managed formal reviews that produce material findings, reconstructed evidence, closeout evidence citations, or explicit durable-record requests must preserve detailed review records before review-driven fixes or downstream routing proceed.

`specs/rigorloop-workflow.md` already defines the formal lifecycle review stages as `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, and `code-review`. It also says material review findings must be recorded before review-driven fixes begin, and reconstructed records must disclose after-fix timing when fixes started before a durable record existed.

`docs/workflows.md` already describes stage-neutral review records under `docs/changes/<change-id>/reviews/`, but also says direct review requests stay isolated by default. That is correct for handoff behavior, but it needs clearer wording so isolation does not suppress material-finding recording.

The 2026-05-06 learn session confirmed recurrence after an earlier review-record placement concern on 2026-05-05. The current proposal treats that follow-up condition as met and frames the change as a workflow clarification rather than a new artifact model.

## Options considered

### Option 0: Keep the current guidance unchanged

This preserves stability, but it leaves the observed ambiguity intact. Agents can continue to treat isolated reviews as exempt from durable recording even when a material finding changes tracked artifacts.

### Option 1: Clarify only `proposal-review`

This addresses the incident that triggered the learn session, but it leaves the same interpretation gap in `spec-review`, `architecture-review`, `plan-review`, and `code-review`. The next recurrence would likely happen at another review stage.

### Option 2: Require detailed records for every isolated review

This is simple to state, but too heavy. Clean isolated reviews would create low-value `docs/changes/` files, and the workflow would lose the current proportional distinction between material findings and routine no-finding settlement.

### Option 3: Make every material finding the trigger across all review skills

This is the recommended option. Isolation continues to mean no automatic downstream handoff. Recording is triggered by the review result itself: if a formal lifecycle review produces a material finding, a durable change-local review record is required.

### Option 4: Add validator-only enforcement without changing skills

Validation can catch some missing records after the fact, but the main failure is guidance interpretation at review and resolution time. Skill and workflow wording need to prevent the omission before validators become the backstop.

## Recommended direction

Adopt Option 3.

Update the workflow contract and the review skill family to state the separation explicitly:

- Isolation controls handoff only. A direct or review-only review does not automatically continue downstream.
- Recording is controlled by the review finding. Every material finding requires a durable change-local review record, even when the review request was isolated.
- If review-driven edits already began before the durable record exists, the record is reconstructed and must disclose source, timing, available evidence, stable Finding IDs, and known fidelity loss.
- The revision also remains incomplete until the finding is durably recorded. This is the fallback gate, not the primary timing rule.

The durable record should stay proportional. For a review that produces a material finding, the minimum change-local record is the initial review-record root:

```text
docs/changes/<change-id>/
|-- change.yaml
|-- review-log.md
|-- review-resolution.md
`-- reviews/
    `-- <stage>-r<n>.md
```

The review file records the finding, evidence, required outcome, safe resolution path or `needs-decision` rationale, review status, source review context, and whether it is reconstructed. `review-resolution.md` records the final disposition, action, rationale, follow-up when applicable, and validation evidence. `review-log.md` makes the review event discoverable.

The initial review-record root preserves the review event and dispositions before review-driven edits begin, or during repair when the record is reconstructed after edits already began. It is not final handoff completion. Final handoff for non-trivial work still requires the baseline non-trivial change pack, including durable Markdown reasoning such as `docs/changes/<change-id>/explain-change.md` or another approved durable reasoning surface.

If no material findings exist but another detailed-record trigger applies, the initial root is lighter:

```text
docs/changes/<change-id>/
|-- change.yaml
|-- review-log.md
`-- reviews/
    `-- <stage>-r<n>.md
```

`review-resolution.md` is required when material findings exist or another approved review-resolution trigger exists. This preserves the existing boundary: `reviews/` requires `review-log.md`; material findings require `review-resolution.md`; no-material detailed reviews do not require an empty `review-resolution.md`.

Clean isolated reviews with no material findings remain lightweight. They may settle in the reviewed artifact or final output when no detailed-record trigger applies.

When `review-resolution.md` is created, it should be scan-first for humans while staying parseable for validators. The default structure should be:

```text
summary first
resolution overview table
common resolution metadata when multiple findings share owner, stage, or validation evidence
one compact detail section per finding
shared validation evidence
closeout checklist
```

Each finding detail still carries validator-readable field labels such as `Finding ID:`, `Disposition:`, `Owner:`, `Owning stage:`, `Chosen action:`, `Rationale:`, `Validation target:`, and `Validation evidence:`. Common metadata can be recorded once for human readability, but each accepted finding still needs enough parseable closeout evidence to satisfy structure and closeout validation.

The readability invariant is: a reader should understand review closeout status in 30 seconds and be able to audit any individual finding in 2 minutes.

The review skills should share the following subsection verbatim from `templates/shared/review-isolation-and-recording.md`. Stage-specific additions may appear above or below this shared block, but not inside it.

```markdown
## Isolation and Recording

Isolation governs handoff. Recording follows the finding. These are
independent.

A direct or review-only review request remains isolated by default: it
does not automatically continue into downstream workflow stages.
Isolation does not suppress recording.

A material finding requires
a durable change-local review record under
`docs/changes/<change-id>/reviews/`.
This applies regardless of whether the review was workflow-managed or
isolated.

If review-driven edits already began before the durable record exists,
the record is reconstructed and must disclose source, timing, available
evidence, stable Finding IDs, and known fidelity loss.

A tracked artifact is any version-controlled repository file whose
change will be committed or reviewed as part of the work. This includes
lifecycle artifacts, governance files, workflow summaries, skills,
specs, schemas, scripts, generated outputs, README content, and
change-local artifacts. Edits to ephemeral chat output, local scratch
files, or unversioned drafts are not tracked artifact edits.

The recording obligation is also a resolution-step gate. A revision
made in response to a material finding is incomplete until the finding
is durably recorded.

Materiality is governed by `CONSTITUTION.md` and is not redefined here.
A material finding requires evidence, required outcome, and a safe
resolution path or `needs-decision` rationale before it drives fixes.

Operational shortcut: if a finding changes or blocks a tracked artifact
edit, changes scope, changes requirements, changes architecture,
changes sequencing, changes validation, creates follow-up work, or
requires disposition, treat it as material unless the reviewer
explicitly records a non-material rationale.

Reconstructed records are governed by `specs/rigorloop-workflow.md`.

Clean reviews with no material findings remain lightweight and may
settle in the reviewed artifact when no detailed-record trigger
applies.

For an isolated review with material findings, final review output names
the isolated handoff status, material Finding IDs, required durable
review record path or reconstruction requirement, confirms
`review-resolution.md` is required, and states that downstream handoff
remains stopped unless explicitly requested.
```

The canonical source for byte-equality assertions is `templates/shared/review-isolation-and-recording.md`. The block should be copied manually into `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, and `code-review` without a generation step. Tests compare each copied skill block against the canonical source. `code-review` adopts the shared isolation-versus-recording rule without an additive code-review-specific layer for this concern.

## Expected behavior changes

- Direct `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, and `code-review` requests remain isolated by default.
- An isolated review with no material findings does not require a detailed review file solely because it happened.
- A material finding from any formal review stage requires a durable change-local review record.
- Review-driven artifact revisions must either create/update the required record before edits begin or explicitly state why the finding is not material and does not require disposition.
- If review-driven fixes already began before the durable record exists, the record is labeled reconstructed and preserves original review source, available evidence, timing disclosure, stable Finding IDs, and known fidelity loss.
- Review skills use consistent language for detailed-record triggers rather than stage-specific variants.
- The isolation-versus-recording guidance appears as an identical shared subsection in all five formal review skills.
- The shared subsection has a canonical source at `templates/shared/review-isolation-and-recording.md`.
- The shared subsection includes a practical materiality shortcut without replacing the `CONSTITUTION.md` authority.
- Stage-specific review guidance appears only above or below the shared block.
- Final review output for isolated material cases names the isolated handoff status, Finding IDs, required record or reconstruction path, confirms `review-resolution.md` is required, and states that no downstream handoff continues automatically.
- The proposal preserves the existing boundary between initial review-record roots and final non-trivial change packs.
- The proposal preserves the existing boundary that no-material detailed records do not need an empty `review-resolution.md`.
- New `review-resolution.md` files use a human-readable, scan-first structure with summary, overview table, shared metadata, compact finding details, shared validation evidence, and closeout checklist.
- Review-resolution guidance preserves validator-readable per-finding fields while avoiding repeated long validation prose when findings share the same evidence.

## Architecture impact

This is a workflow-governance and skill-contract change. It does not require a runtime service, new storage backend, or new review stage.

Expected touched surfaces:

- `specs/rigorloop-workflow.md` for the authoritative isolation-versus-recording rule.
- `docs/workflows.md` for concise contributor-facing operational guidance.
- `CONSTITUTION.md` if its current wording needs the same explicit decoupling.
- `AGENTS.md` if the concise review-record summary needs alignment.
- `skills/proposal-review/SKILL.md`
- `skills/spec-review/SKILL.md`
- `skills/architecture-review/SKILL.md`
- `skills/plan-review/SKILL.md`
- `skills/code-review/SKILL.md`
- `templates/shared/review-isolation-and-recording.md`
- a reusable `review-resolution.md` template or shared guidance for scan-first review-resolution records
- generated `.codex/skills/` output after canonical skill changes.
- generated public adapter output under `dist/adapters/` after canonical skill changes.
- static skill validation tests for byte-equality and placement of the shared subsection.
- existing structural review-artifact validation tests, without semantic edit-reference flagging in the first slice.

## Testing and verification strategy

Use static assertions and existing validation before adding semantic automation.

Candidate coverage:

- Static assertions that every formal review skill contains the exact shared `## Isolation and Recording` subsection.
- Byte-equality assertion from the `## Isolation and Recording` heading up to, but not including, the next `##` heading against `templates/shared/review-isolation-and-recording.md`.
- Placement assertion that stage-specific content does not appear inside the shared block.
- Static assertion that the shared block has exactly one canonical source and that all five review skills match it byte-for-byte.
- Static assertions that every formal review skill says isolation controls handoff only and does not suppress material-finding recording.
- Static assertions that every formal review skill states material findings require evidence, required outcome, and safe resolution path or `needs-decision` rationale before they drive fixes.
- Static assertions that every formal review skill names the same detailed-record triggers, including isolated material findings.
- Static assertions that clean no-material reviews may settle artifact-locally when no detailed-record trigger applies.
- Static or fixture coverage that new `review-resolution.md` guidance uses a scan-first structure with summary, overview table, finding details, shared validation evidence, and closeout checklist.
- Validator regression coverage that the scan-first `review-resolution.md` format remains machine-readable through plain per-finding field labels.
- Regression coverage for reconstructed records when fixes started before a durable review record existed.
- Existing review artifact validation for `review-log.md`, `review-resolution.md`, detailed review files, finding IDs, dispositions, and closeout state.
- Generated skill and adapter drift checks after canonical skill changes.

Expected validation includes focused skill tests, review-artifact validation, skill validation, generated skill drift checks, adapter drift checks, artifact lifecycle validation, and selector-selected CI for changed paths.

Semantic validation that flags tracked artifact edits referencing unresolved review findings without matching records is deferred. Revisit it only if the problem recurs after the shared wording and structural assertions are in place.

## Rollout and rollback

Roll out as a normal workflow-governance change:

1. Update the workflow spec and test spec.
2. Update concise workflow and governance guidance.
3. Add `templates/shared/review-isolation-and-recording.md` as the canonical subsection source.
4. Add scan-first `review-resolution.md` guidance or template that stays validator-readable.
5. Copy the identical shared subsection into all formal review skills.
6. Add byte-equality and placement assertions for the shared subsection.
7. Regenerate derived Codex skills and adapter output through the existing repository generators.
8. Run selector-selected validation.

Rollback is straightforward: revert the spec, workflow docs, review skill wording, assertions, and regenerated outputs. Existing valid review records remain valid because the proposal clarifies when records are required; it does not introduce a new artifact location.

## Risks and mitigations

- Risk: contributors create full review packs for every isolated review. Mitigation: keep the clean no-material lightweight path explicit.
- Risk: agents still skip records by calling findings "minor." Mitigation: define materiality by effect and require durable records for every finding classified as material.
- Risk: the rule adds friction to small proposal/spec edits. Mitigation: clean no-material reviews and routine editorial feedback remain lightweight.
- Risk: wording drifts across review skills. Mitigation: use shared language and static assertions across the formal review skill family.
- Risk: the rule is enforced too late by validators. Mitigation: make the resolution step incomplete until the review finding is recorded.
- Risk: reconstructed records lose context. Mitigation: require reconstructed records to disclose source, timing, available evidence, stable IDs, and known fidelity loss.
- Risk: human-readable `review-resolution.md` formatting breaks structural validation. Mitigation: keep the existing parseable field labels in each finding detail and add regression coverage for the scan-first format.
- Risk: scan-first records hide finding-specific differences behind common metadata. Mitigation: use common metadata only for shared owner, stage, validation target, or validation evidence, and require unique finding details where action or rationale differs.

## Open questions

None.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
|---|---|---|---|
| 2026-05-07 | Recommend clarifying review recording across all formal review skills by decoupling isolation from recording. | The recurrence showed that isolated handoff behavior is being misread as an exemption from durable material-finding evidence. | Keep current guidance; update only `proposal-review`; require records for every isolated review. |
| 2026-05-07 | Use every material finding as the practical trigger. | This simpler rule removes ambiguity: every material finding is recorded, all material findings require change-local review files, and isolation stops handoff rather than recording. | Material-finding-plus-tracked-edit trigger; workflow-context-only trigger; validator-only enforcement. |
| 2026-05-07 | Treat the 2026-05-06 learn session as sufficient evidence to open this clarification proposal. | The prior learn follow-up condition recurred, and the contributor requested a proposal for all review skills. | Wait for another recurrence before proposing workflow clarification. |
| 2026-05-07 | Use one identical shared subsection across all five formal review skills, enforced by byte-equality assertions against `templates/shared/review-isolation-and-recording.md`. | Keeps the rule consistent without introducing a generation step or leaving byte-equality source selection ambiguous. | Stage-specific variants; generated shared content; byte-equality with no canonical source. |
| 2026-05-07 | Let stage-specific guidance appear only above or below the shared subsection. | Preserves a clean byte-equality target and prevents local edits from weakening the shared rule. | Allow stage-specific insertions inside the shared block. |
| 2026-05-07 | Have `code-review` adopt the shared rule without an additive code-review-specific layer for this concern. | The clarification is stage-neutral and should not grow a special code-review exception. | Add code-review-only recording language. |
| 2026-05-07 | Keep first-slice validator coverage structural-only and defer semantic edit-reference flagging. | Structural checks close the immediate wording drift and artifact-shape gap without adding brittle semantic inference. | Add semantic flagging in the first slice. |
| 2026-05-07 | Make record-before-edit the primary timing rule, with reconstructed records for late capture and incomplete-until-recorded as fallback. | Preserves first-pass review evidence and still handles already-started fixes honestly. | Record only before the edit is considered complete. |
| 2026-05-07 | Define tracked artifact as any version-controlled repository file changed for review or commit. | Avoids excluding governance, workflow, skill, script, schema, generated, README, or change-local files from material-finding recording. | Limit tracked artifacts to formal lifecycle files. |
| 2026-05-07 | Preserve the initial review-record root versus final non-trivial change-pack boundary. | Review event evidence should not replace final durable reasoning for non-trivial work. | Treat the initial review-record root as final handoff completion. |
| 2026-05-07 | Preserve the existing `review-resolution.md` boundary for material findings. | Avoids empty resolution files for no-material detailed records while keeping material findings dispositioned. | Require `review-resolution.md` for every detailed record. |
| 2026-05-07 | Add a final-output rule for isolated reviews with material findings. | Makes the stop condition and required change-local review record visible at the point of use. | Leave the behavior only in expected behavior text. |
| 2026-05-07 | Make new `review-resolution.md` records scan-first for humans while preserving validator-readable fields. | Review closeout files should answer closeout status, decisions, remaining work, and proof quickly without duplicating common metadata in every finding. | Keep dense repeated per-finding prose as the default; use pretty Markdown that breaks validators. |

## Next artifacts

- Proposal review.
- Feature spec update for the review material-finding recording clarification.
- Matching test-spec update with static assertions for all formal review skills.
- Execution plan if the accepted spec touches workflow docs, governance guidance, canonical skills, generated outputs, validators, and tests.

## Follow-on artifacts

- Proposal-review R1: revise with material findings `RSV1` through `RSV7`, all accepted and closed after proposal revision.
- Proposal-review R2: approved with no material findings.
- Proposal-review record: [review-log](../changes/2026-05-07-review-skill-material-finding-recording/review-log.md) and [review-resolution](../changes/2026-05-07-review-skill-material-finding-recording/review-resolution.md).
- Feature spec amendments: [Formal Review Recording](../../specs/formal-review-recording.md), [Review Finding Resolution Contract](../../specs/review-finding-resolution-contract.md), and [RigorLoop Workflow](../../specs/rigorloop-workflow.md).

## Readiness

Accepted after proposal-review. Downstream spec amendment readiness is tracked in the amended spec artifacts.
