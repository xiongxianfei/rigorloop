# Architecture Skills with C4, arc42, and ADRs

## Status

- accepted

## Problem

RigorLoop needs architecture guidance that contributors and agents can produce consistently, review quickly, and trace back to durable decisions. Current architecture output can drift between ad hoc diagrams, prose-only explanations, and decision notes that are mentioned once and then lost.

That drift creates recurring risks:

- architecture is described visually but not operationally;
- architecture is described in prose but the important structure is hard to see;
- durable decisions and tradeoffs are buried in a larger design document;
- architecture review has to infer which concerns were intentionally omitted and which were missed.

The project needs one default architecture method that separates structural explanation, architecture document structure, and durable decision records without making ordinary non-trivial work too heavy.

## Goals

- Standardize a default architecture package for non-trivial changes that need architecture work.
- Make architecture artifacts easier to review and compare across changes.
- Keep architecture work lightweight enough for normal feature work.
- Make important architecture decisions durable and traceable.
- Preserve flexibility for small changes while giving larger or boundary-changing changes a stronger architecture contract.
- Give `architecture` and `architecture-review` skills clearer defaults for diagrams, written structure, and ADR expectations.
- Keep one canonical system architecture package current through small, reviewed updates instead of creating a new primary architecture document for every feature.

## Non-goals

- Requiring a heavy architecture document for every trivial change.
- Requiring every possible diagram level for every change.
- Replacing execution plans, test specs, review artifacts, or change-local reasoning.
- Making 4+1 the default authored artifact format.
- Forcing full UML or code-level diagrams by default.
- Adding automated architecture validation before the artifact shape has stabilized.
- Rewriting the whole architecture package for every feature.
- Treating feature-specific architecture notes as permanent substitutes for the canonical system architecture package.

## Context

`CONSTITUTION.md` already treats architecture documents and ADRs as lifecycle-managed sources of truth. It also requires architecture-affecting changes to update the relevant architecture document or ADR in the same change.

`docs/workflows.md` defines the full lifecycle as including `architecture` after `spec-review` when architecture is needed, and `architecture-review` when design review is the next required or default downstream step.

The current `skills/architecture/SKILL.md` asks for a broad architecture document with design areas, failure modes, security, performance, observability, compatibility, alternatives, ADRs, risks, and open questions. It also allows Mermaid diagrams when helpful, but it does not define a default diagram language or a compact architecture document shape.

The current `skills/architecture-review/SKILL.md` reviews useful dimensions, including boundary clarity, data ownership, interface safety, failure handling, security, performance, observability, testing feasibility, complexity discipline, ADR quality, and plan readiness. It does not yet give reviewers a shared default for C4 diagram sufficiency, arc42 section completeness, or when missing ADRs should be called out.

C4 is a useful default for structure because it offers a small set of system views and allows teams to stop at the levels that are useful. arc42 is a useful written architecture structure because it covers context, strategy, building blocks, runtime, deployment, cross-cutting concerns, quality, decisions, and risk. ADRs are a useful companion because they preserve important decisions and consequences outside the main prose flow.

## Options considered

### Option 0: Keep current architecture skill guidance and ad hoc diagrams/prose

Advantages:

- no new artifact method to teach;
- no source-boundary update for templates;
- lowest immediate documentation churn.

Disadvantages:

- does not solve drift between diagram-heavy, prose-heavy, and decision-note-heavy architecture artifacts;
- does not give reviewers a shared default for structure, runtime reasoning, deployment reasoning, or ADR thresholds;
- important decisions can still be lost in prose instead of becoming durable ADRs;
- does not make architecture artifacts easier to compare across changes.

### Option 1: Use C4 only

Advantages:

- simple visual standard;
- easy to teach;
- good for fast structural communication.

Disadvantages:

- diagrams alone do not guarantee complete architecture reasoning;
- runtime, deployment, and cross-cutting concerns can be underspecified;
- decisions can still be lost if they are not separately recorded.

### Option 2: Use arc42 only

Advantages:

- strong architecture document structure;
- good coverage of runtime, deployment, quality, and risk;
- easy to review for completeness.

Disadvantages:

- less visual by default;
- can become too prose-heavy;
- does not itself standardize diagram style.

### Option 3: Use ADR only

Advantages:

- strong decision traceability;
- lightweight and durable;
- good for long-term reasoning.

Disadvantages:

- does not explain the whole architecture;
- weak for structure and runtime communication;
- insufficient as the primary architecture method.

### Option 4: Use C4 plus arc42 plus ADRs

Advantages:

- C4 makes structure visible;
- arc42 gives architecture documentation a complete official section model;
- ADRs preserve important decisions and tradeoffs;
- one canonical architecture baseline avoids scattering system truth across many per-feature architecture documents;
- system shape and decision history stay separate;
- fits the existing RigorLoop lifecycle and artifact model.

Disadvantages:

- contributors need to understand three related surfaces;
- the workflow needs clear guidance on when each artifact is expected;
- templates and examples need to stay aligned with skill guidance.

## Recommended direction

Choose Option 4.

RigorLoop should standardize architecture work around:

- C4 for default architecture diagrams;
- arc42 for the main architecture document structure;
- ADRs for durable architecture decisions.

This separates three architecture jobs:

- C4 answers what the structure is;
- arc42 answers which architecture concerns should be documented;
- ADRs answer why an important decision was made and what consequences follow.

RigorLoop should maintain one canonical system architecture package. The default package should include:

- `architecture.md` under the canonical architecture location;
- one C4 system context diagram;
- one C4 container diagram;
- zero or more ADRs when the change introduces or revises a durable architecture decision.

For a new feature, contributors should update only the touched arc42 sections and C4 views. Most feature work should update the lowest affected C4 level first and propagate upward only when the change is real at that level. A feature-specific architecture delta should be added only when the feature is architecture-significant enough to need reviewable design reasoning before it is merged into the baseline. Accepted deltas should be merged back into the canonical package so the repository has one living architecture baseline rather than many competing current architecture documents.

Feature-specific architecture deltas are change-local working artifacts, not competing canonical architecture documents. The default delta path should be:

- `docs/changes/<change-id>/architecture.md`

Optional supporting diagrams for a delta should live under:

- `docs/changes/<change-id>/diagrams/`

During an active change, the change-local architecture delta is the working architecture artifact for that change. Once the change is accepted, its durable content should be merged into the canonical architecture package, and durable decisions should be recorded as ADRs under `docs/adr/`. After merge-back, the change-local delta remains historical evidence under `docs/changes/<change-id>/`; it should not continue to act as the canonical architecture source for downstream work.

Optional additions should stay conditional:

- C4 component diagram when container-level structure is not enough;
- runtime scenario section with sequence or flow detail when behavior, orchestration, failure paths, or operational flow matter;
- deployment view detail when environments, generated outputs, packaging, adapters, or execution boundaries matter;
- additional ADRs for multiple durable decisions;
- architecture-review checklist notes when review findings need durable resolution.

The default `architecture.md` structure should use all 12 official arc42 section headings:

1. Introduction and Goals
2. Architecture Constraints
3. Context and Scope
4. Solution Strategy
5. Building Block View
6. Runtime View
7. Deployment View
8. Crosscutting Concepts
9. Architecture Decisions
10. Quality Requirements
11. Risks and Technical Debt
12. Glossary

Sections should stay concise. "Not applicable" should be acceptable when the section is genuinely irrelevant, but the rationale should be explicit. Architecture work stays lightweight through concise content and explicit "Not applicable" handling, not by changing the official section model.

Default section expectations:

- Sections 1-5 are almost always present in real architecture work.
- Sections 6-8 are required when runtime behavior, cross-cutting rules, operational flows, generated outputs, packaging, adapters, or execution boundaries matter.
- Section 9 is always present. It should summarize and link ADRs, or state that no ADRs are required for the change.
- Section 10 should be short but explicit about the most relevant quality requirements.
- Section 11 records risks and technical debt.
- Section 12 is always represented; when no glossary terms are needed, it may say "Not applicable" with rationale.

C4 defaults should favor enough structural clarity rather than maximum diagram count:

- system context diagram by default;
- container diagram by default;
- component diagram only when container-level structure is insufficient;
- code-level diagram not required by default;
- deployment diagram only when infrastructure or environment mapping matters.

ADR guidance should create an ADR when a change introduces or revises a durable architecture decision, such as:

- system boundary changes;
- adapter generation or packaging rules;
- validation architecture;
- cache or indexing strategy;
- portability constraints;
- release architecture;
- major workflow architecture decisions.

Each ADR should include title, status, context, decision, alternatives considered, consequences, and follow-up. The status set should align with existing lifecycle guidance: `draft`, `proposed`, `accepted`, `active`, `deprecated`, `superseded`, `archived`, and `abandoned`. ADRs should be append-only after acceptance; later changes should supersede older ADRs with a new ADR that references the old one rather than rewriting decision history.

Architecture update cadence should distinguish living baseline sections from stable or snapshot-like records:

- Tier 1 living updates: Building Block View and C4 container/component views, Runtime View for new flows, Deployment View when infrastructure or execution boundaries shift, and ADRs for non-obvious durable decisions.
- Tier 2 occasional updates: Context and Scope or C4 system context when external actors or systems change, Crosscutting Concepts when a new pattern appears, and Quality Requirements when new quality targets or constraints appear.
- Tier 3 rare updates: Introduction and Goals, Architecture Constraints, and Solution Strategy. Changes here indicate a strategic shift and should receive more scrutiny than ordinary feature work.

Architecture docs should live with the code. C4 diagrams should be stored as reviewable source text, such as Mermaid, Structurizr DSL, or PlantUML, with the exact allowed formats settled by the focused spec. Architecture changes should be reviewed in the same pull request as the feature that requires them, so reviewers can diff architecture changes like code changes.

Feature completion should be architecture-aware without forcing documentation churn:

- A feature that changes architecture should update the C4 component view, and update container or context views only when those levels actually change.
- A feature with a new or changed operational flow should add or amend the relevant Runtime View scenario.
- A feature with a non-obvious durable decision should add an ADR.
- Crosscutting Concepts and Quality Requirements should be touched only when the feature introduces a new pattern or quality target.
- A leaf change that touches none of these architecture surfaces does not need to move the architecture package.

For non-trivial features, writing or updating the relevant Runtime View before coding should be the default design check. For small features, updating the canonical package after implementation is acceptable when the architecture impact is already clear. The method should not force one timing mode for every change.

The detailed normative contract should live in a focused spec:

- `specs/architecture-package-method.md` should own package contents, arc42 section rules, C4 diagram expectations, ADR thresholds, ADR status vocabulary, example requirements, and template requirements.
- `specs/rigorloop-workflow.md` should keep only stage-level routing and handoff rules, such as requiring the architecture stage to produce the focused spec's architecture package before planning continues.

The first positive example should be the architecture-method change itself. That keeps the example real, current, reviewable, and directly tied to the method being introduced. A later completed-initiative example can be added as a reference example, but the first proof should dogfood the method during live authoring.

Templates should live outside live artifact directories. The default template paths should be:

- `templates/architecture.md`
- `templates/adr.md`

`docs/architecture/` and `docs/adr/` should contain real lifecycle-managed artifacts, not disguised templates. If illustrative examples are added later, they should use a clearly non-live path such as `examples/architecture/` or `docs/examples/architecture/`.

The first implementation should remain review-based. It should not add required structural validators, required C4-file checks, ADR-presence enforcement, or package-shape automation until at least one real architecture package has used the new shape. A later non-blocking helper may be acceptable after the shape has proven useful.

The canonical architecture package rule should apply prospectively for new work once this proposal is adopted. Existing approved architecture documents in `docs/architecture/` may still reflect older lifecycle assumptions, and this proposal does not require immediate full migration of all legacy architecture artifacts. Rollout should include a follow-on migration artifact that inventories existing architecture documents and normalizes them as current canonical package content, superseded, archived or historical snapshot, or another explicitly documented historical status. Until that migration is complete, the repository should not claim that all existing architecture artifacts have already been normalized into one canonical package.

## Expected behavior changes

- Architecture work becomes more consistent across changes.
- Reviewers can understand system structure quickly from the default diagrams.
- Contributors and agents have a lightweight but complete architecture template.
- Important architecture decisions become durable instead of being buried in prose.
- New features update the canonical architecture baseline through touched sections and views instead of creating competing current architecture documents.
- Feature-specific architecture deltas are used only when architecture-significant work needs reviewable design reasoning before baseline merge-back.
- Architecture changes are reviewed in the same PR as the code or workflow change that requires them.
- Diagrams become diffable source artifacts rather than opaque files in external tools.
- Architecture review can distinguish missing structure, missing runtime reasoning, missing deployment reasoning, and missing decision records.
- Architecture artifacts become easier to compare because they use a shared section order and shared diagram expectations.

## Architecture impact

This proposal changes architecture authoring and review expectations. It does not introduce a runtime service, data store, dependency, generated-output contract, or release packaging change by itself.

Likely follow-on surfaces if the proposal is accepted:

- `specs/architecture-package-method.md` for the detailed normative architecture package contract;
- `specs/rigorloop-workflow.md` for a short routing/output rule that points to the focused spec;
- `CONSTITUTION.md` for the canonical authored source boundary update that adds `templates/`;
- `AGENTS.md` for concise repository-default guidance that names `templates/` as authored content;
- `docs/workflows.md` for contributor-facing summary guidance and the focused-spec pointer;
- `skills/architecture/SKILL.md` for architecture authoring defaults;
- `skills/architecture-review/SKILL.md` for review checks against C4, arc42, and ADR completeness;
- `templates/architecture.md` and `templates/adr.md` for scaffolding;
- one canonical system architecture package under `docs/architecture/`;
- diagram-as-code files for C4 views under the canonical architecture package location;
- change-local architecture deltas under `docs/changes/<change-id>/architecture.md` when architecture-significant work needs working design reasoning;
- optional supporting delta diagrams under `docs/changes/<change-id>/diagrams/`;
- a feature-specific architecture delta for the architecture-method change itself when needed, with accepted content merged back into the canonical package;
- a legacy architecture lifecycle normalization plan for existing `docs/architecture/` artifacts;
- durable ADRs under `docs/adr/` when a durable decision is recorded;
- generated `.codex/skills/` output only through the normal skill generation path after canonical `skills/` changes.

The source-of-truth boundary should change narrowly: `templates/` becomes a canonical authored workflow-content location for architecture and ADR scaffolding. Canonical skill guidance remains under `skills/`, generated Codex compatibility output remains derived, and lifecycle-managed architecture artifacts remain under `docs/architecture/` and `docs/adr/`. Because this changes the canonical authored source boundary, follow-on implementation should update `CONSTITUTION.md` and `AGENTS.md` in addition to the focused spec and workflow summary.

## Testing and verification strategy

The first implementation slice can rely on artifact review and existing repository validation while the architecture package shape stabilizes.

Expected proof surfaces for follow-on implementation:

- proposal review validates direction, scope, tradeoffs, and non-goals;
- spec review validates the focused architecture package contract and the short workflow-spec routing pointer;
- architecture-review validates the canonical architecture package, any architecture-significant feature delta, and merge-back expectations against the new C4, arc42, and ADR rules;
- review validates that C4 diagrams are stored as diffable source text and updated in the same PR when a feature changes architecture;
- review validates that change-local deltas are treated as temporary working artifacts and that accepted durable content has a merge-back path into the canonical package;
- skill validation checks canonical skill shape after `skills/architecture/SKILL.md` and `skills/architecture-review/SKILL.md` change;
- generated skill drift checks confirm `.codex/skills/` is refreshed only through the normal generator;
- artifact lifecycle validation checks proposal, spec, architecture, ADR, and test-spec statuses when those artifacts are introduced or touched.

The first implementation should use review-based validation rather than new enforcement automation. Later automation may add a validator or checklist coverage for required section names, C4 diagram presence, and ADR links, but only after at least one real architecture package has used the shape.

## Rollout and rollback

Rollout should be incremental:

- settle this proposal through `proposal-review`;
- write `specs/architecture-package-method.md` for the architecture package contract;
- update `specs/rigorloop-workflow.md` only with a short routing/output pointer to the focused spec;
- update `CONSTITUTION.md` to include `templates/` in canonical authored workflow content;
- update `AGENTS.md` to identify `templates/` as authored content and preserve generated-output boundaries;
- add an arc42 architecture template under `templates/architecture.md`;
- add default C4 diagram guidance;
- add an ADR template under `templates/adr.md` and lifecycle guidance;
- define the canonical system architecture package path and baseline package contents;
- define change-local architecture delta paths and merge-back expectations;
- define the allowed diagram-as-code format or formats for C4 views;
- dogfood the method by producing the architecture-method change's own architecture delta when needed and merging the accepted result into the canonical package;
- create a follow-up migration artifact for legacy `docs/architecture/` lifecycle normalization;
- update `skills/architecture/SKILL.md`;
- update `skills/architecture-review/SKILL.md`;
- update workflow summaries and examples;
- keep the first implementation review-based, without required new structural validation automation;
- regenerate derived skill output only after canonical skill changes.

Rollback is straightforward for guidance and template changes: revert the proposal follow-on artifacts, skill edits, templates, generated skill refresh, and canonical-package baseline additions. Because this change does not create runtime state, rollback should not require data migration.

If a later validator is added and proves too strict, rollback can remove or relax that validator while preserving the human-readable guidance.

## Risks and mitigations

- Risk: architecture docs become too heavy.
  Mitigation: use all 12 official arc42 section headings, but allow concise content and explicit "Not applicable" rationale for irrelevant concerns.

- Risk: contributors create too many diagrams.
  Mitigation: require only system context and container diagrams by default, with component and deployment views conditional.

- Risk: decisions are still omitted.
  Mitigation: give ADR trigger examples and make architecture-review check for missing durable decisions.

- Risk: architecture review becomes subjective.
  Mitigation: review against explicit structure, diagram sufficiency, runtime/deployment conditions, cross-cutting concerns, and ADR completeness.

- Risk: arc42, C4, and ADR guidance diverges across templates, examples, and skills.
  Mitigation: keep canonical guidance in `skills/` and workflow/spec artifacts, and refresh generated skill output through existing checks.

- Risk: the new default conflicts with existing architecture artifacts.
  Mitigation: establish one canonical current architecture package for future work while treating older per-change architecture documents as historical snapshots unless a later plan explicitly scopes migration.

- Risk: the repository claims all legacy architecture artifacts are already normalized before migration happens.
  Mitigation: apply the canonical package model prospectively and create a follow-up migration artifact to inventory and normalize existing `docs/architecture/` artifacts.

- Risk: the workflow spec becomes a second full normative home for architecture package details.
  Mitigation: keep detailed package rules in `specs/architecture-package-method.md` and add only a short routing/output pointer to `specs/rigorloop-workflow.md`.

- Risk: templates under live artifact directories confuse validators and reviewers.
  Mitigation: keep templates under `templates/` and reserve `docs/architecture/` and `docs/adr/` for real lifecycle-managed artifacts.

- Risk: adding `templates/` silently changes the canonical authored source boundary.
  Mitigation: treat `templates/` as an explicit source-boundary update and include `CONSTITUTION.md` and `AGENTS.md` updates in the first implementation.

- Risk: feature-specific architecture notes become competing sources of truth.
  Mitigation: require accepted feature deltas to merge back into the canonical architecture package and keep durable decisions in ADRs.

- Risk: contributors over-update stable arc42 sections for ordinary features.
  Mitigation: define living, occasional, and rare update tiers so feature work changes only the affected sections and views.

- Risk: architecture diagrams move into opaque external tools and stop being reviewed.
  Mitigation: keep C4 diagrams as source text in the repository and review architecture diffs in the same PR as the related change.

## Open questions

No open questions block `proposal-review`.

The proposal now carries these next-stage decisions:

- the detailed normative contract belongs in `specs/architecture-package-method.md`;
- `specs/rigorloop-workflow.md` should receive only a short routing/output pointer;
- the first positive example should be the architecture-method change itself;
- templates should live under `templates/`, not under `docs/architecture/` or `docs/adr/`;
- `templates/` is an intentional canonical-source boundary update, not an unchanged-path assumption;
- the repository should maintain one canonical living architecture package and use feature-specific deltas only when architecture-significant work needs reviewable design reasoning;
- feature-specific deltas should live by default at `docs/changes/<change-id>/architecture.md`, with optional diagrams under `docs/changes/<change-id>/diagrams/`;
- accepted architecture deltas should merge back into the canonical architecture package;
- C4 diagrams should be stored as diffable source text and reviewed with the related feature;
- legacy `docs/architecture/` artifacts need a follow-up migration artifact before the repository can claim they are all normalized into one canonical package;
- the first implementation should be review-based, with new enforcement automation deferred until after one real package uses the shape.

## Decision log

- 2026-04-28: Chose C4 as the default diagram language because it gives lightweight structural views without requiring all levels for every change.
- 2026-04-28: Chose arc42 as the written architecture structure because the official 12-section model covers the main architecture concerns while allowing concise or not-applicable content.
- 2026-04-28: Chose ADRs as the durable decision mechanism because important decisions need separate rationale and consequences.
- 2026-04-28: Rejected keeping current architecture skill guidance with ad hoc diagrams and prose because it does not solve drift between architecture artifact shapes or prevent decision loss.
- 2026-04-28: Rejected C4-only because diagrams alone do not cover enough operational and decision reasoning.
- 2026-04-28: Rejected arc42-only because prose structure alone does not give a shared visual model.
- 2026-04-28: Rejected ADR-only because decision records alone do not communicate system structure.
- 2026-04-28: Chose `specs/architecture-package-method.md` as the detailed normative home, with `specs/rigorloop-workflow.md` limited to routing and handoff pointers.
- 2026-04-28: Chose the architecture-method change itself as the first positive example to prove the method on real work.
- 2026-04-28: Chose `templates/architecture.md` and `templates/adr.md` as template paths to keep live architecture and ADR directories limited to real artifacts.
- 2026-04-28: Deferred required architecture-package enforcement automation until after one real package uses the shape.
- 2026-04-28: Chose one canonical living arc42 plus C4 architecture package, with feature-specific architecture deltas only when architecture-significant work needs reviewable design reasoning and accepted deltas merged back into the baseline.
- 2026-04-28: Chose repository-stored diagrams-as-code so architecture diffs can be reviewed with the related code or workflow change.
- 2026-04-28: Chose `docs/changes/<change-id>/architecture.md` as the default change-local architecture delta path and deferred legacy architecture normalization to a follow-up migration artifact.

## Next artifacts

- proposal-review findings for this proposal;
- `specs/architecture-package-method.md`;
- short routing/output update to `specs/rigorloop-workflow.md`;
- `CONSTITUTION.md` canonical-source boundary update for `templates/`;
- `AGENTS.md` repository-default guidance update for `templates/`;
- `templates/architecture.md`;
- `templates/adr.md`;
- canonical system architecture package path and baseline contents;
- change-local architecture delta path and merge-back guidance;
- diagram-as-code format guidance for C4 views;
- architecture-review checklist update;
- architecture-method change architecture delta, if needed, plus merge-back into the canonical package as the first positive example.
- legacy architecture lifecycle normalization plan.

## Follow-on artifacts

- `proposal-review`: approved on 2026-04-28 after the arc42 section model, canonical architecture package, change-local delta lifecycle, template source boundary, and legacy architecture lifecycle clarifications were incorporated.
- [Architecture Package Method spec](../../specs/architecture-package-method.md)

## Readiness

Accepted; may be relied on by the focused architecture package spec.

The recommended direction is specific enough to write the focused architecture package spec, workflow-spec pointer, templates, skill updates, canonical architecture package, and first architecture-significant delta.

Later validation automation is intentionally deferred until the architecture package shape has stabilized through at least one reviewed real example.
