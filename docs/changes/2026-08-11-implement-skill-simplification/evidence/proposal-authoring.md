# Proposal Authoring Evidence: Implement Skill Simplification

Stage: proposal
Date: 2026-08-11
Artifact: `docs/proposals/2026-08-11-implement-skill-simplification.md`

## Initial intent

The user selected `implement` as the next skill-optimization target and requested a new branch, a proposal, and formal proposal review.
The initial exploration favored conditional workflow guidance, one output asset, and a consolidated universal common path while preserving implementation rigor.
Proposal-review R1 then required profile-specific loaded-context proof and a proposal-level decision separating ordinary planned milestones from armed automation.
The user-supplied proposal-review R3 further required a closed profile lattice, one asset with conditional structural groups, and separate semantic-rule and literal-compatibility evidence.

## Evidence used

- `VISION.md` and `CONSTITUTION.md` for project fit, traceability, skill-source, compatibility, and verification boundaries.
- `AGENTS.md` and `docs/workflows.md` for change-local lifecycle and artifact placement.
- `docs/project-map.md` for current canonical skill, validation, adapter, and CI boundaries.
- `skills/implement/SKILL.md` as the complete authored target.
- `docs/proposals/2026-08-10-code-review-skill-simplification.md` and its final evidence as the related completed optimization pattern.
- `docs/architecture/system/architecture.md` and `specs/skill-contract.md` for the existing published-skill package model.
- `python scripts/measure-skill-tokens.py --skills-root skills` for the 395-line and 5,977-estimated-token baseline; `wc` supplied the 3,338-word count.

## Scope decisions

- The proposal covers only the published `implement` package and directly required structural and package proof.
- Optimizing `workflow` or establishing a cross-skill abstraction is routed to a separate proposal.
- Common-path reduction is supporting evidence, not a normative percentage gate.
- Acceptance remains deterministic and excludes target-agent execution.

## Authoring result

All required proposal sections are filled.
Initial user goals and the triggered scope budget are explicitly classified.
The artifact is ready for independent proposal review and does not claim approval or specification readiness.
## R1 revision decisions

- Accepted `IMPSIM-PR1`: the proposal now defines isolated, planned, and armed invocation profiles and evaluates the exact content each profile loads.
- Accepted `IMPSIM-PR2`: the proposal now selects separate planned-milestone and automated-review/correction references, each with a distinct load condition.
- Made material improvement in the isolated and planned profiles part of success, while requiring justified non-regression for the fully armed profile.
- Kept the 30–45 percent value as non-normative planning evidence for the isolated profile rather than a semantic gate.
- Added required and forbidden resource-load fixtures without introducing target-agent runtime execution.

## R3 revision decisions

- Accepted `IMPSIM-PR3`: armed automation is valid only for the same current planned milestone; trigger evidence is durable and identity-bound; invalid or stale combinations stop.
- Accepted `IMPSIM-PR4`: the single result asset has one universal core group plus planned and armed conditional groups, with inapplicable groups omitted and all policy retained outside the asset.
- Accepted `IMPSIM-PR5`: semantic-rule dispositions and literal dependency classifications use separate change-local ledgers and closed vocabularies.
- Made UTF-8 bytes and words the primary portable measurements; token estimates remain optional pinned evidence without a new dependency.
- Recorded `architecture-not-required` as the expected bounded assessment outcome, with only documentation correction or a later package-model change triggering architecture work.
