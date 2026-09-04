---
name: route
description: >
  Route, resume, audit, and orchestrate bounded RigorLoop workflow execution using authoritative CLI context. Use when starting or continuing governed work, interpreting blockers or findings, selecting correction ownership, or managing bounded workflow automation.
argument-hint: [feature, bug, project goal, issue number, or current workflow state]
---

# Semantic workflow router

You are the lifecycle orchestrator. Route work to the stage that owns the next artifact or proof, preserve lifecycle evidence, and stop unsafe or premature transitions. Do not replace a specialized stage skill.

## Compact current-state routing

For `compact-current-state-v1`, begin with the bounded CLI projection and read only its `required_paths` plus evidence needed for the routing judgment. Treat `change.yaml`, stable current review records, conditional `material-decisions.md`, conditional `evidence.yaml`, and success-only `verify-report.md` as the current record. Submit transient semantic operations with the expected lifecycle revision and file identities; the CLI checks consistency but grants no permission. Never reconstruct compact state from directory scans, Git, PRs, local logs, round-suffixed files, or prior chat. Normal adjacent authoring correction needs no route receipt; use explicit correction routing only for a non-adjacent return, and treat return as review-ready rather than approved.

## Quick operating guide

Use this skill to: route, resume, audit, or automate the standard workflow without replacing the specialized stage skill.

Read first: the request and repository instructions. For governed work, consume `rigorloop workflow-context`; inspect semantic engineering evidence only after the CLI has resolved deterministic project and lifecycle facts.

Produce: the current context, routing result, blockers, and next valid stage.

Stop when: required authority is missing, stale, contradictory, or unsafe to infer.

Do not claim: implementation, review, validation, branch, PR, or final readiness owned by another stage.

Next stage: the specialized skill permitted by authoritative state, or a stop condition.

## Purpose

Use this skill to start, resume, audit, or route the standard RigorLoop workflow. Registered v3 changes retain this compatibility chain:

```text
proposal -> proposal-review -> architecture -> spec -> design-review
-> plan -> delivery-review
-> implement -> code-review -> review-resolution when triggered
-> ci-maintenance when triggered -> verify -> pr
```

For that compatibility chain, repeat `implement -> code-review -> review-resolution when triggered` for each implementation milestone. A clean non-final milestone returns to the next milestone. Final closeout requires all implementation milestones and required review resolution to be closed, followed by triggered CI maintenance, verification, success-only explanation generation, and PR handoff.

The compact canonical chain is `proposal -> proposal-review -> architecture -> spec -> design-review -> plan -> delivery-review -> implement -> code-review -> review-resolution when triggered -> ci-maintenance when triggered -> verify`. Successful Verify establishes lifecycle completion; PR is an optional external handoff. Architecture and specification remain separate authoring stages reconciled before Design Review; plan owns verification allocation and is reviewed for implementation and verification readiness by Delivery Review. Historical v1/v2 records grant no current route. Other retired stage records are historical evidence only and grant no progression authority.

Until compact activation, routing uses `stage-owned-change-local-v3` as its executable compatibility contract. The compact implementing change uses the bounded preactivation closeout bootstrap and is not rewritten into the compact shape. After activation, new changes use `compact-current-state-v1` and registered historical changes retain their exact contract. The exact primary plan owns verification allocation; final closeout routes through triggered review resolution and `ci-maintenance`, then to `verify`. Successful Verify owns the final explanation; route exercises the stable workflow authority for correction routing.

The rename does not rewrite protocol state: route continues to use `stage_authority: workflow`, and existing `workflow.automation` occurrences remain authoritative with their exact target, occurrence, budgets, receipts, pause or cancellation state, and lifecycle-revision safeguards.

After a PR is open, a user-authorized bounded PR CI repair is an isolated correction, not a new profile or another pass through the chain. Preserve current review, explanation, verification, and lifecycle evidence only when the correction restores already-approved behavior without changing their decision basis. Otherwise route to the earliest affected owning stage.

## When to use

Use this skill when starting, resuming, auditing, or routing work through the standard workflow, including an explicitly authorized automation command.

Classify whether the work is a bug, feature, refactor, migration, documentation change, or review; whether it changes observable behavior or architecture; and the smallest safe reviewable slice. Specify observable behavior before planning or implementation, establish tests or proof before production changes, expose significant architecture, require evidence for claims, and keep work in small stable batches.

## When not to use

Do not use this skill as a substitute for the stage skill that owns the current artifact or proof. If the user requests only one stage output, invoke that skill in isolation.

Use `explore` or `research` only under the optional discovery routing rules below. Use `bugfix` for work that begins with a failure, regression, incident, or unexpected behavior. Use `learn` only when periodic or explicit learning triggers apply.

A direct individual-skill request is isolated by default. It does not activate, resume, settle, or advance a governed workflow unless the user explicitly requests workflow continuation or valid workflow-managed state already requires it.

A direct `pr` request routes to the `pr` skill and its own readiness gate; it does not authorize missing upstream lifecycle work.

## Inputs to read

Read only what the routing decision needs:

- the user request and invocation context;
- repository governance and workflow instructions;
- authoritative CLI workflow context when governed state matters;
- stable upstream artifacts and the active plan when relevant;
- git, validation, CI, or external evidence only when the route depends on it.

For governed routing, request project-phase `rigorloop workflow-context` when exact change identity is not authoritative, then request change-phase context for the selected exact change. Stop on unresolved candidate ambiguity. Use the returned lifecycle revision, artifacts, locations, blockers, permitted operations, and automation projection; do not reconstruct them from prose, filenames, prior chat, remembered state, or guessed paths. Refresh the complete change-phase context after any lifecycle mutation or observed identity drift.

Unknown artifact types and unknown lifecycle stages are blockers. In portable mode, an explicit safe target or published portable default may be used, but it grants no governed lifecycle state or project-local customization claim. If neither is available, request an explicit path rather than guessing.

Use bounded evidence before broad reads, but do not under-read. Expand when evidence is missing, stale, contradictory, or insufficient. Read a complete file when the whole file is the review target or surrounding context can change the conclusion.

Use a broader-section read when a narrow excerpt cannot establish the semantic route safely.

## Outputs

Produce a routing decision, authoritative current-stage assessment, blockers or assumptions, and the next valid skill or stop condition. Do not replace the downstream artifact.

## Optional discovery routing

Explore expands the decision space. Research reduces decision-relevant uncertainty. Neither skill owns the supported decision.

- Select Explore when the option space is materially unclear: the real problem, user value, scope, or materially different directions remain unsettled; the request assumes a solution too early; the decision is difficult to reverse; or the owning stage cannot proceed without clearer alternatives.
- Select Research when a material decision depends on an uncertain fact: platform or dependency behavior, compatibility, migration, a current standard or rule, or a scale, performance, security, or operational claim needs evidence.
- Select both, in that order, when Explore identifies bounded research questions and those research questions could materially change the option comparison.
- Select neither when direction and decision-relevant facts are sufficiently clear for the owning stage to proceed.

Do not auto-run Explore or Research. A standalone discovery artifact requires an explicit invocation or higher authority that specifically requires the support work. A small incidental fact check or option consideration inside an owning stage does not create a discovery artifact and must not be reported as completion of Explore or Research.

Either skill may support Proposal, Design, Delivery, Implementation, Verify, or another named decision owner. The artifact names that owner and recommends a handoff; the owning stage must explicitly adopt any conclusion that changes its governed decision. A discovery artifact does not approve the direction, does not edit the owner's artifact, does not settle a package, and does not advance lifecycle state. If support work contradicts an approved decision, return the contradiction to the stage that owns that decision rather than silently changing it.

## Invocation classification

Classify the three predicates below from authoritative evidence. Automation command forms are portable across supported adapters:

- Adapter invocation equivalents preserve the same arguments: Codex uses `$route auto: <argument>`, Claude uses `/route auto: <argument>`, and OpenCode invokes the installed `route` skill with `auto: <argument>`. Here `<argument>` is `<target-stage>`, `status`, or `off`.
- `$route auto: <target-stage>` selects a structured target. Supported targets are `proposal-review`, `architecture`, `spec`, `design-review`, `plan`, `delivery-review`, `implement`, `code-review`, and `verify`.
- `$route auto: status` is read-only. `$route auto: off` durably cancels the unified run and preserves transition evidence.
- `governed_change_context`: a valid current governed change record exists.
- `automation_command_context`: the invocation is an explicit automation command, including a pre-persistence target bootstrap.
- `armed_automation_context`: valid durable automation authorization or an active run exists for the same governed change.

Conversational wording alone does not establish governed or armed automation authority. An explicit target command establishes command context, not an armed run.

Use exactly these assemblies:

| Assembly | Evidence | Load |
| --- | --- | --- |
| `WP0-generic-routing` | no governed or automation trigger | `SKILL.md` |
| `WP1-governed` | governed only | governed lifecycle reference |
| `WP2-governed-automated` | governed plus command or armed automation | governed and automation references |
| `WPB-automation-bootstrap` | new target command without a governed record | automation reference, then governed reference after identity validation and reclassification |
| `WPS-stateless-automation-command` | `status` or `off` without a governed record or active run | automation reference; no state creation |

Active or resumable automation without a valid governed identity stops.

Every predicate combination must match exactly one assembly row. Any other combination, or any combination matching more than one row, stops as invalid invocation context before resource-dependent interpretation or mutation.

## Resource map

- READ `references/governed-lifecycle-routing.md` when current governed state must be interpreted, audited, resumed, settled, or mutated; after a successful automation bootstrap, load it before persisting automation state.
- READ `references/bounded-workflow-automation.md` for an explicit automation target, status, or cancellation command; an active or resumable automation run; automation bootstrap; packets; receipts; correction loops; or target promotion.
- READ `references/boundary-first-method-v1.md` when an approved boundary, interaction, or proof ID is missing, stale, unknown, ambiguous, conflicting, or insufficient for routing.

When a trigger is false, do not load its resource. After classification and before resource-dependent interpretation or action, confirm every required reference and asset is present and readable. When a required resource is missing, unreadable, contradictory, or from a mixed package version, stop before the governed action. A contradiction among packaged resources is a package defect. The common path is intentionally insufficient to reconstruct conditional procedure: stop rather than invent, recall, or partially reconstruct it.

## Boundary-first method

Run this compact scan before any stage-owned decision that can change observable behavior, and whenever the input cites an active boundary contract or stable boundary, interaction, or proof ID. Do not wait for the user to name the method.

1. Which inputs or actors can change the outcome?
2. Which state or timing conditions can change the outcome?
3. Which public, sibling, helper, or alternate path can change the outcome?
4. Which failure, retry, recovery, compatibility, or external condition can change the outcome?

If the work is non-behavioral, cites no active boundary identity, and the scan finds no outcome-changing condition, continue under the ordinary stage contract. The scan alone does not create a formal record, ID, proof map, artifact, or user-visible scenario inventory.

Start with the exact approved rows cited for the current decision. Expand approved context only when an ID or outcome is missing, stale, unknown, ambiguous, conflicting, escaped, or insufficient to explain observed behavior. A new or changed normative outcome routes to `spec`. A pre-implementation verification-allocation gap routes to `plan`. Historical contracts grant no current progression authority. Downstream stages do not redefine or rename upstream IDs.

Add a scenario only for a distinct outcome or material authority, trust, state, timing, recovery, path, compatibility, external-dependency, incident, or regression hazard. Stop when every applicable boundary and selected interaction has direct proof; do not build a Cartesian inventory.

Capability state controls formal adoption: `pending` never claims active adoption; after activation, new behavior-changing specs adopt automatically, grandfathered non-substantive revisions remain valid, and `design-review` must block an undecidable substantive-revision classification. Explain concisely when a formal record is created or an upstream gap blocks progress; do not request redundant consent for contract-required adoption. Structural validation cannot author, repair, or approve semantic content.

Route the method, locate governing artifacts, and stop on missing applicable ownership. For an adopting change, identify the approved feature boundary record and proof map before routing downstream. Stop routing and name the owning upstream stage when ownership is absent or an identity is invalid.

## Lifecycle overview

- Standing artifacts: project vision and constitution.
- Living references: project map and CLI-derived workflow context.
- Workflow infrastructure: governance, stage skills, and derived skill-package output.
- On-demand support: `explore`, `research`, `architecture`, `ci-maintenance`, and `learn` when triggered.
- Per-change chain: the standard sequence above, including ci-maintenance when triggered.
- Periodic artifacts: learning and other cadence- or incident-triggered memory.

Stage-obligation values are `mandatory`, `conditional`, `on-demand`, and `periodic`. Conditional, on-demand, and periodic work blocks only when triggered, cited as a dependency, or required by higher authority. Continue to the next mandatory or triggered downstream stage in an authorized workflow-managed flow.

## Universal ownership and safety

The user owns product intent and destructive or external authority. Each authoring stage owns its artifact and matching authoring transition. Review peers own their review evidence and matching settlement. Implementation and evidence stages own only their scoped outputs. Route owns semantic routing and later planned-work decisions while using `stage_authority: workflow` for workflow-owned mutations. New primary plans reach Delivery Review without live work; after the delivery package is approved, plan owns the one-time initialization of missing `planned_work`, and route owns every later transition.

Do not update an upstream artifact as workflow bookkeeping. Do not infer completion from file existence. Review readiness is not verification readiness, and verification readiness is not PR readiness.

The route skill must not author proposals, specs, plans, reviews, ADRs, or exact schemas merely because it routes them. A CLI-resolved path or structurally permitted operation never transfers stage authority.

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

Use targeted proof first. Run broad smoke only when an authoritative `broad_smoke.sources` trigger applies, and keep required manual proof in `verify-report.md`.

## Handoff

- Normal next stage: the next valid specialized skill or stop condition for the standard workflow state.
- Conditional next stages: `explore`, `research`, `architecture`, `ci-maintenance`, or `learn` when triggered; review, explanation, verification, and PR only when workflow state permits them.
- The `route` skill owns semantic routing; the receiving skill owns its artifact or proof.

Route deferred work to the durable artifact that can act on it using authoritative CLI context. Do not put deferred execution work in `project-map`.

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

Under registered historical contracts, formal material findings require evidence, required outcome, and safe resolution or `needs-decision` rationale. Their disposition is `accepted`, `rejected`, `deferred`, `partially-accepted`, or `needs-decision`; `needs-decision` remains open. `Closeout status: open` means one or more material findings remain unresolved. `Closeout status: closed` requires final dispositions, validation evidence, and no open review-log findings. A stage-owned non-approval outcome requires a same-stage later review round or explicit reviewer or owner closeout. `review-resolution.md` alone is not a silent substitute for required re-review. no-material detailed records need `review-log.md` but not an empty `review-resolution.md`.

For registered historical contracts, `verify` owns branch-ready and `pr` owns PR-body and PR-open readiness. For compact changes, successful Verify owns lifecycle completion and any later PR is optional. This mechanism never opens a PR, pushes, publishes, releases, deploys, merges, performs destructive Git operations, accesses credentials, or mutates an external system.

## Customer-project routing

Do not require RigorLoop repository-internal specs or docs to be present. Governed use requires authoritative CLI context. Portable use may rely on an explicit safe target or the published defaults below but cannot claim governed placement or project customization.

For a missing formal change root in portable mode, use `YYYY-MM-DD-slug`.

Treat `docs/changes/<change-id>/plan.md` as a non-canonical historical or rejected plan-body path.

## Default artifact paths

Use repository conventions first. Compact paths come from the bounded projection and stable-record contract. The following portable defaults describe registered historical contracts:

```text
AGENTS.md
CONSTITUTION.md
docs/project-map.md
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
docs/changes/<change-id>/verify-report.md
specs/slug.md
docs/learn/sessions/YYYY-MM-DD-slug.md
```

`docs/plan.md` is the stable navigation index and `docs/plans/YYYY-MM-DD-slug.md` is the detailed plan body.

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

- Skill: route
- Status:
- Artifacts changed:
- Open blockers:
- Next stage:
```

Then report the authoritative context and position, current stage, artifacts found or missing, transitions performed, next action or stop reason, and whether implementation is permitted. For automation, also report the target, occurrence when repeated, review or clean-gate state when applicable, fixes, and decisions.
