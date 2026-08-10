<!-- Template: plan-skeleton-v3 -->
<!-- Skill: plan -->
<!-- Template status: normative -->

# Published-Skill-First Repository Simplification

## Purpose / big picture

Replace repository acceptance built around many selected checks with three deterministic product gates and one bounded lifecycle-governance entry point.
The work preserves canonical skill integrity, all-target package parity, release safety, fail-closed lifecycle values, and negative fixtures while removing target-runtime certification and retiring orchestration only after old-versus-replacement proof.

Implementation is split so every retirement has a contract disposition, a dual-proof checkpoint, and a recoverable rollback boundary.
No milestone may start Codex, Claude Code, or opencode or use prompts, transcripts, model selection, or LLM-output grading as acceptance evidence.

## Current Handoff Summary

- Owning change record: `docs/changes/2026-08-10-published-skill-first-repository-simplification/change.yaml`

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: `docs/proposals/2026-08-10-published-skill-first-repository-simplification.md`
- Proposal review: `docs/changes/2026-08-10-published-skill-first-repository-simplification/reviews/proposal-review-r2.md`
- Spec: `specs/published-skill-first-repository-simplification.md`
- Spec review: `docs/changes/2026-08-10-published-skill-first-repository-simplification/reviews/spec-review-r1.md`
- Architecture: `docs/architecture/system/architecture.md`
- ADR: `docs/adr/ADR-20260810-published-skill-first-validation-architecture.md`
- Architecture review: `docs/changes/2026-08-10-published-skill-first-repository-simplification/reviews/architecture-review-r2.md`
- Test spec: pending `test-spec` after plan-review

## Context and orientation

Canonical skill source lives under `skills/`.
`scripts/skill_validation.py`, `scripts/validate-skills.py`, `scripts/build-skills.py`, `scripts/adapter_distribution.py`, `scripts/build-adapters.py`, and `scripts/validate-adapters.py` are the likely existing owners for Gate A and Gate B.
`scripts/validate-release.py` and `scripts/release-verify.sh` are the likely Gate C composition boundary.

Lifecycle validation is currently split across `scripts/validate-artifact-lifecycle.py`, `scripts/validate-change-metadata.py`, `scripts/validate-review-artifacts.py`, and their implementation modules.
The target has one maintainer-facing governance entry point while retaining focused internal modules when they have distinct deterministic data ownership.

Check selection and execution currently run through `scripts/validation_selection.py`, `scripts/select-validation.py`, `scripts/ci.sh`, validation-cache helpers, broad-smoke classification, and a large selector regression suite.
Dynamic Codex behavior and token evidence use `scripts/run-token-cost-benchmarks.py`, `scripts/analyze-codex-jsonl.py`, benchmark fixtures, and release-report validation.
Documentation prose and readability checks include deterministic formatting facts and semantic heuristics that must be separated before retirement.

The 2026-07-28 project map accurately describes the current machinery but predates the approved target architecture.
Use it only for current path orientation; the approved spec, ADR, canonical architecture, and direct source inspection govern target behavior.

## Non-goals

- Do not redesign or retire the public workflow automation capability.
- Do not delete a check because of line count alone.
- Do not weaken adapter support, archive safety, release metadata, lifecycle review recording, or unknown-value regression proof.
- Do not create new standalone validator CLIs, selector systems, validation caches, or schedulers.
- Do not hand-edit generated public adapter package output.
- Do not publish, release, tag, push, merge, or access credentials.
- Do not embed mutable milestone or routing state in this plan or `docs/plan.md`.

## Requirements covered

| Requirements | Owning milestone or evidence |
| --- | --- |
| R14-R20, R22, R24-R27, R29 | M1 inventory, admission freeze, exact contract disposition, and retirement ledger |
| R1-R3, R11, R15, R16 | M2 Gate A and review-owned semantic quality |
| R4, R5, R9, R10, R27, R28 | M3 Gate B and installer-materialization classification |
| R7, R8, R22, R24 | M4 Gate C and deterministic release boundary |
| R12, R13 | M5 single lifecycle-governance entry point |
| R6, R15-R25 | M6 direct CI composition and proof-backed subsystem retirement |

### Boundary and interaction ownership

| Boundary or interaction | Milestone | Affected surfaces | Rollback unit | Timed proof obligation |
| --- | --- | --- | --- | --- |
| BND-INPUT-001 | M1-M5 | check inventory, canonical skills, packages, releases, lifecycle records | Each milestone's inventory and owner slice | Before any removal, classify valid, invalid, missing, unknown, and undeclared inputs and preserve every contractual negative fixture. |
| BND-STATE-001 | M1, M6 | retirement ledger and per-slice state | One retirement slice | Prove inventoried -> dual-proof -> removable -> retired and pause paths before the first deletion in each slice. |
| BND-AUTH-001, INT-003 | M1-M5 | Gate A/B/C, governance, semantic review | One owner-boundary slice | Before review, prove each invariant has exactly one deterministic owner and semantic concerns have no validator oracle. |
| BND-COMPOSE-001, INT-002 | M2-M6 | Gate chain, CI, release wrapper, governance sibling | Gate owner plus thin composition change | Gate C and CI must expose underlying owner failures and must not copy canonical or package rules. |
| BND-TEMPORAL-001 | M1-M6 | old-only, dual-run, replacement-only, rollback | Most recent retirement commit | Record old and replacement command results before removal; mismatch pauses and rollback restores the slice. |
| BND-RECOVERY-001 | M1-M6 | diagnostics, partial migration, rollback | Per-milestone revert or re-enable path | Unknown failures, incomplete contract disposition, or failed dual proof stop without deleting the old path. |
| BND-COMPAT-001, INT-004 | M1, M3, M4, M6 | active specs, historical evidence, adapter support | Clause-disposition and invocation slice | Exact active-clause disposition precedes implementation removal; historical evidence remains untouched. |
| BND-ENV-001, INT-005 | M3, M4, M6 | local packages, temporary directories, target runtimes, network | Installer/release acceptance slice | Prove package and filesystem behavior locally and assert that acceptance invokes no target runtime, prompt, transcript, model matrix, or nondeterministic retry. |
| INT-001 | M3 | declared adapter transformations and retired checks | Gate B transform contract slice | An undeclared transform must fail Gate B before its former check can retire. |

## Milestones

### Preimplementation gate. Boundary-first proof map

- Gate kind: upstream lifecycle gate, not an implementation milestone.
- Owner: `test-spec`, followed by `test-spec-review`.
- Exit: every requirement, boundary, interaction, acceptance criterion, edge case, milestone, and command has direct automated proof or explicit review-owned evidence.
- Failure: normative gaps route to `spec`; design or placement gaps route to `architecture`; implementation does not repair upstream contracts.

### M1. Freeze script admission and classify every existing proof path

- Milestone type: implementation.
- Goal: Produce the complete retirement ledger and exact contract-disposition map before changing acceptance or deleting code.
- Requirements: R14-R20, R22, R24-R27, R29; BND-INPUT-001; BND-STATE-001; BND-AUTH-001; BND-TEMPORAL-001; BND-RECOVERY-001; BND-COMPAT-001; INT-004.
- Files/components likely touched:
  - `docs/changes/2026-08-10-published-skill-first-repository-simplification/retirement-ledger.json`
  - `specs/skill-contract.md` and matching test spec for the already-approved R26 disposition
  - selector, cache, scheduler, broad-smoke, token-cost, prose, lifecycle, adapter, and release specs only for exact cross-spec disposition already determined by the approved primary spec
  - `docs/workflows.md` and contributor guidance for the script-admission rule
- Dependencies:
  - approved plan and approved test spec
  - complete check catalog, script inventory, fixture inventory, and CI/release invocation inventory
- Tests to add/update:
  - ledger schema accepts complete retained, replaced, optional-analysis, de-contracted, and blocked dispositions
  - missing failure owner, invocation boundary, repair, retirement evidence, active-clause disposition, or rollback fails closed
  - unknown fixture behavior and contradictory clause disposition block retirement
  - R26 clauses no longer impose prompt, transcript, semantic behavior-parity, or all-target clean-install proof
- Implementation steps:
  - capture script, check-ID, direct command, CI, release, spec, and fixture ownership before edits
  - assign each deterministic failure to Gate A, Gate B, Gate C, governance, or explicit de-contracting; assign semantic concerns to review
  - record exact active requirement and acceptance-clause dispositions without rewriting historical evidence
  - stop and route any newly discovered normative decision to `spec` rather than deciding it in code
  - add the admission rule to the existing contributor/governance surface without creating a validator for prose quality
- Validation commands:
  - `python scripts/validate-change-metadata.py docs/changes/2026-08-10-published-skill-first-repository-simplification/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-08-10-published-skill-first-repository-simplification/retirement-ledger.json --path specs/skill-contract.md --path docs/workflows.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-select-validation.py`
- Expected observable result: every existing proof path has one protected-failure and contract disposition, and no deletion is eligible while any entry is unknown or contradictory.
- Commit message: `M1: classify validation ownership and retirement`
- Milestone closeout: targeted validation and implementation evidence, followed by independent code review and required resolution.
- Risks:
  - classification may expose a new normative decision not settled by the primary spec
  - mechanical cross-spec edits could accidentally rewrite historical obligations
- Rollback/recovery:
  - revert M1 as one documentation and ledger slice; no acceptance command or script is removed

### M2. Consolidate Gate A and make semantic quality review-owned

- Milestone type: implementation.
- Goal: Expose one deterministic canonical-skill integrity command and remove required semantic prose or routing evaluation from acceptance.
- Requirements: R1-R3, R11, R15, R16, R24, R26, R27, R29; BND-INPUT-001; BND-AUTH-001; BND-COMPOSE-001; BND-RECOVERY-001; INT-003.
- Files/components likely touched:
  - `scripts/skill_validation.py`, `scripts/validate-skills.py`, `scripts/test-skill-validator.py`
  - deterministic fixtures under `tests/fixtures/skills/`
  - `skills/code-review/SKILL.md` or the existing published-skill review owner for the concise semantic checklist
  - `scripts/validate-documentation-prose.py`, `scripts/validate-markdown-readability.py`, routing fixtures, and their tests only according to M1 dispositions
- Dependencies:
  - M1 closes with exact deterministic versus semantic ownership
- Tests to add/update:
  - every R2 integrity failure, including unknown closed values and unsafe resource paths
  - structurally valid but semantically unclear prose is not failed by Gate A
  - no prompt fixture, transcript, model selection, or broad semantic score is required
  - semantic review checklist covers trigger clarity, ownership, prerequisites, procedure, resources, stops, claims, output, and handoff
- Implementation steps:
  - add failing deterministic Gate A fixtures before consolidation
  - converge parsing and diagnostics on the existing skill-validation owner
  - retain formatting checks only when they express an exact deterministic contract
  - remove or de-route semantic prose, routing coverage, and transcript acceptance paths classified by M1
  - preserve target-independent canonical checks and generated-resource prerequisites for Gate B
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/validate-boundary-first.py --check`
- Expected observable result: one Gate A command reports only deterministic canonical-skill failures, while semantic skill quality is handled by formal review.
- Commit message: `M2: consolidate canonical skill integrity gate`
- Milestone closeout: targeted validation, review-checklist evidence, independent code review, and required resolution.
- Risks:
  - removing a prose check may also remove a deterministic placeholder or forbidden-claim invariant
  - a review checklist may drift into repository-maintainer details shipped to users
- Rollback/recovery:
  - restore the retired check invocation and fixture subset; keep the Gate A consolidation only if dual proof remains complete

### M3. Consolidate Gate B and classify installer materialization

- Milestone type: implementation.
- Goal: Prove equivalent deterministic package parity for Codex, Claude Code, and opencode and retain only installer logic not covered by package copying.
- Requirements: R4, R5, R9, R10, R27, R28; BND-INPUT-001; BND-AUTH-001; BND-COMPOSE-001; BND-ENV-001; INT-001; INT-005.
- Files/components likely touched:
  - `scripts/adapter_distribution.py`, `scripts/build-adapters.py`, `scripts/validate-adapters.py`, `scripts/test-adapter-distribution.py`
  - `dist/adapters/manifest.yaml`, adapter templates, and release-output fixtures
  - CLI installer/materializer implementation and tests under `packages/rigorloop/`
- Dependencies:
  - Gate A is stable and M1 classifies every adapter/install check
- Tests to add/update:
  - all-target skill and file inventory, mapped paths, untransformed bytes, archives, and declared transformations
  - one target cannot pass from another target's proof
  - undeclared transform, stale byte, missing file, extra file, malformed archive, and unsafe path fail
  - installer inventory proves pure copy or names each additional materialization branch
  - any retained materialization smoke uses a local package, empty temporary directory, filesystem assertions, and no target runtime or prompt
- Implementation steps:
  - extend existing adapter fixtures rather than add another adapter validator CLI
  - normalize equivalent all-target proof and target-specific declared transformations
  - inventory installer behavior against package-copy coverage
  - remove mandatory clean installs when package parity is sufficient; retain focused filesystem tests only for additional logic
  - dual-run existing adapter/install proof against Gate B fixtures before removal
- Validation commands:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version <test-version> --output-dir <temporary-output>`
  - `python scripts/validate-adapters.py --version <test-version> --adapter-root <temporary-output>`
  - the existing packed CLI installer test command identified by M1
- Expected observable result: all three target archives receive equivalent deterministic proof, and installer testing ends at the smallest RigorLoop-owned filesystem boundary.
- Commit message: `M3: consolidate all-target adapter parity gate`
- Milestone closeout: generated-package evidence, installer classification, independent code review, and required resolution.
- Risks:
  - equivalence could erase a legitimate opencode multi-root transformation
  - a pure-copy classification could overlook lockfile or state mutation
- Rollback/recovery:
  - restore the affected target's former validation or install fixture while retaining other independently proved target slices

### M4. Compose Gate C and remove target-runtime release acceptance

- Milestone type: implementation.
- Goal: Make release verification compose current Gate A and Gate B proof with release-only deterministic checks.
- Requirements: R6-R8, R22, R24, R26, R28, R29; BND-COMPOSE-001; BND-TEMPORAL-001; BND-RECOVERY-001; BND-COMPAT-001; BND-ENV-001; INT-002; INT-005.
- Files/components likely touched:
  - `scripts/validate-release.py`, `scripts/release-verify.sh`, `scripts/release-preflight.py`
  - release profiles and release-validation tests
  - `scripts/run-token-cost-benchmarks.py`, `scripts/analyze-codex-jsonl.py`, token-cost reports and fixtures according to M1 contract disposition
- Dependencies:
  - Gate A and Gate B commands and failure identities are stable
  - M1 resolves deterministic static token budgets separately from target-runtime benchmark behavior
- Tests to add/update:
  - Gate C rejects stale or missing A/B proof and exposes underlying owner failures
  - version, metadata, archive inventory, checksums, tracked release notes, package freshness, and rollback consistency
  - release acceptance invokes no target runtime, prompt, transcript analyzer, model matrix, or nondeterministic retry
  - deterministic static token or package-size checks remain only when an active release contract assigns them a concrete failure
- Implementation steps:
  - add Gate C composition regressions before changing the release wrapper
  - call existing Gate A and Gate B owners or shared modules rather than duplicate their rules
  - remove dynamic Codex behavior and transcript evidence from release readiness according to M1 disposition
  - preserve preflight, archive, checksum, version, notes, emergency failure visibility, and non-publishing local verification
  - dual-run old and replacement release proof on a local candidate; publish nothing
- Validation commands:
  - `python scripts/validate-release.py --recorded-source-auto --version <fixture-version>`
  - `python scripts/test-release-transaction.py`
  - `python scripts/test-adapter-distribution.py`
  - `bash scripts/release-verify.sh <fixture-version>` against a local fixture only
- Expected observable result: one local release command proves deterministic publication readiness without executing or grading an agent runtime.
- Commit message: `M4: compose deterministic release integrity gate`
- Milestone closeout: local non-publishing release evidence, independent code review, and required resolution.
- Risks:
  - removing dynamic benchmarks could also remove a deterministic report-shape or package-size contract
  - release composition could accidentally cache stale Gate A or B results
- Rollback/recovery:
  - restore the prior release invocation list while keeping the candidate local and unpublished

### M5. Consolidate lifecycle governance behind one entry point

- Milestone type: implementation.
- Goal: Present one deterministic lifecycle-governance result while preserving focused internal parsers and all fail-closed state and review invariants.
- Requirements: R12, R13, R15, R16; BND-INPUT-001; BND-AUTH-001; BND-COMPOSE-001; BND-RECOVERY-001.
- Files/components likely touched:
  - `scripts/validate-artifact-lifecycle.py` and internal lifecycle modules
  - `scripts/validate-change-metadata.py`, `scripts/change_metadata_semantics.py`
  - `scripts/validate-review-artifacts.py`, `scripts/review_artifact_validation.py`
  - lifecycle, metadata, and review fixture suites
- Dependencies:
  - M1 identifies every public invocation and shared or distinct invariant
- Tests to add/update:
  - one entry point covers shape, transitions, review and resolution references, dangling evidence, contradictory state, and closed vocabularies
  - every closed set has an `unknown_value` or `not_in_vocabulary` regression that fails before consistency logic
  - focused internal modules remain independently testable without acting as competing public owners
  - diagnostic names field, unknown value, allowed values, and repair surface
- Implementation steps:
  - write missing unknown-value and composition fixtures first
  - select `validate-artifact-lifecycle.py` as the maintainer-facing composition entry point unless M1 proves a smaller existing owner
  - compose existing change-metadata and review parsers without merging unrelated data models
  - remove duplicated public invocation routes only after old-versus-composed results match
  - retain exact focused commands only as internal/debug surfaces when their admission record justifies them
- Validation commands:
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path <fixture-paths>`
- Expected observable result: contributors and CI receive one governance result, and unknown lifecycle values cannot pass through any internal path.
- Commit message: `M5: consolidate lifecycle governance validation`
- Milestone closeout: focused regression evidence, composed-command parity, independent code review, and required resolution.
- Risks:
  - one wrapper could hide distinct parser failures or become an oversized implementation
  - closing duplicate routes could break change-local review tooling
- Rollback/recovery:
  - restore focused public invocations while keeping new unknown-value regressions and internal owner separation

### M6. Cut CI to stable gates and retire proved orchestration

- Milestone type: implementation.
- Goal: Make routine and release CI call Gate A, Gate B, Gate C, and governance directly, then remove only orchestration entries proved unnecessary by M1-M5.
- Requirements: R6, R14-R25; BND-STATE-001; BND-AUTH-001; BND-COMPOSE-001; BND-TEMPORAL-001; BND-RECOVERY-001; BND-COMPAT-001; BND-ENV-001; INT-002; INT-003; INT-004; INT-005.
- Files/components likely touched:
  - `.github/workflows/ci.yml`, `.github/workflows/release.yml`, `scripts/ci.sh`
  - `scripts/validation_selection.py`, `scripts/select-validation.py`, selector tests
  - `scripts/validation_cache.py`, broad-smoke classification and scheduler support, and their tests
  - obsolete validator orchestration meta-tests and documentation
  - `docs/project-map.md`, canonical architecture, and contributor command guidance after the target is current
- Dependencies:
  - M1-M5 gates are independently reviewed and dual proof has no unexplained difference
  - every retired selector, cache, scheduler, or meta-test contract has exact approved disposition
- Tests to add/update:
  - routine skill changes invoke Gate A and affected Gate B proof directly
  - release paths invoke Gate C, which composes A and B
  - lifecycle changes invoke the governance entry point
  - no target runtime or semantic validator appears in acceptance command graphs
  - deleted routing, cache, scheduler, and meta-test paths are absent and unreferenced
  - representative old failures still fail through their retained owner
- Implementation steps:
  - add direct CI command-graph fixtures before removing selector routes
  - switch thin workflows and the minimal wrapper to stable gates
  - run old and new command graphs on representative changes and record timing and coverage differences
  - remove only ledger entries marked removable; leave any exception or unknown path active and report incomplete simplification
  - update current-state project map, architecture transition notes, and contributor commands to match the implemented boundary
  - run final holistic code review after all milestone-local reviews; final verification remains downstream
- Validation commands:
  - Gate A, Gate B, Gate C, and governance commands from M2-M5
  - `python scripts/test-select-validation.py` while selector compatibility remains
  - `bash scripts/ci.sh --mode explicit --path skills/workflow/SKILL.md`
  - `bash scripts/ci.sh --mode pr`
  - `git diff --check`
- Expected observable result: CI has a small transparent deterministic command graph, retired machinery has no active references, and all protected failures remain observable through named owners.
- Commit message: `M6: cut CI to published-skill product gates`
- Milestone closeout: full direct-gate evidence, final holistic code review after milestone review, and no claim of verify or PR readiness.
- Risks:
  - broad deletion could remove a release-only or governance-only invocation
  - direct gates may increase routine runtime if target scoping is lost
  - active contract disposition may prove one subsystem cannot retire in this initiative
- Rollback/recovery:
  - restore the last removed orchestration slice and its direct invocation; do not roll back earlier independently passing product gates

## Validation plan

| Proof layer | Command or evidence | Purpose |
| --- | --- | --- |
| Change-local lifecycle | `python scripts/validate-change-metadata.py docs/changes/2026-08-10-published-skill-first-repository-simplification/change.yaml` | Reject illegal artifact, planned-work, automation, or review state. |
| Review closeout | `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-08-10-published-skill-first-repository-simplification` | Prove formal review findings and dispositions are closed. |
| Gate A | `python scripts/validate-skills.py` plus focused regressions | Prove deterministic canonical skill and resource integrity. |
| Gate B | existing adapter build and validation commands against temporary output | Prove all-target package parity and declared transformations. |
| Gate C | `bash scripts/release-verify.sh <local-fixture-version>` or the fixture-safe equivalent named by the test spec | Prove composed deterministic release integrity without publication. |
| Governance | `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path ...` | Prove lifecycle shape, transition, evidence, review, and closed-vocabulary consistency. |
| Retirement | `retirement-ledger.json` plus old-versus-replacement command results | Prove no protected failure is silently lost. |
| Final direct graph | PR-mode CI plus explicit representative skill, adapter, release, and lifecycle paths | Prove thin CI calls only stable owners and retains affected-path coverage. |
| Formatting | `git diff --check` | Reject whitespace defects. |

No validation row may use target-agent execution, prompts, transcripts, model selection, or LLM-output grading as pass evidence.

## Risks and recovery

- Risk: the inventory reveals active requirements not settled by the approved spec.
  - Recovery: stop the affected retirement slice and route the exact normative decision to `spec`; continue only independent non-conflicting milestones.
- Risk: a consolidated gate becomes another monolithic validator.
  - Recovery: keep one public owner while preserving focused internal modules and one parser owner per invariant.
- Risk: old and replacement results disagree.
  - Recovery: classify the difference before removal; restore the old path if the replacement missed a contractual failure.
- Risk: dynamic runtime evidence is intertwined with deterministic release metadata.
  - Recovery: preserve deterministic report or package fields in Gate C and retire only prompt execution, transcript analysis, and model-derived pass status.
- Risk: the selector or cache still provides measured value at current scale.
  - Recovery: retain it only through the approved exception path with named scale evidence, owner, invocation boundary, and retirement condition.
- Risk: M6 cannot retire every candidate safely.
  - Recovery: report partial simplification, keep unresolved paths active, and create bounded follow-on changes rather than weakening proof.

## Dependencies

- Accepted proposal, approved feature spec, approved canonical architecture, and accepted ADR.
- Plan-review approval before the matching boundary-first test specification.
- Test-spec and test-spec-review approval before implementation.
- Local package fixtures that do not publish or require credentials.
- Exact current contracts for skill validation, adapter packaging, release verification, lifecycle governance, selector routing, cache behavior, broad smoke, and token-cost evidence.
- Independent code review and required review-resolution after every implementation milestone.
- Final holistic code review, explain-change, and verify after all six implementation milestones close.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-10 | Inventory and contract disposition precede all deletions. | Unknown protected failures and same-rank spec conflicts must stop retirement rather than pass silently. | Delete-first cleanup; infer ownership from script names. |
| 2026-08-10 | Build Gates A, B, and C from existing commands and modules. | The approved admission budget is zero new standalone validator CLIs. | New gate executable package; another validation framework. |
| 2026-08-10 | Keep one governance entry point with focused internal modules. | One maintainer-facing owner simplifies use without forcing unrelated data models into one parser. | Preserve all public validators; merge all parser code into one file. |
| 2026-08-10 | Retire runtime behavior evidence from acceptance, not from historical records. | Repository correctness is deterministic while historical evidence remains valid context. | Delete historical transcripts and reports; keep Codex-only certification. |
| 2026-08-10 | Make CI cutover the last implementation milestone. | Direct gates need reviewed replacement proof before selectors, caches, schedulers, or meta-tests can safely disappear. | Cut CI first; big-bang reset. |

## Readiness

- The plan is ready for `plan-review`.
- Readiness is not Done.
- Remaining completion gates: plan-review, test-spec, test-spec-review, six implementation/code-review loops with review-resolution when triggered, final holistic code review, explain-change, verify, and PR handoff.
