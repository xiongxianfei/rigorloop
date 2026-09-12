---
name: route
description: >
  Route, resume, audit, and orchestrate bounded RigorLoop workflow execution using authoritative CLI context. Use when starting or continuing governed work, interpreting blockers or findings, selecting correction ownership, or managing bounded workflow automation.
argument-hint: [feature, bug, project goal, issue number, or current workflow state]
---

# Semantic workflow router

## Test criteria application

When the project explicitly adopts Test-model criteria, use the selectively loaded guidance below for test quality and maintenance. These criteria replace source-local shared test-purpose, case-selection and maintenance criteria for adopted work; retain specialist methods and historical evidence. Actual judgments, evidence applicability and closeout consequences remain with the responsible assessors under the project's review policy.

## Quick operating guide

Use this skill to: route, resume, audit, or automate the standard workflow without replacing the specialized stage skill.

Read first: the request and repository instructions. For governed work, use the selected profile's authoritative CLI context below before inspecting semantic evidence.

Produce: the current context, routing result, blockers, and next valid stage.

Stop when: required authority is missing, stale, contradictory, or unsafe to infer.

Do not claim: implementation, review, validation, branch, PR, or final readiness owned by another stage.

Next stage: the specialized skill permitted by authoritative state, or a stop condition.

## Review and Closeout application

When project authority explicitly adopts Review and Closeout policy, use the packaged application below for shared assessment meaning. It replaces source-local judgment, independence, applicability, concern-disposition and closeout rules in this skill and its conditional resources; retain specialist methods and contract-selected storage procedures. Historical assessments retain their original meaning but grant no current runtime support. Missing or contradictory required guidance stops dependent reliance.

## Explicit recording

Use this profile when the project has adopted the RigorLoop Record Format and explicitly selected the change. Read the project's governing documents. The Workflow model owns coordination, Review and Closeout owns assessment policy, Record Format owns stored shapes, and CLI owns construction and persistence. Current storage uses `rigorloop-records-v3`; historical stores remain unchanged archival evidence. Select the actual record contract; never mix versions within a store. Retired or unknown stored formats are rejected without fallback. Do not migrate or reinterpret historical records; preserve their bytes and meaning as archival evidence. The project need not contain RigorLoop's internal design repository.

Use the contract-selected recording procedures in this skill and its conditional resources. Dispatch primary results by schema_version (2 or 3), then status and operation; a schema-3 error alone does not establish v3 storage. Read scope and omissions before relying on selected content. Retain substantive stage duties, permissions, independent assessment and proof obligations. Historical records grant no current execution authority.

Use `rigorloop context --root PATH --change ID --input - --format json` with explicitly selected kinds/filters and full detail. Expand the selection when needed: omitted content is not evidence of absence. Copy `record_contract` and `revision` into the targeted request's `contract` and `expected_revision`. Use `rigorloop subject inspect --root PATH --path FILE --content full --format json` for the exact engineering basis and mechanical identities; supply relied-on subjects as `reads` with their expected identities.

Make your decision, then use the purpose-specific command's `--help` and submit its targeted operation on stdin. Use `batch` for related explicit updates. Supply semantic values and any required applicability; the CLI constructs registry entries, preserves neighbors and serializes records. Do not reconstruct complete files or invoke historical eligibility first. Preview is optional; normal writes validate. A save does not approve work, establish readiness or select the next actor. Conflict requires rereading and reassessment; busy/recovery-required is not a save. Use explicit `record-store recover` for interrupted storage. Missing or stale evidence prevents reliance, not recording a correction.

Choose the current activity and responsible owner from the required engineering basis; status/context do not choose them. Record those decisions through activity set, work add/set and explicit applicability set as needed. Different actors may record in successive transactions. Corrections after completed work remain recordable. Do not manufacture another actor’s judgment, blocker disposition or final Verify assessment.

You are the lifecycle orchestrator. Route work to the stage that owns the next artifact or proof, preserve lifecycle evidence, and stop unsafe or premature transitions. Do not replace a specialized stage skill.

## Purpose

Use this skill to start, resume, audit, or route the standard RigorLoop workflow. The responsible actors coordinate:

```text
proposal -> proposal-review -> design -> design-review
-> plan -> delivery-review -> implement -> milestone code-review
-> fresh final whole-change code-review -> verify -> optional pr
```

Repeat implementation and independent review for each milestone. Route required corrections to their owning author; reconcile Design before planning. Trigger CI maintenance when needed before the final reviewed subject is established. After all implementation milestones and required corrections are complete, require fresh independent whole-change Code Review of the complete final diff and cross-milestone interactions before successful final Verify. Prior milestone judgments inform but do not replace that review.

Use only the selected record store for runtime recording. Preserve old records as archival evidence without execution, migration or fallback. Route owns explicit activity and work decisions; CLI observations do not select a stage or grant readiness. Successful Verify owns the final explanation and closeout assessment. PR, release and publication retain separate authority.

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

For governed routing, use factual `rigorloop workflow-context` discovery when the exact change is not selected. Resolve ambiguity explicitly. Then use primary `context` and `show` for the selected registry, activity, work, reviews, findings, evidence and blockers. Inspect exact engineering subjects as needed; do not infer state from prose, filenames or prior chat. Refresh the revision and relied-on reads after mutations or observed drift. Context reports observations, not permitted operations or an automation projection.

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

- Adapter invocation equivalents preserve the same arguments: Codex uses `$route auto: <argument>` and Claude uses `/route auto: <argument>`. Here `<argument>` is `<target-stage>`, `status`, or `off`.
- `$route auto: <target-stage>` selects a structured target. Supported targets are `proposal-review`, `design`, `design-review`, `plan`, `delivery-review`, `implement`, `code-review`, and `verify`.
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

- READ `references/test-quality.md` when adopted criteria apply and this invocation authors, allocates or assesses test obligations.
- READ `references/test-maintenance.md` when adopted criteria apply and this invocation changes tests or assesses test maintenance, removal or its impact.

- READ `references/review-reliance.md` when applying adopted assessment applicability, correction or closeout policy.

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

Start with the exact approved rows cited for the current decision. Expand approved context only when an ID or outcome is missing, stale, unknown, ambiguous, conflicting, escaped, or insufficient to explain observed behavior. A new or changed normative outcome routes to `design`. A pre-implementation verification-allocation gap routes to `plan`. Historical contracts grant no current progression authority. Downstream stages do not redefine or rename upstream IDs.

Add a scenario only for a distinct outcome or material authority, trust, state, timing, recovery, path, compatibility, external-dependency, incident, or regression hazard. Stop when every applicable boundary and selected interaction has direct proof; do not build a Cartesian inventory.

Capability state controls formal adoption: `pending` never claims active adoption; after activation, new behavior-changing specs adopt automatically, grandfathered non-substantive revisions remain valid, and `design-review` must block an undecidable substantive-revision classification. Explain concisely when a formal record is created or an upstream gap blocks progress; do not request redundant consent for contract-required adoption. Structural validation cannot author, repair, or approve semantic content.

Route the method, locate governing artifacts, and stop on missing applicable ownership. For an adopting change, identify the approved feature boundary record and proof map before routing downstream. Stop routing and name the owning upstream stage when ownership is absent or an identity is invalid.

## Lifecycle overview

- Standing artifacts: project vision and constitution.
- Living references: project map and CLI-derived workflow context.
- Workflow infrastructure: governance, stage skills, and derived skill-package output.
- On-demand support: `explore`, `research`, `ci-maintenance`, and `learn` when triggered.
- Per-change chain: the standard sequence above, including ci-maintenance when triggered.
- Periodic artifacts: learning and other cadence- or incident-triggered memory.

Stage-obligation values are `mandatory`, `conditional`, `on-demand`, and `periodic`. Conditional, on-demand, and periodic work blocks only when triggered, cited as a dependency, or required by higher authority. Continue to the next mandatory or triggered downstream stage in an authorized workflow-managed flow.

## Universal ownership and safety

The user owns product intent and destructive or external authority. Authors own their artifacts and authorized evidence; reviewers own judgments, findings and dispositions. Implementation owns its slice and proof. Route owns explicit activity and later work decisions. Plan may initialize absent work once from the exact approved Delivery package; it cannot revise existing work. Targeted recording preserves these supplied decisions without granting permission or deriving progression.

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

Use targeted proof first. Run broad smoke only when an authoritative `broad_smoke.sources` trigger applies. Record required manual proof as registered evidence with its subjects and applicability before final Verify; successful Verify references that evidence.

## Handoff

- Normal next stage: the next valid specialized skill or stop condition for the standard workflow state.
- Conditional next stages: `explore`, `research`, `design`, `ci-maintenance`, or `learn` when triggered; review, explanation, verification, and PR only when workflow state permits them.
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

## Customer-project routing

Do not require RigorLoop repository-internal specs or docs to be present. Governed use requires authoritative CLI context. Portable use may rely on an explicit safe target or the published defaults below but cannot claim governed placement or project customization.

For a missing formal change root in portable mode, use `YYYY-MM-DD-slug`.

Treat `docs/changes/<change-id>/plan.md` as a non-canonical historical or rejected plan-body path.

## Default artifact paths

Use project conventions and the selected registry. These paths are orientation defaults, not inferred registration or authority:

```text
AGENTS.md
CONSTITUTION.md
docs/project-map.md
docs/proposals/YYYY-MM-DD-slug.md
docs/design/<model>/<model>.md
docs/design/<model>/examples/<example>
docs/plans/YYYY-MM-DD-slug.md
docs/plan.md
docs/changes/YYYY-MM-DD-slug/
docs/changes/<change-id>/change.json
docs/changes/<change-id>/reviews/<review-id>.json
docs/changes/<change-id>/evidence.json
docs/changes/<change-id>/material-decisions.json
docs/changes/<change-id>/verify-report.json
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
