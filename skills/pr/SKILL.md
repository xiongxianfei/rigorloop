---
name: pr
description: >
  Prepare a completed, verified change for pull request review. Use when the branch is ready or nearly ready and the agent should summarize the real diff, validation evidence, spec compliance, risks, and reviewer notes.
argument-hint: [branch, feature name, plan path, or PR request]
---

# Pull request preparation

## Purpose

Open one evidence-grounded pull request when ready. `verify` owns `branch-ready`; this skill owns `pr-body-ready` and `pr-open-ready` and has no downstream continuation.

## When to use

Use after `verify`, or for a nearly ready direct PR request.

## When not to use

Do not implement, review, verify, settle lifecycle state, merge, release, or fabricate evidence.

## Project-local evidence

Public skills operate in customer-project mode by default. Use project-local artifacts when present, including `docs/workflows.md`. Do not require RigorLoop repository-internal specs, docs, reports, or governance files. Use portable defaults where safe and block on ambiguity.

## Inputs to read

Resolve repository, remote, branches, verification evidence, handoff, tree, diff, and matching PR. Never summarize from memory.

An explicit change ID, workflow change identity, owning-change field, or governed pointer is a signal even when invalid. governed signal: `no-governed-signal`, `single-governed-candidate`, or `invalid-or-ambiguous-governed-signal`. Only the first uses `PR0-portable`; the second loads `PR1-governed`; malformed, stale, conflicting, duplicated, unsafe, escaped, or ambiguous signals stop without portable fallback. Loading grants no authority.

## Closed classifications

Classify each independent axis exactly. Unknown values fail before consistency checks.

- submission intent: `open`, `draft`, `prepare-only`;
- refresh authority: `none`, `explicit-title-refresh`, `explicit-full-replacement`, `workflow-title-refresh`;
- state-transition authority: `none`, `publish-existing-draft`, `convert-existing-open-to-draft`;
- branch relation: `absent`, `same`, `remote-ancestor-of-local`, `local-ancestor-of-remote`, `diverged`, `ambiguous`;
- PR state: `absent`, `open`, `draft`, `closed`, `merged`, `ambiguous`;
- operation result: `opened`, `draft-opened`, `updated`, `reused`, `prepared-not-opened`, `blocked`;
- hosted-CI state: `passed`, `failed`, `pending`, `unavailable`, `unobserved`, `not-applicable`.

Explicit `pr` defaults to `open`; the other intents require current authority. `prepare-only` performs no push, PR creation, refresh, publication, draft conversion, or other external mutation and returns `prepared-not-opened` with `actual_external_mutation: none`. A blocker does not reclassify intent; report requested intent, actual operation, blocker, and actual mutation.

Submission intent does not grant refresh or PR-state transition authority. Default `open` preserves an existing draft. Explicit `draft` preserves an existing open PR. Publishing or conversion needs matching authority.

## Verification and local safety

Consume and revalidate verify-owned `verification_basis`: immutable `repository_identity`, `remote_identity`, `base_branch`, `base_revision`, `merge_base_revision`, `head_branch`, and `verified_subject_revision`. Do not reconstruct it from commands, names, Git state, or prose. Legacy, prose-only, command-only, missing, stale, unresolved, conflicting, or ambiguous evidence supports preparation only; it blocks opening and routes to verify.

Subject equals handoff unless exactly one direct-child verify-owned evidence commit changes only final verify evidence and matching verify-owned change-record or state-sync fields. Any other change invalidates opening readiness.

Before mutation, require scoped commits, safe tree and diff, no secrets or debug residue, intentional generated files and migrations, and every operation identity.

## Remote safety and PR selection

`remote-ancestor-of-local` means remote is a strict ancestor of the local handoff revision and permits normal fast-forward push after reread. `local-ancestor-of-remote` means remote contains work absent locally and blocks. `absent` may create; `same` does not push; `diverged` or `ambiguous` stops. The skill must not force-push, delete, overwrite, rewrite, or replace remote.

Resolve PR state for exact repository, host, head, and base. Create absent once; reuse adequate open or draft unchanged. Closed, merged, multiple, mismatched, or ambiguous state stops. Retry reconciles state and must never create a duplicate matching PR.

Refresh supports title replacement or explicitly authorized whole-body replacement. It must not parse or mutate Markdown sections, add hidden managed markers, or infer ownership. Existing body bytes remain unchanged without full-replacement authority.

## Hosted CI

`passed` requires current hosted evidence for the exact handoff revision at the PR head. Route `failed` to its owner. `pending`, `unavailable`, and `unobserved` must never be described as passed and open only under current policy. `not-applicable` needs evidence. Local validation is not hosted CI.

## External operation

1. Resolve all local identities, evidence, content, states, and independent authorities.
2. Immediately before push, require the current remote base to equal the verified base and the observed remote-head baseline to match its classified relation.
3. Push only when the intent and relation permit it.
4. After push and before PR mutation, reread remote head, remote base, and matching PR state; require head equal to handoff and base equal to verified base.
5. Immediately before PR mutation, reread exact PR identity, head, base, title, body identity, and draft state; reclassify any concurrent change.
6. Create, reuse, refresh, or transition only within current independent authority.
7. After creation, reuse, refresh, or transition, read back URL, number, state, head, base branch, current base identity, title, and body identity.

Report a successful external write truthfully after later identity drift, but set `pr-open-ready: false` and require fresh verification or the approved base-update route. External success and readiness are separate.

## Body, result, and claims

Compose the asset's core plus applicable governed and impact groups. Procedure owns applicability and adequacy; unresolved data or placeholders block.

## Outputs

Report requested intent, operation, actual external mutation, actual PR state, readiness booleans, hosted-CI state, blockers, claim limitations, and post-read-back URL.

## Review closeout

Inspect `review-log.md`. `Closeout status: open`, `needs-decision`, or open findings block handoff; `Closeout status: closed` requires final dispositions and evidence. A stage-owned non-approval outcome requires a same-stage later review round or explicit reviewer or owner closeout; `review-resolution.md` alone is not a silent substitute. For no-material detailed records need `review-log.md` but not an empty `review-resolution.md`.

Treat the plan and upstream artifacts as read-only.

## Handoff

- Normal next stage: open or reuse the PR when all three readiness gates pass.
- Conditional next stages: return through workflow to fresh verify, review resolution, implementation, or an owning artifact stage; stop on external or authority blockers.

## Stop conditions

Stop on unresolved target or authority, stale verification, unsafe branch relation, ambiguous PR state, unrelated changes, missing required evidence or resources, open review closeout, failed required validation, or unconfirmed external read-back.

## Claims this skill must not make

Do not claim implementation passed, review passed, tests passed, verification passed, CI passed, generated currency, branch readiness, or lifecycle completion without current owning evidence. This skill must not mutate `change.yaml`, workflow routing, artifact settlement, plan state, review state, merge state, release state, or publication state.

Progress means work that has happened so far. Readiness means the next stage that can happen. Closeout means the current artifact or stage satisfied its checklist. Done means final lifecycle state after required gates are complete. Readiness is not Done.

## Required-resource safety

A missing, unreadable, escaped, stale, transformed, or mixed-version governed reference must stop before governed readiness judgment. A missing or invalid body asset must stop before body generation and external mutation. The skill must not reconstruct, recall, or partially invent required resource content.

## Resource map

- READ `references/governed-pr-readiness.md` once for `PR1-governed` after candidate classification and before governed judgment.
- COPY `assets/pr-body-skeleton.md` once when body applicability is known and before any external mutation.

## Evidence collection efficiency

Use bounded evidence before broad reads or raw excerpts.
Use summary and stable-ID first reasoning before broad reads or raw excerpts.
Prefer check IDs, requirement IDs, test IDs, file paths, counts, line citations, matching line numbers, diffs, and targeted excerpts when inspecting large files, generated output, validation logs, or repeated scans.
Output caps are safety rails, not evidence-selection strategy.
Validation summaries must not change selected check coverage, command exit behavior, failure detection, or required validation evidence.
Read exact ranges after locating relevant lines, then expand only when the narrower evidence is insufficient.

## When full-file read is required

Read the full file when the whole file is the review target, the relevant section cannot be isolated safely, surrounding context can change the conclusion, bounded searches disagree or produce incomplete evidence, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Expected output

Start with:

```md
## Result

- Skill: pr
- Status: <completed | blocked>
- Artifacts changed: <external PR or none>
- Open blockers: <blockers or none>
- Next stage: <human review | owning stage | none>
```

Then provide the operation result, readiness booleans, hosted-CI state, actual mutation, actual PR state, URL or limitation, readiness checks, title, composed body, risks, reviewer focus, and exact observed validation and CI evidence.
