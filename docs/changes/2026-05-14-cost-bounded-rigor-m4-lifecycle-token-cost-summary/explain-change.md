# Explain Change: Cost-Bounded Rigor M4 Lifecycle Token-Cost Summary

## Summary

This branch implements the M4 cost-bounded-rigor slice: conditional lifecycle token-cost summaries.

The change adds contributor-facing workflow guidance, a reusable Markdown template, the first M4 lifecycle token-cost summary, and stable static proof for the new summary shape. It keeps summaries diagnostic and warning-only: ordinary small changes do not need one, validators do not infer semantic trigger applicability, token totals do not become a hard gate, and release/adapter/benchmark/progressive-loading behavior is unchanged.

## Problem

After M1, M2, and M3, RigorLoop had narrower proposal scope guidance, bounded-evidence guidance, selected skill reminders, and validation-budget owner-surface guidance. The remaining M4 problem was measurement discipline: large workflow-governance or release changes need a compact way to record observable lifecycle cost drivers without turning measurement into another routine artifact.

The accepted proposal identified lifecycle token-cost summaries as conditional evidence for large workflow-governance or release changes, dynamic benchmark warnings, broad-search incidents, and explicit maintainer requests. The M4 spec narrowed that into one implementation slice that defines the report path, required field groups, warning-only boundary, bounded-evidence rule, and no-change boundaries.

## Decision Trail

| Decision source | Decision |
|---|---|
| Accepted proposal | M4 is the lifecycle token-cost summary slice, after M1 scope budget, M2 selected skill reminders, and M3 validation-budget guidance. |
| Accepted proposal | Lifecycle summaries are conditional, not routine, and detailed numeric comparisons remain advisory unless benchmark evidence or a later plan/test-spec requires them. |
| M4 spec | `R1`-`R4` require conditional triggers and prohibit validator-inferred trigger applicability. |
| M4 spec | `R5`-`R14` define the lifecycle summary path and required field groups. |
| M4 spec | `R15`-`R17`, `R21`, and `R26` preserve advisory numeric data, warning-only behavior, stable shape checks, and no hard token gates. |
| M4 spec | `R18`-`R20` preserve release Token-Friendliness evidence, single-authored skill source, and follow-up routing boundaries. |
| M4 spec | `R22`-`R23`, `R27`-`R28` keep selector, release, adapter, benchmark, and progressive-loading behavior unchanged unless later accepted scope broadens them. |
| M4 test spec | `T1`-`T10` map requirements to static proof, selected validation, lifecycle/manual checks, and final verify expectations. |
| M4 plan | M1 is the only implementation milestone: workflow guidance, template, static proof, and first summary. |
| Code review | `code-review-m1-r1` returned clean-with-notes with no material findings and closed M1. |

Architecture was not required. The approved spec, spec-review, and plan-review scoped this to workflow guidance, report template shape, static proof, and one diagnostic Markdown summary, with no runtime architecture, persistence, external API, security-boundary, release packaging, adapter packaging, or hard-to-reverse validation design change.

## Diff Rationale By Area

| File | Change | Reason | Source artifact | Test/evidence |
|---|---|---|---|---|
| `specs/cost-bounded-rigor-m4-lifecycle-token-cost-summary.md` | Added and approved the focused M4 contract. | Define conditional lifecycle summary triggers, path, field groups, advisory numeric boundaries, privacy, and out-of-scope behavior before implementation. | Accepted proposal; M4 spec `R1`-`R29`. | Clean `spec-review-r1`; artifact lifecycle validation. |
| `specs/cost-bounded-rigor-m4-lifecycle-token-cost-summary.test.md` | Added the active, maintainer-approved M4 test spec. | Map every M4 `MUST` to static, selected-integration, lifecycle, manual, or final-verify proof. | M4 spec `R1`-`R29`; test cases `T1`-`T10`. | Test-spec lifecycle validation and direct maintainer approval. |
| `docs/plans/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary.md` | Added and maintained the active M4 plan, trigger decision, validation notes, no-change rationale, and current handoff state. | Keep the implementation to one reviewable M1 slice and record why this change itself requires a lifecycle summary as a large workflow-governance change. | M4 plan M1; workflow state-owner rules. | Clean `plan-review-r1`, clean `code-review-m1-r1`, selected validation. |
| `docs/plan.md` | Registered M4 as active and updated its next stage as lifecycle gates progressed. | Keep the plan index synchronized with the active plan body. | Plan file policy and workflow state sync. | Artifact lifecycle validation. |
| `docs/proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md` | Added the M4 follow-on artifact link. | Keep the accepted proposal's rollout trail current. | Proposal follow-on artifact convention. | Artifact lifecycle validation. |
| `docs/plans/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance.md` | Marked M3 done after merged PR #56. | Establish the correct baseline before starting M4. | Current branch starts after PR #56 merge. | Artifact lifecycle validation. |
| `docs/workflows.md` | Added `Lifecycle Token-Cost Summaries`. | Give contributors the path, trigger set, trigger ownership, warning-only boundary, bounded-evidence expectation, and follow-up routing in the artifact-location guide. | M4 spec `R1`-`R4`, `R15`-`R20`, `R24`; test spec `T1`, `T2`, `T4`, `T5`, `T6`. | Manual review and selected CI. |
| `templates/lifecycle-token-cost-summary.md` | Added the reusable lifecycle summary scaffold. | Make triggered summaries easy to complete while keeping required fields limited to identity, trigger, scope, source artifacts, observed drivers, largest event, result/rationale, and boundary checks. | M4 spec `R5`-`R14`, `R21`, `R24`-`R25`; test spec `T3`, `T5`, `T8`. | `test_lifecycle_summary_template_has_required_field_groups_and_warning_only_boundary`. |
| `docs/reports/token-cost/lifecycle/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary.md` | Added the first M4 lifecycle token-cost summary. | The active plan classifies M4 as a large workflow-governance change; the summary records the trigger, scope, source artifacts, observed cost drivers, largest observed event, result/rationale, and no-follow-up rationale using bounded evidence. | M4 spec `R2`, `R5`-`R14`, `R18`-`R20`, `R24`-`R25`; test spec `T3`, `T4`, `T6`, `T9`. | `test_m4_lifecycle_summary_has_required_shape_and_bounded_evidence_cues`; code-review checklist. |
| `scripts/test-token-cost-report-validation.py` | Added shape-focused lifecycle summary tests. | Prove the template and first summary contain stable headings, path/trigger cues, cost-driver categories, bounded-evidence cues, and forbidden hard-gate exclusions without freezing one exact prose sentence. | M4 spec `R21`; test spec `T3`, `T5`, `T8`. | Focused tests and full token-cost report validation suite. |
| `docs/changes/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary/change.yaml` | Recorded requirements, changed files, validation evidence, and latest review/explain state. | Keep change-local metadata traceable for review, explain-change, verify, and PR. | Workflow change metadata convention. | Change metadata validator and selected CI. |
| `docs/changes/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary/review-log.md` and `reviews/*.md` | Recorded clean spec-review, plan-review, and code-review evidence. | Preserve formal lifecycle review evidence before downstream reliance. | Formal review recording rules. | Review artifact validation in closeout mode. |
| `docs/changes/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary/explain-change.md` | Added this durable rationale. | Explain why the actual diff exists before final verify. | `explain-change` stage contract. | Explain-change validation and selected CI. |

## Tests Added Or Changed

- `scripts/test-token-cost-report-validation.py::TokenCostReportValidatorTests.test_lifecycle_summary_template_has_required_field_groups_and_warning_only_boundary`
  - Proves the template exists at the expected path and contains required lifecycle headings, approved trigger cues, unavailable-data placeholders, warning-only language, bounded-evidence language, driver categories, and no forbidden hard-gate cues.

- `scripts/test-token-cost-report-validation.py::TokenCostReportValidatorTests.test_m4_lifecycle_summary_has_required_shape_and_bounded_evidence_cues`
  - Proves the first M4 summary exists at the expected path and contains stable field groups, M4 identity, trigger, plan/test-spec links, informational status, unavailable-data cues, bounded-evidence cues, follow-up routing, driver categories, and no forbidden hard-gate cues.

No release Token-Friendliness YAML schema tests were added because lifecycle summaries are Markdown diagnostic reports, not release report metadata. No selector behavior tests were added because selector behavior did not change; the selected validation and plan-review probes showed the new lifecycle report path is already classified as a token-cost surface.

## Validation Evidence Available Before Final Verify

Implementation evidence already recorded:

- `python scripts/test-token-cost-report-validation.py TokenCostReportValidatorTests.test_lifecycle_summary_template_has_required_field_groups_and_warning_only_boundary` failed before the template existed.
- `python scripts/test-token-cost-report-validation.py TokenCostReportValidatorTests.test_lifecycle_summary_template_has_required_field_groups_and_warning_only_boundary` passed after the template was added.
- `python scripts/test-token-cost-report-validation.py TokenCostReportValidatorTests.test_m4_lifecycle_summary_has_required_shape_and_bounded_evidence_cues` passed after the first summary was added.
- `python scripts/test-token-cost-report-validation.py` passed with 18 tests.
- `python scripts/select-validation.py --mode explicit --path docs/workflows.md --path templates/lifecycle-token-cost-summary.md --path docs/reports/token-cost/lifecycle/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary.md --path scripts/test-token-cost-report-validation.py --path docs/plans/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary.md --path docs/plan.md --path docs/changes/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary/change.yaml` passed with selected checks `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `selector.regression`, `token_cost.regression`, and `token_cost.report_regression`; `broad_smoke_required` was false.
- `bash scripts/ci.sh --mode explicit --path docs/workflows.md --path templates/lifecycle-token-cost-summary.md --path docs/reports/token-cost/lifecycle/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary.md --path scripts/test-token-cost-report-validation.py --path docs/plans/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary.md --path docs/plan.md --path docs/changes/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary/change.yaml` passed.
- Full branch-changed selected CI passed after M1 implementation for the M4 artifact set, including review artifacts, lifecycle artifacts, workflow guidance, template, lifecycle summary, and token-cost tests.
- Code-review recording validation passed with selected validation, review-artifact closeout, change metadata validation, artifact lifecycle validation, selected CI, and `git diff --check --`.

Explain-change evidence:

- This explanation records why no before/after dynamic benchmark comparison was required: the branch changes guidance, template/report shape, static proof, and one diagnostic summary, not runtime benchmark behavior, analyzer behavior, benchmark prompts, release report schema, or model/tool versions.
- `python scripts/select-validation.py --mode explicit --path docs/changes/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary/change.yaml --path docs/changes/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary/review-log.md --path docs/changes/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary/reviews/code-review-m1-r1.md --path docs/changes/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary/explain-change.md --path docs/plans/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary.md --path docs/plan.md` passed; `broad_smoke_required` was false.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary` passed.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary/change.yaml` passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary/change.yaml --path docs/changes/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary/review-log.md --path docs/changes/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary/reviews/code-review-m1-r1.md --path docs/changes/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary/explain-change.md --path docs/plans/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary.md --path docs/plan.md` passed.
- `bash scripts/ci.sh --mode explicit --path docs/changes/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary/change.yaml --path docs/changes/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary/review-log.md --path docs/changes/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary/reviews/code-review-m1-r1.md --path docs/changes/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary/explain-change.md --path docs/plans/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary.md --path docs/plan.md` passed.
- `git diff --check --` passed.

This is not final verify evidence. Final `verify` still needs to check the complete branch state against the accepted plan, test spec, code-review record, lifecycle summary trigger, release metadata if any, and selected validation evidence.

## Review Resolution Summary

No material review findings exist for M4 M1.

- `spec-review-r1`: clean, no material findings.
- `plan-review-r1`: clean, no material findings.
- `code-review-m1-r1`: clean-with-notes, no material findings.
- `review-resolution.md`: not required.

## Alternatives Rejected

| Alternative | Why rejected |
|---|---|
| Require lifecycle token-cost summaries for every change. | M4 `R1`-`R3` make summaries conditional and allow ordinary small feature, docs, proposal, and skill edits to omit them when no trigger applies. |
| Make validators infer whether a trigger should have applied. | M4 `R4` and `R21` keep trigger applicability as artifact/reviewer judgment and limit tests to section/path/shape proof. |
| Add hard token thresholds or release gates. | M4 `R15`-`R17` and `R26` keep numeric comparison advisory and require later proposal/spec evidence before blocking thresholds. |
| Run before/after dynamic benchmark comparison. | The branch does not change runtime benchmark behavior, analyzer behavior, benchmark prompts, release report schema, or model/tool versions. M4 `R17` says guidance/template/validation-shape changes do not require this comparison. |
| Change selector behavior for `docs/reports/token-cost/lifecycle/**`. | Existing selector behavior already classifies `docs/reports/token-cost/**` as token-cost; changing selector behavior would have required focused scope and regression coverage. |
| Modify release or adapter packaging. | M4 `R18`, `R19`, and `R28` preserve release Token-Friendliness reports, single-authored skill source, and generated adapter output boundaries. |
| Implement progressive-loading follow-through. | M4 `R27` keeps `workflow`, `implement`, and `code-review` progressive-loading work out of scope. |
| Freeze exact summary prose in tests. | The test spec calls for stable headings, field-group labels, path placement, driver categories, and forbidden-boundary checks instead of exact full-sentence assertions. |

## Scope Control

The branch preserves these non-goals:

- no routine lifecycle summaries for ordinary changes;
- no hard token gates, hard release gates, or CI blockers based on lifecycle token totals;
- no default before/after dynamic benchmark comparison;
- no release Token-Friendliness YAML schema change;
- no release packaging, adapter packaging, generated adapter output tracking, or benchmark suite expansion;
- no generated public adapter skill bodies added back to tracked source;
- no progressive-loading restructuring or high-cost skill rewrite;
- no selector semantic trigger inference;
- no weakening of formal review, verify, PR, material-finding, release, or follow-up routing rules.

## Risks And Follow-Ups

- Final verify must still check that the required M4 lifecycle summary exists, contains the required field groups, and matches the accepted plan/test spec trigger.
- Final verify must also confirm no-change rationale for selector, release, benchmark, adapter, generated-output, and progressive-loading surfaces.
- Hosted CI has not been observed by this explanation stage.
- Trigger expansion or hard token thresholds remain future work only after 3-5 completed lifecycle summaries show actionable value and a later proposal or spec accepts the change.
- No current follow-up is required by the first M4 summary.

## Readiness

M1 implementation and code-review are complete. This explanation records the rationale needed before final verification.

Next stage: `verify`.
