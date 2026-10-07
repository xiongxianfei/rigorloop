# Consolidate REM publication references

## Purpose / big picture

Make external support easy to inspect through one rich document per publication, retaining claim-specific source mappings and the current REM rules.

## Current Handoff Summary

Owning Change: `2026-10-07-rem-reference-consolidation`; resume through `rigorloop change context`. Mutable progress and actual review/verification evidence belong to that local Change.

## Source artifacts

Reuse IR-006, SR-032, SR-033 and SR-056, with FEAT-010 and SCN-031/032. SCN-052 supplies portable-guidance context under its existing IR-009/FEAT-015 ownership. FUNC-032/033/034 and existing allocations remain unchanged. MOD-008 owns [REM composition](../../design/architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/rem-guidance.md); MOD-013 owns projection, MOD-012 invocation and MOD-007 assessment. Applicable bases are selected in the Change.

## Context and orientation

Inspect current sources directly. Twelve concise notes under `rem/sources/` support existing claims. Nine user-supplied publication references have richer explanations, twelve broken local links and imported inspection/version metadata. The separately completed version-basis Change has six pending paths; preserve its REM edition/KPS declaration while reconciling overlaps. Save incoming originals and a working baseline privately before editing. No project-map reliance is needed.

## Non-goals

Changing REM rule semantics, KPS certification, full ISO clause inspection, empirical REM effectiveness claims, new runtime/schema/tooling, merge and release are excluded.

## Requirements covered

SR-032: canonical publication navigation and stable claim mappings. SR-033: source support distinct from REM-owned rules and actual authority. SR-056: equivalent meanings, useful limits and accessible citations across repository and packaged guidance.

## Milestones

### M1. Reconcile reference knowledge and consumers

Prerequisites: independent Requirement, integrated Design and Delivery reviews. Retain nine reference identities and one document per publication. Merge all twelve source notes with their dates, exact locators, contributions and limits; NASA's six notes become separate sections. Preserve S01–S17 mappings already in SOURCES.md. Attribute incoming inspection reports, verify new adopted claims against primary sources and state incomplete inspection explicitly. Inherit central method metadata instead of independently maintaining version/KPS fields. Repair the twelve links with accurate labels to current owners and remove deferred-specification claims. Update every live citation, regenerate selected skill resources using the existing projector, then remove duplicate source notes without compatibility shims. Historical plans keep their original meaning.

Completion requires source-by-source preservation inspection, working links/anchors, no surviving active old-path consumers, unchanged rule content except citation targets, and reproducible generated resources.

### M2. Validate and deliver

Run focused checks and applicable local CI against all pending changes, including the version declaration. Resolve defects before the whole-change gate. Following independent review and distinct final Verify, commit the bounded candidate, push the current branch and update existing PR #210 from its complete diff and current evidence. Preserve its open/draft state; do not merge or release.

## Final review checkpoint

One independent whole-change Code Review assesses the complete candidate, content preservation, source limits, navigation and generated consumers. Corrections and reassessment remain within that gate. A distinct final Verify owns completion. Earlier version approval remains historical; it is not retargeted to altered files.

## Change-level verification

A reader follows an existing S identifier to its exact supported contribution, locates the publication and inspected scope, distinguishes source claims from current REM rules, and finds the single method-version basis. Repository and packaged citations reach the same contribution. No retired live path or implied inspection approval remains.

## Validation plan

- Inspect a twelve-note migration map and nine incoming-reference dispositions against preserved originals; compare protected Model/Method text after normalizing citation targets.
- Check local links and anchors across REM, changed guidance and the actual generated resources; identify any external retrieval limitations separately.
- Run `python3 scripts/project-operational-guidance.py --check`, repeat generation for determinism and inspect actual selected resource inventory.
- Run `python3 -m unittest discover -s tests/skill -p skill_guidance_tests.py -k test_split_rem_projection_preserves_links_and_retires_only_generated_resources`.
- Run `git diff --check` and `bash scripts/ci.sh --mode local` with qualified Node/D2 after newly authored paths are tracked. Retain actual complete result and selection, not just a launch or plan.
- Use existing validation and independent semantic assessment; no permanent tests that merely mirror prose or version numbers.

## Risks and recovery

Imported provenance could be mistaken for performed inspection, and broad publications could obscure claim limits. Keep explicit per-claim scope and attributed incoming reports. Preserve all incoming bytes privately; tracked retired notes are recoverable from the recorded Git baseline. Restore bounded paths from that baseline if needed, preserving pending user/version work. Refresh all consumers before deletion so current operation needs no historical fetch.

## Dependencies

Requirement approval precedes design reliance, Design approval precedes delivery reliance, and Delivery approval precedes implementation. Complete checks precede whole-change approval and final Verify; external handoff uses the verified candidate and existing user authorization.

## Readiness

See the owning Change for actual current status and evidence.
