# Delivery Review recording and settlement

Load for every durable or formal Delivery Review. The parent skill owns judgment, outcome, findings, isolation, and handoff; this reference owns durable recording and exact-package CLI settlement.

## Recording

Resolve the exact change and package from bounded CLI context. For `compact-current-state-v1`, replace the stable current review at `docs/changes/<change-id>/reviews/delivery-review.md`; keep open findings there, and retain only continuing material constraints in `material-decisions.md`. Submit one transient semantic operation with the expected complete-set revision and identities. For registered historical contracts, retain their round-suffixed review, `review-log.md`, and triggered `review-resolution.md` behavior. If placement or identity is ambiguous, report recording blocked without weakening findings.

The record binds package kind `delivery`, the exact member ID-to-path map, approved Design Review ID, Delivery Review ID and round, reviewer authority, outcome, findings, correction targets, and evidence path. Under v3 the member map contains exactly the registered primary plan. Historical packages remain readable without current authority. The record contains no aggregate revision or content hash.

## CLI settlement

For registered historical contracts, submit `record-package-review`, refresh context, then submit `settle-review-package` for the same package and review identity. For compact changes, submit the compact stable-review operation once; the evaluator records the outcome and derives progression together. Only `approved` grants package authority; all other outcomes remain visible and withhold progression. The CLI validates consistency and does not authenticate or grant reviewer permission.

An exact replay is idempotent. Stale lifecycle revision, changed member map, wrong upstream review, mismatched evidence, or failed atomic mutation stops unchanged. Never edit `change.yaml` settlement fields directly.

## Isolation

Settlement does not advance routing. A direct invocation stops after recording and any authorized settlement. Workflow-managed execution returns control to `route`, which alone chooses continuation or correction routes.
