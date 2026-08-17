# Explain Change: Learn Skill Simplification

## Summary

This change makes the published `learn` skill smaller on both real invocation paths while preserving its evidence, confirmation, recording, routing, compatibility, and claim boundaries. The former flat procedure is now a compact universal `SKILL.md` plus one conditionally loaded session-method reference. The change also clarifies that `learn` records owner-bound routes and exact result backlinks; the destination owner performs any proposal, specification, ADR, workflow, skill, plan, issue, or external-system mutation under its own contract.

## Problem

The previous skill loaded the full four-phase session method for every invocation, mixed universal safety with session-only procedure, and used legacy routing language that could be read as granting `learn` direct authority over destination artifacts. The accepted proposal chose one conditional reference, no templates or scripts, no unsupported pre-session assessment operation, and no transaction-grade recovery or reconciliation engine.

## Decision trail

| Source | Decision carried into the diff |
| --- | --- |
| Proposal | Keep universal trigger, evidence, confirmation, ownership, stop, and claim rules inline; move only the full session method; use prospective stable routes and bounded backlink recording. |
| `specs/learn-skill-simplification.md` R1-R6 | Publish exactly one universal skill plus one session-method reference and load the reference only for `run-learn-session`. |
| R7-R10 | Support only `run-learn-session` and `record-learn-route-result`; leave pre-session assessment and closeout with the trigger owner. |
| R11-R18 | Use deterministic collision-safe session paths, a complete first `Frame` write, and fail-closed handling for partial or changed-basis records. |
| R20-R35 and R47 | Keep contributor confirmation narrow, create stable owner-bound routes, require immutable completion kinds, and let destination owners produce authoritative results. |
| R36-R45 | Preserve historical sessions, classify every semantic/literal dependency, shrink both real loaded profiles, retain package parity, and avoid target-agent acceptance. |
| Architecture assessment | `architecture-not-required`: the selected design adds no persistent phase recovery, registry, polling service, integration, schema owner, or cross-owner mutation authority. |
| Plan M1 | Freeze semantic rules, literals, callers, scenarios, architecture triggers, and baselines before canonical edits. |
| Plan M2 | Align the older learn contract, split the canonical package, and add narrow prospective route-result recording. |
| Plan M3 | Prove semantic preservation, both-profile reduction, portability, and canonical-through-installed parity. |

## Diff rationale by area

| File or area | Change | Reason and source | Test or evidence |
| --- | --- | --- | --- |
| `skills/learn/SKILL.md` | Replaced the flat procedure with the universal contract, two operations, exact resource trigger, ownership limits, result recording, stops, and claims. | R1-R10, R20-R22, R31-R37; keep fail-safe decisions available on both profiles. | T1-T2, T5, T8, T15; `LearnSkillSimplificationTests`. |
| `skills/learn/references/session-method.md` | Added the detailed `Frame -> Observe -> Classify -> Route` method, collision handling, confirmation, topic effects, route fields, and completion rules. | R3-R6, R11-R19, R23-R30; load session-only procedure only for LR1. | T1, T3-T8; focused skill tests and package validation. |
| `specs/learn-artifact-model.md` | Replaced ambiguous direct-write wording with owner-bound routes and exact owner-result identities. | R47 exact cross-spec disposition; one writer per authoritative destination. | T9 plus the updated legacy proof map. |
| `specs/learn-artifact-model.test.md` | Updated examples and tests to verify owner-produced authoritative outcomes and prohibit direct plan/tracker writes. | Keep the older contract and its proof map coherent in the same slice. | T5, T6, T8 align with revised R21-R24 and R33. |
| `scripts/test-skill-validator.py` | Added closed ledger tests and focused package-contract tests; made the existing learn check inspect the mapped reference. | R38-R40 and AGENTS.md unknown-vocabulary rule; prove moved behavior rather than relying on prose review alone. | CMD1, CMD3, and full CMD4. |
| Change-local fixtures and ledgers | Recorded rule owners, literal classifications, legacy writer dispositions, scenarios, invalid vocabulary values, and architecture triggers. | Plan M1; prevent semantic loss and fail closed on unknown values before consistency checks. | `evidence/m1-preservation-inventories.md`; CMD1. |
| Measurement and package evidence | Recorded reproducible baselines, final hashes and sizes, semantic preservation, adapter correction, and full package parity. | R41-R45 and Plan M3; distinguish loaded-context reduction from package growth. | `simplification-measurements.md`, `semantic-preservation-review.md`, `m3-package-proof.md`. |
| Proposal, spec, plan, test spec, reviews, and `change.yaml` | Added the required decision, contract, proof, review, correction, and workflow-state trail. | Repository lifecycle contract for a non-trivial published-skill change. | Metadata and review-artifact validators. |

## Tests added or changed

- T1-T3 prove exact package composition, operation selection, collision-safe creation, complete first Frame, and fail-closed partial records.
- T4-T6 prove evidence distinctions, confirmation boundaries, and exact idempotent topic effects.
- T7-T9 prove stable route fields, immutable completion-kind matching, bounded result recording, and destination-owner mutation.
- T10 preserves historical sessions without inferred route IDs.
- T11-T12 prove closed preservation ledgers and both-profile size reduction.
- T13-T14 prove canonical/generated/archive/release/install parity and portable acceptance without target-agent execution.
- T15 directly checks the compact result contract for success, replay, no-lesson, and blocked outcomes.
- T16 closes the architecture trigger before canonical mutation.

The focused tests are static contract tests because the changed product is published Markdown procedure and package composition, not a runtime learning engine. Existing build and adapter suites provide the integration boundary.

## Validation evidence available before final verify

The following evidence is current for the final reviewed implementation content:

- `python scripts/test-skill-validator.py LearnSkillSimplificationLedgerTests` — 5 passed.
- `python scripts/test-skill-validator.py LearnSkillSimplificationTests` — 6 passed.
- `python scripts/validate-skills.py skills/learn/SKILL.md` — canonical skill validation passed.
- `python scripts/test-skill-validator.py` — 397 passed, 16 skipped during M3 proof.
- `python scripts/test-build-skills.py` — 7 passed during M3 proof.
- `python scripts/build-skills.py --check` — passed during M3 proof.
- `python scripts/test-adapter-distribution.py` — 150 passed after correcting the portable invocation wording.
- Boundary, change-metadata, and review-closeout validation passed at their recorded stages.

These are pre-verify results. Hosted CI, final branch readiness, and PR readiness are not claimed here.

## Review resolution summary

The change recorded 16 material findings across proposal, spec, plan, test-spec, and milestone code reviews. All 16 have disposition `accepted` and status `closed`; no `needs-decision`, deferred item, or open review-log finding remains. The durable details and validation links are in [review-resolution.md](review-resolution.md). The final holistic code review found no material issue.

## Alternatives rejected

- Keeping the flat skill would not reduce either real loaded profile enough.
- Multiple narrow references would add navigation without a second genuine activation boundary.
- A pre-session assessment operation was removed because repository inventory found no actual caller.
- Phase-resume state, a route registry, polling, external integration, and a learning engine were rejected because the approved fail-closed Markdown model does not need them and they would require architecture reassessment.
- Templates and scripts were not added because the first version has no demonstrated structural drift or executable behavior to own.
- Letting `learn` update destination artifacts directly was rejected because contributor confirmation is not destination mutation authority.

## Scope control

The change does not redesign the four phases, seven classifications, cadence, confirmation policy, learn namespace, or topic authority. It does not migrate historical sessions, infer route IDs, alter destination review gates, optimize unrelated skills, execute a target agent, or publish external changes.

## Risks and follow-ups

The main residual risk is that future session authors may omit prospective route fields because sessions remain Markdown. The focused contract tests protect shipped guidance, and ordinary review protects authored session quality; no persistent schema was introduced. Any future demand for resumable phase transactions, automated route polling, cross-stage coordination, or external integration must return to architecture assessment rather than expanding this skill implicitly.

The change is ready to enter final `verify`; this explanation does not claim that verification, branch readiness, hosted CI, or PR readiness has completed.
