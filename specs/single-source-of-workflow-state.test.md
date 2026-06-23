# Single Source of Workflow State Test Spec

## Status

- active

## Related spec and plan

- Spec: [Single Source of Workflow State](single-source-of-workflow-state.md), approved.
- Proposal: [Single Source of Workflow State](../docs/proposals/2026-05-09-single-source-of-workflow-state.md), accepted.
- Follow-up proposal: [Workflow-State Projection and Pre-Transition Synchronization Gate](../docs/proposals/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md), accepted.
- Plan: [Single Source of Workflow State Execution Plan](../docs/plans/2026-05-09-single-source-of-workflow-state.md), active after clean plan-review.
- Follow-up plan: [Workflow-State Projection and Pre-Transition Synchronization Gate Plan](../docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md), approved by plan-review-r2.
- Architecture: [RigorLoop Canonical System Architecture](../docs/architecture/system/architecture.md). The approved architecture keeps state-sync validation inside artifact-lifecycle validation and introduces no service, storage, deployment, security, or public API boundary.
- Project map: `docs/project-map.md` is absent. This test spec does not rely on project-map claims; proof uses the approved spec, active plan, workflow docs, stage skills, generator scripts, and existing validator patterns.
- Follow-up reviews:
  - [spec-review-r2](../docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/reviews/spec-review-r2.md)
  - [architecture-review-r1](../docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/reviews/architecture-review-r1.md)
  - [plan-review-r2](../docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/reviews/plan-review-r2.md)
- Related proof surfaces:
  - `scripts/test-skill-validator.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - `scripts/test-change-metadata-validator.py`
  - `scripts/validate-skills.py`
  - `scripts/build-skills.py`
  - `scripts/build-adapters.py`
  - `scripts/validate-adapters.py`
  - `scripts/test-adapter-distribution.py`
  - `scripts/select-validation.py`
  - `scripts/ci.sh`

## Testing strategy

- Use contract and static wording checks because the approved first implementation slice is workflow guidance, skill text, artifact lifecycle guidance, and generated output, not a runtime workflow router.
- Use `scripts/test-skill-validator.py` for machine-checkable invariants in canonical skill wording, public-surface portability, state ownership, and handoff claim boundaries.
- Use `scripts/test-artifact-lifecycle-validator.py` for lifecycle-managed artifact state, readiness wording, and plan/index consistency where structural validation already exists.
- Use `scripts/test-change-metadata-validator.py` and `scripts/validate-change-metadata.py` for compact change metadata structure and unresolved finding count checks.
- Use generated-output drift checks after canonical skill edits to prove `.codex/skills/` and public adapter packages remain derived output.
- Use selector validation and explicit CI scopes to prove changed paths are classified and validated without depending on broad smoke.
- Use unit and integration fixtures for exact owner-field syntax, plan-index table projection parsing, readiness pointer enforcement, stale-token surface boundaries, and review evidence consistency.
- Use contract checks for validator layering so any dedicated state-sync command delegates to the same parser/comparison helpers used by artifact-lifecycle validation.
- Use migration fixtures to prove active, blocked, reopened, and lifecycle-changing plans are enforced while untouched historical ledgers and archived plans remain valid.
- Use manual contract review where natural-language distinction is intentional, such as scoped summaries versus live next-stage authority.
- Do not add broad semantic plan-state parsing, a runtime workflow simulator, or natural-language scoring in the first implementation slice.

## Requirement coverage map

| Requirement IDs | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `R1`, `R2` | `T1`, `T11` | integration, manual | One primary live-state owner and `Current Handoff Summary` authority |
| `R3`-`R8` | `T2`, `T11` | integration, manual | Plan sections outside current handoff remain historical/evidence-only |
| `R9`-`R14` | `T3`, `T7`, `T11` | integration, manual | Change metadata, review-resolution, review-log, explain-change, verify, and PR claim boundaries |
| `R15`-`R20` | `T4`, `T8`, `T11` | integration, manual | Milestone state vocabulary and clean/finding review transitions |
| `R21`-`R28` | `T5`, `T8`, `T11` | integration, manual | State-sync checklist and stale live-state cleanup |
| `R29`-`R31` | `T6`, `T11` | integration, manual | Plan closeout, true downstream events, and merge not being routine completion |
| `R32`, `R33` | `T9`, `T11` | integration, manual | Published skill portability boundary |
| `R34` | `T10`, `T11` | integration, manual | First slice remains static/focused, not broad semantic validation |
| `R35`, `R36` | `T9`, `T11` | integration, smoke | Generated skill/adapters and versioned adapter validation |
| `R37`-`R42` | `T12`, `T16`, `T19`, `T22` | unit, integration, contract | Artifact role taxonomy, owner/projection/pointer/ledger/evidence semantics, and derived last-reviewed evidence |
| `R43`-`R48` | `T12`, `T13`, `T22` | unit, integration | Exact `Current Handoff Summary` fields, milestone state enum, final readiness enum, and structured review status |
| `R49`-`R52` | `T13`, `T15`, `T22` | unit, integration | Final-closeout reason codes and pointer-only `Readiness` |
| `R53`-`R55b` | `T14`, `T22` | unit, integration | Active/blocked `docs/plan.md` projection table and authoritative source fields |
| `R56`, `R57` | `T15`, `T19`, `T22` | unit, migration | Current milestone-state projection and closed historical milestone preservation |
| `R58`-`R63` | `T16`, `T18`, `T22` | integration, contract | Binding pre-transition state-sync gate, verify/CI enforcement, optional hooks, and partial-transition recovery |
| `R64`-`R72` | `T17`, `T22` | integration | Review-log, review-resolution, and change metadata consistency for open material findings, shared closure predicates, and derived-only metadata |
| `R73`-`R76` | `T18`, `T22` | unit, integration | Parser-scoped stale-token detection and raw grep diagnostic boundary |
| `R77`-`R80` | `T20` | unit, contract | Optional projection writer dry-run, write boundaries, and golden fixtures |
| `R81`-`R83` | `T19`, `T22` | migration | First enforcement scope and historical plan compatibility |
| `R84`-`R86` | `T16`, `T21`, `T22` | integration, contract | Shared state-sync parser/comparison module and no conflicting parser authorities |
| `R87` | `T22` | manual | Post-rollout success metric tracking remains an observable follow-up |
| `EB1`-`EB7` | `T5`, `T7`, `T8`, `T9`, `T11` | integration, manual | Boundary/error behavior for stale state, open review-resolution, plan/index drift, and public-skill internals |
| `EB8`-`EB16` | `T12`, `T14`, `T15`, `T17`, `T18`, `T19`, `T22` | unit, integration, migration | Owner parse failures, projection mismatches, pointer violations, material finding conflicts, stale-token boundaries, and partial-transition recovery |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| `E1` | `T1`, `T2`, `T4` | Active plan owns next stage; readiness points to summary |
| `E2` | `T3`, `T5`, `T8` | Review-resolution owns closeout, active plan owns milestone state |
| `E3` | `T4`, `T6`, `T8` | Final closeout waits for closed implementation milestones and review-resolution |
| `E4` | `T6`, `T11` | PR handoff closes repo-local state before review; merge is not routine completion event |
| `E5` | `T14`, `T15`, `T16` | Synchronized implementation handoff passes when owner, projection, and pointer surfaces agree |
| `E6` | `T15`, `T18` | Stale readiness wording blocks review handoff |
| `E7` | `T18`, `T19` | Historical tokens remain valid in ledgers and review history |
| `E8` | `T17` | Unresolved material findings block downstream readiness |
| `E9` | `T12`, `T13` | Bounded owner fields use structured values |
| `E10` | `T14` | Plan-index projection sources are deterministic |

## Edge case coverage

- `EC1`: lifecycle-closeout milestone does not count as implementation milestone: `T6`, `T8`
- `EC2`: direct manual skill invocation does not claim full plan state: `T3`, `T7`
- `EC3`: clean review can settle artifact-locally but milestone state owner remains active plan: `T4`, `T8`
- `EC4`: isolated material finding still records review files while stopping handoff: `T3`, `T5`
- `EC5`: true downstream event keeps plan active only when named: `T6`
- `EC6`: public adapter packages use portable concepts: `T9`
- `EC7`: state-sync can be recorded in several places, but live next-stage value stays in current handoff: `T5`, `T8`
- `EC8`: clean review closes a milestone only after owner, milestone projection, and plan-index projection synchronize: `T15`, `T16`
- `EC9`: `review-requested` after review-resolution means rereview is pending, not downstream gate approval: `T17`
- `EC10`: stable `Readiness is not Done` text is allowed when it does not restate live state: `T15`
- `EC11`: next-stage-like `change.yaml` fields are valid only as derived evidence, not competing owners: `T17`
- `EC12`: raw `rg` stale-token hits are diagnostic only until parser-scoped gate confirms a live-state surface: `T18`
- `EC13`: projection writer must not alter ledgers or evidence files: `T20`
- `EC14`: missing local pre-commit hook does not weaken enforcement because stage handoff, verify, and CI are binding: `T16`

## Test cases

### T1. Active plan exposes one live current handoff owner

- Covers: `R1`, `R2`, `E1`
- Level: integration, manual
- Fixture/setup:
  - `docs/workflows.md`
  - `docs/examples/plans/example-plan.md`
  - `skills/plan/SKILL.md`
  - active plan after each milestone update
- Steps:
  - Assert contributor guidance names `Current Handoff Summary` as the live state owner for planned initiatives.
  - Assert the current handoff fields cover current milestone, milestone state, last reviewed milestone, review status, remaining in-scope implementation milestones, next stage, final closeout readiness, and reason.
  - Inspect the active plan during M1-M5 updates and confirm live state can be located from that one section.
- Expected result:
  - A reviewer can identify current planned-initiative state without comparing several sections.
- Failure proves:
  - The implementation leaves live workflow state distributed across competing surfaces.
- Automation location:
  - `scripts/test-skill-validator.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - manual review during M2-M5.

### T2. Non-owner plan sections do not duplicate live next-stage claims

- Covers: `R3`-`R8`, `R28`, `E1`
- Level: integration, manual
- Fixture/setup:
  - `docs/examples/plans/example-plan.md`
  - active plan body
  - `skills/plan/SKILL.md`
- Steps:
  - Assert `Readiness` guidance points to `Current Handoff Summary` for live state.
  - Assert `Progress`, `Decision log`, `Validation notes`, and final outcome sections are described as history, decisions, evidence, or final-only surfaces.
  - Confirm touched plan sections do not independently claim a stale next stage.
- Expected result:
  - Non-owner plan sections can provide useful history without becoming live next-stage authorities.
- Failure proves:
  - The same next-stage fact can drift between current handoff and other plan sections.
- Automation location:
  - `scripts/test-artifact-lifecycle-validator.py`
  - `scripts/test-skill-validator.py`
  - manual review during M2 and M5.

### T3. Change-local evidence surfaces keep scoped ownership

- Covers: `R9`-`R14`, `EB4`, `EB5`, `EC2`, `EC4`
- Level: integration, manual
- Fixture/setup:
  - `docs/changes/<change-id>/change.yaml`
  - `docs/changes/<change-id>/review-log.md`
  - `docs/changes/<change-id>/review-resolution.md`
  - `skills/explain-change/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/pr/SKILL.md`
- Steps:
  - Assert change metadata stores compact status, unresolved finding counts, validation records, and artifact pointers without owning the active plan next stage.
  - Assert review-resolution owns material-finding disposition and closeout status, not plan readiness.
  - Assert explain-change guidance does not claim final verify, branch-ready, PR-ready, or live plan next-stage status.
  - Assert verify owns final validation proof and branch-readiness evidence while PR owns PR handoff text.
- Expected result:
  - Change-local and final handoff artifacts keep traceability while avoiding duplicated live state.
- Failure proves:
  - Review, rationale, verification, or PR evidence can reintroduce competing state ownership.
- Automation location:
  - `scripts/test-skill-validator.py`
  - `scripts/validate-change-metadata.py`
  - `scripts/validate-review-artifacts.py`
  - manual review during M3 and M5.

### T4. Milestone state vocabulary and transitions are enforced

- Covers: `R15`-`R20`, `E1`, `E3`, `EC3`
- Level: integration, manual
- Fixture/setup:
  - `docs/workflows.md`
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/plan/SKILL.md`
  - active milestone plan
- Steps:
  - Assert allowed milestone states are exactly `planned`, `implementing`, `review-requested`, `resolution-needed`, and `closed`.
  - Assert `implementation-complete` and `review-clean` are rejected as state values but allowed as evidence descriptions.
  - Assert implement hands off with `review-requested` after targeted validation.
  - Assert code-review transitions clean milestones to `closed` and finding-bearing milestones to `resolution-needed`.
  - Assert final closeout is not available until all in-scope implementation milestones are `closed`.
- Expected result:
  - Milestone state is stable and unambiguous across plan, implement, and code-review guidance.
- Failure proves:
  - The implementation permits stale or ambiguous milestone state labels.
- Automation location:
  - `scripts/test-skill-validator.py`
  - manual review during M2-M5.

### T5. State-sync checklist updates affected owners

- Covers: `R21`-`R28`, `EB1`-`EB5`, `EC4`, `EC7`
- Level: integration, manual
- Fixture/setup:
  - `docs/workflows.md`
  - `skills/plan/SKILL.md`
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - active plan and change-local review artifacts
- Steps:
  - Assert state-changing handoff guidance requires updating `Current Handoff Summary`, milestone state, review-resolution when findings change, review-log open findings when review records change, `change.yaml` compact review/status when metadata changes, and `docs/plan.md` when lifecycle state changes.
  - Assert stale live next-stage wording in touched artifacts must be removed or corrected before downstream readiness is claimed.
  - Exercise the checklist manually during each milestone handoff and review-resolution loop.
- Expected result:
  - Handoff state changes are synchronized across affected owners before downstream readiness is claimed.
- Failure proves:
  - The implementation leaves the same stale-state drift that motivated the change.
- Automation location:
  - `scripts/test-skill-validator.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - `scripts/validate-change-metadata.py`
  - `scripts/validate-review-artifacts.py`
  - manual review during M1-M5.

### T6. Plan lifecycle closeout and merge boundary remain explicit

- Covers: `R29`-`R31`, `E3`, `E4`, `EC1`, `EC5`
- Level: integration, manual
- Fixture/setup:
  - `docs/workflows.md`
  - `AGENTS.md`
  - `CONSTITUTION.md`
  - active plan and `docs/plan.md`
- Steps:
  - Assert guidance says a plan should move to `Done` inside the PR when repo-local lifecycle completion is true.
  - Assert active state remains valid only when a true downstream event is named.
  - Assert merge itself is not described as the routine plan-completion event.
  - Confirm lifecycle-closeout milestones are not counted as open implementation milestones.
- Expected result:
  - Plan lifecycle state is closed before review when the PR tree makes completion true, and true downstream events remain explicitly named.
- Failure proves:
  - The implementation preserves or reintroduces stale plan state tied to repository integration instead of PR-tree evidence.
- Automation location:
  - `scripts/test-artifact-lifecycle-validator.py`
  - manual review during M2 and M5.

### T7. Verify, explain-change, and PR claim boundaries stay separated

- Covers: `R12`-`R14`, `EB5`, `EC2`
- Level: integration, manual
- Fixture/setup:
  - `skills/explain-change/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/pr/SKILL.md`
  - final change-local artifacts
- Steps:
  - Assert explain-change does not claim final validation, branch-ready, PR-ready, or CI-final status.
  - Assert verify checks explain-change currency and owns final validation proof/branch-readiness evidence.
  - Assert PR handoff summarizes readiness after verify without becoming the active plan state owner.
  - Confirm final stages stop while required review-resolution remains open.
- Expected result:
  - Final handoff surfaces preserve the approved final order and do not duplicate live plan state.
- Failure proves:
  - Final closeout can again become contradictory across rationale, verify, and PR handoff.
- Automation location:
  - `scripts/test-skill-validator.py`
  - manual review during M3 and M5.

### T8. Milestone review loop blocks premature final closeout

- Covers: `R18`-`R20`, `R21`-`R28`, `E2`, `E3`, `EC1`, `EC3`, `EC7`
- Level: integration, manual
- Fixture/setup:
  - active plan M1-M4
  - code-review and review-resolution records
  - `docs/changes/<change-id>/review-log.md`
  - `docs/changes/<change-id>/review-resolution.md`
- Steps:
  - During each implementation milestone, confirm targeted validation passes before handoff to code-review.
  - Confirm material findings move the same milestone to `resolution-needed`.
  - Confirm accepted findings are fixed or explicitly dispositioned before the milestone returns to `review-requested` or `closed`.
  - Confirm M5 does not begin until M1-M4 are closed and required review-resolution is closed.
- Expected result:
  - The milestone loop remains reviewable and final closeout cannot hide unresolved implementation work.
- Failure proves:
  - The workflow can skip milestone review or closeout under the new state model.
- Automation location:
  - `scripts/validate-review-artifacts.py`
  - `scripts/validate-change-metadata.py`
  - active plan review during M1-M5.

### T9. Public skill portability and generated output stay aligned

- Covers: `R32`, `R33`, `R35`, `R36`, `EB7`, `EC6`
- Level: integration, smoke, manual
- Fixture/setup:
  - changed canonical skills
  - generated `.codex/skills/`
  - generated public adapter packages under `dist/adapters/`
  - adapter manifests
- Steps:
  - Assert published skill wording uses portable concepts such as project workflow guide, local workflow contract, project validation command, active plan, and change metadata.
  - Assert public skill text does not expose repository-internal source paths, validator scripts, generated adapter internals, selector path constraints, or local examples as universal requirements.
  - Regenerate local skills and adapters after canonical skill changes.
  - Run skill validation, generated skill drift check, adapter drift check, adapter validation, and adapter distribution tests.
- Expected result:
  - All shipped skill copies reflect canonical sources and remain portable for downstream users.
- Failure proves:
  - Different tool adapters can ship stale or repository-specific workflow-state guidance.
- Automation location:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/test-adapter-distribution.py`
  - manual generated diff review during M4.

### T10. First implementation slice avoids broad semantic validation

- Covers: `R34`
- Level: integration, manual
- Fixture/setup:
  - `scripts/test-skill-validator.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - active plan changed-file list
- Steps:
  - Confirm M1-M4 do not add broad natural-language scoring, runtime workflow simulation, or semantic plan-state parsing.
  - Confirm focused checks use stable headings, required positive phrases, narrow forbidden stale phrases, and existing structural validators.
  - Confirm any manual contract verification is recorded in plan validation notes or review evidence.
- Expected result:
  - The first implementation slice remains bounded and reviewable.
- Failure proves:
  - The implementation exceeds the approved validation scope.
- Automation location:
  - `rg --files`
  - `scripts/test-skill-validator.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - manual changed-file review before code-review.

### T11. Full milestone and final validation closeout

- Covers: all requirements, examples, edge cases, and acceptance criteria as final integration proof
- Level: integration, smoke, manual
- Fixture/setup:
  - all changed authored, generated, plan, review, and change-local paths
  - active plan validation commands
- Steps:
  - Run selector validation for each milestone's changed path set and record no unclassified paths.
  - Run targeted validation listed in the active plan for each milestone.
  - Before PR, run final lifecycle, skill, generated-output, adapter, review-artifact, change-metadata, and diff checks listed in M5.
  - Manually confirm `Current Handoff Summary`, `Readiness`, change metadata, review-resolution, explain-change, verify evidence, and PR handoff do not conflict.
- Expected result:
  - The implementation is proven by repository-owned static, generated-output, adapter, lifecycle, and selected CI checks with no stale live-state contradictions.
- Failure proves:
  - The change lacks durable proof or reintroduces the workflow-state drift it was designed to remove.
- Automation location:
  - active plan commands
  - `scripts/ci.sh`

### T12. Current Handoff Summary owner fields parse exactly

- Covers: `R37`-`R48`, `EB8`, `E9`, `AC-WSS-001`-`AC-WSS-003`, `AC-WSS-017`-`AC-WSS-019`
- Level: unit
- Fixture/setup:
  - Valid and invalid active plan fixtures under `tests/fixtures/artifact-lifecycle/workflow-state-owner/`.
  - Fixtures contain one `Current Handoff Summary` section with exact required bullet labels.
- Steps:
  - Parse a valid owner block containing all required fields exactly once.
  - Run `TWSS-OWNER-001` with `Review status: review-requested; stage=code-review; round=r1`.
  - Run `TWSS-OWNER-002` with an unknown review status.
  - Run `TWSS-OWNER-003` with `not-started; stage=code-review; round=r1`.
  - Run `TWSS-OWNER-004` with a valid structured value plus prose suffix.
  - Run `TWSS-OWNER-005` with `round=1`.
  - Add negative fixtures for missing, duplicated, and malformed required owner-field labels.
- Expected result:
  - Valid owner fields pass.
  - Unknown status, invalid cross-field combinations, prose suffixes, invalid round tokens, missing labels, duplicate labels, and malformed labels fail closed with file and field diagnostics.
- Failure proves:
  - The owner block is not deterministic enough to be the sole live-state authority.
- Automation location:
  - `scripts/lifecycle_state_sync.py`
  - `scripts/test-artifact-lifecycle-validator.py`

### T13. Final-closeout readiness reason codes are closed and ordered

- Covers: `R46`, `R49`-`R50c`, `E9`, `AC-WSS-020`, `AC-WSS-021`
- Level: unit
- Fixture/setup:
  - Owner-field fixtures under `tests/fixtures/artifact-lifecycle/workflow-state-owner/`.
- Steps:
  - Run `TWSS-REASON-001` with `Final closeout readiness: ready` and sole reason code `ready`.
  - Run `TWSS-REASON-002` with `Final closeout readiness: ready` and `verify-pending`.
  - Run `TWSS-REASON-003` with `Final closeout readiness: not ready` and no reason code.
  - Run `TWSS-REASON-004` with an unknown reason code.
  - Run `TWSS-REASON-005` with duplicate or incorrectly ordered reason codes.
  - Add a positive `not ready` fixture using multiple non-ready codes in normative order.
- Expected result:
  - Readiness and reason code combinations pass only when they use the approved vocabulary, readiness consistency rules, unique codes, and normative ordering.
- Failure proves:
  - Final-closeout readiness can drift through unbounded narrative reason text.
- Automation location:
  - `scripts/lifecycle_state_sync.py`
  - `scripts/test-artifact-lifecycle-validator.py`

### T14. Plan-index table projections compare against named authoritative sources

- Covers: `R53`-`R55b`, `E10`, `EB10`, `AC-WSS-005`, `AC-WSS-022`-`AC-WSS-027`
- Level: integration
- Fixture/setup:
  - `docs/plan.md` fixtures with active and blocked table sections.
  - Plan-body fixtures containing `Plan lifecycle state`, `Change ID`, and `Current Handoff Summary`.
  - Optional governing `change.yaml` fixtures.
- Steps:
  - Run `TWSS-PROJ-001` where `State` matches plan-body lifecycle state.
  - Run `TWSS-PROJ-002` where `State` incorrectly uses current milestone state.
  - Run `TWSS-PROJ-003` where `Next stage` differs from owner `Current Handoff Summary`.
  - Run `TWSS-PROJ-004` where `Change ID` differs from the plan body.
  - Run `TWSS-PROJ-005` where `change.yaml.change_id` differs from the plan body.
  - Run `TWSS-PROJ-006` where an active plan row appears under `Blocked`.
  - Run `TWSS-PROJ-007` with duplicate plan links or duplicate `Change ID` values.
  - Run `TWSS-PROJ-008` with missing plan-body `Change ID`.
- Expected result:
  - Exactly one active or blocked projection row exists per active or blocked plan, table columns are exact, section placement matches lifecycle state, and every projected value matches its named source.
- Failure proves:
  - The plan index remains a narrative or second-owner surface rather than a deterministic projection.
- Automation location:
  - `scripts/lifecycle_state_sync.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path <plan>`

### T15. Readiness pointer and current milestone-state projection stay synchronized

- Covers: `R38`, `R39`, `R51`, `R52`, `R56`, `R57`, `E5`, `E6`, `EB3`, `EB9`, `EB11`, `EC8`, `EC10`, `AC-WSS-004`, `AC-WSS-006`
- Level: integration
- Fixture/setup:
  - Active plan fixtures with current milestone sections and `Readiness`.
  - Historical closed milestone fixtures.
- Steps:
  - Assert current milestone `Milestone state` equals owner `Current milestone state`.
  - Assert previous closed milestones remain historical and are not rewritten by the current projection check.
  - Pass a `Readiness` section containing only a pointer to `Current Handoff Summary` and stable `Readiness is not Done` wording.
  - Fail `Readiness` fixtures that restate live next stage, current review round, current milestone state, or final-readiness value.
- Expected result:
  - Current milestone projection and `Readiness` pointer are accepted only when they mirror or point to the owner without narrative restatement.
- Failure proves:
  - Drift can persist in the two most common live-state mirror surfaces.
- Automation location:
  - `scripts/lifecycle_state_sync.py`
  - `scripts/test-artifact-lifecycle-validator.py`

### T16. State-sync gate is binding at stage handoff, verify, and CI boundaries

- Covers: `R21`-`R28`, `R58`-`R63`, `R84`-`R86`, `E5`, `EB1`, `EB16`, `EC14`
- Level: integration
- Fixture/setup:
  - Lifecycle validation fixtures for a synchronized handoff and a partial transition.
  - Workflow, implement, review, verify, and PR guidance when M4 touches stage skills.
- Steps:
  - Exercise a synchronized implementation-to-review transition with updated owner, milestone projection, plan-index projection, `Readiness`, progress, and validation evidence.
  - Exercise a partial transition where owner changed but projection or pointer surfaces did not.
  - Assert failed state-sync blocks the stage handoff sentence and records the inconsistency or requires reverting the agent's own partial owner/projection edits.
  - Assert verify treats failed state-sync as branch-readiness blocking for touched, referenced, active, or blocked workflow-state artifacts.
  - Assert CI selection includes the same lifecycle state-sync checks when relevant paths are touched.
  - Assert optional local pre-commit hook absence does not change the binding stage, verify, or CI checks.
- Expected result:
  - A synchronized transition passes; a contradictory or partial transition fails before downstream readiness.
- Failure proves:
  - The enforcement mechanism falls back to contributor discipline instead of a binding gate.
- Automation location:
  - `scripts/lifecycle_state_sync.py`
  - `scripts/validate-artifact-lifecycle.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - selector or CI tests when M4 touches validation routing

### T17. Review evidence and change metadata constrain incompatible owner states

- Covers: `R64`-`R72`, including `R65a`, `E8`, `EB4`, `EB5`, `EB12`, `EB13`, `EC9`, `EC11`, `AC-WSS-007`, `AC-WSS-008`, `AC-WSS-012`, `AC-WSS-025`
- Level: integration
- Fixture/setup:
  - Formal review record fixtures with accepted material findings.
  - `review-log.md`, `review-resolution.md`, and `change.yaml` fixtures.
  - Active plan owner-state fixtures.
- Steps:
  - Fail when accepted material findings remain open but owner `Current milestone state` is not `resolution-needed`.
  - Fail when accepted material findings remain open but final-closeout readiness is not `not ready`.
  - Fail when `review-requested` is used while required dispositions remain unresolved.
  - Pass when findings have final dispositions, required validation evidence, no later reopening, and owner routes to rereview rather than downstream gates.
  - Assert the finding-closure summary predicate and closeout-mode review artifact validation agree across negative and positive closeout fixtures.
  - Fail when `change.yaml` unresolved finding count or `change_id` consistency differs from owning review or plan evidence.
  - Fail when a next-stage-like `change.yaml` field acts as competing live next-stage authority.
- Expected result:
  - Review artifacts and derived metadata block incompatible owner states while preserving review-resolution ownership of finding dispositions.
- Failure proves:
  - Downstream readiness can be claimed while review evidence still requires resolution.
- Automation location:
  - `scripts/review_artifact_validation.py`
  - `scripts/change_metadata_semantics.py`
  - `scripts/test-review-artifact-validator.py`
  - `scripts/test-change-metadata-validator.py`
  - `scripts/test-artifact-lifecycle-validator.py`

### T18. Bounded stale-token detection rejects live-surface drift without corrupting history

- Covers: `R73`-`R76`, `EB14`, `EB15`, `EC12`
- Level: unit, integration
- Fixture/setup:
  - Previous owner state and current owner state fixtures.
  - Live-surface fixtures for `Current Handoff Summary`, milestone state, `Readiness`, plan-index row, and compact metadata.
  - Historical ledger fixtures for `Progress`, `review-log.md`, `review-resolution.md`, and review records.
- Steps:
  - Fail when stale prior next stage, milestone state, review round, review result, final-readiness value, or retired lifecycle label appears in a bounded live-state surface after transition.
  - Pass when the same stale-looking token appears only in historical ledgers or review evidence.
  - Assert diagnostics include path, line, expected owner value, and replacement guidance.
  - Assert raw `rg` results are reported only as diagnostics and do not decide gate status.
- Expected result:
  - The validator catches adjacent drift without rewriting or rejecting legitimate history.
- Failure proves:
  - The stale-token check either misses live drift or produces broad false positives against historical evidence.
- Automation location:
  - `scripts/lifecycle_state_sync.py`
  - `scripts/test-artifact-lifecycle-validator.py`

### T19. Enforcement scope preserves historical plans while covering active, blocked, and reopened plans

- Covers: `R81`-`R83`, `R56`, `R57`, `EB2`, `EC8`
- Level: migration
- Fixture/setup:
  - Active, blocked, done, archived, superseded, and reopened plan fixtures.
- Steps:
  - Enforce live projection synchronization for active and blocked plans.
  - Enforce synchronization for any plan whose lifecycle state changes after the contract lands.
  - Enforce synchronization for an archived plan reopened to active.
  - Pass untouched done and archived historical plans without requiring migration solely for this contract.
  - Fail an active applicable plan that lacks `Current Handoff Summary`.
- Expected result:
  - Enforcement applies where lifecycle risk exists and leaves unrelated historical evidence valid.
- Failure proves:
  - Rollout either misses current-risk plans or creates unnecessary historical migration burden.
- Automation location:
  - `scripts/test-artifact-lifecycle-validator.py`

### T20. Optional projection writer is constrained by dry-run, ownership, and golden fixtures

- Covers: `R77`-`R80`, `EC13`
- Level: contract
- Fixture/setup:
  - No writer in the first slice.
  - If a writer is introduced later, hand-authored before/after fixtures for `docs/plan.md`, current milestone state, and `Readiness` pointer.
- Steps:
  - Confirm no first-slice implementation adds writer behavior unless the plan is revised.
  - If present, assert default mode is dry-run.
  - Assert writer can edit only allowed projection and pointer surfaces.
  - Assert writer refuses or leaves unchanged review logs, review records, review-resolution records, validation evidence, finding dispositions, verify evidence, and PR evidence.
  - Assert writer output matches hand-authored golden fixtures, not merely validator pass/fail.
- Expected result:
  - Automatic synchronization cannot silently alter evidence or finding dispositions.
- Failure proves:
  - A projection writer could satisfy its own validator while corrupting workflow evidence.
- Automation location:
  - Future `scripts/test-workflow-state-writer.py` or `scripts/test-artifact-lifecycle-validator.py`
  - Manual changed-file review when no writer exists

### T21. State-sync parser ownership has one implementation path

- Covers: `R84`-`R86`
- Level: contract
- Fixture/setup:
  - `scripts/lifecycle_state_sync.py`
  - `scripts/artifact_lifecycle_validation.py`
  - any dedicated wrapper command if added
- Steps:
  - Assert `validate-artifact-lifecycle.py` composes the shared parser/comparison helper.
  - Assert any dedicated state-sync command imports or delegates to the same helper module.
  - Assert no second parser duplicates `Current Handoff Summary`, `docs/plan.md`, readiness, stale-token, or review-evidence parsing with independently maintained rules.
- Expected result:
  - State-sync has one parser authority and one comparison contract.
- Failure proves:
  - Two validation paths can disagree about the same lifecycle state.
- Automation location:
  - `scripts/test-artifact-lifecycle-validator.py`
  - static import or command-integration checks in M2

### T22. End-to-end workflow-state transition suite and success measurement

- Covers: `R37`-`R87`, `E5`-`E10`, `EB8`-`EB16`, `AC-WSS-001`-`AC-WSS-027`
- Level: e2e, manual
- Fixture/setup:
  - End-to-end fixture pack for implementation-to-review, changes-requested-to-resolution, resolution-to-rereview, clean non-final milestone advance, final closeout, and historical-ledger token retention.
  - Behavior-preservation evidence under `docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/behavior-preservation.md`.
- Steps:
  - Run the end-to-end lifecycle validation fixture suite.
  - Confirm a synchronized transition passes with no manual reviewer repair.
  - Confirm a representative incomplete transition fails before review or downstream handoff.
  - Confirm branch readiness remains owned by verify and PR readiness remains owned by PR.
  - Record post-rollout state-drift findings across proposal-review, plan-review, code-review, verify, and PR handoff for either 10 reviews or 30 days, with partial-window findings treated as coverage or binding defects when drift appears.
- Expected result:
  - The implementation proves the entire workflow-state enforcement slice while preserving stage ownership and historical evidence.
- Failure proves:
  - Individual unit checks do not compose into the intended transition safety gate.
- Automation location:
  - `scripts/test-artifact-lifecycle-validator.py`
  - `scripts/test-review-artifact-validator.py`
  - `scripts/test-change-metadata-validator.py`
  - active plan M5 validation commands
  - manual behavior-preservation evidence

## Fixtures and data

- Existing authored workflow and skill Markdown files are the primary fixtures.
- Test fixtures may be added to existing validator test helpers when needed.
- Workflow-state parser fixtures should live under the existing lifecycle validator fixture tree, grouped by owner parsing, plan-index projection, readiness pointer, review evidence consistency, stale-token boundaries, and historical-plan migration.
- Generated output under `.codex/skills/` and `dist/adapters/` is fixture-like output for drift checks only; do not hand-edit it.
- Change-local artifacts under `docs/changes/2026-05-09-single-source-of-workflow-state/` provide review and validation evidence for this initiative.
- Change-local artifacts under `docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/` provide proposal, spec-review, architecture-review, plan-review, and validation evidence for the enforcement slice.

## Mocking/stubbing policy

- Prefer real repository files and script-level tests over mocks.
- Temporary fixtures inside Python validator tests may be used for isolated positive/negative cases.
- Do not mock generator output when drift checks can run against generated files.

## Migration or compatibility tests

- Historical plans are not migrated unless active, touched, generated, or relied on; verify this by changed-file review.
- Active, blocked, reopened, and lifecycle-changing plans must be normalized before enforcement; untouched done and archived plans remain valid historical records.
- Existing evidence phrases such as `implementation-complete` or `review-clean` may remain as historical descriptions, but new milestone state fields must use the allowed vocabulary.
- Historical stage names, review rounds, and stale-looking next-stage tokens in ledgers and review records must remain valid unless they appear in bounded live-state surfaces.
- Public adapter compatibility is verified through generated adapter drift, adapter validation, and adapter distribution tests.

## Observability verification

- Verify reviewers can locate live planned-initiative state in `Current Handoff Summary`.
- Verify state-sync diagnostics identify owner parse failures, projection mismatches, readiness pointer violations, review-evidence mismatches, and stale live-state tokens with file paths and expected owner values.
- Verify reviewers can locate review finding closeout in `review-resolution.md` when findings exist.
- Verify reviewers can inspect compact status and validation traceability in `change.yaml`.
- Verify validation output names the commands run for touched workflow-state surfaces.

## Security/privacy verification

- Confirm no workflow artifacts add secrets, credentials, tokens, private keys, or machine-local sensitive paths.
- Confirm public skill text does not leak maintainer-only repository internals as downstream user requirements.
- No authentication or authorization behavior changes are expected.

## Performance checks

- No runtime performance checks are required.
- Validation-performance risk is bounded by keeping first-slice checks static and focused.
- State-sync parser checks should operate over bounded sections and exact fields, not whole-repository prose inference.
- Use normal output and bounded-evidence guidance when running validation and reviewing logs.

## Manual QA checklist

- Confirm current state appears once in the active plan `Current Handoff Summary`.
- Confirm other touched artifacts link, summarize, or record scoped evidence instead of owning next-stage state.
- Confirm each implementation milestone moves through targeted validation, code-review, review-resolution when triggered, and closeout before the next milestone.
- Confirm M5 starts only after M1-M4 are closed and required review-resolution is closed.
- Confirm generated output was produced by scripts and not hand-edited.
- Confirm PR handoff, when created, summarizes verified state without creating a new live state owner.
- Confirm `TWSS-OWNER-*`, `TWSS-REASON-*`, and `TWSS-PROJ-*` fixtures exist and exercise both valid and invalid cases.
- Confirm stale-token fixtures include both live-surface rejection and historical-ledger acceptance.
- Confirm review-evidence fixtures cover open, resolved, and reopened material findings.

## What not to test

- Do not add a runtime workflow router or workflow simulator; the approved slice is guidance and static proof.
- Do not migrate or validate every historical plan.
- Do not test UI accessibility because no UI is involved.
- Do not test runtime performance because no runtime behavior changes.
- Do not add broad semantic natural-language scoring for plan state.
- Do not add a projection writer in this first implementation slice.
- Do not test raw repository grep as an authoritative state-sync gate.
- Do not rewrite review evidence, finding dispositions, validation evidence, verify evidence, or PR evidence as part of projection synchronization tests.

## Uncovered gaps

None. Nuanced prose requirements remain covered by manual contract review and existing structural/static validators.

## Next artifacts

- implement M1 after this test spec is active and the active plan handoff is synchronized
- code-review M1 after targeted validation passes

## Follow-on artifacts

None yet.

## Readiness

Active proof surface for M1 implementation. The active plan `Current Handoff Summary` owns the next workflow action.
