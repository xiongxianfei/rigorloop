# Retire feature-format support

## Purpose / big picture

Remove the feature/proof operational surface and its exclusive maintenance while preserving current model validation, compact boundary reasoning, customer source authority and historical change-range compatibility. Deliver the narrowed contract coherently across skills, generated resources, validator dispatch and CLI discovery.

## Current Handoff Summary

- Owning change record: [feature-format retirement](../changes/2026-09-17-retire-feature-format-support/change.json).

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: [bounded withdrawal](../proposals/2026-09-17-retire-feature-format-support.md).
- Spec: current [Design](../design/skill/authoring/design.md), [Validation](../design/engineering/validation.md), [CLI](../design/cli/cli.md) and [Packaging](../design/engineering/packaging.md), with their reconciled System/Skill/Authoring/Workflow consumers; no separate feature spec.
- Architecture: the same owning Designs, including DES-DEC-08 and their existing responsibility/supporting views.
- Prior-contract test spec: none. Current [System rules](../design/test-design/rules.md), Skill/Authoring catalogs and Validation's local coverage govern retained proof.
- Exact upstream Design package: `feature-retirement-design-review-r2`; preserve its member map and the resolved `authoring-retirement-case-accounting` finding.

## Context and orientation

Baseline `5822e0e6` includes merged PR #199. Work takes place on `codex/retire-spec-support`; the original staged retirement workspace is preserved. `boundary_first_validation.py` contains both retired feature/proof parsing and current model helpers, so whole-file deletion is incorrect. `test_design_validation.py` dispatches public requested documents. `validation_selection.py` composes actual selected commands and retains historical deletion routing. `boundary_first_reference.py` projects a closed resource manifest consumed by package generation. `workflow-context.js` derives accepted location kinds from its bundled defaults.

The direct boundary aggregate has separate structural, path, handoff, model, command and catalog groups. Structural/handoff feature grammar is retired; path-group privacy observations must survive on current-model fixtures. Six static feature/proof fixture files and their builders are exclusive candidates, subject to actual consumer inspection. Shared projection/packaging checks remain meaningful with the smaller resource set. Synthetic old-looking filenames are not automatically removal targets.

## Non-goals

- Retiring Skill archive mappings, old examples-prefix routing, relocation/flat aliases or other supported Git ranges.
- Changing record storage/versions, installation permissions, other artifact location kinds, publication/version policy or historical assessments.
- Automatic customer-file migration, a test framework/runner replacement, a new compatibility registry or a quota for test removal.

## Requirements covered

| Requirement basis | Allocation |
| --- | --- |
| DES-SR-14/15/18/23/24/25/26, AUTH-SR-01/02/05, SYS-SR-05/13 | M1, TG-METHOD and TG-INTEGRATION: supported output, authority preservation and coherent consumers. |
| VAL-SR-28/35, TEST-SR-04/05/07/08/09/10/20/22 | M1, TG-VALIDATION: no-read rejection, retained models/catalogs and justified test disposition. |
| CLI-SR-32 and retained CLI-SR-01/10/30 | M1, TG-CONTEXT: spec kind withdrawal with factual discovery and preservation. |
| DIST-SR-18/24 and Skill resource integrity | M1, TG-RESOURCES and TG-INTEGRATION: closed compact-core inventory through actual archives/install. |

## Milestones

### M1. Withdraw the feature/proof surface coherently

- Milestone kind: implementation.
- Engineering purpose: retire one cross-owner supported surface in a single reviewable commit; no independently shipped interval advertises unavailable methods or validates unsupported formats.
- Requirements: all rows above, within the approved feature-retirement scope.
- Architecture responsibility: existing Authoring, Validation, CLI discovery and Packaging boundaries; no new component.
- Dependencies: current approved Proposal and exact Design Review package, followed by independent approval of this plan.
- Implementation scope: reconcile published skills and transitive READ paths; simplify compact reasoning; remove feature/proof resources, parsers, adoption handoff, CLI spec location/config kind, exclusive tests and fixtures; preserve shared current behavior and reconcile test discovery/catalog references.
- Files/components likely touched: `skills/{design,design-review,delivery-review,route,plan,implement,code-review,verify}` and relevant consumers; `templates/shared/boundary-first-*`; boundary resource manifest/projection helpers; validator/document dispatch/selection; package workflow-context and tests; boundary, Skill and Packaging tests; affected model coverage and release communication.
- Required verification: TG-VALIDATION, TG-CONTEXT, TG-RESOURCES and TG-METHOD, plus integrated TG-INTEGRATION before final handoff.
- Evidence expectations: exact before/after test discovery, group-level removal/retained-protection disposition, actual negative-before/positive-after results, generated resource/archive observations and independent guidance assessment with explicit limits.
- Implementation steps: first establish expected unsupported-input and CLI config failures against the old behavior. Separate current model/privacy protection from retired fixtures. Then remove exclusive behavior/resources and reconcile consumers atomically. Generate supported projections through the existing tool, rerun focused proof, audit remaining references and run the required selected suite.
- Validation commands: use the focused and integrated commands below. A full selected local run may supply the same native checks; do not rerun unchanged checks solely to duplicate evidence.
- Expected observable result: old-format operations reject without source reads/writes; current models/catalogs and other context locations work; clean supported packages contain only the current compact resource population with no dangling method references.
- Completion criteria: every changed consumer and deletion has a justified disposition, all allocated proof passes, supported native discovery remains reachable, and evidence accurately separates structural checks from semantic guidance assessment.
- Required evidence: current exact subjects, commands, exits, result counts, baseline comparison, deletion scope and limitations in the owning evidence/material-decision records.
- Review handoff: independent M1 Code Review of the complete implementation and composed boundaries, including remaining negative protection and all deleted method/fixture families.
- Optional commit boundary: `M1: Retire feature-format operations and exclusive tests`.
- Risks: shared helper deletion could weaken models; an unprojected method could break packages; selector omission could hide unsupported input; customer configuration could fail unexpectedly without explanation.
- Rollback/recovery: restore the matching authored guidance, manifest/projections, validator/CLI and test slice from baseline or its reviewed predecessor together. Preserve original customer/source/record bytes and the unrelated original workspace. Do not restore only a retired parser or retarget old assessments.

## Final review checkpoint

- Kind: lifecycle-closeout.
- Dependency: all in-scope implementation milestones and required corrections complete.
- Assessment: fresh independent final whole-change Code Review of the complete delivered engineering change and cross-owner interactions.
- Evidence: exact final subjects, independent reviewer basis, judgment and reporter-owned concern dispositions.
- Successor: distinct final Verify; corrections return to their owner and require affected reassessment.

This checkpoint applies even though there is one implementation milestone. Passing tests and milestone review do not waive it.

## Change-level verification

### TG-VALIDATION. Supported documents and rejected old formats

Public command tests cover present, missing and symlinked `specs/` input; malformed or marked content must not be opened to decide rejection. Observe `BFR-UNSUPPORTED-FORMAT`, nonzero status, empty review-required observations and preserved bytes. A direct no-read guard distinguishes rejection before content access from rejection after parsing. Current model tests retain marker/closed-dimension precedence, malformed tables/references, safe paths, privacy-bounded diagnostics and read-only checks. Default validation still checks the complete declared model/example/catalog population. Exercise actual local/range deletion and mixed valid/unsupported selection through the selector/executor, preserving historical routing instead of claiming a fake successful retired-format check.

### TG-CONTEXT. Configuration withdrawal without other discovery changes

The public CLI omits `spec` from defaults and rejects a config override for it with the existing invalid-input result/exit before candidate discovery. Preserve config, source and record bytes. A retained-override control and existing unknown-kind tests protect other location/configuration behavior; current-record discovery and schema-version domains remain unchanged.

### TG-RESOURCES. Reduced inventory with unchanged integrity

Inspect independent expected compact-core resource/consumer sets. Rework manifest negative fixtures against the surviving resource so unknown resource/consumer values still reject before consistency, missing/escaped sources and destinations reject, and projection drift remains observable. Remove only retired-content assertions. Verify actual generated archive inventory and clean packed-CLI install of both supported targets through the existing Packaging suite. Keep unrelated synthetic resource fixtures when they protect generic copying or containment.

### TG-METHOD. Unsupported output and authorized source interpretation

An independent Code Reviewer applies AUTH-SH-005 to the exact changed guidance: compare a request to amend customer feature/proof documents, the same request with an old template, and separately authorized scoped adoption into the living Design. Expected proposed decisions are unsupported/no project writes for the first two and meaning/identity-preserving authorized adoption for the control, followed by model-owned intent and Plan allocation. Inspect all triggered methods in the generated/installed package. Record the reviewed subjects, variants, expected/actual proposed decisions and limitation: artifact/guidance assessment does not certify universal agent compliance or execute a semantic test runner. Refresh this assessment if relevant guidance changes.

The same independent reviewer separately assesses the rewritten compact-core against Design’s retained method obligation: the four-question scan identifies outcome-changing inputs, state, alternate/composed paths and failure/recovery/environment conditions; all eight risk dimensions remain usable; interactions follow actual combined hazards rather than a Cartesian inventory; missing behavior returns to Design and missing execution allocation returns to Plan. Use a small living-model packet with a stale authority check followed by a retry through a helper path, and compare altered method excerpts omitting identity/authority, inventing mandatory BND/INT/PRF records, requiring all dimension combinations or sending a missing behavioral decision to implementation. Inspect the canonical method and its actual generated/installed availability. Record whether each counterexample is exposed and each required reasoning responsibility survives. This is semantic artifact assessment, not phrase matching, a new case quota or a claim of universal agent compliance. Relevant canonical/projection changes invalidate this assessment and require fresh review.

### TG-INTEGRATION. Complete supported change

Run selected local CI over the complete changed set, using real package/discovery boundaries above; no extra broad smoke unless the selector declares its authoritative trigger. Reconcile deletion/recreation paths and stale consumers, including copied fixture repositories and command fingerprints. At final Verify, use exact committed PR selection and current-record snapshot checks when preparing a PR; affirmatively reuse unchanged execution evidence only under current assessment policy. Hosted CI is separate from local success. Release communication describes the breaking support change without publication or version selection.

## Validation plan

```bash
python tests/engineering/validation/test-boundary-first-validation.py
python tests/engineering/validation/test-boundary-first-reference.py
python tests/engineering/validation/test-select-validation.py
node --test packages/rigorloop/test/workflow-context.test.js
python tests/skill/test-skill-validator.py
python tests/engineering/packaging/test-adapter-distribution.py
python scripts/project-boundary-first-reference.py --check
python scripts/validate-boundary-first.py --check
bash scripts/ci.sh --mode local
```

Run new targeted methods first for failure reproduction, then affected groups. The selected local suite supplies all required selected checks, including unrelated retained protections selected by shared code changes. Record actual commands and failures; no invented or silently skipped checks. TG-METHOD requires the bounded independent assessment above because deterministic text/resource checks cannot establish its semantic conclusion.

## Risks and recovery

The source module and projection system contain shared safety behavior; preserve independently justified oracles before deleting old fixtures. A stale consumer or unknown protective value blocks that deletion until its owner resolves it. Unsupported configuration must fail visibly rather than silently dropping an override. All removed tracked material is recoverable from `5822e0e6`; no uncommitted source in the original workspace is a removal target.

## Dependencies

Design Review and Delivery Review precede implementation. All M1 surfaces are coupled at one support boundary; full local validation and milestone review precede the final whole-change review and distinct Verify. External publication is outside this plan. Historical-path retirement stays with the original initiative and is not a hidden M1 dependency.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-09-17 | One coupled implementation milestone, with distinct focused proof groups and integrated assessment. | Publishing guidance, validator or CLI withdrawal alone would leave contradictory supported operations. | Separate shipped format/guidance retirement, retained dormant parsers and a test-count reduction target. |
| 2026-09-17 | Remove exclusive grammar cases; preserve shared safety on current model/resource fixtures. | Retired positive and negative grammar is no longer an obligation, but containment/privacy/integrity still is. | Keeping every historical test forever or deleting shared protection by filename. |

## Readiness

See the owning change record for current workflow state. Delivery approval permits only its exact allocation; implementation, independent M1 review, final whole-change review and successful Verify remain separate required gates.
