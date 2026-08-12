# Why the Spec-Review Skill Changed

## Summary

The change makes isolated formal spec review shorter and easier to scan without weakening review judgment or durable recording. Universal review, evidence, recording, status, stop, claim, and handoff rules remain in `SKILL.md`; exact governed settlement and workflow-managed automation move to one conditionally loaded reference. The existing result and finding assets remain the sole structural output owners.

The isolated formal profile decreases from 2328 to 2143 words and from 17407 to 16248 UTF-8 bytes. Governed and total-package growth is reported as conditional procedure relocation and clarification, not deletion.

## Problem

The former common path repeated orientation, routing, recording, settlement, automation, boundary, and output guidance. Isolated formal reviews loaded governed procedure they could not use, and exact prose consumers made safe simplification difficult to distinguish from accidental compatibility breakage.

## Decision trail

| Source | Decision |
| --- | --- |
| Proposal | Keep isolated formal judgment and recording self-sufficient; extract only governed settlement and automation. |
| Specification R1-R32 | Preserve formal classification, placement, review judgment, recording, authority, boundary activation, and fail-safe resource behavior. |
| Specification R33-R45 | Account for semantic rules and literals separately, reduce the isolated loaded profile, preserve assets and package parity, and exclude target-agent acceptance. |
| Architecture assessment | `architecture-not-required`; the existing mapped-resource package model already owns references and generated parity. |
| Plan M1 | Freeze rule, literal, scenario, and baseline evidence before editing the package. |
| Plan M2 | Refactor the canonical package and migrate exact consumers with focused tests. |
| Plan M3 | Prove semantic preservation, profile measurements, boundary identity, and package-chain parity. |

## Diff rationale by area

| Area | Change | Reason | Evidence |
| --- | --- | --- | --- |
| `skills/spec-review/SKILL.md` | Reorganized the common path around formal classification, isolated recording, review judgment, status, safety, claims, resource loading, and handoff. | An isolated formal review must remain complete without governed procedure. | R1-R19, R26-R32; M2 reviews. |
| `references/governed-spec-review-settlement.md` | Added one conditional owner for matching-entry settlement and workflow-managed automation. | These procedures require current same-change governed authority and are unusable by isolated review. | R20-R25; scenarios for governed, stale, missing-resource, and automation cases. |
| `assets/review-result-skeleton.md` | Added closed recording, governed-settlement, boundary-review, and automated-review groups. | The asset can remain the sole layout owner without deciding applicability or policy. | R14-R16, R29-R30; focused asset test. |
| `scripts/skill_validation.py` | Allowed the new reference, recognized package-aware isolation wording, and approved the new structural labels. | Existing deterministic checks must follow the new package boundary without preserving obsolete sentences. | R37-R44; CMD2-CMD5. |
| `scripts/test-skill-validator.py` | Added focused package/profile assertions and made lifecycle consumers read the governed reference where applicable. | Static proof must cover conditional loading, recording-before-settlement, result groups, and package-aware contract checks. | T1-T5, T9-T13; 313-test suite. |
| Coupled skill contracts | Amended the published-skill and spec-family resource contracts. | The approved new reference and structural groups must have explicit governing ownership. | R41-R44; boundary and skill validation. |
| Change-local ledgers and fixtures | Recorded semantic dispositions, literal classifications, closed scenarios, invalid values, baseline, measurements, and semantic review. | No significant rule may disappear, and incidental test wording must not become policy. | R33-R40; CMD1 and MP1. |
| Lifecycle evidence | Recorded proposal through final code-review decisions, the M2 correction, and milestone proof. | Formal workflow state must match the actual review and correction history. | Review log, resolution, change metadata, and M1-M3 reviews. |

The existing boundary-first references and material-finding asset were not redesigned. Their identities remain governed by the existing boundary contract.

## Tests and proof

- CMD1 proves closed rule dispositions, literal classifications, scenarios, and fail-closed unknown values.
- Focused validator tests prove exact profile/resource behavior, isolated-versus-governed authority, result groups, and missing-resource failure.
- Existing lifecycle tests prove record-first, matching-entry-only settlement and workflow-owned continuation.
- Existing build and adapter tests prove the new reference survives generated, archived, and installed package boundaries.
- Independent semantic review reconciles every rule, literal, profile, and interaction without executing a target agent.

Validation available before final verification:

- `python scripts/validate-skills.py skills/spec-review/SKILL.md` — passed.
- `python scripts/test-skill-validator.py` — 313 passed, 16 skipped.
- `python scripts/test-build-skills.py` — 7 passed.
- `python scripts/build-skills.py --check` — passed.
- `python scripts/test-adapter-distribution.py` — 150 passed.
- Fresh adapter build and selected `spec-review` clean-install validation — passed for Codex, Claude, and OpenCode.
- Boundary coverage, metadata, review structure, readability, and diff checks — passed.

## Review resolution summary

Fourteen material findings are closed with accepted dispositions. Proposal and specification review closed classification, recording, asset, boundary, and measurement contracts. Code review found one governed procedure-order defect in M2; the implementation moved reference loading before review execution while retaining recording as a settlement precondition, and M2 R2 approved the correction. The final holistic review found no material issue. See `review-resolution.md` and `review-log.md` for durable details.

## Alternatives rejected

- Editorial compression alone would keep governed procedure in every isolated review.
- Moving universal recording into the reference would make isolated formal review incomplete.
- Multiple small settlement and automation references would add package and trigger complexity without independent authority boundaries.
- A generic checklist would remove repository-specific lifecycle, recording, boundary, and claim rigor.
- Target-agent journeys, permanent size gates, or a new tokenizer would add unrelated nondeterministic machinery.

## Scope control

The change does not alter the `change.yaml` schema, lifecycle ownership, boundary-first activation policy, adapter architecture, release behavior, or another skill. It adds no runtime, persistent state, dependency, scheduler, network action, transcript grader, or generated authored source.

## Risks and follow-ups

The governed and total-package profiles grow because conditional procedure now has one explicit owner; this is an intentional maintenance and packaging tradeoff. The common path reduction is modest because universal formal recording and claim safety must remain inline. Final verification must still assess the post-review branch and determine branch readiness; this explanation does not claim verification or PR readiness.
