# Integrate original Practices with current REM rules

## Purpose / big picture

Keep the five original Practices restored by the user as usable, stage-based guidance. Apply current REM semantics within those stages and reconnect canonical and packaged reading paths. This follows the explicit user decision to use current REM rules.

## Current Handoff Summary

Owning Change: `2026-10-07-rem-practice-integration`; resume through `rigorloop change context`. Mutable progress, reviews, evidence and completion belong to that Change. The previously completed principle migration describes its own historical candidate and is not reopened by this work.

## Source artifacts

Reuse IR-006, SR-032, SR-033 and SR-056, FEAT-010 and SCN-031/032/052. FUNC-032/033 retain guidance selection and authoring behavior; FUNC-034 retains assessment intent. [REM guidance composition](../../design/architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/rem-guidance.md) owns this refinement under MOD-008. MOD-012 owns skill instructions and MOD-013 owns resource projection. No new Functions, allocations, Interfaces or ARs are needed. Accepted bases and reviews are recorded through the Change.

## Context and orientation

The five files in `rem/practices/` are incoming source material, with useful local stage detail but incompatible optional-rule wording and unresolved links. The working tree also contains an uncommitted, previously verified principle migration. Preserve that work. Inspect current sources directly; this plan does not rely on project-map freshness. Private before-state copies preserve the restored originals and existing working candidate. Prior reviewed supporting guides and example can be reconstructed from HEAD plus the prior candidate diff.

## Non-goals

Changing current REM rules, replacing the eleven principles, importing the entire incoming Method library, claiming KPS conformance or empirical usability, and commit/push/PR publication are outside scope.

## Requirements covered

| Requirement | Implementation and proof |
| --- | --- |
| SR-032 | Current owner links, navigation and required local packaged guidance |
| SR-033 | Useful inline stages applying current requirement, Scenario, behavior, architecture and assurance rules |
| SR-056 | Preserved explanations and examples; compatible summaries across canonical and skill paths; qualified evidence claims |

## Milestones

### M1. Reconcile Practices and consumers

Prerequisites: accepted requirement basis, integrated Design Review and Delivery Review.

Preserve the original five filenames and identities and all 28 stages, including explanations, examples, troubleshooting and fallback actions except necessary semantic corrections. Apply all seven 5W2H questions without mandatory worksheets; keep all material Change unknowns visible while enforcing the per-IR/SR consequential-question limit. Keep parentage, Scenario ownership, Function coverage, single accountable allocation, Interface exposure and subordinate realization explicit at their relevant stages. Preserve view tailoring with coverage of material concerns and project-required views.

Distinguish model conformance, requirements validation, product verification and intended-use validation. Performed inspection or analysis can establish a scoped design claim before implementation; an unrun plan cannot establish product results. Keep original source identities but remove unadopted version/review/KPS claims. Use existing qualified sources, narrowing attribution where necessary.

Restore the Practices index, prior reviewed supporting `understand-rem/` guides and worked example, moving the example to `rem/practices/WORKED-EXAMPLE.md`. Retire the old core Practice paths and update all current consumers; preserve historical references. Project renamed engineer/assessment Practices and the moved example to existing skills, plus architecture-decision guidance to architecture-design. Update resource maps and regenerate through the supported projector; preserve unrelated files.

Complete when the entire authored/generated candidate is internally consistent and the original-to-current changes are inspectable.

### M2. Demonstrate preservation and integration

Compare original and candidate stages and material prose, with reasons for changed clauses. Compare canonical Model/Method bytes to the before-state, allowing only documented navigation-target replacements for relocated Practices and the example. Check all local links and anchors and retired live paths. Inspect actual packaged local stage content; optional deeper citations can remain remote, but required reasoning cannot depend on the Design checkout or a network lookup.

Walk through normal and failure release selection, including parentage, Scenario/Feature relationships, Function coverage, Module accountability and exposure. Inspect counterexamples: missing allocation, a view omission hiding a concern, unperformed assessment reported as success, and product verification confused with intended-use success. These are editorial/analytical observations, not a human usability trial.

## Final review checkpoint

One independent whole-change Code Review follows complete implementation and relevant checks. It assesses this integration against the saved before-state and its compatibility with the cumulative uncommitted candidate. Exact manifests identify assessed subjects; earlier approvals retain their original meaning. Corrections are reassessed within that gate. Distinct final Verify follows.

## Change-level verification

A reader can start from any of the five Practices, act using its local stages, apply current REM rules and find canonical deeper guidance. Packaged selected routes retain the same meaning without internal Design files. Every deletion has a reconciled current consumer or a justified historical reference. All selected repository checks and independent semantic review support the scoped result.

## Validation plan

- Compare the five saved originals and all 28 stages; independently inspect changed wording and preserved examples/fallbacks.
- Check rendered Markdown links/anchors and current references to retired paths; distinguish historical plans from current guidance.
- Run `python3 scripts/project-operational-guidance.py`, `--check`, and repeat generation for determinism.
- Run the existing `test_split_rem_projection_preserves_links_and_retires_only_generated_resources` regression and inspect actual selected resources and skill resource maps.
- Run skill validation for affected authored skills and `git diff --check`.
- Track new candidate paths before `bash scripts/ci.sh --mode local`; use the qualified Node runtime and D2 renderer and retain its actual result. Correct failures and rerun affected scope as justified.
- Add no permanent tests that simply duplicate prose; existing executable packaging/validation regressions and independent semantic inspection address the relevant failures.

## Risks and recovery

An optional prompt can weaken a required analysis; a concise stage can hide an owner or evidence limit. Compare against current owners and inspect the negative examples. An apparently repaired link can point to a different operation; revise labels and explanatory scope together. Restore only this task's changes from its before-state if needed, keeping original Practices and prior principle work recoverable. Do not reset the entire REM tree or reuse historical approval for new bytes.

## Dependencies

Requirement Review precedes design reliance; integrated Design Review precedes delivery reliance; Delivery Review precedes implementation. Current whole-change review and distinct final Verify precede completion. No external action is part of this plan.

## Readiness

See the owning Change for current status and actual results.
