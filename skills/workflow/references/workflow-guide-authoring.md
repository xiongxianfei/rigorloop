# Workflow-guide authoring

## Load condition

The workflow skill creates or refreshes the project workflow guide and artifact-location map through this procedure. Read it only when creating a new project-local `docs/workflows.md` or substantially refreshing a stale guide. Also copy `assets/workflows-skeleton.md`. Ordinary routing should reference the guide rather than rewrite it.

Do not combine guide authoring with active or resumable automation in one invocation.

## Ownership

This procedure renders established routing policy into a project-local guide. It does not create or own lifecycle policy.

It must not own source precedence, unknown-artifact behavior, stage order, architecture applicability, settlement, automation authorization, review meaning, or claim boundaries. Those remain inline or in their mapped governing procedure.

The skeleton owns section order, labels, tables, registry structure, and placeholders. It owns no policy. Omit inapplicable optional sections and never emit unfilled placeholders.

## Authoring triggers

Create or refresh the guide when:

- RigorLoop is adopted in a project and no workflow guide exists;
- artifact locations are added, removed, renamed, or customized;
- review-recording, examples, reports, or change-root placement changes;
- stage skill guidance starts relying on the artifact-location map;
- generated-output or adapter source-of-truth guidance changes;
- the existing guide contradicts current repository paths or governing specs.

Do not rewrite a current guide during ordinary routing.

## Procedure

1. Inspect repository instructions, existing guide content, actual paths, and governing workflow contracts available in the project.
2. Copy the skeleton and fill project identity, source rank, lifecycle graph, stage obligations, artifact registry, artifact-location table, review placement, plan surfaces, ownership, customization rules, migration notes, and validation notes.
3. Preserve valid project-local customization. Replace stale paths or representations only when evidence supports the new location.
4. Record affected artifact types, old and new placement, migration need, affected skills, and validation performed in a tracked or review-visible surface.
5. Validate structure and path consistency using repository-owned checks when available.

Do not require RigorLoop repository-internal specifications or documentation in a customer project. Use the governing project-local sources that exist. If neither project guidance nor a safe portable default resolves an artifact location, stop for an explicit decision.

## Content boundary

The guide may document project-local paths, custom stage obligations, repository commands, review locations, generated-output ownership, and migration notes.

The workflow skill must not author proposals, specs, plans, reviews, ADRs, or exact schemas through guide authoring. Route their content to the owning stage skill. The guide records where those artifacts live and how established workflow rules apply in the project.
