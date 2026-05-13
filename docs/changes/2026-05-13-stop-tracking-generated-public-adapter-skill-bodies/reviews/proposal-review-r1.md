# Proposal Review R1

Review ID: proposal-review-r1
Stage: proposal-review
Round: 1
Target: docs/proposals/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies.md
Reviewed artifact: docs/proposals/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies.md
Review date: 2026-05-13
Reviewer: Codex proposal-review
Recording status: recorded
Status: changes-requested

## Outcome

- Review status: changes-requested
- Material findings: PAU-R1
- Blocking findings: none

## Scope Checked

Reviewed the proposal against `CONSTITUTION.md`, `VISION.md`, the accepted single-authored-source direction, the accepted public adapter artifact migration direction, and the published `v0.1.2` release precondition recorded in the proposal.

## Review Dimensions

| Dimension | Result | Notes |
|---|---|---|
| Problem clarity | pass | The proposal states the remaining problem: generated public adapter skill bodies remain tracked after `v0.1.2` shipped archive installation. |
| User value | pass | The user value is concrete: less duplicate generated diff noise, clearer source ownership, and release-archive install continuity. |
| Option diversity | pass | The options distinguish keeping tracked output, untracking in `v0.1.3`, main cleanup before release, and waiting another compatibility release. |
| Decision rationale | pass | Choosing `v0.1.3` follows from the user's release request and the satisfied `v0.1.2` compatibility window. |
| Scope control | pass | The proposal excludes PR #51 redo work, skill-validator migration, high-cost skill optimization, and new token threshold gates. |
| Architecture awareness | concern | The proposal names release, packaging, validation, and benchmark boundaries, but misses root guidance surfaces that currently encode the old adapter install/tracking contract. See PAU-R1. |
| Testability | pass | The proposal names temp-output adapter validation, tracked-body absence, release notes, token benchmark source validation, and release verification. |
| Risk honesty | pass | The proposal names user install confusion, validation drift, benchmark-source regression, stale docs, and incomplete release evidence. |
| Rollout realism | concern | Rollout is plausible, but it must include source-of-truth guidance updates because `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md` currently describe the compatibility-window model. See PAU-R1. |
| Readiness for spec | concern | The direction is ready, but the proposal should be revised before spec so the spec does not inherit a stale root-guidance gap. |

## Scope Preservation

Pass. The proposal classifies the user's current goals, including `v0.1.3` release work as in scope and deferred work as follow-up.

## Vision Fit

Pass. The proposal uses the allowed value `fits the current vision`, and the direction aligns with `VISION.md` by reducing duplicate generated review surfaces and making release evidence more traceable.

## Material Findings

### PAU-R1 - Root guidance update obligation is missing

Finding ID: PAU-R1

Severity: major

Location: `docs/proposals/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies.md`, `Architecture impact`, `Goals`, and `Testing and verification strategy`

Evidence: The proposal says the `v0.1.3` release will remove tracked generated public adapter skill bodies and make archive installation the public distribution path. `CONSTITUTION.md` currently says contributors install or copy public Codex adapter output from `dist/adapters/codex/.agents/skills/` into `.codex/skills/`, and that public adapter packages under `dist/adapters/` remain tracked generated installable output during the compatibility window. The proposal does not list `CONSTITUTION.md`, `AGENTS.md`, or `docs/workflows.md` among affected surfaces or required guidance updates.

Required outcome: Revise the proposal before spec/plan so the `v0.1.3` release scope explicitly includes updates to root contributor and workflow guidance affected by retiring tracked public adapter skill bodies, or records why a higher-priority source makes those updates unnecessary.

Safe resolution path: Add a proposal section or revise Architecture impact / Goals / Testing to require updating affected root and workflow guidance in the same release slice, including `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md` when their current wording would become stale. Then rerun proposal-review.

## Open Questions

- Should `CONSTITUTION.md` be amended in `v0.1.3` to replace the compatibility-window tracked-output rule with the archive-install rule, or should it retain compatibility-window history with a version-qualified note?
- Should `AGENTS.md` and `docs/workflows.md` point ordinary contributors at release archives directly, or at `dist/adapters/README.md` as the install-contract surface?

## Readiness

Changes requested before spec/plan. This is an isolated proposal-review result with no automatic downstream handoff.
