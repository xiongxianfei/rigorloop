# Design directory organization

## Purpose / big picture

Make the approved Skill, CLI and Engineering responsibility hierarchy visible in the repository directories, with System at the root. This bounded follow-on covers document moves and the readers needed to keep those moves usable. It does not implement the unified validation executor or claim whole-initiative closeout.

## Current Handoff Summary

Owning change record: [unified validation and hierarchy](../changes/2026-09-12-unified-validation-model/change.json). Mutable activity and review decisions remain in that record.

## Source artifacts

The user explicitly selected the directory tree. [System](../design/system.md) owns the project layout; [Design](../design/skill/authoring/design.md) preserves the generic model convention with an explicit repository-specific mapping. The prior hierarchy proposal remains the product-direction basis. Existing historical approvals retain their original subjects.

## Context and orientation

The model validator currently accepts only flat or matching-directory model names. The validation selector derives owner paths from the old examples directory. CLI contract tests read the Records fixtures from the old path. These actual readers need coordinated path changes; no record format, CLI executable behavior or test oracle changes are selected.

## Non-goals

No cache/executor implementation, published skill changes, generated package edits, record migration, publication or historical source rewriting.

## Requirements covered

System ownership and Design path/selection obligations retain their stable IDs. The approved project override changes physical paths without changing requirement text, logical ownership or example payloads. Containment, symlink rejection and explicit rejection of unknown nested model paths remain required.

## Milestones

### M1. Relocate and reconcile

Move the twelve model documents into the three main directories and root System file. Keep smaller children as parent sections. Move Records examples into CLI's records example namespace and Workflow examples into Skill's workflow namespace. Update current relative navigation, keep historical records and source identities intact, and remove only newly empty source directories. Reconcile current model registry references by stable ID. Independently assess the exact changed Design package before relying on it.

### M2. Repair actual readers

Add a bounded project path map to existing model validation, preserving generic portable paths and safety checks. Update selector defaults, absent-old-path routing and example-to-owner pairing. Update fixture reader locations and relevant test expectations. First demonstrate rejection/selection failures for the new paths, then implement the mapping. Run model-boundary, selector and actual CLI model/record fixture tests. Unknown nested paths, existing invalid old paths and symlinks must not become accepted through aliases.

## Final review checkpoint

Independent review covers the complete directory migration, affected Design contracts, reader changes, tests and preservation evidence. Final whole-initiative Code Review and Verify remain required after the later validation implementation; this slice grants no whole-change readiness.

## Change-level verification

Compare all model requirement rows before/after; compare moved JSON/Mermaid payloads byte-for-byte; resolve moved Markdown links and changed current navigation; inspect that historical change records are unchanged. Run all twelve model checks and focused reader regressions. Review the ownership/selector interaction independently.

## Validation plan

- `python scripts/test-boundary-first-validation.py`: accepted paths, closed vocabulary, containment and model structure.
- `python scripts/test-select-validation.py`: selection and example-owner pairing.
- `node --test packages/rigorloop/test/record-store-model-examples.test.js packages/rigorloop/test/record-store-v3-contract.test.js packages/rigorloop/test/record-store-v3-reads.test.js packages/rigorloop/test/record-store-v3-mutations.test.js packages/rigorloop/test/record-store-workflow.test.js`: actual relocated fixture consumers.
- `python scripts/validate-boundary-first.py --check --path <each current model>` and `python scripts/validate-documentation-prose.py --mode enforce --path <each current model>`: current model integrity.
- `git diff --check`: whitespace integrity.

## Risks and recovery

Missed path consumers can omit proof or break navigation. Search actual source readers and validate their selected commands. Preserve a pre-move path/content snapshot for exact comparison and reversible restoration. Historical references deliberately retain original paths and identities; current navigation identifies the new owners.

## Dependencies

User-approved hierarchy and explicit directory optimization. Downstream executor work remains separately allocated.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- |
| 2026-09-12 | Mirror three main owners in directories; named sections remain valid children. | Makes ownership discoverable without empty child folders. | A directory per logical child adds files without additional contracts; retaining the flat layout hides composition. |

## Readiness

See the owning change record and exact independent review evidence. This plan records stable intent only.
