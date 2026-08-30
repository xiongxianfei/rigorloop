---
name: code-review
version: "1.0.0"
schema-version: skill-readability-v1
description: >
  Review an implementation slice against the actual diff, approved design and delivery packages, tests, and validation evidence, then record findings or a clean first-pass review. Use after implement hands off a milestone or when implementation review is requested. Use design-review, delivery-review, verify, or pr for those gates instead.
argument-hint: [branch, diff, plan path, spec path, or feature name]
---

# Independent implementation review

Review in independent-review mode with fresh eyes. Determine whether the actual implementation satisfies the approved contract safely; passing tests or plausible code alone is not sufficient.

## Purpose

Trace the implementation to its allocated work, governing SRs, and approved design boundaries.

Review the actual implementation slice against approved authority and record a first-pass status with a safe, milestone-aware handoff.

## When to use

Use after implementation handoff or for an explicit implementation-diff review.

## When not to use

Do not use for proposal, spec, architecture, plan, final verification, or PR approval gates, and do not fix the reviewed target before recording findings.

## Workflow role

- role_name: code-review
- stage: review
- upstream: implementation diff, review-requested milestone, governing artifacts, tests, and validation evidence
- downstream: review-resolution, next implementation milestone, or final closeout sequence
- summary: Perform independent implementation review, record the first-pass status and findings, close clean milestones, or route findings to review-resolution.
- ownership: Write review evidence only. Workflow owns milestone and routing state; code-review does not edit implementation, plans, artifact settlement, or change-local routing.
- must_not_claim: branch readiness, PR readiness, final verification, CI success, implementation fixes, or derived-artifact currency without separate owning evidence

It must not edit implementation, the plan, artifact settlement, milestone state, or routing.

## Quick operating guide

Use this skill to: inspect the actual review surface against its governing contract and record a first-pass review outcome.

Read first: the actual diff, tracked governing authority, current milestone, relevant tests, and validation evidence.

Produce: a recorded review status, findings or no-finding rationale, checklist coverage, and milestone-aware handoff.

Stop when: authority, evidence, or milestone state cannot support a credible outcome, or an owner decision is required.

Do not claim: branch-ready, PR-ready, verification passed, CI passed, or fixes owned by another stage.

Next stage: review-resolution for findings, the next milestone after a clean non-final review, or final closeout after the required final holistic review.

Use broader-section or full-file reading when bounded evidence is insufficient.

## Inputs to read

Read the target, tracked authority, current milestone, tests, and relevant validation described below.

## Review authority and evidence

Inspect the actual changed files, staged or unstaged diff, commit range, PR diff, or other explicit target. Read the approved spec, matching test spec, stable plan milestone, relevant architecture or ADR, related tests, and named validation evidence. For planned work, read `change.yaml` for current milestone and handoff state; use the plan only for stable intent and `review-resolution.md` for prior-finding disposition.

For work governed by consolidated gates, require the current approved Design Review ID and its exact member map plus the current approved Delivery Review ID and its exact member map. Treat review-required, partial, stale, or historical artifact-review evidence as non-authorizing. These package inputs strengthen implementation review but do not merge Code Review with Design Review, Delivery Review, or Verify.

Use the smallest sufficient evidence set. Begin with the diff, spec, test spec, milestone, tests, and validation. Add architecture, governance, related code, generated output, or history only when the reviewed behavior or an evidence conflict requires it. Record why substantive evidence outside that set was needed. Full-file reading is appropriate when the whole file is the target or bounded evidence is incomplete, contradictory, or context-sensitive.

Prefer a separate reviewer or fresh session. When unavailable, intentionally reset assumptions before reading the diff. Do not treat remembered intent, author self-assessment, or validation success as review proof.

Tracked governing branch state is required for a clean branch-scoped conclusion. Local-only authority may provide context but cannot support that conclusion. Missing authority does not suppress an independently supported `changes-requested` or `blocked` finding; use `inconclusive` only when the gap prevents both an actionable finding and a clean result. This is the mixed-evidence rule.

## Generated Markdown readability

When this skill creates or updates generated or generator-shaped Markdown:

- Write ordinary prose as normal Markdown paragraphs. Do not split a sentence across physical source lines merely for wrapping or clause separation; multiple sentences may remain in one paragraph.
- Preserve stable IDs for requirements, findings, commands, milestones, and evidence; use tables for repeated mappings.
- Keep commands fenced or table-owned when they carry proof.
- Diagrams are optional. Use them only when they reduce cognitive load and map to real artifacts, stages, components, actors, or states.
- Do not require manual-proof contracts from this readability guidance alone; use governing project rules when manual proof is otherwise required.

## Artifact placement

Use the explicit user path first, then the active change record, plan, reviewed artifact, or current metadata. If placement remains unclear, consult the project workflow guide, then governing specs or schemas for exact shape. Use a portable default only when no project-local owner exists; block on remaining ambiguity. Do not broad-search authoritative documents merely to find paths.

## Operating sequence

1. Identify the target, tracked authority, milestone, remaining milestones, and any explicit isolation or stop instruction.
2. Reset assumptions, inspect the actual diff, and map changed behavior to the governing requirements and boundary or interaction IDs.
3. Inspect tests and direct proof for public, sibling, helper, failure, recovery, compatibility, generated, and external paths that can change the outcome.
4. Challenge whether the selected checks and validation evidence are relevant and sufficient; do not confuse passing checks with compliance.
5. Apply every checklist item, choose one native status, and record findings or an evidence-backed no-finding rationale before any fix begins.
6. Record the formal review, then report the milestone-aware handoff to workflow. Rereview every changed implementation after resolution.

## First-pass checklist coverage

Evaluate each item as `pass`, `concern`, or `block` and cite concrete evidence:

1. Spec alignment: approved scope, requirements, examples, and non-goals.
2. Test coverage: changed behavior, regressions, and named failure paths.
3. Edge cases: boundary, state, timing, retry, recovery, and alternate paths.
4. Error handling: invalid states, partial failure, permissions, and fallback.
5. Architecture boundaries: components, ownership, interfaces, and ADRs.
6. Compatibility: contributor, workflow, data, and migration contracts.
7. Security/privacy: secrets, logging, authorization, and policy regressions.
8. Derived artifact currency: canonical, generated, packed, and installed state.
9. Unrelated changes: no hidden scope expansion.
10. Validation evidence: named commands, results, and proof adequacy.

## Published-skill semantic review

For a changed published skill, assess description and trigger clarity, ownership, prerequisites, executable procedure, evidence use, packaged resources, stop conditions, claims, and output and handoff usefulness. Use judgment rather than structural presence as the semantic oracle. Record material ambiguity as a review finding. Do not convert this checklist into prompt execution, transcript grading, model selection, or a broad semantic score in repository validation.

## Status, severity, and material findings

Use exactly one first-pass status:

- `clean-with-notes`: no unresolved accepted fix is required.
- `changes-requested`: one or more evidenced, in-scope, safely actionable findings exist.
- `blocked`: safe continuation requires a product, spec, architecture, ADR, ownership, or scope decision.
- `inconclusive`: missing evidence prevents both a credible clean result and an actionable finding.

Use severity `blocker`, `major`, `minor`, `nit`, or `positive`. A material finding is a required change or decision, not a quota. Every material finding must include Finding ID, Severity, Location, evidence, required outcome, and a safe resolution path or `needs-decision` rationale naming the decision and owner. Clearly fixable in-scope issues use `changes-requested`, not `blocked`.

## Isolation and Recording

Isolation governs handoff. Recording follows formal review triggers.

A direct or review-only request remains isolated by default: it does not automatically continue into downstream workflow stages.

Isolation does not suppress recording.

Every formal lifecycle review result must be recorded or explicitly blocked.

Use:

- `Recording status: recorded` when the required review evidence was created or updated.
- `Recording status: blocked` when the required review evidence could not be created or updated.

`not-required` is reserved for non-formal review-like requests outside the formal lifecycle review model.

For a clean review, create the lightweight review receipt required by the formal review recording spec and index it in `review-log.md`. Do not create an empty `review-resolution.md` solely for a clean review.

For material findings or blocking outcomes, create the required detailed review record and disposition artifacts.
Use a detailed review record for material or blocking review outcomes.

Material findings must include:

- Finding ID
- Severity
- Location
- Evidence
- Required outcome
- Safe resolution path, or `needs-decision` rationale

Do not merely tell the user that review artifacts should be created. Create or update them before final output, or report `Recording status: blocked` with the blocker and smallest next action.

For an isolated review with material findings, the final review output must state:

- no automatic downstream handoff
- material Finding IDs
- required review record path
- whether the record must be created before fixing or reconstructed
- whether owner decision is needed

## Direct proof and rereview

A clean conclusion for a named edge case requires direct proof from a targeted test, targeted validation output, or an allowed explicit manual verification note. Code-shape inference alone is insufficient. For validation routing, targeted proof names the selected or executed checks; broad smoke remains a separate trigger-owned obligation.

Changed implementation must be rereviewed. A targeted rereview can close its finding, but final closeout still requires a holistic review of the complete final diff and cross-milestone interactions. A clean milestone-local review is not proof that the branch or whole plan is ready.

## Stop conditions

Stop clean handoff when:

- the actual diff, relevant tests, or authoritative upstream artifacts cannot be inspected;
- tracked governing authority required for a clean branch-scoped result is missing;
- a finding needs a product, spec, architecture, ADR, ownership, or scope decision;
- review-only or isolated invocation forbids continuation;
- the reviewed milestone or remaining implementation milestones cannot be determined; or
- required recording cannot be completed.

Use `blocked` when the review already supports a blocker or owner-decision finding. Use `inconclusive` when insufficient evidence prevents a credible verdict. Do not silently repair workflow state or broaden scope.

## Claims this skill must not make

Do not claim branch-ready, PR-ready, `pr-body-ready`, `pr-open-ready`, verification passed, or CI passed. Cite tests or derived-artifact currency only as evidence from their owning surfaces. Do not claim implementation fixes unless a separately authorized resolution flow owns them.

Progress means work that has happened so far. Readiness means the next stage that can happen. Closeout means the current artifact or stage satisfied its checklist. Done means final lifecycle state after required gates are complete. Readiness is not Done.

## Handoff

- Direct or review-only `code-review` requests remain isolated by default.
- Normal next stage: report the review outcome to workflow, which routes from change-local state.
- Conditional next stages: review-resolution, the next implementation milestone, final closeout, or a stop.

## Status and milestone handoff

- `clean-with-notes` in a workflow-managed review follows the current plan and milestone state when no stop applies.
- `changes-requested` routes to review-resolution and rereview on the same milestone.
- `blocked` stops for the named decision or constraint.
- `inconclusive` stops for missing evidence and does not enter resolution.
- A clean non-final milestone closes only that milestone and hands off to the next in-scope implementation milestone.
- A clean final milestone may enter final closeout only when no implementation milestone or required resolution remains open. Final closeout runs triggered CI maintenance, final holistic code-review, explain-change, verify, and PR in workflow-owned order; it never jumps directly from milestone review to verify.

The review output must name the reviewed milestone, native status, milestone closeout, required resolution, remaining milestones, next stage, and final closeout readiness with reason. Code-review writes that evidence; workflow consumes it and changes lifecycle state.

## Boundary-first bridge

The following compact method remains inline so the reviewer can decide whether the mapped boundary reference is needed.

## Boundary-first method

Run this compact scan before any stage-owned decision that can change observable behavior, and whenever the input cites an active boundary contract or stable boundary, interaction, or proof ID. Do not wait for the user to name the method.

1. Which inputs or actors can change the outcome?
2. Which state or timing conditions can change the outcome?
3. Which public, sibling, helper, or alternate path can change the outcome?
4. Which failure, retry, recovery, compatibility, or external condition can change the outcome?

If the work is non-behavioral, cites no active boundary identity, and the scan finds no outcome-changing condition, continue under the ordinary stage contract. The scan alone does not create a formal record, ID, proof map, artifact, or user-visible scenario inventory.

Start with the exact approved rows cited for the current decision. Expand approved context only when an ID or outcome is missing, stale, unknown, ambiguous, conflicting, escaped, or insufficient to explain observed behavior. A new or changed normative outcome routes to `spec`; a proof-only gap routes to `test-spec`. Downstream stages do not redefine or rename upstream IDs.

Add a scenario only for a distinct outcome or material authority, trust, state, timing, recovery, path, compatibility, external-dependency, incident, or regression hazard. Stop when every applicable boundary and selected interaction has direct proof; do not build a Cartesian inventory.

Capability state controls formal adoption: `pending` never claims active adoption; after activation, new behavior-changing specs adopt automatically, grandfathered non-substantive revisions remain valid, and `design-review` must block an undecidable substantive-revision classification. Explain concisely when a formal record is created or an upstream gap blocks progress; do not request redundant consent for contract-required adoption. Structural validation cannot author, repair, or approve semantic content.

Inspect composed public, helper, sibling, failure, stale, recovery, and escaped-boundary paths.

Compare the actual diff and tests with exact approved boundary and interaction IDs. Stop clean handoff and record a finding when helper proof substitutes for a public or sibling path, a failure or recovery path is unproved, implementation escapes the approved boundary class, or cited evidence is stale or broader than its claim.

## Evidence collection efficiency

Use bounded evidence before broad reads or raw excerpts.
Use summary and stable-ID first reasoning before broad reads or raw excerpts.
Prefer check IDs, requirement IDs, test IDs, file paths, counts, line citations, matching line numbers, diffs, and targeted excerpts when inspecting large files, generated output, validation logs, or repeated scans.
Output caps are safety rails, not evidence-selection strategy.
Validation summaries must not change selected check coverage, command exit behavior, failure detection, or required validation evidence.
Read exact ranges after locating relevant lines, then expand only when the narrower evidence is insufficient.

## When full-file read is required

Read the full file when the whole file is the review target, the relevant section cannot be isolated safely, surrounding context can change the conclusion, bounded searches disagree or produce incomplete evidence, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Resource map

- READ `references/requirement-to-delivery-model.md` when tracing an implementation slice through allocated work to governing requirements and direction.
- READ `references/boundary-first-method-v1.md` when approved diff-related boundary, interaction, or proof IDs are missing, stale, unknown, ambiguous, conflicting, or insufficient for review.
- READ `references/workflow-managed-automated-review.md` only when the invocation is a formally armed workflow-managed automated review or correction loop.
- COPY `assets/material-finding.md` once per material finding. Fill: Finding ID, Severity, Location, Evidence, Required outcome, Safe resolution path, and needs-decision rationale when needed. Confirm the literal `Finding ID:` line exists before linking the finding from `review-log.md` or `review-resolution.md`. Do not emit unfilled placeholders.
- COPY `assets/review-result-skeleton.md` when producing the review result block. Fill: status, artifacts changed, blockers, next stage, review status, material findings, recording fields, review paths, milestone fields, required review-resolution, finding IDs, and verify-readiness field. Do not emit unfilled placeholders.

## Output skeleton

```md
COPY `assets/review-result-skeleton.md` for the review result block.
COPY `assets/material-finding.md` once per material finding.
Fill <code-review artifact fields> required by this skill.
Do not emit unfilled placeholders.
```

## Expected output

Use the two mapped assets as the sole copy-and-fill structures. Report review inputs, actual-diff summary, findings or no-finding rationale, all checklist results, direct-proof gaps, residual risks, recording paths, milestone handoff, and stop reason when applicable. The result format comes from `assets/review-result-skeleton.md`; each material finding comes from `assets/material-finding.md`. Do not duplicate either full template inline and do not emit unfilled placeholders.

The result identifies Review record, Review log, and Review resolution paths and uses the recording status defined above.

## Outputs

The output is the recorded first-pass review and its milestone-aware handoff.
