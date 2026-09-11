---
name: pr
description: >
  Prepare a verified pull request from actual diff and evidence.
argument-hint: [branch, feature name, plan path, or PR request]
---

# Pull request preparation


## Review and Closeout application

When project authority explicitly adopts Review and Closeout policy, use the packaged application below for shared assessment meaning. It replaces source-local judgment, independence, applicability, concern-disposition and closeout rules in this skill and its conditional resources; retain specialist methods and contract-selected storage procedures. Historical assessments retain their original meaning but grant no current runtime support. Missing or contradictory required guidance stops dependent reliance.

## Explicit recording

Use this profile when the project has adopted the RigorLoop Record Format and explicitly selected the change. Read the project's governing documents. The Workflow model owns coordination, Review and Closeout owns assessment policy, Record Format owns stored shapes, and CLI owns construction and persistence. New stores use `rigorloop-records-v3`; existing `rigorloop-records-v2` stores retain reads, writes and recovery. Select the actual record contract; never mix versions within a store. Retired or unknown stored formats are rejected without fallback. Do not migrate or reinterpret historical records; preserve their bytes and meaning as archival evidence. The project need not contain RigorLoop's internal design repository.

Use the contract-selected recording procedures in this skill and its conditional resources. Dispatch primary results by schema_version (2 or 3), then status and operation; a schema-3 error alone does not establish v3 storage. Read scope and omissions before relying on selected content. Retain substantive stage duties, permissions, independent assessment and proof obligations. Historical records grant no current execution authority.

Use `rigorloop context --root PATH --change ID --input - --format json` with explicitly selected kinds/filters and full detail. Expand the selection when needed: omitted content is not evidence of absence. Copy `record_contract` and `revision` into the targeted request's `contract` and `expected_revision`. Use `rigorloop subject inspect --root PATH --path FILE --content full --format json` for the exact engineering basis and mechanical identities; supply relied-on subjects as `reads` with their expected identities.

Make your decision, then use the purpose-specific command's `--help` and submit its targeted operation on stdin. Use `batch` for related explicit updates. Supply semantic values and any required applicability; the CLI constructs registry entries, preserves neighbors and serializes records. Do not reconstruct complete files or invoke historical eligibility first. Preview is optional; normal writes validate. A save does not approve work, establish readiness or select the next actor. Conflict requires rereading and reassessment; busy/recovery-required is not a save. Use explicit `record-store recover` for interrupted storage. Missing or stale evidence prevents reliance, not recording a correction.

Read the final assessment with verify show and the relevant review/evidence/decision basis through selected context or show. Assess current applicability and exact subjects before relying on the report; saved or absent observations do not establish permission. Retain repository/remote/branch and explicit external-action authority checks, but do not require historical lifecycle receipts from this profile. Do not manufacture review or Verify results, mutate workflow decisions, or infer authority to merge or release.

## Purpose

Open one evidence-grounded pull request. `verify` owns `branch-ready`; this skill owns `pr-body-ready` and `pr-open-ready`. No downstream continuation.

## When to use

Use after `verify` or for a nearly ready direct PR request.

## When not to use

Do not implement, review, verify, settle lifecycle state, merge, release, or fabricate evidence.

## Project-local evidence

Public skills operate in customer-project mode by default. Use project-local artifacts and authoritative CLI workflow context when governed. Do not require RigorLoop repository-internal files. Use safe portable defaults without governed claims; block on ambiguity.

## Inputs to read

Resolve repository, remote, branches, evidence, handoff, diff, and matching PR; never use memory. For consolidated gates, consume verify-owned accepted Proposal evidence, approved Design Review ID and exact member map, and approved Delivery Review ID and exact member map. Never reconstruct or reperform those reviews. The exact successful Verify report owns explanation, basis, and authority. Reject missing, stale, new, or competing authoritative rationale. Historical rationale grants no current PR authority.

Any explicit change, workflow, owning-change, or governed pointer is a signal. governed signal: `no-governed-signal`, `single-governed-candidate`, or `invalid-or-ambiguous-governed-signal`. The first uses `PR0-portable`; the second loads `PR1-governed`; malformed, stale, conflicting, duplicated, unsafe, escaped, or ambiguous signals stop without portable fallback. Loading grants no authority.

## Closed classifications

Classify each independent axis exactly. Unknown values fail before consistency checks.

- submission intent: `open`, `draft`, `prepare-only`;
- refresh authority: `none`, `explicit-title-refresh`, `explicit-full-replacement`, `workflow-title-refresh`;
- state-transition authority: `none`, `publish-existing-draft`, `convert-existing-open-to-draft`;
- branch relation: `absent`, `same`, `remote-ancestor-of-local`, `local-ancestor-of-remote`, `diverged`, `ambiguous`;
- PR state: `absent`, `open`, `draft`, `closed`, `merged`, `ambiguous`;
- operation result: `opened`, `draft-opened`, `updated`, `reused`, `prepared-not-opened`, `blocked`;
- hosted-CI state: `passed`, `failed`, `pending`, `unavailable`, `unobserved`, `not-applicable`;
- evidence suffix: `none`, `evidence-only`, `invalidating`.

Explicit `pr` defaults to `open`; the other intents require current authority. `prepare-only` performs no push, PR creation, refresh, publication, draft conversion, or other external mutation and returns `prepared-not-opened` with `actual_external_mutation: none`. A blocker does not reclassify intent; report requested intent, actual operation, blocker, and actual mutation.

Submission intent does not grant refresh or PR-state transition authority. Default `open` preserves an existing draft. Explicit `draft` preserves an existing open PR. Publishing or conversion needs matching authority.

## Verification and local safety

Consume and revalidate verify-owned `verification_basis` from the v3 object or the explicitly authored normalized basis block retained for existing v2 reports: immutable `repository_identity`, `remote_identity`, `base_branch`, `base_revision`, `merge_base_revision`, `head_branch`, and `verified_subject_revision`. Do not reconstruct it from commands, names, Git state, or prose. Legacy, prose-only, command-only, missing, stale, unresolved, conflicting, or ambiguous evidence supports preparation only; it blocks opening and routes to verify.

Require the verified subject to equal or precede the local handoff; a non-ancestor blocks. Classify their cumulative final change as `none`, `evidence-only`, or `invalidating`. Evidence-only permits any commit count or direct-parent topology only for current attributable final-review, workflow, and Verify evidence. Path, file name, commit message, or author identity alone grants no authority. Protected, mixed, unknown, stale, cross-change, or unattributable content invalidates opening and routes to its owner for review and fresh Verify.

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

Inspect registered reviews, findings, owned dispositions and blockers. Required unresolved corrections or necessary owner decisions prevent reliance on closeout. A later substantive revision requires the appropriate independent reassessment; a resolution note alone cannot substitute for review. Summarize material dispositions without duplicating every finding.

Treat the plan and upstream artifacts as read-only.

## Handoff

- Normal next stage: open or reuse the PR when all three readiness gates pass.
- Conditional next stages: return through `route` to fresh verify, review resolution, implementation, or an owning artifact stage; stop on external or authority blockers.

## Stop conditions

Stop on unresolved target or authority, stale verification, unsafe branch relation, ambiguous PR state, unrelated changes, missing required evidence or resources, open review closeout, failed required validation, or unconfirmed external read-back.

## Claims this skill must not make

Do not claim implementation passed, review passed, tests passed, verification passed, CI passed, generated currency, branch readiness, or lifecycle completion without current owning evidence. This skill must not mutate `change.json`, workflow, artifact, plan, review, merge, release, or publication state.

Progress means work that has happened so far. Readiness means the next stage that can happen. Closeout means the current artifact or stage satisfied its checklist. Done means final lifecycle state after required gates are complete. Readiness is not Done.

## Required-resource safety

A missing, unreadable, escaped, stale, transformed, or mixed-version governed reference must stop before governed readiness judgment. A missing or invalid body asset must stop before body generation and external mutation. The skill must not reconstruct, recall, or partially invent required resource content.

## Resource map

- READ `references/review-reliance.md` when applying adopted assessment applicability, correction or closeout policy.

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

Then provide readiness, mutation, PR and CI state, content, risks, reviewer focus, and evidence.
