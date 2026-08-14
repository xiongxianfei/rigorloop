# Proposal Skill Simplification

## Owning change record

`docs/changes/2026-08-14-proposal-skill-simplification/change.yaml`

## Problem

The published `proposal` skill currently loads 2,122 words and 14,796 UTF-8 bytes for every invocation. Its common path combines universal decision-quality guidance with governed `change.yaml` mutation, missing-standing-artifact bootstrap procedure, vision-exception handling, broad-request intent classification, and scope-budget procedure.

Direct portable proposals therefore load RigorLoop-specific lifecycle mutation that they cannot use, while small single-decision proposals load detailed exception and multi-workstream procedure that does not apply. The main file also enumerates complete output sections already represented by `assets/proposal-skeleton.md`, leaving two structural owners that can drift.

The problem is not simply file length. The package lacks explicit invocation assemblies, conditional ownership, create-versus-revise behavior, missing-resource failure behavior, and a measurement model that distinguishes loaded context from total packaged content. Simplification must reduce real invocation cost without weakening problem framing, option quality, intent preservation, standing-artifact safety, lifecycle authority, or proposal-review handoff.

## Goals

- Reduce the loaded words and UTF-8 bytes for portable, governed, ordinary, and conditionally gated proposal authoring.
- Keep universal proposal judgment, evidence integrity, scope preservation, stops, claims, and handoff self-sufficient in `SKILL.md`.
- Move governed proposal-entry creation, revision, authoring evidence, retry, and lifecycle transition procedure behind one evidence-based reference trigger.
- Move vision exceptions, missing-standing-artifact bootstrap handling, and broad-scope classification behind one independently triggered reference.
- Make `assets/proposal-skeleton.md` the sole owner of proposal headings, section order, tables, and placeholders, including conditional structural groups.
- Preserve customer-project portability, formal lifecycle authority, exact closed vocabularies, generated-package parity, and all behaviorally significant current rules.
- Establish semantic-rule and literal-compatibility evidence without adding a permanent simplicity validator, prose classifier, or target-agent runtime test.

## Non-goals

- Changing the purpose of proposals, the standard workflow stage order, or `proposal-review` judgment and recording behavior.
- Changing the meaning of `Vision fit`, initial-goal treatments, scope-budget treatments, proposal lifecycle states, or downstream readiness claims.
- Allowing `proposal` to create a governed change root, approve its own output, settle review, advance workflow, or invoke downstream stages outside existing authority.
- Replacing proposal judgment with an executable decision engine, deterministic semantic classifier, scheduler, state store, or new runtime.
- Adding a second proposal artifact template, a result asset, packaged scripts, or more than two new references.
- Rewriting historical proposals solely to adopt the revised skeleton.
- Running Codex, Claude Code, opencode, or another target-agent runtime as acceptance evidence.
- Creating a separate manual semantic-review acceptance stage; ordinary proposal review, code review, and human PR review remain the judgment surfaces.

## Vision fit

fits the current vision

The change makes proposal reasoning easier to inspect and reuse while preserving the traceability and lifecycle boundaries that let another agent or human continue the work without chat history.

## Context

`skills/proposal/SKILL.md` is currently 289 lines, 2,122 words, and 14,796 UTF-8 bytes. Its existing skeleton is 79 lines, 141 words, and 1,089 bytes, giving a total package of 368 lines, 2,263 words, and 15,885 bytes.

The package has one structural asset and no references. The main file owns both ordinary proposal quality and three genuinely conditional procedure families: governed lifecycle authoring, standing-artifact or vision exceptions, and broad multi-workstream classification.

The repository already supports mapped references and assets as parts of one published skill package. `skills/proposal-review/` uses separate recording and conditional-gate references, while the published-skill integrity contract requires explicit resource mapping, canonical presence, containment, generated inventory, and raw-byte parity.

This proposal uses the existing package model. It introduces no new service, persistent state, package transformation, lifecycle owner, or adapter-install mechanism.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Optimize the `proposal` skill | in scope | Goals and Recommended Direction |
| Start a new branch | in scope | Branch `proposal/proposal-skill-simplification` |
| Generate a proposal | in scope | This artifact |
| Run `proposal-review` after authoring | in scope | Next Artifacts and Readiness |
| Preserve rigor while reducing unnecessary context | in scope | Goals, ownership model, and acceptance criteria |

## Options Considered

### Option 1: keep the package unchanged

This has no migration cost, but every invocation continues loading unrelated lifecycle and exceptional procedure. Duplicate structural ownership and unclear conditional boundaries remain.

### Option 2: editorial compression inside `SKILL.md`

This can remove repeated wording and improve scanability with minimal package change. It cannot prevent portable or ordinary proposals from loading governed and exceptional procedure, and aggressive compression risks hiding fragile state transitions in dense prose.

### Option 3: move all conditional procedure into one reference

This shortens the main file, but portable proposals with a vision or scope gate would load governed `change.yaml` mutation, while ordinary governed proposals would load strategic-exception procedure. One catch-all reference therefore recreates common-path coupling one level deeper.

### Option 4: use two independently triggered references and one structural asset

This keeps universal proposal quality inline, loads governed mutation only with current lifecycle authority, loads strategic and scope procedure only when one of its predicates is true, and gives output structure one owner. It creates four explicit loaded assemblies without adding runtime machinery.

### Option 5: replace prose classification with an executable proposal engine

An engine could make predicates mechanically repeatable, but vision exceptions, proposal breadth, option quality, and scope treatment are judgment-heavy. A new classifier would add runtime, testing, and policy ownership disproportionate to a documentation-package refactor.

## Recommended Direction

Adopt Option 4.

The resulting package is:

```text
skills/proposal/
├── SKILL.md
├── references/
│   ├── governed-proposal-authoring.md
│   └── strategic-and-scope-gates.md
└── assets/
    └── proposal-skeleton.md
```

### Invocation predicates

Classify two independent contexts before dependent reads or writes.

`governed_proposal_context` is true only when one exact existing governed change has `lifecycle_contract: stage-owned-change-local-v1`, deterministic proposal placement, settled prerequisites, and current proposal-authoring authority. Conversational references to a workflow or change do not establish this context. `proposal` never creates the governed change root; missing root authority routes to `workflow`.

The specialized predicate set contains `vision_exception_context`, `standing_artifact_context`, and `scope_budget_context`. The first applies when authoring must record a current-vision exception or proposed vision revision. The second applies when the proposal depends on a missing required standing artifact or bootstrap exception. The third applies when broad or multi-workstream scope needs detailed intent and work-item treatment. Predicate classification remains proposal judgment; deterministic validation may check names and recorded shape but must not infer semantic truth from prose.

Apply every true specialized predicate. Load the gates reference once for a non-empty set. Late predicate discovery must load the reference before dependent drafting or readiness selection. Unresolved ambiguity that could change safe output stops.

### Loaded assemblies

| Assembly | Governed context | Specialized context | Loaded procedure |
| --- | ---: | ---: | --- |
| `PA0-portable` | no | no | `SKILL.md` plus skeleton when creating |
| `PA0G-portable-gated` | no | yes | core plus strategic-and-scope reference |
| `PA1-governed` | yes | no | core plus governed-authoring reference |
| `PA1G-governed-gated` | yes | yes | core plus both references |

Loaded resources determine available procedure; they do not grant lifecycle authority or make a gate outcome true.

### Portable and governed operations

Classify artifact operation independently as `create-primary-proposal` or `revise-primary-proposal`.

| Operation | Proposal entry | Canonical proposal file | Result |
| --- | --- | --- | --- |
| Create | absent | absent | May create the proposal; governed mode may create only the matching proposal entry after validating authority |
| Revise | present | present with matching identity | May revise under current portable request or legal governed authoring authority |
| Conflict | absent | present | Stop; do not adopt or overwrite |
| Conflict | present | absent | Stop; do not recreate implicitly |
| Conflict | mismatched entry/path/identity | any | Stop |
| Conflict | multiple primary candidates | any | Stop |

A complete rewrite of an existing proposal is a revision, not creation. Revising a governed accepted or otherwise settled proposal requires an explicit legal reopen or revision state from the workflow contract. The authoring reference may update only the exact proposal entry, preserve historical review records, clear only its current review mapping when authorized, record proposal-authoring evidence, and transition the same entry from `authoring` to `review-required` after complete writes and validation.

Portable authoring writes the proposal artifact only. It does not create or mutate `change.yaml`, review logs, review resolutions, automation records, or workflow routing.

### Resource ownership

| Content | Owner |
| --- | --- |
| Purpose, proposal judgment, evidence precedence, option quality, ordinary vision fit, universal intent preservation, risks, stops, claims, and handoff | `SKILL.md` |
| Governed authority validation, create/revise transaction, proposal-entry mutation, authoring evidence, retries, concurrent writes, and legal authoring transition | `references/governed-proposal-authoring.md` |
| Vision exceptions, missing-standing-artifact bootstrap procedure, detailed broad-request intent classification, scope-budget classification, and follow-up routing | `references/strategic-and-scope-gates.md` |
| Proposal headings, ordering, tables, conditional structural groups, and placeholders | `assets/proposal-skeleton.md` |
| Status meaning, applicability, lifecycle authority, readiness, and handoff | `SKILL.md` and applicable reference, never the asset |

The references may name each other's concepts but must not duplicate governing procedure. Governed authoring cannot redefine strategic gates. Strategic gates cannot grant lifecycle writes. A contradiction among `SKILL.md` and mapped resources is a package defect and stops dependent work.

### Structural asset

Extend `proposal-skeleton.md` to contain one core proposal group and two conditional structural groups:

- `Initial intent preservation`, used when a broad or multi-part request requires explicit goal mapping.
- `Scope budget`, used when `scope_budget_context` is true.

The asset owns the labels, section order, table columns, and placeholders. `SKILL.md` and the gates reference decide applicability and meaning. Inapplicable groups are omitted completely; applicable groups with unresolved required data report an explicit blocker; unfilled placeholders are forbidden.

The main file retains only a compact semantic obligation summary and the resource-map instruction. It does not duplicate the skeleton's full section inventory or table layouts.

### Required-resource failure behavior

| Situation | Result |
| --- | --- |
| Portable ordinary proposal and no conditional reference is required | Continue from `SKILL.md` and the skeleton |
| Governed context and governed reference missing or unreadable | Stop before lifecycle interpretation or mutation |
| Specialized context and gates reference missing or unreadable | Stop before dependent gate judgment or drafting |
| Skeleton missing during creation | Stop before writing a partial proposal |
| Mixed or contradictory resource versions | Stop as a package-integrity blocker |
| A reference trigger is false | Do not load that reference; continue |

The shortened main file must not reconstruct, remember, or partially invent missing conditional procedure.

### Semantic preservation and compatibility

Create two change-local inventories before editing the skill.

`docs/changes/2026-08-14-proposal-skill-simplification/proposal-rule-disposition.yaml` maps every behaviorally significant rule or duplicate cluster to one source location, applicable assemblies, disposition, destination, and preservation proof. Closed dispositions are `retained-inline`, `retained-governed-reference`, `retained-gates-reference`, `asset-owned`, `removed-duplicate`, and `removed-obsolete-with-approved-contract-change`.

`docs/changes/2026-08-14-proposal-skill-simplification/proposal-literal-compatibility.yaml` inventories exact headings, labels, paths, enum values, and phrases consumed by contracts, parsers, packages, fixtures, or incidental tests. Closed classifications are `normative-contract`, `parser-or-package-contract`, `test-only-incidental`, `historical-fixture`, and `obsolete`.

Preserve normative literals unless their governing contract is amended. Migrate parser or package contracts atomically with all consumers. Update incidental tests rather than freezing prose. Keep historical literals only in compatibility fixtures where they prove old artifact readability.

### Measurement

Use canonical authored files, normalize line endings to LF for measurement, count each unique loaded procedural resource once, and assemble resources in documented load order. Record file paths and content identities, UTF-8 bytes, and Unicode whitespace-separated words.

Measure `PA0-portable`, `PA0G-portable-gated`, `PA1-governed`, and `PA1G-governed-gated` separately. Report `SKILL.md`, each reference, the skeleton, representative copied output, and total package size separately. Assets do not count as procedural context unless the invocation actually reads or copies them.

Acceptance requires every real loaded assembly to decrease from its baseline or receive a specific independently reviewed semantic-preservation exception. A smaller main file alone is insufficient. No fixed percentage overrides semantic preservation, and total package growth must be reported rather than presented as deletion.

## Expected Behavior Changes

- A small portable proposal loads only universal proposal guidance and the skeleton.
- A portable broad or exception-bearing proposal additionally loads strategic and scope procedure but no governed lifecycle mutation.
- An ordinary governed proposal additionally loads exact `change.yaml` authoring procedure but no unrelated strategic gate detail.
- A governed broad or exception-bearing proposal loads both references once.
- Existing proposals remain valid and are not rewritten merely because the skeleton changes.
- Governed proposal creation and revision fail closed on missing roots, illegal state, ambiguous identity, file/entry asymmetry, and concurrent conflicting writes.
- Missing required packaged resources stop dependent work instead of triggering remembered reconstruction.
- Proposal output continues to preserve user intent, meaningful alternatives, decision rationale, risks, rollout, open questions, and truthful readiness for `proposal-review`.

## Architecture Impact

The expected architecture assessment is `architecture-not-required`. The change uses the existing published-skill model of one canonical `SKILL.md` plus mapped references and assets, keeps `skills/` as the only authored source, preserves generated raw-byte parity, and introduces no runtime, persistence, schema, lifecycle owner, dependency, or transformation.

A bounded documentation update is required only if the current canonical architecture contains a flat `proposal` package inventory or an example that says `proposal` has no references. A new ADR is required only if specification work discovers a new package model, independent policy owner, persistent state, runtime, or lifecycle authority.

## Testing and Verification Strategy

- Validate canonical frontmatter, normalized sections, resource-map verbs, paths, containment, resource existence, placeholder rules, and forbidden claims with existing repository-owned validation.
- Add focused deterministic contract fixtures for all four assemblies, both operations, governed authority failures, specialized predicate combinations, late loading, missing resources, structural-group omission, and forbidden writes or claims.
- Validate rule-disposition and literal-compatibility ledger schemas with change-local fixtures; do not create a permanent prose-policy or simplicity validator family.
- Prove canonical, generated, archived, release-candidate, and installed resource inventory and raw-byte parity through existing package validation.
- Measure profile words and bytes using the deterministic convention in this proposal and report total package change separately.
- Use ordinary proposal review, code review, and eventual human PR review for semantic judgment. Do not add a separate manual semantic-review acceptance artifact or target-agent runtime journey.

## Rollout and Rollback

Roll out the canonical skill, two references, revised skeleton, focused fixtures, and necessary validator registration atomically. Regenerate or validate derived packages through existing repository commands; do not hand-edit generated public adapter bodies.

Existing proposal artifacts remain readable and unchanged. New or substantively revised proposals use the revised skeleton and conditional groups. No data migration, state migration, or compatibility adapter is required.

Rollback restores the prior `SKILL.md` and skeleton, removes the two references and their validator registration, and regenerates packages atomically. Retain generic validator corrections only when they remain valid independently of this skill package.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Universal proposal quality moves behind a conditional trigger | Use the rule-disposition ledger and require problem, options, rationale, intent, risk, claims, and handoff to remain inline |
| Governed loading is mistaken for lifecycle authority | Separate resource selection from full reference-owned authority validation and stop on missing or stale evidence |
| Strategic predicates drift from `proposal-review` | Align predicate vocabulary and boundaries while keeping authoring and review procedures skill-owned |
| The asset becomes a hidden policy owner | Limit it to labels, ordering, table shapes, and placeholders; validate policy-like content boundaries |
| File splitting reduces `SKILL.md` but not actual loaded profiles | Make all four loaded assemblies primary measurements and report total package size separately |
| Existing exact-string tests freeze incidental wording | Classify literal dependencies separately and update test-only consumers |
| New references are omitted or stale in an adapter package | Use existing mapped-resource inventory and raw-byte parity gates |
| Conditional procedure becomes unavailable at runtime | Stop before dependent work and forbid fallback reconstruction |
| Validation grows into semantic prose scoring | Restrict deterministic checks to closed vocabulary, structure, paths, mappings, and explicit recorded classifications |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Simplify `skills/proposal/SKILL.md` | core to this proposal | Primary user-visible objective |
| Add governed authoring reference | same-slice dependency | Required to remove lifecycle mutation from portable context safely |
| Add strategic and scope gates reference | same-slice dependency | Required to remove genuinely conditional exception and broad-scope procedure |
| Revise `proposal-skeleton.md` | same-slice dependency | Required to establish one structural owner, including conditional groups |
| Add preservation ledgers and deterministic fixtures | same-slice dependency | Required proof of semantic and literal preservation |
| Update validator resource registration and focused contract checks | same-slice dependency | Required for new mapped resources and structural ownership |
| Amend a focused proposal-skill contract | first-slice candidate | Observable public skill behavior requires a reviewed contract before implementation |
| Perform bounded architecture assessment | first-slice candidate | Confirms whether current package documentation already covers the change |
| Update canonical architecture package | separate implementation slice | Required only if the bounded assessment finds a stale flat-package inventory |
| Optimize `proposal-review` again | out of scope | Its package has already been simplified and remains a compatibility peer only |
| Optimize other authoring skills | deferable follow-up | Each skill needs its own ownership and trigger analysis |
| Add target-agent behavioral certification | out of scope | Repository acceptance is deterministic package proof plus normal review |

## Open Questions

None at proposal level. The specification may choose exact metadata field names for retry identities and measurement records without changing the selected ownership, authority, or acceptance boundaries.

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-14 | Use two independently triggered references | Governed mutation and strategic/scope gates have distinct activation and authority boundaries | Inline-only compression and one catch-all reference |
| 2026-08-14 | Keep universal decision quality and intent preservation inline | Every proposal needs these rules before conditional selection | Moving all detailed judgment behind references |
| 2026-08-14 | Keep one structural asset with conditional groups | One skeleton can own layout without owning applicability or policy | Duplicate inline layouts and additional narrow assets |
| 2026-08-14 | Separate portable/governed context from create/revise operation | Lifecycle authority and artifact existence are independent facts | Inferring operation from workflow wording |
| 2026-08-14 | Measure loaded assemblies and total package separately | Relocation improves common-path cost but may increase maintenance footprint | Main-file percentage as the sole success criterion |
| 2026-08-14 | Exclude target-agent and separate manual semantic-review acceptance | Static package proof and normal review are proportionate for a content refactor | Runtime transcript grading and an additional manual gate |

## Next Artifacts

- Independent `proposal-review` with durable formal evidence.
- Focused proposal-skill contract specification or amendment after proposal approval.
- Bounded architecture assessment, with an architecture update only if the current package inventory is stale.
- Execution plan and test specification after the contract and architecture decision are settled.

## Follow-on Artifacts

None yet

## Readiness

Ready for independent `proposal-review`. This proposal does not claim acceptance, specification readiness, architecture approval, implementation readiness, verification, branch readiness, or PR readiness.
