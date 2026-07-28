<!-- Template: test-spec-skeleton-v1 -->
<!-- Skill: test-spec -->
<!-- Template status: normative -->
<!-- Maintained alongside: skills/test-spec/SKILL.md -->

# Boundary-First Proof Model Test Spec

## Status

active

## Related spec and plan

- Spec: `specs/boundary-first-proof-model.md`
- Plan:
  `docs/plans/2026-07-27-portable-boundary-first-capability-for-published-skills.md`
- Architecture: `docs/architecture/system/architecture.md`
- ADR:
  `docs/adr/ADR-20260728-portable-boundary-first-release-manifest-and-package-rollback.md`

## Input artifact identities

| Input | Path | Status / Review state | Identity |
| --- | --- | --- | --- |
| Feature spec | `specs/boundary-first-proof-model.md` | approved; spec-review R5 | `sha256:7d10f72e7dfca18c08c4f7117846c5a655f060f5087ec196725a2c5494af25d1` |
| Spec review | `docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/reviews/spec-review-r5.md` | approved | `sha256:4ed509fc263fc8c14b1a7508ebc0d9d30968af55cc96be77a4093d352da2ea89` |
| Plan | `docs/plans/2026-07-27-portable-boundary-first-capability-for-published-skills.md` | approved plan content at `3a5388bb`; plan-review R3 approved | `sha256:2e9a29b5206d2298d5bbf2a59912ee5642defab68d8b63c6e473321d6ae4c273` |
| Plan review | `docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/reviews/plan-review-r3.md` | approved | `sha256:dbfe83fe10fedc10456842b121c32b1889f627e6aa8d083c80d41e67cab6f2ae` |
| Architecture | `docs/architecture/system/architecture.md` | approved; architecture-review R4 | `sha256:65bc44c6d8a8a6de23879144dca6c524b69558a178ab9127f03907b1f3761843` |
| ADR | `docs/adr/ADR-20260728-portable-boundary-first-release-manifest-and-package-rollback.md` | accepted | `sha256:3d09255eb51dacb2fd2fe756a656fc9719edd6de99763f23ae9ad09fd1b1c1e2` |

## Testing strategy

Fixture-backed unit tests prove closed vocabulary, exact serialization,
identifier and cross-reference rules, projection idempotency, digest
reproducibility, activation state, and fail-closed behavior.
Integration tests prove that all ten governed skills load the same method,
stage-local ownership remains distinct, validation selection includes the new
checks, and generated skill trees preserve mapped resources.
End-to-end local tests build adapter archives, install Codex, Claude Code, and
opencode into empty temporary projects, and inspect every governed installed
skill without network access.
Smoke proof runs repository broad smoke only after all milestone-local tests.
Migration proof verifies parent-revision grandfathering, prospective adoption,
active-only in-flight opt-in, and read-only rollback package selection.
Manual proof is unnecessary because byte identity, package presence, cold-read
availability, manifest states, and rollback package identities are
deterministically observable.

This bootstrap feature spec does not carry
`boundary_contract: boundary-first-v1` while activation is pending, so
PBF-R032 does not require a boundary-ID proof map for this test spec itself.
The tests below prove the contract that future adopting test specs will use;
they do not invent bootstrap boundary IDs.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| PBF-R001-PBF-R007 | T1, T2, T8, T9, T13 | unit, contract, migration | Version, marker, activation state, durable record, complete baseline, and fail-closed activation. |
| PBF-R008-PBF-R014c | T2, T4, T5 | unit, contract | Closed dimensions, applicability, sentinels, ID lists, prefixes, and no extensions/imports. |
| PBF-R015-PBF-R020 | T2, T4, T5 | unit, contract | Contiguous feature record, headings, columns, definitions, and boundary ID grammar. |
| PBF-R021-PBF-R024 | T2, T6 | unit, contract | Example classification, ownership, regressions, discoveries, and exact links. |
| PBF-R025-PBF-R031 | T2, T6 | unit, contract | Hazard-driven interactions, exact table, none-selected rationale, and no Cartesian product. |
| PBF-R032-PBF-R040 | T2, T7 | unit, contract | Exact proof records, coverage states, gaps, references, partitions, and composed paths. |
| PBF-R041-PBF-R045 | T3, T10, T16 | integration, contract | Closed governed set, `READ` mapping, stage ownership, local policy, and proposal exclusion. |
| PBF-R046-PBF-R049 | T1, T3, T11, T12 | unit, integration, e2e | Skill-local reference projections and canonical/generated/packed/installed parity. |
| PBF-R049a-PBF-R051 | T5, T6, T8, T9, T15 | unit, integration, migration | Marker enforcement, baseline membership, structural claim limit, and semantic fixtures. |
| PBF-R052-PBF-R058 | T8, T9, T13 | integration, migration | Prospective activation, opt-in, revision classification, historical validity, and rollback. |
| PBF-R059-PBF-R064 | T6, T7, T10, T16 | integration, contract | Semantic stage ownership, final coherence, and stop rules. |
| PBF-R065 | T12, T14 | e2e, contract | No runtime, model, network, sandbox, interceptor, or attestation dependency. |
| `rigorloop-workflow` R28-R36 | T3, T10, T16 | integration, contract | Workflow routing, stage ownership, plan pair, proof handoffs, and stopping behavior. |
| `skill-contract` R56-R63 | T1, T3, T11, T12 | unit, integration, e2e | Shared `READ` reference projection, mapping, generation, packaging, and installed parity. |

## Acceptance criterion coverage map

| Acceptance criterion | Covered by | Level | Notes |
| --- | --- | --- | --- |
| PBF-AC001 | T1, T2, T5, T8 | unit, integration | Closed contract, record, activation, and evidence vocabularies fail closed. |
| PBF-AC002 | T2, T4 | unit | Feature-owned normalized records are complete and concise. |
| PBF-AC003 | T2, T7 | unit | Exact proof references cover all applicable boundaries and interactions; gaps block. |
| PBF-AC004 | T2, T6 | unit, integration | Examples remain classified and subordinate to normative owners. |
| PBF-AC005 | T3, T10 | integration | All ten governed skills retain distinct stage-local responsibilities. |
| PBF-AC006 | T1, T3 | unit, integration | Every governed skill has the same versioned stage-specific `READ` mapping. |
| PBF-AC007 | T1, T11, T12 | unit, integration, e2e | Canonical, projected, generated, packed, and installed bytes agree. |
| PBF-AC008 | T5, T6, T15 | unit, integration | Unknown values fail before consistency and validators do not claim semantics. |
| PBF-AC009 | T10, T16 | integration | Spec, plan, proof, code, and verify gates keep their named judgments. |
| PBF-AC010 | T4, T6 | unit, integration | Simple changes avoid standalone artifacts and Cartesian interaction sets. |
| PBF-AC011 | T8, T9, T13 | integration, migration | Activation, revision classification, opt-in, grandfathering, and rollback are deterministic. |
| PBF-AC012 | T8, T11 | integration | Mixed, missing, stale, or divergent governed/package surfaces block activation. |
| PBF-AC013 | T12, T14 | e2e, integration | Published use requires no runtime, model, network, sandbox, interceptor, or attestation. |
| PBF-AC014 | T6, T10 | integration | Review skills, not validators, judge structurally valid semantic omissions. |

## Supplemental normative coverage

| Normative surface | Covered by | Command IDs | Required milestone | Direct proof |
| --- | --- | --- | --- | --- |
| Structural diagnostic fields | T5 | CMD6, CMD7 | M3 | Failure assertions include artifact, record surface, stable check ID, offending value or reference, and expected closed contract. |
| Activation diagnostic fields | T8, T9, T13 | CMD6, CMD7, CMD11 | M3 and M4 | Evidence includes state, release tags, parent baseline, path inventory, package matrix, and structurally unclassified-spec identities. |
| Packaging diagnostic fields | T11 | CMD9, CMD10 | M4 | A divergent fixture reports skill, path, expected and actual SHA-256, and first divergent layer. |
| Review-record semantic fields | T10, T16 | CMD4, CMD14 | M2 | Review fixtures name reviewed identity, semantic owner, findings, required outcomes, and disposition state. |
| Structural validators do not claim semantic completeness | T6, T15 | CMD4, CMD6, CMD7 | M2 and M3 | Validator output forbids approval/completeness claims while review fixtures own semantic findings. |
| Redacted evidence and readable published Markdown | T17 | CMD4, CMD6 | M2 and M3 | Evidence schemas reject embedded sensitive payload fields in favor of stable redacted identities; published content retains text headings/tables and no color-only or diagram-only meaning. |
| Simple-change and ordinary-authoring portability | T4, T6, T12, T14 | CMD4, CMD6, CMD10 | M2 through M4 | Concise records pass without Cartesian products, live agents, runtime identity, or network access. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | T4, T6 | A simple adopting fixture uses concise non-applicability without a separate artifact or interaction matrix. |
| E2 | T6, T16 | A retry example without requirement ownership becomes a discovery and blocks downstream work. |
| E3 | T7, T10 | Helper-only proof fails when public and sibling paths are admitted. |
| E4 | T9, T13 | A grandfathered accepted spec remains valid through activation and package rollback. |
| E5 | T13 | Existing immutable release metadata proves rollback readiness without repository or external mutation. |

## Edge case coverage

| Edge case | Covered by | Notes |
| --- | --- | --- |
| EC1 applicable dimension without a boundary ID | T5 | Exact structural validation rejects the missing boundary before reference checks. |
| EC2 not-applicable dimension with a boundary ID | T5 | Applicability field rules reject contradictory ownership. |
| EC3 boundary requirement outside model scope | T5 | Scope consistency rejects the out-of-range owner. |
| EC4 duplicate boundary, interaction, example, or proof ID | T5, T7 | Definition and proof-map uniqueness fail explicitly. |
| EC5 interaction with only one boundary | T5, T6 | Structural shape fails before semantic interaction review. |
| EC6 no interaction without requirement-grounded rationale | T4, T5 | Concise no-interaction records pass only with the exact rationale form. |
| EC7 discovery example without a gap ID | T6, T10 | Semantic review blocks the ownerless discovery. |
| EC8 cross-feature boundary reference | T7 | Proof maps reject IDs absent from their governing feature record. |
| EC9 automated proof with a manual procedure ID | T7 | Closed automation-mode field rules reject the row. |
| EC10 manual or hybrid proof without procedure and evidence | T7 | Required mode fields fail closed. |
| EC10a gap row carrying test or proof metadata | T7 | A gap cannot count as coverage or carry covered-row fields. |
| EC11 formatting-only historical edit | T9 | The historical path stays grandfathered and does not activate adoption. |
| EC12 substantive historical edit after activation | T9 | The edit routes to spec-review and requires adoption. |
| EC13 stale projected skill reference | T1, T11 | Projection and package parity fail and activation remains blocked. |
| EC14 structurally complete record with a semantic omission | T6, T10 | Validators remain structural and the owning review skill reports the omission. |
| EC15 optional runtime load with missing packaged reference | T12, T14 | Package validation fails even if one runtime invocation could skip loading. |

## Validation commands

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMD1 | `python scripts/test-boundary-first-reference.py` | planned-for-implementation | implement | M1 | code-review M1 | block M1 closeout | zero tests is failure | `docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/boundary-reference-evidence.yaml` | local temporary fixtures only |
| CMD2 | `python scripts/project-boundary-first-reference.py --check` | planned-for-implementation | implement | M1 | code-review M1 | block on missing, stale, extra, or divergent projection | not applicable; deterministic check | `docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/boundary-reference-evidence.yaml` | read-only check; `--write` is separately implementation-scoped |
| CMD3 | `python scripts/validate-skills.py` | existing/configured | implement | M2 | code-review M2 | block skill handoff | not applicable; structural validator | change metadata validation entry | local read-only validation |
| CMD4 | `python scripts/test-skill-validator.py` | existing/configured | implement | M2 | code-review M2 | block semantic skill-fixture handoff | zero tests is failure | change metadata validation entry | local tests only |
| CMD5 | `python scripts/build-skills.py --check` | existing/configured | implement | M2 | code-review M2 | block generated-skill parity | not applicable; build check | change metadata validation entry | temporary output only; no canonical mutation |
| CMD6 | `python scripts/test-boundary-first-validation.py` | planned-for-implementation | implement | M3 | code-review M3 | block structural validator handoff | zero tests is failure | `docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/boundary-validation-evidence.yaml` | local temporary fixtures only |
| CMD7 | `python scripts/validate-boundary-first.py --check` | planned-for-implementation | implement | M3 | code-review M3 | block on invalid record, activation, inventory, or parity | not applicable; deterministic check | `docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/boundary-validation-evidence.yaml` | read-only repository check |
| CMD8 | `python scripts/test-select-validation.py` | existing/configured | implement | M3 | code-review M3 | block selector integration | zero tests is failure | change metadata validation entry | local tests only |
| CMD9 | `python scripts/test-adapter-distribution.py` | existing/configured | implement | M4 | code-review M4 | block adapter package proof | zero tests is failure | change metadata validation entry | local fixtures and temporary archives only |
| CMD10 | `python scripts/test-adapter-distribution.py -k boundary_first` | existing/configured | implement | M4 | code-review M4 | block packed and installed parity | zero tests is failure | `docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/boundary-install-evidence.yaml` | extends existing archive and clean-install fixtures; no network or publication |
| CMD11 | `python scripts/test-boundary-first-validation.py -k active_rollback_release_matches_current_adapter_metadata` | planned-for-implementation | implement | M4 | code-review M4 | block rollback-readiness proof | zero tests is failure | `docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/boundary-activation-evidence.yaml` | read-only current metadata integration; no install or publication |
| CMD13 | `bash scripts/ci.sh --mode broad-smoke` | existing/configured | implement | M4 | code-review M4 | block M4 closeout | zero selected tests is failure | change metadata validation entry | local repository validation; no publication |
| CMD14 | `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording` | existing/configured | test-spec-review / verify | lifecycle | test-spec-review | block malformed review evidence | not applicable; validator | review log | local read-only validation |
| CMD15 | `python scripts/validate-change-metadata.py docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/change.yaml` | existing/configured | test-spec / verify | lifecycle | test-spec authoring | block stale change metadata | not applicable; validator | change metadata | local read-only validation |
| CMD16 | `bash scripts/ci.sh --mode broad-smoke` | existing/configured | verify | lifecycle closeout | verify | block final verification | zero selected tests is failure | change metadata validation entry and verify report | local repository validation; no publication |

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | T1, T2 | none | CMD1, CMD2, CMD15 | canonical and projected references; `boundary-reference-evidence.yaml` | code-review M1 | Proves one source, closed consumers, byte projection, digest, and portable method content. |
| M2 | T3, T6, T10, T16, T17 | none | CMD3, CMD4, CMD5, CMD15 | governed `SKILL.md` files; semantic review fixtures | code-review M2 | Proves stage-local responsibility, readable published content, and stage-owned semantics while every stage reads the same method. |
| M3 | T4, T5, T7, T8, T9, T15, T17 | none | CMD6, CMD7, CMD8, CMD15 | validator fixtures; pending activation record; `boundary-validation-evidence.yaml` | code-review M3 | Proves shape/reference enforcement, privacy-bounded evidence, baseline classification, selection, and semantic claim limits. |
| M4 | T11, T12, T13, T14 | none | CMD2, CMD5, CMD7, CMD9, CMD10, CMD11, CMD13, CMD14, CMD15, CMD16 | generated trees; local archives; installed trees; activation, install, and rollback evidence | code-review M4 | CMD11 proves current release-metadata integration; CMD13 is required before code-review M4; CMD16 is deferred to final verify. |

## Test cases

### T1. Canonical reference projection is closed, byte-exact, and reproducible

- Covers: PBF-R001, PBF-R041, PBF-R046-PBF-R048, `skill-contract` R56-R63, EC7, EC11
- Level: unit
- Command IDs: CMD1, CMD2
- Fixture/setup: canonical reference bytes, ten governed consumer paths, missing/extra/stale projections, and cross-platform path fixtures.
- Steps: Exercise write and check modes twice; perturb membership and bytes; compute the specified sorted POSIX-path digest.
- Expected result: Writes are idempotent, all ten projections are byte-identical, the digest is reproducible, and every membership or byte drift fails explicitly.
- Failure proves: the same published method cannot be established or audited across skills.
- Evidence artifact: `boundary-reference-evidence.yaml`
- Automation location: `scripts/test-boundary-first-reference.py`
- Required by milestone: M1

### T2. Shared method contains the complete portable v1 contract and no stage policy

- Covers: PBF-R008-PBF-R040, PBF-R044, PBF-R050, PBF-R065
- Level: unit
- Command IDs: CMD1
- Fixture/setup: canonical shared reference and expected closed vocabulary, table fields, interaction method, example roles, and proof fields.
- Steps: Parse the reference and assert required portable content and forbidden stage-specific lifecycle, approval, placement, and readiness policy.
- Expected result: The method is sufficient for contract/proof work yet does not become a second lifecycle owner.
- Failure proves: installed skills either lack the common method or inherit conflicting stage policy.
- Evidence artifact: `boundary-reference-evidence.yaml`
- Automation location: `scripts/test-boundary-first-reference.py`
- Required by milestone: M1

### T3. Ten governed skills map one reference with stage-specific load conditions

- Covers: PBF-R041-PBF-R048, `rigorloop-workflow` R28-R36, `skill-contract` R56-R63
- Level: integration
- Command IDs: CMD3, CMD4, CMD5
- Fixture/setup: canonical governed skill roots and expected responsibility matrix.
- Steps: Validate exact governed membership, literal `READ` entries, skill-local paths, distinct load conditions, and generated skill parity.
- Expected result: Every governed skill reads the same bytes and only owns its specified stage behavior; proposal skills are excluded.
- Failure proves: the capability drifts across lifecycle stages or ceases to be self-contained.
- Evidence artifact: change metadata validation entry
- Automation location: `scripts/test-skill-validator.py`
- Required by milestone: M2

### T4. Valid concise feature records pass exact structural validation

- Covers: PBF-R002-PBF-R004, PBF-R008-PBF-R020, PBF-R030, E1
- Level: unit
- Command IDs: CMD6, CMD7
- Fixture/setup: minimal and complex adopting feature specs with all eight dimension rows, exact tables, concise non-applicability, and none-selected interaction rationale.
- Steps: Run structural validation and inspect stable parsed identities and references.
- Expected result: Both fixtures pass without a standalone artifact, extension dimension, or unnecessary interaction product.
- Failure proves: the contract imposes avoidable boilerplate or rejects its own normalized record.
- Evidence artifact: `boundary-validation-evidence.yaml`
- Automation location: `scripts/test-boundary-first-validation.py`
- Required by milestone: M3

### T5. Closed record vocabulary fails before consistency checks

- Covers: PBF-R008-PBF-R020, PBF-R029-PBF-R031, PBF-R049-PBF-R050, EC1-EC3
- Level: unit
- Command IDs: CMD6, CMD7
- Fixture/setup: one fixture per unknown version, dimension, applicability, heading, column, prefix, sentinel, duplicate, and forbidden extension/import.
- Steps: Validate each fixture independently and record diagnostic order.
- Expected result: Each unknown value produces an explicit closed-vocabulary error before reference or consistency diagnostics.
- Failure proves: malformed records can pass silently or produce misleading downstream errors.
- Evidence artifact: `boundary-validation-evidence.yaml`
- Automation location: `scripts/test-boundary-first-validation.py`
- Required by milestone: M3

### T6. Examples and interactions remain requirement-owned semantic judgments

- Covers: PBF-R021-PBF-R031, PBF-R050-PBF-R051, PBF-R059, E1, E2
- Level: integration
- Command IDs: CMD4, CMD6
- Fixture/setup: valid structural examples plus semantic omissions, example-only behavior, missing hazard interaction, and Cartesian-product overgeneration.
- Steps: Run structural fixtures and the `spec-review` skill behavior fixtures separately.
- Expected result: Validators check shape and links only; semantic review rejects missing ownership or completeness and routes discoveries upstream.
- Failure proves: examples or deterministic validation can invent normative behavior.
- Evidence artifact: semantic review fixture results
- Automation location: `scripts/test-skill-validator.py`
- Required by milestone: M2 and M3

### T7. Proof maps cover exact boundaries and interactions without treating gaps as proof

- Covers: PBF-R032-PBF-R040, PBF-R061, PBF-R064, E3, EC4-EC6
- Level: unit
- Command IDs: CMD6, CMD7
- Fixture/setup: approved feature boundary records and proof maps covering positive, negative, stale, substituted, conflicting, transition, retry, recovery, public, helper, and sibling paths.
- Steps: Validate complete maps, renamed/cross-feature IDs, incomplete mode fields, helper-only proof, and `gap` rows.
- Expected result: Exact complete maps pass; invalid references fail; gaps remain visible and block; helper-only proof cannot satisfy composed paths.
- Failure proves: implementation can proceed with invented IDs or inadequate direct proof.
- Evidence artifact: `boundary-validation-evidence.yaml`
- Automation location: `scripts/test-boundary-first-validation.py`
- Required by milestone: M3

### T8. Release manifest has one closed two-state contract

- Covers: PBF-R003, PBF-R005-PBF-R007, PBF-R049a-PBF-R049b, PBF-R053, EC8-EC10
- Level: integration
- Command IDs: CMD6, CMD7
- Fixture/setup: pending, active, incomplete, mixed-version, and fixed-authority-symlink release manifests with the exact ten governed skills, canonical/projection content identities, and a controlled ordered set of current, immediately preceding, and older published release tags.
- Steps: Validate the closed version, state, activating-release, rollback-release, governed-skill, canonical-reference, projection, parent-commit, and grandfather-path fields. Require `-` release and baseline values while pending. While active, require immutable release tags, require rollback release to equal the immediately preceding published tag, require a full parent commit, the exact ten-skill governed set, canonical and projected raw-byte identities, and a unique repository-relative POSIX path inventory sorted by raw UTF-8 bytes. Reject an older but otherwise valid rollback release, absolute, traversal, duplicate, unsorted, bootstrap-spec, `README.md`, `*.test.md`, marked-spec, and symlinked-authority entries before reads.
- Expected result: Complete pending and active fixtures using the immediate predecessor pass; unknown, incomplete, mixed, unsafe, incorrectly ordered, ineligible, or older-release manifests fail closed.
- Failure proves: release activation evidence can be ambiguous or unauditable.
- Evidence artifact: `boundary-activation-evidence.yaml`
- Automation location: `scripts/test-boundary-first-validation.py`
- Required by milestone: M3

### T9. Prospective compatibility distinguishes historical paths without semantic inference

- Covers: PBF-R049a-PBF-R056, E4, EC8
- Level: integration
- Command IDs: CMD6, CMD7
- Fixture/setup: an isolated temporary Git repository with a parent commit containing distinct accepted, approved, and active historical specs; draft and other nonterminal specs; marked specs; and excluded files, followed by an activating child commit that adds an otherwise eligible unmarked spec.
- Steps: Derive the inventory from the controlled parent revision, activate from the child revision, and validate historical edits, active-only in-flight opt-in, new marked and unmarked specs, and the child-introduced candidate.
- Expected result: Every eligible accepted, approved, and active parent path is grandfathered; every nonterminal, marked, and excluded parent path is omitted; the child-introduced spec cannot self-grandfather; new behavior specs require the marker after activation; in-flight opt-in is active-only; and grandfathered edits route to `spec-review` without validator classification.
- Failure proves: rollout either invalidates history or creates an unintended exemption.
- Evidence artifact: `boundary-validation-evidence.yaml`
- Automation location: `scripts/test-boundary-first-validation.py`
- Required by milestone: M3

### T10. Stage-local skills enforce semantic ownership and stop behavior

- Covers: PBF-R043-PBF-R045, PBF-R059-PBF-R064, `rigorloop-workflow` R28-R36, E2, E3
- Level: integration
- Command IDs: CMD4
- Fixture/setup: lifecycle packets with missing owner, stale ID, example-only behavior, missing proof, helper-only proof, stale evidence, and discovery gaps.
- Steps: Exercise each governed skill's stage-specific fixture and expected handoff.
- Expected result: The owning review stage judges its semantics, authoring/implementation stages stop on gaps, code review checks escaped paths, and verify checks coherence without reapproval.
- Failure proves: stage responsibilities collapse into generic validation or unsafe continuation.
- Evidence artifact: semantic skill fixture results
- Automation location: `scripts/test-skill-validator.py`
- Required by milestone: M2

### T11. Generated and locally packed packages preserve reference bytes

- Covers: PBF-R046-PBF-R049, `skill-contract` R56-R63, EC7
- Level: integration
- Command IDs: CMD2, CMD5, CMD9, CMD10
- Fixture/setup: generated skill mirrors and local Codex, Claude Code, and opencode release archives.
- Steps: Build each surface, enumerate every governed reference included by the existing adapter support decision, compare relative paths and raw-byte SHA-256, then perturb one archive fixture.
- Expected result: Every surface matches canonical bytes and one perturbed package fails with target, skill, path, expected hash, and actual hash.
- Failure proves: a correct canonical source can ship as a stale or incomplete package.
- Evidence artifact: `boundary-install-evidence.yaml`
- Automation location: `scripts/test-adapter-distribution.py`
- Required by milestone: M4

### T12. Clean installed skills expose the same method without repository or network access

- Covers: PBF-R042, PBF-R046-PBF-R048, PBF-R065, EC12
- Level: e2e
- Command IDs: CMD10
- Fixture/setup: empty temporary projects and locally packed archives for all three targets.
- Steps: Install each target locally, cold-read every governed `SKILL.md` and mapped reference, and compare bytes while network access and repository-root lookup are unavailable.
- Expected result: Every adapter-included governed target/skill combination is self-contained and byte-identical; exclusions remain owned by the existing adapter portability decision rather than this capability.
- Failure proves: the user-visible capability depends on maintainer infrastructure or an omitted package resource.
- Evidence artifact: `boundary-install-evidence.yaml`
- Automation location: `scripts/test-adapter-distribution.py`
- Required by milestone: M4

### T13. Rollback package selection is read-only and complete

- Covers: PBF-R057-PBF-R058, E4, EC10
- Level: integration
- Command IDs: CMD6, CMD7, CMD11
- Fixture/setup: active manifests selecting valid and invalid rollback releases, current `dist/adapters/manifest.yaml`, isolated adapter-metadata fixtures, and one real tracked release metadata file.
- Steps: Snapshot the raw bytes of the activation manifest, governed feature specs, proof maps, `dist/adapters/manifest.yaml`, and the selected `docs/reports/adapter-artifacts/releases/<version>.yaml`; validate missing, additional, duplicated, failing, and mixed-version fixture entries; then run the focused integration proof against current adapter support and tracked release metadata with install and publish hooks replaced by fail-if-called sentinels.
- Expected result: Output names the selected rollback release tag and exactly one passing archive identity per supported adapter in an adapter/archive/SHA-256 matrix sorted by raw UTF-8 adapter name. Every snapshotted input is byte-identical after success and after each failure, no install or publish sentinel is called, and every incomplete or mixed matrix fails without mutation.
- Failure proves: rollback readiness can select an incomplete or inconsistent package bundle.
- Evidence artifact: `boundary-activation-evidence.yaml`
- Automation location: `scripts/test-boundary-first-validation.py`
- Required by milestone: M4

### T14. Portability tests forbid runtime-certification dependencies

- Covers: PBF-R065
- Level: integration
- Command IDs: CMD4, CMD10
- Fixture/setup: governed skill/package corpus and a forbidden dependency token set for model, network, sandbox, interceptor, attestation, and immutable runtime evidence requirements.
- Steps: Inspect published instructions and run cold-read scenarios without those facilities.
- Expected result: The method remains usable from packaged content and project-local artifacts alone.
- Failure proves: the initiative has regressed into the excluded trusted runtime system.
- Evidence artifact: `boundary-install-evidence.yaml`
- Automation location: `scripts/test-skill-validator.py`; `scripts/test-adapter-distribution.py`
- Required by milestone: M4

### T15. Validation selection includes boundary checks and unknown values fail closed

- Covers: PBF-R005, PBF-R007, PBF-R049-PBF-R050, EC1, EC9, EC11
- Level: integration
- Command IDs: CMD6, CMD7, CMD8
- Fixture/setup: changed-path selector cases and unknown activation, dimension, proof, and consumer inventory values.
- Steps: Select validation for affected specs, skills, reference, activation, and adapter paths; run each unknown-value fixture.
- Expected result: Relevant edits select boundary validation and every unknown closed value fails before consistency checks.
- Failure proves: repository-owned automation can bypass the contract or accept future values silently.
- Evidence artifact: `boundary-validation-evidence.yaml`
- Automation location: `scripts/test-select-validation.py`
- Required by milestone: M3

### T16. Workflow handoffs stop on missing boundary ownership and preserve review gates

- Covers: PBF-R041-PBF-R045, PBF-R059-PBF-R064, `rigorloop-workflow` R28-R36
- Level: integration
- Command IDs: CMD4, CMD14
- Fixture/setup: workflow packets at spec, plan, test-spec, implementation, code-review, and verify with current, missing, or stale boundary evidence.
- Steps: Exercise routing and formal review recording for each packet.
- Expected result: The plan pair is present, semantic gates stay distinct, gaps route upstream, and no validator or review substitutes for another stage.
- Failure proves: the lifecycle can bypass an owner or claim readiness from stale evidence.
- Evidence artifact: review log and workflow fixture results
- Automation location: `scripts/test-skill-validator.py`
- Required by milestone: M2

### T17. Published Markdown and evidence remain readable and privacy-bounded

- Covers: feature-spec Security and privacy `MUST`; feature-spec Accessibility and UX `MUST`
- Level: integration
- Command IDs: CMD4, CMD6
- Fixture/setup: governed shared-reference and skill Markdown, evidence-schema fixtures with stable redacted identities, and invalid fixtures containing credential, private-payload, color-only, or diagram-only fields.
- Steps: Validate allowlisted evidence fields and published Markdown structure; reject embedded sensitive payload fields and inaccessible meaning while accepting stable redacted identities and text-owned headings/tables.
- Expected result: Evidence records contain bounded paths, digests, and redacted identities without secret or private payloads; every published method rule remains available in readable text without color or diagram dependence.
- Failure proves: the portable method leaks sensitive evidence or becomes unusable outside a visual rendering surface.
- Evidence artifact: semantic skill fixture results and `boundary-validation-evidence.yaml`
- Automation location: `scripts/test-skill-validator.py`; `scripts/test-boundary-first-validation.py`
- Required by milestone: M2 for published Markdown and M3 for evidence schemas

## Fixtures and data

- `scripts/fixtures/boundary-first/reference/`: canonical, missing, stale,
  extra-consumer, and digest fixtures.
- `scripts/fixtures/boundary-first/feature-records/`: minimal, complex,
  malformed, semantic-omission, discovery, and interaction fixtures.
- `scripts/fixtures/boundary-first/proof-maps/`: complete, gap, invalid
  reference, transition, mutation, retry, recovery, and composed-path fixtures.
- `scripts/fixtures/boundary-first/activation/`: pending, active, mismatched,
  incomplete, historical, in-flight, new-spec, and rollback-metadata fixtures.
- Existing skill and adapter fixture helpers should be extended rather than
  duplicating archive construction or clean-install logic.

All hashes derive from raw fixture bytes.
Tests must not depend on ambient repository Git history, wall-clock ordering,
a network service, or caller-asserted runtime identity. T9 creates and owns a
minimal temporary Git history solely to prove the parent-revision contract.

## Mocking/stubbing policy

Filesystem behavior may use temporary directories.
Adapter cold-read tests must use real locally built archives and the existing
installer path; they must not mock resource copying or installed-tree reads.
Network, model, sandbox, and runtime-attestation services are neither mocked
nor invoked because they are outside the capability.

## Migration or compatibility tests

T8, T9, and T13 own migration coverage.
The activation inventory uses accepted, approved, and active top-level feature
spec paths present at the full parent commit only and excludes `README.md`,
`*.test.md`, this bootstrap spec, marked specs, and later-introduced paths.
Historical path membership is structural; substantive revision remains a
`spec-review` judgment.
Rollback validation reads the manifest-selected immutable release's existing
adapter metadata and compares it with current adapter support.
It writes no repository state and performs no installation or publication.

## Observability verification

Projection, validation, packaging, and rollback-readiness checks emit
stable failure codes plus affected path, skill, target, expected value, and
actual value where applicable.
Evidence YAML records command ID, result, relevant aggregate identity, and
bounded artifact paths without claiming semantic completeness.

## Security/privacy verification

Archive and installed-tree proof remains local, uses temporary projects, and
performs no network access or publication.
Path validation rejects traversal, symlink escape, fixed-authority symlinks,
and consumers outside the closed governed roots by reusing existing package
safety helpers.
Evidence contains repository paths and digests only; no credentials, model
identity, hidden reasoning, or user data is recorded.

## Performance checks

Unit and structural suites should remain bounded by the fixture inventory.
The cold-read matrix may share each target's locally built archive and
installation but must inspect every adapter-included governed skill
independently.
CMD13 runs broad smoke after M4 milestone-local checks and before code-review
M4.
CMD16 independently reruns broad smoke during final verify.

## Manual QA checklist

Not applicable.
All required content, byte, reference, package, install, manifest, and rollback
claims have deterministic automated proof.

## What not to test and why

- Do not test model identity, process isolation, network transport, workspace
  mutation interception, or immutable runtime attestation; PBF-R065 excludes
  them.
- Do not generate a Cartesian product of every dimension; interactions are
  hazard-selected.
- Do not require semantic validators for applicability or completeness;
  review-skill fixtures own those judgments.
- Do not migrate every historical spec; prospective compatibility is the
  contract.
- Do not publish packages or contact registries; local archives and temporary
  installs are sufficient for this initiative.

## Uncovered gaps

None.

## Next artifacts

- `test-spec-review`
- M3 implementation only after approved test-spec-review and separate
  implementation authority

## Follow-on artifacts

None yet.

## Readiness

Active proof surface for the boundary-first initiative.
The active plan `Current Handoff Summary` owns the next workflow action,
including independent proof-adequacy review and separate implementation
authority.
