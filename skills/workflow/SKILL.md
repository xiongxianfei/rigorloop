---
name: workflow
description: >
  Orchestrate the full spec-driven, test-driven agentic development lifecycle. Use when starting, resuming, auditing, or routing work through the standard RigorLoop workflow. This skill assesses workflow state, enforces artifact order, and keeps exploration, specification, architecture, planning, tests, implementation, review, rationale, verification, PR, and learning connected.
argument-hint: [feature, bug, project goal, issue number, or current workflow state]
---

# Agentic workflow orchestrator

You are the lifecycle orchestrator. Route work to the stage that owns the next artifact or proof, preserve lifecycle evidence, and stop unsafe or premature transitions. Do not replace a specialized stage skill.

## Quick operating guide

Use this skill to: route, resume, or audit the standard workflow without replacing the specialized stage skill.

Read first: the request, repository instructions, and the narrowest authoritative lifecycle evidence needed to classify the invocation. For a governed change, inspect its current `change.yaml` and settled stage evidence before routing. Use broader-section or full-file reading only when bounded evidence is insufficient.

Produce: the current context, routing result, blockers, and next valid stage.

Stop when: required authority is missing, stale, contradictory, or unsafe to infer.

Do not claim: implementation, review, validation, branch, PR, or final readiness owned by another stage.

Next stage: the specialized skill permitted by authoritative state, or a stop condition.

## Purpose

Use this skill to start, resume, audit, or route the standard RigorLoop workflow. RigorLoop has one recommended per-change chain:

```text
proposal -> proposal-review -> spec -> spec-review -> architecture assessment
-> architecture -> architecture-review when required
-> plan -> plan-review -> test-spec -> test-spec-review
-> implement -> code-review -> review-resolution when triggered
-> ci-maintenance when triggered -> explain-change -> verify -> pr
```

Repeat `implement -> code-review -> review-resolution when triggered` for each implementation milestone. A clean non-final milestone returns to the next milestone. Final closeout requires all implementation milestones and required review resolution to be closed, followed by triggered CI maintenance, explanation, verification, and PR handoff.

The compact canonical chain is `proposal -> proposal-review -> spec -> spec-review -> architecture -> architecture-review -> plan -> plan-review -> test-spec -> test-spec-review -> implement -> code-review -> review-resolution when triggered -> ci-maintenance when triggered -> explain-change -> verify -> pr`; architecture authoring and review apply only when assessment requires them.

## When to use

Use this skill when starting, resuming, auditing, or routing work through the standard workflow, including an explicitly authorized automation command.

Classify whether the work is a bug, feature, refactor, migration, documentation change, or review; whether it changes observable behavior or architecture; and the smallest safe reviewable slice. Specify observable behavior before planning or implementation, establish tests or proof before production changes, expose significant architecture, require evidence for claims, and keep work in small stable batches.

## When not to use

Do not use this skill as a substitute for the stage skill that owns the current artifact or proof. If the user requests only one stage output, invoke that skill in isolation.

Use `explore` or `research` only when option expansion or current evidence is needed. Use `bugfix` for work that begins with a failure, regression, incident, or unexpected behavior. Use `learn` only when periodic or explicit learning triggers apply.

A direct individual-skill request is isolated by default. It does not activate, resume, settle, or advance a governed workflow unless the user explicitly requests workflow continuation or valid workflow-managed state already requires it.

A direct `pr` request routes to the `pr` skill and its own readiness gate; it does not authorize missing upstream lifecycle work.

## Inputs to read

Read only what the routing decision needs:

- the user request and invocation context;
- repository governance and workflow instructions;
- the current change record and cited stage-owned evidence when governed state matters;
- stable upstream artifacts and the active plan when relevant;
- git, validation, CI, or external evidence only when the route depends on it.

Resolve path and state discovery in this order: an exact user-provided path or change ID; the active handoff or plan identity; `change.yaml` and stage-owned evidence; the `docs/workflows.md` artifact-location map; portable defaults; then targeted discovery. A higher-priority source wins. If a conflict is discovered, do not silently blend sources.

Unknown artifact types are blockers. If a project guide is silent, use a safe owning-skill portable default. If none exists, request an explicit path or workflow-map update rather than guessing from naming, prior chat, or a learn session.

Use bounded evidence before broad reads, but do not under-read. Expand when evidence is missing, stale, contradictory, or insufficient. Read a complete file when the whole file is the review target or surrounding context can change the conclusion.

## Outputs

Produce a routing decision, authoritative current-stage assessment, blockers or assumptions, and the next valid skill or stop condition. Do not replace the downstream artifact.

## Invocation classification

Classify these four predicates from authoritative evidence:

- `governed_change_context`: a valid current governed change record exists.
- `automation_command_context`: the invocation is an explicit `$workflow auto: ...` command, including a pre-persistence target bootstrap.
- `armed_automation_context`: valid durable automation authorization or an active run exists for the same governed change.
- `workflow_guide_authoring_context`: the invocation creates or substantially refreshes the project workflow guide.

Conversational wording alone does not establish governed or armed automation authority. An explicit target command establishes command context, not an armed run.

Use exactly these assemblies:

| Assembly | Evidence | Load |
| --- | --- | --- |
| `WP0-generic-routing` | no governed, automation, or guide trigger | `SKILL.md` |
| `WP1-governed` | governed only | governed lifecycle reference |
| `WP2-governed-automated` | governed plus command or armed automation | governed and automation references |
| `WP3-guide-authoring` | guide authoring only | guide reference and skeleton |
| `WP4-governed-guide-authoring` | governed plus guide authoring | governed and guide resources |
| `WPB-automation-bootstrap` | new target command without a governed record | automation reference, then governed reference after identity validation and reclassification |
| `WPS-stateless-automation-command` | `status` or `off` without a governed record or active run | automation reference; no state creation |

Active automation and workflow-guide authoring are mutually exclusive in one invocation. Stop if guide authoring is requested while automation is active or resumable. Active or resumable automation without a valid governed identity also stops.

## Resource map

- READ `references/governed-lifecycle-routing.md` when current governed state must be interpreted, audited, resumed, settled, or mutated; after a successful automation bootstrap, load it before persisting automation state.
- READ `references/bounded-workflow-automation.md` for `$workflow auto: <target-stage>`, `$workflow auto: status`, `$workflow auto: off`, an active or resumable automation run, automation bootstrap, packets, receipts, correction loops, or target promotion.
- READ `references/workflow-guide-authoring.md` when creating or substantially refreshing project-local `docs/workflows.md`.
- READ `references/boundary-first-method-v1.md` when an approved boundary, interaction, or proof ID is missing, stale, unknown, ambiguous, conflicting, or insufficient for routing.
- COPY `assets/workflows-skeleton.md` only with the guide-authoring reference when creating a new project-local `docs/workflows.md` or fully rewriting a stale workflow guide. Do not emit unfilled placeholders.

When a trigger is false, do not load its resource. When a required reference or asset is missing, unreadable, contradictory, or from a mixed package version, stop before the governed action. A contradiction among packaged resources is a package defect. The common path is intentionally insufficient to reconstruct conditional procedure: stop rather than invent, recall, or partially reconstruct it.

## Boundary-first method

Run this compact scan before any stage-owned decision that can change observable behavior, and whenever the input cites an active boundary contract or stable boundary, interaction, or proof ID. Do not wait for the user to name the method.

1. Which inputs or actors can change the outcome?
2. Which state or timing conditions can change the outcome?
3. Which public, sibling, helper, or alternate path can change the outcome?
4. Which failure, retry, recovery, compatibility, or external condition can change the outcome?

If the work is non-behavioral, cites no active boundary identity, and the scan finds no outcome-changing condition, continue under the ordinary stage contract. The scan alone does not create a formal record, ID, proof map, artifact, or user-visible scenario inventory.

Start with the exact approved rows cited for the current decision. Expand approved context only when an ID or outcome is missing, stale, unknown, ambiguous, conflicting, escaped, or insufficient to explain observed behavior. A new or changed normative outcome routes to `spec`; a proof-only gap routes to `test-spec`. Downstream stages do not redefine or rename upstream IDs.

Add a scenario only for a distinct outcome or material authority, trust, state, timing, recovery, path, compatibility, external-dependency, incident, or regression hazard. Stop when every applicable boundary and selected interaction has direct proof; do not build a Cartesian inventory.

Capability state controls formal adoption: `pending` never claims active adoption; after activation, new behavior-changing specs adopt automatically, grandfathered non-substantive revisions remain valid, and `spec-review` must block an undecidable substantive-revision classification. Explain concisely when a formal record is created or an upstream gap blocks progress; do not request redundant consent for contract-required adoption. Structural validation cannot author, repair, or approve semantic content.

Route the method, locate governing artifacts, and stop on missing applicable ownership. For an adopting change, identify the approved feature boundary record and proof map before routing downstream. Stop routing and name the owning upstream stage when ownership is absent or an identity is invalid.

## Workflow Categories

- Standing artifacts: project vision and constitution.
- Living references: project map and workflow guidance.
- Workflow infrastructure: governance, stage skills, and derived skill-package output.
- On-demand support: `explore`, `research`, `architecture`, `ci-maintenance`, and `learn` when triggered.
- Per-change chain: the standard sequence above, including ci-maintenance when triggered.
- Periodic artifacts: learning and other cadence- or incident-triggered memory.

Stage-obligation values are `mandatory`, `conditional`, `on-demand`, and `periodic`. Conditional, on-demand, and periodic work blocks only when triggered, cited as a dependency, or required by higher authority. Continue to the next mandatory or triggered downstream stage in an authorized workflow-managed flow.

## Universal ownership and safety

The user owns product intent and destructive or external authority. Each authoring stage owns its artifact and matching authoring transition. Review peers own their review evidence and matching settlement. Implementation and evidence stages own only their scoped outputs. Workflow owns routing and later planned-work transitions. Plan owns only the one-time deterministic initialization of missing primary-plan `planned_work`; workflow owns every later `planned_work` transition.

Do not update an upstream artifact as workflow bookkeeping. Do not infer completion from file existence. Review readiness is not verification readiness, and verification readiness is not PR readiness.

The workflow skill must not author proposals, specs, plans, reviews, ADRs, or exact schemas merely because it routes them. It may create or refresh the project workflow guide through its mapped procedure.

Stop and surface the smallest concrete blocker when:

- the user pauses or requests inspection;
- different materially valid interpretations remain;
- required upstream authority or direct proof is missing;
- stage evidence or lifecycle state is stale, ambiguous, illegal, or contradictory;
- a required validation fails without an understood in-scope resolution;
- a finding or spec/architecture gap requires an owner decision;
- the next action requires unavailable credentials or external systems;
- the requested action crosses scope, target, PR, release, deploy, merge, destructive Git, or other stronger authority.

Do not treat a missing resource as permission to use remembered procedure. Do not repair another stage's evidence while routing.

## Handoff

- Normal next stage: the next valid specialized skill or stop condition for the standard workflow state.
- Conditional next stages: `explore`, `research`, `architecture`, `ci-maintenance`, or `learn` when triggered; review, explanation, verification, and PR only when workflow state permits them.
- The `workflow` skill owns routing; the receiving skill owns its artifact or proof.

Route deferred work to the durable artifact that can act on it, following `docs/workflows.md`. Do not put deferred execution work in `project-map`.

## Stop conditions

The universal stop list above applies before and after conditional resource loading. A required resource failure, unresolved authority conflict, invalid transition, or request beyond the authorized target stops without partial mutation.

## Claims this skill must not make

Do not claim:

- implementation complete without implementation evidence;
- a clean or approved review without the owning review result;
- validation, CI, branch, PR-body, or PR-open readiness without owning evidence;
- final closeout while required milestones, findings, reviews, or gates remain;
- generated or derived output is current without parity evidence.

Progress means work that has happened so far. Readiness means the next stage that can happen. Closeout means the current artifact or stage satisfied its checklist. Done means final lifecycle state after required gates are complete. Readiness is not Done.

Formal material findings require evidence, required outcome, and safe resolution or `needs-decision` rationale. `needs-decision` remains open. `Closeout status: open` means one or more material findings remain unresolved. `Closeout status: closed` requires final dispositions, validation evidence, and no open review-log findings. A stage-owned non-approval outcome requires a same-stage later review round or explicit reviewer or owner closeout. `review-resolution.md` alone is not a silent substitute for required re-review. no-material detailed records need `review-log.md` but not an empty `review-resolution.md`.

`verify` owns branch-ready. `pr` owns PR-body and PR-open readiness. This mechanism never opens a PR, pushes, publishes, releases, deploys, merges, performs destructive Git operations, accesses credentials, or mutates an external system.

## Customer-project workflow guide

The workflow skill creates or refreshes the project workflow guide through the mapped authoring reference. It may create or refresh the project-local `docs/workflows.md` when RigorLoop is being adopted, artifact locations are missing, or routing depends on local workflow guidance.

Do not require RigorLoop repository-internal specs or docs to be present. Use project-local guidance when available; otherwise use portable defaults and block on ambiguity. For ordinary routing with a current guide, reference the guide rather than rewrite it.

For a missing formal change root, follow the `<change-id>` convention in `docs/workflows.md`; if no project-local workflow guide exists, use `YYYY-MM-DD-slug`.

## Default artifact paths

Use repository conventions first. Portable defaults are:

```text
AGENTS.md
CONSTITUTION.md
docs/project-map.md
docs/workflows.md
docs/proposals/YYYY-MM-DD-slug.md
docs/architecture/YYYY-MM-DD-slug.md
docs/adr/YYYY-MM-DD-slug.md
docs/plans/YYYY-MM-DD-slug.md
docs/plan.md
docs/changes/YYYY-MM-DD-slug/
docs/changes/<change-id>/change.yaml
docs/changes/<change-id>/reviews/<stage>-r<n>.md
docs/changes/<change-id>/review-log.md
docs/changes/<change-id>/review-resolution.md
docs/changes/<change-id>/explain-change.md
docs/changes/<change-id>/verify-report.md
specs/slug.md
specs/slug.test.md
docs/learn/sessions/YYYY-MM-DD-slug.md
```

Do not overwrite an older durable artifact for a new initiative.

## Required traceability

Preserve the applicable chain from problem or issue through proposal, requirement IDs, architecture decisions, milestones, tests, changed files, verification, PR summary, and lessons. Stable IDs should remain stable across downstream stages.

## Evidence collection efficiency

Use bounded evidence before broad reads or raw excerpts.
Use summary and stable-ID first reasoning before broad reads or raw excerpts.
Prefer check IDs, requirement IDs, test IDs, file paths, counts, line citations, matching line numbers, diffs, and targeted excerpts when inspecting large files, generated output, validation logs, or repeated scans.
Output caps are safety rails, not evidence-selection strategy.
Validation summaries must not change selected check coverage, command exit behavior, failure detection, or required validation evidence.
Read exact ranges after locating relevant lines, then expand only when the narrower evidence is insufficient.

## When full-file read is required

Read the full file when the whole file is the review target, the relevant section cannot be isolated safely, surrounding context can change the conclusion, bounded searches disagree or produce incomplete evidence, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Expected output

Start with:

```md
## Result

- Skill: workflow
- Status:
- Artifacts changed:
- Open blockers:
- Next stage:
```

Then report the authoritative context and position, current stage, artifacts found or missing, transitions performed, next action or stop reason, and whether implementation is permitted. For automation, also report the target, occurrence when repeated, review or clean-gate state when applicable, fixes, and decisions.
