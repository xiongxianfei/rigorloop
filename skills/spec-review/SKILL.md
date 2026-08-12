---
name: spec-review
version: "1.0.0"
schema-version: skill-readability-v1
description: >
  Review a feature spec before architecture, test planning, planning, or implementation. Use when the user asks to challenge requirement clarity, normative language, completeness, testability, examples, compatibility, observability, security/privacy, non-goals, acceptance criteria, or readiness. Use spec to write specs; use proposal-review, architecture-review, plan-review, code-review, verify, or pr for those stages.
argument-hint: [spec path or feature name]
---

# Spec review

Independently review a feature specification as a formal contract gate. Produce durable evidence or report blocked recording. Explicit feedback requesting no formal status, readiness, record, or lifecycle use belongs outside `spec-review`.

## Workflow role

- role_name: spec-review
- stage: review
- upstream: feature spec, linked proposal, exploration, research, local contracts, and workflow evidence
- downstream: spec revision, review-resolution, architecture, plan, no handoff, and eventual test-spec readiness assessment
- summary: Review the feature spec and record approval, changes requested, blockers, or inconclusive state.
- ownership: Write formal review evidence and, with exact governed authority, settle only the matching spec entry. Workflow owns routing and continuation.
- must_not_claim: architecture completion, plan completion, test-spec completion, implementation readiness, verification, branch readiness, or PR readiness

Do not edit the specification unless explicitly asked for combined review and revision. Record first-pass review before any authorized correction.

## Invocation classification

Classify before conditional loading or mutation. Settlement mode is exactly `isolated` or `governed-spec-entry`; governed mode requires one current `stage-owned-change-local-v1` change, specification, and matching reviewable entry. Recording and direct wording never grant governed authority.

Automation mode is exactly `manual` or `workflow-managed-automated`; automated mode requires current same-change and same-entry authorization and implies governed mode. Conversation, stale evidence, and recording-only roots do not arm automation.

unknown, missing, stale, contradictory, or ambiguous classification evidence fails closed before governed loading, settlement, automation, or dependent claims.

Use exactly these profiles:

| Profile | Settlement | Boundary procedure | Loaded resources |
| --- | --- | ---: | --- |
| `SR1-isolated-formal` | isolated | no | `SKILL.md` and result asset |
| `SR1B-isolated-formal-boundary` | isolated | yes | SR1 plus applicable boundary references |
| `SR2-governed-formal` | governed | no | SR1 plus governed reference |
| `SR2B-governed-formal-boundary` | governed | yes | SR1 plus governed and applicable boundary references |

Add the finding asset once per material finding. Automation stays inside SR2/SR2B. Load each resource once; availability never grants authority.

## Review inputs and evidence

Read the complete specification first, then only relied-on intent, proposal, instructions, contracts, architecture, and workflow evidence. Use project guidance for routing and placement. Read code only to confirm claimed current behavior.

## Artifact placement

Use project-local placement. In RigorLoop, formal spec-review records default to `docs/changes/<change-id>/reviews/spec-review-r<n>.md` and `docs/changes/<change-id>/review-log.md`; use `docs/changes/<change-id>/review-resolution.md` only when disposition is required.

Resolve placement in this order: explicit valid path or change ID; existing active owning root; reviewed-artifact metadata; project workflow guide; portable generated `YYYY-MM-DD-<subject>-review-recording` root. Stop on ambiguity, unrelated-root collision, unsafe placement, or write failure.

A fallback contains only recording metadata, review evidence, the log, and conditional resolution. It grants no settlement, plan, routing, lifecycle, or automation authority.

Create or request the recording change pack before claiming `Recording status: recorded`. Explicit critique routed outside `spec-review` creates no formal recording and no lifecycle artifacts.

Create and log a clean receipt without empty resolution. Material or blocking results use a detailed record and conditional resolution. Reconcile identical interrupted writes once; conflicting review-ID reuse stops.

If placement or writing fails, the judgment may remain visible, but report `Recording status: blocked`, the exact blocker, and smallest next action. Do not claim formal completion, settlement, or continuation. Recording never grants settlement authority.

## Core review contract

Evaluate each dimension with `pass`, `concern`, or `block`.

| Review dimension | Verdict |
| --- | --- |
| requirement clarity | `<review dimension verdict>` |
| normative language | `<review dimension verdict>` |
| completeness | `<review dimension verdict>` |
| testability | `<review dimension verdict>` |
| examples | `<review dimension verdict>` |
| compatibility | `<review dimension verdict>` |
| observability | `<review dimension verdict>` |
| security/privacy | `<review dimension verdict>` |
| non-goals | `<review dimension verdict>` |
| acceptance criteria | `<review dimension verdict>` |

Check relevant normal, empty, boundary, error, permission, migration, rollout, rollback, old-client, and old-data behavior. Acceptance must be observable. Reject vague `MUST` requirements and examples treated as exhaustive; do not review plans or code or demand irrelevant implementation detail.

Severity is `blocking` for unsafe guessing, `major` for important pre-implementation gaps, and `minor` for non-blocking clarity. Every material finding has evidence, required outcome, and safe resolution or owner-naming `needs-decision` rationale.

## Routing and testability assessment

Use exactly one review status: `approved`, `changes-requested`, `blocked`, or `inconclusive`.

`Immediate next stage` is `spec revision`, `review-resolution`, `architecture`, `plan`, or `none`; never `test-spec`. Approved uses required unsettled `architecture`, otherwise `plan`; changes requested uses revision or resolution; blocked uses resolution or none; inconclusive uses none.

`Eventual test-spec readiness` is `ready`, `conditionally-ready`, or `not-ready`. A result is approved only when `Eventual test-spec readiness` is `ready` or `conditionally-ready`; name the condition. Other statuses use `not-ready`.

Missing required inputs produce `Review status: inconclusive`, `Immediate next stage: none`, `Eventual test-spec readiness: not-ready`, and an exact stop condition. Workflow-managed approval routes first to recorded architecture assessment; `architecture-ambiguous` stops rather than selecting a path.

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

Use `assets/material-finding.md` for each material finding block.

Do not merely tell the user that review artifacts should be created. Create or update them before final output, or report `Recording status: blocked` with the blocker and smallest next action.

For an isolated review with material findings, the final review output must state:

- no automatic downstream handoff
- material Finding IDs
- required review record path
- whether the record must be created before fixing or reconstructed
- whether owner decision is needed

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

Judge applicability, boundary completeness, interactions, invariants, outcomes, and example ownership. Structural validation proves only shape, closed values, and references. Stop review with a material finding when semantic ownership is absent, a dimension is unjustifiably inapplicable, an interaction or outcome is missing, an example invents behavior, or a substantive revision has not adopted the contract.

## Stop conditions and claims

Stop on unresolved target identity, ambiguous review classification, unsafe or failed recording, missing or stale governed authority, conflicting resource procedure, missing triggered resources, illegal transition, or owner decision. Keep findings visible when recording is blocked.

Do not claim architecture, plan, test-spec, implementation, verification, branch, or PR completion. Direct reviews stop after recording. Governed reviews settle only their exact spec entry after recording and return control to workflow; the reviewer never advances routing.

Direct or review-only `spec-review` requests remain isolated by default.

## Resource map

- READ `references/governed-spec-review-settlement.md` exactly for `governed-spec-entry`, after authority is established. Settlement inside the reference waits for universal recording. Stop dependent settlement or automation if the reference is missing or unreadable.
- READ `references/boundary-first-method-v1.md` when reviewing a `boundary-first-v1` behavior contract.
- READ `references/boundary-first-feature-authoring-v1.md` when judging formal boundary-record completeness or a substantive grandfathered revision, after the method reference.
- COPY `assets/review-result-skeleton.md` for every formal result. Fill: the formal core and recording groups plus only applicable governed-settlement, boundary-review, and automated-review groups. Omit inapplicable groups; report applicable unavailable data as blocked or unknown with its blocker. Do not emit unfilled placeholders.
- COPY `assets/material-finding.md` exactly once per material finding. Fill: the fields defined in the asset, including Finding ID:, and confirm the literal `Finding ID:` line before linking it. Do not emit unfilled placeholders.

Do not emit unfilled placeholders. Any missing, unreadable, escaped, contradictory, or mixed-version triggered resource stops dependent work. Do not reconstruct procedure or layout from memory; an untriggered resource does not load or block.

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

Copy the result asset and applicable conditional groups, then the finding asset once per material finding. Assets own labels and layout only; this skill and its references own applicability, meaning, status, settlement, automation, and handoff.

Report Review record, Review log, Review resolution, material Finding IDs, exact wording suggestions, the immediate next stage, eventual test-spec readiness, and any stop condition.

Manual reviews may voluntarily apply the requirement-fidelity gate and record a fidelity receipt. Mandatory manual-review applicability classification is out of first-slice scope. Direct or review-only requests remain isolated by default.

## Output skeleton

```md
COPY `assets/review-result-skeleton.md` for the formal review result.
COPY `assets/material-finding.md` once per material finding.
Fill <core and applicable conditional groups> required by this skill.
Do not emit unfilled placeholders.
```
