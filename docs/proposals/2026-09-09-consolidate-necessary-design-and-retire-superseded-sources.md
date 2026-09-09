# Consolidate Necessary Design and Retire Superseded Sources

## Challenge

RigorLoop's engineering knowledge is spread across living model Designs, legacy specifications, architecture sections, ADRs and archive copies. Some still contain necessary requirements or rationale; others duplicate content already represented elsewhere. Readers must determine which source governs before changing the system, and maintaining the same responsibility across several documents creates avoidable reconciliation work.

The objective is to replace fragmented design sources with modular, sustainably evolving Design—not to preserve every old document, create a model for every source family, or redesign the validation system. Moving all historical prose into larger model files or automatic archive copies would reproduce the burden in another location. Deleting sources without resolving their current meaning and consumers could lose necessary knowledge or break supported behavior.

The two preceding drafts—[incremental model contract consolidation](2026-09-09-incremental-model-contract-consolidation.md) and [necessary Design with proportionate validation](2026-09-09-simplify-required-validation-and-design-retention.md)—identify validation-related sources as a bounded starting point and report completed common Skill adoption with a remaining System ownership correction. This initiative uses that reported adoption basis for the scoped correction; it does not repeat the proposal-family pilot or imply that specialist Skill remainders have also migrated.

## Goals

Give the necessary engineering content in the selected source group one precise current owner, organized by coherent responsibility. Preserve required behavior, applicability, significant constraints, useful decision rationale, failure knowledge and representative expected outcomes needed to understand and evolve that responsibility.

Remove superseded sources and redundant archive copies when their necessary content has transferred and no remaining use requires the original. Retain narrowly necessary supporting material, not historical documents by default.

Reconcile affected consumers and System navigation, validate the actual change proportionately, and complete this bounded cleanup independently of later model transfers or skill adoption.

## Scope and non-goals

Start with the validation-related legacy design sources identified by System and the existing FU-012 follow-up, including applicable portions of `specs/published-skill-first-repository-simplification.md`, retained validation architecture and their amendments. These identify an inspection boundary, not a list of approved deletions. Design selects the exact source sections and receiving owners before Delivery allocates edits.

**Design must use existing model owners first. Create a new model only when the necessary content cannot be coherently owned by existing models. A standalone Validation model is not a required deliverable.** Neither document category nor the number of old files determines the receiving model count.

| Area | Treatment and boundary |
| --- | --- |
| Necessary design and source cleanup | Core scope: reconcile the selected requirements and rationale; remove superseded specification, architecture/ADR content and redundant copies where justified. |
| System and direct consumers | Include the completed common Skill ownership correction, relevant current navigation, and actual readers affected by the selected transfer. Preserve specialist remainders. |
| Retention requirements | Amend exact current rules that would otherwise require unnecessary copies of selected sources. Do not retroactively rewrite historical decisions. |
| Validation requirements | Permit bounded reconsideration of mandatory checks, repetition and source-specific assertions where needed for this cleanup, through the responsible owner. |
| Other consolidation and capability adoption | Keep Distribution, Installation, Release, specialist remainders and remaining skill improvements with their existing follow-up owners and separate decisions. |

Excluded are a repository-wide rewrite or archive purge, a fixed final model inventory, broad validation-policy redesign, a new runner/cache/scheduler, migration registry, permanent per-test ledger, automatic whole-directory deletion, unrelated supported-behavior retirement, changes to specialist judgment authority, publication and real customer installation. Operational records, resources, schemas, templates and recovery information are not obsolete design prose.

## Governing principle

> Preserve necessary engineering meaning in its coherent model owner, remove superseded sources when their remaining uses are resolved, and validate the affected change rather than repeat historical ceremony.

## Proposed direction

### Select owners and reconcile meaning

For each selected source group, identify the actual current requirements, their applicability, important decisions, exceptions, later amendments and failure knowledge. Include substantive unnumbered prose; a list of requirement IDs or file moves alone cannot establish preservation.

Assign surviving content to the smallest justified set of existing model owners. One source may contribute to several owners, and several sources may contribute to one model. Do not force unrelated content into an existing owner merely to avoid a justified new model. A new model needs a coherent responsibility that the existing owners cannot accommodate—not a historical folder name or a preferred document count.

Keep System focused on composition and references to local owners. Skill, Test, Review and Closeout, Workflow, Record Format and CLI retain their respective responsibilities unless an exact scoped amendment is independently approved. The cleanup does not make one model the owner of every concern found in a legacy validation specification.

Transfer necessary meaning precisely enough that current work does not require reconstructing rules from an archive or Git history. Preserve material technical realization and rationale, not only an attractive summary of the chosen architecture. Do not import completed rollout conditions, superseded procedures, every rejected alternative or repeated narrative merely because they appeared in an approved source.

An apparently obsolete requirement needs an explicit disposition; stylistic cleanup is not authority to change supported behavior. Use the existing Design displacement mapping for destinations, justified retention and approved retirement, with concise grouped rationale rather than a second permanent contract catalogue.

### Remove superseded sources without automatic archiving

As part of the reviewed, coherent adoption of the selected replacement and its consumers, remove superseded originals and redundant copies that have no necessary remaining use. Their necessary meaning and dependencies must be resolved before removal. Do not automatically create an archive snapshot, redirect, index or original-path duplicate for each removal.

Retain supporting material only for an explicit need not adequately met by the current Design or other available evidence: an unmigrated obligation, essential regression context, a real operational reader, or exact evidence still needed for current reliance. A historical citation or prior approval alone does not require permanent checked-in retention. Mixed files retain their necessary remainder rather than being deleted wholesale.

Keep current findings, necessary decisions and relied-on evidence understandable and truthful. Do not retarget old approvals to new Design content. When an original subject is removed, preserve any basis still needed for current reliance or explicitly stop relying on that assessment; do not erase open concerns or rewrite historical outcomes.

Amend conflicting retention requirements through their current owners before adopting the deletion policy. Resources consumed by loaders, generators, validators or recovery mechanisms remain operational dependencies until separately reconciled. Their location beside an obsolete specification is not a reason to delete or move them.

### Reconcile actual consumers

Identify affected current references and actual readers, distinguishing normative dependence, operational consumption and incidental historical citation. Update only the necessary skills, scripts, validators, templates, navigation or generated-candidate consumers. No required dependency may be dismissed as historical simply because its source document is being retired.

System should identify the actual current owners and distinguish completed common Skill adoption from retained specialist obligations. Use the recorded completion basis without rerunning the previous pilot. Do not move unrelated plan-asset or boundary-method policy into Skill just to remove a remaining spec link.

Where source removal changes operational inputs or package identities, reconcile those consumers and their directly dependent metadata under the existing contracts. Source-only work does not automatically authorize or require package, installer or release changes. An inseparable out-of-scope responsibility returns for a bounded scope decision rather than expanding the initiative silently.

### Validate proportionately and reconsider only relevant obligations

For a source-only change, assess whether necessary meaning has a usable current owner and whether affected references and readers still work. Independent review judges semantic preservation; existing mechanical checks establish the relevant structural and consumer facts. Package generation, runtime suites, release checks and historical benchmarks are not required solely because Design prose was consolidated.

If a packaged resource, executable reader, validator, selector or other behavior-bearing dependency changes, include the checks protecting that boundary. Unknown or ambiguous impact requires broader investigation and verification, not a claim of no effect. File extensions alone do not establish impact.

Distinguish keeping a useful check, requiring it for this change, and executing it again. Reuse a recorded pass only when its subjects, dependencies, check implementation/configuration and relevant environment remain applicable under the existing evidence policy. Preserve explicit freshness requirements. Missing, failed or contradicted evidence is not a reusable pass, and runtime write/recovery safeguards continue to execute when those operations run.

Where an existing requirement forces irrelevant or duplicate execution, or an assertion enforces an obsolete source location or wording, select the necessary owner-approved amendment. Do not silently skip a still-required check or demote a failure because it is inconvenient. Retiring a test or exclusive mechanism requires justified retirement of its obligation or adequate retained protection; not running a test for this cleanup does not make it useless.

Use direct terms such as skill checks or package checks where they describe the work. Do not preserve a Gate A/B/C glossary merely for historical continuity; existing command and interface compatibility remains unless explicitly amended. Broad mandatory-check reclassification and new validation machinery remain separate work.

### Complete a bounded replacement

Design identifies the exact source scope, receiving owners, necessary content, approved rule changes, retention/removal decisions and affected interactions. Delivery sequences the authorized edits and focused proof by engineering dependencies. The replacement must be usable and the affected consumers reconciled before superseded authority is relied upon as retired.

Completion evidence should show where necessary content now lives, which redundant sources were removed, what remains and why, and which checks and independent assessments support the result. Use existing change records; do not create a permanent migration ledger duplicating the Designs.

The selected source group must be understandable from its current Designs, justified cleanup must be completed, and actual consumers must remain coherent. No new model count, deletion quota, full-directory disappearance or numerical token/runtime improvement is required. An unresolved removal needs an explicit retained owner and reason rather than a false completion claim.

Existing independent milestone assessments, fresh final whole-change Code Review and distinct Verify remain required. Other consolidation and skill-adoption work stays with its existing follow-up ownership; this change does not close it or require it to finish first.

## Feasibility

**Assessment: feasible as bounded design consolidation, source cleanup and directly necessary consumer or policy amendments.**

The supplied drafts identify living-model conventions, a System inventory, existing assessment and test responsibilities, and a candidate validation-related source family. These support the direction without requiring a new model, archive facility or validation platform in advance.

They do not establish the exact current dependency graph or individual files and tests safe to remove. Design must inspect the selected sources, resolve necessary meaning and applicability, and identify any retention or validation amendments. Existing owners remain available dependencies while this scoped decision is prepared.

The minimum Design package is the affected receiving models, any justified new model, scoped System corrections and exact governing amendments required by the cleanup. No completed cleanup, measured saving or verified prior adoption is asserted by this draft itself.

## Impact and major trade-offs

Removing superseded sources can reduce repeated reading and competing authority, but can also make historical detail less convenient to inspect. Necessary rationale belongs in current Design, while originals with a specific remaining use stay available. Copying entire historical documents into a model would defeat the objective.

Focused validation avoids unrelated repetition but depends on an adequate consumer-impact assessment. Explicit uncertainty handling, retained runtime safeguards and independently assessed evidence limit that risk without making every historical check mandatory again.

The change permits necessary scoped retention and validation-policy amendments; it is not blanket behavior-preserving file relocation. Other supported behavior and specialist authority remain unchanged unless separately and explicitly selected by their owners.

## Decision requested

Approve one bounded initiative to consolidate necessary engineering meaning from the selected validation-related legacy sources into coherent living model Designs, reconcile current consumers, and remove superseded sources and redundant copies whose remaining uses have been resolved.

Let Design choose the receiving owners, using existing models first and creating a new model only when the necessary content cannot be coherently owned by them. Do not require a standalone Validation model, automatic archive, broad validation redesign or completion of every remaining model transfer.

Permit exact retention and validation amendments needed for the selected cleanup, with focused checks, justified evidence reuse and preserved independent assessment. Keep System's common Skill ownership correction in scope and other consolidation and capability adoption separately owned.

Approval selects this merged direction for Design. Exact requirements, source or test removals, consumer changes and proof allocation require their applicable Design, Delivery and independent assessments. This draft neither authorizes implementation or publication nor closes the preceding proposals or retargets their recorded judgments.
