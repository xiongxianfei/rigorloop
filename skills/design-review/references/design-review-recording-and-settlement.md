# Design Review recording and settlement

Load for every durable or formal Design Review. The parent skill owns judgment, outcome, findings, isolation, and handoff; this reference owns durable recording and exact-package CLI settlement.

## Recording

Resolve the exact change and package from `rigorloop lifecycle context design-review --change <change-id> --format json`. Record a clean receipt or detailed review at `docs/changes/<change-id>/reviews/design-review-r<n>.md`, update `review-log.md`, and use `review-resolution.md` only when material findings or dispositions require it. If placement or identity is ambiguous, report recording blocked without weakening findings.

The record binds package kind `design`, the exact member ID-to-path map, accepted Proposal Review ID, Design Review ID and round, reviewer authority, outcome, findings, correction targets, and evidence path. It contains no aggregate revision or content hash.

## CLI settlement

Submit `record-package-review` through the existing lifecycle CLI with the current lifecycle revision, `stage_authority: design-review`, and the exact recorded data. Refresh `context design-review`, then submit `settle-review-package` for the same package and review identity. The CLI derives authority: only `approved` grants package authority; all other outcomes remain visible and withhold progression.

An exact replay is idempotent. Stale lifecycle revision, changed member map, wrong upstream review, mismatched evidence, or failed atomic mutation stops unchanged. Never edit `change.yaml` settlement fields directly.

## Isolation

Settlement does not advance routing. A direct invocation stops after recording and any authorized settlement. Workflow-managed execution returns control to `route`, which alone chooses continuation or correction routes.
