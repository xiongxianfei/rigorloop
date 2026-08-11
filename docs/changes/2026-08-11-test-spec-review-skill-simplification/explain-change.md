# Why the Test-Spec-Review Skill Changed

## Summary

The change makes ordinary test-spec review easier to load and scan while preserving the complete review contract. Universal classification, proof judgment, status, stop, claim, and handoff rules remain in `SKILL.md`. Durable recording and formal-only settlement now live in one conditionally loaded package reference. Existing boundary references and output assets retain their paths and bytes.

The ordinary `TSR0-isolated` profile decreases from 2722 to 2136 words (21.53%) and from 19768 to 16105 bytes (18.53%). The complete package grows 1.75% by words because the conditional procedure is now explicit and independently usable; this is reported as relocation and clarification rather than deletion.

## Problem

The original skill mixed universal review work with procedure needed only when durable recording or formal lifecycle settlement applied. Repeated quick-guide, routing, stop, recording, finding, and output descriptions made the common path longer and created multiple places where closely related rules could drift.

## Decision trail

| Decision source | Decision |
| --- | --- |
| Proposal | Use a compact self-sufficient common path, one late recording/settlement overlay, unchanged boundary resources, and existing assets as sole structural owners. |
| Specification R1-R24 | Close lifecycle and handoff classification, keep universal proof and safety inline, and restrict the overlay to recording and formal settlement. |
| Specification R25-R30 | Account for every semantic rule and exact literal separately; reject unknown ledger values first; measure ordinary and total package cost independently. |
| Specification R31-R39 | Preserve package parity, structural assets, boundary resources, routing authority, and invalid advisory workflow handoff behavior. |
| Architecture assessment | `architecture-not-required`: the existing mapped-resource package model already owns conditional references and generated parity. |
| Plan M1 | Freeze 19 semantic rules, 16 literal dependencies, 16 scenarios, invalid fixtures, and baseline measurements before moving prose. |
| Plan M2 | Rewrite the canonical package and migrate existing validator consumers with failed-first focused tests. |
| Plan M3 | Prove profile measurements, semantic preservation, generated/archive/install parity, and selected clean installs. |

## Diff rationale by area

| Area | Change | Reason | Requirement and evidence |
| --- | --- | --- | --- |
| `skills/test-spec-review/SKILL.md` | Reorganized the common path around closed classification, universal proof review, status, stops, claims, resources, and handoff. | Advisory review must remain complete without loading recording mechanics. | R2-R9, R19-R24, R34-R39; M2 review. |
| `references/test-spec-review-recording-and-settlement.md` | Added one shared recording section and one separately gated formal settlement section. | Recording is additive and may apply late; formal settlement has stricter identity and lifecycle authority. | R10-R18; scenarios T1-T5, T12, T14-T16. |
| `scripts/skill_validation.py` | Allowed the new mapped reference and made installed placement validation read the complete test-spec-review package. | Moving procedure must not weaken the existing installed-artifact contract. | R37-R39; focused placement tests. |
| `scripts/test-skill-validator.py` | Added six simplification contract tests and migrated settlement consumers to package-aware checks. | Static proof must cover profiles, universal ownership, exact resources, formal isolation, and resource failure. | T1-T5, T12, T15-T16; 308-test suite. |
| Rule and literal ledgers | Recorded one closed disposition for 19 semantic rules and one compatibility classification for 16 exact dependencies. | Semantic behavior and accidental wording compatibility are different evidence classes. | R25-R28; CMD1. |
| Scenario and invalid fixtures | Added 16 positive/negative scenarios plus unknown disposition and classification fixtures. | Classification, resource failure, staleness, isolation, and fail-closed values require deterministic proof. | R3-R18, R20-R24, R39. |
| Measurement and semantic evidence | Reported each resource, assembly, overlay, total package, ownership count, and independent semantic conclusion. | Main-file reduction alone could hide relocation or behavioral loss. | R29-R30, R38; M3 evidence. |
| Review records and lifecycle metadata | Recorded all artifact and code reviews, two implementation corrections, closeout, and milestone routing. | Formal lifecycle evidence must reflect the actual review and correction history. | Workflow contract and repository governance. |
| Selector deferral evidence | Recorded five exact-path repository-maintainer deferrals for one-change ledgers and fixtures. | The permanent selector intentionally has no generic simplicity-evidence class; approved CMD1 and MP1 proof remain mandatory and visible. | Evidence-registration contract; final review R2. |

The two boundary references, result asset, and finding asset were not edited. Their unchanged hashes prove that this change did not silently redesign boundary analysis or output structure.

## Tests and proof

- The M1 ledger command proves 19 rules, 16 literals, 16 scenarios, and fail-closed unknown values.
- Six focused contract tests prove closed profiles, universal inline ownership, exact resource mapping, recording/formal separation, structural assets, and missing-resource failure.
- Existing stage-owned lifecycle tests prove record-first, matching-entry-only settlement and workflow-owned continuation.
- Existing boundary-first tests prove exact compact scan and resource projection behavior.
- Generated-skill and adapter tests prove mapped resources survive generated, archived, and installed package boundaries.
- Independent semantic review checks all rules, literals, interactions, and scenarios without executing a target agent.

Validation available before final verification:

- `python scripts/validate-skills.py skills/test-spec-review/SKILL.md` — passed.
- `python scripts/test-skill-validator.py` — 308 passed, 16 skipped.
- `python scripts/test-build-skills.py` — 7 passed.
- `python scripts/build-skills.py --check` — passed.
- `python scripts/test-adapter-distribution.py` — 150 passed.
- Temporary `v0.3.6` adapter build and `--clean-install-smoke --skill test-spec-review` — passed for Codex, Claude, and OpenCode.
- Boundary coverage, change metadata, review artifacts, and diff checks — passed.
- PR-mode validation selection after deferral — passed with 11 selected checks, zero blockers, five complete owner-deferred debt records, and no broad-smoke requirement.

## Review resolution summary

Six material findings are closed with accepted dispositions. Proposal, spec, and test-spec review closed four contract gaps. Code review found and resolved one omitted generated-Markdown-readability rule in M1 and one trailing-whitespace defect in M3. Both implementation findings received same-stage rereview and clean outcomes. See `review-resolution.md` and `review-log.md` for the durable closeout.

## Alternatives rejected

- Inline editorial compression alone would leave conditional recording procedure in the common path.
- Many small references would increase trigger and package complexity without creating distinct authority boundaries.
- A generic checklist would remove project-specific lifecycle, proof, and recording rigor.
- Target-agent journeys, a permanent size gate, or a new tokenizer would add runtime and maintenance machinery unrelated to semantic preservation.
- Registering a permanent selector class for five one-change evidence files would contradict their change-local role; exact owner deferrals keep the debt visible without adding generic infrastructure.

## Scope control

The change does not alter `change.yaml` schema, lifecycle ownership, boundary-first policy, output asset structure, adapter architecture, release behavior, or another skill. Existing change-metadata deferral fields are populated, but no schema or selector behavior changes. The change adds no runtime, persistent state, dependency, scheduler, transcript grader, network action, or generated-source edit.

## Risks and follow-ups

The main residual tradeoff is a small formal-profile and total-package increase. It is intentional: formal users load a complete conditional owner, while ordinary users avoid it. The advisory 30-40% main-file target was not met because further reduction would hide universal safety or proof policy. Final verification must still rerun the repository commands against the post-review branch and determine final workflow readiness; this explanation does not claim branch or PR readiness.
