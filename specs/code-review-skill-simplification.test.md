<!-- Template: test-spec-skeleton-v1 -->
<!-- Skill: test-spec -->
<!-- Template status: normative -->

# Code-Review Skill Simplification Test Spec

## Owning change record

`docs/changes/2026-08-10-code-review-skill-simplification/change.yaml`

boundary_contract: boundary-first-v1

## Related spec and plan

- Spec: `specs/code-review-skill-simplification.md`
- Plan: `docs/plans/2026-08-10-code-review-skill-simplification.md`
- Architecture: `docs/architecture/system/architecture.md`
- Relevant ADRs: `docs/adr/ADR-20260623-published-skill-resource-integrity.md`; `docs/adr/ADR-20260810-published-skill-first-validation-architecture.md`

## Input artifact identities

| Input | Path | Artifact ID | Review evidence |
| --- | --- | --- | --- |
| Feature spec | `specs/code-review-skill-simplification.md` | `spec` | `spec-review-r2`; `docs/changes/2026-08-10-code-review-skill-simplification/reviews/spec-review-r2.md` |
| Architecture | `docs/architecture/system/architecture.md` | `architecture` | `architecture-review-r2`; `docs/changes/2026-08-10-code-review-skill-simplification/reviews/architecture-review-r2.md` |
| Execution plan | `docs/plans/2026-08-10-code-review-skill-simplification.md` | `plan` | `plan-review-r2`; `docs/changes/2026-08-10-code-review-skill-simplification/reviews/plan-review-r2.md` |

## Testing strategy

Contract tests over JSON-compatible YAML prove the change-local rule ledger, closed dispositions, scenario identities, and required/forbidden outcomes without introducing a validator file. Existing skill unit and integration suites prove canonical structure, exact resource mapping, inline and conditional ownership, assets, vocabulary preservation, and missing-resource failures.

Existing adapter integration and end-to-end filesystem proof generate Codex, Claude Code, and opencode packages, validate archives, materialize every supported target into an empty temporary tree, and compare mapped-resource inventory, relative paths, and raw bytes. No test starts a target-agent runtime, sends a prompt, grades a transcript, requires network access, or retries nondeterministic work.

Manual procedure MP1 owns semantic preservation because clarity, completeness, policy ownership, and useful handoff cannot be reduced to structural assertions. Migration and rollback cases compare the old complete package with the new complete package and reject mixed versions.

Scenarios cover distinct outcomes and composed hazards; no Cartesian product of review modes, rules, targets, and package states is required.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1 | T2, T3, T4, T6, T7, MP1 | contract, integration, manual | Complete package with one semantic owner. |
| R2 | T2, T9, MP1 | contract, manual | Direct and isolated review remains complete from `SKILL.md`. |
| R3 | T2, T5, MP1 | contract, manual | Every universal inline contract is checked. |
| R4 | T2, T3, T6 | integration | Exact path, `READ`, and armed load condition. |
| R5 | T3, MP1 | contract, manual | Conditional content is limited to the allowed automation procedure. |
| R6 | T3, T5, MP1 | contract, manual | Forbidden universal policy remains outside the reference. |
| R7 | T4, T6, MP1 | contract, manual | Assets alone own repeated structure and no policy. |
| R8 | T1, MP1 | contract, manual | Every rule has stable identity, fields, and destination. |
| R9 | T1 | unit | Closed vocabulary is checked before consistency. |
| R10 | T1, T12, MP1 | contract, manual | No rule disappears or uses obsolete removal without authority. |
| R11 | T1, T2, T3, T4, T11 | contract | Every named duplication cluster has one owner. |
| R12 | T1, T11, T12, MP1 | contract, manual | Ledger, ownership, reduction, and package accounting all apply. |
| R13 | T11, T12, MP1 | contract, manual | Percentage is non-normative; no material reduction fails. |
| R14 | T11 | contract | All required before/after measurements are present and separate. |
| R15 | T1, T9, T10, T12 | contract | Exactly three proof classes are used. |
| R16 | T9 | contract | Seven fixture scenarios carry required and forbidden outcomes. |
| R17 | T12, MP1 | manual | Semantic review covers the complete eleven-part checklist. |
| R18 | T10 | integration | Command graph and evidence exclude target-agent execution. |
| R19 | T6, T7, T8 | integration | Existing skill and adapter owners retain deterministic scope. |
| R20 | T10, T16 | contract | No prohibited validator or runtime subsystem is added. |
| R21 | T6, T7 | integration, e2e | Canonical through temporary installed targets preserve resources and bytes. |
| R22 | T6, T8 | integration | Missing, escaping, unfilled, stale, or undeclared resources fail actionably. |
| R23 | T5, T15, MP1 | contract, migration, manual | Native review and historical evidence semantics remain unchanged. |
| R24 | T14 | contract | Architecture assessment and review settlement are recorded. |
| R25 | T7, T13, T15 | e2e, migration | Package rollout and rollback remain complete and atomic. |

## Acceptance criterion coverage map

| Acceptance criterion | Covered by | Level | Notes |
| --- | --- | --- | --- |
| AC1 | T1, MP1 | contract, manual | Complete ledger accounting. |
| AC2 | T2, T3, T5 | contract | Universal policy remains inline. |
| AC3 | T3, T6 | integration | Exactly one conditional reference with allowed content. |
| AC4 | T2, T9 | contract | Direct and isolated modes do not load automation detail. |
| AC5 | T4 | contract | Assets exclusively own structure. |
| AC6 | T1, T11, T12 | contract, manual | Clusters consolidate and common path shrinks materially. |
| AC7 | T11 | contract | Metrics are reported separately. |
| AC8 | T9 | contract | Seven fixture classes with required/forbidden outcomes. |
| AC9 | T12, MP1 | manual | Complete semantic review. |
| AC10 | T10 | integration | No target-agent acceptance execution. |
| AC11 | T6-T8, T16 | integration | Existing deterministic owners only. |
| AC12 | T5, T15 | migration | Native semantics and evidence remain compatible. |
| AC13 | T14 | contract | Architecture applicability resolved. |
| AC14 | T7, T13 | e2e, migration | Atomic complete-package rollout and rollback. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | T2, T9 | Direct review remains inline-only. |
| E2 | T3, T9 | Armed automation loads exactly one reference. |
| E3 | T8 | Missing or stale conditional reference fails package integrity. |
| E4 | T1 | Unknown ledger disposition fails before consistency. |
| E5 | T11, T12 | A justified result below 35 percent may pass. |
| E6 | T10 | Runtime execution is rejected as proof. |
| E7 | T4 | Output structures remain asset-owned. |

## Proof map

Boundary model version: boundary-first-v1

Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25

| Proof obligation ID | Coverage state | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Proof level | Automation mode | Command IDs | Evidence artifact | Required milestone | Manual procedure IDs | Uncovered gap ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRF-001 | covered | R2, R4, R8, R9, R15, R16 | BND-INPUT-001 | T1, T2, T9 | contract | automated | CMD1, CMD2, CMD3 | M1 and M2 evidence | M2 | - | - |
| PRF-002 | covered | R4, R5, R6, R16, R23, R24, R25 | BND-STATE-001 | T3, T5, T9, T13, T14 | integration | hybrid | CMD3, CMD6 | M2 and M3 evidence | M3 | MP1 | - |
| PRF-003 | covered | R1, R3, R5, R6, R7, R10, R17, R19 | BND-AUTH-001 | T1, T3, T4, T12 | contract | hybrid | CMD1, CMD3 | Ledger and semantic-review evidence | M3 | MP1 | - |
| PRF-004 | covered | R1, R2, R4, R7, R11, R21, R22 | BND-COMPOSE-001 | T2, T4, T6, T7, T8 | integration | automated | CMD2, CMD3, CMD5, CMD6 | M2 and M3 package evidence | M3 | - | - |
| PRF-005 | covered | R4, R5, R16, R23, R25 | BND-TEMPORAL-001 | T3, T5, T13 | integration | hybrid | CMD3, CMD6 | M2 and M3 review evidence | M3 | MP1 | - |
| PRF-006 | covered | R9, R10, R13, R18, R22, R24, R25 | BND-RECOVERY-001 | T1, T8, T10, T11, T13, T14 | integration | automated | CMD1, CMD2, CMD5, CMD6 | Owning milestone evidence | M3 | - | - |
| PRF-007 | covered | R19, R21, R23, R25 | BND-COMPAT-001 | T7, T13, T15 | integration | automated | CMD5, CMD6 | M3 package and compatibility evidence | M3 | - | - |
| PRF-008 | covered | R15, R16, R18, R21, R22 | BND-ENV-001 | T7, T9, T10 | end-to-end | automated | CMD1, CMD5, CMD6 | M1 and M3 evidence | M3 | - | - |
| PRF-009 | covered | R2, R3, R4 | INT-001 | T1, T2, T12 | contract | hybrid | CMD1, CMD3 | M1 ledger, M2 structural, and M3 semantic evidence | M3 | MP1 | - |
| PRF-010 | covered | R1, R5, R6, R7 | INT-002 | T3, T4, T12 | contract | hybrid | CMD3 | M2 package and M3 semantic evidence | M3 | MP1 | - |
| PRF-011 | covered | R21, R22, R25 | INT-003 | T7, T8, T13 | end-to-end | automated | CMD5, CMD6 | M3 package evidence | M3 | - | - |
| PRF-012 | covered | R12, R13, R14, R17 | INT-004 | T1, T11, T12 | contract | hybrid | CMD1, CMD10, CMD11 | M1 ledger and M3 measurement evidence | M3 | MP1 | - |
| PRF-013 | covered | R15, R16, R18, R20 | INT-005 | T9, T10 | integration | automated | CMD1, CMD5, CMD6 | Fixture and command-graph evidence | M3 | - | - |
| PRF-014 | covered | R4, R5, R23, R25 | INT-006 | T3, T5, T13 | integration | hybrid | CMD3, CMD6 | M2 and M3 evidence | M3 | MP1 | - |

Evidence names are relative to `docs/changes/2026-08-10-code-review-skill-simplification/` when not written as repository paths.

## Edge case coverage

| Edge case | Covered by | Notes |
| --- | --- | --- |
| EC1 shared direct and automated rule | T1-T3, MP1 | Universal portion stays inline; only conditional detail moves. |
| EC2 similar paragraphs differ semantically | T1, T12, MP1 | Ledger and semantic review preserve distinct behavior. |
| EC3 output example mixes policy and structure | T4, T12 | Only repeated fields move to assets. |
| EC4 intentional generated transformation | T6-T8 | Requires existing declared transformation proof. |
| EC5 automation mentioned but not armed | T2, T9 | Conditional reference remains unloaded. |
| EC6 reference present but unmapped | T6, T8 | Canonical package validation fails. |
| EC7 apparently obsolete rule lacks contract change | T1, T12 | Removal is rejected or routed upstream. |
| EC8 sharp reduction by hiding policy in references | T3, T11, T12 | One reference and universal-inline rule block the move. |
| EC9 architecture applicability | T14 | Recorded `architecture-required` result and approved review. |

## Validation commands

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMD1 | `python -c 'import json; from pathlib import Path; root=Path("docs/changes/2026-08-10-code-review-skill-simplification"); ledger=json.loads((root/"code-review-rule-disposition.yaml").read_text()); scenarios=json.loads((root/"fixtures/scenario-contracts.yaml").read_text()); invalid=json.loads((root/"fixtures/invalid-ledger-disposition.yaml").read_text()); allowed={"retained-inline","retained-conditional-reference","asset-owned","removed-duplicate","removed-obsolete-with-approved-contract-change"}; required_fields={"rule_id","source_locations","behavior","disposition","destination","governing_requirements"}; required_scenarios={"direct-review","formal-recorded-review","missing-governing-authority","material-finding","clean-non-final-milestone","clean-final-milestone","workflow-managed-automated-review"}; destination_valid=lambda row: (row["disposition"] == "retained-inline" and row["destination"].startswith("skills/code-review/SKILL.md")) or (row["disposition"] == "retained-conditional-reference" and row["destination"].startswith("skills/code-review/references/workflow-managed-automated-review.md")) or (row["disposition"] == "asset-owned" and row["destination"].startswith("skills/code-review/assets/")) or (row["disposition"] == "removed-duplicate" and row["destination"].startswith("skills/code-review/")) or (row["disposition"] == "removed-obsolete-with-approved-contract-change" and row["destination"].startswith(("specs/","docs/"))); validate_rule=lambda row: ["unknown-disposition"] if row.get("disposition") not in allowed else (["missing-required-fields"] if not required_fields <= row.keys() else (["empty-required-fields"] if not all(row[field] for field in required_fields) else (["destination-inconsistent"] if not destination_valid(row) else []))); rules=ledger["rules"]; assert rules and all(validate_rule(row) == [] for row in rules); assert validate_rule(invalid)[0] == "unknown-disposition"; rows=scenarios["scenarios"]; assert {row["scenario"] for row in rows} == required_scenarios; assert all(row["required"] and row["forbidden"] for row in rows); print(f"ledger_rules={len(rules)} scenarios={len(rows)} unknown_fixture=unknown-disposition")'` | planned-for-implementation | implement | M1 | code-review M1 | Block on the shared validator's explicit unknown-disposition result before required-field and disposition-specific destination consistency, or on a missing field, missing scenario, or empty required/forbidden outcome. | Not applicable; deterministic assertions. | `evidence/m1-rule-ownership.md` | Repository-local read-only proof over change-local JSON-compatible YAML. |
| CMD2 | `python scripts/validate-skills.py skills/code-review/SKILL.md` | existing/configured | implement | M2 | code-review M2 | Block invalid frontmatter, structure, resource map, containment, placeholder, or narrow claim. | Not applicable; deterministic validator. | `evidence/m2-skill-refactor.md` | Read-only canonical skill validation. |
| CMD3 | `python scripts/test-skill-validator.py` | existing/configured | implement | M2 | code-review M2 | Block focused ownership, load-trigger, asset, vocabulary, or resource regression. | Zero tests is failure. | `evidence/m2-skill-refactor.md` | Repository-local test fixtures only. |
| CMD4 | `python scripts/build-skills.py --check` | existing/configured | implement | M2 | code-review M2 | Block generated local-skill drift or package omission. | Not applicable; deterministic check mode. | `evidence/m2-skill-refactor.md` | Check mode; does not hand-edit generated output. |
| CMD5 | `python scripts/test-adapter-distribution.py` | existing/configured | implement | M3 | code-review M3 | Block generation, archive, mapped-resource, installed-tree, or target-specific regression. | Zero tests is failure. | `evidence/m3-package-proof.md` | Local fixtures and temporary directories; no network or model runtime. |
| CMD6 | `python -c 'exec("""import subprocess, sys, tempfile\nversion = "v0.3.6"\nwith tempfile.TemporaryDirectory(prefix="rigorloop-adapters-") as output:\n    subprocess.run([sys.executable, "scripts/build-adapters.py", "--version", version, "--output-dir", output], check=True)\n    subprocess.run([sys.executable, "scripts/validate-adapters.py", "--version", version, "--adapter-root", output, "--clean-install-smoke", "--skill", "code-review"], check=True)""")'` | existing/configured | implement | M3 | code-review M3 | Block immediately on generation, archive validation, or temporary installed-tree mapped-resource parity failure for any supported target. | Not applicable; deterministic generation and validation. | `evidence/m3-package-proof.md` | Uses immutable trusted release-fixture identity `v0.3.6`; Python owns one fresh temporary directory and removes it on success or failure; no publication, network, prompt, or target runtime. |
| CMD7 | `python scripts/validate-boundary-first.py --check --path specs/code-review-skill-simplification.md` | existing/configured | test-spec | preimplementation gate | test-spec-review | Block malformed feature/proof boundary records, missing proof, or resource projection drift. | Not applicable; deterministic validator. | Test-spec review evidence. | Read-only checked-revision proof. |
| CMD8 | `python scripts/validate-change-metadata.py docs/changes/2026-08-10-code-review-skill-simplification/change.yaml` | existing/configured | workflow | lifecycle | every lifecycle gate | Block illegal artifact, workflow, planned-work, automation, or review state. | Not applicable; deterministic validator. | Change metadata validation result. | Read-only metadata validation. |
| CMD9 | `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-08-10-code-review-skill-simplification` | existing/configured | test-spec-review | lifecycle | test-spec-review | Block malformed, unindexed, or unresolved formal review evidence. | Not applicable; deterministic validator. | Review log and resolution. | Read-only review validation. |
| CMD10 | `python scripts/measure-skill-tokens.py --skills-root skills` | existing/configured | implement | M1 baseline and M3 comparison | code-review M1 | Block when the existing deterministic estimator cannot report the canonical `code-review` `SKILL.md` token estimate; record the M1 and M3 outputs separately. | Not applicable; deterministic measurement. | `evidence/m1-rule-ownership.md`; `evidence/simplification-measurements.md` | Read-only repository measurement; no threshold is enforced. |
| CMD11 | `python -c 'import json,runpy; from pathlib import Path; root=Path("skills/code-review"); change=Path("docs/changes/2026-08-10-code-review-skill-simplification"); estimate=runpy.run_path("scripts/measure-skill-tokens.py")["estimate_tokens"]; skill=(root/"SKILL.md").read_text(); docs={str(path.relative_to(root)):path.read_text() for path in sorted(root.rglob("*.md"))}; reference=docs.get("references/workflow-managed-automated-review.md",""); package="\n".join(docs.values()); ledger=json.loads((change/"code-review-rule-disposition.yaml").read_text()); cluster_ids={"quick-guide-restatement","evidence-reading-guidance","claim-boundaries","handoff-and-milestone-routing","full-inline-output-templates","shared-boundary-method-detail","workflow-managed-automation-procedure"}; cluster_rows=[row for row in ledger["rules"] if row.get("cluster_id") in cluster_ids]; assert {row["cluster_id"] for row in cluster_rows} == cluster_ids; destinations={cluster_id:{row.get("destination") for row in cluster_rows if row["cluster_id"] == cluster_id and row.get("destination")} for cluster_id in cluster_ids}; duplicate_after=sum(len(owners) != 1 for owners in destinations.values()); template_markers=("## Recommended clean review template","## Result\n\n- Review surface:"); metrics={"skill_lines":len(skill.splitlines()),"skill_words":len(skill.split()),"skill_estimated_tokens":estimate(skill),"conditional_reference_words":len(reference.split()),"conditional_reference_estimated_tokens":estimate(reference) if reference else 0,"package_words":len(package.split()),"package_estimated_tokens":estimate(package),"duplicated_rule_clusters_before":len(cluster_ids),"duplicated_rule_clusters_after":duplicate_after,"inline_templates":sum(marker in skill for marker in template_markers),"mapped_resources":sum(line.startswith("- READ `") or line.startswith("- COPY `") for line in skill.splitlines())}; print(json.dumps(metrics,sort_keys=True))'` | planned-for-implementation | implement | M1 baseline and M3 comparison | code-review M1 | Block when a named duplication cluster is absent or any required size, ownership, template, or mapped-resource metric cannot be produced; report every cluster without exactly one destination owner in `duplicated_rule_clusters_after`. | Not applicable; deterministic measurement. | `evidence/m1-rule-ownership.md`; `evidence/simplification-measurements.md` | Read-only repository and change-local measurement; run unchanged at M1 and M3 and record outputs separately without a permanent gate. |

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Preimplementation gate | T1-T16 | none | CMD7, CMD8, CMD9 | This test spec, authoring evidence, and test-spec-review record | implementation handoff | Every requirement, criterion, example, edge case, boundary, interaction, command, and milestone is mapped with no gaps; execution proof remains milestone-owned. |
| M1 | T1, T9 | none | CMD1, CMD8, CMD10, CMD11 | `evidence/m1-rule-ownership.md`; baseline measurement evidence | code-review M1 | Complete ownership, fixture proof, and exact baseline measurements precede prose movement; T11 comparison remains deferred to M3. |
| M2 | T2-T6, T8, T10 | none | CMD2, CMD3, CMD4, CMD8 | `evidence/m2-skill-refactor.md`; M2 code-review record | code-review M2 | Proves canonical refactor, conditional load, assets, vocabulary, and no runtime test machinery; final semantic preservation remains deferred to MP1 at M3. |
| M3 | T7-T16 | MP1 | CMD2, CMD3, CMD5, CMD6, CMD8, CMD10, CMD11 | `evidence/m3-package-proof.md`; `evidence/simplification-measurements.md`; semantic review; M3 code-review record | code-review M3 | Repeats the exact measurements and proves all targets, installed trees, rollback, compatibility, metrics, and final semantic preservation. |

## Test cases

### T1. Ledger and fixture contract fails closed

- Covers: R8-R10, R12, R15, R16, E4, EC1, EC2, EC7, BND-INPUT-001, BND-AUTH-001, BND-RECOVERY-001, INT-001, INT-004
- Level: unit
- Command IDs: CMD1
- Fixture/setup: JSON-compatible YAML ledger, seven-scenario fixture, and unknown-disposition fixture.
- Steps: Parse closed values before checking required fields and destinations; compare scenario identities and non-empty outcomes.
- Expected result: The valid ledger and scenarios pass; an unknown disposition is rejected before consistency.
- Failure proves: A rule can disappear, use an unknown state, or lack fixture coverage without stopping M1.
- Evidence artifact: `evidence/m1-rule-ownership.md`
- Automation location: CMD1 over change-local artifacts
- Required by milestone: M1

### T2. Direct review is complete without conditional loading

- Covers: R2-R4, E1, EC1, EC5, BND-INPUT-001, BND-COMPOSE-001, INT-001
- Level: integration
- Command IDs: CMD2, CMD3
- Fixture/setup: Canonical `code-review` package and focused skill-validator assertions.
- Steps: Inspect direct and isolated paths, exact resource mappings, and load trigger.
- Expected result: All universal policy is inline and the automation reference remains unloaded unless formally armed.
- Failure proves: Direct review depends on hidden conditional procedure.
- Evidence artifact: `evidence/m2-skill-refactor.md`
- Automation location: `scripts/test-skill-validator.py`
- Required by milestone: M2

### T3. Armed automation loads one bounded reference

- Covers: R1, R4-R6, E2, EC8, BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001, INT-002, INT-006
- Level: integration
- Command IDs: CMD2, CMD3
- Fixture/setup: Canonical skill plus conditional reference.
- Steps: Verify exact `READ` path and trigger, allowed automation sections, and forbidden universal-policy absence.
- Expected result: One reference supplies only automation procedure while `code-review` retains native authority.
- Failure proves: Conditional loading transfers policy ownership or hides universal safety.
- Evidence artifact: `evidence/m2-skill-refactor.md`
- Automation location: `scripts/test-skill-validator.py`; final semantic ownership is deferred to T12 and MP1 at M3
- Required by milestone: M2

### T4. Assets own structure only

- Covers: R7, E7, EC3, BND-AUTH-001, BND-COMPOSE-001, INT-002
- Level: integration
- Command IDs: CMD2, CMD3
- Fixture/setup: Both mapped assets and canonical skill.
- Steps: Confirm assets contain complete repeated field structures, no policy, and no full duplicate inline templates.
- Expected result: Assets are sole structural leaves and policy remains with `code-review`.
- Failure proves: Output structure is duplicated or an asset becomes a policy owner.
- Evidence artifact: `evidence/m2-skill-refactor.md`
- Automation location: `scripts/test-skill-validator.py`; final semantic ownership is deferred to T12 and MP1 at M3
- Required by milestone: M2

### T5. Native review semantics remain unchanged

- Covers: R3, R6, R23, EC1, BND-STATE-001, BND-TEMPORAL-001, INT-006
- Level: integration
- Command IDs: CMD3
- Fixture/setup: Before/after vocabulary and rule-disposition comparison.
- Steps: Compare statuses, severities, finding fields, recording, settlement, milestone, rereview, claim, and handoff rules.
- Expected result: Every native semantic owner and value is unchanged.
- Failure proves: Simplification changes lifecycle or review behavior.
- Evidence artifact: `evidence/m2-skill-refactor.md`
- Automation location: focused assertions; final semantic preservation is deferred to T12 and MP1 at M3
- Required by milestone: M2

### T6. Canonical resource integrity covers the complete package

- Covers: R1, R4, R7, R19, R21, R22, EC4, EC6, BND-COMPOSE-001
- Level: integration
- Command IDs: CMD2, CMD3, CMD4
- Fixture/setup: Valid package and missing, escaping, unfilled, unmapped, and duplicate mapping variants.
- Steps: Run existing skill and generated-skill validation against each variant.
- Expected result: Valid package passes; every invalid resource state fails with path, invariant, and repair surface.
- Failure proves: Canonical or generated packages can omit or misdeclare resources.
- Evidence artifact: `evidence/m2-skill-refactor.md`
- Automation location: existing skill validator suites
- Required by milestone: M2

### T7. Every supported target preserves packed and installed bytes

- Covers: R19, R21, R25, BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001, INT-003
- Level: e2e
- Command IDs: CMD5, CMD6
- Fixture/setup: Generated Codex, Claude Code, and opencode archives plus empty temporary install trees.
- Steps: Generate, validate archives, materialize each target, and compare inventory, relative paths, and raw-byte identities.
- Expected result: Every mapped reference and asset matches canonical bytes in every target.
- Failure proves: A supported package or installed tree is incomplete or stale.
- Evidence artifact: `evidence/m3-package-proof.md`
- Automation location: adapter distribution suite and `validate-adapters.py`
- Required by milestone: M3

### T8. Package resource failures are target-specific and actionable

- Covers: R22, E3, EC4, EC6, BND-COMPOSE-001, BND-RECOVERY-001, INT-003
- Level: integration
- Command IDs: CMD2, CMD3, CMD5
- Fixture/setup: Missing, stale, path-escaping, unfilled, undeclared, and malformed resource variants.
- Steps: Mutate one target or package boundary at a time and run its existing owner.
- Expected result: The affected target fails with the violated invariant and repair surface; other target proof cannot substitute.
- Failure proves: A broken target can pass from sibling evidence or unclear diagnostics.
- Evidence artifact: `evidence/m3-package-proof.md`
- Automation location: existing skill and adapter suites
- Required by milestone: M3

### T9. Static scenario fixtures cover required and forbidden outcomes

- Covers: R15, R16, E1, E2, BND-INPUT-001, BND-STATE-001, BND-ENV-001, INT-005
- Level: unit
- Command IDs: CMD1
- Fixture/setup: Seven required scenario records.
- Steps: Verify exact scenario identities and non-empty required/forbidden outcome lists; semantically compare them with the spec.
- Expected result: All seven distinct outcomes are represented without executing a model.
- Failure proves: Acceptance omits a required mode or uses runtime behavior as proof.
- Evidence artifact: `evidence/m1-rule-ownership.md`
- Automation location: CMD1; semantic outcome quality is deferred to T12 and MP1 at M3
- Required by milestone: M1

### T10. Acceptance command graph excludes target-agent execution

- Covers: R18, R20, E6, BND-RECOVERY-001, BND-ENV-001, INT-005
- Level: integration
- Command IDs: CMD2, CMD3, CMD5, CMD6
- Fixture/setup: Test-spec command ledger and changed acceptance surfaces.
- Steps: Inspect commands and changed scripts for runtime launch, prompts, transcript grading, model selection, network model calls, or nondeterministic retries.
- Expected result: Only repository-local deterministic and semantic-review proof remains.
- Failure proves: The change recreates model-behavior certification.
- Evidence artifact: `evidence/m3-package-proof.md`
- Automation location: focused static assertions and MP1
- Required by milestone: M2, M3

### T11. Measurements distinguish context reduction from package size

- Covers: R11-R14, E5, EC8, BND-RECOVERY-001, INT-004
- Level: integration
- Command IDs: CMD10, CMD11
- Fixture/setup: Recorded baseline and after measurements.
- Steps: Compare required line, word, token-estimate, reference, package, cluster, template, and resource counts.
- Expected result: Common-path and total-package deltas are separate; no material reduction fails; percentage shortfall alone does not fail.
- Failure proves: Relocation is misreported as deletion or numeric optimization overrides semantics.
- Evidence artifact: `evidence/simplification-measurements.md`
- Automation location: CMD10 and CMD11, repeated unchanged at M1 and M3, plus MP1
- Required by milestone: M3

### T12. Independent semantic review approves the package and ledger

- Covers: R8, R10, R12, R13, R15, R17, AC1, AC6, AC9, EC2, EC3, EC7, EC8, BND-AUTH-001, INT-002, INT-004
- Level: manual
- Command IDs: none
- Fixture/setup: Final canonical package, rule ledger, scenario fixtures, and measurements.
- Steps: Execute MP1 independently from the authoring rationale.
- Expected result: Every semantic criterion passes or produces a formal material finding.
- Failure proves: Structural proof has substituted for meaning or a rule has been weakened.
- Evidence artifact: `evidence/semantic-preservation-review.md`
- Automation location: MP1
- Required by milestone: M3

### T13. Atomic rollout and rollback reject mixed packages

- Covers: R21, R22, R25, BND-STATE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-COMPAT-001, INT-003, INT-006
- Level: e2e
- Command IDs: CMD5, CMD6
- Fixture/setup: Old complete package, new complete package, and mixed canonical/generated/archive variants.
- Steps: Validate both complete versions, reject each mixed variant, then regenerate from the selected canonical rollback version.
- Expected result: Only complete single-version packages pass and rollback restores all targets.
- Failure proves: Partial resource movement can publish or rollback incompletely.
- Evidence artifact: `evidence/m3-package-proof.md`
- Automation location: adapter distribution fixtures
- Required by milestone: M3

### T14. Architecture applicability and settlement are unambiguous

- Covers: R24, EC9, BND-STATE-001, BND-RECOVERY-001
- Level: integration
- Command IDs: CMD8, CMD9
- Fixture/setup: Architecture assessment, R1 finding, correction evidence, R2 approval, and change metadata.
- Steps: Validate the recorded `architecture-required` route and approved final architecture entry.
- Expected result: Planning depends on the approved corrected architecture; ambiguity would stop.
- Failure proves: Workflow bypassed an architecture decision or retained contradictory settlement.
- Evidence artifact: `architecture-assessment.md`; `reviews/architecture-review-r2.md`
- Automation location: lifecycle and review validation
- Required by milestone: preimplementation gate

### T15. Historical review artifacts and native compatibility remain valid

- Covers: R23, R25, BND-COMPAT-001
- Level: integration
- Command IDs: CMD3, CMD5
- Fixture/setup: Existing review records and before/after package vocabulary.
- Steps: Confirm historical records remain readable and no migration or rewrite is required.
- Expected result: Old evidence keeps its meaning while new packages use the simplified structure.
- Failure proves: Simplification invalidates historical review evidence or old native values.
- Evidence artifact: `evidence/m3-package-proof.md`
- Automation location: existing review and skill fixtures plus MP1
- Required by milestone: M3

### T16. No permanent simplicity validator or forbidden subsystem is introduced

- Covers: R19, R20, BND-AUTH-001, BND-ENV-001, INT-005
- Level: integration
- Command IDs: CMD2, CMD3, CMD5
- Fixture/setup: Final changed-path inventory and command ledger.
- Steps: Inspect new scripts, selectors, schedulers, caches, validators, runtime journeys, and token/prose gates.
- Expected result: Only existing owners and change-local evidence are present.
- Failure proves: The change adds durable machinery beyond the approved boundary.
- Evidence artifact: `evidence/m3-package-proof.md`
- Automation location: changed-path inspection and MP1
- Required by milestone: M3

## Fixtures and data

- `docs/changes/2026-08-10-code-review-skill-simplification/code-review-rule-disposition.yaml`: JSON-compatible YAML with top-level `rules` array.
  The seven R11 duplication-cluster rows use stable `cluster_id` values matching CMD11; all other rows may use `-` or omit `cluster_id`.
- `docs/changes/2026-08-10-code-review-skill-simplification/fixtures/scenario-contracts.yaml`: JSON-compatible YAML with the seven scenario records.
- `docs/changes/2026-08-10-code-review-skill-simplification/fixtures/invalid-ledger-disposition.yaml`: one `moved-somewhere` negative value.
- Existing skill fixtures under `tests/fixtures/skills/` for structural and mapped-resource failures.
- Existing adapter fixtures and temporary generated/archive/install trees owned by `scripts/test-adapter-distribution.py`.

Fixtures contain repository-local synthetic content only. No prompts, transcripts, credentials, user data, external package state, or model identifiers are required.

## Mocking/stubbing policy

Do not mock canonical skill parsing, adapter archive construction, resource hashing, or installed-tree filesystem comparison. Temporary directories and synthetic package variants are allowed because the observed boundary is local package content. No target-agent runtime is mocked because target-runtime behavior is outside acceptance.

## Migration or compatibility tests

T13 proves complete old/new packages and rejects mixed rollout or rollback. T15 proves historical review evidence and native vocabularies remain readable without migration. Intentional generated transformations remain accepted only through an already-approved explicit transformation contract.

## Observability verification

Deterministic failures must name the affected skill or target, resource path, violated invariant, and repair surface. Change-local evidence must record ledger count, scenario count, duplicate clusters, baseline and after metrics, selected commands, target identities, semantic-review outcome, and any justified percentage shortfall.

No model ID, prompt, transcript, runtime retry, or external publication status is acceptance evidence.

## Security/privacy verification

All commands operate on repository files and newly created temporary directories. Tests reject path traversal outside a skill root and archive/install target. Evidence must not contain credentials, private prompts, user data, raw environment dumps, or machine-local absolute paths. CMD6 has no network, publication, or target-runtime side effect.

## Performance checks

Record `SKILL.md` line, word, and tokenizer-estimate reductions and separate conditional-reference and total-package sizes. Treat 35–45 percent as a reported planning target only. No timing, token, or prose-quality threshold is a permanent gate.

## Manual QA checklist

Manual procedure ID: MP1

- Automation rationale: Semantic preservation, policy ownership, and useful handoff require bounded independent judgment that deterministic structure checks cannot establish.
- Owning stage: code-review M3
- Owner: independent semantic reviewer
- Required environment: final M3 repository worktree containing the canonical `skills/code-review/` package, completed rule-disposition ledger, scenario fixtures, and M1/M3 measurements; no network or target-agent runtime.
- Evidence artifact: `docs/changes/2026-08-10-code-review-skill-simplification/evidence/semantic-preservation-review.md`
- Pass condition: Every R17 criterion passes, every behaviorally significant rule has one allowed owner and destination, universal policy remains inline, conditional loading remains exact, assets own structure only, and any sub-35-percent result has an adequate semantic-preservation rationale.
- Failure condition: Any rule is missing, weakened, ambiguously owned, or incorrectly relocated; direct review depends on conditional content; assets own policy; the load trigger broadens; measurement accounting is misleading; or required evidence is absent.
- Rerun condition: Repeat after any substantive package, ledger, fixture, measurement, or review-driven correction.

Exact steps:

1. Use the final canonical `skills/code-review/` package, ledger, fixtures, and measurements without relying on author-hidden reasoning.
2. Check trigger clarity, package ownership, prerequisites, operating sequence, evidence use, stop conditions, claim boundaries, output usefulness, handoff clarity, rule dispositions, and the exact conditional-reference load trigger.
3. Confirm every universal status, stop, recording, claim, handoff, milestone, and rereview rule is inline and every reference/asset rule has one allowed owner.
4. Confirm each ledger source resolves to its destination and every removed duplicate points to the retained owner.
5. Compare common-path and total-package metrics and explain any result below the 35 percent planning target.
6. Record approval or formal material findings in `evidence/semantic-preservation-review.md` and the applicable code-review record.

## What not to test and why

- Do not execute Codex, Claude Code, opencode, or another target agent; repository acceptance owns package files, not model interpretation.
- Do not send prompts, grade transcripts, compare models, or retry nondeterministic sessions.
- Do not add a permanent line, token, prose-quality, or simplicity gate; measurements are change evidence.
- Do not test unrelated skills, release publication, network download, credentials, or external registries.
- Do not require a Cartesian scenario matrix when the sixteen cases directly prove every boundary and selected interaction.

## Uncovered gaps

None.

Every requirement, acceptance criterion, example, edge case, boundary, interaction, milestone, and validation command has direct automated, manual, or hybrid proof.

## Next artifacts

- Formal test-spec review.
- M1-M3 implementation and code-review loops only after test-spec approval.

## Follow-on artifacts

None yet

## Readiness

Ready for `test-spec-review`. This proof map does not authorize implementation until the formal review is approved and recorded.
