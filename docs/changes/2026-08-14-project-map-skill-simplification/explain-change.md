# Explain Change: Project-Map Skill Simplification

## Summary

The change makes simple repository-map creation substantially shorter while preserving evidence, freshness, command, reliance, and claim safety inline. Maintenance, audit, and root/area coordination now load one conditional reference, the existing skeleton remains the sole structural owner, and operation is independent from repository or area scope.

## Problem

The former skill loaded refresh comparison, audit handling, area coordination, recovery, and repeated structure for every invocation. It also treated `area` as a peer of `create`, `refresh`, and `audit`, even though area is a scope that can coexist with any operation. This increased common-path context and left create/refresh target-state behavior and coordinated area recovery less explicit than the approved contract requires.

## Decision trail

The accepted proposal selected a compact universal skill, one maintenance/coordination reference, and the existing skeleton. Spec R6-R11 closes operation, scope, target-state, and result behavior; R85-R101 closes package ownership and loading; R102-R111 closes the area transaction; and R112-R117 closes compatibility, measurements, and deterministic acceptance. The architecture update applies the existing mapped-resource package model without a new runtime or ADR. Plan milestones M1-M3 froze preservation evidence, implemented the package split, and proved measurements and adapter parity.

## Diff rationale by area

| File or area | Change | Reason | Source and proof |
| --- | --- | --- | --- |
| `skills/project-map/SKILL.md` | Shortened the universal contract; added independent operation/scope classification, target-state rules, bounded preflight, PMA0/PMA1 loading, resource failure, and new result fields. | Simple root creation must remain safe and self-sufficient without loading maintenance procedure. | R6-R25, R30-R101, R112-R117; T1-T5, T12-T14. |
| `skills/project-map/references/map-maintenance-and-area-coordination.md` | Added refresh, audit, root/area coordination, area creation, commit order, and exact retry procedure. | These behaviors share a genuine conditional boundary and must not be reconstructed when the resource is absent. | R26-R29, R49-R57, R87-R111; T3-T11. |
| `skills/project-map/assets/project-map-skeleton.md` | Kept byte-identical. | The existing asset already owns the required structural labels, tables, and insertion points; adding or duplicating structure was unnecessary. | R58-R65, R89-R92; T7 and package hash evidence. |
| `scripts/skill_validation.py` | Replaced the old four-mode check with operation and scope checks, stopped requiring skill-body duplication of skeleton structure, and rejects legacy `Mode` in new output. | The validator must enforce the approved contract rather than incidental old prose. | R6, R11, R89-R90, R112-R115; CMD2-CMD4. |
| `scripts/test-skill-validator.py` | Added six focused simplification tests and migrated the directly coupled fixture assertion. | Static assertions cover exact package, classification, preflight, universal ownership, transaction, and failure behavior without an agent runtime. | T1-T14; CMD3-CMD4. |
| `tests/fixtures/skills/project-map-contract/valid/SKILL.md` | Migrated the controlled fixture to `Operation`, `Map scope`, and skeleton structural ownership. | Real parser/test consumers must migrate atomically with the contract. | R112-R115; literal ledger. |
| Change-local ledgers and evidence | Recorded 24 rule dispositions, 15 literal dependencies, 35 scenarios, baseline/final measurements, package proof, and milestone reviews. | Semantic preservation, literal compatibility, honest package accounting, and lifecycle closeout require durable evidence. | R83-R84, R115-R117; CMD1-CMD11. |

## Tests added or changed

`ProjectMapSkillSimplificationTests` proves package closure, PMA0/PMA1 assembly names, independent operation and scope, target-state behavior, the seven coordination surfaces, universal evidence and reliance rules, reference-owned transaction procedure, and fail-closed resource behavior. Existing canonical and fixture tests continue to prove normalized structure, skeleton integrity, generated-resource behavior, representative outputs, readability, and cross-skill compatibility.

This is static contract and integration proof because the changed behavior is published instruction and package structure, not an executable target runtime. No Codex, Claude Code, opencode, or other target agent was executed or graded.

## Validation evidence available before final verify

- CMD1 passed with 24 rules, 15 literals, 35 scenarios, and unknown values rejected first.
- Canonical skill validation and 6 focused tests passed.
- The full skill suite passed 336 tests with 16 skips.
- Generated-skill tests passed 7 tests and `build-skills.py --check` passed.
- Boundary-first validation passed for `specs/project-map.md`.
- The adapter-distribution suite passed.
- Fresh `v0.4.0` generation and selected `project-map` clean-install validation passed for Codex, Claude Code, and opencode.
- Change metadata, review structure, and diff checks passed at each handoff.

Formal final verification has not yet run, so this artifact does not claim branch or PR readiness.

## Review resolution summary

Seven material findings from proposal and test-spec review are closed: six accepted proposal refinements and one rejected manual-semantic-test procedure. There are no open or `needs-decision` findings. The detailed dispositions are in `review-resolution.md`; M1, M2, M3, and final holistic code review are clean.

## Alternatives rejected

Inline-only compression would leave conditional procedure on every invocation. Multiple narrow references would increase navigation without distinct activation boundaries. An executable routing or map engine would add runtime and state outside the problem. Replacing the skeleton or adding another asset would create duplicate structural ownership. A scripted manual semantic-review acceptance step was rejected by the user; ordinary PR review remains the human judgment point.

## Scope control

The change does not migrate existing project maps, add a map artifact validator, create a runtime, alter workflow persistence, modify generated adapter source trees, publish artifacts, or broaden `project-map` into architecture design, backlog, review, verification, or PR authority.

## Risks and follow-ups

PMA1 has a deliberately small byte reduction because exact transaction identity and recovery behavior remain explicit; its word count still decreases by 162 and total package size also decreases. The package now has two mapped resources instead of one, which is reported rather than hidden. Ordinary PR review should assess readability and semantic clarity, but no further implementation follow-up is currently identified.
