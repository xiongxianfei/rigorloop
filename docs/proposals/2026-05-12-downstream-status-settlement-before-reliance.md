# Downstream Status Settlement Before Reliance

## Status

accepted

## Problem

RigorLoop review artifacts can clearly approve an upstream lifecycle artifact while the reviewed artifact's own durable status still remains stale. For example, a proposal may still say `Status: draft` even after proposal-review approved it and no material findings remain.

The previous review-recording guardrail intentionally did not make review skills update reviewed artifact status. That was the right scope split: formal review skills should record review evidence and material findings, while downstream authoring and execution skills should settle upstream status before relying on upstream artifacts.

The remaining problem is that the downstream settlement model is only a follow-up direction. Without a concrete proposal and later spec, downstream skills can still rely on stale upstream status, or different skills may update lifecycle fields inconsistently.

## Goals

- Define downstream status settlement before reliance as the preferred follow-up direction.
- Keep review skills focused on review evidence and material-finding recording.
- Treat artifacts as the durable source of truth.
- Allow downstream skills to perform minimal upstream lifecycle/status settlement when review evidence is clear.
- Make stale, contradictory, missing, or unresolved upstream review evidence a blocker before reliance.
- Keep settlement edits narrow: lifecycle/status/readiness/follow-on/closeout metadata only.
- Implement the first slice for `spec`, `architecture`, and `plan`.
- Preserve isolated review-only behavior.

## Non-goals

- Do not move artifact-status sync back into formal review skills.
- Do not implement downstream settlement in this proposal.
- Do not rewrite substantive artifact content as part of settlement.
- Do not create a new review stage.
- Do not change formal review recording rules from the previous slice.
- Do not make downstream skills bypass unresolved material findings.
- Do not settle every possible artifact type in the first implementation slice.

## Vision fit

fits the current vision

This proposal supports RigorLoop's goal of making AI-assisted changes traceable and reviewable from durable artifacts rather than chat history. It reduces a source-of-truth mismatch before downstream work relies on upstream decisions.

## Context

The accepted review-recording guardrail proposal recorded this follow-up direction:

```text
Review records evidence.
Downstream settles status before reliance.
Artifacts remain the source of truth.
```

`specs/formal-review-recording.md` also records that downstream status settlement may be specified later and that downstream skill execution may imply permission for minimal upstream lifecycle/status settlement before reliance. The first implementation slice for that amendment explicitly did not update downstream authoring or execution skills.

PR #45 merged the review-recording guardrail. This proposal is a separate follow-up and should not be bundled with that prior implementation.

This proposal is the follow-up decision artifact for that deferred scope.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
|---|---|---|
| Implement the follow-up direction for downstream status settlement before reliance | in scope as proposal direction, implementation deferred to spec/plan | Problem, Recommended direction, Next artifacts |
| Keep review skills focused on review evidence and material-finding recording | in scope | Goals, Non-goals, Recommended direction |
| Let downstream skills settle upstream status by default before relying | in scope | Recommended direction, Expected behavior changes |
| Keep artifacts as source of truth | in scope | Goals, Recommended direction |

## Options considered

### Option 1: Review skills update reviewed artifact status

Advantages:

- Status changes happen immediately after review.
- Downstream skills see settled upstream artifacts without extra checks.

Disadvantages:

- Reopens the PR #44 scope problem.
- Blurs reviewer and authoring responsibilities.
- Makes isolated review requests more edit-heavy.
- Requires review skills to know every artifact lifecycle mapping.

### Option 2: Manual maintainer status updates only

Advantages:

- Keeps automation simple.
- Maintainers retain explicit control over lifecycle fields.

Disadvantages:

- Leaves stale status easy to miss.
- Makes downstream readiness depend on memory or manual cleanup.
- Does not scale across repeated workflow-managed changes.

### Option 3: Downstream skills settle upstream status before reliance

Advantages:

- Keeps review skills independent.
- Settles status at the point where stale status matters.
- Preserves artifacts as the source of truth before downstream work proceeds.
- Allows a narrow, testable settlement contract.

Disadvantages:

- Requires updates across several downstream skills.
- Needs exact artifact-specific status mappings before implementation.
- Requires blocker behavior when evidence is ambiguous.

## Recommended direction

Choose Option 3.

When a downstream authoring or execution skill is running and must rely on an upstream lifecycle artifact, it should check whether the upstream artifact's durable status matches clear review evidence.

If the review evidence is clear, final, and has no unresolved material findings, the downstream skill should perform minimal lifecycle/status settlement and continue.

If evidence is missing, contradictory, stale, ambiguous, or has unresolved material findings, the downstream skill should stop and report a settlement blocker.

In workflow-managed downstream execution, minimal upstream lifecycle/status settlement is allowed. A no-edit or review-only request remains an isolated manual skill invocation and does not enter downstream execution.

Downstream settlement should not ask whether edits are allowed during normal downstream execution. It blocks only when:

- review evidence is missing, stale, contradictory, or inconclusive;
- unresolved material findings remain;
- the expected status mapping is not deterministic;
- the artifact lacks the required status surface;
- multiple durable records conflict.

Allowed settlement edits should be limited to:

- `Status`
- readiness fields
- follow-on artifact fields
- closeout or lifecycle metadata

Settlement should not rewrite substantive proposal, spec, architecture, plan, test, or implementation content.

## First implementation slice

The first implementation slice should cover:

- `spec`
- `architecture`
- `plan`

These skills cover the clearest upstream reliance chain:

```text
proposal -> spec
spec -> architecture
spec/architecture -> plan
```

Deferred to later slices:

- `test-spec`
- `implement`
- `explain-change`
- `verify`
- `pr`

The first spec may include brief later-slice design notes for those skills, but it should not define detailed requirements for them. Later slices must define exact artifact mappings, blockers, and output rules before implementation. The first spec does not authorize those skills to perform settlement yet.

## Initial settlement mappings

| Downstream skill | Upstream artifact | Clear review evidence | Settlement |
|---|---|---|---|
| `spec` | proposal | proposal-review approved, no unresolved material findings | proposal `Status: accepted` |
| `architecture` | spec | spec-review approved, no unresolved material findings | spec `Status: approved` |
| `plan` | spec | spec-review approved, no unresolved material findings | spec `Status: approved` |
| `plan` | architecture package | architecture-review approved, no unresolved material findings | architecture `Status: approved` |
| `plan` | ADR | architecture-review approved, no unresolved material findings | ADR status remains artifact-specific: `accepted` or `active` only when the ADR vocabulary supports it |

If a mapping is not listed, the downstream skill must not guess. It should report `Settlement result: blocked`.

ADR settlement is allowed only when the ADR artifact already exposes a lifecycle/status field with a known target status. If the ADR vocabulary is absent or ambiguous, settlement blocks.

## Block-on-unknown lifecycle vocabulary

A downstream skill may settle an upstream artifact only when the status mapping is explicitly defined for that artifact type.

If the artifact type, lifecycle field, or next status is not defined, the downstream skill should report `Settlement result: blocked` and name the missing mapping.

## Clear review evidence

Review evidence is clear only when all are true:

- a durable formal review record or approved review artifact exists;
- the review outcome is approving or clean for the relevant artifact;
- no later review record contradicts that outcome;
- `review-log.md`, when present, lists no open findings for the artifact;
- `review-resolution.md`, when required, has closed all material findings;
- the artifact status mapping is listed in the settlement mapping table.

If any condition fails, downstream settlement should report `Settlement result: blocked`.

## Settlement output

Downstream skills should report `Upstream status settlement` when:

- status was updated;
- status settlement was blocked;
- stale upstream status was detected;

When no upstream lifecycle artifact is relied on, all relied-on artifacts are already settled, or settlement is irrelevant to the task, the skill may omit the block or report `Settlement result: not-needed`.

The settlement block, when required, should include:

```md
## Upstream status settlement

- Upstream artifact:
- Review evidence:
- Previous status:
- New status:
- Settlement result: updated | blocked
- Settlement blocker:
```

## Expected behavior changes

Before:

```text
spec may rely on a proposal whose artifact still says draft even though proposal-review approved it
```

After:

```text
spec checks proposal review evidence, updates proposal Status to accepted when clear, then continues
```

Before:

```text
implement may rely on a plan or test-spec whose readiness/status fields lag behind review evidence
```

After:

```text
plan settles clear upstream lifecycle/readiness metadata for spec or architecture artifacts, or blocks before relying
```

Before:

```text
review skills may be tempted to own artifact-status sync
```

After:

```text
review skills record verdicts and findings; downstream skills settle before reliance
```

## Architecture impact

No runtime architecture change is expected.

This is a workflow contract and skill-behavior change. Affected surfaces may include:

- `specs/rigorloop-workflow.md`
- `specs/formal-review-recording.md` only if the follow-up boundary needs cross-reference cleanup
- relevant test specs
- downstream skills `spec`, `architecture`, and `plan` in the first slice
- `workflow` guidance
- static skill-validator coverage
- generated `.codex/skills/` and `dist/adapters/` output after canonical skill changes

Later slices may extend the contract to `test-spec`, `implement`, `explain-change`, `verify`, and `pr`. The first spec should include later-slice notes only, not detailed requirements for those skills. The first implementation slice should avoid changing formal review skills except for removing stale cross-references if a later spec requires it.

## Testing and verification strategy

The spec should define artifact-specific settlement mappings and blocker cases. The test spec should map them to static and structural proof.

Likely validation:

```bash
python scripts/test-skill-validator.py
python scripts/validate-skills.py
python scripts/build-skills.py --check
python scripts/build-adapters.py --version 0.1.1 --check
python scripts/validate-adapters.py --version 0.1.1
python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path <touched-artifacts>
git diff --check -- <touched-paths>
```

Candidate tests:

- `spec`, `architecture`, and `plan` include a concise `Upstream status settlement` guardrail;
- review skills do not gain standardized `Status sync` fields;
- ambiguous settlement evidence routes to blocked;
- unresolved material findings block settlement;
- unmapped artifact/status combinations route to blocked;
- settlement output is required for updates, blockers, and stale detected status;
- generated skill/adapters reflect canonical skill changes;
- examples or fixtures, if added, live under `docs/examples/**`.

Lifecycle validation should not enforce stale-status detection in the first implementation slice. A later lifecycle validator may detect stale upstream artifact status when clear review evidence exists and a downstream artifact relies on the upstream artifact. Initial lifecycle validation should run in explicit-path or warning mode until settlement mappings are stable.

## Rollout and rollback

Rollout:

1. Review and accept this proposal.
2. Write a focused spec amendment defining downstream settlement rules, mappings, and blockers.
3. Review the spec.
4. Create an execution plan with a small first slice.
5. Update the selected downstream skills and static checks.
6. Refresh generated outputs.
7. Verify and open a PR.

Rollback:

- If settlement behavior proves too broad, revert downstream skill guidance and keep the spec as historical evidence.
- If a specific mapping is unsafe, remove that mapping and require blocked settlement until a later proposal clarifies it.
- Do not roll back the already-merged review-recording guardrail.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Downstream skills rewrite substantive content while settling status. | Limit settlement to lifecycle/status/readiness/follow-on/closeout metadata. |
| Status mappings are guessed inconsistently. | Start with the initial mapping table and block on unmapped combinations. |
| Unresolved material findings are ignored. | Make unresolved findings a blocker before settlement and reliance. |
| The first slice becomes too broad. | Limit the first slice to `spec`, `architecture`, and `plan`. |
| Review skills regain status-sync responsibility. | Keep review-side status sync as a non-goal and add static checks if needed. |
| Validators miss stale status cases. | Begin with skill/static checks, then consider lifecycle-validator detection after mappings and behavior stabilize. |

## Open questions

- None before spec.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
|---|---|---|---|
| 2026-05-12 | Propose downstream status settlement as a follow-up to review-recording guardrails. | PR #45 intentionally kept review skills focused on review evidence and left settlement as follow-up scope. | Reopen review-side status sync. |
| 2026-05-12 | Keep settlement edits minimal and metadata-only. | Downstream skills should not rewrite substantive upstream content while settling lifecycle state. | Allow broad artifact rewrites during settlement. |
| 2026-05-12 | Limit the first implementation slice to `spec`, `architecture`, and `plan`. | These skills cover the clearest upstream reliance chain and keep the first reviewable slice small. | Include `test-spec`, `implement`, `explain-change`, `verify`, and `pr` immediately. |
| 2026-05-12 | Block on unmapped or unclear settlement evidence. | Deterministic settlement is safer than guessing lifecycle state. | Let downstream skills infer mappings ad hoc. |
| 2026-05-12 | Include later-slice notes only for `test-spec`, `implement`, `explain-change`, `verify`, and `pr`. | The first spec should stay focused while preserving the follow-up direction. | Define detailed requirements for later-slice skills now. |
| 2026-05-12 | Require settlement output only for updates, blockers, or detected stale status. | Output should expose meaningful status settlement events without adding boilerplate to every downstream run. | Emit settlement output on every run. |
| 2026-05-12 | Defer lifecycle-validator stale-status detection. | The validator needs stable mappings and behavior to avoid false positives. | Add semantic lifecycle validation in the first slice. |

## Next artifacts

- proposal-review
- focused spec amendment for downstream status settlement before reliance
- spec-review
- plan
- test-spec
- implementation slice for `spec`, `architecture`, and `plan`

## Follow-on artifacts

- Spec: [Downstream Status Settlement Before Reliance](../../specs/downstream-status-settlement-before-reliance.md), draft.

## Readiness

Accepted. The draft spec now carries the next review gate for this change.

Implementation should not begin until the draft spec is reviewed and approved.

## Core invariant

```text
Review records evidence.
Downstream settles status before reliance.
Artifacts remain the source of truth.
```
