---
name: implement
version: "1.0.0"
schema-version: skill-readability-v1
description: >
  Implement one approved milestone or isolated implementation request with tests or proof first, then hand it to code-review with validation evidence. Use when requirements, scope, and validation commands are clear enough to code. Use bugfix for defect reproduction/fix loops, code-review to review implementation, verify for final readiness, and pr for PR handoff.
argument-hint: [plan path, milestone ID, feature name, or implementation request]
---

# Test-driven implementation

Implement the smallest scope-complete approved slice with tests or proof first.
Do not expand scope, silently alter the contract, or claim success without direct evidence.

## Workflow role

- role_name: implement
- stage: execution
- upstream: approved Design Review package, approved Delivery Review package, accepted review-resolution finding, bugfix request, or isolated implementation request with clear scope
- downstream: code-review
- summary: Implement one scope-complete slice, record validation evidence, and hand it to code-review.
- must_not_claim: review passed, clean review, branch readiness, PR readiness, final verification, final closeout readiness, or derived artifact currency without owning proof.

For planned initiatives, treat the plan and upstream artifacts as read-only.
Write implementation, tests, and implementation evidence only; workflow owns milestone and routing state.

## Quick operating guide

Use this skill to:
- implement one approved milestone or isolated request with proof first.

Read first:
- change-local state when planned;
- the current milestone, governing spec, active test spec, recorded review evidence, relevant code/tests, and validation commands.

Produce:
- tests or proof, implementation, validation evidence, and a code-review handoff.

Stop when:
- authority, scope, proof, or validation is missing, contradictory, stale, or failing.

Do not claim:
- review, branch, PR, final-verification, or final-closeout outcomes.

Next stage:
- code-review.

Use full-file or broader-section reading when bounded evidence cannot preserve correctness.

## Purpose

Use after requirements and proof are stable enough to implement.
Use `bugfix` for defect repair, `code-review` for review, `verify` for final readiness, and `pr` for PR handoff.
Do not invent requirements, bypass required approvals, or use implementation to resolve unrecorded review findings.

## When to use

Use for an approved milestone or a clear isolated implementation request whose requirements and proof obligations are stable.

## When not to use

Do not use for defect investigation, artifact authoring or review, final verification, or PR preparation; route those tasks to their owning skill.

## Project-local evidence

Public skills operate in customer-project mode by default.
Use relevant project-local artifacts such as `AGENTS.md`, `CONSTITUTION.md`, approved specs, the active plan and test spec, architecture records, review resolution, `docs/workflows.md`, code, tests, and CI commands.
Do not require RigorLoop repository-internal artifacts in customer projects; use safe portable defaults and block on ambiguity.

## Inputs to read

Read before editing:

- `AGENTS.md` and `CONSTITUTION.md` when present;
- the approved feature spec and concrete current milestone or isolated scope;
- the active test spec and recorded, approved, current Delivery Review package when a formal workflow-managed delivery package is required;
- the approved Delivery Review ID and exact contract-selected member map, plus the approved Design Review ID it binds;
- relevant architecture or ADRs when the slice touches their boundaries;
- code, tests, neighboring patterns, and milestone validation commands;
- accepted review-resolution evidence when implementing recorded findings.

## Evidence access

Start with the smallest sufficient set: change-local state, current milestone, approved Design Review and Delivery Review packages, relevant code/tests, and scoped validation commands.
Read architecture, review resolution, workflow guidance, governance, or neighboring code only when triggered.
Expand when bounded evidence is missing, stale, contradictory, or insufficient; read the full file when the whole file or surrounding context controls the decision.

## Invocation profiles and authority

Classify the invocation before loading conditional procedure or mutating implementation state.

| Profile | Required authority | Conditional procedure |
| --- | --- | --- |
| `IP0-isolated` | Clear direct implementation scope | neither conditional reference |
| `IP1-planned` | Valid `planned_milestone_context` | planned-milestone reference only |
| `IP2-planned-armed` | Valid planned context plus matching `armed_automation_context` | both conditional references |

`planned_milestone_context` requires a workflow-managed invocation, a valid active plan, one exact current milestone owned by `implement`, and a milestone state that permits implementation.

`armed_automation_context` additionally requires current durable workflow authorization, the current review or correction mode, matching change and milestone identity, and non-stale evidence.

Armed automation without a valid planned milestone is invalid.
Conversational wording alone establishes neither predicate.
Missing, stale, mismatched, contradictory, or ambiguous evidence stops before conditional procedure is loaded or implementation state is mutated.

## First-pass completeness

Before editing, identify the same-slice completeness set: in-scope requirements, authored and aligned surfaces, named edge cases, and targeted validation.

A `first-pass acceptable result` means:

- every in-scope requirement and edge case is addressed;
- each required surface is updated or recorded as `unaffected with rationale`;
- no known in-scope defect is deferred to review or cleanup;
- the smallest scope-complete change, rather than merely the smallest diff, is implemented;
- required targeted validation passes;
- the result does not depend on later cleanup to become contract-complete.

Record any unchanged required surface and its rationale in contributor-visible evidence.
A later issue that this completeness set should have caught is a `preventable first-pass miss`.
If missing or conflicting inputs prevent a complete first pass, stop rather than guess.
If a formal workflow-managed delivery package lacks recorded, approved, current `delivery-review` evidence, or a substantive member edit made that approval stale, stop before implementation and route to the owning authoring or review stage.

## Implementation contract

### Tests and validation

- Write or update tests or deterministic proof first when feasible.
- Confirm expected failure for new behavior or regression coverage when feasible.
- Implement the minimum scope-complete change, rerun narrow proof, then refactor only within scope.
- Prefer selector-selected targeted proof before optional broad smoke.
- Use the project's validation selector, run all selected checks, and preserve stable check IDs such as `skills.validate` when they apply.
- Preserve authoritative broad-smoke triggers and record stable selected check IDs when useful.
- Stop on a failing required command until it is fixed or recorded as a blocker.

### Scope and ownership

- Implement only approved requirements and the current slice.
- Do not add unrelated refactors or unapproved public behavior.
- Do not defer a required same-slice correction.
- Stop and route newly discovered spec, architecture, security, permission, or owner-decision gaps.
- Do not update the plan, upstream artifacts, artifact settlement, or workflow as implementation bookkeeping.

### Change-local evidence

For ordinary non-trivial work, maintain `docs/changes/<change-id>/change.yaml` plus stage-owned implementation evidence. Successful final Verify records the durable change explanation in `verify-report.md`.
When creating a root, follow the `<change-id>` convention in `docs/workflows.md`; if no project-local workflow guide exists, use `YYYY-MM-DD-slug`.
Do not broaden this requirement to isolated manual work that does not claim complete workflow delivery.
Keep `review-resolution.md` and `verify-report.md` conditional on their governing triggers.

## Operating sequence

1. Confirm authority, profile, scope, requirements, approved boundaries, proof obligations, and edge cases.
2. Load only the resources mapped for that profile.
3. Add or update tests/proof first and run the narrowest relevant command.
4. Implement the smallest scope-complete change and rerun narrow proof.
5. Audit authored and aligned surfaces; refactor only inside the slice.
6. Run milestone-targeted validation before optional broad smoke.
7. Record decisions, discoveries, commands, results, unchanged surfaces, and follow-ups in implementation evidence.
8. For planned work, follow the mapped milestone procedure for commit and state-sync evidence.
9. Hand the completed slice to `code-review`; do not start the next milestone before clean review.

Tests must assert real behavior rather than broad mocks or snapshots that pass for the wrong reason.
Before changing behavior, confirm every implemented boundary or selected interaction has an approved owner and proof obligation.

## Outputs

Produce tests or proof first where feasible, implementation changes, validation evidence, and a `code-review` handoff.

## Handoff

- Normal next stage: `code-review` for the implemented milestone or isolated slice.
- Conditional next stages: stop for a spec, architecture, owner-decision, permission, or validation blocker; return to the same milestone for accepted review corrections; continue to another milestone only after workflow records clean review.
- Route planned stage transitions through `workflow`.

## Stop conditions

Stop before mutation or review handoff when:

- required authority, source artifacts, boundary ownership, or proof is missing, stale, unknown, or contradictory;
- scope is ambiguous or a spec, architecture, security, permission, or owner decision is needed;
- tests or required validation fail and are not fixed;
- the slice cannot meet first-pass completeness;
- planned work cannot produce current implementation evidence, state synchronization, and a review-requested handoff.

## Claims this skill must not make

Do not claim review passed, clean review, review-clean status, branch-ready, PR-ready, `pr-body-ready`, `pr-open-ready`, ready-for-final-closeout, final verification, final closeout, or generated-resource currency without owning proof.

Implementation completion is evidence for review, not milestone closeout.

## Progress, readiness, closeout, and Done

- Progress means work that has happened so far.
- Readiness means the next stage that can happen.
- Closeout means the current artifact or stage satisfied its checklist.
- Done means final lifecycle state after required gates are complete.
- Readiness is not Done. Implementation readiness for `code-review` is not review closeout, branch readiness, or PR readiness.

## Generated Markdown readability

When creating generated or generator-shaped Markdown, write ordinary prose as normal Markdown paragraphs. Do not split a sentence across physical source lines merely for wrapping or clause separation; multiple sentences may remain in one paragraph. Keep stable IDs and use tables for repeated mappings.
Diagrams are optional and should reduce real cognitive load.
Do not require manual-proof contracts from readability guidance alone.

## Resource map

- READ `references/boundary-first-method-v1.md` when approved boundary, interaction, or proof IDs are missing, stale, unknown, ambiguous, conflicting, or insufficient for implementation.
- READ `references/planned-milestone-implementation.md` when authoritative workflow evidence establishes a current planned milestone owned by `implement`.
- READ `references/automated-review-correction.md` only when durable workflow evidence formally arms automated review or correction for that same current change and milestone.
- COPY `assets/implementation-result-skeleton.md` when producing the implementation result.
  Fill: the core result and only the conditional groups applicable to the classified profile.
  Omit: inapplicable groups, empty fields, and meaningless `not applicable` values.
  Do not emit unfilled placeholders.

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

Stop on missing boundary or proof ownership and implement against the approved model and proof map.

Before changing production behavior, confirm every implemented boundary or selected interaction has an approved owner and proof obligation. Stop implementation before mutation when an owner is absent, an ID is stale or unknown, required proof is missing, or implementation exposes a new boundary that requires an upstream decision.

## Evidence collection efficiency

Use bounded evidence before broad reads or raw excerpts.
Use summary and stable-ID first reasoning before broad reads or raw excerpts.
Prefer check IDs, requirement IDs, test IDs, file paths, counts, line citations, matching line numbers, diffs, and targeted excerpts when inspecting large files, generated output, validation logs, or repeated scans.
Output caps are safety rails, not evidence-selection strategy.
Validation summaries must not change selected check coverage, command exit behavior, failure detection, or required validation evidence.
Read exact ranges after locating relevant lines, then expand only when the narrower evidence is insufficient.

## When full-file read is required

Read the full file when the whole file is the review target, the relevant section cannot be isolated safely, surrounding context can change the conclusion, bounded searches disagree or produce incomplete evidence, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Output skeleton

```md
COPY `assets/implementation-result-skeleton.md` for the implementation result.
Fill <core fields and applicable profile groups> required by this skill.
Omit inapplicable groups and do not emit unfilled placeholders.
```

## Expected output

Copy `assets/implementation-result-skeleton.md` and emit its core result plus only the groups applicable to the invocation profile.
The asset owns labels and layout; this file and the applicable procedure reference own status meaning, permission, claims, and handoff behavior.
Do not imply review, verification, branch, PR, or final-closeout outcomes.
