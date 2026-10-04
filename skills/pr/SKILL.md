---
name: pr
description: Prepare or submit a pull request from the actual delivered diff, current review and verification evidence, and explicit external-action authority. Use after final Verify or for an isolated PR preparation request.
---

# Pull request

Identify the requested repository, remote, base, branch and submission intent. An isolated preparation request produces a reviewable title/body and next action; it does not push or create a PR. Existing user authorization to continue through PR submission permits the necessary push and creation. Merge, release, force-push, deleting remote branches and changing an existing PR's publication state require their own applicable authorization.

Inspect the actual cumulative diff against a freshly observed remote base, including relevant uncommitted work. Preserve unrelated user work. For Change-managed delivery, consume the recorded accepted basis, independent whole-change Code Review and distinct successful final Verify through the supported CLI. Read the conditional readiness reference. Unknown or outdated support returns to the responsible owner; PR work does not supply an assessment judgment.

Before pushing, identify the exact remote branch relation. Normal pushes may create an absent branch or advance a known ancestor. If remote work is ahead, diverged or uncertain, reconcile it safely and reassess affected scope. Do not force-push as a shortcut. Record the actual resulting branch/head and verify remote readback.

Look for an existing PR matching the repository, head and base before creating one. Reuse an appropriate open/draft PR. Closed, merged or ambiguous matches need an explicit disposition; do not silently create a replacement. Preserve user-authored title/body unless the request authorizes refresh or replacement. Inspect and reconcile an uncertain submission result before retrying creation.

Write the title and description around the concrete problem, delivered behavior and actual validation. Include material limitations and current review/Verify basis when relevant. Use the project's template or packaged skeleton when helpful. Do not claim hosted CI success from local tests: distinguish passed, failed, pending, unavailable, unobserved and not-applicable using actual observations. Follow supported PR/remote tools and preserve exact multiline text.

After an authorized submission, report the PR link and observed CI standing. An authorized bounded CI repair may route defects to their owner, then require applicable review and verification before updating the PR. Do not broaden execution authority or conceal a failing check merely to finish the handoff.

## Recording boundary

PR preparation reads current operational support and does not author review or verification judgments. A submitted PR is an external handoff, not completion evidence or merge authority. Skills use CLI operations and opaque revisions; never SQL or direct runtime-file edits.

## Resource map

- READ `references/targeted-recording-v2.schema.json` when constructing a supported mutation input within the invocation’s authority.
- READ `references/rigorloop-records-v4.schema.json` when interpreting closed record fields or referenced task types.

- READ `references/operational-recording.md` when inspecting the selected Change's current handoff.
- READ `references/governed-pr-readiness.md` when assessing Change-managed external readiness.
- READ `references/review-reliance.md` when later changes may affect a relied-upon judgment.
- COPY `assets/pr-body-skeleton.md` when drafting a PR description; fill applicable sections with actual scope and evidence and remove unfilled placeholders.

## Expected output

Return the actual PR link or prepared title/body, submitted repository/head/base, validation and observed hosted CI standing, current blockers and next authorized action. Distinguish prepared, submitted, reused and blocked outcomes.
