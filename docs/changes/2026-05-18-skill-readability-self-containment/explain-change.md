# Skill Readability and Self-Containment Change Explanation

## Summary

This change pilots the approved skill readability and self-containment contract on `proposal` and `proposal-review`.

It adds opt-in validation for the new skill shape, rewrites the pilot skills so installed users can read the complete contract without repository context, records cold-read and behavior-parity proof, and preserves follow-on ownership for the remaining R30 rollout. Token cost stays below the approved +5% tolerance and below the +10% hard cap after resolving the M3 duplicate-enum review finding.

## Problem

Users receive installed adapter skill files, not the maintainer repository's `specs/`, `schemas/`, or workflow docs. The prior pilot skills were usable but not optimized for that constraint: key enum values were embedded in prose, long contracts were harder to scan, output skeletons were incomplete or absent for the proposal side, and workflow-wide versus skill-local rules were not always visually obvious.

The approved priority order for this change is:

1. high-quality skill output;
2. clear and concise installed skills;
3. token cost as a subordinate constraint.

## Decision Trail

| Source | Decision or requirement | How the implementation follows it |
|---|---|---|
| Proposal | Choose in-skill restructuring instead of build-time partials or references to unavailable repo specs. | Rewrites canonical skill text under `skills/`; no build-time include mechanism was added. |
| Spec R1-R10 | Preserve source/generated boundaries, quality-first priority, self-containment, portable defaults, and ambiguity blocking. | Canonical source is edited under `skills/`; adapter archives are generated to `/tmp` only; cold-read checks inspect installed output. |
| Spec R11-R15 | Add workflow role blocks with required fields and valid stage values. | `proposal` and `proposal-review` now include `## Workflow role` blocks. |
| Spec R16-R24 | Fence/table closed enums, avoid duplicate enum prose, tabulate long contracts, and label workflow-wide rules. | Pilot skills use authoritative enum blocks, tables for named contracts, and explicit workflow-wide labels. |
| Spec R25-R28 | Add fenced output skeletons while preserving review result fields. | Both pilot skills now include fenced output skeletons near the bottom. |
| Spec R29-R31 | Pilot `proposal` and `proposal-review`; keep remaining R30 skills owned as follow-on rollout work. | Only the pilot pair was rewritten; follow-on ownership remains recorded in the plan. |
| Spec R36-R40 | Add focused static validation for the readability contract. | `scripts/skill_validation.py` adds opt-in checks and `scripts/test-skill-validator.py` adds fixtures. |
| Spec R41-R47 | Record cold-read and behavior-parity evidence before rollout. | M3 adds cold-read and behavior-parity reports with no regression classifications. |
| Spec R48-R53 | Compare token cost against baseline without overriding quality or clarity. | Token report records baseline and final counts within approved thresholds. |
| Plan M1 | Add validator foundation and baseline evidence before skill rewrites. | M1 changed validation and fixtures first, then recorded token baseline. |
| Plan M2 | Rewrite the pilot skills and prove generated adapter output remains derived. | M2 rewrote the pilot pair and validated generated adapter archives. |
| Plan M3 | Record cold-read, behavior parity, token comparison, and rollout handoff. | M3 records the evidence reports, token comparison, and follow-on ownership. |

No architecture or ADR artifact was required. The approved plan records that this is skill-surface and validation work, not a runtime architecture or adapter package format change.

## Diff Rationale By Area

| File or area | Change | Reason | Source artifact | Test or evidence |
|---|---|---|---|---|
| `skills/proposal/SKILL.md` | Added `version`, `schema-version`, workflow role, fenced enums, tables, workflow-wide labels, and a fillable output skeleton; removed duplicated enum restatements after review. | Make the installed proposal skill self-contained, scannable, and compliant with one-authoritative-enum placement. | R11-R28, R32-R34, R54 | `test-skill-validator.py`; `validate-skills.py`; cold-read report; behavior-parity report; `code-review-m3-r2` |
| `skills/proposal-review/SKILL.md` | Added the same readability contract shape while preserving review result and recording obligations; removed duplicated enum restatements after review. | Preserve review rigor while making the installed review contract easier to scan and fill. | R11-R28, R32-R34, R54 | `test-skill-validator.py`; `validate-skills.py`; cold-read report; behavior-parity report; `code-review-m3-r2` |
| `scripts/skill_validation.py` | Added opt-in `skill-readability-v1` validation for workflow role blocks, output skeletons, forbidden required internal references, and known closed enum placement. | Enforce the pilot contract without forcing untouched skills into the new structure. | R36-R40, R53 | `test-skill-validator.py`; `validate-skills.py` |
| `scripts/test-skill-validator.py` | Added positive and negative fixture tests and pilot opt-in coverage; updated assertions after SRSC-M3-CR1 to check enum references instead of duplicated values. | Prove validator behavior before and after pilot skill adoption. | Test spec T2, T3, T5, T8, T10 | 97-test validator run passes |
| `scripts/adapter_distribution.py` | Treats `version` and `schema-version` as transformable front matter for non-Codex adapters. | Preserve adapter portability after the pilot skills add readability-contract front matter; Codex keeps the fields, Claude/OpenCode generated skill bodies drop them like `argument-hint`. | R32-R35; R54 | `test-adapter-distribution.py`; selected CI; broad smoke rerun |
| `scripts/test-adapter-distribution.py` and `tests/fixtures/adapters/transformable-frontmatter/SKILL.md` | Extended the transformable-frontmatter fixture and assertion coverage to include `version` and `schema-version`. | Prevent regressions where readability front matter makes otherwise portable skills Codex-only. | R35; T10 | Targeted adapter distribution tests |
| `scripts/validation_selection.py` and `scripts/test-select-validation.py` | Classified adapter fixture paths, skill validator fixture paths, and change-local evidence reports used by this pilot. | Keep PR-mode CI from blocking on fixtures and durable evidence files that are intentionally part of this change. | R35, R41-R47 | `test-select-validation.py`; PR-mode CI reproduction |
| `tests/fixtures/skills/skill-readability/` | Added fixtures for valid pilot shape, missing workflow role, invalid stage, missing output skeleton, required internal reference, and duplicate closed enum. | Keep validation focused on explicit contract shape instead of broad semantic prose scoring. | T2, T3, T5, T8 | `test-skill-validator.py` |
| `specs/skill-readability-contract.md` | Added the approved contract for workflow role blocks, enum placement, skeletons, cold-read, behavior parity, token thresholds, and rollout scope. | Convert the accepted proposal into implementation requirements. | Proposal; spec-review-r1 | Artifact lifecycle validation; spec-review-r1 |
| `specs/skill-readability-contract.test.md` | Added traceable test cases T1-T16 mapping requirements to static validation, manual review, generated-output checks, cold-read, parity, and token evidence. | Define proof obligations before implementation. | Plan; R1-R60 | Artifact lifecycle validation; user approval |
| `docs/plans/2026-05-18-skill-readability-self-containment.md` and `docs/plan.md` | Created and maintained the active milestone plan, handoff state, validation notes, and lifecycle index. | Keep multi-milestone work sequenced and reviewable. | Plan-review-r2/r3 | Artifact lifecycle validation |
| `docs/reports/token-cost/skills/2026-05-18-skill-readability-self-containment.md` | Recorded baseline and final pilot token counts. | Apply the approved token budget as a constraint, not the driver. | R48-R52; T12-T13 | `measure-skill-tokens.py` |
| Change-local reports and review records | Added proposal/spec/plan/code review records, review log, review-resolution, implementation notes, cold-read report, and behavior-parity report. | Preserve durable reasoning, review outcomes, and rollout evidence. | Workflow contract; active plan | `validate-review-artifacts.py`; `validate-change-metadata.py` |

The temporary adapter archives under `/tmp/rigorloop-skill-readability-adapters` and installed cold-read extraction under `/tmp/rigorloop-skill-readability-cold-read/codex` are evidence surfaces only. No generated adapter body was hand-edited or tracked.

## Tests Added Or Changed

| Test or proof | What it proves | Why this level is appropriate |
|---|---|---|
| `scripts/test-skill-validator.py` readability fixture cases | Opt-in skills fail on missing workflow role, invalid stage, missing output skeleton, required unavailable internal references, and duplicate closed enum blocks. | Unit-level validation is enough for explicit Markdown structure and path phrases. |
| `test_skill_readability_pilot_pair_opts_into_contract` | `proposal` and `proposal-review` opted into `skill-readability-v1` and expose the required structural blocks. | Directly guards the pilot pair required by R29. |
| `scripts/validate-skills.py` | Canonical skills remain valid under repository skill validation. | Confirms the validator integrates with the normal skill validation path. |
| `scripts/build-skills.py --check` | Generated skill output remains derived from canonical source. | Required because adapters consume generated output, not hand-edited mirrors. |
| `scripts/build-adapters.py` and `scripts/validate-adapters.py` | Temporary adapter archives build and validate for the current `v0.1.5` support surface. | Integration-level proof for installed adapter packaging without tracking generated bodies. |
| Cold-read report | Installed `proposal` and `proposal-review` skills are self-contained and scannable without maintainer repo context. | Manual review is appropriate for reader discoverability and rule-scope clarity. |
| Behavior-parity report | Pilot rewrites preserve required output behavior and classify differences as `equivalent` or `improvement`, with no `regression`. | Manual contract comparison is allowed by the test spec for quality-preservation checks. |
| Token report | Final pilot token counts remain within the approved thresholds. | The repository already has a token measurement script and report surface. |

## Validation Evidence

Validation already recorded in the change pack includes:

```sh
python scripts/test-skill-validator.py
python scripts/validate-skills.py
python scripts/measure-skill-tokens.py
python scripts/build-skills.py --check
python scripts/build-adapters.py --version v0.1.5 --output-dir /tmp/rigorloop-skill-readability-adapters
python scripts/validate-adapters.py --root /tmp/rigorloop-skill-readability-adapters --version v0.1.5
python scripts/validate-change-metadata.py docs/changes/2026-05-18-skill-readability-self-containment/change.yaml
python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-18-skill-readability-self-containment.md --path docs/plan.md --path specs/skill-readability-contract.md --path specs/skill-readability-contract.test.md --path docs/changes/2026-05-18-skill-readability-self-containment/change.yaml --path docs/changes/2026-05-18-skill-readability-self-containment/review-log.md --path docs/changes/2026-05-18-skill-readability-self-containment/review-resolution.md
python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-18-skill-readability-self-containment
git diff --check --
```

During final `verify`, broad smoke exposed a branch-specific compatibility gap: `version` and `schema-version` front matter made `proposal` and `proposal-review` appear non-portable to the adapter distributor. The fix updates adapter front-matter transformation so those fields are kept for Codex and dropped from Claude/OpenCode generated skill bodies.

After PR #69 opened, hosted CI exposed selector routing gaps for the full PR diff: three change-local evidence reports and the `tests/fixtures/skills/skill-readability/` fixtures were unclassified in PR mode. The selector now routes those evidence reports through artifact lifecycle validation and the skill fixtures through skill regression checks.

The latest recorded post-resolution token counts are:

| Skill | Baseline | Final | Delta | Status |
|---|---:|---:|---:|---|
| `proposal` | 3189 | 3300 | +3.48% | within +5% tolerance; below +10% hard cap |
| `proposal-review` | 3255 | 3405 | +4.61% | within +5% tolerance; below +10% hard cap |

Final `verify` passed after the verify-stage compatibility fix and rerun code-review. It recorded selected CI, broad smoke, review artifact closeout, change metadata validation, artifact lifecycle validation, and diff check evidence in the active plan and change metadata. The later hosted CI selector-routing fix was locally reproduced with PR-mode CI and pushed for hosted rerun.

## Review Resolution Summary

The change-local `review-resolution.md` is closed.

| Review | Material findings | Disposition |
|---|---:|---|
| `proposal-review-r2` | 0 | no material findings |
| `proposal-review-r3` | 0 | no material findings |
| `spec-review-r1` | 0 | no material findings |
| `plan-review-r1` | 1 | `SRSC-PLAN-1` accepted and cleared by `plan-review-r2` |
| `plan-review-r2` | 0 | no material findings |
| `plan-review-r3` | 0 | no material findings |
| `code-review-m1-r1` | 0 | no material findings |
| `code-review-m2-r1` | 0 | no material findings |
| `code-review-m3-r1` | 1 | `SRSC-M3-CR1` accepted and cleared by `code-review-m3-r2` |
| `code-review-m3-r2` | 0 | no material findings |

`SRSC-M3-CR1` was fixed by replacing repeated closed enum value lists with references to the authoritative enum blocks and updating stale validator assertions.

## Alternatives Rejected

| Alternative | Why it was rejected |
|---|---|
| Move shared rules into repo specs and reference them from skills | Installed users do not receive those specs, so this would violate the skill-is-the-contract constraint. |
| Add build-time partials/includes now | It could reduce source duplication, but it introduces new tooling and was explicitly deferred by the proposal and spec. |
| Rewrite the full R30 skill set in this change | The approved plan uses a pilot-first rollout to keep quality, review, and token evidence manageable. |
| Hand-edit generated adapter output | Repository rules make `skills/` the authored source; generated adapter output must be produced by scripts. |
| Accept duplicate enum values for readability | The spec requires each closed enum to appear exactly once per skill; references to authoritative enum blocks preserve readability without drift. |
| Mark the pilot skills Codex-only after adding new front matter | R35 requires existing consumers to tolerate the new fields; adapter transformation preserves portability instead. |

## Scope Control

This change does not alter workflow stage order, review verdict meanings, formal review recording rules, adapter packaging, adapter manifest format, release archive contracts, legacy archives, or generated adapter bodies.

The pilot rewrites only `proposal` and `proposal-review`. Remaining R30 skills are still owned by the accepted contract as follow-on rollout work; they are not silently excluded.

## Risks And Follow-Ups

| Risk or follow-up | Current handling |
|---|---|
| Verify-stage compatibility fix changed implementation after explain-change was first recorded. | Verify ran, found and fixed adapter front-matter compatibility drift, SRSC-VERIFY-CR1 was resolved, rerun code-review was clean, and final verify passed. |
| Hosted CI failed after PR open because PR-mode selector routing missed new evidence and fixture paths. | Classified the missing path families and reproduced the hosted PR-mode CI command locally. |
| Full R30 rollout remains incomplete after the pilot. | Follow-on rollout ownership is recorded in the active plan. |
| Manual behavior-parity proof is less exhaustive than live LLM execution. | The test spec allowed manual contract comparison for this pilot; no regression classifications remain. |
| Token increases are accepted for readability. | Both increases are within +5%, justified by cold-read and behavior-parity evidence, and below the hard cap. |

## Readiness

`explain-change` is recorded and updated for the verify-stage adapter compatibility fix and the PR-mode selector-routing fix. SRSC-VERIFY-CR1 is resolved, rerun code-review is clean, final verify passed, and the active-plan handoff remains `pr`.
