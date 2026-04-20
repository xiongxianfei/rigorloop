# RigorLoop Constitution

## Project purpose

RigorLoop is a Git-first starter kit for AI-assisted software delivery. It exists to help contributors and maintainers build software with explicit proposals, specs, architecture decisions, plans, tests, review gates, verification, and explainable change history.

The repository MUST optimize for reviewability, traceability, and trustworthy automation over speed-by-default.

## Source of truth order

External runtime instructions still outrank repository artifacts. Within the repository, the source-of-truth order is:

1. `CONSTITUTION.md`
2. approved feature specs in `specs/`
3. approved architecture and ADR documents under `docs/architecture/` and `docs/adr/`
4. active execution plans under `docs/plans/`
5. matching test specs in `specs/*.test.md`
6. workflow summaries such as `docs/workflows.md`
7. `AGENTS.md`
8. code, scripts, schemas, and tracked fixtures
9. chat history and prior informal discussion

Rules derived from a lower-priority artifact MUST NOT silently override a higher-priority artifact.

`AGENTS.md` and `docs/workflows.md` are operating guides. They SHOULD summarize and point to the governing artifacts above, not compete with them.

## Spec-driven rules

Changes that affect externally observable behavior MUST have an approved spec before implementation.

The full lifecycle MUST be used for changes that affect any of the following:

- public behavior
- workflow order or stage policy
- architecture boundaries
- CI behavior
- schemas
- generated-output logic
- security-sensitive behavior
- release packaging

Fast-lane work MAY skip the full lifecycle only when it stays inside the approved trivial-change categories and still records the required fast-lane spec evidence.

Specs MUST express normative requirements in reviewable form. When the repository uses requirement IDs, downstream tests, verification notes, and change artifacts MUST cite those IDs rather than relying on vague prose references.

Specs MUST define non-goals and compatibility expectations for behavior-changing work.

## Test-driven rules

Before implementing non-trivial behavior changes, contributors MUST read the matching test spec when one exists.

For non-trivial work, the test spec MUST operationalize the approved feature spec and MUST NOT override it.

Tests, fixtures, or other proof surfaces SHOULD be written or updated before implementation when feasible.

Bug fixes MUST add regression coverage or an explicit failure reproduction path before the fix is considered complete.

Contributors MUST NOT claim a behavior works unless they ran or inspected a concrete proof surface for it. “Should work” is not verification.

## Architecture rules

Canonical authored workflow content lives in:

- `docs/`
- `specs/`
- `skills/`
- `schemas/`
- `scripts/`

Generated Codex compatibility output under `.codex/skills/` MUST NOT be hand-edited. It is derived output, not the source of truth.

Repository validation logic MUST live in repo-owned scripts. GitHub Actions workflows SHOULD remain thin wrappers that set up tooling and delegate to those scripts.

Plans MUST follow `docs/plans/0000-00-00-example-plan.md`. `.codex/PLANS.md` MUST NOT be reintroduced as a second planning surface.

For planned initiatives, `docs/plan.md` MUST remain the lifecycle index and concrete files under `docs/plans/` MUST remain the plan bodies that carry initiative detail.

During execution, `implement` MUST keep the active plan body's progress, decisions, discoveries, and validation notes current enough that later stages can review the real initiative state.

Change-local artifacts under `docs/changes/<change-id>/` SHOULD stay concise and MUST link back to approved top-level artifacts instead of becoming a second long-form source of truth.

Architecture-affecting changes MUST update the relevant architecture document or ADR in the same change.

## Security and privacy rules

Secrets, credentials, tokens, and private keys MUST NOT be committed.

Machine-local paths, usernames, host-specific command workarounds, and debug-only artifacts MUST NOT be committed unless they are intentionally part of a reviewed example and clearly justified.

Changes that affect security-sensitive behavior, review gates, or release boundaries MUST use the full lifecycle and MUST NOT be treated as fast-lane work.

New dependencies SHOULD be avoided when existing repository scripts or the standard runtime can solve the problem. When a new dependency is necessary, the spec or architecture doc MUST justify it.

## Compatibility rules

Changes to workflow stage order, CI behavior, schema shape, generated-output logic, or public contributor expectations MUST be treated as compatibility-sensitive changes.

Compatibility-sensitive changes MUST document migration, rollback, or adoption expectations in the governing artifacts for that change.

Generated output changes MUST be deterministic and reproducible from canonical sources.

Deprecations or removed paths MUST be reflected in contributor-facing docs in the same change that removes or supersedes them.

## Verification rules

Before PR, contributors MUST run the repository-owned validation commands required by the active plan, matching test spec, or workflow docs.

When `scripts/ci.sh` is the repository-wide validation wrapper, contributors SHOULD run it unless the task is intentionally narrower and the plan or test spec names a smaller proof scope first.

Hosted CI MUST NOT be claimed as passed unless the hosted run was actually observed.

Local validation claims MUST name the commands actually run.

Non-trivial changes MUST leave contributor-visible verification evidence in the plan, verify report, PR body, or change-local artifacts.

For planned initiatives, final lifecycle closeout MUST update both `docs/plan.md` and the plan body when lifecycle state changes, and `verify` MUST treat stale lifecycle state between them as blocking PR readiness.

Until repository-specific release checks replace the current conservative template behavior, contributors MUST treat `scripts/release-verify.sh` and `release.yml` as non-authoritative for broader completion claims.

## Review rules

`proposal-review` SHOULD be used for major, risky, or direction-setting changes.

`spec-review` MUST happen before implementation for behavior, workflow, schema, or compatibility changes.

`architecture-review` SHOULD happen for cross-component, high-risk, or boundary-changing design work.

`plan-review` MUST happen for multi-milestone or sequencing-sensitive work.

`code-review` and `verify` MUST happen before non-trivial changes are considered ready for PR.

When review feedback exists, each material item MUST be resolved, rejected, or deferred with rationale. When the review creates durable project memory, a standalone `review-resolution.md` MUST be used.

## Documentation rules

Behavior changes MUST update the relevant spec, test spec, docs, fixtures, or examples in the same change when those artifacts exist.

Workflow or governance changes MUST update `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md` when their guidance is affected.

Architecture or boundary changes MUST update the relevant architecture document or ADR.

When a change leaves durable lessons for future contributors, the repository SHOULD capture them through the `learn` stage instead of leaving them only in chat or PR comments.

## Agent behavior rules

Agents MUST prefer the smallest change that fully satisfies the request.

Agents MUST NOT add unrelated refactors while implementing a scoped task.

Agents MUST NOT silently guess around spec gaps, review findings, or failing validation.

Agents MUST NOT fake CI status, verification status, review completion, or artifact readiness.

Agents MUST NOT rewrite history, revert user changes, or delete unrelated work unless explicitly requested.

Agents MUST remove or challenge stale instructions when they are demonstrably wrong, instead of working around them silently.

Agents MUST keep chat-only reasoning subordinate to tracked repository artifacts once the project has written guidance for a topic.

## Fast-lane exceptions

The fast lane MAY be used only for:

- typos
- formatting-only changes
- small documentation clarifications
- comment-only changes
- small test-fixture corrections
- small non-behavioral renames
- minor generated-artifact refreshes that do not change generator behavior

Fast-lane work MUST still record:

- intent
- expected change
- out of scope
- validation

That fast-lane spec MUST be visible in at least one tracked or review-visible location such as the PR body, commit message, issue comment, or linked change note.

The fast lane MUST NOT be used for behavior changes, workflow-order changes, CI behavior changes, schema changes, architecture changes, generated-output logic changes, release packaging changes, or changes that are hard to roll back safely.
