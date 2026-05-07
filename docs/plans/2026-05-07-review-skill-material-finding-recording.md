# Review Skill Material Finding Recording Execution Plan

## Status

- active
- Owner: maintainers
- Start date: 2026-05-07
- Last updated: 2026-05-07
- Related issue or PR: none yet
- Supersedes: none
- selected_workflow_contract: refactored
- broad_smoke_required: false
- broad_smoke_reason: This initiative changes workflow-governance artifacts, review skill guidance, structural/static validation, templates, generated skill mirrors, and generated adapter packages. It does not add runtime data flow, storage, network boundaries, deployment behavior, release packaging, schemas, or external integrations that require repository broad smoke by default.

## Purpose / Big Picture

Implement the accepted review skill material-finding recording clarification across all formal review skills.

The implementation must make the simple rule operational and hard to drift:

- every material finding is recorded;
- all material findings require change-local review files;
- isolation stops handoff, not recording.

The work also makes new `review-resolution.md` records easier to scan while keeping the validator-readable per-finding fields required for closeout.

## Source Artifacts

- Proposal: [Review Skill Material Finding Recording](../proposals/2026-05-07-review-skill-material-finding-recording.md), accepted.
- Spec: [Formal Review Recording](../../specs/formal-review-recording.md), approved on 2026-05-07 after clean direct `spec-review`.
- Spec: [Review Finding Resolution Contract](../../specs/review-finding-resolution-contract.md), approved on 2026-05-07 after clean direct `spec-review`.
- Spec: [RigorLoop Workflow](../../specs/rigorloop-workflow.md), approved on 2026-05-07 after clean direct `spec-review`.
- Architecture: not required. The approved work reuses the existing `docs/changes/<change-id>/reviews/`, `review-log.md`, `review-resolution.md`, skill generation, adapter generation, and structural validation boundaries. No new storage model, parser architecture, external service, runtime boundary, deployment boundary, or adapter architecture is introduced.
- Test specs: [Formal Review Recording test spec](../../specs/formal-review-recording.test.md), [Review Finding Resolution Contract test spec](../../specs/review-finding-resolution-contract.test.md), and [RigorLoop Workflow test spec](../../specs/rigorloop-workflow.test.md), updated on 2026-05-07 after clean `plan-review`.
- Project map: `docs/project-map.md` is absent. No-map rationale: this plan does not rely on repository-map claims for architecture, runtime flow, data flow, or ownership. Orientation comes from governing specs, proposal, current skill sources, validation scripts, generated-output scripts, and existing review artifact tests.
- Review records: [review log](../changes/2026-05-07-review-skill-material-finding-recording/review-log.md), [review resolution](../changes/2026-05-07-review-skill-material-finding-recording/review-resolution.md), and detailed review records under `docs/changes/2026-05-07-review-skill-material-finding-recording/reviews/`.

## Context and Orientation

- Canonical authored skills live under `skills/`. Generated Codex runtime mirrors under `.codex/skills/` and public adapter packages under `dist/adapters/` must be refreshed through generators, not hand-edited.
- The five formal review skills are `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, and `code-review`.
- The accepted proposal requires a manually copied shared subsection, with `templates/shared/review-isolation-and-recording.md` as the canonical source and byte-equality checks across the five formal review skills.
- `code-review` adopts the shared rule without an additive code-review-specific layer for this concern.
- The first implementation slice keeps validator coverage structural/static. Semantic detection of tracked edits that reference unresolved review findings remains deferred.
- Existing `scripts/test-review-artifact-validator.py` already covers many review artifact relationships, including upstream stages and no-material detailed records. This initiative tightens coverage for the new shared block and scan-first review-resolution contract rather than replacing the parser model.
- `docs/workflows.md`, `AGENTS.md`, `CONSTITUTION.md`, and the governing specs already contain the simplified broad trigger from the spec amendment. Implementation should keep them aligned if test-spec or plan-review identifies a wording gap.

## Non-Goals

- Do not make isolated reviews auto-continue into downstream stages.
- Do not require detailed review files for clean reviews with no material findings when no detailed-record trigger applies.
- Do not create a dedicated `pr-review` stage.
- Do not copy every maintainer PR comment into `docs/changes/`.
- Do not make `review-resolution.md` a transcript of every review comment.
- Do not replace artifact-local proposal, spec, architecture, ADR, plan, or code-review status.
- Do not introduce a generation step for the shared review-skill subsection.
- Do not add semantic review-quality automation or semantic edit-reference flagging in this slice.
- Do not treat the initial review-record root as sufficient final handoff for non-trivial work.
- Do not hand-edit generated `.codex/skills/` or `dist/adapters/` output.
- Do not migrate historical review records unless touched, generated, or relied on as current guidance.

## Requirements Covered

| Requirement IDs | Planned implementation surface |
| --- | --- |
| `formal-review-recording` `R2`-`R5a`, `R17`-`R20c`, `R22`-`R23` | formal review skill shared subsection, workflow guidance alignment, static assertions, and isolated material-review final-output guidance |
| `formal-review-recording` `R4`-`R4g`, `R8`-`R16b`, edge cases 1-17 | review artifact validator tests, change-local review record examples, no-material detailed record behavior, and unsupported `pr-review` boundary |
| `formal-review-recording` `R21`-`R21d` | `templates/shared/review-isolation-and-recording.md`, copied blocks in all five formal review skills, and byte-equality/placement assertions |
| `review-finding-resolution-contract` `R1`-`R6m`, `R8d`-`R8h`, `R11`, edge cases 26-29 | scan-first `review-resolution.md` template/guidance, closeout validator regression coverage, and proof that parseable finding labels remain required |
| `rigorloop-workflow` `R12a`-`R12c`, `R12an`-`R12bg` | workflow contract alignment, skill guidance, generated outputs, and downstream blocking behavior |
| Governance guidance in `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md` | concise contributor-facing rule: every material finding is recorded, all material findings require change-local review files, isolation stops handoff rather than recording |

## Immediate Test-Spec Handoff

Plan-review approved this plan on 2026-05-07 with no material findings.

The matching test specs now define exact assertions for:

- the canonical shared block source;
- byte-equality across the five formal review skills;
- placement of stage-specific guidance outside the shared block;
- isolated material-review output fields;
- material-finding broad trigger wording;
- no-material lightweight settlement;
- scan-first `review-resolution.md` structure;
- preservation of validator-readable per-finding labels;
- generated skill and adapter drift checks.

Implementation should proceed test-first within each milestone.

## Aggregate Implementation Slice

Owner direction on 2026-05-07 replans the original M1, M2, and M3 as one explicit aggregate implementation slice.

The M1, M2, and M3 sections below remain as sub-slice detail for review and traceability. Their individual milestone closeout checklists are superseded by this aggregate closeout boundary because the M1 proof assertions are intentionally green only after the M2 canonical guidance and M3 generated output exist.

The aggregate closeout commit will use the milestone-formatted subject:

```text
M1: implement review recording proof and guidance
```

The commit body must name the aggregate scope:

- former M1: proof map and static validator coverage;
- former M2: shared review guidance and scan-first `review-resolution.md` guidance;
- former M3: generated Codex skill and public adapter output refresh.

The aggregate closeout is complete only when validation passes, progress and validation notes are current, the aggregate commit exists, and code-review is rerun against the committed aggregate slice.

## Milestones

### M1. Define Proof Map and Static Validator Coverage

- Goal: Add the concrete tests and static assertions that will enforce the shared review-recording rule before changing skill text.
- Requirements: `formal-review-recording` `R17`-`R23`, `review-finding-resolution-contract` `R11`, `rigorloop-workflow` `R12be`-`R12bf`.
- Files/components likely touched:
  - `specs/formal-review-recording.test.md`
  - `specs/review-finding-resolution-contract.test.md`
  - `specs/rigorloop-workflow.test.md`
  - `scripts/test-skill-validator.py`
  - `scripts/test-review-artifact-validator.py`
  - `docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml`
  - this plan
- Dependencies:
  - plan-review approval
  - matching test-spec completed before implementation
- Tests to add/update:
  - Static assertion that `templates/shared/review-isolation-and-recording.md` exists and is the canonical source.
  - Byte-equality assertion from the `## Isolation and Recording` heading through the next `##` boundary across `skills/proposal-review/SKILL.md`, `skills/spec-review/SKILL.md`, `skills/architecture-review/SKILL.md`, `skills/plan-review/SKILL.md`, and `skills/code-review/SKILL.md`.
  - Placement assertion that stage-specific guidance does not appear inside the shared block.
  - Static assertions for the broad rule and isolated material-review output fields.
  - Review-resolution fixture or static coverage for a scan-first summary, overview table, shared validation evidence, closeout checklist, and per-finding parseable labels.
- Implementation steps:
  - Update the matching test specs after plan-review to map each new `MUST` to a proof surface.
  - Add focused tests before changing canonical skill/template prose.
  - Keep tests structural/static; do not add semantic review-quality judgment.
  - Reuse existing review artifact validator tests for review-log and review-resolution relationships where possible.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/select-validation.py --mode explicit --path specs/formal-review-recording.test.md --path specs/review-finding-resolution-contract.test.md --path specs/rigorloop-workflow.test.md --path scripts/test-skill-validator.py --path scripts/test-review-artifact-validator.py`
  - `bash scripts/ci.sh --mode explicit --path specs/formal-review-recording.test.md --path specs/review-finding-resolution-contract.test.md --path specs/rigorloop-workflow.test.md --path scripts/test-skill-validator.py --path scripts/test-review-artifact-validator.py --path docs/plans/2026-05-07-review-skill-material-finding-recording.md --path docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml`
  - `git diff --check -- specs/formal-review-recording.test.md specs/review-finding-resolution-contract.test.md specs/rigorloop-workflow.test.md scripts/test-skill-validator.py scripts/test-review-artifact-validator.py docs/plans/2026-05-07-review-skill-material-finding-recording.md docs/changes/2026-05-07-review-skill-material-finding-recording`
- Expected observable result: tests fail against missing or mismatched shared review-skill recording guidance and against non-scan-first review-resolution guidance.
- Aggregate closeout: superseded by `Aggregate Implementation Slice`.
- Risks:
  - Byte-equality tests can be brittle if the extraction boundary is ambiguous.
  - Scan-first tests can overfit Markdown decoration instead of the required durable fields.
- Rollback/recovery:
  - Revert brittle assertions and replace them with stable heading-boundary, field-label, and table-presence checks mapped to the approved test spec.

### M2. Add Shared Review Guidance and Scan-First Review-Resolution Template

- Goal: Implement the canonical shared review-skill subsection and reusable scan-first review-resolution guidance in authored source files.
- Requirements: `formal-review-recording` `R17`-`R22b`, `review-finding-resolution-contract` `R5`-`R6m`, `R11`, `rigorloop-workflow` `R12bd`-`R12bf`.
- Files/components likely touched:
  - `templates/shared/review-isolation-and-recording.md`
  - `templates/review-resolution.md` or another approved durable guidance surface for scan-first review resolution
  - `skills/proposal-review/SKILL.md`
  - `skills/spec-review/SKILL.md`
  - `skills/architecture-review/SKILL.md`
  - `skills/plan-review/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/explain-change/SKILL.md`
  - `skills/pr/SKILL.md`
  - `docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml`
  - this plan
- Dependencies:
  - M1 tests in place
- Tests to add/update:
  - Adjust M1 assertions only if canonical guidance reveals a missing proof obligation.
- Implementation steps:
  - Create the canonical `templates/shared/review-isolation-and-recording.md` block from the accepted proposal.
  - Copy the block verbatim into all five formal review skills.
  - Keep stage-specific review guidance above or below the shared block.
  - Remove any formal review-skill wording that implies isolation suppresses recording.
  - Ensure `code-review` does not introduce a special local exception for this concern.
  - Add scan-first `review-resolution.md` template or guidance with summary, overview table, compact finding details, shared validation evidence, and closeout checklist while preserving parseable labels.
  - Update downstream `verify`, `explain-change`, and `pr` guidance only where needed to point to the scan-first closeout shape and avoid duplicating full findings in summaries.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/select-validation.py --mode explicit --path templates/shared/review-isolation-and-recording.md --path templates/review-resolution.md --path skills/proposal-review/SKILL.md --path skills/spec-review/SKILL.md --path skills/architecture-review/SKILL.md --path skills/plan-review/SKILL.md --path skills/code-review/SKILL.md --path skills/verify/SKILL.md --path skills/explain-change/SKILL.md --path skills/pr/SKILL.md --path scripts/test-skill-validator.py --path scripts/test-review-artifact-validator.py`
  - `bash scripts/ci.sh --mode explicit --path templates/shared/review-isolation-and-recording.md --path templates/review-resolution.md --path skills/proposal-review/SKILL.md --path skills/spec-review/SKILL.md --path skills/architecture-review/SKILL.md --path skills/plan-review/SKILL.md --path skills/code-review/SKILL.md --path skills/verify/SKILL.md --path skills/explain-change/SKILL.md --path skills/pr/SKILL.md --path scripts/test-skill-validator.py --path scripts/test-review-artifact-validator.py --path docs/plans/2026-05-07-review-skill-material-finding-recording.md --path docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml`
  - `git diff --check -- templates skills scripts/test-skill-validator.py scripts/test-review-artifact-validator.py docs/plans/2026-05-07-review-skill-material-finding-recording.md docs/changes/2026-05-07-review-skill-material-finding-recording`
- Expected observable result: canonical review skills share one byte-identical rule, isolated material findings visibly require change-local review files, and new review-resolution records have human-readable guidance that remains validator-readable.
- Aggregate closeout: superseded by `Aggregate Implementation Slice`.
- Risks:
  - Manual copied blocks can drift if one skill is edited after copying.
  - The scan-first template can accidentally hide per-finding obligations behind shared metadata.
- Rollback/recovery:
  - Revert canonical skill/template changes together, rerun skill validation, and keep the approved specs as the source of truth until wording is corrected.

### M3. Refresh Generated Skill and Adapter Output

- Goal: Propagate canonical review-skill guidance to generated Codex runtime mirrors and public adapter packages.
- Requirements: generated-output alignment for changed review skills and adapter-shipped guidance.
- Files/components likely touched:
  - `.codex/skills/proposal-review/SKILL.md`
  - `.codex/skills/spec-review/SKILL.md`
  - `.codex/skills/architecture-review/SKILL.md`
  - `.codex/skills/plan-review/SKILL.md`
  - `.codex/skills/code-review/SKILL.md`
  - generated public adapter skill copies under `dist/adapters/`
  - generated adapter manifests if generator output changes them
  - `docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml`
  - this plan
- Dependencies:
  - M1 through M2 complete
- Tests to add/update:
  - No new generator behavior expected. Add generator tests only if the generated inventory changes beyond expected skill content propagation.
- Implementation steps:
  - Run `python scripts/build-skills.py`.
  - Run `python scripts/build-adapters.py --version 0.1.1`.
  - Inspect generated diffs for expected formal review skill changes only.
  - Do not patch generated files manually.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `bash scripts/ci.sh --mode explicit --path skills/proposal-review/SKILL.md --path skills/spec-review/SKILL.md --path skills/architecture-review/SKILL.md --path skills/plan-review/SKILL.md --path skills/code-review/SKILL.md --path .codex/skills/proposal-review/SKILL.md --path .codex/skills/spec-review/SKILL.md --path .codex/skills/architecture-review/SKILL.md --path .codex/skills/plan-review/SKILL.md --path .codex/skills/code-review/SKILL.md --path dist/adapters/codex/.agents/skills/proposal-review/SKILL.md --path dist/adapters/codex/.agents/skills/spec-review/SKILL.md --path dist/adapters/codex/.agents/skills/architecture-review/SKILL.md --path dist/adapters/codex/.agents/skills/plan-review/SKILL.md --path dist/adapters/codex/.agents/skills/code-review/SKILL.md --path dist/adapters/claude/.claude/skills/proposal-review/SKILL.md --path dist/adapters/claude/.claude/skills/spec-review/SKILL.md --path dist/adapters/claude/.claude/skills/architecture-review/SKILL.md --path dist/adapters/claude/.claude/skills/plan-review/SKILL.md --path dist/adapters/claude/.claude/skills/code-review/SKILL.md --path dist/adapters/opencode/.opencode/skills/proposal-review/SKILL.md --path dist/adapters/opencode/.opencode/skills/spec-review/SKILL.md --path dist/adapters/opencode/.opencode/skills/architecture-review/SKILL.md --path dist/adapters/opencode/.opencode/skills/plan-review/SKILL.md --path dist/adapters/opencode/.opencode/skills/code-review/SKILL.md`
  - `git diff --check -- .codex/skills dist/adapters docs/plans/2026-05-07-review-skill-material-finding-recording.md docs/changes/2026-05-07-review-skill-material-finding-recording`
- Expected observable result: generated Codex and public adapter outputs match canonical review-skill guidance with no hand edits or unrelated generated churn.
- Aggregate closeout: superseded by `Aggregate Implementation Slice`.
- Risks:
  - Generated output may include broader adapter churn if generator templates or manifests derive from changed skill metadata.
- Rollback/recovery:
  - Revert generated output and rerun generator check commands; if canonical skill changes are reverted, regenerate from the reverted source.

### Lifecycle Closeout Gates. Verification and PR Handoff

- Goal: Prove the full implementation, close review findings when triggered, synchronize lifecycle state, and prepare the PR handoff.
- Requirements: all requirements covered by this plan.
- Files/components likely touched:
  - `docs/plan.md`
  - this plan
  - `docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml`
  - `docs/changes/2026-05-07-review-skill-material-finding-recording/explain-change.md`
  - review or review-resolution artifacts if downstream review creates material findings
  - final changed authored and generated surfaces from M1 through M3
- Dependencies:
  - M1 through M3 complete
  - code-review and review-resolution when triggered
  - verify and explain-change before PR
- Tests to add/update:
  - None expected beyond M1 through M3 unless code-review, verify, or test-spec identifies a missing proof.
- Implementation steps:
  - Update this plan's progress, surprises, decisions, validation notes, outcome, and readiness as milestones complete.
  - Update `docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml` with final changed files and validation evidence.
  - Keep `docs/plan.md` synchronized with this plan body when lifecycle state changes.
  - If the PR claims this initiative is complete, move both the plan index entry and this plan body to Done before PR review opens.
  - Run final targeted validation over authored, test, selector, generated, review, plan, and change-local artifacts.
  - Leave the plan Active only if a true downstream completion event remains. Merge itself is not that event.
- Validation commands:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-07-review-skill-material-finding-recording`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-05-07-review-skill-material-finding-recording.md --path docs/proposals/2026-05-07-review-skill-material-finding-recording.md --path specs/formal-review-recording.md --path specs/formal-review-recording.test.md --path specs/review-finding-resolution-contract.md --path specs/review-finding-resolution-contract.test.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml --path docs/changes/2026-05-07-review-skill-material-finding-recording/review-log.md --path docs/changes/2026-05-07-review-skill-material-finding-recording/review-resolution.md`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/test-select-validation.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `bash scripts/ci.sh --mode explicit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path docs/plan.md --path docs/plans/2026-05-07-review-skill-material-finding-recording.md --path docs/proposals/2026-05-07-review-skill-material-finding-recording.md --path specs/formal-review-recording.md --path specs/formal-review-recording.test.md --path specs/review-finding-resolution-contract.md --path specs/review-finding-resolution-contract.test.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path templates/shared/review-isolation-and-recording.md --path templates/review-resolution.md --path skills/proposal-review/SKILL.md --path skills/spec-review/SKILL.md --path skills/architecture-review/SKILL.md --path skills/plan-review/SKILL.md --path skills/code-review/SKILL.md --path scripts/test-skill-validator.py --path scripts/test-review-artifact-validator.py --path docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml`
  - `git diff --check -- .`
- Expected observable result: lifecycle artifacts are synchronized, review findings are closed, targeted validation passes, generated output is in sync, and the change is ready for PR handoff after `code-review`, `verify`, and `explain-change`.
- Closeout commit message: `Lifecycle: close review recording handoff`
- Lifecycle closeout checklist:
  - [ ] validation passed
  - [ ] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] milestone committed
- Risks:
  - Lifecycle state can drift if the plan index is updated without the plan body or vice versa.
  - Final validation can miss generated-output drift if generator checks are omitted.
- Rollback/recovery:
  - Keep the plan active, reopen review-resolution if a material finding appears, and rerun the targeted validation set after fixes.

## Validation Plan

Use the milestone-specific validation commands above. The final validation gate must include:

- review artifact closeout validation;
- change metadata validation;
- artifact lifecycle validation for touched authoritative and change-local artifacts;
- skill validation;
- skill-validator tests;
- review artifact validator tests;
- selector regression tests when selector routing is touched;
- generated skill and adapter drift checks when canonical skills are changed;
- selector-selected CI for the touched surfaces;
- `git diff --check -- .`.

## Risks and Recovery

- Shared block drift: byte-equality assertions catch copied subsection drift. Recovery is to copy from `templates/shared/review-isolation-and-recording.md` and rerun the skill-validator tests.
- Over-recording clean reviews: preserve explicit no-material lightweight paths in specs, workflow guidance, and skills. Recovery is to narrow clean-review wording without changing the material-finding trigger.
- Under-recording material findings: the broad rule and isolated final-output requirements must stay visible in all formal review skills. Recovery is to update the canonical shared block and recopy it.
- Scan-first formatting breaks parser expectations: keep per-finding labels parseable and validate with review-artifact tests. Recovery is to restore required labels while keeping the summary/table sections.
- Generated-output drift: never patch generated files by hand. Recovery is to rerun generators from canonical sources.

## Dependencies

- `plan-review` must approve this plan before `test-spec`.
- `test-spec` must define the concrete proof map before implementation.
- M1 proof work should precede M2 canonical skill/template edits.
- M3 generated output depends on M2 canonical skill edits.
- Lifecycle closeout depends on completed implementation milestones M1 through M3, code-review, review-resolution when triggered, verify, and explain-change.

## Progress

- [x] 2026-05-07: plan created and added to `docs/plan.md` as Active.
- [x] 2026-05-07: plan-review approved with no material findings; no detailed review record was required.
- [x] 2026-05-07: test specs updated across `formal-review-recording.test.md`, `review-finding-resolution-contract.test.md`, and `rigorloop-workflow.test.md`.
- [x] M1-M3 aggregate implementation content is present in the working tree and validated as one combined slice.
- [x] M1-M3 aggregate closeout commit: `M1: implement review recording proof and guidance`.
- [x] 2026-05-07: code-review-r1 recorded `changes-requested` with material finding `CR1-F1`.
- [x] 2026-05-07: `CR1-F1` fixed, generated outputs refreshed, and review-resolution closeout restored.
- [x] 2026-05-07: clean `code-review` rerun completed with no blocking or required-change findings; no new detailed review record was triggered.
- [x] 2026-05-07: plan readiness wording updated so `Ready for verify` depends on completed implementation milestones M1-M3 and clean code-review, while downstream lifecycle gates remain active.
- [x] 2026-05-07: M1 implementation request found a blocker: M1 cannot be formally closed as an independent milestone under the current plan because its proof tests require M2/M3 surfaces and no coherent `M1:` commit exists.
- [x] 2026-05-07: owner directed M1-M3 to be replanned as one explicit aggregate closeout.
- [x] 2026-05-07: code-review-r2 recorded `changes-requested` with material finding `CR2-F1`; aggregate closeout commit is required before the post-closeout code-review rerun.
- [x] 2026-05-07: `CR2-F1` resolved by the aggregate closeout commit and aggregate validation evidence.
- [x] 2026-05-07: post-aggregate code-review-r3 rerun completed against commit `3f1fbda80ae41203be2c576cac4e6d998589f6b3` with no blocking or required-change findings.
- [ ] Lifecycle closeout gates: verify, explain-change, PR handoff, then Done if no true downstream event remains.

## Decision Log

- 2026-05-07: no separate architecture artifact for this initiative. Reason: the work changes workflow contracts, skill guidance, templates, tests, and generated outputs while reusing existing review artifact and adapter generation architecture.
- 2026-05-07: broad smoke is not required by default. Reason: selector-selected structural, skill, adapter, lifecycle, and review-artifact checks cover the touched surfaces without runtime, release, deployment, storage, or network-risk changes.
- 2026-05-07: the clean direct `spec-review` approval is recorded artifact-locally in the touched specs before planning relies on them.
- 2026-05-07: the clean direct `plan-review` approval is recorded in this plan and final assistant output; no detailed review record was created because there were no material findings or detailed-record triggers.
- 2026-05-07: M1, M2, and M3 were implemented as one green implementation slice. Reason: M1's static assertions intentionally fail until M2 creates the canonical shared block and review-resolution template, and the selector requires generated skill and adapter drift checks for the changed skill sources.
- 2026-05-07: final verification and PR handoff are tracked as lifecycle closeout gates, not as an implementation milestone. Reason: code should enter `verify` only after planned implementation milestones are complete and code-review has been conducted; the plan remains Active until verification, explain-change, PR handoff, and final Done transition finish.
- 2026-05-07: M1 formal closeout is blocked pending owner direction. Reason: `specs/rigorloop-workflow.md` `R8a` requires completed planned milestones to have passed validation, updated plan evidence, and one coherent milestone commit with no unrelated changes; the current M1 proof surfaces require M2/M3 implementation files and the working tree has no `M1:` commit for this initiative.
- 2026-05-07: owner resolved the M1 closeout blocker by directing M1-M3 to be replanned as one explicit aggregate implementation slice with a single milestone-formatted closeout commit.
- 2026-05-07: code-review-r2 found `CR2-F1`. Reason: the requested code-review happened before the aggregate closeout commit existed, so it cannot satisfy the required post-closeout code-review rerun.

## Surprises and Discoveries

- 2026-05-07: a standalone M1 closeout could not be green because the new static assertions were expected to fail against missing source guidance. The smallest first-pass acceptable implementation slice was M1 through M3.
- 2026-05-07: attempting to implement M1 after M2/M3 content already existed exposed a milestone-boundary mismatch. The working tree can pass M1 proof commands only with later milestone surfaces present, so M1 is not independently closeable without re-planning or an explicitly approved aggregate closeout.
- 2026-05-07: the approved recovery is aggregate closeout. Future review should inspect the aggregate commit body for the former M1/M2/M3 sub-slice list and validation evidence.

## Validation Notes

- 2026-05-07: `python scripts/validate-change-metadata.py docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml` passed.
- 2026-05-07: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` passed for the plan index, plan body, proposal, approved specs, and change-local review artifacts with existing lifecycle-language warnings in `docs/plan.md` and `specs/rigorloop-workflow.md`.
- 2026-05-07: `git diff --check -- ...` passed for the planning surfaces.
- 2026-05-07: `rg -n '[[:blank:]]$|\t' ...` found no trailing whitespace or tab matches.
- 2026-05-07: `bash scripts/ci.sh --mode explicit --path ...` passed selected checks for review artifacts, artifact lifecycle, change metadata regression, and change metadata validation.
- 2026-05-07: after test-spec updates, `python scripts/validate-change-metadata.py docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml` passed.
- 2026-05-07: after test-spec updates, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` passed for the plan index, plan body, proposal, specs, test specs, and change-local review artifacts with existing lifecycle-language warnings in `docs/plan.md`, `specs/rigorloop-workflow.md`, and `specs/rigorloop-workflow.test.md`.
- 2026-05-07: after test-spec updates, `git diff --check -- ...` passed.
- 2026-05-07: after test-spec updates, `rg -n '[[:blank:]]$|\t' ...` found no trailing whitespace or tab matches.
- 2026-05-07: after test-spec updates, `bash scripts/ci.sh --mode explicit --path ...` passed selected checks for review artifacts, artifact lifecycle, change metadata regression, and change metadata validation.
- 2026-05-07: `python scripts/test-skill-validator.py` initially failed as expected because the canonical shared block did not yet exist; after implementing the shared block, copied skill sections, governance wording, and downstream closeout guidance, it passed.
- 2026-05-07: `python scripts/test-review-artifact-validator.py` initially failed as expected because the scan-first `review-resolution.md` template did not yet exist; after adding the template and preserving parseable finding labels, it passed.
- 2026-05-07: `python scripts/validate-skills.py` passed after authored skill updates.
- 2026-05-07: `python scripts/select-validation.py --mode explicit --path ...` selected `skills.validate`, `skills.regression`, `skills.drift`, `adapters.drift`, `review_artifacts.regression`, `artifact_lifecycle.validate`, and `selector.regression` for the implementation slice.
- 2026-05-07: `python scripts/build-skills.py` refreshed generated Codex skill mirrors.
- 2026-05-07: `python scripts/build-adapters.py --version 0.1.1` refreshed generated public adapter outputs.
- 2026-05-07: `python scripts/build-skills.py --check` passed.
- 2026-05-07: `python scripts/test-adapter-distribution.py` passed.
- 2026-05-07: `python scripts/build-adapters.py --version 0.1.1 --check` passed.
- 2026-05-07: `python scripts/test-select-validation.py` passed.
- 2026-05-07: `python scripts/validate-adapters.py --version 0.1.1` passed.
- 2026-05-07: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-07-review-skill-material-finding-recording` passed after M1 through M3 implementation.
- 2026-05-07: `python scripts/validate-change-metadata.py docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml` passed after M1 through M3 implementation.
- 2026-05-07: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` passed after M1 through M3 implementation with existing lifecycle-language warnings in `docs/plan.md`, `docs/workflows.md`, `specs/rigorloop-workflow.md`, and `specs/rigorloop-workflow.test.md`.
- 2026-05-07: `git diff --check -- ...` passed for governance, workflow, plan, proposal, spec, test-spec, template, skill, generated, script, and change-local surfaces.
- 2026-05-07: `rg -n '[[:blank:]]$|\t' ...` found no trailing whitespace or tab matches across the implementation surfaces.
- 2026-05-07: `bash scripts/ci.sh --mode explicit --path ...` passed selected checks: `skills.validate`, `skills.regression`, `skills.drift`, `adapters.regression`, `adapters.drift`, `adapters.validate`, `review_artifacts.regression`, `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `selector.regression`.
- 2026-05-07: after recording `code-review-r1`, `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-07-review-skill-material-finding-recording` passed with `reviews=5`, `findings=12`, `log_entries=5`, and `resolution_entries=12`.
- 2026-05-07: after recording `code-review-r1`, `python scripts/validate-change-metadata.py docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml` passed.
- 2026-05-07: after recording `code-review-r1`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` passed for the code-review record and review closeout artifacts.
- 2026-05-07: after recording `code-review-r1`, `git diff --check -- ...` passed for the review record, review log, review resolution, and change metadata.
- 2026-05-07: after recording `code-review-r1`, `rg -n '[[:blank:]]$|\t' ...` found no trailing whitespace or tab matches.
- 2026-05-07: `python scripts/test-skill-validator.py` passed after tightening mandatory timing wording coverage for `CR1-F1`.
- 2026-05-07: `python scripts/validate-skills.py` passed after the `CR1-F1` fix.
- 2026-05-07: `python scripts/build-skills.py` refreshed generated Codex skill mirrors after the `CR1-F1` fix.
- 2026-05-07: `python scripts/build-adapters.py --version 0.1.1` refreshed generated public adapter outputs after the `CR1-F1` fix.
- 2026-05-07: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-07-review-skill-material-finding-recording` passed after adding the explicit `Review closeout: code-review-r1` pointer.
- 2026-05-07: `git diff --check -- .` passed after the `CR1-F1` fix.
- 2026-05-07: `rg -n '[[:blank:]]$|\t' ...` found no trailing whitespace or tab matches after the `CR1-F1` fix.
- 2026-05-07: `bash scripts/ci.sh --mode local` passed selected checks after the `CR1-F1` fix: `skills.validate`, `skills.regression`, `skills.drift`, `adapters.regression`, `adapters.drift`, `adapters.validate`, `review_artifacts.regression`, `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `selector.regression`.
- 2026-05-07: clean `code-review` rerun passed with no blocking or required-change findings after reviewing the current working tree, specs, test specs, plan, generated-output contract, and review closeout evidence.
- 2026-05-07: during the clean `code-review` rerun, `python scripts/test-skill-validator.py`, `python scripts/test-review-artifact-validator.py`, `python scripts/validate-skills.py`, `python scripts/build-skills.py --check`, `python scripts/build-adapters.py --version 0.1.1 --check`, `python scripts/validate-adapters.py --version 0.1.1`, `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-07-review-skill-material-finding-recording`, and `git diff --check -- .` passed.
- 2026-05-07: after recording clean code-review readiness, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-05-07-review-skill-material-finding-recording.md --path docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml` passed with the existing lifecycle-language warning in `docs/plan.md`.
- 2026-05-07: after recording clean code-review readiness, `python scripts/select-validation.py --mode explicit --path docs/plans/2026-05-07-review-skill-material-finding-recording.md --path docs/plan.md` selected `artifact_lifecycle.validate`.
- 2026-05-07: after recording clean code-review readiness, `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/plans/2026-05-07-review-skill-material-finding-recording.md` passed selected check `artifact_lifecycle.validate`.
- 2026-05-07: after recording clean code-review readiness, `git diff --check -- docs/plans/2026-05-07-review-skill-material-finding-recording.md docs/plan.md` passed and `rg -n '[[:blank:]]$|\t' docs/plans/2026-05-07-review-skill-material-finding-recording.md docs/plan.md` found no trailing whitespace or tab matches.
- 2026-05-07: after recording clean code-review readiness in `change.yaml`, `python scripts/validate-change-metadata.py docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml` passed.
- 2026-05-07: after recording clean code-review readiness in `change.yaml`, `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/plans/2026-05-07-review-skill-material-finding-recording.md --path docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml` passed selected checks `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- 2026-05-07: after recording clean code-review readiness in `change.yaml`, `git diff --check -- docs/plans/2026-05-07-review-skill-material-finding-recording.md docs/plan.md docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml` passed and `rg -n '[[:blank:]]$|\t' docs/plans/2026-05-07-review-skill-material-finding-recording.md docs/plan.md docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml` found no trailing whitespace or tab matches.
- 2026-05-07: after clarifying verify handoff versus lifecycle closeout, `python scripts/validate-change-metadata.py docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml` passed.
- 2026-05-07: after clarifying verify handoff versus lifecycle closeout, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-05-07-review-skill-material-finding-recording.md --path docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml` passed with the existing lifecycle-language warning in `docs/plan.md`.
- 2026-05-07: after clarifying verify handoff versus lifecycle closeout, `python scripts/select-validation.py --mode explicit --path docs/plan.md --path docs/plans/2026-05-07-review-skill-material-finding-recording.md --path docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml` selected `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- 2026-05-07: after clarifying verify handoff versus lifecycle closeout, `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/plans/2026-05-07-review-skill-material-finding-recording.md --path docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml` passed selected checks `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- 2026-05-07: after clarifying verify handoff versus lifecycle closeout, `git diff --check -- docs/plan.md docs/plans/2026-05-07-review-skill-material-finding-recording.md docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml` passed and `rg -n '[[:blank:]]$|\t' docs/plan.md docs/plans/2026-05-07-review-skill-material-finding-recording.md docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml` found no trailing whitespace or tab matches.
- 2026-05-07: M1 implementation attempt found a formal closeout blocker. `python scripts/test-skill-validator.py` and `python scripts/test-review-artifact-validator.py` passed on the current combined working tree, but the result relies on M2/M3 source surfaces and therefore does not prove an independent M1 closeout.
- 2026-05-07: after recording the M1 closeout blocker, `python scripts/select-validation.py --mode explicit --path specs/formal-review-recording.test.md --path specs/review-finding-resolution-contract.test.md --path specs/rigorloop-workflow.test.md --path scripts/test-skill-validator.py --path scripts/test-review-artifact-validator.py --path docs/plan.md --path docs/plans/2026-05-07-review-skill-material-finding-recording.md --path docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml` selected `skills.regression`, `review_artifacts.regression`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- 2026-05-07: after recording the M1 closeout blocker, `bash scripts/ci.sh --mode explicit --path specs/formal-review-recording.test.md --path specs/review-finding-resolution-contract.test.md --path specs/rigorloop-workflow.test.md --path scripts/test-skill-validator.py --path scripts/test-review-artifact-validator.py --path docs/plan.md --path docs/plans/2026-05-07-review-skill-material-finding-recording.md --path docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml` passed selected checks `skills.regression`, `review_artifacts.regression`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- 2026-05-07: after recording the M1 closeout blocker, `git diff --check -- specs/formal-review-recording.test.md specs/review-finding-resolution-contract.test.md specs/rigorloop-workflow.test.md scripts/test-skill-validator.py scripts/test-review-artifact-validator.py docs/plan.md docs/plans/2026-05-07-review-skill-material-finding-recording.md docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml` passed and `rg -n '[[:blank:]]$|\t' specs/formal-review-recording.test.md specs/review-finding-resolution-contract.test.md specs/rigorloop-workflow.test.md scripts/test-skill-validator.py scripts/test-review-artifact-validator.py docs/plan.md docs/plans/2026-05-07-review-skill-material-finding-recording.md docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml` found no trailing whitespace or tab matches.
- 2026-05-07: after moving the plan to Blocked for the M1 milestone-boundary issue, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-05-07-review-skill-material-finding-recording.md --path docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml` passed with the existing lifecycle-language warning in `docs/plan.md`.
- 2026-05-07: after moving the plan to Blocked for the M1 milestone-boundary issue, `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/plans/2026-05-07-review-skill-material-finding-recording.md --path docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml` passed selected checks `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- 2026-05-07: after re-planning M1-M3 as one aggregate implementation slice, `python scripts/validate-change-metadata.py docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml` passed.
- 2026-05-07: after re-planning M1-M3 as one aggregate implementation slice, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-05-07-review-skill-material-finding-recording.md --path docs/learn/sessions/2026-05-07-milestone-closeout-vs-progress.md --path docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml` passed with the existing lifecycle-language warning in `docs/plan.md`.
- 2026-05-07: after re-planning M1-M3 as one aggregate implementation slice, `python scripts/select-validation.py --mode explicit --path docs/plan.md --path docs/plans/2026-05-07-review-skill-material-finding-recording.md --path docs/learn/sessions/2026-05-07-milestone-closeout-vs-progress.md --path docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml` selected `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- 2026-05-07: after re-planning M1-M3 as one aggregate implementation slice, `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/plans/2026-05-07-review-skill-material-finding-recording.md --path docs/learn/sessions/2026-05-07-milestone-closeout-vs-progress.md --path docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml` passed selected checks `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- 2026-05-07: after re-planning M1-M3 as one aggregate implementation slice, `git diff --check -- docs/plan.md docs/plans/2026-05-07-review-skill-material-finding-recording.md docs/learn/sessions/2026-05-07-milestone-closeout-vs-progress.md docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml` passed and `rg -n '[[:blank:]]$|\t' docs/plan.md docs/plans/2026-05-07-review-skill-material-finding-recording.md docs/learn/sessions/2026-05-07-milestone-closeout-vs-progress.md docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml` found no trailing whitespace or tab matches.
- 2026-05-07: after recording code-review-r2, `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-07-review-skill-material-finding-recording` passed with `reviews=6`, `findings=13`, `log_entries=6`, and `resolution_entries=13`.
- 2026-05-07: after recording code-review-r2, `bash scripts/ci.sh --mode explicit --path docs/changes/2026-05-07-review-skill-material-finding-recording/reviews/code-review-r2.md --path docs/changes/2026-05-07-review-skill-material-finding-recording/review-log.md --path docs/changes/2026-05-07-review-skill-material-finding-recording/review-resolution.md --path docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml` passed selected checks `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- 2026-05-07: aggregate validation before closeout commit passed: `python scripts/test-skill-validator.py`, `python scripts/test-review-artifact-validator.py`, `python scripts/validate-skills.py`, `python scripts/test-select-validation.py`, `python scripts/test-adapter-distribution.py`, `python scripts/build-skills.py --check`, `python scripts/build-adapters.py --version 0.1.1 --check`, `python scripts/validate-adapters.py --version 0.1.1`, `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-07-review-skill-material-finding-recording`, `python scripts/validate-change-metadata.py docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml`, `python scripts/test-change-metadata-validator.py`, `bash scripts/ci.sh --mode local`, and `git diff --check -- .`.
- 2026-05-07: aggregate whitespace scan over changed paths found no trailing whitespace or tab matches.
- 2026-05-07: after resolving `CR2-F1` and recording aggregate closeout readiness, `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-07-review-skill-material-finding-recording`, `python scripts/validate-change-metadata.py docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml`, lifecycle validation, selected CI for closeout files, `git diff --check -- .`, and whitespace scan passed.
- 2026-05-07: during post-aggregate code-review-r3, `python scripts/test-skill-validator.py`, `python scripts/test-review-artifact-validator.py`, `python scripts/build-skills.py --check`, `python scripts/build-adapters.py --version 0.1.1 --check`, `python scripts/validate-adapters.py --version 0.1.1`, `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-07-review-skill-material-finding-recording`, `python scripts/validate-change-metadata.py docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml`, and `git diff --check HEAD^ HEAD -- .` passed.

## Outcome and Retrospective

- Active. M1 through M3 implementation content is closed as one explicit aggregate implementation slice with validation evidence, the planned closeout commit, and a clean post-aggregate code-review rerun. Remaining work starts with verify, followed by explain-change, PR handoff, and Done transition.

## Readiness

- Ready for `verify`.
- Not ready for `explain-change` or PR handoff until `verify` completes.
