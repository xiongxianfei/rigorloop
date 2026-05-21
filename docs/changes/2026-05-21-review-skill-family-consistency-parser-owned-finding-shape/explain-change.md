# Explain Change

Change: `2026-05-21-review-skill-family-consistency-parser-owned-finding-shape`
Date: 2026-05-21

## Summary

This change makes `code-review`, `proposal-review`, and `spec-review` share the same parser-owned material-finding field shape through packaged `assets/material-finding.md` templates, while keeping review judgment, status vocabularies, recording rules, and handoff behavior in each `SKILL.md`.

It also adds deterministic validator coverage, preservation evidence, generated-output proof, token-cost evidence, cold-read evidence, and lifecycle review records so the change is structural and behavior-preserving rather than a hidden review-policy rewrite.

## Problem

The review-skill family repeated material-finding shape and result-output structure in prose. That made it possible for a reviewer to produce a human-readable finding that omitted the parser-owned `Finding ID:` field. The accepted proposal narrowed the fix to review-family field-shape assets and validator-backed proof, without adding severity-enum validation or build-time partials.

## Decision Trail

| Source | Decision |
| --- | --- |
| Proposal | Use `assets/material-finding.md` and per-skill `assets/review-result-skeleton.md` for `code-review`, `proposal-review`, and `spec-review`. |
| Spec | Requirements `RSF-R1` through `RSF-R45` define first-slice scope, parser-owned labels, asset boundaries, generated-output proof, token/cold-read proof, and follow-on triggers. |
| Spec review | `RSF-SR1` was accepted; invalid-fill proof was narrowed to parser-owned `Finding ID:` identity defects and severity-enum validation stayed out of scope. |
| Plan | M1 added validator foundation, M2 added `code-review` assets, M3 conformed `proposal-review`, M4 conformed `spec-review`, and M5 recorded generated-output/token/cold-read evidence. |
| M1 code review | `RSF-M1-CR1` was accepted; the non-enum severity non-validation proof now includes an actual `Severity:` field. |
| Architecture | No separate architecture package was required because the change stays within skill text/assets, deterministic validators, generated-output proof, and lifecycle evidence. |

## Diff Rationale By Area

| File or area | Change | Reason | Source | Evidence |
| --- | --- | --- | --- | --- |
| `skills/code-review/SKILL.md` | Added Resource map entries for `COPY assets/material-finding.md` and `COPY assets/review-result-skeleton.md`; shifted result/finding shape guidance to assets. | Make the parser-shaped finding block the copied starting point while preserving `code-review` rules and `clean-with-notes` semantics. | `RSF-R4` through `RSF-R11`, `RSF-R22` through `RSF-R26` | `m2-code-review-preservation.md`, `code-review-m2-r1.md` |
| `skills/code-review/assets/material-finding.md` | Added parser-owned material-finding template with required labels and placeholders. | Give reviewers a reusable field block whose labels match the review-artifact parser contract. | `RSF-R12` through `RSF-R18` | `python scripts/test-skill-validator.py` |
| `skills/code-review/assets/review-result-skeleton.md` | Added skill-specific result skeleton with `clean-with-notes | changes-requested | blocked | inconclusive`. | Preserve code-review status vocabulary and milestone fields without sharing a gate-review skeleton. | `RSF-R22` through `RSF-R26` | `m2-code-review-preservation.md` |
| `skills/proposal-review/SKILL.md` and assets | Conformed existing assets by adding literal `Finding ID:` confirmation and explicit gate-review status vocabulary. | Bring the existing asset-enabled skill under the review-family contract without changing proposal-review behavior. | `RSF-R8`, `RSF-R23`, `RSF-R43` | `m3-proposal-review-preservation.md`, `code-review-m3-r1.md` |
| `skills/spec-review/SKILL.md` and assets | Replaced `assets/review-finding.md` with `assets/material-finding.md`; preserved result status and eventual test-spec readiness. | Adopt the approved review-family asset name and remove stale finding-asset references. | `RSF-R1`, `RSF-R4`, `RSF-R23`, `RSF-R26` | `m4-spec-review-preservation.md`, `code-review-m4-r1.md` |
| `scripts/skill_validation.py` | Added deterministic review-family asset validation for inventory, metadata, placeholders, review-class boundaries, resource maps, parser labels, byte-identical field blocks, and generated-output support. | Make drift and policy leakage detectable instead of relying on reviewer discipline. | `RSF-R5` through `RSF-R18`, `RSF-R38`, `RSF-R39` | `python scripts/test-skill-validator.py` |
| `scripts/test-skill-validator.py` | Added focused positive and negative tests for review-family assets and per-skill status preservation. | Prove first-slice assets conform and deferred/shared-skeleton/out-of-scope forms fail. | Test spec `T2`, `T3`, `T5` through `T7` | `pass_159_tests_after_m4` in `change.yaml` |
| `scripts/test-review-artifact-validator.py` | Added parser-owned finding identity tests and non-enum severity non-validation proof. | Keep validation aligned with the current parser contract and avoid silently adding severity-enum behavior. | `RSF-R19` through `RSF-R21`, `AC-RSF-009`, `AC-RSF-010` | `python scripts/test-review-artifact-validator.py` |
| `docs/changes/.../*preservation.md` | Added per-skill preservation and representative parity evidence for M2, M3, and M4. | Prove extraction did not change review dimensions, status values, recording rules, stop conditions, or handoff behavior. | `RSF-R27` through `RSF-R30` | Clean M2-M4 code reviews |
| `docs/changes/.../m5-generated-token-cold-read-evidence.md` | Recorded generated mirror proof, temporary adapter archive proof, no-hand-edit proof, token-cost evidence, cold-read sample, scope boundaries, and follow-on triggers. | Close generated-output, token, cold-read, and deferred-trigger acceptance criteria. | `RSF-R31` through `RSF-R37`, `RSF-R44`, `RSF-R45` | `code-review-m5-r1.md` |
| Lifecycle artifacts | Added proposal, spec, test spec, plan, review records, review-resolution, and change metadata updates. | Keep the workflow state and formal review evidence durable and synchronized. | `RSF-R40`, `AC-RSF-019`, repository workflow | `review-log.md`, `review-resolution.md`, `change.yaml` |

## Tests Added Or Changed

| Test area | What it proves |
| --- | --- |
| `test_review_family_asset_resource_map_requires_finding_id_confirmation` | Material-finding resource maps must instruct reviewers to confirm the literal `Finding ID:` line before linking. |
| `test_code_review_family_assets_are_installed_and_preserve_status_vocabulary` | `code-review` has the required assets and keeps `clean-with-notes` status vocabulary. |
| `test_proposal_review_family_assets_preserve_gate_status_vocabulary` | `proposal-review` keeps `approved | changes-requested | blocked | inconclusive` and shares the parser-owned field block. |
| `test_spec_review_family_assets_use_material_finding_and_preserve_readiness` | `spec-review` uses `material-finding.md`, removes stale `review-finding.md` references, and keeps eventual test-spec readiness. |
| `test_review_family_material_finding_requires_parser_owned_labels` | Material-finding assets must contain exactly the parser-owned labels. |
| `test_review_family_material_finding_field_block_must_match_across_skills` | The parser-owned field block stays byte-identical across first-slice review skills. |
| `test_material_finding_identity_label_is_parser_owned` | Review-artifact structure validation owns `Finding ID:` identity shape. |
| `test_non_enum_severity_is_not_structure_validated` | This slice does not add severity-enum validation. |

These tests are appropriate because the change is mostly contract and packaging behavior: deterministic static validation and review-artifact parser fixtures are the lowest-cost way to prevent drift.

## Validation Evidence Before Final Verify

Key local validation already run and recorded in `change.yaml`:

```bash
python scripts/test-skill-validator.py
python scripts/test-review-artifact-validator.py
python scripts/validate-skills.py
python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape
python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape
python scripts/build-skills.py --check
python scripts/build-adapters.py --version v0.1.5 --output-dir /tmp/tmp.cG1mr7T4PH
python scripts/validate-adapters.py --root /tmp/tmp.cG1mr7T4PH --version v0.1.5
python scripts/measure-skill-tokens.py
python scripts/validate-change-metadata.py docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape/change.yaml
python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...
git diff --check --
```

Hosted CI and final verify are not claimed here; they belong to downstream verification and PR stages.

## Review Resolution Summary

`review-resolution.md` is closed with two accepted findings:

| Finding | Disposition | Summary |
| --- | --- | --- |
| `RSF-SR1` | accepted | Revised the spec so invalid-fill examples use parser-owned `Finding ID:` identity defects, not non-enum severity values. |
| `RSF-M1-CR1` | accepted | Made the non-enum severity non-validation test non-vacuous by inserting a real `Severity:` field before validation. |

All implementation milestones M1 through M5 received clean code-review reruns or first-pass clean reviews.

## Alternatives Rejected

| Alternative | Reason rejected |
| --- | --- |
| Add severity-enum validation | Out of scope and would expand the parser contract. |
| Use one shared result skeleton | Would risk homogenizing `code-review` `clean-with-notes` semantics with gate-review `approved` semantics. |
| Add build-time partials | A separate mechanism with separate risk; deferred until another shared review concept needs single-sourcing or checked copies drift. |
| Add packaged `references/` or `scripts/` | The accepted slice is assets-only and field-shape-only for review skills. |
| Update `plan-review` or `architecture-review` now | First slice is limited to `code-review`, `proposal-review`, and `spec-review`; other `*-review` skills are follow-on work. |
| Hand-edit generated adapter output | Generated public adapter output is derived release output; proof uses temporary generated archives instead. |

## Scope Control

The change preserves:

- review dimensions and judgment;
- severity values and severity-enum behavior;
- review-status values and per-skill status semantics;
- recording and isolation rules;
- lifecycle boundaries and handoff behavior;
- adapter install roots, lockfile semantics, CLI behavior, and historical adapter archives.

Generated output was checked from canonical sources, not committed as hand-edited adapter output.

## Risks And Follow-Ups

Remaining risks are bounded:

- Total packaged footprint increased because assets are now explicit; this is recorded separately from common-path `SKILL.md` size and is acceptable under the approved priority order.
- The three `material-finding.md` copies remain duplicated until build-time partials exist; parser-owned field-block checks make drift detectable.
- Referential-integrity validation remains deferred. If the cross-file-reference failure recurs once after this slice ships, or the next review-artifact learn session cites it, a validator check should be proposed.

Current active handoff: `verify`. The plan is not PR-ready until final verification and PR handoff complete.
