# Formal Review Recording

## Status

- accepted

## Problem

`docs/changes/<change-id>/reviews/` is structurally capable of recording formal lifecycle reviews beyond `code-review`, but current usage and contributor guidance still make `code-review` the only consistently recorded review stage.

That leaves proposal-review, spec-review, architecture-review, and plan-review outcomes too easy to lose in chat, artifact comments, or final status updates. When those upstream reviews produce material findings, later contributors cannot reliably reconstruct what was found, what changed because of it, whether the finding was re-reviewed, and which evidence closed it.

The result is an uneven review history: implementation review is durable, while earlier direction, contract, design, and sequencing review can become implicit.

## Goals

- Make formal lifecycle review recording stage-neutral instead of code-review-specific.
- Preserve material upstream review findings before review-driven fixes begin.
- Keep top-level proposal, spec, architecture, and plan artifacts as their own source of truth for final status.
- Keep `docs/changes/<change-id>/` concise and proportional.
- Reuse the existing `reviews/`, `review-log.md`, and `review-resolution.md` model.
- Avoid forcing empty review boilerplate for clean, low-risk, or isolated review outputs.
- Make review records useful for downstream `verify`, `explain-change`, and PR summaries.

## Non-goals

- Creating separate directories for each review stage.
- Replacing artifact-local status, decision logs, readiness, or follow-on sections.
- Requiring a full review artifact pack for every clean review.
- Automatically copying maintainer PR comments into `reviews/`.
- Turning `change.yaml` into a long-form review transcript.
- Automating semantic judgment about whether a review finding is correct.
- Migrating historical change packs that are not touched or relied on by the new change.

## Vision fit

fits the current vision

This proposal strengthens RigorLoop's Git-first reviewability by preserving important review evidence in tracked files without expanding into a broad project-management layer.

## Context

`CONSTITUTION.md` requires RigorLoop to optimize for reviewability, traceability, and trustworthy automation. It also says change-local artifacts should stay concise and link to approved top-level artifacts instead of becoming a second long-form source of truth.

`specs/review-finding-resolution-contract.md` already defines `docs/changes/<change-id>/reviews/` as the home for detailed formal lifecycle review records. It explicitly allows `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, and `code-review` as formal lifecycle review stages.

The same spec already defines the supporting structure:

- one detailed review file per formal review event;
- `review-log.md` as the compact index;
- `review-resolution.md` as the material-finding disposition and closeout surface;
- closeout validation before `verify`, final `explain-change`, and `pr` handoff.

The practical gap is not a missing storage location. The gap is a stage-usage policy: contributors need to know when upstream review outputs should become detailed change-local records, and how those records relate to artifact-local status.

`docs/project-map.md` is absent, so this proposal relies on the current governing specs, workflow docs, skills, validators, and existing change-local examples rather than a project-map summary.

## Options considered

### Option 1: Keep durable review records mostly code-review-only

Advantages:

- Requires no new guidance or validation.
- Keeps upstream authoring stages lightweight.
- Matches recent common practice.

Disadvantages:

- Loses important review evidence before implementation.
- Makes review-resolution appear implementation-specific even though the contract is stage-neutral.
- Forces downstream contributors to infer why proposals, specs, architecture, or plans changed.
- Weakens traceability for the stages that most often decide scope, contract, and design.

### Option 2: Require detailed records for every formal review invocation

Advantages:

- Maximum consistency.
- Every review gate has a predictable file.
- Simple to audit whether a stage happened.

Disadvantages:

- Creates empty or low-value files for clean reviews.
- Conflicts with the current lightweight clean-review path.
- Turns `docs/changes/` into ceremony for early-stage reviews that may not yet have a change root.
- Encourages transcript storage instead of targeted material-finding capture.

### Option 3: Use one stage-neutral review ledger with proportional triggers

Advantages:

- Reuses the existing review-artifact model.
- Records upstream review findings when they materially affect the change.
- Preserves clean-review lightweight behavior.
- Keeps artifact-local status authoritative.
- Avoids new path taxonomy and migration work.

Disadvantages:

- Requires clearer trigger language in workflow and stage skills.
- Requires contributors to distinguish artifact-local settlement from change-local review evidence.
- May require reconstructed records when earlier review findings were acted on before a change root existed.

### Option 4: Record upstream reviews only inside the reviewed artifact

Advantages:

- Keeps review evidence close to the artifact being reviewed.
- Avoids creating or updating `docs/changes/` early.
- Makes accepted proposal/spec/architecture/plan status easy to see.

Disadvantages:

- Mixes first-pass findings, fixes, and final settlement in the same artifact.
- Makes cross-stage review closeout hard to validate.
- Does not provide a common review-resolution surface for findings that affect multiple artifacts.
- Makes PR and explain-change summaries less consistent.

## Recommended direction

Choose Option 3.

Use the existing change-local review artifact model for all formal lifecycle review stages, not only `code-review`.

The recommended practice is:

1. `docs/changes/<change-id>/reviews/<stage>-r<n>.md` records one formal review event when the event produces material findings, a stage-owned non-approval outcome that blocks downstream progress or requires revision, or a review result that downstream stages will cite as required closeout evidence.
2. `Stage:` in the detailed review file is one of `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, or `code-review`.
3. `review-log.md` indexes every detailed review file under `reviews/`, including upstream stage reviews.
4. `review-resolution.md` records final dispositions for every material Finding ID from any formal review stage.
5. Artifact-local status remains authoritative:
   - proposals settle in the proposal;
   - specs settle in the spec;
   - architecture artifacts settle in the architecture document or ADR;
   - plans settle in the plan body and `docs/plan.md`;
   - change-local review files preserve review evidence and closeout, but do not replace those artifact states.
6. Clean reviews with no material findings do not require empty `reviews/`, `review-log.md`, or `review-resolution.md` files solely to prove the review happened. The reviewed artifact's status, decision log, readiness, or follow-on section can record clean settlement.
7. When a clean review is still a required gate and downstream stages cite it, the lightest durable record should be the reviewed artifact's decision log or readiness section. A detailed review file is reserved for material findings, stage-owned non-approval outcomes that block downstream progress or require revision, reconstructed evidence, or explicit reviewer/maintainer request.
8. If review-driven fixes already began before a durable upstream review record was created, repair only material findings with a reconstructed review record that follows the existing reconstructed-record rules.

This keeps the rule consistent: review records are event evidence, not stage status. Stage status still belongs to the reviewed artifact or plan lifecycle.

### Initial review-record root

When a workflow-managed formal review triggers a detailed review file before a change-local root exists, create the smallest review-record root needed to preserve the review event and make it discoverable before review-driven fixes or downstream routing proceed.

When material findings exist, the initial review-record root includes:

```text
docs/changes/<change-id>/
|-- change.yaml
|-- review-log.md
|-- review-resolution.md
`-- reviews/
    `-- <stage>-r<n>.md
```

`review-resolution.md` is included because material findings require dispositions.

When no material findings exist, but a detailed review file is still required by a stage-owned non-approval outcome, reconstructed evidence, closeout evidence citation, or explicit reviewer or maintainer request, the initial review-record root includes:

```text
docs/changes/<change-id>/
|-- change.yaml
|-- review-log.md
`-- reviews/
    `-- <stage>-r<n>.md
```

Do not create an empty `review-resolution.md` solely because `reviews/` exists.

The initial review-record root is not the final non-trivial change pack. Final handoff for non-trivial work still requires the baseline non-trivial pack, including durable Markdown reasoning such as `docs/changes/<change-id>/explain-change.md` or another approved durable reasoning surface.

If the review is isolated or review-only and no tracked change will proceed, a durable detailed review file remains optional unless the reviewer or maintainer asks for one.

### Clean required review recording

A required formal review with no material findings can be recorded in the reviewed artifact's status, decision log, readiness, or follow-on section.

A detailed review file is reserved for cases where:

- material findings exist;
- the review result is a stage-owned non-approval outcome that blocks downstream progress or requires revision;
- downstream stages cite the review as closeout evidence that cannot be understood from artifact-local status;
- the review is reconstructed;
- a reviewer or maintainer explicitly requests a detailed record.

Stage-owned non-approval outcomes include `revise`, `changes-requested`, `blocked`, `rethink`, `inconclusive`, and any equivalent stage-specific outcome that prevents downstream progress.

Create `docs/changes/<change-id>/reviews/<stage>-r<n>.md` when a formal lifecycle review produces any of:

- material findings;
- a stage-owned non-approval outcome that blocks downstream progress or requires revision;
- reconstructed review evidence;
- review findings that will be cited as closeout evidence;
- explicit reviewer or maintainer request.

### Material finding boundary

A review finding is material when it:

- changes or blocks the reviewed proposal, spec, architecture, plan, code, tests, validation, or generated output;
- requires a disposition in `review-resolution.md`;
- changes scope, behavior, architecture, sequencing, proof strategy, or risk;
- creates a follow-up action;
- exposes a workflow or process problem;
- is classified as blocker, major, or review-outcome-changing.

Minor copyedits, formatting nits, and non-actionable notes are not material unless the reviewer explicitly marks them material.

### Maintainer PR comments

Maintainer PR comments are not automatically copied into `reviews/`.

If a maintainer PR comment creates a material finding that changes tracked artifacts or requires disposition, it must have a stable Finding ID before it can be dispositioned in `review-resolution.md`.

The stable Finding ID comes from a durable review record, such as:

- `docs/changes/<change-id>/reviews/code-review-r<n>.md`;
- another formal review record that captures the PR comment as evidence;
- `docs/changes/<change-id>/reviews/pr-review-r<n>.md`, if the follow-on spec explicitly adds PR-review records to the allowed review-stage set.

`review-resolution.md` must not introduce new material Finding IDs that do not exist in a review record.

This proposal focuses on formal lifecycle review stages. It does not forbid durable capture of material PR review findings when needed, but a dedicated `pr-review` record type would require explicit spec and validator support.

### Structural and metadata rules

If `docs/changes/<change-id>/reviews/` exists, `docs/changes/<change-id>/review-log.md` is required.

Every detailed review file under `reviews/` has exactly one `Review ID`, and every detailed review file's `Review ID` appears exactly once in `review-log.md`.

`change.yaml.review` keeps the existing schema-required fields:

- `status`;
- `unresolved_items`.

Optional pointer fields can be added when review artifacts exist:

- `review_log`;
- `review_resolution`.

`change.yaml` must not duplicate detailed review records or finding transcripts. It should keep review state as an aggregate summary and pointer surface, not as the detailed review ledger:

```yaml
review:
  status: none | clean | findings-open | resolved | blocked
  unresolved_items: 0
  review_log: docs/changes/<change-id>/review-log.md
  review_resolution: docs/changes/<change-id>/review-resolution.md
```

Detailed review records remain in `reviews/`. Finding dispositions remain in `review-resolution.md`.

## Expected behavior changes

- Material findings from `proposal-review`, `spec-review`, `architecture-review`, and `plan-review` are recorded before fixes begin when the change is workflow-managed.
- Workflow-managed formal reviews that trigger detailed review files before a change-local root exists create the smallest initial review-record root before fixes or downstream routing proceed.
- `review-resolution.md` can close findings from any formal review stage, not only code review.
- `review-log.md` becomes the compact index for the whole formal review history of a change.
- Clean upstream reviews stay lightweight and can be recorded in artifact-local settlement sections instead of detailed review files.
- `change.yaml` continues to summarize review status, unresolved items, and artifact links rather than duplicating detailed review records.
- Maintainer PR comments are not automatically copied into `reviews/`, but material PR review findings can still be promoted into durable review records when durable closeout is needed.
- `verify`, `explain-change`, and `pr` can rely on the same closeout model regardless of which review stage produced the material finding.

## Architecture impact

This is a workflow-contract and guidance clarification, not a new storage architecture.

Likely touched surfaces if this proposal advances:

- `specs/rigorloop-workflow.md` to clarify that formal review recording is stage-neutral and proportionally triggered.
- `specs/review-finding-resolution-contract.md` for sharper trigger wording and for any accepted `pr-review` record extension.
- `docs/workflows.md` for contributor-facing summary.
- `CONSTITUTION.md` and `AGENTS.md` if their concise review summaries need alignment.
- `skills/proposal-review/SKILL.md`, `skills/spec-review/SKILL.md`, `skills/architecture-review/SKILL.md`, and `skills/plan-review/SKILL.md` to add record-trigger instructions matching `code-review`.
- `skills/verify/SKILL.md`, `skills/explain-change/SKILL.md`, and `skills/pr/SKILL.md` if they need to describe upstream review closeout checks more explicitly.
- `schemas/change.schema.json` only if the aggregate optional `review` pointer fields need explicit schema validation beyond the current permissive shape.
- `scripts/review_artifact_validation.py` and `scripts/test-review-artifact-validator.py` only if current validator coverage lacks representative upstream-stage fixture coverage or if a dedicated `pr-review` stage is accepted.

The existing `scripts/review_artifact_validation.py` stage set already includes the desired review stages, so this should not require a new review-artifact parser model.

## Testing and verification strategy

- Add or update test-spec coverage showing that formal review records are stage-neutral.
- Cover the change-local root trigger for workflow-managed formal review findings before fixes proceed.
- Cover clean required review settlement through artifact-local status, decision log, readiness, or follow-on sections.
- Cover the material finding boundary so copyedits, formatting nits, and non-actionable notes do not force review-resolution.
- Cover that `change.yaml.review` keeps `status` and `unresolved_items`, with `review_log` and `review_resolution` only as optional pointers.
- Cover that `review-resolution.md` cannot introduce a material Finding ID that does not exist in a review record.
- Add regression coverage for at least one upstream detailed review file, such as `spec-review-r1.md` or `plan-review-r1.md`, passing the review-artifact validator.
- Confirm `review-log.md` and `review-resolution.md` behavior remains identical for upstream stages and `code-review`.
- Confirm `change.yaml.review` remains an aggregate summary and pointer surface.
- Run targeted selector and review-artifact validation for touched workflow, skill, spec, and script paths.
- If canonical skills change, regenerate `.codex/skills/` and public adapter output through the repository generators.

## Rollout and rollback

Rollout:

- Update the workflow/spec guidance first.
- Align upstream review skills.
- Add focused validator regression coverage only if missing.
- Start using upstream review records on the next change whose proposal/spec/architecture/plan review produces material findings.

Rollback:

- Revert the guidance and skill wording.
- Keep already-recorded upstream review files as valid historical review artifacts, since the existing validator already recognizes their stages.
- Continue relying on artifact-local status and `code-review` records until a narrower policy is approved.

## Risks and mitigations

- Risk: contributors create detailed files for every clean review.
  - Mitigation: make the trigger proportional and repeat that clean review settlement can live in the reviewed artifact.
- Risk: upstream review records become a second source of truth for proposal/spec/architecture/plan status.
  - Mitigation: state that artifact-local status remains authoritative and review files are event evidence.
- Risk: early review happens before `docs/changes/<change-id>/` exists.
  - Mitigation: create the smallest initial review-record root before fixes or downstream routing proceed when workflow-managed review events need durable preservation.
- Risk: `change.yaml` becomes overloaded with per-stage details.
  - Mitigation: keep `change.yaml.review` as an aggregate summary and link detailed artifacts instead of embedding them.
- Risk: maintainer PR comments are either ignored or over-copied.
  - Mitigation: do not automatically copy PR comments, but require material PR review findings to receive stable Finding IDs through durable review records before disposition.
- Risk: historical inconsistency appears worse after the policy changes.
  - Mitigation: do not migrate old packs unless touched, generated, or relied on as current guidance.

## Open questions

- None. Clean required reviews can use artifact-local settlement, detailed review indexing remains in `review-log.md`, and workflow-managed reviews that require detailed records open or update the change-local root before fixes or downstream routing proceed.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-05-04 | Draft proposal created with a stage-neutral, proportional recording recommendation. | The existing review-artifact contract already supports all formal review stages; the gap is guidance and usage consistency. | Code-review-only records, mandatory records for every review invocation, and reviewed-artifact-only records. |
| 2026-05-04 | Accepted the proportional trigger details for change-local roots, clean review recording, material finding scope, PR comments, structural review-log rules, and aggregate `change.yaml.review` shape. | These details preserve traceability where review findings drive change without turning every clean review into a detailed artifact pack. | Mandatory clean-review detailed files, automatic PR-comment copying, and storing detailed review records in `change.yaml`. |
| 2026-05-04 | Resolved proposal-review findings by preserving `change.yaml.review.status` and `unresolved_items`, distinguishing initial review-record roots from final non-trivial packs, requiring PR-comment Finding IDs to originate in durable review records, and using one stage-neutral non-approval outcome phrase. | These fixes align the recommendation with the existing schema, baseline change-pack policy, review-resolution Finding ID contract, and stage-owned review vocabularies. | Dropping `unresolved_items`, treating the initial root as the final pack, introducing Finding IDs directly in `review-resolution.md`, and using inconsistent outcome terms. |
| 2026-05-04 | Proposal accepted after clean `proposal-review`; focused spec authored as the next contract artifact. | The reviewed direction has no open decision questions and is ready to govern spec work. | Leaving the relied-on proposal in draft while downstream spec work proceeds. |
| 2026-05-04 | Approved spec refined the initial review-record root into material and no-material variants. | Non-material detailed-record triggers need a discoverable root and `review-log.md`, but they must not create empty `review-resolution.md` files solely because `reviews/` exists. | Material-only root wording and mandatory empty `review-resolution.md` files for no-material review events. |

## Next artifacts

- `plan-review` for `docs/plans/2026-05-04-formal-review-recording.md`.
- Matching test-spec coverage for upstream formal review records after plan-review.
- Implementation only after plan-review and test-spec.

## Follow-on artifacts

- Spec: `specs/formal-review-recording.md`
- Plan: `docs/plans/2026-05-04-formal-review-recording.md`

## Readiness

Accepted. Downstream spec is approved at `specs/formal-review-recording.md`; execution planning is underway at `docs/plans/2026-05-04-formal-review-recording.md`.
