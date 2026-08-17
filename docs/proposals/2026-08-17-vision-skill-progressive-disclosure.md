# Vision Skill Progressive Disclosure

## Owning change record

`docs/changes/2026-08-17-vision-skill-progressive-disclosure/change.yaml`

## Problem

The published `vision` skill preserves the approved project-vision contract, but its single 2,268-word, 15,845-byte `SKILL.md` loads every concern on every invocation. A read-only vision assessment, a marker-bounded README synchronization, and a typo correction all load the complete strategic-positioning method, product-category fixtures, drafting heuristics, full vision structure, and initial-creation placement procedure.

The flat package also makes structural and procedural ownership difficult to see. The required `VISION.md` section sequence is embedded beside applicability policy; README marker parsing and insertion mechanics are embedded beside universal write authority; and strategic analysis is interleaved with ordinary state classification. Current validators consequently assert many exact phrases directly in `SKILL.md`, even when the behavior could remain normative in a mapped reference or structural asset.

The accepted behavior is not the problem. Root `VISION.md`, state-based behavior, substantive versus editorial revision, strategic-positioning rationale, word limits, README marker safety, retired lowercase-path handling, privacy, research, and output truthfulness must remain intact. The problem is that every path pays for every procedure and repeated structure has no structural owner.

## Goals

- Reduce loaded procedure for vision assessment, README synchronization, editorial revision, and strategic authoring without weakening the approved contract.
- Keep source precedence, repository-state and operation classification, write authority, substantive/editorial classification, canonical paths, privacy, research, stops, claims, resource triggers, and result obligations in a compact universal `SKILL.md`.
- Move detailed strategic-positioning, drafting, content-quality, and full-authoring procedure into one conditional strategic-authoring reference.
- Move exact README marker validation, deterministic insertion, bounded replacement, and idempotence procedure into one conditional README-synchronization reference.
- Make one copied `VISION.md` skeleton the structural owner of standard headings, section order, optional insertion points, and placeholders without making it a policy owner.
- Preserve ordinary state-based user intent rather than reintroducing public `create`, `revise`, or `mirror` modes.
- Measure actual loaded assemblies and total package size separately.
- Prove semantic and compatibility-literal preservation across canonical, generated, archived, release-candidate, and installed packages.

## Non-goals

- Revising the current project vision or `docs/vision/strategic-positioning.md`.
- Changing the approved vision content model, 750-word normal cap, 900-word hard cap, strategic-positioning fields, methodology exception, README marker pair, or output vocabulary.
- Restoring lowercase root `vision.md` migration behavior or public operating modes.
- Making `vision` a normal per-change lifecycle stage or creating a `vision-review` skill.
- Migrating or rewriting historical proposals, specs, plans, reviews, or change-local evidence.
- Creating a README helper script, prompt-output grader, tokenizer dependency, agent-runtime harness, or executable vision engine.
- Adding a second strategic rationale artifact, generated content cache, new lifecycle state, persistence owner, or external integration.
- Refactoring unrelated skills except directly coupled validator, package, selector, or contract consumers.

## Vision fit

fits the current vision

This change makes the project-vision workflow easier to inspect and use while preserving its durable rationale, human authority, and Git-tracked source of truth. It reduces irrelevant procedure without turning vision work into a hidden runtime, autonomous decision-maker, or prose-generation benchmark.

## Context

The approved `specs/vision-skill.md` is the active consolidated contract. It incorporates the accepted lowercase-path and state-based migration and the later strategic-positioning requirements. The historical focused migration spec remains useful compatibility evidence, but its superseded 500-word language is not the current word-limit authority.

The current package contains only `skills/vision/SKILL.md`. The repository's published-skill model already supports mapped references and assets, generated packages, release archives, and installed parity. This proposal uses that package model; it does not invent a new resource loader or state mechanism.

Current deterministic tests rely on exact headings and phrases in `SKILL.md`, including `State-Based Behavior`, `Strategic Positioning`, `Drafting Heuristics`, marker literals, path literals, word-limit phrases, and output labels. Before editing, every such consumer must be classified as a normative contract, parser/package contract, test-only incidental assertion, historical fixture, or obsolete dependency. The implementation may relocate behaviorally significant wording only when its complete consumer set is updated in the same reviewed slice.

## Options Considered

### Option 1: Keep the flat package

This has no migration risk and keeps current validators unchanged. It retains the 2,268-word cost for every invocation and leaves structure, strategic method, README mechanics, and universal authority interleaved.

### Option 2: Compress only `SKILL.md`

Editorial compression could reduce total package size. It would still require simple assessment and README synchronization to load strategic fixtures and full drafting method, and aggressive compression would make safety and applicability rules harder to review.

### Option 3: Add one catch-all reference

A compact main file plus one reference would create a disclosure boundary, but README synchronization and strategic authoring are independent. A README-only invocation would still load product-category analysis, and an assessment that later needs only marker handling would acquire unrelated authoring procedure.

### Option 4: Use two conditional references and one structural asset

Keep universal classification and safety inline. Put strategic vision authoring in one reference, README synchronization in another, and stable document structure in one copied skeleton. This follows two real procedural activation boundaries and gives repeated structure one non-normative owner.

### Option 5: Split every concern or add executable machinery

Separate references for positioning, heuristics, content validation, revision, and output would increase navigation and missing-resource states. A script or runtime could enforce markers or prose shape, but it would create disproportionate architecture, portability, and acceptance surface for a judgment-heavy skill.

## Recommended Direction

Choose Option 4:

```text
compact universal skills/vision/SKILL.md
+ references/strategic-vision-authoring.md
+ references/readme-vision-sync.md
+ assets/vision-skeleton.md
+ no scripts
```

### Classify operation independently from revision significance

Use these internal operation values:

```text
assess-vision
establish-vision
revise-vision
sync-readme
```

These values describe behavior and loaded resources; they are not user-facing modes. Legacy words remain ordinary intent hints and are never required or reported as modes.

For `revise-vision`, classify revision significance separately:

```text
editorial
substantive-nonmaterial
material-repositioning
```

The focused specification may select exact labels, but it must retain the approved `substantive` versus `editorial` result vocabulary. `substantive-nonmaterial` and `material-repositioning` are procedural sub-classifications of a substantive result, not new user-visible revision results.

### Bind operations to repository state and authority

| Requested behavior | Canonical state | Result |
| --- | --- | --- |
| Assess current vision | `VISION.md` present | Read-only assessment; no vision or README write |
| Assess current vision | `VISION.md` absent | Report no canonical vision; no implicit establishment |
| Establish vision | `VISION.md` absent and intent explicit | Strategic authoring, skeleton composition, rationale creation, and README synchronization permitted |
| Establish vision | `VISION.md` present | Stop; require explicit revision intent |
| Revise vision | `VISION.md` present and exact update intent clear | Classify revision; apply the narrowest authorized edit |
| Revise vision | `VISION.md` absent | Stop; route to explicit establishment |
| Sync README | `VISION.md` present | Leave `VISION.md` unchanged; perform only authorized marker-bounded synchronization |
| Sync README | `VISION.md` absent | Stop because no canonical source exists |
| Any write | Intent, path, authority, markers, or classification ambiguous | Stop before mutation |

An editorial revision loads no strategic reference unless the proposed edit reveals a strategic inconsistency or cannot safely be classified as editorial. A substantive revision loads the strategic reference before final classification. Only initial establishment or material repositioning writes `docs/vision/strategic-positioning.md`; the approved exceptions for changed assumptions or discovered conflict remain intact.

### Keep universal obligations inline

The compact `SKILL.md` remains responsible for:

- workflow placement and no automatic downstream handoff;
- source precedence and canonical-path rules;
- bounded evidence collection and full-read triggers;
- triage of ordinary intent into the four internal operations;
- repository-state, edit-authority, and revision-significance gates;
- substantive change-local causal-link requirements;
- the retired root `vision.md` stop;
- resource selection and missing-resource behavior;
- privacy and external-research boundaries;
- universal stops, claim limits, and result fields.

If a required conditional resource is absent or invalid, the skill stops before dependent judgment or mutation. The main file must not reconstruct missing procedure from memory.

### Give each reference one procedural concern

`references/strategic-vision-authoring.md` owns:

- the ten-field strategic-positioning pass;
- category, substrate, methodology-as-product, audience, mechanism, tradeoff, refusal, and falsifiability judgment;
- current product-category fixtures and drafting heuristics;
- initial and material-repositioning rationale procedure;
- word-limit application, optional methodology section applicability, full-content quality scan, and strategic output summary.

It remains subordinate to the active spec and `SKILL.md`. It does not decide write authority, lifecycle routing, or README behavior.

`references/readme-vision-sync.md` owns:

- exact marker-pair validation;
- malformed, nested, multiple, and missing-marker handling;
- deterministic initial or explicitly authorized marker insertion;
- front-matter derivation and permitted content;
- bounded replacement, outside-byte preservation, idempotence, and README result reporting.

It does not authorize establishment, revision, marker insertion, or skipping. Those decisions remain inline.

### Make the asset structural only

`assets/vision-skeleton.md` owns the standard headings, their order, the optional methodology insertion point, the optional `Open questions` insertion point, and fillable placeholders. It contains no policy about when a section applies, what evidence is adequate, who may edit, word limits, README behavior, or strategic quality.

Use the skeleton for initial creation and an explicitly authorized full-document rewrite. Narrow revision edits the existing document in place and does not force historical documents through the current skeleton. The strategic reference decides whether the optional methodology section is applicable before copying; unresolved applicability becomes an open question rather than invented content.

### Define actual loaded assemblies

| Assembly | Trigger | Loaded procedure | Structural asset |
| --- | --- | --- | --- |
| `VA0-assessment` | `assess-vision` | `SKILL.md` | none |
| `VA1-readme-sync` | `sync-readme` | `SKILL.md` + README reference | none |
| `VA2-editorial-revision` | confirmed editorial `revise-vision` | `SKILL.md`; README reference only when sync is requested or required by the authorized operation | none |
| `VA3-strategic-authoring` | `establish-vision` or substantive revision | `SKILL.md` + strategic reference; README reference when synchronization is in scope | skeleton only for creation or full rewrite |

Late evidence that changes classification loads the newly required resource before dependent judgment or write. It does not silently change user intent or expand write authority.

## Expected Behavior Changes

- Read-only assessment no longer loads strategic drafting or README mutation procedure.
- README-only synchronization loads exact marker procedure but not product positioning or drafting fixtures.
- A confirmed editorial update loads universal revision safety and only the additional procedure actually required.
- Establishment and substantive revision retain complete strategic judgment through the conditional reference.
- Initial creation and authorized full rewrites use a single structural skeleton; narrow edits preserve existing document structure.
- Existing user intent, output vocabulary, word limits, rationale ownership, README markers, canonical path, and historical compatibility remain unchanged.
- Current validators may inspect the assembled package rather than require every normative literal to remain in `SKILL.md`.

## Architecture Impact

Perform a bounded architecture assessment and expect `architecture-not-required`. The proposal uses the existing published-skill package, resource-map, asset-copy, generated-output, archive, and installation model. It introduces no service, runtime, persistence mechanism, schema, lifecycle state, external system, or new authority owner.

A documentation-only architecture correction is required if current architecture inventory depicts `vision` as permanently flat. Architecture becomes required only if implementation discovers that conditional resources or structural assets need a new loader, persistent classification state, generated-content owner, or executable README synchronization mechanism.

## Testing and Verification Strategy

Before refactoring, create two change-local inventories:

1. a semantic-rule ledger assigning every current rule to retained inline, strategic reference, README reference, asset structure, clarified contract, intentionally retired, or historical-only treatment;
2. a literal-compatibility ledger classifying every exact consumer as normative contract, parser/package contract, test-only incidental, historical fixture, or obsolete.

Use deterministic scenarios for:

- all operation/state matrix rows and ambiguous intent;
- editorial, substantive nonmaterial, and material repositioning classification;
- first establishment, narrow revision, and authorized full rewrite;
- strategic rationale create, update, unchanged, conflict, and causal-link gates;
- standard and methodology-oriented structure;
- README valid, missing, malformed, nested, duplicate, explicit insertion, skip, unchanged, and outside-byte preservation cases;
- retired lowercase root path behavior;
- missing, invalid, and late-loaded resources;
- sensitive inputs, research provenance, word caps, and truthful result fields;
- canonical, generated, archived, release-candidate, and clean-installed resource parity.

Measure normalized-LF Unicode whitespace-separated words and UTF-8 bytes for `VA0` through `VA3`. Count each unique loaded procedural resource once in `SKILL.md`, strategic-reference, README-reference order. Exclude copied assets from procedural totals and report the skeleton separately. Record file paths and content identities. Report total package words and bytes separately so moving prose into resources is not presented as deletion.

Each primary procedural assembly must decrease from the current flat baseline of 2,268 words and 15,845 bytes. The complete package may grow when structure and conditional procedure become explicit; that growth remains visible and is acceptable only when every real loaded path shrinks and ownership becomes clearer.

Use existing skill validation, selector tests, build checks, adapter tests, lifecycle checks, and package parity. Update existing validators and fixtures rather than adding a permanent simplicity validator or new validator family. Do not execute Codex, Claude Code, opencode, or another target-agent runtime as acceptance, and do not add a separate manual prose-grading gate.

## Rollout and Rollback

Roll out after an approving proposal review, focused contract amendment, bounded architecture assessment, reviewed plan, and test specification:

1. Freeze baselines, rule ownership, literal consumers, and package inventory.
2. Amend the active vision contract only where resource loading, structural ownership, or internal classification must become explicit.
3. Add the two mapped references and one asset; compact the canonical skill.
4. Update directly coupled validators, fixtures, selector expectations, and package manifests atomically.
5. Rebuild supported generated and release-candidate outputs through repository-owned generators.
6. Prove every loaded assembly reduction and canonical-through-installed parity.

Existing `VISION.md`, strategic-positioning rationale, README front-matter, and historical artifacts remain unchanged. No data migration or reverse synchronization is required.

Rollback restores the prior flat `SKILL.md`, removes the mapped references and skeleton, restores the prior package inventory and validator expectations from the same reviewed revision, rebuilds generated outputs, and reruns package validation. It does not restore lowercase-path behavior, public modes, or superseded word limits.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Universal write or privacy safety moves behind a conditional trigger. | Freeze rule ownership first and keep authority, canonical paths, privacy, research, stops, claims, and triggers inline. |
| Editorial changes bypass strategic inconsistencies. | Load the strategic reference whenever evidence prevents confident editorial classification or reveals changed assumptions or conflict. |
| README reference is mistaken for marker-insertion authority. | Keep authorization inline; the reference owns mechanics only. |
| The skeleton becomes a second vision specification. | Limit it to labels, ordering, insertion points, and placeholders; reject applicability or adequacy policy in the asset. |
| Existing tests freeze obsolete file placement. | Classify literal consumers and update test-only assertions to inspect the assembled owning package. |
| Total package grows while main-file shrinkage is overstated. | Measure every real procedural assembly, the asset, references, and total package separately. |
| Generated and installed packages mix resource versions. | Require canonical-through-installed identities and missing-resource failure scenarios. |
| Historical documents are rewritten to match the new skeleton. | Apply the skeleton prospectively to creation or explicit full rewrite only. |

## Open Questions

None at proposal level. Exact schema field names, fixture representation, and validation command composition remain downstream specification and planning details.

## Decision Log

| Date | Decision | Rationale | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-17 | Preserve the active consolidated vision contract. | The accepted state-based, strategic-positioning, marker, and safety behavior remains useful; loading and ownership are the problem. | Redesign vision behavior; restore older migration rules. |
| 2026-08-17 | Use two conditional references. | Strategic authoring and README synchronization activate independently and have distinct failure boundaries. | Flat file, inline compression, catch-all reference, fragmented references. |
| 2026-08-17 | Use one structural skeleton prospectively. | Stable heading order is repeated output structure, while narrow historical edits should remain bounded. | No structural owner; policy-heavy template; mandatory historical rewrite. |
| 2026-08-17 | Separate operation from revision significance. | Assessment, establishment, revision, and sync decide behavior; editorial versus substantive decides deeper procedure and evidence. | Public modes; one overloaded state value. |
| 2026-08-17 | Measure real loaded assemblies and total package separately. | Main-file shrinkage is not simplification when conditional paths load equal or greater procedure. | Main-file-only metric; fixed percentage target; tokenizer dependency. |
| 2026-08-17 | Exclude target-agent and separate prose-grading acceptance. | Static contract, package, and lifecycle proof is proportionate for a content/package refactor. | Runtime journeys, transcript grading, permanent simplicity validator. |

## Next Artifacts

- Independent `proposal-review` of value, operation closure, resource ownership, structure, compatibility, measurement, architecture awareness, and spec readiness.
- Focused amendment to `specs/vision-skill.md` and its test specification after proposal approval.
- Bounded architecture assessment, expected `architecture-not-required` unless a new package or state mechanism is discovered.
- Reviewed execution plan and focused test specification before implementation.

## Follow-on Artifacts

None yet

## Readiness

Ready for independent proposal review. It does not claim proposal acceptance, specification readiness, architecture settlement, implementation authority, verification, or PR readiness.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Optimize the `vision` skill after the previous skill-simplification sequence. | in scope | Problem, Goals, Recommended Direction |
| Identify the best progressive-disclosure package. | in scope | Options Considered, Recommended Direction |
| Preserve approved vision quality and safety. | in scope | Goals, Expected Behavior Changes, Risks and Mitigations |
| Avoid unnecessary scripts, runtimes, or manual semantic acceptance. | in scope | Non-goals, Testing and Verification Strategy |
| Create a new branch, author a proposal, and perform proposal review. | in scope | Owning change record, Next Artifacts, Readiness |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Compact universal vision contract | core to this proposal | It is the common-path simplification surface. |
| Strategic-authoring reference | core to this proposal | It isolates the deep positioning and drafting method. |
| README-synchronization reference | core to this proposal | It isolates exact marker and bounded-replacement mechanics. |
| Vision structural skeleton | core to this proposal | It gives stable repeated output shape one structural owner. |
| Focused active-contract and proof-map amendment | same-slice dependency | Progressive disclosure and structural ownership must be normative before implementation. |
| Existing validator and fixture migration | same-slice dependency | Current tests bind exact behavior to the flat file. |
| Generated, archive, release-candidate, and installed parity | same-slice dependency | Published skill resources must ship together. |
| Bounded architecture assessment | first downstream assessment | It confirms the existing package model is sufficient. |
| Rewrite current project vision or strategic rationale | out of scope | The proposal changes the skill package, not project direction. |
| Target-agent evaluation, prose grading, or helper runtime | out of scope | These add disproportionate machinery and are unnecessary for acceptance. |
| Other skill simplifications | follow-up | They require separate proposals and evidence. |
