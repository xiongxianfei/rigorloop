# Relax PR Evidence Tail Topology

## Challenge

The current PR handoff contract protects against post-review drift by allowing the verified subject to differ from the PR handoff revision by exactly one direct-child Verify-owned evidence commit. The active governed workflow, however, normally records final Code Review evidence, a workflow transition into Verify, and the final Verify result after the product revision that Code Review reviewed. A correctly completed change can therefore require several evidence-only commits and still fail PR readiness solely because of commit count or ownership labels, even though no product or governing contract changed.

PR #169 demonstrated this mismatch: the reviewed product revision was followed only by final-review, workflow-routing, and Verify evidence, yet the literal one-commit rule classified the handoff as invalid. The rule is stricter than the safety outcome it is meant to protect and encourages history rewriting or one-off overrides instead of ordinary additive, auditable workflow evidence.

## Goals

- Preserve the guarantee that no unreviewed product or decision-bearing change reaches a PR.
- Allow the ordinary governed lifecycle to record final review, routing, and Verify evidence without invalidating PR readiness because of commit count alone.
- Make PR readiness depend on the final content and authority of a contiguous evidence-only suffix rather than one exact Git topology.
- Keep the rule deterministic, inspectable, fail-closed for unknown or mixed changes, and portable across supported adapters.
- Preserve Verify ownership of `branch-ready`, PR ownership of `pr-body-ready` and `pr-open-ready`, and Workflow ownership of routing.
- Avoid new revision schemas, persistent PR transaction state, history rewriting, or additional lifecycle stages.

## Scope and non-goals

In scope are the canonical PR handoff contract, the `pr` skill, directly coupled Verify evidence-tail wording, deterministic regression coverage, examples, and generated package projections required to publish the revised behavior.

The scope budget is:

| Work item | Treatment | Reason |
| --- | --- | --- |
| Replace the one-commit exception with a contiguous evidence-only suffix | core to this proposal | This is the behavioral correction. |
| Preserve reviewed-subject, handoff, remote-head, and PR-head identity checks | same-slice dependency | Relaxing topology must not weaken identity binding. |
| Define permitted and invalidating post-review changes | same-slice dependency | Readiness needs an objective safety boundary. |
| Align Verify wording and PR regression fixtures | same-slice dependency | Producer and consumer descriptions must not conflict. |
| Regenerate supported adapter packages through existing tooling | same-slice dependency | Published skills must remain coherent. |
| Introduce stored intermediate revision identities | out of scope | The final handoff can be derived without a new schema. |
| Add a fixed maximum number of evidence commits | out of scope | Commit count is not the protected safety property. |
| Permit post-review product, specification, architecture, plan, dependency, configuration, test, or generated-output changes | out of scope | Those changes require the owning review and fresh Verify. |
| Rewrite or squash contributor history | out of scope | Additive evidence should remain auditable and recoverable. |
| Change remote mutation, refresh, CI, draft, or PR-state behavior | out of scope | Those existing PR safety contracts remain valid. |

## Governing principle

> Protect the reviewed product boundary, not a particular number of evidence commits.

## Proposed direction

Replace the exact one-direct-child rule with a proportional evidence-tail rule:

```text
reviewed product revision
        ↓
zero or more contiguous review, workflow, and verification evidence changes
        ↓
local handoff revision = pushed remote head = PR head
```

The PR skill should accept a handoff descendant of the verified subject when the cumulative post-review change is limited to current, attributable lifecycle evidence. Ordinary permitted evidence includes final Code Review records and closeout, workflow transition requests and matching change-local state, and the final Verify report and registration.

The skill should not reject an otherwise valid suffix because it contains multiple commits, because a permitted evidence record belongs to Code Review or Workflow rather than Verify, or because the handoff is not the verified subject's direct child.

The suffix remains bounded. Any post-review change to implementation, tests, specifications, architecture, plans, dependencies, configuration, generated product output, public documentation outside the governed evidence pack, or another decision-bearing surface invalidates PR opening readiness and routes to the relevant owner. Unknown, mixed, stale, conflicting, missing, or unattributable evidence also blocks. The existing successful Verify report, clean review closeout, lifecycle consistency, remote-base checks, safe push rules, and final PR read-back remain required.

Validation should evaluate the final reviewed-to-handoff diff and current evidence identities. It need not impose a fixed commit count, store another revision identity, require history rewriting, or reject harmless evidence based only on intermediate commit boundaries.

## Feasibility

**Assessment: feasible.** The current package already distinguishes the verified subject, handoff revision, evidence tail, and invalidating paths. The correction primarily changes the acceptance predicate from an exact direct-child/single-commit topology to a content-and-authority predicate over the reviewed-to-handoff suffix.

Implementation can reuse the existing `pr` package, Verify report, governed readiness reference, Git inspection, skill validators, static fixtures, adapter generation, and release parity checks. No new service, dependency, lifecycle state, persistent transaction record, or host API is required. Design must define the exact evidence categories and fail-closed treatment of mixed or unknown changes without turning repository-maintainer paths into published customer-project assumptions.

## Impact and major trade-offs

This direction makes valid governed PR handoff composable with the lifecycle that produces its evidence and removes pressure to squash or bypass normal records. It also makes the safety argument more semantic: reviewers and agents must distinguish evidence-only changes from product or governing changes rather than relying on commit count as a shortcut.

That judgment must remain constrained by closed evidence categories, current artifact identities, and conservative failure behavior. A path-only allowlist would be too permissive for mutable change records, while a field-perfect parser in the public skill would be too repository-specific. Design should combine bounded path categories, authoritative lifecycle validation, current Verify registration, and explicit invalidating surfaces.

Historical reports and merged PRs remain historical evidence. Current invocations adopt the refined rule; the change does not reinterpret old readiness results or reopen completed PRs.

## Decision requested

Approve replacing the single-direct-child Verify-commit exception with a contiguous evidence-only suffix whose safety is determined by current content and authority rather than commit count. Approval keeps all existing remote, verification, review-closeout, CI, mutation, and read-back protections; permits only attributable review, workflow, and Verify evidence after the reviewed product; and requires any product, governing, unknown, mixed, or stale change to return to its owner.

Approval does not authorize post-review product changes, history rewriting, a new revision schema, a new lifecycle stage, or broader PR automation.
