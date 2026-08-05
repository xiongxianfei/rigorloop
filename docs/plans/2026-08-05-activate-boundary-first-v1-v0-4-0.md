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
| BFA-R014-R019 | M1, M3, M4, explicit release checkpoint |
| BFA-R020-R023, BFA-R035 | M2 |
| BFA-R001-R003, BFA-R024-R030 | M3, M4, explicit release checkpoint, and public closeout |
| AC-BFA-001-006, AC-BFA-013 | M1 |
| AC-BFA-008-009, AC-BFA-015 | M2 |
| AC-BFA-007, AC-BFA-010-012, AC-BFA-014 | M3, M4, explicit release checkpoint, and public closeout |

### Boundary and interaction ownership

| Proof phase and owner | Boundaries / interactions | Rollback unit | Required proof |
| --- | --- | --- | --- |
| M1 candidate-validator implementation | BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001; INT-001, INT-002 | M1 commit | focused tests prove exact inputs, P/B/T/H derivation, lifecycle-only path classification, strict-default preservation, determinism, and no side effects |
| M2 atomic-publisher implementation | BND-AUTH-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001; INT-003, INT-005, INT-007 | M2 commit | local bare-remote tests prove compare-and-swap, atomic capability, all-or-neither refs, no fallback, failed-pre-publish cleanup, and replacement-history rejection |
| M3 pre-transition release baseline B | BND-COMPAT-001, BND-COMPOSE-001; INT-006 | M3 commit B | release preparation and preflight prove exact v0.4.0 payload and immutable v0.3.6 rollback before activation |
| M4 transition candidate T and reviewed head H | BND-AUTH-001, BND-TEMPORAL-001, BND-RECOVERY-001; INT-002, INT-007 | M4 commit T; later lifecycle-only H commits | candidate validation at H proves one `B -> T`, self-contained T, allowed `T..H` paths, and rejects post-T release payload drift |
| Explicit release checkpoint | BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, BND-ENV-001; INT-002, INT-004, INT-005 | removable local tag and temporary detached worktree before publication | operator creates local `v0.4.0 -> T`, reruns strict validation at H, and runs full release verification from detached T; any failure removes only the local tag/worktree and publishes nothing |
| Atomic Git publication | BND-AUTH-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001; INT-003, INT-005 | one non-forced atomic push | helper revalidates evidence and advertised refs, then one `git push --atomic` maps main `P -> H` and absent tag to T or changes neither ref |
| Public publication and closeout | BND-STATE-001, BND-COMPOSE-001, BND-RECOVERY-001, BND-COMPAT-001, BND-ENV-001; INT-004, INT-005, INT-006 | immutable published refs and standing fix-forward process | tag workflow, GitHub/npm/archive/smoke evidence, rollback selection, partial-publication recovery, and final change-local closeout prove public state without rewriting refs |

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
  - `python scripts/select-validation.py --mode explicit --path scripts/validate-boundary-first.py --path scripts/boundary_first_validation.py --path scripts/test-boundary-first-validation.py --path scripts/fixtures/boundary-first/activation`
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
  - implement the exact non-mutating preflight command `python scripts/publish-boundary-activation.py --check --release v0.4.0 --candidate-evidence docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7/evidence/boundary-activation-candidate.json`
  - implement the matching explicit mutation command by replacing `--check` with `--publish`; reject invocation with neither or both modes
  - parse and revalidate candidate evidence
  - create an isolated temporary pre-push guard for same-push advertised identities
  - execute one plain `git push --atomic` only after all local gates pass
  - keep actual remote mutation behind an explicit release-only command boundary
- Validation commands:
  - `python scripts/test-boundary-activation-release.py`
  - `python scripts/test-select-validation.py`
  - `python -m py_compile scripts/boundary_activation_release.py scripts/publish-boundary-activation.py`
  - `python scripts/select-validation.py --mode explicit --path scripts/boundary_activation_release.py --path scripts/publish-boundary-activation.py --path scripts/test-boundary-activation-release.py --path scripts/validation_selection.py --path scripts/test-select-validation.py`
- Expected observable result: local integration fixtures update both refs or neither; normal implementation runs perform no external push.
- Commit message: `M2: add guarded atomic activation publication`
- Milestone closeout: focused validation, implementation evidence, commit, and independent code review.
- Risks: hook or remote capability assumptions could permit stale authority or partial mutation.
- Rollback/recovery: revert M2; no external ref was authorized or changed.

### M3. Commit the complete pre-transition v0.4.0 payload baseline B

- Milestone state: planned
- Goal: Generate, test, and commit every release-gated v0.4.0 input while activation remains pending; the resulting milestone commit is baseline `B`.
- Requirements: BFA-R001-R003, BFA-R002, BFA-R014, BFA-R026, BFA-R029-R030, BFA-R034; AC-BFA-004, AC-BFA-006, AC-BFA-010, AC-BFA-012-014.
- Files/components likely touched:
  - `docs/releases/profiles/v0.4.0.yaml` and generated v0.4.0 release surfaces
  - `packages/rigorloop/package.json` and profile-owned version projections
  - release notes, adapter metadata, token-cost baselines, package-lock projections, archives, fixtures, and packed-smoke inputs required by existing release tooling
  - any M1/M2 source and tests required in the tagged transition tree
- Dependencies:
  - M1 and M2 closed
  - clean approved test proof and current release generators
- Tests to add/update:
  - exact v0.4.0/v0.3.6 release identities while activation remains pending
  - three-target generated, archive, packed, and clean-install parity
  - complete release-gated input inventory for later tagged-tree proof
- Implementation steps:
  - create the routine profile and run repository-owned release preparation
  - complete all release-gated code, metadata, notes, package, fixture, generated-surface, and rollback changes
  - keep `specs/boundary-first-activation.yaml` pending and do not create an active projection
  - run generation checks, preflight, selected CI, and focused package/archive/rollback tests
  - commit the complete payload once as `B`; do not amend B after M4 starts
- Validation commands:
  - `python scripts/prepare-release.py v0.4.0 --check`
  - `python scripts/release-preflight.py v0.4.0`
  - `python scripts/select-validation.py --mode release --release-version v0.4.0`
  - `bash scripts/ci.sh --mode release --release-version v0.4.0`
- Expected observable result: commit `B` contains the complete v0.4.0 release payload, activation is still pending, and no release-gated change is needed to activate it.
- Commit message: `M3: prepare boundary-first v0.4.0 payload baseline`
- Milestone closeout: release preparation/preflight proof, selected validation, implementation evidence, commit B, and independent code review.
- Risks: an omitted release input discovered after T invalidates the entire candidate history.
- Rollback/recovery: before M4, fix and recommit the baseline through the normal M3 review loop; after T exists, supersede the branch instead of appending a payload fix.

### M4. Create and prove the narrow activation transition T

- Milestone state: planned
- Goal: Change pending to active exactly once as the child of B, then record non-public candidate proof at reviewed head H without changing release payload after T.
- Requirements: BFA-R004-R019, BFA-R024, BFA-R027-R028, BFA-R031-R035; AC-BFA-001-007, AC-BFA-011, AC-BFA-013-015.
- Exact tracked path changed by transition T:
  - `specs/boundary-first-activation.yaml`
- Files permitted after T:
  - only lifecycle evidence paths classified by the M1 validator and owned by this change record
- Dependencies:
  - M1-M3 closed, with M3 head designated as B
  - activation inputs in B are complete and reviewed
- Tests to add/update:
  - one exact first-parent `B -> T` pending-to-active transition
  - candidate proof of P/B/T/H and self-contained T with remote and local tag absent
  - lifecycle-only `T..H` acceptance and exact release-gated changed-path rejection
  - replacement branch required for any invalid post-T payload correction
- Implementation steps:
  - modify only the enumerated activation paths and commit them once, producing T with B as first parent
  - run candidate validation at H and record its stable JSON evidence as non-public proof
  - allow only validator-classified lifecycle evidence after T
  - if any release-gated file must change, stop, mark the candidate invalid, and rebuild one transition on a replacement branch from current authorized remote main
- Validation commands:
  - `python scripts/test-boundary-first-validation.py`
  - `python scripts/validate-boundary-first.py --check --activation-candidate v0.4.0`
  - `python scripts/select-validation.py --mode release --release-version v0.4.0`
  - `bash scripts/ci.sh --mode release --release-version v0.4.0`
- Expected observable result: candidate evidence proves `P ... B -> T ... H`, `v0.4.0` is absent locally and remotely, release-gated content is fixed at T, and publication remains pending.
- Commit message: `M4: activate boundary-first v1 for v0.4.0`
- Milestone closeout: candidate proof, implementation evidence, transition commit T, lifecycle-only evidence as needed, and independent code review.
- Risks: a code-review finding that requires a release-gated change makes this candidate history unusable.
- Rollback/recovery: abandon the local candidate and PR, delete any unpushed local tag if present, create a replacement branch from current authorized remote main, rebuild B and one new T, and repeat all reviews without force-push.

### Lifecycle closeout. Review, rationale, verification, PR, and explicit release

- Final holistic code review runs after all implementation milestones close.
- `explain-change` and `verify` require fresh actual-run evidence and coherent lifecycle state.
- `pr` prepares and opens the review handoff only after verify passes.
- Local tag creation, atomic remote main/tag publication, GitHub/npm publication, and public closeout require an explicit external-action checkpoint and are not authorized by implementation milestones.
- At that checkpoint, the release operator uses the candidate evidence at `docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7/evidence/boundary-activation-candidate.json` and performs these phases in order:
  1. read `transition_commit` from the candidate evidence and run `git tag v0.4.0 "$activation_transition"`;
  2. from H, run `python scripts/validate-boundary-first.py --check`;
  3. from a detached temporary worktree at T, run `bash scripts/release-verify.sh v0.4.0`;
  4. run `python scripts/publish-boundary-activation.py --check --release v0.4.0 --candidate-evidence docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7/evidence/boundary-activation-candidate.json`;
  5. only after all prior steps pass, replace `--check` with `--publish` to perform the single atomic ref update;
  6. let the existing tag workflow publish GitHub/npm/archive surfaces, then run `python scripts/close-release-publication.py v0.4.0` and `python scripts/validate-release.py v0.4.0` until public evidence closes.
- A failure before atomic publication removes the temporary worktree and local tag only; remote refs remain unchanged. A failure after atomic publication preserves immutable refs, records the exact partial state, and follows standing release closeout or fix-forward recovery.
- The exact tagged-tree command rule is: set `activation_candidate` to the candidate-evidence path; set `activation_transition` to `python -c 'import json,sys; print(json.load(open(sys.argv[1], encoding="utf-8"))["transition_commit"])' "$activation_candidate"`; set `activation_tmp_root` to `mktemp -d`; set `activation_worktree` to `$activation_tmp_root/tree`; run `git worktree add --detach "$activation_worktree" "$activation_transition"`; run `(cd "$activation_worktree" && bash scripts/release-verify.sh v0.4.0)`; then run `git worktree remove "$activation_worktree"` and `rmdir "$activation_tmp_root"`. If any pre-publication gate fails, perform the worktree cleanup when present and run `git tag -d v0.4.0`; do not run the publication command.

## Validation plan

- Run each milestone's focused unit/integration tests before broader selection.
- M1 and M2 use the exact explicit selector commands written in their milestone sections. If implementation touches another path, the test spec MUST add that literal `--path` argument before the milestone begins; no ellipsis or inferred path set is valid proof.
- M3 and M4 use `python scripts/select-validation.py --mode release --release-version v0.4.0` and `bash scripts/ci.sh --mode release --release-version v0.4.0`; the test spec records the resulting selected check IDs before M1 begins.
- Candidate-H proof is exactly `python scripts/validate-boundary-first.py --check --activation-candidate v0.4.0` from reviewed H with both local and remote `v0.4.0` absent.
- Strict-H proof is exactly `python scripts/validate-boundary-first.py --check` from H after local `v0.4.0` resolves to T.
- Detached-T proof is exactly `bash scripts/release-verify.sh v0.4.0` with the current directory set to a detached temporary worktree whose HEAD is T.
- Bare-remote proof is `python scripts/test-boundary-activation-release.py`; fixtures MUST exercise success, stale P, existing tag, non-fast-forward, unsupported atomic capability, one-ref rejection, and unchanged refs on every rejection.
- Failed-before-publish proof records local tag/worktree cleanup and unchanged advertised remote refs; public closeout proof uses `python scripts/close-release-publication.py v0.4.0` followed by `python scripts/validate-release.py v0.4.0`.
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
| 2026-08-05 | Use four implementation milestones: candidate validator, atomic publisher, pre-transition payload B, and narrow transition T. | B must be a committed and proved parent before the single transition can be created; splitting B from T makes review and replacement recovery realizable. | One broad release milestone; three milestones that conflate B and T; per-file micro-milestones. |
| 2026-08-05 | Record candidate output as workflow evidence instead of adding a manifest. | Existing profile, activation manifest, and change-local evidence already own state and proof. | New candidate manifest or profile schema. |
| 2026-08-05 | Keep external release operations in lifecycle closeout. | Tag, push, GitHub release, and npm publication require explicit authority. | Automatic publication during M3. |

## Readiness

- Ready for plan-review-r2 after lifecycle registration and validation.
- Readiness is not Done; test-spec, implementation reviews, final review, rationale, verify, PR, and explicit release remain.
