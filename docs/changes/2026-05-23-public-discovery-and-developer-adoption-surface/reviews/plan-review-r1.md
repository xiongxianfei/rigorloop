# Plan Review R1: Public Discovery and Developer Adoption Surface

Review ID: plan-review-r1
Stage: plan-review
Round: 1
Reviewer: Codex plan-review skill
Target: docs/plans/2026-05-23-public-discovery-and-developer-adoption-surface.md
Status: changes-requested

Reviewed artifact: docs/plans/2026-05-23-public-discovery-and-developer-adoption-surface.md
Review date: 2026-05-23
Recording status: recorded

## Result

- Skill: plan-review
- Review status: changes-requested
- Material findings: DXA-PLAN1
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-05-23-public-discovery-and-developer-adoption-surface/reviews/plan-review-r1.md
- Review log: docs/changes/2026-05-23-public-discovery-and-developer-adoption-surface/review-log.md
- Review resolution: docs/changes/2026-05-23-public-discovery-and-developer-adoption-surface/review-resolution.md#plan-review-r1
- Open blockers: DXA-PLAN1
- Immediate next stage: plan revision

## Review Dimensions

| Dimension | Result | Notes |
|---|---|---|
| self-contained context | pass | The plan names the proposal, approved spec, spec review, existing README positioning spec, current drift, primary files, and required proof artifacts. |
| source alignment | pass | Milestones trace to `DXA-R*` requirements and keep runtime behavior, workflow semantics, skills, adapters, validators, and release archive boundaries out of scope. |
| milestone size | concern | M1 combines baseline proof, version proof, README ownership proof, and live GitHub repository metadata mutation; the mutation part has a different permission and rollback profile. |
| sequencing | concern | M1's live metadata update can block M2 and M3 even though README/package tracked work can proceed after recording a permission blocker or deferring external metadata mutation. |
| scope discipline | pass | The plan excludes website, GIF/video, off-platform promotion, analytics, runtime changes, workflow semantic changes, and unsupported adoption claims. |
| validation quality | pass | The plan names concrete repo validators, package tests, stale-version sweeps, manual link review, cold-read review, and unsupported-claim sweep. |
| TDD readiness | pass | The plan routes to test-spec after plan-review unless plan-review explicitly says otherwise, which is appropriate for this proof-heavy documentation change. |
| risk coverage | concern | GitHub metadata permission risk is named, but the milestone structure turns that risk into a broad sequencing blocker instead of isolating it. |
| architecture alignment | pass | Architecture is correctly marked not required because no runtime data flow or boundary changes are planned. |
| operational readiness | concern | External repository settings need a small isolated update/proof path so lack of GitHub settings permission does not prevent all tracked README/package work. |
| plan maintainability | pass | The plan has clear handoff state, milestone states, validation notes, risks, dependencies, and recovery paths. |

## Findings

### DXA-PLAN1 - Isolate external GitHub metadata mutation from tracked adoption-surface implementation

Finding ID: DXA-PLAN1
Severity: major
Location: `docs/plans/2026-05-23-public-discovery-and-developer-adoption-surface.md`, M1 and Current Handoff Summary
Evidence: M1 goal says to "Set or prepare the external repository metadata decision" and its steps include "Set the approved description and topic list"; M1 also gates M2 and M3 through dependencies on M1 proof. The same milestone depends on "Maintainer account permission to update GitHub repository metadata." If that permission is missing, the plan's first milestone blocks README and package README changes even though those tracked changes can proceed with a recorded metadata blocker.
Required outcome: Revise the plan so live GitHub metadata mutation is isolated from baseline evidence and tracked README/package implementation. The plan must make clear which work can proceed if repository-settings permission is unavailable and which acceptance criteria remain blocked until metadata is actually changed.
Safe resolution path: Split M1 into a baseline/proof milestone and a separate metadata-setting milestone, or revise M1 so it records before-state, approved target metadata, permission status, and blocker/defer evidence while moving the actual live metadata update to its own milestone or explicit dependency. Update Current Handoff Summary, Requirements covered, milestone dependencies, validation plan, and risks so M2/M3 can proceed after baseline proof even if live metadata mutation remains blocked. Do not claim `AC-DXA-001` through `AC-DXA-003` complete until after-state metadata proof exists.
needs-decision rationale: none

## Recommended Plan Edits

- Separate the permission-sensitive GitHub settings update from the baseline proof work.
- Keep `repository-metadata-proof.md` as the durable source for approved target values, before-state, after-state when available, permission context, and any blocker.
- Ensure M2 and M3 depend on version proof and README ownership proof, not on successful live GitHub metadata mutation.
- Preserve final closeout blocking on `AC-DXA-001` through `AC-DXA-003` until live metadata after-state proof exists.

## Recommendation

Changes requested. Revise the plan, then rerun `plan-review`.

No automatic downstream handoff occurred.
