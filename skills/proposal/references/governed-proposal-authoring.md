# Governed proposal authoring

Load only for `governed_proposal_candidate_context`. The parent owns proposal judgment; this reference owns the governed write boundary.

## CLI-bound authoring

Run `rigorloop lifecycle context proposal --change <change-id> --format json`. Require one supported governed change, legal proposal authority, settled inputs, an exact target or unambiguous creation path, and no blocker. Capture the current target identity before revising.

If context returns `RL_WORKFLOW_ROUTE_REQUIRED`, do not author or mutate state. Return its route facts to workflow and resume only after context makes `record-artifact-revision` immediately available.

Author only the proposal and its authoring evidence. The proposal itself contains no status, ownership pointer, lifecycle identity, or reverse link. Creation requires an absent entry and non-conflicting path. Revision requires the exact current governed entry and explicit revision authority; downstream reliance first routes to workflow impact handling. Preserve history and every unrelated artifact.

After writing and validating both files, refresh context and submit `record-artifact-revision` with the returned lifecycle revision, exact artifact ID, `artifact_kind: proposal`, role, path, evidence path, `stage_authority: proposal`, and the captured prior digest for revision. The CLI derives `review-required`, invalidates replaced evidence, and changes only the matching entry. Never edit lifecycle fields directly.

An `already-recorded` result is success. Any stale revision, identity mismatch, conflict, unsupported partial authoring, or rejected operation stops without adoption or routing. Workflow owns recovery and continuation; proposal authoring never settles review or changes workflow state.

## Result

Report artifact and evidence paths, creation or revision, CLI result, blockers, and `proposal-review` handoff. Do not claim settlement or downstream readiness.
