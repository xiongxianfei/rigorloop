# Clean the Repository Around Its Current Design

## Challenge

Current RigorLoop contracts coexist with superseded specifications, test specifications, architecture documents, ADRs, archive copies and reports. Some validation machinery still reads those sources. Contributors must distinguish current authority from historical evidence before they can safely change the product, and obsolete dependencies can perpetuate unnecessary checks and documents.

The earlier [necessary-Design consolidation](2026-09-09-simplify-required-validation-and-design-retention.md) selected a bounded Validation-related source set. The requested cleanup now covers the repository's legacy documentation and unnecessary check scripts together. The user has already requested simpler governance and a [Git-history retention policy](../../CONSTITUTION.md#repository-cleanup-and-historical-retention); those edits are present on this branch and form the direction's basis, without establishing cleanup completion.

## Goals

- Make current responsibilities and behavior understandable from the living Design hierarchy and concise entry guidance.
- Remove obsolete documents, archive copies, reports, check scripts and exclusive fixtures from the current tree, using Git for retired history.
- Preserve necessary requirements, decisions, failure knowledge and regression protection in current owners and useful proof.
- Complete real removals and consumer reconciliation; an inventory alone does not satisfy the cleanup.

## Scope and non-goals

| User intent or dependency | Initial goal treatment | Scope budget treatment | Boundary |
| --- | --- | --- | --- |
| Remove old design documents | in scope | core to this proposal | Assess `docs/archive/`, `docs/adr/`, `docs/architecture/` and legacy `specs/*.md`, including `specs/*.test.md`; transfer surviving meaning and remove retired sources. |
| Clean reports and references | in scope | core to this proposal | Assess `docs/reports/` and `specs/references/`; resolve actual release, resource and validation consumers before removal or justified retention. |
| Remove unnecessary check scripts | in scope | core to this proposal | Assess repository-owned check scripts, supporting modules and exclusive fixtures for retired behavior or redundant protection. |
| Reflect the newest design | in scope | same-slice dependency | Reconcile affected owning Designs, README, contributor guidance, project map, indexes, skills, manifests and current links. Preserve the concise Constitution and AGENTS direction. |
| Reconcile executable consumers | in scope | same-slice dependency | Correct directly affected CLI, CI, validation catalog, generators, packaging and release dependencies; this includes retiring consumers that exist only to support obsolete material. |
| Remove completed historical evidence | in scope | separate implementation slice | Historical change records, proposals, plans and evidence may leave the tree once ongoing work and current reliance are resolved; preserve recoverability and original judgments. |
| Redesign the product or validation platform | out of scope | out of scope | No new runner, cache, archival service, permanent retirement ledger, customer migration or unrelated feature retirement. |

These directories are assessment boundaries, not blanket deletion instructions. Every selected family needs an explicit disposition; a retained file needs a concrete current purpose and owner. Necessary operational files may remain or receive a coherent current home. No family may silently disappear into a follow-up to claim completion.

The [independent-parallel-tests initiative](2026-09-13-independent-parallel-tests.md) retains its case-isolation and scheduling direction. This proposal consumes that work's actual adopted state and addresses remaining obsolete sources and checks; it does not reopen or claim its completion. Open work and evidence required for current review, verification or release remain available. Publishing, pushing, merging and rewriting Git history are excluded.

## Governing principle

Keep what the current system needs in the current tree; preserve retired history in Git.

## Proposed direction

Use [System](../design/system.md) and its Skill, CLI and Engineering owners to establish the current responsibility map. Identify which legacy requirements, decisions and acceptance obligations survive, and reconcile them into their owning Design without copying obsolete rollout narratives or every historical alternative.

Assess documents and their consumers together. Retire a check whose only purpose is enforcing a retired contract; consolidate overlapping checks only when retained proof covers the distinct required failures. A current caller is evidence to investigate, not an automatic reason to preserve an obsolete dependency chain. Likewise, age, filename and a passing reduced suite do not establish safe deletion.

Record a concise change-local disposition of removals, transfers and justified retention. Replace current provenance references with recoverable commit-and-path references where history is still cited. Do not create replacement archives or rewrite historical judgments and links. Current operation and current governing meaning must remain available without retrieving deleted sources from Git.

Design will settle exact responsibility transfers, affected compatibility boundaries and retention exceptions. Delivery will allocate reviewable source groups and suitable verification. Reconcile navigation and operating guidance with actual removal so contributors encounter the current hierarchy consistently. Completion requires actual cleanup, preserved current protection and the required independent review and Verify evidence.

## Feasibility

Assessment: feasible to enter Design, with consumer analysis required before deletion. The repository already has a current model hierarchy, Git history, repository-owned validation and a cleanup policy. Initial tracked-file inspection found 5 archive files, 54 ADR/architecture files, 107 report files, 102 top-level test specifications and 3 reference documents. These counts establish a bounded starting population, not a deletion estimate.

Inspected consumers demonstrate why coordinated cleanup is necessary: `scripts/boundary_first_reference.py` reads `specs/references/`, and `scripts/release_execution.py` writes and consumes adapter reports under `docs/reports/`. Existing [Validation](../design/engineering/validation.md) and [Packaging](../design/engineering/packaging.md) owners provide the relevant contract boundaries. The project map contains stale record-format descriptions, so this assessment uses direct source inspection rather than relying on its architecture summary.

The main unknown is how much unique current meaning or failure protection remains in each candidate. An unresolved owner, unrecoverable historical content or required consumer without a coherent replacement blocks that removal, rather than justifying weaker coverage. None prevents drafting and reviewing this direction. No file-count, runtime or maintenance-cost improvement is claimed yet.

## Impact and major trade-offs

This extends earlier bounded consolidation to broad repository cleanup and deliberately replaces historical-only tree retention with Git retention. A shallow checkout or source archive will no longer necessarily contain retired evidence; historical investigation may require obtaining the referenced revision. Current work and current reliance must remain self-contained.

The owner-requested clarification to [VISION.md](../../VISION.md#what-would-prove-this-wrong) distinguishes current reliance from retired history: current authoritative work remains reconstructable without Git, while retired history in this repository may require it. The matching [positioning rationale](../vision/strategic-positioning.md) preserves recoverability and customer portability. This resolves the prior wording conflict without removing current evidence duties; [authoring evidence](../changes/2026-09-13-current-design-repository-cleanup/evidence/vision-authoring.json) records the bounded revision.

Removing obsolete enforcement reduces maintenance but can hide regressions if protection is mistaken for historical clutter. Required negative, recovery, packaging and release proof remains a condition of acceptance. The cleanup should not replace old documents with equally large inventories or proliferating model files.

## Decision requested

Approve a repository-wide cleanup direction covering all listed document and check families, with current Design ownership, real removals, Git retention for retired history and dependency-complete preservation of required behavior and proof.

Use the owner-authorized current-versus-retired distinction now reflected in the vision. Approve proceeding to detailed Design after Proposal Review; exact removals, implementation, adoption and external actions remain subject to their own contracts and gates.
