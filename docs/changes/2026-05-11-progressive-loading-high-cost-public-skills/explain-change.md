# Progressive Loading High-Cost Public Skills Explain Change

## Status

explain-change complete; verify pending

## Summary

This change makes the measured high-cost public skills progressively loadable without changing workflow order, release token-friendliness gates, benchmark schema, or adapter layout.

The implementation added compact quick operating guides to `workflow`, `implement`, and `code-review`; added bounded handoff-state inspection guidance to `implement`; compressed repeated public skill prose where safe; moved or accounted workflow detail in contributor-facing workflow guidance and the optimization report; regenerated local and public adapter output; and recorded static plus dynamic token-cost evidence.

## Problem

The accepted proposal targeted measured runtime and static token-cost drivers from the `v0.1.1` Token-Friendliness report:

- `implement-handoff` produced a 20,738 estimated-token command output.
- `workflow` was the largest public skill at 6,674 estimated tokens.
- `code-review` was above the warning range at 4,726 estimated tokens.
- All ten required transition benchmarks read active public skill files.

The core goal was not just to make skills shorter. The change needed to help agents perform the right narrow read first while preserving workflow, review, validation, material-finding, and milestone-handoff safety contracts.

## Decision Trail

| Source | Decision | Why it mattered |
|---|---|---|
| Proposal | Use progressive loading for `workflow`, `implement`, and `code-review`. | Targets measured high-cost public skills without broad deletion. |
| Proposal review | Require a testable quick-guide shape, workflow migration accounting, durable comparison report, regenerated public output before dynamic benchmarks, protected `code-review` content, and concrete forbidden broad-search wording. | Made the optimization reviewable and protected safety contracts. |
| Spec requirements | `R2`-`R6` define quick guides, handoff inspection, workflow migration, code-review preservation, and section-first reading guidance. | Drove canonical skill and workflow-doc edits. |
| Spec requirements | `R7`-`R10` require generated output refresh, static measurement, dynamic benchmark evidence, and a durable optimization report. | Drove generated adapter updates and M4 evidence. |
| Spec requirements | `R11`-`R12` preserve public portability and review/validation gates. | Kept maintainer-only details out of shipped skills and kept review stages intact. |
| Architecture decision | No architecture artifact was required. | The approved scope changed public skill text, docs, generated output, and evidence only; no runtime architecture, persistence, API, or deployment boundary changed. |
| Plan | M1 static proof, M2 canonical guidance, M3 generated output, M4 benchmark evidence. | Split the work into reviewable milestones with independent validation. |
| Code review | M1-M4 each completed `clean-with-notes` with no material findings. | No review-resolution was required before final explanation and verify. |

## Diff Rationale By Area

| File or area | Change | Reason | Source artifact | Test/evidence |
|---|---|---|---|---|
| `scripts/test-skill-validator.py` | Added static proof helpers for quick-guide labels, top placement, `implement` handoff guidance, workflow migration evidence, and protected `code-review` contracts. | M1 needed testable proof before canonical skill edits. | `R2`, `R3`, `R4c`, `R5a`, `R6`, test spec `T1`-`T6`. | `python scripts/test-skill-validator.py` passed after M1/M2. |
| `skills/workflow/SKILL.md` | Added `## Quick operating guide`, compressed long routing/lifecycle prose, and kept required routing, claim-boundary, stop-condition, lifecycle, and handoff anchors. | Make the public router usable from a shorter top section while preserving safety. | `R2`, `R4`, `R6`, `R11`, `R12`. | `python scripts/validate-skills.py`; static token measurement: `workflow` 6,674 to 4,857. |
| `skills/implement/SKILL.md` | Added `## Quick operating guide` and `## Handoff inspection budget` requiring active plan `Current Handoff Summary` before broad milestone search. | Directly address the `implement-handoff` broad output spike and state-discovery cost. | `R2`, `R3`, `R6`, `R12`. | Static validator checks; dynamic benchmark `implement-handoff` largest command output 20,738 to 3,098. |
| `skills/code-review/SKILL.md` | Added `## Quick operating guide` and compressed repeated input/template prose while preserving independent-review, mixed-evidence, material-finding, detailed-record, handoff, stop-condition, and result-format contracts. | Reduce repeated prose without weakening review safety. | `R2`, `R5`, `R12`. | Static validator checks; static token measurement: 4,726 to 4,671. |
| `docs/workflows.md` | Added workflow detail ownership guidance for summarized public-skill content. | Ensure workflow safety topics moved or summarized from `workflow` still have an explicit owner surface. | `R4b`, `R4c`. | Workflow migration table in the optimization report. |
| `docs/reports/token-cost/optimizations/2026-05-11-progressive-loading-high-cost-skills.md` | Added workflow migration table, static before/after sizes, dynamic before/after targeted benchmark table, largest-output/read-count evidence, and remaining warning explanations. | Provide the durable before/after comparison required for review. | `R8`, `R9`, `R10`. | M4 benchmark run and reviewer inspection of `/tmp/rigorloop-token-progressive-loading-m4/*-run1.analysis.yaml`. |
| `.codex/skills/` and `dist/adapters/` | Regenerated local Codex mirror and public adapters for Codex, Claude, and opencode from canonical skills. | Dynamic benchmarks must measure regenerated public Codex skill output, not stale canonical-only edits. | `R7`, `R7a`, `R7b`, `R11`. | `python scripts/build-skills.py --check`; `python scripts/build-adapters.py --version 0.1.1 --check`; `python scripts/validate-adapters.py --version 0.1.1`; `python scripts/test-adapter-distribution.py`. |
| `specs/progressive-loading-high-cost-public-skills.test.md` | Added traceable test spec for static proof, generated-output proof, dynamic benchmark evidence, and safety-preservation checks. | Every `MUST` needed a proof path before implementation. | Accepted spec and plan-review outcomes. | Lifecycle validation and milestone validations. |
| `docs/plans/2026-05-11-progressive-loading-high-cost-public-skills.md` | Kept milestone state, validation notes, decisions, surprises, and current handoff summary synchronized through M1-M4, review closeout, and explain-change handoff. | The active plan owns live milestone and next-stage state. | Workflow contract and plan requirements. | M4 closed after code-review; explain-change hands off to `verify`. |
| `docs/changes/2026-05-11-progressive-loading-high-cost-public-skills/` | Added change metadata, review records for plan-review findings, review-resolution evidence, and this explanation. | Non-trivial work requires a durable change-local evidence pack. | Plan-review `PL-PR1`, repository workflow contract. | `python scripts/validate-change-metadata.py`; `python scripts/validate-review-artifacts.py`. |

## Tests Added Or Changed

| Test or proof | What it proves | Why this level is appropriate |
|---|---|---|
| `scripts/test-skill-validator.py` quick-guide tests | The optimized skills can be checked for required quick-guide labels and top placement. | Static contract proof is enough for heading/label shape. |
| `scripts/test-skill-validator.py` handoff tests | `implement` names `Current Handoff Summary` and forbids broad repository search for handoff-state inference. | The requirement is textual behavior guidance, so stable phrase checks are appropriate. |
| `scripts/test-skill-validator.py` protected-content checks | `code-review` still carries protected safety contracts. | Prevents accidental deletion during compression. |
| `python scripts/validate-skills.py` | Canonical skills remain valid after edits. | Required for public skill surface changes. |
| `python scripts/build-skills.py --check` and adapter commands | Generated local/public output is current. | Required before dynamic benchmark evidence can be accepted. |
| `python scripts/run-token-cost-benchmarks.py --suite benchmarks/token-cost/manifest.yaml --release v0.1.1 --tool codex --output-dir /tmp/rigorloop-token-progressive-loading-m4` | Runtime behavior was measured against regenerated public Codex skills. | Dynamic evidence is the only proof of runtime token-cost behavior. |
| Manual M4 result-quality comparison | No targeted benchmark regressed from `pass` to `fail`. | Result quality requires review of benchmark outputs in addition to numeric signals. |

## Validation Evidence Available Before Final Verify

Validation recorded in the active plan and `change.yaml` includes:

- `python scripts/test-skill-validator.py` passed, 62 tests after canonical skill guidance.
- `python scripts/validate-skills.py` passed, validating 23 skill files after canonical and generated-output milestones.
- `python scripts/measure-skill-tokens.py` passed: total 52,843 estimated tokens; `workflow` 4,857, `implement` 3,963, `code-review` 4,671.
- `python scripts/build-skills.py --check` initially found stale generated local skills in M3, then passed after regeneration.
- `python scripts/build-adapters.py --version 0.1.1 --check` initially found stale public adapter output in M3, then passed after regeneration.
- `python scripts/validate-adapters.py --version 0.1.1` passed.
- `python scripts/test-adapter-distribution.py` passed, 68 tests.
- `python scripts/run-token-cost-benchmarks.py --suite benchmarks/token-cost/manifest.yaml --release v0.1.1 --tool codex --output-dir /tmp/rigorloop-token-progressive-loading-m4` passed for the full required suite.
- `python scripts/validate-token-cost-report.py docs/reports/token-cost/releases/v0.1.1.yaml` passed.
- `python scripts/test-token-cost-measurement.py` passed, 24 tests.
- `python scripts/test-token-cost-report-validation.py` passed, 16 tests.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-11-progressive-loading-high-cost-public-skills/change.yaml` passed.
- Artifact lifecycle validation passed with the existing `docs/plan.md` lifecycle-language warning.
- `git diff --check` passed for the touched milestone surfaces.

Code-review M4 also reran targeted evidence checks and found the optimization report metrics matched `/tmp/rigorloop-token-progressive-loading-m4/*-run1.analysis.yaml` for the targeted benchmarks.

Hosted CI status is not known from this local workflow stage.

## Review Resolution Summary

Plan-review recorded material finding `PL-PR1`; it was resolved before implementation by requiring the change-local artifact pack, change metadata validation, durable reasoning/evidence surfaces, change metadata validation in milestone commands, and change-local pack closeout expectations.

Implementation code reviews M1, M2, M3, and M4 each completed `clean-with-notes` with no material findings and no review-resolution required.

Durable review surfaces:

- `docs/changes/2026-05-11-progressive-loading-high-cost-public-skills/review-log.md`
- `docs/changes/2026-05-11-progressive-loading-high-cost-public-skills/review-resolution.md`
- `docs/changes/2026-05-11-progressive-loading-high-cost-public-skills/reviews/plan-review-r1.md`
- `docs/changes/2026-05-11-progressive-loading-high-cost-public-skills/reviews/plan-review-r2.md`

## Alternatives Rejected

- Shrink all skills aggressively: rejected because it risked deleting safety-critical behavior and did not target the measured runtime amplification.
- Only reduce static size of `workflow` and `code-review`: rejected because it would not directly address the `implement-handoff` broad-search spike or whole-skill read behavior.
- Add a hard `workflow` token budget in this slice: rejected because the accepted policy keeps early warnings as warning-only until more comparable reports exist.
- Add `skill section read` analyzer support in this slice: deferred until quick-guide sections are stable and range-to-heading mapping can be reliable.
- Split `code-review` templates into reference files in this slice: deferred until compression and measurement show whether the problem remains.

## Scope Control

The change preserved the explicit non-goals:

- no release token-friendliness gate changes;
- no benchmark schema changes;
- no workflow order changes;
- no new hard token thresholds;
- no optimization of every skill;
- no split of `code-review` reference templates;
- no hand-edited generated adapter output;
- no removal of review, validation, material-finding, milestone-handoff, or public portability safety guidance.

Repository-maintainer validation commands and generated-output details are kept in specs, test specs, plans, reports, and change-local evidence rather than shipped public skills.

## Risks And Follow-Ups

- Whole-skill-style reads persisted across all required dynamic runs. This suggests runtime prompt/tool behavior still drives some cost.
- Targeted broad-search count increased from 2 to 8 even though `implement-handoff` command-output amplification improved. A later analyzer or prompt update may be needed.
- `workflow` remains above the 4,000 warning target at 4,857 estimated tokens, justified by retained safety-critical router guidance.
- `code-review` remains above the target range at 4,671 estimated tokens, justified by protected review contracts.
- Future follow-up: add `skill section read` measurement after stable section boundaries exist.
- Future follow-up: consider externalizing `code-review` reference templates only if later measurements show the problem remains.

## Current Workflow State

All implementation milestones are closed after clean code-review. This explain-change stage is complete, and the active plan's current next stage is `verify`.

This artifact does not claim final verify, branch-ready, PR-ready, `pr-body-ready`, or `pr-open-ready` status.
