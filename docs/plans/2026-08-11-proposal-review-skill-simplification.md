# Proposal-Review Skill Simplification Execution Plan

## Purpose / big picture

Simplify the published `proposal-review` package without weakening proposal judgment, durable review recording, formal settlement, specialized gates, or handoff authority.
The work first freezes semantic and literal ownership, then separates the universal advisory path from two conditional procedures and structural layouts, and finally proves assembly reduction and package integrity.

## Current Handoff Summary

- Owning change record: `docs/changes/2026-08-11-proposal-review-skill-simplification/change.yaml`

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: `docs/proposals/2026-08-11-proposal-review-skill-simplification.md`
- Spec: `specs/proposal-review-skill-simplification.md`
- Architecture: not required; recorded in `docs/changes/2026-08-11-proposal-review-skill-simplification/architecture-assessment.md`
- Test spec: pending at `specs/proposal-review-skill-simplification.test.md`

## Context and orientation

`skills/proposal-review/` is the only authored package source.
The current package contains `SKILL.md` and two structural assets.
This change adds `references/proposal-review-recording-and-settlement.md` and `references/conditional-proposal-gates.md`, keeps universal proposal judgment, materiality, status, recording triggers, authority, stops, claims, and resource selection inline, and makes the existing assets the sole repeated result and finding layouts.

`specs/formal-review-recording.md` remains the authority for change-ID selection, generated minimal recording roots, required log and resolution evidence, and blocked recording.
`scripts/skill_validation.py`, `scripts/validate-skills.py`, and `scripts/test-skill-validator.py` own canonical skill and mapped-resource proof.
Adapter generation and validation scripts own generated, archived, and temporary installed-tree proof.

Semantic-rule, literal-compatibility, static-scenario, and measurement artifacts are change-local evidence, not a new permanent validator family.

## Non-goals

- Change proposal judgment, review statuses, material finding shape, formal recording, settlement, isolation, claim, or handoff semantics.
- Change workflow stages, `change.yaml`, formal-review artifact schemas, correction authority, adapter roots, or publication behavior.
- Add more than two conditional references or the two existing structural assets.
- Add a generic review engine, runtime reviewer, target-agent execution, prompt journey, or transcript grader.
- Add permanent simplicity, token, word, line, prose-quality, semantic-classifier, scenario-framework, selector, or scheduler machinery.
- Hand-edit generated adapters or installed runtime copies.
- Treat the advisory 30-45 percent reduction as a semantic gate.

## Requirements covered

| Requirement and boundary scope | Owning milestone or evidence |
| --- | --- |
| R29-R34; BND-INPUT-001, BND-RECOVERY-001, BND-COMPAT-001, BND-ENV-001; INT-005 | M1 semantic and literal inventories, scenarios, negative fixtures, and baseline measurement |
| R1-R28; BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001; INT-001-INT-004 | M2 universal skill, two references, result groups, exact authority, and focused validation |
| R32-R35, R37; BND-COMPOSE-001, BND-RECOVERY-001, BND-COMPAT-001, BND-ENV-001; INT-005-INT-006 | M3 assembly measurement, semantic preservation, and generated, archive, and installed proof |
| R36 | Completed `architecture-not-required` assessment before this plan |

## Milestones

### M1. Freeze proposal-review rule and literal ownership

- Milestone state: planned
- Goal: Account for every behaviorally significant rule and compatibility-sensitive literal, and establish deterministic static scenarios before moving prose.
- Requirements: R29-R34; BND-INPUT-001; BND-RECOVERY-001; BND-COMPAT-001; BND-ENV-001; INT-005.
- Files/components likely touched:
  - `docs/changes/2026-08-11-proposal-review-skill-simplification/proposal-review-rule-disposition.yaml`
  - `docs/changes/2026-08-11-proposal-review-skill-simplification/proposal-review-literal-compatibility.yaml`
  - `docs/changes/2026-08-11-proposal-review-skill-simplification/fixtures/`
  - `docs/changes/2026-08-11-proposal-review-skill-simplification/evidence/profile-size-baseline.md`
- Dependencies:
  - approved spec, clean spec review, and recorded architecture assessment
  - complete current `skills/proposal-review/` package and exact literal consumers
- Tests to add/update:
  - static scenarios for advisory, durable, material, formal, automated, specialized, combined, late-trigger, fallback-root, blocked-recording, output-group, missing-resource, and package profiles
  - unknown semantic disposition and literal classification fixtures
  - required fields, unique IDs, exact closed vocabulary, and non-empty required and forbidden scenario outcomes
- Implementation steps:
  - inventory significant rules and duplicate clusters with stable IDs, sources, behavior, requirements, assemblies, disposition, destination, and preservation proof
  - inventory exact-string consumers separately as normative, parser/package, incidental-test, or obsolete
  - serialize ledgers and fixtures as JSON-compatible YAML and prove unknown values fail before consistency checks
  - record LF-normalized baseline words, bytes, resource identities, four assemblies, and total package
  - route any proposed obsolete semantic rule without an approved contract change to the spec owner
- Validation commands:
  - run the exact `M1 change-local ledger and fixture proof` command below
  - `python scripts/validate-change-metadata.py docs/changes/2026-08-11-proposal-review-skill-simplification/change.yaml`
  - independently inspect coverage against the complete current skill and literal consumers
- Expected observable result: every current rule and literal has one closed treatment, all required scenarios exist, unknown values fail closed, and canonical skill prose has not moved.
- Commit message: `M1: freeze proposal-review rule and literal ownership`
- Milestone closeout:
  - validation passed
  - implementation evidence recorded
  - milestone committed and handed to independent code review
- Risks:
  - similar passages may encode distinct judgment or recording behavior
  - an incidental assertion may be mistaken for a normative contract
- Rollback/recovery:
  - revert M1 evidence; canonical skill files remain unchanged

### M2. Separate universal judgment from conditional procedure

- Milestone state: planned
- Goal: Make `SKILL.md` a shorter self-sufficient advisory review contract, move only recording and specialized-gate procedure into two mapped references, and give output structure one owner.
- Requirements: R1-R28; BND-INPUT-001; BND-STATE-001; BND-AUTH-001; BND-COMPOSE-001; BND-TEMPORAL-001; BND-RECOVERY-001; INT-001-INT-004.
- Files/components likely touched:
  - `skills/proposal-review/SKILL.md`
  - `skills/proposal-review/references/proposal-review-recording-and-settlement.md`
  - `skills/proposal-review/references/conditional-proposal-gates.md`
  - `skills/proposal-review/assets/review-result-skeleton.md`
  - `skills/proposal-review/assets/material-finding.md` only if layout deduplication requires it
  - `scripts/test-skill-validator.py`
  - directly coupled literal consumers classified in M1
- Dependencies:
  - M1 evidence and code review are complete
- Tests to add/update:
  - exact recording and automation modes, valid and invalid combinations, and exhaustive late durable activation
  - change-ID selection, minimal fallback root, collision and write blockers, formal settlement identity, and continuation prohibition
  - three specialized predicates, positive and negative evidence, combined and late triggers, and ambiguity stops
  - four exact resource assemblies and required and forbidden loads
  - one core and four conditional result groups, omission, blocked data, and placeholder rejection
  - missing reference or asset, escaped path, contradiction, and mixed-version failure
  - normalized structure, shared recording block, statuses, claims, stops, and default formal record path
- Implementation steps:
  - add failing focused assertions to existing skill validation before changing package text
  - consolidate universal repetition according to the semantic ledger while retaining every R2-R8 and R28 rule inline
  - create the recording reference with visibly separate advisory, formal, and automated branches
  - create the conditional-gates reference with only specialized vision, standing-artifact, and scope-budget procedure
  - revise the result asset to one core and four conditional structural groups without policy text
  - migrate real literal consumers atomically, update incidental tests, and finalize ledger destinations
- Validation commands:
  - `python scripts/validate-skills.py skills/proposal-review/SKILL.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-build-skills.py`
  - `python scripts/build-skills.py --check`
- Expected observable result: ordinary advisory review is complete from a shorter `SKILL.md`; conditional procedure loads only from exact triggers; recording, settlement, automation, and continuation authority remain separate; assets own layout only.
- Commit message: `M2: simplify proposal-review package paths`
- Milestone closeout:
  - validation passed
  - implementation evidence recorded
  - milestone committed and handed to independent code review
- Risks:
  - a universal judgment or blocker could move behind a conditional trigger
  - late recording could accidentally grant settlement or continuation authority
  - asset consolidation could move policy into layout
  - exact-string migration could weaken a real parser contract
- Rollback/recovery:
  - restore the prior complete canonical package and focused assertions together, then regenerate derived packages

### M3. Prove assembly reduction and package parity

- Milestone state: planned
- Goal: Prove assembly-specific context reduction, semantic preservation, and canonical-through-installed package integrity.
- Requirements: R32-R35, R37; BND-COMPOSE-001; BND-RECOVERY-001; BND-COMPAT-001; BND-ENV-001; INT-005-INT-006.
- Files/components likely touched:
  - `scripts/test-adapter-distribution.py` only if existing focused selection cannot prove `proposal-review`
  - existing adapter fixtures only where focused coverage is absent
  - `docs/changes/2026-08-11-proposal-review-skill-simplification/evidence/simplification-measurements.md`
  - `docs/changes/2026-08-11-proposal-review-skill-simplification/evidence/semantic-preservation-review.md`
  - `docs/changes/2026-08-11-proposal-review-skill-simplification/evidence/m3-package-proof.md`
- Dependencies:
  - M2 package refactor and code review are complete
- Tests to add/update:
  - supported generated, archived, and temporary installed targets contain both references and both assets at identical paths and bytes
  - missing, escaped, transformed, stale, contradictory, or mixed resources fail package proof
  - all four assemblies count each LF-normalized unique resource once in documented order
  - no acceptance command starts or grades a target agent
- Implementation steps:
  - extend only existing adapter-distribution proof where direct `proposal-review` selection is absent
  - generate supported packages in a temporary directory and validate archive and clean-install resource parity
  - report before and after `SKILL.md`, each resource, PRR0, PRR0G, PRR1, PRR1G, total package, duplicate clusters, inline templates, and mapped-resource counts in words and bytes
  - require material PRR0 improvement, explain recorded-profile and total-package deltas, and keep token evidence optional and pinned
  - independently review the complete package against both ledgers and R28
- Validation commands:
  - `python scripts/test-adapter-distribution.py`
  - `python -c 'exec("""import subprocess, sys, tempfile\nversion = "v0.3.6"\nwith tempfile.TemporaryDirectory(prefix="rigorloop-adapters-") as output:\n    subprocess.run([sys.executable, "scripts/build-adapters.py", "--version", version, "--output-dir", output], check=True)\n    subprocess.run([sys.executable, "scripts/validate-adapters.py", "--version", version, "--adapter-root", output, "--clean-install-smoke", "--skill", "proposal-review"], check=True)""")'`
  - `python scripts/validate-skills.py skills/proposal-review/SKILL.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-boundary-first.py --check --path specs/proposal-review-skill-simplification.md`
- Expected observable result: ordinary assemblies materially shrink, conditional assemblies have no unjustified growth, semantics remain complete, and every supported package contains byte-identical mapped resources without target-runtime execution.
- Commit message: `M3: prove proposal-review simplification`
- Milestone closeout:
  - validation passed
  - package and semantic evidence recorded
  - milestone committed and handed to independent code review
- Risks:
  - generic adapter tests may pass without selecting `proposal-review`
  - main-file reduction may hide conditional-profile or total-package growth
  - partial packaging may mix old and new ownership
- Rollback/recovery:
  - restore the prior complete canonical package, regenerate every derived target, and discard temporary package trees

## Validation plan

### M1 change-local ledger and fixture proof

The ledgers and fixtures use JSON serialization, which is valid YAML.
This standard-library command rejects unknown closed values before destination consistency and validates every required scenario identity.

```bash
python -c 'import json; from pathlib import Path; root=Path("docs/changes/2026-08-11-proposal-review-skill-simplification"); rules=json.loads((root/"proposal-review-rule-disposition.yaml").read_text())["rules"]; literals=json.loads((root/"proposal-review-literal-compatibility.yaml").read_text())["literals"]; scenarios=json.loads((root/"fixtures/scenario-contracts.yaml").read_text())["scenarios"]; bad_rule=json.loads((root/"fixtures/invalid-rule-disposition.yaml").read_text()); bad_literal=json.loads((root/"fixtures/invalid-literal-classification.yaml").read_text()); rd={"retained-inline","retained-recording-reference","retained-conditional-gates-reference","asset-owned","removed-duplicate","removed-obsolete-with-approved-contract-change"}; lc={"normative-contract","parser-or-package-contract","test-only-incidental","obsolete"}; rf={"rule_id","source_locations","behavior","governing_requirements","applicable_assemblies","disposition","destination","preservation_proof"}; lf={"literal_id","literal","source_location","consumers","classification","required_semantics","disposition","replacement"}; dest=lambda row: (row["disposition"] == "retained-inline" and row["destination"].startswith("skills/proposal-review/SKILL.md")) or (row["disposition"] == "retained-recording-reference" and row["destination"].startswith("skills/proposal-review/references/proposal-review-recording-and-settlement.md")) or (row["disposition"] == "retained-conditional-gates-reference" and row["destination"].startswith("skills/proposal-review/references/conditional-proposal-gates.md")) or (row["disposition"] == "asset-owned" and row["destination"].startswith("skills/proposal-review/assets/")) or (row["disposition"] == "removed-duplicate" and row["destination"].startswith("skills/proposal-review/")) or (row["disposition"] == "removed-obsolete-with-approved-contract-change" and row["destination"].startswith(("specs/","docs/"))); vr=lambda row: ["unknown-disposition"] if row.get("disposition") not in rd else (["missing-required-fields"] if not rf <= row.keys() else (["empty-required-fields"] if not all(row[field] for field in rf) else (["destination-inconsistent"] if not dest(row) else []))); vl=lambda row: ["unknown-classification"] if row.get("classification") not in lc else (["missing-required-fields"] if not lf <= row.keys() else (["empty-required-fields"] if not all(row[field] for field in lf) else [])); expected={"advisory-clean","advisory-explicit-recording","advisory-material-existing-root","advisory-material-generated-root","generated-root-collision","formal-manual","formal-automated","invalid-advisory-automated","invalid-none-automated","late-durable-trigger","vision-exception","ordinary-vision","standing-artifact","standing-artifact-citation-only","scope-budget-broad","scope-budget-focused","combined-specialized","late-specialized","ambiguous-specialized","formal-specialized","result-groups","blocked-result-group","missing-reference","missing-asset","package-parity"}; assert rules and literals; assert all(vr(row) == [] for row in rules); assert all(vl(row) == [] for row in literals); assert vr(bad_rule)[0] == "unknown-disposition"; assert vl(bad_literal)[0] == "unknown-classification"; assert len({row["rule_id"] for row in rules}) == len(rules); assert len({row["literal_id"] for row in literals}) == len(literals); assert {row["scenario"] for row in scenarios} == expected; assert all(row.get("required") and row.get("forbidden") for row in scenarios); print(f"rules={len(rules)} literals={len(literals)} scenarios={len(scenarios)} unknown_values=rejected-first")'
```

- `python scripts/validate-skills.py skills/proposal-review/SKILL.md`: normalized structure, resource syntax, containment, placeholders, and narrow claim checks.
- `python scripts/test-skill-validator.py`: focused skill-contract and regression proof.
- `python scripts/test-build-skills.py` and `python scripts/build-skills.py --check`: generated skill inventory and resource parity.
- `python scripts/test-adapter-distribution.py`: adapter generation, archive, resource, and clean-install regression proof.
- Temporary adapter build plus `validate-adapters.py --clean-install-smoke --skill proposal-review`: direct all-target archive and installed-tree proof.
- `python scripts/validate-boundary-first.py --check --path specs/proposal-review-skill-simplification.md`: final boundary-to-proof coverage through the matching test spec.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-11-proposal-review-skill-simplification/change.yaml`: lifecycle and planned-work consistency.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-08-11-proposal-review-skill-simplification`: formal review structure.
- Independent semantic review: universal judgment, durable triggers, mode authority, recording fallback, specialized predicates, resource assemblies, result groups, stops, claims, settlement, handoff, and literal treatment.

## Risks and recovery

- Risk: conditional extraction hides universal proposal judgment or blocker behavior.
  - Recovery: rule ledger, core fixtures, focused assertions, and semantic review block the move; restore the prior package atomically.
- Risk: durable recording accidentally grants settlement, automation, or continuation authority.
  - Recovery: classify each authority independently and prove every forbidden write and handoff.
- Risk: generated fallback roots conflict with existing change identity.
  - Recovery: preserve formal-review-recording collision and blocked-write behavior and never infer settlement from recording.
- Risk: incidental literal tests become policy owners.
  - Recovery: classify literal consumers separately and migrate only real contracts atomically.
- Risk: relocation is reported as deletion or a misleading percentage win.
  - Recovery: report every assembly and total package words and bytes, with semantic preservation taking precedence.
- Risk: one package target omits a new reference or existing asset.
  - Recovery: block acceptance on selected archive and temporary installed-tree parity, then regenerate from the last complete canonical revision.

## Dependencies

- Accepted proposal, approved spec, clean formal reviews, closed prior finding resolution, and recorded `architecture-not-required` assessment.
- Governing formal-review-recording and installed-skill artifact-placement contracts.
- Existing published-skill resource and package architecture.
- Existing skill validation, adapter generation, archive validation, and clean-install resource owners.
- Approved test specification and test-spec review before implementation.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-11 | Use three implementation milestones: preservation evidence, package refactor, and assembly and package proof. | Each slice has an independent failure, review, and rollback boundary. | One large prose-and-package rewrite. |
| 2026-08-11 | Keep semantic and literal inventories separate and validate both before prose movement. | Behavior preservation and exact-string compatibility are different contracts. | One combined ledger; preserve every asserted phrase. |
| 2026-08-11 | Keep recording, settlement, automation, and continuation independently authorized. | Material advisory findings need evidence without acquiring lifecycle authority. | Authority-coupled packages or duplicated procedure. |
| 2026-08-11 | Reuse the existing assets with closed result groups. | One layout owner removes duplication without moving policy into assets. | New profile-specific assets or inline templates. |
| 2026-08-11 | Extend only existing skill and adapter validators for durable proof. | The contract excludes a permanent simplification validator. | New CLI, tokenizer, or runtime journey gate. |
| 2026-08-11 | Measure four assemblies and total package words and bytes. | Main-file size alone can hide conditional-profile or relocation cost. | A normative percentage threshold. |

## Readiness

- See the owning change record for current workflow state.
- Readiness is not Done; plan review, test-spec authoring and review, implementation and code-review milestones, explanation, verification, and PR handoff remain.
