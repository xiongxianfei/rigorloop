<!-- Template: proposal-skeleton-v1 -->
<!-- Skill: proposal -->
<!-- Template status: normative -->
<!-- Maintained alongside: skills/proposal/SKILL.md -->
<!-- Readability contract: use normal prose paragraphs, keep complete sentences intact, and retain stable IDs and tables for repeated proof or mapping structures. -->

# Spec Skill Simplification

## Owning change record

`docs/changes/2026-08-15-spec-skill-simplification/change.yaml`

## Problem

The published `spec` skill loads 1,813 words of stage-local guidance plus 1,207 words from two boundary-first references that the approved boundary contract requires for every invocation. Its stage-local common path mixes universal behavioral-contract judgment, governed `change.yaml` mutation, proposal-settlement procedure, workflow-managed continuation, a long restatement of boundary procedure already owned by the two references, and ordinary document headings already owned by the skeleton.

This makes both portable and governed specification authoring harder to scan and creates multiple owners for boundary procedure and ordinary spec layout. The package already has the correct boundary resources and structural skeleton, but `SKILL.md` does not consistently treat them as the detailed owners of those concerns.

The problem is not that the specification contract is too rigorous. Observable behavior, stable requirements, examples, errors, compatibility, observability, security, accessibility, performance, edge cases, acceptance criteria, boundary adoption, and review handoff remain necessary. The problem is that universal contract quality, governed lifecycle mutation, shared boundary procedure, and structural layout are not separated cleanly.

## Goals

- Reduce the procedural context loaded for portable and governed spec authoring without weakening behavioral-contract quality or lifecycle safety.
- Keep a self-sufficient universal `SKILL.md` for evidence use, observable behavior, requirements, examples, failure behavior, compatibility, quality dimensions, stops, claims, and `spec-review` handoff.
- Move only governed upstream settlement, artifact creation and revision, authoring evidence, retries, same-entry stale-authoring restart, and the matching `authoring → review-required` transition into one conditionally loaded reference.
- Preserve the existing contract that `spec` initially loads both boundary-first references for every invocation; remove duplicated inline boundary procedure instead of changing that loading policy.
- Keep the existing skeleton as the owner of ordinary spec headings, ordering, placeholders, and one conditional boundary-block insertion point while retaining the boundary feature reference as the owner of the formal boundary-record block.
- Preserve customer-project portability and allow portable authoring from an accepted direction, behavior request, issue, exploration, or research without requiring a RigorLoop change record.
- Measure real loaded profiles and total package size separately so relocated content is not presented as deletion.

## Non-goals

- Reducing specification rigor, removing stable requirement IDs, weakening compatibility or failure contracts, or allowing examples to become the sole owner of behavior.
- Changing `boundary-first-v1`, its resource bytes, identifiers, capability activation, scenario stop rule, feature-record shape, or required initial loading profile.
- Changing `spec-review` authority, workflow stage order, architecture assessment routing, plan readiness, or downstream settlement ownership.
- Replacing Markdown specification with an executable schema compiler, routing engine, model evaluator, or generator-owned semantic contract.
- Adding another output asset, a new boundary reference, a permanent simplicity validator, a tokenizer dependency, a prose classifier, a target-agent journey test, or a separate manual semantic-review acceptance gate.
- Rewriting historical specs or changing their lifecycle state merely to adopt the simplified skill.

## Vision fit

fits the current vision

The change makes the behavioral-contract stage easier to inspect and use while preserving the traceability chain from accepted direction through requirements, boundaries, proof planning, implementation, and review. It reduces avoidable context without weakening durable evidence or human review.

## Context

The canonical package currently contains:

```text
skills/spec/
├── SKILL.md
├── references/
│   ├── boundary-first-method-v1.md
│   └── boundary-first-feature-authoring-v1.md
└── assets/
    └── spec-skeleton.md
```

Current canonical measurements are:

| Resource | Lines | Words | UTF-8 bytes |
| --- | ---: | ---: | ---: |
| `SKILL.md` | 218 | 1,813 | 12,853 |
| Boundary-first method reference | 110 | 857 | 6,346 |
| Boundary-first feature-authoring reference | 66 | 350 | 2,324 |
| Spec skeleton | 94 | 209 | 1,564 |
| Initially loaded procedural profile | 394 | 3,020 | 21,523 |
| Complete package | 488 | 3,229 | 23,087 |

The approved boundary-first loading profile requires `spec` to package and initially load both the compact core and feature-authoring guidance. This proposal does not make either reference conditional. Instead, it removes the stage-local restatement of detailed boundary procedure and keeps only spec-owned semantic obligations and routing in the main file.

The stage-owned lifecycle contract permits `spec` to create or revise only its own artifact, authoring evidence, and matching artifact-state entry. Portable invocations have no such mutation authority. The current skill states governed proposal settlement and mutation inline even when the invocation is portable.

The skeleton already owns ordinary specification headings and ordering, while the feature-authoring reference owns the contiguous formal boundary record and tables. `SKILL.md` currently repeats the ordinary section inventory and output skeleton. This duplication should be removed without moving semantic adequacy or boundary policy into the asset.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Optimize the `spec` skill | in scope | Goals and Recommended Direction |
| Identify the best solution rather than only shortening prose | in scope | Options Considered and Recommended Direction |
| Create a new branch | in scope | Decision Log |
| Generate a governed proposal | in scope | This artifact and owning change record |
| Run `proposal-review` after authoring | in scope | Next Artifacts and Readiness |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Simplify universal spec guidance | core to this proposal | This is the primary stage-local reduction. |
| Add one governed authoring reference | core to this proposal | It isolates conditional lifecycle mutation behind exact authority. |
| Preserve both boundary-first references and initial loading | same-slice dependency | The approved boundary capability contract is compatibility-sensitive and remains unchanged. |
| Remove ordinary section-layout duplication | core to this proposal | The skeleton already owns ordinary headings and ordering. |
| Preserve boundary-record structural ownership | same-slice dependency | The existing feature-authoring reference remains the owner of its contiguous formal block. |
| Update skill and package validators | same-slice dependency | Resource ownership, closed values, and package parity need deterministic proof. |
| Add change-local preservation and measurement evidence | same-slice dependency | Simplification needs semantic accounting and honest profile metrics. |
| Redesign boundary-first loading across the spec family | out of scope | That would change an independently governed capability contract. |
| Optimize `spec-review` again | out of scope | It was simplified separately and owns peer judgment and settlement. |

## Options Considered

### Option 1: leave the package unchanged

This avoids compatibility risk but leaves governed mutation, duplicated ordinary structure, and repeated boundary procedure on every authoring path. It does not address the usability problem.

### Option 2: editorial compression inside `SKILL.md`

This can reduce wording without changing package shape. It is lower risk, but governed and portable responsibilities remain interleaved, authority ownership stays unclear, and future edits can restore the same duplication.

### Option 3: extract only the inline boundary restatement

This recognizes the existing boundary references as detailed owners and reduces duplication. It does not remove governed proposal-settlement and lifecycle mutation from portable authoring, so the principal authority boundary remains mixed.

### Option 4: add one governed reference, retain both boundary resources, and preserve structural owners

This option shortens `SKILL.md`, adds one conditional governed-authoring reference, preserves the two always-loaded boundary references unchanged, removes inline boundary duplication, and removes ordinary section inventories already owned by the skeleton. Universal contract quality stays inline, while lifecycle mutation becomes progressively disclosed.

This is the recommended option because each resource boundary follows an existing authority or structural owner and both real procedural profiles can shrink without changing the boundary capability.

### Option 5: split requirements, examples, compatibility, security, and performance into separate references

This could make `SKILL.md` very short, but these are universal behavioral-contract obligations. Fragmenting them would make ordinary spec authoring navigate several resources and could hide quality requirements behind optional loading.

### Option 6: replace prose authoring with an executable spec engine

An engine could enforce some structure, but semantic requirements, examples, boundaries, compatibility, and non-goals remain judgment-heavy. It would introduce runtime, schema, migration, and architecture beyond a package-content refactor.

## Recommended Direction

Adopt Option 4.

The final package should be:

```text
skills/spec/
├── SKILL.md
├── references/
│   ├── governed-spec-authoring.md
│   ├── boundary-first-method-v1.md
│   └── boundary-first-feature-authoring-v1.md
└── assets/
    └── spec-skeleton.md
```

### Invocation profiles and resource loading

Use two procedural profiles because the approved boundary contract keeps both boundary references in every invocation. Classify governed signals before selecting either profile.

| Profile or stop | Governed-signal classification | Loaded procedure or result |
| --- | --- | --- |
| `SA0-portable` | `no-governed-signal` | `SKILL.md` plus both boundary-first references |
| `SA1-governed` | `single-governed-candidate` | Portable procedure plus `governed-spec-authoring.md` |
| Stop | `invalid-or-ambiguous-governed-signal` | Stop before portable or governed mutation |

The skeleton is copied when creating or fully rewriting a spec and is measured separately from procedural context.

Governed-signal classification has exactly three values: `no-governed-signal`, `single-governed-candidate`, and `invalid-or-ambiguous-governed-signal`. Any explicit change ID, workflow-managed change identity, or structured owning-change field counts as a governed signal even when malformed. Conversational references to a workflow, proposal, or change do not establish a signal.

`no-governed-signal` is valid only when none of those signal sources exists and is the only classification that permits portable authoring. `single-governed-candidate` requires every present signal to parse safely and resolve to the same exact change. A malformed, stale, duplicated, escaped, unsafe, missing-root, mismatched, or conflicting signal produces `invalid-or-ambiguous-governed-signal` and stops without portable fallback.

`governed_spec_candidate_context` is true only for `single-governed-candidate`. It selects the governed reference but grants no mutation authority.

After loading, the governed reference validates `governed_spec_authority` from the complete change record, `lifecycle_contract: stage-owned-change-local-v1`, exact spec entry or deterministic creation path, settled governing inputs, proposal settlement when applicable, and legal spec-authoring state. A candidate that fails validation stops before mutation and must not fall back to portable authoring.

The two boundary references load initially according to the existing boundary-first profile. Loading them makes approved boundary vocabulary and feature-record procedure available; it does not establish that a new boundary outcome exists, grant lifecycle authority, or allow examples to invent behavior.

### Portable and governed operations

Classify artifact operation independently as `create-primary-spec` or `revise-primary-spec`.

Portable operations resolve from the exact target path and file state without a lifecycle entry.

| Portable operation | Resolved spec file | Result |
| --- | --- | --- |
| `create-primary-spec` | absent | Create the spec artifact |
| `create-primary-spec` | present | Stop and require explicit revision |
| `revise-primary-spec` | present | Revise the exact resolved artifact |
| `revise-primary-spec` | absent | Stop and route to creation |
| Either operation | ambiguous, conflicting, or unresolved target | Stop |

Portable authoring may use an explicit accepted direction, behavior request, issue, exploration, research, or project-local proposal without requiring RigorLoop lifecycle metadata. It treats upstream evidence as read-only, writes only the spec artifact, and never creates or mutates `change.yaml`, review logs, review resolutions, automation records, or routing state.

Governed operations additionally require the matching entry, identity, authoring authority, and retry conditions owned by the governed reference.

| Governed operation | Spec entry | Canonical spec file | Result |
| --- | --- | --- | --- |
| Create | absent | absent | Start governed creation after authority validation |
| Revise | present | present with matching identity | Start governed revision under legal authority |
| Matching create retry | matching `authoring` entry | absent or matching partial file | Reconcile only the identical transaction |
| Matching incomplete write | matching `authoring` entry | matching spec file | Validate and complete only the identical transaction |
| Matching completed retry | matching `review-required` entry | matching complete file and evidence | Idempotent success without duplicate evidence or transition |
| Conflict | asymmetry outside the same transaction | conflicting or unrelated state | Stop without adoption or overwrite |
| Conflict | mismatched entry, path, identity, inputs, or authority | any | Stop |
| Conflict | multiple primary candidates or attempts | any | Stop |

A complete rewrite of an existing spec is a revision, not creation. Revising a governed approved or otherwise settled spec requires an explicit legal reopen or revision state. When architecture, plans, test specs, implementation, or other downstream artifacts rely on the current spec identity, workflow must complete impact and staleness handling before granting revision authority.

### Governed creation, revision, and retry

Creation binds the change ID, artifact ID, normalized intended path, governing input identities, and authoring-evidence path. It confirms absent entry and file, creates only the exact entry in `authoring`, writes and validates the spec, records content identity and evidence, and transitions only the matching entry to `review-required` as the commit point.

Revision additionally binds the prior spec identity and exact reopen, review finding, upstream input change, or legal revision evidence. It preserves historical authoring and review records, clears only the authorized current review mapping, writes and validates the revised spec, records the new identity and revision basis, returns only the matching entry to `review-required`, and requires fresh `spec-review`.

An identical interruption resumes from the first incomplete step. Exact completed retry is idempotent. Changed path, input basis, prior identity, authority, or concurrent state is not an identical retry and stops without adoption.

### Same-entry stale-authoring restart

An interrupted operation whose governing input basis changes returns `stale-authoring-attempt` and stops. This is a diagnostic transaction result, not a new persisted lifecycle state, and detection performs no adoption, overwrite, rebind, restart, or evidence-pointer update.

The governed spec reference owns `restart-stale-authoring` as a separate bounded recovery operation over the same spec entry. Restart requires either an explicit current user instruction naming the exact stale attempt and new governing basis or a current same-change workflow handoff that explicitly requests that restart. Detecting or routing a stale attempt does not establish restart authority.

Restart is valid only when the exact entry remains in `authoring`; its artifact ID, kind, role, and normalized path still match; the old retry identity and governing inputs are known; the new governing input identities are known; current restart authority names that exact transition; no formal review or downstream artifact relies on the incomplete identity; no competing attempt exists; and the partial file is absent, empty, or attributable to the stale attempt. Any relied-upon, ambiguous, mismatched, competing, unpreservable, unrelated, or illegally settled state stops.

The new authoring evidence records the authority source and request identity, the old retry identity and governing inputs, the new retry identity and governing inputs, and the partial-content state and identity. Exact field names remain specification-level, but those semantic fields are mandatory.

| Partial content | Required disposition |
| --- | --- |
| Canonical file absent | Record `absent`; no snapshot is required |
| Canonical file exists with zero bytes and belongs to the stale attempt | Record `empty` and its identity; no separate byte copy is required |
| Canonical file is nonempty and belongs to the stale attempt | Preserve exact bytes and hash at a distinct change-local evidence path before replacement |
| File identity cannot be tied to the stale attempt | Stop |
| Required bytes cannot be preserved safely | Stop |
| File contains unrelated or competing changes | Stop |

Restart may write only the same canonical spec file, a new authoring-evidence record, the matching entry's `authoring_evidence` pointer, and the immutable partial-content snapshot required for nonempty bytes. It preserves the entry ID, kind, role, normalized path, and `authoring` state and must not change review mappings, another artifact entry, workflow state, automation state, or downstream artifacts.

Restart never deletes completed authoring evidence or review evidence. After restart, the entry remains `authoring`, and the normal governed authoring transaction must complete it to `review-required`.

| Observed state | Result |
| --- | --- |
| Same transaction identity and unchanged basis | Resume the identical attempt |
| Same incomplete entry, changed basis, explicit current restart authority, and every restart prerequisite satisfied | Restart the same entry with new retry and evidence identities |
| Formal review or downstream reliance exists | Stop and route to workflow-owned reopen and impact handling |
| Entry is not `authoring` | Stop |
| Artifact identity, role, kind, or path differs | Stop |
| Competing or ambiguous attempt exists | Stop |
| Matching operation already completed at `review-required` | Return idempotent success without restart |

This recovery records authority in the existing authoring-evidence model and introduces no new lifecycle state, persistent authorization subsystem, schema, or write owner. If implementation discovers that safe recovery requires cross-stage mutation, broader cleanup, or new persistent state, stop and require architecture and workflow-contract revision rather than expanding the simplification implicitly.

### Upstream settlement ownership

Universal `SKILL.md` states that upstream inputs are read-only and must be sufficiently authoritative for the requested claim. It does not require customer projects to have RigorLoop lifecycle records.

The governed reference validates an accepted proposal when the current governed spec relies on one. It requires the matching proposal entry to be `accepted`, current formal review evidence, no later contradictory review, and closed material review resolution when required. Missing or contradictory governed settlement stops and routes to `proposal-review` without modifying proposal state.

When no governed proposal applies, an explicit user-selected direction, issue, exploration, research result, or other project-local authority may support portable spec authoring. The spec must record its related upstream source and must not claim formal proposal settlement that does not exist.

### Ownership model

| Content | Owner |
| --- | --- |
| Purpose, evidence use, observable behavior, requirements, examples, quality dimensions, errors, compatibility, stops, claims, and `spec-review` handoff | `SKILL.md` |
| Tri-state governed-signal classification and invalid-signal stop before profile selection | `SKILL.md` |
| Governed authority, proposal settlement, create/revise transaction, entry mutation, authoring evidence, retry, same-entry stale restart, concurrency, and legal state transition | `references/governed-spec-authoring.md` |
| Shared boundary vocabulary, dimensions, identifiers, interactions, examples, stop rule, and structural-validation limits | Existing boundary-first method reference |
| Formal feature boundary-record headings, tables, and owner-scoped semantic procedure | Existing boundary-first feature-authoring reference |
| Ordinary spec headings, ordering, placeholders, and the conditional boundary-block insertion position | `assets/spec-skeleton.md` |
| Stale-attempt detection and routing, including an explicit same-change restart handoff when authorized, without spec-state mutation | `workflow` |
| Status meaning, section adequacy, lifecycle authority, and handoff | `SKILL.md` and applicable reference, never the asset |

The main file retains the compact four-question scan, spec-owned applicability and upstream-gap routing, and requirement-owned behavior rule. It removes detailed boundary dimensions, interaction procedure, capability-state restatement, and record layout already owned by the two initially loaded references.

The main file also stops reproducing the complete ordinary section table and output skeleton. It names the skeleton as the ordinary layout owner and retains compact semantic adequacy rules for requirements, examples, failure behavior, compatibility, observability, security/privacy, accessibility/UX, performance, edge cases, non-goals, acceptance criteria, open questions, artifact history, and readiness.

The skeleton does not absorb boundary tables, lifecycle policy, section applicability, or adequacy rules. The feature-authoring reference remains the single owner of its formal boundary block. A contradiction among the main file, references, and asset is a package defect and stops dependent work.

### Structural composition and boundary-block applicability

The skeleton contains one conditional insertion point immediately after `## Error and boundary behavior` and before `## Compatibility and migration`. The skeleton owns only that position; the feature-authoring reference owns the four contiguous formal boundary-record headings, their tables, and their owner-scoped semantic procedure.

```text
## Boundary model
## Boundary definitions
## Selected interactions
## Example ownership
```

Initial loading of the feature-authoring reference does not imply that the formal boundary block must be emitted. Current block state, current contract applicability, revision class, structural anchors, and any deactivation or full-rewrite authority are classified independently before writing.

Boundary-block state is exactly `absent`, `present-complete`, `present-incomplete`, `present-duplicated`, or `present-misplaced`. Structural-anchor state is exactly `unique-ordered`, `missing`, `duplicated`, or `misordered` for the `Error and boundary behavior` and `Compatibility and migration` headings.

| Current block state | Current applicability | Structural or revision condition | Result |
| --- | --- | --- | --- |
| `absent` | required | New current-skeleton spec or `unique-ordered` anchors | Insert the complete block at the owned insertion point |
| `absent` | required | Grandfathered spec without `unique-ordered` anchors and explicit full-rewrite authority | Rewrite through the current skeleton, preserving stable requirement IDs and semantic content, then emit the complete block |
| `absent` | required | Grandfathered spec without `unique-ordered` anchors and no full-rewrite authority | Stop |
| `present-complete` | required | Any authorized revision | Preserve the complete block and stable boundary IDs; update it in place only when the revision changes governed boundary semantics |
| `absent` | not applicable | Any revision | Omit the block |
| `present-complete` | not applicable | No explicit approved deactivation or supersession with downstream-impact handling | Preserve the complete block unchanged |
| `present-complete` | not applicable | Explicit approved deactivation or supersession with downstream-impact handling | Apply the authorized removal or supersession treatment while preserving required history and stable-ID traceability |
| `present-incomplete`, `present-duplicated`, or `present-misplaced` | required or not applicable | Any revision | Stop and require structural correction before dependent writing |
| Any | unresolved | Any revision | Stop |

A non-behavioral edit does not implicitly remove or relocate an existing complete block. A grandfathered spec adopts the block through bounded insertion only when both anchors exist exactly once and in order; otherwise adoption requires an explicitly authorized full-document rewrite using the current skeleton. An applicable block must be complete and contiguous, an absent non-applicable block is omitted, and no path may leave placeholders or insert the block ad hoc.

### Required-resource failure behavior

| Situation | Result |
| --- | --- |
| Any spec invocation and either initially required boundary reference is missing or unreadable | Stop before contract authoring or revision |
| Governed candidate and governed reference is missing or unreadable | Stop before authority validation or mutation |
| Skeleton is missing during creation or full rewrite | Stop before writing a partial spec |
| Mixed, contradictory, escaped, or stale required resources | Stop as a package-integrity blocker |
| Portable invocation with valid required boundary resources and `no-governed-signal` | Continue without the governed reference |
| Invalid or ambiguous governed signal | Stop before portable fallback or governed mutation |

The shortened main file must not reconstruct, remember, or partially invent missing boundary or governed procedure.

### Semantic preservation and literal compatibility

Create two change-local inventories before editing the skill.

`docs/changes/2026-08-15-spec-skill-simplification/spec-rule-disposition.yaml` maps every behaviorally significant rule or duplicate cluster to one source location, applicable profiles, disposition, destination, and preservation proof. Closed dispositions are `retained-inline`, `retained-governed-reference`, `retained-boundary-reference`, `asset-owned`, `removed-duplicate`, and `removed-obsolete-with-approved-contract-change`.

`docs/changes/2026-08-15-spec-skill-simplification/spec-literal-compatibility.yaml` inventories exact headings, labels, paths, enum values, resource commands, and phrases consumed by contracts, parsers, packages, fixtures, or incidental tests. Closed classifications are `normative-contract`, `parser-or-package-contract`, `test-only-incidental`, `historical-fixture`, and `obsolete`.

Preserve normative literals unless their governing contract is amended. Migrate parser or package contracts atomically with all consumers. Update incidental tests rather than freezing prose. Keep historical literals only in compatibility fixtures where they prove old artifact readability.

### Measurement

Use canonical authored files, normalize line endings to LF, count each unique loaded procedural resource once in documented order, and record file paths, identities, UTF-8 bytes, and Unicode whitespace-separated words.

Measure `SA0-portable` and `SA1-governed` separately. Both profiles include `SKILL.md`, the boundary-first method reference, and the feature-authoring reference; `SA1` additionally includes the governed reference. Report `SKILL.md`, each reference, the skeleton, representative copied output, and complete package size separately.

Acceptance requires both real procedural profiles to decrease from the current 3,020-word and 21,523-byte baseline. A smaller main file alone is insufficient. No fixed percentage overrides semantic or lifecycle preservation. A 25–40 percent `SKILL.md` reduction is planning evidence, not a release gate.

Use words and bytes as required portable metrics. Use token counts only when an existing repository-owned pinned implementation already supports the exact profile assembly; otherwise omit them and do not add a tokenizer dependency.

### Validation and acceptance boundary

Use deterministic proof for:

- exact resource inventory, mapping verbs, paths, required initial boundary resources, and package parity;
- tri-state governed-signal classification, identity agreement, and no malformed-signal portable fallback;
- portable and governed profile assembly;
- create, revise, identical retry, stale detection, explicit same-entry restart authority, deterministic partial-content preservation, conflicts, missing resources, and forbidden writes;
- semantic-rule and literal-classification closed vocabularies, including unknown-value rejection before consistency checks;
- ordinary skeleton ownership, the exact conditional insertion point, block and anchor closed states, applicability, preservation, explicit deactivation, grandfathered adoption, boundary-record ownership, resource failure, stops, claims, and handoff;
- generated, archived, release-candidate, and clean-installed resource path and raw-byte parity;
- words, bytes, content identities, and total package accounting.

Do not execute or grade Codex, Claude Code, opencode, or another target-agent runtime. Do not add transcript grading, a prose classifier, a permanent simplicity validator, a tokenizer dependency, or a separate manual semantic-review acceptance stage. Ordinary formal proposal review, spec review, code review, and PR review remain the semantic judgment surfaces already owned by the lifecycle.

### Proposal acceptance criteria

| ID | Criterion |
| --- | --- |
| `AC-SPSIM-001` | Stale governed authoring produces the transaction result `stale-authoring-attempt` without adding a lifecycle state. |
| `AC-SPSIM-002` | `restart-stale-authoring` is owned by the governed spec procedure and applies only to the same incomplete spec entry. |
| `AC-SPSIM-003` | Restart requires exact artifact, path, old basis, new basis, retry, evidence, no-reliance, and no-competition proof. |
| `AC-SPSIM-004` | Restart may write only the incomplete canonical spec, the matching authoring-evidence pointer, new authoring evidence, and any required immutable partial snapshot. |
| `AC-SPSIM-005` | Workflow detects and routes stale attempts but gains no new spec-state mutation or persisted authorization owner. |
| `AC-SPSIM-006` | Unsafe, relied-upon, mismatched, settled, or ambiguous stale attempts stop without adoption or overwrite. |
| `AC-SPSIM-007` | The skeleton provides exactly one conditional boundary-block insertion point after error behavior and before compatibility. |
| `AC-SPSIM-008` | The feature-authoring reference remains the sole owner of the four contiguous formal boundary-record headings and tables. |
| `AC-SPSIM-009` | Boundary-reference loading and formal boundary-block emission are classified independently. |
| `AC-SPSIM-010` | Every authoring condition in the applicability matrix has one emit, preserve, omit, or stop result. |
| `AC-SPSIM-011` | Required boundary blocks are complete and contiguous, absent non-applicable blocks and unfilled placeholders are omitted, and existing complete blocks follow explicit preservation or deactivation rules. |
| `AC-SPSIM-012` | Both procedural profiles decrease while semantic preservation, package parity, and the no-target-runtime boundary remain intact. |
| `AC-SPSIM-013` | Any structured owning-change field is treated as a governed signal even when malformed. |
| `AC-SPSIM-014` | A malformed, stale, escaped, unsafe, or missing-root pointer cannot fall through to portable revision. |
| `AC-SPSIM-015` | Multiple candidate change identities fail closed. |
| `AC-SPSIM-016` | An explicit change ID, workflow identity, and artifact pointer must resolve to the same change when more than one exists. |
| `AC-SPSIM-017` | Failed governed-signal or authority validation never reclassifies the invocation as portable. |
| `AC-SPSIM-018` | Detecting `stale-authoring-attempt` performs no overwrite or evidence-pointer update. |
| `AC-SPSIM-019` | Restart requires an explicit current user request or same-change workflow handoff for the exact stale attempt and new basis. |
| `AC-SPSIM-020` | Restart authority and old and new attempt identities are recorded in authoring evidence. |
| `AC-SPSIM-021` | Every nonempty matching partial file is preserved byte-for-byte with a hash before replacement. |
| `AC-SPSIM-022` | Unknown, unrelated, conflicting, or unpreservable partial content blocks restart. |
| `AC-SPSIM-023` | Restart writes only the canonical spec, matching evidence pointer, new evidence, and required immutable partial snapshot. |
| `AC-SPSIM-024` | Restart leaves the matching artifact entry in `authoring`. |
| `AC-SPSIM-025` | Every boundary-block presence, applicability, and structural-anchor combination has one deterministic result. |
| `AC-SPSIM-026` | Existing complete boundary blocks are not removed implicitly by non-behavioral or non-applicable edits. |
| `AC-SPSIM-027` | Boundary-contract deactivation, removal, or supersession requires explicit approved authority and downstream-impact handling. |
| `AC-SPSIM-028` | Grandfathered bounded insertion requires unique ordered structural anchors. |
| `AC-SPSIM-029` | Missing, duplicated, or misordered anchors require an authorized full rewrite or stop. |
| `AC-SPSIM-030` | Incomplete, duplicate, or misplaced formal boundary blocks fail closed. |
| `AC-SPSIM-031` | Stable boundary IDs remain preserved or receive explicit traceable supersession treatment. |

### Architecture assessment

The expected result is `architecture-not-required` when the bounded assessment confirms that the existing architecture already defines a published skill as canonical `SKILL.md` plus mapped references and assets, preserves canonical/generated/archive/install parity, and supports spec-owned same-entry recovery through the existing artifact entry and authoring-evidence fields without schema expansion.

A documentation-only architecture correction is appropriate if an inventory depicts `skills/spec/` as permanently limited to its current resources. A new ADR is required only if implementation introduces a new runtime, persistent state, lifecycle owner, package model, independent policy owner, or recovery mechanism. None is selected here.

## Expected Behavior Changes

- Portable spec authoring no longer loads governed proposal-settlement and `change.yaml` mutation procedure.
- Only `no-governed-signal` permits portable authoring; malformed, duplicated, stale, unsafe, missing-root, or conflicting governed signals stop.
- Governed spec authoring loads one explicit reference and must validate exact authority before any mutation.
- Every invocation continues initially loading both approved boundary-first references.
- The common file no longer repeats detailed boundary procedure or the complete ordinary section inventory.
- The ordinary skeleton supplies one conditional composition point while the feature-boundary reference remains the sole owner of the complete formal boundary block.
- A changed-basis incomplete governed attempt stops until an explicit user request or same-change workflow handoff authorizes the spec-owned same-entry restart, and every matching nonempty partial file is preserved before replacement.
- Formal boundary blocks use closed block and anchor states, are never removed implicitly, and enter grandfathered specs only through valid anchors or an authorized full rewrite.
- Missing required resources fail closed rather than being reconstructed from memory.
- Every real procedural profile and the main file become measurably smaller while total package changes remain visible.

## Architecture Impact

Likely `architecture-not-required` after bounded assessment. The change uses the existing packaged-skill, stage-owned lifecycle, boundary-first, generated-resource parity, and spec-owned artifact-entry models. Same-entry restart records current authority and partial-content identity in existing authoring evidence and introduces no runtime, service, dependency, schema, persistent authorization subsystem, lifecycle state, write owner, or deployment change.

## Testing and Verification Strategy

- Inventory every behaviorally significant rule and exact literal consumer before editing.
- Add deterministic fixtures for tri-state governed signals, both profiles, create/revise state matrices, identical retry, stale detection, explicit restart authority, partial-content preservation, boundary-block and anchor state transitions, grandfathered adoption, missing resources, structural ownership, unknown closed values, and forbidden claims.
- Run focused spec-skill validation, the broad skill-validator suite, generated-skill drift checks, boundary validation, adapter distribution validation, and clean-install checks for Codex, Claude Code, and opencode.
- Measure loaded words and bytes for both profiles plus each resource, the skeleton, representative output, and total package.
- Use ordinary lifecycle reviews for semantic judgment; do not introduce a separate scripted or manual semantic-review acceptance gate.

## Rollout and Rollback

Implement atomically across canonical skill text, the new reference, affected validators and fixtures, generated-package inputs, and change-local proof. Preserve both existing boundary reference files and their loading profile unchanged.

Rollback removes the new governed reference, restores governed procedure to the main file, restores affected validators and fixtures, and regenerates package outputs through existing tooling. Historical specs remain unchanged in either direction.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Governed procedure is removed from the common file but not loaded when needed | Use an evidence-based candidate predicate, deterministic profile fixtures, and missing-resource stops. |
| Malformed or conflicting governed ownership is mistaken for portable context | Treat every structured ownership field as a signal and allow portable authoring only after a tri-state classifier returns `no-governed-signal`. |
| Portable authoring becomes dependent on RigorLoop lifecycle metadata | Keep portable operations and upstream authority explicit and test the absence of lifecycle writes. |
| Boundary-first loading or semantics drift during simplification | Preserve both resources and the approved initial-loading profile; validate paths, bytes, and semantic ownership. |
| Section labels move but adequacy rules disappear | Maintain separate rule and literal ledgers and test the skeleton/reference ownership split, exact insertion point, and applicability matrix. |
| New governed reference merely relocates prose without reducing real context | Require both `SA0` and `SA1` words and bytes to decrease and report total package separately. |
| Same-entry restart overwrites useful partial evidence or broadens spec authority | Require explicit current authority, exact old and new identities, immutable preservation of every matching nonempty partial file, bounded writes, no reliance, and unchanged entry ownership. |
| Boundary structure is removed, duplicated, or inserted ad hoc during revision | Use closed block and anchor states, preserve complete blocks without explicit deactivation, and require valid anchors or an authorized full rewrite. |
| Exact headings or phrases are parser-sensitive | Classify every literal consumer and migrate real parser contracts atomically. |
| Package growth is hidden behind main-file reduction | Report main file, profiles, references, skeleton, representative output, and complete package separately. |

## Open Questions

None at proposal level. The specification may choose exact authoring-evidence field names, but it must preserve the proposal's mandatory restart-authority, old and new identity, partial-content state, snapshot, bounded-write, and boundary-transition semantics without adding a new persistence or ownership model.

## Decision Log

- 2026-08-15: Created branch `proposal/spec-skill-simplification` from current `origin/main`.
- 2026-08-15: Selected one governed authoring reference rather than editorial compression, boundary-only extraction, fragmented quality references, or an executable engine.
- 2026-08-15: Preserved both boundary-first references and their required initial loading.
- 2026-08-15: Kept ordinary spec layout in the skeleton and formal boundary-record layout in the existing feature-authoring reference.
- 2026-08-15: Made portable and governed loaded-profile reduction the primary success surface rather than main-file reduction alone.
- 2026-08-15: Excluded target-agent runtime acceptance and a separate manual semantic-review gate.
- 2026-08-15: Replaced the unsupported workflow reset-authorization handshake with a bounded spec-owned same-entry stale-authoring restart.
- 2026-08-15: Added one conditional skeleton insertion point and a closed applicability matrix for the formal boundary-record block.
- 2026-08-15: Made governed-signal classification tri-state so invalid ownership indicators cannot fall through to portable authoring.
- 2026-08-15: Required explicit current restart authority and byte-for-byte preservation of every matching nonempty partial spec before replacement.
- 2026-08-15: Replaced the overlapping boundary applicability table with closed block and anchor states, explicit deactivation authority, and grandfathered adoption rules.

## Next Artifacts

- Formal `proposal-review` evidence and settlement.
- Focused feature specification if the proposal is approved.
- Bounded architecture assessment after the specification settles the contract.
- Execution plan and test specification after accepted upstream stages.

## Follow-on Artifacts

None yet

## Readiness

Ready for independent `proposal-review`. This proposal does not claim approval, specification readiness, implementation readiness, verification, branch readiness, or PR readiness.
