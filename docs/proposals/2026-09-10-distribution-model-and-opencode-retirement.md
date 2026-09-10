# Unify Distribution and Installation, Retire OpenCode and Superseded Sources

Owning change: [Distribution model and OpenCode retirement](../changes/2026-09-10-distribution-model-and-opencode-retirement/change.json).

## Challenge

Skill delivery spans adapter generation, archive identity, target installation, managed state and recovery, but its current engineering contract is spread across specifications, ADRs and mixed architecture prose. System lists Distribution and Installation as separate candidates even though they share one source-to-installed-environment responsibility. Contributors must reconcile that boundary themselves, making duplicate tooling and conflicting installation guidance harder to detect.

The local skill investigation exposed a concrete example: `scripts/build-skills.py` defaults to generating `.codex/skills/`, while the supported Codex installer targets `.agents/skills/`. Both directories were present in the session's skill catalog. The script explains a possible creation mechanism, not who created that particular copy. Current adapter metadata also selects OpenCode alongside Codex and Claude Code, extending generation, installation, validation and release obligations beyond the desired supported population.

## Goals

Establish one Distribution model covering packaging and safe installation, remove the design sources it fully supersedes, withdraw current OpenCode support, remove managed-state creation and automatic managed upgrades, and remove stale delivery scripts and their obsolete consumers. Leave contributors with one accessible contract and a coherent supported path for Codex and Claude Code, without losing archive integrity, local-state safety or necessary regression protection.

## Scope and non-goals

| Initial user intent | Initial goal treatment | Scope budget treatment | Intended outcome |
| --- | --- | --- | --- |
| Make the new model | in scope | core to this proposal | Create `docs/design/distribution/distribution.md`, combining generation, distribution and installation responsibilities; reconcile System and FU-013. |
| Remove old design documents | in scope | core to this proposal | Transfer surviving meaning and decisions, then remove fully superseded specifications, matching test specifications and ADRs, plus precisely selected mixed-architecture prose. |
| Remove OpenCode support | in scope | separate implementation slice | Withdraw OpenCode from current supported targets, generated packages and aliases, CLI installation, current guidance, validation and release composition. |
| Remove stale scripts | in scope | separate implementation slice | Delete obsolete or redundant distribution/installation/OpenCode tooling and reconcile actual callers while retaining necessary protection. |
| Remove managed-state creation and automatic managed upgrades | in scope | explicit user refinement | Keep safe install-only delivery; ignore and preserve project state, stop on destination conflicts by default, and allow explicit complete replacement with `--force` without a managed upgrade/migration path. |
| Coordinate shared consumers | in scope | same-slice dependency | Amend affected Skill, Release, System, documentation, metadata, CI and tests so the selected direction works across the complete delivery path. |

All four original outcomes and the explicit state/upgrade simplification belong to this initiative; implementation slicing does not defer any of them. The script cleanup is bounded to this delivery responsibility and support withdrawal, rather than an unrelated repository-wide cleanup. A script's age or filename alone does not establish that it is stale.

Preserve immutable published archives, historical release metadata and assessment records with their original meaning. Historical mention of OpenCode is not current support and is not a blanket deletion target. Existing customer files and installations are not automatically deleted or migrated; explicit force installation may replace only candidate destination units. Preserve safe handling of old managed state and provide an explicit transition disposition without retaining an undocumented current OpenCode installation path.

Do not introduce a separate Installation model, a Validation Execution model, new adapter platforms, a new workflow engine or unrelated skill-procedure changes. This proposal does not perform implementation, configure remote services, publish packages or authorize destructive cleanup of local runtime directories.

## Governing principle

Give skill delivery one accountable owner while keeping package construction, local installation permission and public publication authority explicit.

## Proposed direction

Adopt Distribution as the owner of canonical-to-adapter transformation, package inventory and identities, verified acquisition, target placement, destination-conflict handling and explicit replacement. Skill continues to own authored content and resource requirements. Release continues to own publication authorization, public observations and release recovery. CLI's adopted recording responsibility does not absorb the installer contract merely because both use the same executable.

Remove managed-state creation and automatic managed upgrades from the product scope. After acquiring and verifying the package, check every destination skill directory or declared file before writing. Any existing destination conflicts by default, even when identical; report all conflicts and install nothing. Explicit `--force` replaces complete conflicting skill directories/files, including obsolete contents, while preserving unrelated skills and project files. Shared target parent directories are not conflict units. Archive, containment and symlink safeguards apply in both modes. Existing project state is neither interpreted nor an admission marker and remains untouched. This supersedes the earlier state-presence rejection and additive identical-file no-op choices.

Replace the two candidate boundaries in System with this combined responsibility. Resolve build output versus active installation explicitly: ordinary generation should not implicitly create a second active skill installation. Reconcile the existing `.codex/skills/` mirror path with supported Codex placement under the new contract; preserve intentional local edits and require appropriate authority for cleanup.

Design must map the surviving clauses, decisions, compatibility obligations and consumers of the adapter invocation/archive-install, target-native init, multi-adapter download and lockfile source families. Transfer necessary meaning into Distribution and remove the fully superseded documents without automatic archive copies or competing normative redirects. Retain only explicitly bounded mixed-source obligations with a named owner. Historical judgments remain about their original subjects; model adoption requires reviewed coherent implementation and successful Verify.

Limit current supported adapters to Codex and Claude Code. Remove OpenCode's active generation, command aliases, installer selection, published support claims and applicable current package/release requirements together. Define safe rejection and transition behavior for removed-target requests and existing state. Reconcile Release's current three-target routine population explicitly; support withdrawal cannot silently bypass its contract or overwrite historical release evidence.

Inspect delivery scripts and their callers, including the local mirror builder, adapter builders and validators, installer helpers, selectors and CI/release consumers. Remove scripts whose necessary capability is obsolete or coherently supplied elsewhere. Preserve useful independent operations and required negative/regression proof; do not rename a redundant script or replace it with a wrapper merely to claim retirement. Design settles exact dispositions, and Delivery allocates concrete implementation and proof.

## Feasibility

Assessment: feasible with bounded but material compatibility work. The [System inventory](../design/system/system.md#candidate-models-and-legacy-source-ownership) already identifies the relevant source families and [FU-013](../follow-ups.md) assigns the remaining responsibility. The [adapter manifest](../../dist/adapters/manifest.yaml), [installation guide](../../dist/adapters/README.md), [CLI adapter mapping](../../packages/rigorloop/dist/lib/adapters.js) and [local mirror builder](../../scripts/build-skills.py) provide concrete existing implementation boundaries. Reuse those mechanisms where they retain necessary behavior; no new platform is needed.

The [Release model](../design/release/release.md) is an affected dependency: REL-SR-03 names all three current targets, while package proof and public smoke consume that population. Existing [target-native installation](../../specs/target-native-init.md) and [lockfile](../../specs/rigorloop-cli-lockfile.md) contracts protect local state; their integrity and no-data-loss safeguards survive, while state interpretation, recorded managed-tree verification, creation, migration and automatic replacement are intentionally superseded. The [adapter invocation contract](../../specs/skill-invocation-commands-for-adapters.md) contains OpenCode-specific behavior whose withdrawal is intentional, alongside retained target guidance.

The project map predates recent model adoption, so this proposal uses direct inspection of the named owners and implementation surfaces for this area. No claim is made that the complete deletion set or all historical readers have already been audited. Unknown operational consumers, unresolved retained-target obligations or unsafe old-state handling block the affected retirement until Design resolves them. None currently prevents entering Design on this direction.

## Impact and major trade-offs

Removing OpenCode, state creation and automatic managed upgrades remains a public compatibility break. Repeated default installation now reports conflicts even for identical content. Explicit force replacement removes local changes and obsolete files within selected skill directories; unrelated skills, project files and state files are preserved. Existing state may become stale after replacement; the installer makes no managed-state consistency claim. This direction supersedes both successful read-only compatibility and state-marker rejection without rewriting their historical judgments. Release applies its versioning/publication policy to the separately authorized adopting release.

A combined model reduces cross-document reconciliation but carries both artifact and filesystem concerns. Keep those internal boundaries explicit rather than creating two owners prematurely. Source and script removal reduces maintenance only if necessary behavior and evidence remain accessible; a smaller inventory alone is not success.

## Decision requested

Approve one Distribution model covering packaging and installation, exact retirement of superseded design sources, complete withdrawal of current OpenCode support, removal of managed-state interpretation, creation and automatic upgrades, default conflict rejection and explicit force replacement, and bounded removal of stale delivery scripts as one initiative. Accept the public compatibility change while preserving Codex/Claude Code protection, historical evidence and existing local-state safety.

The next stage is independent Proposal Review, followed by reconciled Design and its source/consumer dispositions. Approval of this direction does not approve an uninspected deletion list, waive later review or authorize publication.
