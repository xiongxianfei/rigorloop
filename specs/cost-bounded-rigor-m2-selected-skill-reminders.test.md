# Cost-Bounded Rigor M2 Selected Skill Reminders Test Spec

## Status

active

## Related spec and plan

- Spec: [Cost-Bounded Rigor M2 Selected Skill Reminders](cost-bounded-rigor-m2-selected-skill-reminders.md), approved.
- Plan: [Cost-Bounded Rigor M2 Selected Skill Reminders Plan](../docs/plans/2026-05-14-cost-bounded-rigor-m2-selected-skill-reminders.md), active after clean plan-review.
- Proposal: [Cost-Bounded Rigor After Single-Source Skills and Follow-Up Routing](../docs/proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md), accepted.
- Spec review: [spec-review-r1](../docs/changes/2026-05-14-cost-bounded-rigor-m2-selected-skill-reminders/reviews/spec-review-r1.md), approved with no material findings.
- Plan review: [plan-review-r2](../docs/changes/2026-05-14-cost-bounded-rigor-m2-selected-skill-reminders/reviews/plan-review-r2.md), approved with no material findings.
- Change metadata: [change.yaml](../docs/changes/2026-05-14-cost-bounded-rigor-m2-selected-skill-reminders/change.yaml).
- Architecture: not required. The approved spec, spec-review, and plan-review scope this slice to selected skill wording and optional focused static proof.
- Project map: [docs/project-map.md](../docs/project-map.md) exists as a living orientation reference. This test spec relies on the approved spec, reviewed plan, and touched files for implementation proof.

## Approval

Maintainer-approved on 2026-05-14 by direct user request. Status remains `active` because this test spec is the relied-on proof-planning surface for M2 implementation.

## Testing strategy

This M2 slice is verified through contract, static, lifecycle, and manual review checks. It does not require runtime end-to-end tests, release validation, adapter packaging validation, validation-selector behavior changes, lifecycle token-cost summary artifacts, broad-smoke changes, or dynamic benchmark comparison.

- Use selected skill audits before editing to decide whether each selected skill needs a concise reminder or an unchanged-with-rationale decision.
- Use static checks only when a stable assertion can prove a real M2 boundary without enforcing one exact sentence or broad natural-language scoring.
- Use manual contract review for semantic checks that should remain flexible, including whether wording is concise, local, non-duplicative, and sufficient for the selected skill.
- Use skill validation and build checks when canonical skill text changes.
- Use static skill token measurement after canonical skill changes and treat the result as diagnostic and warning-only.
- Use selected explicit validation for changed paths. If implementation updates `change.yaml` or other change-local artifacts, include those paths so change-metadata and lifecycle checks remain selected.
- Treat `docs/workflows.md` as the full bounded-evidence and path-search guide. M2 does not retest M1's full workflow-guide rule except to prove selected skills do not duplicate or conflict with it.

## Requirement coverage map

| Requirement IDs | Covered by | Notes |
|---|---|---|
| `R1` | `T1`, `T10`, `T11` | M2 scope, lifecycle bookkeeping, and final acceptance proof. |
| `R2` | `T1`, `T6` | Selected skill surface boundary. |
| `R3` | `T1`, `T6` | `implement` and `code-review` exclusion. |
| `R4` | `T1`, `T6`, `T10` | Forbidden selector, release, adapter, token-report, benchmark, and hard-gate changes. |
| `R5` | `T3`, `T10` | `docs/workflows.md` remains the full bounded-evidence guide. |
| `R6` | `T3`, `T11` | Selected skills do not duplicate the full workflow rule. |
| `R7` | `T3` | Reminder wording is concise and local. |
| `R8` | `T3` | Bounded-first behavior in selected reminders. |
| `R9` | `T4` | Do-not-under-read behavior. |
| `R10` | `T4` | Full-file-read escape behavior. |
| `R11` | `T2` | Audit selected skills before editing. |
| `R12` | `T2`, `T11` | Avoid wording churn and record no-change rationale. |
| `R13` | `T5` | Optional static proof uses narrow stable checks. |
| `R14` | `T5` | Static proof does not require one exact sentence. |
| `R15` | `T7` | Token-cost measurement remains diagnostic. |
| `R16` | `T7` | No required dynamic benchmark comparison. |
| `R17` | `T8` | Safety-critical review, verify, PR, material-finding, release, and full-file-read guidance preserved. |
| `R18` | `T6`, `T9` | Single-authored-skill-source and generated adapter boundaries preserved. |
| `R19` | `T2`, `T11` | Affected-surface decisions recorded for every selected skill. |

## Example coverage map

| Example | Coverage |
|---|---|
| `E1` selected skill needs a short reminder | `T2`, `T3` |
| `E2` selected skill already has sufficient wording | `T2`, `T11` |
| `E3` full workflow rule stays in one place | `T3`, `T10` |
| `E4` validation-budget work is out of scope | `T1`, `T6`, `T10` |
| `E5` progressive-loading restructuring is out of scope | `T1`, `T6`, `T7` |

## Edge case coverage

| Edge case | Coverage |
|---|---|
| `EC1` `proposal` already has relevant wording | `T2` |
| `EC2` `proposal-review` already has relevant wording | `T2` |
| `EC3` `workflow` already has relevant wording | `T2` |
| `EC4` bounded-first wording lacks do-not-under-read escape | `T3`, `T4` |
| `EC5` full-file escape lacks path/state lookup wording | `T3`, `T4` |
| `EC6` proposed edit copies the full workflow sequence | `T3`, `T5` |
| `EC7` proposed static test enforces exact prose | `T5` |
| `EC8` proposed edit touches `implement` or `code-review` | `T1`, `T6` |
| `EC9` proposed edit changes selector behavior | `T1`, `T6`, `T10` |
| `EC10` proposed edit changes adapter or release surfaces | `T1`, `T6` |
| `EC11` selected skill left unchanged without rationale | `T2`, `T11` |
| `EC12` static skill total increases | `T7` |

## Acceptance criteria coverage map

| Acceptance criterion | Covered by |
|---|---|
| M2 selected surfaces are limited to `proposal`, `proposal-review`, and `workflow` | `T1`, `T6` |
| Each selected skill is either updated with a concise reminder or recorded unchanged with rationale | `T2`, `T11` |
| `docs/workflows.md` remains the full bounded-evidence and path-search guide | `T3`, `T10` |
| Selected skills do not duplicate the full workflow-guide rule | `T3`, `T5`, `T11` |
| Do-not-under-read and full-file-read escape behavior is preserved | `T4` |
| No validation-selector, release, adapter, lifecycle-token-summary, dynamic benchmark, hard token gate, `implement`, or `code-review` behavior changes are included | `T1`, `T6`, `T10` |
| Static proof, if added, checks stable boundaries without broad natural-language scoring | `T5` |
| Static skill token measurement remains diagnostic | `T7` |
| Safety-critical review, verify, PR, material-finding, release, and full-file-read guidance remains intact | `T8` |

## Milestone coverage map

| Milestone | Coverage |
|---|---|
| `M1. Selected skill reminder audit and implementation` | `T1`-`T11` |

## Test cases

### T1. M2 implementation scope stays limited

- Covers: `R1`-`R4`, `R17`, `E4`, `E5`, `EC8`-`EC10`
- Level: contract, manual
- Fixture/setup:
  - final implementation diff
  - approved M2 spec
  - active M2 plan
- Steps:
  - Assert implementation touches only selected skill reminders, optional focused static proof, lifecycle bookkeeping, and required explanation or verification evidence.
  - Assert selected skill surfaces are limited to `skills/proposal/SKILL.md`, `skills/proposal-review/SKILL.md`, and `skills/workflow/SKILL.md`.
  - Assert implementation does not edit `skills/implement/SKILL.md` or `skills/code-review/SKILL.md`.
  - Assert implementation does not change validation-selector behavior, broad-smoke triggers, release validation, adapter packaging, lifecycle token-cost summary artifacts, dynamic benchmark requirements, or hard token gates.
- Expected result: the final diff remains a narrow selected-skill reminder slice.
- Failure proves: M2 absorbed another workstream and violated the approved scope.
- Automation location: manual final diff review, `git diff --name-only`, selected validation output.

### T2. Selected skill audit and affected-surface decisions are recorded

- Covers: `R11`, `R12`, `R19`, `E1`, `E2`, `EC1`-`EC3`, `EC11`
- Level: manual, contract
- Fixture/setup:
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
  - `skills/workflow/SKILL.md`
  - active plan, change metadata, explain-change, or another tracked contributor-visible rationale surface
- Steps:
  - Confirm implementation audits all three selected skills before editing.
  - For each selected skill, record one outcome: edited, unchanged with rationale, or deferred with rationale.
  - If a selected skill already satisfies the M2 contract, assert it is left unchanged or receives only a justified clarification.
  - Assert no selected skill is silently left unchanged without a rationale.
- Expected result: reviewers can see why each selected skill changed or did not change.
- Failure proves: implementation either skipped the required audit or created invisible wording churn decisions.
- Automation location: manual review of plan/change metadata/explain-change plus final diff.

### T3. Selected reminders are concise, local, bounded-first, and non-duplicative

- Covers: `R5`-`R8`, `E1`, `E3`, `EC4`-`EC6`
- Level: static, manual
- Fixture/setup:
  - changed selected skills
  - `docs/workflows.md`
  - `scripts/test-skill-validator.py`, if stable static proof is added
- Steps:
  - Assert `docs/workflows.md` remains the full bounded-evidence and path-search guide.
  - Assert any selected skill reminder is short and local to that skill's stage behavior.
  - Assert reminders preserve bounded-first behavior by starting from active state, metadata, `docs/workflows.md`, headings, targeted excerpts, paths, IDs, counts, or diffs before broad reads when sufficient.
  - Assert selected skills do not copy the full workflow-guide evidence sequence or another long shared bounded-evidence template.
- Expected result: selected skills reduce broad reads without recreating duplicated full rules.
- Failure proves: selected skill wording either under-specifies M2 behavior or duplicates the full workflow guide.
- Automation location: `scripts/test-skill-validator.py` for stable phrase or absence checks, manual wording review.

### T4. Do-not-under-read and full-file-read escapes are preserved

- Covers: `R9`, `R10`, `EC4`, `EC5`
- Level: static, manual
- Fixture/setup:
  - changed selected skill wording
  - `docs/workflows.md`
  - final implementation diff
- Steps:
  - Assert selected reminder wording does not imply that bounded evidence is a reason to skip needed context.
  - Assert relevant selected skill wording or its workflow-guide pointer preserves expansion when narrower evidence is incomplete, contradictory, or insufficient.
  - Assert full-file-read escape behavior remains available when the whole file is the target, surrounding context can change the conclusion, relevant sections cannot be isolated safely, bounded searches disagree or are incomplete, or behavior-changing edits depend on the whole source-of-truth artifact.
- Expected result: cost reduction does not weaken correctness or review rigor.
- Failure proves: M2 guidance encourages under-reading.
- Automation location: static term checks when stable, manual review for semantic sufficiency.

### T5. Optional static proof is narrow and not brittle

- Covers: `R13`, `R14`, `EC6`, `EC7`
- Level: unit, static, manual
- Fixture/setup:
  - `scripts/test-skill-validator.py`
  - changed selected skill text
- Steps:
  - If static proof is added, assert it checks selected-surface boundaries, stable section presence, stable behavior cues, or forbidden-surface absence.
  - Assert static proof does not use broad natural-language scoring.
  - Assert static proof does not require one exact sentence when equivalent concise wording satisfies the M2 contract.
  - Assert any absence check for duplicated full workflow guidance is tied to stable phrases or structural markers.
- Expected result: automation catches real regressions without freezing prose.
- Failure proves: the implementation adds brittle validator ceremony or semantic scoring.
- Automation location: `scripts/test-skill-validator.py` and manual review of changed validator assertions.

### T6. Forbidden surfaces and generated adapter boundaries remain untouched

- Covers: `R2`-`R4`, `R18`, `EC8`-`EC10`
- Level: contract, manual
- Fixture/setup:
  - final implementation diff
  - `dist/adapters/README.md`
  - `dist/adapters/manifest.yaml`
  - selected validation output
- Steps:
  - Assert no generated public adapter skill bodies are edited or reintroduced as tracked source.
  - Assert `skills/` remains the authored skill source for any skill wording change.
  - Assert release, adapter, selector, broad-smoke, lifecycle-token-summary, dynamic benchmark, and hard-token-gate surfaces are unchanged unless a later approved artifact explicitly broadens scope.
  - Assert `implement` and `code-review` are not touched.
- Expected result: M2 preserves the single-authored-skill-source model and avoids non-M2 surfaces.
- Failure proves: implementation reopened completed PR #52 or expanded into later proposal slices.
- Automation location: `git diff --name-only`, selected validation output, manual diff review.

### T7. Token-cost measurement stays diagnostic and no dynamic benchmark is required

- Covers: `R15`, `R16`, `E5`, `EC12`
- Level: smoke, manual
- Fixture/setup:
  - canonical skill changes
  - `scripts/measure-skill-tokens.py`
  - active plan or change metadata for validation notes
- Steps:
  - Run `python scripts/measure-skill-tokens.py` after canonical skill changes.
  - Record the static token result as diagnostic evidence only.
  - Assert no hard token threshold or release blocker is introduced.
  - Assert no before/after dynamic benchmark comparison is required or run unless a later approved plan or test spec explicitly requires it.
  - If static token totals increase, require a qualitative explanation rather than automatic failure.
- Expected result: M2 measures static cost without creating a new cost driver or hard gate.
- Failure proves: token-cost measurement became either missing evidence or premature governance.
- Automation location: `python scripts/measure-skill-tokens.py`, validation notes, change metadata, explain-change.

### T8. Safety-critical lifecycle and review guidance remains intact

- Covers: `R17`
- Level: manual, contract
- Fixture/setup:
  - changed selected skill wording
  - final implementation diff
  - affected review and workflow guidance
- Steps:
  - Assert implementation does not weaken formal review, verify, PR, material-finding, release, or full-file-read guidance.
  - Assert any wording compression preserves safety-critical obligations or leaves their owner surface intact.
  - Assert no safety guidance is removed solely for token-cost reduction.
- Expected result: M2 reduces waste without weakening rigor.
- Failure proves: cost-bounded rigor was implemented as weaker workflow safety.
- Automation location: manual diff review, code-review checklist.

### T9. Canonical skill validation and generated local mirror checks pass

- Covers: `R18`
- Level: smoke, static
- Fixture/setup:
  - canonical skill edits under `skills/`
  - repository-owned skill validators
- Steps:
  - Run `python scripts/test-skill-validator.py`.
  - Run `python scripts/validate-skills.py`.
  - Run `python scripts/build-skills.py --check`.
  - Assert generated public adapter package output is not hand-edited as part of this proof.
- Expected result: authored skill changes are valid and local generated mirror checks still pass.
- Failure proves: selected skill wording broke the skill contract or generated local skill mirror consistency.
- Automation location: named commands.

### T10. Selected validation covers implementation and lifecycle paths without broad smoke

- Covers: `R1`, `R4`, `R5`, `E3`, `E4`, `EC9`
- Level: integration, smoke
- Fixture/setup:
  - changed implementation paths
  - `scripts/select-validation.py`
  - `scripts/ci.sh`
- Steps:
  - Run `python scripts/select-validation.py --mode explicit` with changed skills, `scripts/test-skill-validator.py` when changed, M2 spec/test spec, active plan, `docs/plan.md`, and changed M2 change-local artifacts.
  - Run `bash scripts/ci.sh --mode explicit` with the same changed paths.
  - Assert selected checks include skill, lifecycle, review-artifact, and change-metadata checks when their paths are changed.
  - Assert broad smoke is not required unless a later authoritative trigger is introduced.
- Expected result: validation is targeted to the changed M2 surfaces and keeps change-local metadata/lifecycle checks selected.
- Failure proves: proof is either under-selected or expanded into unnecessary broad validation.
- Automation location: selected validation and selected CI output.

### T11. Final acceptance and no-change rationale are reviewable

- Covers: `R1`, `R6`, `R12`, `R19`, `E2`, `EC11`
- Level: manual, contract
- Fixture/setup:
  - active plan
  - change metadata
  - explain-change when created
  - code-review record
- Steps:
  - Confirm every selected skill has a recorded affected-surface decision.
  - Confirm selected skills do not duplicate the full workflow-guide rule.
  - Confirm any unchanged selected skill has a rationale.
  - Confirm acceptance criteria are traceable from the implementation diff to validation evidence and final review evidence.
- Expected result: reviewers can close M2 without relying on chat-only rationale.
- Failure proves: M2 lacks durable proof for changed or unchanged selected skill surfaces.
- Automation location: manual review, code-review, explain-change, change metadata.

## Fixtures and data

- Existing selected skill files:
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
  - `skills/workflow/SKILL.md`
- Full bounded-evidence guide:
  - `docs/workflows.md`
- Static proof surface:
  - `scripts/test-skill-validator.py`
- Lifecycle and review surfaces:
  - `specs/cost-bounded-rigor-m2-selected-skill-reminders.md`
  - `specs/cost-bounded-rigor-m2-selected-skill-reminders.test.md`
  - `docs/plans/2026-05-14-cost-bounded-rigor-m2-selected-skill-reminders.md`
  - `docs/plan.md`
  - `docs/changes/2026-05-14-cost-bounded-rigor-m2-selected-skill-reminders/`

No new runtime fixtures, adapter fixtures, release fixtures, generated output fixtures, or benchmark fixtures are required for M2.

## Mocking/stubbing policy

No mocks or stubs are required. Tests operate on repository files and repository-owned validation scripts. Do not mock `scripts/select-validation.py`, skill validators, or token measurement for final proof; run the real commands.

## Migration or compatibility tests

No data migration is required. Compatibility proof is manual and static:

- existing accepted proposals, reviews, plans, lifecycle artifacts, release archives, adapter packages, reports, and selected skill behavior remain valid unless they conflict with the approved M2 spec;
- historical generated adapter skill bodies are not restored as tracked source;
- rollback is removal of unnecessary selected skill wording while preserving the full `docs/workflows.md` rule and recorded rationale.

## Observability verification

No runtime logs, metrics, traces, or hosted observability changes are required. Observable proof is:

- selected skill text;
- optional static proof in `scripts/test-skill-validator.py`;
- selected validation output;
- active plan validation notes;
- change metadata and explain-change evidence when created;
- review findings if a selected skill duplicates the full rule, under-reads, or drifts from `docs/workflows.md`.

## Security/privacy verification

- Manually review changed text and evidence artifacts to ensure they do not encourage broad dumps of secrets, credentials, private logs, or irrelevant large excerpts.
- Confirm selected reminders continue to prefer targeted excerpts, paths, IDs, counts, diffs, and line citations over unnecessary broad output.
- Confirm no authentication, authorization, secrets handling, dependency trust, release signing, or data-access behavior changes are introduced.

## Performance checks

- Run `python scripts/measure-skill-tokens.py` after canonical skill changes.
- Treat static token measurements as diagnostic and warning-only.
- Do not run or require dynamic benchmark comparison unless a later approved plan or test spec explicitly requires it.
- Do not introduce hard token gates.

## Manual QA checklist

- Confirm all selected skills were audited before edits.
- Confirm edited reminders are concise and local.
- Confirm unchanged selected skills have tracked rationale.
- Confirm `docs/workflows.md` remains the full bounded-evidence guide.
- Confirm selected skills do not duplicate the full workflow-guide evidence sequence.
- Confirm do-not-under-read and full-file-read escape behavior is preserved.
- Confirm forbidden surfaces and later slices remain untouched.
- Confirm validation evidence names the actual commands run.

## What not to test

- Do not test runtime end-to-end behavior; RigorLoop has no deployed runtime for this slice.
- Do not test release validation, adapter packaging, generated public adapter archives, or adapter smoke.
- Do not run dynamic token benchmarks by default.
- Do not add natural-language semantic scoring for broadness, concision, or exact reminder equivalence.
- Do not require exact selected-skill prose when equivalent concise wording satisfies the M2 contract.
- Do not retest all M1 scope-budget behavior except where needed to prove selected-skill M2 boundaries.
- Do not require broad repository smoke unless selected validation or a later authoritative trigger requires it.

## Uncovered gaps

None. If implementation discovers that selected reminders require selector behavior, release/adapter changes, dynamic benchmarks, lifecycle token-cost summaries, or progressive-loading restructuring, stop and route that work to the appropriate later slice or proposal.

## Next artifacts

```text
implement
code-review
explain-change
verify
pr
```

## Follow-on artifacts

None yet.

## Readiness

Active proof-planning surface for M2. Downstream work must follow this test spec, the approved M2 spec, and the reviewed M2 plan.
