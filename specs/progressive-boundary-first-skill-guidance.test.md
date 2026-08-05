<!-- Template: test-spec-skeleton-v1 -->
<!-- Skill: test-spec -->
<!-- Template status: normative -->
<!-- Maintained alongside: skills/test-spec/SKILL.md -->

# Progressive Boundary-First Skill Guidance Test Spec

## Owning change record

`docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/change.yaml`

## Related spec and plan

- Spec: `specs/progressive-boundary-first-skill-guidance.md`
- Plan:
  `docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md`
- Architecture: `docs/architecture/system/architecture.md`
- ADR:
  `docs/adr/ADR-20260729-progressive-boundary-guidance-resources.md`

## Input artifact identities

| Input | Path | Artifact ID | Review evidence |
| --- | --- | --- | --- |
| Feature spec | `specs/progressive-boundary-first-skill-guidance.md` | `spec` | `spec-review-r1`; `docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/reviews/spec-review-r1.md` |
| Architecture | `docs/architecture/system/architecture.md` | `architecture` | `architecture-review-r2`; `docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/reviews/architecture-review-r2.md` |
| Resource ADR | `docs/adr/ADR-20260729-progressive-boundary-guidance-resources.md` | `adr-progressive-boundary-resources` | `architecture-review-r2`; `docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/reviews/architecture-review-r2.md` |
| Execution plan | `docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md` | `plan` | `plan-review-r2`; `docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/reviews/plan-review-r2.md` |

## Testing strategy

Fixture-backed unit tests prove the closed resource manifest, safe paths,
projection identities, activation fields, fail-closed vocabularies, and
selector classifications.
Integration tests prove resource ownership across all ten governed skills,
prompt-independent compact scanning, stable-ID slice consumption, upstream
routing, mixed changed-set composition, and structural-versus-semantic claim
boundaries.
Local end-to-end tests generate temporary Codex, Claude, and opencode
packages, install them into empty temporary targets, and compare every mapped
resource without network or publication.
Smoke proof runs the repository-owned broad-smoke command only after all four
milestones close their focused tests.
Compatibility tests distinguish repository-live `pending` behavior from
isolated active-candidate, grandfathering, preactivation rollback, and
immutable-release rollback fixtures.
No manual proof is required because every accepted outcome is deterministically
observable from repository-local fixtures, temporary package trees, and
stable validation output.

The proof set is deliberately outcome-driven.
Cases combine partitions only when a boundary or selected interaction changes
the expected result; they do not enumerate a Cartesian product.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| PBS-R001 | T5, T13 | contract, migration | Only the named refinement surfaces change; non-conflicting behavior remains. |
| PBS-R002 | T1, T5 | unit, integration | Version, vocabulary, identifiers, and record ownership remain `boundary-first-v1`. |
| PBS-R003 | T2, T3, T15 | integration, e2e | Pending state and complete atomic candidate closure are distinct. |
| PBS-R004 | T3, T4 | integration | Pending fixtures cannot claim active formal adoption. |
| PBS-R005 | T3, T4, T13 | integration, migration | Active new behavior specs adopt automatically without method-name opt-in. |
| PBS-R006 | T3, T4, T13 | integration, migration | M2 guidance and M4 state fixtures distinguish grandfathered revision classes. |
| PBS-R007 | T4 | integration | All ten governed skills contain and apply the exact four-question scan. |
| PBS-R008 | T4, T7 | integration | Scan-only and duplicate-outcome cases create no formal artifacts or inventory. |
| PBS-R009 | T4 | integration | Non-behavior work continues without formal adoption. |
| PBS-R010 | T4, T6 | integration | Active IDs are followed without repeating the method name. |
| PBS-R011 | T4, T6 | integration | Formalization and upstream gaps receive concise explanations without redundant consent. |
| PBS-R012 | T1, T5 | unit, integration | Exactly four non-overlapping logical ownership layers are enforced. |
| PBS-R013 | T1 | contract | Exact filenames, manifest fields, identities, and aliases follow the ADR. |
| PBS-R014 | T1, T5, T11 | integration, e2e | Every package contains exactly its stage-family resource set. |
| PBS-R015 | T1, T5 | unit, integration | Resource verbs, load conditions, containment, and unknown layers fail closed. |
| PBS-R016 | T4, T12 | integration | Inline scanning needs no formal-resource read for non-behavior work. |
| PBS-R017 | T5, T6, T14 | integration | Each stage consumes and contributes only its approved surface. |
| PBS-R018 | T6, T14 | integration | Downstream stages begin with exact slices and never redefine upstream IDs. |
| PBS-R019 | T6 | integration | Every invalid, stale, conflicting, or insufficient ID expands or routes. |
| PBS-R020 | T6, T14 | integration | New outcomes route to `spec`; proof-only gaps route to `test-spec`. |
| PBS-R021 | T6, T7 | integration | Scenarios correspond to distinct outcomes or material hazards. |
| PBS-R022 | T7 | integration | Proof stops after all outcomes and hazards are covered. |
| PBS-R023 | T7 | integration | No stage or validator requires Cartesian combinations. |
| PBS-R024 | T6, T7 | integration | Ownerless behavior becomes a discovery and blocks downstream reliance. |
| PBS-R025 | T8, T9 | integration | Skill wording alone never selects artifact-lifecycle validation. |
| PBS-R026 | T8, T9 | integration | Skill-only changes retain every purpose-built check. |
| PBS-R027 | T8 | integration | Selector changes select `selector.regression`. |
| PBS-R028 | T9, T16 | integration | Governed artifacts and change records retain lifecycle checks. |
| PBS-R029 | T9, T15 | integration | Mixed sets preserve both check families and owned affected paths. |
| PBS-R030 | T8, T14 | integration | Skill prose checks remain skill-owned and cannot settle lifecycle state. |
| PBS-R031 | T1, T8, T14 | unit, integration | Deterministic validators make structural claims only. |
| PBS-R032 | T1, T2, T11 | unit, e2e | Canonical owners and all projections preserve byte identity. |
| PBS-R033 | T1, T2, T11 | unit, e2e | Missing, additional, stale, mixed, path, and byte divergence fail closed. |
| PBS-R034 | T2, T3, T11, T15 | integration, e2e | Partial progressive activation cannot become accepted state. |
| PBS-R035 | T3, T4, T13 | migration | M2 guidance preserves grandfathering; M4 proves historical and package compatibility. |
| PBS-R036 | T3, T13, T15 | migration, e2e | Pre- and post-activation rollback restore one coherent bundle. |
| PBS-R037 | T1, T6, T8, T9, T10, T11 | integration | Diagnostics identify the stable surface and reason without private paths. |
| PBS-R038 | T1, T10, T11, T12 | e2e, smoke | Proof and use remain repository-local, portable, and network-independent. |

## Acceptance criterion coverage map

| Acceptance criterion | Covered by | Level | Notes |
| --- | --- | --- | --- |
| AC-PBS-001 | T4 | integration | Prompt-independent scan across all governed skills. |
| AC-PBS-002 | T4, T7 | integration | Non-behavior and duplicate-outcome restraint. |
| AC-PBS-003 | T1, T5 | contract | One version, vocabulary, record pair, and responsibility model. |
| AC-PBS-004 | T1, T5 | integration | Closed, non-overlapping resource ownership. |
| AC-PBS-005 | T1, T5, T11 | e2e | Exact stage-family package inventory. |
| AC-PBS-006 | T6, T14 | integration | Slice-first reads and correct upstream routing. |
| AC-PBS-007 | T7 | integration | Distinct-outcome and hazard-driven scenario stop rule. |
| AC-PBS-008 | T8 | integration | Purpose-built skill-only selection. |
| AC-PBS-009 | T9, T16 | integration | Governed-artifact and mixed-set lifecycle selection. |
| AC-PBS-010 | T2, T11 | e2e | Canonical through installed byte parity. |
| AC-PBS-011 | T1, T2, T11 | unit, e2e | Every defined resource divergence fails closed. |
| AC-PBS-012 | T3, T15 | integration | Pending state and atomic candidate closure. |
| AC-PBS-013 | T3, T13 | migration | Grandfathering and coherent rollback. |
| AC-PBS-014 | T14 | integration | Semantic review remains separate from deterministic validation. |
| AC-PBS-015 | T10 | integration | Actionable repository-relative privacy-bounded diagnostics. |
| AC-PBS-016 | T12 | integration | Measurements are recorded without a hard budget. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | T4 | A behavior-changing request without a method name still scans and adopts only in the active fixture. |
| E2 | T4 | Spelling-only work scans but creates no boundary or proof record. |
| E3 | T6 | Implementation consumes cited rows before any compact-core expansion. |
| E4 | T7 | A materially different sibling outcome adds proof; duplicate outcomes do not. |
| E5 | T8 | Canonical skill-only changes receive purpose-built checks without lifecycle validation. |
| E6 | T9 | Mixed skill-and-spec changes retain both check families with owned paths. |

## Boundary and interaction proof map

Boundary model version: boundary-first-v1

Boundary model scope: PBS-R001, PBS-R002, PBS-R003, PBS-R004, PBS-R005, PBS-R006, PBS-R007, PBS-R008, PBS-R009, PBS-R010, PBS-R011, PBS-R012, PBS-R013, PBS-R014, PBS-R015, PBS-R016, PBS-R017, PBS-R018, PBS-R019, PBS-R020, PBS-R021, PBS-R022, PBS-R023, PBS-R024, PBS-R025, PBS-R026, PBS-R027, PBS-R028, PBS-R029, PBS-R030, PBS-R031, PBS-R032, PBS-R033, PBS-R034, PBS-R035, PBS-R036, PBS-R037, PBS-R038

| Proof obligation ID | Coverage state | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Proof level | Automation mode | Command IDs | Evidence artifact | Required milestone | Manual procedure IDs | Uncovered gap ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRF-001 | covered | PBS-R005, PBS-R007, PBS-R008, PBS-R009, PBS-R010 | BND-INPUT-001 | T4 | integration | automated | CMD5 | `evidence/m2-skill-guidance.md` | M2 | - | - |
| PRF-002 | covered | PBS-R015, PBS-R019, PBS-R021, PBS-R022 | BND-INPUT-002 | T6, T7 | integration | automated | CMD5 | `evidence/m2-skill-guidance.md` | M2 | - | - |
| PRF-003 | covered | PBS-R003, PBS-R004, PBS-R005, PBS-R006, PBS-R034 | BND-STATE-001 | T3, T15 | integration | automated | CMD3, CMD4 | `evidence/m4-package-readiness.md` | M4 | - | - |
| PRF-004 | covered | PBS-R034, PBS-R036 | BND-STATE-002 | T3, T13 | integration | automated | CMD3 | `evidence/m4-package-readiness.md` | M4 | - | - |
| PRF-005 | covered | PBS-R012, PBS-R014, PBS-R017 | BND-AUTH-001 | T1, T5 | integration | automated | CMD1, CMD5 | `evidence/m1-resource-projection.md` | M1 | - | - |
| PRF-006 | covered | PBS-R017, PBS-R018, PBS-R020, PBS-R031 | BND-AUTH-002 | T6, T14 | integration | automated | CMD5 | `evidence/m2-skill-guidance.md` | M2 | - | - |
| PRF-007 | covered | PBS-R025, PBS-R026, PBS-R028, PBS-R030 | BND-AUTH-003 | T8, T9 | integration | automated | CMD8, CMD9, CMD10 | `evidence/m3-selector-routing.md` | M3 | - | - |
| PRF-008 | covered | PBS-R014, PBS-R032, PBS-R033 | BND-COMPOSE-001 | T2, T11 | end-to-end | automated | CMD1, CMD2, CMD12, CMD13 | `evidence/m4-package-readiness.md` | M4 | - | - |
| PRF-009 | covered | PBS-R017, PBS-R018, PBS-R019, PBS-R021, PBS-R022, PBS-R023 | BND-COMPOSE-002 | T6, T7 | integration | automated | CMD5 | `evidence/m2-skill-guidance.md` | M2 | - | - |
| PRF-010 | covered | PBS-R026, PBS-R027, PBS-R028, PBS-R029 | BND-COMPOSE-003 | T8, T9 | integration | automated | CMD8, CMD9, CMD10 | `evidence/m3-selector-routing.md` | M3 | - | - |
| PRF-011 | covered | PBS-R003, PBS-R021, PBS-R022, PBS-R024, PBS-R033, PBS-R034, PBS-R036 | BND-TEMPORAL-001 | T2, T3, T7 | integration | automated | CMD1, CMD3 | `evidence/m4-package-readiness.md` | M4 | - | - |
| PRF-012 | covered | PBS-R015, PBS-R019, PBS-R020, PBS-R024, PBS-R037 | BND-RECOVERY-001 | T1, T6 | integration | automated | CMD1, CMD5 | `evidence/m2-skill-guidance.md` | M2 | - | - |
| PRF-013 | covered | PBS-R029, PBS-R033, PBS-R034, PBS-R036 | BND-RECOVERY-002 | T2, T3, T9, T11 | end-to-end | automated | CMD3, CMD8, CMD12, CMD13 | `evidence/m4-package-readiness.md` | M4 | - | - |
| PRF-014 | covered | PBS-R001, PBS-R002, PBS-R004, PBS-R006, PBS-R035 | BND-COMPAT-001 | T4 | integration | automated | CMD5 | `evidence/m2-skill-guidance.md` | M2 | - | - |
| PRF-015 | covered | PBS-R025, PBS-R028, PBS-R029, PBS-R036 | BND-COMPAT-002 | T9, T13 | migration | automated | CMD3, CMD8 | `evidence/m4-package-readiness.md` | M4 | - | - |
| PRF-016 | covered | PBS-R032, PBS-R033, PBS-R034, PBS-R037, PBS-R038 | BND-ENV-001 | T10, T11 | end-to-end | automated | CMD12, CMD13 | `evidence/m4-package-readiness.md` | M4 | - | - |
| PRF-017 | covered | PBS-R003, PBS-R014, PBS-R032, PBS-R033, PBS-R034 | INT-001 | T15 | end-to-end | automated | CMD3, CMD12, CMD13 | `evidence/m4-package-readiness.md` | M4 | - | - |
| PRF-018 | covered | PBS-R018, PBS-R019, PBS-R020, PBS-R021 | INT-002 | T6 | integration | automated | CMD5 | `evidence/m2-skill-guidance.md` | M2 | - | - |
| PRF-019 | covered | PBS-R025, PBS-R026, PBS-R028, PBS-R029 | INT-003 | T9 | integration | automated | CMD8, CMD10 | `evidence/m3-selector-routing.md` | M3 | - | - |
| PRF-020 | covered | PBS-R005, PBS-R006, PBS-R007, PBS-R009, PBS-R035 | INT-004 | T4 | integration | automated | CMD5 | `evidence/m2-skill-guidance.md` | M2 | - | - |
| PRF-021 | covered | PBS-R015, PBS-R032, PBS-R033, PBS-R036, PBS-R038 | INT-005 | T11 | end-to-end | automated | CMD12, CMD13 | `evidence/m4-package-readiness.md` | M4 | - | - |
| PRF-022 | covered | PBS-R001, PBS-R002, PBS-R004, PBS-R006, PBS-R035 | BND-COMPAT-001 | T3, T13 | migration | automated | CMD3 | `evidence/m4-package-readiness.md` | M4 | - | - |
| PRF-023 | covered | PBS-R005, PBS-R006, PBS-R007, PBS-R009, PBS-R035 | INT-004 | T3, T13 | integration | automated | CMD3 | `evidence/m4-package-readiness.md` | M4 | - | - |

All evidence paths in this table are relative to
`docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/`.

## Edge case coverage

| Edge case | Covered by | Notes |
| --- | --- | --- |
| EC1 unnamed method on behavior work | T4 | Scan and active-only adoption do not depend on prompt wording. |
| EC2 named method on spelling-only work | T4 | No formal record is created. |
| EC3 formatting-only grandfathered edit | T4, T13 | M2 guidance and M4 state fixtures both preserve non-substantive classification. |
| EC4 unknown outcome while pending | T3, T6 | Gap routes without an active claim. |
| EC5 valid but insufficient sibling slice | T6 | Context expands and missing ownership stops. |
| EC6 duplicate-outcome inputs | T7 | No additional scenario is required. |
| EC7 distinct recovery outcome | T7 | Recovery proof remains required. |
| EC8 unowned proof guidance mapping | T1, T5 | Resource validation fails. |
| EC9 missing owner-family guidance | T1, T11 | Package-integrity validation fails. |
| EC10 mixed skill and feature-spec paths | T9 | Both check families remain selected. |
| EC11 generated skill path only | T8 | Derivation and drift checks run without lifecycle validation. |
| EC12 lifecycle words in skill prose | T8 | Classification remains path-owned. |
| EC13 installed adapter missing family resource | T11 | First divergent installed layer fails. |
| EC14 repeated complete projection | T2 | Bytes and aggregate identity remain stable. |
| EC15 interrupted partial projection | T2, T15 | Partial matrix cannot activate. |
| EC16 runtime fallback for missing package resource | T11 | Fallback cannot establish parity. |
| EC17 future hard context budget | T12 | Current proof records measurements only and rejects a threshold. |

## Validation commands

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMD1 | `python scripts/test-boundary-first-reference.py` | existing/configured | implement | M1 | code-review M1 | Block M1 on manifest, path, projection, or identity failure. | Zero tests is failure. | `evidence/m1-resource-projection.md` | Repository-local temporary fixtures only. |
| CMD2 | `python scripts/project-boundary-first-reference.py --check` | existing/configured | implement | M1 | code-review M1 | Block on missing, additional, stale, or divergent projections. | Not applicable; deterministic check. | `evidence/m1-resource-projection.md` | Read-only check; `--write` remains implementation-scoped. |
| CMD3 | `python scripts/test-boundary-first-validation.py` | existing/configured | implement | M1, M4 | code-review M1 | Block the owning milestone on structural, activation, compatibility, or rollback regression. | Zero tests is failure. | `evidence/m1-resource-projection.md`; `evidence/m4-package-readiness.md` | Repository-local temporary fixtures only. |
| CMD4 | `python scripts/validate-boundary-first.py --check` | existing/configured | implement | M1, M2, M4 | code-review M1 | Block when repository-live records, resources, or pending activation are inconsistent. | Not applicable; deterministic check. | Owning milestone evidence. | Read-only repository check. |
| CMD5 | `python scripts/test-skill-validator.py` | existing/configured | implement | M1, M2 | code-review M1 | Block on resource-map, shared-scan, ownership, routing, or semantic-claim regression. | Zero tests is failure. | `evidence/m1-resource-projection.md`; `evidence/m2-skill-guidance.md` | Local fixtures only. |
| CMD6 | `python scripts/validate-skills.py` | existing/configured | implement | M1, M2 | code-review M1 | Block canonical skill handoff. | Not applicable; deterministic validator. | Owning milestone evidence. | Read-only canonical validation. |
| CMD7 | `python scripts/build-skills.py --check` | existing/configured | implement | M2, M4 | code-review M2 | Block generated-skill parity. | Not applicable; build check. | `evidence/m2-skill-guidance.md`; `evidence/m4-package-readiness.md` | Temporary output only; no canonical mutation. |
| CMD8 | `python scripts/test-select-validation.py` | existing/configured | implement | M3 | code-review M3 | Block selector routing or affected-path handoff. | Zero tests is failure. | `evidence/m3-selector-routing.md` | Local fixtures only. |
| CMD9 | `python scripts/select-validation.py --mode explicit --path skills/spec/SKILL.md` | existing/configured | implement | M3 | code-review M3 | Block if skill-only selection includes lifecycle validation or omits owned checks. | Not applicable; deterministic selector. | `evidence/m3-selector-routing.md` | Read-only selection; executes no selected checks. |
| CMD10 | `python scripts/select-validation.py --mode explicit --path skills/spec/SKILL.md --path specs/progressive-boundary-first-skill-guidance.md` | existing/configured | implement | M3 | code-review M3 | Block unless mixed selection preserves both families and exact affected paths. | Not applicable; deterministic selector. | `evidence/m3-selector-routing.md` | Read-only selection; executes no selected checks. |
| CMD11 | `python scripts/test-artifact-lifecycle-validator.py` | existing/configured | implement | M3 | code-review M3 | Block if the exact-owning-change-record prerequisite regresses. | Zero tests is failure. | `evidence/m3-selector-routing.md` | Local fixtures only; prerequisite is not reimplemented. |
| CMD12 | `python scripts/test-adapter-distribution.py` | existing/configured | implement | M4 | code-review M4 | Block adapter archive or installed-resource parity. | Zero tests is failure. | `evidence/m4-package-readiness.md` | Local fixtures and temporary archives only. |
| CMD13 | `tmp_output="$(mktemp -d)" && python scripts/build-adapters.py --version v0.1.5 --output-dir "$tmp_output" && python scripts/validate-adapters.py --root "$tmp_output" --version v0.1.5 --clean-install-smoke --skill workflow --skill spec --skill spec-review --skill plan --skill plan-review --skill test-spec --skill test-spec-review --skill implement --skill code-review --skill verify` | existing/configured | implement | M4 | code-review M4 | Block on generation, archive, or clean-install divergence for any supported adapter. | Not applicable; deterministic build and validation. | `evidence/m4-package-readiness.md` | Version comes from tracked manifest; temporary local output only; no network, registry, or publication. |
| CMD14 | `bash scripts/ci.sh --mode broad-smoke` | ci-owned | implement | M4 | code-review M4 | Block M4 integration closeout. | Zero selected tests is failure. | Change metadata validation entry and `evidence/m4-package-readiness.md` | Repository-local validation; no publication. |
| CMD15 | `python scripts/validate-change-metadata.py docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/change.yaml` | existing/configured | test-spec | lifecycle | test-spec authoring | Block an invalid authoring or review transition. | Not applicable; deterministic validator. | Change metadata validation entry. | Read-only metadata validation. |
| CMD16 | `python scripts/validate-review-artifacts.py docs/changes/2026-07-29-progressive-boundary-first-skill-guidance` | existing/configured | test-spec-review | lifecycle | test-spec-review | Block malformed or unindexed review evidence. | Not applicable; deterministic validator. | Review log. | Read-only review validation. |
| CMD17 | `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/progressive-boundary-first-skill-guidance.test.md --path docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/change.yaml --path docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/evidence/test-spec-authoring.md` | existing/configured | test-spec | lifecycle | test-spec authoring | Block incomplete test-spec authoring evidence or illegal settlement. | Not applicable; deterministic validator. | Change metadata validation entry. | Read-only explicit-path validation. |

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Preimplementation gate | T1-T16 | none | CMD15, CMD16, CMD17 | This test spec, authoring evidence, and test-spec-review record | implementation handoff | Every requirement, boundary, interaction, example, edge case, and command is mapped before M1. |
| M1 | T1, T2, T5 | none | CMD1, CMD2, CMD3, CMD4, CMD5, CMD6 | `evidence/m1-resource-projection.md` | code-review M1 | Proves the closed manifest, resource ownership, safe projection transaction, and pending identities. |
| M2 | T4, T5, T6, T7, T10, T14 | none | CMD2, CMD4, CMD5, CMD6, CMD7 | `evidence/m2-skill-guidance.md` | code-review M2 | Proves automatic concise scanning, activation-aware compatibility guidance, stage authority, slice routing, projection currency, and scenario restraint. |
| M3 | T8, T9, T10, T16 | none | CMD8, CMD9, CMD10, CMD11 | `evidence/m3-selector-routing.md` | code-review M3 | Proves skill-only, lifecycle-only, mixed, generated-only, and selector-change routing. |
| M4 | T3, T10, T11, T12, T13, T15 | none | CMD1, CMD3, CMD4, CMD5, CMD6, CMD7, CMD12, CMD13, CMD14 | `evidence/m4-package-readiness.md` | code-review M4 | Proves package parity, loading measurements, pending state, isolated active candidate, and both rollback modes. |

## Test cases

### T1. Closed resource manifest and mappings fail closed

- Covers: PBS-R002, PBS-R012-PBS-R015, PBS-R031-PBS-R033, PBS-R037, PBS-R038, AC-PBS-003-AC-PBS-005, AC-PBS-011, BND-AUTH-001, BND-RECOVERY-001
- Level: unit
- Command IDs: CMD1, CMD3, CMD5
- Fixture/setup: Exact ADR manifest plus missing, additional, duplicate, unknown-value, unsafe-path, escaping, symlink, missing-source, unknown-consumer, and unowned-mapping variants.
- Steps: Parse every variant, resolve the complete consumer matrix, and inspect validation order and diagnostics.
- Expected result: The exact three-resource manifest passes; every closed-vocabulary or containment defect fails before dependent consistency checks and before projection mutation.
- Failure proves: Resource or authority drift can enter the published package set.
- Evidence artifact: `evidence/m1-resource-projection.md`
- Automation location: `scripts/test-boundary-first-reference.py`; `scripts/test-boundary-first-validation.py`; `scripts/test-skill-validator.py`
- Required by milestone: M1

### T2. Projection is atomic, byte-exact, and retry-safe

- Covers: PBS-R003, PBS-R014, PBS-R015, PBS-R032-PBS-R034, AC-PBS-010-AC-PBS-012, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-002
- Level: integration
- Command IDs: CMD1, CMD2, CMD3
- Fixture/setup: Canonical resources, complete expected targets, interrupted preflight/write doubles, repeated writes, and missing, extra, stale, path-divergent, byte-divergent, and mixed-version trees.
- Steps: Preflight the full matrix, write twice, interrupt before commit, perturb each layer, and recompute manifest and sorted projection-set identities.
- Expected result: Complete retries preserve raw bytes and identities; invalid input performs no partial mutation; every incomplete or divergent set blocks.
- Failure proves: Projection can expose or accept a mixed resource bundle.
- Evidence artifact: `evidence/m1-resource-projection.md`
- Automation location: `scripts/test-boundary-first-reference.py`; `scripts/test-boundary-first-validation.py`
- Required by milestone: M1

### T3. Activation and rollback preserve coherent state

- Covers: PBS-R003-PBS-R006, PBS-R034-PBS-R036, AC-PBS-012, AC-PBS-013, BND-STATE-001, BND-STATE-002, BND-COMPAT-001, BND-COMPAT-002
- Level: integration
- Command IDs: CMD3, CMD4
- Fixture/setup: Repository-live pending manifest, isolated complete and partial active candidates, preactivation source rollback, immutable release metadata, and invalid rollback package identities.
- Steps: Validate pending, candidate, activation, grandfathering, and both rollback paths without changing the live repository marker.
- Expected result: Pending never claims active adoption; only a complete isolated candidate passes readiness; rollback selects one coherent pending tree or immutable release.
- Failure proves: Formal adoption or rollback can expose partial or invented state.
- Evidence artifact: `evidence/m4-package-readiness.md`
- Automation location: `scripts/test-boundary-first-validation.py`
- Required by milestone: M4

### T4. Compact scanning and compatibility guidance are automatic and proportional

- Covers: PBS-R004-PBS-R011, PBS-R016, PBS-R035, E1, E2, EC1, EC2, EC3, AC-PBS-001, AC-PBS-002, BND-INPUT-001, BND-COMPAT-001, INT-004
- Level: integration
- Command IDs: CMD5, CMD6
- Fixture/setup: All ten governed skill bodies and equivalent behavior, non-behavior, named-method, unnamed-method, pending, isolated active-contract, grandfathered non-substantive, and grandfathered substantive invocations.
- Steps: Apply the four-question decision and compatibility guidance to each fixture and compare artifacts, classification, explanations, consent prompts, and stage routing.
- Expected result: Prompt wording never controls scanning; non-behavior work stays concise; pending work makes no active claim; active qualifying work formalizes automatically; grandfathered non-substantive work remains valid; substantive post-activation work routes through formal adoption.
- Failure proves: Users must know the method name, simple work receives unnecessary machinery, or M2 guidance applies active adoption to the wrong compatibility state.
- Evidence artifact: `evidence/m2-skill-guidance.md`
- Automation location: `scripts/test-skill-validator.py`
- Required by milestone: M2

### T5. Stage-family resources and responsibilities remain exact

- Covers: PBS-R001, PBS-R002, PBS-R012-PBS-R018, PBS-R031, PBS-R032, AC-PBS-003-AC-PBS-005, EC8, EC9, BND-AUTH-001
- Level: integration
- Command IDs: CMD1, CMD5, CMD6, CMD7
- Fixture/setup: Expected resource set, `READ` mapping, load condition, and stage authority for each of the ten governed skills plus missing and additional family-resource mutations.
- Steps: Compare each canonical and generated skill with the closed ownership matrix and prohibited stage contributions.
- Expected result: Every skill has compact core; only spec family has feature guidance; only test-spec family has proof guidance; stage-local mutation and review authority remain unchanged.
- Failure proves: Progressive loading created semantic duplication, missing guidance, or cross-stage authority.
- Evidence artifact: `evidence/m1-resource-projection.md`; `evidence/m2-skill-guidance.md`
- Automation location: `scripts/test-boundary-first-reference.py`; `scripts/test-skill-validator.py`
- Required by milestone: M1 and M2

### T6. Slice expansion and upstream routing preserve ownership

- Covers: PBS-R010, PBS-R011, PBS-R017-PBS-R021, PBS-R024, PBS-R037, E3, EC4, EC5, AC-PBS-006, BND-INPUT-002, BND-AUTH-002, BND-COMPOSE-002, BND-RECOVERY-001, INT-002
- Level: integration
- Command IDs: CMD5
- Fixture/setup: Known, missing, stale, unknown, ambiguous, conflicting, escaped, and insufficient cited rows plus a sibling path with an owned and an unowned distinct outcome.
- Steps: Begin with exact cited rows, exercise each expansion trigger, and inspect the resulting read expansion, stop reason, and owner route.
- Expected result: Valid sufficient slices proceed; invalid or insufficient slices expand; new behavior routes to `spec`; proof-only gaps route to `test-spec`.
- Failure proves: A downstream stage can guess, redefine, or silently omit governed behavior.
- Evidence artifact: `evidence/m2-skill-guidance.md`
- Automation location: `scripts/test-skill-validator.py`
- Required by milestone: M2

### T7. Scenario selection stops at distinct outcomes and hazards

- Covers: PBS-R008, PBS-R021-PBS-R024, E4, EC6, EC7, AC-PBS-002, AC-PBS-007, BND-COMPOSE-002, BND-TEMPORAL-001
- Level: integration
- Command IDs: CMD5
- Fixture/setup: Duplicate input partitions with one outcome, shared inputs with distinct recovery, public/helper/sibling divergence, retry/idempotency hazard, and ownerless discovery.
- Steps: Select the minimum scenario set, then offer redundant and materially distinct candidates.
- Expected result: Every distinct outcome and hazard remains; duplicate outcome combinations stop; ownerless behavior records a discovery and routes upstream.
- Failure proves: The method either misses material proof or recreates a Cartesian inventory.
- Evidence artifact: `evidence/m2-skill-guidance.md`
- Automation location: `scripts/test-skill-validator.py`
- Required by milestone: M2

### T8. Skill-only and generated-only selector routes stay purpose-built

- Covers: PBS-R025-PBS-R027, PBS-R030, PBS-R031, PBS-R037, E5, EC11, EC12, AC-PBS-008, BND-AUTH-003, BND-COMPOSE-003
- Level: integration
- Command IDs: CMD8, CMD9
- Fixture/setup: Canonical skill-only, generated skill-only, lifecycle-like prose, boundary resource, projection script, adapter surface, and selector-owning changed sets.
- Steps: Select checks and affected paths for each set, including a selector-code change.
- Expected result: Skill paths omit lifecycle validation but retain every owned check; selector changes add regression; prose wording never changes ownership.
- Failure proves: The checker remains irrelevant or purpose-built skill coverage is lost.
- Evidence artifact: `evidence/m3-selector-routing.md`
- Automation location: `scripts/test-select-validation.py`
- Required by milestone: M3

### T9. Governed-artifact and mixed selector routes retain lifecycle proof

- Covers: PBS-R025, PBS-R026, PBS-R028, PBS-R029, PBS-R037, E6, EC10, AC-PBS-009, BND-AUTH-003, BND-COMPOSE-003, BND-COMPAT-002, INT-003
- Level: integration
- Command IDs: CMD8, CMD10, CMD11
- Fixture/setup: Lifecycle-only proposal, spec, test spec, architecture, ADR, plan, review, and change-record paths plus mixed skill-and-spec sets.
- Steps: Select checks, compare check-owned affected paths, and run exact-owner lifecycle regression fixtures.
- Expected result: Every governed path retains lifecycle validation; mixed sets retain both families; neither affected-path set is broadened by the other.
- Failure proves: Removing an irrelevant skill route suppresses governed-artifact safety.
- Evidence artifact: `evidence/m3-selector-routing.md`
- Automation location: `scripts/test-select-validation.py`; `scripts/test-artifact-lifecycle-validator.py`
- Required by milestone: M3

### T10. Diagnostics are actionable, portable, and privacy-bounded

- Covers: PBS-R031, PBS-R037, PBS-R038, AC-PBS-015, BND-ENV-001
- Level: integration
- Command IDs: CMD1, CMD3, CMD5, CMD8, CMD12
- Fixture/setup: Representative resource, ID, selector, package, unavailable-tool, secret-like, absolute-private-path, and repository-relative failures.
- Steps: Trigger one failure per surface and inspect bounded diagnostic fields.
- Expected result: Diagnostics name the affected surface, stable check or ID, expected outcome, and reason using repository-relative redacted evidence; unavailable proof is never success.
- Failure proves: Failures cannot be resolved safely or leak environment-specific data.
- Evidence artifact: Owning milestone evidence.
- Automation location: Boundary, skill, selector, and adapter regression tests.
- Required by milestone: M1 through M4

### T11. Packages preserve every mapped resource without fallback

- Covers: PBS-R014, PBS-R015, PBS-R032-PBS-R034, PBS-R037, PBS-R038, EC13, EC16, AC-PBS-005, AC-PBS-010, AC-PBS-011, BND-COMPOSE-001, BND-RECOVERY-002, BND-ENV-001, INT-005
- Level: e2e
- Command IDs: CMD7, CMD12, CMD13
- Fixture/setup: Canonical, generated, packed, and clean-installed Codex, Claude, and opencode skill roots plus missing, additional, stale, path-divergent, and byte-divergent resources.
- Steps: Build into a temporary versioned directory, install into empty temporary targets, compare mapped identities, perturb each layer, and offer a runtime fallback.
- Expected result: Complete trees match byte-for-byte; the first divergent layer fails; runtime fallback cannot satisfy package integrity.
- Failure proves: Published consumers can receive a different or incomplete boundary contract.
- Evidence artifact: `evidence/m4-package-readiness.md`
- Automation location: `scripts/test-adapter-distribution.py`; `scripts/validate-adapters.py`
- Required by milestone: M4

### T12. Loading measurements remain descriptive

- Covers: PBS-R016, PBS-R038, AC-PBS-016, EC17
- Level: integration
- Command IDs: CMD3, CMD5
- Fixture/setup: Closed loading-profile fixture for every representative stage family and before/after canonical resource bytes and mapped counts.
- Steps: Validate mapped, initially loaded, and permitted-expansion resource IDs; record counts; inject an unapproved threshold.
- Expected result: Stable measurements are emitted without runtime telemetry or a pass/fail budget; an unapproved threshold is rejected.
- Failure proves: Progressive loading is unmeasured or measurement silently becomes product policy.
- Evidence artifact: `evidence/m4-package-readiness.md`
- Automation location: `scripts/test-boundary-first-validation.py`; `scripts/test-skill-validator.py`
- Required by milestone: M4

### T13. Grandfathering and rollback remain compatible

- Covers: PBS-R001, PBS-R003-PBS-R006, PBS-R035, PBS-R036, EC3, AC-PBS-013, BND-STATE-002, BND-COMPAT-001, BND-COMPAT-002, INT-004
- Level: integration
- Command IDs: CMD3
- Fixture/setup: Accepted historical artifacts, formatting-only and substantive revisions, new post-activation specs, pending mappings, and immutable release rollback metadata.
- Steps: Classify each revision, validate active-only adoption, then exercise pre- and post-activation rollback fixtures.
- Expected result: History remains valid; formatting-only edits stay grandfathered; substantive post-activation work adopts; rollback restores one coherent prior bundle without rewriting artifacts.
- Failure proves: The refinement breaks accepted history or makes rollback mutable.
- Evidence artifact: `evidence/m4-package-readiness.md`
- Automation location: `scripts/test-boundary-first-validation.py`
- Required by milestone: M4

### T14. Structural validation cannot claim semantic settlement

- Covers: PBS-R017-PBS-R020, PBS-R030, PBS-R031, AC-PBS-006, AC-PBS-014, BND-AUTH-002
- Level: integration
- Command IDs: CMD5, CMD8
- Fixture/setup: Structurally valid but semantically incomplete feature, proof, plan, and skill fixtures plus diagnostics that attempt approval or completeness claims.
- Steps: Run structural checks, then apply the owning semantic-review expectations.
- Expected result: Structure may pass while semantic review reports the gap; validators never create, repair, approve, or settle semantic content.
- Failure proves: Deterministic tooling becomes a competing semantic owner.
- Evidence artifact: `evidence/m2-skill-guidance.md`; `evidence/m3-selector-routing.md`
- Automation location: `scripts/test-skill-validator.py`; `scripts/test-select-validation.py`
- Required by milestone: M2 and M3

### T15. One candidate identity closes every activation layer

- Covers: PBS-R003, PBS-R029, PBS-R032-PBS-R036, AC-PBS-009-AC-PBS-013, INT-001, BND-STATE-001, BND-COMPOSE-001, BND-RECOVERY-002, BND-TEMPORAL-001
- Level: e2e
- Command IDs: CMD3, CMD8, CMD12, CMD13
- Fixture/setup: Complete candidate identity plus stale resource, stale selector route, mixed package, interrupted projection, mismatched source revision, and rollback variants.
- Steps: Bind tracked and derived proof to one candidate, perturb each constituent independently, and attempt acceptance and recovery.
- Expected result: Only one fully coherent candidate can pass readiness; every partial state blocks before an active claim and preserves or restores the last coherent bundle.
- Failure proves: Individually passing layers can compose into a false activation.
- Evidence artifact: `evidence/m4-package-readiness.md`
- Automation location: Boundary, selector, and adapter integration fixtures.
- Required by milestone: M4

### T16. Exact-owner lifecycle validation remains an independent prerequisite

- Covers: PBS-R028, PBS-R029, AC-PBS-009
- Level: integration
- Command IDs: CMD8, CMD11
- Fixture/setup: Current stage-owned artifacts with exact, missing, duplicate, ambiguous, mismatched, unknown, and explicit legacy state ownership.
- Steps: Run the existing regression matrix, then compose its selected check with the M3 mixed-path route.
- Expected result: Exact current ownership fails closed while explicit legacy compatibility remains bounded; M3 does not reimplement or bypass the prerequisite.
- Failure proves: Selector refinement relies on a lifecycle validator that can resolve the wrong owner or silently pass unknown state.
- Evidence artifact: `evidence/m3-selector-routing.md`
- Automation location: `scripts/test-artifact-lifecycle-validator.py`; `scripts/test-select-validation.py`
- Required by milestone: M3

## Fixtures and data

- `specs/boundary-first-resources.yaml`: future exact live manifest authored in M1.
- `scripts/fixtures/boundary-first/loading-profiles.yaml`: future closed
  representative-loading fixture authored in M4.
- Existing temporary-fixture helpers in the boundary reference, boundary
  validation, skill validation, selector, lifecycle, and adapter test suites.
- Isolated active-candidate and rollback manifests created only in temporary
  fixtures; the repository-live activation record remains `pending`.
- Version `v0.1.5` read from `dist/adapters/manifest.yaml` for the M4 package
  command.
- Temporary generated, archive, and installed trees created beneath
  `mktemp -d` locations and discarded after proof.

Every fixture uses repository-relative expected paths.
Unknown-value fixtures must include `unknown_value` or `not_in_vocabulary` in
their test names when they exercise a closed vocabulary.

## Mocking/stubbing policy

Use filesystem and process-boundary doubles only for interruption,
unavailable-tool, runtime-fallback, and external-publication containment.
Do not mock manifest parsing, digest computation, selector composition,
resource-map resolution, archive contents, or installed-tree inspection.
No fixture may access a live registry, network service, user installation, or
secret store.

## Migration or compatibility tests

T3 and T13 own pending-versus-active behavior, grandfathered formatting and
substantive revisions, coherent preactivation source rollback, and immutable
post-activation package rollback.
T16 preserves explicit legacy lifecycle-state compatibility independently of
the progressive selector change.
Historical accepted artifacts and immutable release archives are read-only
fixtures and are never rewritten by a test.

## Observability verification

T10 verifies that each failure reports the affected skill or artifact, stable
check or feature ID, resource layer or cited ID, expected outcome, and
blocking reason.
Projection and package cases identify the first divergent layer.
Selector cases report selected check IDs and check-owned affected paths.
Evidence must remain bounded and repository-relative.

## Security/privacy verification

T10 injects secret-like values and private absolute paths and asserts that
diagnostics emit stable redacted identities and repository-relative paths
only.
All package and install proof uses empty temporary targets.
No command requires credentials, network access, publication, live registry
installation, or runtime attestation.

## Performance checks

T12 records canonical bytes, mapped-resource counts, and representative
initial and expanded loaded-resource counts.
The values are baselines only.
No hard byte, token, document-length, or runtime threshold is accepted by this
change.

## Manual QA checklist

Not applicable.
All required behavior, resource parity, selector routing, compatibility,
diagnostics, and loading measurements have deterministic automated proof.
Human semantic judgment remains part of formal review, not a repeatable manual
implementation test.

## What not to test and why

- Do not test every combination of boundary partitions; T7 selects distinct
  outcomes and material hazards.
- Do not activate the repository-live capability; M4 uses isolated candidate
  fixtures and leaves the accepted record `pending`.
- Do not publish, contact a registry, or modify a user installation; package
  proof is local and temporary.
- Do not enforce context-size or runtime budgets; the approved first slice
  authorizes measurements only.
- Do not reimplement the completed exact-owner lifecycle bug fix; T16 keeps
  its existing regression suite as a prerequisite.
- Do not test a runtime service, model identity, interceptor, or attestation
  store because the approved design excludes them.
- Do not hand-edit generated resources or adapter output; all derived proof
  comes from repository-owned generators.

## Uncovered gaps

None.

Every approved requirement, acceptance criterion, example, edge case,
boundary, and selected interaction has direct automated proof.
No proof obligation depends on an unknown command owner or manual procedure.

## Next artifacts

1. Complete independent `test-spec-review`.
2. If approved, implement M1 and its tests before production changes.
3. Repeat implementation and code-review for M2 through M4.

## Follow-on artifacts

None yet

## Readiness

Ready for `test-spec-review`.

This proof map does not claim that tests exist or commands pass.
Implementation remains blocked until an approved test-spec review allows the
M1 handoff.
