---
name: proposal-review
version: "1.0.0"
schema-version: skill-readability-v1
description: >
  Review a concise proposal and its embedded feasibility evaluation before Design. Use when the user asks whether a direction is valuable, bounded, feasible, vision-aligned, and specific enough to pursue without prematurely settling downstream decisions. Use proposal to write proposals; use design-review, delivery-review, code-review, verify, or pr for later gates.
argument-hint: [proposal path, feature idea, or review focus]
---

# Proposal review

Independently answer: **Does this proposal provide enough evidence for a responsible decision about whether to pursue the direction?** Do not rubber-stamp formatting or demand information owned by Design or Delivery.

Judge whether the proposal responsibly refines the incoming RR into an IR-level direction sufficient for Design.

## Workflow role

- role_name: proposal-review
- stage: review
- upstream: proposal artifact plus user intent when available
- downstream: proposal revision, accepted proposal, or isolated stop before architecture and specification
- summary: Review proposal direction, scope, risk, and feasibility as one decision.
- ownership: Write review evidence and, with exact formal authority, settle only the matching proposal entry. Route owns semantic routing and continuation.
- must_not_claim: spec completion, implementation review, final verification, branch readiness, PR readiness, or automatic downstream handoff

Do not edit the proposal unless the user explicitly requests a combined review-and-revision action. Record the first-pass review before any separately authorized correction.

## Invocation classification

Classify two independent modes from current evidence before side effects.

Recording mode is exactly `none`, `advisory-durable`, or `formal-lifecycle`. Automation mode is exactly `manual` or `workflow-managed-automated`. The only valid pairs are `none/manual`, `advisory-durable/manual`, `formal-lifecycle/manual`, and `formal-lifecycle/workflow-managed-automated`; unknown, missing, contradictory, and other pairs stop before dependent work.

`durable_recording_context` is true for a formal lifecycle review, explicit durable-record request, material finding, or status `changes-requested`, `blocked`, or `inconclusive`. A late trigger reclassifies and loads recording procedure before any dependent write or recording claim. Loading procedure never grants settlement, automation, correction, or continuation authority.

Classify specialized predicates through proposal-review judgment, not deterministic prose inference:

- `vision_exception_context`: the review must decide or record an exception to current vision.
- `standing_artifact_context`: bootstrap or governance direction depends on a missing required standing artifact or an explicit bootstrap exception.
- `scope_budget_context`: broad or multi-workstream scope needs detailed work-item classification.

Apply every true predicate. Load the gates reference once for a non-empty set; late discovery completes before status, and unresolved ambiguity blocks approval.

Use exactly these resource assemblies:

| Assembly | Durable context | Specialized context | Loaded procedure |
| --- | ---: | ---: | --- |
| `PRR0-core` | no | no | `SKILL.md` and result asset |
| `PRR0G-context-gated` | no | yes | core plus conditional gates |
| `PRR1-recorded` | yes | no | core plus recording procedure |
| `PRR1G-recorded-context-gated` | yes | yes | core plus both references |

## Review inputs and evidence

Read the complete proposal and original intent first. Add only evidence the proposal relies on: standing authority, linked research or artifacts, workflow guidance, or current code. Use prior review evidence for prior findings, and read complete `change.yaml` only for formal settlement, reconstruction, dispute, or whole-record review.

## Project-local evidence

Public skills operate in customer-project mode by default. Use project-local evidence and portable defaults; do not require RigorLoop repository-internal files outside this repository. Consume authoritative CLI workflow context for governed routing or placement and block on ambiguity.

## Evidence access

Default evidence:

- proposal under review
- user's original request or initial intent
- `VISION.md` or `CONSTITUTION.md` when standing gates or vision fit matter

Conditional evidence:

- linked specs, ADRs, plans, or learn sessions when the proposal relies on them
- authoritative CLI workflow context when governed workflow behavior or artifact placement is proposed
- code only when the proposal depends on current implementation reality

Bounded discovery is not evidence expansion. Record a compact reason only when reading substantive evidence outside the default and triggered conditional set. Expand further only when bounded evidence is incomplete, contradictory, or insufficient.

## Artifact placement

When operating inside the RigorLoop repository, formal proposal-review records default to `docs/changes/<change-id>/reviews/proposal-review-r<n>.md` and are indexed in `docs/changes/<change-id>/review-log.md`. Use `docs/changes/<change-id>/review-resolution.md` only when material findings, blocking outcomes, or accepted dispositions require it.

If formal review lacks a change pack, create or request `docs/changes/<change-id>/` before claiming `Recording status: recorded`. For an isolated advisory review without a durable trigger, do not create lifecycle artifacts.

## Core review contract

Judge every proposal across:

| Dimension | Question |
| --- | --- |
| Challenge | Is the current insufficiency clear, material, and framed before the solution? |
| Goals | Do outcome-oriented goals address the challenge without dictating downstream design? |
| Scope | Are included work, exclusions, and major boundaries clear enough to prevent silent expansion or narrowing? |
| Governing principle | Is it sound, brief, and independent of implementation detail? |
| Direction | Is the high-level direction concrete enough to approve and reasonably supported by the preceding reasoning? |
| Feasibility | Is there one proportionate credible assessment with evidence or bounded assumptions, constraints, and blockers explicit? |
| Material impact | Are consequences that could change approval disclosed, without requiring a routine impact section? |
| Vision alignment | Does the direction align with `VISION.md`, or is a material conflict, revision, or bootstrap decision explicit? |
| Downstream authority | Do behavior, architecture, APIs, sequencing, proof design, and rollout mechanics remain with Design or Delivery? |
| Requested decision | Is the direction-level decision and its limits explicit? |

Use `pass`, `concern`, or `block`. Judge decision sufficiency and proportionality, not maximum available information. No fixed word count, length, or token budget applies.

### Feasibility

Require exactly one embedded `Feasibility` section with an assessment, basis, constraints, and blockers. Treat supporting research as input, not as a separate proposal artifact or gate. A missing, unsupported, contradicted, materially stale, or blocking evaluation requires proposal revision and cannot authorize architecture or specification authoring. Approval confirms only that the direction is valuable, bounded, and feasible enough for design work; it does not approve detailed behavior, architecture, delivery, implementation, or proof adequacy.

### Vision alignment

Compare the direction with current `VISION.md` and record exactly one outcome in review evidence: `aligned`, `material-conflict`, `vision-revision-requested`, or `no-vision-bootstrap`. Routine alignment belongs only in review evidence; do not request a `Vision fit` section.

A material conflict, requested vision revision, or bootstrap exception that could affect approval must be disclosed in `Impact and major trade-offs` and made explicit in `Decision requested`. Withhold approval when that disclosure or the required owner decision is absent. Load specialized procedure only for `vision_exception_context` or `standing_artifact_context`.

## Scope preservation review

Compare the user's initial request with the proposal. Each material goal must remain visible in goals, scope, or the requested decision. For a broad request, an `initial goal treatment` of `in scope`, `out of scope`, `deferred follow-up`, `rejected option`, or `open question` may make the boundary explicit inside `Scope and non-goals`.

Return `changes-requested` if any initial user goal disappears. Return `changes-requested` if a deferred goal has no follow-up. Return `changes-requested` if a rejected goal has no rationale. Return `changes-requested` if the proposal narrows scope but does not say why. Scope-preservation failures must return `changes-requested`.

Do not rewrite the proposal as part of proposal-review unless the user explicitly asks.

For ordinary scope, judge silent narrowing and hidden follow-up inline. Load detailed classification only when `scope_budget_context` is true.

Report the scope-preservation result in the mapped result asset.

## Material findings and status

Every material finding includes Finding ID, Severity, Location, Evidence, Required outcome, and Safe resolution path or a `needs-decision` rationale naming the decision and owner. Copy the finding asset once per material finding. A material finding is a required change or decision, not a quota.

Use exactly one review status: `approved`, `changes-requested`, `blocked`, or `inconclusive`. Approval locks only the accepted challenge, goals, scope and non-goals, governing principle, high-level direction, sufficient feasibility, and disclosed proposal-level impacts. It authorizes architecture and specification authoring only, not that either artifact exists or is approved. Use `changes-requested` for actionable proposal or feasibility defects, `blocked` for an authority, feasibility blocker, or owner decision, and `inconclusive` when evidence supports neither approval nor an actionable finding.

A direction that is too vague to approve is a material finding. Content that prematurely settles a detailed Design or Delivery decision is also a material finding. Proposal Review must not create a finding solely because downstream detail or a routine impact section is absent.

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

## Isolation and handoff

Direct and review-only requests remain isolated. `advisory-durable` never settles or reports formal eligibility; `formal-lifecycle` settles only the exact same-change proposal entry after recording and never advances workflow. Only `formal-lifecycle/workflow-managed-automated` uses automation procedure before returning control to workflow.

Direct or review-only `proposal-review` requests remain isolated by default.

## Stop conditions and claims

Stop on unresolved target or identity, missing or stale authority, unsafe or failed writes, ambiguous specialized predicates, contradictory package procedure, missing triggered resources, or an owner decision. Keep complete findings visible when recording is blocked.

Do not claim spec completion, downstream execution, implementation review, verification, branch or PR readiness, or automatic handoff. Do not infer that recording grants settlement, settlement grants continuation, or package loading grants authority.

## Resource map

- READ `references/requirement-to-delivery-model.md` when tracing an incoming need through proposal direction or downstream Design handoff.
- READ `references/proposal-review-recording-and-settlement.md` exactly when `durable_recording_context` is true. Stop before dependent writes, settlement, automation, or recording claims if it is missing or unreadable.
- READ `references/conditional-proposal-gates.md` exactly when one or more specialized predicates are true. Apply every true predicate and load the reference once.
- COPY `assets/review-result-skeleton.md` for every proposal-review result. Fill: the core group and only the specialized-gate, durable-recording, formal-settlement, and automated-review groups selected by current classification. Do not emit unfilled placeholders.
- COPY `assets/material-finding.md` once per material finding. Fill: Finding ID, Severity, Location, Evidence, Required outcome, Safe resolution path, and needs-decision rationale. Confirm the literal `Finding ID:` line exists before linking it. Do not emit unfilled placeholders.

When a trigger is false, do not load its reference. Any missing, unreadable, escaped, contradictory, or mixed-version required resource stops dependent work. Do not reconstruct procedure or layout from memory.

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

Copy the result asset with the core and applicable conditional groups. Omit inapplicable groups; report unavailable required data as `blocked` or `unknown` with its blocker. Assets own layout only; skill procedure owns meaning and authority.

## Output skeleton

```md
COPY `assets/review-result-skeleton.md` for the review result.
COPY `assets/material-finding.md` once per material finding.
Fill <core and applicable conditional groups> required by this skill.
Do not emit unfilled placeholders.
```
