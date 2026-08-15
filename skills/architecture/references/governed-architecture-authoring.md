# Governed architecture authoring

Load only for `AA2-governed-authoring`. The parent owns universal policy and the package method owns architecture content quality.

## Authority and assessment basis

Read the complete current `change.yaml`. Require `lifecycle_contract: stage-owned-change-local-v1`, exact change and paths, settled inputs, legal authority, and one current `architecture-required` assessment receipt. Bind receipt ID, exact spec identity, approving spec-review identity, and decision basis; missing, stale, contradictory, `not-required`, or `ambiguous` basis blocks.

Bind each target's artifact ID, kind, role, normalized path, and operation. Create only absent targets, revise matching identities, and supersede/deprecate only with authority and impact handling. Never select by kind alone or change another entry, `workflow_state`, routing, automation, or downstream state.

## Prepared manifest

Before the first target-file mutation, validate content and durably record one ordered manifest in existing authoring evidence. Bind transaction, change, assessment, inputs, baseline, targets, operations, current and intended file identities, paths, dependency edges, commit groups, independent-validity result, transition, and evidence path.

Evidence state is `prepared`, `partial-blocked`, `complete`, or `abandoned`; batch result is `complete`, `partial-blocked`, or `blocked-before-write`. If existing evidence cannot represent manifest, progress, dependencies, and groups without new schema, authority, persistence, or owner, stop and return `architecture-required` rather than weaken recovery.

After recording `prepared`, re-read authority, assessment, inputs, target entries, and file baselines. Any drift stops before mutation.

## Dependencies, writes, and commit points

A target commits only after dependencies and only when the partial state is independently structurally and semantically valid. Coupled targets share a commit group.

Write diagrams and subordinate sources before canonical Markdown, the target commit point. For ADR supersession, validate the replacement, then update predecessor status/link, then canonical references. Authoring proposes; architecture-review approves.

Before a target write, set only its entry to `authoring`, clear its authorized review, and point `authoring_evidence` to this transaction. Record progress there; complete content and evidence move only that entry to `review-required`.

All targets yield `complete`. Failure preserves independently valid targets as `partial-blocked`; otherwise retain prepared evidence as `blocked-before-write`. Canonical Markdown never references incomplete dependencies.

## Retry and recovery

An identical retry requires the same transaction, assessment, inputs, manifest, paths, operations, baselines, identities, dependencies, groups, and authority. Resume once, reconcile only listed files, and avoid duplicate evidence or transitions.

An unrecorded file, changed basis, conflicting or ambiguous entry, dependency drift, unrelated content, unsafe partial group, or concurrent write stops without adoption or overwrite. Interrupted completed targets remain only when the manifest proves independent validity; otherwise route exact reconciliation to the governing owner.

## Result

Report manifest identity and state, assessment basis, each target operation and progress, dependencies and commit groups, entry states before and after, batch result, blockers, preserved partial state, and architecture-review eligibility. Only a complete required manifest is eligible for review handoff.
