# Single Source of Workflow State Test Spec

## Status

- active

## Related spec and plan

- Spec: [Single Source of Workflow State](single-source-of-workflow-state.md), approved.
- Proposal: [Single Source of Workflow State](../docs/proposals/2026-05-09-single-source-of-workflow-state.md), accepted.
- Plan: [Single Source of Workflow State Execution Plan](../docs/plans/2026-05-09-single-source-of-workflow-state.md), active after clean plan-review.
- Architecture: no runtime architecture impact. The approved plan records a no-impact rationale because the change updates workflow contracts, skills, validation checks, generated skill/adapters, and durable artifacts without changing runtime service boundaries, storage, data flow, deployment, security boundaries, or public APIs.
- Project map: `docs/project-map.md` is absent. This test spec does not rely on project-map claims; proof uses the approved spec, active plan, workflow docs, stage skills, generator scripts, and existing validator patterns.
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
| `EB1`-`EB7` | `T5`, `T7`, `T8`, `T9`, `T11` | integration, manual | Boundary/error behavior for stale state, open review-resolution, plan/index drift, and public-skill internals |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| `E1` | `T1`, `T2`, `T4` | Active plan owns next stage; readiness points to summary |
| `E2` | `T3`, `T5`, `T8` | Review-resolution owns closeout, active plan owns milestone state |
| `E3` | `T4`, `T6`, `T8` | Final closeout waits for closed implementation milestones and review-resolution |
| `E4` | `T6`, `T11` | PR handoff closes repo-local state before review; merge is not routine completion event |

## Edge case coverage

- `EC1`: lifecycle-closeout milestone does not count as implementation milestone: `T6`, `T8`
- `EC2`: direct manual skill invocation does not claim full plan state: `T3`, `T7`
- `EC3`: clean review can settle artifact-locally but milestone state owner remains active plan: `T4`, `T8`
- `EC4`: isolated material finding still records review files while stopping handoff: `T3`, `T5`
- `EC5`: true downstream event keeps plan active only when named: `T6`
- `EC6`: public adapter packages use portable concepts: `T9`
- `EC7`: state-sync can be recorded in several places, but live next-stage value stays in current handoff: `T5`, `T8`

## Test cases

### T1. Active plan exposes one live current handoff owner

- Covers: `R1`, `R2`, `E1`
- Level: integration, manual
- Fixture/setup:
  - `docs/workflows.md`
  - `docs/plans/0000-00-00-example-plan.md`
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
  - `docs/plans/0000-00-00-example-plan.md`
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
  - The implementation preserves or reintroduces merge-dependent stale plan state.
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

## Fixtures and data

- Existing authored workflow and skill Markdown files are the primary fixtures.
- Test fixtures may be added to existing validator test helpers when needed.
- Generated output under `.codex/skills/` and `dist/adapters/` is fixture-like output for drift checks only; do not hand-edit it.
- Change-local artifacts under `docs/changes/2026-05-09-single-source-of-workflow-state/` provide review and validation evidence for this initiative.

## Mocking/stubbing policy

- Prefer real repository files and script-level tests over mocks.
- Temporary fixtures inside Python validator tests may be used for isolated positive/negative cases.
- Do not mock generator output when drift checks can run against generated files.

## Migration or compatibility tests

- Historical plans are not migrated unless active, touched, generated, or relied on; verify this by changed-file review.
- Existing evidence phrases such as `implementation-complete` or `review-clean` may remain as historical descriptions, but new milestone state fields must use the allowed vocabulary.
- Public adapter compatibility is verified through generated adapter drift, adapter validation, and adapter distribution tests.

## Observability verification

- Verify reviewers can locate live planned-initiative state in `Current Handoff Summary`.
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
- Use normal output and bounded-evidence guidance when running validation and reviewing logs.

## Manual QA checklist

- Confirm current state appears once in the active plan `Current Handoff Summary`.
- Confirm other touched artifacts link, summarize, or record scoped evidence instead of owning next-stage state.
- Confirm each implementation milestone moves through targeted validation, code-review, review-resolution when triggered, and closeout before the next milestone.
- Confirm M5 starts only after M1-M4 are closed and required review-resolution is closed.
- Confirm generated output was produced by scripts and not hand-edited.
- Confirm PR handoff, when created, summarizes verified state without creating a new live state owner.

## What not to test

- Do not add a runtime workflow router or workflow simulator; the approved slice is guidance and static proof.
- Do not migrate or validate every historical plan.
- Do not test UI accessibility because no UI is involved.
- Do not test runtime performance because no runtime behavior changes.
- Do not add broad semantic natural-language scoring for plan state.

## Uncovered gaps

None. Nuanced prose requirements remain covered by manual contract review and existing structural/static validators.

## Next artifacts

- implement M1 after this test spec is active
- code-review M1 after targeted validation passes

## Follow-on artifacts

None yet.

## Readiness

Active proof surface for M1 implementation. The active plan `Current Handoff Summary` owns the next workflow action.
