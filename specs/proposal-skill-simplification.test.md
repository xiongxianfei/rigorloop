<!-- Template: test-spec-skeleton-v1 -->

# Proposal Skill Simplification Test Specification

## Owning change record

`docs/changes/2026-08-14-proposal-skill-simplification/change.yaml`

## Related spec and plan

- Spec: `specs/proposal-skill-simplification.md`
- Plan: `docs/plans/2026-08-14-proposal-skill-simplification.md`
- Architecture/ADRs: `docs/changes/2026-08-14-proposal-skill-simplification/architecture-assessment.md`; architecture not required under the existing mapped-skill package and stage-owned lifecycle models

## Input artifact identities

| Input | Path | Artifact ID | Review evidence |
| --- | --- | --- | --- |
| Feature spec | `specs/proposal-skill-simplification.md` | `spec` | `spec-review-r1`; `docs/changes/2026-08-14-proposal-skill-simplification/reviews/spec-review-r1.md` |
| Architecture assessment | `docs/changes/2026-08-14-proposal-skill-simplification/architecture-assessment.md` | not applicable | Recorded `architecture-not-required` assessment |
| Execution plan | `docs/plans/2026-08-14-proposal-skill-simplification.md` | `plan` | `plan-review-r1`; `docs/changes/2026-08-14-proposal-skill-simplification/reviews/plan-review-r1.md` |

## Testing strategy

Use deterministic contract fixtures for loaded assemblies, portable and governed operations, authoring retries, stale-reset authorization, strategic predicates, structural composition, compatibility, measurement, and missing resources. Existing validators own permanent skill, lifecycle, boundary, build, and adapter checks. Change-local ledgers, scenarios, representative outputs, and measurements prove semantic disposition, observable preservation, and actual loaded-context reduction. Ordinary proposal review, code review, and human PR review retain their existing judgment roles; no separate manual semantic-review acceptance stage or target-agent runtime is part of this proof map.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1-R7 | T1, T4, T12, T15 | contract | Package inventory, universal ownership, resource mapping, reference ownership, and fail-safe loading. |
| R8-R15 | T1-T3 | contract | Four assemblies, candidate evidence, closed operations, target state, no fallback, and portable isolation. |
| R16-R23 | T5-T8 | contract | Governed create, revise, commit, retry, collision, concurrency, and downstream reliance. |
| R24-R32 | T9-T11 | contract | Stale-attempt result, workflow authorization, proposal-owned reset, preservation, idempotency, and architecture stop. |
| R33-R40 | T4, T12-T14 | contract | Closed predicates, semantic ownership, late loading, scope triggers, structural groups, blockers, and placeholders. |
| R41-R44 | T16 | contract | Separate rule and literal ledgers plus unknown-value-first validation. |
| R45-R47 | T17 | integration | Deterministic assembly measurement, complete reporting, and real-profile reduction. |
| R48-R49 | T15, T18 | integration | Canonical-through-installed parity and deterministic acceptance without target-agent or manual semantic-review gates. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | T1-T2 | PA0 portable creation loads only the common path and skeleton and writes no lifecycle state. |
| E2 | T2 | Portable revision uses exact file state without a proposal entry. |
| E3 | T3 | Candidate loading precedes full authority validation and failure never falls back. |
| E4 | T5 | Governed creation commits only at `review-required`. |
| E5 | T7 | Identical partial and completed retries resume or no-op once. |
| E6 | T9-T10 | Workflow authorizes while proposal resets only exact proposal-owned incomplete state. |
| E7 | T11 | Changed identity, reliance, or competing state invalidates reset authorization. |
| E8 | T12-T13 | All four strategic groups compose independently after one gates-reference load. |
| E9 | T14 | An applicable unresolved group emits an explicit blocker and no placeholder. |
| E10 | T4 | Every required-resource integrity defect stops dependent work. |
| E11 | T8 | Downstream reliance requires workflow-owned impact handling and reopen authority. |
| E12 | T17 | Loaded assemblies, resources, output, and total package are reported separately. |

## Proof map

Boundary model version: boundary-first-v1
Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R49

| Proof obligation ID | Coverage state | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Proof level | Automation mode | Command IDs | Evidence artifact | Required milestone | Manual procedure IDs | Uncovered gap ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRF-001 | covered | R8, R9, R10, R11, R12, R13, R14, R15, R33, R34, R35, R36, R37 | BND-INPUT-001 | T1, T2, T3 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-002 | covered | R8, R9, R10, R11, R12, R13, R14, R15, R33, R34, R35, R36, R37 | BND-INPUT-002 | T4, T12, T13, T14 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-003 | covered | R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32 | BND-STATE-001 | T5, T6, T7, T8 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-004 | covered | R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32 | BND-STATE-002 | T7, T9, T10, T11 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-005 | covered | R9, R10, R11, R12, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32 | BND-AUTH-001 | T3, T5, T6, T8 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-006 | covered | R9, R10, R11, R12, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32 | BND-AUTH-002 | T9, T10, T11 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-007 | covered | R1, R2, R3, R4, R5, R6, R7, R33, R34, R35, R36, R37, R38, R39, R40 | BND-COMPOSE-001 | T1, T4, T12, T15 | integration | automated | CMD2, CMD3, CMD4, CMD5, CMD6, CMD7, CMD8 | `evidence/m2-package-implementation.md`; `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-008 | covered | R1, R2, R3, R4, R5, R6, R7, R33, R34, R35, R36, R37, R38, R39, R40 | BND-COMPOSE-002 | T12, T13, T14 | contract | automated | CMD2, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-009 | covered | R22, R23, R24, R25, R26, R27, R28, R29, R30, R31 | BND-TEMPORAL-001 | T7, T9, T10, T11 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-010 | covered | R4, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32 | BND-RECOVERY-001 | T7, T9, T10, T11 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-011 | covered | R4, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32 | BND-RECOVERY-002 | T4, T15 | integration | automated | CMD2, CMD3, CMD5, CMD8 | `evidence/m2-package-implementation.md`; `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-012 | covered | R41, R42, R43, R44, R45, R46, R47, R48 | BND-COMPAT-001 | T16, T17, T18 | integration | automated | CMD1-CMD9 | `evidence/m1-preservation-inventories.md`; `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-013 | covered | R4, R48, R49 | BND-ENV-001 | T4, T15, T18 | integration | automated | CMD2, CMD4-CMD9 | `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-014 | covered | R9, R10, R11, R12, R13, R14, R15 | INT-001 | T2, T3 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-015 | covered | R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32 | INT-002 | T7, T9, T10, T11 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-016 | covered | R33, R34, R35, R36, R37, R38, R39, R40 | INT-003 | T12, T13, T14 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-017 | covered | R4, R41, R42, R43, R44, R45, R46, R47, R48, R49 | INT-004 | T4, T15-T18 | integration | automated | CMD1-CMD9 | `evidence/m1-preservation-inventories.md`; `evidence/m3-package-proof.md` | M3 | - | - |

## Edge case coverage

| Edge case | Covered by | Expected handling |
| --- | --- | --- |
| Conversational change mention without structured identity | T2-T3 | Remain portable when the portable target is valid; do not infer authority. |
| Structured pointer resolves an invalid change | T3 | Load governed procedure and stop without portable fallback. |
| Portable create targets an existing file or revision targets an absent file | T2 | Stop and name the correct explicit operation. |
| Creation or revision is interrupted at each durable step | T5-T7 | Resume only the identical transaction or return idempotent success. |
| Governing basis changes during partial authoring | T9 | Return `authoring-reset-required` without starting another operation. |
| Review, downstream reliance, identity change, or competing write appears before reset | T10-T11 | Invalidate authorization and stop without mutation. |
| Accepted proposal already has downstream reliance | T8 | Require workflow impact handling and legal reopen authority. |
| Multiple or late predicates become true | T12-T13 | Load the strategic reference once and compose every true group before readiness selection. |
| Applicable group data is unresolved | T14 | Emit the applicable group with a blocker and no placeholder. |
| Required reference is missing, unreadable, escaped, contradictory, or mixed | T4, T15 | Stop dependent work without remembered reconstruction. |
| Total package grows while every loaded assembly shrinks | T17 | Report and justify total growth without failing solely on percentage. |
| Derived package omits or transforms one mapped resource | T15 | Fail path and raw-byte parity even when canonical validation passes. |

## Validation commands

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMD1 | `python -c 'import json; from pathlib import Path; root=Path("docs/changes/2026-08-14-proposal-skill-simplification"); load=lambda path: json.loads(path.read_text(encoding="utf-8")); rules=load(root/"proposal-rule-disposition.yaml")["rules"]; literals=load(root/"proposal-literal-compatibility.yaml")["literals"]; scenarios=load(root/"fixtures/scenario-contracts.yaml")["scenarios"]; bad_rule=load(root/"fixtures/invalid-rule-disposition.yaml"); bad_literal=load(root/"fixtures/invalid-literal-classification.yaml"); rd={"retained-inline","retained-governed-reference","retained-strategic-reference","asset-owned","removed-duplicate","removed-obsolete-with-approved-contract-change"}; lc={"normative-contract","parser-or-package-contract","test-only-incidental","obsolete","historical-fixture"}; rf={"rule_id","source_locations","behavior","governing_requirements","applicable_assemblies","disposition","destination","preservation_proof"}; lf={"literal_id","literal","source_location","consumers","classification","required_semantics","disposition","replacement"}; vr=lambda row: ["unknown-disposition"] if row.get("disposition") not in rd else (["missing-required-fields"] if not rf <= row.keys() else []); vl=lambda row: ["unknown-classification"] if row.get("classification") not in lc else (["missing-required-fields"] if not lf <= row.keys() else []); assert rules and literals and scenarios; assert all(vr(row)==[] for row in rules); assert all(vl(row)==[] for row in literals); assert vr(bad_rule)[0]=="unknown-disposition"; assert vl(bad_literal)[0]=="unknown-classification"; assert len({row["rule_id"] for row in rules})==len(rules); assert len({row["literal_id"] for row in literals})==len(literals); assert len({row["scenario"] for row in scenarios})==len(scenarios); print(f"rules={len(rules)} literals={len(literals)} scenarios={len(scenarios)} unknown_values=rejected-first")'` | planned-for-implementation | implement | M1 | M1 code-review | Reject unknown values first, then missing fields, duplicates, or scenario drift. | Not applicable; every assertion executes. | `evidence/m1-preservation-inventories.md` | Repository-local reads only; no network or target-agent runtime. |
| CMD2 | `python scripts/validate-skills.py skills/proposal/SKILL.md` | existing/configured | implement | M2 | M2 code-review | Block normalized structure, mapping, containment, placeholder, or claim defects. | Not applicable. | `evidence/m2-package-implementation.md` | Read-only repository validation. |
| CMD3 | `python scripts/test-skill-validator.py ProposalSkillSimplificationTests` | planned-for-implementation | implement | M2 | M2 code-review | Block assembly, operation, transaction, recovery, structure, or failure defects. | Zero discovered tests is failure. | `evidence/m2-package-implementation.md` | Repository-local tests; no target-agent runtime. |
| CMD4 | `python scripts/test-skill-validator.py` | existing/configured | implement | M2 | M2 code-review | Block broad skill-contract regression. | Zero discovered tests is failure. | `evidence/m2-package-implementation.md` | Repository-local tests; no target-agent runtime. |
| CMD5 | `python scripts/test-build-skills.py` | existing/configured | implement | M2 | M2 code-review | Block generated inventory or resource regression. | Zero discovered tests is failure. | `evidence/m2-package-implementation.md` | Temporary filesystem only. |
| CMD6 | `python scripts/build-skills.py --check` | existing/configured | implement | M2 | M2 code-review | Block generated-skill drift or missing resources. | Not applicable. | `evidence/m2-package-implementation.md` | Read-only check against canonical sources. |
| CMD7 | `python scripts/test-adapter-distribution.py` | existing/configured | implement | M3 | M3 code-review | Block adapter generation, archive, install, or parity regression. | Zero discovered tests is failure. | `evidence/m3-package-proof.md` | Temporary files only; no publication or network. |
| CMD8 | `python -c 'exec("""import subprocess, sys, tempfile\nversion = "v0.4.0"\nwith tempfile.TemporaryDirectory(prefix="rigorloop-adapters-") as output:\n    subprocess.run([sys.executable, "scripts/build-adapters.py", "--version", version, "--output-dir", output], check=True)\n    subprocess.run([sys.executable, "scripts/validate-adapters.py", "--version", version, "--adapter-root", output, "--clean-install-smoke", "--skill", "proposal"], check=True)""")'` | existing/configured | implement | M3 | M3 code-review | Block generated, archived, release-candidate, or installed resource mismatch. | Not applicable; all supported targets are selected. | `evidence/m3-package-proof.md` | Fresh temporary directory; no publication, network, or agent execution. |
| CMD9 | `python scripts/validate-boundary-first.py --check --path specs/proposal-skill-simplification.md` | existing/configured | implement | M2 | M2 code-review | Block invalid or missing proof for any boundary or interaction. | Not applicable; the matching proof map is mandatory. | `evidence/m2-package-implementation.md` | Read-only repository validation. |
| CMD10 | `python scripts/validate-change-metadata.py docs/changes/2026-08-14-proposal-skill-simplification/change.yaml` | existing/configured | workflow | lifecycle | Every state-changing handoff | Block invalid artifact, review, or planned-work state. | Not applicable. | Owning change validation ledger | Read-only validation. |
| CMD11 | `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-08-14-proposal-skill-simplification` | existing/configured | review stages | lifecycle | Every formal review handoff | Block malformed or missing review evidence. | Not applicable. | Review log and records | Read-only validation. |

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | T16-T17 | none | CMD1, CMD10 | `evidence/profile-size-baseline.md`; `evidence/m1-preservation-inventories.md` | M1 code-review | Canonical package remains unchanged while ownership, scenarios, and baselines are frozen. |
| M2 | T1-T16 | none | CMD2-CMD6, CMD9-CMD11 | `evidence/m2-package-implementation.md` | M2 code-review | Focused failing assertions precede the atomic canonical package and structural changes. |
| M3 | T15-T18 | none | CMD1-CMD11 | `evidence/simplification-measurements.md`; `evidence/semantic-preservation-review.md`; `evidence/m3-package-proof.md` | M3 code-review and final review | Proves loaded-profile reduction, semantic preservation, boundary coverage, and package parity. |
| M4 | T18 | none | CMD1-CMD11 | Final review, explanation, and verify evidence | verify | Lifecycle closeout begins only after M1-M3 and required review resolution are closed. |

## Test cases

### T1. Loaded assemblies and resource ownership are closed

- Covers: R1-R8; E1; BND-INPUT-001, BND-COMPOSE-001
- Level: contract
- Command IDs: CMD2-CMD5
- Fixture/setup: PA0, PA0G, PA1, and PA1G trigger fixtures plus forbidden and duplicate load combinations.
- Steps: Classify each invocation, assemble unique resources in documented order, and inspect resource maps and ownership assertions.
- Expected result: Exactly four assemblies exist; each loads only required procedure once; universal rules remain inline; references have non-overlapping owners; the skeleton is copied only for output.
- Failure proves: Progressive disclosure changes authority, duplicates policy, or admits an unsupported package profile.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: `scripts/test-skill-validator.py` focused fixtures and `validate-skills.py`.
- Required by milestone: M2

### T2. Portable create and revise use exact file state only

- Covers: R8-R15; E1-E2; EC1, EC3; BND-INPUT-001; INT-001
- Level: contract
- Command IDs: CMD3
- Fixture/setup: Absent, existing, ambiguous, and conflicting portable targets with and without conversational change wording.
- Steps: Request each explicit operation and inspect resolved writes.
- Expected result: Create accepts only an absent exact path, revise accepts only an existing exact path, invalid targets stop, and successful portable authoring writes only the proposal artifact.
- Failure proves: Portable authoring depends on lifecycle state, reclassifies operations, or mutates governed surfaces.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Focused portable-operation fixtures.
- Required by milestone: M2

### T3. Governed candidate selection never grants mutation authority

- Covers: R9-R12; E3; EC1-EC2; BND-INPUT-001, BND-AUTH-001; INT-001
- Level: contract
- Command IDs: CMD3
- Fixture/setup: Explicit change ID, workflow-selected change, valid pointer, conversational mention, missing record, stale identity, invalid lifecycle marker, and illegal authoring state.
- Steps: Select resources, then independently validate the complete governed authority record.
- Expected result: Only structured evidence selects the reference; only complete current authority permits mutation; every validation defect stops without portable fallback.
- Failure proves: Loading and authority are conflated or failed governed work escapes into portable mutation.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Focused candidate and authority fixtures.
- Required by milestone: M2

### T4. Required conditional resources fail safely

- Covers: R3-R7, R35-R36; E10; BND-INPUT-002, BND-COMPOSE-001, BND-RECOVERY-002, BND-ENV-001; INT-004
- Level: integration
- Command IDs: CMD2-CMD5, CMD8
- Fixture/setup: Missing, unreadable, escaped, contradictory, stale, and mixed-version governed or strategic references plus untriggered controls.
- Steps: Activate each conditional path and attempt dependent judgment or mutation.
- Expected result: Every required-resource defect stops before dependent work, no procedure is reconstructed from memory, and an untriggered missing reference does not block PA0.
- Failure proves: The shortened common path can partially recreate or bypass conditional procedure.
- Evidence artifact: `evidence/m2-package-implementation.md`; `evidence/m3-package-proof.md`
- Automation location: Resource-map, package, and focused failure fixtures.
- Required by milestone: M2 and M3

### T5. Governed creation commits only at review-required

- Covers: R16-R18; E4; EC4; BND-STATE-001, BND-AUTH-001
- Level: contract
- Command IDs: CMD3
- Fixture/setup: Authorized absent entry and file plus interruptions before entry, after entry, after content, and before complete evidence.
- Steps: Bind identities, create the exact authoring entry, write and validate content, record identity and evidence, and perform the final transition.
- Expected result: Only the matching entry and proposal-owned evidence change, and `review-required` is the sole commit point.
- Failure proves: Creation adopts unrelated state, publishes incomplete evidence, or mutates another lifecycle surface.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Static ordered-write fixtures.
- Required by milestone: M2

### T6. Governed revision preserves history and requires fresh review

- Covers: R19-R21; E11; EC5, EC9; BND-STATE-001, BND-AUTH-001
- Level: contract
- Command IDs: CMD3
- Fixture/setup: Legal review finding, upstream change, explicit reopen, stale reopen, settled proposal without reliance, and proposal with downstream reliance.
- Steps: Bind the prior identity and revision authority, attempt the revision, and inspect evidence and entry state.
- Expected result: Only current authorized review mapping is cleared, prior records remain historical, new content receives a new identity, and downstream reliance blocks until workflow impact handling and reopen authority exist.
- Failure proves: Revision invalidates history or changes an in-use proposal without owned staleness handling.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Focused governed-revision fixtures.
- Required by milestone: M2

### T7. Exact retries resume or no-op without duplication

- Covers: R22-R23; E5; EC4-EC5; BND-STATE-001, BND-STATE-002, BND-TEMPORAL-001, BND-RECOVERY-001; INT-002
- Level: contract
- Command IDs: CMD3
- Fixture/setup: Every partial creation and revision step, completed operation, mismatched path, unrelated asymmetry, stale authority, multiple candidate, and concurrent-write states.
- Steps: Replay the original or changed transaction identity.
- Expected result: Exact partial work resumes from the first incomplete step, exact completion is idempotent, and every mismatch stops without adoption or overwrite.
- Failure proves: Retry silently rebinds identity, duplicates evidence, or corrupts competing work.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Static retry and collision fixtures.
- Required by milestone: M2

### T8. Downstream reliance requires workflow-owned reopening

- Covers: R20-R21; E11; EC9; BND-STATE-001, BND-AUTH-001
- Level: contract
- Command IDs: CMD3
- Fixture/setup: Accepted proposal identities referenced by a spec, architecture record, plan, implementation, or no downstream artifact.
- Steps: Request ordinary governed revision and inspect authority resolution.
- Expected result: Any current downstream reliance blocks revision until workflow completes impact and staleness handling and grants exact reopen authority.
- Failure proves: Proposal changes can silently stale downstream contracts.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Static reliance fixtures.
- Required by milestone: M2

### T9. Changed-basis partial authoring returns reset-required

- Covers: R24-R27; E6; EC6; BND-STATE-002, BND-AUTH-002, BND-TEMPORAL-001, BND-RECOVERY-001; INT-002
- Level: contract
- Command IDs: CMD3
- Fixture/setup: Partial authoring with changed path, inputs, prior identity, or authorization basis.
- Steps: Attempt an ordinary retry, then ask workflow to classify no-review and no-reliance evidence and produce exact reset authorization.
- Expected result: Proposal returns `authoring-reset-required` without mutation; workflow preserves proposal state and issues authorization only for one exact stale transaction and allowed surface set.
- Failure proves: Stale work is silently rebound or workflow crosses proposal-owned mutation authority.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Static workflow/proposal handshake fixtures.
- Required by milestone: M2

### T10. Proposal consumes exact reset authorization once

- Covers: R26-R31; E6-E7; EC7-EC8; BND-STATE-002, BND-AUTH-002, BND-TEMPORAL-001, BND-RECOVERY-001; INT-002
- Level: contract
- Command IDs: CMD3
- Fixture/setup: Current authorization, completed reset replay, and changed proposal identity, reliance, competing write, or allowed-surface set.
- Steps: Validate and consume authorization, then retry identical and changed requests.
- Expected result: Proposal resets only the exact incomplete entry and proposal-authored evidence, preserves all other surfaces, returns idempotent success for exact completion, and stops on every changed basis.
- Failure proves: Authorization can be replayed broadly, stale evidence can authorize mutation, or unrelated records can be lost.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Static authorized-reset fixtures.
- Required by milestone: M2

### T11. Recovery does not create a new lifecycle owner or state

- Covers: R25, R29-R32; E6-E7; BND-STATE-002, BND-AUTH-002, BND-TEMPORAL-001, BND-RECOVERY-001; INT-002
- Level: contract
- Command IDs: CMD1, CMD3, CMD10
- Fixture/setup: Valid handshake plus attempted workflow mutation, new reset state, new persistence record, completed-record deletion, and downstream-artifact mutation.
- Steps: Validate the serialized state and permitted write sets.
- Expected result: Workflow owns identity, no-reliance, authorization, and routing only; proposal owns its exact reset; any design requiring a new state, evidence type, persistence mechanism, or write owner blocks and routes to architecture and workflow-contract revision.
- Failure proves: Simplification hides an architecture or ownership change.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Lifecycle metadata and forbidden-write fixtures.
- Required by milestone: M2

### T12. Specialized predicates use a closed semantic vocabulary

- Covers: R33-R37; E8; EC10; BND-INPUT-002, BND-COMPOSE-001, BND-COMPOSE-002; INT-003
- Level: contract
- Command IDs: CMD1, CMD3
- Fixture/setup: Empty, each singleton, every meaningful combination, unknown name, late discovery, unresolved applicability, and every named scope-budget trigger.
- Steps: Classify predicates and assemble the strategic resource.
- Expected result: Exactly four names are accepted, semantic truth remains proposal-owned, a non-empty set loads the reference once, every true predicate remains active, and unresolved material applicability stops before readiness.
- Failure proves: A validator becomes a prose classifier, a trigger disappears, or one predicate suppresses another.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Closed-vocabulary and static classification fixtures.
- Required by milestone: M2

### T13. All four conditional groups compose independently

- Covers: R35, R38-R40; E8; EC10; BND-INPUT-002, BND-COMPOSE-002; INT-003
- Level: contract
- Command IDs: CMD2-CMD3
- Fixture/setup: Core-only output, every singleton group, all pairwise material combinations, and all four groups together.
- Steps: Copy the skeleton, select applicable groups, fill resolved fields, and inspect ordering and ownership.
- Expected result: Core structure is always present, each true group appears once without suppressing another, inapplicable groups are absent, and neither asset nor reference duplicates applicability policy.
- Failure proves: The sole structural owner cannot represent a valid proposal profile.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Representative-output composition fixtures.
- Required by milestone: M2

### T14. Unresolved applicable groups remain explicit and placeholder-free

- Covers: R36, R39-R40; E9; EC11; BND-INPUT-002, BND-COMPOSE-002; INT-003
- Level: contract
- Command IDs: CMD2-CMD3
- Fixture/setup: Each applicable group with one required datum unavailable plus inapplicable controls.
- Steps: Compose output and validate the emitted structure.
- Expected result: Applicable unresolved groups remain present with a concrete blocker, inapplicable groups are omitted, and no output contains an unfilled placeholder.
- Failure proves: Output hides unresolved strategic work or exposes template residue.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Skeleton and representative-output fixtures.
- Required by milestone: M2

### T15. Canonical and derived packages retain complete resource parity

- Covers: R1, R3-R7, R38-R40, R48; E10; EC13; BND-COMPOSE-001, BND-RECOVERY-002, BND-ENV-001; INT-004
- Level: integration
- Command IDs: CMD2, CMD4-CMD8
- Fixture/setup: Canonical package and freshly generated, packed, archived, release-candidate, and installed adapter trees.
- Steps: Validate mapping, build packages, select `proposal`, and compare every required relative path and raw byte.
- Expected result: Every supported target contains both references and the skeleton exactly once at the required paths and bytes; missing, transformed, escaped, stale, or mixed resources fail.
- Failure proves: Canonical success does not guarantee a complete published package.
- Evidence artifact: `evidence/m3-package-proof.md`
- Automation location: Existing skill, build, and adapter distribution tests.
- Required by milestone: M3

### T16. Semantic-rule and literal inventories remain separate and closed

- Covers: R41-R44; BND-COMPAT-001; INT-004
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

- Covers: R45-R47; E12; EC12; BND-COMPAT-001; INT-004
- Level: integration
- Command IDs: CMD1
- Fixture/setup: Before and after canonical resources assembled in documented order with LF normalization and unique-file counting.
- Steps: Measure PA0, PA0G, PA1, PA1G, `SKILL.md`, each reference, skeleton, representative copied output, duplicate clusters, mapped-resource count, and total package.
- Expected result: Every real loaded assembly uses fewer words and bytes unless one exact independently reviewed preservation exception is recorded; total package change remains separately visible and no fixed percentage overrides semantics.
- Failure proves: File splitting or relocation is misreported as simplification.
- Evidence artifact: `evidence/simplification-measurements.md`; `evidence/semantic-preservation-review.md`
- Automation location: Change-local deterministic measurement and inventory assertions.
- Required by milestone: M3

### T18. Final deterministic acceptance excludes target-agent and extra manual gates

- Covers: R41-R49; BND-COMPAT-001, BND-ENV-001; INT-004
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
- Change-local scenarios for assemblies, candidates, operations, transactions, retries, stale reset, predicates, output groups, resource failure, compatibility, and forbidden writes.
- Existing controlled skill fixtures and generated adapter fixtures extended only where focused `proposal` coverage is absent.
- Representative PA0, PA0G, PA1, and PA1G outputs plus partial, stale, conflicting, and completed transaction states.

## Mocking/stubbing policy

Use temporary filesystem fixtures for proposal targets, change records, authoring evidence, reset authorization, conditional resources, generated adapters, and interrupted writes. Do not mock away public skill/resource assembly, workflow/proposal authority separation, or proposal-review handoff. No network, hosted service, target-agent runtime, publication, or external state mutation is required.

## Migration or compatibility tests

T16 proves semantic/literal separation, atomic parser or package migration, incidental-test updates, and historical readability. T15 proves package migration is atomic across canonical and every derived target. Historical proposals and review evidence are never rewritten solely for this change.

## Observability verification

T3, T5-T11, T14, and T17 verify visible classification, entry transitions, transaction results, blockers, authorization identity, reset outcomes, and size accounting. No telemetry is introduced.

## Security/privacy verification

T3-T4, T9-T11, T15, and T18 prove exact mutation authority, fail-safe resources, bounded reset writes, absence of secrets or machine-local requirements, bounded temporary filesystem use, and no network or target-runtime dependency.

## Performance checks

PA0, PA0G, PA1, and PA1G LF-normalized words and UTF-8 bytes are the required portable context metrics. Resource, representative output, and total package sizes are reported separately. No wall-clock, tokenizer, or target-runtime benchmark is required.

## Manual QA checklist

None. Deterministic proof owns test acceptance; ordinary proposal review, code review, and human PR review retain their normal roles and are not represented as a new manual QA procedure.

## What not to test and why

- Do not execute or grade a target-agent runtime; this is a deterministic content and package refactor.
- Do not add a permanent tokenizer, prose classifier, proposal artifact validator, or simplicity validator; change-local evidence and existing owners are sufficient.
- Do not turn ordinary reviewer judgment into a scripted manual acceptance procedure or pre-implementation gate.
- Do not test publication, release, deployment, network, or destructive Git behavior because those systems do not change.
- Do not rewrite historical proposals or test them as newly emitted output.
- Do not test another skill's independent optimization in this change.

## Uncovered gaps

None.

## Next artifacts

`test-spec-review`, then M1 implementation and code review if the proof map is approved.

## Follow-on artifacts

None yet.

## Readiness

Ready for independent `test-spec-review`. This proof map does not claim peer approval, implementation readiness, validation success, verification, branch readiness, or PR readiness.
