# Refine REM using current KPS guidance

## Topic and decision supported

Recommend how to refine REM knowledge using the current Knowledge Practice System repository.
The decision belongs to the REM maintainer and MOD-008 Engineering Authoring; this is supporting research, not an accepted migration or implementation plan.
The local comparison baseline is RigorLoop commit `ca14a113301fc14e76d0665f90106a96980fcd14`.

## Research questions and stopping condition

1. What does the latest KPS source actually declare, and which changes apply only to its own Core?
2. Which current REM explanations would benefit from that guidance?
3. What bounded pilot can demonstrate editorial improvement while preserving current REM semantics?

Use pinned upstream source and current REM documents as primary evidence.
Stop once version distinctions, adoption boundaries and representative actionable gaps are clear.
This inspection does not establish complete disciplinary coverage or empirical effectiveness.

## Inputs examined

Inspected on 2026-10-18 through GitHub's API and an archive of KPS `main` at [ddb7370cba7b19df02237a7d17b0f853d4ea3485](https://github.com/xiongxianfei/knowledge-practice-system/commit/ddb7370cba7b19df02237a7d17b0f853d4ea3485), committed 2026-10-17.
The web reader could not fetch the repository; the authenticated GitHub API supplied the actual source files.
The API returned no tags and no latest GitHub Release; version claims below refer to source declarations.

Local inputs: [REM overview](../../rem/README.md), [metadata](../../rem/metadata.md), [source map](../../rem/SOURCES.md), the Concept/Principle/Model/Method/Practice indexes, representative requirements and allocation documents, both architecture-decision and change-engineering Practices, the improvement Practice, and the Understand REM navigation and knowledge explanation.
The [owning guidance composition](../../design/architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/rem-guidance.md) supplies current responsibility and preservation constraints.
Sources were inspected directly; no project-map currency is assumed.

## Evidence and source quality

| Evidence | Established finding | Authority and limits |
| --- | --- | --- |
| [KPS publication declaration](https://github.com/xiongxianfei/knowledge-practice-system/blob/ddb7370cba7b19df02237a7d17b0f853d4ea3485/publication.json) | Core version is 11.0.0; language is 9.x; declared checker is 9.2.1; minimum checker is 9.2.0. | Primary source for declarations; checks were not rerun in this research. |
| [Compatibility](https://github.com/xiongxianfei/knowledge-practice-system/blob/ddb7370cba7b19df02237a7d17b0f853d4ea3485/docs/compatibility.md) and [migration](https://github.com/xiongxianfei/knowledge-practice-system/blob/ddb7370cba7b19df02237a7d17b0f853d4ea3485/docs/migration.md) | Core content, language and checker versions are distinct; domains adopt changes separately. Core retired 41 earlier non-Practice objects. | Authoritative for KPS's own migration, not authorization to retire REM knowledge. |
| [Authoring contract](https://github.com/xiongxianfei/knowledge-practice-system/blob/ddb7370cba7b19df02237a7d17b0f853d4ea3485/docs/authoring.md) | Roles allow useful overlap; Models need usable representations; Methods explain operations and adaptations; Practices select approaches from reader needs and conditions. | Current upstream authoring convention, not an externally standardized taxonomy or automatically adopted REM contract. |
| [Core alignment policy](https://github.com/xiongxianfei/knowledge-practice-system/blob/ddb7370cba7b19df02237a7d17b0f853d4ea3485/docs/alignment.md) | Standalone Core knowledge identifies inspected source support; authored Method adaptations distinguish their contribution. Domains retain their declared curation policies. | Relevant model for attribution; its admission rules are Core-specific. |
| [Body-of-knowledge outline guide](https://github.com/xiongxianfei/knowledge-practice-system/blob/ddb7370cba7b19df02237a7d17b0f853d4ea3485/docs/body-of-knowledge-outline-guide.md) | Coverage starts from subject sources and intended capabilities, then maps explanations and gaps; it is distinct from task order. | Optional authoring guidance marked draft; adoption is a local decision. |
| [Reader review](https://github.com/xiongxianfei/knowledge-practice-system/blob/ddb7370cba7b19df02237a7d17b0f853d4ea3485/docs/review.md) | Coverage, local usability and source fidelity require separate judgments; structural success is insufficient. | A review procedure, not evidence of actual REM reader outcomes. |

## Findings

### Established evidence

REM declares edition 1.0.0 based on KPS 9.0.0, without asserting conformance.
It already distinguishes explanatory Principles from selected engineering rules, has nine publication Reference documents and five operating Practices, and labels examples and source limitations.
These are useful foundations to preserve.

The inspected REM documents show specific opportunities:

- [Requirements Concepts](../../rem/concepts/requirements.md) groups IR, SR and AR definitions but provides little contrasting application or local explanation of their derivation.
- [Allocation Model](../../rem/models/architecture-allocation.md) supplies a relationship diagram and cardinalities but no worked allocation showing how behavior, obligations and supporting participation lead to a justified ownership decision.
- [5W2H](../../rem/methods/5w2h.md) clearly documents REM's required use, but has no direct external publication basis for the named technique; its benefit should not be presented as empirically established by this inspection.
- [Architecture decision Practice](../../rem/practices/make-an-architecture-decision.md) has substantive actions and fallbacks, but repeats fixed six-part summaries and offers limited selection guidance among analysis, inspection, prototyping and testing.
- [Understand REM](../../rem/practices/understand-rem/README.md) explains knowledge owners and reading paths; it does not provide a source-derived subject coverage account with required capability and explicit depth gaps.
- [Independent representations can diverge](../../rem/principles/independent-representations-can-diverge.md) correctly labels its logical explanation and limits PROV's contribution to background; that distinction must survive any stronger source-alignment presentation.

### Inference and assumptions

The recommended direction is to improve explanatory depth and practical choice while retaining current engineering contracts.
This is a maintainer recommendation inferred from the comparison, not a KPS mandate.
The assumed intended reader is an engineer or coding agent applying REM to bounded software-intensive changes; the owner should refine that audience before adopting a coverage outline.

KPS's Core-specific retirement does not imply that REM must move its requirement model, allocation rules or reusable authored methods into Practices.
REM's current owners explicitly retain those responsibilities.
A domain policy can distinguish published knowledge, REM-authored adaptations and selected normative commitments within the existing owners.
Strict adoption of Core's narrower admission policy would require a separate ownership and compatibility decision.

## Confidence

High confidence in the pinned version declarations, adoption boundaries and inspected document characteristics.
Moderate confidence in prioritizing the pilot below: this is editorial diagnosis without independent reader trials.
The proposed subject coverage is provisional until suitable engineering accounts and intended reader capabilities are investigated directly.

## Decision implications

### 1. Establish one subject coverage outline

Propose `rem/docs/body-of-knowledge-outline.md` as shared navigation, while preserving the five knowledge-role folders.
Start from intended engineering capabilities and inspected disciplinary accounts, then map current files.
Candidate areas are stakeholder needs and context; requirements and scenarios; logical behavior; architecture and interfaces; realization and integration; verification and intended-use validation; evolution and provenance; and operational support and improvement.
These areas are an authored starting hypothesis, not a claimed standard or complete syllabus.

For each topic, state what the reader must understand, a bounded task they should be able to perform, existing explanations and the specific remaining gap.
For example, requirement derivation should enable a reader to reconcile a request, distinguish a need from a solution suggestion, reuse or refine an obligation, and identify acceptance criteria without inventing missing thresholds.
Keep roadmap and activity sequence outside the outline.
Reconcile overlapping navigation with Understand REM while retaining its useful explanatory content.
If adopting the complete upstream outline guide, include its one overall illustration after the written subject structure settles; further illustrations remain optional.

### 2. Deepen Models where readers must infer the reasoning

Prioritize Requirements, System Design and Allocation.
Add purpose, locally sufficient terms, relevant attributes, relationship meanings, a connected worked case, and assumptions or conclusions the model cannot support.
Use a short introduction and linked Contents where helpful; let the subject determine the remaining sections.
For allocation, show why one Module owns a Function, how another supports it, where AR accountability sits, and when the boundaries must be reconsidered.
Keep existing cardinalities and authority unchanged.

### 3. Explain Method basis, adaptation and interpretation

For each selected Method, distinguish an established operation, an REM adaptation or synthesis, and a proposed operation whose usefulness needs investigation.
Locate procedural support rather than attaching a thematically relevant citation.
Explain inputs, decisions, output interpretation, failure cases and relevant alternatives to the depth needed for competent use.
For 5W2H, distinguish the technique's source basis from REM's selected requirement to address all seven questions at each level.
For architecture assessment, distinguish locally selected scenario comparisons from claiming execution of complete ATAM.
Keep a standalone Method when its operation has independent explanatory value; multiple existing callers are not required.

### 4. Refine Practices around decisions and outcomes

Replace repetitive summary cards where connected actions and explanations communicate more clearly.
Preserve useful stage identity and update links deliberately if adopting upstream stage syntax.
At a consequential choice, explain why an approach fits, the alternatives that matter, the trade-off and what observation would change the choice.
In architecture decisions, distinguish a missing documented guarantee, a runtime-performance uncertainty and a boundary-responsibility ambiguity; these may call for source inspection, a representative prototype or a scenario walkthrough respectively.
These are illustrative options, not a closed catalogue or a claim of superiority.
Keep essential instructions local even if a corresponding reusable Method exists.
Additional approaches may supplement the current Method inventory while binding REM and project requirements remain applicable.

### 5. Preserve source distinctions and useful overlap

Extend the current publication references with claim-level source relationships only where this improves inspection.
Preserve publication identity, exact passages, inspected extent, authored adaptation and nonclaims.
Reassess Principle support individually; a logical explanatory argument, an empirical finding and a policy decision need different justification.
Do not convert provenance background into proof of a Principle or automatic source equivalence.
Allow a Model or Practice to restate the essential meaning of a Concept locally while keeping one canonical definition.
Split grouped documents only when independent use and readability justify it.

### 6. Make adoption and review claims precise

If adopted, distinguish REM's edition, the KPS Core revision consulted, the selected language/profile and any checker actually executed.
Do not mechanically change `based_on.version` to 11.0.0 or copy upstream `validated_with` into REM.
Decide explicitly whether to adopt a full authoring contract or selected editorial guidance; the latter must not claim full checker compatibility.
Preserve the existing canonical metadata owner and reconcile generated skill consumers for any changed canonical guidance.

Assess coverage against the target and relevant sources, usability through a link-hidden task, and fidelity against inspected passages separately.
Use a new ambiguous case in addition to the authored example.
Structural checks support links, identities and projections; actual reader outcomes require actual observations.
Keep review judgments in RigorLoop's operational records under its governing rules, rather than importing KPS's PR-based recording practice.

## Remaining uncertainty

No fresh inspection of NASA, ISO, ATAM or other engineering publications was performed here; existing REM source notes retain their stated inspection limits.
No KPS validator, full REM compatibility assessment, independent reader study or effectiveness experiment was performed.
The current upstream source includes clarifications after its declared 2026-10-12 Core release date, so the pinned commit is needed in addition to version 11.0.0.
The exact REM version increment and adopted authoring profile depend on the accepted scope.

## Recommended handoff

Begin with one bounded pilot: reconcile a raw requirement and derive assessable system obligations.
Develop the coverage slice, relevant Concepts, Requirements Model, 5W2H/Requirement Analysis and the corresponding Engineer a change stages together.
Reuse the current worked example where useful and add an ambiguous request that tests a gap rather than merely replaying the example.
Check whether a reader can distinguish RR from IR, justify reuse versus creation, derive an SR and acceptance criteria, expose unresolved assumptions and choose the next action without opening every link.
Then extend demonstrated editorial improvements to architecture and assurance.

Return this recommendation to requirement-analysis and the REM owner for scope adoption, followed by the applicable design and delivery reviews before implementation.
This research changes no REM contract, version declaration, lifecycle state or publication status and supplies no approval for the proposed refinement.
