# Explain Change: Cost-Bounded Rigor M3 Validation-Budget Guidance

## Summary

This branch implements the M3 cost-bounded-rigor slice: validation-budget guidance.

The implementation keeps validation targeted by default when changed paths are known, while preserving mandatory broader validation when an authoritative trigger requires it. The only behavior-facing workflow change is a short `docs/workflows.md` owner-surface section that states which artifacts own validation guidance or executable validation behavior. The selector and CI wrapper behavior are unchanged.

## Problem

After M1 and M2, RigorLoop had scope-budget guidance and bounded-evidence reminders, but validation-budget ownership was still easy to blur. Without an explicit owner split, contributors could treat stage skill prose as executable validation authority, run broad smoke by habit, or assume guidance-only wording changed selected-check behavior.

M3 addresses that workflow-amplification risk without adding release work, adapter work, lifecycle token-cost reports, dynamic benchmarks, hard token gates, or broad skill rewrites.

## Decision Trail

| Decision source | Decision |
|---|---|
| Accepted proposal | M3 is the validation-budget slice: stage validation remains targeted unless release, test-spec, review-resolution, broad-smoke, or plan triggers apply. |
| M3 spec | `R1`-`R4` require targeted validation first and trigger-driven broad smoke; `R5`-`R7` require owner-surface separation and guidance-only guardrails. |
| M3 spec | `R8`-`R10` require selector behavior changes to have executable proof and require the implementation to record whether selector behavior changed. |
| M3 spec | `R11`-`R16` keep stage skills concise and keep lifecycle token-cost, release, adapter, dynamic benchmark, hard-token-gate, and progressive-loading work out of scope. |
| M3 test spec | `T1`-`T11` define static, selected-integration, lifecycle, manual review, and final-verify proof. |
| M3 plan | M1 is one milestone: owner-surface audit and minimal validation-budget guidance. |
| Code review | `code-review-m1-r1` found no material findings and closed M1. |

Architecture was not required. The approved spec, spec-review, and plan-review scoped this to workflow guidance, static proof, and lifecycle evidence, with no runtime architecture, persistence, external API, release packaging, adapter packaging, or security-boundary change.

## Diff Rationale By Area

| File | Change | Reason | Source artifact | Test/evidence |
|---|---|---|---|---|
| `specs/cost-bounded-rigor-m3-validation-budget-guidance.md` | Added the focused M3 contract and approved it after spec-review. | Provide a normative contract before changing validation-budget guidance. | Accepted proposal; M3 spec `R1`-`R19`. | Spec-review receipt and lifecycle validation. |
| `specs/cost-bounded-rigor-m3-validation-budget-guidance.test.md` | Added the active, maintainer-approved M3 test spec. | Map M3 requirements and edge cases to static, selected-integration, lifecycle, and manual proof. | M3 spec `R1`-`R19`; test cases `T1`-`T11`. | Test-spec lifecycle validation and direct maintainer approval. |
| `docs/plans/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance.md` | Added and maintained the active M3 plan, owner-surface audit, validation notes, and current handoff state. | Keep implementation narrow, record selector/no-change rationale, and keep workflow state synchronized. | M3 plan M1; workflow state-owner rules. | Plan-review receipt, selected validation, code-review receipt. |
| `docs/plan.md` | Registered M3 as active and updated its next stage as lifecycle gates progressed. | Keep the plan index aligned with the active plan body. | Plan file policy and workflow state sync. | Artifact lifecycle validation. |
| `docs/workflows.md` | Added `Validation owner surfaces` and a guidance-only guardrail. | Make `docs/workflows.md` the contributor-facing guide while keeping executable selected-check behavior in selector scripts and CI wrapper. | M3 spec `R5`-`R7`; plan M1. | `scripts/test-select-validation.py` stable cue checks; code review. |
| `scripts/test-select-validation.py` | Added stable owner-surface terms to existing validation-layering proof. | Prove the new workflow guidance exists without freezing a full exact sentence or changing selector behavior. | Test spec `T2`, `T6`; plan M1. | Red/green targeted test; full selector regression. |
| `docs/changes/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance/change.yaml` | Recorded requirements, changed files, validation evidence, and latest review state. | Keep change-local metadata traceable for review, explain-change, verify, and PR. | Workflow change metadata convention. | Change metadata validator and selected CI. |
| `docs/changes/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance/review-log.md` and `reviews/*.md` | Recorded clean spec-review, plan-review, and code-review evidence. | Preserve formal lifecycle review evidence before downstream reliance. | Formal review recording rules. | Review artifact validation in closeout mode. |
| `docs/proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md` | Added M2 and M3 follow-on artifact links. | Keep the accepted proposal's follow-on artifact trail current. | Proposal follow-on artifact convention. | Artifact lifecycle validation. |
| `docs/plans/2026-05-14-cost-bounded-rigor-m2-selected-skill-reminders.md` | Marked M2 done after merged PR #55. | Establish M3's baseline: M2 is complete and no longer the active next slice. | Current branch starts after PR #55 merge. | Artifact lifecycle validation. |

## Tests Added Or Changed

- `scripts/test-select-validation.py::ValidationSelectionTests.test_workflow_guidance_aligns_with_validation_layering_contract`
  - Added stable checks for `Validation owner surfaces`, contributor-facing validation guidance, executable check selection, skill-local reminders, change-specific requirements, finding-specific requirements, and release-specific requirements.
  - This proves the owner split required by M3 without making the test depend on one exact prose sentence.

No selector behavior tests were added because selector behavior did not change. The active test spec allows static proof and manual review for guidance-only changes, while reserving selector regression coverage for actual changes to selector behavior, wrapper behavior, or selected-check behavior.

## Validation Evidence Available Before Final Verify

Implementation evidence already recorded:

- `python scripts/test-select-validation.py ValidationSelectionTests.test_workflow_guidance_aligns_with_validation_layering_contract` failed before `docs/workflows.md` gained the owner-surface guidance.
- `python scripts/test-select-validation.py ValidationSelectionTests.test_workflow_guidance_aligns_with_validation_layering_contract` passed after the guidance edit.
- `python scripts/test-select-validation.py` passed after M1 guidance and static proof.
- `python scripts/select-validation.py --mode explicit --path docs/workflows.md --path scripts/test-select-validation.py --path docs/plans/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance.md --path docs/plan.md --path docs/changes/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance/change.yaml` passed with selected checks `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `selector.regression`; `broad_smoke_required` was false.
- `bash scripts/ci.sh --mode explicit --path docs/workflows.md --path scripts/test-select-validation.py --path docs/plans/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance.md --path docs/plan.md --path docs/changes/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance/change.yaml` passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/cost-bounded-rigor-m3-validation-budget-guidance.md --path docs/plans/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance.md --path docs/plan.md --path docs/workflows.md --path docs/changes/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance/change.yaml` passed.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance/change.yaml` passed.
- Code-review recording validation passed with review-artifact, lifecycle, change-metadata, selected CI, and `git diff --check --` checks.
- Explain-change validation passed with selected lifecycle and change-metadata checks, selected CI, and `git diff --check --`.

This is not final verify evidence. Final `verify` still needs to check the complete branch state against the accepted plan, test spec, review-resolution state, and release metadata triggers.

## Review Resolution Summary

No material code-review findings exist for M3 M1.

- `spec-review-r1`: clean, no material findings.
- `plan-review-r1`: clean, no material findings.
- `code-review-m1-r1`: clean-with-notes, no material findings.
- `review-resolution.md`: not required.

## Alternatives Rejected

| Alternative | Why rejected |
|---|---|
| Change selector or CI wrapper behavior in M3 M1. | The owner-surface gap was guidance and proof, not executable check selection. Selector changes would require focused plan/test-spec coverage and regression proof. |
| Edit `implement`, `code-review`, or `verify`. | The plan audit found those skills already have targeted-validation and broad-smoke cues; M3 `R13` blocks edits without a specific plan-scoped gap. |
| Add lifecycle token-cost summaries. | M3 explicitly excludes lifecycle token-cost summary artifacts; that work belongs to a later conditional slice. |
| Run dynamic benchmark comparison. | This branch changes workflow guidance and static proof only; the active test spec makes dynamic benchmark comparison unnecessary unless a later approved artifact requires it. |
| Run release or adapter validation. | No release metadata, adapter packaging, generated public adapter output, or authored skill source changed. |
| Freeze exact workflow prose in tests. | The test spec calls for stable behavior cues and warns against brittle exact-sentence checks. |

## Scope Control

The branch preserves these non-goals:

- no release validation or adapter packaging changes;
- no generated public adapter skill bodies;
- no lifecycle token-cost summary artifact;
- no hard token gates;
- no dynamic benchmark requirement;
- no progressive-loading restructuring;
- no broad stage-skill rewrite;
- no selector behavior change;
- no weakening of formal review, review-resolution, verify, PR, material-finding, release, generated-output, or broad-smoke rules.

## Risks And Follow-Ups

- Final verify must still confirm that validation evidence matches the plan, test spec, review-resolution state, and release metadata triggers.
- Hosted CI has not been observed by this explanation stage.
- Future selector behavior changes remain separate work and must include executable selector regression coverage.
- Future lifecycle token-cost summaries remain deferred and conditional; this branch does not create that artifact class.

## Readiness

M1 implementation and code-review are complete. This explanation records the rationale needed before final verification.

Next stage: `verify`.
