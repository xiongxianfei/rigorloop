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
  - `proposal -> proposal-review -> spec -> spec-review -> architecture -> architecture-review -> plan -> plan-review -> test-spec -> test-spec-review -> implement -> code-review -> review-resolution when triggered -> ci-maintenance when triggered -> explain-change -> verify -> pr`
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
- Formal workflow-managed test specs route from `test-spec` to `test-spec-review` before `implement`; the test spec remains `active`, and approval lives in the review record.
- `implement` requires the active test spec plus a current approved `test-spec-review` with no open material findings when a formal workflow-managed test spec is required.
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

Unknown artifact types are not placed by naming convention. If an artifact type is absent from this guide and no owning skill has a safe portable default, block and request a workflow-map update or explicit path.

## Guide ownership

Each guide should answer one kind of question. This table routes users to the
primary live surface without making orientation guides duplicate specs, schemas,
or stage-skill contracts.

| Question | Primary guide | Secondary source | Owner |
| --- | --- | --- | --- |
| Why does this project exist? | `VISION.md` | README summary | `vision` / proposal |
| What rules govern source of truth? | `CONSTITUTION.md` | this workflow guide summary | constitution |
| Where does an artifact go? | this workflow guide | owning stage skill portable default | `workflow` |
| What does this repo contain? | `docs/project-map.md` | README links | `project-map` |
| What work is active? | `docs/plan.md` | active plan body | `plan` / workflow bookkeeping |
| What happened in one change? | `docs/changes/<change-id>/` | `docs/plan.md` index entry | relevant stage skills |
| How do I perform one stage? | `skills/<stage>/SKILL.md` | this workflow guide | owning stage skill |
| Why did a rule change? | proposal, spec, or learn session | promoted live guide or contract | proposal / learn / owning stage |

Learn sessions explain historical rationale. They are not live routing authority
unless the rule also appears in this guide, an approved spec, a schema, or an
owning stage skill.

## Customer-project portability

Public skills operate in customer-project mode by default.

Use project-local artifacts when present and relevant, such as `docs/workflows.md`, `rigorloop.yaml`, `rigorloop.lock`, `docs/changes/<change-id>/change.yaml`, local specs, local plans, local governance files, and local architecture records.

Do not require RigorLoop repository-internal `specs/`, `docs/`, `CONSTITUTION.md`, `AGENTS.md`, reports, or follow-up files in a customer project.

When local guidance is absent, use portable defaults where safe and block on ambiguity where no safe default exists.

## Artifact registry

The following canonical fenced YAML artifact registry is the machine-checkable source of truth for project-local workflow-managed artifact placement. Markdown tables in this guide are human-readable projections of this registry and must not contradict it.

```yaml
artifact_locations:
  project_vision:
    owner: vision
    path: VISION.md
    required_when: project vision exists or is being bootstrapped
  project_map:
    owner: project-map
    path: docs/project-map.md
    required_when: architecture or repository orientation depends on it
  workflow_guide:
    owner: workflow
    path: docs/workflows.md
    required_when: RigorLoop is adopted or artifact locations change
  follow_up_register:
    owner: workflow
    path: docs/follow-ups.md
    required_when: unowned cross-change follow-up exists
  examples:
    owner: none
    path: docs/examples/
    required_when: illustrative examples are maintained
  proposal:
    owner: proposal
    path: docs/proposals/YYYY-MM-DD-slug.md
    required_when: proposal stage
  spec:
    owner: spec
    path: specs/slug.md
    required_when: spec stage
  test_spec:
    owner: test-spec
    path: specs/slug.test.md
    required_when: test-spec stage
  architecture_record:
    owner: architecture
    path: docs/architecture/YYYY-MM-DD-slug.md
    required_when: architecture stage is triggered
  adr:
    owner: architecture
    path: docs/adr/ADR-YYYYMMDD-slug.md
    required_when: durable architecture decision is recorded
  plan_index:
    owner: plan / workflow
    path: docs/plan.md
    required_when: planned initiatives exist
  change_plan:
    owner: plan
    path: docs/plans/YYYY-MM-DD-slug.md
    required_when: planned initiative
  plan_archive:
    owner: lifecycle closeout
    path: docs/plan-archive.md
    required_when: terminal plan history exceeds recent index window
  change_root:
    owner: current change lifecycle
    path: docs/changes/<change-id>/
    required_when: workflow-managed formal lifecycle evidence exists
  change_metadata:
    owner: relevant stage / workflow
    path: docs/changes/<change-id>/change.yaml
    required_when: non-trivial workflow-managed change
  formal_review_record:
    owner: review skills
    path: docs/changes/<change-id>/reviews/<stage>-r<n>.md
    required_when: formal lifecycle review
  review_log:
    owner: review skills
    path: docs/changes/<change-id>/review-log.md
    required_when: formal lifecycle review
  review_resolution:
    owner: review-resolution
    path: docs/changes/<change-id>/review-resolution.md
    required_when: material findings, blocking outcomes, accepted dispositions, or another governing trigger
  explain_change:
    owner: explain-change
    path: docs/changes/<change-id>/explain-change.md
    required_when: final rationale for non-trivial change
  verify_report:
    owner: verify
    path: docs/changes/<change-id>/verify-report.md
    required_when: verify stage requires a standalone report
  pr_handoff:
    owner: pr
    external_surface: pull_request_body
    required_when: pr stage
  learn_session:
    owner: learn
    path: docs/learn/sessions/YYYY-MM-DD-slug.md
    required_when: learn session reaches Frame
  token_cost_summary:
    owner: workflow / measurement
    path: docs/reports/token-cost/lifecycle/<change-id>.md
    required_when: token-cost summary trigger applies
  adapter_artifact_metadata:
    owner: release workflow
    path: docs/reports/adapter-artifacts/releases/
    required_when: adapter artifact metadata is produced
```

## Artifact locations

The table defines default locations and owning skills. It is the human-readable artifact-location map projection of the canonical registry above.

This workflow guide routes project-local artifact placement. Stage skills own artifact content, do not lose their placement contracts here, and carry portable defaults for skill-only adopters.

It does not define full artifact schemas, required fields, lifecycle status values, or validation rules. For exact shapes, use the governing spec, schema, or reference for that artifact type.

If this project customizes artifact locations, update the registry and this table together. Skills use rows in this table for the artifact types those rows specify, then fall back to portable defaults when this guide is silent for an artifact type.

| Artifact type | Default location | Owning skill | Required when |
| --- | --- | --- | --- |
| Project vision | `VISION.md` | `vision` | Project vision exists or is being bootstrapped. |
| Project map | `docs/project-map.md` | `project-map` | Architecture or repository orientation depends on it. |
| Workflow guide | `docs/workflows.md` | `workflow` | RigorLoop is adopted or artifact locations change. |
| Follow-up register | `docs/follow-ups.md` | `workflow` | Unowned cross-change follow-up exists. |
| Examples | `docs/examples/` | none; examples are non-normative | Illustrative examples are maintained. |
| Proposals | `docs/proposals/YYYY-MM-DD-slug.md` | `proposal` | Proposal stage. |
| Specs | `specs/slug.md` | `spec` | Spec stage. |
| Test specs | `specs/slug.test.md` | `test-spec` | Test-spec stage. |
| Architecture | `docs/architecture/YYYY-MM-DD-slug.md` | `architecture` | Architecture stage is triggered. |
| ADRs | `docs/adr/ADR-YYYYMMDD-slug.md` | `architecture` | Durable architecture decision is recorded. |
| Plan index | `docs/plan.md` | `plan` / workflow bookkeeping | Planned initiatives exist. |
| Plans | `docs/plans/YYYY-MM-DD-slug.md` | `plan` | Planned initiative. |
| Plan archive | `docs/plan-archive.md` | lifecycle closeout / archive maintenance | Terminal plan history exceeds recent index window. |
| Change root | `docs/changes/<change-id>/` | current change lifecycle | Workflow-managed formal lifecycle evidence exists. |
| Change metadata | `docs/changes/<change-id>/change.yaml` | relevant stage / workflow | Non-trivial workflow-managed change. |
| Formal review records | `docs/changes/<change-id>/reviews/<stage>-r<n>.md`; default location only; exact receipt/root rules are owned by the formal review recording contract | review skills | Formal lifecycle review. |
| Review log | `docs/changes/<change-id>/review-log.md` | review skills | Formal lifecycle review. |
| Review resolution | `docs/changes/<change-id>/review-resolution.md` when findings or blocking outcomes require disposition | `review-resolution` | Material findings, blocking outcomes, accepted dispositions, or another governing trigger. |
| Explain change | `docs/changes/<change-id>/explain-change.md` | `explain-change` | Final rationale for non-trivial change. |
| Verify report | `docs/changes/<change-id>/verify-report.md` when required | `verify` | Verify stage requires a standalone report. |
| PR handoff | Pull request body | `pr` | PR stage. |
| Learn session | `docs/learn/sessions/YYYY-MM-DD-slug.md` | `learn` | Learn session reaches Frame. |
| Reports | `docs/reports/` | release / verify / measurement workflows | Report-producing workflow is triggered. |
| Adapter artifact metadata | `docs/reports/adapter-artifacts/releases/` | release workflow | Adapter artifact metadata is produced. |

## Review record placement

| Review type | Path | Creates review-log entry? | Creates review-resolution? |
| --- | --- | --- | --- |
| Proposal review | `docs/changes/<change-id>/reviews/proposal-review-r<n>.md` | yes | Only when material findings, blocking outcomes, accepted dispositions, or another governing trigger require it. |
| Spec review | `docs/changes/<change-id>/reviews/spec-review-r<n>.md` | yes | Only when material findings, blocking outcomes, accepted dispositions, or another governing trigger require it. |
| Architecture review | `docs/changes/<change-id>/reviews/architecture-review-r<n>.md` | yes | Only when material findings, blocking outcomes, accepted dispositions, or another governing trigger require it. |
| Plan review | `docs/changes/<change-id>/reviews/plan-review-r<n>.md` | yes | Only when material findings, blocking outcomes, accepted dispositions, or another governing trigger require it. |
| Code review | `docs/changes/<change-id>/reviews/code-review-<milestone>-r<n>.md` | yes | Only when material findings, blocking outcomes, accepted dispositions, or another governing trigger require it. |

## Plan surfaces

| Surface | Path | Purpose |
| --- | --- | --- |
| Plan index | `docs/plan.md` | Bounded lifecycle index of active, blocked, recent done, and active supersession context. |
| Plan body | `docs/plans/YYYY-MM-DD-slug.md` | Concrete execution plan for one workflow-managed planned initiative. |
| Change metadata | `docs/changes/<change-id>/change.yaml` | Compact change metadata and validation ledger. |
| Change-local evidence | `docs/changes/<change-id>/` | Reviews, rationale, verification, PR handoff evidence, and other scoped lifecycle evidence. |

## Customization and migration notes

- The registry is the current project-local map; update it and the Markdown projections together when artifact placement changes.
- `docs/plan.md` remains the plan index. Concrete plan bodies remain under `docs/plans/`.
- Existing `docs/plans/*.md` files are not migrated by this workflow-map optimization.
- Formal review records stay under `docs/changes/<change-id>/reviews/` unless a higher-priority explicit path, active metadata, approved spec, schema, safety constraint, or user instruction permits another path.
- Learn sessions may explain historical decisions, but they are not live placement authority unless the current rule also appears in this guide, an approved spec, a schema, or owning stage-skill guidance.

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
- Change-local autoprogression profiles are off unless explicitly and durably authorized. The canonical policy record is `docs/changes/<change-id>/change.yaml` at `workflow.autoprogression`; `docs/changes/<change-id>/workflow-policy.yaml` is only a fallback when the change-metadata contract rejects policy data, and that fallback decision must be auditable.
- Profile policy records are authorization evidence only. They do not own current stage, next stage, review status, branch readiness, PR readiness, or active plan state.
- `authoring-through-plan-review` uses profile states `off`, `armed`, `active`, `paused`, and `completed`. Activation requires workflow-managed context, durable authorization, an armed profile, and a proposal gate ready from tracked artifacts.
- Proposal gate readiness is artifact/review readiness only; user authorization is checked separately as the armed profile state.
- When active, `authoring-through-plan-review` routes through `spec`, `spec-review`, recorded architecture assessment, conditional `architecture` and `architecture-review`, `plan`, and `plan-review`, then stops.
- Architecture assessment records `architecture-required`, `architecture-not-required`, or `architecture-ambiguous`; ambiguity pauses instead of guessing.
- Review stages inside `authoring-through-plan-review` remain independent formal reviews: reset to the tracked artifact, governing sources, formal criteria, and relevant recorded findings; record the result before downstream routing; do not rely on hidden authoring reasoning or edit the reviewed artifact during review.
- Stop or pause `authoring-through-plan-review` on non-clean reviews, material findings, `needs-decision`, user pause or cancellation, missing or malformed authorization persistence, contradictory workflow state, unreliable partial completion, exhausted transition budget, direct review-only invocation, or an out-of-scope stage request.
- Resume must use tracked artifact and review evidence. Do not recreate completed artifacts, rerun clean reviews without an explicit rereview event, or infer completion from file existence alone.
- Clean `plan-review` completes this profile and reports `test-spec` next without invoking `test-spec`, implementation, review-fix loops, verification, or PR.
- The bounded review-fix profile uses the command form `$workflow auto: <target-stage>` and persists authorization as `workflow.autoprogression.review_fix` with profile `bounded-review-fix`.
- `$workflow auto: status` reports current review-fix state without mutating artifacts.
- `$workflow auto: off` clears or terminally cancels review-fix authorization.
- Valid review-fix target stages are `proposal-review`, `spec`, `spec-review`, `architecture`, `architecture-review`, `plan`, `plan-review`, `test-spec`, and `test-spec-review`; unknown targets fail closed before routing.
- Review-fix activation requires workflow-managed context, durable user authorization, accepted proposal, approved recorded `proposal-review`, no open findings, closed resolution, clean current gate evidence, current review evidence, fresh artifact state, and unambiguous artifact placement.
- Direct review invocations do not activate, resume, or advance `bounded-review-fix`, even when persisted review-fix state exists.
- After approved recorded `spec-review`, review-fix routing requires exactly one architecture assessment: `architecture-required`, `architecture-not-required`, or `architecture-ambiguous`. `architecture-required` routes through `architecture` and `architecture-review`; `architecture-not-required` skips those conditional stages; `architecture-ambiguous` pauses for owner decision.
- If `architecture-not-required` skips a user-requested conditional target such as `architecture` or `architecture-review`, stop with `target-not-applicable` instead of claiming that target was reached.
- `bounded-review-fix` never routes past the requested target and never invokes `implement`, `code-review`, `verify`, `pr`, release, publication, network, destructive, or external-state operations.
- Review-fix never continues past the requested target and never invokes implementation, code-review, verify, PR, release, publication, network, destructive, or external-state operations.
- Review-fix chat results report mode, target stage, current stage, review status, auto-applied fixes, human decisions required, artifacts changed, review rerun status, next stage run, and stop reason.
- The implementation profile is verify-bounded implementation autoprogression.
- Existing `authoring-through-plan-review` and `implementation-through-verify` behavior remains unchanged unless a later approved spec explicitly changes those profiles.
- In v1, workflow-managed autoprogression applies only to:
  - `proposal -> proposal-review`
  - `proposal-review -> spec -> spec-review -> architecture assessment -> architecture/architecture-review when required -> plan -> plan-review -> stop`, only under the explicitly armed `authoring-through-plan-review` profile
  - `$workflow auto: <target-stage>` through the proposal-side path ending no later than `test-spec-review`, only under the explicitly armed `bounded-review-fix` profile
  - `spec -> spec-review`
  - `architecture -> architecture-review` when that review stage is the next mandatory or triggered downstream step
  - standard workflow execution from `implement -> code-review -> review-resolution when triggered -> ci-maintenance when triggered -> explain-change -> verify -> pr`
- In workflow-managed standard workflow runs, `code-review` first emits a first-pass review record grounded in the actual diff, upstream artifacts, checklist coverage, and validation evidence before any review-driven fixes begin.
- Workflow-managed automated `code-review` uses the independent adversarial review gate. The orchestrator creates the neutral review invocation manifest and initial packet before invoking review, and it withholds validation-result summaries, evidence menus, implementation notes, and prior finding content until the required phase receipts allow release.
- Workflow-managed automated `code-review` uses the requirement-fidelity gate when deterministic applicability is `applicable`.
- The requirement-fidelity gate is additive with the independent adversarial review gate; both receipts must pass when both contracts apply.
- Manual reviews may voluntarily apply the requirement-fidelity gate, but mandatory manual-review applicability classification is out of first-slice scope.
- A clean automated review may advance only after the normalized `review_gate_outcome`, independence manifest, phase receipts, clean receipt, risk-tier gates, unresolved-finding check, and second-review policy all pass.
- In workflow-managed standard workflow milestone-based plans, first-pass `clean-with-notes` on a non-final implementation milestone closes the reviewed milestone and continues to the next in-scope implementation milestone.
- In workflow-managed standard workflow milestone-based plans, first-pass `clean-with-notes` on the final implementation milestone reaches final closeout only when no in-scope implementation milestone remains open or unresolved.
- Before `explain-change` or `verify`, require final holistic code-review evidence covering the complete final diff and cross-milestone interactions.
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
- Run `python scripts/validate-artifact-lifecycle.py --mode explicit-paths` after stage-owned evidence is updated and before claiming `code-review`, `verify`, or PR handoff readiness.
- A failed state-sync gate blocks the next-stage handoff sentence until the agent either reverts its own in-progress owner/projection edits or records the failure as the current blocker with the rerun command.
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
