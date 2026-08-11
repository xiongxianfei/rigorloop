# Test-Spec-Review Skill Simplification Execution Plan

## Purpose / big picture

Simplify the published `test-spec-review` package without weakening proof-map judgment, durable review recording, formal settlement, or implementation-handoff authority.
The work first freezes semantic and literal ownership, then separates the universal advisory path from conditional recording and settlement procedure, and finally proves assembly reduction and package integrity.

## Current Handoff Summary

- Owning change record: `docs/changes/2026-08-11-test-spec-review-skill-simplification/change.yaml`

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: `docs/proposals/2026-08-11-test-spec-review-skill-simplification.md`
- Spec: `specs/test-spec-review-skill-simplification.md`
- Architecture: not required; recorded in `docs/changes/2026-08-11-test-spec-review-skill-simplification/architecture-assessment.md`
- Test spec: pending at `specs/test-spec-review-skill-simplification.test.md`

## Context and orientation

`skills/test-spec-review/` is the only authored package source.
The current package contains `SKILL.md`, two mapped boundary-first references, and two mapped structural assets.
This change adds `references/test-spec-review-recording-and-settlement.md`, keeps lifecycle and handoff classification, boundary applicability, durable-recording triggers, proof semantics, findings, statuses, stops, claims, and bounded handoff inline, and moves only durable-recording mechanics and formal-only settlement procedure.

`scripts/skill_validation.py`, `scripts/validate-skills.py`, and `scripts/test-skill-validator.py` own canonical skill and mapped-resource proof.
`scripts/adapter_distribution.py`, adapter generation and validation commands, and `scripts/test-adapter-distribution.py` own generated, archived, and temporary installed-tree proof.
Existing owners are extended only where focused `test-spec-review` coverage is absent.

Semantic-rule, literal-compatibility, static-scenario, and measurement artifacts are change-local evidence, not permanent policy or a new validator family.

## Non-goals

- Change proof adequacy, review statuses, recording triggers, formal settlement, staleness, implementation eligibility, claim, output, or handoff semantics.
- Change workflow stages, `change.yaml`, planned-work state, downstream implementation authority, adapter roots, or publication behavior.
- Add another result asset, multiple recording fragments, a runtime reviewer, target-agent execution, prompt journeys, or transcript grading.
- Add permanent simplicity, token, word, line, prose-quality, scenario-framework, selector, or scheduler machinery.
- Hand-edit generated adapters or installed runtime copies.
- Treat the advisory 30-40 percent reduction as a semantic gate.

## Requirements covered

| Requirement and boundary scope | Owning milestone or evidence |
| --- | --- |
| R25-R30, R35, R38; BND-INPUT-001, BND-RECOVERY-001, BND-COMPAT-001, BND-ENV-001; INT-005-INT-006 | M1 semantic/literal inventories, scenarios, negative fixtures, and baseline measurement |
| R1-R24, R34-R35, R38-R39; BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001; INT-001-INT-005 | M2 universal skill, recording reference, exact overlays, authority boundaries, and focused validation |
| R29-R33, R37-R38; BND-COMPOSE-001, BND-RECOVERY-001, BND-COMPAT-001, BND-ENV-001; INT-005-INT-007 | M3 assembly measurement, semantic preservation, and generated/archive/installed proof |
| R36 | Completed `architecture-not-required` assessment before this plan |

## Milestones

### M1. Freeze test-spec-review rule and literal ownership

- Milestone type: implementation.
- Goal: Account for every behaviorally significant rule and compatibility-sensitive literal, and establish deterministic static scenarios before moving prose.
- Requirements: R25-R30, R35, R38; BND-INPUT-001; BND-RECOVERY-001; BND-COMPAT-001; BND-ENV-001; INT-005-INT-006.
- Files/components likely touched:
  - `docs/changes/2026-08-11-test-spec-review-skill-simplification/test-spec-review-rule-disposition.yaml`
  - `docs/changes/2026-08-11-test-spec-review-skill-simplification/test-spec-review-literal-compatibility.yaml`
  - `docs/changes/2026-08-11-test-spec-review-skill-simplification/fixtures/`
  - `docs/changes/2026-08-11-test-spec-review-skill-simplification/evidence/profile-size-baseline.md`
- Dependencies:
  - approved spec, clean spec review, and recorded architecture assessment
  - complete current `skills/test-spec-review/` package and exact literal consumers
- Tests to add/update:
  - static scenarios for advisory clean review, explicit recording, late material recording, formal isolated review, workflow-managed formal review, invalid advisory workflow handoff, boundary-additive assemblies, stale identity, missing resources, settlement isolation, and blocked recording
  - unknown semantic disposition and literal classification fixtures
  - required fields, unique IDs, exact closed vocabulary, and non-empty required and forbidden scenario outcomes
- Implementation steps:
  - inventory significant rules and duplicate clusters with stable IDs, sources, behavior, requirements, assemblies, disposition, destination, and preservation proof
  - inventory exact-string consumers separately as normative, parser/package, incidental-test, or obsolete
  - serialize ledgers and fixtures as JSON-compatible YAML and prove unknown values fail before consistency checks
  - record LF-normalized baseline words, bytes, resource identities, all four base assemblies, the recording overlay, and total package
  - route any proposed obsolete semantic rule without an approved contract change to the spec owner
- Validation commands:
  - run the exact `M1 change-local ledger and fixture proof` command below
  - `python scripts/validate-change-metadata.py docs/changes/2026-08-11-test-spec-review-skill-simplification/change.yaml`
  - independently inspect coverage against the complete current skill and literal consumers
- Expected observable result: every current rule and literal has one closed treatment, all required scenarios exist, unknown values fail closed, and canonical skill prose has not moved.
- Commit message: `M1: freeze test-spec-review rule and literal ownership`
- Milestone closeout: focused proof and implementation evidence, then independent code review and resolution when required.
- Risks:
  - similar passages may encode distinct review or settlement behavior
  - an incidental assertion may be mistaken for a normative contract
- Rollback/recovery:
  - revert M1 evidence; canonical skill files remain unchanged

### M2. Separate universal review from recording and settlement procedure

- Milestone type: implementation.
- Goal: Make `SKILL.md` a shorter self-sufficient advisory review contract and move only durable-recording mechanics and formal-only settlement into one exact mapped reference.
- Requirements: R1-R24, R34-R35, R38-R39; BND-INPUT-001; BND-STATE-001; BND-AUTH-001; BND-COMPOSE-001; BND-TEMPORAL-001; BND-RECOVERY-001; INT-001-INT-005.
- Files/components likely touched:
  - `skills/test-spec-review/SKILL.md`
  - `skills/test-spec-review/references/test-spec-review-recording-and-settlement.md`
  - `scripts/test-skill-validator.py`
  - literal consumers classified for atomic migration in M1
- Dependencies:
  - M1 evidence and code review are complete
- Tests to add/update:
  - exact lifecycle and handoff classification, including all three valid pairs and the invalid advisory workflow-managed pair
  - four base assemblies, late recording-overlay activation, and boundary-first additive loading
  - shared recording versus formal-only settlement ownership and advisory no-settlement behavior
  - formal isolated settlement without automatic continuation and workflow-managed return to workflow
  - missing reference, result asset, finding asset, boundary resource, escaped path, and mixed-version failure
  - normalized structure, closed statuses, staleness, claims, result fields, finding multiplicity, and absence of unfilled placeholders
- Implementation steps:
  - add failing focused assertions to existing skill validation before changing package text
  - consolidate universal repetition according to the semantic ledger while retaining every R2-R8 and R17-R24 rule inline
  - create the recording-and-settlement reference with visibly separate shared-recording and formal-only sections
  - retain both unchanged boundary references and the two structural assets under their existing ownership
  - migrate real literal consumers atomically, update incidental tests, and finalize ledger destinations
- Validation commands:
  - `python scripts/validate-skills.py skills/test-spec-review/SKILL.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-build-skills.py`
  - `python scripts/build-skills.py --check`
- Expected observable result: advisory review is complete from a shorter `SKILL.md`; recording loads only from exact triggers; formal settlement cannot leak into advisory or isolated handoff authority; boundary guidance remains independently additive.
- Commit message: `M2: simplify test-spec-review package paths`
- Milestone closeout: focused package proof and implementation evidence, then independent code review and resolution when required.
- Risks:
  - a universal proof rule or blocker could move behind the recording trigger
  - late overlay loading could accidentally upgrade lifecycle or handoff authority
  - exact-string migration could weaken a real parser contract
- Rollback/recovery:
  - restore the prior complete canonical package and focused assertions together, then regenerate derived packages

### M3. Prove assembly reduction and package parity

- Milestone type: implementation.
- Goal: Prove assembly-specific context reduction, semantic preservation, and canonical-through-installed package integrity.
- Requirements: R29-R33, R37-R38; BND-COMPOSE-001; BND-RECOVERY-001; BND-COMPAT-001; BND-ENV-001; INT-005-INT-007.
- Files/components likely touched:
  - `scripts/test-adapter-distribution.py` only if existing focused selection cannot prove `test-spec-review`
  - existing adapter fixtures only where focused coverage is absent
  - `docs/changes/2026-08-11-test-spec-review-skill-simplification/evidence/simplification-measurements.md`
  - `docs/changes/2026-08-11-test-spec-review-skill-simplification/evidence/semantic-preservation-review.md`
  - `docs/changes/2026-08-11-test-spec-review-skill-simplification/evidence/m3-package-proof.md`
- Dependencies:
  - M2 package refactor and code review are complete
- Tests to add/update:
  - supported generated, archived, and temporary installed targets contain the new reference, both boundary references, and both assets at identical paths and bytes
  - missing, escaped, transformed, stale, or mixed resources fail package proof
  - all four base assemblies and the recording overlay count each LF-normalized unique resource once in documented order
  - no acceptance command starts or grades a target agent
- Implementation steps:
  - extend only existing adapter-distribution proof where direct `test-spec-review` selection is absent
  - generate supported packages in a temporary directory and validate archive and clean-install resource parity
  - report before and after `SKILL.md`, each resource, TSR0, TSR0B, TSR1, TSR1B, overlay, total package, duplicate clusters, inline templates, and mapped-resource counts in words and bytes
  - require material ordinary-path improvement, explain formal-profile and total-package deltas, and keep token evidence optional and pinned
  - independently review the complete package against both ledgers and R38
- Validation commands:
  - `python scripts/test-adapter-distribution.py`
  - `python -c 'exec("""import subprocess, sys, tempfile\nversion = "v0.3.6"\nwith tempfile.TemporaryDirectory(prefix="rigorloop-adapters-") as output:\n    subprocess.run([sys.executable, "scripts/build-adapters.py", "--version", version, "--output-dir", output], check=True)\n    subprocess.run([sys.executable, "scripts/validate-adapters.py", "--version", version, "--adapter-root", output, "--clean-install-smoke", "--skill", "test-spec-review"], check=True)""")'`
  - `python scripts/validate-skills.py skills/test-spec-review/SKILL.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-boundary-first.py --check --path specs/test-spec-review-skill-simplification.md`
- Expected observable result: ordinary assemblies materially shrink, formal assemblies have no unjustified growth, semantics remain complete, and every supported package contains byte-identical mapped resources without target-runtime execution.
- Commit message: `M3: prove test-spec-review simplification`
- Milestone closeout: package and evidence proof, independent code review, and resolution before final lifecycle closeout.
- Risks:
  - generic adapter tests may pass without selecting `test-spec-review`
  - main-file reduction may hide formal-profile or total-package growth
  - partial packaging may mix old and new ownership
- Rollback/recovery:
  - restore the prior complete canonical package, regenerate every derived target, and discard temporary package trees

## Validation plan

### M1 change-local ledger and fixture proof

The ledgers and fixtures use JSON serialization, which is valid YAML.
This standard-library command rejects unknown closed values before destination consistency and validates every required scenario identity.

```bash
python -c 'import json; from pathlib import Path; root=Path("docs/changes/2026-08-11-test-spec-review-skill-simplification"); rules=json.loads((root/"test-spec-review-rule-disposition.yaml").read_text())["rules"]; literals=json.loads((root/"test-spec-review-literal-compatibility.yaml").read_text())["literals"]; scenarios=json.loads((root/"fixtures/scenario-contracts.yaml").read_text())["scenarios"]; bad_rule=json.loads((root/"fixtures/invalid-rule-disposition.yaml").read_text()); bad_literal=json.loads((root/"fixtures/invalid-literal-classification.yaml").read_text()); rd={"retained-inline","retained-recording-reference","retained-boundary-reference","asset-owned","removed-duplicate","removed-obsolete-with-approved-contract-change"}; lc={"normative-contract","parser-or-package-contract","test-only-incidental","obsolete"}; rf={"rule_id","source_locations","behavior","governing_requirements","applicable_assemblies","disposition","destination","preservation_proof"}; lf={"literal_id","literal","source_location","consumers","classification","required_semantics","disposition","replacement"}; dest=lambda row: (row["disposition"] == "retained-inline" and row["destination"].startswith("skills/test-spec-review/SKILL.md")) or (row["disposition"] == "retained-recording-reference" and row["destination"].startswith("skills/test-spec-review/references/test-spec-review-recording-and-settlement.md")) or (row["disposition"] == "retained-boundary-reference" and row["destination"].startswith("skills/test-spec-review/references/boundary-first-")) or (row["disposition"] == "asset-owned" and row["destination"].startswith("skills/test-spec-review/assets/")) or (row["disposition"] == "removed-duplicate" and row["destination"].startswith("skills/test-spec-review/")) or (row["disposition"] == "removed-obsolete-with-approved-contract-change" and row["destination"].startswith(("specs/","docs/"))); vr=lambda row: ["unknown-disposition"] if row.get("disposition") not in rd else (["missing-required-fields"] if not rf <= row.keys() else (["empty-required-fields"] if not all(row[field] for field in rf) else (["destination-inconsistent"] if not dest(row) else []))); vl=lambda row: ["unknown-classification"] if row.get("classification") not in lc else (["missing-required-fields"] if not lf <= row.keys() else (["empty-required-fields"] if not all(row[field] for field in lf) else [])); expected={"advisory-clean-isolated","advisory-explicit-recording","advisory-material-late-overlay","formal-isolated","formal-workflow-managed","advisory-workflow-managed-invalid","boundary-advisory","boundary-formal","missing-recording-reference","missing-result-asset","missing-finding-asset","missing-boundary-resource","stale-formal-target","formal-settlement-isolation","blocked-recording","unknown-review-status"}; assert rules and literals; assert all(vr(row) == [] for row in rules); assert all(vl(row) == [] for row in literals); assert vr(bad_rule)[0] == "unknown-disposition"; assert vl(bad_literal)[0] == "unknown-classification"; assert len({row["rule_id"] for row in rules}) == len(rules); assert len({row["literal_id"] for row in literals}) == len(literals); assert {row["scenario"] for row in scenarios} == expected; assert all(row.get("required") and row.get("forbidden") for row in scenarios); print(f"rules={len(rules)} literals={len(literals)} scenarios={len(scenarios)} unknown_values=rejected-first")'
```

- `python scripts/validate-skills.py skills/test-spec-review/SKILL.md`: normalized structure, Resource-map syntax, containment, placeholders, and narrow claim checks.
- `python scripts/test-skill-validator.py`: focused skill-contract and regression proof.
- `python scripts/test-build-skills.py` and `python scripts/build-skills.py --check`: generated skill inventory and resource parity.
- `python scripts/test-adapter-distribution.py`: adapter generation, archive, resource, and clean-install regression proof.
- Temporary adapter build plus `validate-adapters.py --clean-install-smoke --skill test-spec-review`: direct all-target archive and installed-tree proof.
- `python scripts/validate-boundary-first.py --check --path specs/test-spec-review-skill-simplification.md`: final boundary-to-proof coverage through the matching test spec.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-11-test-spec-review-skill-simplification/change.yaml`: lifecycle and planned-work consistency.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-08-11-test-spec-review-skill-simplification`: formal review structure.
- Independent semantic review: lifecycle and handoff classification, universal proof completeness, overlay triggers, formal-only settlement, resource assemblies, stops, claims, recording, handoff, and literal treatment.

## Risks and recovery

- Risk: conditional extraction hides universal proof, status, or blocker behavior.
  - Recovery: rule ledger, advisory fixtures, focused assertions, and semantic review block the move; restore the prior package atomically.
- Risk: late recording procedure accidentally grants formal settlement or workflow continuation.
  - Recovery: classify lifecycle and handoff independently and prove recording changes neither authority value.
- Risk: incidental literal tests become policy owners.
  - Recovery: classify literal consumers separately and migrate only real contracts atomically.
- Risk: relocation is reported as deletion or a misleading percentage win.
  - Recovery: report every assembly, overlay, and total package words and bytes, with semantic preservation taking precedence.
- Risk: one package target omits the new reference or an existing asset.
  - Recovery: block acceptance on selected archive and temporary installed-tree parity, then regenerate from the last complete canonical revision.

## Dependencies

- Accepted proposal, approved spec, clean formal reviews, closed prior finding resolution, and recorded `architecture-not-required` assessment.
- Existing boundary-first references and published-skill resource and package architecture.
- Existing skill validation, adapter generation, archive validation, and clean-install resource owners.
- Approved test specification and test-spec review before implementation.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-11 | Use three implementation milestones: preservation evidence, package refactor, and assembly and package proof. | Each slice has an independent failure, review, and rollback boundary. | One large prose-and-package rewrite. |
| 2026-08-11 | Keep semantic and literal inventories separate and validate both before prose movement. | Behavior preservation and exact-string compatibility are different contracts. | One combined ledger; preserve every asserted phrase. |
| 2026-08-11 | Treat recording as a late additive overlay and settlement as a formal-only subsection. | Material advisory findings need durable evidence without acquiring lifecycle authority. | Formal-only reference; inline all recording procedure. |
| 2026-08-11 | Extend only existing skill and adapter validators for durable proof. | The contract excludes a permanent simplification validator. | New CLI, tokenizer, or runtime journey gate. |
| 2026-08-11 | Measure four base assemblies, the overlay, and total package words and bytes. | Main-file size alone can hide formal-profile or relocation cost. | A normative percentage threshold. |

## Readiness

- See the owning change record for current workflow state.
- Readiness is not Done; plan review, test-spec authoring and review, implementation and code-review milestones, explanation, verification, and PR handoff remain.
