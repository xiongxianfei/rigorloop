<!-- Template: plan-skeleton-v3 -->
<!-- Skill: plan -->
<!-- Template status: normative -->

# Usability-First Boundary-First v0.4.0 Release

## Purpose / big picture

Make the existing `boundary-first-v1` guidance automatic and concise in ten published lifecycle skills, replace the unpublished candidate/publication experiment with current-file-only checked-revision activation, and prepare `v0.4.0` through the existing routine release workflow.

The implementation keeps one declarative activation record, one focused validator, one internal read-only inventory-derivation function, the existing resource projection model, and the standing release transaction. It adds no public activation command, state writer, custom publisher, service, dependency, or workflow stage.

## Current Handoff Summary

- Owning change record: `docs/changes/2026-08-06-usability-first-boundary-release/change.yaml`

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: `docs/proposals/2026-08-06-usability-first-boundary-release.md`
- Spec: `specs/usability-first-boundary-release.md`
- Spec review: `docs/changes/2026-08-06-usability-first-boundary-release/reviews/spec-review-r3.md`
- Architecture: `docs/architecture/system/architecture.md`
- ADR: `docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md`
- Architecture review: `docs/changes/2026-08-06-usability-first-boundary-release/reviews/architecture-review-r2.md`
- Test spec: pending `test-spec` after plan-review

## Context and orientation

`templates/shared/boundary-first-compact-scan.md` is the checked contributor source for the automatic compact scan copied into the ten governed `skills/*/SKILL.md` files. Canonical boundary resources live under `specs/references/`, their closed projection inventory is `specs/boundary-first-resources.yaml`, and projection, semantic, skill, and package regressions live under `scripts/` and `scripts/fixtures/boundary-first/`.

`specs/boundary-first-activation.yaml` is the only activation record. `scripts/boundary_first_validation.py` owns structural activation logic, the internal `derive_grandfathered_specs(root, baseline_revision)` authoring function, and rollback selection. `scripts/validate-boundary-first.py --check` is the retained public local validation path.

The exact UBR-R013 retirement inventory consists of three deleted scripts plus candidate/publication behavior removed from five retained script or test surfaces. Ordinary changed-path selection and the routine release path must remain.

Routine `v0.4.0` release work is profile-driven through `docs/releases/profiles/v0.4.0.yaml`, `scripts/prepare-release.py`, `scripts/release-preflight.py`, `scripts/release-verify.sh`, the trusted tag workflow, and `scripts/close-release-publication.py`. Lifecycle work prepares and verifies release inputs but performs no tag creation, push, publication, merge, or public-success claim.

The project map predates this activation revision, so it is used only for repository orientation. The approved spec, architecture, ADR, and directly inspected script interfaces govern exact behavior.

## Non-goals

- Do not redesign the eight-dimension proof model or create a separate boundary artifact for informal work.
- Do not add a public activation-preparation CLI, activation writer, state ledger, candidate evidence, custom readiness gate, or atomic publisher.
- Do not remove or weaken routine release preparation, preflight, verification, package smoke, trusted publication, public closeout, or immutable recovery.
- Do not migrate every historical accepted spec; preserve the frozen inventory and prospective-adoption model.
- Do not create or push `v0.4.0`, publish GitHub/npm artifacts, merge, or claim public availability during lifecycle execution.
- Do not embed mutable milestone or routing state in this plan or `docs/plan.md`.

## Requirements covered

| Requirements | Owning milestone or downstream evidence |
| --- | --- |
| UBR-R001 through UBR-R005, UBR-R018 | M1 automatic concise skill guidance and semantic journeys |
| UBR-R006 through UBR-R008, UBR-R013, UBR-R015, UBR-R017, UBR-R019 | M2 checked-revision validator, frozen-inventory compatibility, rollback proof, and exact custom-path retirement |
| UBR-R009 through UBR-R012, UBR-R015 through UBR-R017, UBR-R020 | M3 routine `v0.4.0` release inputs, parity, verification, and immutable release handoff |
| UBR-R006 through UBR-R012, UBR-R015, UBR-R017, UBR-R019, UBR-R020 | M4 active snapshot, exact reviewed pending baseline, integrated checked-revision and release proof |
| UBR-R014 | Every milestone plus the explicit external release boundary |

### Boundary and interaction ownership

| Boundary or interaction | Milestone | Affected surfaces | Rollback unit | Timed proof obligation |
| --- | --- | --- | --- | --- |
| BND-INPUT-001, INT-001 | M1 | compact scan, ten skills, semantic journeys, mapped resources | M1 source and fixture slice | Before M1 code review, prove ordinary, deeper, contract-required, and no-boundary cases semantically without prose or count assertions. |
| BND-STATE-001, BND-COMPAT-001 | M2, M4 | activation record, derivation function, validator, rollback selection | M2 validator cleanup; M4 active record | M2 proves independent pending/active fixtures and frozen compatibility; M4 proves the actual active record from an exact reviewed pending baseline. |
| BND-COMPOSE-001, INT-003 | M1 through M3 | ten skills, projections, generated targets, selector, routine release, deleted custom path | Each milestone's owned source slice | Each milestone proves its public and sibling paths before review; M3 executes the release-selected bundle and standing full gate while activation is pending. |
| BND-AUTH-001, BND-TEMPORAL-001 | M3, M4, external release handoff | profile/package/tag identities, pre-tag retry, trusted publication | Pre-public source correction; immutable patch-only recovery after publication | M3/M4 prove one coherent `v0.4.0` source package; only the trusted workflow may publish the exact reviewed commit. |
| BND-RECOVERY-001 | M2 through M4 | rollback metadata, validation failures, routine closeout | Exact `v0.3.6` selection and fix-forward release process | M2 proves local rollback selection; M3/M4 preserve phase-specific routine recovery and public closeout contracts. |
| BND-ENV-001, INT-002 | M2 through M4 | local checked revision, Git objects during one-time authoring, trusted GitHub/npm boundary | Local correction before publication; public closeout remains open on unavailable evidence | M2 proves normal `--check` needs no history/network/tag; M4 proves active-but-unpublished output; external evidence is never synthesized locally. |

## Milestones

### Preimplementation gate. Test-proof alignment

- Gate kind: upstream lifecycle gate, not an implementation milestone.
- Owner: `test-spec`, followed by `test-spec-review`.
- Exit: every UBR requirement, boundary, interaction, acceptance criterion, edge case, milestone, and command maps to executable automated proof or explicitly release-owned evidence.
- Failure: behavioral gaps route to spec; placement or interface gaps route to architecture; implementation does not repair upstream contracts.

### M1. Automatic concise behavior and semantic journeys

- Milestone type: implementation.
- Goal: Make automatic stage-owned boundary coverage explicit and semantically proven across all ten governed skills without adding a user-visible stage or exhaustive scenario matrix.
- Requirements: UBR-R001 through UBR-R005, UBR-R018; BND-INPUT-001; BND-COMPOSE-001; INT-001.
- Files/components likely touched:
  - `templates/shared/boundary-first-compact-scan.md`
  - the ten governed `skills/{workflow,spec,spec-review,plan,plan-review,test-spec,test-spec-review,implement,code-review,verify}/SKILL.md` files
  - `scripts/fixtures/boundary-first/semantic/`
  - `scripts/test-skill-validator.py`
  - `scripts/test-boundary-first-reference.py`
- Dependencies:
  - approved plan and approved test spec
  - standing resource projection and skill-contract rules
- Tests to add/update:
  - E1 specification journey: automatic material snapshot coverage with no irrelevant release or Git-history expansion
  - E2 inspection journey: loader and public caller coverage with no provider/publication expansion
  - E3 code-review journey: exact custom-path retirement plus retained validator, release, and rollback behavior
  - ordinary, explicit-deeper, contract-required, and no-admitted-boundary behavior
  - semantic inclusion/exclusion assertions with no exact prose, word-count, bullet-count, or method-name requirement
- Implementation steps:
  - add or revise semantic fixtures and failing assertions first
  - refine the shared compact-scan source only as needed to express automatic, concise, owner-scoped behavior
  - synchronize the shared block in all ten canonical skill bodies while preserving their distinct stage authority
  - preserve normalized formal spec/test-spec records and avoid creating informal boundary artifacts
  - regenerate or check skill-local mapped resources and generated Codex output through existing tooling
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-boundary-first-reference.py`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/validate-boundary-first.py --check`
- Expected observable result: related skills cover their material boundaries automatically and concisely, expand only when justified, and preserve formal artifact ownership.
- Commit message: `M1: make boundary coverage automatic and concise`
- Milestone closeout: targeted validation and implementation evidence, followed by independent code review and any required resolution.
- Risks:
  - shared wording could erase stage-specific responsibility or make every task look behavior-bearing
  - brittle semantic fixtures could test prose instead of decisions
- Rollback/recovery:
  - revert the M1 source and fixture slice together; regenerate derived output from canonical skills

### M2. Checked-revision activation and exact custom-path retirement

- Milestone type: implementation.
- Goal: Replace history/tag/remote-dependent activation with declarative current-file validation, retain one internal read-only derivation function, and remove only the closed custom experiment inventory.
- Requirements: UBR-R006 through UBR-R008, UBR-R013, UBR-R015, UBR-R017, UBR-R019; BND-STATE-001; BND-COMPOSE-001; BND-RECOVERY-001; BND-COMPAT-001; BND-ENV-001; INT-002; INT-003.
- Files/components likely touched:
  - `scripts/boundary_first_validation.py`
  - `scripts/validate-boundary-first.py`
  - `scripts/test-boundary-first-validation.py`
  - `scripts/validation_selection.py`
  - `scripts/test-select-validation.py`
  - `scripts/fixtures/boundary-first/activation/`
  - deleted: `scripts/boundary_activation_release.py`
  - deleted: `scripts/publish-boundary-activation.py`
  - deleted: `scripts/test-boundary-activation-release.py`
- Dependencies:
  - M1 closes with coherent governed skill/resource identities
  - approved test proof for pending, active-unpublished, malformed, compatibility, and cleanup paths
- Tests to add/update:
  - independently valid pending and active snapshots with exact field tuples
  - missing, additional, malformed, unknown, mixed, stale, and divergent current-file inputs
  - active validation with no tag, unreachable baseline, absent history, no remote, and no network
  - output identifies snapshot and release intent but never public availability
  - `derive_grandfathered_specs(root, baseline_revision)` accepts one exact full baseline, returns raw-byte-sorted eligible paths or bounded issues, and performs no writes
  - normal `--check` never invokes the derivation function
  - exact `v0.3.6` three-adapter rollback selection and private-value suppression
  - three deleted paths are absent; five retained surfaces omit candidate/publication behavior; ordinary selector and routine release checks remain
- Implementation steps:
  - write checked-revision and cleanup regressions before changing production paths
  - extract and expose the internal derivation function contract without adding a CLI
  - make normal validation read only the current activation record, current source/resource/projection/adapter identities, and frozen inventory
  - remove candidate, publication-readiness, transition, tag-derived, remote-ref, and custom-publication logic from retained modules and tests
  - delete the three custom scripts and remove their selector catalog/path dependencies
  - preserve ordinary boundary validation, changed-spec routing, rollback selection, routine release selection, and closed-vocabulary failure behavior
- Validation commands:
  - `python scripts/test-boundary-first-validation.py`
  - `python scripts/test-select-validation.py`
  - `python scripts/validate-boundary-first.py --check`
  - `python scripts/select-validation.py --mode explicit --path scripts/boundary_first_validation.py --path scripts/validate-boundary-first.py --path scripts/test-boundary-first-validation.py --path scripts/validation_selection.py --path scripts/test-select-validation.py`
  - `python -m py_compile scripts/boundary_first_validation.py scripts/validate-boundary-first.py scripts/validation_selection.py`
- Expected observable result: pending or active current files validate locally without public-state dependencies; retired custom behavior is absent and unselectable; routine release and rollback paths remain.
- Commit message: `M2: simplify boundary activation to checked revision`
- Milestone closeout: targeted validation and implementation evidence, followed by independent code review and any required resolution.
- Risks:
  - removing history logic could accidentally remove frozen-inventory or rollback enforcement
  - broad selector cleanup could suppress ordinary boundary or routine release checks
- Rollback/recovery:
  - revert the M2 slice before activation; keep the record pending and publish nothing

### M3. Routine v0.4.0 release payload and package parity

- Milestone type: implementation.
- Goal: Prepare every routine `v0.4.0` source, metadata, package, archive, and local proof surface while the activation record remains pending.
- Requirements: UBR-R009 through UBR-R012, UBR-R015 through UBR-R017, UBR-R020; BND-AUTH-001; BND-COMPOSE-001; BND-TEMPORAL-001; BND-RECOVERY-001; BND-COMPAT-001; BND-ENV-001; INT-002; INT-003.
- Files/components likely touched:
  - `docs/releases/profiles/v0.4.0.yaml`
  - `docs/releases/v0.4.0.md` and `docs/releases/v0.4.0/`
  - `docs/reports/adapter-artifacts/releases/v0.4.0.yaml`
  - release token-cost evidence required by the profile
  - `packages/rigorloop/package.json`, bundled release metadata, and package tests
  - `scripts/release-verify.sh` and profile-owned routine release support for `v0.4.0`
  - generated temporary adapter archives and packed npm package proof, not tracked generated adapter bodies
- Dependencies:
  - M1 and M2 closed and reviewed
  - `v0.3.6` immutable rollback metadata remains complete
  - routine release generators and validators remain authoritative
- Tests to add/update:
  - exact `v0.4.0`/`0.4.0`/`latest` profile, package, notes, and metadata agreement
  - Codex, Claude, and opencode mapped-resource parity across canonical, generated, archived, packed, and clean-installed surfaces
  - archive integrity, package allowlist, version consistency, rollback metadata, secret suppression, and routine recovery evidence shape
  - routine release selection remains present after custom-path retirement
- Implementation steps:
  - add the `v0.4.0` routine profile and failing release-contract fixtures first
  - run release preparation to generate only profile-owned surfaces and complete required human-authored notes/evidence
  - update package and bundled metadata through existing generators; do not hand-edit generated adapter bodies
  - keep `specs/boundary-first-activation.yaml` pending throughout M3
  - run preflight, execute the release-selected CI bundle, then run the standing full release gate for package/archive generation and clean-install smoke
  - treat the M3 gates as proof of the pending baseline; M4 reruns them only after activation changes the checked state
  - close M3 only after independent code review; the exact reviewed pending revision selected after closeout becomes M4's explicit baseline input
- Validation commands:
  - `python scripts/prepare-release.py v0.4.0`
  - `python scripts/prepare-release.py v0.4.0 --check`
  - `python scripts/release-preflight.py v0.4.0 --skip-remote`
  - `python scripts/test-release-transaction.py`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/test-npm-package-publication.py`
  - `python scripts/select-validation.py --mode release --release-version v0.4.0`
  - `bash scripts/ci.sh --mode release --release-version v0.4.0`
  - `bash scripts/release-verify.sh v0.4.0`
- Expected observable result: one reviewed pending revision passes the executable release-selected bundle and standing full gate for the complete routine `v0.4.0` payload and coherent three-target package proof, without a tag or public claim.
- Commit message: `M3: prepare routine v0.4.0 release payload`
- Milestone closeout: release preparation/preflight evidence and targeted validation, followed by independent code review and any required resolution.
- Risks:
  - generated release surfaces could drift from canonical skills or package version
  - release-specific support could accidentally become a second publication path
- Rollback/recovery:
  - while pending, correct and regenerate through the M3 review loop; no public state changes

### M4. Active snapshot and integrated pre-public verification

- Milestone type: implementation.
- Goal: Freeze the exact reviewed pending baseline and derived historical inventory in one active snapshot, then prove checked-revision activation and the complete routine release package together.
- Requirements: UBR-R006 through UBR-R012, UBR-R015, UBR-R017, UBR-R019, UBR-R020; all eight BND IDs; INT-002; INT-003.
- Files/components likely touched:
  - `specs/boundary-first-activation.yaml`
  - activation fixtures and release metadata affected by the active snapshot identity
  - generated temporary skill/package/archive proof required by the routine gate
- Dependencies:
  - M1 through M3 closed and independently reviewed
  - one exact full reviewed pending-revision commit identity selected from the closed M3 source state
  - no unresolved plan, test-spec, implementation, or code-review finding affecting the activation input
- Tests to add/update:
  - successful internal derivation result exactly matches the active record's sorted inventory
  - invalid or unavailable baseline derivation performs no activation write
  - the actual active record passes with baseline history unavailable and no `v0.4.0` tag
  - active output reports release intent only; tag/public claims remain blocked
  - complete canonical/generated/adapter/rollback identities remain coherent
  - full routine release gate accepts `v0.4.0` without invoking retired custom paths
- Implementation steps:
  - record the exact reviewed M3 pending revision as the authoring input
  - call `derive_grandfathered_specs(root, baseline_revision)` once and record its successful input/output in implementation evidence
  - update only the declarative activation fields and frozen inventory; do not create a writer or transition receipt
  - regenerate or revalidate every derived identity affected by the active record
  - run checked-revision, release preflight, selected CI, full routine release verification, and three-target packed installation proof
  - preserve `v0.3.6` rollback and stop before any tag, push, publication, merge, or public-success claim
- Validation commands:
  - `python scripts/test-boundary-first-validation.py`
  - `python scripts/validate-boundary-first.py --check`
  - `python scripts/release-preflight.py v0.4.0 --skip-remote`
  - `bash scripts/ci.sh --mode release --release-version v0.4.0`
  - `bash scripts/release-verify.sh v0.4.0`
- Expected observable result: the checked repository is coherently active for release intent `v0.4.0`, the frozen inventory comes from the exact reviewed pending baseline, routine release proof passes, and no public availability is claimed.
- Commit message: `M4: activate checked-revision boundary-first v0.4.0`
- Milestone closeout: integrated validation and implementation evidence, followed by independent code review and any required resolution.
- Risks:
  - choosing the wrong baseline would freeze an incorrect compatibility inventory
  - release verification could accidentally depend on the removed custom path or public state
- Rollback/recovery:
  - before publication, restore the pending record or correct the source through a reviewed M4 revision and rerun all integrated proof; after immutable publication, use routine closeout, dist-tag correction or deprecation when applicable, or a later patch without rewriting `v0.4.0`

## Validation plan

| Validation layer | Commands | Purpose |
| --- | --- | --- |
| Skill semantics | `python scripts/test-skill-validator.py`; `python scripts/test-boundary-first-reference.py`; `python scripts/validate-skills.py` | Prove automatic concise stage ownership and non-brittle E1-E3 journeys. |
| Activation | `python scripts/test-boundary-first-validation.py`; `python scripts/validate-boundary-first.py --check` | Prove snapshot closure, one-time derivation, current-file-only validation, rollback, and claim separation. |
| Selector and cleanup | `python scripts/test-select-validation.py`; explicit selection over M2 paths | Prove retired behavior is unselectable while ordinary boundary and release checks remain. |
| Generated parity | `python scripts/build-skills.py --check`; `python scripts/test-adapter-distribution.py`; release-output adapter validation selected by the routine gate | Prove canonical/generated/archive/install parity for all three targets. |
| Routine release | `python scripts/prepare-release.py v0.4.0 --check`; `python scripts/release-preflight.py v0.4.0 --skip-remote`; `bash scripts/ci.sh --mode release --release-version v0.4.0`; `bash scripts/release-verify.sh v0.4.0` | Prove the pending M3 baseline, then rerun after M4 activation changes the checked state, without external mutation. |
| Final lifecycle verification | Commands named by the approved test spec plus final `explain-change`, `verify`, and `pr` gates | Prove artifact/code/test coherence and branch readiness only after all implementation milestones close. |

## External release handoff

After PR approval and merge, an authorized maintainer may tag the exact reviewed release commit and run the trusted routine publication workflow. That external operation must use the existing `v0.4.0` profile, verify the immutable tag identity, publish GitHub and npm artifacts, run fresh public `npx` smoke for Codex, Claude, and opencode, and record rerunnable public closeout. It is not an implementation milestone and is not authorized by this plan.

If public evidence is delayed or partial, closeout remains open and records the failed phase. Recovery uses rerunnable closeout, dist-tag correction or deprecation when applicable, or a later patch; neither `v0.4.0` nor `v0.3.6` is rewritten.

## Risks and recovery

- Risk: automatic guidance becomes exhaustive or repetitive.
  - Recovery: revert the shared guidance/fixtures together and preserve the last accepted concise semantics.
- Risk: cleanup removes standing validation or routine release protection.
  - Recovery: the closed UBR-R013 table controls deletion; selector and routine-release regressions must pass before M2 closes.
- Risk: the frozen historical inventory is incomplete or grows after activation.
  - Recovery: derive once from the exact reviewed pending SHA, compare the recorded tuple directly, and make later validation read only the frozen record.
- Risk: checked activation is confused with public release.
  - Recovery: keep local output release-intent-only and require immutable tag plus public evidence for public claims.
- Risk: generated targets or package metadata diverge.
  - Recovery: regenerate from canonical sources and rerun three-target archive, package, and clean-install proof before review.
- Risk: public release becomes partial.
  - Recovery: retain immutable artifacts, keep closeout open, rerun closeout or fix forward through a later patch.

## Dependencies

- Approved spec, architecture, ADR, and their closed formal reviews.
- Approved test spec and test-spec review before M1 implementation.
- M1 closes before M2 so checked activation sees final governed skill/resource identities.
- M2 closes before M3 so release proof cannot select or depend on retired custom behavior.
- M3 closes before M4 so one exact reviewed pending revision can be supplied to the internal derivation function.
- Every implementation milestone follows `implement -> code-review -> review-resolution when triggered -> fixes/rereview when needed -> close` before the next milestone.
- Existing Python, Git, Node/npm, archive, adapter, and trusted GitHub release tooling; no new dependency.
- External tag creation and publication require explicit maintainer authority after lifecycle readiness and merge.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-06 | Use four implementation milestones: skill behavior, activation cleanup, pending routine release payload, then active integrated proof. | Each milestone has one primary rollback unit and proof boundary; M4 receives a concrete reviewed pending baseline only after the payload is stable. | One large milestone would couple usability, cleanup, activation, and release failure; more milestones would split tightly coupled validator or release proof. |
| 2026-08-06 | Keep inventory derivation as an internal function used once in M4. | It gives deterministic authoring and testability without a permanent user-facing command or second writer. | Public CLI, separate script, manual unscripted inventory, or recurring Git-history validation. |
| 2026-08-06 | Prepare the complete routine release while activation remains pending. | It makes the baseline input reviewable and keeps pre-public recovery simple. | Activate before package/release payload review or restore the custom candidate/publication protocol. |
| 2026-08-06 | Execute both the release-selected CI bundle and standing full gate in M3, then rerun after activation in M4. | The selector only reports checks, release-mode CI does not invoke `release-verify.sh`, and each checked state must close independently. | Selection-only proof in M3 or deferring pending-baseline proof to M4. |
| 2026-08-06 | Treat publication as an external handoff, not an implementation milestone. | UBR-R014 forbids lifecycle stages from tagging, publishing, merging, or claiming public availability. | Automatic tag/push/publication during implementation or verification. |

## Readiness

- See the owning change record for current workflow and milestone state.
- The plan is ready for plan-review after authoring validation.
- Remaining completion gates: plan-review, test-spec, test-spec-review, four implementation/code-review loops, any triggered review-resolution or CI maintenance, explain-change, verify, PR, merge, and the separately authorized routine public release and closeout.
- Readiness is not Done.
