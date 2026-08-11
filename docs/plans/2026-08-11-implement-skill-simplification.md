# Implement Skill Simplification Execution Plan

## Purpose / big picture

Simplify the published `implement` package without weakening implementation or lifecycle behavior. The work first accounts for semantic rules and literal dependencies, then refactors the universal and conditional instruction surfaces, and finally proves profile-specific context reduction plus canonical, generated, archived, and temporary installed package integrity.

## Current Handoff Summary

- Owning change record: `docs/changes/2026-08-11-implement-skill-simplification/change.yaml`

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: `docs/proposals/2026-08-11-implement-skill-simplification.md`
- Spec: `specs/implement-skill-simplification.md`
- Architecture: not required; recorded in `docs/changes/2026-08-11-implement-skill-simplification/architecture-assessment.md`
- Test spec: pending at `specs/implement-skill-simplification.test.md`

## Context and orientation

`skills/implement/` is the only authored package source. The current package contains `SKILL.md` and the mapped boundary-first reference. This change adds two conditionally loaded procedure references and one structural result asset while retaining universal authority, prerequisites, test-first execution, completeness, validation, stop, claim, direct-handoff, profile-classification, and resource-trigger policy inline.

`scripts/skill_validation.py`, `scripts/validate-skills.py`, and `scripts/test-skill-validator.py` own canonical skill and mapped-resource proof. `scripts/adapter_distribution.py`, `scripts/build-adapters.py`, `scripts/validate-adapters.py`, and `scripts/test-adapter-distribution.py` own generated, archived, and temporary installed-tree proof for supported adapters. Existing owners must be extended only where focused `implement` coverage is absent; this plan creates no standalone simplification validator.

The semantic-rule ledger, literal-compatibility ledger, scenario fixtures, and size measurements are change-local evidence. They prove this refactor without becoming permanent prose or size budgets.

## Non-goals

- Simplify another skill or change existing implementation, milestone, review-fix, validation, claim, or downstream-stage semantics.
- Add target-agent execution, prompt journeys, transcript grading, model-selection evidence, or nondeterministic retries.
- Add a permanent simplicity, token, word, line, prose-quality, selector, scheduler, or validator family.
- Give a reference or asset independent policy, lifecycle, or readiness ownership.
- Hand-edit generated adapter packages or installed runtime copies.
- Treat the 30–45 percent planning range as a normative acceptance threshold.

## Requirements covered

| Requirement and boundary scope | Owning milestone or evidence |
| --- | --- |
| R16-R22, R28; BND-INPUT-001, BND-AUTH-001, BND-RECOVERY-001, BND-COMPAT-001; INT-005, INT-007 | M1 semantic/literal inventories, fixtures, negative proof, and baseline measurements |
| R1-R15, R31; BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001; INT-001-INT-004 | M2 universal contract, two conditional references, one grouped result asset, and focused validator coverage |
| R23-R30, R33; BND-COMPOSE-001, BND-RECOVERY-001, BND-COMPAT-001, BND-ENV-001; INT-006-INT-008 | M3 profile measurements, semantic preservation, and generated/archive/installed package proof |
| R32 | Completed `architecture-not-required` assessment before this plan |

## Milestones

### M1. Freeze semantic and literal ownership

- Milestone type: implementation.
- Goal: Account for every behaviorally significant current rule and compatibility-sensitive literal, and establish deterministic fixtures before moving or deleting prose.
- Requirements: R16-R22, R28; BND-INPUT-001; BND-AUTH-001; BND-RECOVERY-001; BND-COMPAT-001; INT-005; INT-007.
- Files/components likely touched:
  - `docs/changes/2026-08-11-implement-skill-simplification/implement-rule-disposition.yaml`
  - `docs/changes/2026-08-11-implement-skill-simplification/implement-literal-compatibility.yaml`
  - `docs/changes/2026-08-11-implement-skill-simplification/fixtures/`
  - `docs/changes/2026-08-11-implement-skill-simplification/evidence/profile-size-baseline.md`
- Dependencies:
  - approved feature spec and recorded architecture assessment
  - current canonical `skills/implement/` package and exact literal consumers as the inventory baseline
- Tests to add/update:
  - static scenarios for all valid profiles, invalid unplanned automation, stale or mismatched authority, result groups, validation failure, spec gaps, accepted correction return, review handoff, and premature milestone transition
  - unknown semantic disposition and unknown literal classification negative fixtures
  - complete required fields, one disposition/classification per entry, and exact closed vocabularies
- Implementation steps:
  - inventory significant rules and duplication clusters with stable IDs, source locations, behavior, requirements, applicable profiles, disposition, destination, and preservation proof
  - inventory exact-string consumers and classify normative, parser/package, incidental-test, and obsolete dependencies independently from semantic rules
  - create JSON-compatible YAML scenario and invalid-value fixtures without executing a model
  - record LF-normalized resource identities and baseline words and UTF-8 bytes for all three profiles and the total package
  - route any proposed obsolete semantic rule lacking an approved contract change back to the spec owner
- Validation commands:
  - `python scripts/validate-change-metadata.py docs/changes/2026-08-11-implement-skill-simplification/change.yaml`
  - run the exact `M1 change-local ledger and fixture proof` command in the Validation plan
  - independently inspect ledger coverage against the complete current `skills/implement/SKILL.md` and its literal consumers
- Expected observable result: every significant rule and discovered literal has one closed treatment, all required scenario classes exist, unknown values fail closed, and no canonical skill prose has moved.
- Commit message: `M1: freeze implement rule and literal ownership`
- Milestone closeout: targeted proof and implementation evidence, followed by independent code review and any required resolution.
- Risks:
  - repeated passages may encode distinct behavior despite similar wording
  - an incidental assertion may be mistaken for a normative contract
- Rollback/recovery:
  - revert the M1 evidence slice; the canonical skill remains unchanged

### M2. Refactor the universal and conditional package surfaces

- Milestone type: implementation.
- Goal: Make `SKILL.md` a shorter self-sufficient universal contract, move only planned and armed procedure to their exact references, and make one asset the sole result-layout owner.
- Requirements: R1-R15, R31; BND-INPUT-001; BND-STATE-001; BND-AUTH-001; BND-COMPOSE-001; BND-TEMPORAL-001; INT-001-INT-004.
- Files/components likely touched:
  - `skills/implement/SKILL.md`
  - `skills/implement/references/planned-milestone-implementation.md`
  - `skills/implement/references/automated-review-correction.md`
  - `skills/implement/assets/implementation-result-skeleton.md`
  - `scripts/test-skill-validator.py`
  - literal consumers classified for atomic migration in M1
- Dependencies:
  - M1 inventories, fixtures, baseline, and code review are complete
- Tests to add/update:
  - exact three-profile classification and invalid armed-without-planned stop
  - identity-bound, non-conversational trigger evidence and stale/mismatched stop behavior
  - exact `READ` mappings and required/forbidden reference loads
  - planned/automation reference ownership and no cross-reference policy duplication
  - sole `COPY` asset ownership, exact core/planned/armed groups, omission of inapplicable groups, and absence of policy/placeholders
  - preservation of universal status, validation, stop, claim, correction, milestone, and handoff semantics
- Implementation steps:
  - add failing focused assertions to the existing skill-validator suite before changing package text
  - consolidate universal repetition according to the semantic ledger while retaining all R3 policy inline
  - create the planned reference and move only R9 procedure
  - create the automation reference and move only R11 procedure
  - create the grouped result skeleton and remove overlapping inline output structures
  - migrate real literal consumers atomically, update incidental tests, and update both ledgers with final destinations
- Validation commands:
  - `python scripts/validate-skills.py skills/implement/SKILL.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-build-skills.py`
  - `python scripts/build-skills.py --check`
- Expected observable result: isolated implementation is complete from a shorter `SKILL.md`; planned and planned-armed profiles load only their exact procedures; one policy-free asset supplies applicable result structure.
- Commit message: `M2: simplify implement package paths`
- Milestone closeout: focused skill proof and implementation evidence, followed by independent code review and any required resolution.
- Risks:
  - universal policy could move behind a conditional trigger
  - an asset or procedure reference could become a competing policy owner
  - exact-string migrations could weaken a real parser contract
- Rollback/recovery:
  - restore the prior complete canonical package and focused assertions as one slice, then regenerate derived packages

### M3. Prove profile reduction and package parity

- Milestone type: implementation.
- Goal: Prove deterministic behavior and filesystem identity across all profiles and supported package targets, then record honest size and semantic-preservation evidence.
- Requirements: R23-R30, R33; BND-COMPOSE-001; BND-RECOVERY-001; BND-COMPAT-001; BND-ENV-001; INT-006-INT-008.
- Files/components likely touched:
  - `scripts/test-adapter-distribution.py` only if existing focused selection cannot prove `implement`
  - existing adapter fixtures only when focused coverage is absent
  - `docs/changes/2026-08-11-implement-skill-simplification/evidence/simplification-measurements.md`
  - `docs/changes/2026-08-11-implement-skill-simplification/evidence/semantic-preservation-review.md`
- Dependencies:
  - M2 package refactor and code review are complete
- Tests to add/update:
  - every supported generated, archived, and temporary installed target contains both references and the asset at identical relative paths and bytes
  - missing, escaped, or stale mapped resources fail package proof
  - all profile fixtures remain deterministic and no command starts or grades a target agent
  - LF-normalized loaded-resource accounting counts each unique resource once in documented order
- Implementation steps:
  - extend only existing adapter-distribution proof where direct `implement` selection is missing
  - generate supported packages into a temporary output directory and validate archive plus clean-install mapped-resource parity
  - record before/after words, UTF-8 bytes, resource identities, `SKILL.md`, each resource, total package, duplicate clusters, inline templates, and mapped-resource counts
  - require material `IP0-isolated` and `IP1-planned` improvement, explain `IP2-planned-armed` non-regression, and keep token evidence optional and pinned
  - independently review the complete package against both ledgers and R31
- Validation commands:
  - `python scripts/test-adapter-distribution.py`
  - `ADAPTER_OUTPUT_DIR="$(mktemp -d)"; python scripts/build-adapters.py --version 0.0.0-implement-simplification --output-dir "$ADAPTER_OUTPUT_DIR"; python scripts/validate-adapters.py --version 0.0.0-implement-simplification --adapter-root "$ADAPTER_OUTPUT_DIR" --clean-install-smoke --skill implement`
  - `python scripts/validate-skills.py skills/implement/SKILL.md`
  - `python scripts/test-skill-validator.py`
- Expected observable result: isolated and planned profiles materially shrink, armed context has no unjustified growth, semantics are preserved, and canonical through installed resource bytes match without target-runtime execution.
- Commit message: `M3: prove implement simplification`
- Milestone closeout: package and evidence proof, independent code review, and required resolution before final lifecycle closeout.
- Risks:
  - generic adapter tests may pass without selecting the changed skill
  - a main-file decrease may hide planned-profile or total-package growth
  - partial packaging could mix old and new ownership
- Rollback/recovery:
  - restore the prior complete canonical package, regenerate every derived target, and discard temporary package trees

## Validation plan

### M1 change-local ledger and fixture proof

The ledgers and fixtures use JSON serialization, which is valid YAML. The standard-library proof rejects unknown closed values before treatment or destination consistency and validates the required scenario identities.

```bash
python -c 'import json; from pathlib import Path; root=Path("docs/changes/2026-08-11-implement-skill-simplification"); rules=json.loads((root/"implement-rule-disposition.yaml").read_text())["rules"]; literals=json.loads((root/"implement-literal-compatibility.yaml").read_text())["literals"]; scenarios=json.loads((root/"fixtures/scenario-contracts.yaml").read_text())["scenarios"]; bad_rule=json.loads((root/"fixtures/invalid-rule-disposition.yaml").read_text()); bad_literal=json.loads((root/"fixtures/invalid-literal-classification.yaml").read_text()); rd={"retained-inline","retained-planned-reference","retained-automation-reference","asset-owned","removed-duplicate","removed-obsolete-with-approved-contract-change"}; lc={"normative-contract","parser-or-package-contract","test-only-incidental","obsolete"}; rf={"rule_id","source_locations","behavior","governing_requirements","applicable_profiles","disposition","destination","preservation_proof"}; lf={"literal_id","literal","source_location","consumers","classification","required_semantics","disposition","replacement"}; expected={"isolated","planned","planned-armed","invalid-unplanned-armed","stale-or-mismatched-authority","result-group-applicability","validation-failure","specification-gap","accepted-correction-return","code-review-handoff","premature-next-milestone-transition"}; assert rules and literals; assert all(rf <= row.keys() for row in rules); assert all(lf <= row.keys() for row in literals); assert not [row.get("disposition") for row in rules if row.get("disposition") not in rd]; assert not [row.get("classification") for row in literals if row.get("classification") not in lc]; assert len({row["rule_id"] for row in rules}) == len(rules); assert len({row["literal_id"] for row in literals}) == len(literals); assert {row["scenario"] for row in scenarios} == expected; assert all(row.get("required") and row.get("forbidden") for row in scenarios); assert bad_rule.get("disposition") not in rd; assert bad_literal.get("classification") not in lc; print(f"rules={len(rules)} literals={len(literals)} scenarios={len(scenarios)} unknown_values=rejected")'
```

- `python scripts/validate-skills.py skills/implement/SKILL.md`: canonical structure, Resource-map syntax, containment, placeholders, and narrow claim checks.
- `python scripts/test-skill-validator.py`: focused skill-contract and regression proof.
- `python scripts/test-build-skills.py` and `python scripts/build-skills.py --check`: generated skill inventory and resource parity.
- `python scripts/test-adapter-distribution.py`: adapter generation, archive, resource, and clean-install regression proof.
- Temporary build plus `validate-adapters.py --clean-install-smoke --skill implement`: direct all-target archive and installed-tree proof for the changed package.
- `python scripts/validate-boundary-first.py --check --path specs/implement-skill-simplification.md`: final feature-to-proof boundary coverage; the validator discovers the matching `.test.md` proof map.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-11-implement-skill-simplification/change.yaml`: lifecycle and planned-work consistency.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-08-11-implement-skill-simplification`: formal review structure.
- Independent semantic review: profile authority, universal completeness, reference and asset ownership, test-first and validation semantics, stops, claims, correction return, handoff, and literal treatment.

## Risks and recovery

- Risk: conditional extraction hides universal behavior.
  - Recovery: the rule ledger, profile fixtures, focused validator assertions, and semantic review block the move; restore the prior package atomically.
- Risk: incidental literal tests become accidental policy owners.
  - Recovery: classify literal consumers separately and migrate only real contracts atomically.
- Risk: relocation is reported as deletion or a misleading percentage win.
  - Recovery: report every profile and the total package in words and bytes, with semantic preservation taking precedence.
- Risk: one package target omits a new resource.
  - Recovery: block acceptance on selected archive and temporary installed-tree parity, then regenerate from the last complete canonical revision.

## Dependencies

- Approved proposal and spec, approving formal reviews, closed review resolution, and recorded `architecture-not-required` assessment.
- Existing boundary-first reference and published-skill resource/package architecture.
- Existing skill validation, adapter generation, archive validation, and clean-install resource owners.
- Approved test specification and test-spec review before implementation.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-11 | Use three implementation milestones: preservation evidence, package refactor, and profile/package proof. | Each slice has an independent failure, review, and rollback boundary. | One large prose-and-package rewrite. |
| 2026-08-11 | Keep semantic and literal inventories separate and validate both change-locally before prose movement. | Behavior preservation and exact-string compatibility are different contracts. | One combined ledger; preserve every asserted phrase. |
| 2026-08-11 | Extend only existing skill and adapter validators for durable proof. | The approved contract excludes a permanent simplicity validator family. | New simplification CLI or token-budget gate. |
| 2026-08-11 | Measure all three loaded profiles plus total package words and bytes. | `SKILL.md` size alone can hide planned-profile regression or relocation cost. | Main-file percentage as the acceptance gate. |

## Readiness

- See the owning change record for current workflow state.
- Readiness is not Done; plan review, test-spec authoring and review, all implementation and code-review milestones, final review, explanation, verification, and PR handoff remain.
