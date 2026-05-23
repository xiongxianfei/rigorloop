# Proposal Review R1

Review ID: proposal-review-r1
Stage: proposal-review
Round: 1
Reviewer: Contributor proposal-review
Target: docs/proposals/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later.md
Status: changes-requested

## Review inputs

- Proposal: `docs/proposals/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later.md`
- User-supplied proposal-review result in chat on 2026-05-23
- Governing boundaries: `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`

## Result

- Material findings: `VIC-PR1`, `VIC-PR2`, `VIC-PR3`, `VIC-PR4`, `VIC-PR5`
- Recording status: recorded after initial chat-only blocker was resolved
- Recording blocker: none
- Review record: `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/reviews/proposal-review-r1.md`
- Review log: `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/review-log.md`
- Review resolution: `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/review-resolution.md`
- Open blockers: none after proposal revision
- Immediate next stage: proposal revision, then proposal-review R2
- No automatic downstream handoff: this review does not start spec, test-spec, plan, or implementation.

## Overall verdict

Good direction, changes requested before spec.

The proposal has the right core decision: lead with validation idempotency/caching and defer edit-scoped validation. The review requested sharper first-slice contract boundaries before downstream spec reliance.

## Findings

### VIC-PR1 - Workstream B is still too close to the first implementing spec

Finding ID: VIC-PR1
Severity: major
Location: `Scope budget`, `Acceptance criteria`, `Next artifacts`, proposal title
Evidence: Workstream B was marked as a separate proposal, while next artifacts still named a combined validation idempotency and edit-scoped validation spec, and acceptance criteria included Workstream B checks.
Required outcome: Make the first spec strictly Workstream A and keep Workstream B as context and follow-on criteria.
Safe resolution: Revise the proof route and next artifacts so the first spec covers validation idempotency/cache hits only, and move Workstream B criteria into a follow-on gate.

### VIC-PR2 - Cache storage and formal cache-hit evidence need a first-slice decision

Finding ID: VIC-PR2
Severity: major
Location: `Workstream A`, `Open questions`
Evidence: The proposal left cache record location open, with only a candidate of untracked local cache plus change-local evidence.
Required outcome: Decide that cache execution state may be local/untracked, but any cache hit used as formal workflow evidence is recorded in change-local evidence.
Safe resolution: Add a cache storage decision separating local execution cache from change-local cache-hit evidence.

### VIC-PR3 - The first cacheable validator/input-surface pilot is not chosen

Finding ID: VIC-PR3
Severity: major
Location: `First-slice boundary`, `Open questions`
Evidence: The proposal allowed one or two validators and left the first validator undecided between `validate-change-metadata.py` and `validate-artifact-lifecycle.py`.
Required outcome: Choose a conservative first validator, or require an input-surface audit gate before implementation.
Safe resolution: Start with `validate-artifact-lifecycle.py --mode explicit-paths`, only for explicit-path invocations.

### VIC-PR4 - Validator implementation identity is too loose

Finding ID: VIC-PR4
Severity: major
Location: `Cache key`
Evidence: The cache key allowed a hash of validator code and helper modules, or a conservative version stamp.
Required outcome: Replace optional version-stamp language with a deterministic implementation manifest for the first slice.
Safe resolution: Require a manifest covering the entrypoint, repository-local imports, shared semantics/parser modules, and policy/config/spec files.

### VIC-PR5 - Closeout full-bundle enforcement is stated but not made mechanically checkable

Finding ID: VIC-PR5
Severity: major
Location: `Stage-closeout gate`, `Acceptance criteria`
Evidence: The proposal said closeout bundles should not be replaced by cache hits, but did not say what rejects a closeout that only records cache hits.
Required outcome: Define the closeout enforcement surface.
Safe resolution: Require actual validator execution evidence for closeout, define cache-hit evidence as inner-loop only, and add acceptance criteria for closeout-only cache-hit rejection.

## Review dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | The proposal clearly identifies repeated validation as a different risk class from output compaction. |
| User value | pass | Reduces repeated validation work while preserving safety if scoped correctly. |
| Option diversity | pass | The proposal compares do nothing, self-declared narrowing, diff-derived narrowing, caching first, and staged caching plus later narrowing. |
| Decision rationale | pass | Caching first is the right recommendation. |
| Scope control | concern | Workstream B remains too present in the first spec/test acceptance surface. |
| Architecture awareness | concern | Cache storage, implementation identity, and first validator choice need sharper decisions. |
| Testability | concern | Closeout enforcement and helper-module invalidation need explicit tests. |
| Risk honesty | pass | The proposal names stale cache, skipped defects, failed-result reuse, self-declared edit classes, and mixed edits. |
| Rollout realism | concern | The rollout should choose one pilot validator and one cache evidence model before implementation. |
| Readiness for spec | changes-requested | Direction is good; fix the five findings first. |

## Recommended next stage

Revise the proposal to resolve `VIC-PR1`, `VIC-PR2`, `VIC-PR3`, `VIC-PR4`, and `VIC-PR5`, then rerun proposal-review before downstream spec reliance.
