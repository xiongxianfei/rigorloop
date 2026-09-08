# RigorLoop Constitution

## Design and System ownership

For this repository’s explicitly selected design-authoring and model-composition responsibility, [Design](docs/design/design/design.md) owns living model conventions, reconciled behavioral/technical authoring, decision preservation and validation mapping. [System](docs/design/system/system.md) owns the selected composition view and shared-owner relationships. The normal public author is `design`; `design-review` remains independent and selects the exact affected models, retained legacy contracts, examples and interactions. Workflow coordinates and consumes the mapping. Unmigrated responsibilities retain their declared owners and formats; installation does not adopt customer governance. The exact transfer is bounded by the models’ displacement maps and takes effect only with reviewed implementation and successful Verify. Historical IDs and approvals retain their original meaning.

## Test criteria ownership

For this repository's explicitly adopted model work, [Test](docs/design/test/test.md) owns shared derivation, protective-value and maintenance criteria (TEST-SR-01–13). Specialist reviewers and Verify judge actual plans, tests and evidence; Review and Closeout retains assessment authority policy, applicability and closeout consequences. Workflow retains coordination. Canonical consumers apply the criteria through selective quality and maintenance resources; those resources are application guidance, not another policy owner. This initiative's coordinated consumer adoption preserves historical contracts, required negative/regression proof and separately owned execution permissions. Installation does not adopt customer policy. Internal requirement mappings and package mechanics remain in contributor/governance surfaces rather than published skills.

## Review and Closeout ownership

For explicitly adopted model work, [Review and Closeout](docs/design/review-closeout/review-closeout.md) owns shared assessment and final-closeout policy within Workflow (RC-SR-01–18). Workflow retains coordination; Record Format and CLI retain representation and mechanics. This change adopts that ownership for this repository's explicitly selected initiative; installation and distribution do not activate customer projects. The model's clause-level map identifies replacement ownership, while historical contracts and their stable IDs, judgments and stored procedures below retain their exact meaning. Specialized skills apply the owner through selectively packaged guidance; they do not define competing policy. Existing separately authorized release, PR, publication and destructive-action boundaries remain in force.

## Project purpose

RigorLoop is a rigorous software engineering workflow for AI coding agents. It exists to help contributors and maintainers turn product intent into traceable proposals, requirements, tests, architecture decisions, plans, implementation, verification evidence, and review outcomes.

The repository MUST optimize for reviewability, traceability, trustworthy automation, and design-implementation consistency over speed-by-default or code volume. Git, CI, and pull requests are compatibility surfaces for that workflow; they are not the project purpose.

## Source of truth order

For explicitly adopted RigorLoop Record Format work, the [Workflow](docs/design/workflow/workflow.md), [Record Format](docs/design/record-format/record-format.md) and [CLI](docs/design/cli/cli.md) models own decision meaning, stored representation and recording mechanics respectively. The coordinated local candidate uses primary targeted commands and explicit `rigorloop-records-v2` creation; installation does not activate a project or customer. `rigorloop-records-v2` is the only supported runtime stored format. Retired inputs are rejected without fallback; historical records retain unchanged bytes and meaning as archives, not operational compatibility. In this scoped profile, one living Design file per model replaces separate specification/architecture/ADR truth. Actors own decisions, applicability and correction; the CLI constructs and safely records explicit edits. Use scoped primary reads and subject inspection, not manual file reconstruction or eligibility gates. Independent review, current proof, success-only Verify, permissions and historical preservation remain mandatory. Release/customer activation requires its separately authorized coherent adoption; retired stored-format procedures below grant no current runtime authority.

External runtime instructions still outrank repository artifacts. Within the repository, the source-of-truth order is:

1. `CONSTITUTION.md`
2. approved owning living Designs for adopted responsibilities; approved feature specs in `specs/` for unmigrated responsibilities
3. approved architecture and ADR documents under `docs/architecture/` and `docs/adr/`
4. active execution plans under `docs/plans/`
5. matching test specs in `specs/*.test.md` for manifest-bound v1 continuation
6. `AGENTS.md`
7. code, scripts, schemas, and tracked fixtures
8. chat history and prior informal discussion

Rules derived from a lower-priority artifact MUST NOT silently override a higher-priority artifact.

`AGENTS.md` is the concise operating guide. Deterministic project-local workflow facts come from `rigorloop workflow-context`; neither surface competes with the governing artifacts above.

For project vision and proposal-fit questions, the source-of-truth order is:

1. `CONSTITUTION.md`
2. `VISION.md`
3. `specs/`
4. proposals
5. README front-matter

`VISION.md` is the canonical project-vision artifact for project identity, target users, commitments, refusals, and proposal-fit reference. It is subordinate to `CONSTITUTION.md` and does not replace specs, proposals, architecture artifacts, or execution plans.

Routine vision alignment is Proposal Review evidence, not a required proposal section. A material vision conflict, revision request, or bootstrap exception belongs in the proposal's material-impact disclosure and requested decision because it can change approval. README content between `<!-- vision:start -->` and `<!-- vision:end -->` is generated from `VISION.md`. README front-matter is not the source of truth when it conflicts with `VISION.md`.

`docs/project-map.md`, when present, is a living reference rather than a standing artifact. Contributors MUST NOT rely on it when it is absent, known-stale, contradicted by the current repository, or missing the relied-on area unless they refresh it or record a no-map rationale.

## Spec-driven rules

Changes that affect externally observable behavior MUST have an approved owning Design or retained feature spec before implementation.

RigorLoop recommends one standard workflow for complete AI-assisted delivery. Public workflow guidance MUST NOT classify work into separate routes by speed, completeness, size, or risk labels.

Users MAY manually invoke an individual skill for focused output. A manual skill invocation is isolated by default and does not imply that the full workflow has been completed.

Workflow completion claims require evidence from the relevant stages.

Specs MUST express normative requirements in reviewable form. When the repository uses requirement IDs, downstream tests, verification notes, and change artifacts MUST cite those IDs rather than relying on vague prose references.

Specs MUST define non-goals and compatibility expectations for behavior-changing work.

## Test-driven rules

Before implementing a manifest-bound v1 continuation, contributors MUST read its matching test spec. V2 work reads verification allocation from the approved plan.

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

`skills/` is the only authored skill source.

For public adapter installation, contributors MUST use the active install guidance in `dist/adapters/README.md`. For `v0.1.3` and later, generated public adapter skill bodies are release archives, not tracked source under `dist/adapters/`. Contributors MUST keep `.codex/skills/` untracked when copying installed Codex adapter skills there for local runtime use, and edit canonical skills under `skills/`.

`dist/adapters/README.md` and `dist/adapters/manifest.yaml` are the tracked adapter support surface. Historical note: `v0.1.2` kept repository-tree adapter packages during the compatibility window.

Repository validation logic MUST live in repo-owned scripts. GitHub Actions workflows SHOULD remain thin wrappers that set up tooling and delegate to those scripts.

Plans MUST use the packaged scaffold in `skills/plan/assets/plan-skeleton.md`. The repository MUST NOT maintain a second plan scaffold under documentation, `templates/`, or `.codex/PLANS.md`.

For planned initiatives, `docs/plan.md` MUST remain a navigation index and concrete files under `docs/plans/` MUST remain the stable plan bodies that carry execution intent.

For current workflow-managed changes, the v2 `docs/changes/<change-id>/change.json` registry and its registered records MUST own explicit activity, work, reviews, findings, blockers, evidence and closeout assessments. Plans and other governed artifacts MUST keep stable intent and MUST NOT carry mutable workflow status or execution progress.

Authoring skills MUST write only their own governed content and authorized authoring evidence. Plan may initialize absent work exactly once from its current approved Delivery Review package; it MUST NOT initialize an unreviewed draft or replace existing work. Independent reviewers own their assessment evidence and findings. Route owns explicit activity and later work decisions, using targeted recording with current revision and exact reads; no save derives settlement or progression. Downstream skills treat upstream content and other actors' judgments as read-only and return corrections to the owner.

Historical pre-adoption artifacts MAY retain embedded status as historical evidence. A current lifecycle stage MUST NOT update that embedded status or resume a retired writable state model; concrete contradictory unfinished work discovered during retirement requires a bounded owner disposition, without automatic migration.

For lifecycle-managed artifacts, `Next artifacts` preserves planned next steps while the artifact is active. `Follow-on artifacts` or `Closeout` records actual downstream artifacts or final disposition instead of rewriting planning history. `superseded` artifacts MUST identify their replacement through `superseded_by` or equivalent labeled text.

Change-local artifacts under `docs/changes/<change-id>/` SHOULD stay concise and MUST link back to approved top-level artifacts instead of becoming a second long-form source of truth.

For non-trivial governed changes, use the selected v2 manifest and registered evidence. Successful Verify owns the durable final explanation. Preserve completed historical records and recorded identities unchanged; no migration, temporary continuation or permanent legacy reader is selected.

Architecture-affecting changes MUST update the owning Design, or the relevant unmigrated architecture document or ADR under its retained contract, in the same change.

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

Before PR, contributors MUST run the repository-owned validation commands required by the active plan, any registered v1 test spec, or workflow docs.

When `scripts/ci.sh` is the repository-wide validation wrapper, contributors SHOULD run it unless the task is intentionally narrower and the plan or test spec names a smaller proof scope first.

Hosted CI MUST NOT be claimed as passed unless the hosted run was actually observed.

Local validation claims MUST name the commands actually run.

Non-trivial changes MUST leave contributor-visible verification evidence in a verify report, PR body, or change-local artifact.

For planned initiatives, final lifecycle closeout MUST update the authoritative change-local state and stage-owned evidence. `verify` MUST treat mutable lifecycle or routing state in a governed artifact or plan as blocking PR readiness.

Synchronization happens within the PR that performs the lifecycle transition, before the PR opens for review. The merge of a PR is a fast-forward of pre-validated state, not a trigger for further lifecycle changes.

For lifecycle-managed proposals, specs, test specs, architecture documents, and ADRs, `verify` MUST block on stale or inconsistent artifacts that are touched, referenced, generated, or authoritative for the changed area, and it MUST report unrelated stale baseline artifacts as warnings instead of blockers.

Before draft PR text exists, `verify` MUST use pre-PR handoff surfaces such as `docs/changes/<change-id>/change.json`, the current contract's durable rationale surface, stable plan intent, and other touched or referenced authoritative artifacts. Only successful final Verify produces the final explanation in its v2 record. Final PR text MUST NOT introduce new authoritative artifact references without rerunning `verify`.

Until repository-specific release checks replace the current conservative template behavior, contributors MUST treat `scripts/release-verify.sh` and `release.yml` as non-authoritative for broader completion claims.

## Review rules

The following consolidated package-gate rules are current.

Only `rigorloop-records-v2` is supported at runtime. The named legacy stored formats and their exclusive creators, readers, validators, writers, progression handlers and recovery are retired. Current discovery excludes unrelated archives and fails honestly on malformed current stores; explicit retired input is rejected safely without mutation or fallback. Independent transport and document-validation versions remain separate.

Use scoped primary reads, subject inspection and targeted operations. Record explicit judgments and applicability without retargeting old approval or granting permission through a save. The CLI provides construction, validation and recoverable persistence; actors assess authority and adequacy. Correctness of recording and closeout does not universally depend on Git, PRs or network access.

`proposal-review` MUST evaluate proposal direction, scope, and embedded feasibility before design work for governed changes.

`design-review` MUST independently approve the exact affected Design package, including applicable retained legacy contracts, examples and interactions, before delivery planning relies on it.

`delivery-review` MUST independently approve the exact contract-selected delivery package before implementation.

Behavioral and technical authorship are reconciled by `design`; plan authorship remains separate. Historical registered v1 test-specification evidence remains a separate record. A package reviewer MUST NOT edit and approve the artifacts it reviews.

`spec-review`, `architecture-review`, `plan-review`, and `test-spec-review` are retired as progression entrypoints. Historical evidence remains readable but does not grant package authority.

The workflow requires `code-review` and `verify`; only successful Verify produces the final explanation and readiness evidence. After all milestones and required corrections, every governed change requires fresh independent whole-change Code Review of the complete final diff and cross-milestone interactions before successful final Verify. Milestone reviews do not substitute. PR readiness remains a separately scoped consumer assessment.

After a PR is open, a user-authorized CI repair MAY preserve those completed gates when it only restores already-approved behavior and does not change their decision basis. Such a repair uses existing commands and authority; a substantive or ambiguous correction returns to the earliest affected owning stage.

In workflow-managed completion flows, agents MUST continue into the next mandatory or triggered downstream stage when an approved autoprogression spec says continuation applies. Review-only or otherwise isolated stage requests MUST remain isolated by default, except that direct `pr` still performs PR opening when readiness passes.

Manual skill invocations and bugfix skill invocations remain isolated or explicit-step unless a higher-priority approved artifact broadens their automation scope. On-demand or periodic actions such as `explore`, `research`, and `learn` MUST NOT auto-run by default unless a higher-priority approved artifact elevates them.

When review feedback exists, each material finding MUST include evidence, a required outcome, and a safe resolution path or `needs-decision` rationale before it drives fixes.

Every supported formal lifecycle review MUST create durable review evidence or report blocked recording. Clean formal reviews use a lightweight clean review receipt. Material review findings MUST always be recorded. All material findings require detailed change-local review records. Isolation controls downstream handoff; it does not erase or downgrade review recording. Isolation stops handoff, not recording.

A detailed change-local review record MUST be preserved for every material finding before review-driven fixes or downstream routing proceed. For isolated or review-only requests, the record is required even when no downstream handoff follows.

For registered historical contracts, when material findings exist for a non-trivial change, dispositions MUST be recorded in `review-resolution.md` using only `accepted`, `rejected`, `deferred`, `partially-accepted`, or `needs-decision`. `needs-decision` is not final and blocks `verify` and `pr` until resolved or explicitly deferred by an authorized owner. Verify creates the final rationale only after success.

For registered historical contracts, clean required formal reviews with no material findings MUST still create a clean review receipt or report blocked recording. A clean review receipt proves the review happened; it does not by itself settle the reviewed artifact's lifecycle status. A no-material detailed review record requires `review-log.md` but MUST NOT create an empty `review-resolution.md` solely because `reviews/` exists.

Under registered historical contracts, `review-resolution.md` MUST use top-level `Closeout status: open` or `Closeout status: closed`. `Closeout status: closed` requires final dispositions, no `review-log.md` open findings, plus the disposition-specific action, rationale, follow-up, and validation evidence records required by the governing spec.

For current v2 work, a formal review MUST record its exact assessment, findings and applicability through targeted recording; storage does not settle or route the work. A review MUST NOT edit the artifact it reviewed, another artifact's state, or workflow routing.

## Documentation rules

Behavior changes MUST update the relevant spec, test spec, docs, fixtures, or examples in the same change when those artifacts exist.

Workflow or governance changes MUST update affected operating and governance guidance, including `CONSTITUTION.md`, `AGENTS.md`, authoritative CLI workflow context, and current stage skills when their guidance is affected. If an affected surface is intentionally unchanged, contributors MUST record it as unaffected with rationale or defer it with owner and follow-up in a contributor-visible tracked or review-visible surface.

Architecture or boundary changes MUST update the owning Design or relevant unmigrated architecture document or ADR.

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

Users may manually invoke individual current skills such as `route`, `verify`, `code-review`, or `pr` for focused tasks. Standalone `explain-change` remains invocable only from the released preactivation v2 package; the current v3 package has no standalone explanation stage or historical-contract execution branch.

A manual skill invocation may produce useful output, but it is isolated by default and does not claim that omitted upstream or downstream workflow stages have completed.

If the user asks for full workflow completion, or if an agent claims workflow completion, the claim must be backed by evidence from the relevant standard workflow stages.
