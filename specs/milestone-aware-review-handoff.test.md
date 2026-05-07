# Milestone-Aware Review Handoff Test Spec

## Status

- active

## Related spec and plan

- Spec: [Milestone-Aware Review Handoff](milestone-aware-review-handoff.md), approved.
- Proposal: [Milestone-Aware Review Handoff](../docs/proposals/2026-05-07-milestone-aware-review-handoff.md), accepted.
- Plan: [Milestone-Aware Review Handoff Execution Plan](../docs/plans/2026-05-07-milestone-aware-review-handoff.md), active after clean plan-review rerun.
- Architecture: not required. The approved first slice is guidance and static wording checks only, with no executable routing, storage, API, deployment, parser, or runtime validation boundary.
- Project map: `docs/project-map.md` is absent. This test spec does not rely on project-map claims; proof uses the approved spec, active plan, workflow specs, stage skills, workflow docs, generator scripts, and existing static validator patterns.
- Related workflow proof surfaces:
  - [Workflow stage autoprogression test spec](workflow-stage-autoprogression.test.md)
  - [RigorLoop workflow test spec](rigorloop-workflow.test.md)
  - `scripts/test-skill-validator.py`
  - `scripts/select-validation.py`
  - `scripts/build-skills.py`
  - `scripts/build-adapters.py`
  - `scripts/validate-skills.py`
  - `scripts/validate-adapters.py`
  - `scripts/ci.sh`

## Testing strategy

- Use contract and static wording checks because the approved first slice is guidance-driven and does not add a workflow router or executable plan-state validator.
- Use `scripts/test-skill-validator.py` for stable, machine-checkable invariants in authored skills and workflow guidance.
- Use the related workflow test specs to keep the broader autoprogression and lifecycle contract aligned with the milestone-aware amendment.
- Use selector validation to prove changed paths choose the expected repo-owned validation families.
- Use generated-output drift checks after canonical skill edits to prove `.codex/skills/` and public adapter skill copies are derived from authored `skills/`.
- Use manual contract review for nuanced prose requirements such as no milestone postponement, lifecycle-closeout distinction, and preserving isolated-stage behavior.
- Do not add executable plan-state parsing, workflow simulation, or a standalone `review-resolution` skill in this first implementation slice.

## Requirement coverage map

| Requirement IDs | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `R1`, `R1a`, `R1b`, `R10`, `R10a` | `T1`, `T3`, `T10` | manual, integration | Scope boundary, unchanged lanes, and preserved downstream gates |
| `R2`, `R2a`, `R2b`, `R2c` | `T5` | integration, manual | Single milestone state vocabulary and evidence-only terms |
| `R3`, `R3a`, `R3b` | `T6` | integration, manual | `implement` transitions and no implement-owned verify readiness |
| `R4`, `R4a`, `R4b`, `R4c`, `R4d` | `T2`, `T4`, `T7` | integration, manual | Reviewed milestone identification, final/non-final routing, and plan update requirements |
| `R5`, `R5a`, `R5b`, `R5c`, `R5d`, `R5e` | `T3`, `T7` | integration, manual | Same-milestone findings, fix loop, re-review, and owner-decision stops |
| `R6`, `R6a`, `R6b` | `T4` | integration, manual | Inconclusive review behavior and missing-evidence output |
| `R7`, `R7a`, `R7b` | `T8` | manual | Plan revision before removing milestones from scope |
| `R8`, `R8a`, `R8b`, `R8c`, `R8d` | `T2`, `T3`, `T7` | integration, manual | Current handoff summary fields and verify-readiness reasons |
| `R9`, `R9a`, `R9b` | `T9` | manual, integration | Lifecycle-closeout distinction and mixed milestone handling |
| `R11`, `R11a`, `R11b` | `T11` | integration, manual | Static-only first slice and no standalone review-resolution skill |

## Acceptance criteria coverage

| Acceptance criterion | Covered by |
| --- | --- |
| `AC1` | `T2`, `T10` |
| `AC2` | `T2`, `T10` |
| `AC3` | `T5` |
| `AC4` | `T5` |
| `AC5` | `T3`, `T6`, `T7`, `T9`, `T10` |
| `AC6` | `T5`, `T10`, `T11` |
| `AC7` | `T10`, `T12` |
| `AC8` | `T10`, `T12` |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| `E1` | `T2`, `T7` | Clean non-final milestone closes and routes to `implement <next milestone>` |
| `E2` | `T2`, `T7` | Clean final milestone closes and routes to `verify` |
| `E3` | `T3`, `T7` | Findings keep the workflow on the same milestone |
| `E4` | `T4` | Ambiguous remaining milestones block verify |
| `E5` | `T8` | Removed milestone requires plan revision before handoff |
| `E6` | `T9` | Lifecycle-closeout milestone does not block verify |

## Edge case coverage

- `EC1`: clean non-final milestone review: `T2`, `T7`
- `EC2`: clean final milestone review: `T2`, `T7`
- `EC3`: review findings on a non-final milestone: `T3`, `T7`
- `EC4`: accepted fixes requiring re-review: `T3`
- `EC5`: findings closed without re-review when explicitly allowed: `T3`
- `EC6`: inconclusive review due to missing evidence: `T4`
- `EC7`: ambiguous remaining implementation milestones: `T4`
- `EC8`: milestone removed from current scope: `T8`
- `EC9`: lifecycle-closeout milestone after final implementation milestone: `T9`
- `EC10`: mixed implementation and lifecycle-closeout milestone: `T9`
- `EC11`: isolated direct `code-review`: `T1`
- `EC12`: explicit user pause after clean milestone review: `T1`, `T7`
- `EC13`: stage cannot edit the active plan: `T7`
- `EC14`: existing untouched plan lacks new handoff summary: `T14`

## Test cases

### T1. Scope boundary preserves existing lanes and stop conditions

- Covers: `R1`, `R1a`, `R1b`, `R10`, `R10a`, `EC11`, `EC12`
- Level: manual
- Fixture/setup:
  - `specs/milestone-aware-review-handoff.md`
  - `specs/workflow-stage-autoprogression.md`
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `skills/workflow/SKILL.md`
  - `skills/code-review/SKILL.md`
- Steps:
  - Review normative and operating workflow surfaces after implementation.
  - Confirm milestone-aware routing applies only to workflow-managed full-feature execution with a milestone-based active plan.
  - Confirm isolated `code-review`, isolated `verify`, review-only, fast-lane, bugfix, direct `pr`, merge, release, deploy, and destructive actions keep their existing behavior.
  - Confirm explicit user pauses report the correct next stage and stop before entering it.
- Expected result:
  - The milestone-aware rule narrows full-feature milestone routing without widening default autoprogression.
- Failure proves:
  - The change broadened the lifecycle contract beyond the approved spec or weakened existing stop conditions.
- Automation location:
  - Manual review during M2 and M3.

### T2. Clean review routing distinguishes non-final and final milestones

- Covers: `R4`, `R4a`, `R4b`, `R4c`, `R8b`, `R8c`, `AC1`, `AC2`, `E1`, `E2`, `EC1`, `EC2`
- Level: integration, manual
- Fixture/setup:
  - `specs/workflow-stage-autoprogression.md`
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `skills/code-review/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `scripts/test-skill-validator.py`
- Steps:
  - Add static assertions that a clean non-final milestone review closes the reviewed milestone and routes to `implement <next in-scope implementation milestone>`.
  - Add static assertions that a clean final milestone review closes the reviewed milestone and routes to `verify`.
  - Search affected guidance for unconditional `clean-with-notes -> verify` or equivalent wording and either remove it or qualify it as final-milestone-only.
  - Manually confirm the handoff examples preserve the non-final and final split.
- Expected result:
  - No changed authoritative surface implies that a clean review of `M1` in a multi-milestone plan is enough for `verify`.
- Failure proves:
  - The original workflow bug remains.
- Automation location:
  - `scripts/test-skill-validator.py`
  - `specs/workflow-stage-autoprogression.test.md`
  - `specs/rigorloop-workflow.test.md`

### T3. Findings stay attached to the reviewed milestone

- Covers: `R5`, `R5a`, `R5b`, `R5c`, `R5d`, `R5e`, `R8d`, `R10a`, `E3`, `EC3`, `EC4`, `EC5`
- Level: integration, manual
- Fixture/setup:
  - `specs/milestone-aware-review-handoff.md`
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `skills/code-review/SKILL.md`
  - `skills/implement/SKILL.md`
  - `skills/plan/SKILL.md`
  - `scripts/test-skill-validator.py`
- Steps:
  - Assert that review findings requiring resolution transition the reviewed milestone to `resolution-needed`.
  - Assert that the next stage is review-resolution for that same milestone.
  - Assert that accepted fixes stay on the same milestone and return to `review-requested` before rerun review when re-review is required.
  - Confirm `needs-decision` or unresolved findings block the next implementation milestone, `verify`, final `explain-change`, and `pr`.
- Expected result:
  - Findings, fixes, disposition, and re-review cannot leak into the next milestone until the reviewed milestone is closed or explicitly deferred by the governing review contract.
- Failure proves:
  - Required review-resolution can be skipped, detached from the reviewed milestone, or hidden behind later work.
- Automation location:
  - `scripts/test-skill-validator.py`
  - manual contract review during M2 and M3.

### T4. Inconclusive or ambiguous review never hands off to verify

- Covers: `R4d`, `R6`, `R6a`, `R6b`, `E4`, `EC6`, `EC7`
- Level: integration, manual
- Fixture/setup:
  - `skills/code-review/SKILL.md`
  - `skills/plan/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `docs/workflows.md`
  - `scripts/test-skill-validator.py`
- Steps:
  - Assert code-review guidance requires the reviewed milestone to be identifiable.
  - Assert ambiguous remaining implementation milestones require a plan update or `inconclusive` result.
  - Assert inconclusive review leaves the milestone at `review-requested` unless a stronger stop condition applies.
  - Confirm the output names missing evidence or required plan updates instead of routing to `verify`.
- Expected result:
  - Missing review evidence or ambiguous plan state blocks verify readiness.
- Failure proves:
  - The workflow can infer finality from insufficient evidence.
- Automation location:
  - `scripts/test-skill-validator.py`
  - manual review during M3.

### T5. Milestone state vocabulary is single-field and exact

- Covers: `R2`, `R2a`, `R2b`, `R2c`, `AC3`, `AC4`
- Level: integration, manual
- Fixture/setup:
  - `specs/milestone-aware-review-handoff.md`
  - `specs/workflow-stage-autoprogression.md`
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/plan/SKILL.md`
  - `scripts/test-skill-validator.py`
- Steps:
  - Assert the only allowed `Milestone state` values are `planned`, `implementing`, `review-requested`, `resolution-needed`, and `closed`.
  - Assert the guidance does not introduce a parallel routing state or implementation evidence state.
  - Assert `implementation-complete` and `review-clean` are described only as evidence phrases, not milestone state values.
  - Manually confirm any evidence fields remain subordinate to the single state field.
- Expected result:
  - Contributors and agents have one authoritative milestone state field.
- Failure proves:
  - The state model can drift back into ambiguous parallel state machines.
- Automation location:
  - `scripts/test-skill-validator.py`
  - manual review during M2 and M3.

### T6. Implement handoff uses `review-requested` and does not claim verify readiness

- Covers: `R3`, `R3a`, `R3b`, `AC5`
- Level: integration, manual
- Fixture/setup:
  - `skills/implement/SKILL.md`
  - `skills/plan/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `docs/workflows.md`
  - `scripts/test-skill-validator.py`
- Steps:
  - Assert `implement` transitions a started milestone from `planned` to `implementing`.
  - Assert post-implementation handoff transitions the milestone to `review-requested` after targeted validation passes.
  - Assert `implement` records targeted validation evidence and hands off to `code-review` for that milestone.
  - Assert `implement` does not set the whole plan to `Ready for verify` while any implementation milestone remains unreviewed, unresolved, or open.
- Expected result:
  - Implementation completion creates review handoff evidence, not milestone closeout or whole-plan verify readiness.
- Failure proves:
  - The implementation stage can prematurely route a multi-milestone plan to verify.
- Automation location:
  - `scripts/test-skill-validator.py`
  - manual review during M3.

### T7. Handoff summaries and plan update obligations are explicit

- Covers: `R4d`, `R8`, `R8a`, `R8b`, `R8c`, `R8d`, `AC5`, `E1`, `E2`, `E3`, `EC13`
- Level: integration, manual
- Fixture/setup:
  - `skills/code-review/SKILL.md`
  - `skills/plan/SKILL.md`
  - `skills/workflow/SKILL.md`
  - active plan examples in `docs/plans/`
  - `scripts/test-skill-validator.py`
- Steps:
  - Assert plan and review output guidance require current milestone, current milestone state, last reviewed milestone, review status, remaining in-scope implementation milestones, next stage, verify readiness, and reason.
  - Assert a clean non-final handoff names remaining milestones and says verify is not ready.
  - Assert a clean final handoff says verify is ready because all in-scope implementation milestones are closed and code-review is complete.
  - Assert a findings handoff says verify is not ready because review findings remain unresolved or require owner decision.
  - Assert a stage that cannot edit the plan explicitly requires the plan update before downstream routing relies on the state.
- Expected result:
  - The active plan or stage output always exposes why the next stage is next and whether verify is available.
- Failure proves:
  - Downstream stages can rely on stale or unstated milestone status.
- Automation location:
  - `scripts/test-skill-validator.py`
  - manual plan review during M3 and M4.

### T8. Milestones are not postponed to reach verify

- Covers: `R7`, `R7a`, `R7b`, `E5`, `EC8`
- Level: manual
- Fixture/setup:
  - `specs/milestone-aware-review-handoff.md`
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `skills/plan/SKILL.md`
  - `skills/code-review/SKILL.md`
- Steps:
  - Review workflow and planning guidance after implementation.
  - Confirm a listed implementation milestone cannot be skipped solely to make `verify` available.
  - Confirm a milestone removed from scope requires plan revision before next-stage routing relies on that removal.
  - Confirm verify may proceed after revision only when no in-scope implementation milestone remains open or unresolved.
- Expected result:
  - Scope changes are explicit plan changes, not hidden routing decisions.
- Failure proves:
  - Milestone-aware handoff can be bypassed by silently reclassifying or postponing work.
- Automation location:
  - Manual review during M2 and M3.

### T9. Lifecycle-closeout milestones are distinguishable from implementation milestones

- Covers: `R9`, `R9a`, `R9b`, `AC5`, `E6`, `EC9`, `EC10`
- Level: manual, integration
- Fixture/setup:
  - `skills/plan/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `docs/workflows.md`
  - `specs/rigorloop-workflow.md`
  - `scripts/test-skill-validator.py`
- Steps:
  - Assert guidance names `lifecycle-closeout` for downstream gates such as `verify`, `explain-change`, and PR handoff.
  - Confirm lifecycle-closeout work does not block entry into `verify` after all implementation milestones are closed.
  - Confirm a mixed milestone that still contains implementation work remains an implementation milestone for verify-readiness decisions.
- Expected result:
  - Verify readiness is based on open implementation work, not on the existence of downstream lifecycle gates.
- Failure proves:
  - Plans can either block verify incorrectly or hide real implementation work in closeout language.
- Automation location:
  - `scripts/test-skill-validator.py`
  - manual review during M2 and M3.

### T10. Affected workflow, skill, and generated surfaces remain aligned

- Covers: `R1`-`R11b`, `AC1`, `AC2`, `AC5`, `AC6`, `AC7`, `AC8`
- Level: integration, smoke, manual
- Fixture/setup:
  - authored workflow specs and test specs touched by this initiative
  - `docs/workflows.md`
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/plan/SKILL.md`
  - `skills/workflow/SKILL.md`
  - generated `.codex/skills/` mirrors for changed skills
  - generated public adapter skill copies under `dist/adapters/`
- Steps:
  - Run skill validation and focused skill-validator assertions.
  - Regenerate canonical skill mirrors and adapter packages after authored skill changes.
  - Run generated-output drift checks.
  - Run selected CI over touched workflow, skill, test-spec, generated, plan, and change-local paths.
  - Manually inspect generated diffs for expected skill-content propagation only.
- Expected result:
  - Authored and generated workflow guidance agree on the milestone-aware handoff rule.
- Failure proves:
  - Contributors using different adapters or local Codex mirrors can receive stale routing guidance.
- Automation location:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `bash scripts/ci.sh --mode explicit ...` with the paths named in the active plan.

### T11. First implementation slice stays static-only

- Covers: `R11`, `R11a`, `R11b`, `AC6`
- Level: integration, manual
- Fixture/setup:
  - `scripts/test-skill-validator.py`
  - `skills/`
  - `specs/`
  - `docs/workflows.md`
  - active plan changed-file list
- Steps:
  - Confirm no executable plan-state validation, semantic plan parser, or runtime workflow simulator is added in this slice.
  - Confirm no standalone `skills/review-resolution/SKILL.md` is added.
  - Confirm static checks operate on wording, stable headings, required terms, forbidden stale terms, and generated drift only.
  - Review changed paths before code-review to ensure no hidden runtime enforcement surface was introduced.
- Expected result:
  - The first slice proves and updates guidance without adding an unapproved enforcement mechanism.
- Failure proves:
  - The implementation exceeds the approved first-slice scope.
- Automation location:
  - `scripts/test-skill-validator.py`
  - `test ! -e skills/review-resolution/SKILL.md`
  - manual changed-file review before code-review.

### T12. Validation selector accepts concrete generated adapter paths

- Covers: `AC7`, `AC8`
- Level: integration
- Fixture/setup:
  - public adapter skill copies for `implement`, `code-review`, `plan`, and `workflow`
- Steps:
  - Run selector validation with every changed generated adapter skill file path, not the directory `dist/adapters`.
  - Confirm selector output has no `unclassified_paths`.
- Expected result:
  - Explicit validation scope is precise enough for generated adapter output.
- Failure proves:
  - The validation plan can hide generated adapter drift behind an unclassified directory path.
- Automation location:
  - `python scripts/select-validation.py --mode explicit --path dist/adapters/codex/.agents/skills/implement/SKILL.md --path dist/adapters/codex/.agents/skills/code-review/SKILL.md --path dist/adapters/codex/.agents/skills/plan/SKILL.md --path dist/adapters/codex/.agents/skills/workflow/SKILL.md --path dist/adapters/claude/.claude/skills/implement/SKILL.md --path dist/adapters/claude/.claude/skills/code-review/SKILL.md --path dist/adapters/claude/.claude/skills/plan/SKILL.md --path dist/adapters/claude/.claude/skills/workflow/SKILL.md --path dist/adapters/opencode/.opencode/skills/implement/SKILL.md --path dist/adapters/opencode/.opencode/skills/code-review/SKILL.md --path dist/adapters/opencode/.opencode/skills/plan/SKILL.md --path dist/adapters/opencode/.opencode/skills/workflow/SKILL.md`

### T13. Handoff summaries do not expose sensitive data

- Covers: security/privacy requirement
- Level: manual, smoke
- Fixture/setup:
  - changed Markdown, skill, generated, and change-local files
- Steps:
  - Review changed handoff examples, plan updates, review outputs, validation notes, and generated skill copies.
  - Confirm no secrets, credentials, tokens, private keys, or host-specific sensitive data are introduced.
- Expected result:
  - Workflow evidence remains contributor-visible without leaking sensitive data.
- Failure proves:
  - The new handoff summaries or validation notes created a disclosure risk.
- Automation location:
  - Manual review during M4 and final verify.

### T14. Compatibility expectations remain true for existing plans

- Covers: compatibility and migration, `EC14`
- Level: manual
- Fixture/setup:
  - `specs/milestone-aware-review-handoff.md`
  - `docs/workflows.md`
  - `skills/plan/SKILL.md`
  - existing untouched plan files under `docs/plans/`
- Steps:
  - Confirm guidance says existing untouched plans are not invalid solely because they lack the new handoff summary or state vocabulary.
  - Confirm touched or newly relied-on milestone-based plans adopt the single-state vocabulary and current handoff summary when milestone readiness changes.
  - Confirm lifecycle-closeout guidance remains valid when it distinguishes downstream gates from implementation milestones.
- Expected result:
  - Adoption is forward-compatible for touched or relied-on plans without forcing a repository-wide historical plan migration.
- Failure proves:
  - The change unintentionally requires broad migration or weakens lifecycle-closeout compatibility.
- Automation location:
  - Manual review during M2, M3, and final verify.

## Fixtures and data

- No runtime fixtures are required.
- The proof uses real repository Markdown, authored skill files, generated skill output, and repo-owned validation scripts.
- Adapter-path selector validation must use the concrete generated skill file paths named in `T12`.

## Mocking/stubbing policy

- Do not mock workflow state, generated output, selector behavior, or validation commands.
- Use the repository's actual files and scripts as the proof surface.
- Do not introduce synthetic plan-state fixtures for executable parsing in this first slice.

## Migration or compatibility tests

- `T1` proves unchanged lanes and stop conditions.
- `T8` proves planned milestones cannot be silently postponed to reach verify.
- `T9` proves lifecycle-closeout milestones do not behave like implementation milestones.
- `T14` proves existing untouched plans are not made invalid solely by lacking the new summary fields.

## Observability verification

- `T7` verifies that milestone handoff summaries expose the current milestone, current milestone state, last reviewed milestone, review status, remaining implementation milestones, next stage, verify readiness, and reason.
- `T6` verifies implement output and plan updates expose targeted validation evidence and `review-requested` handoff.
- `T2` and `T3` verify code-review output exposes clean-review closeout or findings-driven `resolution-needed` routing.

## Security/privacy verification

- `T13` verifies changed handoff summaries and workflow evidence do not include secrets, credentials, tokens, private keys, or host-specific sensitive data.
- No authentication, authorization, encryption, retention, or external data exposure behavior changes are expected.

## Performance checks

- No runtime performance behavior is involved.
- `T11` verifies the first slice does not add executable plan-state validation, semantic plan parsing, or runtime workflow simulation that could introduce new validation-runtime cost.

## Manual QA checklist

- Confirm non-final clean milestone review routes to `implement <next milestone>`, not `verify`.
- Confirm final clean milestone review routes to `verify`.
- Confirm findings route to same-milestone review-resolution and block next milestone/verify until resolved or explicitly deferred under the governing review contract.
- Confirm inconclusive or ambiguous review state blocks verify and names missing evidence or required plan update.
- Confirm allowed `Milestone state` values are exactly `planned`, `implementing`, `review-requested`, `resolution-needed`, and `closed`.
- Confirm `implementation-complete` and `review-clean` are not milestone state values.
- Confirm no standalone `review-resolution` skill or executable plan-state validator was added.
- Confirm generated `.codex/skills/` and public adapter skill copies are refreshed from canonical skills after authored skill changes.

## What not to test

- Do not test an executable workflow router; none is approved or implemented in this slice.
- Do not test semantic plan-state parsing or a plan-state validator; `R11a` forbids adding that in the first slice.
- Do not add or test a standalone `review-resolution` skill; `R11b` forbids adding it.
- Do not simulate live PR opening, merge, release, deployment, tag publication, or destructive Git actions.
- Do not require every historical plan under `docs/plans/` to migrate to the new summary format.
- Do not introduce plan-template or example-plan tests in this first slice.

## Uncovered gaps

None. If implementation discovers that guidance-only static proof cannot satisfy an approved requirement, return to `spec-review` instead of adding unapproved runtime enforcement.

## Next artifacts

- `implement M1`: add or update static proof surfaces before canonical workflow guidance changes.
- `code-review M1` after M1 implementation handoff.
- Continue the milestone loop defined in the active plan until all in-scope implementation milestones are closed.

## Follow-on artifacts

None yet.

## Readiness

Status: Active.

Progress: proposal is accepted, spec is approved, plan-review is approved, and this matching test spec is active.

Readiness: Active proof surface for `implement M1`.

Remaining completion gates: implement M1, code-review M1, review-resolution if triggered, implement and review M2-M4, final verify after all in-scope implementation milestones are closed, explain-change, PR handoff, and Done if no true downstream event remains.
