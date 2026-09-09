# Establish the Skill Model with a Bounded Proposal-Family Pilot

Owning change: [2026-09-08-skill-model-proposal-family-pilot](../changes/2026-09-08-skill-model-proposal-family-pilot/change.json).

## Challenge

RigorLoop's shared skill contract is distributed across the Skill Contract, readability and portability specifications, resource-integrity decisions, and sections of the mixed system architecture. The current System model still identifies public skill structure and resource integrity as an unmigrated responsibility. These sources combine enduring requirements, completed pilot conditions, and references to policy now owned elsewhere.[S1][S2]

A new Design file alone would not demonstrate that the shared contract improves real skills. Conversely, rewriting every published skill while extracting the model would turn a bounded consolidation into another broad refactor.

This initiative must establish one coherent Skill-model owner, improve a small named pilot against it, and retire the corresponding duplicate current authorities. It must preserve useful history and existing non-pilot behavior without claiming that all skills have adopted the new improvements.

## Goals

Establish one living Skill Design for common skill structure, invocation descriptions, readable operating instructions, conditional resources, output assets, portability, and truthful claim boundaries. Keep specialist methods and assessment policy with their existing owners.

Demonstrate the model through a bounded pilot of **`proposal` and `proposal-review`**. Improve their usability and maintainability where the current baseline supports a specific correction, while preserving proposal scope, review independence, governed recording, and isolated-invocation behavior.

Reconcile and retire superseded common Skill specifications and architecture sections. Keep originals that remain useful directly readable in the checked-in archive. Assign remaining skill adoption to named later work.

Success means clearer ownership and demonstrated pilot improvement—not a required reduction in file count, skill length, or tokens.

## Scope and non-goals

### Selected pilot and scope budget

The pilot is exactly `proposal` and `proposal-review`. They provide complementary authoring and independent-assessment paths, with artifact assets and conditional guidance already established in the source material.[S3] This selection is not a finding that both skills are defective, nor permission to repeat their completed simplification or asset-extraction work.

The pilot includes their canonical `SKILL.md` files and the exact references, assets, and shared-source dependencies selected by Design and allocated by Delivery. Their public invocation names remain unchanged. No third skill becomes a pilot implicitly through a shared-resource edit.

| Work and initial intent | Initial goal treatment | Scope budget treatment | Boundary and destination |
| --- | --- | --- | --- |
| Shared Skill model | in scope | core to this proposal | Create `docs/design/skill/skill.md` using the established model convention; update System's owner reference and necessary consumers. |
| Common source consolidation | in scope | core to this proposal | Reconcile common obligations from Skill Contract, readability, applicable portability/resource-integrity sources, and corresponding architecture sections and decisions. Design identifies exact clauses. |
| Two-skill pilot improvement | in scope | core to this proposal | Assess and improve the named pair; preserve specialist responsibilities and previously adopted improvements. |
| Necessary integration | in scope | same-slice dependency | Update directly affected validators, resource projections, navigation, and generated candidates under existing tooling contracts. Other skills receive only necessary compatibility or ownership-reference corrections. |
| Source retirement and readable history | in scope | core to this proposal | Retire mapped current authority after adoption, archive useful originals, and preserve historical references and identities. |
| Remaining skill adoption | deferred follow-up | deferable follow-up | Repository maintainer receives the remaining skills or bounded families through existing follow-up records; Design identifies differences and the next adoption decision before this initiative closes. |
| Other model consolidation | out of scope | separate proposal | Distribution, Installation, Validation Execution, Release, and CLI Observability remain separate initiatives with their existing owners. |
| Expanded pilot or operational activation | out of scope | out of scope | No inventory-wide improvement, publication, real customer installation, or implicit additional pilot. |

This change does not repeat the unified `design` skill replacement, redesign proposal content or review judgments, add a lifecycle gate or standalone test-spec, create a public `skill` command, introduce a record schema or adoption service, authorize blanket test deletion, or remove whole directories.

## Governing principle

> Define the shared skill contract once, demonstrate improvements through a bounded pilot, and expand adoption only through explicit, evidence-backed changes.

## Proposed direction

### 1. Give the Skill model a precise responsibility

The Skill model should define how a published capability presents its purpose, invocation conditions, inputs, procedure, outputs, resource dependencies, and limits. It should make common instructions compact without removing information necessary for correct use.

Its Design should explain the relationship between `SKILL.md`, conditional references, reusable assets, and declared scripts. Resources must be complete for the paths that require them, selectively loaded, and governed by existing integrity and transformation contracts. Preserve the distinction between safe invocation fallback and a valid package.[S4]

Skill does not become a universal manual of specialist decisions. Workflow owns coordination; Review and Closeout owns assessment authority and consequences; Test owns test-quality criteria; Design owns model authoring; Record Format and CLI own representation and recording mechanics. Skill explains how a capability exposes and applies those obligations without duplicating their definitions.[S1]

Common published structure must not standardize all skills into the same reasoning procedure. Authoring and review skills retain different inputs, methods, outputs, and authority.

### 2. Separate contract consolidation from adoption of improvements

Design must distinguish preserved common obligations, new or revised pilot requirements, and obligations owned elsewhere. Consolidating an unchanged common requirement transfers its authority; it does not establish that every consumer has been audited. New or tightened requirements initially apply only to the selected pilot. Non-pilot skills retain their currently applicable contract until their own adoption is authorized. Applicability must be explicit, without universal requirements followed by silent exemptions.

Retire old normative prose only after its surviving responsibility has a complete destination. Where non-pilot behavior depends on an unmigrated clause, retain an explicit owner and boundary. A mapped obligation must not have two independently maintained current definitions.

Validators and shared resources must respect the same boundary rather than enforce pilot-only requirements inventory-wide. A shared-source edit that necessarily affects another consumer requires bounded compatibility correction and evidence. An uncontainable behavior change returns to Design or replanning rather than expanding the pilot without a decision.

Use existing reviewed allocations and resource-selection mechanisms. No new compatibility framework, second universal skill manual, or serialized adoption registry is selected.

### 3. Improve the pilot from an inspected baseline

Inspect the then-current pilot subjects and applicable contracts before selecting edits. Earlier approved simplifications, resource extractions, and recording changes are baseline behavior, not new deliverables.

| Assessment area | Intended improvement where a gap is established |
| --- | --- |
| Invocation clarity | Readers can distinguish proposal authoring from assessment and later-stage work. |
| Procedure and resource loading | Common work avoids unrelated guidance; exceptional paths receive their complete required procedure. |
| Output usability | Assets support complete usable artifacts without contradicting the skill or embedding another owner's judgment policy. |
| Handoff and claim limits | Each skill explains what it produced, what it did not establish, and which responsibilities remain independent. |

These are assessment dimensions, not pre-established defects. Design selects concrete before/after outcomes supported by the inspected baseline and retains compliant content. Required-rule coverage, output quality, and readability take priority over token reduction.[S5] Moving text into references is not an improvement if ordinary users need more reading to recover the same necessary information.

The pilot must show justified improvement in the selected scope; an audit or shorter text alone is insufficient. An unfavorable or inconclusive result must be reported and dispositioned before recommending broader adoption, without silently adding skills to this initiative.

### 4. Retire corresponding sources without losing current meaning

Design must map selected numbered and unnumbered obligations, material decisions, and representative acceptance intent to Skill, another existing owner, explicit supersession, or justified retention. Use substantive replacement mappings rather than filename-only consolidation.[S6]

Common portions of Skill Contract, readability, portability, resource integrity, and relevant architecture are extraction candidates. Proposal-specific direction criteria, exact artifact sections, and review judgments remain with their specialist owners. Specialist documents may be removed only when their actual responsibilities are fully dispositioned, not because their names match the pilot.

After reviewed adoption, current navigation points to the new owner. Fully superseded useful originals move to the checked-in archive under the project-selected retention policy; mixed files retain clearly bounded unmigrated authority. Do not delete the whole system architecture, `specs/`, or `docs/adr/`.

Preserve original bytes where historical identity matters. Put replacement/provenance information in archive navigation rather than rewriting old judgments. Archives remain directly readable, including necessary related links and diagrams. Source-path retention may accommodate a retained dependency but must not create duplicate current authority.

Resource manifests, canonical references, and templates still used by tooling are operational inputs. Relocate them only with their actual consumers and identity-sensitive projections, or retain their current location. Directory cleanup is not a reason to break them.

### 5. Demonstrate both pilot value and safe coexistence

The Skill Design should define representative outcomes from which Delivery allocates concrete proof, preserving these distinctions without an exhaustive case catalogue:

| Situation | Required demonstration |
| --- | --- |
| Ordinary proposal authoring versus independent assessment | Each pilot supplies a usable procedure and artifact while preserving its own scope and authority. |
| Required, missing, or untriggered conditional resource | Required methods are available; missing required content is not invented; unrelated resources are not prerequisites. |
| Canonical content reaches a supported candidate package | Declared resources, transformations, and identities remain consistent under applicable distribution checks. |
| Pilot-only rules coexist with unchanged skills | Non-pilot behavior and required validation remain supported, without inventory-wide conformance claims. |
| An old source is retired or archived | Its current obligations have one accessible owner and useful history remains readable without governing new work. |

Mechanical checks establish structure, references, resource integrity, and supported package behavior. Independent assessment judges instruction coherence, useful pilot improvement, and preservation of source meaning. Keyword checks do not replace those judgments; examples do not establish universal agent correctness.

Use currently applicable validation and assessment contracts. Skill Contract's selected proof policy makes earlier pilot-specific prompt, transcript, and clean-install requirements historical; consolidation must not reactivate them by copying old clauses.[S2] This proposal adds no universal target-agent benchmark, numeric savings gate, or requirement to relaunch historical experiments. Additional proof policy requires explicit selection by its owner.

### 6. Finish the pilot and assign the remainder

Completion requires the reviewed Skill model and exact ownership transfer, implemented pilot improvements, coherent necessary consumers, demonstrated representative outcomes, approved source dispositions, and concrete follow-up ownership for remaining adoption.

Use existing work and follow-up records. After inspection, name remaining skills or bounded families, their receiving owner, applicable differences, and next adoption decision. The repository maintainer receives this remaining adoption work for assignment to the appropriate capability owners. Do not copy mutable progress into Skill Design or leave the remainder only in chat.

Preserve independent milestone assessments, fresh final whole-change Code Review, and distinct Verify. A package pass, model-validation pass, or completed pilot neither authorizes publication nor establishes that all skills satisfy the improved contract.

## Feasibility

**Assessment: feasible as a shared-contract extraction, two-skill pilot, and bounded consumer reconciliation.**

The source material already defines common skill structure, readability, resource maps, artifact assets, generated-source integrity, and separate specialist authority. Previous proposal-family work supplies an established baseline rather than requiring a new capability.[S2][S3][S4][S5]

Design must reconcile applicable clauses and supersessions, select concrete pilot improvements, define non-pilot applicability, and identify exact source and consumer dispositions. This proposal does not establish the repository-wide dependency graph or an executed pilot assessment. No individual source is yet declared safe to delete, and no token or runtime benefit has been measured.

The minimum Design package is the new Skill model, the scoped System ownership update, and exact existing contract amendments needed for pilot applicability or source retirement. Other model extractions and new packaging or installation mechanisms are not prerequisites. No direction-level blocker has been identified; unresolved ownership contradictions, inability to contain shared-resource effects, or failure to identify a justified pilot improvement must be dispositioned before dependent adoption or closeout.

### Source basis and evidence limits

The submitted direction cited supplied snapshots (`design(5).zip`, `specs(1).tar`, `skills(2).zip`, and `adr.tar`). Those snapshot bytes were not independently compared here. The links below identify repository counterparts inspected for bounded direction evidence, not a current conformance audit. Current governing amendments take precedence over historical rollout clauses. The project map contains historical inventories; this proposal relies on the directly inspected System responsibility inventory and named contracts rather than treating the map as a current dependency audit.

- [S1] [System Model: responsibility inventory](../design/system/system.md#responsibility-inventory), including retained public skill/resource responsibility and selected shared owners.
- [S2] [Skill Contract](../../specs/skill-contract.md), especially adopted ownership boundaries, common structure/resource obligations, and prospective proof disposition.
- [S3] [Proposal-Family Assets Progressive Disclosure](../../specs/proposal-family-assets-progressive-disclosure.md); canonical pilot subjects for subsequent baseline assessment are [proposal](../../skills/proposal/SKILL.md) and [proposal-review](../../skills/proposal-review/SKILL.md). Earlier source descriptions are not evidence of a present defect or a new deliverable.
- [S4] [Published Skill Resource Integrity decision](../adr/ADR-20260623-published-skill-resource-integrity.md), read with currently governing proof amendments in Skill Contract.
- [S5] [Skill Readability and Self-Containment Contract](../../specs/skill-readability-contract.md), especially the priority of output quality, clear instructions, then token cost.
- [S6] [Design Model](../design/design/design.md), DES-SR-02/06/13/14/18/19 on coherent ownership, preserved decisions, substantive displacement maps, retained-contract boundaries, and coordinated adoption.

## Impact and major trade-offs

A shared model reduces fragmented authority only when source obligations are reconciled. Copying historical amendments into a larger file preserves the problem. Organize the living model around current responsibilities and important rationale, with useful historical originals archived separately.

A bounded pilot reduces immediate implementation scope but leaves temporary adoption differences. Make them explicit and support them through validation and resource boundaries. Necessary shared-dependency compatibility work does not authorize inventory-wide improvement.

An author/reviewer pair exercises complementary paths but does not demonstrate adequacy for implementation, recovery, or other specialist skills. Later adoption must assess those responsibilities in context. Preserve safety and useful evidence ahead of text or token reduction.

## Decision requested

Approve establishing the shared **Skill model** and improving the bounded **`proposal` / `proposal-review` pilot**, with necessary compatibility, validation, resource, and navigation changes.

Approve reconciling and retiring corresponding common specification and architecture authorities after adoption, while keeping useful historical originals directly readable in a checked-in archive and preserving explicitly unmigrated obligations.

Permit this initiative to finish with the shared model, evidenced pilot improvements, and named later adoption work. Do not require every published skill to adopt the improvements before this slice can close.

Approval selects this direction and pilot boundary. Exact requirements, edits, source deletions or moves, proof allocation, and adoption remain subject to Design, Delivery, and independent assessment. It does not authorize implementation, publication, customer adoption, rewriting historical evidence, changing specialist policy, or adding pilot skills implicitly.
