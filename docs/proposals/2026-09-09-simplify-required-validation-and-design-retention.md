# Retain Only Necessary Design with Proportionate Validation

## Challenge

RigorLoop keeps current engineering meaning across living Designs, legacy specifications, architecture sections, ADRs and archive copies. Some sources still own necessary rules or evidence; others repeat content whose purpose is already satisfied elsewhere. Contributors must read and maintain more material than the current project needs.

The preceding [consolidation proposal](2026-09-09-incremental-model-contract-consolidation.md) preserved readable originals by default. The earlier version of this proposal also made validation-policy redesign a primary deliverable. Neither expresses the user's priority precisely: retain only necessary Design content, remove unnecessary duplication, and use proportionate validation to support that cleanup.

A cleanup that creates a large new validation catalogue, requires every historical experiment to run again, or copies obsolete prose into larger models would reproduce the maintenance burden. Conversely, deleting a source without understanding its remaining use could remove the only current definition of a requirement or break a real consumer.

## Goals

Keep the current behavior, significant constraints, meaningful decisions and representative expected outcomes needed to understand and evolve each selected responsibility in its living Design owner.

Remove superseded design-source documents and redundant archive copies when no necessary use remains. Retain supporting originals only for an explicit current need and owner; historical existence alone is insufficient.

Make the cleanup easy to assess through a concise source disposition and focused checks of affected content and consumers. Validation should be sufficient for the actual change without becoming an independent redesign project or requiring unrelated execution.

## Scope and non-goals

The initial cleanup boundary remains the Validation-related legacy design sources identified by [System](../design/system/system.md#responsibility-inventory) and the preceding consolidation work. This is a bounded place to demonstrate necessary-design retention, not a requirement to redesign Validation or complete every remaining model transfer. Design selects the exact source set and receiving owners before removal.

| Area | Scope budget treatment | Boundary |
| --- | --- | --- |
| Necessary Design content and source cleanup | core to this proposal | Reconcile surviving meaning into its owner; remove unnecessary selected specifications, architecture/ADR content and archive duplicates. |
| Retention rules | same-slice dependency | Explicitly amend current rules where they otherwise require redundant copies for the selected sources. Do not rewrite historical decisions retroactively. |
| System and direct consumers | same-slice dependency | Correct completed common Skill ownership, current navigation and actual readers affected by the cleanup; keep specialist remainders explicit. |
| Proportionate validation | same-slice dependency | Check preservation of necessary meaning and affected references or consumers; revise only a directly obstructing validation obligation through its owner. |
| Broad mandatory-check, runner or gate redesign | separate proposal | Do not inventory and reclassify every check family or make a new Validation model a prerequisite for this cleanup. |
| Distribution, Installation, Release and remaining skill adoption | separate proposal | Existing FU-013–018 and their receiving owners retain this work. Their contracts remain dependencies where relevant. |

The latest goal of retaining only necessary Design is the primary outcome. The earlier request to reconsider excessive validation is preserved as a constraint on this cleanup and permission for necessary bounded amendments, rather than a second general policy initiative.

No repository-wide archive purge, new runner, cache, scheduler, migration registry, permanent per-test ledger or historical-document service is selected. Operational records, schemas, templates, resources and recovery information are not redundant design prose. Publication, real customer installation and unrelated supported-behavior retirement remain excluded.

## Governing principle

> Keep the Design information the current project needs, remove the rest when its dependencies are resolved, and validate in proportion to the change.

## Proposed direction

### Decide what must remain useful

For each selected coherent source group, identify the current requirements, applicability, important constraints, decision rationale and failure knowledge that its consumers still need. Use existing owners first. A new model is justified only by a coherent responsibility that needs its own current contract; creating a Validation Design is not an unconditional completion requirement.

Transfer surviving meaning precisely enough that authors and maintainers can work from current artifacts without reconstructing rules from archives or version history. Preserve relevant exceptions and later amendments. Do not carry obsolete rollout conditions, every rejected alternative or repeated narrative into the living Design merely because they once appeared in a source.

Use direct language. Terms such as skill checks, package checks and release checks can describe necessary obligations without introducing a glossary or inherited Gate A/B/C hierarchy. Existing interfaces retain their compatibility contract unless an explicit bounded amendment changes it.

### Remove unnecessary sources without automatic archiving

Once necessary content has a complete destination and current consumers are reconciled, remove the superseded source or redundant copy from the checkout when no remaining use requires it. Do not automatically replace it with a snapshot, redirect, archive index or original-path duplicate.

Retain an original only for a named need not adequately served elsewhere: an unmigrated current obligation, essential regression context, an operational reader or exact evidence still relied upon. Mixed files retain their necessary remainder. A historical citation alone does not make the cited file permanently necessary.

Keep current rules and required evidence understandable without Git history. Historical approvals keep their original meaning; do not retarget them to replacement content. If an assessment's original subject will no longer be available, preserve the basis needed for current reliance or explicitly cease that reliance. This does not authorize erasing open findings, falsifying completed plans or rewriting old judgments.

Amend applicable retention requirements through their current owners before adopting a conflicting deletion policy. Operational manifests, templates, schemas, fixtures and recovery files stay with their actual consumers; path cleanup alone is not a reason to move them.

### Keep validation focused on the affected obligation

For a source-only change, the normal proof should focus on whether necessary meaning has an accessible owner and whether affected references and actual readers still work. Independent assessment judges meaning; existing mechanical checks support the relevant structure and consumer boundaries. Do not require package generation, runtime suites, release checks or historical benchmarks solely because design prose was consolidated.

If the selected change affects a packaged resource, executable reader, validator, selector or other behavior-bearing dependency, include the checks that protect that affected boundary. Broaden investigation and proof when impact is uncertain; uncertainty is not evidence that nothing changed. File extensions alone do not establish impact.

Reuse an earlier passing result when its subjects, dependencies, check implementation/configuration and relevant environment remain applicable under existing evidence policy. Preserve explicit freshness requirements and the original result's limits. Failed, missing or contradicted evidence is not a reusable pass. Safeguards required during an actual write or recovery still execute at that operation.

Where a current rule would require irrelevant or duplicate execution for this cleanup, select an explicit, bounded owner amendment rather than silently skip a required check. Remove a test or exclusive mechanism only when its obligation has a justified retirement or adequate retained protection; a useful test need not be deleted merely because this change does not require it to run.

No new exhaustive validation inventory, benchmark programme or repeated full-suite requirement is selected. Use existing checks and concise grouped evidence. Fresh independent final whole-change Code Review and distinct Verify remain unchanged; their assessment scope follows the actual delivered change.

### Finish with a smaller necessary documentation set

Design identifies the exact source boundaries, surviving obligations, retention/removal decisions and directly affected consumers. Delivery allocates only the changes and proof needed to adopt those decisions. An inseparable responsibility outside the selected boundary returns for a scope decision instead of expanding into every remaining model.

A concise comparison in existing change evidence should show where necessary content now lives, what duplication was removed, what originals remain and why, and what focused proof supports the result. It must not become another permanent document catalogue duplicating the living Designs.

Completion means the selected responsibility is understandable from necessary current Design content, redundant source material has been removed where justified, remaining owners and dependencies are explicit, and affected consumers work. A validation-policy rewrite, new model count, deletion quota or measured runtime/token improvement is not required. System's completed common Skill adoption is existing evidence to reconcile, not a reason to repeat the proposal-family pilot.

## Feasibility

**Assessment: feasible as bounded Design-content consolidation and source cleanup with proportionate validation.**

Existing [Design](../design/design/design.md) and [System](../design/system/system.md) conventions provide responsibility ownership and substantive source mapping. [Test](../design/test/test.md) supplies protective-value criteria, and [Review and Closeout](../design/review-closeout/review-closeout.md) governs assessment and evidence reuse. These owners provide the necessary process without a new validation or archival platform.

The available material identifies a candidate source family, not individual documents safe to delete or a complete dependency graph. Exact necessary content, current consumers and applicable retention amendments require inspection. Such uncertainty can be resolved for the selected sources without auditing the entire repository or reopening every historical check.

The minimum Design package is the affected living owner or justified new owner, scoped System corrections and exact retention or validation amendments required by the cleanup. Existing runtime behavior and other model extractions need not change. No savings or safe deletion is claimed before inspection and adoption.

## Impact and major trade-offs

A smaller maintained documentation set should reduce repeated reading and conflicting authority, but removing sources can make older reasoning less convenient to inspect. Necessary rationale belongs in the current owner; narrowly necessary originals remain. Replacing archive copies with equally large history sections would miss the objective.

Focused validation avoids work unrelated to the cleanup, while an incomplete consumer assessment could miss a real dependency. Explicit impact assessment, proportionate checks and justified evidence reuse address that risk without making broad execution mandatory by default.

This direction changes automatic archival preservation for selected sources and narrows the preceding proposal's validation-policy redesign ambition. It does not waive supported runtime safety, specialist authority, required independent assessment or current obligations before their owning amendments are adopted.

## Decision requested

Approve retaining only necessary Design information and narrowly justified supporting material within the selected source boundary, with reviewed removal of superseded sources and redundant archive copies once their necessary content and consumers are reconciled.

Require proportionate validation of that cleanup: focused checks for affected obligations and dependencies, applicable evidence reuse, and only necessary bounded amendments to excessive execution requirements. Do not make broad validation-policy redesign, a new Validation model or unrelated full-suite execution a prerequisite for completion.

Keep System's common Skill ownership correction in scope. Leave other model transfers and remaining skill improvements with their existing follow-up owners. Preserve fresh independent final whole-change Code Review, distinct Verify, truthful records and separately authorized external actions.

Approval selects this direction for Design. Individual file or test removals, exact policy amendments and proof sufficiency remain subject to their owning Design, Delivery and assessment decisions; implementation and publication are not authorized by this proposal alone.
