---
name: pr
description: >
  Prepare a completed, verified change for pull request review. Use when the branch is ready or nearly ready and the agent should summarize the real diff, validation evidence, spec compliance, risks, and reviewer notes.
argument-hint: [branch, feature name, plan path, or PR request]
---

# Pull request preparation

## Purpose

Prepare and, when readiness passes, open one pull request grounded in the actual diff and current evidence. `verify` owns `branch-ready`; this skill owns `pr-body-ready` and `pr-open-ready` and has no downstream continuation.

## When to use

Use after `verify` establishes branch readiness, or for a nearly ready direct PR request.

## When not to use

Do not implement, review, verify, settle lifecycle state, merge, release, or fabricate evidence.

## Project-local evidence

Public skills operate in customer-project mode by default. Use project-local artifacts when present, including `docs/workflows.md`. Do not require RigorLoop repository-internal specs, docs, reports, or governance files. Use portable defaults where safe and block on ambiguity.

## Inputs to read

Resolve the repository, remote, base and head, verification evidence, handoff revision, working tree, diff, and matching PR. Read applicable evidence; never summarize from memory.

Classify a governed signal before readiness work:

- `no-governed-signal`: no explicit change ID, workflow-managed change identity, structured owning-change field, or active governed pointer exists;
- `single-governed-candidate`: exactly one signal resolves safely;
- `invalid-or-ambiguous-governed-signal`: a signal is malformed, stale, conflicting, duplicated, unsafe, escaped, or ambiguous.

Any explicit or structured signal counts even when invalid. Only `no-governed-signal` uses `PR0-portable`. A single candidate uses `PR1-governed` and loads the governed reference; invalid or ambiguous signals stop without portable fallback. Loading never grants mutation authority.

## Closed classifications

Classify each independent axis exactly. Unknown values fail before consistency checks.

- submission intent: `open`, `draft`, `prepare-only`;
- refresh authority: `none`, `explicit-title-refresh`, `explicit-full-replacement`, `workflow-title-refresh`;
- state-transition authority: `none`, `publish-existing-draft`, `convert-existing-open-to-draft`;
- branch relation: `absent`, `same`, `remote-ancestor-of-local`, `local-ancestor-of-remote`, `diverged`, `ambiguous`;
- PR state: `absent`, `open`, `draft`, `closed`, `merged`, `ambiguous`;
- operation result: `opened`, `draft-opened`, `updated`, `reused`, `prepared-not-opened`, `blocked`;
- hosted-CI state: `passed`, `failed`, `pending`, `unavailable`, `unobserved`, `not-applicable`.

Explicit `pr` defaults to `open`; `draft` and `prepare-only` require explicit current authority. `prepare-only` permits bounded inspection and content construction but performs no push, PR creation, refresh, publication, draft conversion, or other external mutation. It returns `prepared-not-opened` and `actual_external_mutation: none`. A blocker never silently converts requested `open` or `draft` into successful preparation; report requested intent, actual operation, blocker, and actual mutation separately.

Submission intent does not grant refresh or PR-state transition authority. Default `open` preserves an existing draft. Explicit `draft` preserves an existing open PR. Publishing or converting an existing PR requires the matching separate authority for that exact PR.

## Verification and local safety

Consume one verify-owned `verification_basis` containing immutable `repository_identity`, `remote_identity`, `base_branch`, `base_revision`, `merge_base_revision`, `head_branch`, and `verified_subject_revision`. Revalidate it; do not reconstruct it from commands, unresolved names, current Git state, arbitrary prose, or historical conventions. Legacy, prose-only, command-only, missing, stale, unresolved, conflicting, or ambiguous evidence may support truthful preparation, but blocks `open`, `draft`, and `pr-open-ready` and routes to fresh verification.

The verified subject equals the handoff revision unless exactly one direct-child verify-owned evidence commit intervenes. It may change only final verify evidence and matching verify-owned change-record or state-sync fields. Any other-owner, product, test, governing artifact, dependency, configuration, generated, multi-commit, or non-direct-child change invalidates opening readiness.

Before mutation, require scoped commits, an acceptable tree and diff, no secret or debug-only inclusion, intentional generated files and migrations, and every operation identity.

## Remote safety and PR selection

`remote-ancestor-of-local` means the remote head is a strict ancestor of the local handoff revision and permits only a normal fast-forward push after baseline reread. `local-ancestor-of-remote` means remote contains work absent locally and blocks. `absent` may create the branch, `same` performs no push, and `diverged` or `ambiguous` stops. The skill must not force-push, delete, overwrite, rewrite, or implicitly replace a remote branch.

Resolve PR state for the exact repository, host, head, and base. An absent PR may be created once. Adequate open or draft PRs are reused without mutation. Closed, merged, multiple, mismatched, or ambiguous PR state stops without reopening or duplicate creation. Retry must reconcile observed state and never create a duplicate matching PR.

Refresh supports title replacement or explicitly authorized whole-body replacement. It must not parse or mutate Markdown sections, add hidden managed markers, or infer body ownership. Existing body bytes remain unchanged without current full-replacement authority.

## Hosted CI

`passed` requires current hosted evidence for the exact handoff revision at the PR head. Route required `failed` checks to their owner. `pending`, `unavailable`, and `unobserved` must never be described as passed; they permit initial opening only when current policy allows post-open CI. `not-applicable` requires current evidence. Local validation is not hosted CI.

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

Compose from the body asset. Include its core group; include governed and impact groups when applicable. Procedure owns applicability and adequacy. Unresolved required data blocks, and no placeholder may remain.

## Outputs

Every result reports requested intent, actual operation, actual external mutation or none, actual PR state or none, `pr-body-ready`, `pr-open-ready`, hosted-CI state, blockers, claim limitations, and the exact URL only after read-back.

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
