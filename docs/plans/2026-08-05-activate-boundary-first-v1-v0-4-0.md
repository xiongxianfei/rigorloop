<!-- Template: plan-skeleton-v3 -->
<!-- Skill: plan -->
<!-- Template status: normative -->

# Activate Boundary-First v1 in v0.4.0

## Purpose / big picture

Deliver the already-implemented `boundary-first-v1` guidance as active public
behavior in stable `v0.4.0` while preserving strict tag proof, tagged-tree
reproducibility, and immutable `v0.3.6` rollback.

Implementation adds one read-only pre-tag candidate mode and one guarded atomic
publication helper, then prepares the complete v0.4.0 transition tree. External
tag creation, remote ref mutation, GitHub release creation, and npm publication
remain outside automatic execution.

## Current Handoff Summary

- Owning change record: `docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7/change.yaml`

Mutable lifecycle state, current milestone state, review status, blockers,
routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: `docs/proposals/2026-08-05-activate-boundary-first-v1-v0-3-7.md`
- Spec: `specs/boundary-first-v1-v0-3-7-activation-release.md`
- Architecture: `docs/architecture/system/architecture.md`
- ADR: `docs/adr/ADR-20260805-boundary-first-activation-candidate-and-atomic-publication.md`
- Test spec: pending `test-spec` after plan-review

## Context and orientation

`scripts/validate-boundary-first.py` is the CLI and
`scripts/boundary_first_validation.py` owns activation history, manifest,
resource, projection, grandfathering, and rollback proof. Focused regressions
live in `scripts/test-boundary-first-validation.py`.

`scripts/release_transaction.py`, `scripts/release-preflight.py`,
`scripts/validate-release.py`, and `scripts/release-verify.sh` own routine
release preparation and proof. Release state remains profile-driven under
`docs/releases/profiles/<tag>.yaml`; the activation manifest remains
`specs/boundary-first-activation.yaml`.

The implementation branch may contain preparation commits between remote main
`P` and grandfathering baseline `B`. The unique transition `T` changes pending
to active and contains every release-gated input. Later `T..H` commits may add
only lifecycle evidence owned by this change. Any later payload correction
supersedes the branch and PR and restarts from current authorized remote main.

## Non-goals

- Do not add another manifest, profile schema, activation state, service, dependency, or persistent remote-state cache.
- Do not generalize candidate mode beyond exact release `v0.4.0`.
- Do not weaken default strict activation validation or the full release gate.
- Do not use force push, sequential branch/tag publication, tag overwrite, or history rewrite.
- Do not publish, tag, push, merge, create a GitHub release, or publish npm during implementation milestones.

## Requirements covered

| Requirements | Owning milestone |
| --- | --- |
| BFA-R004-R013, BFA-R031-R034 | M1 |
| BFA-R014-R019 | M1, M3 |
| BFA-R020-R023, BFA-R035 | M2 |
| BFA-R001-R003, BFA-R024-R030 | M3 and lifecycle closeout |
| AC-BFA-001-006, AC-BFA-013 | M1 |
| AC-BFA-008-009, AC-BFA-015 | M2 |
| AC-BFA-007, AC-BFA-010-012, AC-BFA-014 | M3 and lifecycle closeout |

### Boundary and interaction ownership

| Boundary / interaction | Milestone | Rollback unit | Proof timing |
| --- | --- | --- | --- |
| BND-INPUT-001, BND-STATE-001, INT-001 | M1 | candidate-validator commit | focused tests before M1 review |
| BND-AUTH-001, BND-COMPOSE-001, INT-002, INT-004 | M1, M3 | validator commit; transition candidate | focused tests in M1; tagged-tree proof in M3 |
| BND-TEMPORAL-001, BND-RECOVERY-001, INT-003, INT-005, INT-007 | M2 | atomic publisher commit | local bare-remote integration tests before M2 review |
| BND-COMPAT-001, INT-006 | M3 | complete v0.4.0 transition candidate | rollback/archive proof before M3 review |
| BND-ENV-001 | M1-M3 | owning milestone commit | unreachable remote, atomic capability, and public-boundary proof at owning stage |

## Milestones

### Preimplementation gate. Test-proof alignment

- Gate kind: upstream lifecycle gate, not an implementation milestone.
- Owner: `test-spec`, followed by `test-spec-review`.
- Exit: every BFA requirement, boundary, interaction, acceptance criterion, and edge case maps to an executable test or explicit release-owned proof.
- Failure: route behavioral gaps to spec and design gaps to architecture; implementation does not repair upstream contracts.

### M1. Read-only activation candidate validation

- Milestone state: planned
- Goal: Add the exact opt-in candidate command and deterministic `P/B/T/H` proof without changing strict default behavior.
- Requirements: BFA-R004-R019, BFA-R031-R034.
- Files/components likely touched:
  - `scripts/validate-boundary-first.py`
  - `scripts/boundary_first_validation.py`
  - `scripts/test-boundary-first-validation.py`
  - `scripts/fixtures/boundary-first/activation/`
- Dependencies:
  - approved plan and test spec
  - reachable configured remote for real candidate success; local bare remotes for tests
- Tests to add/update:
  - exact flag and release vocabulary, absent/present/unreachable tag, unique transition, and strict-default preservation
  - exact `P ... B -> T ... H`, stable JSON fields, rollback/bundle identity, and side-effect absence
  - accepted lifecycle-only `T..H` paths and exact rejected release-gated path output
- Implementation steps:
  - extend CLI parsing with `--activation-candidate` valid only with `--check`
  - derive fresh `P`, transition parent `B`, transition `T`, and head `H`
  - share strict invariant helpers while skipping only logically absent-tag proof
  - classify `T..H` paths and emit non-public candidate status
- Validation commands:
  - `python scripts/test-boundary-first-validation.py`
  - `python scripts/validate-boundary-first.py --check`
  - `python -m py_compile scripts/validate-boundary-first.py scripts/boundary_first_validation.py`
- Expected observable result: candidate mode proves exact pre-tag state; ordinary mode remains strict.
- Commit message: `M1: add boundary activation candidate validation`
- Milestone closeout: focused validation, implementation evidence, commit, and independent code review.
- Risks: helper reuse could accidentally weaken strict mode.
- Rollback/recovery: revert the M1 commit; pending strict behavior remains the baseline.

### M2. Guarded atomic activation publication helper

- Milestone state: planned
- Goal: Implement and test exact all-or-neither publication without force or sequential fallback.
- Requirements: BFA-R020-R024, BFA-R027-R028, BFA-R031-R035.
- Files/components likely touched:
  - `scripts/boundary_activation_release.py`
  - `scripts/publish-boundary-activation.py`
  - `scripts/test-boundary-activation-release.py`
  - `scripts/validation_selection.py` and focused selector tests when the new evidence/commands need routing
- Dependencies:
  - M1 stable candidate result contract
  - Git atomic push and pre-push hook protocol
- Tests to add/update:
  - exact advertised `main == P` and absent-tag guard
  - fast-forward proof, successful atomic branch/tag update, stale P, existing tag, non-fast-forward, unsupported atomic capability, and one-ref rejection
  - no force option, no sequential fallback, no mutation in check/preflight mode
  - invalid post-T payload requires replacement history with one transition
- Implementation steps:
  - parse and revalidate candidate evidence
  - create an isolated temporary pre-push guard for same-push advertised identities
  - execute one plain `git push --atomic` only after all local gates pass
  - keep actual remote mutation behind an explicit release-only command boundary
- Validation commands:
  - `python scripts/test-boundary-activation-release.py`
  - `python scripts/test-select-validation.py`
  - `python -m py_compile scripts/boundary_activation_release.py scripts/publish-boundary-activation.py`
- Expected observable result: local integration fixtures update both refs or neither; normal implementation runs perform no external push.
- Commit message: `M2: add guarded atomic activation publication`
- Milestone closeout: focused validation, implementation evidence, commit, and independent code review.
- Risks: hook or remote capability assumptions could permit stale authority or partial mutation.
- Rollback/recovery: revert M2; no external ref was authorized or changed.

### M3. Build and prove the v0.4.0 transition candidate

- Milestone state: planned
- Goal: Generate the complete release payload, make the single pending-to-active transition, and prove tagged-tree and package parity without publishing.
- Requirements: BFA-R001-R003, BFA-R014-R019, BFA-R025-R030; AC-BFA-004, AC-BFA-006-007, AC-BFA-010-014.
- Files/components likely touched:
  - `docs/releases/profiles/v0.4.0.yaml` and generated v0.4.0 release surfaces
  - `packages/rigorloop/package.json` and profile-owned version projections
  - `specs/boundary-first-activation.yaml` and activation projection/spec fixtures
  - adapter artifact, token-cost, packed-smoke, and candidate-verification evidence required by existing release tooling
- Dependencies:
  - M1 and M2 closed
  - clean approved test proof and current release generators
- Tests to add/update:
  - exact v0.4.0/v0.3.6 release identities and one pending-to-active transition
  - self-contained strict validation and full release verification from `T`
  - three-target generated, archive, packed, and clean-install parity
  - post-T lifecycle-only acceptance and release-gated drift rejection
- Implementation steps:
  - create the routine profile and run repository-owned release preparation
  - complete all release-gated code, metadata, notes, package, fixture, and generated-surface changes before activation
  - update the activation record once, with `B` as its exact first parent, producing `T`
  - generate derived proof outside tracked rollback state and record candidate evidence
  - after `T`, change only lifecycle evidence; replace the branch if payload correction is required
- Validation commands:
  - `python scripts/prepare-release.py v0.4.0 --check`
  - `python scripts/release-preflight.py v0.4.0`
  - `python scripts/validate-boundary-first.py --check --activation-candidate v0.4.0`
  - `bash scripts/release-verify.sh v0.4.0`
  - exact selected CI commands named by the test spec
- Expected observable result: reviewed candidate evidence proves `P/B/T/H`, exact packages, tagged-tree self-containment, and pending external publication.
- Commit message: `M3: prepare boundary-first v0.4.0 activation candidate`
- Milestone closeout: candidate validation, derived proof, implementation evidence, commit, and independent code review; payload findings trigger replacement rather than an appended fix.
- Risks: late release-payload findings invalidate `T` and require a new candidate branch.
- Rollback/recovery: before publication abandon the candidate and regenerate from current authorized remote main; after publication use immutable v0.3.6 and standing fix-forward rules.

### Lifecycle closeout. Review, rationale, verification, PR, and explicit release

- Final holistic code review runs after all implementation milestones close.
- `explain-change` and `verify` require fresh actual-run evidence and coherent lifecycle state.
- `pr` prepares and opens the review handoff only after verify passes.
- Local tag creation, atomic remote main/tag publication, GitHub/npm publication, and public closeout require the explicit external release action and are not authorized by this plan.

## Validation plan

- Run each milestone's focused unit/integration tests before broader selection.
- Run `python scripts/select-validation.py --mode explicit --path ...` for the actual changed set and resolve registration debt.
- Run `bash scripts/ci.sh --mode explicit --path ...` for the selected set before milestone closeout.
- M3 runs repository-owned preflight, candidate validation, release verification, adapter/package smoke, and the test-spec commands.
- Final verify reruns correctness-, lifecycle-, generated-output-, security-, and release-sensitive checks with actual-run evidence.

## Risks and recovery

- Risk: candidate mode becomes an alternate activation authority.
  - Recovery: keep output explicitly non-public and preserve strict default/tag gates.
- Risk: P changes or atomic push is unsupported.
  - Recovery: change neither ref; regenerate and rereview from current authorized remote main.
- Risk: payload changes after T.
  - Recovery: supersede branch/PR; never append a second transition or force-push.
- Risk: public publication partially succeeds after Git refs publish.
  - Recovery: preserve immutable refs and use existing failed-release, closeout, dist-tag, deprecation, and patch fix-forward rules.

## Dependencies

- Git remote must advertise exact refs and support atomic push for publication; absence blocks release, not implementation.
- Existing trusted publishing, adapter archive, package smoke, token-cost, and public closeout contracts remain unchanged.
- `v0.3.6` remains publicly available as the exact rollback release.
- Test-spec review must approve proof ownership before M1 begins.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-05 | Use three implementation milestones: candidate proof, atomic publisher, and transition candidate. | Each is independently testable and reversible before the immutable transition, while M3 isolates release payload and replacement risk. | One broad release milestone; per-file micro-milestones. |
| 2026-08-05 | Record candidate output as workflow evidence instead of adding a manifest. | Existing profile, activation manifest, and change-local evidence already own state and proof. | New candidate manifest or profile schema. |
| 2026-08-05 | Keep external release operations in lifecycle closeout. | Tag, push, GitHub release, and npm publication require explicit authority. | Automatic publication during M3. |

## Readiness

- Ready for plan-review after lifecycle registration and validation.
- Readiness is not Done; test-spec, implementation reviews, final review, rationale, verify, PR, and explicit release remain.
