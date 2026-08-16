# PR Skill Simplification

## Owning change record

This proposal is governed by `docs/changes/2026-08-16-pr-skill-simplification/change.yaml`.

## Problem

The current `pr` skill is a flat 1,678-word, 11,375-byte file that combines universal branch and remote checks, RigorLoop-specific lifecycle aggregation, PR-body structure, hosted-CI interpretation, submission behavior, evidence-reading guidance, claim boundaries, and repeated output labels. Every invocation therefore loads governed change-pack procedure and a full inline body template even when a portable repository needs only a verified diff, a concise body, and one pull-request operation.

The flat shape also leaves several execution outcomes implicit. It does not close how to handle an existing open or draft PR, how retries avoid duplicate PRs, how a pushed head is rebound to verification evidence, or how known failed, pending, unavailable, and unobserved hosted CI affect PR-opening claims. Those gaps are safety and idempotency concerns, not merely editorial opportunities.

## Goals

- Reduce the universal and governed procedural context loaded by `pr` while preserving evidence truthfulness, branch and remote safety, submission behavior, and claim ownership.
- Keep universal target resolution, exact verified-revision binding, working-tree and push safety, remote PR classification, submission authority, hosted-CI truthfulness, stops, claims, and concise result behavior inline.
- Move governed lifecycle aggregation into one conditional reference with no lifecycle mutation, settlement, or routing authority.
- Move repeated PR-body headings, ordering, and placeholders into one structural asset without moving readiness or claim policy into the asset.
- Make create, refresh, reuse, and retry behavior deterministic and idempotent for the exact repository, head, base, and remote PR identity.
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

This option keeps universal submission safety inline, moves governed lifecycle aggregation behind one real trigger, and gives repeated body layout one structural owner. It also closes remote-state, exact-head, retry, and hosted-CI behavior in the universal contract.

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
- exact repository, remote, head, base, local commit, pushed commit, and matching PR resolution;
- current `verify` evidence and exact verified-revision binding;
- actual diff, working-tree, commit-scope, secrets, generated-output, migration, and reviewer-context checks;
- remote PR-state classification and idempotent operation selection;
- hosted-CI state meanings and claim limitations;
- concise title and PR-body adequacy rules;
- push-before-open sequence, remote reread, create or refresh result, and read-back confirmation;
- universal stops, no-lifecycle-mutation boundary, output result, and no downstream continuation.

The universal file must not embed the complete PR-body section layout or detailed RigorLoop change-pack closeout procedure.

### `governed-pr-readiness.md` ownership

Load the reference only after one exact governed change candidate resolves from an explicit change ID, workflow-managed same-change authority, a current verify report, or a structured owning-change pointer. Any governed signal counts even when malformed. Classification is exactly:

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

Resolve one remote state for the exact repository, head, base, and host:

```text
absent
open
draft
closed
merged
ambiguous
```

Use this closed operation matrix:

| Remote state | Operation and result |
| --- | --- |
| `absent` | `create-primary-pr`; push the exact verified head, create once, read back identity, and report `opened` or `draft-opened`. |
| `open` | `refresh-primary-pr`; preserve PR identity, update stale title or body from current evidence, or return idempotent `reused` when current. |
| `draft` | `refresh-primary-pr`; preserve draft status unless explicit authority publishes it, update stale title or body, or return `reused`. |
| `closed` | Stop; require an explicit reopen or new-branch decision. |
| `merged` | Stop; do not treat merge as lifecycle completion or create another PR implicitly. |
| `ambiguous` | Stop before push or PR mutation. |

Multiple matching PRs, mismatched base, mismatched repository, unsafe branch, unavailable remote identity, or conflicting host evidence are `ambiguous`. Retry reuses the same remote PR identity and must never create a duplicate for the same head/base operation.

### Exact verified-revision sequence

The operation binds:

```text
repository identity
remote identity
base branch and base revision
head branch
local head revision
verify report identity
verified head revision
intended title and body identity
matching PR identity when present
```

Require this sequence:

1. Resolve the current local target, working tree, governing evidence, and intended PR content.
2. Require the verify report's exact head to match the local head; any later decision-bearing commit makes verification stale.
3. Resolve the current remote and matching PR state without mutation.
4. Push the exact local head when needed.
5. Re-read the remote head and require it to match the verified local head.
6. Create, refresh, or reuse exactly one matching PR.
7. Read back the PR URL, number, state, head, base, title, and body identity before claiming success.

Failure before confirmed read-back reports the exact operation failure and must not claim that a PR opened or updated. A retry reconciles the remote state rather than blindly repeating create.

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

`passed` requires current hosted evidence for the exact PR head. `failed` blocks a clean handoff when the failing check is required and routes to the owning correction or CI stage. `pending` permits initial opening only when current repository and verify evidence permit CI to begin after opening, and the PR body must say pending. `unavailable` and `unobserved` may permit opening only when hosted CI is not a pre-open prerequisite; neither may be described as passed. `not-applicable` requires current evidence that no hosted check applies.

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
- Existing open and draft PRs are reconciled idempotently rather than risking duplicate creation.
- Local verified head, pushed remote head, and PR head must match before success is claimed.
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
- exact verified local, remote, and PR head binding;
- absent, open, draft, closed, merged, and ambiguous remote behavior;
- idempotent create, refresh, reuse, interrupted read-back, and duplicate prevention;
- all hosted-CI states and their claim boundaries;
- body core, governed, and impact group applicability, omission, and blocked data;
- no lifecycle, plan, review, workflow, merge, release, or publication mutation;
- canonical, generated, archived, release-candidate, and clean-installed resource parity;
- unknown closed-vocabulary values fail before consistency checks.

Acceptance uses repository-owned static tests, fixtures, package validation, adapter distribution proof, and ordinary proposal, spec, code, verification, and PR review. It does not open a live acceptance PR, invoke a target-agent runtime, grade transcripts, add a prose classifier, or add a permanent tokenizer or simplicity validator.

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
| Existing-PR refresh mutates user-authored PR text unexpectedly | Reviewer context may be overwritten | Bind refresh to one exact matching PR, compare intended and current content, preserve draft status, and require current `pr` authority; stop on ambiguity or unrelated content ownership. |
| A commit after verify is pushed and opened | PR is not covered by branch-ready evidence | Bind verify, local, remote, and PR head identities and stop on any mismatch. |
| Pending or unobserved hosted CI is presented as passed | Reviewers receive a false readiness claim | Use the closed CI vocabulary and exact-head evidence rules. |
| Governed detection misses malformed change evidence | Lifecycle-owned work falls through to portable behavior | Treat every structured signal as a signal and use tri-state fail-closed classification. |
| Asset gains policy ownership | Body layout silently controls readiness | Restrict the asset to labels, order, placeholders, and table shapes; test applicability from procedure. |
| Main file shrinks but governed loaded context does not | Simplification is cosmetic | Require both real procedural profiles to decrease and report asset and total package separately. |
| Live acceptance creates external state or becomes provider-specific | Tests become nondeterministic and costly | Use static operation scenarios and existing package proof; leave actual external opening to ordinary PR use and review. |

## Open Questions

None at proposal level. Exact evidence field names, fixture encoding, focused test class names, and repository command selection belong to specification and planning.

## Decision Log

- Select one governed-readiness reference and one PR-body skeleton.
- Keep remote operation, exact revision binding, hosted-CI meanings, opening authority, stops, and claims inline.
- Use tri-state governed-signal classification with no invalid-signal portable fallback.
- Reconcile one matching open or draft PR idempotently; never create duplicates or publish drafts implicitly.
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

Ready for independent proposal review. Specification is not authorized until proposal-review approval and material finding resolution, when applicable.

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
