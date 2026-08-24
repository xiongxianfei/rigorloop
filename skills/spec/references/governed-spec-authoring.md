# Governed spec authoring

Load for `single-governed-candidate`; the parent owns contract quality and this reference owns the governed write boundary.

## CLI-bound authoring

Run `rigorloop lifecycle context spec --change <change-id> --format json`. Require one supported governed change, settled applicable proposal, exact target or unambiguous creation path, legal authority, and no blocker. Capture the current target digest before revision.

Write only the specification and evidence containing `Artifact path`, `Artifact identity`, and `Authoring result: complete`. Creation requires no conflicting primary spec. Revision requires exact prior identity plus current finding, upstream-change, reopen, or user authority. Preserve historical evidence; route downstream reliance or unsafe partial authoring to workflow rather than repairing lifecycle state.

After content and evidence validation, refresh context and submit `record-artifact-revision` with the returned lifecycle revision, exact artifact ID, `artifact_kind: spec`, role, path, evidence path, `stage_authority: spec`, and prior digest for revision. The CLI derives `review-required` and invalidates registrations tied to the replaced identity. Never edit `change.yaml` lifecycle fields directly.

Treat `already-recorded` as success. Stop on stale context, identity or path mismatch, competing primary, invalid authority, rejected registration, or ambiguous recovery. Do not mutate workflow, review, routing, automation, or another artifact.

## Result

Report operation, paths, identities, CLI result, blockers, and `spec-review` handoff without claiming settlement or downstream readiness.
