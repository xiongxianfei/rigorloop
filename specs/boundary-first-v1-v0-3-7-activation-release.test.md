<!-- Template: test-spec-skeleton-v1 -->
<!-- Skill: test-spec -->
<!-- Template status: normative -->

# Boundary-First v1 v0.4.0 Activation Release Test Spec

## Owning change record

`docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7/change.yaml`

## Related spec and plan

- Spec: `specs/boundary-first-v1-v0-3-7-activation-release.md`
- Plan: `docs/plans/2026-08-05-activate-boundary-first-v1-v0-4-0.md`
- Architecture: `docs/architecture/system/architecture.md`
- ADR: `docs/adr/ADR-20260805-boundary-first-activation-candidate-and-atomic-publication.md`

## Input artifact identities

| Input | Path | Artifact ID | Review evidence |
| --- | --- | --- | --- |
| Feature spec | `specs/boundary-first-v1-v0-3-7-activation-release.md` | `spec` | `spec-review-r5`; `docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7/reviews/spec-review-r5.md` |
| Architecture | `docs/architecture/system/architecture.md` | `architecture` | `architecture-review-activation-r3`; `docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7/reviews/architecture-review-activation-r3.md` |
| Activation publication ADR | `docs/adr/ADR-20260805-boundary-first-activation-candidate-and-atomic-publication.md` | `adr-activation-publication` | `architecture-review-activation-r3`; `docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7/reviews/architecture-review-activation-r3.md` |
| Execution plan | `docs/plans/2026-08-05-activate-boundary-first-v1-v0-4-0.md` | `plan` | `plan-review-r4`; `docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7/reviews/plan-review-r4.md` |

## Testing strategy

Fixture-backed unit and integration tests prove the candidate CLI, strict-mode
preservation, exact `P/B/T/R -> C ... H` topology, phase-specific path
classification, stable diagnostics, and side-effect freedom.
Local bare remotes prove atomic two-ref publication and every reject-without-
mutation outcome without touching a real remote.
Release-mode checks prove the v0.4.0 payload, v0.3.6 rollback, archive/package
parity, and tag-workflow composition.
Two release-owned manual procedures cover the irreversible boundary: local tag
plus detached-T proof, then atomic/public publication and closeout.

Cases are selected by distinct outcomes and authority crossings.
They do not enumerate a Cartesian product of Git states, release surfaces, or
boundary dimensions.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| BFA-R001 | T3, T10, T13 | contract, smoke | Exact stable release, package version, and dist-tag. |
| BFA-R002 | T3, T10, T11, T15 | integration, migration | Exact immediate rollback predecessor. |
| BFA-R003 | T3, T10 | contract | Contract version and ten-skill inventory remain exact. |
| BFA-R004 | T1 | integration | Exact opt-in command shape only. |
| BFA-R005 | T1, T3 | integration | Default strict behavior is unchanged. |
| BFA-R006 | T1, T3 | integration | Candidate accepts only active v0.4.0 with v0.3.6 rollback. |
| BFA-R007 | T1 | integration | Local/remote tag presence and unreachable remote block. |
| BFA-R008 | T2 | integration | Fresh remote main supplies full P. |
| BFA-R009 | T2, T4 | integration | Unique T and exact first-parent B. |
| BFA-R010 | T2, T4 | integration | Full candidate-validation head R and first-parent reachability. |
| BFA-R011 | T3, T16 | integration | Every non-tag strict invariant and sibling gate remains. |
| BFA-R012 | T2 | contract | Stable machine result exposes every required field. |
| BFA-R013 | T1, T2 | contract | Candidate result is explicitly non-public. |
| BFA-R014 | T5, T10, T11 | integration, smoke | T is self-contained for release proof. |
| BFA-R015 | T5, T12 | integration | Only owning lifecycle evidence may follow T through R, C, and H. |
| BFA-R016 | T5, T12 | integration | Candidate T..R and readiness T..H rejected paths are reported exactly. |
| BFA-R017 | T12 | integration, contract | Exact result at R is persisted by immediate child C and required lifecycle evidence settles before publication. |
| BFA-R018 | T7, T11, T12, MP1 | integration, manual, smoke | Local tag, strict H, publication readiness H, and detached T run before publication. |
| BFA-R019 | T11, MP1 | manual, smoke | Tag resolves to T and detached proof reads no H content. |
| BFA-R020 | T7, T9, T12, MP1 | integration, manual | Readiness-bound exact H feeds one atomic main/tag update only. |
| BFA-R021 | T7, T8 | integration | Same-push advertised main must equal P. |
| BFA-R022 | T8 | integration | Every ref/capability failure changes neither ref. |
| BFA-R023 | T8, T9 | integration | No sequential fallback; regeneration follows failure. |
| BFA-R024 | T9, T12, MP1, MP2 | contract, manual | All external mutation requires explicit release action. |
| BFA-R025 | T13, MP2 | smoke, manual | Tag workflow runs the repository release gate first. |
| BFA-R026 | T10, T13, MP2 | e2e, smoke | Trust, archives, packages, registry, and three-target smoke remain. |
| BFA-R027 | T8, T11 | integration, manual | Pre-publish recovery removes local state only. |
| BFA-R028 | T9, T14 | integration, manual | Post-publish recovery never rewrites published refs. |
| BFA-R029 | T15 | migration | Runtime rollback is exact v0.3.6 or fails. |
| BFA-R030 | T14, MP2 | integration, manual | Partial/delayed publication remains open and rerunnable. |
| BFA-R031 | T1, T2, T5, T8, T12 | integration | Candidate and readiness diagnostics expose bounded phase identities, invariant, and action. |
| BFA-R032 | T6 | integration | Candidate checks are deterministic and side-effect free. |
| BFA-R033 | T16 | integration | Candidate cannot bypass selected sibling gates. |
| BFA-R034 | T6, T10, T12, T13, MP1 | integration, smoke, manual | Candidate, readiness, checkpoint, atomic, package, and public evidence suppress private values. |
| BFA-R035 | T5, T8 | integration | Invalid post-T history is replaced and fully rereviewed. |

## Acceptance criterion coverage map

| Acceptance criterion | Covered by | Level | Notes |
| --- | --- | --- | --- |
| AC-BFA-001 | T1-T3 | integration | Candidate succeeds without the absent tag and remains non-public. |
| AC-BFA-002 | T1, T3 | integration | Default validation fails without the tag. |
| AC-BFA-003 | T2, T4, T12 | integration | Exact `P ... B -> T ... R -> C ... H` first-parent chain. |
| AC-BFA-004 | T3, T15 | integration | Rollback and bundle identities. |
| AC-BFA-005 | T5 | integration | Post-T drift reports paths. |
| AC-BFA-006 | T10, T11 | smoke | T includes every strict/full-gate input. |
| AC-BFA-007 | T11, T12, MP1 | integration, manual, smoke | Strict H, publication readiness H, and detached T pass after local tag. |
| AC-BFA-008 | T8 | integration | Failure matrix changes neither ref. |
| AC-BFA-009 | T7, MP1 | integration, manual | Authorized atomic mapping is exact. |
| AC-BFA-010 | T13, MP2 | smoke, manual | Existing public release gates remain composed. |
| AC-BFA-011 | T11, T14 | integration, manual | Recovery changes at the publication boundary. |
| AC-BFA-012 | T15 | migration | Exact rollback and mixed-bundle rejection. |
| AC-BFA-013 | T6 | integration | Determinism, bounds, side effects, and privacy. |
| AC-BFA-014 | T1-T16 | contract | This proof map covers every BFA requirement. |
| AC-BFA-015 | T5, T8 | integration | Replacement history has one new transition and rereview. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | T1-T3 | Candidate succeeds on exact absent-tag P/B/T/R state. |
| E2 | T1, T3 | Ordinary validation stays strict. |
| E3 | T11, T12, MP1 | Local tag enables strict H, readiness H, and detached T proof. |
| E4 | T5, T12 | Immediate R-to-C evidence and lifecycle-only H are allowed without weakening T. |
| E5 | T8 | Base drift changes neither ref. |
| E6 | T8, T9 | Missing atomic capability has no fallback. |
| E7 | T5, T8 | Post-T payload drift requires replacement history. |
| E8 | T14, MP2 | Partial public publication stays open and fixes forward. |

## Proof map

Boundary model version: boundary-first-v1

Boundary model scope: BFA-R001, BFA-R002, BFA-R003, BFA-R004, BFA-R005, BFA-R006, BFA-R007, BFA-R008, BFA-R009, BFA-R010, BFA-R011, BFA-R012, BFA-R013, BFA-R014, BFA-R015, BFA-R016, BFA-R017, BFA-R018, BFA-R019, BFA-R020, BFA-R021, BFA-R022, BFA-R023, BFA-R024, BFA-R025, BFA-R026, BFA-R027, BFA-R028, BFA-R029, BFA-R030, BFA-R031, BFA-R032, BFA-R033, BFA-R034, BFA-R035

| Proof obligation ID | Coverage state | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Proof level | Automation mode | Command IDs | Evidence artifact | Required milestone | Manual procedure IDs | Uncovered gap ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRF-001 | covered | BFA-R004, BFA-R006, BFA-R007, BFA-R031 | BND-INPUT-001 | T1 | integration | automated | CMD1 | `evidence/implementation-m1.md` | M1 | - | - |
| PRF-002 | covered | BFA-R005, BFA-R006, BFA-R013, BFA-R017, BFA-R024 | BND-STATE-001 | T1, T12, T14 | integration | hybrid | CMD1, CMD13, CMD14, CMD18, CMD19 | `evidence/implementation-m1.md`; `evidence/boundary-activation-candidate.json`; `evidence/release-checkpoint.md`; `docs/releases/v0.4.0/npm-publication.md` | public closeout | MP1, MP2 | - |
| PRF-003 | covered | BFA-R008, BFA-R009, BFA-R010, BFA-R012, BFA-R014, BFA-R017, BFA-R018, BFA-R019, BFA-R020, BFA-R021 | BND-AUTH-001 | T2, T4, T7, T11, T12 | integration | hybrid | CMD1, CMD5, CMD13-CMD15, CMD17 | `evidence/implementation-m1.md`; `evidence/implementation-m2.md`; `evidence/boundary-activation-candidate.json`; `evidence/release-checkpoint.md`; `evidence/atomic-publication.json` | release checkpoint | MP1 | - |
| PRF-004 | covered | BFA-R005, BFA-R014, BFA-R018, BFA-R019, BFA-R025, BFA-R026, BFA-R033 | BND-COMPOSE-001 | T3, T10, T11, T13, T16 | end-to-end | hybrid | CMD4, CMD8, CMD11, CMD12, CMD14, CMD16-CMD20, CMD25 | `evidence/implementation-m1.md`; `evidence/implementation-m2.md`; `evidence/implementation-m3.md`; `evidence/release-checkpoint.md`; `evidence/atomic-publication.json`; `docs/releases/v0.4.0.md`; `docs/releases/v0.4.0/npm-publication.md` | public closeout | MP1, MP2 | - |
| PRF-005 | covered | BFA-R015, BFA-R016, BFA-R021, BFA-R022, BFA-R023, BFA-R035 | BND-TEMPORAL-001 | T5, T8, T12 | integration | automated | CMD1, CMD5 | `evidence/implementation-m1.md`; `evidence/implementation-m2.md` | M2 | - | - |
| PRF-006 | covered | BFA-R022, BFA-R023, BFA-R027, BFA-R028, BFA-R030, BFA-R035 | BND-RECOVERY-001 | T5, T8, T11, T14 | integration | hybrid | CMD5, CMD14-CMD19 | `evidence/implementation-m2.md`; `evidence/release-checkpoint.md`; `evidence/atomic-publication.json`; `docs/releases/v0.4.0/npm-publication.md` | public closeout | MP1, MP2 | - |
| PRF-007 | covered | BFA-R002, BFA-R003, BFA-R005, BFA-R029 | BND-COMPAT-001 | T3, T10, T15 | integration | automated | CMD1, CMD12 | `evidence/implementation-m3.md` | M3 | - | - |
| PRF-008 | covered | BFA-R007, BFA-R020, BFA-R022, BFA-R025, BFA-R030 | BND-ENV-001 | T1, T8, T13, T14 | end-to-end | hybrid | CMD1, CMD5, CMD17-CMD20, CMD25 | `evidence/atomic-publication.json`; `docs/releases/v0.4.0.md`; `docs/releases/v0.4.0/npm-publication.md` | public closeout | MP1, MP2 | - |
| PRF-009 | covered | BFA-R005, BFA-R007, BFA-R013 | INT-001 | T1, T3 | integration | automated | CMD1 | `evidence/implementation-m1.md` | M1 | - | - |
| PRF-010 | covered | BFA-R008, BFA-R009, BFA-R010, BFA-R012, BFA-R014, BFA-R015, BFA-R016, BFA-R017, BFA-R019, BFA-R020 | INT-002 | T2, T5, T11, T12 | integration | hybrid | CMD1, CMD13-CMD17 | `evidence/boundary-activation-candidate.json`; `evidence/release-checkpoint.md`; `evidence/atomic-publication.json` | release checkpoint | MP1 | - |
| PRF-011 | covered | BFA-R020, BFA-R021, BFA-R022 | INT-003 | T7, T8 | integration | automated | CMD5 | `evidence/implementation-m2.md` | M2 | - | - |
| PRF-012 | covered | BFA-R018, BFA-R019, BFA-R025, BFA-R033 | INT-004 | T11, T12, T13, T16 | end-to-end | hybrid | CMD4, CMD8, CMD11, CMD12, CMD14-CMD20, CMD25 | `evidence/implementation-m1.md`; `evidence/implementation-m2.md`; `evidence/implementation-m3.md`; `evidence/release-checkpoint.md`; `evidence/atomic-publication.json`; `docs/releases/v0.4.0.md`; `docs/releases/v0.4.0/npm-publication.md` | public closeout | MP1, MP2 | - |
| PRF-013 | covered | BFA-R027, BFA-R028, BFA-R030 | INT-005 | T11, T14 | integration | hybrid | CMD17, CMD18, CMD19 | `evidence/atomic-publication.json`; `docs/releases/v0.4.0/npm-publication.md` | public closeout | MP1, MP2 | - |
| PRF-014 | covered | BFA-R002, BFA-R029 | INT-006 | T15 | integration | automated | CMD12 | `evidence/implementation-m3.md` | M3 | - | - |
| PRF-015 | covered | BFA-R016, BFA-R023, BFA-R035 | INT-007 | T5, T8 | integration | automated | CMD1, CMD5 | `evidence/implementation-m2.md` | M2 | - | - |

Evidence paths without a leading directory are relative to
`docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7/`.

## Edge case coverage

| Edge case | Covered by | Notes |
| --- | --- | --- |
| EC1 candidate flag without check | T1 | Parser fails before Git or filesystem mutation. |
| EC2 other or malformed release | T1 | Closed release vocabulary rejects it. |
| EC3 one namespace already has tag | T1 | Diagnostic names local or remote conflict. |
| EC4 remote lookup unavailable | T1 | Candidate blocks instead of assuming absence. |
| EC5 zero or multiple transitions | T4 | Topology fails closed. |
| EC6 T only on non-first-parent path | T4 | First-parent proof fails. |
| EC7 lifecycle receipt follows T | T5 | Owning lifecycle evidence is accepted. |
| EC7A candidate evidence is self-naming, copied, modified, non-immediate, or off first-parent | T12 | Provenance fails before readiness. |
| EC8 release-gated review fix follows T | T5, T8 | Candidate is replaced and rereviewed. |
| EC9 remote main changes after proof | T8 | Both refs remain unchanged. |
| EC10 remote rejects atomic push | T8, T9 | No sequential fallback. |
| EC11 strict H passes but detached T fails | T11, MP1 | Local tag is removed; publication never starts. |
| EC11A stored provenance, live H, fresh identities, tag authority, or remote base fails readiness | T7, T8, T12 | Publication stops before remote mutation. |
| EC12 Git refs publish but npm fails | T14, MP2 | Immutable refs remain; closeout stays open. |

## Validation commands

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMD1 | `python scripts/test-boundary-first-validation.py` | existing/configured | implement | M1, M4 | code-review M1 | Block candidate, strict, topology, drift, rollback, or diagnostic regression. | Zero tests is failure. | Owning milestone implementation evidence. | Temporary local Git fixtures only. |
| CMD2 | `python scripts/validate-boundary-first.py --check` | existing/configured | implement | M1 | code-review M1 | Block strict-default regression or invalid repository state. | Not applicable; deterministic check. | `evidence/implementation-m1.md` | Read-only local check. |
| CMD3 | `python -m py_compile scripts/validate-boundary-first.py scripts/boundary_first_validation.py` | existing/configured | implement | M1 | code-review M1 | Block syntax/import handoff. | Not applicable; compile check. | `evidence/implementation-m1.md` | Writes only normal Python cache output; no network. |
| CMD4 | `python scripts/select-validation.py --mode explicit --path scripts/validate-boundary-first.py --path scripts/boundary_first_validation.py --path scripts/test-boundary-first-validation.py --path scripts/fixtures/boundary-first/activation --path scripts/validation_selection.py --path scripts/test-select-validation.py` | existing/configured | implement | M1 | code-review M1 | Block unclassified paths, registration debt, or missing owned checks across the complete M1 validator and selector surface. | Not applicable; deterministic selector. | `evidence/implementation-m1.md` | Read-only selection; executes no checks. |
| CMD5 | `python scripts/test-boundary-activation-release.py` | planned-for-implementation | implement | M2 | code-review M2 | Block atomic publication or recovery handoff. | Zero tests is failure. | `evidence/implementation-m2.md` | Local bare remotes only; no configured external remote. |
| CMD6 | `python scripts/test-select-validation.py` | existing/configured | implement | M2 | code-review M2 | Block validation routing for new publication paths. | Zero tests is failure. | `evidence/implementation-m2.md` | Local fixtures only. |
| CMD7 | `python -m py_compile scripts/boundary_activation_release.py scripts/publish-boundary-activation.py` | planned-for-implementation | implement | M2 | code-review M2 | Block syntax/import handoff. | Not applicable; compile check. | `evidence/implementation-m2.md` | Local compile only; no remote mutation. |
| CMD8 | `python scripts/select-validation.py --mode explicit --path scripts/boundary_activation_release.py --path scripts/publish-boundary-activation.py --path scripts/test-boundary-activation-release.py --path scripts/validation_selection.py --path scripts/test-select-validation.py` | existing/configured | implement | M2 | code-review M2 | Block unclassified paths, registration debt, or missing owned checks. | Not applicable; deterministic selector. | `evidence/implementation-m2.md` | Read-only selection; executes no checks. |
| CMD9 | `python scripts/prepare-release.py v0.4.0 --check` | existing/configured | implement | M3 | code-review M3 | Block stale or incomplete generated release payload. | Not applicable; generation check. | `evidence/implementation-m3.md` | Check mode writes no tracked output. |
| CMD10 | `python scripts/release-preflight.py v0.4.0` | existing/configured | implement | M3 | code-review M3 | Block profile, version, tag, remote, evidence, or changed-literal inconsistency. | Not applicable; deterministic preflight. | `evidence/implementation-m3.md` | Reads remote tag state but does not mutate it. |
| CMD11 | `python scripts/select-validation.py --mode release --release-version v0.4.0` | existing/configured | implement | M3, M4 | code-review M3 | Block missing release checks or selector debt. | Not applicable; deterministic selector. | Owning milestone implementation evidence. | Read-only selection; no publication. |
| CMD12 | `bash scripts/ci.sh --mode release --release-version v0.4.0` | existing/configured | implement | M3, M4 | code-review M3 | Block release-selected or broad-smoke failure. | Zero selected tests is failure. | Owning milestone implementation evidence. | Repository validation only; no publication. |
| CMD13 | `python scripts/validate-boundary-first.py --check --activation-candidate v0.4.0` | planned-for-implementation | implement | M1 | code-review M4 | Block absent-tag candidate or P/B/T/R proof. | Not applicable; deterministic check. | `evidence/boundary-activation-candidate.json` | Read-only; remote advertisement only. |
| CMD14 | `python scripts/publish-boundary-activation.py --check --release v0.4.0 --candidate-evidence docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7/evidence/boundary-activation-candidate.json` | planned-for-implementation | implement | M2 | release checkpoint | Block stale R/C provenance, live-H ancestry, local/remote tag, P/B/T, rollback, bundle, T..H drift, ref, or capability mismatch. | Not applicable; deterministic preflight. | `evidence/release-checkpoint.md` | Check mode derives exact H but must not mutate refs. |
| CMD15 | `python scripts/validate-boundary-first.py --check` | release-owned | release operator | release checkpoint | release checkpoint | Stop and remove local tag before publication. | Not applicable; deterministic strict check. | `evidence/release-checkpoint.md` | Runs at H with local v0.4.0 at T; no remote mutation. |
| CMD16 | `bash scripts/release-verify.sh v0.4.0` | release-owned | release operator | release checkpoint | release checkpoint | Stop, clean detached worktree, and remove local tag before publication. | Zero tests or skipped required gate is failure. | `evidence/release-checkpoint.md` | Runs only in detached worktree at T. |
| CMD17 | `python scripts/publish-boundary-activation.py --publish --release v0.4.0 --candidate-evidence docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7/evidence/boundary-activation-candidate.json` | external-owned | release operator | release checkpoint | explicit release action | Rerun readiness in-process, retain exact full H through refspec construction, and stop on any guard or push failure for exact reconciliation. | Not applicable; publication command. | `evidence/atomic-publication.json` | Authorized external mutation; one non-forced atomic push only. |
| CMD18 | `python scripts/close-release-publication.py v0.4.0` | release-owned | release operator | public closeout | explicit release action | Keep closeout open with exact unavailable or failed phase. | Not applicable; evidence generator. | `docs/releases/v0.4.0/npm-publication.md` | Reads public GitHub/npm/npx; writes closeout evidence, not publication. |
| CMD19 | `python scripts/validate-release.py --version v0.4.0` | release-owned | release operator | public closeout | explicit release action | Keep release open until published evidence is valid. | Not applicable; deterministic validation. | `docs/releases/v0.4.0.md` | Read-only release validation. |
| CMD20 | `bash scripts/release-verify.sh "$GITHUB_REF_NAME"` | ci-owned | GitHub tag workflow | public publication | tag workflow | Block GitHub release and npm publication. | Zero tests or skipped required gate is failure. | GitHub Actions run and release evidence. | CI tag context; trusted publication starts only after pass. |
| CMD21 | `python scripts/validate-change-metadata.py docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7/change.yaml` | existing/configured | test-spec | lifecycle | test-spec authoring | Block illegal artifact or workflow metadata. | Not applicable; deterministic validator. | Change metadata validation entry. | Read-only metadata validation. |
| CMD22 | `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/boundary-first-v1-v0-3-7-activation-release.test.md --path docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7/change.yaml --path docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7/evidence/test-spec-authoring.md` | existing/configured | test-spec | lifecycle | test-spec authoring | Block incomplete authoring evidence or illegal lifecycle state. | Not applicable; deterministic validator. | Change metadata validation entry. | Read-only explicit-path validation. |
| CMD23 | `python scripts/validate-review-artifacts.py docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7` | existing/configured | test-spec-review | lifecycle | test-spec-review | Block malformed, unindexed, or unresolved review evidence. | Not applicable; deterministic validator. | Review log and review receipt. | Read-only review validation. |
| CMD24 | `python scripts/validate-boundary-first.py --path specs/boundary-first-v1-v0-3-7-activation-release.test.md` | existing/configured | test-spec | lifecycle | test-spec authoring | Block malformed, missing, or untraceable boundary proof obligations. | Not applicable; deterministic validator. | Test-spec authoring evidence. | Read-only proof-map validation. |
| CMD25 | `python scripts/test-release-transaction.py` | existing/configured | implement | M3 | code-review M3 | Block tag-workflow ordering, release-gate delegation, closeout, or partial-publication regression. | Zero tests is failure. | `evidence/implementation-m3.md` | Local fixtures and provider stubs only; no publication. |

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Preimplementation gate | T1-T16 | none | CMD21-CMD24 | This test spec, authoring evidence, and test-spec-review receipt | implementation handoff | Every requirement, boundary, interaction, example, edge case, and command must remain mapped. |
| M1 | T1-T6, T12, T16 | none | CMD1-CMD4 | `evidence/implementation-m1.md` | code-review M1 | Candidate implementation and missing-evidence readiness matrix are fixture-proved; real candidate command is deferred until T exists. |
| M2 | T7-T9, T12 | none | CMD5-CMD8 | `evidence/implementation-m2.md` | code-review M2 | Bare remotes prove both-ref success/all-or-neither failure, R/C/H readiness, and privacy-safe fixture serializers. |
| M3 | T3, T10, T13, T15, T16 | none | CMD9-CMD12, CMD25 | `evidence/implementation-m3.md` | code-review M3 | Complete pending payload, tag-workflow composition, public-closeout fixtures, and rollback proof settle before B. |
| M4 | T2, T4-T6, T12 | none | CMD1, CMD11-CMD13 | `evidence/implementation-m4.md`; `evidence/boundary-activation-candidate.json` | code-review M4 | T changes only the activation record; candidate runs at R; immediate child C persists its result; later H adds lifecycle evidence only. |
| Release checkpoint | T11-T12 | MP1 | CMD14-CMD17 | Release-checkpoint and atomic publication evidence | atomic Git publication | Tag, strict H, detached T, preflight, then atomic publish. |
| Public closeout | T13-T15 | MP2 | CMD18-CMD20 | `docs/releases/v0.4.0.md`; `docs/releases/v0.4.0/npm-publication.md` | final release closeout | Existing tag workflow and rerunnable public closeout own external proof. |

## Test cases

### T1. Candidate command, state, tag, and remote input matrix

- Covers: BFA-R004-R007, BFA-R013, BFA-R031, E1, E2, EC1-EC4, INT-001
- Level: integration
- Command IDs: CMD1
- Fixture/setup: Temporary repositories with pending/active manifests, exact/invalid releases, local/remote tag variants, and reachable/unreachable bare remotes.
- Steps: Invoke exact, absent, malformed, conflicting, and unreachable candidate forms; invoke default validation on the same active tag-absent tree.
- Expected result: Only exact active v0.4.0 with both tags absent proceeds; every other partition fails before mutation, and default mode remains strict.
- Failure proves: Candidate authority escaped its explicit input or state boundary.
- Evidence artifact: `evidence/implementation-m1.md`
- Automation location: `scripts/test-boundary-first-validation.py`
- Required by milestone: M1

### T2. P/B/T/R identity and stable candidate result

- Covers: BFA-R008-R010, BFA-R012-R013, BFA-R031, E1, AC-BFA-003
- Level: integration
- Command IDs: CMD1, CMD13
- Fixture/setup: First-parent histories with exact P/B/T/R identities and lifecycle-only commits after T.
- Steps: Run candidate validation repeatedly and parse the machine result.
- Expected result: Full identities and required fields, including exact `candidate_validation_head: R`, are stable; no `reviewed_head` field appears; tag state is absent and no public activation claim appears.
- Failure proves: Identity authority or result serialization is ambiguous or conflated.
- Evidence artifact: `evidence/boundary-activation-candidate.json`
- Automation location: `scripts/test-boundary-first-validation.py`; `scripts/validate-boundary-first.py`
- Required by milestone: M1 fixture proof; M4 real-candidate proof

### T3. Strict invariant, bundle, release, and rollback compatibility

- Covers: BFA-R001-R003, BFA-R005-R006, BFA-R011, BFA-R029, E2, INT-006
- Level: integration
- Command IDs: CMD1, CMD12
- Fixture/setup: Exact and mismatched resource, projection, skill, package, release, and rollback matrices.
- Steps: Compare candidate and default modes across exact, mixed, older, missing, and substituted identities.
- Expected result: Candidate skips only absent-tag authority; strict sibling invariants remain exact and mixed rollback fails closed.
- Failure proves: Candidate mode weakened compatibility or bundle authority.
- Evidence artifact: `evidence/implementation-m1.md`; `evidence/implementation-m3.md`
- Automation location: `scripts/test-boundary-first-validation.py`; release-selected checks
- Required by milestone: M1 and M3

### T4. Transition uniqueness and first-parent topology

- Covers: BFA-R009-R010, EC5, EC6
- Level: integration
- Command IDs: CMD1
- Fixture/setup: Histories with zero, one, or two transitions and merge-only reachability.
- Steps: Run candidate validation on each topology.
- Expected result: Only one B-to-T transition on R's first-parent chain passes.
- Failure proves: Transition identity can be absent, ambiguous, or hidden behind a merge parent.
- Evidence artifact: `evidence/implementation-m1.md`
- Automation location: `scripts/test-boundary-first-validation.py`
- Required by milestone: M1

### T5. Post-T lifecycle classifier and replacement history

- Covers: BFA-R014-R016, BFA-R023, BFA-R035, E4, E7, EC7, EC8, INT-002, INT-007
- Level: integration
- Command IDs: CMD1, CMD5
- Fixture/setup: Candidate histories through R and readiness histories through H, one release-gated path per class, multiple rejected paths, and replacement histories from fresh P.
- Steps: Validate accepted and drifted `T..R` in candidate mode; validate accepted and drifted `T..H` in readiness; exercise appended repair, second transition, and clean replacement branch.
- Expected result: Lifecycle evidence passes in both phases; every release-gated path is listed; invalid history never becomes reusable; replacement has exactly one new transition.
- Failure proves: Tagged payload can drift or invalid transition history can be retained.
- Evidence artifact: `evidence/implementation-m1.md`; `evidence/implementation-m2.md`
- Automation location: `scripts/test-boundary-first-validation.py`; `scripts/test-boundary-activation-release.py`
- Required by milestone: M1 and M2

### T6. Determinism, side effects, bounded diagnostics, and privacy

- Covers: BFA-R031-R034, AC-BFA-013
- Level: integration
- Command IDs: CMD1
- Fixture/setup: Snapshot Git refs/files plus injected token, OTP, username, hostname, private environment value, and temporary path sentinels.
- Steps: Repeat success/failure runs, compare outputs and repository state, and scan diagnostics for sentinels and unbounded values.
- Expected result: Results are deterministic; refs/files do not change; output is bounded and contains no private sentinel.
- Failure proves: Candidate validation mutates state, leaks data, or produces unstable evidence.
- Evidence artifact: `evidence/implementation-m1.md`
- Automation location: `scripts/test-boundary-first-validation.py`
- Required by milestone: M1

### T7. Authorized atomic publication succeeds

- Covers: BFA-R020-R021, AC-BFA-009, INT-003
- Level: integration
- Command IDs: CMD5
- Fixture/setup: Atomic-capable local bare remote with main at P, absent remote v0.4.0, local v0.4.0 at T, exact `R -> C ... H`, and valid candidate evidence produced at R.
- Steps: Run publish mode; instrument readiness return and push argv; move symbolic local HEAD after readiness in one partition without changing the captured full SHA.
- Expected result: Publish mode reruns readiness, retains its exact full H SHA, and uses that literal SHA in one non-forced atomic push advancing main P-to-H and creating v0.4.0 at T; it never re-resolves symbolic HEAD.
- Failure proves: The authorized two-ref mapping cannot complete atomically.
- Evidence artifact: `evidence/implementation-m2.md`
- Automation location: `scripts/test-boundary-activation-release.py`
- Required by milestone: M2

### T8. Atomic publication failure and regeneration matrix

- Covers: BFA-R021-R023, BFA-R027, BFA-R035, E5-E7, EC8-EC10, INT-003, INT-007
- Level: integration
- Command IDs: CMD5
- Fixture/setup: Bare remotes and histories for stale P, existing remote tag, non-fast-forward H, local-head movement before readiness, evidence drift, absent atomic capability, and one-ref rejection.
- Steps: Attempt publication, re-read both refs, inspect command argv, and exercise replacement-candidate recovery.
- Expected result: Every failure changes neither ref, uses no force/sequential fallback, and requires fresh P plus full validation/rereview.
- Failure proves: Stale authority or partial Git publication can escape the guard.
- Evidence artifact: `evidence/implementation-m2.md`
- Automation location: `scripts/test-boundary-activation-release.py`
- Required by milestone: M2

### T9. Publication interface and explicit-action boundary

- Covers: BFA-R023-R024, BFA-R027-R028
- Level: contract
- Command IDs: CMD5, CMD14, CMD17
- Fixture/setup: CLI invocations with neither, both, check, and publish modes plus source inspection of allowed push argv.
- Steps: Exercise parsing and check mode; assert mutation is reachable only through explicit publish and argv contains one plain `--atomic` push.
- Expected result: Ambiguous modes fail, check is read-only, publish is explicit, and no force, overwrite, or sequential fallback exists.
- Failure proves: Routine lifecycle continuation can mutate external refs or fallback unsafely.
- Evidence artifact: `evidence/implementation-m2.md`
- Automation location: `scripts/test-boundary-activation-release.py`
- Required by milestone: M2

### T10. Complete pending v0.4.0 payload and package parity

- Covers: BFA-R001-R003, BFA-R014, BFA-R026, BFA-R029, BFA-R034, AC-BFA-004, AC-BFA-006, AC-BFA-010, AC-BFA-012
- Level: end-to-end
- Command IDs: CMD9-CMD12
- Fixture/setup: Prepared v0.4.0 profile and generated release surfaces while activation remains pending.
- Steps: Run preparation check, preflight, release selection, and release CI; inspect three-target archives/packages and v0.3.6 rollback identities.
- Expected result: Every release-gated input is present before T, generated output is current, all targets match, and rollback is exact.
- Failure proves: T would depend on later payload or contain an incoherent release bundle.
- Evidence artifact: `evidence/implementation-m3.md`
- Automation location: Existing release, adapter, package, and smoke checks selected by release mode
- Required by milestone: M3

### T11. Local tag, strict H, readiness H, detached T, and failed-before-publish cleanup

- Covers: BFA-R014, BFA-R018-R019, BFA-R027, E3, EC11, INT-004, INT-005
- Level: manual
- Command IDs: CMD14-CMD16
- Fixture/setup: Reviewed H containing valid R-to-C evidence, local tag v0.4.0 at T, absent remote tag, remote main P, and detached temporary worktree at T.
- Steps: Follow MP1; additionally inject strict-H, readiness-H, and detached-T failures in automated shell harness tests.
- Expected result: All three gates pass before publication; preview-phase failure removes local tag/worktree and never invokes publish; publish-invocation failure preserves local evidence for reconciliation; detached proof reads only T.
- Failure proves: Candidate proof substituted for strict/tagged proof or cleanup crossed the external boundary.
- Evidence artifact: `evidence/release-checkpoint.md`; `evidence/atomic-publication.json`
- Automation location: MP1 plus `scripts/test-boundary-activation-release.py`
- Required by milestone: release checkpoint

### T12. Lifecycle evidence and publication readiness gate

- Covers: BFA-R015-R018, BFA-R020, BFA-R024, BFA-R031, BFA-R034, EC7A, EC11A, AC-BFA-003, BND-STATE-001, BND-AUTH-001
- Level: contract
- Command IDs: CMD1, CMD5, CMD13, CMD14
- Fixture/setup: Change records missing each required artifact/evidence class; exact `T ... R -> C ... H`; malformed variants where evidence is missing, duplicated, self-naming, copied from another R, modified after C, introduced by a non-immediate child, reachable only through a merge parent, or excluded from live H; and token, OTP, username, hostname, private-environment, temporary-path, malicious persisted-evidence, and remote-diagnostic sentinels.
- Steps: In M1, run the missing-evidence and provenance fixture matrix; at M4 run CMD13 at actual R and commit its exact JSON in immediate child C; through CMD5 inject every privacy sentinel into stored evidence, runtime identity/environment, readiness failures, drift paths, and remote diagnostics; at the release checkpoint run CMD14 at live H after local tag creation; inject fresh P/B/T, rollback, bundle, local/remote tag, remote-main, and T..H mismatches; inspect stdout, stderr, checkpoint serialization, and atomic-publication serialization.
- Expected result: Only exact producer result plus immediate first-parent R-to-C provenance and C-in-H containment passes; every stale or forged variant and fresh-authority mismatch blocks; candidate evidence names R rather than C or H; diagnostics and both evidence serializers contain no raw sentinel or machine-local path; no external action autoprogresses.
- Failure proves: Publication can precede required lifecycle evidence or explicit authority.
- Evidence artifact: `evidence/implementation-m1.md`; `evidence/implementation-m2.md`; `evidence/boundary-activation-candidate.json`; `evidence/release-checkpoint.md`
- Automation location: `scripts/test-boundary-first-validation.py`; `scripts/test-boundary-activation-release.py`; candidate validator; publication preflight
- Required by milestone: M1 missing-evidence fixtures, M2 readiness/privacy fixtures, M4 actual-state proof, and release checkpoint

### T13. Tag workflow and public package composition

- Covers: BFA-R001, BFA-R025-R026, BFA-R034, AC-BFA-010
- Level: smoke
- Command IDs: CMD20, CMD25
- Fixture/setup: v0.4.0 tag workflow plus repository release/profile fixtures.
- Steps: In M3, run CMD25 to prove static workflow ordering, release-gate delegation, and closeout fixtures; in MP2, observe actual CMD20 and public evidence.
- Expected result: Any omitted or failing sibling gate blocks publication.
- Failure proves: Candidate or helper validation bypassed the standing public release path.
- Evidence artifact: `evidence/implementation-m3.md`; exact GitHub Actions run URL/ID in `docs/releases/v0.4.0.md`; `docs/releases/v0.4.0/npm-publication.md`
- Automation location: Release workflow regression tests and MP2 observation
- Required by milestone: M3 fixture proof; public publication actual proof

### T14. Partial publication and rerunnable closeout

- Covers: BFA-R028, BFA-R030, E8, EC12, INT-005
- Level: integration
- Command IDs: CMD18, CMD19
- Fixture/setup: Public-evidence providers with GitHub-only, npm-only, delayed, failed-smoke, and complete states.
- Steps: Run closeout and validation repeatedly across partial then complete evidence.
- Expected result: Partial states stay open with exact phase; published refs are never rewritten; later complete evidence closes idempotently.
- Failure proves: Partial publication can be reported as success or recovered destructively.
- Evidence artifact: `docs/releases/v0.4.0/npm-publication.md`
- Automation location: `scripts/test-release-transaction.py`; MP2 actual closeout
- Required by milestone: M3 fixtures; public closeout actual proof

### T15. Exact v0.3.6 runtime rollback

- Covers: BFA-R002, BFA-R029, INT-006, AC-BFA-012
- Level: migration
- Command IDs: CMD1, CMD12
- Fixture/setup: Exact v0.3.6 archives/packages and mixed, older, overwritten, or incomplete variants.
- Steps: Select rollback through the standing validator and compare all adapter/package identities.
- Expected result: Only one coherent immutable v0.3.6 bundle passes; v0.4.0 remains untouched.
- Failure proves: Recovery can construct a mixed or mutable rollback.
- Evidence artifact: `evidence/implementation-m3.md`
- Automation location: Boundary-first, adapter-distribution, and release-selected tests
- Required by milestone: M3

### T16. Candidate composition retains sibling validation

- Covers: BFA-R011, BFA-R033, BND-COMPOSE-001, INT-004
- Level: integration
- Command IDs: CMD4, CMD8, CMD11, CMD12
- Fixture/setup: Changed sets spanning validator, lifecycle, skill, adapter, package, release, and security paths.
- Steps: Select validation for each set and inject one failing sibling check at a time.
- Expected result: Candidate mode changes only tag authority; every path-owned check remains selected and blocking.
- Failure proves: Candidate success can bypass a sibling proof owner.
- Evidence artifact: Owning milestone implementation evidence
- Automation location: `scripts/test-select-validation.py`; release selection fixtures
- Required by milestone: M1-M3

## Fixtures and data

- Extend `scripts/fixtures/boundary-first/activation/` with exact candidate,
  invalid-input, P/B/T/R topology, immediate R-to-C evidence, C-in-H ancestry,
  post-T path, and privacy-sentinel cases.
- M2 creates temporary non-network bare remotes and isolated hook directories;
  fixtures never reference the configured public remote.
- M3 uses the canonical v0.4.0 profile and repository-owned generated surfaces.
- Public closeout tests use existing fixture-provider mode; fixture evidence is
  never accepted as routine public proof.

## Mocking/stubbing policy

Mock only external Git transport capability, GitHub/npm responses, public npx,
and deliberate command failures.
Do not mock Git history, ref identity, filesystem side effects, path
classification, release profile parsing, package/archive identities, or the
actual `git push --atomic` behavior used by local bare-remote integration tests.

## Migration or compatibility tests

T3, T10, and T15 preserve strict pending/active behavior, historical fixtures,
the exact ten-skill contract, immediate v0.3.6 rollback, and coherent adapter
packages.
No generalized future missing-tag mode is accepted.

## Observability verification

T1, T2, T5, T6, T8, T12, and T14 assert stable mode, release, P/B/T/R/C/H, tag/path,
expected invariant, corrective action, failed phase, and bounded public state.
Evidence must not claim a broader state than the command directly proved.

## Security/privacy verification

T6 injects sensitive sentinels and rejects their appearance in normal output or
committed evidence.
T12 injects the same classes through readiness and M2 checkpoint/atomic
serializers; MP1 scans the actual authorized checkpoint and atomic evidence.
T9 rejects force, overwrite, and sequential publication paths.
T13 preserves trusted publishing and existing security gates.

## Performance checks

CMD1 records focused-suite duration and T6 repeats candidate validation to catch
unbounded work.
No new hard timing threshold is introduced; existing release timing evidence
remains authoritative.

## Manual QA checklist

### MP1. Explicit activation tag and atomic Git publication

- Owner role: authorized release operator.
- Owning stage: explicit release checkpoint after PR approval and merge authorization.
- Automation rationale: local fixture automation proves mechanics, but only the authorized remote can prove current P, atomic capability, authenticated two-ref publication, and receive-side acceptance.
- Required environment: clean reviewed H containing exact immediate-child R-to-C candidate evidence; Git and Python; configured authorized `origin`; local and remote v0.4.0 absent before the procedure; release credentials available but never printed or recorded.
- Exact procedure: execute verbatim the failure-safe Bash block under `Lifecycle closeout. Review, rationale, verification, PR, and explicit release` in `docs/plans/2026-08-05-activate-boundary-first-v1-v0-4-0.md`. That block creates local v0.4.0 at `transition_commit`, runs CMD15 at H, runs CMD16 from a detached T worktree, runs CMD14, then and only then runs CMD17.
- Evidence artifacts: `docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7/evidence/release-checkpoint.md` records R/C/H/T, strict, readiness, and detached commands, exit results, and advertised P/tag state; `docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7/evidence/atomic-publication.json` records P, readiness-bound H, T, push mode, and resulting advertised refs.
- Pass condition: CMD15, CMD16, and CMD14 pass; CMD17 independently reruns readiness and uses its returned exact full H; one non-forced atomic push maps main P-to-H and absent remote v0.4.0-to-T; fresh advertised refs equal H and T; scan actual checkpoint and atomic evidence for credential, token, OTP, private-environment, username, hostname, and machine-local-path disclosure and find none.
- Failure condition: any pre-publish gate fails, push capability/guard/ref acceptance fails, resulting refs are uncertain or mismatched, or evidence is incomplete/private; public closeout must not start.
- Cleanup and recovery: before publication starts, the plan trap removes the temporary worktree and local tag and remote refs remain unchanged. After CMD17 starts, preserve the local tag and evidence, re-query both remote refs, record the exact state, and follow standing immutable recovery without retrying from stale evidence.
- Forbidden actions: force push, force-with-lease, tag overwrite/deletion, sequential branch/tag pushes, manual ref repair, credential capture, or continuing after a failed/uncertain gate.

### MP2. Public publication and closeout

- Owner role: authorized release operator.
- Owning stage: public publication and closeout after MP1 proves exact remote refs.
- Automation rationale: CI and closeout automate validation, but public GitHub/npm availability, trusted-publishing outcome, registry propagation, and live npx installation must be observed against the real public services.
- Required environment: MP1 atomic evidence; authenticated read access for `gh`; public network; Node/npm/npx; three fresh empty temporary projects; no npm publish token is read by these verification commands.
- Exact commands, in order:
  1. `gh run list --workflow release.yml --branch v0.4.0 --limit 5 --json databaseId,status,conclusion,headSha,event,url`
  2. `gh release view v0.4.0 --json tagName,targetCommitish,isDraft,isPrerelease,url,assets`
  3. `npm view @xiongxianfei/rigorloop@0.4.0 version dist-tags.latest dist.integrity --json`
  4. `npx @xiongxianfei/rigorloop@0.4.0 version`
  5. From a fresh empty Codex project: `npx @xiongxianfei/rigorloop@0.4.0 init codex`
  6. From a fresh empty Claude project: `npx @xiongxianfei/rigorloop@0.4.0 init claude`
  7. From a fresh empty opencode project: `npx @xiongxianfei/rigorloop@0.4.0 init opencode`
  8. CMD18: `python scripts/close-release-publication.py v0.4.0`
  9. CMD19: `python scripts/validate-release.py --version v0.4.0`
- Evidence artifacts: the exact workflow run URL/ID and release proof in `docs/releases/v0.4.0.md`; generated provider, integrity, version, and three-target smoke proof in `docs/releases/v0.4.0/npm-publication.md`.
- Pass condition: tag workflow conclusion is success at T and ran CMD20 before publication; release assets/checksums match profile metadata; npm version is 0.4.0, latest is 0.4.0, integrity is present; version and all three fresh init commands pass; CMD18 and CMD19 close exact public evidence.
- Failure condition: workflow or any public query/smoke fails, evidence is delayed/ambiguous, assets or identities mismatch, latest differs, integrity is absent, or CMD18/CMD19 remains open.
- Cleanup and recovery: remove only the three disposable smoke projects. Preserve immutable Git/npm artifacts, record failed-during-publish or failed-after-publish, and rerun closeout after propagation or use standing fix-forward, dist-tag correction, deprecation, or patch-release recovery.
- Forbidden actions: deleting/rewriting v0.4.0, republishing 0.4.0, treating fixture evidence as public proof, exposing credentials/environment dumps, or marking release closed while any public check is open.

## What not to test and why

- Do not test force-push, overwrite, or sequential publication as valid paths;
  assert they are absent or rejected.
- Do not test arbitrary future candidate releases; the public contract is
  intentionally v0.4.0-only.
- Do not duplicate every existing adapter, package, security, and release test;
  prove their composition through release selection and targeted gate-removal
  regressions.
- Do not publish to real GitHub or npm during implementation tests.

## Uncovered gaps

None.

## Next artifacts

- Test-spec review.
- M1-M4 implementation and independent milestone code reviews.
- Release-owned MP1 and MP2 only after verify, PR review, merge authorization,
  and the explicit external-action checkpoint.

## Follow-on artifacts

None yet

## Readiness

Ready for `test-spec-review` after authoring evidence and lifecycle validation
are recorded. Implementation is not yet authorized.
