<!-- Template: test-spec-skeleton-v1 -->

# Test-Spec Skill Simplification Test Specification

## Owning change record

`docs/changes/2026-08-13-test-spec-skill-simplification/change.yaml`

## Related spec and plan

- Spec: `specs/test-spec-skill-simplification.md`
- Plan: `docs/plans/2026-08-13-test-spec-skill-simplification.md`
- Architecture/ADRs: `docs/changes/2026-08-13-test-spec-skill-simplification/architecture-assessment.md`; existing published-skill resource-integrity and stage-owned lifecycle architecture

## Input artifact identities

| Input | Path | Artifact ID | Review evidence |
| --- | --- | --- | --- |
| Feature spec | `specs/test-spec-skill-simplification.md` | `spec` | `spec-review-r1`; `docs/changes/2026-08-13-test-spec-skill-simplification/reviews/spec-review-r1.md` |
| Execution plan | `docs/plans/2026-08-13-test-spec-skill-simplification.md` | `plan` | `plan-review-r1`; `docs/changes/2026-08-13-test-spec-skill-simplification/reviews/plan-review-r1.md` |
| Architecture assessment | `docs/changes/2026-08-13-test-spec-skill-simplification/architecture-assessment.md` | `architecture-assessment` | `architecture-not-required` |

## Testing strategy

Use deterministic contract fixtures for profile selection, authority, creation, retry, restart, revision, structural composition, proof modes, resource failure, and forbidden writes. Existing validators own permanent skill, boundary, lifecycle, build, and distribution checks. Change-local ledgers and measurements prove semantic disposition and loaded-profile reduction, while MP0 and MP1 provide the semantic judgments that deterministic validation cannot make. No target-agent runtime, transcript grading, prompt journey, tokenizer dependency, network service, publication, or release action is part of acceptance.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1-R7 | T1, T2, T11, T15 | integration | Package membership, resource mapping, universal ownership, and fail-safe loading. |
| R8-R14 | T1-T3 | contract | Closed profiles, candidate loading, exact authority, operations, and forbidden writes. |
| R15-R21 | T3-T5 | contract | Entry-first creation, retry identity, interruption, idempotency, and authoring boundary. |
| R22-R29 | T5, T6 | contract | Stale detection, same-entry restart, partial-byte treatment, and invalid restart stops. |
| R30-R37 | T7, T8 | contract | Revision authority, identity, state, historical evidence, retry, and reliance blocking. |
| R38-R42 | T3, T8, T9 | contract | Authoring handoff, peer settlement, workflow isolation, and claim boundaries. |
| R43-R51 | T10-T12 | contract | Five-asset composition, placeholder rejection, policy boundaries, and optional manual verification. |
| R52-R56 | T13, T14, T16 | contract | Semantic and literal inventories, unknown-value failure, scenarios, and bounded acceptance. |
| R57-R61 | T14, T16 | integration | Deterministic profile accounting, reduction, no tokenizer, and no permanent simplicity gate. |
| R62 | T15 | integration | Canonical-through-installed resource parity. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | T1, T2 | Portable authoring loads no governed procedure and remains complete. |
| E2 | T3, T4 | Governed creation registers one entry before content and ends at review-required. |
| E3 | T2, T3 | Candidate loading never grants write authority. |
| E4 | T4, T5 | Identical creation retries resume or return idempotent success. |
| E5 | T5, T6 | Changed basis first stops, then restarts the same entry under exact authority. |
| E6 | T7, T8 | Revision preserves old evidence and requires fresh review. |
| E7 | T8 | Active implementation reliance blocks ordinary revision. |
| E8 | T10, T11 | Skeleton and row assets compose output without duplicate bodies. |
| E9 | T12 | Automated proof omits inapplicable manual identifiers. |
| E10 | T12 | Manual and hybrid proof use current structures and procedures. |
| E11 | T1, T11 | Missing required resources stop without fallback reconstruction. |
| E12 | T14, T16 | Loaded profiles and total package size are reported separately. |

## Proof map

Boundary model version: boundary-first-v1
Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R49, R50, R51, R52, R53, R54, R55, R56, R57, R58, R59, R60, R61, R62

| Proof obligation ID | Coverage state | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Proof level | Automation mode | Command IDs | Evidence artifact | Required milestone | Manual procedure IDs | Uncovered gap ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRF-001 | covered | R8, R9, R10, R11, R12, R13, R14, R18, R30, R33 | BND-INPUT-001 | T1-T3, T7, T13 | contract | automated | CMD1, CMD3 | `evidence/m1-preservation-inventories.md`; `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-002 | covered | R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41 | BND-STATE-001 | T3-T9 | contract | automated | CMD1, CMD3, CMD9 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-003 | covered | R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41 | BND-STATE-002 | T4-T9 | contract | automated | CMD1, CMD3, CMD9 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-004 | covered | R9, R10, R11, R12, R13, R14, R18, R19, R20, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37 | BND-AUTH-001 | T2-T9 | contract | hybrid | CMD1, CMD3, CMD9 | `evidence/m2-package-implementation.md`; `evidence/semantic-preservation-review.md` | M3 | MP1 | - |
| PRF-005 | covered | R9, R10, R11, R12, R13, R14, R18, R19, R20, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37 | BND-AUTH-002 | T4-T8 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-006 | covered | R1, R2, R3, R4, R5, R6, R7, R43, R44, R45, R46, R47, R48, R49, R50, R51 | BND-COMPOSE-001 | T1, T2, T11, T15 | integration | hybrid | CMD2-CMD7 | `evidence/m2-package-implementation.md`; `evidence/m3-package-proof.md` | M3 | MP1 | - |
| PRF-007 | covered | R1, R2, R3, R4, R5, R6, R7, R43, R44, R45, R46, R47, R48, R49, R50, R51 | BND-COMPOSE-002 | T10-T12 | contract | automated | CMD2-CMD5 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-008 | covered | R18, R19, R20, R22, R23, R24, R25, R26, R27, R28, R29, R33, R34, R35, R36, R37 | BND-TEMPORAL-001 | T4-T8 | contract | automated | CMD1, CMD3, CMD9 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-009 | covered | R5, R6, R20, R22, R23, R24, R25, R26, R27, R28, R29, R37 | BND-RECOVERY-001 | T5, T6, T8 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-010 | covered | R5, R6, R20, R29, R37 | BND-RECOVERY-002 | T1, T3, T6, T8, T11 | contract | automated | CMD2, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-011 | covered | R4, R35, R49, R50, R51, R52, R53, R62 | BND-COMPAT-001 | T8, T12-T15 | integration | hybrid | CMD1, CMD3-CMD8 | `evidence/m1-preservation-inventories.md`; `evidence/m3-package-proof.md` | M3 | MP0, MP1 | - |
| PRF-012 | covered | R5, R42, R56, R62 | BND-ENV-001 | T1, T9, T15, T16 | integration | automated | CMD2-CMD8 | `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-013 | covered | R18, R19, R20 | INT-001 | T2-T5 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-014 | covered | R23, R24, R25, R26, R27, R28, R29 | INT-002 | T5, T6 | contract | automated | CMD1, CMD3, CMD9 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-015 | covered | R35 | INT-003 | T7, T8 | contract | automated | CMD1, CMD3, CMD9 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-016 | covered | R49, R50, R51 | INT-004 | T10-T14 | contract | hybrid | CMD1, CMD3 | `evidence/m1-preservation-inventories.md`; `evidence/semantic-preservation-review.md` | M3 | MP0, MP1 | - |
| PRF-017 | covered | R5 | INT-005 | T1, T11, T15 | integration | automated | CMD2-CMD7 | `evidence/m3-package-proof.md` | M3 | - | - |

## Edge case coverage

| Edge case | Covered by | Expected handling |
| --- | --- | --- |
| Unknown profile, operation, disposition, literal class, state, or proof mode | T1, T2, T12, T13 | Fail closed before consistency logic or writes. |
| Candidate points to a missing, stale, mismatched, or multiple change | T2, T3 | Load governed procedure when indicated, then stop without portable fallback. |
| Creation is interrupted before file, before evidence, or before transition | T4, T5 | Resume only the same retry tuple and produce one effective result. |
| Governing inputs change during incomplete creation | T5, T6 | Report stale first; restart only the same authoring entry with new bound evidence. |
| Partial bytes are required for audit or are disposable | T6 | Preserve required bytes distinctly or record why incomplete bytes are unnecessary before replacement. |
| Active test spec has implementation reliance | T8 | Stop ordinary revision and route to separately governed reopen or migration. |
| Required resource is missing, unreadable, escaped, contradictory, or mixed | T1, T11, T15 | Stop dependent work and never reconstruct procedure from memory. |
| Automated proof has no manual procedure | T12 | Use the approved inapplicable sentinel and add no manual ceremony. |
| Main file shrinks while a loaded profile grows | T14 | Acceptance fails despite main-file reduction. |

## Validation commands

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMD1 | `python -c 'import json; from pathlib import Path; root=Path("docs/changes/2026-08-13-test-spec-skill-simplification"); rules=json.loads((root/"test-spec-rule-disposition.yaml").read_text())["rules"]; literals=json.loads((root/"test-spec-literal-compatibility.yaml").read_text())["literals"]; scenarios=json.loads((root/"fixtures/scenario-contracts.yaml").read_text())["scenarios"]; rd={"retained-inline","retained-governed-reference","retained-boundary-reference","asset-owned","removed-duplicate","removed-obsolete-with-approved-contract-change"}; lc={"normative-contract","parser-or-package-contract","test-only-incidental","obsolete","historical-fixture"}; assert rules and literals and scenarios; assert all(row.get("disposition") in rd for row in rules); assert all(row.get("classification") in lc for row in literals); assert len({row["rule_id"] for row in rules})==len(rules); assert len({row["literal_id"] for row in literals})==len(literals); print(f"rules={len(rules)} literals={len(literals)} scenarios={len(scenarios)}")'` | planned-for-implementation | implement | M1 | M1 code-review | Reject unknown values first, then incomplete rows, duplicate IDs, or scenario drift. | Not applicable; every assertion executes. | `evidence/m1-preservation-inventories.md` | Repository-local reads only; no network or target-agent runtime. |
| CMD2 | `python scripts/validate-skills.py skills/test-spec/SKILL.md` | existing/configured | implement | M2 | M2 code-review | Block skill structure, mapping, containment, placeholder, or claim defects. | Not applicable; deterministic validation. | `evidence/m2-package-implementation.md` | Read-only repository validation. |
| CMD3 | `python scripts/test-skill-validator.py TestSpecSkillSimplificationTests` | planned-for-implementation | implement | M2 | M2 code-review | Block focused package, transaction, structure, or failure behavior. | Zero discovered tests is failure. | `evidence/m2-package-implementation.md` | Repository-local tests; no target-agent runtime. |
| CMD4 | `python scripts/test-skill-validator.py` | existing/configured | implement | M2 | M2 code-review | Block broad skill-contract regression. | Zero discovered tests is failure. | `evidence/m2-package-implementation.md` | Repository-local tests; no target-agent runtime. |
| CMD5 | `python scripts/test-build-skills.py` | existing/configured | implement | M2 | M2 code-review | Block generated inventory or resource regressions. | Zero discovered tests is failure. | `evidence/m2-package-implementation.md` | Temporary filesystem only. |
| CMD6 | `python scripts/build-skills.py --check` | existing/configured | implement | M2 | M2 code-review | Block generated-package drift or missing resources. | Not applicable. | `evidence/m2-package-implementation.md` | Read-only check against canonical sources. |
| CMD7 | `python scripts/test-adapter-distribution.py` | existing/configured | implement | M3 | M3 code-review | Block adapter generation, archive, install, or parity regression. | Zero discovered tests is failure. | `evidence/m3-package-proof.md` | Temporary files only; no publication or network. |
| CMD8 | `python -c 'exec("""import subprocess, sys, tempfile\nversion = "v0.4.0"\nwith tempfile.TemporaryDirectory(prefix="rigorloop-adapters-") as output:\n    subprocess.run([sys.executable, "scripts/build-adapters.py", "--version", version, "--output-dir", output], check=True)\n    subprocess.run([sys.executable, "scripts/validate-adapters.py", "--version", version, "--adapter-root", output, "--clean-install-smoke", "--skill", "test-spec"], check=True)""")'` | existing/configured | implement | M3 | M3 code-review | Block generation or archive/installed resource mismatch. | Not applicable; all supported targets are selected. | `evidence/m3-package-proof.md` | One fresh temporary directory; no publication, network, or agent execution. |
| CMD9 | `python scripts/validate-boundary-first.py --check --path specs/test-spec-skill-simplification.md` | existing/configured | implement | M2 | M2 code-review | Block invalid or missing proof for any boundary or interaction. | Not applicable; matching proof map is mandatory. | `evidence/m2-package-implementation.md` | Read-only repository validation. |
| CMD10 | `python scripts/validate-change-metadata.py docs/changes/2026-08-13-test-spec-skill-simplification/change.yaml` | existing/configured | workflow | lifecycle | Every state-changing handoff | Block invalid artifact, review, or planned-work state. | Not applicable. | Owning change validation ledger | Read-only validation. |
| CMD11 | `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-08-13-test-spec-skill-simplification` | existing/configured | review stages | lifecycle | Every formal review handoff | Block malformed or missing review evidence. | Not applicable. | Review log and records | Read-only validation. |

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | T13, T14 | MP0 | CMD1, CMD10 | `evidence/profile-size-baseline.md`; `evidence/m1-preservation-inventories.md` | M1 code-review | Canonical skill prose remains unchanged while ownership and baselines are frozen. |
| M2 | T1-T13 | none | CMD2-CMD6, CMD9-CMD11 | `evidence/m2-package-implementation.md` | M2 code-review | Focused failing assertions precede the atomic canonical package change. |
| M3 | T11-T16 | MP1 | CMD1-CMD11 | `evidence/simplification-measurements.md`; `evidence/semantic-preservation-review.md`; `evidence/m3-package-proof.md` | M3 code-review and final review | Proves profile reduction, semantics, boundary coverage, and package-chain parity. |
| M4 | T16 | MP1 | CMD1-CMD11 | Final review, explanation, and verify evidence | verify | Lifecycle-only closeout begins after M1-M3 are closed. |

## Test cases

### T1. Procedural profiles load exact resources once

- Covers: R1-R10; E1, E11; BND-INPUT-001, BND-COMPOSE-001, BND-ENV-001; INT-005
- Level: contract
- Command IDs: CMD2-CMD6
- Fixture/setup: Portable and governed profiles plus late-discovery, missing, unreadable, escaped, duplicate, and mixed-version resources.
- Steps: Assemble each profile in documented order and exercise required, forbidden, late, missing, and duplicate loads.
- Expected result: Both boundary references load initially once, the governed reference loads only for a candidate, every applicable asset loads as needed, and defective resources stop dependent behavior.
- Failure proves: Progressive disclosure is incomplete, duplicated, or unsafe.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Existing skill validator tests.
- Required by milestone: M2

### T2. Portable proof design remains complete and isolated

- Covers: R2, R7-R14; E1, E3; BND-INPUT-001, BND-AUTH-001; INT-001
- Level: contract
- Command IDs: CMD2, CMD3
- Fixture/setup: Portable proof-design fixture and plausible but invalid governed candidates.
- Steps: Classify the profile, design proof, and test candidate validation and forbidden writes.
- Expected result: Portable authoring needs no governed procedure; candidate loading alone permits no mutation; invalid candidates stop without fallback.
- Failure proves: Universal policy was hidden or resource loading manufactures authority.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Focused skill-validator fixtures.
- Required by milestone: M2

### T3. Entry-first creation has a bounded write set

- Covers: R11-R17, R21, R38-R42; E2, E3; BND-STATE-001, BND-AUTH-001; INT-001
- Level: contract
- Command IDs: CMD3, CMD10
- Fixture/setup: Exact governed creation plus missing, colliding, ambiguous, and forbidden-write variants.
- Steps: Resolve intended identities, register one authoring entry, compose content and evidence, and finish the matching entry.
- Expected result: Only the test-spec entry changes from absent to authoring to review-required; review, workflow, automation, and implementation state remain untouched.
- Failure proves: Governed authoring crosses lifecycle ownership or writes before authority.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Static lifecycle scenarios and metadata validation.
- Required by milestone: M2

### T4. Identical creation retries produce one effective result

- Covers: R15-R20; E2, E4; BND-STATE-001, BND-AUTH-002, BND-TEMPORAL-001; INT-001
- Level: contract
- Command IDs: CMD1, CMD3, CMD10
- Fixture/setup: Interruptions after entry creation, after file write, after evidence write, and after review-required transition.
- Steps: Replay the exact retry tuple at every interruption boundary.
- Expected result: Each retry resumes only its bound partial transaction or returns idempotent success without duplicate entries, files, or evidence.
- Failure proves: Creation recovery is non-idempotent or silently rebinds identity.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Static lifecycle fixtures.
- Required by milestone: M2

### T5. Changed-basis creation stops before restart

- Covers: R18-R24; E4, E5; BND-STATE-002, BND-AUTH-002, BND-TEMPORAL-001, BND-RECOVERY-001; INT-002
- Level: contract
- Command IDs: CMD1, CMD3
- Fixture/setup: Incomplete authoring attempts whose governing spec, plan, path, entry, or evidence identity changed.
- Steps: Retry creation, classify staleness, and attempt an unauthorized direct restart.
- Expected result: Changed identity returns `stale-authoring-attempt`; workflow may route but cannot mutate; restart waits for exact test-spec authority.
- Failure proves: Retry silently adopts, overwrites, abandons, or rebinds stale work.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Static lifecycle fixtures.
- Required by milestone: M2

### T6. Same-entry restart preserves identity and required partial evidence

- Covers: R24-R29; E5; BND-STATE-002, BND-AUTH-002, BND-TEMPORAL-001, BND-RECOVERY-001, BND-RECOVERY-002; INT-002
- Level: contract
- Command IDs: CMD1, CMD3, CMD10
- Fixture/setup: Authorized exact authoring entry with disposable, audit-required, ambiguous, reviewed, relied-on, terminal, and competing variants.
- Steps: Validate no reliance, preserve required prior bytes or rationale, replace the evidence path, and restart with a new retry identity.
- Expected result: Safe restart retains the entry ID, kind, role, path, and authoring state; unsafe variants block before mutation and never create a duplicate or terminal entry.
- Failure proves: Recovery loses evidence, broadens ownership, or strands duplicate artifact state.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Static lifecycle and filesystem fixtures.
- Required by milestone: M2

### T7. Governed revision binds old and new identities

- Covers: R30-R37; E6; BND-STATE-002, BND-AUTH-001, BND-AUTH-002, BND-TEMPORAL-001; INT-003
- Level: contract
- Command IDs: CMD1, CMD3, CMD10
- Fixture/setup: Revision-required, identical authoring retry, authorized pre-settlement correction, reopened pre-reliance active, ambiguous, and unsupported states.
- Steps: Resolve the authorizing finding or input change, bind the prior identity, revise, compute the new identity, and replay identical and changed retries.
- Expected result: Legal revision preserves prior evidence, creates one new identity, returns only the matching entry to review-required, and requires fresh review; changed retries stop.
- Failure proves: Revision invalidates history, bypasses review, or silently rebinds an attempt.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Static lifecycle fixtures.
- Required by milestone: M2

### T8. Implementation reliance and settlement ownership block unsafe revision

- Covers: R31-R42; E6, E7; BND-STATE-001, BND-STATE-002, BND-AUTH-001, BND-RECOVERY-001; INT-003
- Level: contract
- Command IDs: CMD3, CMD10, CMD11
- Fixture/setup: Active test specs with and without implementation reliance, current peer review, stale review, and workflow-managed routing.
- Steps: Attempt ordinary revision, peer settlement, workflow mutation, and handoff claims under each authority state.
- Expected result: Relied-on active state requires separate reopen or migration; test-spec ends at review-required; only test-spec-review settles active; workflow routes without rewriting content or review evidence.
- Failure proves: Authoring can change an active proof contract or usurp peer/workflow authority.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Static lifecycle and review fixtures.
- Required by milestone: M2

### T9. Claim and external-action boundaries remain narrow

- Covers: R14, R21, R38-R42, R56; BND-STATE-001, BND-AUTH-001, BND-ENV-001
- Level: contract
- Command IDs: CMD2, CMD3
- Fixture/setup: Portable, governed, workflow-managed, and user-wording fixtures that request broader readiness or action.
- Steps: Complete authoring and inspect result, handoff, and side effects.
- Expected result: The skill claims only proof-map authoring and review-required handoff; it never claims implementation, validation, verification, branch, PR, release, deployment, or publication readiness.
- Failure proves: Simplification broadens authority or claims.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Focused skill-validator fixtures.
- Required by milestone: M2

### T10. Five assets compose complete output without duplicate bodies

- Covers: R43-R48; E8; BND-COMPOSE-002; INT-004
- Level: contract
- Command IDs: CMD2-CMD6
- Fixture/setup: Full creation and bounded revisions of cases, coverage maps, commands, and milestone proof rows.
- Steps: Compose output from the skeleton and applicable smaller assets, then scan headings, tables, bodies, insertion points, and placeholders.
- Expected result: The skeleton owns document structure, each smaller asset owns its repeated body, bounded revision loads only affected structure, and no body or placeholder is duplicated.
- Failure proves: Structural ownership is incomplete or assets contain policy.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Focused skill and build tests.
- Required by milestone: M2

### T11. Missing assets and boundary resources fail safely

- Covers: R1-R7, R43-R48; E8, E11; BND-COMPOSE-001, BND-COMPOSE-002, BND-RECOVERY-002; INT-005
- Level: integration
- Command IDs: CMD2-CMD6
- Fixture/setup: Missing, unreadable, escaped, transformed, contradictory, and mixed-version resource fixtures.
- Steps: Trigger each resource and attempt dependent interpretation or composition.
- Expected result: Required-resource failure stops before dependent work and the skill never reconstructs remembered procedure or ad hoc structure.
- Failure proves: A smaller main file masks an incomplete package.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Existing mapping, containment, and build tests.
- Required by milestone: M2

### T12. Automated, manual, and hybrid proof retain current semantics

- Covers: R48-R51; E9, E10; BND-COMPOSE-002, BND-COMPAT-001; INT-004
- Level: contract
- Command IDs: CMD3
- Fixture/setup: Automated, manual, and hybrid proof obligations using the existing proof, case, milestone, and optional Manual QA structures.
- Steps: Render each mode and validate applicability, fields, evidence, procedure IDs, and asset inventory.
- Expected result: Automated proof omits manual IDs; manual and hybrid proof cite current required procedure and evidence fields; no manual-proof contract, conditional asset group, or sixth asset appears.
- Failure proves: Simplification adds ceremony or removes supported manual evidence.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Focused static fixtures.
- Required by milestone: M2

### T13. Rule and literal inventories are complete and fail closed

- Covers: R52-R55; BND-INPUT-001, BND-COMPAT-001; INT-004
- Level: contract
- Command IDs: CMD1, CMD3
- Fixture/setup: Complete rule and literal ledgers plus unknown, missing, duplicate, and empty-field fixtures and real exact-string consumer searches.
- Steps: Validate vocabulary before consistency and reconcile every current semantic rule, duplicate cluster, literal, and consumer.
- Expected result: Every rule and literal has one valid treatment; unknown values fail first; incidental assertions do not become prose owners.
- Failure proves: Behavior can disappear or accidental wording can block simplification.
- Evidence artifact: `evidence/m1-preservation-inventories.md`
- Automation location: Change-local standard-library proof and MP0.
- Required by milestone: M1

### T14. Scenarios and profile accounting are deterministic and honest

- Covers: R54-R61; E12; BND-COMPAT-001; INT-004
- Level: integration
- Command IDs: CMD1, CMD3
- Fixture/setup: Baseline and final LF-normalized canonical resources, every required scenario, both profiles, full-create and bounded-revision assemblies, and duplicate clusters.
- Steps: Validate scenario inventory and count each unique resource once in documented order using words and UTF-8 bytes.
- Expected result: Every valid and invalid outcome is represented, both procedural profiles shrink, total package and assets are separate, and no fixed percentage or token estimate overrides preservation.
- Failure proves: Relocation or selective metrics are misrepresented as simplification.
- Evidence artifact: `evidence/simplification-measurements.md`
- Automation location: Change-local scenario and measurement proof.
- Required by milestone: M3

### T15. Package-chain resources retain exact parity

- Covers: R1-R6, R62; BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001; INT-005
- Level: integration
- Command IDs: CMD4-CMD8
- Fixture/setup: Canonical, generated, packed, archived, and clean-installed targets, including missing and transformed resource fixtures.
- Steps: Build temporary targets, select test-spec directly, and compare required paths and raw bytes.
- Expected result: Every target contains the governed reference, both boundary references, and five assets exactly; partial rollout and drift fail.
- Failure proves: Release packaging can omit or alter required resources.
- Evidence artifact: `evidence/m3-package-proof.md`
- Automation location: Existing build and adapter tests plus temporary package proof.
- Required by milestone: M3

### T16. Acceptance and architecture remain bounded

- Covers: R52-R62; E12; BND-COMPAT-001, BND-ENV-001
- Level: contract
- Command IDs: CMD1-CMD11
- Fixture/setup: Final package, ledgers, scenarios, measurements, architecture assessment, and proposals for a new runtime, package class, state owner, or permanent validator.
- Steps: Compare final semantics to approved artifacts, verify architecture triggers, and inspect every acceptance command and durable validator change.
- Expected result: Existing architecture remains sufficient unless its explicit triggers occur, semantic review approves, and no target runtime, tokenizer, new validator family, or external action is added.
- Failure proves: The refactor exceeded its approved architecture or proof boundary.
- Evidence artifact: `evidence/semantic-preservation-review.md`
- Automation location: Deterministic checks plus MP1.
- Required by milestone: M3 and M4

## Fixtures and data

M1 creates JSON-compatible YAML ledgers and static scenario records under the owning change root. Scenarios cover both profiles, candidate validation, every creation interruption, identical and stale retries, same-entry restart with partial-byte variants, every legal and illegal revision state, settlement boundaries, full and bounded composition, missing resources, automated/manual/hybrid proof, forbidden writes, and unknown vocabulary. Existing repository fixtures remain the owners of skill parsing, boundary validation, lifecycle metadata, build output, and adapter packaging.

## Mocking/stubbing policy

Use static filesystem and lifecycle fixtures plus temporary package directories only. Do not mock an agent runtime or infer semantic behavior from transcripts. Authority fixtures must provide explicit current identities and state rather than caller assertions.

## Migration or compatibility tests

T8 and T12-T15 prove historical review preservation, current optional manual-verification behavior, literal migration, unchanged boundary resources, and canonical-through-installed raw-byte parity. Rollback restores the prior complete package and directly coupled consumers atomically; mixed versions are invalid.

## Observability verification

Change-local evidence records operation identities, profile inputs, measurements, command results, rule and literal treatments, semantic-review conclusions, and package paths. No production logs, metrics, traces, or audit service is introduced.

## Security/privacy verification

All proof is repository-local. Temporary package roots are removed, network and publication are excluded, and fixtures contain no secrets or personal data.

## Performance checks

Loaded-profile UTF-8 bytes and Unicode whitespace-separated words are the only required performance proxies. Token estimates and runtime benchmarks are out of scope unless an existing pinned repository implementation already supports the exact assembly.

## Manual QA checklist

### MP0. Pre-movement semantic and literal inventory audit

- Manual procedure ID: MP0
- Automation rationale: Exact-string checks cannot decide semantic equivalence, normative ownership, or whether similar passages encode distinct rules.
- Required environment: Tracked M1 baseline with the complete current test-spec package and bounded consumers.
- Steps: Read the full package, group every significant rule and duplicate cluster, search all consumers for exact dependencies, and reconcile each item to one valid ledger row before prose moves.
- Evidence artifact: `docs/changes/2026-08-13-test-spec-skill-simplification/evidence/m1-preservation-inventories.md`
- Pass condition: Every rule, duplicate, literal, source, consumer, and intended owner has one supported treatment.
- Failure condition: Any material rule or consumer is missing, duplicated, ambiguous, or unsupported.
- Owning stage: Implement M1 before M1 code-review.

### MP1. Final semantic preservation and ownership review

- Manual procedure ID: MP1
- Automation rationale: Validators cannot establish completeness of proof policy, lifecycle authority, recovery, composition, or claims.
- Required environment: Final package, ledgers, scenarios, measurements, approved artifacts, and package proof.
- Steps: Compare every rule with its destination; confirm portable completeness; validate candidate, creation, restart, revision, settlement, asset, optional manual-verification, boundary, failure, claim, and handoff behavior; and verify literal treatments and measurements.
- Evidence artifact: `docs/changes/2026-08-13-test-spec-skill-simplification/evidence/semantic-preservation-review.md`
- Pass condition: Every rule has one correct owner, both profiles remain usable, every write is authorized, and no unapproved semantic change exists.
- Failure condition: Any rule disappears, duplicates, loads behind the wrong trigger, broadens authority, or lacks direct evidence.
- Owning stage: Implement M3 before M3 code-review and final review.

## What not to test and why

- Do not execute or grade Codex, Claude Code, opencode, or another model runtime because this change refactors published guidance and deterministic resources.
- Do not add prompt journeys, transcript snapshots, runtime-version evidence, tokenizer dependencies, permanent size or prose validators, or a new semantic classifier.
- Do not test unrelated skills, redesign workflow stages, create a sixth test-spec asset, publish adapters, release packages, or open a pull request.
- Do not infer semantic boundary truth with deterministic validators; they validate approved record shape and exact IDs only.

## Uncovered gaps

None.

## Next artifacts

- Independent formal `test-spec-review`.
- Implementation M1 only after review approval and subsequent workflow routing.

## Follow-on artifacts

None yet

## Readiness

Active proof map ready for formal `test-spec-review`. This artifact does not claim implemented tests, validation success, implementation eligibility, verification, branch readiness, or PR readiness.
