# ADR-20260810: Published-Skill-First Validation Architecture

## Owning change record

`docs/changes/2026-08-10-published-skill-first-repository-simplification/change.yaml`

## Context

RigorLoop publishes canonical skills, packaged resources, generated adapter archives, CLI installation behavior, and releases.
Its repository validation has also accumulated selectors, caches, schedulers, prompt fixtures, behavior corpora, runtime benchmarks, lifecycle parsers, and meta-tests that can become a second product architecture.

The repository deterministically owns its files, transformations, archives, metadata, and filesystem materialization.
It does not own how a particular model interprets an instruction in one runtime session.
The architecture needs one stable proof chain that preserves real package and governance failures while allowing internal validation machinery to retire in bounded slices.

## Decision

Adopt three composed deterministic product gates:

1. Gate A validates canonical skill and packaged-resource integrity.
2. Gate B generates and proves equivalent inventory, resource, declared-transformation, archive, and byte parity for Codex, Claude Code, and opencode.
3. Gate C consumes current A and B proof and adds release-only version, metadata, checksum, release-note, freshness, and rollback consistency.

Keep one separate deterministic lifecycle-governance entry point for change-record shape, transitions, review references, contradictory state, dangling evidence, and fail-closed contractual vocabularies.
Keep semantic skill quality in human or agent review.

Do not execute target-agent runtimes, send prompts, grade LLM output, inspect routing transcripts, maintain model matrices, or retry nondeterministic model runs for repository acceptance.
Allow installer materialization smoke only when installer inventory shows RigorLoop-owned filesystem logic beyond copying Gate B-proved package content; the smoke uses a local package and empty temporary directory and stops after filesystem inspection.

Retire existing subsystems only through a ledger-backed slice that records protected fixtures and failures, governing clause disposition, old-versus-replacement proof, differences, removal scope, and rollback.
The workflow automation product is not part of this retirement decision and remains governed by its own contracts.

## Alternatives considered

- Keep the current validation architecture: rejected because it preserves self-reinforcing orchestration and semantic-oracle growth.
- Keep Codex-only target-runtime behavior smoke: rejected because one LLM session is nondeterministic, does not prove other packages, and makes model interpretation a repository acceptance oracle.
- Run behavior certification across all target runtimes: rejected because it multiplies nondeterminism, cost, version matrices, and transcript grading.
- Move current machinery to another repository: rejected because it relocates rather than removes ownership complexity.
- Delete most scripts in one reset: rejected because undocumented protected failures and active contracts would be lost without recoverable proof.

## Consequences

- Canonical skill contribution and publication gain a small stable proof vocabulary.
- All three public adapter targets retain equivalent deterministic package proof.
- Release proof becomes a composition boundary instead of another semantic implementation.
- Semantic review becomes visibly responsible for instruction quality and cannot be replaced by structural validators.
- Target-runtime defects remain valid user-reported product issues, but they do not create routine model certification.
- Some current contracts and architecture remain transitional until their owning retirement slices amend them; simplification therefore occurs over several reviewable milestones.
- A single governance entry point may still use internal focused modules, but duplicated public owners and silent unknown-value fallthrough are prohibited.
- Rollback restores the last retired slice and its direct invocation without rewriting canonical skills, public archives, or historical evidence.

## Follow-up

- Inventory scripts, routed checks, fixtures, active contract clauses, and invocation sites.
- Identify the existing modules that become Gate A, Gate B, Gate C, and the governance entry point.
- Inventory installer branches and classify pure copy versus additional materialization.
- Amend or supersede each retirement candidate's active contract in its implementation slice.
- Update the canonical architecture and project map as each target-state slice becomes current.
