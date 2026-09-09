# Establish the Release Model and Retire Superseded Design Sources

## Challenge

RigorLoop's standing release responsibility is distributed across the release-process specification, transaction-automation specification, their ADRs and sections of the mixed system architecture. [System](../design/system/system.md#candidate-models-and-legacy-source-ownership) already identifies a potential Release owner for release identity, transaction profiles, publication permissions, composed proof, evidence and recovery. Those sources mix enduring obligations with initial rollout conditions and version-specific history.

Maintainers need a coherent current contract without reconstructing it from several generations of documents. Creating a new model while retaining duplicate current definitions would not resolve that burden. Removing old documents before their necessary meaning and readers are reconciled would risk losing publication safeguards or relied-on evidence.

## Goals

Establish `docs/design/release/release.md` as the living owner of the standing Release responsibility, with precise requirements, applicability, technical relationships, meaningful rationale and representative expected outcomes.

Remove superseded Release design sources and redundant copies once their necessary content and remaining uses are resolved. Reconcile System and directly affected consumers as part of the same adoption. Preserve operational release safety and truthful historical evidence, using validation proportionate to the actual changes.

## Scope and non-goals

| Item | Scope budget treatment | Boundary |
| --- | --- | --- |
| Release model and source retirement | core to this proposal | Build the Release model and complete justified removal of its superseded design sources. |
| System and direct consumers | same-slice dependency | Update ownership, navigation and necessary references or operational readers affected by the transfer. |
| Retention and source-specific checks | same-slice dependency | Select exact amendments needed to remove redundant sources; retain the obligations and proof protecting real release operations. |
| Distribution, Installation and general Validation Execution models | separate proposal | Consume their existing contracts; do not require those model transfers before Release can complete. |
| Actual release or publication | out of scope | No version bump, tag, registry publish, GitHub release, public installation or customer adoption. |

The initial source group is [Release Process Contract](../../specs/release-process-contract.md), [Release Transaction Automation](../../specs/release-transaction-automation.md), their matching test specifications, [standing-process ADR](../adr/ADR-20260523-release-process-contract.md) and [transaction-profile ADR](../adr/ADR-20260629-release-transaction-profile.md). Include their applicable amendments and Release portions of the mixed architecture, notably “Standing release-process flow”, “Release and adapter evidence” and “Public npm package boundary”, plus release-specific obligations in the published-skill-first contract. This is an inspection boundary, not an approved deletion list.

Design selects exact clauses, related diagrams and necessary consumers. Shared documents retain their unmigrated remainder. Version-specific publication contracts enter only where they supply a still-applicable standing obligation or a direct dependency. Unrelated skill improvements, archive cleanup, broad validation redesign, new release automation and supported-behavior retirement remain outside this initiative.

## Governing principle

> Give Release one complete current contract, preserve necessary engineering meaning, and remove superseded representations only when their remaining uses are resolved.

## Proposed direction

### Establish a distinct, bounded Release owner

Release should explain the boundary between routine operations on reviewed work and changes requiring engineering approval; release identity and profile authority; preparation and publication permissions; required proof and evidence; external-state uncertainty; and failure, retry and recovery behavior.

Keep component invariants with their existing owners. Distribution supplies package contents and identities; Installation owns materialization and project-state safety; Skill owns common content requirements. Test supplies protective-value criteria, Review and Closeout owns engineering assessment and evidence applicability, and Workflow coordinates engineering work. Release owns how their applicable results compose for a release operation. A passing check or completed engineering review does not itself grant publication authority.

System should reference the adopted Release model and its relationships without duplicating its local rules. Creating the model alone does not transfer authority: adoption requires reviewed coherent implementation and successful Verify.

### Transfer current meaning precisely

Reconcile numbered and substantive unnumbered obligations, later amendments, important exceptions, technical realization, failure knowledge and representative acceptance intent. State each surviving rule and its applicable population precisely enough for a maintainer or validator author to apply it without consulting deleted prose. Identify approved equivalents and supersessions instead of restoring older requirements or relying on a general “preserve behavior” promise.

Preserve distinctions that matter in the inspected baseline: routine versus special releases; profile-generated content versus human narrative and historical immutable surfaces; preparation versus publication; preflight versus full release verification; local candidate proof versus observed public evidence; uncertain publication outcomes versus safe retry; and emergency deferrals versus non-deferrable requirements. Retain meaningful rationale for immutable published versions and recovery through the currently supported actions.

Do not copy completed rollout conditions or old lifecycle procedures into the current contract. Resolve their status through existing Design displacement mappings. This initiative consolidates Release ownership; it does not silently weaken authentication, provenance, identity, freshness, recovery or publication requirements.

### Remove superseded sources and reconcile consumers together

Make source removal part of the delivered outcome. Remove fully superseded originals and redundant archive copies when their necessary meaning has a complete destination and no remaining use requires them. Do not create archive snapshots, redirects or original-path duplicates by default. Extend or amend the exact current retention rules through their owners where required; the earlier cleanup's scoped exception is not blanket deletion authority.

Retain a source only for a named remaining need and owner, such as an unmigrated obligation, operational reader or exact evidence still relied upon. Preserve mixed remainders. Historical citations alone do not mandate permanent checkout retention, but removing a subject must not retarget its old approval, erase an open concern or undermine current reliance on its evidence.

Release profiles, schemas, manifests, templates, fixtures, release notes and publication evidence are operational or evidentiary artifacts, not disposable design prose. Preserve them with their real consumers. Reconcile affected scripts, validators, workflow guidance and navigation; where package bytes actually change, inspect and update dependent current metadata through its owning builder. Preserve historical release identities. An inseparable out-of-scope change returns for a scope decision.

### Validate the affected result proportionately

For source-only changes, focus on semantic preservation, usable ownership, links, actual readers and exact removal boundaries. Independent assessment judges meaning; mechanical checks establish relevant structure and dependency facts. Do not require running a release, public smoke or every historical experiment merely because Release documentation changes.

If an executable, packaged input, selector, schema or evidence generator changes, allocate checks protecting that boundary. Unknown impact requires investigation and broader proof where justified. Reuse applicable passing evidence under its owner's existing policy; retain explicit freshness requirements and runtime safeguards for real operations. Amend obsolete location assertions through their owner rather than skipping required failures. No new runner, permanent check catalogue or test-deletion quota is selected.

Completion requires a usable adopted Release model, coherent consumers, justified source cleanup and explicit ownership of retained remainders. Fresh independent final whole-change Code Review and distinct Verify remain required. The remaining Distribution, Installation and validation work stays separately owned in the existing follow-up records.

## Feasibility

**Assessment: feasible as a bounded Release-model extraction and coordinated source cleanup.** System already identifies this coherent recurring responsibility, and the two principal specifications and ADRs provide a concrete baseline for standing process and transaction-profile ownership. No new publishing mechanism is needed to begin Design.

The inspected sources do not establish a complete dependency graph, current conformance of all release tooling, or individual files safe to remove. Design must reconcile later amendments and actual consumers before selecting deletions. The minimum package is Release, scoped System changes and exact existing-owner amendments needed for retention or integration. No measured savings or safe whole-spec deletion is claimed by this proposal.

## Impact and major trade-offs

One living owner can reduce competing authority, but only if it preserves useful technical depth and removes the replaced definitions. Retained exceptions may temporarily leave mixed legacy documents. That is preferable to losing necessary obligations, but each exception needs a concrete owner and reason.

Release touches irreversible external operations. Proportionate proof for documentation cleanup must remain distinct from the proof and permissions required when a real release runs. This direction preserves that distinction while avoiding publication work as a prerequisite for consolidation.

## Decision requested

Approve establishing the **Release model** and retiring its superseded design sources through one bounded, coordinated adoption. Preserve necessary rules, applicability, rationale and evidence; remove originals and redundant copies whose remaining uses are resolved, without automatic archival duplication.

Approve the scoped System, retention and consumer amendments needed for that result, with proportionate validation and preserved independent assessment. Leave other model transfers and actual publication separately authorized.

Approval selects this direction for Design. Exact requirements, file removals, consumer edits and proof allocation require the normal reviewed Design and Delivery process. This proposal does not authorize implementation, publication, rewriting historical judgments or deletion merely because a source lacks a model owner.
