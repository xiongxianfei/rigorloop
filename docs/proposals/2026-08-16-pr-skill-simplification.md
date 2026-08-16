# PR Skill Simplification

## Owning change record

This proposal is governed by `docs/changes/2026-08-16-pr-skill-simplification/change.yaml`.

## Problem

The current `pr` skill is a flat 1,678-word, 11,375-byte file that combines universal branch and remote checks, RigorLoop-specific lifecycle aggregation, PR-body structure, hosted-CI interpretation, submission behavior, evidence-reading guidance, claim boundaries, and repeated output labels. Every invocation therefore loads governed change-pack procedure and a full inline body template even when a portable repository needs only a verified diff, a concise body, and one pull-request operation.

The flat shape also leaves several execution outcomes implicit. It does not close how to handle an existing open or draft PR, how retries avoid duplicate PRs, how a pushed head is rebound to verification evidence, or how known failed, pending, unavailable, and unobserved hosted CI affect PR-opening claims. Those gaps are safety and idempotency concerns, not merely editorial opportunities.

## Goals

- Reduce the universal and governed procedural context loaded by `pr` while preserving evidence truthfulness, branch and remote safety, submission behavior, and claim ownership.
- Keep universal target resolution, exact verified-subject and handoff-revision binding, working-tree and push safety, remote branch and PR classification, submission authority, hosted-CI truthfulness, stops, claims, and concise result behavior inline.
- Move governed lifecycle aggregation into one conditional reference with no lifecycle mutation, settlement, or routing authority.
- Move repeated PR-body headings, ordering, and placeholders into one structural asset without moving readiness or claim policy into the asset.
- Make prepare, create, explicitly authorized host-field or whole-body refresh, reuse, state transition, and retry behavior deterministic for the exact repository, verified base/head pair, handoff revision, remote branch, and PR identity.
- Extend the existing `verify` result and governed verify-report evidence with one normalized verification-basis block that `pr` consumes without taking ownership of `branch-ready`.
- Preserve portable customer-project behavior and canonical-through-installed package integrity.
- Prove simplification with change-local semantic and literal inventories, static scenarios, real loaded-profile measurements, and repository-owned validation.

## Non-goals

- Do not change `verify` ownership of `branch-ready`, `workflow` ownership of lifecycle routing, or `pr` ownership of `pr-body-ready` and `pr-open-ready`.
- Do not add automatic merge, approval, release, publication, deployment, reviewer assignment, label management, or post-PR lifecycle continuation.
- Do not add a provider-specific orchestration engine, new CLI, new dependency, new validator family, or persistent PR transaction schema.
- Do not make `pr` edit `change.yaml`, settle artifacts or milestones, rewrite plans, or mark lifecycle completion after opening or merge.
- Do not require hosted CI to pass before a new PR may open when current repository policy permits CI to begin after opening.
- Do not execute Codex, Claude Code, opencode, or another target-agent runtime as acceptance proof.
- Do not redesign the GitHub, GitLab, or other host APIs used by available tooling.
- Do not add Markdown section mutation, managed-body markers, content-provenance parsing, or a PR-body ownership protocol.
- Do not otherwise optimize or restructure `verify`; only its directly coupled result/report contract, fixtures, and package projections needed for exact PR base/head binding are in scope.
- Do not optimize unrelated skills or hand-edit generated adapter implementation in this change.

## Vision fit

fits the current vision

The change strengthens the traceable idea-to-PR chain while reducing ceremony on the common path. Reviewers still receive the governing artifacts, evidence, risks, and unresolved external status they need, while customer projects avoid RigorLoop-specific lifecycle procedure unless governed evidence actually activates it.

## Context

`pr` is the terminal submit/open stage of the normal workflow. A direct invocation still opens a PR when readiness passes, but it has no downstream stage. The current contract already distinguishes local validation from hosted CI, requires actual-diff evidence, and prohibits lifecycle settlement. This proposal preserves those boundaries and reorganizes procedure around evidence-based activation.

The existing published-skill package architecture supports canonical `SKILL.md`, mapped `references/`, mapped `assets/`, generated archives, release-candidate packages, and clean-installed parity. The proposal uses that model without adding runtime or persistence architecture.

Current verify evidence does not guarantee one normalized exact PR basis. Historical reports variously cite branch names, commands, merge bases, stacked bases, or prose. The new PR rule therefore requires a directly coupled amendment to the existing verify-owned result and report contract; `pr` must not reconstruct a past verification basis from those incidental forms.

## Options Considered

### Option 0: Keep the flat skill

This avoids migration risk but preserves a large common path, inline structural duplication, and ambiguous existing-PR and retry behavior.

### Option 1: Compress the current file editorially

Editorial compression could remove repeated wording but would keep portable and governed procedure interleaved and leave the PR-body template as a second policy-bearing region inside the common file.

### Option 2: Extract only the PR-body skeleton

An asset-only change would establish structural ownership but would not remove governed change-pack inspection, review closeout, lifecycle evidence, or external-completion handling from portable invocations.

### Option 3: Add one governed-readiness reference and one PR-body asset

This option keeps universal submission safety inline, moves governed lifecycle aggregation behind one real trigger, and gives repeated body layout one structural owner. It also closes remote-branch state, remote-PR state, verified-subject and handoff binding, refresh authority, retry, and hosted-CI behavior in the universal contract.

### Option 4: Split references by lifecycle, CI, provider, remote operation, and release behavior

This would create several narrow resources with overlapping triggers. Most PR invocations need remote operation and CI truthfulness together, while governed lifecycle evidence has one clear independent activation boundary. The additional navigation would not be proportionate.

### Option 5: Replace prose orchestration with an executable PR engine

An engine could centralize host calls, but it would introduce provider coupling, runtime behavior, error-handling architecture, and a new acceptance surface for a change whose main problem is package ownership and progressive disclosure.

## Recommended Direction

Choose Option 3.

The published package becomes:

```text
skills/pr/
├── SKILL.md
├── references/
│   └── governed-pr-readiness.md
└── assets/
    └── pr-body-skeleton.md
```

### Universal `SKILL.md` ownership

Keep these obligations inline for every invocation:

- purpose, submit/open default, explicit draft or prepare-only exceptions, intent-specific side effects, and external-action authority;
- exact repository, remote, verified base/head pair, optional verify-owned evidence tail, handoff revision, pushed commit, and matching PR resolution;
- current `verify` evidence and exact verified-subject binding without invalidation by its own closed durable-recording commit;
- actual diff, working-tree, commit-scope, secrets, generated-output, migration, and reviewer-context checks;
- remote branch-state and PR-state classification, explicit refresh authority, and idempotent operation selection;
- hosted-CI state meanings and claim limitations;
- concise title and PR-body adequacy rules;
- push-before-open sequence, remote reread, create or refresh result, and read-back confirmation;
- universal stops, no-lifecycle-mutation boundary, output result, and no downstream continuation.

The universal file must not embed the complete PR-body section layout or detailed RigorLoop change-pack closeout procedure.

### Existing verify-evidence contract amendment

`verify` remains the sole owner of `branch-ready`. This slice amends its existing branch-readiness and workflow-final-verification result contract to emit one normalized verification basis:

```yaml
verification_basis:
  repository_identity: <canonical repository identity>
  remote_identity: <canonical remote identity>
  base_branch: <exact base branch>
  base_revision: <resolved base commit identity>
  merge_base_revision: <resolved merge-base identity>
  head_branch: <exact head branch>
  verified_subject_revision: <resolved verified subject identity>
```

The basis is part of the current `verify` invocation result in portable use and the existing `verify-report.md` in governed or explicitly durable use. It creates no new artifact, lifecycle state, persistence mechanism, schema owner, or routing authority. `verify` resolves every branch name to an immutable identity before reporting `branch-ready`; `pr` only consumes and revalidates the recorded tuple.

The directly coupled same-slice surfaces are the `verify` output contract, its existing branch-readiness reference when needed, the workflow or skill contract that defines the result, deterministic fixtures, semantic and literal preservation ledgers, and generated package projections. The amendment must not move PR opening, body preparation, hosted-CI interpretation, or `pr-open-ready` into `verify`.

Compatibility is fail-closed:

| Verification evidence | PR behavior |
| --- | --- |
| Complete current normalized basis | Continue to current remote revalidation. |
| Missing, stale, prose-only, command-only, unresolved-name, conflicting, or ambiguous basis | Permit truthful `prepare-only` content construction; block `open`, `draft`, and `pr-open-ready`; route to fresh branch-readiness or final verification. |
| Complete basis whose repository, remote, base, merge base, head, or subject differs | Block opening and route to fresh verification or the repository's approved base-update procedure. |

`pr` must not infer the verified basis from a command containing `--base`, an unresolved branch name, current Git state, arbitrary prose, or historical report conventions. Fresh verification is the compatibility path for old evidence.

### `governed-pr-readiness.md` ownership

Load the reference only after one exact governed change candidate resolves from an explicit change ID, workflow-managed same-change authority, a current verify report containing a structured owning-change identity, or another structured owning-change pointer. Any governed signal counts even when malformed. Classification is exactly:

```text
no-governed-signal
single-governed-candidate
invalid-or-ambiguous-governed-signal
```

Only `no-governed-signal` permits portable handling. A single candidate loads the reference and validates authority. Invalid, stale, conflicting, escaped, duplicated, or ambiguous signals stop without portable fallback.

The reference owns:

- bounded `change.yaml` and plan-state inspection;
- required change-pack and durable-rationale presence;
- closed implementation milestones and final review identity;
- review-log and review-resolution closeout;
- explain-change and verify-report currency;
- passing state-sync evidence for touched, referenced, active, and blocked workflow-state artifacts;
- external-completion-event treatment;
- generated-output, migration, release-sensitive, and governed risk evidence when applicable;
- governed blockers and their owning return stages.

Loading the reference grants no permission to mutate lifecycle state, settle artifacts, rewrite plans, change routing, create follow-up state, or claim completion.

### `pr-body-skeleton.md` ownership

The asset owns labels, ordering, placeholders, and repeated table shapes only. It contains these closed groups:

#### Core group

```text
Summary
Why
What changed
Tests and verification
Risks and rollback
Reviewer notes
Follow-ups
```

#### Governed traceability group

```text
Spec / plan / architecture
Requirement coverage
Review resolution summary
Lifecycle and verification evidence
```

#### Conditional impact group

```text
Migration
Security and privacy
Release or operational impact
```

The skill procedure selects groups. Inapplicable groups are omitted. Applicable groups with unavailable required data show an explicit blocker. Unfilled placeholders are forbidden. The asset does not determine readiness, CI status, requirement coverage, review closeout, submission authority, or whether a group applies.

### Invocation and operation model

Resolve one submission intent:

```text
open
draft
prepare-only
```

`open` is the default for an explicit `pr` invocation. `draft` or `prepare-only` requires an explicit user instruction or repository contract. A blocker or tooling limitation does not reclassify `open` or `draft` as successful `prepare-only`; the result preserves requested intent and reports the actual blocked operation separately.

`prepare-only` is externally read-only. It may inspect local evidence, inspect available remote evidence, construct title and body, and predict the operation, but it must not push, create or refresh a PR, publish a draft, convert an open PR to draft, or perform another external mutation. It returns `prepared-not-opened` with `actual_external_mutation: none`.

Resolve refresh authority independently:

```text
none
explicit-title-refresh
explicit-full-replacement
workflow-title-refresh
```

`explicit-title-refresh` and `explicit-full-replacement` require a current user instruction naming the existing PR and permitted replacement scope. `workflow-title-refresh` requires same-change workflow authority naming title refresh. Ordinary `pr` invocation, matching PR identity, stale generated content, or loaded governed procedure does not itself authorize replacement. Unknown, conflicting, or ambiguous refresh authority stops before content mutation.

The first version refreshes only the host-native title field or the entire body. It performs no Markdown section mutation. Existing body bytes are preserved unless `explicit-full-replacement` authorizes replacing the entire body. A future managed-section capability requires a separate approved ownership, parsing, compatibility, and architecture contract.

Resolve existing PR state-transition authority independently:

```text
none
publish-existing-draft
convert-existing-open-to-draft
```

Both non-`none` values require a current explicit user instruction naming the exact existing PR and requested state transition. Submission intent does not imply this authority. Default `open` preserves an existing draft, and explicit `draft` preserves an existing open PR unless the corresponding separate authority is present. Content refresh and PR-state transition are independent operations.

Use this intent side-effect matrix:

| Submission intent | Remote push | Create absent PR | Refresh existing content | Change existing draft/open state |
| --- | --- | --- | --- | --- |
| `prepare-only` | forbidden | forbidden | forbidden | forbidden |
| `open` | allowed when safe | create non-draft | only with matching refresh authority | only with `publish-existing-draft` |
| `draft` | allowed when safe | create draft | only with matching refresh authority | only with `convert-existing-open-to-draft` |

Resolve one remote branch state for the exact repository, remote, and head branch:

```text
absent
same
remote-ancestor-of-local
local-ancestor-of-remote
diverged
ambiguous
```

`remote-ancestor-of-local` means the remote head is a strict ancestor of the local handoff revision and permits only a normal non-force fast-forward push after the expected remote baseline is revalidated. `local-ancestor-of-remote` means the local handoff revision is a strict ancestor of the remote head and stops because remote work is absent locally. `absent` permits branch creation, `same` requires no push, and `diverged` or `ambiguous` stops. The skill never force-pushes, deletes, rewrites, or implicitly replaces a remote branch.

Resolve one remote PR state for the exact repository, head, base, and host:

```text
absent
open
draft
closed
merged
ambiguous
```

Use this closed PR operation matrix after safe remote-head confirmation and a fresh matching-PR read:

| Remote PR state | Content and authority state | Operation and result |
| --- | --- | --- |
| `absent` | intended content complete | `create-primary-pr`; create once, read back identity, and report `opened` or `draft-opened`. |
| `open` or `draft` | current title and body already adequate | `reuse-existing-pr`; preserve PR identity and state, perform no content mutation, and report `reused`. |
| `open` or `draft` | title differs and current title-refresh authority covers it | `refresh-primary-pr`; reread current content, replace only the title, preserve the body byte-for-byte and preserve PR identity, then report `updated` after read-back. |
| `open` or `draft` | body differs and explicit full-replacement authority is current | `refresh-primary-pr`; replace the entire authorized body and optionally the title only when separately named, preserve PR identity, and report `updated` after read-back. |
| `open` or `draft` | stale content but refresh authority is absent, insufficient, conflicting, or ambiguous | Stop; report the exact authority or ownership blocker without mutation. |
| `closed` | any | Stop; require an explicit reopen or new-branch decision. |
| `merged` | any | Stop; do not treat merge as lifecycle completion or create another PR implicitly. |
| `ambiguous` | any | Stop before push or PR mutation. |

Draft/open state is preserved unless separate explicit state-transition authority changes it. The refresh model introduces no hidden markers, section parser, or managed-section protocol. A stale body without explicit full-replacement authority blocks `pr-body-ready` but remains byte-for-byte unchanged.

Multiple matching PRs, mismatched base, mismatched repository, unsafe branch, unavailable remote identity, or conflicting host evidence are `ambiguous`. If another actor creates the exact matching PR after preflight, the mandatory post-push reread selects `reuse-existing-pr` or an authorized refresh rather than duplicate creation. Retry reuses the same remote PR identity and must never create a duplicate for the same head/base operation.

### Exact verified-revision sequence

The operation binds:

```text
repository identity
remote identity
verified base branch
verified base revision
verified merge-base identity when the verification contract uses one
verified head branch
local head revision
verify report identity
verified subject revision
verify-owned evidence-tail identity or none
handoff revision
intended title and body identity
matching PR identity when present
```

Require this sequence:

1. Resolve the current local target, working tree, governing evidence, and intended PR content.
2. Resolve the verify report's exact repository, remote, base branch, base revision, optional verified merge base, head branch, and `verified_subject_revision`. Require the verified subject to be an ancestor of or equal to the local handoff revision.
3. When the local head differs, require exactly one direct-child verify-owned evidence commit. Its diff may contain only the final verify report and the matching owning change record or explicitly required verify-owned state-sync evidence. The change-record diff may update only final verification evidence and verify-owned readiness or routing fields. Any product, test, specification, architecture, plan, dependency, configuration, generated-output, unrelated documentation, or other lifecycle-owner change makes verification stale.
4. Validate the allowed tail paths, parent relationship, content identities, and change-record field boundary. The local head becomes the exact `handoff_revision`; no in-memory or self-referential handoff hash is required inside its own commit.
5. Read the current remote base revision, directional remote branch relation, and matching PR state when those read-only surfaces are available. Classify missing evidence explicitly rather than treating it as current.
6. If intent is `prepare-only`, return the prepared content, predicted operation, observed external state, evidence limits, and readiness result without performing any external mutation. `pr-open-ready` cannot be true when required current remote evidence is unavailable or mismatched.
7. For `open` or `draft`, require the current remote base revision to equal the verified base revision. When the verification contract records a merge base, also require the current head/base relationship to satisfy that exact verified merge-base contract. Stop for closed, merged, unsafe, `local-ancestor-of-remote`, diverged, or ambiguous state.
8. Create an absent remote branch or normally fast-forward `remote-ancestor-of-local` to the exact handoff revision. Never use a force, delete, overwrite, or implicit branch-replacement operation.
9. Re-read both the remote head and remote base. Require the remote head to equal the handoff revision and the remote base to remain equal to the verified base revision before PR mutation.
10. Re-read the matching PR state, head, base, title, body, and draft status immediately before PR mutation. Reclassify the operation when concurrent state changed; never use the stale pre-push PR classification.
11. Create, reuse, explicitly refresh, or explicitly transition exactly one matching PR within current independent authorities.
12. Read back the PR URL, number, state, head, base branch, current remote base revision, title, and body identity. Require the PR head to equal the handoff revision and the base to remain on the verified branch and revision before claiming `pr-open-ready`.

Failure before confirmed read-back reports the exact operation failure and must not claim that a PR opened or updated. A retry reconciles the remote state rather than blindly repeating create.

External-operation truth and readiness are separate. If push, creation, refresh, or state transition succeeds but the base or another readiness identity changes before final read-back, report the successful external operation and resulting PR state truthfully, set `pr-open-ready: false`, and require fresh verification or the repository's explicit base-update procedure.

The allowed verify-owned evidence tail is a narrow compatibility rule for durable final-verification recording, not general post-verify mutability. If the repository's verification contract requires more than one post-validation commit or broader paths, the proposal must return to review rather than silently broadening the exception.

### Hosted-CI semantics

Use exactly:

```text
passed
failed
pending
unavailable
unobserved
not-applicable
```

`passed` requires current hosted evidence for the exact handoff revision at the PR head. `failed` blocks a clean handoff when the failing check is required and routes to the owning correction or CI stage. `pending` permits initial opening only when current repository and verify evidence permit CI to begin after opening, and the PR body must say pending. `unavailable` and `unobserved` may permit opening only when hosted CI is not a pre-open prerequisite; neither may be described as passed. `not-applicable` requires current evidence that no hosted check applies.

An already-open PR with a current required failure remains externally open, but `pr` performs no content mutation under a clean-ready claim and reports the existing URL plus the blocker. Opening authority does not convert failing CI into readiness.

### Readiness and result model

`verify` remains the sole owner of `branch-ready`. `pr` consumes that exact evidence and owns only:

```text
pr-body-ready
pr-open-ready
```

Use one operation result:

```text
opened
draft-opened
updated
reused
prepared-not-opened
blocked
```

The result must distinguish local validation from hosted CI and report the exact PR URL only after confirmed creation or reuse. It must not imply workflow completion, merge readiness, release readiness, or publication.

Every result reports separately:

```text
requested submission intent
actual external operation
actual external mutation or none
actual PR state or none
pr-body-ready
pr-open-ready
hosted CI state
blockers and claim limitations
```

### Resource failure behavior

A missing, unreadable, escaped, contradictory, stale, transformed, or mixed-version triggered reference stops governed readiness judgment. A missing or invalid skeleton stops PR-body generation and external submission. The common file must not reconstruct missing conditional procedure or layout from memory.

## Expected Behavior Changes

- Portable PR invocations no longer load detailed RigorLoop change-pack and lifecycle-closeout procedure.
- Governed invocations load one reference after a tri-state governed-signal classification and remain unable to mutate lifecycle state.
- PR bodies use one structural owner with closed optional groups instead of an inline full template.
- Existing open and draft PRs are reused without mutation when adequate and refreshed only under explicit field or full-replacement authority.
- `prepare-only` performs no external mutation, and submission intent never implies publication or draft conversion authority for an existing PR.
- The verified subject may differ from the handoff revision only by one validated verify-owned durable-evidence commit; the pushed remote head and PR head must equal the handoff revision.
- Verification binds the exact remote base/head pair; remote branch relations use directional ancestry names, and matching base and PR state are reread after push.
- First-version refresh changes only the title or an explicitly authorized whole body; it never parses or mutates Markdown sections.
- Hosted CI states become closed, current-head-bound, and truthfully reported.
- Missing required resources and ambiguous remote or governed state fail closed.

## Architecture Impact

A bounded architecture assessment is required because the change introduces mapped skill resources and clarifies an external-operation transaction. The expected result is `architecture-not-required` when current architecture already supports packaged references and assets, the normalized tuple fits the existing verify result and verify-report evidence surfaces, and the operation uses existing Git and host tooling without a new persistent record, service, schema, state owner, or provider abstraction.

Architecture becomes required if specification or implementation needs a new durable PR transaction artifact, provider-neutral runtime layer, lifecycle mutation owner, remote-state schema, cross-process recovery service, managed-section parser, body-ownership protocol, or new base/head evidence owner.

## Testing and Verification Strategy

### Change-local preservation evidence

Before editing canonical skill content, create:

- a semantic-rule disposition ledger with one owner and disposition for every current behaviorally significant rule and duplicate cluster;
- a literal-compatibility ledger for headings, readiness labels, status values, resource paths, output fields, and exact phrases consumed by tests or packages;
- a directly coupled verify-evidence ledger classifying current branch, base, merge-base, repository, remote, and subject representations and their migration to the normalized basis;
- deterministic baseline measurements for `SKILL.md`, each planned reference or asset, portable and governed procedural profiles, representative body composition, and total package;
- static scenario fixtures for every operation, remote state, submission intent, CI state, resource failure, retry, and forbidden mutation.

### Deterministic proof

Prove at least:

- exact `READ` and `COPY` mappings, path containment, triggers, and one-load behavior;
- tri-state governed-signal classification and no invalid-signal portable fallback;
- exact verified-subject, handoff, remote-head, and PR-head binding;
- normalized portable verify-result and governed verify-report basis emission under the existing `verify` owner;
- complete, missing, stale, prose-only, command-only, unresolved-name, conflicting, and ambiguous verification-basis compatibility behavior;
- same-revision and one-commit verify-owned evidence-tail binding, including every forbidden post-verify path and field class;
- absent, same, remote-ancestor-of-local, local-ancestor-of-remote, diverged, and ambiguous remote-branch behavior;
- absent, open, draft, closed, merged, and ambiguous remote-PR behavior;
- `prepare-only` zero-mutation behavior and blocked open or draft requests that are not silently reclassified;
- independent creation intent, refresh authority, and existing PR state-transition authority;
- idempotent create and reuse, explicitly authorized title or whole-body refresh, insufficient refresh authority, body-byte preservation, interrupted read-back, concurrent creation, and duplicate prevention;
- exact verified base revision and optional merge-base binding before push, before PR mutation, and after read-back;
- force-push, remote deletion, remote overwrite, and implicit draft publication rejection;
- all hosted-CI states and their claim boundaries;
- body core, governed, and impact group applicability, omission, and blocked data;
- no lifecycle, plan, review, workflow, merge, release, or publication mutation;
- canonical, generated, archived, release-candidate, and clean-installed resource parity;
- unknown closed-vocabulary values fail before consistency checks.

Acceptance uses repository-owned static tests, fixtures, package validation, adapter distribution proof, and ordinary proposal, spec, code, verification, and PR review. It does not open a live acceptance PR, invoke a target-agent runtime, grade transcripts, add a prose classifier, or add a permanent tokenizer or simplicity validator.

### Acceptance criteria

| ID | Criterion |
| --- | --- |
| `AC-PRSIM-001` | Verification binds one exact verified subject revision separately from the handoff revision. |
| `AC-PRSIM-002` | The handoff revision may differ only by one direct-child verify-owned evidence commit with closed paths and fields. |
| `AC-PRSIM-003` | Any decision-bearing, unrelated, broader, or multi-commit post-verify change invalidates PR readiness. |
| `AC-PRSIM-004` | The local handoff revision, pushed remote head, and PR head are identical before success is claimed. |
| `AC-PRSIM-005` | An adequate existing matching PR is reused without content mutation. |
| `AC-PRSIM-006` | Title refresh or whole-body replacement requires explicit current authority covering the exact host-native field. |
| `AC-PRSIM-007` | Existing body bytes remain unchanged unless explicit whole-body replacement authority is current. |
| `AC-PRSIM-008` | Draft publication requires separate explicit authority. |
| `AC-PRSIM-009` | Remote branch state uses the closed absent, same, remote-ancestor-of-local, local-ancestor-of-remote, diverged, and ambiguous vocabulary. |
| `AC-PRSIM-010` | The skill never force-pushes, deletes, overwrites, or implicitly replaces a remote branch. |
| `AC-PRSIM-011` | Matching PR state is reread after push and immediately before PR mutation. |
| `AC-PRSIM-012` | A concurrently created matching PR is reconciled and reused or explicitly refreshed rather than duplicated. |
| `AC-PRSIM-013` | Portable and governed procedural profiles both decrease from the flat baseline. |
| `AC-PRSIM-014` | Canonical, generated, archived, release-candidate, and installed resources retain required parity. |
| `AC-PRSIM-015` | Acceptance opens no live test PR and executes no target-agent runtime. |
| `AC-PRSIM-016` | `prepare-only` performs no push, PR creation, PR refresh, or PR-state transition. |
| `AC-PRSIM-017` | Submission intent and existing PR state-transition authority are independent. |
| `AC-PRSIM-018` | Default `open` does not publish an existing draft. |
| `AC-PRSIM-019` | Explicit `draft` does not convert an existing open PR without separate authority. |
| `AC-PRSIM-020` | Every result separates requested intent, actual external operation, actual PR state, and readiness. |
| `AC-PRSIM-021` | Verification binds the exact base revision and any governing merge-base identity in addition to the verified subject. |
| `AC-PRSIM-022` | The remote base is checked before push, immediately before PR mutation, and after read-back. |
| `AC-PRSIM-023` | A changed base invalidates `pr-open-ready` and requires fresh verification or an approved base-update route. |
| `AC-PRSIM-024` | Every remote branch relationship is defined directionally relative to the local handoff revision. |
| `AC-PRSIM-025` | A remote branch containing commits absent locally always blocks push. |
| `AC-PRSIM-026` | First-version refresh units are closed host-native fields and never Markdown sections. |
| `AC-PRSIM-027` | Existing PR-body bytes are preserved unless explicit whole-body replacement authority exists. |
| `AC-PRSIM-028` | Section-level mutation requires a separate approved managed-content contract. |
| `AC-PRSIM-029` | External-operation success and readiness success remain separate when base or PR state changes concurrently. |
| `AC-PRSIM-030` | Static fixtures prove the complete intent, base/head, branch-relation, refresh, and retry matrices without a live acceptance PR. |
| `AC-PRSIM-031` | `verify` remains the sole owner of `branch-ready` and emits the normalized verification basis through its existing result or report surface. |
| `AC-PRSIM-032` | The normalized basis records immutable repository, remote, base, merge-base, head, and verified-subject identities. |
| `AC-PRSIM-033` | `pr` never reconstructs the verified basis from command text, unresolved names, current Git state, arbitrary prose, or historical report conventions. |
| `AC-PRSIM-034` | Legacy, portable, missing, stale, or ambiguous evidence without a complete exact basis permits preparation but blocks opening and `pr-open-ready`. |
| `AC-PRSIM-035` | Directly coupled verify-contract and fixture changes preserve ownership and canonical-through-installed package parity. |

### Measurement

Record UTF-8 bytes and Unicode whitespace-separated words using LF-normalized canonical files. Report separately:

```text
PR0-portable procedural profile:
  SKILL.md

PR1-governed procedural profile:
  SKILL.md + governed-pr-readiness.md

Structural asset:
  pr-body-skeleton.md

Representative composed package:
  procedural profile + applicable asset structure

Total canonical package:
  SKILL.md + reference + asset
```

Acceptance requires both PR0 and PR1 procedural profiles to decrease from the current 1,678-word, 11,375-byte flat baseline, every identified duplicate cluster to have one loaded owner, and any representative or total-package growth to be explicit and justified. No fixed percentage overrides semantic, lifecycle, or submission safety.

## Rollout and Rollback

Implement the `pr` package atomically in canonical `skills/pr/` source. In the same slice, amend only the existing verify result/report contract and directly coupled `skills/verify/` reference or output wording, workflow or skill contract, fixtures, and package projections required for the normalized basis. Update directly coupled validator and fixture consumers, regenerate only through existing repository tooling, and prove archive and clean-install parity before PR handoff.

Rollback restores the prior flat `pr` skill, removes its reference and asset, restores the prior verify result/report wording and focused fixtures, and regenerates every derived package atomically. Keep only validator improvements that remain correct for the restored contracts.

## Risks and Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Universal submission safety moves behind the governed trigger | Portable PRs may open unsafely | Keep exact target, verify, remote, CI, operation, push, read-back, stops, and claims inline; prove missing-reference independence for portable paths. |
| Existing-PR refresh mutates user-authored PR text unexpectedly | Reviewer context may be overwritten | Reuse adequate PRs without mutation; require explicit field or full-replacement authority; preserve draft status and stop on unknown, mixed, or indivisible content. |
| `prepare-only` or creation intent mutates existing external state unexpectedly | A supposedly bounded operation pushes or changes a review surface | Make `prepare-only` zero-write and separate submission intent, refresh authority, and existing state-transition authority. |
| Durable verify recording makes its own valid result appear stale | Governed PR handoff becomes impossible or broad post-verify changes become accepted | Separate verified subject and handoff revisions; permit exactly one direct-child verify-owned evidence commit with closed paths and fields; reject every broader change. |
| Remote base advances after verification | The effective review and integration surface differs from validated evidence | Bind the exact base/head pair, reread the base before mutation and after read-back, and separate external success from readiness. |
| `pr` infers a basis that current verify evidence never recorded | Stale or historically formatted evidence is presented as exact | Make `verify` the normalized basis owner, include its directly coupled amendment in scope, reject inference, and route incomplete legacy evidence to fresh verification. |
| The normalized tuple becomes a new persistence or ownership system | Simplification expands into architecture work | Use only existing verify result and verify-report surfaces; require architecture reassessment if they cannot carry the tuple safely. |
| Remote branch changed after local verification | A push overwrites or obscures another actor's work | Use closed remote-branch states, allow only absent creation or verified normal fast-forward, and prohibit every force, delete, or overwrite operation. |
| A matching PR appears after preflight | Duplicate PR creation or stale mutation occurs | Reread matching PR state after push and reclassify create, reuse, or refresh immediately before mutation. |
| Section refresh overwrites reviewer-authored Markdown | User context is lost through ambiguous heading parsing | Do not parse or mutate sections; preserve the body or replace it wholly only under explicit authority. |
| Pending or unobserved hosted CI is presented as passed | Reviewers receive a false readiness claim | Use the closed CI vocabulary and exact-head evidence rules. |
| Governed detection misses malformed change evidence | Lifecycle-owned work falls through to portable behavior | Treat every structured signal as a signal and use tri-state fail-closed classification. |
| Asset gains policy ownership | Body layout silently controls readiness | Restrict the asset to labels, order, placeholders, and table shapes; test applicability from procedure. |
| Main file shrinks but governed loaded context does not | Simplification is cosmetic | Require both real procedural profiles to decrease and report asset and total package separately. |
| Live acceptance creates external state or becomes provider-specific | Tests become nondeterministic and costly | Use static operation scenarios and existing package proof; leave actual external opening to ordinary PR use and review. |

## Open Questions

None at proposal level. Exact evidence field names, fixture encoding, focused test class names, and repository command selection belong to specification and planning.

## Decision Log

- Select one governed-readiness reference and one PR-body skeleton.
- Keep remote operation, verified-subject and handoff binding, hosted-CI meanings, opening authority, stops, and claims inline.
- Use tri-state governed-signal classification with no invalid-signal portable fallback.
- Permit one direct-child verify-owned durable-evidence commit after the verified subject and reject every broader post-verify change.
- Make `prepare-only` externally read-only and separate creation intent from existing PR state-transition authority.
- Reuse an adequate matching PR without mutation; refresh only the title or whole body under corresponding explicit authority.
- Bind verification to the exact base/head pair and use directional remote-branch ancestry states.
- Keep `verify` as the existing normalized verification-basis owner and include only its directly coupled result/report contract and fixtures in this slice.
- Treat incomplete legacy or portable verification evidence as preparation-only and require fresh verification before opening.
- Reconcile base, branch, and PR state after push without force operations to prevent stale readiness and duplicates.
- Defer Markdown section mutation to a separate managed-content and architecture decision.
- Preserve draft status unless explicit authority changes it.
- Keep hosted CI pending permissible only under current repository and verify evidence and never call it passed.
- Add no provider engine, persistent PR transaction record, lifecycle state, or mutation owner.
- Exclude live PR creation and target-agent runtime execution from acceptance.

## Next Artifacts

- independent `proposal-review` record;
- focused `pr` skill-contract specification after proposal approval;
- bounded architecture assessment;
- execution plan and test specification after the contract is approved.

## Follow-on Artifacts

None yet

## Readiness

Ready for independent proposal rereview after resolving `PRSIM-PR7`. Specification remains unauthorized until proposal-review approval.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Optimize the `pr` skill with the strongest package and safety design. | in scope | Goals, Recommended Direction, and Testing and Verification Strategy |
| Create the work on a new branch. | in scope | Governed change record and branch `proposal/pr-skill-simplification` |
| Generate a formal proposal. | in scope | This proposal artifact |
| Run `proposal-review` after authoring. | in scope | Next Artifacts and governed workflow state |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Compact universal PR procedure | core to this proposal | This is the primary common-path simplification surface. |
| Governed PR-readiness reference | core to this proposal | It provides the only independent procedural activation boundary. |
| PR-body structural asset | core to this proposal | Repeated output layout requires one non-policy owner. |
| Exact verified-revision and remote operation model | same-slice dependency | Simplification cannot preserve safe external action while leaving these outcomes implicit. |
| Existing verify result/report basis amendment | same-slice dependency | Exact PR base/head binding requires the current `verify` owner to emit immutable repository, remote, base, merge-base, head, and subject identities. |
| Verify compatibility fixtures and package projections | same-slice dependency | Legacy and portable evidence must fail closed without changing `branch-ready` ownership or inventing a new artifact. |
| Hosted-CI vocabulary and claims | same-slice dependency | Current truthfulness and post-open CI behavior are compatibility-sensitive. |
| Rule, literal, profile, scenario, and package-parity proof | same-slice dependency | Public skill behavior and generated resources require deterministic preservation evidence. |
| Provider-specific PR engine or new CLI | out of scope | Existing host tooling remains the external-operation mechanism. |
| Automatic merge, release, publication, labels, and reviewer assignment | out of scope | These are separate authorities and product decisions. |
| Other skill simplifications | separate proposal | They have different activation boundaries and proof surfaces. |
