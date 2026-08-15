<!-- Template: test-spec-skeleton-v1 -->

# Spec Skill Simplification Test Specification

## Owning change record

`docs/changes/2026-08-15-spec-skill-simplification/change.yaml`

## Related spec and plan

- Spec: `specs/spec-skill-simplification.md`
- Plan: `docs/plans/2026-08-15-spec-skill-simplification.md`
- Architecture/ADRs: `docs/changes/2026-08-15-spec-skill-simplification/architecture-assessment.md`; architecture not required under the existing mapped-skill package, boundary-first, and stage-owned lifecycle models

## Input artifact identities

| Input | Path | Artifact ID | Review evidence |
| --- | --- | --- | --- |
| Feature spec | `specs/spec-skill-simplification.md` | `spec` | `spec-review-r1`; `docs/changes/2026-08-15-spec-skill-simplification/reviews/spec-review-r1.md` |
| Architecture assessment | `docs/changes/2026-08-15-spec-skill-simplification/architecture-assessment.md` | not applicable | Recorded `architecture-not-required` assessment |
| Execution plan | `docs/plans/2026-08-15-spec-skill-simplification.md` | `plan` | `plan-review-r1`; `docs/changes/2026-08-15-spec-skill-simplification/reviews/plan-review-r1.md` |

## Testing strategy

Use deterministic contract fixtures for resource assemblies, tri-state governed signals, portable and governed operations, authoring retries, explicitly authorized stale restart, partial-content preservation, formal boundary-block transitions, compatibility, measurement, and missing resources. Existing validators own permanent skill, lifecycle, boundary, build, and adapter checks. Change-local ledgers, scenarios, representative outputs, and measurements prove semantic disposition, observable preservation, and actual loaded-context reduction. Ordinary lifecycle and PR review retain their existing judgment roles; no separate manual semantic-review acceptance stage or target-agent runtime is part of this proof map.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1-R9 | T1, T4, T12, T15 | contract | Package inventory, universal ownership, resource mapping, boundary ownership, skeleton ownership, and fail-safe loading. |
| R10-R20 | T2-T3 | contract | Tri-state signals, profile selection, operations, target state, portable isolation, and no failed-authority fallback. |
| R21-R29 | T5-T7 | contract | Governed authority, create, revise, commit, retry, collision, concurrency, and downstream reliance. |
| R30-R42 | T8-T11 | contract | Stale detection, explicit restart authority, partial-content preservation, bounded writes, idempotency, and architecture stop. |
| R43-R56 | T12-T14 | contract | Formal block and anchor states, adoption, preservation, deactivation, malformed structure, and review authority. |
| R57-R62 | T16 | contract | Separate rule and literal ledgers plus unknown-value-first validation. |
| R63-R65 | T17 | integration | Deterministic assembly measurement, complete reporting, and real-profile reduction. |
| R66-R67 | T15, T18 | integration | Canonical-through-installed parity and deterministic acceptance without target-agent or extra manual semantic-review gates. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | T1-T2 | SA0 portable creation loads the common procedure, both boundary references, and skeleton and writes no lifecycle state. |
| E2 | T2-T3 | Malformed ownership is an invalid governed signal and cannot become portable revision. |
| E3 | T3 | Multiple governed signals must resolve to the same exact change. |
| E4 | T3 | Governed reference loading precedes full authority validation and grants no mutation authority. |
| E5 | T5 | Governed creation commits only at `review-required`. |
| E6 | T7 | Identical partial and completed retries resume or no-op once. |
| E7 | T8 | Changed-basis detection reports stale state without starting restart. |
| E8 | T9-T10 | Current explicit authority permits same-entry restart only after nonempty bytes are preserved. |
| E9 | T10 | Unknown, unrelated, or competing partial content blocks restart. |
| E10 | T12 | New applicable specifications emit the complete formal block at the owned insertion point. |
| E11 | T13 | Grandfathered adoption requires unique ordered anchors or an authorized full rewrite. |
| E12 | T13 | Existing complete blocks remain absent explicit approved deactivation. |
| E13 | T14 | Incomplete, duplicate, or misplaced formal blocks fail closed. |
| E14 | T4 | Every required-resource integrity defect stops dependent work. |
| E15 | T17 | Loaded profiles, resources, output, and total package are reported separately. |

## Proof map

Boundary model version: boundary-first-v1
Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R49, R50, R51, R52, R53, R54, R55, R56, R57, R58, R59, R60, R61, R62, R63, R64, R65, R66, R67

| Proof obligation ID | Coverage state | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Proof level | Automation mode | Command IDs | Evidence artifact | Required milestone | Manual procedure IDs | Uncovered gap ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRF-001 | covered | R10, R11, R12, R13, R14, R15, R16, R17, R18 | BND-INPUT-001 | T2, T3 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-002 | covered | R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R49, R50, R51, R52, R53, R54, R55 | BND-STATE-001 | T5-T14 | contract | automated | CMD1, CMD3, CMD9 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-003 | covered | R10, R11, R12, R13, R14, R15, R20, R21, R22, R25, R27, R30, R31, R32, R33, R34, R38, R39, R40, R41, R42, R49, R52, R56 | BND-AUTH-001 | T3, T5, T6, T8-T10, T13 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-004 | covered | R1, R2, R3, R4, R5, R6, R7, R8, R9, R43, R44, R45, R46, R47, R48, R49, R50, R51, R52, R53, R54, R55, R56 | BND-COMPOSE-001 | T1, T4, T12-T15 | integration | automated | CMD2-CMD9 | `evidence/m2-package-implementation.md`; `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-005 | covered | R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41 | BND-TEMPORAL-001 | T7-T10 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-006 | covered | R5, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R49, R53, R54 | BND-RECOVERY-001 | T4, T7-T11, T13-T14 | contract | automated | CMD1-CMD3, CMD9 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-007 | covered | R43, R44, R45, R46, R47, R48, R49, R50, R51, R52, R53, R54, R55, R56, R57, R58, R59, R60, R61, R62, R63, R64, R65, R66 | BND-COMPAT-001 | T12-T17 | integration | automated | CMD1-CMD9 | `evidence/m1-preservation-inventories.md`; `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-008 | covered | R5, R36, R37, R38, R42, R66, R67 | BND-ENV-001 | T4, T9-T10, T15, T18 | integration | automated | CMD2, CMD4-CMD9 | `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-009 | covered | R10, R11, R12, R13, R14, R15 | INT-001 | T2-T3 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-010 | covered | R30, R31, R32, R33, R34, R38, R39, R40, R41 | INT-002 | T8-T10 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-011 | covered | R49, R52 | INT-003 | T13 | contract | automated | CMD3, CMD9 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-012 | covered | R66 | INT-004 | T15, T17-T18 | integration | automated | CMD1-CMD9 | `evidence/m3-package-proof.md` | M3 | - | - |

## Edge case coverage

| Edge case | Covered by | Expected handling |
| --- | --- | --- |
| Conversational change mention without structured identity | T2-T3 | Remain portable when the portable target is valid; do not infer authority. |
| Structured pointer is malformed, stale, unsafe, escaped, or points to a missing root | T3 | Return invalid or ambiguous governed signal and stop without portable fallback. |
| Multiple valid signals agree or disagree | T3 | One exact shared change becomes a candidate; disagreement stops. |
| Portable create targets an existing file or revision targets an absent file | T2 | Stop and name the correct explicit operation. |
| Creation or revision is interrupted at each durable step | T5-T7 | Resume only the identical transaction or return idempotent success. |
| Governing basis changes during partial authoring | T8 | Report `stale-authoring-attempt` without overwrite or pointer update. |
| Restart request is absent, stale, or names another attempt | T9 | Stop before restart and record no new evidence. |
| Matching partial file is absent, zero bytes, nonempty, unknown, or unrelated | T10 | Record absence or empty identity, preserve matching nonempty bytes, and stop on every unattributable or unpreservable state. |
| Entry reaches `review-required` before restart | T11 | Return idempotent completed success and do not restart. |
| Grandfathered spec has one, duplicate, or misordered anchors | T13-T14 | Require authorized full rewrite or stop; never insert ad hoc. |
| Existing complete block becomes currently non-applicable | T13 | Preserve it unless explicit approved deactivation includes downstream-impact handling. |
| Required reference is missing, unreadable, escaped, contradictory, or mixed | T4, T15 | Stop dependent work without remembered reconstruction. |
| Total package grows while both loaded profiles shrink | T17 | Report and justify total growth without failing solely on percentage. |
| Derived package omits or transforms one mapped resource | T15 | Fail path and raw-byte parity even when canonical validation passes. |
| New closed vocabulary receives an unknown value | T16 | Reject the unknown value before consistency checks. |

## Validation commands

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMD1 | `python -c 'import json; from pathlib import Path; root=Path("docs/changes/2026-08-15-spec-skill-simplification"); load=lambda path: json.loads(path.read_text(encoding="utf-8")); rules=load(root/"spec-rule-disposition.yaml")["rules"]; literals=load(root/"spec-literal-compatibility.yaml")["literals"]; scenarios=load(root/"fixtures/scenario-contracts.yaml")["scenarios"]; bad_rule=load(root/"fixtures/invalid-rule-disposition.yaml"); bad_literal=load(root/"fixtures/invalid-literal-classification.yaml"); rd={"retained-inline","retained-governed-reference","retained-boundary-reference","asset-owned","removed-duplicate","removed-obsolete-with-approved-contract-change"}; lc={"normative-contract","parser-or-package-contract","test-only-incidental","historical-fixture","obsolete"}; rf={"rule_id","source_locations","behavior","governing_requirements","applicable_profiles","disposition","destination","preservation_proof"}; lf={"literal_id","literal","source_location","consumers","classification","required_semantics","disposition","replacement"}; vr=lambda row: ["unknown-disposition"] if row.get("disposition") not in rd else (["missing-required-fields"] if not rf <= row.keys() else []); vl=lambda row: ["unknown-classification"] if row.get("classification") not in lc else (["missing-required-fields"] if not lf <= row.keys() else []); assert rules and literals and scenarios; assert all(vr(row)==[] for row in rules); assert all(vl(row)==[] for row in literals); assert vr(bad_rule)[0]=="unknown-disposition"; assert vl(bad_literal)[0]=="unknown-classification"; assert len({row["rule_id"] for row in rules})==len(rules); assert len({row["literal_id"] for row in literals})==len(literals); assert len({row["scenario"] for row in scenarios})==len(scenarios); print(f"rules={len(rules)} literals={len(literals)} scenarios={len(scenarios)} unknown_values=rejected-first")'` | planned-for-implementation | implement | M1 | M1 code-review | Reject unknown values first, then missing fields, duplicates, or scenario drift. | Not applicable; every assertion executes. | `evidence/m1-preservation-inventories.md` | Repository-local reads only; no network or target-agent runtime. |
| CMD2 | `python scripts/validate-skills.py skills/spec/SKILL.md` | existing/configured | implement | M2 | M2 code-review | Block normalized structure, mapping, containment, placeholder, or claim defects. | Not applicable. | `evidence/m2-package-implementation.md` | Read-only repository validation. |
| CMD3 | `python scripts/test-skill-validator.py SpecSkillSimplificationTests` | planned-for-implementation | implement | M2 | M2 code-review | Block assembly, classification, operation, transaction, recovery, structure, or failure defects. | Zero discovered tests is failure. | `evidence/m2-package-implementation.md` | Repository-local tests; no target-agent runtime. |
| CMD4 | `python scripts/test-skill-validator.py` | existing/configured | implement | M2 | M2 code-review | Block broad skill-contract regression. | Zero discovered tests is failure. | `evidence/m2-package-implementation.md` | Repository-local tests; no target-agent runtime. |
| CMD5 | `python scripts/test-build-skills.py` | existing/configured | implement | M2 | M2 code-review | Block generated inventory or resource regression. | Zero discovered tests is failure. | `evidence/m2-package-implementation.md` | Temporary filesystem only. |
| CMD6 | `python scripts/build-skills.py --check` | existing/configured | implement | M2 | M2 code-review | Block generated-skill drift or missing resources. | Not applicable. | `evidence/m2-package-implementation.md` | Read-only check against canonical sources. |
| CMD7 | `python scripts/test-adapter-distribution.py` | existing/configured | implement | M3 | M3 code-review | Block adapter generation, archive, install, or parity regression. | Zero discovered tests is failure. | `evidence/m3-package-proof.md` | Temporary files only; no publication or network. |
| CMD8 | `python -c 'exec("""import subprocess, sys, tempfile\nversion = "v0.4.0"\nwith tempfile.TemporaryDirectory(prefix="rigorloop-adapters-") as output:\n    subprocess.run([sys.executable, "scripts/build-adapters.py", "--version", version, "--output-dir", output], check=True)\n    subprocess.run([sys.executable, "scripts/validate-adapters.py", "--version", version, "--adapter-root", output, "--clean-install-smoke", "--skill", "spec"], check=True)""")'` | existing/configured | implement | M3 | M3 code-review | Block generated, archived, release-candidate, or installed resource mismatch. | Not applicable; all supported targets are selected. | `evidence/m3-package-proof.md` | Fresh temporary directory; no publication, network, or agent execution. |
| CMD9 | `python scripts/validate-boundary-first.py --check --path specs/spec-skill-simplification.md` | existing/configured | implement | M2 | M2 code-review | Block invalid or missing proof for any boundary or interaction. | Not applicable; the matching proof map is mandatory. | `evidence/m2-package-implementation.md` | Read-only repository validation. |
| CMD10 | `python scripts/validate-change-metadata.py docs/changes/2026-08-15-spec-skill-simplification/change.yaml` | existing/configured | workflow | lifecycle | Every state-changing handoff | Block invalid artifact, review, or planned-work state. | Not applicable. | Owning change validation ledger | Read-only validation. |
| CMD11 | `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-08-15-spec-skill-simplification` | existing/configured | review stages | lifecycle | Every formal review handoff | Block malformed or missing review evidence. | Not applicable. | Review log and records | Read-only validation. |

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | T16-T17 | none | CMD1, CMD10 | `evidence/profile-size-baseline.md`; `evidence/m1-preservation-inventories.md` | M1 code-review | Canonical package remains unchanged while ownership, scenarios, and baselines are frozen. |
| M2 | T1-T16 | none | CMD2-CMD6, CMD9-CMD11 | `evidence/m2-package-implementation.md` | M2 code-review | Focused failing assertions precede the atomic canonical package, recovery, and structural changes. |
| M3 | T15-T18 | none | CMD1-CMD11 | `evidence/simplification-measurements.md`; `evidence/semantic-preservation-review.md`; `evidence/m3-package-proof.md` | M3 code-review and final review | Proves loaded-profile reduction, semantic preservation, boundary coverage, and package parity. |
| M4 | T18 | none | CMD1-CMD11 | Final review, explanation, and verify evidence | verify | Lifecycle closeout begins only after M1-M3 and required review resolution are closed. |

## Test cases

### T1. Loaded assemblies and resource ownership are closed

- Covers: R1-R9; E1; BND-COMPOSE-001
- Level: contract
- Command IDs: CMD2-CMD5
- Fixture/setup: SA0 and SA1 trigger fixtures plus forbidden, duplicate, missing, and mixed-version load combinations.
- Steps: Classify each invocation, assemble unique resources in documented order, and inspect resource maps and ownership assertions.
- Expected result: Exactly two valid assemblies exist; both load the two boundary references once, SA1 alone loads the governed reference, the skeleton is copied only for output, and each rule or structure has one owner.
- Failure proves: Progressive disclosure changes authority, duplicates policy, or admits an unsupported package profile.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: `scripts/test-skill-validator.py` focused fixtures and `validate-skills.py`.
- Required by milestone: M2

### T2. Portable create and revise use exact file state only

- Covers: R10-R19; E1-E2; EC1-EC2; BND-INPUT-001; INT-001
- Level: contract
- Command IDs: CMD3
- Fixture/setup: Absent, existing, ambiguous, and conflicting portable targets with and without conversational change wording.
- Steps: Classify signals, request each explicit operation, and inspect resolved writes.
- Expected result: Only no signal permits portable authoring, create accepts only an absent exact path, revise accepts only an existing exact path, invalid targets stop, and successful portable authoring writes only the spec artifact.
- Failure proves: Portable authoring depends on lifecycle state, ignores a governed signal, reclassifies operations, or mutates governed surfaces.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Focused signal and portable-operation fixtures.
- Required by milestone: M2

### T3. Governed signals and authority fail closed independently

- Covers: R10-R20; E2-E4; EC2-EC5; BND-INPUT-001, BND-AUTH-001; INT-001
- Level: contract
- Command IDs: CMD3
- Fixture/setup: Valid, malformed, duplicated, escaped, stale, missing-root, agreeing, and conflicting signals plus invalid lifecycle and authoring states.
- Steps: Classify signals, select resources for one candidate, then independently validate the complete governed authority record.
- Expected result: Invalid or ambiguous signals stop before a profile, one agreeing candidate loads the governed reference, only complete authority permits mutation, and every validation defect stops without portable fallback.
- Failure proves: Invalid ownership disappears during classification or loading and mutation authority are conflated.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Focused candidate and authority fixtures.
- Required by milestone: M2

### T4. Required resources fail safely

- Covers: R1-R9; E14; EC14; BND-COMPOSE-001, BND-RECOVERY-001, BND-ENV-001
- Level: integration
- Command IDs: CMD2-CMD5, CMD8
- Fixture/setup: Missing, unreadable, escaped, contradictory, stale, and mixed-version boundary references, governed reference, or skeleton plus untriggered governed-reference controls.
- Steps: Activate each dependent path and attempt judgment, authoring, or output composition.
- Expected result: Every required-resource defect stops before dependent work, no procedure or layout is reconstructed from memory, and an untriggered governed reference is not loaded.
- Failure proves: The shortened common path can partially recreate or bypass required procedure.
- Evidence artifact: `evidence/m2-package-implementation.md`; `evidence/m3-package-proof.md`
- Automation location: Resource-map, package, and focused failure fixtures.
- Required by milestone: M2 and M3

### T5. Governed creation commits only at review-required

- Covers: R21-R24; E5; BND-STATE-001, BND-AUTH-001
- Level: contract
- Command IDs: CMD3
- Fixture/setup: Authorized absent entry and file plus interruptions before entry, after entry, after content, and before complete evidence.
- Steps: Bind identities, create the exact authoring entry, write and validate content, record identity and evidence, and perform the final transition.
- Expected result: Only the matching entry, spec file, and spec-owned evidence change, and `review-required` is the sole commit point.
- Failure proves: Creation adopts unrelated state, publishes incomplete evidence, or mutates another lifecycle surface.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Static ordered-write fixtures.
- Required by milestone: M2

### T6. Governed revision preserves history and requires fresh review

- Covers: R25-R27; BND-STATE-001, BND-AUTH-001
- Level: contract
- Command IDs: CMD3
- Fixture/setup: Legal review finding, upstream change, explicit reopen, stale reopen, settled spec without reliance, and spec with downstream reliance.
- Steps: Bind the prior identity and revision authority, attempt the revision, and inspect evidence and entry state.
- Expected result: Prior records remain historical, only the authorized current review mapping is cleared, new content receives a new identity, and downstream reliance blocks until workflow impact handling establishes legal reopen authority.
- Failure proves: Revision invalidates history or changes an in-use proof contract without owned staleness handling.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Focused governed-revision fixtures.
- Required by milestone: M2

### T7. Exact retries resume or no-op without duplication

- Covers: R28-R29; E6; BND-STATE-001, BND-TEMPORAL-001, BND-RECOVERY-001
- Level: contract
- Command IDs: CMD3
- Fixture/setup: Every partial creation and revision step, completed operation, mismatched path, unrelated asymmetry, stale authority, multiple candidates, and concurrent-write states.
- Steps: Replay the original or changed transaction identity.
- Expected result: Exact partial work resumes from the first incomplete step, exact completion is idempotent, and every mismatch stops without adoption or overwrite.
- Failure proves: Retry silently rebinds identity, duplicates evidence, or corrupts competing work.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Static retry and collision fixtures.
- Required by milestone: M2

### T8. Stale detection grants no restart authority

- Covers: R30-R32; E7; EC6, EC9; BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001, BND-RECOVERY-001; INT-002
- Level: contract
- Command IDs: CMD3
- Fixture/setup: Changed input basis with no restart request, a current user request, a same-change workflow handoff, stale authority, and another-attempt authority.
- Steps: Detect stale state, inspect writes, then classify separate restart authority.
- Expected result: Detection reports `stale-authoring-attempt` and writes nothing; only a current request naming the exact stale attempt and new basis permits restart validation.
- Failure proves: Diagnosis or routing silently authorizes destructive recovery.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Static stale and authority fixtures.
- Required by milestone: M2

### T9. Restart validates identity, no reliance, and a bounded write set

- Covers: R31-R34, R38-R40, R42; E8; EC9; BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001, BND-RECOVERY-001; INT-002
- Level: contract
- Command IDs: CMD1, CMD3, CMD10
- Fixture/setup: Valid restart plus changed artifact, path, old basis, new basis, state, review reliance, downstream reliance, competition, or requested write surface.
- Steps: Validate authority and evidence, attempt the exact restart, and compare every durable field.
- Expected result: Only the canonical spec, new authoring evidence, matching evidence pointer, and required snapshot may change; entry identity and `authoring` state remain; every mismatch stops.
- Failure proves: Restart broadens spec authority, crosses lifecycle ownership, or introduces an unapproved architecture mechanism.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Lifecycle metadata and forbidden-write fixtures.
- Required by milestone: M2

### T10. Partial-content disposition is deterministic and non-destructive

- Covers: R34-R38; E8-E9; EC7-EC8; BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001, BND-RECOVERY-001; INT-002
- Level: contract
- Command IDs: CMD3
- Fixture/setup: Absent file, zero-byte matching file, nonempty matching file, unknown identity, unrelated content, competing changes, and unavailable snapshot path.
- Steps: Classify content, prepare evidence, and attempt replacement.
- Expected result: Absence and empty identity are recorded, every matching nonempty file is snapshotted byte-for-byte with a hash before replacement, and every unattributable or unpreservable state stops unchanged.
- Failure proves: Restart discards user-authored bytes or adopts unrelated content.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Temporary filesystem content fixtures.
- Required by milestone: M2

### T11. Restart completion remains authoring and is idempotent

- Covers: R39-R42; EC10; BND-STATE-001, BND-TEMPORAL-001, BND-RECOVERY-001
- Level: contract
- Command IDs: CMD3, CMD10
- Fixture/setup: Successful restart at `authoring`, ordinary completion to `review-required`, replay before completion, replay after completion, and attempted new lifecycle state or schema.
- Steps: Reconcile each retry and validate metadata.
- Expected result: Restart leaves `authoring`, ordinary authoring owns completion, already completed work returns idempotent success, and any need for a new state, schema, or owner stops for architecture and contract revision.
- Failure proves: Restart settles its own work, duplicates evidence, or hides an architecture change.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Static lifecycle and idempotency fixtures.
- Required by milestone: M2

### T12. Formal boundary structure has one composition owner

- Covers: R43-R48; E10; BND-STATE-001, BND-COMPOSE-001, BND-COMPAT-001
- Level: contract
- Command IDs: CMD2-CMD3, CMD9
- Fixture/setup: Current skeleton, required and non-applicable output, and zero, one, duplicate, or misplaced insertion positions.
- Steps: Compose output from the skeleton and feature-authoring reference and inspect headings and ownership.
- Expected result: The skeleton owns one insertion point after error behavior and before compatibility, the feature reference owns exactly four contiguous headings and tables, and resource loading does not itself determine emission.
- Failure proves: Layout policy is duplicated, formal structure is incomplete, or loading and applicability are conflated.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Skeleton, resource, and boundary validator fixtures.
- Required by milestone: M2

### T13. Grandfathered adoption and deactivation are explicit

- Covers: R47-R52, R55-R56; E11-E12; EC11-EC13; BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, BND-COMPAT-001; INT-003
- Level: contract
- Command IDs: CMD3, CMD9
- Fixture/setup: Grandfathered documents with unique ordered, missing, duplicated, or misordered anchors plus complete blocks under required and non-applicable states with and without approved deactivation.
- Steps: Classify anchors and applicability, attempt insertion, full rewrite, preservation, update, or removal, and inspect stable IDs and history.
- Expected result: Unique anchors allow bounded insertion, missing valid anchors require authorized full rewrite or stop, complete blocks persist absent explicit approved deactivation, and `spec-review` retains substantive-revision classification authority.
- Failure proves: Historical structure is rewritten ad hoc or stable boundary content disappears implicitly.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Static compatibility and authority fixtures.
- Required by milestone: M2

### T14. Malformed or unresolved formal boundary state fails closed

- Covers: R46-R56; E13; EC11, EC13; BND-STATE-001, BND-COMPOSE-001, BND-RECOVERY-001, BND-COMPAT-001
- Level: contract
- Command IDs: CMD3, CMD9
- Fixture/setup: Incomplete, duplicated, misplaced, applicability-unresolved, partial-authority, and placeholder-bearing formal blocks.
- Steps: Request revision and inspect structural and lifecycle writes.
- Expected result: Every malformed or unresolved state stops before writing, no duplicate or ad hoc block is inserted, and explicit structural correction remains separately authorized.
- Failure proves: Revision can normalize ambiguous contract structure silently.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Boundary and skeleton failure fixtures.
- Required by milestone: M2

### T15. Canonical and derived packages retain complete resource parity

- Covers: R1-R5, R66; E14; EC14; BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001; INT-004
- Level: integration
- Command IDs: CMD2, CMD4-CMD8
- Fixture/setup: Canonical package and freshly generated, packed, archived, release-candidate, and installed adapter trees.
- Steps: Validate mapping, build packages, select `spec`, and compare every required relative path and raw byte.
- Expected result: Every supported target contains the governed reference, both boundary references, and skeleton exactly once at required paths and bytes; missing, transformed, escaped, stale, additional, or mixed resources fail.
- Failure proves: Canonical success does not guarantee a complete published package.
- Evidence artifact: `evidence/m3-package-proof.md`
- Automation location: Existing skill, build, and adapter distribution tests.
- Required by milestone: M3

### T16. Semantic-rule and literal inventories remain separate and closed

- Covers: R57-R62; EC15; BND-COMPAT-001
- Level: contract
- Command IDs: CMD1
- Fixture/setup: Complete valid ledgers and scenarios plus unknown disposition and classification fixtures, duplicate IDs, parser consumers, incidental tests, and historical fixtures.
- Steps: Validate closed values first, required fields, unique IDs, destination ownership, atomic consumer treatment, and preservation proof.
- Expected result: Every significant rule and duplicate cluster has one destination, every literal consumer has one classification, unknown values fail before consistency, and incidental tests do not freeze prose.
- Failure proves: Semantic behavior or true compatibility can disappear without trace or tests can become policy owners.
- Evidence artifact: `evidence/m1-preservation-inventories.md`
- Automation location: Change-local standard-library assertion command.
- Required by milestone: M1

### T17. Measurements prove real loaded-context reduction

- Covers: R63-R65; E15; BND-COMPAT-001; INT-004
- Level: integration
- Command IDs: CMD1
- Fixture/setup: Before and after canonical resources assembled in documented order with LF normalization and unique-file counting.
- Steps: Measure SA0, SA1, `SKILL.md`, each reference, skeleton, representative copied output, duplicate clusters, mapped-resource count, and total package.
- Expected result: Both real loaded profiles use fewer words and bytes, total package change remains separately visible, and no fixed percentage overrides semantic preservation.
- Failure proves: File splitting or relocation is misreported as simplification.
- Evidence artifact: `evidence/simplification-measurements.md`; `evidence/semantic-preservation-review.md`
- Automation location: Change-local deterministic measurement and inventory assertions.
- Required by milestone: M3

### T18. Final deterministic acceptance excludes target-agent and extra manual gates

- Covers: R66-R67; BND-ENV-001; INT-004
- Level: smoke
- Command IDs: CMD1-CMD11
- Fixture/setup: Completed M1-M3 package and evidence with every approved boundary and interaction mapped.
- Steps: Run the complete command ledger, lifecycle and review validation, and final boundary proof; retain ordinary review stages without creating a new manual procedure.
- Expected result: Contract, scenarios, packages, parity, preservation, and measurements pass without executing or grading Codex, Claude Code, opencode, or another target runtime and without another manual semantic-review acceptance stage.
- Failure proves: Acceptance is incomplete or depends on a nondeterministic or unapproved review mechanism.
- Evidence artifact: `evidence/m3-package-proof.md`; final review and verify evidence
- Automation location: Existing repository validators; human PR review remains outside this test procedure.
- Required by milestone: M3 and M4

## Fixtures and data

- Change-local JSON-compatible YAML ledgers for semantic rules and literal consumers.
- Change-local scenarios for assemblies, signals, operations, transactions, retries, stale restart, partial content, formal block states, resource failure, compatibility, and forbidden writes.
- Existing controlled skill fixtures and generated adapter fixtures extended only where focused `spec` coverage is absent.
- Representative SA0 and SA1 outputs plus partial, stale, conflicting, malformed, and completed transaction states.

## Mocking/stubbing policy

Use temporary filesystem fixtures for spec targets, change records, authoring evidence, restart authority, partial-content snapshots, conditional resources, generated adapters, and interrupted writes. Do not mock away public skill/resource assembly, signal classification, stage-owned authority, boundary-block composition, or `spec-review` handoff. No network, hosted service, target-agent runtime, publication, or external state mutation is required.

## Migration or compatibility tests

T12-T14 prove new and grandfathered formal-block structure, stable IDs, explicit deactivation, and malformed-state stops. T16 proves semantic/literal separation, atomic parser or package migration, incidental-test updates, and historical readability. T15 proves package migration is atomic across canonical and every derived target. Historical specs and review evidence are never rewritten solely for this change.

## Observability verification

T3, T5-T14, and T17 verify visible classification, entry transitions, transaction results, blockers, restart authority, content disposition, boundary structure, and size accounting. No telemetry is introduced.

## Security/privacy verification

T3-T4, T8-T11, T15, and T18 prove exact mutation authority, fail-safe resources, non-destructive recovery, bounded writes, absence of secrets or machine-local requirements, bounded temporary filesystem use, and no network or target-runtime dependency.

## Performance checks

SA0 and SA1 LF-normalized words and UTF-8 bytes are the required portable context metrics. Resource, representative output, and total package sizes are reported separately. No wall-clock, tokenizer, or target-runtime benchmark is required.

## Manual QA checklist

None. Deterministic proof owns test acceptance; ordinary lifecycle review and human PR review retain their normal roles and are not represented as a new manual QA procedure.

## What not to test and why

- Do not execute or grade a target-agent runtime; this is a deterministic content and package refactor.
- Do not add a permanent tokenizer, prose classifier, spec artifact validator, or simplicity validator; change-local evidence and existing owners are sufficient.
- Do not turn ordinary reviewer judgment into a scripted manual acceptance procedure or pre-implementation gate.
- Do not test publication, release, deployment, network, or destructive Git behavior because those systems do not change.
- Do not rewrite historical specs or test them as newly emitted output.
- Do not test another skill's independent optimization in this change.

## Uncovered gaps

None.

## Next artifacts

`test-spec-review`, then M1 implementation and code review if the proof map is approved.

## Follow-on artifacts

None yet.

## Readiness

Ready for independent `test-spec-review`. This proof map does not claim peer approval, implementation readiness, validation success, verification, branch readiness, or PR readiness.
