---
name: spec
version: "1.0.0"
schema-version: skill-readability-v1
description: >
  Author observable feature contracts before delivery planning or implementation; Design Review approves the specification with architecture.
argument-hint: [proposal path, feature name, behavior request, or issue number]
---

# Feature spec authoring

## Workflow role

- role_name: spec
- stage: authoring
- upstream: accepted proposal or approved direction
- downstream: design-review after reconciliation with architecture and applicable ADRs
- summary: Author the contract.
- ownership: Write the spec and authorized governed evidence/transition.
- must_not_claim: Design Review approval, plan readiness, implementation readiness, verification, branch readiness, or PR readiness.

Portable work is isolated. Workflow-managed execution does not enlarge the `spec` write set.

## Purpose and evidence

Resolve placement from identity, metadata, contracts, guidance, then defaults. A relied-on proposal requires accepted settlement, no open finding or later contradictory review, and required closed resolution; treat upstream as read-only.

## Project-local evidence

Public skills use customer-project mode by default and project-local artifacts when present, including `docs/workflows.md` for local routing or placement. Do not require RigorLoop repository-internal artifacts in customer projects; use portable defaults or block on ambiguity.

## Invocation profiles and governed signals

Classify every invocation before mutation.

| Profile | Signal classification | Loaded procedure |
| --- | --- | --- |
| `SA0-portable` | `no-governed-signal` | Core plus both boundary references |
| `SA1-governed` | `single-governed-candidate` | SA0 plus governed reference |

Signals are `no-governed-signal`, `single-governed-candidate`, and `invalid-or-ambiguous-governed-signal`. Explicit change ID, workflow-managed identity, or structured owning-change field counts even when malformed; conversational references do not.

`no-governed-signal` is the only classification that permits portable authoring. `single-governed-candidate` requires safe, agreeing signals. Malformed, stale, duplicated, escaped, unsafe, missing-root, mismatched, or conflicting signals stop as invalid; governed failure must not fall back to portable authoring.

Loading selects procedure, not authority; validate before writing.

## Operations and portable authority

Operations are `create-primary-spec` and `revise-primary-spec`. Portable create needs an absent target and revise an existing exact target; conflict stops. Never overwrite an unrelated spec. Portable authoring writes only the spec artifact, never lifecycle, review, routing, or automation state.

## Contract quality

Treat the approved proposal direction as IR-level input and author stable SR identities for downstream traceability.

Answer: **What must be demonstrably true?** Make each applicable SR explicit enough for downstream verification planning. Cover normal behavior, invalid input, failure behavior, state transitions, permissions and authority, compatibility, migration, retries, concurrency, recovery, important system boundaries, important scenarios, and acceptance conditions. Explain inapplicability rather than forcing irrelevant categories.

Keep this contract behavioral. Do not normally prescribe test filenames, test frameworks, fixtures, mocks, exact validation commands, implementation-specific test mechanics, or milestone allocation. Those mechanics and allocations belong downstream; the specification owns the observable outcome they must preserve.

Also cover inputs, outputs, observability, security/privacy, accessibility, performance, and edges with normative, testable requirements. Examples illustrate but never own behavior, and the spec must not invent excluded scope. Preserve `Next artifacts`; use `Follow-on artifacts` for outcomes and `None yet` before any exist. A superseded spec identifies its replacement.

## Formal boundary composition

Both boundary references load initially; loading and formal-block emission are independent. The feature reference owns the block; the skeleton owns its position.

Block state is `absent`, `present-complete`, `present-incomplete`, `present-duplicated`, or `present-misplaced`; anchors are `unique-ordered`, `missing`, `duplicated`, or `misordered`. Adoption needs unique anchors or an authorized full rewrite; otherwise stop.

A complete block preserves IDs and is never removed implicitly. Removal needs approved deactivation/supersession and impact traceability. Malformed or unresolved structure stops. Design Review retains final authority over grandfathered substantive-revision classification.

## Generated Markdown readability

Write normal Markdown paragraphs. Do not split a sentence across physical source lines merely for wrapping or clause separation. Preserve stable IDs; use tables for repeated mappings. Diagrams are optional. Do not require manual-proof contracts from readability guidance.

## Rules and handoff

Only governed authority may end at `review-required`; `design-review` settles the complete design package. Never change other artifact or stage state. Governed work hands off; portable stays isolated; unclear behavior routes upstream.

## Stop conditions

Stop on missing, unreadable, escaped, contradictory, stale, mixed-version, ambiguous, conflicting, unknown, or insufficient evidence/resources; illegal state; unsafe recovery; unowned behavior; malformed structure; or placeholders.

The common path must not reconstruct missing procedure. Report blocker and owner.

## Claims this skill must not make

Never claim Design Review approval; plan, implementation, branch, or PR readiness; validation, verification, release, deployment, publication, or settlement.

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

- READ `references/requirement-to-delivery-model.md` when refining an approved direction into system requirements or defining their downstream traceability.
- READ `references/boundary-first-method-v1.md` initially for every `spec` invocation.
- READ `references/boundary-first-feature-authoring-v1.md` initially after the method reference for every `spec` invocation.
- READ `references/governed-spec-authoring.md` only for `single-governed-candidate`; validate exact authority before any governed write.
- COPY `assets/spec-skeleton.md` when creating or fully rewriting. Fill: applicable fields and sections. Do not emit unfilled placeholders or insertion markers.

Require readable, contained, same-version resources; never infer missing procedure or structure.

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

Author the normative applicability, boundary, interaction, and example-ownership record. Stop spec authoring and route the gap upstream when governing requirements cannot own an applicable boundary, an example would be the only source of behavior, or applicability is unsafe to decide. The two initially loaded references own detailed vocabulary, record shape, semantic procedure, and structural-validation limits.

## Output skeleton

```md
COPY `assets/spec-skeleton.md` for <spec path>.
Fill every required and applicable section and remove the conditional insertion marker and all placeholders.
```

## Expected output

Report path, requirements, boundaries, blockers, and readiness.

## Outputs

Output is the spec and evidence, not review or downstream completion.
