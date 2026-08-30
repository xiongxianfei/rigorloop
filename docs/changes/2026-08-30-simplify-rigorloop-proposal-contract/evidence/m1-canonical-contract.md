# M1 Canonical Contract Implementation Evidence

Milestone: M1
Validation result: passed

## Result

## Core result

- Skill: implement
- Status: implemented
- Completed scope: Replaced the proposal and Proposal Review canonical contract with the approved direction-level model, aligned the normative assets and conditional references, updated governing guidance, and added focused static conformance proof.
- Artifacts changed: `skills/proposal/`, `skills/proposal-review/`, `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, `specs/skill-contract.md`, `scripts/skill_validation.py`, and `scripts/test-skill-validator.py`.
- Tests added or updated: The existing proposal contract tests now assert the exact seven-section grammar, conditional material impact, proportional feasibility, proposal-review vision outcome, bounded approval authority, downstream-detail exclusion, portable/governed ownership boundary, and direct-review isolation.
- Validation performed: `python scripts/validate-skills.py skills/proposal/SKILL.md`; `python scripts/validate-skills.py skills/proposal-review/SKILL.md`; `python scripts/test-skill-validator.py`; `python scripts/validate-documentation-prose.py --mode audit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path specs/skill-contract.md`; `python scripts/validate-change-metadata.py docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/change.yaml`; `node packages/rigorloop/dist/bin/rigorloop.js lifecycle context implement --change 2026-08-30-simplify-rigorloop-proposal-contract --format json`; `git diff --check`.
- Validation result: Both canonical skill packages validate; all 361 skill-validator tests pass; the required prose audit exits successfully; change metadata is valid; lifecycle context remains current on M1 with approved Design and Delivery packages and no blocker, stale evidence, warning, or error; and the diff check passes.
- Open blockers: none
- Next stage: code-review
- Claim limitations: M1 does not implement proposal lifecycle structure validation, compatibility cutover, generated adapter parity, release validation, later milestones, final verification, or PR readiness.

## Planned milestone

- Change ID: `2026-08-30-simplify-rigorloop-proposal-contract`
- Plan identity: `docs/plans/2026-08-30-simplify-rigorloop-proposal-contract.md`, initialized from approved Delivery Review R2.
- Milestone ID: M1
- Milestone state: implementation complete; lifecycle completion remains owned by workflow after code review.
- Baseline or change-pack status: Delivery Review R2 is approved and the initialized plan identifies M1 as the active milestone.
- Milestone validation evidence: this file
- Commit status: handoff commit subject `M1: implement simplified proposal contract`.
- Code-review handoff: ready for independent review of the exact M1 commit.

## Test-first proof

The focused `test_proposal_skills_define_simplified_direction_contract` assertion failed before the canonical edits because the asset still exposed the legacy `Owning change record`, `Vision fit`, architecture, testing, rollout, and other downstream sections. The same assertion passes after the implementation.

## MP-001 semantic review

- An ordinary proposal can support approval from the seven required sections because the authoring contract requires a concrete direction and a credible, proportionate feasibility assessment rather than downstream design.
- `Impact and major trade-offs` is the sole optional level-two section and is included only when its content could affect approval.
- Proposal Review records exactly one routine or exceptional vision-alignment outcome. It withholds approval when a material conflict, revision request, or bootstrap decision is undisclosed or lacks owner authority.
- Proposal Review explicitly avoids requiring detailed behavior, architecture, APIs, commands, schemas, sequencing, proof design, test cases, or rollout mechanics.
- A direction that is too vague and content that prematurely settles a Design or Delivery decision are both material findings.
- Direct and review-only Proposal Review remains independent and isolated; settlement does not start Design.

## Prose audit disposition

The required audit reported 38 errors and 45 warnings in pre-existing mechanically wrapped lines, primarily in the long-standing `specs/skill-contract.md` amendment history and existing `docs/workflows.md` sections. The command exits successfully in audit mode. None of the reported locations is an M1-changed contract line, and `git diff --check` is clean. These baseline formatting findings are not expanded into this behavior milestone.
