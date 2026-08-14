---
name: test-spec
version: "1.0.0"
schema-version: skill-readability-v1
description: >
  Generate a traceable test specification from an approved feature spec and execution plan before writing test code or production code. Use to map requirements, examples, edge cases, architecture boundaries, and milestones into concrete tests.
argument-hint: [feature spec path, plan path, or feature name]
---

# Test spec authoring

Design proof before implementation.

## Workflow role

- role_name: test-spec
- stage: authoring
- upstream: approved spec and review, approved plan, and applicable architecture or ADRs
- downstream: test-spec-review
- summary: Map settled requirements and execution intent to concrete proof before implementation.
- ownership: Author test-spec content and, with exact governed authority, only its authoring evidence and matching artifact-entry transition.
- must_not_claim: implementation, validation, verification, branch, PR, release, deployment, publication, or peer-review completion

Portable work is isolated. Workflow-managed execution does not enlarge the `test-spec` write set.

## Quick operating guide

Use this skill to create or revise a proof map from settled requirements and execution intent.

Read first: the approved spec and review, plan, applicable architecture, project guidance, test conventions, and both initially required boundary references.

Produce: traceable cases, coverage and command ledgers, milestone proof timing, explicit gaps, and a `test-spec-review` handoff.

Stop when: required input, identity, proof, authority, resource, or output is unsafe to infer.

Do not claim: implementation or downstream readiness.

Next stage: required `test-spec-review` for formal governed authoring.

## Purpose and use

Before implementation, create or revise proof from governing artifacts, repository guidance, test conventions, fixtures, commands, and related tests. Resolve placement from explicit path, current metadata, governing contract, project guidance, then the portable default `specs/slug.test.md`; stop on conflict or ambiguity.

## Invocation profiles and authority

| Profile | Trigger | Loaded procedure |
| --- | --- | --- |
| `TSA0-portable` | No exact governed candidate | This file and both initial boundary references |
| `TSA1-governed` | `governed_test_spec_candidate_context` | Portable procedure plus governed authoring reference |

The candidate requires exactly one current `stage-owned-change-local-v1` change plausibly needing an operation. Prompt wording grants no authority. Loading does not grant mutation authority.

After loading the governed reference, resolve one change, operation, artifact identity or intended identity, normalized path, governing inputs, and current authority. Missing, stale, unknown, ambiguous, conflicting, multiple, or illegal evidence stops; never fall back to portable mutation. The closed operations are `create-primary-test-spec`, `revise-primary-test-spec`, and `restart-stale-authoring`.

## Proof-design contract

Map every normative requirement, error, compatibility or migration claim, material boundary, feasible example, and regression to proof of its outcome; snapshots, helper-only checks, and unrelated assertions do not count.

Use stable requirement, example, boundary, interaction, proof, test, command, milestone, manual-procedure, gap, and evidence IDs. Map every applicable boundary and selected interaction to proof without inventing contract IDs. Stop test-spec authoring and return to the feature spec when an ID is missing, stale, unknown, renamed, ambiguous, conflicting, escaped, or insufficient; route a proof-only gap to test-spec authoring.

Cover applicable proof levels, fixtures, mocking, compatibility, observability, security/privacy, performance, and exclusions.

## Validation commands and milestone proof

Give each depended-on command a stable ID and classify it exactly as `existing/configured`, `planned-for-implementation`, `release-owned`, `ci-owned`, `external-owned`, or `not-applicable`; unknown values fail first. Record ownership, timing, failure and zero-test behavior, evidence, and side effects. Do not run commands merely for authoring or infer external-effect authority.

For staged work, map each implementation milestone to test IDs, manual proof IDs or `none`, command IDs or `none`, evidence, and required gate. Do not depend silently on proof owned by a later milestone.

## Optional manual verification

Automation mode is exactly `automated`, `manual`, or `hybrid`. Manual or hybrid proof uses existing proof, case, milestone, optional `Manual QA checklist`, manual procedure, and evidence artifact structures only when automation is insufficient. This creates no new manual-proof contract or conditional group and no sixth asset; missing required evidence is a blocking gap.

## Output content and composition

Copy the skeleton and applicable body assets for full creation; copy only changed structures for revision. The skeleton owns document structure, and smaller assets own repeated bodies. Assets own layout, never policy. Omit inapplicable structures or use the approved sentinel; never emit markers, placeholders, duplicates, or ad hoc replacements. Before real follow-ons exist, use `None yet`.

## Generated Markdown readability

Write ordinary prose as normal Markdown paragraphs. Do not split a sentence across physical source lines merely for wrapping or clause separation. Preserve stable IDs and use tables for repeated mappings. Diagrams are optional. Do not require manual-proof contracts from readability guidance.

## Rules and handoff

- Do not invent behavior, substitute helper proof for an admitted public path, or count proof that misses the asserted outcome.
- Route untestable requirements to their spec or architecture owner.
- Authoring ends at `review-required`; only `test-spec-review` may settle the matching artifact to `active` after independent approval.
- Workflow may validate and route later state but cannot rewrite content or peer-review evidence.
- Preserve prior authoring and review evidence when revision creates a new identity.
- Governed authoring hands off to `test-spec-review`; portable authoring remains isolated.

## Stop conditions

Stop before dependent interpretation or mutation, and before dependent output, when required input or resource is missing, unreadable, escaped, contradictory, mixed-version, stale, ambiguous, conflicting, unknown, or insufficient. Stop when the spec is unstable, spec review records eventual `test-spec` readiness as `not-ready`, an approved ID lacks an owner, governed state or retry identity is illegal, or output would retain placeholders.

The common path must not reconstruct missing governed, boundary, or structural procedure from memory. Report the exact blocker and owning action.

## Claims this skill must not make

Do not claim implementation completion, validation success, code-review approval, verification, branch readiness, PR readiness, release, deployment, publication, or peer-review settlement. Authoring proves only readiness for its owned review gate.

## Evidence access

Use summary and stable-ID first reasoning before broad reads or raw excerpts. Prefer check IDs, requirement IDs, file paths, line citations, counts, commands, and targeted excerpts. Expand when evidence is missing, stale, contradictory, or insufficient.

## When full-file read is required

Read the full file when the whole file is the review target, bounded searches disagree or produce incomplete evidence, surrounding context can change the conclusion, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Resource map

- READ `references/boundary-first-method-v1.md` initially for every `test-spec` invocation.
- READ `references/boundary-first-proof-v1.md` initially after the method reference for every `test-spec` invocation.
- READ `references/governed-test-spec-authoring.md` only when `governed_test_spec_candidate_context` is established; validate exact authority before any governed write.
- COPY `assets/test-spec-skeleton.md` when creating or fully rewriting a test spec. Fill: document headings, table headers, insertion locations, and document-level fields. Do not emit unfilled placeholders.
- COPY `assets/test-case.md` when adding or revising a test case. Fill: test identity, coverage, level, commands, setup, steps, outcome, failure proof, evidence, location, and milestone. Do not emit unfilled placeholders.
- COPY `assets/coverage-map-row.md` when adding or revising requirement or example coverage. Fill: the selected row variant. Do not emit unfilled placeholders.
- COPY `assets/validation-command-row.md` when adding or revising a validation command. Fill: command identity, command, classification, owner, timing, failure, zero-test, evidence, and side-effect fields. Do not emit unfilled placeholders.
- COPY `assets/milestone-proof-row.md` when adding or revising milestone proof. Fill: milestone, tests, manual proof, commands, evidence, required gate, and notes. Do not emit unfilled placeholders.

Confirm required resources are readable, contained, and from one package version. Stop rather than infer missing procedure or structure.

## Boundary-first bridge

Apply the proof reference when a proof map consumes a `boundary-first-v1` feature record.

Run this compact scan before any stage-owned decision that can change observable behavior, and whenever the input cites an active boundary contract or stable boundary, interaction, or proof ID. Do not wait for the user to name the method.

1. Which inputs or actors can change the outcome?
2. Which state or timing conditions can change the outcome?
3. Which public, sibling, helper, or alternate path can change the outcome?
4. Which failure, retry, recovery, compatibility, or external condition can change the outcome?

If the work is non-behavioral, cites no active boundary identity, and the scan finds no outcome-changing condition, continue under the ordinary stage contract. The scan alone does not create a formal record, ID, proof map, artifact, or user-visible scenario inventory.

Start with the exact approved rows cited for the current decision. Expand approved context only when an ID or outcome is missing, stale, unknown, ambiguous, conflicting, escaped, or insufficient to explain observed behavior. A new or changed normative outcome routes to `spec`; a proof-only gap routes to `test-spec`. Downstream stages do not redefine or rename upstream IDs.

Add a scenario only for a distinct outcome or material authority, trust, state, timing, recovery, path, compatibility, external-dependency, incident, or regression hazard. Stop when every applicable boundary and selected interaction has direct proof; do not build a Cartesian inventory.

Capability state controls formal adoption: `pending` never claims active adoption; after activation, new behavior-changing specs adopt automatically, grandfathered non-substantive revisions remain valid, and `spec-review` must block an undecidable substantive-revision classification. Explain concisely when a formal record is created or an upstream gap blocks progress; do not request redundant consent for contract-required adoption. Structural validation cannot author, repair, or approve semantic content.

The two initially loaded references own the detailed boundary vocabulary and proof contract. Apply their exact-ID consumption, interaction selection, direct-proof, gap-routing, and scenario-stop rules.

## Output skeleton

```md
COPY `assets/test-spec-skeleton.md` for <full document structure>.
COPY applicable smaller assets for <repeated bodies>.
Fill <all applicable fields> and remove insertion markers and placeholders.
```

## Expected output

Report the test-spec path, grouped cases, coverage and proof maps, fixtures, commands, milestone proof timing, exclusions, gaps, and truthful `test-spec-review` readiness.

## Outputs

The output is a portable or governed test specification and authoring evidence within the classified authority. It is not peer review or downstream completion evidence.
