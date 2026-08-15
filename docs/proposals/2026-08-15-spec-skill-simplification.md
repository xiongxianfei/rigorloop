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

Use two procedural profiles because the approved boundary contract keeps both boundary references in every invocation.

| Profile | Governed candidate | Loaded procedure |
| --- | ---: | --- |
| `SA0-portable` | no | `SKILL.md` plus both boundary-first references |
| `SA1-governed` | yes | portable procedure plus `governed-spec-authoring.md` |

The skeleton is copied when creating or fully rewriting a spec and is measured separately from procedural context.

`governed_spec_candidate_context` selects the governed reference but grants no mutation authority. It is true only when the invocation supplies one explicit current change ID, a workflow-managed spec invocation identifies one exact current change, or the spec artifact contains one valid structured owning-change pointer. Conversational references to a workflow, proposal, or change do not establish it.

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

An interrupted operation whose governing input basis changes returns `stale-authoring-attempt`. This is a transaction result, not a new persisted lifecycle state, and it grants no authority to adopt, overwrite, rebind, or restart the attempt automatically.

Workflow may detect, classify, and route the stale attempt, but it does not authorize restart through a new persisted mechanism and does not mutate spec-owned artifact state. The governed spec reference owns `restart-stale-authoring` as a bounded recovery of the same spec entry.

Restart is valid only when the exact entry remains in `authoring`; its artifact ID, kind, role, and normalized path still match; the old and new governing input identities are known; no formal review or downstream artifact relies on the incomplete identity; no competing attempt exists; and the disposition of any partial spec content is known. Any relied-upon, ambiguous, mismatched, competing, or illegally settled state stops.

The restart binds the old retry identity, new governing input identities, a new retry identity, and a new authoring-evidence path. It may replace only the incomplete spec bytes and the same entry's `authoring_evidence`; it preserves the entry ID, kind, role, path, and `authoring` state and leaves every other artifact entry, review, workflow state, automation record, and downstream artifact unchanged.

Before replacing partial content, preserve the bytes at a distinct evidence path when they are required to explain the interrupted attempt, or record why the incomplete output has no durable evidentiary value. Restart never deletes completed authoring evidence or review evidence. After restart, the entry remains `authoring`, and the normal governed authoring transaction must complete it to `review-required`.

| Observed state | Result |
| --- | --- |
| Same transaction identity and unchanged basis | Resume the identical attempt |
| Same incomplete entry, changed basis, and every restart prerequisite satisfied | Restart the same entry with new retry and evidence identities |
| Formal review or downstream reliance exists | Stop and route to workflow-owned reopen and impact handling |
| Entry is not `authoring` | Stop |
| Artifact identity, role, kind, or path differs | Stop |
| Competing or ambiguous attempt exists | Stop |
| Matching operation already completed at `review-required` | Return idempotent success without restart |

This recovery introduces no new lifecycle state, persistent authorization, evidence type, or write owner. If implementation discovers that safe recovery requires cross-stage mutation or broader cleanup, stop and require architecture and workflow-contract revision rather than expanding the simplification implicitly.

### Upstream settlement ownership

Universal `SKILL.md` states that upstream inputs are read-only and must be sufficiently authoritative for the requested claim. It does not require customer projects to have RigorLoop lifecycle records.

The governed reference validates an accepted proposal when the current governed spec relies on one. It requires the matching proposal entry to be `accepted`, current formal review evidence, no later contradictory review, and closed material review resolution when required. Missing or contradictory governed settlement stops and routes to `proposal-review` without modifying proposal state.

When no governed proposal applies, an explicit user-selected direction, issue, exploration, research result, or other project-local authority may support portable spec authoring. The spec must record its related upstream source and must not claim formal proposal settlement that does not exist.

### Ownership model

| Content | Owner |
| --- | --- |
| Purpose, evidence use, observable behavior, requirements, examples, quality dimensions, errors, compatibility, stops, claims, and `spec-review` handoff | `SKILL.md` |
| Governed authority, proposal settlement, create/revise transaction, entry mutation, authoring evidence, retry, same-entry stale restart, concurrency, and legal state transition | `references/governed-spec-authoring.md` |
| Shared boundary vocabulary, dimensions, identifiers, interactions, examples, stop rule, and structural-validation limits | Existing boundary-first method reference |
| Formal feature boundary-record headings, tables, and owner-scoped semantic procedure | Existing boundary-first feature-authoring reference |
| Ordinary spec headings, ordering, placeholders, and the conditional boundary-block insertion position | `assets/spec-skeleton.md` |
| Stale-attempt detection and routing without spec-state mutation | `workflow` |
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

Initial loading of the feature-authoring reference does not imply that the formal boundary block must be emitted. Applicability is resolved independently from the current artifact and boundary contract.

| Authoring condition | Boundary-block result |
| --- | --- |
| New behavior-changing spec under the active boundary contract | Emit the complete formal boundary block at the insertion point |
| Substantive revision of a grandfathered spec that now adopts the boundary contract | Emit the complete formal boundary block at the insertion point |
| Revision of a spec that already contains the formal boundary block | Preserve and update the complete block in place |
| Formatting-only or otherwise non-substantive revision of a grandfathered spec | Omit the block when absent; preserve it unchanged when already present |
| Non-behavioral artifact or no active boundary identity | Omit the block |
| Applicability or required boundary data cannot be resolved | Stop before writing or emit an explicit blocker in a review-only result |

An inapplicable block is omitted completely. An applicable block must be complete and contiguous; it cannot be replaced by placeholders or duplicated elsewhere in the skeleton or `SKILL.md`.

### Required-resource failure behavior

| Situation | Result |
| --- | --- |
| Any spec invocation and either initially required boundary reference is missing or unreadable | Stop before contract authoring or revision |
| Governed candidate and governed reference is missing or unreadable | Stop before authority validation or mutation |
| Skeleton is missing during creation or full rewrite | Stop before writing a partial spec |
| Mixed, contradictory, escaped, or stale required resources | Stop as a package-integrity blocker |
| Portable invocation with valid required boundary resources and no governed candidate | Continue without the governed reference |

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
- portable and governed profile assembly;
- create, revise, identical retry, same-entry stale restart, conflicts, missing resources, and forbidden writes;
- semantic-rule and literal-classification closed vocabularies, including unknown-value rejection before consistency checks;
- ordinary skeleton ownership, the exact conditional insertion point, boundary-block applicability and omission, boundary-record ownership, resource failure, stops, claims, and handoff;
- generated, archived, release-candidate, and clean-installed resource path and raw-byte parity;
- words, bytes, content identities, and total package accounting.

Do not execute or grade Codex, Claude Code, opencode, or another target-agent runtime. Do not add transcript grading, a prose classifier, a permanent simplicity validator, a tokenizer dependency, or a separate manual semantic-review acceptance stage. Ordinary formal proposal review, spec review, code review, and PR review remain the semantic judgment surfaces already owned by the lifecycle.

### Proposal acceptance criteria

| ID | Criterion |
| --- | --- |
| `AC-SPSIM-001` | Stale governed authoring produces the transaction result `stale-authoring-attempt` without adding a lifecycle state. |
| `AC-SPSIM-002` | `restart-stale-authoring` is owned by the governed spec procedure and applies only to the same incomplete spec entry. |
| `AC-SPSIM-003` | Restart requires exact artifact, path, old basis, new basis, retry, evidence, no-reliance, and no-competition proof. |
| `AC-SPSIM-004` | Restart may change only incomplete spec bytes and the matching entry's authoring-evidence pointer. |
| `AC-SPSIM-005` | Workflow detects and routes stale attempts but gains no new spec-state mutation or persisted authorization owner. |
| `AC-SPSIM-006` | Unsafe, relied-upon, mismatched, settled, or ambiguous stale attempts stop without adoption or overwrite. |
| `AC-SPSIM-007` | The skeleton provides exactly one conditional boundary-block insertion point after error behavior and before compatibility. |
| `AC-SPSIM-008` | The feature-authoring reference remains the sole owner of the four contiguous formal boundary-record headings and tables. |
| `AC-SPSIM-009` | Boundary-reference loading and formal boundary-block emission are classified independently. |
| `AC-SPSIM-010` | Every authoring condition in the applicability matrix has one emit, preserve, omit, or stop result. |
| `AC-SPSIM-011` | Applicable boundary blocks are complete and contiguous; inapplicable blocks and unfilled placeholders are omitted. |
| `AC-SPSIM-012` | Both procedural profiles decrease while semantic preservation, package parity, and the no-target-runtime boundary remain intact. |

### Architecture assessment

The expected result is `architecture-not-required` when the bounded assessment confirms that the existing architecture already defines a published skill as canonical `SKILL.md` plus mapped references and assets, preserves canonical/generated/archive/install parity, and supports spec-owned same-entry recovery through the existing artifact entry and authoring-evidence fields.

A documentation-only architecture correction is appropriate if an inventory depicts `skills/spec/` as permanently limited to its current resources. A new ADR is required only if implementation introduces a new runtime, persistent state, lifecycle owner, package model, independent policy owner, or recovery mechanism. None is selected here.

## Expected Behavior Changes

- Portable spec authoring no longer loads governed proposal-settlement and `change.yaml` mutation procedure.
- Governed spec authoring loads one explicit reference and must validate exact authority before any mutation.
- Every invocation continues initially loading both approved boundary-first references.
- The common file no longer repeats detailed boundary procedure or the complete ordinary section inventory.
- The ordinary skeleton supplies one conditional composition point while the feature-boundary reference remains the sole owner of the complete formal boundary block.
- A changed-basis incomplete governed attempt may restart only through the spec-owned same-entry recovery contract; workflow routes but gains no new write authority.
- Missing required resources fail closed rather than being reconstructed from memory.
- Every real procedural profile and the main file become measurably smaller while total package changes remain visible.

## Architecture Impact

Likely `architecture-not-required` after bounded assessment. The change uses the existing packaged-skill, stage-owned lifecycle, boundary-first, generated-resource parity, and spec-owned artifact-entry models. Same-entry restart reuses the existing `authoring` state and authoring-evidence surface and introduces no runtime, service, dependency, schema, persistent authorization, lifecycle state, or deployment change.

## Testing and Verification Strategy

- Inventory every behaviorally significant rule and exact literal consumer before editing.
- Add deterministic fixtures for both profiles, create/revise state matrices, identical retry and same-entry restart cases, boundary-block applicability and composition, missing resources, structural ownership, unknown closed values, and forbidden claims.
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
| Portable authoring becomes dependent on RigorLoop lifecycle metadata | Keep portable operations and upstream authority explicit and test the absence of lifecycle writes. |
| Boundary-first loading or semantics drift during simplification | Preserve both resources and the approved initial-loading profile; validate paths, bytes, and semantic ownership. |
| Section labels move but adequacy rules disappear | Maintain separate rule and literal ledgers and test the skeleton/reference ownership split, exact insertion point, and applicability matrix. |
| New governed reference merely relocates prose without reducing real context | Require both `SA0` and `SA1` words and bytes to decrease and report total package separately. |
| Same-entry restart overwrites useful partial evidence or broadens spec authority | Require exact old and new identities, bounded writes, explicit partial-content disposition, no reliance, and unchanged entry ownership. |
| Exact headings or phrases are parser-sensitive | Classify every literal consumer and migrate real parser contracts atomically. |
| Package growth is hidden behind main-file reduction | Report main file, profiles, references, skeleton, representative output, and complete package separately. |

## Open Questions

None at proposal level. The specification must name exact metadata fields, partial-content evidence rules, and permitted same-entry restart writes after inspecting current schema and consumers, without changing the selected ownership or persistence model.

## Decision Log

- 2026-08-15: Created branch `proposal/spec-skill-simplification` from current `origin/main`.
- 2026-08-15: Selected one governed authoring reference rather than editorial compression, boundary-only extraction, fragmented quality references, or an executable engine.
- 2026-08-15: Preserved both boundary-first references and their required initial loading.
- 2026-08-15: Kept ordinary spec layout in the skeleton and formal boundary-record layout in the existing feature-authoring reference.
- 2026-08-15: Made portable and governed loaded-profile reduction the primary success surface rather than main-file reduction alone.
- 2026-08-15: Excluded target-agent runtime acceptance and a separate manual semantic-review gate.
- 2026-08-15: Replaced the unsupported workflow reset-authorization handshake with a bounded spec-owned same-entry stale-authoring restart.
- 2026-08-15: Added one conditional skeleton insertion point and a closed applicability matrix for the formal boundary-record block.

## Next Artifacts

- Formal `proposal-review` evidence and settlement.
- Focused feature specification if the proposal is approved.
- Bounded architecture assessment after the specification settles the contract.
- Execution plan and test specification after accepted upstream stages.

## Follow-on Artifacts

None yet

## Readiness

Ready for independent `proposal-review`. This proposal does not claim approval, specification readiness, implementation readiness, verification, branch readiness, or PR readiness.
