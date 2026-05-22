# Learn Session: Change Metadata Reading Scope After Compaction

## Frame

- Date: 2026-05-22
- Status: session-recorded; routing pending contributor confirmation for any authoritative follow-up
- Trigger: maintainer explicitly invoked `learn` after observing that the completed Compact Change Validation Metadata work did not stop agents from reading lots of unnecessary `change.yaml` information.
- Trigger type: explicit maintainer observation after completed proposal/implementation.
- Scope: root cause and best practices for reducing unnecessary `change.yaml` reads after compact metadata support.
- Session path: `docs/learn/sessions/2026-05-22-change-yaml-reading-scope-after-compaction.md`

## Evidence Reviewed

- `docs/proposals/2026-05-21-compact-change-validation-metadata.md`
  - The proposal targets verbose durable validation evidence and says the goal is cheaper common reads while preserving reconstructable validation detail.
  - It explicitly preserves durable audit value and avoids weakening validation evidence.
- `docs/plans/2026-05-21-compact-change-validation-metadata.md`
  - The plan implements schema/validator behavior in M1-M3 and records that final verification passed.
  - The completed change still leaves current change metadata as a long evidence record; `docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml` is 433 lines.
- `docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml`
  - The file contains compacted structured metadata but still holds lifecycle, review, and validation chronology across many workflow stages.
- `specs/compact-change-validation-metadata.md`
  - The spec defines compact metadata and requires ordinary review to remain possible from `change.yaml` alone.
- `specs/compact-change-validation-metadata.test.md`
  - `TCVM-023` checks that an ordinary reviewer can inspect compact `change.yaml` alone for bundles, reconstructed commands, stage results, counts, blockers, and failure details.
- `docs/workflows.md`
  - Efficient evidence collection already says to use bounded extraction, targeted headings, stable IDs, line ranges, counts, and full-file reads only when bounded evidence is insufficient.
  - The workflow guide also says change metadata is scoped evidence and does not own the active plan's current next stage.
- Prior learn topic: `docs/learn/topics/evidence-preserving-compaction.md`
  - The existing lesson says to compress the safe surface while pinning the preservation mechanism.

## Exclusions

- This session does not change the compact metadata spec, validator, selector, workflow docs, or skill behavior.
- This session does not claim any PR, verification, CI, or lifecycle readiness.
- This session does not evaluate the correctness of the completed compact metadata implementation beyond the evidence needed for this observation.

## Prior Learnings Reviewed

- `docs/learn/topics/evidence-preserving-compaction.md` already captures that compaction must preserve evidence and behavior.
- This session adds a narrower follow-on observation: even evidence-preserving compaction does not automatically define how agents should query or bound reads of the compact artifact.

## Observations

### O1: The compact metadata change solved storage shape, not reader behavior

The compact metadata proposal and implementation make validation evidence more structured and reconstructable, but they do not by themselves force agents to read only the relevant slice of `change.yaml`.

Evidence:

- The proposal focuses on schema shape, validation bundles, path variables, structured results, summaries, and reconstructability.
- The workflow guide already warns agents to use bounded evidence, but `change.yaml` remains a default evidence surface for many stages.
- The completed compact metadata `change.yaml` is still 433 lines because it remains a durable change-local evidence ledger.

Root reason:

```text
Compaction changed the artifact representation, but the consumer access pattern
still treats the whole artifact as the evidence unit.
```

### O2: `change.yaml` is doing too many first-read jobs unless the stage asks a narrower question

`change.yaml` currently acts as path index, requirement/test map, review summary, validation ledger, and sometimes state-orientation input. For many stage questions, only one of those slices is needed.

Examples:

- To find owning artifacts, read `artifacts` and `change_id`.
- To confirm review closeout, read `review` and then `review-resolution.md` or `review-log.md`.
- To confirm final validation, read `validation_summary` or the latest relevant validation event, not every historical event.
- To answer current workflow state, prefer the active plan `Current Handoff Summary`, not `change.yaml`.

Root reason:

```text
The repository has a compact data model, but it lacks a first-class read model
or query contract for common stage questions.
```

### O3: The existing durable lesson is necessary but incomplete for this failure mode

`evidence-preserving-compaction` correctly says to preserve evidence while compacting noisy surfaces. The new failure mode is downstream: once evidence is preserved, agents still need a scoped access rule or helper so they do not repeatedly load preserved detail when only an index answer is needed.

Root reason:

```text
Preservation was pinned, but read-path selection was left to agent judgment.
```

## Classification Decisions

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | observation | observation | candidate process-follow-up | Maintainer observation; evidence from proposal/plan/current metadata | This is a real observed gap, but the existing compactness lesson already covers preservation. The new behavior change needs an owning artifact before it becomes policy. |
| O2 | process-follow-up | candidate process-follow-up | possible proposal/spec or workflow/skill update | Confirmation pending | A read model or query helper would change workflow/skill behavior, so learn should not route it unilaterally. |
| O3 | durable-lesson | candidate durable-lesson | possible topic update after confirmation | Confirmation pending | The pattern may be reusable, but it should not be added to topic guidance until contributor confirms the wording and route. |

Contributor confirmation status: pending for routing. The maintainer explicitly asked for root cause and best practices, but did not explicitly authorize updating topic guidance or starting a new proposal/spec change.

## Best Practices

1. Treat `change.yaml` as a metadata catalog, not the default transcript.

Start with the stage-owned question, then read the smallest relevant slice. Do not open the whole file just because it is in the baseline artifact pack.

2. Use the right state owner first.

- Current live workflow state: active plan `Current Handoff Summary`.
- Durable rationale: `explain-change.md`.
- Review finding status: `review-log.md` and `review-resolution.md`.
- Validation command/result inventory: `change.yaml`.
- Forensic detail: validation events and transcript references.

3. Add or use a query/read model for common questions.

Useful future commands or helper modes would answer questions such as:

- `metadata summary`: artifacts, status, review state, latest validation state;
- `metadata validation --latest`: final validation commands and results only;
- `metadata validation --stage <stage>`: one stage's bundles/events;
- `metadata artifacts`: canonical artifact paths only.

4. Keep common-read fields physically early and bounded.

For compact `schema_version: 2`, the first-read material should be enough to answer:

```text
What change is this?
Which artifacts govern it?
What is the review state?
What is the latest validation state?
Are there blockers?
Where is the detail if I need it?
```

Historical validation events remain recoverable, but they should not be the first evidence an agent reads unless the stage is validating event reconstruction.

5. Make stage skills name exact fields or views.

Instead of "read `change.yaml`", stage guidance should say which slice to read for its claim. For example:

- `verify`: read artifacts, review status, validation summary/latest events, then expand only for missing or contradictory evidence.
- `pr`: read artifacts, review counts, final validation summary, and explain-change; do not read every historical validation event unless drafting reviewer notes requires it.
- `code-review`: read changed files, review-resolution if relevant, and validation evidence for the reviewed milestone, not all prior stage events.

6. Preserve detail, but make expansion explicit.

The compact metadata proposal was right to keep reconstruction and auditability. The missing practice is an expansion trigger: read full validation events only when checking exact command reconstruction, failure/blocker history, event-derived summary consistency, or disputed validation evidence.

## Routing Results

- Observation routing: recorded in this session.
- Durable topic routing: not performed; confirmation pending.
- Artifact update routing: not performed.
- Candidate follow-up: create a proposal or spec amendment for a `change.yaml` read model / metadata query helper and stage-skill field-specific reading guidance.

## No-Policy Rationale

This session identifies a likely process and artifact-design gap, but learn is not the authoritative owner of workflow or skill behavior. A durable behavior change should be routed through a proposal/spec/workflow/skill update after contributor confirmation.

