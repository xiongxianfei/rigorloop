# Workflows

This file is the short operational summary for working in this repository. The normative workflow contract lives in `specs/rigorloop-workflow.md`.

## Skill Contract

- The normative skill-contract source is `specs/skill-contract.md`.
- The workflow-routing source is `specs/rigorloop-workflow.md`.
- Skills are operational guides, not substitute specs.
- Shipped skill text is the user-facing interface. Keep repository-maintainer details such as canonical source paths, generated mirrors, adapter paths, selector path constraints, drift-check mechanics, and shared-block implementation details in contributor surfaces rather than in published skills.
- Skill-contract summaries in this file and `AGENTS.md` do not override approved specs.
- Shared skill policy blocks live under `templates/shared/<block-name>.md`.
- Public shared blocks are copied into consuming skills and checked for drift; maintainer-only blocks such as generated-output handling are not copied into published skills.
- Edit canonical skill source under `skills/<skill>/SKILL.md`; for public adapter installation, use `dist/adapters/README.md`. For `v0.1.3` and later, generated public adapter skill bodies are release archives, not tracked source under `dist/adapters/`.
- Evidence reading starts from summaries, stable IDs, headings, targeted sections, check IDs, file paths, counts, and line citations before broad reads.
- Add a skill only when it owns a distinct artifact, gate, review responsibility, recurring action, or approved operational process.
- Do not create a new skill for one-off helper behavior, tiny formatting rules, or checklists that belong inside an existing skill.

## Standard Workflow

RigorLoop recommends one standard workflow for complete AI-assisted delivery.

Users may manually invoke an individual skill for focused output. Manual skill invocation is isolated by default and does not mean the full workflow is complete.

Workflow completion claims require evidence from the relevant standard workflow stages.

## Project Vision

- `VISION.md` is the canonical project-vision artifact for project identity, target users, commitments, refusals, and proposal-fit reference.
- The `vision` skill is upstream of the per-change workflow, not a normal lifecycle stage.
- Proposals created or substantively revised after this spec is adopted include `Vision fit`.
- README content between `<!-- vision:start -->` and `<!-- vision:end -->` is generated from `VISION.md`.
- README front-matter is not the source of truth when it conflicts with `VISION.md`.

## Workflow Categories

- Standing artifacts: `VISION.md` and `CONSTITUTION.md`.
  - `VISION.md` absence blocks the first substantive proposal unless the proposal bootstraps project vision.
  - `CONSTITUTION.md` absence blocks governance adoption, workflow-governance changes, and source-of-truth changes unless the proposal bootstraps the constitution.
- Living references: `docs/project-map.md`.
  - Do not rely on the map when it is absent, known-stale, contradicted, or missing the relied-on area. Refresh it or record a no-map rationale before reliance.
  - Calendar freshness thresholds, markers, and the full project-map revision workflow are deferred.
- Workflow infrastructure: `specs/rigorloop-workflow.md`, this summary, affected root guidance, affected stage skills, and generated skill or adapter output when canonical skills change.
  - Workflow-governance changes update affected surfaces, mark them unaffected with rationale, or defer them with owner and follow-up in a tracked or review-visible surface.
- On-demand support: `explore` and `research`.
  - Use them when ambiguity, option expansion, architecture uncertainty, external facts, platform behavior, standards, laws, pricing, or other current evidence affects the decision.
- Per-change chain:
  - `proposal -> proposal-review -> spec -> spec-review -> architecture -> architecture-review -> plan -> plan-review -> test-spec -> implement -> code-review -> review-resolution when triggered -> ci-maintenance when triggered -> explain-change -> verify -> pr`
  - For milestone-based plans, the `implement -> code-review -> review-resolution when triggered` segment repeats for each in-scope implementation milestone. Final closeout follows only after all in-scope implementation milestones are closed and required review-resolution is closed.
  - `review-resolution` runs only when material review findings, non-final dispositions, or review outcomes require explicit closeout.
  - `ci-maintenance` is conditional support when hosted workflow automation or related CI infrastructure for a material risk is missing, stale, or wrong.
- Periodic artifacts: `learn`.
  - Run it on cadence, after incident response, contributor observation, repeated findings, blocker or major workflow-process findings, failed release or adapter smoke, accepted postmortem actions, or explicit maintainer request.
  - When a learn session reaches Frame, record it under `docs/learn/sessions/YYYY-MM-DD-<slug>.md`; durable topic guidance uses `docs/learn/topics/<topic>.md` only when confirmed durable lessons justify it.
  - Pre-session scheduled follow-up, deferral, or no-learn rationale can close a trigger only when `learn` does not actually run as a session. Triggered `learn` blocks downstream only when a higher-priority artifact makes it blocking.

## Stage Obligations

The workflow spec owns the full stage-obligation table. The stable obligation values are:

| Obligation | Meaning |
| --- | --- |
| `mandatory` | Required whenever the row's trigger applies. |
| `conditional` | Required only when the trigger applies or the artifact or action is cited as a dependency. |
| `on-demand` | Created or run only when explicitly invoked or when the work depends on it. |
| `periodic` | Run on cadence, incident response, contributor observation, repeated finding, failed smoke, accepted postmortem action, or maintainer request. |

Notes:

- `explore` and `research` are on-demand support, not default prerequisites.
- `learn` is periodic or explicitly invoked, not a default final per-change stage. It uses tracked session records after Frame and review-visible no-record closeout only before a session runs.
- `ci-maintenance` means creating or updating hosted CI workflow files, validation automation, or platform configuration. It does not mean running validation, designing tests, specifying validation commands, or waiting for existing CI checks.
- After `spec-review`, the immediate next stage is still `architecture` when needed, otherwise `plan`. Any mention of eventual `test-spec` readiness is downstream readiness, not a stage skip.
- `plan-review` remains the normal immediate handoff into `test-spec`. If implementation readiness is mentioned there, it is downstream readiness rather than the handoff itself.
- In standard workflow execution, stage-owned language stays split: `implement` reports implementation completion or readiness for `code-review`; `code-review` owns review findings; `verify` owns `branch-ready`; `pr` owns `pr-body-ready` and `pr-open-ready`.
- Before `implement` hands off to `code-review`, the slice should satisfy a first-pass acceptable result: address in-scope requirements, required authored and aligned surfaces, required edge cases, and targeted validation for the smallest scope-complete change.
- If a required surface stays unchanged, record `unaffected with rationale` in an authoritative surface such as the active plan or required change-local artifacts. If missing or contradictory inputs prevent that standard, stop with a blocker instead of handing off an incomplete slice.
- Later review comments may still happen. A preventable first-pass miss is a finding that should have been caught by the slice's completeness set, required edge cases, or targeted validation before `code-review`.
- `code-review` may inspect staged or unstaged diffs, but cited governing artifacts only support a clean branch-scoped conclusion when they are confirmed in tracked governing branch state.
- Missing tracked governing authority blocks `clean-with-notes` but does not suppress independently supported findings, and named edge cases need direct proof for clean review or `branch-ready`.
- A material review finding is incomplete unless it has evidence, a required outcome, and a safe resolution path or `needs-decision` rationale.

## Architecture Packages

- When architecture is required, the architecture stage produces or updates the architecture package defined by `specs/architecture-package-method.md` before planning continues.
- Use `templates/architecture.md` and `templates/adr.md` as scaffolds. Real architecture and ADR records live under `docs/architecture/` and `docs/adr/`.

## Efficient Evidence Collection

- Use bounded extraction as the default first pass for large files, repeated scans, generated output, and validation logs.
- Do not broad-search authoritative documents solely for path or state discovery when narrower evidence is available.
- Default evidence sequence for path or state discovery:
  1. exact user-provided path or change ID;
  2. current handoff summary or active plan state;
  3. `change.yaml`, review log, review resolution, or release metadata;
  4. `docs/workflows.md` artifact-location map;
  5. targeted headings, stable IDs, line ranges, counts, or diffs;
  6. full-file read only when the whole file is the target or bounded evidence is insufficient.
- Start with inventories, headings, stable IDs, path lists, counts, or matching line numbers before reading broad file content.
- After locating relevant lines, read exact ranges first; broaden to neighboring sections or a full-file read only when needed.
- Prefer check IDs, requirement IDs, test IDs, file paths, counts, and line citations before raw excerpts or pasted logs.
- Use bounded evidence before broad reads, but do not under-read.
- Expand to a broader section or full file when bounded evidence is incomplete, contradictory, or insufficient to support the claim being made.
- Use summary-first, failure-focused, and diff-focused normal output by default. Expand only when needed with `--verbose` or an equivalent documented escape hatch.
- Normal output budgets:
  - routine command output target: 40 lines
  - routine command output warning threshold: 80 lines
  - single excerpt target: 12 lines
  - single excerpt warning threshold: 20 lines
  - multi-file summary default: one summary line per file, with details only for changed, failing, or explicitly requested files
- Do not print every parsed field, every unchanged file, large excerpts, repeated path lists, or routine command output by default.
- Output budgets guide readability and token use; they must not change validation semantics, selected check coverage, or command exit behavior.
- When normal output omits detail, it must say how to request the omitted detail.
- A full-file read is required when the file itself is the review target, the relevant section cannot be isolated safely, surrounding context can change the conclusion, bounded searches disagree or produce incomplete evidence, or a behavior-changing edit depends on understanding the whole source-of-truth artifact.

## Stage Evidence Access

Stage skills should start from the smallest sufficient evidence set needed to prove their owned claim.

- Default evidence: read first without extra explanation because the stage normally needs it.
- Conditional evidence: read only when the named trigger applies.
- Expansion evidence: substantive content outside its default evidence and triggered conditional evidence.
- Broad or full-file evidence: read only when bounded evidence cannot answer the stage-owned question.

Bounded discovery is not evidence expansion. Bounded discovery includes path inventory, heading scan, line-number search, count query, targeted diff summary, and metadata lookup.

Evidence expansion begins when a stage reads substantive content outside its default evidence and triggered conditional evidence. Record a compact reason when that happens. Only include `Evidence expansion` when expansion occurred.

Do not broad-search authoritative documents solely for path or state discovery when bounded discovery can answer the question. Use active artifacts, `docs/workflows.md`, headings, stable IDs, counts, targeted excerpts, and diffs before broad reads.

A stage must expand when bounded evidence is missing, stale, contradictory, or insufficient for the stage-owned claim. Full-file reads remain allowed when the whole file is the target, the relevant section cannot be isolated safely, bounded evidence is contradictory or incomplete, surrounding context can change the conclusion, or the decision depends on whole-file context.

First-slice ownership:

- M1 validation covers `docs/workflows.md`, `skills/proposal/SKILL.md`, and `skills/proposal-review/SKILL.md`; include `skills/spec/SKILL.md` only when M1 updates `spec`.
- M2 validation separately covers `skills/implement/SKILL.md` and `skills/code-review/SKILL.md` when M2 runs.
- The first slice is operational guidance. It does not create a new normative spec unless validators enforce the contract.

## Workflow Detail Ownership

The public `workflow` skill should route and assess state. Long-form workflow explanation belongs here, the workflow spec, or the owning stage skill.

Moved or summarized detail is owned as follows:

- review-resolution detail: `docs/workflows.md`, `specs/rigorloop-workflow.md`, and review-resolution or review-stage guidance own detailed disposition, review-log, and closeout behavior.
- lifecycle-managed artifact tables: `docs/workflows.md` and the workflow spec own full contributor-facing artifact state tables and settlement rules.
- validation-layering detail: validation selectors, test specs, release specs, and verify guidance own detailed proof selection, broad-smoke triggers, and manual-proof rules.
- default artifact path lists: contributor-facing workflow guidance and examples own repository path conventions; public skill text should not require path-list reads to route ordinary work.
- bugfix and support-stage detail: the owning skill and workflow summary own specialized behavior after the workflow router identifies the trigger.

Workflow safety topics MUST NOT be removed when public skill text is compressed. A removed or summarized topic needs a new owner surface or an explicit no-longer-needed rationale in the change evidence.

## Follow-up ownership

Record follow-ups where they can be acted on.

| Follow-up type | Owner |
| --- | --- |
| Active implementation follow-up | active plan |
| Review finding follow-up | `review-resolution.md` |
| Change closeout follow-up | `explain-change.md` or `change.yaml` |
| Release follow-up | release report or release plan |
| Repeated lesson | `learn` |
| Architecture risk or open question | `project-map` risk/open-question note |
| Unowned cross-change future work | `docs/follow-ups.md`, only when needed |
| New direction or policy change | `proposal` |

`project-map` may identify risks and open questions, but it does not own deferred execution.

## Artifact-location source rank

`docs/workflows.md` is the project-local user-facing artifact-location map. It summarizes and customizes artifact placement; it does not replace the owning stage skill's placement contract.

The source rank is precedence when sources conflict, not mandatory read order. Skills should use the artifact-location map as a concise path index, while still obeying known higher-priority constraints.

When artifact placement conflicts, use this rank:

1. explicit user-provided path or change ID
2. active artifact metadata, active plan metadata, or active change metadata
3. approved project specs or schemas
4. `docs/workflows.md` artifact-location map
5. portable default path
6. block on ambiguity

An explicit user-provided path or change ID does not override a higher-priority governance, safety, schema, or security constraint.

If a conflict is discovered between this guide and a higher-priority source, the higher-priority source wins. Refresh this guide or report the stale artifact-location map before downstream reliance.

The workflow guide takes precedence only for artifact types it specifies. If this guide is present but silent for a particular artifact type, use the owning skill's portable default path before blocking on ambiguity.

## Customer-project portability

Public skills operate in customer-project mode by default.

Use project-local artifacts when present and relevant, such as `docs/workflows.md`, `rigorloop.yaml`, `rigorloop.lock`, `docs/changes/<change-id>/change.yaml`, local specs, local plans, local governance files, and local architecture records.

Do not require RigorLoop repository-internal `specs/`, `docs/`, `CONSTITUTION.md`, `AGENTS.md`, reports, or follow-up files in a customer project.

When local guidance is absent, use portable defaults where safe and block on ambiguity where no safe default exists.

## Artifact locations

The table defines default locations and owning skills.

This workflow guide summarizes and customizes artifact placement. It does not replace the owning stage skill's placement contract, and installed skills carry portable defaults for skill-only adopters.

It does not define full artifact schemas, required fields, lifecycle status values, or validation rules. For exact shapes, use the governing spec, schema, or reference for that artifact type.

If this project customizes artifact locations, update this table. Skills use rows in this table for the artifact types those rows specify, then fall back to portable defaults when this guide is silent for an artifact type.

| Artifact type | Default location | Owning skill |
| --- | --- | --- |
| Project vision | `VISION.md` | `vision` |
| Project map | `docs/project-map.md` | `project-map` |
| Workflow guide | `docs/workflows.md` | `workflow` |
| Follow-up register | `docs/follow-ups.md` | `workflow` |
| Examples | `docs/examples/` | none; examples are non-normative |
| Proposals | `docs/proposals/YYYY-MM-DD-slug.md` | `proposal` |
| Specs | `specs/slug.md` | `spec` |
| Test specs | `specs/slug.test.md` | `test-spec` |
| Architecture | `docs/architecture/` or project-configured architecture path | `architecture` |
| ADRs | `docs/adr/ADR-YYYYMMDD-slug.md` | `architecture` |
| Plans | `docs/plans/YYYY-MM-DD-slug.md` | `plan` |
| Plan index | `docs/plan.md` | `plan` / workflow bookkeeping |
| Plan archive | `docs/plan-archive.md` | lifecycle closeout / archive maintenance |
| Change root | `docs/changes/<change-id>/` | current change lifecycle |
| Change metadata | `docs/changes/<change-id>/change.yaml` | relevant stage / workflow |
| Formal review records | `docs/changes/<change-id>/reviews/<stage>-r<n>.md`; default location only; exact receipt/root rules are owned by the formal review recording contract | review skills |
| Review log | `docs/changes/<change-id>/review-log.md` | review skills |
| Review resolution | `docs/changes/<change-id>/review-resolution.md` when findings or blocking outcomes require disposition | `review-resolution` |
| Explain change | `docs/changes/<change-id>/explain-change.md` | `explain-change` |
| Verify report | `docs/changes/<change-id>/verify-report.md` when required | `verify` |
| Reports | `docs/reports/` | release / verify / measurement workflows |
| Adapter artifact metadata | `docs/reports/adapter-artifacts/releases/` | release workflow |

## Lifecycle Token-Cost Summaries

Lifecycle token-cost summaries are conditional diagnostic evidence, not a default artifact for every change.

- Path: `docs/reports/token-cost/lifecycle/<change-id>.md`.
- Required triggers: large workflow-governance change, release change, dynamic benchmark warning, broad-search incident, or explicit maintainer request.
- Trigger ownership stays with the active plan, test spec, review-resolution, release metadata, maintainer request, or reviewer judgment. Validators may check a summary that exists, but must not infer that an ordinary change needed one.
- Ordinary small feature, docs, proposal, and skill edits may omit the summary when no trigger applies.
- Summaries are warning-only and not a hard token gate, hard release gate, or CI blocker based on token totals.
- Before/after dynamic benchmark comparison and exact token telemetry are advisory unless a benchmark actually ran or a later accepted artifact requires them.
- Use bounded evidence: summarize broad searches, large command outputs, full-skill reads, repeated file reads, generated-output reads, review rounds, and validation runs rather than pasting raw logs.
- Route recommended follow-up through the active plan, review-resolution, learn, proposal, or the follow-up ownership surface.

## Change-Local Artifacts

- Manual skill invocations may omit `docs/changes/<change-id>/` when they are not used to claim complete workflow delivery.
- For non-trivial work, the baseline change-local pack is `docs/changes/<change-id>/change.yaml` plus durable Markdown reasoning.
- For new non-trivial work, the default durable reasoning artifact is `docs/changes/<change-id>/explain-change.md`.
- PR text remains the reviewer-facing summary surface; it does not replace required durable reasoning for non-trivial work.
- Standalone `review-resolution.md` and `verify-report.md` remain conditional and are added only when their governing workflow triggers apply.
- Detailed formal review files under `docs/changes/<change-id>/reviews/` are stage-neutral across proposal, spec, architecture, plan, and code review.
- Every supported formal lifecycle review creates durable review evidence or reports blocked recording. Clean formal reviews use a lightweight clean review receipt. Material review findings are always recorded. All material findings require detailed change-local review files.
- Direct or review-only requests remain isolated by default. Isolation stops handoff, not recording.
- If a detailed file is required before a change-local root exists, create the smallest initial review-record root first. Material findings require `change.yaml`, `review-log.md`, `review-resolution.md`, and `reviews/<stage>-r<n>.md`; no-material triggers require `change.yaml`, `review-log.md`, and `reviews/<stage>-r<n>.md` without an empty `review-resolution.md`.
- Clean required reviews with no material findings still create a clean review receipt or report blocked recording. A clean review receipt proves the review happened; it does not settle artifact lifecycle/status by itself.
- When material findings exist for a non-trivial change, use `docs/changes/<change-id>/review-resolution.md` and approved dispositions: `accepted`, `rejected`, `deferred`, `partially-accepted`, and `needs-decision`.
- `needs-decision` is not final. It keeps `review-resolution.md` at `Closeout status: open` and blocks `explain-change`, `verify`, and `pr` until an authorized owner resolves or explicitly defers it.
- `Closeout status: closed` means every material finding has a final disposition, `review-log.md` lists no open findings, and the required action, rationale, follow-up, and validation evidence records for that disposition exist.
- Keep PR and explain-change review summaries concise: summarize counts by disposition and link `review-resolution.md` instead of duplicating detailed review records.
- Approved legacy top-level artifacts under `docs/explain/` remain valid durable reasoning surfaces until they are migrated or retired.
- `docs/changes/0001-skill-validator/` is retained as a rich validator fixture and historical proof pack, not the universal minimum for every non-trivial change.

## Autoprogression

- Distinguish `workflow-managed` completion flows from isolated stage requests.
- In v1, workflow-managed autoprogression applies only to:
  - `proposal -> proposal-review`
  - `spec -> spec-review`
  - `architecture -> architecture-review` when that review stage is the next mandatory or triggered downstream step
  - standard workflow execution from `implement -> code-review -> review-resolution when triggered -> ci-maintenance when triggered -> explain-change -> verify -> pr`
- In workflow-managed standard workflow runs, `code-review` first emits a first-pass review record grounded in the actual diff, upstream artifacts, checklist coverage, and validation evidence before any review-driven fixes begin.
- In workflow-managed standard workflow milestone-based plans, first-pass `clean-with-notes` on a non-final implementation milestone closes the reviewed milestone and continues to the next in-scope implementation milestone.
- In workflow-managed standard workflow milestone-based plans, first-pass `clean-with-notes` on the final implementation milestone reaches final closeout only when no in-scope implementation milestone remains open or unresolved.
- In workflow-managed standard workflow runs, first-pass `changes-requested` continues to `review-resolution`, and first-pass `blocked` or `inconclusive` stops.
- If the active plan does not clearly identify the reviewed milestone or remaining in-scope implementation milestones, stop for a plan update or inconclusive review instead of inferring final-closeout readiness.
- Clean reviews require checklist coverage plus no-finding rationale. Positive notes are optional and only useful when they add specific evidence-backed context.
- Direct `pr` remains in scope and opens the PR when readiness passes.
- Direct `proposal-review`, `spec-review`, `architecture-review`, `code-review`, `verify`, and `explain-change` stay isolated by default unless the user asks to carry the change through completion.
- Manual skill invocations and bugfix skill invocations stay isolated or explicit-step in v1.
- On-demand and periodic actions such as `explore`, `research`, and `learn` do not auto-run by default.
- Stop automatic continuation when the user explicitly pauses, validation fails, a review or design issue needs a real decision, permissions or tooling block the next step, or the next action would be stronger than PR creation such as merge, release, deploy, or destructive Git operations.
- Autoprogression does not replace lifecycle bookkeeping. After `code-review`, `verify`, or other review gates change the real initiative state, update the active plan, any affected active test spec, and `docs/plan.md` before claiming downstream readiness.
- Repo-local lifecycle synchronization happens inside the PR that performs the lifecycle transition, before that PR opens for review. Merge integrates pre-validated state; it is not a routine trigger for further lifecycle closeout.

## Planned Milestone Work

- Use a concrete plan under `docs/plans/` for multi-file, risky, ambiguous, migration-heavy, or milestone-based work.
- `docs/plan.md` is the bounded lifecycle index for planned initiatives; concrete plan bodies live under `docs/plans/`.
- Keep Active and Blocked complete and first in `docs/plan.md`; keep only the recent completed window in `Done (recent)` and move older terminal history to `docs/plan-archive.md`.
- Plan bodies use the explicit `## Status` lifecycle marker fields `Plan lifecycle state` and `Terminal disposition`; do not infer terminal state from prose.
- Superseded entries remain in `docs/plan.md` only while they carry `superseded by:` and non-empty `active-context:`; terminal superseded history without active context belongs in `docs/plan-archive.md`.
- For planned initiatives, the active plan `Current Handoff Summary` is the live state owner.
- `Readiness` points to `Current Handoff Summary` for current live state instead of duplicating the current next stage.
- Each implementation milestone has one `Milestone state`: `planned`, `implementing`, `review-requested`, `resolution-needed`, or `closed`.
- Use `review-requested` after implementation and targeted validation are complete and the milestone is handed to `code-review`.
- Use `resolution-needed` when review findings require review-resolution, fixes, owner decision, or re-review.
- Track the current milestone, current milestone state, last reviewed milestone, review status, remaining in-scope implementation milestones, next stage, final closeout readiness, and the reason in `Current Handoff Summary`.
- State-sync checks update affected state owners before downstream readiness is claimed.
- State-sync checks update `Current Handoff Summary`, milestone state, review-resolution closeout status when findings change, review-log open findings when formal review records change, `change.yaml` compact review/status when metadata changes, and `docs/plan.md` when plan lifecycle state changes.
- Change metadata, review-resolution, review-log, explain-change, verify output, and PR handoff own scoped evidence; they do not own the active plan's current next stage.
- Remove or correct stale live next-stage wording in touched artifacts before claiming downstream readiness.
- Use `lifecycle-closeout` for a milestone or section that tracks only downstream gates such as `ci-maintenance`, `explain-change`, `verify`, PR handoff, release, deploy, or final plan closeout.
- During execution, `implement` keeps the active plan body's progress, decisions, discoveries, and validation notes current.
- When a planned initiative changes lifecycle state, final lifecycle closeout updates both `docs/plan.md` and the plan body.
- If a PR completes a planned initiative, move it to `Done (recent)` or `docs/plan-archive.md` as the recent window requires, and update the plan body before opening the PR for review.
- If completion depends on a true downstream event such as release, deploy, package publication, external migration, or an observed hosted result, keep the plan `Active` and name the downstream event or follow-up condition.
- Do not use merge itself as a routine downstream completion event.
- `verify` blocks PR readiness when stale lifecycle state remains between the plan index and the plan body.
- Execution plans follow the illustrative structure in `docs/examples/plans/example-plan.md`; examples under `docs/examples/` are not active lifecycle state.
- Each completed planned milestone ends with a coherent commit using:
  - `M<n>: <completed milestone outcome>`
- A pull request may contain one or more completed milestone commits when that is the clearest review boundary.
- Before opening or repairing a PR, compare the head branch against the current base branch. If the branch already backed a merged PR or drags already-merged history into the diff, create a fresh branch from the current base and cherry-pick or restack only the intended commits before final validation and PR creation.

## Artifact Lifecycle

Lifecycle-managed top-level artifacts keep their own tracked status. Do not treat PR state, branch state, or chat-only review outcomes as a replacement for artifact-local lifecycle state.

| Artifact | Settlement states | Closeout or terminal states |
| --- | --- | --- |
| Proposal | `accepted` | `rejected`, `abandoned`, `superseded`, `archived` |
| Spec | `approved` | `abandoned`, `superseded`, `archived` |
| Architecture | `approved` | `abandoned`, `superseded`, `archived` |
| Test spec | `active` | `abandoned`, `superseded`, `archived` |
| ADR | `accepted`, `active` | `deprecated`, `superseded`, `archived`, `abandoned` |

Notes:

- `reviewed` is transitional review output, not a durable relied-on state for proposals, top-level specs, test specs, or architecture docs.
- `accepted`, `approved`, and `active` are settlement states. `done`, `deprecated`, `rejected`, `abandoned`, `superseded`, and `archived` are closeout or terminal states.
- Keep `Next artifacts` as planning history while an artifact is active. Use `Follow-on artifacts` or `Closeout` for actual downstream artifacts or final disposition. If a `Follow-on artifacts` section appears before real follow-ons exist, it must say `None yet`.
- `superseded` artifacts must identify their replacement with `superseded_by` or equivalent labeled text. `archived` artifacts do not require a replacement pointer.
- `verify` blocks on stale lifecycle-managed artifacts that are touched, referenced, generated, or authoritative for the changed area, and it warns on unrelated stale baseline artifacts.
- Draft PR-body references participate in `verify` only when draft PR text already exists. Before that, `verify` uses `docs/changes/<change-id>/change.yaml`, explain-change artifacts, the active plan, and other touched or referenced authoritative artifacts.
- Broader repo-local lifecycle inconsistency blocks `branch-ready` when the inconsistent artifact is touched, referenced, generated, or authoritative for the changed area.
- Tracked wording that defers lifecycle state to later repository integration should be treated as a reviewer-attention warning unless it is corrected, classified as a true downstream event, or made blocking by a lifecycle inconsistency.

## Source Of Truth

- Edit canonical workflow content in:
  - `docs/`
  - `specs/`
  - `skills/`
  - `schemas/`
  - `scripts/`
  - `templates/`
- Do not hand-edit generated public adapter packages in:
  - `dist/adapters/`
- `skills/` is the only authored skill source.
- `.codex/skills/` is ignored local Codex runtime state. Keep `.codex/skills/` untracked when copying installed Codex adapter skills there for local runtime use, and edit canonical skills under `skills/`.
- Public adapter installation uses `dist/adapters/README.md` as the install-contract surface. For `v0.1.3` and later, generated public adapter skill bodies are release archives, not tracked source under `dist/adapters/`.
- `dist/adapters/README.md` and `dist/adapters/manifest.yaml` are the tracked adapter support surface. Historical note: `v0.1.2` kept repository-tree adapter packages during the compatibility window.
- Public-surface token-cost benchmarks must use generated public adapter output or release archive output. They must not use `.codex/skills/`, which is repository-local runtime output.
- Use `docs/examples/plans/example-plan.md` for illustrative plan structure. Do not treat `docs/examples/**` as active lifecycle state or reintroduce a second plan-template path.

## Validation

Use selector-selected targeted proof as the first validation layer for non-trivial work when the changed paths are known:

- Inspect selection without running checks: `python scripts/select-validation.py --mode explicit --path <path>...`
- Execute targeted proof through the wrapper: `bash scripts/ci.sh --mode explicit --path <path>...`
- Examples of stable selected-check IDs are `skills.validate`, `review_artifacts.validate`, and `artifact_lifecycle.validate`.

`scripts/ci.sh` is the execution wrapper for selected checks. It does not imply broad smoke for every PR.

Use broad smoke only when an authoritative trigger requires it, such as selector mode `main`, selector mode `release`, an explicit `--broad-smoke` request, active plan field `broad_smoke_required: true`, test-spec requirement, review-resolution requirement, or release metadata. The selected check ID for repository broad smoke is `broad_smoke.repo`, and the direct command is:

```bash
bash scripts/ci.sh --mode broad-smoke
```

Validation owner surfaces:

- `docs/workflows.md` owns contributor-facing validation guidance.
- Validation-selection scripts, selector tests, and the CI wrapper own executable check selection, selected-check behavior, command exit behavior, and failure detection.
- Stage skills own concise local validation reminders when a stage directly needs one; they do not replace selected checks.
- Active plans and test specs own change-specific validation requirements.
- `review-resolution.md` owns finding-specific validation requirements.
- Release metadata owns release-specific validation requirements.

Guidance-only wording must not change selected check coverage, command exit behavior, failure detection, or required validation evidence.

Run these structural checks before PR:

- `python scripts/validate-skills.py`
- `python scripts/test-skill-validator.py`
- `python scripts/build-skills.py --check`
- `python scripts/test-adapter-distribution.py`
- `python scripts/build-adapters.py --version v0.1.3 --output-dir <release-output-dir>`
- `python scripts/validate-adapters.py --root <release-output-dir> --version v0.1.3`
- `python scripts/validate-token-cost-report.py docs/reports/token-cost/releases/v0.1.1.yaml`
- `python scripts/validate-release.py --version v0.1.1`
- `python scripts/test-artifact-lifecycle-validator.py`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path <repo-path> [...]`

Use `bash scripts/ci.sh` with an explicit mode to run checks through the repository-owned CI wrapper and report the commands you actually ran. Hosted PR CI uses `--mode pr --base <sha> --head <sha>`, main CI uses `--mode main --base <sha> --head <sha>`, and release automation uses release-specific validation. No-argument `bash scripts/ci.sh` remains legacy broad smoke, not the normal first proof step.

Selected-check execution supports bounded local parallelism. Use `--jobs <N>` to cap concurrent reviewed parallel-safe checks; when omitted, the wrapper uses available CPU count minus one with a floor of one. Use `--jobs 1` for explicit sequential execution when debugging races or reducing local resource pressure. Use `--timeout <seconds>` to override the 60-second per-check timeout, `--fail-fast` to stop launching queued checks after an observed failure while preserving already-started check results, and `--verbose` to include successful check output in stable order.

Ordinary contributors do not need all supported tools installed locally for non-smoke validation. Repository-owned checks validate generated package structure, drift, manifests, release metadata, and security without invoking Codex, Claude Code, or opencode.

Reserve `python scripts/validate-artifact-lifecycle.py --mode local` for clean worktrees only. When unrelated drafts, untracked files, or other local-only changes are present, use `--mode explicit-paths`, the diff-derived CI modes, or `bash scripts/ci.sh` instead of treating `local` mode as milestone proof.

When a change updates canonical `skills/`, use `python scripts/build-skills.py --check` to validate generated local mirror temp output. Do not treat generated `.codex/skills/*` files as authored lifecycle-managed inputs for explicit-path artifact validation.

## CI And Release

- `.github/workflows/ci.yml` should remain a thin wrapper around repo-owned validation commands. It may set up required tooling and pass explicit diff inputs, but validation logic belongs in `scripts/ci.sh`.
- The hosted CI workflow stays matrix-free in this first bounded-parallelism slice. Future hosted fan-out, if approved later, should consume stable check IDs from repository-owned scripts instead of duplicating selector path classification or hardcoded selected-check lists in workflow YAML.
- `scripts/release-verify.sh` is the repository-owned release gate for `v0.1.0-rc.1`, `v0.1.0`, and `v0.1.1`. It accepts a tag argument or `GITHUB_REF_NAME`, checks generated adapters and release metadata, consumes tracked release notes from `docs/releases/<tag>/release-notes.md`, and validates the `v0.1.1` Token-Friendliness report metadata.
- RC releases may be published before full manual smoke only when non-smoke gates pass and no smoke row records `fail`. Stable releases require passing Codex, Claude Code, and opencode smoke rows.

## Documentation Ownership

- `README.md`: public project overview
- `docs/workflows.md`: operational workflow summary
- `docs/plan.md`: bounded index of active, blocked, recent done, and active supersession context
- `docs/plan-archive.md`: older terminal plan history
- `docs/plans/*.md`: concrete execution plans
- `specs/*.md`: normative behavior contract
- `specs/*.test.md`: contract-to-test mapping
- `templates/*.md`: canonical scaffolds for workflow artifacts
