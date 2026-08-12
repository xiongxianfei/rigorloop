# Proposal Review R3: Proposal-Review Skill Simplification

Review ID: proposal-review-r3
Stage: proposal-review
Round: r3
Reviewer: user-supplied independent proposal-review
Target: docs/proposals/2026-08-11-proposal-review-skill-simplification.md
Reviewed artifact: `docs/proposals/2026-08-11-proposal-review-skill-simplification.md` at commit `ea4785fa`
Status: changes-requested
Review date: 2026-08-11
Recording status: recorded

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: PRRSIM-PR1, PRRSIM-PR2, PRRSIM-PR3
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-08-11-proposal-review-skill-simplification/reviews/proposal-review-r3.md
- Review log: docs/changes/2026-08-11-proposal-review-skill-simplification/review-log.md
- Review resolution: docs/changes/2026-08-11-proposal-review-skill-simplification/review-resolution.md
- Open blockers: recording modes, advisory location authority, and result-asset applicability require proposal revision
- Immediate next stage: proposal revision

## Material Findings

### Finding PRRSIM-PR1

Finding ID: PRRSIM-PR1
Severity: major
Location: Recording-and-settlement reference; closed resource assemblies
Evidence: One broad `durable_recording_context` covers formal reviews, material or blocking outcomes, and explicit durable requests while the reference also owns formal settlement, automated review packets, correction boundaries, and workflow-managed handoff. The proposal separates loading from authority but does not close ordinary advisory, advisory durable, formal manual, and formal automated operational modes or their writes.
Required outcome: Define independent recording and automation modes, exhaustive durable-record triggers including `changes-requested`, `blocked`, and `inconclusive`, valid and invalid combinations, and exact record, settlement, automation, correction, and handoff permissions.
Safe resolution path: Use `none`, `advisory-durable`, and `formal-lifecycle` recording modes plus `manual` and `workflow-managed-automated` execution modes; keep one reference with internal mode-specific sections; allow automation only with current formal authority.
needs-decision rationale: none; the mode axes close authority without changing the selected package design.

### Finding PRRSIM-PR2

Finding ID: PRRSIM-PR2
Severity: major
Location: Material advisory review; recording-and-settlement reference
Evidence: A material advisory review requires detailed durable finding evidence but may have no existing governed change root, explicit record path, inferable change identity, or configured advisory location. Implicitly creating `docs/changes/<new-id>/` would convert isolated review into unauthorized lifecycle creation.
Required outcome: Define deterministic advisory location resolution, prohibit implicit governed-root creation, preserve required change-local material-finding records when an existing root is available, and specify blocked recording and formal-root prerequisites.
Safe resolution path: Resolve an explicit path, existing owning root, matching active root, or explicit project advisory location in order; otherwise emit the complete finding with `recording status: blocked`, no settlement, and no handoff. A formal review must have a valid governed root before claiming completion.
needs-decision rationale: none; repository governance already distinguishes required recording from lifecycle settlement authority.

### Finding PRRSIM-PR3

Finding ID: PRRSIM-PR3
Severity: major
Location: Output ownership; result asset
Evidence: `PRR0`, `PRR0G`, `PRR1`, `PRR1G`, and formal automated review produce different evidence, but the proposal only says to omit inapplicable fields. Without closed groups, policy may leak into the asset or profile-specific structures may be recreated inline.
Required outcome: Define one core result group and specialized-gate, durable-recording, formal-settlement, and automated-review conditional groups, with exact applicability, blocked-data, omission, and placeholder rules.
Safe resolution path: Let the asset own group order, labels, tables, and placeholders only; let `SKILL.md` and references select groups and govern status, settlement, correction, and handoff.
needs-decision rationale: none; the existing result and finding assets remain sufficient.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | Common-path overload and duplicated ownership are concrete. |
| User value | pass | Ordinary advisory review should load less irrelevant procedure. |
| Option diversity | pass | Alternatives are materially different. |
| Decision rationale | pass | Two references remain proportionate. |
| Scope control | pass | Work remains bounded to `proposal-review` and directly coupled surfaces. |
| Architecture awareness | pass | The existing packaged-skill model likely covers the change. |
| Testability | block | Recording modes, advisory location authority, and result groups are not closed enough for deterministic fixtures. |
| Risk honesty | concern | Unauthorized side effects and structural policy leakage need explicit prevention. |
| Rollout realism | pass | Static proof and package parity remain appropriate. |
| Readiness for spec | block | PRRSIM-PR1 through PRRSIM-PR3 require proposal-level closure. |

## Scope Preservation Review

- Scope-preservation result: pass. The central two-reference direction and original goals remain intact.
- Scope-budget result: pass. The findings close existing package behavior and do not introduce another reference, asset, runtime, or architecture model.
- Vision-fit result: pass. The proposal remains aligned with the current vision.

## Recommended Proposal Edits

- Recommended edits: add closed recording and automation mode matrices; add deterministic advisory location and blocked-recording rules; define the result asset's core and four optional groups; state that specialized-gate semantic classification remains review-owned.

## Recommendation

- Recommendation: changes requested. Resolve `PRRSIM-PR1` through `PRRSIM-PR3`, validate the revised proposal and lifecycle artifacts, and perform independent proposal review again.
- No automatic downstream handoff follows this review.
