# Plan-Review Skill Simplification Execution Plan

## Purpose / big picture

Simplify the published `plan-review` package without weakening plan judgment, formal recording, reviewed-plan initialization and settlement, boundary-first behavior, or lifecycle authority. The work freezes semantic and literal ownership before moving prose, separates portable review from governed transaction procedure, and proves deterministic retry behavior, loaded-profile reduction, and complete package parity.

## Current Handoff Summary

- Owning change record: `docs/changes/2026-08-13-plan-review-skill-simplification/change.yaml`

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: `docs/proposals/2026-08-13-plan-review-skill-simplification.md`
- Spec: `specs/plan-review-skill-simplification.md`
- Architecture: not required; recorded in `docs/changes/2026-08-13-plan-review-skill-simplification/architecture-assessment.md`
- Test spec: pending at `specs/plan-review-skill-simplification.test.md`

## Context and orientation

`skills/plan-review/` is the only authored package source. The current package contains `SKILL.md` and the shared boundary reference. This change adds `references/governed-plan-review-settlement.md`, `assets/review-result-skeleton.md`, and `assets/material-finding.md`; keeps portable plan-quality judgment and executable recording inline; and moves only exact governed candidate validation, operation-state handling, settlement, interruption recovery, and workflow-managed procedure.

`specs/skill-contract.md`, `specs/formal-review-recording.md`, `specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md`, `ADR-20260813-reviewed-plan-initialization-and-settlement.md`, and existing review-family assets and validators are directly coupled surfaces. Existing skill, build, boundary, adapter, change-metadata, lifecycle, and review-artifact checks remain permanent proof owners. Rule, literal, scenario, and profile-measurement records remain change-local evidence.

## Non-goals

- Change plan-quality criteria, semantic review statuses, transaction values, lifecycle stages, `planned_work` ownership, workflow routing, or implementation authorization.
- Add a content hash, `content_identity` field, package class, transformation, validator family, generic review engine, runtime, state store, scheduler, or selector.
- Optimize adjacent skills or redesign the reviewed-plan transaction.
- Execute a target-agent runtime, grade transcripts, add prompt journeys, or add a tokenizer dependency.
- Hand-edit generated adapters, archives, installed copies, or the projected boundary reference.

## Requirements covered

| Requirement and boundary scope | Owning milestone or evidence |
| --- | --- |
| R48-R53; BND-RECOVERY-001, BND-COMPAT-001; INT-006 | M1 rule/literal inventories, duplicate clusters, scenarios, and baseline measurements |
| R1-R47; BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001; INT-001-INT-005 | M2 package, transaction, assets, contract, and focused validation |
| R40, R47-R55; BND-COMPOSE-001, BND-RECOVERY-001, BND-COMPAT-001, BND-ENV-001; INT-005-INT-007 | M3 semantic, profile, boundary, and package-chain proof |
| R55 | Completed `architecture-not-required` assessment before this plan |

## Milestones

### M1. Freeze plan-review rule and literal ownership

- Milestone kind: implementation
- Goal: Account for every behaviorally significant rule, duplicate cluster, exact literal dependency, and required lifecycle scenario before changing canonical skill prose.
- Requirements: R48, R49, R50, R51, R52, R53.
- Architecture decisions: `ADR-20260623-published-skill-resource-integrity`, `ADR-20260813-reviewed-plan-initialization-and-settlement`.
- Files/components likely touched:
  - `docs/changes/2026-08-13-plan-review-skill-simplification/plan-review-rule-disposition.yaml`
  - `docs/changes/2026-08-13-plan-review-skill-simplification/plan-review-literal-compatibility.yaml`
  - `docs/changes/2026-08-13-plan-review-skill-simplification/fixtures/`
  - `docs/changes/2026-08-13-plan-review-skill-simplification/evidence/profile-size-baseline.md`
- Dependencies:
  - approved spec, clean spec review, and `architecture-not-required` assessment
  - complete current `skills/plan-review/` package and exact-string consumers
- Tests and proof:
  - static scenarios for portable and governed review, candidate validation, each operation and non-clean result, pending initialization, matching and active retry, stale/duplicate/conflicting state, recording failure, missing resource, boundary variants, asset groups, and forbidden writes
  - unknown semantic disposition and literal classification fixtures that prove fail-closed ordering
- Implementation steps:
  - inventory rules with stable IDs, sources, behavior, governing requirements, profiles, one disposition, destination, and preservation proof
  - inventory exact-string dependencies separately and classify normative, parser/package, incidental-test, obsolete, or historical-fixture treatment
  - identify duplicate clusters and one intended loaded owner
  - serialize deterministic scenario fixtures with required and forbidden outcomes
  - record LF-normalized baseline words, bytes, exact resources, all four procedural profiles, both assets, and total package
- Validation commands:
  - run the exact `M1 change-local evidence proof` command in the Validation plan
  - `python scripts/validate-change-metadata.py docs/changes/2026-08-13-plan-review-skill-simplification/change.yaml`
  - independently inspect both ledgers against the complete current skill and exact-string consumers
- Expected observable result: every current rule, literal, duplicate, and lifecycle scenario has one closed treatment; unknown values fail first; canonical skill prose remains unchanged.
- Completion criteria: change-local evidence is complete, deterministic proof passes, and independent M1 code review is clean or resolved.
- Required evidence: M1 preservation and measurement evidence plus code-review receipt.
- Review handoff: `code-review` reviews the complete inventories, baseline, scenarios, and fail-closed evidence before M2.
- Optional commit boundary: `M1: freeze plan-review rule and literal ownership`
- Risks:
  - similar review and settlement passages may encode different authority boundaries
  - an incidental assertion may be mistaken for a normative literal
- Rollback/recovery:
  - revert M1 evidence without changing canonical skill behavior

### M2. Separate portable judgment from governed transaction procedure

- Milestone kind: implementation
- Goal: Create a shorter self-sufficient portable formal-review path and move only governed candidate, operation-state, settlement, retry, recovery, and workflow-managed procedure into one reference.
- Requirements: R1-R47.
- Architecture decisions: existing package-resource architecture and reviewed-plan transaction ADR; no new architecture decision.
- Files/components likely touched:
  - `skills/plan-review/SKILL.md`
  - `skills/plan-review/references/governed-plan-review-settlement.md`
  - `skills/plan-review/assets/review-result-skeleton.md`
  - `skills/plan-review/assets/material-finding.md`
  - `specs/skill-contract.md`
  - `specs/formal-review-recording.md` only if exact plan-review projection needs clarification
  - `specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md` only if current text contradicts the approved retained-evidence or idempotency contract
  - existing review-family validators, tests, and fixtures directly coupled to changed literals
- Dependencies:
  - M1 evidence and code review are closed
- Tests and proof:
  - exact operation, candidate, settlement, execution, status, and transaction vocabularies with unknown-value regression tests
  - four exact resource profiles and required/forbidden loads
  - complete portable judgment and recording without governed procedure
  - candidate load without authority and invalid-candidate no-fallback behavior
  - initial review, each non-clean status, blocked recording, pending initialization, matching settlement, active idempotency, stale identity, conflicting bases, open resolution, and interruption reconciliation
  - six result groups, judgment omission on invalid retry, no placeholders, and byte-identical finding structure
  - unchanged boundary activation and reference identity
- Implementation steps:
  - add failing focused assertions to existing validators before moving prose
  - rewrite `SKILL.md` from the rule ledger with concise executable recording and every universal obligation
  - create the governed reference with non-overlapping candidate, initial-review, retry, settlement, recovery, and workflow-managed sections
  - add the result and finding assets as structural-only owners
  - preserve stable artifact and reviewed-revision identity and prohibit hashes or `content_identity`
  - migrate parser/package literals atomically and update incidental tests instead of preserving accidental prose
- Validation commands:
  - `python scripts/validate-skills.py skills/plan-review/SKILL.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-build-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/validate-boundary-first.py --check --path specs/plan-review-skill-simplification.md`
- Expected observable result: portable formal review is executable from a shorter common path; governed procedure loads only for candidates and grants no authority by loading; every transaction and output rule remains compatible and deterministic.
- Completion criteria: focused contract, validator, lifecycle, recording, and package tests pass and independent M2 code review is clean or resolved.
- Required evidence: M2 package implementation evidence, validation results, and code-review receipt.
- Review handoff: `code-review` reviews the skill package, governed transaction, assets, coupled contracts, and focused tests.
- Optional commit boundary: `M2: simplify plan-review package paths`
- Risks:
  - concise recording may omit collision, blocked-write, or review-resolution behavior
  - candidate loading may be mistaken for settlement authority
  - retry logic may duplicate judgment or mutate the wrong entry
- Rollback/recovery:
  - restore the prior complete canonical package and coupled consumers together, then regenerate derived outputs

### M3. Prove profile reduction and complete package parity

- Milestone kind: implementation
- Goal: Prove profile-specific reduction, semantic preservation, exact reviewed-plan behavior, boundary identity, and canonical-through-installed package integrity.
- Requirements: R40, R47, R48, R49, R50, R51, R52, R53, R54, R55.
- Architecture decisions: existing resource-integrity and reviewed-plan ADRs.
- Files/components likely touched:
  - existing adapter-distribution or package tests only if focused `plan-review` selection is absent
  - `docs/changes/2026-08-13-plan-review-skill-simplification/evidence/simplification-measurements.md`
  - `docs/changes/2026-08-13-plan-review-skill-simplification/evidence/semantic-preservation-review.md`
  - `docs/changes/2026-08-13-plan-review-skill-simplification/evidence/m3-package-proof.md`
- Dependencies:
  - M2 package refactor and code review are closed
- Tests and proof:
  - canonical, generated, archived, and temporary installed targets contain both references and both assets at required paths and raw bytes
  - missing, escaped, transformed, stale, or mixed resources fail existing proof owners
  - all four procedural assemblies count each normalized unique resource once
  - all boundaries and interactions map to direct static proof
  - no acceptance command invokes or grades a target agent
- Implementation steps:
  - extend only existing package proof when direct `plan-review` selection is missing
  - generate supported package forms in temporary directories and inspect exact resources
  - report before/after main file, each resource, every procedural profile, each asset, total package, duplicate clusters, inline templates, and mapped-resource counts
  - require lower `PRV0-portable` and `PRV1-governed` words and bytes and explain total-package change
  - independently review the final package against both ledgers, every lifecycle scenario, and R55 reassessment triggers
- Validation commands:
  - `python scripts/test-adapter-distribution.py`
  - run the exact `Temporary plan-review adapter proof` command in the Validation plan
  - `python scripts/validate-skills.py skills/plan-review/SKILL.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-boundary-first.py --check --path specs/plan-review-skill-simplification.md`
- Expected observable result: portable and governed profiles shrink, total package movement is honest, semantics and transaction behavior remain complete, and every supported package contains byte-consistent resources without target-runtime execution.
- Completion criteria: measurement, semantic review, boundary proof, package proof, and independent M3 code review are complete before final holistic review.
- Required evidence: M3 measurement, semantic-preservation, package-proof, and code-review records.
- Review handoff: `code-review` reviews complete proof and package integrity; final holistic review remains a later lifecycle gate.
- Optional commit boundary: `M3: prove plan-review simplification`
- Risks:
  - generic adapter checks may pass without selecting `plan-review`
  - main-file reduction may hide governed-profile or total-package growth
  - package rollout may mix old and new ownership
- Rollback/recovery:
  - restore the previous package, regenerate every derived target, and discard temporary package trees

## Validation plan

### M1 change-local evidence proof

The ledgers and scenarios use JSON serialization valid as YAML. The standard-library proof rejects unknown values before consistency checks, requires unique stable IDs, validates required fields, and checks the exact scenario inventory.

```bash
python -c 'import json; from pathlib import Path; root=Path("docs/changes/2026-08-13-plan-review-skill-simplification"); rules=json.loads((root/"plan-review-rule-disposition.yaml").read_text())["rules"]; literals=json.loads((root/"plan-review-literal-compatibility.yaml").read_text())["literals"]; scenarios=json.loads((root/"fixtures/scenario-contracts.yaml").read_text())["scenarios"]; bad_rule=json.loads((root/"fixtures/invalid-rule-disposition.yaml").read_text()); bad_literal=json.loads((root/"fixtures/invalid-literal-classification.yaml").read_text()); rd={"retained-inline","retained-governed-reference","retained-boundary-reference","asset-owned","removed-duplicate","removed-obsolete-with-approved-contract-change"}; lc={"normative-contract","parser-or-package-contract","test-only-incidental","obsolete","historical-fixture"}; rf={"rule_id","source_locations","behavior","governing_requirements","applicable_profiles","disposition","destination","preservation_proof"}; lf={"literal_id","literal","source_location","consumers","classification","required_semantics","disposition","replacement"}; vr=lambda row: ["unknown-disposition"] if row.get("disposition") not in rd else (["missing-required-fields"] if not rf <= row.keys() else (["empty-required-fields"] if not all(row[field] for field in rf) else [])); vl=lambda row: ["unknown-classification"] if row.get("classification") not in lc else (["missing-required-fields"] if not lf <= row.keys() else (["empty-required-fields"] if not all(row[field] for field in lf) else [])); expected={"portable-clean","portable-material","blocked-recording","governed-candidate-invalid","governed-initial-clean","governed-changes-requested","governed-blocked","governed-inconclusive","retry-initialization-absent","retry-matching","retry-already-active","retry-stale-plan","retry-duplicate-review","retry-mismatched-basis","retry-open-resolution","planned-work-without-clean-review","interrupted-settlement","boundary-portable","boundary-governed","missing-resource","asset-judgment-omitted","workflow-managed","invalid-vocabulary"}; assert rules and literals; assert all(vr(row) == [] for row in rules); assert all(vl(row) == [] for row in literals); assert vr(bad_rule)[0] == "unknown-disposition"; assert vl(bad_literal)[0] == "unknown-classification"; assert len({row["rule_id"] for row in rules}) == len(rules); assert len({row["literal_id"] for row in literals}) == len(literals); assert {row["scenario"] for row in scenarios} == expected; assert all(row.get("required") and row.get("forbidden") for row in scenarios); print(f"rules={len(rules)} literals={len(literals)} scenarios={len(scenarios)} unknown_values=rejected-first")'
```

- `python scripts/validate-skills.py skills/plan-review/SKILL.md`: normalized structure, Resource map, containment, placeholders, portability, and claim boundaries.
- `python scripts/test-skill-validator.py`: focused skill-contract and regression proof.
- `python scripts/test-build-skills.py` and `python scripts/build-skills.py --check`: generated inventory and resource parity.
- `python scripts/test-adapter-distribution.py`: adapter generation, archive, and installed-resource regressions.
- `Temporary plan-review adapter proof`: direct all-target package proof using the current tracked adapter-manifest version.

```bash
plan_review_adapter_tmp="$(mktemp -d)"
trap 'rm -rf "$plan_review_adapter_tmp"' EXIT
python scripts/build-adapters.py --version v0.1.5 --output-dir "$plan_review_adapter_tmp"
python scripts/validate-adapters.py --version v0.1.5 --adapter-root "$plan_review_adapter_tmp" --clean-install-smoke --skill plan-review
```

- `python scripts/validate-boundary-first.py --check --path specs/plan-review-skill-simplification.md`: boundary record and matching proof-map coverage.
- Change metadata, lifecycle, review-artifact, Markdown readability, and diff checks: change-local governance proof.
- Independent semantic review: package ownership, judgment, recording, candidate loading, operation state, settlement, evidence retention, output applicability, boundary activation, automation, failures, claims, handoff, and literal treatment.

## Risks and recovery

- Risk: conditional extraction hides universal recording or plan-quality behavior.
  - Recovery: rule ledger, portable scenarios, focused assertions, and semantic review block the move; restore the prior package atomically.
- Risk: retry classification or settlement diverges from the accepted ADR.
  - Recovery: direct static lifecycle cases prove each legal and illegal state; restore the prior transaction procedure if identity or ownership differs.
- Risk: incidental literal tests become policy owners.
  - Recovery: keep literal classification separate and migrate only real contracts atomically.
- Risk: relocation is reported as deletion.
  - Recovery: report every profile and total package in words and bytes, with semantic preservation taking precedence.
- Risk: one package target omits a new resource.
  - Recovery: block acceptance on selected archive and installed-tree parity, then regenerate from the last complete canonical revision.

## Dependencies

- Accepted proposal, approved identity-corrected spec, clean formal reviews, and recorded `architecture-not-required` assessment.
- Existing formal-review recording, review-family asset, boundary projection, published-skill package, and reviewed-plan transaction contracts.
- Existing skill validation, build, adapter generation, archive, clean-install, lifecycle, and review-artifact proof owners.
- Approved test specification and test-spec review before implementation.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-13 | Use three implementation milestones: preservation evidence, package/transaction refactor, and profile/package proof. | Each has an independent review, proof, and rollback boundary. | One large prose and package rewrite. |
| 2026-08-13 | Freeze semantic rules and literal dependencies before moving prose. | Behavioral ownership and exact-string compatibility require different evidence. | One combined ledger or preserving every asserted phrase. |
| 2026-08-13 | Keep all operation and transaction implementation in M2. | Splitting the governed state machine across milestones would create an unsafe partial package. | Separate initial-review and retry milestones. |
| 2026-08-13 | Treat basis evidence retention and no-hash identity as architecture-preserving invariants. | The accepted ADR already owns those decisions. | New content identity or optional evidence deletion. |

## Readiness

- See the owning change record for current workflow state. The stable plan is ready for formal `plan-review` after plan authoring evidence and change-record registration complete.
