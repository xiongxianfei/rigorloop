# Learn Session: Isolated Review Material Finding Records

## Frame

- Date: 2026-05-06
- Status: session-recorded; retrospective review-record reconstruction completed
- Trigger: contributor asked why the material `proposal-review` finding for the vision-skill strategic-positioning proposal was not recorded under `docs/changes/`, then explicitly invoked `learn`.
- Trigger type: explicit maintainer request after contributor observation.
- Scope: review-record placement for direct or isolated formal lifecycle reviews that produce material findings and then drive proposal edits.
- Session path: `docs/learn/sessions/2026-05-06-isolated-review-material-finding-records.md`

## Evidence Reviewed

- `docs/learn/README.md`
- Prior learn session: `docs/learn/sessions/2026-05-05-review-record-placement.md`
- Current proposal under review: `docs/proposals/2026-05-06-optimize-vision-skill-strategic-positioning-quality.md`
- Current `proposal-review` skill guidance: `skills/proposal-review/SKILL.md`
- Current workflow summary: `docs/workflows.md`
- Current workflow spec: `specs/rigorloop-workflow.md`
- Current review-finding contract search results: `specs/review-finding-resolution-contract.md`
- Chat-local evidence from the current review: first `proposal-review` returned material finding `PR-1`; proposal was revised; second `proposal-review` approved.

## Exclusions

- No workflow, spec, skill, or validator behavior is changed by this session.
- A retrospective `docs/changes/<change-id>/` review record was created after contributor confirmation.
- No learn topic entry is created.
- No generated Codex runtime or adapter output is touched.

## Prior Learnings Reviewed

- `docs/learn/README.md` states session records are primary learn outputs and topic files are curated guidance, not policy.
- `docs/learn/sessions/2026-05-05-review-record-placement.md` observed that review-record placement confusion could recur and said that if it recurs, the repository should evaluate focused workflow-doc clarification or a proposal for review-result discoverability.

## Observations

### O1: The earlier review-record placement confusion recurred

The prior session recorded a single contributor observation about why some upstream review results were not under `docs/changes/`. It did not create a durable lesson because one event was insufficient, but it explicitly named a recurrence follow-up.

The same class of question recurred here after a `proposal-review` produced material finding `PR-1`, the proposal was edited to resolve it, and a second `proposal-review` approved the result. The contributor asked why the first-pass material review finding was not recorded in `docs/changes/`.

Evidence:

- `docs/learn/sessions/2026-05-05-review-record-placement.md` O4 and Follow-Ups.
- Current chat-local review outcome: `PR-1` was a material proposal-review finding about ambiguous lowercase `vision.md` retirement scope.
- Current proposal now includes the resolution: lowercase `vision.md` handling is retired across active user-facing guidance and repository validation.

### O2: Current guidance makes direct review isolation easy to over-apply

The `proposal-review` skill says direct or review-only `proposal-review` requests remain isolated by default. That rule correctly prevents automatic downstream handoff. But the same skill also says material findings are detailed-record triggers for workflow-managed formal lifecycle reviews, and the workflow spec states that detailed review files are required when a formal lifecycle review produces material findings.

The resulting interpretation gap is practical: an agent can treat "isolated" as "no durable record," even when the review produces a material finding that drives artifact edits. That weakens traceability for the exact cases the formal-review-recording rules were designed to preserve.

Evidence:

- `skills/proposal-review/SKILL.md` says direct or review-only `proposal-review` requests remain isolated by default.
- `skills/proposal-review/SKILL.md` lists material findings as detailed-review triggers for workflow-managed formal lifecycle reviews.
- `docs/workflows.md` says detailed formal review files are created for material findings and direct `proposal-review` stays isolated by default unless the user asks to carry the change through completion.
- `specs/rigorloop-workflow.md` says a detailed review file must be created for a formal lifecycle review when the review produces material findings.

### O3: The missing record is not just a user-memory problem

The first-pass material finding was preserved in chat only. The proposal contains the resulting scope decision, but not the first-pass finding, required outcome, or safe resolution path as a durable formal-review record. That makes it harder for later reviewers to reconstruct why the proposal changed between review rounds.

Evidence:

- The proposal decision log now records the final lowercase-path scope decision.
- No change-local review record exists yet for this proposal finding.
- The first-pass `PR-1` evidence, required outcome, and safe resolution path exist only in chat output.

## Classification Decisions

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
|---|---|---|---|---|---|
| O1 | process-follow-up | pending | Candidate proposal or workflow-spec clarification | Not yet confirmed for routing | The recurrence satisfies the prior session's follow-up condition, but routing a workflow behavior change still needs contributor confirmation. |
| O2 | process-follow-up | pending | Candidate proposal or artifact update to clarify isolated-review material finding persistence | Not yet confirmed for routing | The rules create an interpretation gap between isolated stage behavior and material-finding record triggers. This likely needs an action-owning workflow artifact, not a topic-only lesson. |
| O3 | observation | process-follow-up | Retrospective review-record reconstruction completed at `docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/` | Contributor requested retrospective record creation | The current proposal contains the final decision, but the first-pass material finding was not durably discoverable until the reconstructed review record was created. |

Contributor confirmation status: confirmed for O3 retrospective record reconstruction. O1 and O2 remain unconfirmed for broader workflow or policy routing.

## Routing Results

- Observation routing: recorded in this session.
- Durable lesson routing: not created.
- Artifact update routing: retrospective review record created at `docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/`.
- Decision routing: not created.
- Process follow-up routing: O3 completed; O1 and O2 remain pending contributor confirmation for any broader workflow clarification.

## No-Durable-Lesson Rationale

No topic-level durable lesson was created. The evidence points to a workflow/process gap that belongs in action-owning artifacts if adopted. A learn topic would be the wrong source of truth for review-record policy.

## Follow-Ups

- Pending contributor confirmation: open a proposal or targeted workflow-spec clarification for how direct or isolated formal reviews should preserve material findings when those findings drive tracked artifact edits.
- Completed: reconstructed the current `PR-1` finding under `docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/` so this proposal's review history is durable before downstream stages.
