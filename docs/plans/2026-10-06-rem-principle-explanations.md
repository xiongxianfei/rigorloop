# Explain REM principles

## Purpose / big picture

Explain what deeper relationship each REM principle expresses and why it matters, then connect that reasoning to the existing engineering commitment.
Use the refined REM at commit `bd31311864a7a51c113c75c29431071700ecd7f5` as the source baseline while preserving its accepted semantics.

## Current Handoff Summary

- Owning Change: `2026-10-06-rem-principle-explanations`; inspect through `rigorloop change context`.

Mutable progress, review judgments, assessed identities and execution results belong to the owning Change.

## Source artifacts

- Requirement reuse: IR-006, SR-032, SR-033 and SR-056; FEAT-010 and the existing canonical-guidance Scenarios.
- Logical behavior: FUNC-032 selects applicable canonical guidance; FUNC-033 explains authoring rules and correction steps.
- Architecture: MOD-008 owns guidance interpretation under [REM guidance composition](../../design/architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/rem-guidance.md); MOD-012 owns invocation procedures and MOD-013 generated distribution.
- Rules and application owners: [Principles](../../rem/principles/README.md), [Models](../../rem/models/README.md) and [Methods](../../rem/methods/README.md).
- Acceptance of scoped reuse belongs to the owning Change; this plan does not approve unrelated draft capabilities.

## Context and orientation

Each of the 22 principles has a stable ID, title and path.
Most currently state a commitment without explaining its underlying relationship.
The overview and reconstruction reading guide describe Principles as commitments; these entry paths need the same explanatory definition.
Inspect actual sources and consumers; no project-map inference is needed for this bounded prose change.

## Non-goals

- Changing principle identities, REM obligations, requirement parentage, Scenario cardinalities, seven-question analysis, open-question limits, Function coverage, accountable allocation or realization ownership.
- New runtime behavior, schemas, workflow gates, tooling, citations or empirical effectiveness claims.
- Reopening the historical acceptance of the selective integration or updating PR 209.

## Requirements covered

SR-032 maps to identifiable owning explanations and application links.
SR-033 maps to explanatory relationships, rationale and preservation of existing authoring commitments.
SR-056 maps to consistent reading paths, unchanged semantic coverage and bounded claims.

## Milestones

### M1. Explain and reconcile all principles

Prerequisites: accepted requirement reuse, reviewed integrated design reuse and approved delivery plan.
Add a relationship-and-why explanation, retain the REM commitment, and link its existing Model or Method application in all 22 files.
Keep titles and IDs unchanged; explanations are engineering rationale rather than claims of universal empirical laws.
Reconcile the REM overview, principle index and reconstruction knowledge guide; add this plan to the navigation index.
Replace Principle 19's duplicated procedural detail with links only after locating every surviving obligation at its existing owner and recording a clause-to-owner comparison.
Completion requires a complete candidate with source identities, preserved commitments, valid navigation and current generated consumers.

Proof combines direct comparison of original commitments, semantic inspection of all new explanations, local link/anchor checks and repository-selected validation.
Use existing checks; do not add permanent tests that merely mirror prose or its section layout.

## Final review checkpoint

Obtain one independent whole-change Code Review after the complete candidate and checks are available.
Include all explanation, navigation, plan and any generated consumer changes.
Corrections remain in that gate and precede distinct final Verify.

## Change-level verification

Starting from either the REM overview or reconstruction guide, a reader can locate the same principle, identify its explanatory relationship and rationale, distinguish the retained REM commitment and reach its authoritative application.
Every original commitment remains present or has an explicit verified surviving owner; no rationale introduces a stronger guarantee or weaker obligation.
The assessment is an editorial and semantic review, not empirical proof of general method effectiveness or human usability.

## Validation plan

- Compare all 22 principles with the source baseline, including unchanged IDs/titles and the Principle 19 clause-to-owner map.
- Inspect every explanatory relationship for accuracy within existing REM semantics; inspect all new local links and anchors.
- `python scripts/project-operational-guidance.py --check`: confirm projected resources remain current; regenerate through the supported script only if needed.
- `git diff --check`: check changed text formatting.
- `bash scripts/ci.sh --mode local`: run checks selected for the actual complete working-tree change with the qualified Node runtime and required renderer, retaining the execution report.
- If source changes require browser regeneration, use the supported generator and rerun the affected freshness check; preserve the actual original invocation outcome.

## Risks and recovery

Explanatory prose can accidentally strengthen a heuristic into a guarantee or justify a different rule.
Retain explicit commitments and review each explanation against its owning model; correct the explanation instead of broadening the model.
Replacing detailed reminders can hide obligations; require the clause-to-owner map and resolvable application links before removing duplication.
Recover only this Change's edits from the recorded source baseline, preserving unrelated work and original review identities.

## Dependencies

Requirement Review precedes reliance on the requirement basis, integrated Design Review precedes plan reliance, and Delivery Review precedes implementation.
Whole-change Code Review and distinct final Verify precede any completion claim.
No external publication is included in this local revision scope.

## Readiness

See the owning Change for current workflow state and evidence.
