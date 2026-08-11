# Verify Skill Simplification Execution Plan

## Purpose / big picture

Simplify the published `verify` package without weakening verification or `branch-ready` authority.
The work first freezes semantic and literal ownership, then separates the universal common path from final-readiness procedure, and finally proves scoped-profile reduction and package integrity.

## Current Handoff Summary

- Owning change record: `docs/changes/2026-08-11-verify-skill-simplification/change.yaml`

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: `docs/proposals/2026-08-11-verify-skill-simplification.md`
- Spec: `specs/verify-skill-simplification.md`
- Architecture: not required; recorded in `docs/changes/2026-08-11-verify-skill-simplification/architecture-assessment.md`
- Test spec: pending at `specs/verify-skill-simplification.test.md`

## Context and orientation

`skills/verify/` is the only authored package source.
The current package contains `SKILL.md` and the mapped boundary-first reference.
This change adds `references/branch-readiness-verification.md`, keeps requested-outcome classification, exact target resolution, item-level evidence semantics, execution authority, universal stops, claims, and compact results inline, and moves only final applicability, aggregation, closeout, and mode-specific completion procedure.

`scripts/skill_validation.py`, `scripts/validate-skills.py`, and `scripts/test-skill-validator.py` own canonical skill and mapped-resource proof.
`scripts/adapter_distribution.py`, adapter generation/validation commands, and `scripts/test-adapter-distribution.py` own generated, archived, and temporary installed-tree proof.
Existing owners are extended only where focused `verify` coverage is absent.

Semantic-rule, literal-compatibility, static-scenario, and measurement artifacts are change-local evidence, not permanent policy or a new validator family.

## Non-goals

- Change verification verdicts, branch-ready ownership, lifecycle/review closeout, CI, release, claim, recording, output, or handoff semantics.
- Change workflow stages, `change.yaml`, planned-work state, PR authority, adapter roots, or publication behavior.
- Add a result asset, multiple final-readiness fragments, a runtime verifier, target-agent execution, prompt journeys, or transcript grading.
- Add permanent simplicity, token, word, line, prose-quality, scenario-framework, selector, or scheduler machinery.
- Hand-edit generated adapters or installed runtime copies.
- Treat the advisory 30-40 percent reduction as a semantic gate.

## Requirements covered

| Requirement and boundary scope | Owning milestone or evidence |
| --- | --- |
| R23-R29; BND-INPUT-001, BND-RECOVERY-001, BND-COMPAT-001, BND-ENV-001; INT-005 | M1 semantic/literal inventories, scenarios, negative fixtures, and baseline measurement |
| R1-R22, R31; BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001; INT-001-INT-004 | M2 universal skill, conditional reference, exact loads, authority boundaries, and focused validation |
| R27-R31, R33; BND-COMPOSE-001, BND-RECOVERY-001, BND-COMPAT-001, BND-ENV-001; INT-005-INT-006 | M3 profile measurement, semantic preservation, and generated/archive/installed proof |
| R32 | Completed `architecture-not-required` assessment before this plan |

## Milestones

### M1. Freeze verify rule and literal ownership

- Milestone type: implementation.
- Goal: Account for every behaviorally significant rule and compatibility-sensitive literal, and establish deterministic static scenarios before moving prose.
- Requirements: R23-R29; BND-INPUT-001; BND-RECOVERY-001; BND-COMPAT-001; BND-ENV-001; INT-005.
- Files/components likely touched:
  - `docs/changes/2026-08-11-verify-skill-simplification/verify-rule-disposition.yaml`
  - `docs/changes/2026-08-11-verify-skill-simplification/verify-literal-compatibility.yaml`
  - `docs/changes/2026-08-11-verify-skill-simplification/fixtures/`
  - `docs/changes/2026-08-11-verify-skill-simplification/evidence/profile-size-baseline.md`
- Dependencies:
  - approved spec, clean spec review, and recorded architecture assessment
  - complete current `skills/verify/` package and exact literal consumers
- Tests to add/update:
  - static scenarios for scoped evidence types, direct and governed final readiness, ambiguous/cross-target/stale identity, release applicability, exact resource profiles, missing resources, isolated write prohibition, governed handoff, and boundary-first additive loading
  - unknown semantic disposition and literal classification fixtures
  - required fields, unique IDs, exact closed vocabulary, and non-empty required/forbidden scenario outcomes
- Implementation steps:
  - inventory significant rules and duplicate clusters with stable IDs, sources, behavior, requirements, profiles, disposition, destination, and preservation proof
  - inventory exact-string consumers separately as normative, parser/package, incidental-test, or obsolete
  - serialize ledgers and fixtures as JSON-compatible YAML and prove unknown values fail before consistency checks
  - record LF-normalized baseline words, bytes, resource identities, all four profiles, and total package
  - route any proposed obsolete semantic rule without an approved contract change to the spec owner
- Validation commands:
  - run the exact `M1 change-local ledger and fixture proof` command below
  - `python scripts/validate-change-metadata.py docs/changes/2026-08-11-verify-skill-simplification/change.yaml`
  - independently inspect coverage against the complete current skill and literal consumers
- Expected observable result: every current rule and literal has one closed treatment, all required scenarios exist, unknown values fail closed, and canonical skill prose has not moved.
- Commit message: `M1: freeze verify rule and literal ownership`
- Milestone closeout: focused proof and implementation evidence, then independent code review and resolution when required.
- Risks:
  - similar passages may encode distinct behavior
  - an incidental assertion may be mistaken for a normative contract
- Rollback/recovery:
  - revert M1 evidence; canonical skill files remain unchanged

### M2. Separate scoped and final-readiness procedure

- Milestone type: implementation.
- Goal: Make `SKILL.md` a shorter self-sufficient scoped-verification contract and move only final-readiness procedure into one exact mapped reference.
- Requirements: R1-R22, R31; BND-INPUT-001; BND-STATE-001; BND-AUTH-001; BND-COMPOSE-001; BND-TEMPORAL-001; BND-RECOVERY-001; INT-001-INT-004.
- Files/components likely touched:
  - `skills/verify/SKILL.md`
  - `skills/verify/references/branch-readiness-verification.md`
  - `scripts/test-skill-validator.py`
  - literal consumers classified for atomic migration in M1
- Dependencies:
  - M1 evidence and code review are complete
- Tests to add/update:
  - exact three-outcome classification and target-resolution stops
  - four exact resource profiles and independent two-mode authority
  - required and forbidden reference loads, including boundary-first additive cases
  - isolated no-write/no-PR behavior and governed verify/workflow/pr ownership
  - inline item-level semantics for CI, generated output, manual proof, commands, and release metadata
  - branch-reference final applicability/aggregation ownership and missing-resource failure
  - normalized structure, claims, stop conditions, output fields, and absence of unfilled placeholders
- Implementation steps:
  - add failing focused assertions to existing skill validation before changing package text
  - consolidate universal repetition according to the semantic ledger while retaining every R3 and R17-R22 rule inline
  - create the branch-readiness reference and move only R18 procedure
  - replace the long boundary-first bridge with a compact trigger that still maps the unchanged reference
  - migrate real literal consumers atomically, update incidental tests, and finalize ledger destinations
- Validation commands:
  - `python scripts/validate-skills.py skills/verify/SKILL.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-build-skills.py`
  - `python scripts/build-skills.py --check`
- Expected observable result: scoped verification is complete from a shorter `SKILL.md`; final outcomes load one coherent reference; boundary-first remains additive; no shared procedure leaks authority.
- Commit message: `M2: simplify verify package paths`
- Milestone closeout: focused package proof and implementation evidence, then independent code review and resolution when required.
- Risks:
  - a universal blocker or evidence meaning could move behind the final trigger
  - shared final procedure could leak governed writes into isolated use
  - exact-string migration could weaken a real parser contract
- Rollback/recovery:
  - restore the prior complete canonical package and focused assertions together, then regenerate derived packages

### M3. Prove profile reduction and package parity

- Milestone type: implementation.
- Goal: Prove profile-specific context reduction, semantic preservation, and canonical-through-installed package integrity.
- Requirements: R27-R31, R33; BND-COMPOSE-001; BND-RECOVERY-001; BND-COMPAT-001; BND-ENV-001; INT-005-INT-006.
- Files/components likely touched:
  - `scripts/test-adapter-distribution.py` only if existing focused selection cannot prove `verify`
  - existing adapter fixtures only where focused coverage is absent
  - `docs/changes/2026-08-11-verify-skill-simplification/evidence/simplification-measurements.md`
  - `docs/changes/2026-08-11-verify-skill-simplification/evidence/semantic-preservation-review.md`
  - `docs/changes/2026-08-11-verify-skill-simplification/evidence/m3-package-proof.md`
- Dependencies:
  - M2 package refactor and code review are complete
- Tests to add/update:
  - supported generated, archived, and temporary installed targets contain both references at identical paths and bytes
  - missing, escaped, transformed, stale, or mixed resources fail package proof
  - all four profile assemblies count each LF-normalized unique resource once in documented order
  - no acceptance command starts or grades a target agent
- Implementation steps:
  - extend only existing adapter-distribution proof where direct `verify` selection is absent
  - generate supported packages in a temporary directory and validate archive and clean-install resource parity
  - report before/after `SKILL.md`, each resource, VP0, VP0B, VP1, VP1B, total package, duplicate clusters, inline templates, and mapped-resource counts in words and bytes
  - require material VP0 improvement, explain final-profile and total-package deltas, and keep token evidence optional and pinned
  - independently review the complete package against both ledgers and R31
- Validation commands:
  - `python scripts/test-adapter-distribution.py`
  - `python -c 'exec("""import subprocess, sys, tempfile\nversion = "v0.3.6"\nwith tempfile.TemporaryDirectory(prefix="rigorloop-adapters-") as output:\n    subprocess.run([sys.executable, "scripts/build-adapters.py", "--version", version, "--output-dir", output], check=True)\n    subprocess.run([sys.executable, "scripts/validate-adapters.py", "--version", version, "--adapter-root", output, "--clean-install-smoke", "--skill", "verify"], check=True)""")'`
  - `python scripts/validate-skills.py skills/verify/SKILL.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-boundary-first.py --check --path specs/verify-skill-simplification.md`
- Expected observable result: scoped profiles materially shrink, final profiles have no unjustified growth, semantics remain complete, and every supported package contains byte-identical mapped resources without target-runtime execution.
- Commit message: `M3: prove verify simplification`
- Milestone closeout: package/evidence proof, independent code review, and resolution before final lifecycle closeout.
- Risks:
  - generic adapter tests may pass without selecting `verify`
  - main-file reduction may hide final-profile or total-package growth
  - partial packaging may mix old and new ownership
- Rollback/recovery:
  - restore the prior complete canonical package, regenerate every derived target, and discard temporary package trees

## Validation plan

### M1 change-local ledger and fixture proof

The ledgers and fixtures use JSON serialization, which is valid YAML.
This standard-library command rejects unknown closed values before destination consistency and validates every required scenario identity.

```bash
python -c 'import json; from pathlib import Path; root=Path("docs/changes/2026-08-11-verify-skill-simplification"); rules=json.loads((root/"verify-rule-disposition.yaml").read_text())["rules"]; literals=json.loads((root/"verify-literal-compatibility.yaml").read_text())["literals"]; scenarios=json.loads((root/"fixtures/scenario-contracts.yaml").read_text())["scenarios"]; bad_rule=json.loads((root/"fixtures/invalid-rule-disposition.yaml").read_text()); bad_literal=json.loads((root/"fixtures/invalid-literal-classification.yaml").read_text()); rd={"retained-inline","retained-branch-readiness-reference","retained-boundary-reference","removed-duplicate","removed-obsolete-with-approved-contract-change"}; lc={"normative-contract","parser-or-package-contract","test-only-incidental","obsolete"}; rf={"rule_id","source_locations","behavior","governing_requirements","applicable_profiles","disposition","destination","preservation_proof"}; lf={"literal_id","literal","source_location","consumers","classification","required_semantics","disposition","replacement"}; dest=lambda row: (row["disposition"] == "retained-inline" and row["destination"].startswith("skills/verify/SKILL.md")) or (row["disposition"] == "retained-branch-readiness-reference" and row["destination"].startswith("skills/verify/references/branch-readiness-verification.md")) or (row["disposition"] == "retained-boundary-reference" and row["destination"].startswith("skills/verify/references/boundary-first-method-v1.md")) or (row["disposition"] == "removed-duplicate" and row["destination"].startswith("skills/verify/")) or (row["disposition"] == "removed-obsolete-with-approved-contract-change" and row["destination"].startswith(("specs/","docs/"))); vr=lambda row: ["unknown-disposition"] if row.get("disposition") not in rd else (["missing-required-fields"] if not rf <= row.keys() else (["empty-required-fields"] if not all(row[field] for field in rf) else (["destination-inconsistent"] if not dest(row) else []))); vl=lambda row: ["unknown-classification"] if row.get("classification") not in lc else (["missing-required-fields"] if not lf <= row.keys() else (["empty-required-fields"] if not all(row[field] for field in lf) else [])); expected={"scoped-command","scoped-ci","scoped-generated-output","scoped-manual-proof","scoped-release-metadata","direct-branch-readiness","governed-final-verification","ambiguous-target","cross-target-evidence","informal-final-wording","release-sensitive","missing-branch-reference","boundary-additive-scoped","boundary-additive-final","isolated-write-prohibition","governed-handoff","stale-evidence"}; assert rules and literals; assert all(vr(row) == [] for row in rules); assert all(vl(row) == [] for row in literals); assert vr(bad_rule)[0] == "unknown-disposition"; assert vl(bad_literal)[0] == "unknown-classification"; assert len({row["rule_id"] for row in rules}) == len(rules); assert len({row["literal_id"] for row in literals}) == len(literals); assert {row["scenario"] for row in scenarios} == expected; assert all(row.get("required") and row.get("forbidden") for row in scenarios); print(f"rules={len(rules)} literals={len(literals)} scenarios={len(scenarios)} unknown_values=rejected-first")'
```

- `python scripts/validate-skills.py skills/verify/SKILL.md`: normalized structure, Resource-map syntax, containment, placeholders, and narrow claim checks.
- `python scripts/test-skill-validator.py`: focused skill-contract and regression proof.
- `python scripts/test-build-skills.py` and `python scripts/build-skills.py --check`: generated skill inventory and resource parity.
- `python scripts/test-adapter-distribution.py`: adapter generation, archive, resource, and clean-install regression proof.
- Temporary adapter build plus `validate-adapters.py --clean-install-smoke --skill verify`: direct all-target archive and installed-tree proof.
- `python scripts/validate-boundary-first.py --check --path specs/verify-skill-simplification.md`: final boundary-to-proof coverage through the matching test spec.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-11-verify-skill-simplification/change.yaml`: lifecycle and planned-work consistency.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-08-11-verify-skill-simplification`: formal review structure.
- Independent semantic review: outcome/target classification, universal completeness, item semantics, reference ownership, resource profiles, execution authority, stops, claims, recording, handoff, and literal treatment.

## Risks and recovery

- Risk: conditional extraction hides universal evidence or blocker behavior.
  - Recovery: rule ledger, scoped fixtures, focused assertions, and semantic review block the move; restore the prior package atomically.
- Risk: direct and governed final readiness share resources and accidentally share authority.
  - Recovery: classify execution mode separately and prove every forbidden write and handoff.
- Risk: incidental literal tests become policy owners.
  - Recovery: classify literal consumers separately and migrate only real contracts atomically.
- Risk: relocation is reported as deletion or a misleading percentage win.
  - Recovery: report every profile and total package words/bytes, with semantic preservation taking precedence.
- Risk: one package target omits the new reference.
  - Recovery: block acceptance on selected archive and temporary installed-tree parity, then regenerate from the last complete canonical revision.

## Dependencies

- Accepted proposal, approved spec, clean formal reviews, closed prior finding resolution, and recorded `architecture-not-required` assessment.
- Existing boundary-first reference and published-skill resource/package architecture.
- Existing skill validation, adapter generation, archive validation, and clean-install resource owners.
- Approved test specification and test-spec review before implementation.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-11 | Use three implementation milestones: preservation evidence, package refactor, and profile/package proof. | Each slice has an independent failure, review, and rollback boundary. | One large prose-and-package rewrite. |
| 2026-08-11 | Keep semantic and literal inventories separate and validate both before prose movement. | Behavior preservation and exact-string compatibility are different contracts. | One combined ledger; preserve every asserted phrase. |
| 2026-08-11 | Keep resource loading independent of execution authority. | Direct and governed final readiness can share procedure without sharing writes. | Duplicate references or authority-coupled packages. |
| 2026-08-11 | Extend only existing skill and adapter validators for durable proof. | The contract excludes a permanent simplification validator. | New CLI, tokenizer, or runtime journey gate. |
| 2026-08-11 | Measure four profiles and total package words/bytes. | Main-file size alone can hide final-profile or relocation cost. | A normative percentage threshold. |

## Readiness

- See the owning change record for current workflow state.
- Readiness is not Done; plan review, test-spec authoring and review, implementation/code-review milestones, explanation, verification, and PR handoff remain.
