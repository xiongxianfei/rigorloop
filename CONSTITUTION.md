# RigorLoop Constitution

## Project purpose

RigorLoop is a rigorous software engineering workflow for AI coding agents. It exists to help contributors and maintainers turn product intent into traceable proposals, requirements, tests, architecture decisions, plans, implementation, verification evidence, and review outcomes.

The repository MUST optimize for reviewability, traceability, trustworthy automation, and design-implementation consistency over speed-by-default or code volume. Git, CI, and pull requests are compatibility surfaces for that workflow; they are not the project purpose.

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

For project vision and proposal-fit questions, the source-of-truth order is:

1. `CONSTITUTION.md`
2. `VISION.md`
3. `specs/`
4. proposals
5. README front-matter

`VISION.md` is the canonical project-vision artifact for project identity, target users, commitments, refusals, and proposal-fit reference. It is subordinate to `CONSTITUTION.md` and does not replace specs, proposals, architecture artifacts, or execution plans.

Proposals created or substantively revised after this spec is adopted include `Vision fit`. README content between `<!-- vision:start -->` and `<!-- vision:end -->` is generated from `VISION.md`. README front-matter is not the source of truth when it conflicts with `VISION.md`.

`docs/project-map.md`, when present, is a living reference rather than a standing artifact. Contributors MUST NOT rely on it when it is absent, known-stale, contradicted by the current repository, or missing the relied-on area unless they refresh it or record a no-map rationale.

## Spec-driven rules

Changes that affect externally observable behavior MUST have an approved spec before implementation.

RigorLoop recommends one standard workflow for complete AI-assisted delivery. Public workflow guidance MUST NOT classify work into separate routes by speed, completeness, size, or risk labels.

Users MAY manually invoke an individual skill for focused output. A manual skill invocation is isolated by default and does not imply that the full workflow has been completed.

Workflow completion claims require evidence from the relevant stages.

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
- `templates/`

Templates under `templates/` are canonical authored scaffolds. They are not lifecycle-managed architecture or ADR records, and template-like files MUST NOT be placed under `docs/architecture/` or `docs/adr/`.

Generated Codex compatibility output under `.codex/skills/` MUST NOT be hand-edited. It is derived output, not the source of truth.

Repository validation logic MUST live in repo-owned scripts. GitHub Actions workflows SHOULD remain thin wrappers that set up tooling and delegate to those scripts.

Plans MUST follow `docs/plans/0000-00-00-example-plan.md`. `.codex/PLANS.md` MUST NOT be reintroduced as a second planning surface.

For planned initiatives, `docs/plan.md` MUST remain the lifecycle index and concrete files under `docs/plans/` MUST remain the plan bodies that carry initiative detail.

During execution, `implement` MUST keep the active plan body's progress, decisions, discoveries, and validation notes current enough that later stages can review the real initiative state.

For planned initiatives, the active plan `Current Handoff Summary` MUST own current live state. Change metadata, review-resolution records, review logs, explain-change records, verify evidence, and PR handoff text are scoped evidence surfaces and must not own the active plan's current next stage. State-changing handoffs MUST perform a state-sync check across affected owners before downstream readiness is claimed.

Lifecycle-managed top-level artifacts under `docs/proposals/`, top-level `specs/`, `specs/*.test.md`, `docs/architecture/`, and `docs/adr/` MUST keep status inside the artifact as tracked source of truth. For proposals, top-level specs, test specs, and architecture documents, `reviewed` is transitional review output rather than a durable relied-on state. Durable current states are `accepted`, `approved`, and `active`; terminal or historical states include `deprecated`, `rejected`, `abandoned`, `superseded`, and `archived`.

For lifecycle-managed artifacts, `Next artifacts` preserves planned next steps while the artifact is active. `Follow-on artifacts` or `Closeout` records actual downstream artifacts or final disposition instead of rewriting planning history. `superseded` artifacts MUST identify their replacement through `superseded_by` or equivalent labeled text.

Change-local artifacts under `docs/changes/<change-id>/` SHOULD stay concise and MUST link back to approved top-level artifacts instead of becoming a second long-form source of truth.

For non-trivial changes, the baseline change-local artifact pack MUST include `docs/changes/<change-id>/change.yaml` plus durable Markdown reasoning. New work SHOULD default to `docs/changes/<change-id>/explain-change.md`, while approved legacy top-level `docs/explain/*.md` artifacts remain valid until migrated or retired.

Architecture-affecting changes MUST update the relevant architecture document or ADR in the same change.

## Security and privacy rules

Secrets, credentials, tokens, and private keys MUST NOT be committed.

Machine-local paths, usernames, host-specific command workarounds, and debug-only artifacts MUST NOT be committed unless they are intentionally part of a reviewed example and clearly justified.

Changes that affect security-sensitive behavior, review gates, or release boundaries MUST follow the standard workflow before completion is claimed.

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

Synchronization happens within the PR that performs the lifecycle transition, before the PR opens for review. The merge of a PR is a fast-forward of pre-validated state, not a trigger for further lifecycle changes.

For lifecycle-managed proposals, specs, test specs, architecture documents, and ADRs, `verify` MUST block on stale or inconsistent artifacts that are touched, referenced, generated, or authoritative for the changed area, and it MUST report unrelated stale baseline artifacts as warnings instead of blockers.

Before draft PR text exists, `verify` MUST use pre-PR handoff surfaces such as `docs/changes/<change-id>/change.yaml`, explain-change artifacts, the active plan, and other touched or referenced authoritative artifacts. Final PR text MUST NOT introduce new authoritative artifact references without rerunning `verify`.

Until repository-specific release checks replace the current conservative template behavior, contributors MUST treat `scripts/release-verify.sh` and `release.yml` as non-authoritative for broader completion claims.

## Review rules

`proposal-review` SHOULD be used for major, risky, or direction-setting changes.

`spec-review` MUST happen before implementation for behavior, workflow, schema, or compatibility changes.

`architecture-review` SHOULD happen for cross-component, broad-impact, hard-to-reverse, or boundary-changing design work.

`plan-review` MUST happen for multi-milestone or sequencing-sensitive work.

`code-review`, `explain-change`, and `verify` MUST happen before non-trivial changes are considered ready for PR.

In workflow-managed completion flows, agents MUST continue into the next mandatory or triggered downstream stage when an approved autoprogression spec says continuation applies. Review-only or otherwise isolated stage requests MUST remain isolated by default, except that direct `pr` still performs PR opening when readiness passes.

Manual skill invocations and bugfix skill invocations remain isolated or explicit-step unless a higher-priority approved artifact broadens their automation scope. On-demand or periodic actions such as `explore`, `research`, and `learn` MUST NOT auto-run by default unless a higher-priority approved artifact elevates them.

When review feedback exists, each material finding MUST include evidence, a required outcome, and a safe resolution path or `needs-decision` rationale before it drives fixes.

Material review findings MUST always be recorded. All material findings require detailed change-local review records. Isolation controls downstream handoff; it does not erase or downgrade material findings. Isolation stops handoff, not recording.

A detailed change-local review record MUST be preserved for every material finding before review-driven fixes or downstream routing proceed. For isolated or review-only requests, the record is required even when no downstream handoff follows.

When material findings exist for a non-trivial change, dispositions MUST be recorded in `review-resolution.md` using only `accepted`, `rejected`, `deferred`, `partially-accepted`, or `needs-decision`. `needs-decision` is not final and blocks `explain-change`, `verify`, and `pr` until resolved or explicitly deferred by an authorized owner.

Clean required formal reviews with no material findings MAY settle in the reviewed artifact when no detailed-record trigger applies. A no-material detailed review record requires `review-log.md` but MUST NOT create an empty `review-resolution.md` solely because `reviews/` exists.

`review-resolution.md` MUST use top-level `Closeout status: open` or `Closeout status: closed`. `Closeout status: closed` requires final dispositions, no `review-log.md` open findings, plus the disposition-specific action, rationale, follow-up, and validation evidence records required by the governing spec.

## Documentation rules

Behavior changes MUST update the relevant spec, test spec, docs, fixtures, or examples in the same change when those artifacts exist.

Workflow or governance changes MUST update affected operating and governance guidance, including `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md` when their guidance is affected. If an affected surface is intentionally unchanged, contributors MUST record it as unaffected with rationale or defer it with owner and follow-up in a contributor-visible tracked or review-visible surface.

Architecture or boundary changes MUST update the relevant architecture document or ADR.

When a change leaves durable lessons for future contributors, the repository SHOULD capture them through the periodic or explicitly invoked `learn` stage instead of leaving them only in chat or PR comments. Learn sessions that reach Frame use tracked records under `docs/learn/sessions/`, with durable topic guidance under `docs/learn/topics/` only when confirmed reusable lessons justify it.

## Agent behavior rules

Agents MUST prefer the smallest change that fully satisfies the request.

Agents MUST NOT add unrelated refactors while implementing a scoped task.

Agents MUST NOT silently guess around spec gaps, review findings, or failing validation.

Agents MUST NOT fake CI status, verification status, review completion, or artifact readiness.

Agents MUST NOT rewrite history, revert user changes, or delete unrelated work unless explicitly requested.

Agents MUST remove or challenge stale instructions when they are demonstrably wrong, instead of working around them silently.

Agents MUST keep chat-only reasoning subordinate to tracked repository artifacts once the project has written guidance for a topic.

## Manual skill invocation

Users may manually invoke individual skills such as `verify`, `code-review`, `explain-change`, or `pr` for focused tasks.

A manual skill invocation may produce useful output, but it is isolated by default and does not claim that omitted upstream or downstream workflow stages have completed.

If the user asks for full workflow completion, or if an agent claims workflow completion, the claim must be backed by evidence from the relevant standard workflow stages.
