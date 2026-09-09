# Simplify Required Validation and Retain Only Necessary Design

## Challenge

RigorLoop's remaining validation rules are distributed across legacy specifications, architecture sections, scripts, and later amendments. The preceding [consolidation proposal](2026-09-09-incremental-model-contract-consolidation.md) selected a bounded Validation Execution transfer, but preserved existing validation policy by default and required readable historical originals. That direction is insufficient for the user's latest decision: reconsider which checks are mandatory and retain only design information necessary for the current project.

The [published-skill-first contract](../../specs/published-skill-first-repository-simplification.md) groups canonical-skill, generated-package, and release-candidate checks under Gate A, Gate B, and Gate C. Those names describe existing check groupings; they do not independently justify keeping every check, repeating every execution, or retaining every historical document. A new model that copies all old obligations and terminology would preserve the maintenance problem.

The preceding proposal reports completed common Skill adoption and an outdated prospective owner reference in System. Reconcile that reference against its actual adoption basis without repeating the completed proposal-family pilot. Specialist Skill remainders retain their explicit owners until separately addressed.

## Goals

Establish a clear Validation Design that explains necessary checks, their protected obligations, applicable circumstances, result meaning, and conditions for using existing evidence. Assess mandatory status and execution frequency rather than inheriting them solely from historical clauses.

Use direct language such as skill checks, package checks, and release checks. Keep a technical term only where it removes a real ambiguity. Do not require a glossary or named gate hierarchy merely to preserve old aliases.

Consolidate necessary behavior, constraints, meaningful decisions, and representative acceptance outcomes into their living Design owners. Remove fully superseded design-source documents and redundant archive copies when they have no remaining current use. Keep the work bounded to Validation and its necessary ownership and consumer corrections.

## Scope and non-goals

| Area | Selected treatment |
| --- | --- |
| Validation policy and model | Reassess the selected check families: continued necessity, mandatory applicability, advisory treatment, duplication, evidence reuse, and retirement. Design selects exact requirements and source boundaries. |
| Necessary-design retention | Replace automatic archival preservation for the selected sources with a current-use decision. Include necessary amendments to current retention rules that would otherwise require redundant copies. |
| System ownership | Correct completed common Skill ownership and identify the selected Validation owner without moving specialist remainders merely to remove links. |
| Implementation and consumers | Reconcile affected runners, selectors, validators, tests, skills, resource references, candidate metadata, and current navigation. Remove obsolete exclusive machinery only within the selected responsibility. |
| Other model transfers and skill adoption | Distribution, Installation, Release, unrelated legacy responsibilities, and the remaining skill improvements stay separately owned. Their existing contracts are dependencies, not requirements to consolidate them now. |

This is not a repository-wide validation rewrite or archive purge. It does not introduce a new runner, cache, scheduler, adoption registry, permanent per-test ledger, or historical-document service. It does not authorize publication, real customer installation, or unrelated product-behavior retirement.

Fresh independent final whole-change Code Review and distinct Verify remain unchanged. Current effective state, open findings, material decisions, and evidence still needed for reliance remain available under their existing owners. This proposal concerns validation-policy redesign and design-source retention, not blanket deletion of operational records, schemas, templates, resources, or recovery information.

## Governing principle

> Preserve the necessary engineering obligation, not every historical check or document used to express it. Require a check and a fresh execution when their purpose and evidence basis justify them.

## Proposed direction

### Use plain responsibilities instead of inherited gate terminology

Validation owns selection and execution of checks, their deterministic composition, and truthful reporting of what ran and what the results establish. Component owners define the behavior and artifact invariants being checked. Test supplies protective-value criteria; Review and Closeout owns assessment authority and evidence applicability; Workflow coordinates responsible actors. Release and Installation keep their domain obligations and execution permissions.

Use skill checks, package checks, and release checks in ordinary guidance. Existing command names, result identifiers, and integrations that contain older terminology need an explicit compatibility disposition; changing explanatory language is not an automatic public-interface break. Do not require Gate A/B/C as a new model hierarchy or workflow stage.

The selected Validation change may revise its own mandatory-check and composition policy through reviewed Design. A check tied to another owner's supported guarantee cannot be discarded by silently changing that guarantee; any necessary cross-owner amendment must be explicit and remain bounded. No passing check grants publication or engineering approval by itself.

### Reassess necessity, applicability, and execution separately

For each selected coherent check group, establish the current obligation or failure it protects, what it actually observes, the conditions in which that protection matters, and the consequence of failure. Assess equivalent retained protection and limitations. Use the living Design and existing change evidence; do not create an administrative record for every test function.

Select the appropriate disposition: retain a required check, restrict it to relevant changes or an operation, make genuinely advisory guidance non-blocking, consolidate equivalent checks, or retire a check whose obligation is no longer required. Existing mandatory status is a baseline to examine, not proof that it must survive unchanged. Equally, cost, age, absence of a Design label, or a passing reduced suite do not establish that protection is unnecessary.

A useful test can remain in the repository without running on every change. A required validation result can sometimes be satisfied by an applicable earlier passing result without another execution. Neither conclusion makes that test redundant. Design must distinguish these decisions rather than express all of them as keep or delete.

Where equivalent protection replaces a check, establish the retained detection at the required boundary. Where an obligation is explicitly retired, no substitute check must reproduce the retired behavior; preserve any safe-rejection, compatibility, or shared-safety obligations that survive. Uncertain protection needs investigation before removal, not a fabricated equivalence claim.

### Make mandatory scope and failure consequences explicit

Define checks in terms of their actual inputs and dependencies, not filename extensions alone. A pure documentation change need not automatically require every package or runtime check; a shared resource, package selector, ignore rule, or validation change may have wider effects than its filename suggests.

Unknown or ambiguous impact must select broader verification under the retained policy, rather than imply no impact. The CLI may calculate declared paths, identities, dependencies, and results mechanically; it does not decide whether engineering evidence is sufficient or whether an obligation should be retired.

Distinguish a failure that makes an applicable artifact or operation unacceptable from an advisory improvement. Mandatory versus advisory is a reviewed policy decision, not an implementer's means of turning a failure green. Any blocking result must leave the authorized correction path available; validation must not prevent recording the defect that explains why work cannot yet be relied on.

### Reuse valid evidence without weakening runtime safeguards

Reuse previously passing validation evidence only with an affirmative basis that the final subjects, relevant dependencies, check implementation or configuration, and relevant environment have not invalidated it. Reuse must satisfy any explicitly selected freshness obligation and preserve the original result and its limitations. Failed, missing, incomplete, or contradicted evidence is not a reusable pass.

A cached development test result is not permission to bypass safeguards during a real operation. Identity, containment, authorization, structural, and transaction checks that protect an actual write or recovery attempt still run where the supported operation requires them. The separate final whole-change review remains fresh even when some execution evidence is reused.

The resulting guidance should explain why evidence is sufficient for the selected scope, without making every ordinary invocation read the entire validation catalogue or rerun all historical proof procedures.

### Keep necessary design; do not create archives by default

A living Design must contain the current behavior, significant constraints, shared relationships, meaningful decision rationale, and representative expected outcomes needed to evolve its responsibility. Preserve relevant exceptions and failure knowledge. Do not copy obsolete requirements or every rejected alternative merely to maintain historical volume.

Once selected source content has a complete current disposition and its consumers are reconciled, remove the superseded specification, architecture, or ADR from the current checkout when no necessary use remains. Do not automatically create a snapshot, an archive index, a redirect, or an original-path duplicate. Existing redundant archive copies within the selected scope are eligible for the same assessment; earlier archival treatment does not make them permanent.

Retain an original only for an explicit remaining need that the current Design or another necessary artifact does not satisfy—for example, an unmigrated current obligation, essential regression context, an actual operational reader, or exact evidence still relied upon. Such retention should name the need and owner, not rest on the fact that a historical file exists. Mixed documents retain their necessary remainder until that portion is reconciled.

Ordinary version history may preserve deleted sources, but current engineering work must not depend on reconstructing its rules from that history. Do not rewrite old approvals to pretend they assessed replacement content. A historical citation alone does not automatically require the cited file to remain in the checkout; where current reliance requires the original subject, preserve the needed basis or explicitly stop relying on that historical assessment. Do not claim the new Design proves the old review's original basis.

Operational resource manifests, templates, schemas, fixtures, and recovery files are not unnecessary design prose. Preserve or deliberately relocate them with their real consumers. Amend current retention requirements explicitly where necessary; do not falsify completed plans or historical decisions to make the new policy appear retroactive.

### Deliver one complete, bounded simplification

Start with the Validation responsibility identified by the existing consolidation work. Design names the exact source families, selected checks, retained protections, changed mandatory conditions, source-removal decisions, and necessary consumer interactions. A newly discovered inseparable responsibility returns for a scope decision rather than recruiting all remaining models.

Delivery implements the selected policy and source consolidation together with their required consumer changes. A baseline-to-final comparison must show which checks remain required, which become conditional or advisory, which are consolidated or removed, and how the surviving protection is established. The comparison can be grouped and stored in existing evidence; it is not a new permanent catalogue duplicating the Design.

Completion requires an actionable current Validation contract, implemented and assessed check selection and outcomes, coherent consumers, necessary source cleanup, and explicit remaining ownership. The result must demonstrate simplification of obsolete obligation, redundant execution, or unnecessary documentation within the selected slice—not merely a renamed file. It does not require a deletion quota or promise a measured runtime or token improvement.

## Feasibility

**Assessment: feasible as a bounded policy redesign and consolidation; exact check and deletion decisions require Design and implementation inspection.**

The supplied contracts already identify canonical-skill, package, and release checks, separate deterministic validation from semantic assessment, and permit some reuse and scoped filesystem proof. Existing [Test](../design/test/test.md), [Review and Closeout](../design/review-closeout/review-closeout.md), [Design](../design/design/design.md), and [System](../design/system/system.md) responsibilities provide the adjacent owners.

The new work is not simply preserving that historical arrangement. It must examine which requirements remain necessary, clarify when checks are mandatory, and replace redundant source retention where its purpose has been satisfied. The available materials do not establish current execution cost, complete selection/dependency behavior, safe individual removals, or actual savings.

The minimum Design package is the selected Validation Design, scoped System corrections, and exact amendments to Design or other current owners whose validation or retention rules must change. No new general migration, archival, or validation platform is needed by this direction.

## Impact and major trade-offs

Narrowing mandatory execution can reduce repeated work, but an incomplete impact assessment can hide regressions. Explicit applicability, adequate retained protection, conservative treatment of uncertainty, and truthful evidence reuse must be assessed together.

Removing redundant historical sources improves the maintained documentation set but can reduce convenient access to old reasoning. Necessary rationale belongs in the current owner; narrowly necessary originals remain. Replacing archival duplication with an equally large history section inside every model would not meet the goal.

This revision deliberately changes the preceding proposal's preserve-existing-validation-policy and preserve-readable-originals defaults. Within the selected scope, those arrangements may now be redesigned rather than inherited. Runtime safety, specialist authority, publication permissions, and required independent review are not silently waived by that authorization.

## Decision requested

Approve a bounded initiative to simplify Validation: reconsider which checks are mandatory, when they apply, when existing passing evidence can be reused, and which checks or exclusive mechanisms can be consolidated or retired with an explicit protection or obligation-retirement basis.

Approve retaining only necessary current design and narrowly justified supporting material, without automatic archival duplication. Permit reviewed removal of superseded design sources and redundant archive copies in the selected slice once necessary content, evidence, and consumer dependencies are resolved.

Keep System's completed common Skill ownership correction in scope and leave other model transfers and remaining skill improvements separately owned. Preserve fresh independent whole-change Code Review, distinct Verify, truthful records, supported runtime safety, and separately authorized external actions.

Approval selects this revised direction for Design. It does not itself select individual test or file deletions, waive a currently applicable failed check, establish evidence sufficiency, authorize implementation or publication, or erase historical approvals. Exact policy changes and their adoption follow the normal reviewed Design and Delivery process.
