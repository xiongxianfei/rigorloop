# Vision Skill Progressive Disclosure

## Owning change record

`docs/changes/2026-08-17-vision-skill-progressive-disclosure/change.yaml`

## Problem

The published `vision` skill preserves the approved project-vision contract, but its single 2,268-word, 15,845-byte `SKILL.md` loads every concern on every invocation. A marker-bounded README synchronization and a typo correction both load the complete strategic-positioning method, product-category fixtures, drafting heuristics, full vision structure, and initial-creation placement procedure.

The flat package also makes structural and procedural ownership difficult to see. The required `VISION.md` section sequence and ten-field `docs/vision/strategic-positioning.md` shape are embedded beside applicability policy; README marker parsing and insertion mechanics are embedded beside universal write authority; and strategic analysis is interleaved with ordinary state classification. Current validators consequently assert many exact phrases directly in `SKILL.md`, even when the behavior could remain normative in a mapped reference or structural asset.

The accepted behavior is not the problem. Root `VISION.md`, state-based behavior, substantive versus editorial revision, strategic-positioning rationale, word limits, README marker safety, retired lowercase-path handling, privacy, research, and output truthfulness must remain intact. The problem is that every path pays for every procedure and repeated structure has no structural owner.

## Goals

- Reduce loaded procedure for the three supported invocation surfaces: README synchronization, editorial revision, and strategic authoring.
- Keep source precedence, repository-state and operation classification, write authority, substantive/editorial classification, canonical paths, privacy, research, stops, claims, resource triggers, and result obligations in a compact universal `SKILL.md`.
- Move detailed strategic-positioning, drafting, content-quality, and full-authoring procedure into one conditional strategic-authoring reference.
- Move exact README marker validation, deterministic insertion, bounded replacement, and idempotence procedure into one conditional README-synchronization reference.
- Give root `VISION.md` and `docs/vision/strategic-positioning.md` separate copied structural skeletons without making either asset a policy owner.
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

Editorial compression could reduce total package size. It would still require README synchronization and narrow editorial revision to load strategic fixtures and full drafting method, and aggressive compression would make safety and applicability rules harder to review.

### Option 3: Add one catch-all reference

A compact main file plus one reference would create a disclosure boundary, but README synchronization and strategic authoring are independent. A README-only invocation would still load product-category analysis, while strategic authoring would load exact marker procedure even when an authorized skip had already been resolved.

### Option 4: Use two conditional references and two structural assets

Keep universal classification and safety inline. Put strategic vision authoring in one reference, README synchronization in another, and the two stable artifact shapes in separate copied skeletons. This follows two real procedural activation boundaries and gives each repeated structure one non-normative owner.

### Option 5: Split every concern or add executable machinery

Separate references for positioning, heuristics, content validation, revision, and output would increase navigation and missing-resource states. A script or runtime could enforce markers or prose shape, but it would create disproportionate architecture, portability, and acceptance surface for a judgment-heavy skill.

## Recommended Direction

Choose Option 4:

```text
compact universal skills/vision/SKILL.md
+ references/strategic-vision-authoring.md
+ references/readme-vision-sync.md
+ assets/vision-skeleton.md
+ assets/strategic-positioning-skeleton.md
+ no scripts
```

### Classify operation independently from revision significance

Use these internal operation values:

```text
establish-vision
revise-vision
sync-readme
```

These values describe behavior and loaded resources; they are not user-facing modes. Legacy words remain ordinary intent hints and are never required or reported as modes. The current repository has no formal caller or approved contract for `assess-vision`, so the first version does not invent or measure that operation. Ordinary read-only questions may be answered without entering the vision mutation operation model.

For `revise-vision`, classify revision significance separately:

```text
editorial
substantive-nonmaterial
material-repositioning
```

The focused specification may select exact labels, but it must retain the approved `substantive` versus `editorial` result vocabulary. `substantive-nonmaterial` and `material-repositioning` are procedural sub-classifications of a substantive result, not new user-visible revision results.

After resolving one of the three mutation operations, classify resource needs independently:

```text
strategic_authoring_context:
  false
  true

readme_sync_context:
  required
  skipped
```

`blocked` is an operation result, not a loaded profile. Uncertain marker state requires the README reference before a blocker can be concluded. Late strategic evidence changes `strategic_authoring_context` to `true` and loads the strategic reference before final classification or any write.

### Bind operations to repository state and authority

| Requested behavior | Canonical state | Result |
| --- | --- | --- |
| Establish vision | `VISION.md` absent and intent explicit | Strategic authoring, skeleton composition, rationale creation, and README synchronization permitted |
| Establish vision | `VISION.md` present | Stop; require explicit revision intent |
| Revise vision | `VISION.md` present and exact update intent clear | Classify revision; apply the narrowest authorized edit |
| Revise vision | `VISION.md` absent | Stop; route to explicit establishment |
| Sync README | `VISION.md` present | Leave `VISION.md` unchanged; perform only authorized marker-bounded synchronization |
| Sync README | `VISION.md` absent | Stop because no canonical source exists |
| Any write | Intent, path, authority, markers, or classification ambiguous | Stop before mutation |

An editorial revision loads no strategic reference unless the proposed edit reveals a strategic inconsistency or cannot safely be classified as editorial. A substantive revision loads the strategic reference before final classification. Revision significance does not by itself decide whether the positioning rationale changes; the independent positioning action below applies the approved changed-assumption and discovered-conflict exceptions.

### Close README synchronization applicability

README synchronization remains part of establishment and vision revision by default. It is not a separately optional afterthought merely because its procedure moves to a reference.

| Vision operation | README authority and result | README reference |
| --- | --- | --- |
| `establish-vision` | Synchronize README; automatic marker insertion is permitted by the approved initial-establishment rule | required |
| `revise-vision` with one valid marker pair | Synchronize the derived front-matter | required |
| `revise-vision` with exact current skip authority resolved before marker-dependent judgment | Leave README unchanged and report `skipped` | not required |
| `revise-vision` with exact current insertion authority | Insert one block at the deterministic location and synchronize it | required |
| `revise-vision` with missing, malformed, nested, duplicate, or ambiguous markers and no exact insertion or skip authority | Stop before any vision or README write | required |
| `sync-readme` | Leave `VISION.md` unchanged and synchronize through the approved marker rules | required |

Missing or malformed markers never imply skip authority. If skip authority is not already exact and current, load the README reference before marker-dependent judgment or any vision write. This preserves the active contract's fail-closed update behavior and makes each primary assembly deterministic.

### Classify secondary-artifact actions independently

Use these internal action values:

```text
positioning_action:
  unchanged
  create
  update
  full-rewrite
  blocked

readme_action:
  synchronize-existing
  insert-and-synchronize
  skip
  blocked
```

These actions do not change the public `substantive` or `editorial` revision result.

| Vision condition | Positioning action |
| --- | --- |
| Initial establishment | `create`; an unrelated pre-existing rationale blocks adoption |
| Editorial revision | `unchanged`; uncertainty or strategic inconsistency forces substantive reclassification before writing |
| Substantive nonmaterial revision with no positioning effect | `unchanged` |
| Changed positioning assumption under active contract R78 | `update` |
| Discovered conflict under R77 with one authorized correction | `update`; unresolved owner choice is `blocked` |
| Material repositioning under R73-R79 | `update`, `create` when the required rationale is absent, or explicitly authorized `full-rewrite` |
| Applicability, identity, or authority unresolved | `blocked` |

The strategic reference determines positioning meaning and adequacy. The main file determines whether the selected positioning action is authorized. Narrow `update` preserves existing structure; `create` and `full-rewrite` use the positioning skeleton.

| Vision and README condition | README action | Authority basis |
| --- | --- | --- |
| Establishment with one valid block | `synchronize-existing` | establishment operation plus R41-R44 |
| Establishment with no marker block | `insert-and-synchronize` | automatic initial-establishment authority in R43 |
| Establishment with malformed, nested, or multiple markers | `blocked` | no automatic repair authority |
| Revision or explicit sync with one valid block | `synchronize-existing` | current operation plus R44 |
| Revision with no block and exact current insertion instruction | `insert-and-synchronize` | current owner instruction under R45-R46 |
| Revision with exact current skip instruction | `skip` | current owner instruction under R45 |
| Missing or invalid markers without exact current handling | `blocked` | R45 fail-closed behavior |

Every insertion or skip binds the governing requirement ID or exact current owner instruction, mutation operation, current `VISION.md` identity, current README identity, observed marker state, and authorized action. A change to the vision, README, markers, operation, or authority basis invalidates the decision. Silence, conversational omission, malformed markers, remembered approval, or historical authority never implies insertion or skip.

### Keep universal obligations inline

The compact `SKILL.md` remains responsible for:

- workflow placement and no automatic downstream handoff;
- source precedence and canonical-path rules;
- bounded evidence collection and full-read triggers;
- triage of ordinary intent into exactly three internal mutation operations;
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

### Make both assets structural only

`assets/vision-skeleton.md` owns the standard headings, their order, the optional methodology insertion point, the optional `Open questions` insertion point, and fillable placeholders. It contains no policy about when a section applies, what evidence is adequate, who may edit, word limits, README behavior, or strategic quality.

Use the skeleton for initial creation and an explicitly authorized full-document rewrite. Narrow revision edits the existing document in place and does not force historical documents through the current skeleton. The strategic reference decides whether the optional methodology section is applicable before copying; unresolved applicability becomes an open question rather than invented content.

`assets/strategic-positioning-skeleton.md` owns the ten compact positioning headings, their order, the location of the statement that `VISION.md` remains canonical, and fillable placeholders. It contains no rules for when positioning is required, what evidence satisfies a field, conflict settlement, revision authority, or whether the rationale is adequate.

Use the positioning skeleton for initial establishment, material repositioning, or an explicitly authorized full rationale rewrite. Narrow updates preserve the existing rationale structure. The strategic reference owns applicability, field meaning, evidence quality, conflict behavior, and the decision to copy or update the asset.

### Define actual loaded assemblies

| Assembly | Trigger | Loaded procedure | Structural asset |
| --- | --- | --- | --- |
| `VA0-readme-sync` | `sync-readme` | `SKILL.md` + README reference | none |
| `VA1-editorial-sync` | confirmed editorial `revise-vision` with normal synchronization | `SKILL.md` + README reference | none |
| `VA1S-editorial-skip` | confirmed editorial revision with exact pre-resolved skip authority | `SKILL.md` | none |
| `VA2-strategic-sync` | `establish-vision` or substantive revision with synchronization | `SKILL.md` + strategic reference + README reference | vision skeleton for creation/full rewrite; positioning skeleton when rationale creation/full rewrite applies |
| `VA2S-strategic-skip` | substantive revision with exact pre-resolved README skip authority | `SKILL.md` + strategic reference | positioning skeleton only when rationale creation/full rewrite applies |

`VA0`, `VA1`, and `VA2` are the three primary real assemblies. `VA1S` and `VA2S` are supported secondary authority variants and must not replace normal synchronization profiles in acceptance measurements. Initial establishment always uses `VA2-strategic-sync`. Late evidence loads every newly required resource before dependent judgment or write; previously gathered evidence may be retained, but the smaller profile cannot authorize mutation after its trigger becomes stale.

### Use one bounded multi-artifact update protocol

Every mutating invocation resolves one exact target manifest before the first write. Each included target records path, role, action, prior identity or confirmed absence, and intended identity. Targets not applicable to the classified operation are omitted rather than represented as implicit no-ops.

```yaml
vision_update:
  operation: revise-vision
  revision_significance: material-repositioning
  positioning_action: update
  readme_action: synchronize-existing
  targets:
    - path: VISION.md
      role: canonical
      action: revise
      prior_identity: sha256:<old>
      intended_identity: sha256:<new>
    - path: docs/vision/strategic-positioning.md
      role: rationale
      action: revise
      prior_identity: sha256:<old>
      intended_identity: sha256:<new>
    - path: README.md
      role: derived
      action: synchronize
      prior_identity: sha256:<old>
      intended_identity: sha256:<new>
```

Before mutation:

1. Resolve operation, significance, secondary actions, paths, authority, and current identities.
2. Prepare all intended content in memory or safely isolated temporary files.
3. Validate word limits, structural completeness, positioning applicability, README markers, skip/insertion authority, privacy, research provenance, and intended identities.
4. Re-read every target identity and stop if any baseline changed.

Write in source-first order:

1. Atomically replace canonical `VISION.md`.
2. Atomically create or update strategic-positioning rationale when applicable.
3. Atomically update derived README content last.
4. Read back every required target and compare it with the manifest.

Use closed operation results:

```text
complete
partial-retry-required
blocked-before-write
```

`complete` requires every required target to match its intended identity. `blocked-before-write` performs no target mutation. `partial-retry-required` reports the exact committed targets, pending targets, current identities, manifest identity, and required retry action; it never claims the vision package is synchronized.

For governed work, persist the complete manifest in the existing change-local authoring evidence before the first target write when that approved evidence surface supports the fields. An exact retry may finish only pending targets when the operation and manifest are unchanged, committed files retain intended identities, pending files retain their expected prior or safe partial identities, and authority remains current.

Portable work adds no new tracked transaction artifact. It may resume within the same retained invocation context when the complete manifest is available and every identity matches. If the manifest was lost, cannot be represented by an existing authorized evidence surface, or any target is unrelated, stale, ambiguous, or concurrently changed, stop and require explicit owner-directed recovery rather than adopt or overwrite the state. If cross-session portable recovery becomes a required product capability, architecture is required before implementation.

## Expected Behavior Changes

- README-only synchronization loads exact marker procedure but not product positioning or drafting fixtures.
- A normal editorial update loads universal revision safety and README synchronization, while an explicitly skipped variant stays compact and reports the skip truthfully.
- Establishment and substantive revision retain complete strategic judgment through the conditional reference, including the `VA2S` path when README skip authority is exact.
- Positioning and README actions are decided independently from public revision significance.
- Multi-artifact writes validate one manifest, commit canonical vision before supporting and derived surfaces, and report partial state without claiming completion.
- Initial creation and authorized full rewrites use the applicable vision and positioning skeletons; narrow edits preserve existing document structure.
- Existing user intent, output vocabulary, word limits, rationale ownership, README markers, canonical path, and historical compatibility remain unchanged.
- Current validators may inspect the assembled package rather than require every normative literal to remain in `SKILL.md`.

## Architecture Impact

Perform a bounded architecture assessment and expect `architecture-not-required` when the existing authoring-evidence model can carry the governed target manifest and portable execution remains fail-closed when retained manifest evidence is unavailable. The proposal uses the existing published-skill package, resource-map, asset-copy, generated-output, archive, and installation model. It introduces no service, runtime, persistence mechanism, schema, lifecycle state, external system, or new authority owner.

A documentation-only architecture correction is required if current architecture inventory depicts `vision` as permanently flat. Architecture becomes required if implementation discovers that conditional resources or either structural asset need a new loader, governed recovery needs a new persisted transaction surface, cross-session portable recovery becomes required, action classification needs a persistent owner, or README synchronization becomes executable machinery.

## Testing and Verification Strategy

Before refactoring, create two change-local inventories:

1. a semantic-rule ledger assigning every current rule to retained inline, strategic reference, README reference, asset structure, clarified contract, intentionally retired, or historical-only treatment;
2. a literal-compatibility ledger classifying every exact consumer as normative contract, parser/package contract, test-only incidental, historical fixture, or obsolete.

Use deterministic scenarios for:

- all three operation/state matrix rows and ambiguous intent;
- all five loaded assemblies and late editorial-to-strategic reclassification;
- editorial, substantive nonmaterial, and material repositioning classification;
- every `positioning_action` and `readme_action` row, authority source, identity invalidation, and blocked result;
- first establishment, narrow revision, and authorized full rewrite;
- strategic rationale create, update, unchanged, conflict, and causal-link gates;
- standard and methodology-oriented vision structure plus all ten strategic-positioning headings and authority statement;
- README valid, missing, malformed, nested, duplicate, explicit insertion, skip, unchanged, and outside-byte preservation cases;
- retired lowercase root path behavior;
- missing, invalid, and late-loaded resources;
- manifest preparation, baseline change before write, each interruption point, committed/pending reporting, exact retry, lost portable manifest, and concurrent edit;
- sensitive inputs, research provenance, word caps, and truthful result fields;
- canonical, generated, archived, release-candidate, and clean-installed resource parity.

Measure normalized-LF Unicode whitespace-separated words and UTF-8 bytes for primary assemblies `VA0`, `VA1`, and `VA2` and secondary variants `VA1S` and `VA2S`. Count each unique loaded procedural resource once in `SKILL.md`, strategic-reference, README-reference order. Exclude copied assets from procedural totals and report both skeletons separately. Record file paths and content identities. Report total package words and bytes separately so moving prose into resources is not presented as deletion.

Each primary procedural assembly must decrease from the current flat baseline of 2,268 words and 15,845 bytes. `VA1S` and `VA2S` must also be reported but cannot substitute for `VA1` or `VA2`. The complete package may grow when structure and conditional procedure become explicit; that growth remains visible and is acceptable only when every real loaded path shrinks and ownership becomes clearer.

Use existing skill validation, selector tests, build checks, adapter tests, lifecycle checks, and package parity. Update existing validators and fixtures rather than adding a permanent simplicity validator or new validator family. Do not execute Codex, Claude Code, opencode, or another target-agent runtime as acceptance, and do not add a separate manual prose-grading gate.

The downstream contract and proof map must preserve these acceptance decisions:

| ID | Criterion |
| --- | --- |
| `AC-VISSIM-001` | Every measured procedural profile corresponds to a current supported invocation surface. |
| `AC-VISSIM-002` | No formal `assess-vision` operation or measurement profile is introduced without a later evidence-backed contract. |
| `AC-VISSIM-003` | Establishment always applies the approved README synchronization behavior. |
| `AC-VISSIM-004` | Revision loads README procedure unless exact current skip authority was resolved before marker-dependent judgment. |
| `AC-VISSIM-005` | Missing, malformed, nested, duplicate, or ambiguous markers never imply skip authority. |
| `AC-VISSIM-006` | Revision-with-sync is represented as the primary editorial loaded assembly. |
| `AC-VISSIM-007` | Root vision and strategic-positioning rationale have separate explicit structural owners. |
| `AC-VISSIM-008` | Both assets own labels, ordering, insertion locations, and placeholders only. |
| `AC-VISSIM-009` | Strategic and README applicability, evidence adequacy, and write authority remain procedural. |
| `AC-VISSIM-010` | Both structural assets are reported separately from procedural loaded-context totals. |
| `AC-VISSIM-011` | Canonical, generated, archived, release-candidate, and installed resources retain required parity. |
| `AC-VISSIM-012` | No target-agent runtime or separate prose-grading system is used for acceptance. |
| `AC-VISSIM-013` | The mutation operation vocabulary contains exactly `establish-vision`, `revise-vision`, and `sync-readme`. |
| `AC-VISSIM-014` | Read-only questions remain outside the mutation operation model. |
| `AC-VISSIM-015` | Strategic and README procedure applicability are classified independently. |
| `AC-VISSIM-016` | Every supported resource combination has one named assembly. |
| `AC-VISSIM-017` | A substantive revision with exact skip authority uses `VA2S-strategic-skip`. |
| `AC-VISSIM-018` | Late strategic discovery loads the strategic reference before final classification or mutation. |
| `AC-VISSIM-019` | Every mutating invocation resolves one exact target manifest before writing. |
| `AC-VISSIM-020` | Marker, authority, content, path, and identity checks complete before the first target write. |
| `AC-VISSIM-021` | Canonical vision writes precede rationale and README-derived writes. |
| `AC-VISSIM-022` | Partial operations report committed and pending targets and never claim completion. |
| `AC-VISSIM-023` | Exact retry adopts no unrelated, stale, ambiguous, or concurrently changed file. |
| `AC-VISSIM-024` | Positioning action is classified independently from the public revision result. |
| `AC-VISSIM-025` | README insertion and skip bind an exact current authority source and current target identities. |
| `AC-VISSIM-026` | Silence, malformed markers, remembered approval, and historical authority never imply skip or insertion. |
| `AC-VISSIM-027` | Historical vision and rationale documents are not rewritten merely to adopt the new skeletons. |
| `AC-VISSIM-028` | Architecture becomes required if safe recovery needs a new persistent transaction or authority owner. |

## Rollout and Rollback

Roll out after an approving proposal review, focused contract amendment, bounded architecture assessment, reviewed plan, and test specification:

1. Freeze baselines, rule ownership, literal consumers, package inventory, and current multi-file authority/evidence capabilities.
2. Amend the active vision contract where resource loading, secondary actions, structural ownership, manifest recovery, or internal classification must become explicit.
3. Add the two mapped references and two structural assets; compact the canonical skill.
4. Update directly coupled validators, fixtures, selector expectations, and package manifests atomically.
5. Rebuild supported generated and release-candidate outputs through repository-owned generators.
6. Prove every loaded assembly reduction and canonical-through-installed parity.

Existing `VISION.md`, strategic-positioning rationale, README front-matter, and historical artifacts remain unchanged. No data migration or reverse synchronization is required.

Rollback restores the prior flat `SKILL.md`, removes the mapped references and both skeletons, restores the prior package inventory and validator expectations from the same reviewed revision, rebuilds generated outputs, and reruns package validation. It does not restore lowercase-path behavior, public modes, or superseded word limits.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Universal write or privacy safety moves behind a conditional trigger. | Freeze rule ownership first and keep authority, canonical paths, privacy, research, stops, claims, and triggers inline. |
| Editorial changes bypass strategic inconsistencies. | Load the strategic reference whenever evidence prevents confident editorial classification or reveals changed assumptions or conflict. |
| README reference is mistaken for marker-insertion authority. | Keep authorization inline; the reference owns mechanics only. |
| A substantive skip path is omitted from proof or package accounting. | Treat strategic and README contexts independently and measure `VA2S` explicitly. |
| Partial multi-file work is mistaken for completion. | Require one manifest, source-first order, complete read-back, and a distinct `partial-retry-required` result. |
| A retry overwrites unrelated or concurrent edits. | Resume only the exact retained or governed manifest with matching target identities; otherwise stop. |
| Positioning changes are inferred solely from substantive/editorial labels. | Classify `positioning_action` independently using R73-R79 and current authority. |
| Either skeleton becomes a second vision specification. | Limit both to labels, ordering, insertion points, authority-statement location, and placeholders; reject applicability or adequacy policy in assets. |
| Existing tests freeze obsolete file placement. | Classify literal consumers and update test-only assertions to inspect the assembled owning package. |
| Total package grows while main-file shrinkage is overstated. | Measure every real procedural assembly, both assets, references, and total package separately. |
| Generated and installed packages mix resource versions. | Require canonical-through-installed identities and missing-resource failure scenarios. |
| Historical documents are rewritten to match new skeletons. | Apply each skeleton prospectively to creation or explicit full rewrite only. |

## Open Questions

None at proposal level. Exact schema field names, fixture representation, and validation command composition remain downstream specification and planning details.

## Decision Log

| Date | Decision | Rationale | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-17 | Preserve the active consolidated vision contract. | The accepted state-based, strategic-positioning, marker, and safety behavior remains useful; loading and ownership are the problem. | Redesign vision behavior; restore older migration rules. |
| 2026-08-17 | Use two conditional references. | Strategic authoring and README synchronization activate independently and have distinct failure boundaries. | Flat file, inline compression, catch-all reference, fragmented references. |
| 2026-08-17 | Use separate vision and strategic-positioning skeletons prospectively. | Both authored artifacts have stable required shapes, while narrow historical edits should remain bounded. | Missing rationale owner; policy-heavy template; mandatory historical rewrite. |
| 2026-08-17 | Separate operation from revision significance. | Establishment, revision, and sync decide behavior; editorial versus substantive decides deeper procedure and evidence. | Public modes; one overloaded state value. |
| 2026-08-17 | Do not add formal `assess-vision` in the first version. | No current approved caller or result contract supports it, so it would be an artificial acceptance surface. | Measure an invented compact profile. |
| 2026-08-17 | Preserve README synchronization as the revision default. | README is a derived vision surface; only exact current skip authority may omit its procedure and write. | Request-dependent or implicit synchronization; malformed markers as skip. |
| 2026-08-17 | Classify strategic and README resource needs independently. | Substantive revision with exact skip authority is a real path and must have its own assembly. | Force README procedure into every strategic revision; omit `VA2S`. |
| 2026-08-17 | Use a source-first target manifest for multi-file writes. | Canonical vision must settle before supporting rationale and derived README, and partial work must be recoverable or fail closed. | Unordered writes; silent partial completion; destructive rollback. |
| 2026-08-17 | Keep portable recovery fail-closed without new persistence. | The simplification should not create a transaction subsystem; lost or ambiguous manifests require owner-directed recovery. | New portable transaction artifact; implicit adoption. |
| 2026-08-17 | Classify positioning and README actions independently. | Revision significance does not exhaust secondary-artifact applicability or authority. | Infer all secondary writes from editorial/substantive alone. |
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
| Vision structural skeleton | core to this proposal | It owns the canonical vision document shape. |
| Strategic-positioning structural skeleton | core to this proposal | It owns the required ten-field rationale shape. |
| Exhaustive resource and secondary-action classifiers | core to this proposal | Every valid strategic/README combination and write action needs deterministic procedure and authority. |
| Multi-artifact target manifest and fail-closed recovery | core to this proposal | Establishment and material repositioning can touch canonical, rationale, and derived surfaces in one invocation. |
| Focused active-contract and proof-map amendment | same-slice dependency | Progressive disclosure and structural ownership must be normative before implementation. |
| Existing validator and fixture migration | same-slice dependency | Current tests bind exact behavior to the flat file. |
| Generated, archive, release-candidate, and installed parity | same-slice dependency | Published skill resources must ship together. |
| Bounded architecture assessment | first downstream assessment | It confirms the existing package model is sufficient. |
| Rewrite current project vision or strategic rationale | out of scope | The proposal changes the skill package, not project direction. |
| Target-agent evaluation, prose grading, or helper runtime | out of scope | These add disproportionate machinery and are unnecessary for acceptance. |
| Other skill simplifications | follow-up | They require separate proposals and evidence. |
