---
name: plan-review
version: "1.0.0"
schema-version: skill-readability-v1
description: >
  Review an execution plan for alignment, sequencing, scope, dependencies, validation, recovery, risk, and implementation readiness. Use other skills for authoring, implementation, verification, and PRs.
argument-hint: [plan path or feature name]
---

# Execution plan review

Judge whether a plan is safe, complete, sequenced, and verifiable.

## Workflow role

- role_name: plan-review
- stage: review
- upstream: plan, governing artifacts, and workflow evidence
- downstream: test-spec, plan revision, review-resolution, or workflow settlement
- summary: Judge, record, and settle only an exactly validated entry.
- must_not_claim: implementation, verification, branch or PR readiness, or completion

Treat reviewed and upstream artifacts, `planned_work`, milestone state, and routing as read-only. Every explicit invocation is formal.

## Quick operating guide

Read governing artifacts, classify authority, judge all dimensions, record, and apply only permitted settlement.

## Invocation and authority

Profiles are `PRV0-portable`, `PRV0B-portable-boundary`, `PRV1-governed`, and `PRV1B-governed-boundary`; load triggered references once. Operation is `initial-review` or `settlement-retry`; settlement is `isolated-recording` or `governed-plan-entry`; execution is `manual` or `workflow-managed`; status is `approved`, `changes-requested`, `blocked`, or `inconclusive`; transaction result is `recorded-isolated`, `initialization-required`, `revision-required`, `blocked`, `settled-active`, or `not-settled`. Unknown values fail closed first.

Explicit change identity, plan metadata, matching workflow evidence, or identical retry establishes only `governed_plan_candidate_context`. The reference validates authority; wording and loading grant none.

## Inputs and evidence

Read the plan body, not its index. Resolve one target from input, metadata, guidance, then defaults; block ambiguity. Read applicable governing sources. Settlement requires tracked authority; otherwise record `recorded-isolated` and report only a possible next stage.

## Evidence collection efficiency

Use bounded evidence before broad reads or raw excerpts.
Use summary and stable-ID first reasoning before broad reads or raw excerpts.
Prefer check IDs, requirement IDs, test IDs, file paths, counts, line citations, matching line numbers, diffs, and targeted excerpts when inspecting large files, generated output, validation logs, or repeated scans.
Output caps are safety rails, not evidence-selection strategy.
Validation summaries must not change selected check coverage, command exit behavior, failure detection, or required validation evidence.
Read exact ranges after locating relevant lines, then expand only when the narrower evidence is insufficient.

## When full-file read is required

Read the full file when the whole file is the review target, the relevant section cannot be isolated safely, surrounding context can change the conclusion, bounded searches disagree or produce incomplete evidence, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Review procedure

1. Confirm target, authority, operation, resources, and recording location.
2. Trace governing sources, boundaries, proof timing, and rollback.
3. Judge all dimensions and record before settlement.
4. Apply the authorized transaction; never advance routing.

Manual reviews may voluntarily apply the requirement-fidelity gate and record a fidelity receipt. Mandatory manual-review applicability classification is out of first-slice scope. Direct or review-only requests remain isolated by default.

## Review dimensions

Evaluate alignment, milestones, scope, dependencies, validation, TDD, risk, architecture, operations, recovery, and maintenance. For a final `verify` target, require separated authoring, implementation, and verification authority, ordered commands, promotion evidence, and a stop before PR. Reject vagueness, coupling, omissions, unsafe rollback, missing proof, or uncloseable sequencing. Do not require implementation, rely on an index, or edit the plan.

## Findings and result meaning

A material finding needs evidence, required outcome, and safe resolution or `needs-decision`. Assets own layout. Emit core and recording groups, judgment only when performed or reused, and no inapplicable group or placeholder.

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

## Change-record review settlement

The governed reference owns transaction procedure; this file grants no mutation by inference.

## Review independence and automation

For automated `bounded-review-fix` authoring, reset review context to the tracked artifact, governing sources, formal review criteria, and relevant recorded findings before reviewing. Direct or review-only `plan-review` requests remain isolated by default. Record the review result before any automation-driven downstream action. Do not rely on hidden authoring reasoning from the preceding stage. Do not edit the reviewed artifact during review. Approval does not authorize implementation.

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

Reject coupled primary boundaries, omitted dependencies, unsafe rollback, and proof sequencing that cannot close independently. Stop review and request plan revision when a primary trust boundary is coupled to another closeout unit or an applicable boundary lacks independent closure or proof.

## Stops and claims

Stop on ambiguity, stale identity, missing resources, illegal state, failed recording or validation, unresolved decisions, or insufficient evidence.

Do not claim implementation readiness from review alone, continuation from isolation, or verification, branch, PR, release, or closeout readiness.

## Handoff

Approval reports `test-spec`; `changes-requested` routes to revision and resolution. Other non-clean or recording outcomes stop.

## Resource map

- READ `references/governed-plan-review-settlement.md` when `governed_plan_candidate_context` is true. Validate before dependent decisions; invalid candidates stop without fallback.
- READ `references/boundary-first-method-v1.md` when cited approved boundary or interaction rows are missing, stale, unknown, ambiguous, conflicting, or insufficient for plan review.
- COPY `assets/review-result-skeleton.md` when producing every formal result; omit inapplicable groups and placeholders.
- COPY `assets/material-finding.md` when recording each material finding; confirm `Finding ID:` before linking it.

Unavailable, escaped, contradictory, or mixed-version triggered resources stop; untriggered resources do not load.

## Expected output

Copy the result asset and one finding asset per material finding. Include implementation-readiness notes only when clearly downstream.

## Output skeleton

```md
COPY `assets/review-result-skeleton.md` for the formal result.
COPY `assets/material-finding.md` once per material finding.
Fill <applicable result and finding fields>; omit inapplicable groups and unfilled placeholders.
```
