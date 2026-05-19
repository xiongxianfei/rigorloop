# Skill Contract Test Spec

## Status

- active

## Related spec and plan

- Spec: [Skill Contract](skill-contract.md), approved after clean spec-review on 2026-05-08.
- Proposal: [Skill Contract Optimization](../docs/proposals/2026-05-08-skill-contract-optimization.md), accepted.
- Plan: [Skill Contract Optimization Execution Plan](../docs/plans/2026-05-08-skill-contract-optimization.md), active after clean plan-review.
- Current consuming proposal: [Single Workflow Lane, Explain-Change Before Verify, and Public Skill Surface Boundary](../docs/proposals/2026-05-08-single-workflow-lane-explain-before-verify.md), accepted.
- Current consuming plan: [Single Workflow Lane, Explain-Change Before Verify Execution Plan](../docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md), active after plan-review R2.
- Current amendment proposal: [RigorLoop Published Skill Design Contract](../docs/proposals/2026-05-19-rigorloop-published-skill-design-contract.md), accepted.
- Completed amendment plan: [RigorLoop Published Skill Design Contract Execution Plan](../docs/plans/2026-05-19-rigorloop-published-skill-design-contract.md), completed after PR #71 merged.
- Completed rollout plan: [Published Skill Design Spec Family Rollout](../docs/plans/2026-05-19-published-skill-design-spec-family.md), completed after PR #72 merged.
- Completed rollout plan: [Published Skill Design Implement And Code-Review Rollout](../docs/plans/2026-05-19-published-skill-design-implement-code-review.md), completed after PR #73 merged.
- Current rollout plan: [Published Skill Design Plan Family Rollout](../docs/plans/2026-05-19-published-skill-design-plan-family.md), active in final closeout after clean M3 code-review and explain-change.
- Architecture: not required. The approved slices change workflow-governance Markdown, canonical skill guidance, shared text blocks, static validation, generated skill mirrors, public adapter validation, and pilot skill wording. They do not add runtime components, storage, API boundaries, deployment boundaries, or a new validation architecture.
- Project map: `docs/project-map.md` is present and was read for repository orientation. This test spec relies on the approved spec, active plan, workflow specs, stage skills, shared templates, generator scripts, existing validator patterns, and change-local pilot evidence.
- Related proof surfaces:
  - `scripts/test-skill-validator.py`
  - `scripts/validate-skills.py`
  - `scripts/select-validation.py`
  - `scripts/build-skills.py`
  - `scripts/build-adapters.py`
  - `scripts/validate-adapters.py`
  - `scripts/measure-skill-tokens.py`
  - `scripts/test-adapter-distribution.py`
  - `scripts/ci.sh`

## Testing strategy

- Use contract and static wording checks because the approved first implementation slice is skill guidance and validator behavior, not a runtime workflow router.
- Use `scripts/test-skill-validator.py` for machine-checkable invariants in canonical skills, shared blocks, workflow summaries, public skill surface boundaries, and narrow forbidden-overclaim checks.
- Use `scripts/validate-skills.py` for authored skill structure after canonical skills are edited.
- Use selector-selected validation to prove changed spec, plan, skill, template, generated, adapter, and change-local paths are classified without unclassified paths.
- Use generated-output drift checks after canonical skill edits to prove `.codex/skills/` and public adapter packages remain derived output.
- Use manual contract review for nuanced prose boundaries: claim ownership, local handoff, preserving useful skill-specific guidance, avoiding hollow required sections, and preventing broad semantic quality scoring.
- Use change-local evidence for the published-skill design pilot: skill audit, routing coverage tables, behavior-preservation notes, behavior-parity evidence, and token-cost deltas.
- Use change-local evidence for the published-skill design spec-family rollout: skill audit, routing coverage tables, behavior-preservation notes, behavior-parity evidence, and token-cost deltas for `spec` and `spec-review`.
- Use change-local evidence for the published-skill design execution/review rollout: skill audit, routing coverage tables, behavior-preservation notes, behavior-parity evidence, and token-cost deltas for `implement` and `code-review`.
- Use change-local evidence for the published-skill design plan-family rollout: skill audit, routing coverage tables, behavior-preservation notes, behavior-parity evidence, and token-cost deltas for `plan` and `plan-review`.
- Do not add runtime workflow simulation, natural-language scoring, broad prose linting, a shared-block generation build step, a standalone `review-resolution` skill, or a `skills/ci-maintenance/SKILL.md` path.
- Do not claim routing fixtures prove deterministic model auto-selection unless a later approved routing harness exists.

## Requirement coverage map

| Requirement IDs | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `R1`, `R1a`, `R1b`, `R1c`, `R1d`, `R20`, `R20a`, `R20b` | `T1`, `T11`, `T13` | contract, manual | Normative source split and source-of-truth order |
| `R2`, `R2a`, `R2b`, `R2c`, `R2d` | `T9`, `T13` | integration, smoke | Canonical skills, generated mirrors, adapter output, and drift checks |
| `R3`, `R3a`, `R3b`, `R3c`, `R3d`, `R3e` | `T2`, `T14`, `T13` | integration, manual | Required core sections, conditional sections, public skill surface boundary, and preservation of useful local guidance |
| `R4`, `R4a` | `T2`, `T5` | manual, integration | Authoring skill output ownership and quality checklist expectations, within first-slice applicability |
| `R5`, `R5a`, `R5b` | `T4`, `T5`, `T7` | integration, manual | Review skill status/finding/recording contract and shared review recording preservation |
| `R6`, `R6a`, `R6b`, `R6c` | `T3`, `T4`, `T12` | integration, manual | Execution skill proof boundaries and `ci`/`ci-maintenance` naming split |
| `R7`, `R7a` | `T4`, `T11` | manual | `learn` and later support skills keep trigger/output/handoff boundaries |
| `R8`, `R8a`, `R8b`, `R8c`, `R8d`, `R8e`, `R8f`, `R8g`, `R8h` | `T2`, `T3`, `T4`, `T5`, `T6`, `T8`, `T9`, `T14` | integration, manual | First-slice scope, core sections, claims, result output, readiness wording, targeted reading, generated drift, and public surface cleanup |
| `R9`, `R9a`, `R9b`, `R9c`, `R9d` | `T3`, `T12` | manual, integration | Later-phase normalization order and optional skills remain out of scope |
| `R10`, `R10a`, `R10b`, `R10c`, `R10d`, `R10e`, `R10f` | `T4`, `T10`, `T13` | integration, manual | Claims this skill must not make and narrow overclaim checks |
| `R11`, `R11a`, `R11b`, `R11c` | `T5`, `T13` | integration, manual | Summary-first result output and common/optional fields |
| `R12`, `R12a`, `R12b`, `R12c` | `T5`, `T14`, `T13` | integration, manual | Local handoff, public workflow routing pointer, and isolated invocation boundary |
| `R13`, `R13a`, `R13b`, `R13c`, `R13d`, `R13e`, `R13f` | `T6`, `T13` | integration, manual | Progress, readiness, closeout, Done, and final closeout readiness wording |
| `R14`, `R14a`, `R14b`, `R14c`, `R14d`, `R14e` | `T7`, `T13` | integration, manual | Shared-block source, copy-and-check, authority boundary, and no generation v1 |
| `R15`, `R15a`, `R15b`, `R15c` | `T7`, `T14`, `T13` | integration, manual | First published shared-block set, contributor-only generated-output rule, and deferred shared blocks |
| `R16`, `R16a`, `R16b`, `R16c` | `T8`, `T13` | integration, manual | Evidence-reading guidance and full-file read escalation |
| `R17`, `R17a`, `R17b` | `T8`, `T13` | manual | Optional bounded examples and long-example exclusion |
| `R18`, `R18a`, `R18b`, `R18c`, `R18d` | `T10`, `T13` | integration, manual | Positive-first, narrow, incident-based validator strategy |
| `R19`, `R19a`, `R19b`, `R19c` | `T11`, `T13` | manual, integration | Minimum viable skill rule and guidance placement |
| `R21`-`R26` | `T15`, `T13` | integration, manual | Token-cost discipline amendment, bounded evidence, output caps, validation semantics, narrow static proof, and noisy-evidence process defects |
| `R27`, `R27a`, `R27b`, `R27c`, `R28`, `R28a`, `R28b` | `T16`, `T20` | manual, integration | Published skills as portable operating documentation and skill existence audit |
| `R29`, `R29a`, `R29b`, `R29c`, `R29d`, `R29e`, `R29f` | `T17`, `T19` | integration, manual | Description routing source, length cap, near misses, optional `when_to_use`, and routing coverage |
| `R30`, `R30a`, `R30b`, `R31`, `R31a`, `R31b`, `R31c`, `R31d`, `R34`, `R34a`, `R34b` | `T18`, `T20` | integration, manual | Workflow role, execution body, body routing boundary, output skeletons, examples, and hard-constraint discipline |
| `R32`, `R32a`, `R32b`, `R32c`, `R32d`, `R33`, `R33a`, `R33b`, `R33c` | `T18`, `T20` | integration, manual | Resource-map coverage and repository-root versus packaged-resource self-containment |
| `R35`, `R35a`, `R35b`, `R35c`, `R35d`, `R35e`, `R35f`, `R35g` | `T17`, `T19` | integration, manual | Routing fixtures, coverage tables, bounded phrase coverage, transcript review, and no runtime auto-selection CI claim |
| `R36`, `R36a`, `R36b`, `R36c`, `R36d`, `R36e`, `R36f`, `R36g`, `R36h`, `R36i`, `R36j` | `T16`, `T19`, `T20`, `T13` | integration, manual | Audit-first pilot scope, no merge/retire side effects, token-cost budget, preservation notes, parity evidence, and generated adapter validation |
| Spec-family rollout plan requirements | `T21`, `T22`, `T23`, `T24` | integration, manual, smoke | Approved follow-on rollout for `spec` and `spec-review`, preserving R27-R35 behavior and reusing R36 audit, preservation, parity, and token discipline without changing the original pilot boundary |
| Execution/review rollout plan requirements | `T25`, `T26`, `T27`, `T28` | integration, manual, smoke | Approved follow-on rollout for `implement` and `code-review`, preserving R27-R35 behavior and reusing R36 audit, preservation, parity, and token discipline without changing the original pilot boundary |
| Plan-family rollout plan requirements | `T29`, `T30`, `T31`, `T32` | integration, manual, smoke | Approved follow-on rollout for `plan` and `plan-review`, preserving R27-R35 behavior and reusing R36 audit, preservation, parity, and token discipline without changing the original pilot boundary |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| `E1` | `T4`, `T6` | `implement` may report implementation/validation and `code-review` handoff, but not review, branch, PR, or verify ownership |
| `E2` | `T3` | Non-first-slice skills remain valid until later phases |
| `E3` | `T7` | Shared block is copied verbatim and checked for drift |
| `E4` | `T9`, `T14` | Generated skill mirrors and adapter outputs stay derived, while public skills omit maintainer mechanics |
| `E5` | `T10` | Overclaim validation is narrow and positive-first |
| `E6` | `T11` | One-off behavior does not create a new skill |
| `E7` | `T3`, `T12` | `ci-maintenance` maps to existing `ci` skill entrypoint |
| `E8` | `T17`, `T19` | `description` carries portable routing before skill bodies load |
| `E9` | `T18` | Packaged scripts are allowed when mapped with load conditions and failure behavior |
| `E10` | `T18` | Repository-root scripts are blocked as normal customer-project dependencies |
| `E11` | `T19` | Routing fixtures are coverage and transcript evidence, not model-selection proof |
| `E12` | `T16`, `T20` | Audit records merge/retire candidates without acting on them |

## Edge case coverage

- EC1, existing skill has domain-specific section overlapping required core: `T2`
- EC2, skill is both authoring and execution oriented: `T2`, `T5`
- EC3, clean review output has no material findings: `T4`, `T7`
- EC4, shared block adopted by only one skill initially: `T7`
- EC5, normalized skill needs a short example: `T8`
- EC6, generated adapter path changes or selector path is concrete: `T9`
- EC7, final closeout readiness appears in negative guidance: `T10`
- EC8, optional Phase 4 skill is named but not approved: `T3`, `T12`
- EC9, skill ships no packaged resources: `T18`
- EC10, skill ships a rarely used packaged script: `T18`
- EC11, customer project has project-local workflow docs: `T18`
- EC12, prompt fixture suggests a competing skill: `T19`
- EC13, audit finds a retirement candidate: `T16`, `T20`
- EC14, body `When to use` section summarizes scope after load: `T17`, `T18`
- EC15, routing coverage depends on a phrase table: `T19`
- EC16, touched pilot skill moves behavior-significant wording: `T20`
- EC17, spec-family audit finds no validator changes are needed: `T21`, `T22`
- EC18, `spec-review` rewrite touches formal review recording language: `T23`
- EC19, spec-family token cost regresses after moving routing into `description`: `T23`, `T24`
- EC20, execution/review audit finds no validator changes are needed: `T25`, `T26`
- EC21, `code-review` rewrite touches material finding, recording, or downstream routing language: `T27`
- EC22, `implement` rewrite touches first-pass completeness or milestone handoff language: `T27`
- EC23, execution/review token cost regresses after moving routing into `description`: `T27`, `T28`
- EC24, plan-family audit finds no validator changes are needed: `T29`, `T30`
- EC25, `plan-review` rewrite touches formal review recording or downstream-blocking language: `T31`
- EC26, `plan` rewrite touches current handoff summary, upstream status settlement, or readiness-vs-Done language: `T31`
- EC27, plan-family token cost regresses after moving routing into `description`: `T31`, `T32`

## Acceptance criteria coverage map

| Acceptance criterion | Covered by |
| --- | --- |
| Skill contract source is identifiable | `T1`, `T13` |
| Skill-contract behavior is distinct from workflow-routing behavior | `T1`, `T5`, `T14` |
| Required core sections are identifiable | `T2` |
| First implementation slice is identifiable | `T3` |
| Later normalization phases are identifiable | `T3` |
| `ci` is the `ci-maintenance` entrypoint | `T3`, `T12` |
| Normalized skills include do-not-overclaim guidance | `T4`, `T10` |
| Skill outputs are summary-first | `T5` |
| Shared blocks are copied and drift-checked | `T7` |
| Generated output is regenerated, not hand-edited | `T9` |
| Published skills omit repository-maintainer internals | `T14` |
| Validator checks are positive-first, narrow, and not broad semantic scoring | `T10` |
| New skill justification is clear | `T11` |
| `description` is the required portable routing source and is capped at 1024 characters | `T17`, `T19` |
| Optional `when_to_use` metadata is not required and does not replace `description` | `T17` |
| Lifecycle skills with handoff, gate, artifact closeout, or downstream readiness responsibilities require `Workflow role` | `T18` |
| Skills with packaged resources include a resource map naming every packaged resource with a load condition | `T18` |
| Packaged skill-local scripts are distinguished from forbidden repository-root scripts | `T18` |
| Published-skill design pilot routing tests are bounded fixture and transcript evidence unless an approved harness exists | `T19` |
| Published-skill design pilot audit results do not directly merge, retire, rename, remove, or change ownership of skills | `T16`, `T20` |
| Pilot token-cost measurement uses the zero target, `+5%` rationale tolerance, and `+10%` hard cap | `T20` |
| Body `When to use` and `When not to use` sections do not replace `description` as the portable routing source | `T17`, `T18` |
| Routing coverage table exists for each changed published-skill design pilot skill | `T19` |
| Behavior-preservation note exists for each changed published-skill design pilot skill | `T20` |
| Behavior-parity evidence shows no weakening of material review status, finding format, recording obligations, stop conditions, validation obligations, or claim boundaries | `T20` |
| Spec-family rollout remains scoped to `skills/spec/SKILL.md` and `skills/spec-review/SKILL.md` for skill-body changes | `T21`, `T23` |
| Spec-family rollout creates audit, routing coverage, behavior-preservation, behavior-parity, and token evidence before skill-body rewrites close | `T21`, `T23` |
| Spec-family validator changes are deterministic, fixture-backed, and limited to gaps found by the audit or existing R27-R35 checks | `T22` |
| Spec-family generated skill and temporary adapter validation are run from canonical `skills/` without hand-editing generated public adapter bodies | `T24` |
| Execution/review rollout remains scoped to `skills/implement/SKILL.md` and `skills/code-review/SKILL.md` for skill-body changes | `T25`, `T27` |
| Execution/review rollout creates audit, routing coverage, behavior-preservation, behavior-parity, and token evidence before skill-body rewrites close | `T25`, `T27` |
| Execution/review validator changes are deterministic, fixture-backed, and limited to gaps found by the audit or existing R27-R35 checks | `T26` |
| Execution/review generated skill and temporary adapter validation are run from canonical `skills/` without hand-editing generated public adapter bodies | `T28` |
| Plan-family rollout remains scoped to `skills/plan/SKILL.md` and `skills/plan-review/SKILL.md` for skill-body changes | `T29`, `T31` |
| Plan-family rollout creates audit, routing coverage, behavior-preservation, behavior-parity, and token evidence before skill-body rewrites close | `T29`, `T31` |
| Plan-family validator changes are deterministic, fixture-backed, and limited to gaps found by the audit or existing R27-R35 checks | `T30` |
| Plan-family generated skill and temporary adapter validation are run from canonical `skills/` without hand-editing generated public adapter bodies | `T32` |

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
  - Assert `implement` does not claim review passed, clean review, branch-ready, PR-ready, or final closeout readiness.
  - Assert `code-review` does not claim branch-ready, PR-ready, CI passed, or verification passed.
  - Assert `verify` does not claim PR-ready, PR body ready, or review passed.
  - Assert `pr` links implementation, review, verification, and test claims to owning evidence rather than proving them itself.
  - Assert `plan` distinguishes Done, complete, ready for PR, and final closeout readiness from remaining gates.
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
  - Assert handoff sections name local normal and conditional next stages and route full workflow questions through the `workflow` skill or another user-facing workflow instruction surface.
  - Assert handoff sections do not point published skill users to this repository's internal workflow spec path.
  - Manually confirm no skill implies automatic downstream continuation for isolated invocations.
- Expected result:
  - Later agents can read a compact result first, while workflow routing remains owned by the user-facing workflow guidance.
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
  - Assert final closeout readiness is not described as Done, PR-ready, branch-ready, or full lifecycle completion.
  - Assert plans that mention final closeout readiness pair it with remaining completion gates when ambiguity is possible.
  - Confirm milestone closeout depends on the reviewed milestone state and generated-output refresh when applicable.
- Expected result:
  - A next-stage readiness line cannot be mistaken for final lifecycle completion.
- Failure proves:
  - The skill contract does not fix the known readiness/closeout confusion.
- Automation location:
  - `scripts/test-skill-validator.py`
  - manual plan and skill review during M3 and verify

### T7. Public shared blocks are canonical copied text with drift checks

- Covers: `R5b`, `R14`, `R14a`, `R14b`, `R14c`, `R14d`, `R14e`, `R15`, `R15a`, `R15b`, E3, EC3, EC4
- Level: integration, manual
- Fixture/setup:
  - `templates/shared/review-isolation-and-recording.md`
  - `templates/shared/evidence-collection-efficiency.md`
  - consuming first-slice skills
  - `scripts/test-skill-validator.py`
- Steps:
  - Assert the v1 public shared block source files exist for adopted stable rules.
  - Assert copied consuming skill subsections match the shared source verbatim when a block is adopted.
  - Assert shared blocks do not replace or outrank `specs/skill-contract.md` or `specs/rigorloop-workflow.md`.
  - Assert no build step generates shared blocks into skills in the first implementation slice.
  - Assert deferred shared blocks are not accidentally enforced.
  - Assert no unused `templates/shared/generated-output-handling.md` source remains.
- Expected result:
  - Public shared policy stays consistent where exact wording matters without introducing a new policy authority or generator, and maintainer-only generated-output guidance stays out of published skills.
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
  - Assert checks do not block explicit negative guidance, including "Do not set final closeout readiness from implement."
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

### T14. Published skills exclude repository-maintainer details

- Covers: `R3d`, `R3e`, `R8h`, `R12b`, `R15c`, E4
- Level: integration, manual
- Fixture/setup:
  - first-slice canonical skills
  - generated Codex skill mirrors
  - public adapter skill copies
  - `scripts/test-skill-validator.py`
- Steps:
  - Assert first-slice canonical skills do not include this repository's internal workflow spec path.
  - Assert first-slice canonical skills do not include canonical skill source paths, generated mirror paths, adapter package paths, selector path constraints, generated-output drift-check mechanics, or shared-block implementation details.
  - Assert generated mirrors and public adapter skill copies inherit the same public-surface cleanup from canonical skills.
  - Assert contributor-maintenance details remain available in contributor or governance surfaces instead of public skill text.
- Expected result:
  - Shipped skills explain how to operate the skill without exposing how this repository authors, validates, generates, or packages those skills.
- Failure proves:
  - Skill text remains a leaky repository-maintainer interface rather than a user-facing skill package surface.
- Automation location:
  - `scripts/test-skill-validator.py`
  - generated-output drift checks

### T15. Token-cost amendment and static proof stay narrow

- Covers: `R21`, `R21a`, `R21b`, `R22`, `R22a`, `R22b`, `R22c`, `R23`, `R23a`, `R23b`, `R24`, `R24a`, `R24b`, `R24c`, `R25`, `R25a`, `R25b`, `R25c`, `R25d`, `R26`, `R26a`, `R26b`
- Level: integration, manual
- Fixture/setup:
  - `specs/skill-contract.md`
  - `specs/skill-token-cost-optimization.md`
  - `scripts/test-skill-validator.py`
  - repository `skills/` tree
- Steps:
  - Assert the skill contract defines token-cost discipline as normalized skill behavior and an amendment to the existing skill contract.
  - Assert normalized skills that collect high-volume evidence prefer bounded evidence before broad reads.
  - Assert full-file-read and correctness obligations are preserved by existing evidence-reading requirements.
  - Assert output caps are safety rails, not evidence-selection strategy.
  - Assert summary-first and failure-focused output preserve validation semantics.
  - Assert static proof remains narrow and does not use broad natural-language quality scoring.
  - Assert no `skills/token-budget/SKILL.md` path exists or is required.
  - Manually confirm process-defect findings for noisy evidence cite the broad evidence surface and safer bounded strategy without reducing correctness checks.
- Expected result:
  - The token-cost contract is reviewable before canonical skill and generated-output updates begin.
- Failure proves:
  - Token-cost optimization is not anchored in the normative skill contract or the proof is too broad to review safely.
- Automation location:
  - `scripts/test-skill-validator.py`
  - manual review during M1 and code-review

### T16. Published skill existence audit and pilot scope

- Covers: `R27`, `R27a`, `R27b`, `R27c`, `R28`, `R28a`, `R28b`, `R36`, `R36a`, `R36b`, `R36c`, `R36d`, `R36e`, E12, EC13
- Level: manual, integration
- Fixture/setup:
  - `docs/changes/2026-05-19-rigorloop-published-skill-design-contract/skill-audit.md`
  - `docs/plans/2026-05-19-rigorloop-published-skill-design-contract.md`
  - repository `skills/` tree
- Steps:
  - Assert the audit covers current RigorLoop skills and classifies findings using the R36a categories.
  - Assert `proposal` and `proposal-review` are identified as the only pilot skill body edit targets.
  - Assert any merge or retire candidate is recorded only as a follow-on with skill name, reason, affected artifacts or gates, likely owner, and whether a separate proposal or spec amendment is required.
  - Assert the pilot does not merge, retire, rename, remove, or change ownership of any skill.
  - Manually confirm retained or changed pilot skills still earn their existence through a specialized workflow, artifact contract, gate, validation behavior, tool sequence, output shape, or trust boundary.
- Expected result:
  - The pilot starts from a reviewable audit and does not mutate skill inventory or ownership.
- Failure proves:
  - The change either lacks the required existence evidence or expands beyond the approved pilot scope.
- Automation location:
  - manual review during M1
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-19-rigorloop-published-skill-design-contract/change.yaml`
  - negative proof with `rg --files skills` when merge, retire, rename, removal, or ownership change is suspected

### T17. Description routing source and body routing boundary

- Covers: `R29`, `R29a`, `R29b`, `R29c`, `R29d`, `R29e`, `R29f`, `R31a`, E8, EC14
- Level: integration, manual
- Fixture/setup:
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
  - `scripts/skill_validation.py`
  - `scripts/test-skill-validator.py`
  - `tests/fixtures/skills/`
- Steps:
  - Assert each changed pilot skill has frontmatter `description` with capability and trigger contexts.
  - Assert important near-miss boundaries are present in `description` when the skill has competing skills or common false positives.
  - Assert `description` is `<= 1024` characters.
  - Assert required routing logic is present in `description`, not only in body `When to use`, body `When not to use`, or optional `when_to_use`.
  - Assert any optional `when_to_use` metadata does not replace or weaken `description`.
  - Assert body routing sections, when present, summarize scope, local stop conditions, or competing skills after load without becoming the primary routing source.
- Expected result:
  - Adapter skill listings can route from `description`, while the body executes the workflow after selection.
- Failure proves:
  - Published skill selection depends on unloaded body text, optional metadata, excessive descriptions, or duplicated routing prose.
- Automation location:
  - `scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - manual review during M2 and M3

### T18. Workflow role, output skeleton, resource map, and self-containment

- Covers: `R30`, `R30a`, `R30b`, `R31`, `R31b`, `R31c`, `R31d`, `R32`, `R32a`, `R32b`, `R32c`, `R32d`, `R33`, `R33a`, `R33b`, `R33c`, `R34`, `R34a`, `R34b`, E9, E10, EC9, EC10, EC11, EC14
- Level: integration, manual
- Fixture/setup:
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
  - any packaged pilot resources under `skills/proposal/` or `skills/proposal-review/`
  - `scripts/skill_validation.py`
  - `scripts/test-skill-validator.py`
  - `tests/fixtures/skills/`
- Steps:
  - Assert each changed lifecycle pilot skill includes `Workflow role` when it produces or closes an artifact, gates a stage, participates in handoff, or claims downstream readiness.
  - Assert `Workflow role` states lifecycle role, received input, produced output or status, and downstream claims the skill must not make.
  - Assert body instructions contain normal-path execution guidance, imperative procedure, output expectations, validation, and rationale where a judgment-affecting rule could be over-applied or under-applied.
  - Assert artifact-producing pilot skills include compact fenced output skeletons or reviewed equivalent templates, and examples do not replace normative skeletons.
  - If packaged `references/`, `scripts/`, or `assets/` exist, assert `Resource map` names every packaged resource with a load condition.
  - If a packaged script exists, assert the skill states when to run it, expected input, output or exit-code meaning, and failure behavior.
  - Assert skills without packaged resources are not required to include a "No bundled resources" line.
  - Assert self-containment validation blocks required customer-project dependencies on repository-root internal paths while allowing project-local docs, user-provided paths, packaged skill resources, and internal paths when operating inside this repository or when those paths are the target artifact.
  - Assert validators distinguish packaged skill-local `<skill>/scripts/` from forbidden repository-root `scripts/`.
- Expected result:
  - Pilot skill bodies execute the workflow, disclose optional resources only when needed, and remain portable for adapter users.
- Failure proves:
  - The pilot either lacks required workflow/output/resource contracts or requires unavailable maintainer-only repository context.
- Automation location:
  - `scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - manual review during M2 and M3

### T19. Routing fixtures and coverage tables stay deterministic

- Covers: `R35`, `R35a`, `R35b`, `R35c`, `R35d`, `R35e`, `R35f`, `R35g`, `R29f`, E11, EC12, EC15
- Level: integration, manual
- Fixture/setup:
  - `docs/changes/2026-05-19-rigorloop-published-skill-design-contract/routing-coverage.md`
  - prompt fixture data under `tests/fixtures/` or the change root when implementation creates it
  - `scripts/test-skill-validator.py`
- Steps:
  - Assert each changed pilot skill has a routing coverage table in the plan, test spec, change-local evidence, or fixture file.
  - Assert the table identifies positive triggers, near misses when relevant, competing skills when relevant, and should-not-trigger prompt classes.
  - Assert prompt fixtures cover obvious positives, casual positives, edge positives, near negatives, competing-skill prompts, and should-not-trigger prompts for each changed skill.
  - Assert static checks, if implemented, validate table presence and bounded phrase coverage only.
  - Assert validation and review evidence do not claim deterministic runtime skill auto-selection in CI unless a later approved routing harness defines that oracle.
  - Assert transcript review records under-triggering, over-triggering, or unnecessary resource loading observations when transcripts are available.
- Expected result:
  - Routing proof is deterministic, reviewable, and bounded to fixture and transcript evidence.
- Failure proves:
  - The pilot relies on broad semantic scoring, unsupported model-selection claims, or incomplete routing evidence.
- Automation location:
  - `scripts/test-skill-validator.py`
  - manual review during M1, M2, and M3

### T20. Behavior preservation, parity, token budget, and generated-output validation

- Covers: `R27b`, `R27c`, `R34a`, `R34b`, `R36b`, `R36c`, `R36d`, `R36e`, `R36f`, `R36g`, `R36h`, `R36i`, `R36j`, E12, EC13, EC16
- Level: integration, manual, smoke
- Fixture/setup:
  - `docs/changes/2026-05-19-rigorloop-published-skill-design-contract/behavior-preservation.md`
  - `docs/changes/2026-05-19-rigorloop-published-skill-design-contract/behavior-parity.md`
  - `docs/changes/2026-05-19-rigorloop-published-skill-design-contract/routing-coverage.md`
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
  - `scripts/measure-skill-tokens.py`
  - `scripts/build-skills.py`
  - `scripts/build-adapters.py`
  - `scripts/validate-adapters.py`
- Steps:
  - Assert each changed pilot skill has a behavior-preservation note identifying removed or rewritten behavior-significant wording, why the change is safe, and where the essential rule is preserved.
  - Assert behavior-parity evidence for representative proposal and proposal-review artifacts shows material review status, finding format, recording obligations, stop conditions, validation obligations, and claim boundaries were not weakened.
  - Assert structural validation alone is not used to close the pilot when behavior-significant wording changed.
  - Measure token cost for `proposal` and `proposal-review`; assert the recorded delta targets zero regression, requires rationale up to `+5%`, and blocks above `+10%` unless the spec changes.
  - Assert generated local skill output and public adapter validation come from canonical `skills/` and no generated public adapter body is hand-edited.
  - Assert the pilot does not rewrite all skills or act on merge/retire candidates.
- Expected result:
  - Pilot skill rewrites preserve lifecycle behavior, stay inside token budget, and keep generated outputs derived from canonical source.
- Failure proves:
  - The pilot may have weakened a lifecycle rule, exceeded the approved cost budget, or bypassed canonical generation boundaries.
- Automation location:
  - `python scripts/measure-skill-tokens.py --skills-root skills`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version v0.1.5 --output-dir <tmp-output>`
  - `python scripts/validate-adapters.py --root <tmp-output> --version v0.1.5`
  - `scripts/test-skill-validator.py`
  - manual behavior-parity review during M3

### T21. Spec-family audit and evidence scaffold

- Covers: approved spec-family rollout plan M1; `R27`, `R27a`, `R27b`, `R27c`, `R28`, `R28a`, `R28b`, `R29`, `R29a`, `R29b`, `R29c`, `R29d`, `R29e`, `R29f`, `R30`, `R30a`, `R31`, `R31a`, `R34`, `R35`, `R35a`, `R35e`, `R35f`, EC17
- Level: manual, integration
- Fixture/setup:
  - `skills/spec/SKILL.md`
  - `skills/spec-review/SKILL.md`
  - `docs/changes/2026-05-19-published-skill-design-spec-family/skill-audit.md`
  - `docs/changes/2026-05-19-published-skill-design-spec-family/routing-coverage.md`
  - `docs/changes/2026-05-19-published-skill-design-spec-family/behavior-preservation.md`
  - `docs/changes/2026-05-19-published-skill-design-spec-family/behavior-parity.md`
  - `docs/changes/2026-05-19-published-skill-design-spec-family/change.yaml`
- Steps:
  - Audit `spec` and `spec-review` descriptions, workflow-role blocks, output skeletons, stop conditions, body-routing boundaries, and self-containment wording before validator or skill-body changes rely on the evidence.
  - Record whether each skill earns its existence through a durable artifact contract, lifecycle procedure, review responsibility, output shape, validation behavior, or trust boundary.
  - Record routing coverage tables for each changed spec-family skill with positive triggers, near misses when relevant, competing skills when relevant, and should-not-trigger prompt classes.
  - Record behavior-preservation notes for behavior-significant wording that may be rewritten later.
  - Define representative spec and spec-review artifacts for behavior parity.
  - Record baseline static token estimates for `spec` and `spec-review`.
  - If the audit finds no deterministic validator gap, record that no-change result explicitly before bypassing M2 validator edits.
- Expected result:
  - Reviewers can inspect spec-family evidence before any `spec` or `spec-review` skill rewrite closes.
- Failure proves:
  - The rollout is changing lifecycle skill behavior without an auditable baseline or deterministic routing/preservation plan.
- Automation location:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-19-published-skill-design-spec-family/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-19-published-skill-design-spec-family.md --path docs/changes/2026-05-19-published-skill-design-spec-family/change.yaml`
  - manual review during M1

### T22. Spec-family deterministic validator and fixture support

- Covers: approved spec-family rollout plan M2; `R29`, `R29d`, `R29f`, `R31a`, `R32`, `R32a`, `R32b`, `R32c`, `R32d`, `R33`, `R33a`, `R33b`, `R33c`, `R35`, `R35c`, `R35d`, `R35e`, `R35f`, `R35g`, EC17
- Level: integration, manual
- Fixture/setup:
  - `scripts/skill_validation.py`
  - `scripts/test-skill-validator.py`
  - `tests/fixtures/skills/`
  - `docs/changes/2026-05-19-published-skill-design-spec-family/routing-coverage.md`
  - `docs/changes/2026-05-19-published-skill-design-spec-family/skill-audit.md`
- Steps:
  - Add or reuse focused validator fixtures only for deterministic spec-family gaps identified by `T21` or already required by R27-R35.
  - Assert description length, description routing source, body routing boundary, packaged-resource map, and self-containment checks remain static and phrase/path/table based.
  - Assert any routing fixture check validates coverage-table presence or bounded phrase coverage, not model auto-selection.
  - Assert repository-root internal paths remain blocked only when required as normal customer-project dependencies and packaged skill-local scripts remain allowed when mapped.
  - Assert no broad natural-language scoring, free-form semantic prose scoring, or runtime model-selection CI oracle is introduced.
- Expected result:
  - Deterministic validation supports the spec-family rewrite without overfitting prose or broadening the proof surface beyond the approved slice.
- Failure proves:
  - Validator changes either miss a concrete spec-family risk or become a brittle semantic quality gate.
- Automation location:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `bash scripts/ci.sh --mode explicit --path scripts/skill_validation.py --path scripts/test-skill-validator.py --path specs/skill-contract.test.md --path docs/changes/2026-05-19-published-skill-design-spec-family/change.yaml`
  - manual validator review during M2

### T23. Spec and spec-review skill rewrite preserves lifecycle behavior

- Covers: approved spec-family rollout plan M3; `R27`, `R27a`, `R27b`, `R27c`, `R29`, `R29a`, `R29b`, `R29c`, `R29d`, `R29e`, `R29f`, `R30`, `R30a`, `R31`, `R31a`, `R31b`, `R31c`, `R31d`, `R32`, `R32a`, `R32b`, `R32c`, `R32d`, `R33`, `R33a`, `R33b`, `R33c`, `R34`, `R34a`, `R34b`, `R35`, `R35a`, `R35b`, `R35c`, `R35d`, `R35e`, `R35f`, `R35g`, EC18, EC19
- Level: integration, manual
- Fixture/setup:
  - `skills/spec/SKILL.md`
  - `skills/spec-review/SKILL.md`
  - `docs/changes/2026-05-19-published-skill-design-spec-family/behavior-preservation.md`
  - `docs/changes/2026-05-19-published-skill-design-spec-family/behavior-parity.md`
  - `docs/changes/2026-05-19-published-skill-design-spec-family/routing-coverage.md`
  - `scripts/measure-skill-tokens.py`
- Steps:
  - Assert `spec` and `spec-review` frontmatter descriptions state capability and trigger contexts, include important near misses, avoid synonym dumping, and stay `<= 1024` characters.
  - Assert any optional `when_to_use` metadata does not replace description routing.
  - Assert bodies contain normal-path execution guidance and do not hide essential trigger logic absent from `description`.
  - Assert lifecycle role, received input, produced output or status, handoff boundary, and downstream claims the skill must not make are preserved or clarified.
  - Assert output skeletons remain compact and fenced, or a reviewed equivalent template is present.
  - Assert no required maintainer-only repository-root dependency is introduced; any packaged resources have explicit load conditions and script input/output/failure guidance.
  - Assert behavior-preservation evidence maps removed or rewritten behavior-significant wording to preserved essential rules.
  - Assert behavior-parity evidence shows no weakening of spec output shape, spec-review material finding format, review recording obligations, stop conditions, validation obligations, or claim boundaries.
  - Measure after-change token estimates for `spec` and `spec-review`, compare against the M1 baseline, and record rationale for material regression.
- Expected result:
  - `spec` and `spec-review` route more reliably, remain portable, and preserve lifecycle behavior while staying within the approved scoped rollout.
- Failure proves:
  - The skill rewrite changed behavior, weakened a formal review contract, introduced unavailable repository dependencies, or moved routing out of the portable description surface.
- Automation location:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/measure-skill-tokens.py --skills-root skills`
  - manual behavior-preservation and parity review during M3 and code-review

### T24. Spec-family generated output, adapter proof, and final selected validation

- Covers: approved spec-family rollout final proof; `R2`, `R2a`, `R2b`, `R2c`, `R2d`, `R24`, `R24a`, `R24b`, `R24c`, `R33c`, `R35c`, `R35d`
- Level: integration, smoke, manual
- Fixture/setup:
  - `skills/spec/SKILL.md`
  - `skills/spec-review/SKILL.md`
  - `specs/skill-contract.test.md`
  - `docs/plans/2026-05-19-published-skill-design-spec-family.md`
  - `docs/changes/2026-05-19-published-skill-design-spec-family/`
  - temporary adapter output directory for `v0.1.5`
- Steps:
  - Run canonical skill validation and validator regression tests after spec-family skill edits.
  - Run generated-skill drift checks from canonical `skills/`.
  - Build temporary adapter archives for `v0.1.5` into a temporary directory and validate them from that output.
  - Assert generated public adapter skill bodies are not hand-edited as tracked source.
  - Run change metadata, artifact lifecycle, whitespace, and selected CI commands for changed spec, plan, skill, script, fixture, and change-local paths.
  - Before PR handoff, assert explain-change, code-review closeout, verify, and PR readiness cite the actual validation commands rather than generic success claims.
- Expected result:
  - The spec-family rollout is proven from canonical skill source through generated skill and temporary adapter validation, with lifecycle evidence synchronized.
- Failure proves:
  - The rollout has stale generated output, missing adapter proof, unclassified validation paths, or unsynchronized lifecycle evidence.
- Automation location:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version v0.1.5 --output-dir <tmpdir>`
  - `python scripts/validate-adapters.py --root <tmpdir> --version v0.1.5`
  - `bash scripts/ci.sh --mode explicit --path skills/spec/SKILL.md --path skills/spec-review/SKILL.md --path specs/skill-contract.test.md --path docs/plans/2026-05-19-published-skill-design-spec-family.md --path docs/plan.md --path docs/changes/2026-05-19-published-skill-design-spec-family/change.yaml`

### T25. Execution/review audit and evidence scaffold

- Covers: approved execution/review rollout plan M1; `R27`, `R27a`, `R27b`, `R27c`, `R28`, `R28a`, `R28b`, `R29`, `R29a`, `R29b`, `R29c`, `R29d`, `R29e`, `R29f`, `R30`, `R30a`, `R31`, `R31a`, `R34`, `R35`, `R35a`, `R35e`, `R35f`, EC20, EC21, EC22
- Level: manual, integration
- Fixture/setup:
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `docs/changes/2026-05-19-published-skill-design-implement-code-review/skill-audit.md`
  - `docs/changes/2026-05-19-published-skill-design-implement-code-review/routing-coverage.md`
  - `docs/changes/2026-05-19-published-skill-design-implement-code-review/behavior-preservation.md`
  - `docs/changes/2026-05-19-published-skill-design-implement-code-review/behavior-parity.md`
  - `docs/changes/2026-05-19-published-skill-design-implement-code-review/change.yaml`
- Steps:
  - Audit `implement` and `code-review` descriptions, workflow-role blocks, output skeletons, stop conditions, body-routing boundaries, and self-containment wording before validator or skill-body changes rely on the evidence.
  - Record whether each skill earns its existence through lifecycle procedure, review responsibility, artifact contract, output shape, validation behavior, tool sequence, or trust boundary.
  - Record routing coverage tables for each changed execution/review skill with positive triggers, near misses when relevant, competing skills when relevant, and should-not-trigger prompt classes.
  - Record behavior-preservation notes for behavior-significant wording that may be rewritten later.
  - Define representative implementation handoff and first-pass code-review artifacts for behavior parity.
  - Record baseline static token estimates for `implement` and `code-review`.
  - If the audit finds no deterministic validator gap, record that no-change result explicitly before bypassing M2 validator edits.
- Expected result:
  - Reviewers can inspect execution/review evidence before any `implement` or `code-review` skill rewrite closes.
- Failure proves:
  - The rollout is changing high-risk lifecycle skill behavior without an auditable baseline or deterministic routing/preservation plan.
- Automation location:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-19-published-skill-design-implement-code-review/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-19-published-skill-design-implement-code-review.md --path docs/changes/2026-05-19-published-skill-design-implement-code-review/change.yaml`
  - manual review during M1

### T26. Execution/review deterministic validator and fixture support

- Covers: approved execution/review rollout plan M2; `R29`, `R29d`, `R29f`, `R31a`, `R32`, `R32a`, `R32b`, `R32c`, `R32d`, `R33`, `R33a`, `R33b`, `R33c`, `R35`, `R35c`, `R35d`, `R35e`, `R35f`, `R35g`, EC20
- Level: integration, manual
- Fixture/setup:
  - `scripts/skill_validation.py`
  - `scripts/test-skill-validator.py`
  - `tests/fixtures/skills/`
  - `docs/changes/2026-05-19-published-skill-design-implement-code-review/routing-coverage.md`
  - `docs/changes/2026-05-19-published-skill-design-implement-code-review/skill-audit.md`
- Steps:
  - Add or reuse focused validator fixtures only for deterministic execution/review gaps identified by `T25` or already required by R27-R35.
  - Assert description length, description routing source, body routing boundary, packaged-resource map, and self-containment checks remain static and phrase/path/table based.
  - Assert any routing fixture check validates coverage-table presence or bounded phrase coverage, not model auto-selection.
  - Assert repository-root internal paths remain blocked only when required as normal customer-project dependencies and packaged skill-local scripts remain allowed when mapped.
  - Assert no broad natural-language scoring, free-form semantic prose scoring, or runtime model-selection CI oracle is introduced.
- Expected result:
  - Deterministic validation supports the execution/review rewrite without overfitting prose or broadening the proof surface beyond the approved slice.
- Failure proves:
  - Validator changes either miss a concrete execution/review risk or become a brittle semantic quality gate.
- Automation location:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `bash scripts/ci.sh --mode explicit --path scripts/skill_validation.py --path scripts/test-skill-validator.py --path specs/skill-contract.test.md --path docs/changes/2026-05-19-published-skill-design-implement-code-review/change.yaml`
  - manual validator review during M2

### T27. Implement and code-review skill rewrite preserves lifecycle behavior

- Covers: approved execution/review rollout plan M3; `R27`, `R27a`, `R27b`, `R27c`, `R29`, `R29a`, `R29b`, `R29c`, `R29d`, `R29e`, `R29f`, `R30`, `R30a`, `R31`, `R31a`, `R31b`, `R31c`, `R31d`, `R32`, `R32a`, `R32b`, `R32c`, `R32d`, `R33`, `R33a`, `R33b`, `R33c`, `R34`, `R34a`, `R34b`, `R35`, `R35a`, `R35b`, `R35c`, `R35d`, `R35e`, `R35f`, `R35g`, EC21, EC22, EC23
- Level: integration, manual
- Fixture/setup:
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `docs/changes/2026-05-19-published-skill-design-implement-code-review/behavior-preservation.md`
  - `docs/changes/2026-05-19-published-skill-design-implement-code-review/behavior-parity.md`
  - `docs/changes/2026-05-19-published-skill-design-implement-code-review/routing-coverage.md`
  - `scripts/measure-skill-tokens.py`
- Steps:
  - Assert `implement` and `code-review` frontmatter descriptions state capability and trigger contexts, include important near misses, avoid synonym dumping, and stay `<= 1024` characters.
  - Assert any optional `when_to_use` metadata does not replace description routing.
  - Assert bodies contain normal-path execution guidance and do not hide essential trigger logic absent from `description`.
  - Assert lifecycle role, received input, produced output or status, handoff boundary, and downstream claims the skill must not make are preserved or clarified.
  - Assert `implement` preserves first-pass completeness, tests/proof first, validation layering, milestone state updates, plan update ownership, review-requested handoff, and no review/branch/PR readiness claims.
  - Assert `code-review` preserves independent-review mode, required first-pass review record, material finding shape, clean review receipt behavior, review-resolution routing, direct proof for named edge cases, and no verify/CI/PR readiness claims.
  - Assert output skeletons remain compact and fenced, or a reviewed equivalent template is present.
  - Assert no required maintainer-only repository-root dependency is introduced; any packaged resources have explicit load conditions and script input/output/failure guidance.
  - Assert behavior-preservation evidence maps removed or rewritten behavior-significant wording to preserved essential rules.
  - Assert behavior-parity evidence shows no weakening of implementation handoff state, validation obligations, material review status, finding format, review recording obligations, stop conditions, review-resolution routing, or claim boundaries.
  - Measure after-change token estimates for `implement` and `code-review`, compare against the M1 baseline, and record rationale for material regression.
- Expected result:
  - `implement` and `code-review` route more reliably, remain portable, and preserve lifecycle behavior while staying within the approved scoped rollout.
- Failure proves:
  - The skill rewrite changed behavior, weakened implementation or formal review contracts, introduced unavailable repository dependencies, or moved routing out of the portable description surface.
- Automation location:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/measure-skill-tokens.py --skills-root skills`
  - manual behavior-preservation and parity review during M3 and code-review

### T28. Execution/review generated output, adapter proof, and final selected validation

- Covers: approved execution/review rollout final proof; `R2`, `R2a`, `R2b`, `R2c`, `R2d`, `R24`, `R24a`, `R24b`, `R24c`, `R33c`, `R35c`, `R35d`
- Level: integration, smoke, manual
- Fixture/setup:
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `specs/skill-contract.test.md`
  - `docs/plans/2026-05-19-published-skill-design-implement-code-review.md`
  - `docs/changes/2026-05-19-published-skill-design-implement-code-review/`
  - temporary adapter output directory for `v0.1.5`
- Steps:
  - Run canonical skill validation and validator regression tests after execution/review skill edits.
  - Run generated-skill drift checks from canonical `skills/`.
  - Build temporary adapter archives for `v0.1.5` into a temporary directory and validate them from that output.
  - Assert generated public adapter skill bodies are not hand-edited as tracked source.
  - Run change metadata, artifact lifecycle, review artifact, whitespace, and selected CI commands for changed spec, plan, skill, script, fixture, and change-local paths.
  - Before PR handoff, assert explain-change, code-review closeout, verify, and PR readiness cite the actual validation commands rather than generic success claims.
- Expected result:
  - The execution/review rollout is proven from canonical skill source through generated skill and temporary adapter validation, with lifecycle evidence synchronized.
- Failure proves:
  - The rollout has stale generated output, missing adapter proof, unclassified validation paths, or unsynchronized lifecycle evidence.
- Automation location:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version v0.1.5 --output-dir <tmpdir>`
  - `python scripts/validate-adapters.py --root <tmpdir> --version v0.1.5`
  - `bash scripts/ci.sh --mode explicit --path skills/implement/SKILL.md --path skills/code-review/SKILL.md --path specs/skill-contract.test.md --path docs/plans/2026-05-19-published-skill-design-implement-code-review.md --path docs/plan.md --path docs/changes/2026-05-19-published-skill-design-implement-code-review/change.yaml`

### T29. Plan-family audit and evidence scaffold

- Covers: approved plan-family rollout plan M1; `R27`, `R27a`, `R27b`, `R27c`, `R28`, `R28a`, `R28b`, `R29`, `R29a`, `R29b`, `R29c`, `R29d`, `R29e`, `R29f`, `R30`, `R30a`, `R31`, `R31a`, `R34`, `R35`, `R35a`, `R35e`, `R35f`, EC24, EC25, EC26
- Level: manual, integration
- Fixture/setup:
  - `skills/plan/SKILL.md`
  - `skills/plan-review/SKILL.md`
  - `docs/changes/2026-05-19-published-skill-design-plan-family/skill-audit.md`
  - `docs/changes/2026-05-19-published-skill-design-plan-family/routing-coverage.md`
  - `docs/changes/2026-05-19-published-skill-design-plan-family/behavior-preservation.md`
  - `docs/changes/2026-05-19-published-skill-design-plan-family/behavior-parity.md`
  - `docs/changes/2026-05-19-published-skill-design-plan-family/change.yaml`
- Steps:
  - Audit `plan` and `plan-review` descriptions, workflow-role blocks, output skeletons, stop conditions, body-routing boundaries, and self-containment wording before validator or skill-body changes rely on the evidence.
  - Record whether each skill earns its existence through lifecycle procedure, formal review responsibility, artifact contract, output shape, validation behavior, or trust boundary.
  - Record routing coverage tables for each changed plan-family skill with positive triggers, near misses when relevant, competing skills when relevant, and should-not-trigger prompt classes.
  - Record behavior-preservation notes for behavior-significant wording that may be rewritten later.
  - Define representative plan and plan-review artifacts for behavior parity, including current handoff state and material finding outcomes.
  - Record baseline static token estimates for `plan` and `plan-review`.
  - If the audit finds no deterministic validator gap, record that no-change result explicitly before bypassing M2 validator edits.
- Expected result:
  - Reviewers can inspect plan-family evidence before any `plan` or `plan-review` skill rewrite closes.
- Failure proves:
  - The rollout starts from unreviewable assumptions, misses scope/routing/preservation risks, or changes skill bodies before evidence exists.
- Automation location:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-19-published-skill-design-plan-family/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-19-published-skill-design-plan-family.md --path docs/changes/2026-05-19-published-skill-design-plan-family/change.yaml --path docs/plan.md`
  - manual audit during M1

### T30. Plan-family deterministic validator and fixture support

- Covers: approved plan-family rollout plan M2; `R29`, `R29d`, `R29f`, `R31a`, `R32`, `R32a`, `R32b`, `R32c`, `R32d`, `R33`, `R33a`, `R33b`, `R33c`, `R35`, `R35c`, `R35d`, `R35e`, `R35f`, `R35g`, EC24
- Level: integration, manual
- Fixture/setup:
  - `scripts/skill_validation.py`
  - `scripts/test-skill-validator.py`
  - `tests/fixtures/skills/`
  - `docs/changes/2026-05-19-published-skill-design-plan-family/routing-coverage.md`
  - `docs/changes/2026-05-19-published-skill-design-plan-family/skill-audit.md`
- Steps:
  - Add or reuse focused validator fixtures only for deterministic plan-family gaps identified by `T29` or already required by R27-R35.
  - Assert description length, description routing source, body routing boundary, packaged-resource map, and self-containment checks remain static and phrase/path/table based.
  - Assert any routing fixture check validates coverage-table presence or bounded phrase coverage, not model auto-selection.
  - Assert repository-root internal paths remain blocked only when required as normal customer-project dependencies and packaged skill-local scripts remain allowed when mapped.
  - Assert no broad natural-language scoring, free-form semantic prose scoring, or runtime model-selection CI oracle is introduced.
- Expected result:
  - Deterministic validation supports the plan-family rewrite without overfitting prose or broadening the proof surface beyond the approved slice.
- Failure proves:
  - Validator changes either miss a concrete plan-family risk or become a brittle semantic quality gate.
- Automation location:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `bash scripts/ci.sh --mode explicit --path scripts/skill_validation.py --path scripts/test-skill-validator.py --path specs/skill-contract.test.md --path docs/changes/2026-05-19-published-skill-design-plan-family/change.yaml`
  - manual validator review during M2

### T31. Plan and plan-review skill rewrite preserves lifecycle behavior

- Covers: approved plan-family rollout plan M3; `R27`, `R27a`, `R27b`, `R27c`, `R29`, `R29a`, `R29b`, `R29c`, `R29d`, `R29e`, `R29f`, `R30`, `R30a`, `R31`, `R31a`, `R31b`, `R31c`, `R31d`, `R32`, `R32a`, `R32b`, `R32c`, `R32d`, `R33`, `R33a`, `R33b`, `R33c`, `R34`, `R34a`, `R34b`, `R35`, `R35a`, `R35b`, `R35c`, `R35d`, `R35e`, `R35f`, `R35g`, EC25, EC26, EC27
- Level: integration, manual
- Fixture/setup:
  - `skills/plan/SKILL.md`
  - `skills/plan-review/SKILL.md`
  - `docs/changes/2026-05-19-published-skill-design-plan-family/behavior-preservation.md`
  - `docs/changes/2026-05-19-published-skill-design-plan-family/behavior-parity.md`
  - `docs/changes/2026-05-19-published-skill-design-plan-family/routing-coverage.md`
  - `scripts/measure-skill-tokens.py`
- Steps:
  - Assert `plan` and `plan-review` frontmatter descriptions state capability and trigger contexts, include important near misses, avoid synonym dumping, and stay `<= 1024` characters.
  - Assert any optional `when_to_use` metadata does not replace description routing.
  - Assert bodies contain normal-path execution guidance and do not hide essential trigger logic absent from `description`.
  - Assert lifecycle role, received input, produced output or status, handoff boundary, and downstream claims the skill must not make are preserved or clarified.
  - Assert `plan` preserves active plan state ownership, upstream status settlement, milestone handoff, `docs/plan.md` lifecycle indexing, validation evidence, and readiness-vs-Done boundaries.
  - Assert `plan-review` preserves independent plan critique, formal review recording, material finding shape, blocked recording behavior, downstream-blocking semantics, and no implementation/verification claims.
  - Assert output skeletons remain compact and fenced, or a reviewed equivalent template is present.
  - Assert no required maintainer-only repository-root dependency is introduced; any packaged resources have explicit load conditions and script input/output/failure guidance.
  - Assert behavior-preservation evidence maps removed or rewritten behavior-significant wording to preserved essential rules.
  - Assert behavior-parity evidence shows no weakening of plan state ownership, formal review status, finding format, review recording obligations, stop conditions, validation obligations, or claim boundaries.
  - Measure after-change token estimates for `plan` and `plan-review`, compare against the M1 baseline, and record rationale for material regression.
- Expected result:
  - `plan` and `plan-review` route more reliably, remain portable, and preserve lifecycle behavior while staying within the approved scoped rollout.
- Failure proves:
  - The skill rewrite changed behavior, weakened planning or formal review contracts, introduced unavailable repository dependencies, or moved routing out of the portable description surface.
- Automation location:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/measure-skill-tokens.py --skills-root skills`
  - manual behavior-preservation and parity review during M3 and code-review

### T32. Plan-family generated output, adapter proof, and final selected validation

- Covers: approved plan-family rollout final proof; `R2`, `R2a`, `R2b`, `R2c`, `R2d`, `R24`, `R24a`, `R24b`, `R24c`, `R33c`, `R35c`, `R35d`
- Level: integration, smoke, manual
- Fixture/setup:
  - `skills/plan/SKILL.md`
  - `skills/plan-review/SKILL.md`
  - `specs/skill-contract.test.md`
  - `docs/plans/2026-05-19-published-skill-design-plan-family.md`
  - `docs/changes/2026-05-19-published-skill-design-plan-family/`
  - temporary adapter output directory for `v0.1.5`
- Steps:
  - Run canonical skill validation and validator regression tests after plan-family skill edits.
  - Run generated-skill drift checks from canonical `skills/`.
  - Build temporary adapter archives for `v0.1.5` into a temporary directory and validate them from that output.
  - Assert generated public adapter skill bodies are not hand-edited as tracked source.
  - Run change metadata, artifact lifecycle, review artifact, whitespace, and selected CI commands for changed spec, plan, skill, script, fixture, and change-local paths.
  - Before PR handoff, assert explain-change, code-review closeout, verify, and PR readiness cite the actual validation commands rather than generic success claims.
- Expected result:
  - The plan-family rollout is proven from canonical skill source through generated skill and temporary adapter validation, with lifecycle evidence synchronized.
- Failure proves:
  - The rollout has stale generated output, missing adapter proof, unclassified validation paths, or unsynchronized lifecycle evidence.
- Automation location:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version v0.1.5 --output-dir <tmpdir>`
  - `python scripts/validate-adapters.py --root <tmpdir> --version v0.1.5`
  - `bash scripts/ci.sh --mode explicit --path skills/plan/SKILL.md --path skills/plan-review/SKILL.md --path specs/skill-contract.test.md --path docs/plans/2026-05-19-published-skill-design-plan-family.md --path docs/plan.md --path docs/changes/2026-05-19-published-skill-design-plan-family/change.yaml`

## Fixtures and data

- No new external fixtures or runtime data are required.
- Static tests use canonical repository files as fixtures:
  - approved spec and active test spec under `specs/`;
  - first-slice canonical skills under `skills/`;
  - published-skill design pilot skills `skills/proposal/SKILL.md` and `skills/proposal-review/SKILL.md`;
  - shared blocks under `templates/shared/`;
  - generated mirrors under `.codex/skills/`;
  - public adapter output under `dist/adapters/`;
  - active plan and change-local metadata under `docs/`.
- Change-local pilot evidence uses:
  - `docs/changes/2026-05-19-rigorloop-published-skill-design-contract/skill-audit.md`;
  - `docs/changes/2026-05-19-rigorloop-published-skill-design-contract/routing-coverage.md`;
  - `docs/changes/2026-05-19-rigorloop-published-skill-design-contract/behavior-preservation.md`;
  - `docs/changes/2026-05-19-rigorloop-published-skill-design-contract/behavior-parity.md`.
- Change-local spec-family evidence uses:
  - `docs/changes/2026-05-19-published-skill-design-spec-family/skill-audit.md`;
  - `docs/changes/2026-05-19-published-skill-design-spec-family/routing-coverage.md`;
  - `docs/changes/2026-05-19-published-skill-design-spec-family/behavior-preservation.md`;
  - `docs/changes/2026-05-19-published-skill-design-spec-family/behavior-parity.md`.
- Change-local execution/review evidence uses:
  - `docs/changes/2026-05-19-published-skill-design-implement-code-review/skill-audit.md`;
  - `docs/changes/2026-05-19-published-skill-design-implement-code-review/routing-coverage.md`;
  - `docs/changes/2026-05-19-published-skill-design-implement-code-review/behavior-preservation.md`;
  - `docs/changes/2026-05-19-published-skill-design-implement-code-review/behavior-parity.md`.
- Change-local plan-family evidence uses:
  - `docs/changes/2026-05-19-published-skill-design-plan-family/skill-audit.md`;
  - `docs/changes/2026-05-19-published-skill-design-plan-family/routing-coverage.md`;
  - `docs/changes/2026-05-19-published-skill-design-plan-family/behavior-preservation.md`;
  - `docs/changes/2026-05-19-published-skill-design-plan-family/behavior-parity.md`.
- Any temporary fixture for validator failure cases should live under existing test fixture roots such as `tests/fixtures/skills/` and must not reference machine-local paths.

## Mocking/stubbing policy

- Do not mock repository-owned validation commands for milestone closeout.
- Unit-level validator tests may use small fixture skill trees for negative cases when the production skill files should remain valid.
- Generated-output tests may use temporary output roots when helper-level tests need stale, missing, or unexpected generated files.
- Do not stub `scripts/build-skills.py --check`, `scripts/build-adapters.py --version 0.1.1 --check`, `scripts/validate-adapters.py --version 0.1.1`, or `scripts/ci.sh` in final milestone proof.
- For the current published-skill design pilot, do not stub `scripts/build-skills.py --check`, `scripts/build-adapters.py --check`, `scripts/validate-adapters.py --version 0.1.4`, `scripts/measure-skill-tokens.py --skills-root skills`, or `scripts/ci.sh` when those commands are used as final milestone proof.
- For the spec-family rollout, do not stub `scripts/build-skills.py --check`, `scripts/build-adapters.py --version v0.1.5 --output-dir <tmpdir>`, `scripts/validate-adapters.py --root <tmpdir> --version v0.1.5`, `scripts/measure-skill-tokens.py --skills-root skills`, or `scripts/ci.sh` when those commands are used as final milestone proof.
- For the execution/review rollout, do not stub `scripts/build-skills.py --check`, `scripts/build-adapters.py --version v0.1.5 --output-dir <tmpdir>`, `scripts/validate-adapters.py --root <tmpdir> --version v0.1.5`, `scripts/measure-skill-tokens.py --skills-root skills`, or `scripts/ci.sh` when those commands are used as final milestone proof.
- For the plan-family rollout, do not stub `scripts/build-skills.py --check`, `scripts/build-adapters.py --version v0.1.5 --output-dir <tmpdir>`, `scripts/validate-adapters.py --root <tmpdir> --version v0.1.5`, `scripts/measure-skill-tokens.py --skills-root skills`, or `scripts/ci.sh` when those commands are used as final milestone proof.

## Migration or compatibility tests

- Existing unnormalized skills remain valid until later phases: `T3`, `T12`.
- Existing `skills/ci/SKILL.md` remains the `ci-maintenance` entrypoint: `T3`, `T12`.
- Generated `.codex/skills/` and `dist/adapters/` output remain derived and deterministic: `T9`, `T13`.
- Rollback for wording-only skill changes reverts canonical skills, shared blocks, validator checks, and generated output together; manual recovery review is covered by `T13`.
- Existing skills outside `proposal` and `proposal-review` remain valid until their approved implementation slice: `T16`, `T20`.
- Existing skills outside `spec` and `spec-review` remain valid during the spec-family rollout unless a reviewed plan revision changes scope: `T21`, `T23`.
- Existing skills outside `implement` and `code-review` remain valid during the execution/review rollout unless a reviewed plan revision changes scope: `T25`, `T27`.
- Existing skills outside `plan` and `plan-review` remain valid during the plan-family rollout unless a reviewed plan revision changes scope: `T29`, `T31`.
- Optional `when_to_use` remains compatible where supported but does not replace `description`: `T17`.
- Packaged skill-local resources remain allowed when mapped and included in adapter output, while repository-root internal paths remain blocked as normal customer-project dependencies: `T18`.

## Observability verification

- No runtime logs, metrics, traces, or audit events are required.
- Validation output should identify failed required sections, shared-block drift, generated-output drift, selector classification gaps, and overclaim checks clearly enough for maintainers to fix them: `T7`, `T9`, `T10`, `T13`.
- Published-skill design validation output should identify description-length failures, missing trigger contexts, missing near-miss boundaries, missing resource-map entries, unavailable repository-root dependencies, and routing fixture coverage gaps by stable check ID when those checks are implemented: `T17`, `T18`, `T19`.
- Spec-family validation output should identify deterministic `spec` and `spec-review` failures by stable check ID or fixture expectation when those checks are implemented: `T22`, `T23`.
- Execution/review validation output should identify deterministic `implement` and `code-review` failures by stable check ID or fixture expectation when those checks are implemented: `T26`, `T27`.
- Plan-family validation output should identify deterministic `plan` and `plan-review` failures by stable check ID or fixture expectation when those checks are implemented: `T30`, `T31`.
- Review and verification artifacts should cite concrete commands and results, not generic success claims: `T13`.

## Security/privacy verification

- Static and generated-output changes must not commit secrets, credentials, tokens, private keys, private user data, or unjustified machine-local paths: `T12`.
- Evidence-reading guidance must not encourage pasting sensitive logs or secrets into skill output: `T8`, `T12`.
- Adapter output remains generated proof surface, not an independent source of truth: `T9`, `T12`.
- Published skills must not instruct users to expose secrets, credentials, proxy URLs, private hostnames, tokens, private keys, or raw environment values while using packaged resources or scripts: `T18`.

## Performance checks

- Skill-contract validation remains static and repository-local in the first implementation slice: `T10`, `T13`.
- Skill-contract validation remains static and repository-local in the published-skill design pilot: `T17`, `T18`, `T19`, `T20`.
- Skill-contract validation remains static and repository-local in the spec-family rollout: `T21`, `T22`, `T23`, `T24`.
- Skill-contract validation remains static and repository-local in the execution/review rollout: `T25`, `T26`, `T27`, `T28`.
- Skill-contract validation remains static and repository-local in the plan-family rollout: `T29`, `T30`, `T31`, `T32`.
- No broad natural-language quality scoring is added: `T10`, `T19`, `T22`, `T23`, `T26`, `T27`, `T30`, `T31`.
- Evidence-reading guidance should reduce broad reads by preferring targeted summaries, IDs, headings, paths, counts, and line citations: `T8`.
- Broad smoke is not required unless triggered by selector, plan, test spec, review-resolution, release metadata, or explicit reviewer requirement: `T13`.
- The pilot token-cost budget is measured for `proposal` and `proposal-review` before rollout expands: `T20`.
- The spec-family rollout measures token estimates for `spec` and `spec-review` before and after the rewrite and records rationale for material regression: `T21`, `T23`.
- The execution/review rollout measures token estimates for `implement` and `code-review` before and after the rewrite and records rationale for material regression: `T25`, `T27`.
- The plan-family rollout measures token estimates for `plan` and `plan-review` before and after the rewrite and records rationale for material regression: `T29`, `T31`.

## Manual QA checklist

- Confirm first-slice skill changes are smaller and easier to scan, not merely reorganized into longer files.
- Confirm every required core section has actionable content and no hollow filler.
- Confirm no useful domain-specific section is removed from a skill without an equivalent local instruction.
- Confirm the result block shape is adapted to skill type without losing the common handoff fields.
- Confirm handoff guidance stays local and routes full workflow questions through user-facing workflow guidance, not this repository's internal workflow spec path.
- Confirm published skills do not expose repository-maintainer source paths, generated mirror paths, adapter paths, selector path constraints, drift-check mechanics, or shared-block implementation details.
- Confirm generated-output selector validation uses concrete generated files, not `--path dist/adapters`.
- Confirm pilot skill descriptions route from `description` without relying on body-only trigger logic or optional `when_to_use`.
- Confirm routing coverage tables name positive triggers, near misses, competing skills, and should-not-trigger prompt classes for both pilot skills.
- Confirm behavior-preservation notes cite where every moved or rewritten essential rule now lives.
- Confirm behavior-parity evidence covers material review status, finding format, recording obligations, stop conditions, validation obligations, and claim boundaries.
- Confirm spec-family evidence exists before the `spec` and `spec-review` rewrites close.
- Confirm `spec-review` material-finding and formal review recording obligations are preserved after rewrite.
- Confirm temporary adapter validation uses generated output from canonical `skills/spec` and `skills/spec-review`, not hand-edited generated bodies.
- Confirm execution/review evidence exists before the `implement` and `code-review` rewrites close.
- Confirm `implement` first-pass completeness, milestone handoff, plan update ownership, and no review/branch/PR readiness claims are preserved after rewrite.
- Confirm `code-review` independent-review mode, material finding shape, clean review receipt behavior, direct-proof expectations, and review-resolution routing are preserved after rewrite.
- Confirm temporary adapter validation uses generated output from canonical `skills/implement` and `skills/code-review`, not hand-edited generated bodies.
- Confirm plan-family evidence exists before the `plan` and `plan-review` rewrites close.
- Confirm `plan` current handoff summary, upstream status settlement, active plan ownership, and readiness-vs-Done boundaries are preserved after rewrite.
- Confirm `plan-review` formal review recording, material finding shape, blocked recording behavior, and downstream-blocking semantics are preserved after rewrite.
- Confirm temporary adapter validation uses generated output from canonical `skills/plan` and `skills/plan-review`, not hand-edited generated bodies.

## What not to test and why

- Do not test runtime workflow routing; this slice does not add a workflow engine.
- Do not test broad semantic quality of skill prose with natural-language scoring; the spec explicitly forbids that in the first validation slice.
- Do not test deterministic model auto-selection for published-skill routing unless a later approved routing harness defines that oracle.
- Do not require every skill in the repository to normalize in this slice; Phase 2/3/4 skills are deferred.
- Do not require every skill in the repository to satisfy R27-R36 in this pilot; the published-skill design pilot changes only `proposal`, `proposal-review`, validator support needed for the pilot, and generated adapter validation for changed skills.
- Do not treat the spec-family rollout as a change to the original pilot boundary in `R36b`; this rollout is separately scoped by the approved spec-family plan to `spec` and `spec-review`.
- Do not treat the execution/review rollout as a change to the original pilot boundary in `R36b`; this rollout is separately scoped by the approved execution/review plan to `implement` and `code-review`.
- Do not treat the plan-family rollout as a change to the original pilot boundary in `R36b`; this rollout is separately scoped by the approved plan-family plan to `plan` and `plan-review`.
- Do not require deterministic validator changes in M2 if M1 records that existing validation already covers the deterministic spec-family risks.
- Do not require deterministic validator changes in M2 if M1 records that existing validation already covers the deterministic execution/review risks.
- Do not require deterministic validator changes in M2 if M1 records that existing validation already covers the deterministic plan-family risks.
- Do not require hosted CI observation for milestone proof unless a later stage actually observes hosted CI.
- Do not require external tools for Codex, Claude Code, or opencode smoke; repository-owned adapter checks cover non-smoke package validation.
- Do not snapshot entire skill files as the primary proof; exact shared-block drift checks are allowed only for adopted shared blocks.

## Uncovered gaps

- None. Nuanced prose quality remains manual review by design, not an uncovered automation gap.

## Next artifacts

- Current rollout: final `verify`, then `pr` handoff under [Published Skill Design Plan Family Rollout](../docs/plans/2026-05-19-published-skill-design-plan-family.md).
- Historical carried context: the merged spec-family rollout used `T21`-`T24` for `spec` and `spec-review`.
- Historical carried context: the merged execution/review rollout used `T25`-`T28` for `implement` and `code-review`.
- Historical carried context: the merged published-skill design pilot used `T16`-`T20` for `proposal` and `proposal-review`.

## Follow-on artifacts

- None yet.

## Readiness

Active proof-planning surface for public skill portability, claim-boundary checks, the merged published-skill design pilot, the completed spec-family rollout, the completed execution/review rollout, and the plan-family rollout. The Published Skill Design Plan Family Rollout plan owns the current execution handoff through final `verify`, then `pr`.
