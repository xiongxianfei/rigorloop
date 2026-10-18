# Migrate REM explanatory principles

## Purpose / big picture

Use eleven explanatory principles to answer what deeper engineering relationship matters and why. Preserve every still-applicable commitment of the twenty-two former principles under its Model, Method or authoring owner. The source baseline is `4daf85689562255ddddfeda74c29e3999be8ff2e`; the supplied REM KPS proposal is selective input, not a replacement of current REM semantics.

## Current Handoff Summary

Owning Change: `2026-10-07-rem-principle-migration`; resume through `rigorloop change context`. Mutable progress, assessed subjects, findings and execution results belong to that Change.

## Source artifacts

IR-006, SR-032, SR-033 and SR-056 cover applicable canonical guidance, bounded authoring and preservation of guidance meaning. FEAT-010 and SCN-031, SCN-032 and SCN-052 retain their existing meanings. FUNC-032/033, MOD-008 guidance interpretation, MOD-012 invocation and MOD-013 distribution are reused. The owning [REM guidance composition](../../design/architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/rem-guidance.md) refines knowledge classification without changing allocations, Interfaces or ARs. Accepted basis identities and review standing are recorded in the Change.

## Context and orientation

Canonical content lives in `rem/`. The existing projection script publishes selected REM resources into `skills/*/references/`. Direct consumers also include reconstruction Practices and `design/support/README.md`. Inspect sources directly; no project-map inference is needed. The supplied package is preserved byte-for-byte in private operational storage before baseline restoration.

## Non-goals

- Relaxing requirement parentage, Scenario cardinalities, seven-question analysis, open-question limits, Function coverage, accountable allocation, Interface exposure, subordinate realization, evidence applicability or single semantic authority.
- Wholesale KPS adoption, new runtime/schema behavior, public skills, workflow gates, empirical effectiveness claims or external publication.
- Rewriting historical plans or approval subjects to apply to this migration.

## Requirements covered

SR-032 maps to direct authoritative owner links and complete packaged dependencies. SR-033 maps to distinguishable explanatory principles and preserved authoring rules. SR-056 maps to consistent reading paths, source qualifications and semantic transfer across canonical and generated guidance.

## Milestones

### M1. Migrate knowledge and all consumers

Prerequisites: accepted requirement basis, integrated design approval and delivery-plan approval.

Adapt the eleven named principles with distinct supplied `rem:principle:*` identities, relationship/reason, examples, limits and scoped sources. Do not import proposal release, KPS-conformance or review metadata. Retain existing source IDs; add focused source notes only where used.

Account for every old principle paragraph, including rationale, commitment and application, before retiring its path. Confirm equivalent existing owners or transfer missing meaning. Move general clarity guidance to Operational Support; keep public-entry correspondence with architecture realization. Keep the concise original-identity/current-owner mapping as migration provenance; full assessed clause matrices remain operational evidence.

Reconcile all live consumers and entry paths; retired internal paths get no shims. Use the supported projection script to regenerate resources. Include the new clarity owner in any affected selected skill's packaged dependencies so required reasoning remains available offline. Preserve unrelated authored resources. Historical plans retain their original scope and source identity.

Completion requires a complete candidate, clause-level transfer evidence, verified source scope, resolvable links and no stale live principle references.

### M2. Validate the complete migration

Run focused link/anchor, retired-reference, protected-semantics and projection checks, then repository-selected local CI. Compare each old document with current owners: file-count coverage alone is insufficient. Inspect both normal interpretation and counterexamples: a passing component result does not imply system success, a generated view may be stale, and an explanatory principle cannot optionalize a selected cardinality.

Walk through a requirement, an architecture boundary and an evidence claim from principle to authoritative rule and existing Method. Check that a source reference supports only the stated premise, that examples remain illustrative, and that current project rules remain available without network access.

## Final review checkpoint

One independent whole-change Code Review assesses the complete diff, source support, transfer map, generated resources and actual check results. Correct findings and reassess within that gate. Distinct final Verify follows; neither structural validation nor this plan grants approval.

## Change-level verification

A reader can start at the REM overview or reconstruction Practice, identify an explanatory relationship, distinguish it from selected rules and reach a current Model or Method owner. All twenty-two original identities have recoverable provenance and surviving meaning; all eleven new identities are distinct. The same clarity guidance is available in affected packaged skills. This is semantic/editorial and automated integration evidence, not an empirical human-usability trial.

## Validation plan

- Inspect all old paragraphs and protected invariants against baseline, recording precise owner sections and reasons for consolidation or transfer privately.
- Check rendered local Markdown links and anchors; search live consumers for old numbered principles and deleted paths, distinguishing historical provenance.
- `python scripts/project-operational-guidance.py`: regenerate canonical projections; then `python scripts/project-operational-guidance.py --check` and compare a second generation for determinism.
- Run the existing split-resource regression and inspect generated local clarity links; add no permanent tests that merely repeat prose.
- `git diff --check`: validate formatting.
- `bash scripts/ci.sh --mode local`: complete actual selected scope with qualified Node and D2 renderer; retain the execution result. Track new candidate source paths before selection so required checks can see the entire candidate.
- If a source change affects browser freshness, regenerate through the existing supported command and rerun affected checks while retaining the original result.

## Risks and recovery

A classification change can hide a normative weakening. Preserve exact constraints and inspect entire clauses rather than titles. A general explanation can be mistaken for the only possible rule; distinguish external premises, REM synthesis and current local commitments. Generated links can point to web-only owners; include required local dependencies and inspect the isolated packaged reading path.

Recover this Change's source edits from the recorded baseline without disturbing unrelated work. Preserve the supplied package copy and original identities. Never retarget an old review to changed subjects or claim the package's reported checks as current evidence.

## Dependencies

Requirement Review precedes design reliance; integrated Design Review precedes plan reliance; Delivery Review precedes implementation. Whole-change Code Review and distinct final Verify precede completion. Commit, push and PR publication are outside this local implementation scope.

## Readiness

See the owning Change for current state and actual evidence.
