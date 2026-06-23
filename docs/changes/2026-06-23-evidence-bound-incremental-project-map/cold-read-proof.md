# Cold-Read Proof

Change: `2026-06-23-evidence-bound-incremental-project-map`

Milestone: M3. Representative Output and Preservation Evidence

Status: recorded

No deferral is recorded for M3.

## Scope

This proof records a manual cold-read exercise against three representative
repository shapes. It is evidence that the revised `project-map` skill and
skeleton are usable without relying on chat-only memory or building a broad
project-map artifact validator.

## Small repository

Fixture shape:

- `package.json`
- `src/server.ts`
- `src/routes/index.ts`
- `src/db/schema.sql`
- `.github/workflows/ci.yml`
- `tests/accounts.test.ts`

Cold-read route:

1. Read the skill workflow role, operating modes, metadata contract, evidence classes, and skeleton resource-map entry.
2. Inspect the listed source, schema, test, and CI paths.
3. Select `create` mode and `repository` scope.

Result: root map only.

Reason: the API content fits in the root map summary and the area does not yet exceed roughly a screen of content in the root map. There is no separate deploy or release lifecycle that requires an area map.

Proof points:

- Baseline uses commit plus dirty marker when the working tree has inspected uncommitted paths.
- The map records `Configured command` for `npm test` without claiming it passed.
- Runtime flow is statically traced.
- Data flow is demonstrated by tests where tests exist and partially inferred where runtime writes are not observed.

## Monorepo or multi-service fixture

Fixture shape:

- `apps/api/package.json`
- `apps/api/src/server.ts`
- `apps/web/package.json`
- `apps/web/src/main.tsx`
- `packages/domain/src/accounts.ts`
- `infra/terraform/main.tf`
- `.github/workflows/api-release.yml`
- `.github/workflows/web-release.yml`

Cold-read route:

1. Read the root skeleton and area-map contract.
2. Inspect top-level package, app, shared package, infrastructure, and release workflow boundaries.
3. Select `area` mode for the API service while preserving a concise root map.

Result: root map plus area map.

Reason: `apps/api/` has a durable runtime entry point, package manifest, focused release workflow, and service boundary. The root map registers `docs/project-map/api.md`; the API area map names `docs/project-map.md` as parent.

Proof points:

- Root registration table contains Area, Map, Scope, Baseline, Freshness, and Known gaps columns.
- The area map owns detailed API runtime flow.
- The root map links to the API area map rather than duplicating detailed route descriptions.
- Overlap with `packages/domain/` is named; API owns delivery flow, while the root map owns shared package placement.

## Intentionally stale map

Fixture shape:

- Existing `docs/project-map.md` cites `src/routes/index.ts`.
- Current source moved route registration to `src/http/routes.ts`.
- Existing map also said billing routes were registered at the previous baseline, but the previous file only registered account routes.

Cold-read route:

1. Compare cited map paths to current source.
2. Distinguish changed source from wrong-at-baseline content.
3. Select `refresh` mode if rewriting is requested, or `audit` mode if only reporting drift.

Result: stale map plus correction note.

Reason: the cited path changed, so freshness is stale. The billing-route claim was wrong at the previous baseline, so the evidence includes a correction note rather than treating it only as stale.

Proof points:

- The stale case records the changed cited path and affected section.
- The correction note states that prior reliance on the affected section was unsafe.
- The map does not invent a billing runtime surface from an accepted proposal or plan.
- Downstream architecture must inspect current source directly before relying on the route boundary.

## Conclusion

The revised skill remains usable from a cold read across small, multi-service, and stale-map cases. The proof supports M3 only: it does not claim generated adapter inclusion, final verification, branch readiness, PR readiness, or lifecycle closeout.
