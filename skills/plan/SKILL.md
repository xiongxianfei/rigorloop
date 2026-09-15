---
name: plan
version: "1.0.0"
schema-version: skill-readability-v1
description: >
  Create or revise a stable execution plan after the proposal and affected Designs are settled enough to implement. Use for multi-file, multi-component, risky, migration-heavy, or milestone-based work that needs reviewable implementation slices, verification allocation, validation commands, recovery paths, and dependencies. Do not use plan to choose product direction, write code, review diffs, update workflow routing or existing planned work, verify branch readiness, or open PRs.
argument-hint: [affected Design set, retained source path, or implementation goal]
---

# Stable execution plan

## Workflow role

- role_name: plan
- stage: authoring
- upstream: accepted proposal, approved affected Design package and relevant retained legacy contracts, and project-local workflow evidence
- downstream: delivery-review
- summary: Own stable plan content and its authoring transition; initialize approved plan work only through the governed operation.
- must_not_claim: implementation completion, review approval, verification, branch readiness, PR readiness, final closeout, or Done

## Purpose

Create or revise a concrete plan with traceable milestones, validation, dependencies, risks, and recovery.

## When to use

Use after proposal, spec, and architecture are stable enough to sequence multi-file, risky, milestone-based, migration-heavy, or cross-component work.

## When not to use

Do not choose product direction, replace a missing specification, implement code, review a diff, verify branch readiness, or open a PR.

## Invocation classification

Classify the invocation before writing.

- Portable planning has no exact governed change authority. It writes the plan and navigation only; it does not read or mutate `change.json` as lifecycle state.
- Governed planning requires a supported stored contract, settled prerequisites, plan-owned authority, and a deterministic plan path. Load `references/governed-plan-authoring.md` and select exactly one operation: `create-primary-plan`, `revise-primary-plan`, or `initialize-approved-plan`. Hand the exact plan directly to Delivery Review.
- Boundary-first procedure is additive. Load its reference only under the mapped trigger.

Conversational wording, resource availability, or an automation command does not establish governed authority. Missing, stale, conflicting, or ambiguous authority stops before dependent writes. Manual and workflow-managed execution use the same plan-owned write boundary; only `route` may coordinate later stages or routing.

The phrase `valid governed plan authority` means the supported contract, exact selected change, settled prerequisites, intended target and authority for the selected operation agree. Validate any governed signal before dependent writes; malformed signals cannot select portable fallback. Loading recording never establishes automation or approval. Reassess late triggers before dependent action.

## Project-local evidence

Public skills operate in customer-project mode by default. Use project-local artifacts when present and relevant, including `AGENTS.md`, `CONSTITUTION.md`, proposals, specs, architecture, plans, tests, CI, and source. For governed placement and lifecycle facts, consume authoritative CLI workflow context. Do not require RigorLoop repository-internal specs or docs in customer projects. Use portable defaults where safe without claiming governed placement, and block on ambiguity.

## Inputs to read

Read project-local `AGENTS.md` and `CONSTITUTION.md` when present, then the accepted proposal, approved affected model/example subjects and relevant retained legacy sources, project map when reliable, current code and tests when needed for sequencing, and workflow guidance. For governed work, read the bounded change-record view first and the complete `change.json` when authoring, migration, disputed evidence, or whole-record validation requires it.

Verify upstream settlement from current artifact entries and formal review evidence. Treat upstream content, reviews, and other lifecycle entries as read-only. If authority is missing, contradictory, unknown, or unmapped, record the blocker and route to the owning stage.

Use bounded evidence before broad reads. Read a full file when it is the target, surrounding context controls the plan, bounded evidence conflicts, or a behavior-changing decision cannot be made safely from a smaller range.

## Recording boundary

For valid governed plan authority, read `references/governed-plan-authoring.md` before dependent recording or approved-plan initialization. It owns complete context/subject inspection, record-contract dispatch, revision/read checks, targeted writes, applicability and conflict/recovery procedure. A late governed trigger requires the same complete method; do not reconstruct it from memory or an unrelated file.

Keep create/revise separate from `initialize-approved-plan`: initialization may add only absent work from the exact current approved Delivery Review plan, once. Existing or conflicting work returns to `route` unchanged. Recording grants no approval, routing or execution authority. Missing, unreadable, escaped, stale or mixed-version required procedure stops dependent work; an untriggered method does not block unrelated portable planning.

## Test criteria application

When the project explicitly adopts Validation-model test criteria, use the selectively loaded guidance below for test quality and maintenance. These criteria replace source-local shared test-purpose, case-selection and maintenance criteria for adopted work; retain specialist methods and historical evidence. Actual judgments, evidence applicability and closeout consequences remain with the responsible assessors under the project's review policy.

## Review and Closeout application

When project authority explicitly adopts Review and Closeout policy, use the packaged application below for shared assessment meaning. It replaces source-local judgment, independence, applicability, concern-disposition and closeout rules in this skill and its conditional resources; retain specialist methods and contract-selected storage procedures. Historical assessments retain their original meaning but grant no current runtime support. Missing or contradictory required guidance stops dependent reliance.

## Plan quality contract

Treat the plan as the primary allocation surface from SRs and architecture boundaries into proportional delivery work.

The plan's primary responsibility is to define the safe engineering and dependency sequence. Shape milestones first by dependencies, safe intermediate states, migration order, reversibility, integration boundaries, implementation risk, and reviewability; attach verification to that sequence rather than reshaping it merely to manufacture isolated tests.

- Derive every behavior-changing step from approved requirements and architecture; do not add unstated behavior.
- Map applicable boundaries to independently closeable milestones, dependencies, affected surfaces, rollback units, and proof timing.
- Give each implementation milestone a unique ordered ID and kind, engineering purpose, governing SRs or justified non-SR obligations, architecture responsibility, dependencies, implementation scope, completion criteria, required verification groups, evidence expectations, review handoff, risks, and rollback or recovery.
- Apply the packaged closeout guidance: name final whole-change Code Review as a checkpoint after all implementation and required corrections, before successful final Verify.
- Separate implementation milestones from `lifecycle-closeout` work. Do not postpone or hide in-scope implementation merely to expose final closeout.
- Put direct proof near the milestone that first establishes the behavior. Include negative, failure, retry, recovery, compatibility, generated-output, security, and external-boundary proof when applicable.
- Add change-level verification whenever end-to-end, cross-milestone, cross-component, compatibility, migration, concurrency, failure/recovery, security, authority, generated-output parity, or other integrated behavior cannot be demonstrated adequately within one milestone. Milestone completion does not imply complete-change correctness.
- Use lightweight `TG-<id>` verification groups to state what behavior and important scenarios must be demonstrated. Preserve `SR → allocated milestone or work → verification group → concrete proof → evidence`; do not require one SR per group, one group per test, or identities for individual test functions.
- Keep concrete test and check mechanics implementation-owned. A verification group is plan-local stable intent, not a governed artifact, lifecycle state, replacement requirement hierarchy, or standalone verification skill.
- Keep ordinary verification guidance compact. Load only the specialist method whose risk trigger applies; do not load every specialist reference by default.

- Name exact repository-owned validation commands. Record a visible rationale when an applicable proof cannot be automated.
- Keep milestones small enough for independent implementation and code review, with explicit commit boundaries when the project requires them.
- Keep `docs/plan.md` as navigation, never as a second plan body or state owner.

New and substantively revised plan bodies contain stable execution intent only. Do not embed current milestone state, command outcomes, validation progress, blockers, review status, routing, or closeout progress. For governed work, `change.json work entries` is the sole current milestone-state owner. Later changes to a settled milestone ID, order, kind, completion criteria, or required evidence require governed replan or migration.

## Artifact placement

Use the explicit user path or change ID, then authoritative CLI workflow context, change metadata, reviewed artifact path, and governing schemas, followed by the portable default `docs/plans/YYYY-MM-DD-slug.md`. Stop on unresolved ambiguity. Maintain `docs/plan.md` with relative clickable links; never overwrite an older initiative plan.

Plan surfaces are distinct: authoritative CLI context resolves governed workflow paths; `docs/plan.md` is navigation; `docs/plans/YYYY-MM-DD-slug.md` is the stable plan body; `docs/changes/<change-id>/change.json` owns mutable lifecycle and milestone state; and `docs/changes/<change-id>/` stores stage-owned evidence. In `docs/plan.md`, use clickable relative Markdown links such as `[Title](plans/YYYY-MM-DD-slug.md)`.

## Operating sequence

1. Resolve the invocation mode, exact plan target, upstream settlement, and any boundary trigger.
2. Read the smallest sufficient evidence and map requirements, decisions, boundaries, risks, and proof obligations.
3. Design ordered, independently reviewable milestones with validation and recovery.
4. Copy the mapped structural assets, fill every applicable field, and omit no required execution intent.
5. For governed work, follow the loaded reference for create, revise, or approved-plan initialization and validate the complete candidate state.
6. Check traceability, sequencing, scope completeness, rollback, source readability, and absence of mutable plan state.
7. Produce the Expected output and hand the exact plan to `delivery-review`; do not settle review or advance routing.

## Boundary-first method

Run this compact scan before any stage-owned decision that can change observable behavior, and whenever the input cites an active boundary contract or stable boundary, interaction, or proof ID. Do not wait for the user to name the method.

1. Which inputs or actors can change the outcome?
2. Which state or timing conditions can change the outcome?
3. Which public, sibling, helper, or alternate path can change the outcome?
4. Which failure, retry, recovery, compatibility, or external condition can change the outcome?

If the work is non-behavioral, cites no active boundary identity, and the scan finds no outcome-changing condition, continue under the ordinary stage contract. The scan alone does not create a formal record, ID, proof map, artifact, or user-visible scenario inventory.

Start with the exact approved rows cited for the current decision. Expand approved context only when an ID or outcome is missing, stale, unknown, ambiguous, conflicting, escaped, or insufficient to explain observed behavior. A new or changed normative outcome routes to `design`. A pre-implementation verification-allocation gap routes to `plan`. Historical contracts grant no current progression authority. Downstream stages do not redefine or rename upstream IDs.

Add a scenario only for a distinct outcome or material authority, trust, state, timing, recovery, path, compatibility, external-dependency, incident, or regression hazard. Stop when every applicable boundary and selected interaction has direct proof; do not build a Cartesian inventory.

The project's selected contract owns formal adoption and document format. An unmarked feature requiring an adoption decision goes to Design Review; unknown markers and malformed records fail structural validation. Do not infer adoption from a historical activation snapshot or from installing a skill. Explain concisely when a formal record is required or an upstream gap blocks progress; do not request redundant consent for contract-required work. Structural validation cannot author, repair, or approve semantic content.

Stop planning when an applicable boundary lacks an allocation owner and route a contract gap upstream.

## Resource map

- READ `references/test-quality.md` when adopted criteria apply and this invocation authors, allocates or assesses test obligations.
- READ `references/test-maintenance.md` when adopted criteria apply and this invocation changes tests or assesses test maintenance, removal or its impact.

- READ `references/review-reliance.md` when applying adopted assessment applicability, correction or closeout policy.

- READ `references/requirement-to-delivery-model.md` when allocating system requirements and architecture boundaries into milestones or optional work hierarchy.
- READ `references/governed-plan-authoring.md` exactly when valid governed plan authority exists for `create-primary-plan`, `revise-primary-plan`, or `initialize-approved-plan`.
- READ `references/boundary-first-method-v1.md` when cited approved boundary or interaction rows are missing, stale, unknown, ambiguous, conflicting, or insufficient for planning.
- READ `references/boundary-and-negative-verification.md` only when inputs, outputs, system seams, invalid cases, or negative outcomes materially affect verification.
- READ `references/state-machine-verification.md` only when governed states, transitions, invariants, or invalid predecessor states materially affect verification.
- READ `references/concurrency-and-retry-verification.md` only when concurrency, ordering, idempotency, retry, or race behavior materially affects verification.
- READ `references/migration-and-compatibility-verification.md` only when old and new states, clients, formats, rollout, rollback, or migration materially affect verification.
- READ `references/failure-and-recovery-verification.md` only when partial failure, interruption, recovery, reconciliation, or degraded operation materially affects verification.
- READ `references/security-and-authority-verification.md` only when permissions, trust boundaries, credentials, policy, or authority materially affect verification.
- READ `references/cross-milestone-integration-verification.md` only when required behavior spans milestones, components, generated outputs, or an end-to-end workflow.
- READ `references/manual-and-operational-evidence.md` only when an important outcome cannot be proved adequately through deterministic automated checks.
- COPY `assets/plan-skeleton.md` when creating a plan or replacing its full structure.
  Fill: sections, source artifacts, owning change-record pointer, milestones, validation, recovery, dependencies, decisions, and readiness wording.
- COPY `assets/milestone.md` when adding each reviewable milestone.
  Fill: ID, kind, engineering purpose, requirements, architecture responsibility, dependencies, implementation scope, components, required verification groups, evidence expectations, steps, validation, expected result, completion criteria, handoff, risks, recovery, and optional commit boundary.
- COPY `assets/decision-log-row.md` for each material sequencing decision.
  Fill: date, decision, reason, and rejected alternatives.

Do not emit unfilled placeholders.

A missing or unreadable triggered reference stops dependent work. An untriggered resource does not load and does not block portable planning. Do not reconstruct missing conditional procedure from memory, combine mixed resource versions, or let an asset define policy.

## Generated Markdown readability

Write ordinary prose as normal Markdown paragraphs. Do not split a sentence across physical source lines merely for wrapping or clause separation; multiple sentences may remain in one paragraph. Preserve stable IDs and use tables for repeated mappings. Keep commands fenced or table-owned when they carry proof. Diagrams are optional; use them only when they reduce cognitive load and map to real artifacts, stages, components, actors, or states. Do not require manual-proof contracts from this readability guidance alone; use governing project rules when manual proof is otherwise required.

## Evidence collection efficiency

Use bounded evidence before broad reads or raw excerpts.
Use summary and stable-ID first reasoning before broad reads or raw excerpts.
Prefer check IDs, requirement IDs, test IDs, file paths, counts, line citations, matching line numbers, diffs, and targeted excerpts when inspecting large files, generated output, validation logs, or repeated scans.
Output caps are safety rails, not evidence-selection strategy.
Validation summaries must not change selected check coverage, command exit behavior, failure detection, or required validation evidence.
Read exact ranges after locating relevant lines, then expand only when the narrower evidence is insufficient.

## When full-file read is required

Read the full file when the whole file is the review target, the relevant section cannot be isolated safely, surrounding context can change the conclusion, bounded searches disagree or produce incomplete evidence, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Stop conditions

Stop when source artifacts conflict, upstream settlement is insufficient, architecture or security boundaries are unclear, a milestone depends on chat-only context, validation cannot be identified, governed identity or operation is ambiguous, required procedure is unavailable, or the plan would hide open work behind readiness language.

## Claims this skill must not make

Do not claim implementation, review, verification, CI, derived-artifact currency, branch readiness, PR readiness, ready for PR, ready for final closeout, or Done. Keep Remaining completion gates visible whenever readiness could be mistaken for completion.

Progress means work that has happened so far. Readiness means the next stage that can happen. Closeout means the current artifact or stage satisfied its checklist. Done means final lifecycle state after required gates are complete. Readiness is not Done.

## Outputs

Produce the stable plan, its navigation link when needed, and authorized plan-owned evidence. Use the mapped assets and Expected output for the handoff.

## Handoff

Normal next stage: independent `delivery-review` of the exact plan and applicable authoring evidence.

Conditional next stages: return behavior gaps to `design`, and governed migration or coordination to `route`; Plan never marks review clean or initializes routing.

## Output skeleton

```md
COPY `assets/plan-skeleton.md` for <the complete plan>.
COPY `assets/milestone.md` for <each applicable milestone>.
COPY `assets/decision-log-row.md` for <each material sequencing decision>.
Report <status, operation, changed artifacts, blockers, and next stage>.
Do not emit unfilled placeholders.
```

## Expected output

Report the selected operation, exact plan subject, changed artifacts, author-owned evidence and recording outcome when governed, blockers and immediate review handoff. Use the mapped assets as the sole full-plan, milestone and decision-row structures; keep mutable lifecycle state in its owning record.

Normal next stage: `delivery-review`. Return missing behavior to `design` and coordination or existing-work changes to `route`. A result does not establish review, implementation or final readiness.

## Result

- Skill: plan
- Status: <created | updated | initialized | blocked>
- Artifacts changed: <paths or none>
- Open blockers: <blockers or none>
- Next stage: <delivery-review | spec | architecture | workflow | blocked>
