# Spec-Review Skill Simplification Execution Plan

## Purpose / big picture

Simplify the published `spec-review` package without weakening formal review judgment, durable recording, boundary-first behavior, or lifecycle authority. The work freezes semantic and literal ownership before moving prose, separates isolated review from governed settlement procedure, and then proves loaded-profile reduction and complete package parity.

## Current Handoff Summary

- Owning change record: `docs/changes/2026-08-12-spec-review-skill-simplification/change.yaml`

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: `docs/proposals/2026-08-12-spec-review-skill-simplification.md`
- Spec: `specs/spec-review-skill-simplification.md`
- Architecture: not required; recorded in `docs/changes/2026-08-12-spec-review-skill-simplification/architecture-assessment.md`
- Test spec: pending at `specs/spec-review-skill-simplification.test.md`

## Context and orientation

`skills/spec-review/` is the only authored package source. The current package contains `SKILL.md`, two projected boundary references, and two structural assets. This change adds `references/governed-spec-review-settlement.md`, keeps universal review judgment and executable recording inline, and moves only exact same-change settlement and workflow-managed automation procedure.

`specs/skill-contract.md`, `specs/spec-family-assets-progressive-disclosure.md`, and `specs/formal-review-recording.md` are directly coupled contract surfaces. `scripts/skill_validation.py`, `scripts/test-skill-validator.py`, build validation, boundary projection validation, and adapter distribution checks are existing permanent proof owners. Rule, literal, scenario, and measurement records remain change-local evidence.

## Non-goals

- Change review verdicts, severity, material findings, recording artifacts, lifecycle state meaning, boundary activation, status, readiness, claims, or handoff semantics.
- Change workflow order, `change.yaml` schema, package classes, adapter roots, publication flow, or runtime architecture.
- Add another result asset, generic review engine, target-agent execution, transcript grading, tokenizer dependency, or permanent simplicity validator.
- Hand-edit projected boundary references, generated adapters, archives, or installed copies.

## Requirements covered

| Requirement and boundary scope | Owning milestone or evidence |
| --- | --- |
| R33-R40, R42; BND-RECOVERY-001, BND-COMPAT-001, BND-ENV-001; INT-005 | M1 rule/literal inventories, duplicate clusters, scenarios, and baseline measurement |
| R1-R32, R42, R45; BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001; INT-001-INT-004 | M2 contract amendment, inline recording, governed reference, assets, and focused validation |
| R26-R28, R32-R44; BND-COMPOSE-001, BND-RECOVERY-001, BND-COMPAT-001, BND-ENV-001; INT-004-INT-006 | M3 measurement, semantic preservation, boundary identity, and package-chain proof |
| R43 | Completed `architecture-not-required` assessment before this plan |

## Milestones

### M1. Freeze spec-review rule and literal ownership

- Milestone state: planned
- Goal: Account for every behaviorally significant rule, duplicate cluster, compatibility-sensitive literal, and required static scenario before changing canonical skill prose.
- Requirements: R33-R40, R42; BND-RECOVERY-001; BND-COMPAT-001; BND-ENV-001; INT-005.
- Files/components likely touched:
  - `docs/changes/2026-08-12-spec-review-skill-simplification/spec-review-rule-disposition.yaml`
  - `docs/changes/2026-08-12-spec-review-skill-simplification/spec-review-literal-compatibility.yaml`
  - `docs/changes/2026-08-12-spec-review-skill-simplification/fixtures/`
  - `docs/changes/2026-08-12-spec-review-skill-simplification/evidence/profile-size-baseline.md`
- Dependencies:
  - approved spec, clean spec review, and recorded architecture assessment
  - complete current `skills/spec-review/` package and exact-string consumers
- Tests to add/update:
  - static scenarios for formal routing, isolated clean/material recording, governed manual/automated settlement, boundary variants, missing resources, blocked placement, stale authority, retries, asset groups, and invalid classifications
  - unknown semantic disposition and literal classification fixtures that prove fail-closed ordering
- Implementation steps:
  - inventory rules with stable IDs, sources, behavior, governing requirements, profiles, disposition, destination, and preservation proof
  - inventory exact-string dependencies separately and classify normative, parser/package, incidental-test, or obsolete treatment
  - record duplicate clusters and one intended loaded owner for each
  - serialize deterministic scenario fixtures with required and forbidden outcomes
  - record LF-normalized baseline words, bytes, exact resources, all four profiles, manual/automated governed evaluations, and total package
- Validation commands:
  - run the exact `M1 change-local evidence proof` command in the Validation plan
  - `python scripts/validate-change-metadata.py docs/changes/2026-08-12-spec-review-skill-simplification/change.yaml`
  - independently inspect both ledgers against the complete current skill and literal consumers
- Expected observable result: every current rule, literal, and duplicate has one closed treatment; required scenarios exist; unknown values fail first; canonical skill prose is unchanged.
- Commit message: `M1: freeze spec-review rule and literal ownership`
- Milestone closeout:
  - validation and independent code review complete before M2
- Risks:
  - similar recording passages may encode distinct safety behavior
  - an incidental assertion may be mistaken for a normative literal
- Rollback/recovery:
  - revert M1 evidence without touching canonical skill content

### M2. Separate isolated review from governed settlement

- Milestone state: planned
- Goal: Create a shorter self-sufficient isolated formal-review path and move only governed settlement and automation procedure into one exact reference.
- Requirements: R1-R32, R42, R45; BND-INPUT-001; BND-STATE-001; BND-AUTH-001; BND-COMPOSE-001; BND-TEMPORAL-001; BND-RECOVERY-001; INT-001-INT-004.
- Files/components likely touched:
  - `skills/spec-review/SKILL.md`
  - `skills/spec-review/references/governed-spec-review-settlement.md`
  - `skills/spec-review/assets/review-result-skeleton.md`
  - `skills/spec-review/assets/material-finding.md` only if structural parity requires a deliberate compatible update
  - `specs/skill-contract.md`
  - `specs/spec-family-assets-progressive-disclosure.md`
  - existing skill-contract and spec-family test specs or validators directly coupled to changed literals
  - `scripts/test-skill-validator.py`
- Dependencies:
  - M1 evidence and code review are closed
- Tests to add/update:
  - exact formal routing and two authority axes
  - four exact resource profiles and required/forbidden loads
  - complete isolated recording without the governed reference
  - recording-only roots and forbidden governed mutations
  - governed settlement after recording, automated authority, stale identity, retries, and missing-reference preservation
  - unchanged checked boundary activation, load order, and grandfathering
  - one formal core, required recording group, conditional groups, omitted inapplicable groups, and no placeholders
- Implementation steps:
  - add failing focused assertions to existing validation before moving prose
  - amend only directly coupled `SFA-R6` and package-contract wording needed to distinguish universal obligations from conditional mechanics
  - rewrite `SKILL.md` from the ledger, retaining compact executable recording and every universal obligation
  - create the governed reference with manual and automated branches and no universal-policy duplication
  - update the existing result asset structure without adding policy or another asset
  - migrate parser/package literals atomically and update incidental tests instead of preserving accidental prose
- Validation commands:
  - `python scripts/validate-skills.py skills/spec-review/SKILL.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-build-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/validate-boundary-first.py --check --path specs/spec-review-skill-simplification.md`
- Expected observable result: isolated formal review is executable from a shorter common path; governed procedure loads only with exact authority; recording, boundary behavior, assets, statuses, claims, and handoff remain compatible.
- Commit message: `M2: simplify spec-review package paths`
- Milestone closeout:
  - focused validation and independent code review complete before M3
- Risks:
  - concise recording could omit collision, retry, or blocked-result behavior
  - loading the governed reference could be mistaken for settlement authority
  - changing an exact heading could break a real parser contract
- Rollback/recovery:
  - restore the prior complete canonical package and coupled consumers together, then regenerate derived packages

### M3. Prove isolated reduction and package parity

- Milestone state: planned
- Goal: Prove profile-specific reduction, complete semantic preservation, and canonical-through-installed resource integrity.
- Requirements: R26-R28, R32-R44; BND-COMPOSE-001; BND-RECOVERY-001; BND-COMPAT-001; BND-ENV-001; INT-004-INT-006.
- Files/components likely touched:
  - existing adapter-distribution tests only if focused `spec-review` coverage is absent
  - `docs/changes/2026-08-12-spec-review-skill-simplification/evidence/simplification-measurements.md`
  - `docs/changes/2026-08-12-spec-review-skill-simplification/evidence/semantic-preservation-review.md`
  - `docs/changes/2026-08-12-spec-review-skill-simplification/evidence/m3-package-proof.md`
- Dependencies:
  - M2 package refactor and code review are closed
- Tests to add/update:
  - canonical, generated, archived, and temporary installed targets contain the governed and existing boundary references at required paths and bytes
  - missing, escaped, transformed, stale, or mixed resources fail existing package proof
  - all four assemblies count each normalized unique resource once
  - no acceptance command invokes or grades a target agent
- Implementation steps:
  - extend only existing package proof when direct `spec-review` selection is missing
  - generate supported package forms in temporary directories and inspect exact resources
  - report before/after main file, each resource, all profiles, manual/automated governed evaluations, total package, duplicate clusters, inline templates, and mapped-resource counts
  - require lower `SR1-isolated-formal` words and bytes and justify every governed or total-package increase
  - independently review the final package against both ledgers and R42
- Validation commands:
  - `python scripts/test-adapter-distribution.py`
  - temporary adapter build followed by `python scripts/validate-adapters.py --clean-install-smoke --skill spec-review`
  - `python scripts/validate-skills.py skills/spec-review/SKILL.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-boundary-first.py --check --path specs/spec-review-skill-simplification.md`
- Expected observable result: isolated profiles shrink, governed and total-package changes are honest and justified, semantics remain complete, and every supported package contains byte-consistent resources without target-runtime execution.
- Commit message: `M3: prove spec-review simplification`
- Milestone closeout:
  - package proof, independent code review, and required resolution complete before final holistic review
- Risks:
  - generic adapter tests may pass without selecting `spec-review`
  - main-file reduction may hide governed-profile or total-package growth
  - partial packaging may mix old and new ownership
- Rollback/recovery:
  - restore the prior complete package, regenerate every derived target, and discard temporary package trees

## Validation plan

### M1 change-local evidence proof

The ledgers and scenarios use JSON serialization, which is valid YAML. This standard-library command rejects unknown values before destination consistency and validates required scenario identity.

```bash
python -c 'import json; from pathlib import Path; root=Path("docs/changes/2026-08-12-spec-review-skill-simplification"); rules=json.loads((root/"spec-review-rule-disposition.yaml").read_text())["rules"]; literals=json.loads((root/"spec-review-literal-compatibility.yaml").read_text())["literals"]; scenarios=json.loads((root/"fixtures/scenario-contracts.yaml").read_text())["scenarios"]; bad_rule=json.loads((root/"fixtures/invalid-rule-disposition.yaml").read_text()); bad_literal=json.loads((root/"fixtures/invalid-literal-classification.yaml").read_text()); rd={"retained-inline","retained-governed-reference","retained-boundary-reference","asset-owned","removed-duplicate","removed-obsolete-with-approved-contract-change"}; lc={"normative-contract","parser-or-package-contract","test-only-incidental","obsolete"}; rf={"rule_id","source_locations","behavior","governing_requirements","applicable_profiles","disposition","destination","preservation_proof"}; lf={"literal_id","literal","source_location","consumers","classification","required_semantics","disposition","replacement"}; vr=lambda row: ["unknown-disposition"] if row.get("disposition") not in rd else (["missing-required-fields"] if not rf <= row.keys() else (["empty-required-fields"] if not all(row[field] for field in rf) else [])); vl=lambda row: ["unknown-classification"] if row.get("classification") not in lc else (["missing-required-fields"] if not lf <= row.keys() else (["empty-required-fields"] if not all(row[field] for field in lf) else [])); expected={"outside-skill-feedback","isolated-clean","isolated-material","isolated-recording-root","blocked-recording","governed-manual","governed-automated","stale-authorization","missing-governed-reference","isolated-boundary","governed-boundary","late-boundary-activation","grandfathered-nonsubstantive","substantive-ambiguous","asset-groups","retry-conflict","invalid-axis"}; assert rules and literals; assert all(vr(row) == [] for row in rules); assert all(vl(row) == [] for row in literals); assert vr(bad_rule)[0] == "unknown-disposition"; assert vl(bad_literal)[0] == "unknown-classification"; assert len({row["rule_id"] for row in rules}) == len(rules); assert len({row["literal_id"] for row in literals}) == len(literals); assert {row["scenario"] for row in scenarios} == expected; assert all(row.get("required") and row.get("forbidden") for row in scenarios); print(f"rules={len(rules)} literals={len(literals)} scenarios={len(scenarios)} unknown_values=rejected-first")'
```

- `python scripts/validate-skills.py skills/spec-review/SKILL.md`: normalized structure, resource-map syntax, containment, placeholders, and narrow claims.
- `python scripts/test-skill-validator.py`: focused skill-contract and regression proof.
- `python scripts/test-build-skills.py` and `python scripts/build-skills.py --check`: generated inventory and resource parity.
- `python scripts/test-adapter-distribution.py`: adapter generation, archive, and installed-resource regressions.
- Temporary adapter generation plus clean-install validation for `spec-review`: direct all-target package proof.
- `python scripts/validate-boundary-first.py --check --path specs/spec-review-skill-simplification.md`: boundary record and later proof-map coverage.
- Review artifact, change metadata, lifecycle, Markdown readability, and diff checks: change-local governance proof.
- Independent semantic review: invocation classification, universal recording, authority, profiles, boundary activation, assets, failures, statuses, claims, handoff, and literal treatment.

## Risks and recovery

- Risk: conditional extraction hides universal recording or claim behavior.
  - Recovery: rule ledger, isolated fixtures, focused assertions, and semantic review block the move; restore the prior package atomically.
- Risk: governed procedure gains authority merely by loading.
  - Recovery: classify authority first and prove forbidden isolated and mismatched writes.
- Risk: incidental literal tests become policy owners.
  - Recovery: keep literal classification separate and migrate only real contracts atomically.
- Risk: relocation is reported as deletion.
  - Recovery: report each profile and total package in words and bytes, with semantic preservation taking precedence.
- Risk: one package target omits the new reference.
  - Recovery: block acceptance on selected archive and installed-tree parity, then regenerate from the last complete canonical revision.

## Dependencies

- Accepted proposal, approved spec, clean formal reviews, closed prior findings, and recorded `architecture-not-required` assessment.
- Existing formal-review recording, spec-family asset, boundary projection, and published-skill package contracts.
- Existing skill validation, build, adapter generation, archive, and clean-install proof owners.
- Approved test specification and test-spec review before implementation.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-12 | Use three implementation milestones: preservation evidence, package refactor, and profile/package proof. | Each has an independently reviewable failure and rollback boundary. | One large prose-and-package rewrite. |
| 2026-08-12 | Keep semantic and literal inventories separate and complete before prose movement. | Behavioral ownership and exact-string compatibility are different contracts. | One combined ledger or preserving every asserted phrase. |
| 2026-08-12 | Keep universal recording in M2 common-path work and governed settlement in one reference. | Direct review must record safely without loading mutation procedure. | Always-loaded recording reference or fragmented recording resources. |
| 2026-08-12 | Extend only existing validators for durable package proof. | The approved contract excludes new permanent simplicity machinery. | New validator family, tokenizer, or runtime journey gate. |
| 2026-08-12 | Measure all four profiles and total package words and bytes. | Main-file size alone can hide relocation and governed-profile cost. | A normative percentage threshold. |

## Readiness

- See the owning change record for current workflow state.
- Readiness is not Done; plan review, test-spec authoring and review, implementation/code-review milestones, explanation, verification, and PR handoff remain.
