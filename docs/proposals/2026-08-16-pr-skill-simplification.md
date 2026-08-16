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
- Make create, explicitly authorized refresh, reuse, and retry behavior deterministic and idempotent for the exact repository, verified subject, handoff revision, head, base, remote branch, and PR identity.
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
- Do not optimize unrelated skills or generated adapter implementation in this change.

## Vision fit

fits the current vision

The change strengthens the traceable idea-to-PR chain while reducing ceremony on the common path. Reviewers still receive the governing artifacts, evidence, risks, and unresolved external status they need, while customer projects avoid RigorLoop-specific lifecycle procedure unless governed evidence actually activates it.

## Context

`pr` is the terminal submit/open stage of the normal workflow. A direct invocation still opens a PR when readiness passes, but it has no downstream stage. The current contract already distinguishes local validation from hosted CI, requires actual-diff evidence, and prohibits lifecycle settlement. This proposal preserves those boundaries and reorganizes procedure around evidence-based activation.

The existing published-skill package architecture supports canonical `SKILL.md`, mapped `references/`, mapped `assets/`, generated archives, release-candidate packages, and clean-installed parity. The proposal uses that model without adding runtime or persistence architecture.

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

- purpose, submit/open default, explicit draft or prepare-only exceptions, and external-action authority;
- exact repository, remote, head, base, verified subject, optional verify-owned evidence tail, handoff revision, pushed commit, and matching PR resolution;
- current `verify` evidence and exact verified-subject binding without invalidation by its own closed durable-recording commit;
- actual diff, working-tree, commit-scope, secrets, generated-output, migration, and reviewer-context checks;
- remote branch-state and PR-state classification, explicit refresh authority, and idempotent operation selection;
- hosted-CI state meanings and claim limitations;
- concise title and PR-body adequacy rules;
- push-before-open sequence, remote reread, create or refresh result, and read-back confirmation;
- universal stops, no-lifecycle-mutation boundary, output result, and no downstream continuation.

The universal file must not embed the complete PR-body section layout or detailed RigorLoop change-pack closeout procedure.

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

`open` is the default for an explicit `pr` invocation. `draft` or `prepare-only` requires an explicit user instruction, a repository contract, or a blocker or tooling limitation that prevents opening; a limitation is reported as an outcome and never silently reframed as successful opening.

Resolve refresh authority independently:

```text
none
explicit-field-refresh
explicit-full-replacement
workflow-field-refresh
```

`explicit-field-refresh` and `explicit-full-replacement` require a current user instruction naming the existing PR and permitted replacement scope. `workflow-field-refresh` requires same-change workflow authority naming refresh and the exact fields or sections it may replace. Ordinary `pr` invocation, matching PR identity, stale generated content, or loaded governed procedure does not itself authorize replacement. Unknown, conflicting, or ambiguous refresh authority stops before content mutation.

Resolve one remote branch state for the exact repository, remote, and head branch:

```text
absent
same
fast-forwardable
ahead
diverged
ambiguous
```

`absent` permits creation of the remote branch. `same` requires no push. `fast-forwardable` permits only a normal non-force push after the expected remote baseline is revalidated. `ahead`, `diverged`, and `ambiguous` stop. The skill never force-pushes, deletes, rewrites, or implicitly replaces a remote branch.

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
| `open` or `draft` | exact permitted fields differ and current refresh authority covers them | `refresh-primary-pr`; reread current content, replace only the authorized fields or sections, preserve every other byte and PR identity, and report `updated` after read-back. |
| `open` or `draft` | full content differs and explicit full-replacement authority is current | `refresh-primary-pr`; replace the authorized title or body, preserve PR identity, and report `updated` after read-back. |
| `open` or `draft` | stale content but refresh authority is absent, insufficient, conflicting, or ambiguous | Stop; report the exact authority or ownership blocker without mutation. |
| `closed` | any | Stop; require an explicit reopen or new-branch decision. |
| `merged` | any | Stop; do not treat merge as lifecycle completion or create another PR implicitly. |
| `ambiguous` | any | Stop before push or PR mutation. |

Draft state is preserved unless separate explicit authority publishes it. The refresh model introduces no hidden markers or managed-section protocol. Current content that cannot be separated safely into authorized and preserved regions blocks field refresh; full replacement requires explicit full-replacement authority.

Multiple matching PRs, mismatched base, mismatched repository, unsafe branch, unavailable remote identity, or conflicting host evidence are `ambiguous`. If another actor creates the exact matching PR after preflight, the mandatory post-push reread selects `reuse-existing-pr` or an authorized refresh rather than duplicate creation. Retry reuses the same remote PR identity and must never create a duplicate for the same head/base operation.

### Exact verified-revision sequence

The operation binds:

```text
repository identity
remote identity
base branch and base revision
head branch
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
2. Resolve the verify report's exact `verified_subject_revision` and require it to be an ancestor of or equal to the local handoff revision.
3. When the local head differs, require exactly one direct-child verify-owned evidence commit. Its diff may contain only the final verify report and the matching owning change record or explicitly required verify-owned state-sync evidence. The change-record diff may update only final verification evidence and verify-owned readiness or routing fields. Any product, test, specification, architecture, plan, dependency, configuration, generated-output, unrelated documentation, or other lifecycle-owner change makes verification stale.
4. Validate the allowed tail paths, parent relationship, content identities, and change-record field boundary. The local head becomes the exact `handoff_revision`; no in-memory or self-referential handoff hash is required inside its own commit.
5. Resolve the remote branch and matching PR states without mutation. Stop early for closed, merged, unsafe, divergent, ahead, or ambiguous state.
6. Create an absent remote branch or normally fast-forward the expected remote baseline to the exact handoff revision. Never use a force, delete, overwrite, or implicit branch-replacement operation.
7. Re-read the remote branch and require its head to equal the local handoff revision.
8. Re-read the matching PR state, head, base, title, body, and draft status immediately before PR mutation. Reclassify the operation when concurrent state changed; never use the stale pre-push PR classification.
9. Create, reuse, or explicitly refresh exactly one matching PR.
10. Read back the PR URL, number, state, head, base, title, and body identity before claiming success. Require the PR head to equal the handoff revision.

Failure before confirmed read-back reports the exact operation failure and must not claim that a PR opened or updated. A retry reconciles the remote state rather than blindly repeating create.

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

### Resource failure behavior

A missing, unreadable, escaped, contradictory, stale, transformed, or mixed-version triggered reference stops governed readiness judgment. A missing or invalid skeleton stops PR-body generation and external submission. The common file must not reconstruct missing conditional procedure or layout from memory.

## Expected Behavior Changes

- Portable PR invocations no longer load detailed RigorLoop change-pack and lifecycle-closeout procedure.
- Governed invocations load one reference after a tri-state governed-signal classification and remain unable to mutate lifecycle state.
- PR bodies use one structural owner with closed optional groups instead of an inline full template.
- Existing open and draft PRs are reused without mutation when adequate and refreshed only under explicit field or full-replacement authority.
- The verified subject may differ from the handoff revision only by one validated verify-owned durable-evidence commit; the pushed remote head and PR head must equal the handoff revision.
- Remote branches are created or normally fast-forwarded only from safe states, and matching PR state is reread after push to reconcile concurrent creation.
- Hosted CI states become closed, current-head-bound, and truthfully reported.
- Missing required resources and ambiguous remote or governed state fail closed.

## Architecture Impact

A bounded architecture assessment is required because the change introduces mapped skill resources and clarifies an external-operation transaction. The expected result is `architecture-not-required` when current architecture already supports packaged references and assets and the operation uses existing Git and host tooling without a new persistent record, service, schema, state owner, or provider abstraction.

Architecture becomes required if specification or implementation needs a new durable PR transaction artifact, provider-neutral runtime layer, lifecycle mutation owner, remote-state schema, or cross-process recovery service.

## Testing and Verification Strategy

### Change-local preservation evidence

Before editing canonical skill content, create:

- a semantic-rule disposition ledger with one owner and disposition for every current behaviorally significant rule and duplicate cluster;
- a literal-compatibility ledger for headings, readiness labels, status values, resource paths, output fields, and exact phrases consumed by tests or packages;
- deterministic baseline measurements for `SKILL.md`, each planned reference or asset, portable and governed procedural profiles, representative body composition, and total package;
- static scenario fixtures for every operation, remote state, submission intent, CI state, resource failure, retry, and forbidden mutation.

### Deterministic proof

Prove at least:

- exact `READ` and `COPY` mappings, path containment, triggers, and one-load behavior;
- tri-state governed-signal classification and no invalid-signal portable fallback;
- exact verified-subject, handoff, remote-head, and PR-head binding;
- same-revision and one-commit verify-owned evidence-tail binding, including every forbidden post-verify path and field class;
- absent, same, fast-forwardable, ahead, diverged, and ambiguous remote-branch behavior;
- absent, open, draft, closed, merged, and ambiguous remote-PR behavior;
- idempotent create and reuse, explicitly authorized field or full refresh, insufficient refresh authority, mixed content ownership, interrupted read-back, concurrent creation, and duplicate prevention;
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
| `AC-PRSIM-006` | Title, body, or section refresh requires explicit current authority covering the exact replacement scope. |
| `AC-PRSIM-007` | Unknown, mixed, conflicting, or indivisible existing content blocks field refresh unless full replacement is explicitly authorized. |
| `AC-PRSIM-008` | Draft publication requires separate explicit authority. |
| `AC-PRSIM-009` | Remote branch state uses the closed absent, same, fast-forwardable, ahead, diverged, and ambiguous vocabulary. |
| `AC-PRSIM-010` | The skill never force-pushes, deletes, overwrites, or implicitly replaces a remote branch. |
| `AC-PRSIM-011` | Matching PR state is reread after push and immediately before PR mutation. |
| `AC-PRSIM-012` | A concurrently created matching PR is reconciled and reused or explicitly refreshed rather than duplicated. |
| `AC-PRSIM-013` | Portable and governed procedural profiles both decrease from the flat baseline. |
| `AC-PRSIM-014` | Canonical, generated, archived, release-candidate, and installed resources retain required parity. |
| `AC-PRSIM-015` | Acceptance opens no live test PR and executes no target-agent runtime. |

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

Implement the package atomically in canonical `skills/pr/` source, update directly coupled validator and fixture consumers, regenerate only through existing repository tooling, and prove archive and clean-install parity before PR handoff.

Rollback restores the prior flat `SKILL.md`, removes the reference and asset, updates focused assertions, and regenerates every derived package atomically. Keep only validator improvements that remain correct for the restored flat package.

## Risks and Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Universal submission safety moves behind the governed trigger | Portable PRs may open unsafely | Keep exact target, verify, remote, CI, operation, push, read-back, stops, and claims inline; prove missing-reference independence for portable paths. |
| Existing-PR refresh mutates user-authored PR text unexpectedly | Reviewer context may be overwritten | Reuse adequate PRs without mutation; require explicit field or full-replacement authority; preserve draft status and stop on unknown, mixed, or indivisible content. |
| Durable verify recording makes its own valid result appear stale | Governed PR handoff becomes impossible or broad post-verify changes become accepted | Separate verified subject and handoff revisions; permit exactly one direct-child verify-owned evidence commit with closed paths and fields; reject every broader change. |
| Remote branch changed after local verification | A push overwrites or obscures another actor's work | Use closed remote-branch states, allow only absent creation or verified normal fast-forward, and prohibit every force, delete, or overwrite operation. |
| A matching PR appears after preflight | Duplicate PR creation or stale mutation occurs | Reread matching PR state after push and reclassify create, reuse, or refresh immediately before mutation. |
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
- Reuse an adequate matching PR without mutation; refresh only exact fields or full content under corresponding explicit authority.
- Reconcile remote branch state without force operations and reread matching PR state after push to prevent duplicates.
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

Ready for independent proposal rereview after resolving `PRSIM-PR1`, `PRSIM-PR2`, and `PRSIM-PR3`. Specification remains unauthorized until proposal-review approval.

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
| Hosted-CI vocabulary and claims | same-slice dependency | Current truthfulness and post-open CI behavior are compatibility-sensitive. |
| Rule, literal, profile, scenario, and package-parity proof | same-slice dependency | Public skill behavior and generated resources require deterministic preservation evidence. |
| Provider-specific PR engine or new CLI | out of scope | Existing host tooling remains the external-operation mechanism. |
| Automatic merge, release, publication, labels, and reviewer assignment | out of scope | These are separate authorities and product decisions. |
| Other skill simplifications | separate proposal | They have different activation boundaries and proof surfaces. |
