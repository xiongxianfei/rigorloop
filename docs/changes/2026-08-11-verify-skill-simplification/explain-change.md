# Verify Skill Simplification Explain Change

## Summary

This change makes ordinary `verify` invocations materially smaller and easier to classify while preserving `branch-ready`, evidence, review-closeout, lifecycle, release, claim, and handoff rigor.

The universal `SKILL.md` falls from 2,896 to 2,141 words. `VP0-scoped` is 26.1% smaller by words and 24.7% smaller by bytes; all final profiles and the total package also shrink. One 502-word branch-readiness reference now loads only for direct branch readiness or governed final verification.

## Problem

The prior 308-line skill loaded final lifecycle closeout, all-milestone aggregation, broad validation, release, and PR-handoff procedure even for a single command or evidence check. It repeated orientation, evidence, closeout, stop, claim, and handoff guidance, making ordinary verification harder to scan and giving final procedure more than one textual owner.

The goal was to separate final aggregation from universal evidence truthfulness, not to weaken verification.

## Decision trail

- The proposal selected a compact self-sufficient common path, the existing boundary-first reference, and one conditional branch-readiness reference; it rejected a result asset and runtime verifier.
- R1-R22 define the three outcomes, exact target resolution, four resource profiles, two independent execution modes, universal evidence semantics, conditional ownership, missing-resource stops, and claim boundaries.
- R23-R29 require separate semantic and literal ledgers, deterministic profile accounting, an advisory size target, and no target-agent acceptance.
- R30-R33 require package-chain parity, behavioral compatibility, a bounded architecture assessment, and atomic rollback. The assessment returned `architecture-not-required` because the existing packaged-skill model already covers mapped references.
- M1 froze 16 semantic rules, 14 literal dependencies, 17 scenarios, and the baseline. M2 refactored the package and permanent tests. M3 measured final profiles, corrected stale evidence anchors, and proved generated/archive/install parity.

## Diff rationale by area

| File or area | Change | Reason | Source and proof |
| --- | --- | --- | --- |
| `skills/verify/SKILL.md` | Consolidated outcome/target classification, execution authority, item evidence truthfulness, review closeout, stops, claims, boundary bridge, and result/handoff. | Scoped verification must remain safe and self-sufficient without final procedure. | R1-R13, R16-R17, R20-R22; T1-T3, T5, T9, T12. |
| `branch-readiness-verification.md` | Added final prerequisites, evidence composition, lifecycle/review aggregation, blocker calculation, verdict, and mode-specific completion. | Final readiness needs one conditional procedure owner without gaining lifecycle or PR authority. | R14, R18-R19; T4-T5, T12. |
| `scripts/test-skill-validator.py` | Added five focused package-contract tests. | Existing deterministic owners should prove mappings, closed profiles/modes, universal semantics, reference ownership, and fail-safe loading. | R4-R20, R30-R31; CMD3. |
| Rule/literal ledgers and fixtures | Recorded stable dispositions, classifications, destinations, invalid values, and 17 static scenarios. | No meaningful rule may disappear, and incidental tests must not become prose-policy owners. | R23-R26, R29; CMD1, MP0-MP1. |
| Measurements and package proof | Recorded every resource/profile/package word and byte count plus generated, archived, and installed validation. | Main-file reduction must not hide relocation, final-profile growth, or adapter loss. | R27-R30, R33; CMD2-CMD8. |
| Change-local lifecycle and review records | Recorded accepted artifacts, four resolved upstream findings, clean M1-M3 reviews, and clean final holistic review. | Formal workflow gates require durable evidence and current state before final verification. | Workflow contract; CMD9-CMD10. |

## Tests added or changed

- T1-T2 prove exact outcomes/targets and keep loaded resources separate from execution authority.
- T3 proves commands, CI, generated output, manual proof, and release metadata remain available to scoped verification.
- T4-T5 prove aggregation-only reference ownership, exact loads, and missing-resource stops.
- T6-T7 prove semantic and literal evidence fails closed without freezing incidental prose.
- T8 proves deterministic and honest profile/package measurements.
- T9 proves 17 negative and positive scenarios without executing a model.
- T10-T11 prove canonical and mapped-resource integrity.
- T12-T14 prove semantic preservation, adapter archive/install parity, and atomic rollback.

Five permanent focused assertions were added to the existing skill-validator suite. Change-local scenarios, measurements, and semantic judgment remain evidence rather than a new permanent simplicity validator.

## Validation evidence available before final verify

- CMD1: 16 rules, 14 literals, and 17 scenarios passed; unknown values were rejected first.
- Canonical `verify` skill validation passed.
- `scripts/test-skill-validator.py`: 302 tests passed, 16 skipped.
- `scripts/test-build-skills.py`: seven tests passed.
- Generated-skill checking passed in temporary output.
- `scripts/test-adapter-distribution.py`: 150 tests passed.
- Trusted `v0.3.6` package proof built Codex, Claude, and OpenCode archives and passed selected `verify` clean-install validation.
- Boundary-first, change-metadata, review-structure/closeout, and diff-whitespace checks passed.
- No target-agent runtime, network publication, or tracked generated-package hand-edit was used.

M2’s first focused run failed as intended because the new reference and contracts did not exist. The full validator initially exposed genuine shared boundary-first, portability, closeout, and final-order contracts; those remained compactly inline. M3 semantic review found five stale rule-ledger destination anchors and corrected them to actual headings before all 16 destinations passed a direct anchor audit.

## Review resolution summary

All four material upstream findings are accepted and closed: three proposal findings established target/mode/evidence ownership, and one test-spec finding aligned rollback proof with the trusted package fixture. There are no `needs-decision` or open review-log findings. See `review-resolution.md` for dispositions without repeating the review transcripts.

M1, M2, M3, and the final holistic code review are clean with no material implementation finding.

## Alternatives rejected

- Keeping the prior skill preserves the 2,896-word common path and repeated final procedure.
- Editorial compression alone cannot stop scoped checks from loading final-closeout procedure.
- Moving item-level CI, generated-output, or manual-proof semantics would make valid scoped checks depend on final readiness.
- Multiple small references would fragment one coherent final decision and increase trigger complexity.
- A result asset adds indirection to a compact profile-neutral result.
- A runtime verifier, prompt journey, permanent size gate, or tokenizer dependency creates a new unstable acceptance owner.

## Scope control

The change does not alter workflow stage order, `change.yaml` schema, review outcomes, milestone behavior, validation meanings, release authority, PR authority, adapter roots, or publication. It adds no runtime, service, state store, dependency, selector, scheduler, result asset, permanent simplicity validator, or target-agent test. Canonical authorship remains under `skills/`; adapter output remains derived.

## Risks and follow-ups

The package has one additional mapped file, so exact resource triggers and archive/install parity remain important. Structural assertions cannot prove prose semantics; the retained rule ledger and independent semantic review record that judgment. The common-path word reduction is 26.1%, below the advisory 30-40% range, because universal boundary-first, portability, formal-review, evidence, claim, and result contracts must remain inline. Further extraction would weaken scoped self-sufficiency.

No follow-up is required for this scoped change. Other skill simplifications require separate proposals.

## Readiness

All implementation milestones and review obligations are closed, and this explanation covers the final reviewed diff through `8e14257f`. Final `verify` must still rerun the required repository checks and owns any `branch-ready` result. This artifact does not claim PR, hosted-CI, release, or merge readiness.
