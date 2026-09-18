---
name: code-review
version: "1.0.0"
schema-version: skill-readability-v1
description: >
  Review a milestone or the final whole change against the actual diff, approved design and delivery packages, tests, and validation evidence, then record findings or a clean first-pass review. Use after implement hands off a milestone, after all milestones for fresh final Code Review, or when implementation review is requested. Use design-review, delivery-review, verify, or pr for those gates instead.
argument-hint: [branch, diff, plan path, spec path, or feature name]
---

# Independent implementation review

## Workflow role

- role_name: code-review
- stage: review
- upstream: implementation diff, review-requested milestone, governing artifacts, tests, and validation evidence
- downstream: review-resolution, next implementation milestone, or final closeout sequence
- summary: Perform independent implementation review, record the first-pass status and findings, and return the outcome to route.
- ownership: Write review evidence only. Route owns milestone and routing state; code-review does not edit implementation, plans, artifact settlement, or change-local routing.
- must_not_claim: branch readiness, PR readiness, final verification, CI success, implementation fixes, or derived-artifact currency without separate owning evidence

It must not edit implementation, the plan, artifact settlement, milestone state, or routing.

## Scope

Trace the implementation to its allocated work, governing SRs, and approved design boundaries. Review in independent-review mode against the actual diff. Passing tests or plausible code alone is insufficient. Use this after implementation handoff or for an explicit diff review; proposal, Design, Delivery, Verify and PR gates retain their owners. Record findings before any fix; do not author the reviewed target.

## Invocation classification

Identify the exact review target and whether this is isolated advisory work, a governed milestone review or final whole-change review before loading conditional procedure. Direct or review-only requests remain isolated unless continuation is separately authorized; isolation never suppresses required recording.

Classify `governed_recording_context` independently using the Recording boundary below. Formal lifecycle review needs current exact authority and durable evidence; an advisory judgment cannot settle a gate. Apply adopted assessment/reliance guidance under its own triggers. Manual review does not acquire automation prerequisites: load `workflow-managed-automated-review.md` only for a formally armed supported workflow-managed automated review or correction loop. Loading cannot arm it or restore a retired adapter. Missing, stale, unknown, conflicting or ambiguous required authority stops dependent judgment or writes. Reassess late triggers before dependent action.

## Recording boundary

`governed_recording_context` means the project has adopted the RigorLoop Record Format and explicitly selected a change requiring its current recording profile. It is independent of planned or armed execution and does not mean every durable advisory result uses a governed store.

Read `references/governed-code-review-recording.md` before dependent recording, including when the trigger becomes true later. Select the actual `rigorloop-records-v3` contract; malformed, stale, conflicting or ambiguous governed signals stop affected writes without portable fallback. Missing, unreadable, escaped, stale or mixed-version required resources stop dependent work; do not reconstruct them. Untriggered resources do not block unrelated runtime work.

Loading or saving grants no approval, readiness or continuation. Preserve exact subjects, other actors' decisions and unresolved origins; use the mapped procedure for scoped reads, targeted writes, applicability and conflict/recovery. Project-selected recording outside this profile keeps its own authority.

## Test criteria application

When the project explicitly adopts shared test criteria, use the selectively loaded guidance below for test quality and maintenance. These criteria replace source-local shared test-purpose, case-selection and maintenance criteria for adopted work; retain specialist methods and historical evidence. Actual judgments, evidence applicability and closeout consequences remain with the responsible assessors under the project's review policy.

## Review and Closeout application

When project authority explicitly adopts Review and Closeout policy, use the packaged application below for shared assessment meaning. It replaces source-local judgment, independence, applicability, concern-disposition and closeout rules in this skill and its conditional resources; retain specialist methods and contract-selected storage procedures. Historical assessments retain their original meaning but grant no current runtime support. Missing or contradictory required guidance stops dependent reliance.

## Review authority and evidence

For mixed-evidence assessments, apply the packaged judgment rule: retain supported findings while exposing missing or contradictory assessment basis.

Inspect the actual changed files, staged or unstaged diff, commit range, PR diff, or other explicit target. Read the approved spec, stable plan milestone, relevant architecture or ADR, related tests, named validation evidence. For planned work, read `change.json` for current milestone and handoff state and use the plan only for stable intent. Use registered findings, their dispositions and material decisions for prior concerns.

For work governed by consolidated gates, require the current approved Design Review ID and its exact member map plus the current approved Delivery Review ID and its exact member map. Treat review-required, partial, stale, or historical artifact-review evidence as non-authorizing. These package inputs strengthen implementation review but do not merge Code Review with Design Review, Delivery Review, or Verify.

Use the smallest sufficient evidence set. Begin with the diff, spec, test spec, milestone, tests, and validation. Add architecture, governance, related code, generated output, or history only when the reviewed behavior or an evidence conflict requires it. Record why substantive evidence outside that set was needed. Full-file reading is appropriate when the whole file is the target or bounded evidence is incomplete, contradictory, or context-sensitive.

Apply the adopted assessment application for actual nonauthor independence. A separate session is useful only with concrete contributor separation. Historical assumption-reset assessments remain archival evidence and cannot establish current independent approval.

## Generated Markdown readability

When this skill creates or updates generated or generator-shaped Markdown:

- Write ordinary prose as normal Markdown paragraphs. Do not split a sentence across physical source lines merely for wrapping or clause separation; multiple sentences may remain in one paragraph.
- Preserve stable IDs for requirements, findings, commands, milestones, and evidence; use tables for repeated mappings.
- Keep commands fenced or table-owned when they carry proof.
- Diagrams are optional. Use them only when they reduce cognitive load and map to real artifacts, stages, components, actors, or states.
- Do not require manual-proof contracts from this readability guidance alone; use governing project rules when manual proof is otherwise required.

## Artifact placement

Use the explicit user path first, then authoritative CLI workflow context, the active change record, plan, reviewed artifact, or current metadata, followed by governing specs or schemas for exact shape. Use a portable default only when no project-local owner exists; block on remaining ambiguity. Do not broad-search authoritative documents merely to find paths.

## Operating sequence

1. Identify the target, tracked authority, milestone, remaining milestones, and any explicit isolation or stop instruction.
2. Reset assumptions, inspect the actual diff, and map changed behavior to the governing requirements and boundary or interaction IDs.
3. Inspect tests and direct proof for public, sibling, helper, failure, recovery, compatibility, generated, and external paths that can change the outcome.
4. Challenge whether the selected checks and validation evidence are relevant and sufficient; do not confuse passing checks with compliance.
5. Apply every checklist item, choose one native status, and record findings or an evidence-backed no-finding rationale before any fix begins.
6. Record the formal review, then report the milestone-aware handoff to `route`. Rereview every changed implementation after resolution.

## First-pass checklist coverage

Evaluate each item as `pass`, `concern`, or `block` and cite concrete evidence:

1. Spec alignment: approved scope, requirements, examples, and non-goals.
2. Test coverage: changed behavior, regressions, and named failure paths. Under adopted test criteria, apply the [selection method](references/test-quality.md#select-requirements-and-proof) to the actual assertions, fixture state, native discovery and observation boundaries. Check requirement and parent-interaction protection against plausible defects, preserve useful unlisted regressions, and distinguish inspected realization from gaps. Counts, timings and links cannot establish adequacy or justify lost protection.
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

Use one first-pass status: `approved`, `changes-requested`, `blocked`, or `inconclusive`. Apply the packaged assessment policy for their meaning and combined conditions. An isolated advisory conclusion does not claim governed gate approval or continuation authority.

Use severity `blocker`, `major`, `minor`, `nit`, or `positive`. A material finding is a required change or decision, not a quota. Every material finding must include Finding ID, Severity, Location, evidence, required outcome, and a safe resolution path or `needs-decision` rationale naming the decision and owner. Apply the shared combined-condition rule and preserve supported findings under blocked or inconclusive judgments.

## Isolation and Recording

The following recording procedure applies the selected recording interface. Use packaged assessment and reliance guidance for the judgment and its consequences.

Isolation governs handoff. Recording follows formal review triggers.

A direct or review-only request remains isolated by default: it does not automatically continue into downstream workflow stages.

Isolation does not suppress recording.

Every formal lifecycle review result must be recorded or explicitly blocked.

Use:

- `Recording status: recorded` when the required review evidence was created or updated.
- `Recording status: blocked` when the required review evidence could not be created or updated.

`not-required` is reserved for non-formal review-like requests outside the formal lifecycle review model.

Do not merely tell the user that review artifacts should be created. Create or update them before final output, or report `Recording status: blocked` with the blocker and smallest next action.

For an isolated review with material findings, the final review output must state:

- no automatic downstream handoff
- material Finding IDs
- required review record path
- whether the record must be created before fixing or reconstructed
- whether owner decision is needed

## Direct proof and rereview

A clean conclusion for a named edge case requires direct proof from a targeted test, targeted validation output, or an allowed explicit manual verification note. Code-shape inference alone is insufficient. For validation routing, targeted proof names the selected or executed checks; broad smoke remains a separate trigger-owned obligation.

Apply the packaged reliance guidance for adopted reassessment and final whole-change scope. Historical contracts retain changed-implementation rereview and holistic review of the complete final diff and cross-milestone interactions; milestone-local review alone is not whole-plan readiness.

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
- Normal next stage: report the review outcome to `route`, which routes from change-local state.
- Conditional next stages: review-resolution, the next implementation milestone, final closeout, or a stop.

## Status and milestone handoff

Identify milestone versus final whole-change scope in the judgment. Return the outcome to `route`; Code Review writes evidence, and `route` owns milestone/routing changes. An applicable clean non-final review permits only its own milestone closeout. Findings retain their correction owner even when the overall judgment is inconclusive. Blocked or inconclusive work stops the affected handoff for its named decision, constraint or missing proof.

After every implementation milestone and required correction, final closeout requires a fresh independent holistic Code Review of the complete final diff and cross-milestone interactions, any triggered CI maintenance and distinct `verify`. Milestone review never substitutes or jumps directly to final verification; only successful Verify produces the final explanation. Apply adopted reliance policy when selected; portable review retains its isolated scope, changed-implementation rereview and complete-final-diff assessment without claiming governed authority. Historical contracts grant no current route.

The output names the reviewed milestone when applicable, native status, milestone closeout, required resolution, remaining milestones, next stage and final closeout readiness with reason. The assets retain their applicable fields.

## Boundary-first method

Run this compact scan before any stage-owned decision that can change observable behavior, and whenever the input cites an active boundary contract or stable boundary, interaction, or proof ID. Do not wait for the user to name the method.

1. Which inputs or actors can change the outcome?
2. Which state or timing conditions can change the outcome?
3. Which public, sibling, helper, or alternate path can change the outcome?
4. Which failure, retry, recovery, compatibility, or external condition can change the outcome?

If the work is non-behavioral, cites no active boundary identity, and the scan finds no outcome-changing condition, continue under the ordinary stage contract. The scan alone does not create a formal record, ID, proof map, artifact, or user-visible scenario inventory.

Start with the exact approved rows cited for the current decision. Expand approved context only when an ID or outcome is missing, stale, unknown, ambiguous, conflicting, escaped, or insufficient to explain observed behavior. A new or changed normative outcome routes to `design`. A pre-implementation verification-allocation gap routes to `plan`. Historical contracts grant no current progression authority. Downstream stages do not redefine or rename upstream IDs.

Add a scenario only for a distinct outcome or material authority, trust, state, timing, recovery, path, compatibility, external-dependency, incident, or regression hazard. Stop when every applicable boundary and selected interaction has direct proof; do not build a Cartesian inventory.

The project's selected contract owns formal adoption and document format. Unknown current model markers and malformed records fail structural validation. Feature/proof operations are unsupported; existing documents may be read as sources, and scoped adoption requires explicit project authority. Do not infer adoption from a historical activation snapshot or from installing a skill. Explain concisely when a formal record is required or an upstream gap blocks progress; do not request redundant consent for contract-required work. Structural validation cannot author, repair, or approve semantic content.

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

- READ `references/governed-code-review-recording.md` when `governed_recording_context` is true, before dependent recording.

- READ `references/test-quality.md` when adopted criteria apply and this invocation authors, allocates or assesses test obligations.
- READ `references/test-maintenance.md` when adopted criteria apply and this invocation changes tests or assesses test maintenance, removal or its impact.

- READ `references/review-reliance.md` when applying adopted assessment applicability, correction or closeout policy.
- READ `references/review-assessment.md` for every review under explicitly adopted Review and Closeout policy.

- READ `references/requirement-to-delivery-model.md` when tracing an implementation slice through allocated work to governing requirements and direction.
- READ `references/boundary-first-method-v1.md` when approved diff-related boundary, interaction, or proof IDs are missing, stale, unknown, ambiguous, conflicting, or insufficient for review.
- READ `references/workflow-managed-automated-review.md` only when the invocation is a formally armed workflow-managed automated review or correction loop.
- COPY `assets/material-finding.md` once per material finding. Fill: Finding ID, Severity, Location, Evidence, Required outcome, Safe resolution path, and needs-decision rationale when needed. Confirm the literal `Finding ID:` line in the presentation aid; preserve exact finding identity and any origin required by the selected contract when recording it. Do not emit unfilled placeholders.
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

The result identifies the review record and finding references and reports the recording outcome separately from the judgment.
