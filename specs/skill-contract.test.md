# Skill Contract Test Spec

## Status

- active

## Related spec and plan

- Spec: [Skill Contract](skill-contract.md), approved after clean spec-review on 2026-05-08.
- Proposal: [Skill Contract Optimization](../docs/proposals/2026-05-08-skill-contract-optimization.md), accepted.
- Plan: [Skill Contract Optimization Execution Plan](../docs/plans/2026-05-08-skill-contract-optimization.md), active after clean plan-review.
- Architecture: not required. The approved slice changes workflow-governance Markdown, canonical skill guidance, shared text blocks, static validation, generated skill mirrors, and public adapter skill copies. It does not add runtime components, storage, API boundaries, deployment boundaries, or a new validation architecture.
- Project map: `docs/project-map.md` is absent. This test spec does not rely on project-map claims; proof uses the approved spec, active plan, workflow specs, stage skills, shared templates, generator scripts, and existing validator patterns.
- Related proof surfaces:
  - `scripts/test-skill-validator.py`
  - `scripts/validate-skills.py`
  - `scripts/select-validation.py`
  - `scripts/build-skills.py`
  - `scripts/build-adapters.py`
  - `scripts/validate-adapters.py`
  - `scripts/test-adapter-distribution.py`
  - `scripts/ci.sh`

## Testing strategy

- Use contract and static wording checks because the approved first implementation slice is skill guidance and validator behavior, not a runtime workflow router.
- Use `scripts/test-skill-validator.py` for machine-checkable invariants in canonical skills, shared blocks, workflow summaries, and narrow forbidden-overclaim checks.
- Use `scripts/validate-skills.py` for authored skill structure after canonical skills are edited.
- Use selector-selected validation to prove changed spec, plan, skill, template, generated, adapter, and change-local paths are classified without unclassified paths.
- Use generated-output drift checks after canonical skill edits to prove `.codex/skills/` and public adapter packages remain derived output.
- Use manual contract review for nuanced prose boundaries: claim ownership, local handoff, preserving useful skill-specific guidance, avoiding hollow required sections, and preventing broad semantic quality scoring.
- Do not add runtime workflow simulation, natural-language scoring, broad prose linting, a shared-block generation build step, a standalone `review-resolution` skill, or a `skills/ci-maintenance/SKILL.md` path.

## Requirement coverage map

| Requirement IDs | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `R1`, `R1a`, `R1b`, `R1c`, `R1d`, `R20`, `R20a`, `R20b` | `T1`, `T11`, `T13` | contract, manual | Normative source split and source-of-truth order |
| `R2`, `R2a`, `R2b`, `R2c`, `R2d` | `T9`, `T13` | integration, smoke | Canonical skills, generated mirrors, adapter output, and drift checks |
| `R3`, `R3a`, `R3b`, `R3c` | `T2`, `T13` | integration, manual | Required core sections, conditional sections, and preservation of useful local guidance |
| `R4`, `R4a` | `T2`, `T5` | manual, integration | Authoring skill output ownership and quality checklist expectations, within first-slice applicability |
| `R5`, `R5a`, `R5b` | `T4`, `T5`, `T7` | integration, manual | Review skill status/finding/recording contract and shared review recording preservation |
| `R6`, `R6a`, `R6b`, `R6c` | `T3`, `T4`, `T12` | integration, manual | Execution skill proof boundaries and `ci`/`ci-maintenance` naming split |
| `R7`, `R7a` | `T4`, `T11` | manual | `learn` and later support skills keep trigger/output/handoff boundaries |
| `R8`, `R8a`, `R8b`, `R8c`, `R8d`, `R8e`, `R8f`, `R8g` | `T2`, `T3`, `T4`, `T5`, `T6`, `T8`, `T9` | integration, manual | First-slice scope, core sections, claims, result output, readiness wording, targeted reading, and generated drift |
| `R9`, `R9a`, `R9b`, `R9c`, `R9d` | `T3`, `T12` | manual, integration | Later-phase normalization order and optional skills remain out of scope |
| `R10`, `R10a`, `R10b`, `R10c`, `R10d`, `R10e`, `R10f` | `T4`, `T10`, `T13` | integration, manual | Claims this skill must not make and narrow overclaim checks |
| `R11`, `R11a`, `R11b`, `R11c` | `T5`, `T13` | integration, manual | Summary-first result output and common/optional fields |
| `R12`, `R12a`, `R12b`, `R12c` | `T5`, `T13` | integration, manual | Local handoff, workflow spec pointer, and isolated invocation boundary |
| `R13`, `R13a`, `R13b`, `R13c`, `R13d`, `R13e`, `R13f` | `T6`, `T13` | integration, manual | Progress, readiness, closeout, Done, and Ready for verify wording |
| `R14`, `R14a`, `R14b`, `R14c`, `R14d`, `R14e` | `T7`, `T13` | integration, manual | Shared-block source, copy-and-check, authority boundary, and no generation v1 |
| `R15`, `R15a`, `R15b` | `T7`, `T13` | integration, manual | First shared-block set and deferred shared blocks |
| `R16`, `R16a`, `R16b`, `R16c` | `T8`, `T13` | integration, manual | Evidence-reading guidance and full-file read escalation |
| `R17`, `R17a`, `R17b` | `T8`, `T13` | manual | Optional bounded examples and long-example exclusion |
| `R18`, `R18a`, `R18b`, `R18c`, `R18d` | `T10`, `T13` | integration, manual | Positive-first, narrow, incident-based validator strategy |
| `R19`, `R19a`, `R19b`, `R19c` | `T11`, `T13` | manual, integration | Minimum viable skill rule and guidance placement |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| `E1` | `T4`, `T6` | `implement` may report implementation/validation and `code-review` handoff, but not review, branch, PR, or verify ownership |
| `E2` | `T3` | Non-first-slice skills remain valid until later phases |
| `E3` | `T7` | Shared block is copied verbatim and checked for drift |
| `E4` | `T9` | Generated skill mirrors and adapter outputs stay derived |
| `E5` | `T10` | Overclaim validation is narrow and positive-first |
| `E6` | `T11` | One-off behavior does not create a new skill |
| `E7` | `T3`, `T12` | `ci-maintenance` maps to existing `ci` skill entrypoint |

## Edge case coverage

- EC1, existing skill has domain-specific section overlapping required core: `T2`
- EC2, skill is both authoring and execution oriented: `T2`, `T5`
- EC3, clean review output has no material findings: `T4`, `T7`
- EC4, shared block adopted by only one skill initially: `T7`
- EC5, normalized skill needs a short example: `T8`
- EC6, generated adapter path changes or selector path is concrete: `T9`
- EC7, `ready for verify` appears in negative guidance: `T10`
- EC8, optional Phase 4 skill is named but not approved: `T3`, `T12`

## Acceptance criteria coverage map

| Acceptance criterion | Covered by |
| --- | --- |
| Skill contract source is identifiable | `T1`, `T13` |
| Skill-contract behavior is distinct from workflow-routing behavior | `T1`, `T5` |
| Required core sections are identifiable | `T2` |
| First implementation slice is identifiable | `T3` |
| Later normalization phases are identifiable | `T3` |
| `ci` is the `ci-maintenance` entrypoint | `T3`, `T12` |
| Normalized skills include do-not-overclaim guidance | `T4`, `T10` |
| Skill outputs are summary-first | `T5` |
| Shared blocks are copied and drift-checked | `T7` |
| Generated output is regenerated, not hand-edited | `T9` |
| Validator checks are positive-first, narrow, and not broad semantic scoring | `T10` |
| New skill justification is clear | `T11` |

## Test cases

### T1. Normative skill-contract source and workflow-routing split

- Covers: `R1`, `R1a`, `R1b`, `R1c`, `R1d`, `R20`, `R20a`, `R20b`
- Level: contract, manual
- Fixture/setup:
  - `specs/skill-contract.md`
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `AGENTS.md`
- Steps:
  - Assert `specs/skill-contract.md` states it owns skill shape, claim boundaries, result output, shared-block rules, generated-output boundaries, evidence-reading guidance, and minimum viable skill rules.
  - Assert `specs/rigorloop-workflow.md` remains the source for stage order, stage obligation, handoff, and downstream-blocking semantics.
  - Assert `docs/workflows.md` and `AGENTS.md` summarize or point to the skill contract without overriding it.
  - Manually review conflicts: skill-contract behavior follows the skill contract; workflow-routing semantics follow the workflow spec.
- Expected result:
  - Reviewers can identify the normative skill-contract source and the separate workflow-routing source without guessing.
- Failure proves:
  - Validator-enforced skill behavior lacks a clear source of truth or competes with workflow routing.
- Automation location:
  - `scripts/test-skill-validator.py`
  - manual contract review during M2

### T2. Required and conditional sections are present without hollow normalization

- Covers: `R3`, `R3a`, `R3b`, `R3c`, `R4`, `R4a`, `R8a`, EC1, EC2
- Level: integration, manual
- Fixture/setup:
  - `skills/workflow/SKILL.md`
  - `skills/plan/SKILL.md`
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/pr/SKILL.md`
  - `skills/learn/SKILL.md`
  - `scripts/test-skill-validator.py`
  - `scripts/validate-skills.py`
- Steps:
  - Assert every first-slice canonical skill includes `Purpose`, `When to use`, `When not to use`, `Inputs to read`, `Outputs`, `Handoff`, `Stop conditions`, and `Claims this skill must not make`.
  - Assert conditional sections appear only when relevant and do not flatten useful skill-specific sections.
  - Manually confirm behavior-changing local guidance, artifact shapes, review formats, validation proof, and stop conditions remain present after normalization.
  - Confirm any overlapping or dual-role sections stay clear instead of creating duplicate or hollow sections.
- Expected result:
  - First-slice skills gain common scanning anchors while preserving meaningful local guidance.
- Failure proves:
  - Normalization created checklist-only skill prose or erased behavior-critical instructions.
- Automation location:
  - `scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`

### T3. First-slice and later-phase scope stay exact

- Covers: `R6b`, `R6c`, `R8`, `R8g`, `R9`, `R9a`, `R9b`, `R9c`, `R9d`, E2, E7, EC8
- Level: integration, manual
- Fixture/setup:
  - `specs/skill-contract.md`
  - `docs/plans/2026-05-08-skill-contract-optimization.md`
  - `docs/workflows.md`
  - repository `skills/` tree
- Steps:
  - Assert the first implementation slice names only `workflow`, `plan`, `implement`, `code-review`, `verify`, `pr`, and `learn`.
  - Assert Phase 2 includes core lifecycle authoring/review skills and the existing `ci` skill for the `ci-maintenance` stage label.
  - Assert Phase 3 and Phase 4 are described as later work.
  - Assert no implementation creates or requires `skills/ci-maintenance/SKILL.md`, standalone `review-resolution` skill, or Phase 4 optional skill paths.
  - Manually confirm unnormalized Phase 2/3/4 skills are not treated as failing first-slice proof.
- Expected result:
  - The implementation stays reviewable and does not accidentally normalize every skill.
- Failure proves:
  - Scope creep or naming confusion invalidates the accepted first slice.
- Automation location:
  - `scripts/test-skill-validator.py`
  - `rg --files skills | rg '(^|/)(ci-maintenance|review-resolution|ui-design|ui-design-review|workflow-contract|adopt-rigorloop)/SKILL.md$'` as negative proof

### T4. Claim boundaries and do-not-overclaim guidance

- Covers: `R5`, `R5a`, `R5b`, `R6`, `R6a`, `R7`, `R7a`, `R8b`, `R10`, `R10a`, `R10b`, `R10c`, `R10d`, `R10e`, `R10f`, E1
- Level: integration, manual
- Fixture/setup:
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/pr/SKILL.md`
  - `skills/plan/SKILL.md`
  - `skills/learn/SKILL.md`
  - `scripts/test-skill-validator.py`
- Steps:
  - Assert `implement` does not claim review passed, clean review, branch-ready, PR-ready, or ready-for-verify.
  - Assert `code-review` does not claim branch-ready, PR-ready, CI passed, or verification passed.
  - Assert `verify` does not claim PR-ready, PR body ready, or review passed.
  - Assert `pr` links implementation, review, verification, and test claims to owning evidence rather than proving them itself.
  - Assert `plan` distinguishes Done, complete, ready for PR, and ready for verify from remaining gates.
  - Assert `learn` routes new policy to authoritative artifacts instead of creating policy in the lesson alone.
  - Manually confirm review skills preserve formal review recording rules when findings exist.
- Expected result:
  - Each skill owns only its local proof and next-stage readiness.
- Failure proves:
  - The recurring progress/readiness/closeout/Done overclaim remains possible.
- Automation location:
  - `scripts/test-skill-validator.py`
  - manual review during M3

### T5. Result blocks and handoff sections are summary-first and local

- Covers: `R4`, `R5`, `R8c`, `R11`, `R11a`, `R11b`, `R11c`, `R12`, `R12a`, `R12b`, `R12c`
- Level: integration, manual
- Fixture/setup:
  - first-slice canonical skill files
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
- Steps:
  - Assert normalized skills require a compact `## Result` block or reviewed equivalent summary format.
  - Assert the common fields `Skill`, `Status`, `Artifacts changed`, `Open blockers`, and `Next stage` are present where the result block is specified.
  - Assert optional fields are used only where relevant, such as `Validation`, `Review status`, `Finding IDs`, `Milestone state`, `Readiness`, `Follow-ups`, `Session path`, or `Lessons captured`.
  - Assert handoff sections name local normal and conditional next stages and point to `specs/rigorloop-workflow.md` for full routing.
  - Manually confirm no skill implies automatic downstream continuation for isolated invocations.
- Expected result:
  - Later agents can read a compact result first, while workflow routing remains owned by the workflow spec.
- Failure proves:
  - Skills remain long, stateful, or overbroad in downstream routing claims.
- Automation location:
  - `scripts/test-skill-validator.py`
  - manual review during M3

### T6. Progress, readiness, closeout, and Done stay distinct

- Covers: `R8d`, `R13`, `R13a`, `R13b`, `R13c`, `R13d`, `R13e`, `R13f`, E1
- Level: integration, manual
- Fixture/setup:
  - `skills/plan/SKILL.md`
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/pr/SKILL.md`
  - `skills/workflow/SKILL.md`
  - active plan examples under `docs/plans/`
- Steps:
  - Assert planning and execution guidance defines or preserves distinct meanings for `Progress`, `Readiness`, `Closeout`, and `Done`.
  - Assert `Ready for verify` is not described as Done, PR-ready, branch-ready, or full lifecycle completion.
  - Assert plans that mention `Ready for verify` pair it with remaining completion gates when ambiguity is possible.
  - Confirm milestone closeout depends on the reviewed milestone state and generated-output refresh when applicable.
- Expected result:
  - A next-stage readiness line cannot be mistaken for final lifecycle completion.
- Failure proves:
  - The skill contract does not fix the known readiness/closeout confusion.
- Automation location:
  - `scripts/test-skill-validator.py`
  - manual plan and skill review during M3 and verify

### T7. Shared blocks are canonical copied text with drift checks

- Covers: `R5b`, `R14`, `R14a`, `R14b`, `R14c`, `R14d`, `R14e`, `R15`, `R15a`, `R15b`, E3, EC3, EC4
- Level: integration, manual
- Fixture/setup:
  - `templates/shared/review-isolation-and-recording.md`
  - `templates/shared/evidence-collection-efficiency.md`
  - `templates/shared/generated-output-handling.md`
  - consuming first-slice skills
  - `scripts/test-skill-validator.py`
- Steps:
  - Assert the v1 shared block source files exist for adopted stable rules.
  - Assert copied consuming skill subsections match the shared source verbatim when a block is adopted.
  - Assert shared blocks do not replace or outrank `specs/skill-contract.md` or `specs/rigorloop-workflow.md`.
  - Assert no build step generates shared blocks into skills in the first implementation slice.
  - Assert deferred shared blocks are not accidentally enforced.
- Expected result:
  - Shared policy stays consistent where exact wording matters without introducing a new policy authority or generator.
- Failure proves:
  - Copied policy can drift or shared-block governance is ambiguous.
- Automation location:
  - `scripts/test-skill-validator.py`
  - manual review during M2 and M3

### T8. Evidence-reading and example guidance stay bounded

- Covers: `R8e`, `R16`, `R16a`, `R16b`, `R16c`, `R17`, `R17a`, `R17b`, EC5
- Level: integration, manual
- Fixture/setup:
  - first-slice canonical skill files
  - `templates/shared/evidence-collection-efficiency.md`
  - `docs/workflows.md`
  - `scripts/test-skill-validator.py`
- Steps:
  - Assert normalized skills prefer summaries, stable IDs, headings, targeted sections, check IDs, file paths, counts, or line citations before broad reads.
  - Assert full-file reads remain required when the whole file is the review target, relevant sections cannot be isolated safely, context can change the conclusion, bounded searches conflict, or behavior-changing edits depend on the whole artifact.
  - Assert evidence-reading guidance does not weaken exact artifact review obligations.
  - Assert examples are optional, bounded, and route long examples outside skill files.
- Expected result:
  - Skill guidance reduces broad reads without weakening review or authoring correctness.
- Failure proves:
  - The optimization trades correctness for token savings or bloats skills with examples.
- Automation location:
  - `scripts/test-skill-validator.py`
  - manual review during M2 and M3

### T9. Generated output is refreshed from concrete canonical changes

- Covers: `R2`, `R2a`, `R2b`, `R2c`, `R2d`, `R8f`, E4, EC6
- Level: integration, smoke
- Fixture/setup:
  - canonical first-slice skills after M3
  - `.codex/skills/`
  - `dist/adapters/codex/.agents/skills/`
  - `dist/adapters/claude/.claude/skills/`
  - `dist/adapters/opencode/.opencode/skills/`
- Steps:
  - Run `python scripts/build-skills.py`.
  - Run `python scripts/build-adapters.py --version 0.1.1`.
  - Run `python scripts/build-skills.py --check`.
  - Run `python scripts/build-adapters.py --version 0.1.1 --check`.
  - Run `python scripts/validate-adapters.py --version 0.1.1`.
  - Run `python scripts/test-adapter-distribution.py`.
  - Run selector validation with concrete generated skill and adapter file paths for each changed generated file; do not pass `--path dist/adapters`.
  - Manually confirm generated files were not hand-edited as source.
- Expected result:
  - Generated mirrors and adapter packages match canonical first-slice skills and selector classification has no unclassified generated paths.
- Failure proves:
  - Generated output can drift from canonical skill source or selector validation can miss adapter proof.
- Automation location:
  - commands named above

### T10. Forbidden-overclaim validation is narrow and positive-first

- Covers: `R10`, `R18`, `R18a`, `R18b`, `R18c`, `R18d`, E5, EC7
- Level: integration, manual
- Fixture/setup:
  - `scripts/test-skill-validator.py`
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/pr/SKILL.md`
  - `skills/plan/SKILL.md`
  - `skills/learn/SKILL.md`
- Steps:
  - Assert validator coverage prefers positive required wording and required sections before forbidden phrases.
  - Assert any forbidden phrase checks are limited to historically dangerous skill-specific claims.
  - Assert checks do not block explicit negative guidance, including "Do not set Ready for verify from implement."
  - Assert no broad natural-language quality scoring or semantic prose scoring is added.
- Expected result:
  - Static validation catches known dangerous overclaims without becoming a brittle language judge.
- Failure proves:
  - Validator behavior either misses the recurring incidents or overfits broad prose.
- Automation location:
  - `scripts/test-skill-validator.py`
  - manual review of validator changes

### T11. Minimum viable skill rule and guidance placement

- Covers: `R7`, `R7a`, `R19`, `R19a`, `R19b`, `R19c`, `R20`, E6
- Level: manual, integration
- Fixture/setup:
  - `specs/skill-contract.md`
  - `docs/workflows.md`
  - `AGENTS.md`
  - `templates/skill.md` or skill-creator guidance if updated
- Steps:
  - Assert `specs/skill-contract.md` owns the normative minimum viable skill rule.
  - Assert `docs/workflows.md` and `AGENTS.md` summarize the rule without replacing the spec.
  - Assert detailed examples or templates, if added, live in skill-creator guidance rather than root agent instructions.
  - Assert one-off helper behavior, tiny formatting rules, and checklists that belong in existing skills do not create new skill paths.
- Expected result:
  - Contributors can decide when a new skill is justified and where detailed creation guidance belongs.
- Failure proves:
  - The repository can accumulate one-off skills or competing skill-creation policy.
- Automation location:
  - manual review during M2
  - `scripts/test-skill-validator.py` for required terms if implemented

### T12. Compatibility, security, and non-goal boundaries

- Covers: `R6b`, `R6c`, `R9c`, `R9d`, E7, EC8
- Level: manual, integration
- Fixture/setup:
  - repository tree after implementation
  - `specs/skill-contract.md`
  - `docs/workflows.md`
  - `AGENTS.md`
- Steps:
  - Confirm existing unnormalized skills remain valid until their approved phase.
  - Confirm existing `skills/ci/` path remains valid for `ci-maintenance` and no `skills/ci-maintenance/SKILL.md` path exists.
  - Confirm no standalone `review-resolution` skill is introduced.
  - Confirm Phase 4 candidate skills are not created solely because they are named in the spec.
  - Confirm generated output refreshes do not commit secrets, credentials, tokens, private keys, private user data, or machine-local paths.
- Expected result:
  - The skill-contract implementation is compatible with existing repository skill paths and security boundaries.
- Failure proves:
  - The change creates unsupported paths, overreaches optional-skill scope, or weakens generated-output safety.
- Automation location:
  - `rg --files`
  - manual review during M2, M3, and M4

### T13. Full milestone and final validation closeout

- Covers: all requirements as final integration proof
- Level: integration, smoke, manual
- Fixture/setup:
  - all changed authored, generated, plan, review, and change-local paths
  - active plan validation commands
- Steps:
  - Run selector validation for each milestone's changed path set and record no unclassified paths.
  - Run `bash scripts/ci.sh --mode explicit` for each milestone's changed path set.
  - Before PR, run `python scripts/validate-skills.py`, `python scripts/test-skill-validator.py`, `python scripts/build-skills.py --check`, `python scripts/build-adapters.py --version 0.1.1 --check`, `python scripts/validate-adapters.py --version 0.1.1`, and `python scripts/test-adapter-distribution.py`.
  - Run `python scripts/validate-change-metadata.py docs/changes/2026-05-08-skill-contract-optimization/change.yaml` when change metadata changes.
  - Run `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-08-skill-contract-optimization` before final handoff.
  - Run broad smoke only if triggered by selector, plan, test spec, review-resolution, release metadata, or explicit reviewer requirement.
  - Manually confirm final plan state, explain-change, and PR handoff do not introduce new authoritative references after verify without rerunning verify.
- Expected result:
  - The implementation is proven by repository-owned static, generated-output, adapter, lifecycle, and selected CI checks, with broad smoke only when triggered.
- Failure proves:
  - A milestone or final handoff lacks durable proof or generated/lifecycle artifacts are stale.
- Automation location:
  - active plan commands
  - `scripts/ci.sh`

## Fixtures and data

- No new external fixtures or runtime data are required.
- Static tests use canonical repository files as fixtures:
  - approved spec and active test spec under `specs/`;
  - first-slice canonical skills under `skills/`;
  - shared blocks under `templates/shared/`;
  - generated mirrors under `.codex/skills/`;
  - public adapter output under `dist/adapters/`;
  - active plan and change-local metadata under `docs/`.
- Any temporary fixture for validator failure cases should live under existing test fixture roots such as `tests/fixtures/skills/` and must not reference machine-local paths.

## Mocking/stubbing policy

- Do not mock repository-owned validation commands for milestone closeout.
- Unit-level validator tests may use small fixture skill trees for negative cases when the production skill files should remain valid.
- Generated-output tests may use temporary output roots when helper-level tests need stale, missing, or unexpected generated files.
- Do not stub `scripts/build-skills.py --check`, `scripts/build-adapters.py --version 0.1.1 --check`, `scripts/validate-adapters.py --version 0.1.1`, or `scripts/ci.sh` in final milestone proof.

## Migration or compatibility tests

- Existing unnormalized skills remain valid until later phases: `T3`, `T12`.
- Existing `skills/ci/SKILL.md` remains the `ci-maintenance` entrypoint: `T3`, `T12`.
- Generated `.codex/skills/` and `dist/adapters/` output remain derived and deterministic: `T9`, `T13`.
- Rollback for wording-only skill changes reverts canonical skills, shared blocks, validator checks, and generated output together; manual recovery review is covered by `T13`.

## Observability verification

- No runtime logs, metrics, traces, or audit events are required.
- Validation output should identify failed required sections, shared-block drift, generated-output drift, selector classification gaps, and overclaim checks clearly enough for maintainers to fix them: `T7`, `T9`, `T10`, `T13`.
- Review and verification artifacts should cite concrete commands and results, not generic success claims: `T13`.

## Security/privacy verification

- Static and generated-output changes must not commit secrets, credentials, tokens, private keys, private user data, or unjustified machine-local paths: `T12`.
- Evidence-reading guidance must not encourage pasting sensitive logs or secrets into skill output: `T8`, `T12`.
- Adapter output remains generated proof surface, not an independent source of truth: `T9`, `T12`.

## Performance checks

- Skill-contract validation remains static and repository-local in the first implementation slice: `T10`, `T13`.
- No broad natural-language quality scoring is added: `T10`.
- Evidence-reading guidance should reduce broad reads by preferring targeted summaries, IDs, headings, paths, counts, and line citations: `T8`.
- Broad smoke is not required unless triggered by selector, plan, test spec, review-resolution, release metadata, or explicit reviewer requirement: `T13`.

## Manual QA checklist

- Confirm first-slice skill changes are smaller and easier to scan, not merely reorganized into longer files.
- Confirm every required core section has actionable content and no hollow filler.
- Confirm no useful domain-specific section is removed from a skill without an equivalent local instruction.
- Confirm the result block shape is adapted to skill type without losing the common handoff fields.
- Confirm handoff guidance stays local and points to `specs/rigorloop-workflow.md` for full routing.
- Confirm generated-output selector validation uses concrete generated files, not `--path dist/adapters`.

## What not to test and why

- Do not test runtime workflow routing; this slice does not add a workflow engine.
- Do not test broad semantic quality of skill prose with natural-language scoring; the spec explicitly forbids that in the first validation slice.
- Do not require every skill in the repository to normalize in this slice; Phase 2/3/4 skills are deferred.
- Do not require hosted CI observation for milestone proof unless a later stage actually observes hosted CI.
- Do not require external tools for Codex, Claude Code, or opencode smoke; repository-owned adapter checks cover non-smoke package validation.
- Do not snapshot entire skill files as the primary proof; exact shared-block drift checks are allowed only for adopted shared blocks.

## Uncovered gaps

- None. Nuanced prose quality remains manual review by design, not an uncovered automation gap.

## Next artifacts

- `implement` M1: define skill-contract static proof.

## Follow-on artifacts

- None yet.

## Readiness

Active proof-planning surface. The active plan owns the current execution handoff.
