# Skill Token Cost Optimization Test Spec

## Status

- active

## Related spec and plan

- Spec: [Skill Token Cost Optimization](skill-token-cost-optimization.md), approved after clean spec-review on 2026-05-09.
- Proposal: [Skill Token Cost Optimization](../docs/proposals/2026-05-09-skill-token-cost-optimization.md), accepted.
- Plan: [Skill Token Cost Optimization Execution Plan](../docs/plans/2026-05-09-skill-token-cost-optimization.md), active after plan-review R1 resolution and clean architecture-review.
- Architecture: no runtime architecture impact. The approved spec records a no-impact rationale, and architecture-review approved it on 2026-05-09 with no material findings.
- Project map: `docs/project-map.md` is absent. This test spec does not rely on project-map claims; proof uses the approved spec, active plan, skill contract, selected canonical skills, shared evidence block, generated output, adapter validators, and existing repo-owned validation patterns.
- Related proof surfaces:
  - `specs/skill-contract.md`
  - `specs/skill-contract.test.md`
  - `templates/shared/evidence-collection-efficiency.md`
  - selected `skills/*/SKILL.md`
  - `scripts/test-skill-validator.py`
  - `scripts/validate-skills.py`
  - `scripts/build-skills.py`
  - `scripts/build-adapters.py`
  - `scripts/validate-adapters.py`
  - `scripts/test-adapter-distribution.py`
  - `scripts/ci.sh`

## Testing strategy

- Use contract and static wording checks because the approved behavior changes skill guidance, skill-contract text, validation coverage, and generated public skill output, not runtime workflow execution.
- Use `scripts/test-skill-validator.py` for stable phrase, section, and requirement coverage checks in the skill contract, shared evidence guidance, selected canonical skills, and public-surface portability rules.
- Use `scripts/validate-skills.py` for authored skill structure and frontmatter validity after canonical skill edits.
- Use generated-output drift checks after canonical skill changes to prove `.codex/skills/` remains derived output.
- Use adapter drift, adapter validation, and adapter distribution tests when public skill text changes.
- Use manual contract review for nuanced correctness boundaries: bounded evidence must not become under-reading, output caps must not become query design, validation semantics must not weaken, and process-defect findings must cite a safer bounded alternative.
- Do not add broad natural-language quality scoring, runtime workflow simulation, token-count scoring, or a standalone `token-budget` skill.

## Requirement coverage map

| Requirement IDs | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `R1`, `R1a`, `R1b` | `T1`, `T9` | contract, manual | Token-cost discipline becomes a skill-contract amendment without changing workflow gates. |
| `R2`, `R2a`, `R2b`, `R2c` | `T2`, `T5`, `T9` | integration, manual | Bounded evidence comes before broad reads on high-volume surfaces. |
| `R3`, `R3a`-`R3f` | `T3`, `T5`, `T9` | integration, manual | Full-file-read escape conditions and correctness priority remain explicit. |
| `R4`, `R4a`, `R4b` | `T4`, `T5`, `T9` | integration, manual | Output caps are safety rails, not query strategy. |
| `R5`, `R5a`-`R5c` | `T6`, `T9` | integration, manual | Summary-first and failure-focused output preserve validation semantics. |
| `R6`, `R6a`-`R6e` | `T1`, `T7`, `T9` | integration, manual | First implementation slice updates the contract, tests, selected skills, and no new token-budget skill. |
| `R7`, `R7a`-`R7c` | `T8`, `T10` | integration, manual | Published skill wording stays project-portable while maintainer commands stay internal. |
| `R8`, `R8a`-`R8d` | `T1`, `T2`, `T3`, `T4`, `T9` | integration, manual | Static validation is narrow and preserves escape-condition and output-cap distinctions. |
| `R9`, `R9a`-`R9c` | `T10`, `T11` | smoke, integration | Generated skill output and public adapters remain deterministic derived output. |
| `R10`, `R10a`, `R10b` | `T12`, `T9` | manual, integration | Reviewers can report noisy evidence collection without reducing correctness checks. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| `E1` | `T2`, `T9` | Proposal-context guidance uses known paths, heading searches, stable IDs, and targeted ranges before broad repository scans. |
| `E2` | `T3`, `T9` | Whole-artifact review still requires full-file or whole-section reading. |
| `E3` | `T4`, `T9` | Output caps do not excuse broad first-pass commands. |
| `E4` | `T6`, `T11` | Validation commands keep check coverage and expose focused detail when summaries are insufficient. |
| `E5` | `T8`, `T10` | Public skill wording uses project-portable surfaces and excludes maintainer-only paths and mechanics. |

## Edge case coverage

- EC1, short artifact is the smallest sufficient surface: `T3`, `T9`.
- EC2, generated-output tree is the review target: `T10`, `T11`.
- EC3, command failure output needs focused diagnostic detail: `T6`, `T11`.
- EC4, user explicitly asks for full command output: `T6`, manual review.
- EC5, bounded search terms are noisy: `T2`, `T4`, manual review.
- EC6, exact wording in a governing artifact changes: `T1`, `T3`, `T9`.
- EC7, public skill text needs validation wording: `T8`, `T10`.
- EC8, process-defect finding needs reconstruction: `T12`.

## Acceptance criteria coverage map

| Acceptance criterion | Covered by |
| --- | --- |
| Skill-contract amendment is identifiable | `T1`, `T9` |
| Correctness outranks token savings | `T3`, `T9` |
| Bounded-evidence-first behavior is identifiable | `T2`, `T5`, `T9` |
| Full-file-read escape conditions are identifiable | `T3`, `T9` |
| Output caps are not query design | `T4`, `T9` |
| Validation semantics are not weakened | `T6`, `T11` |
| First-slice skills are identifiable | `T7`, `T9` |
| No standalone token-budget skill is required | `T7` |
| Public skill wording remains project-portable | `T8`, `T10` |
| Static validation is narrow and not semantic scoring | `T1`, `T4`, `T9` |
| Generated skill drift, adapter drift, and adapter validation are required | `T10`, `T11` |

## Test cases

### T1. Skill contract records the token-cost amendment

- Covers: `R1`, `R1a`, `R1b`, `R6a`, `R6b`, `R8`, `R8a`
- Level: integration, manual
- Fixture/setup:
  - `specs/skill-contract.md`
  - `specs/skill-contract.test.md`
  - `scripts/test-skill-validator.py`
- Steps:
  - Assert `specs/skill-contract.md` states token-cost discipline as part of normalized skill behavior.
  - Assert the amendment is part of the existing skill contract, not a new workflow stage.
  - Assert skill-contract tests or validator tests cover bounded evidence, escape conditions, output-cap distinction, and unchanged validation semantics.
  - Manually confirm the amendment does not reduce artifact, review, validation, or workflow stage obligations.
- Expected result:
  - Reviewers can identify the normative token-cost behavior and its proof surface without a new stage.
- Failure proves:
  - Token-cost optimization lacks a stable contract or weakens lifecycle obligations.
- Automation location:
  - `scripts/test-skill-validator.py`
  - `specs/skill-contract.test.md`

### T2. High-volume evidence guidance prefers bounded evidence first

- Covers: `R2`, `R2a`, `R2b`, `R2c`, `R8a`, `E1`, EC5
- Level: integration, manual
- Fixture/setup:
  - `templates/shared/evidence-collection-efficiency.md`
  - selected first-slice canonical skills
  - `scripts/test-skill-validator.py`
- Steps:
  - Assert the shared evidence guidance names bounded evidence examples, including inventories, changed paths, headings, stable IDs, requirement IDs, test IDs, check IDs, path lists, counts, matching line numbers, diffs, and targeted excerpts.
  - Assert selected skills guide agents to broaden only when bounded evidence is insufficient.
  - Assert selected skills do not present broad recursive search, generated-output dumps, validation-log dumps, or full-file reads as the default first step for high-volume surfaces.
  - Manually confirm noisy search examples route to narrower next queries rather than repeated broad searches with output caps.
- Expected result:
  - High-volume evidence collection starts narrow and broadens for correctness when needed.
- Failure proves:
  - The implementation preserves the behavior that caused excessive context use.
- Automation location:
  - `scripts/test-skill-validator.py`
  - manual review during M2

### T3. Full-file-read escape conditions and correctness priority remain intact

- Covers: `R3`, `R3a`, `R3b`, `R3c`, `R3d`, `R3e`, `R3f`, `R8b`, `E2`, EC1, EC6
- Level: integration, manual
- Fixture/setup:
  - `specs/skill-contract.md`
  - `templates/shared/evidence-collection-efficiency.md`
  - selected review and implementation skills
- Steps:
  - Assert the guidance requires full-file or broader-section reads when the whole file is the target, relevant sections cannot be isolated safely, surrounding context can change the conclusion, bounded searches conflict or are incomplete, or behavior-changing edits depend on the whole source-of-truth artifact.
  - Assert token-cost guidance states or preserves that correctness outranks token savings.
  - Manually review spec-review, code-review, verify, and implement guidance to confirm they cannot rely only on search snippets when whole-artifact review is required.
- Expected result:
  - Token-cost discipline cannot be used as an excuse for under-reading.
- Failure proves:
  - The optimization trades correctness for token savings.
- Automation location:
  - `scripts/test-skill-validator.py`
  - manual review during M1 and M2

### T4. Output caps stay safety rails rather than query design

- Covers: `R4`, `R4a`, `R4b`, `R8c`, `E3`, EC5
- Level: integration, manual
- Fixture/setup:
  - `specs/skill-contract.md`
  - `templates/shared/evidence-collection-efficiency.md`
  - selected canonical skills
  - `scripts/test-skill-validator.py`
- Steps:
  - Assert skill-contract or shared guidance says output caps are safety rails, not evidence-selection strategy.
  - Assert guidance names low-volume strategies such as filename-first searches, count-first searches, precise globs, stable IDs, and targeted range reads where appropriate.
  - Assert no selected skill implies that setting an output cap makes a broad query acceptable as the normal first pass.
- Expected result:
  - Output caps limit accidental verbosity but do not replace precise evidence selection.
- Failure proves:
  - Agents can continue broad scans and hide the cost behind truncation.
- Automation location:
  - `scripts/test-skill-validator.py`
  - manual review during M1 and M2

### T5. Selected high-volume skills adopt bounded-evidence behavior

- Covers: `R2`, `R2a`, `R2b`, `R2c`, `R3`, `R4`, `R6c`, `R6d`
- Level: integration, manual
- Fixture/setup:
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
  - `skills/spec/SKILL.md`
  - `skills/spec-review/SKILL.md`
  - `skills/plan/SKILL.md`
  - `skills/plan-review/SKILL.md`
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/pr/SKILL.md`
  - `skills/learn/SKILL.md`
- Steps:
  - Assert every required first-slice skill includes or inherits the tightened evidence-collection guidance.
  - Assert any additional skill updated under `R6d` already had evidence guidance or is updated to reduce drift without broadening the behavior contract.
  - Manually confirm each skill preserves its own full-file-read and correctness obligations.
- Expected result:
  - The high-volume workflow stages consistently teach bounded evidence first.
- Failure proves:
  - The first implementation slice leaves common high-volume stages with stale guidance.
- Automation location:
  - `scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`

### T6. Summary-first output preserves validation semantics

- Covers: `R5`, `R5a`, `R5b`, `R5c`, `E4`, EC3, EC4
- Level: integration, manual
- Fixture/setup:
  - affected validation scripts
  - affected skill result-output guidance
  - active plan validation notes
- Steps:
  - Assert normal output budgets do not change selected check coverage, command exit behavior, failure detection, or required validation evidence.
  - Assert guidance says omitted details must remain available through focused reruns, verbose output, or recorded failure paths when omission affects reviewability.
  - Manually confirm user-requested full output remains allowed when explicitly requested, without broadening unrelated evidence reads.
- Expected result:
  - Shorter output remains reviewable and does not mask failed checks.
- Failure proves:
  - Token-cost optimization weakens validation proof or hides failures.
- Automation location:
  - `scripts/test-skill-validator.py`
  - milestone validation command output review

### T7. First implementation slice and token-budget exclusion stay exact

- Covers: `R6`, `R6a`, `R6b`, `R6c`, `R6d`, `R6e`
- Level: integration, manual
- Fixture/setup:
  - `specs/skill-token-cost-optimization.md`
  - `docs/plans/2026-05-09-skill-token-cost-optimization.md`
  - repository `skills/` tree
- Steps:
  - Assert M1 updates `specs/skill-contract.md`, `specs/skill-contract.test.md` or equivalent repo-owned tests, and focused validator coverage.
  - Assert M2 updates the required first-slice skill set: `proposal`, `proposal-review`, `spec`, `spec-review`, `plan`, `plan-review`, `implement`, `code-review`, `verify`, `pr`, and `learn`.
  - Assert no `skills/token-budget/SKILL.md` path exists or is required.
  - Manually confirm optional additional skill edits are justified as drift reduction, not scope expansion.
- Expected result:
  - Implementation stays scoped to the approved first slice.
- Failure proves:
  - The change either misses required skills or expands into an unapproved new skill.
- Automation location:
  - `scripts/test-skill-validator.py`
  - `rg --files skills | rg '(^|/)token-budget/SKILL.md$'` as negative proof

### T8. Published skill wording stays project-portable

- Covers: `R7`, `R7a`, `R7b`, `R7c`, `E5`, EC7
- Level: integration, manual
- Fixture/setup:
  - selected canonical skill files
  - generated Codex skill mirrors
  - public adapter skill copies
  - `scripts/test-skill-validator.py`
- Steps:
  - Assert published skill text uses portable terms such as project workflow guide, local workflow contract, changed paths, generated output, validation logs, and project validation command.
  - Assert published skill text does not expose RigorLoop maintainer-only source paths, generated mirror paths, adapter package paths, selector path constraints, drift-check mechanics, shared-block implementation mechanics, or RigorLoop-local examples.
  - Assert repository-maintainer validation commands and generated-output procedures remain allowed in internal specs, tests, plans, contributor docs, and change-local evidence.
- Expected result:
  - Public skill packages read as portable user-facing guidance, while repo-specific maintenance details remain internal.
- Failure proves:
  - Published skills leak this repository's maintenance model to downstream users.
- Automation location:
  - `scripts/test-skill-validator.py`
  - `python scripts/validate-adapters.py --version 0.1.1`

### T9. Final contract review covers nuanced behavior not suited to broad scoring

- Covers: all requirements and acceptance criteria
- Level: manual, contract
- Fixture/setup:
  - approved spec
  - test spec
  - active plan
  - changed canonical skill, validator, generated, adapter, and change-local evidence
- Steps:
  - Manually confirm the implementation does not reduce required validation coverage, review obligations, artifact obligations, or workflow gates.
  - Manually confirm static checks are narrow and reviewable, not broad natural-language quality scoring.
  - Manually confirm exact wording changes preserve the spec's invariants and do not introduce ambiguous under-reading advice.
  - Confirm review artifacts cite material noisy-evidence defects only when they include evidence and a safer bounded strategy.
- Expected result:
  - Human review can verify the semantic boundaries that narrow static checks intentionally avoid scoring.
- Failure proves:
  - Static proof is either too weak to protect the contract or too broad to be reviewable.
- Automation location:
  - `code-review` for each implementation milestone
  - final `verify`

### T10. Generated skill mirrors and adapter output stay derived and portable

- Covers: `R7`, `R9`, `R9a`, `R9b`, `R9c`, `E5`, EC2, EC7
- Level: smoke, integration
- Fixture/setup:
  - `.codex/skills/`
  - `dist/adapters/`
  - canonical `skills/`
- Steps:
  - Run `python scripts/build-skills.py --check`.
  - Run `python scripts/build-adapters.py --version 0.1.1 --check`.
  - Run `python scripts/validate-adapters.py --version 0.1.1`.
  - Run `python scripts/test-adapter-distribution.py`.
  - Manually confirm generated outputs were refreshed from canonical sources rather than hand-edited.
- Expected result:
  - Generated skill mirrors and public adapters are deterministic, current, and portable.
- Failure proves:
  - Derived output drifted from canonical skill source or public adapter output violates the portability boundary.
- Automation location:
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/test-adapter-distribution.py`

### T11. Milestone and final validation commands prove the selected scope

- Covers: `R5`, `R5b`, `R9`, `R9b`, `R9c`
- Level: smoke, integration
- Fixture/setup:
  - active plan validation commands
  - changed authored, generated, adapter, plan, and change-local paths
- Steps:
  - Run each milestone's targeted validation before code-review handoff.
  - Before final PR handoff, run the final validation suite named in M5, including lifecycle, skill, generated-output, adapter, selected CI, and diff checks.
  - Confirm command failures are fixed in the owning milestone and rerun before advancing.
- Expected result:
  - The branch is proven by repo-owned validation without broad smoke unless selected validation requires it.
- Failure proves:
  - A milestone or final handoff lacks the required proof or stale generated/lifecycle artifacts remain.
- Automation location:
  - commands listed in the active plan M1-M5 validation sections

### T12. Noisy evidence collection can be reviewed as a process defect

- Covers: `R10`, `R10a`, `R10b`, EC8
- Level: manual
- Fixture/setup:
  - affected review skills
  - review records when material findings exist
- Steps:
  - Assert review guidance allows reporting broad, noisy evidence collection when it materially affects an artifact, review, implementation, or verification result.
  - Assert the finding must identify the noisy evidence surface and safer bounded evidence strategy.
  - Assert the finding must not require reducing correctness checks, skipping required artifacts, or ignoring full-file-read escape conditions.
- Expected result:
  - Reviewers can correct excessive context use without weakening the workflow.
- Failure proves:
  - Process defects can be recorded either too vaguely to fix or in a way that conflicts with correctness obligations.
- Automation location:
  - manual `code-review`, `verify`, and formal review records when triggered

## Fixtures and data

- Existing repository Markdown artifacts are the fixtures: approved spec, active plan, skill-contract spec, selected canonical skills, shared evidence block, generated skill mirrors, public adapter packages, and change-local evidence.
- Generated-output tests may use temporary output roots only when helper-level tests need stale, missing, or unexpected generated files.
- No runtime data fixtures, databases, network services, or external tool installations are required beyond repository-owned scripts.

## Mocking/stubbing policy

- Do not stub `scripts/test-skill-validator.py`, `scripts/validate-skills.py`, `scripts/build-skills.py --check`, `scripts/build-adapters.py --version 0.1.1 --check`, `scripts/validate-adapters.py --version 0.1.1`, or `scripts/test-adapter-distribution.py` for milestone or final proof.
- Unit-level helper tests may use temporary files or directories to exercise stale, missing, or invalid text cases.
- Manual review is allowed only for semantic boundaries intentionally not covered by static checks.

## Migration or compatibility tests

- Existing historical artifacts and learn records do not require migration: manual review confirms no implementation step modifies them.
- Existing unmodified skills remain valid until touched by this approved slice or later normalization work: `T7`, `T9`.
- Existing validation commands keep their semantics: `T6`, `T11`.
- Generated `.codex/skills/` and `dist/adapters/` output remain derived and deterministic: `T10`, `T11`.
- Rollback can revert the spec, test, canonical skill, validator, generated-output, and adapter-output changes together: `T9`, `T11`.

## Observability verification

- Validation failures should identify the missing token-cost guidance, missing escape condition, portability issue, generated-output drift, or adapter validation failure: `T1`-`T4`, `T8`, `T10`, `T11`.
- Review and verify artifacts should cite concrete commands run rather than generic success claims: `T9`, `T11`.
- No runtime logs, metrics, traces, or audit events are required.

## Security/privacy verification

- Confirm skill guidance does not encourage committing or pasting secrets, credentials, tokens, private keys, private incident data, unnecessary machine-local paths, or private user data: `T8`, `T9`.
- Confirm summary-first guidance reduces unnecessary exposure of large logs or generated output while preserving reviewable proof: `T6`.
- Confirm generated-output and adapter refreshes do not introduce secrets or machine-local debug paths: `T10`, `T11`.

## Performance checks

- Confirm the first validation slice remains static and repository-local: `T1`, `T9`.
- Confirm no broad semantic quality scoring or token-count scoring is added: `T4`, `T9`.
- Confirm skill and adapter validation remain suitable for normal pre-PR validation: `T10`, `T11`.
- No numeric token reduction target is required.

## Manual QA checklist

- Confirm correctness outranks token savings in skill-contract and selected skill guidance.
- Confirm full-file-read escape conditions remain explicit.
- Confirm output caps are described as safety rails rather than query design.
- Confirm public skill text stays project-portable.
- Confirm repository-maintainer commands and generated-output procedures stay in internal specs, tests, plans, contributor docs, or change-local evidence.
- Confirm code-review findings about noisy evidence include evidence and a safer bounded strategy.
- Confirm M1-M4 each pass targeted validation and code-review before M5 final lifecycle closeout.

## What not to test

- Do not test actual token counts; the spec requires guidance and reviewability, not a numeric token budget.
- Do not add runtime workflow simulations; this change updates skill and validation guidance.
- Do not add broad natural-language quality scoring; the spec requires narrow static validation and manual review for nuanced boundaries.
- Do not test historical learn sessions or historical proposals for migration.
- Do not require local Codex, Claude Code, or opencode installations; repository-owned adapter generation, validation, and distribution tests cover non-smoke package proof.

## Uncovered gaps

- None. The approved open questions are implementation choices covered by the plan and manual review: whether `docs/workflows.md` needs tightening, and whether additional evidence-guidance skills are included to reduce drift.

## Next artifacts

- Implement M1: skill-contract and static-proof updates.
- Code-review M1 after targeted validation passes.
- Continue M2-M4 only after each prior milestone review loop closes.
- M5 final lifecycle closeout only after M1-M4 have each passed their milestone review loop.

## Follow-on artifacts

- None yet.

## Readiness

Active proof surface for implementation. The active plan `Current Handoff Summary` owns the next workflow action.
