---
name: test-spec-review
version: "1.0.0"
schema-version: skill-readability-v1
description: >
  Independently review an active test specification before implementation. Use to assess proof-map alignment, requirement and edge-case coverage, milestone mapping, validation commands, fixtures, automation versus manual evidence, and implementation handoff readiness. Use test-spec to author or revise the proof map; use code-review and verify for implemented tests and final evidence.
argument-hint: [test-spec path, change ID, or proof-review focus]
---

# Test spec review

Independently decide whether a test specification is an adequate, executable, and traceable proof map for its approved contract and plan.

## Workflow role

- role_name: test-spec-review
- stage: review
- upstream: active test spec, approved feature spec, approved architecture when required, approved plan, clean plan-review, and project-local workflow evidence
- downstream: implement, test-spec revision, upstream artifact revision, review-resolution when triggered, or isolated stop
- summary: Review proof-map completeness and implementation handoff readiness.
- ownership: Write review evidence and, in formal mode, settle only the matching test-spec artifact. Workflow owns routing and continuation.
- must_not_claim: test implementation, production implementation, code-review approval, validation success, branch readiness, PR readiness, or final lifecycle closeout

Do not author or rewrite the test spec, reapprove requirements, redesign architecture, re-sequence the plan, implement tests, or replace `code-review` or `verify`. Record first-pass findings before any separately authorized fix.

## Invocation classification

Classify lifecycle and handoff independently from authoritative evidence, not conversational wording.

Lifecycle mode is exactly:

- `formal`: exactly one active test-spec artifact resolves in a `stage-owned-change-local-v1` change record with current authoring evidence and lifecycle state requiring `test-spec-review`;
- `advisory`: a focused proof-map critique without formal settlement authority.

Handoff mode is exactly:

- `isolated`: direct, review-only, or lacking current workflow continuation authority;
- `workflow-managed`: current workflow authority selects this formal review for the same change.

| Lifecycle | Handoff | Validity |
| --- | --- | --- |
| `formal` | `isolated` | valid |
| `formal` | `workflow-managed` | valid |
| `advisory` | `isolated` | valid |
| `advisory` | `workflow-managed` | invalid; stop before review or routing |

Formal review may remain isolated. Advisory approval never establishes formal implementation eligibility. The `advisory + workflow-managed` pair is invalid.

Classify two additional predicates:

- `boundary_first_context`: governing feature or proof evidence makes `boundary-first-v1` applicable, or applicability is materially undecidable;
- `durable_recording_context`: formal review, a material finding, a blocking outcome, or an explicit durable-record request.

The four base assemblies are:

| Assembly | Loaded procedure |
| --- | --- |
| `TSR0-isolated` | `SKILL.md` |
| `TSR0B-isolated-boundary` | `SKILL.md` plus both boundary references |
| `TSR1-formal` | `SKILL.md` plus the recording overlay |
| `TSR1B-formal-boundary` | `SKILL.md`, both boundary references, and the recording overlay |

The recording overlay is the recording-and-settlement reference plus the result asset. Copy the finding asset exactly once per material finding.

## Review inputs and authority

Read the smallest sufficient authoritative set:

- target test spec and exact revision;
- approved feature spec and latest approving spec-review evidence;
- approved plan and latest clean plan-review evidence;
- approved architecture and architecture-review when required;
- current change record and workflow evidence when formal or workflow-managed;
- project guidance when routing, placement, or validation ownership matters.

Read existing tests, framework configuration, package or CI manifests, source, schemas, migrations, fixtures, API contracts, security policy, or compatibility policy only when the test spec makes a feasibility or existing-behavior claim that depends on them. Do not broadly review implementation code that does not yet exist.

Missing, stale, contradictory, mismatched, or ambiguous formal identity stops before settlement. Boundary applicability comes from governing evidence; the mere presence or absence of an ID in conversation is not authority.

## Operating sequence

1. Resolve target, lifecycle mode, handoff mode, boundary applicability, and initial resource assembly.
2. Read the approved contract, plan, target proof map, reviews, and only the conditional evidence needed to test feasibility.
3. Map requirements, examples, boundaries, interactions, milestones, commands, fixtures, and manual proof to direct evidence.
4. Challenge negative paths, failures, determinism, isolation, observability, scope, and execution economics.
5. Choose one status and record findings or a no-finding rationale before any review-driven correction.
6. If durable recording becomes true after review begins, load the overlay before final output. This does not change lifecycle mode, handoff mode, review status meaning, or implementation authority.
7. In formal mode, record first and run formal-only settlement. Then stop when isolated or return control to workflow when workflow-managed.

## Proof review contract

Universal review quality applies equally to advisory and formal review:

- requirement and acceptance-criterion traceability to automated tests, manual proof, or explicit not-applicable rationale;
- example, negative and failure coverage, including invalid state, permission, security, compatibility, migration, rollback, old-client, and old-data paths when relevant;
- proof-level adequacy across unit, integration, end-to-end, smoke, static, and manual evidence;
- milestone mapping so proof becomes active when it first becomes meaningful;
- command ownership, milestone, and classification as existing/configured, planned, manual-only, or external/release-owned;
- deterministic fixtures protected from order, shared state, network, time, randomness, and environment drift;
- manual proof with stable ID, automation rationale, exact steps, environment, evidence artifact, pass condition, failure condition, and owning stage;
- observability that identifies the requirement, case, command, or environment;
- scope fidelity and bounded execution economics.

A configured command is not evidence that it runs. Optional review-time checks are limited to side-effect-free resolution, help text, or dry run; do not set up fixtures, access secrets or network services, mutate data, or execute final validation during review.

Structural validity cannot establish proof adequacy. Record a material finding when direct proof is missing, helper-only proof substitutes for a required public or sibling path, negative partitions are omitted, command ownership is unclear, or manual evidence lacks an exact procedure.

## Status and routing

Use exactly one review status:

```text
approved
changes-requested
blocked
inconclusive
```

Use exactly one immediate next stage:

```text
test-spec revision
spec revision
architecture revision
plan revision
review-resolution
implement
none
```

Implementation handoff is exactly `allowed` or `not-allowed`.

- `approved` requires `Immediate next stage: implement` and `Implementation handoff: allowed`.
- `changes-requested`, `blocked`, and `inconclusive` require `Implementation handoff: not-allowed`.
- Use `changes-requested` for reviewable defects inside the test spec.
- Use `blocked` when missing or contradictory upstream authority prevents a valid review; route to its owning revision stage or `none`.
- Use `inconclusive` when evidence cannot support either an actionable finding or approval; use `Immediate next stage: none` and name the smallest needed evidence.
- Use `review-resolution` only for recorded findings requiring disposition.

Do not add a `conditionally-approved` result or lower the finding threshold because implementation is waiting.

## Staleness

An approved review becomes stale after a substantive test-spec change, including changed mappings, cases, commands, fixtures, manual proof, milestones, automation levels, criteria, or non-goal treatment. Confirmed formatting, typo, heading, reorder, or link-only edits do not automatically stale approval when proof obligations are unchanged. Implementation must not rely on stale approval.

## Material findings

Every material finding includes Finding ID, Severity, Location, Evidence, Required outcome, and Safe resolution path or a `needs-decision` rationale that names the decision and owner. A material feature with required failure behavior cannot be approved from happy-path-only proof.

Do not rewrite the test spec during review unless the user explicitly requests a combined review-and-revision action.

## Recording applicability and resource failure

Every formal review, material finding, blocking outcome, or explicit durable record request activates the recording overlay. A clean advisory review does not load it otherwise.

If a missing or unreadable triggered reference or asset prevents recording, keep every finding visible, report `Recording status: blocked`, name the expected path and smallest corrective action, and stop downstream handoff. A missing boundary resource stops the dependent proof judgment. The skill must not reconstruct missing procedure or layout from memory, combine mixed package versions, or continue with a partial overlay. An untriggered resource does not load and does not block review.

Loading a late recording overlay does not change lifecycle mode, handoff mode, review status meaning, or implementation authority. Advisory mode must not run formal-only settlement.

## Isolation and handoff

Isolation governs handoff, not recording. Direct or review-only requests remain isolated by default and never auto-start implementation. A clean formal isolated review may record `Implementation handoff: allowed` but still stops after its own settlement. Workflow-managed formal review returns control to workflow; the reviewer does not mutate routing, milestone state, or other artifacts.

Direct or review-only `test-spec-review` requests remain isolated by default.

## Stop conditions

Stop with `blocked` or `inconclusive` when the target or revision is missing, the test spec is inactive, the spec or required architecture is unapproved, the plan or plan-review is unapproved, upstream findings remain open, requirement or milestone identity is unresolved, command ownership is unknown, essential external or compatibility evidence is unavailable, sources conflict, required resources fail, or review identity is ambiguous.

Return `changes-requested`, not `blocked`, when the target remains reviewable and defects are inside the test spec.

## Claims this skill must not make

Do not claim tests were implemented or executed, validation passed, code review or verify passed, branch-ready, PR-ready, or final lifecycle closeout. Cite only evidence actually inspected. Advisory approval is not formal implementation authorization.

## Generated Markdown readability

Use semantic source lines for human prose, stable IDs for requirements, findings, commands, milestones, and evidence, and tables for repeated mappings. Keep proof-bearing commands fenced or table-owned. Use diagrams only when they reduce cognitive load and map to real entities. This guidance alone does not create a manual-proof contract.

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

Judge proof adequacy, negative coverage, fixtures, command ownership, and manual-proof boundaries.

Stop review with a material finding when an applicable boundary or selected interaction lacks direct proof, helper-only proof substitutes for a public or sibling path, negative partitions are omitted, command ownership is unclear, or manual evidence lacks an exact procedure.

## Evidence reading

Prefer stable IDs, paths, counts, line citations, diffs, and targeted excerpts. Output caps do not replace evidence selection. Read the full file when it is the review target or when surrounding context, conflicts, or incomplete bounded evidence can change the conclusion.

## Resource map

- READ `references/test-spec-review-recording-and-settlement.md` exactly when `durable_recording_context` is true.
- READ `references/boundary-first-method-v1.md` when reviewing a proof map governed by a `boundary-first-v1` feature record.
- READ `references/boundary-first-proof-v1.md` when judging proof-map completeness or proof adequacy, after the method reference.
- COPY `assets/review-result-skeleton.md` exactly when `durable_recording_context` is true. Fill: skill, review status, material findings, recording fields, review paths, blockers, immediate next stage, implementation handoff, and stop condition. Do not emit unfilled placeholders.
- COPY `assets/material-finding.md` when recording each material finding, exactly once per finding. Fill: Finding ID, Severity, Location, Evidence, Required outcome, Safe resolution path, and needs-decision rationale. Confirm the literal `Finding ID:` line exists before linking the finding from `review-log.md` or `review-resolution.md`. Do not emit unfilled placeholders.

## Output skeleton

```md
COPY `assets/review-result-skeleton.md` for a durable review result.
COPY `assets/material-finding.md` once per material finding.
Fill <test-spec review result and finding fields> required by this skill.
Do not emit unfilled placeholders.
```

## Expected output

Report lifecycle mode, handoff mode, boundary applicability, recording applicability, loaded resources, review status, findings or no-finding rationale, recording status and paths, blockers, immediate next stage, implementation handoff, stop condition, and claim limitations. Use the mapped assets only when their triggers apply; assets own labels and layout, never policy.
