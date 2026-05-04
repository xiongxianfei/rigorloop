# Optimize Learn Skill

## Status

- accepted

## Problem

The `learn` skill is now correctly classified as periodic or explicitly invoked, but its final artifact model is still deferred. The current guidance says scheduled follow-ups and no-learn rationales use temporary contributor-visible or review-visible surfaces until a focused learn refactor defines the final model.

That temporary state leaves contributors without a durable answer to several practical questions:

- where raw periodic learn-session output belongs;
- where distilled, topic-specific learning should be found later;
- when a lesson should update an existing artifact instead of becoming another retrospective note;
- how action-producing lessons become trackable work;
- how to keep learn output useful without turning it into an unbounded pile of notes.

Without a clearer routing model, future learn sessions may either over-write policy into the wrong artifact, hide lessons in per-change files, or create retrospective documents that are hard to find when a contributor is working on a specific topic.

## Goals

- Define canonical learning surfaces for raw session output, distilled durable lessons, and actions taken from those lessons.
- Keep `learn` retrospective and non-authoritative for lifecycle bookkeeping.
- Preserve the current rule that `learn` is periodic or explicitly invoked, not a default final per-change stage.
- Make durable lessons traceable back to the session, change, incident, or review evidence that produced them.
- Route decisions, directions, improvements, and observations to the right artifact type.
- Define `learn` as a guided process for framing, observing, classifying, and routing evidence-bound observations.
- Keep topic-organized learning files curated and useful instead of append-only.
- Make lessons that require action produce trackable follow-ups or direct artifact updates.
- Start with the smallest structure that earns its place while leaving a clear path to topic organization.

## Non-goals

- Making `learn` mandatory for every change.
- Making `learn` the owner of `docs/plan.md`, plan-body lifecycle state, review-resolution closeout, verification, or PR readiness.
- Replacing proposals, specs, ADRs, architecture docs, workflow docs, or affected skill files with learning notes.
- Building an issue tracker, project-management layer, or automated lesson triage system.
- Requiring every observation from a learn session to become a durable rule.
- Producing lessons from isolated single events unless the evidence shows a reusable pattern or systemic gap. An explicit maintainer request can trigger a learn session, but it does not lower the evidence standard for capturing a durable lesson.
- Letting the skill make final classification decisions without contributor confirmation or adjustment.
- Bypassing downstream review for derivative ADRs, proposals, specs, or workflow changes.
- Manufacturing observations to justify a learn session.
- Pre-creating empty topic files or enforcing a fixed taxonomy before real lessons justify it.
- Adding session or topic templates before repeated usage reveals a stable shape worth codifying.
- Using `docs/roadmap.md` as the tracking surface for learn follow-ups.
- Reopening the workflow category model adopted by `docs/proposals/2026-05-01-workflow-refactor.md`.

## Vision fit

fits the current vision

This proposal supports the current vision by keeping AI-assisted change rationale and retrospective evidence visible in Git. It improves reviewability by separating raw retrospective output, curated guidance, and action records, while avoiding a broad project-management surface that the vision explicitly refuses.

## Context

`CONSTITUTION.md` says RigorLoop optimizes for reviewability, traceability, and trustworthy automation. It also says durable lessons should be captured through the periodic or explicitly invoked `learn` stage rather than left only in chat or PR comments.

`specs/rigorloop-workflow.md` now classifies `learn` as a periodic artifact. It says triggered `learn` closes through immediate capture, scheduled follow-up, or explicit no-learn rationale, and that the final learn artifact model is deferred to a focused follow-up.

`skills/learn/SKILL.md` currently sends lessons to the narrowest durable home. Its possible destinations include feature specs, test specs, architecture docs, ADRs, `AGENTS.md`, `CONSTITUTION.md`, `docs/workflows.md`, `docs/project-map.md`, completed plans, and `docs/retrospectives/YYYY-MM-DD-slug.md`. It also lists temporary follow-up and no-learn rationale surfaces before the learn refactor.

No `docs/learn/` or `docs/retrospectives/` directory exists in the repository today. That means this proposal can define the model without needing a large migration of existing learning records.

## Options considered

### Option 1: Keep the current temporary surfaces

Advantages:

- Requires no immediate workflow or skill changes.
- Avoids creating new directories.
- Lets individual contributors choose the most convenient surface for each situation.

Disadvantages:

- Keeps the final artifact model unresolved after the workflow refactor intentionally deferred it.
- Makes periodic learn sessions hard to discover as a historical thread.
- Allows durable guidance to scatter across change-local files, PR bodies, and governance artifacts without a consistent index.
- Does not distinguish raw observations from lessons that should guide future contributors.

### Option 2: Use one retrospective directory for all learn output

Advantages:

- Simple to explain.
- Creates one durable historical record for each learn session.
- Avoids deciding on topic organization or action-routing rules up front.

Disadvantages:

- Makes topic-specific discovery weak as the number of sessions grows.
- Mixes observations, durable guidance, and action records in one document type.
- Encourages future contributors to browse chronology when they need guidance on proposals, verification, CI, architecture, or another topic.
- Does not clearly say when a lesson should update an affected artifact or become an ADR.

### Option 3: Route learn output through session files, curated topic files, and affected artifacts

Advantages:

- Separates raw retrospective output from durable guidance.
- Gives periodic sessions a historical thread through dated files.
- Gives future contributors a topic-oriented discovery layer when a topic has enough durable lessons.
- Keeps actual behavior, workflow, skill, architecture, or decision changes in the artifact that owns that contract.
- Allows topic files to stay curated rather than append-only.
- Matches the current workflow principle that learn captures lessons but does not own operational lifecycle state.

Disadvantages:

- Adds more concepts than a single retrospective directory.
- Requires careful wording so contributors do not duplicate the same lesson across every surface.
- Needs a follow-up rule for trackable actions when no external issue tracker is available.

### Option 4: Make learn produce only artifact updates and ADRs

Advantages:

- Minimizes new documentation surfaces.
- Forces action-producing lessons into authoritative artifacts.
- Avoids stale retrospective files becoming quasi-policy.

Disadvantages:

- Loses raw session history.
- Hides observations that are useful context but not yet policy.
- Makes it harder to reconstruct why a durable lesson was adopted.
- Provides no home for periodic learning that concludes with observations, no immediate artifact change, or a scheduled follow-up.

## Recommended direction

Choose Option 3.

The learn refactor should define three canonical surfaces, each with a distinct lifecycle:

| Surface | Purpose | Canonical location | Lifecycle |
| --- | --- | --- | --- |
| Session output | Raw periodic or explicitly invoked learn-session record: observations, patterns, evidence, hypotheses, no-learn rationale, and candidate lessons. | `docs/learn/sessions/YYYY-MM-DD-<slug>.md` | Historical record. Dated files are retained as the session thread. |
| Durable topic guidance | Curated lessons worth finding by topic after the session. Each entry includes a date, short lesson, source link, and action classification. | `docs/learn/topics/<topic>.md` | Curated guidance. Entries are removed, revised, or absorbed when lessons are superseded, absorbed into stronger artifacts, or no longer useful. |
| Action-owning artifacts | The authoritative artifact changed because a lesson requires action: affected skill, workflow doc, spec, test spec, architecture doc, ADR, proposal, linked issue, or active plan. | Existing artifact path for the affected contract or follow-up tracker. | Owned by that artifact's normal lifecycle. The lesson references the action; the action does not live only in the lesson. |

This model should use the lightest structure that solves the current problem, with clear triggers for adding structure only after the lightest version proves insufficient. The first implementation can create `docs/learn/` and document `docs/learn/topics/<topic>.md` as the canonical topic layer without creating empty topic files, adding templates, or pre-building taxonomy. A topic file appears only when a learn session distills at least one durable lesson for that topic.

The shared `docs/learn/` parent is intentional. It avoids visually similar sibling paths by keeping raw historical session records under `docs/learn/sessions/` and curated topic guidance under `docs/learn/topics/`. The first implementation may add `docs/learn/README.md` as a lightweight index that explains the namespace, but it must not introduce session or topic templates before repeated usage shows a stable shape worth codifying.

Learning topic authority:

- Topic learning files are curated guidance, not authoritative workflow, product, architecture, validation, skill, or implementation contracts.
- Topic learning files may summarize lessons and point to authoritative artifacts.
- Topic learning files must not override `CONSTITUTION.md`, approved `specs/`, accepted ADRs, approved architecture docs, workflow docs, skill files, accepted proposals, or active plans.
- If a lesson changes behavior, workflow, architecture, validation, or skill behavior, the authoritative artifact must be updated. The topic file may link to that update, but it is not the source of truth.

The session file is the primary output of a learn session. It records the trigger, scope, evidence reviewed, observations, classification outcomes, contributor decisions, no-learn rationale when applicable, and links to all derivative artifacts. Topic files and action-owning artifacts are derivative outputs, not replacements for the session record.

The learn skill should guide the session as a process, not a template fill-in:

| Phase | Purpose | Output |
| --- | --- | --- |
| Frame | Establish the trigger, scope, evidence in scope, exclusions, prior learnings reviewed, and whether the session is periodic, incident-driven, or explicitly invoked. | Session frame in `docs/learn/sessions/YYYY-MM-DD-<slug>.md`. |
| Observe | Examine the evidence for repeated patterns, surprises, drift, gaps, and already-captured lessons. Each observation is tied to evidence. | Evidence-bound observations, or an explicit no-observation result. |
| Classify | Apply the classification scheme to each observation. The skill proposes classifications, but the contributor confirms or adjusts them before routing. | Confirmed classifications with rationale. |
| Route | Execute each classification's routing through topic entries, affected artifact updates, ADRs, proposals, linked follow-ups, or no-learn rationale. | Updated or linked derivative artifacts plus a session summary of what changed and what did not. |

Classification decisions record: the session file must record classification decisions before route actions proceed.

| Observation ID | Proposed classification | Final classification | Confirmed by | Rationale |
| --- | --- | --- | --- | --- |
| `OBS-001` | `Durable lesson` | `Artifact update` | contributor | This changes skill behavior, so the skill is the authoritative home. |

Routing must not proceed until every routed observation has a final classification. If confirmation is not available, the session may record candidate classifications, but it must not update topic files or action-owning artifacts.

The evidence set varies by trigger:

| Trigger type | Evidence to read |
| --- | --- |
| Every learn session | Trigger statement, named artifacts, relevant `docs/learn/` index entries when present, relevant session or topic files when present, and bounded governance or workflow context only when classification or routing depends on it. |
| Periodic session | Changes in the time window, including proposals, plans, change packs, ADRs, recent commits to canonical surfaces, and generated-output or validation records when relevant. |
| Incident session | Incident report, related artifacts, affected specs or plans, review or verify findings, and any relevant postmortem action records. |
| Explicit invocation | Artifacts named by the user and artifacts implied by the stated pattern, such as related reviews, specs, plans, change packs, ADRs, or workflow surfaces. |

Learn starts from compact summaries and targeted evidence. For every learn session, the skill must check whether governance or workflow context is needed, but it should not full-read every governance artifact by default. Use this order:

1. trigger statement and named artifacts;
2. relevant session or topic indexes, if present;
3. compact summaries or headings for governance and workflow artifacts;
4. exact sections only when classification or routing depends on them;
5. full-file reads only when narrower evidence is insufficient.

A learn session can be triggered by periodic cadence, incident response, contributor observation, or explicit maintainer request. None of these triggers lowers the evidence standard for capturing a durable lesson. The trigger establishes that a session runs; the evidence determines what the session captures. Sessions that run without producing durable lessons are valid outcomes.

The learn skill should classify each session output item by required action:

| Classification | Meaning | Routing |
| --- | --- | --- |
| Observation | Useful context, but no durable guidance or action yet. | Keep in the session file. |
| Durable lesson | Guidance future contributors should be able to find by topic. | Add or update the relevant `docs/learn/topics/<topic>.md` entry with source link. |
| Artifact update | Lesson changes an existing contract, checklist, skill, workflow, spec, test spec, architecture doc, or example. | Update the affected artifact and note the update in the session file and, when durable by topic, the topic file. |
| Decision | Lesson records a durable architecture or governance decision. | Create or update the relevant ADR or decision artifact, with links from the session and topic entry. |
| Direction | Lesson identifies a possible change that still needs deliberation. | Create a proposal or tracked follow-up; do not encode the direction as policy in a learning note. |
| Process follow-up | Lesson requires work but not immediate artifact editing. | Create or link a trackable follow-up in an issue when available, use the active plan when one owns the work, or open a proposal when no tracker or active plan exists. |
| No durable lesson | A trigger occurred, but evidence does not support a durable lesson. | Record a no-learn rationale in the session file or the triggering review-visible surface. |

During classification, evidence requirements are independent of trigger type. An observation supported by a single event remains an `Observation` or `No durable lesson` classification regardless of whether the session was triggered by maintainer request, periodic cadence, incident response, contributor observation, or explicit invocation. Maintainer-requested sessions that produce no durable lessons are recorded as such with a no-learn rationale.

Maintainer-driven rule adoption that lacks accumulated evidence is appropriate work for a proposal that may produce an ADR, not for a learn session. Learn sessions capture lessons that emerge from evidence; proposals deliberate decisions that require justification.

The `learn` skill should keep the existing narrowest-home principle, but make the routing order explicit:

1. Capture the session record in `docs/learn/sessions/YYYY-MM-DD-<slug>.md` when a learn session actually runs.
2. Distill only durable, reusable guidance into `docs/learn/topics/<topic>.md` when a topic entry is justified.
3. Update the affected authoritative artifact when the lesson changes a contract, decision, checklist, skill behavior, workflow, or example.
4. Create or link a trackable follow-up when the lesson requires action that is not completed in the same change.
5. Record an explicit no-learn rationale when the trigger produced no durable lesson.

Topic files should be deliberately curated. They are not an append-only log and do not need to preserve every historical observation. Session files preserve the historical record; topic files preserve what future contributors should find quickly.

Topic entry lifecycle:

- Topic files are curated, not append-only.
- A topic entry may be added, revised, superseded, absorbed into an authoritative artifact, or removed as obsolete.
- When an entry is removed or absorbed, the edit must preserve traceability by linking the session record that explains the change, linking the authoritative artifact that absorbed the lesson, or recording the removal rationale in the topic file edit or explain-change.

Empty sessions are valid. If the frame and observation phases find no durable lesson, the correct output is a session record or triggering review-visible note that explains the evidence reviewed and why no durable lesson was captured.

## Expected behavior changes

- A contributor running `learn` writes a dated session record under `docs/learn/sessions/` instead of choosing from several temporary surfaces for the raw session.
- A learn session proceeds through frame, observe, classify, and route phases rather than starting from output structure alone.
- Observations are evidence-bound, and empty sessions are accepted when evidence does not support durable lessons.
- Classification is proposed by the skill and confirmed or adjusted by the contributor before routing.
- Durable lessons can be found by topic under `docs/learn/topics/` when a topic file exists.
- Every durable lesson links back to the learn session, incident, change, review, or plan evidence that produced it.
- Lessons that change behavior or process update the affected authoritative artifact instead of living only in a retrospective note.
- Lessons that require future work become linked follow-ups rather than untracked "we should" observations.
- Topic files stay curated and may remove, revise, supersede, or absorb lessons while preserving traceability to the session record or authoritative artifact.
- `learn` remains retrospective and does not become lifecycle bookkeeping for plans, review resolution, verification, or PR state.

## Architecture impact

This is a workflow-governance and documentation-architecture change.

Likely touched surfaces for implementation:

- `specs/rigorloop-workflow.md` for final learn artifact model and temporary-surface retirement.
- `specs/rigorloop-workflow.test.md` for learn-routing proof.
- `skills/learn/SKILL.md` for session, topic, action, and no-learn routing.
- `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md` for canonical authored learn-surface and workflow summary alignment when their guidance is affected.
- `scripts/select-validation.py` and `scripts/test-select-validation.py` to classify `docs/learn/sessions/**` and `docs/learn/topics/**` as known learn artifact paths, even if validation remains lightweight.
- `scripts/test-skill-validator.py` and related validation tests if structural learn guidance should be regression-checked.
- Generated `.codex/skills/` and public adapters under `dist/adapters/` through existing generators when canonical skill content changes.

The first implementation should use skill guidance only for session and topic shape and defer templates until actual usage reveals a stable repeated shape worth codifying. The new `docs/learn/sessions/**` and `docs/learn/topics/**` paths are still canonical authored surfaces; source-boundary docs and selector behavior should recognize them in the first implementation slice. No runtime service, storage layer, network integration, security boundary, or release packaging change is expected unless the later spec chooses to add stronger validation automation for the new directories.

## Testing and verification strategy

The future implementation should use targeted proof first.

Likely validation:

```bash
python scripts/select-validation.py --mode explicit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path skills/learn/SKILL.md --path scripts/select-validation.py --path scripts/test-select-validation.py
bash scripts/ci.sh --mode explicit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path skills/learn/SKILL.md --path scripts/select-validation.py --path scripts/test-select-validation.py
python scripts/validate-skills.py
python scripts/test-skill-validator.py
python scripts/test-select-validation.py
python scripts/build-skills.py --check
python scripts/build-adapters.py --version 0.1.1 --check
python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-03-optimize-learn-skill.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md
git diff --check --
```

Focused proof should cover:

- `learn` remains periodic or explicitly invoked, not a default per-change stage.
- Learn artifacts use one parent namespace: `docs/learn/sessions/**` for raw sessions and `docs/learn/topics/**` for topic guidance.
- Topic files are curated guidance, not authoritative contracts, and do not override governance, specs, ADRs, architecture docs, workflow docs, skill files, accepted proposals, or active plans.
- The skill frames trigger, scope, evidence in scope, exclusions, and prior learning review before observing.
- Evidence reads are bounded, using summaries and exact sections before full-file reads.
- Observations are tied to evidence and do not repeat already-captured lessons.
- Contributor confirmation or adjustment happens before classifications are routed.
- Session files record proposed classifications, final classifications, confirmation, and rationale before routing.
- Empty sessions record why no durable lessons emerged.
- Session files, topic files, affected artifacts, ADRs, proposals, and follow-ups have distinct routing guidance.
- Raw session output and durable guidance are not treated as the same record type.
- Topic files are curated, not append-only.
- Topic entry removal or absorption preserves traceability through the session record, authoritative artifact link, topic-file edit, or explain-change.
- Lessons that require action produce an artifact update or trackable follow-up.
- Existing rules that keep `learn` non-authoritative for lifecycle bookkeeping remain intact.
- Selector behavior recognizes `docs/learn/sessions/**` and `docs/learn/topics/**` as known learn artifact paths.
- Generated skill and adapter outputs match canonical skill sources when skill content changes.

## Rollout and rollback

Rollout should use the full lifecycle because the change affects workflow policy, skill behavior, and contributor-visible artifact routing.

Recommended rollout:

1. Write an approved spec for the learn artifact model.
2. Update the matching test spec.
3. Update `skills/learn/SKILL.md` and affected governance or workflow summaries.
4. Classify `docs/learn/sessions/**` and `docs/learn/topics/**` in selector behavior as known learn artifact paths with lightweight validation.
5. Use skill guidance only for session and topic shape; defer templates until repeated usage reveals a consistent shape worth codifying.
6. Refresh generated skill and adapter output through the existing generators.
7. Run targeted validation and record commands actually run.

Rollback is straightforward because no existing `docs/learn/` or `docs/retrospectives/` content exists today. If the model proves too heavy during review, the implementation can revert to the current temporary-surface rule from `specs/rigorloop-workflow.md` and keep this proposal as rejected or superseded history.

Migration expectations:

- Existing change-local learning notes do not need migration unless a later plan explicitly relies on them as current guidance.
- New learn sessions after adoption use `docs/learn/sessions/YYYY-MM-DD-<slug>.md`.
- New durable topic entries appear only when a real lesson justifies a `docs/learn/topics/<topic>.md` file.

## Risks and mitigations

- Risk: The model creates too much process for small learn sessions.
  - Mitigation: Session files can record no durable lesson, and topic files are created only when durable guidance exists.

- Risk: Topic files become unbounded logs.
  - Mitigation: Treat session files as the historical record and topic files as curated guidance where entries can be removed, revised, or absorbed into stronger artifacts.

- Risk: Topic files become quasi-policy and compete with authoritative artifacts.
  - Mitigation: Define topic files as curated guidance only, require authoritative artifacts for behavior or contract changes, and make topic entries link to rather than override governing sources.

- Risk: Topic entry removal loses traceability.
  - Mitigation: Require removed or absorbed entries to preserve traceability through a session link, authoritative artifact link, topic-file edit rationale, or explain-change rationale.

- Risk: Lessons duplicate or compete with authoritative artifacts.
  - Mitigation: Route contract changes to the affected artifact and use learning files as traceability records, not policy substitutes.

- Risk: Actionable lessons become untracked notes.
  - Mitigation: Require action-producing lessons to link an artifact update, proposal, ADR, issue, or active-plan follow-up.

- Risk: Contributors treat `learn` as a blocker for ordinary PR closeout.
  - Mitigation: Preserve the current workflow rule that triggered `learn` blocks downstream only when a higher-priority artifact makes it blocking.

- Risk: The topic taxonomy fragments into near-duplicate files.
  - Mitigation: Start with natural existing workflow topics such as proposals, verification, reviews, architecture, CI, adapters, and workflow only when real lessons exist, then consolidate during periodic curation.

- Risk: The skill overreaches by creating lessons or classifications without enough contributor judgment.
  - Mitigation: Require evidence-bound observations, contributor confirmation before routing, no durable lessons from single events unless the evidence shows a reusable pattern or systemic gap, and valid empty-session outcomes even when a maintainer requested the session.

- Risk: Required learn evidence reads become too expensive for small explicit invocations.
  - Mitigation: Start from trigger statements, named artifacts, indexes, headings, and exact sections, and full-read governance files only when narrower evidence is insufficient.

- Risk: New canonical learn paths are created but remain invisible to repository validation routing.
  - Mitigation: Classify `docs/learn/sessions/**` and `docs/learn/topics/**` as known learn artifact paths in selector behavior in the first implementation slice, even if validation remains lightweight.

## Open questions

None.

The previously open questions are resolved by the lightest-structure principle: use skill guidance before templates, open a proposal when no issue tracker or active plan exists for follow-up work, and edit topic entries in place with source links rather than adding archive infrastructure.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-05-03 | Draft the focused learn artifact model proposal. | The workflow refactor intentionally deferred the final learn model, and the current temporary-surface rule is not a durable enough contributor contract. | Keeping temporary surfaces as the final state. |
| 2026-05-03 | Recommend session files, curated topic files, and affected-artifact routing as distinct surfaces. | The surfaces have different lifecycles: historical thread, findable durable guidance, and authoritative action. | Single retrospective directory; artifact-updates-only model. |
| 2026-05-03 | Keep topic files curated and create them only when real durable lessons exist. | This preserves discoverability without pre-building taxonomy or making topic files append-only logs. | Pre-created topic taxonomy; session-only browsing. |
| 2026-05-04 | Resolve proposal open questions by applying the lightest-structure principle. | Skill guidance is enough before repeated usage justifies templates, proposals force prioritization when no tracker or active plan exists, and in-place topic edits preserve source links without archive infrastructure. | First-version templates; `docs/roadmap.md` as a follow-up sink; retired-entry archive path. |
| 2026-05-04 | Define `learn` as a four-phase process rather than an output-template exercise. | The hard part of learning is surfacing evidence-bound observations, classifying them with contributor judgment, and routing them correctly; artifacts should emerge from that process. | Template-first skill behavior; unilateral classification; lessons manufactured from thin evidence. |
| 2026-05-04 | Keep the evidence standard independent of the trigger type. | Maintainer request, cadence, incident response, contributor observation, and explicit invocation can trigger a session, but only evidence determines whether a durable lesson is captured. | Letting maintainer-requested sessions create durable learn output from isolated events without reusable evidence. |
| 2026-05-04 | Use one learn namespace with `sessions/` and `topics/` subdirectories. | A `docs/learn/` session directory plus a similarly named sibling topic directory was too visually similar for different semantics. A single parent makes the distinction explicit. | Sibling session and topic directories under different parent paths. |
| 2026-05-04 | Make topic-file authority, classification confirmation, and topic-entry traceability explicit. | Topic guidance must not become quasi-policy, routing must not happen from unconfirmed classifications, and curated topic edits must preserve reviewable history. | Implicit authority boundaries; unrecorded confirmation; removable topic entries without trace rules. |
| 2026-05-04 | Bound learn evidence reads and classify new learn paths in selector behavior. | Learn should stay evidence-bound without full-reading every governance artifact by default, and canonical learn paths should be visible to validation routing from the first implementation slice. | Full-file governance reads by default; unclassified canonical learn paths. |

## Next artifacts

- `proposal-review` for the added process model, scope, and artifact-surface challenge.
- Feature spec for the learn artifact model, likely updating `specs/rigorloop-workflow.md`.
- Matching test spec updates for learn routing and validation evidence.
- Architecture or ADR only if review decides the model introduces a durable repository-architecture or governance decision beyond workflow artifact routing.
- Execution plan if implementation touches workflow spec, test spec, skill source, generated outputs, and validation tests.

## Follow-on artifacts

- [Learn Artifact Model](../../specs/learn-artifact-model.md)

## Readiness

Accepted after `proposal-review`.

The recommended direction is settled enough to support downstream spec work: it chooses a three-surface learn model, defines `learn` as a four-phase evidence-bound process, preserves the current nonblocking periodic role of `learn`, identifies alternatives and tradeoffs, and has no open questions blocking review.
