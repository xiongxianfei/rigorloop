# Proposal Review R1

Review ID: proposal-review-r1
Stage: proposal-review
Round: 1
Reviewer: Codex proposal-review
Target: docs/proposals/2026-05-09-simplify-architecture-skill-surfaces.md
Status: revise

## Review inputs

- Proposal: `docs/proposals/2026-05-09-simplify-architecture-skill-surfaces.md`
- Governance: `CONSTITUTION.md`, `VISION.md`
- Related spec: `specs/architecture-package-method.md`
- Related ADR: `docs/adr/ADR-20260428-architecture-package-method.md`

## Findings

### PASS-F1 - ADR amendment path is ambiguous

Finding ID: PASS-F1
Severity: material
Evidence: The proposal says an "ADR amendment is warranted" and that the later change should "amend the existing architecture-package-method ADR." The existing ADR is already accepted, and it currently records change-local architecture deltas as part of the method. The approved spec says accepted or active ADRs are append-only for decision history and later changes must supersede or deprecate an old ADR with a new ADR or explicit lifecycle update rather than rewriting old decisions as if they had always been different.
Required outcome: Clarify that the later architecture work creates a new ADR that amends or narrows `ADR-20260428-architecture-package-method`, while preserving the existing accepted ADR as decision history and not fully superseding the whole C4 plus arc42 plus ADR method.
Safe resolution: Revise the proposal's architecture impact, decision log, and next artifacts from "ADR amendment" to "new ADR amending/narrowing `ADR-20260428-architecture-package-method`"; state that the existing ADR may receive only an explicit lifecycle cross-reference if the later spec/ADR contract requires it.

## Review dimensions

| Dimension | Result | Notes |
|---|---|---|
| Problem clarity | pass | The proposal states the issue as architecture deltas becoming a normal surface and attracting unsettled direction. |
| User value | pass | The benefit is concrete: clearer artifact ownership, less temporary architecture work, and more portable public skill guidance. |
| Option diversity | pass | It compares keeping the model, making deltas rare, routing uncertainty away from architecture, and using ADRs only. |
| Decision rationale | concern | The main direction follows from the options, but PASS-F1 needs a precise ADR path. |
| Scope control | pass | Non-goals preserve C4, arc42, ADRs, proposal/spec review, and legacy normalization boundaries. |
| Architecture awareness | concern | The proposal names the touched spec, skills, workflow guidance, generated outputs, and ADR, but PASS-F1 must sharpen the ADR update path. |
| Testability | pass | Expected behavior is specific enough to map into `specs/architecture-package-method.test.md`. |
| Risk honesty | pass | Risks include skipped architecture work, premature canonical updates, ADR overuse, and stale tests/docs. |
| Rollout realism | pass | Rollout sequences spec, skills, generated outputs, adapter checks, and rollback. |
| Readiness for spec | revise | Ready after PASS-F1 is resolved. |

## Vision fit review

Pass. The proposal includes `Vision fit` with the exact allowed value `fits the current vision`, and root `VISION.md` exists.

## Standing artifact gate review

Pass. `VISION.md` and `CONSTITUTION.md` exist, and this is not bypassing a bootstrap gate.

## Recommended next stage

Revise the proposal to resolve PASS-F1, then rerun proposal-review before downstream spec authoring relies on it.
