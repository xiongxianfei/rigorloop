# RigorLoop Constitution

## Purpose

RigorLoop helps people turn product intent into traceable, reviewable and verified software changes with AI coding agents.
The repository MUST prioritize correctness, explicitness, reviewability and agreement between design and implementation over speed or code volume.
[VISION.md](VISION.md) owns project identity and direction; Git, CI and pull requests are optional integration surfaces for the product.

## Authority and ownership

External runtime instructions and direct user instructions govern within their applicable precedence.
Within repository artifacts, follow this order:

1. This Constitution.
2. Approved owning Designs, including their decisions.
3. The initiative's approved execution plan and verification allocation.
4. [AGENTS.md](AGENTS.md), implementation and informal historical discussion.

Contributors MUST identify conflicts and follow the highest applicable authority; they MUST NOT silently blend contradictory rules or invent missing decisions.
[VISION.md](VISION.md) governs vision and proposal fit below this Constitution, ahead of feature documents, proposals and README summaries.

[System](docs/design/system.md) owns model composition and delegates detailed contracts to [Skill](docs/design/skill/skill.md), [CLI](docs/design/cli/cli.md) and [Engineering](docs/design/engineering/engineering.md).
Their approved child contracts govern their declared responsibilities; this Constitution establishes principles, and AGENTS supplies repository operating instructions.
Customer projects retain their explicitly selected contracts. Current repository responsibilities follow these owners; a new document, package or installation alone MUST NOT establish adoption or expand an approval.
Actors MUST respect artifact ownership and return corrections to the responsible owner; recording a decision does not grant approval, progression or execution permission.

## Design and compatibility

Externally observable behavior MUST have an approved owning Design before implementation.
Contracts MUST define requirements, edge cases, non-goals, compatibility and acceptance; required behavior MUST map to concrete verification, retaining stable requirement IDs where used.
[Design](docs/design/skill/authoring/design.md) owns authoring conventions and reconciled behavioral and technical decisions.
Architecture or behavior changes MUST update the affected contract, consumers, documentation and examples in the same change.

Workflow, CI, schema, generation and public contributor-contract changes MUST address compatibility and appropriate adoption, migration or recovery.
Contributors SHOULD reuse existing tooling and dependencies; new dependencies MUST have a documented justification.
Generated output MUST be deterministic and reproducible from canonical sources.

## Workflow and review

[Workflow](docs/design/skill/workflow.md) owns the standard delivery lifecycle, routing and authorized progression; [Review and Closeout](docs/design/skill/assessment.md) owns assessment and completion policy.
RigorLoop MUST present one standard delivery workflow, without separate public routes labeled by speed, completeness, size or risk.
Multi-file, risky, ambiguous, architecture-affecting or migration-heavy work MUST have a reviewable execution plan before implementation.
Plans carry stable intent; the owning change record and stage-owned evidence carry mutable progress, decisions and closeout.

Required proposal, Design and delivery reviews MUST precede reliance on their respective packages.
Reviewers MUST independently assess the exact work they approve and MUST NOT edit and approve the same subject.
Formal reviews MUST leave durable evidence, including clean outcomes; material findings MUST record evidence, required outcomes and a safe resolution path or explicit decision need before driving fixes.
Governed completion MUST include milestone reviews where applicable, fresh independent whole-change Code Review after all implementation and corrections, and distinct successful final Verify.
Only successful Verify owns the final explanation and closeout assessment; a save, milestone review, merge or PR MUST NOT substitute for required gates.

Manual skill invocations MAY produce isolated work without claiming full workflow completion; isolation does not waive review recording.
Automation MUST stay within its authorized scope and continue through required downstream stages when that authorization applies.
Optional discovery and learning remain on-demand or periodic under their owning contracts.

## Validation and evidence

[Validation](docs/design/engineering/validation.md) owns proof quality, maintenance, selection and execution; specialist reviewers judge actual adequacy.
Tests or other concrete proof SHOULD precede implementation when feasible; bug fixes MUST include regression coverage or an explicit failure reproduction path.
Contributors MUST run the applicable repository-owned checks, starting with focused validation and resolving failures before advancing dependent work.
CI SHOULD delegate validation logic to repository-owned scripts.

Completion claims MUST identify the actual commands, results and limitations; hosted CI success requires observing the hosted run.
Non-trivial changes MUST leave durable validation evidence, and governed closeout MUST reconcile the owning records before external handoff.
Stale or contradictory evidence needed for the change blocks reliance; unrelated baseline debt MUST be reported without being mistaken for a new failure.
Required behavior, edge cases and failure paths MUST be proved or explicitly disposed of by the responsible owner; missing proof MUST NOT be presented as success.

## Security and permissions

Secrets, credentials and private keys MUST NOT be committed or exposed.
Machine-local details and debug artifacts MUST NOT be committed unless intentionally justified in a reviewed example.
Agents MUST preserve unrelated work and user changes, keep scope bounded and disclose material assumptions or blockers.
External mutations and destructive actions MUST stay within explicit applicable authorization; workflow completion and installation grant no additional permissions.
Security-sensitive changes and changes to review or release boundaries MUST follow the standard workflow before completion is claimed.

## Documentation and governance maintenance

Each responsibility SHOULD have one current normative owner; entry guides MUST link to detailed contracts instead of reproducing their procedures or migration histories.
Governance changes MUST reconcile affected guidance and consumers, or explicitly document why they are unaffected or who owns deferred reconciliation.
Constitution amendments MUST make changed principles explicit; shortening a document MUST NOT silently discard a surviving obligation or broaden historical approval.
Durable reusable lessons SHOULD be captured through the learning process rather than left only in chat.

## Repository cleanup and historical retention

The current tree SHOULD contain current contracts, implementation, useful validation, operational resources and evidence needed for ongoing work or current reliance.
Git history is this repository's default retention location for retired material; historical value alone MUST NOT require retaining files or creating archive copies in the current tree.
Before deletion, contributors MUST verify recoverability from retained Git history, preserve uncommitted content and resolve surviving requirements and dependencies.
Current provenance references to retired material MUST identify a recoverable commit and repository-relative path; a tag MAY accompany the commit.

Still-applicable requirements, decisions and acceptance obligations MUST transfer to their current owner or receive explicit retirement disposition.
Cleanup MUST reconcile current links, imports, manifests, generators, CI, packaging, release consumers and validation in the same reviewed change; current operation MUST NOT depend on fetching retired files from history.
Obsolete checks and exclusive fixtures SHOULD be removed when their behavior is retired or their protection is demonstrably redundant; required negative and regression protection MUST remain supported by current proof.

Completed historical records MAY leave the current tree once current reliance is resolved; their original bytes, identities, judgments and links MUST NOT be rewritten to repair history or retarget approvals.
Historical references retain their original revision's meaning; active work, unresolved findings and required review, verification or release evidence MUST remain available until resolved or coherently replaced.
This policy supersedes older requirements for repository-tree retention solely for historical preservation, without waiving current obligations, review or validation.
Cleanup changes MUST document removal scope, surviving responsibilities, dependency reconciliation and checks run; this repository policy imposes no Git requirement on customer projects.
