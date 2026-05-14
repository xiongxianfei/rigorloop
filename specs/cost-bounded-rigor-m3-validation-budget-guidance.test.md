# Cost-Bounded Rigor M3 Validation-Budget Guidance Test Spec

## Status

active

## Related spec and plan

- Spec: [Cost-Bounded Rigor M3 Validation-Budget Guidance](cost-bounded-rigor-m3-validation-budget-guidance.md), approved.
- Plan: [Cost-Bounded Rigor M3 Validation-Budget Guidance Plan](../docs/plans/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance.md), active after clean plan-review.
- Proposal: [Cost-Bounded Rigor After Single-Source Skills and Follow-Up Routing](../docs/proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md), accepted.
- Spec review: [spec-review-r1](../docs/changes/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance/reviews/spec-review-r1.md), approved with no material findings.
- Plan review: [plan-review-r1](../docs/changes/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance/reviews/plan-review-r1.md), approved with no material findings.
- Change metadata: [change.yaml](../docs/changes/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance/change.yaml).
- Architecture: not required. The approved spec, spec-review, and plan-review scope this slice to validation-budget guidance, owner-surface decisions, and optional static proof.
- Project map: [docs/project-map.md](../docs/project-map.md) exists as a living orientation reference. This test spec relies on the approved spec, reviewed plan, and touched files for proof.

## Testing strategy

M3 is verified through contract, static, selected-integration, lifecycle, and manual review checks. It does not require runtime end-to-end tests, release validation, adapter packaging validation, lifecycle token-cost summary artifacts, hard token gates, dynamic benchmark comparison, or progressive-loading restructuring.

- Use an owner-surface audit before editing to decide whether `docs/workflows.md`, selector behavior, wrapper behavior, and validation-related stage skills need edits or no-change rationale.
- Use static proof in `scripts/test-select-validation.py` only for stable behavior cues, selected-surface coverage, broad-smoke trigger preservation, or forbidden-scope checks.
- Use selector regression coverage only if implementation changes `scripts/validation_selection.py`, `scripts/select-validation.py`, `scripts/ci.sh`, or selected-check behavior.
- Use manual contract review for semantic checks that should remain flexible, including whether guidance is concise, whether owner boundaries are clear, and whether unchanged surfaces have rationale.
- Use selected explicit validation for changed paths. If implementation updates `change.yaml` or other change-local artifacts, include those paths so change-metadata and lifecycle checks remain selected.
- Run broad smoke only if an authoritative trigger appears in selector mode, explicit flags, active plan state, this test spec, review-resolution, or release metadata.

## Requirement coverage map

| Requirement IDs | Covered by | Notes |
|---|---|---|
| `R1` | `T2`, `T9` | Targeted validation first when paths are known and no broad-smoke trigger applies. |
| `R2` | `T3`, `T8`, `T11` | Mandatory validation semantics remain intact. |
| `R3` | `T2`, `T3` | Broad smoke stays trigger-driven. |
| `R4` | `T3` | Authoritative broad-smoke trigger set is preserved. |
| `R5` | `T1`, `T2`, `T7`, `T10` | Owner surfaces are distinguished and recorded. |
| `R6` | `T4`, `T7` | Skill prose does not become executable selector authority. |
| `R7` | `T4`, `T6` | Guidance-only changes do not alter selected checks or command behavior. |
| `R8` | `T5` | Selector behavior changes require regression tests. |
| `R9` | `T4`, `T6` | Guidance-only changes may use static/manual proof. |
| `R10` | `T4`, `T10` | Selector behavior state is recorded as changed, unchanged, or deferred. |
| `R11` | `T7` | Skill wording, if any, is concise and subordinate to `docs/workflows.md`. |
| `R12` | `T1`, `T7` | M3 does not require every stage skill to change. |
| `R13` | `T1`, `T7` | `implement`, `code-review`, and `verify` stay untouched unless a later approved plan scopes a gap. |
| `R14` | `T3`, `T8`, `T11` | Review-resolution and material-finding closeout remain intact. |
| `R15` | `T8`, `T11` | Release validation and adapter packaging boundaries remain intact. |
| `R16` | `T1`, `T8` | Lifecycle token-cost summaries, dynamic benchmarks, hard gates, release packaging, and progressive loading remain out of scope. |
| `R17` | `T9`, `T11` | Dirty-worktree proof uses explicit paths, diff-derived modes, or selected CI. |
| `R18` | `T10`, `T11` | Final verify must compare validation evidence with plan, test spec, review-resolution, and release metadata triggers. |
| `R19` | `T1`, `T10` | Existing satisfactory owner surfaces may remain unchanged with rationale. |

## Example coverage map

| Example | Coverage |
|---|---|
| `E1` proposal-only or spec-only change uses targeted validation | `T2`, `T9` |
| `E2` skill wording change validates canonical skills | `T8`, `T11` |
| `E3` review-resolution trigger can require broader proof | `T3`, `T11` |
| `E4` release metadata triggers release validation | `T3`, `T8`, `T11` |
| `E5` selector behavior change needs executable proof | `T5` |
| `E6` guidance-only change does not require selector behavior changes | `T4`, `T6`, `T10` |

## Edge case coverage

| Edge case | Coverage |
|---|---|
| `EC1` plan sets its broad-smoke-required flag for a docs-only change | `T3`, `T11` |
| `EC2` test spec requires broad smoke for a selector change | `T3`, `T5` |
| `EC3` review-resolution requires broad smoke after a finding | `T3`, `T11` |
| `EC4` release metadata changes | `T3`, `T8`, `T11` |
| `EC5` selector output omits a changed unclassified path | `T5`, `T9` |
| `EC6` guidance-only change attempts to alter selector behavior | `T4`, `T5` |
| `EC7` stage skill adds a long copied validation checklist | `T7` |
| `EC8` dirty worktree contains unrelated drafts | `T9` |
| `EC9` no-argument `bash scripts/ci.sh` is treated as normal first proof | `T2`, `T9` |
| `EC10` generated adapter release output changes | `T8`, `T11` |

## Acceptance criteria coverage map

| Acceptance criterion | Covered by |
|---|---|
| `docs/workflows.md` or no-change rationale identifies targeted validation first and broad smoke trigger-driven | `T2`, `T10` |
| Owner split is recorded across workflow guidance, selector behavior, skill reminders, plans, test specs, review-resolution, and release metadata | `T1`, `T10` |
| Any selector behavior changes have selector regression coverage | `T5` |
| Guidance-only implementation does not change selected check coverage or command semantics | `T4`, `T6` |
| Broad-smoke triggers remain intact | `T3`, `T11` |
| Review-resolution, release validation, adapter validation, and generated-output rules remain intact | `T8`, `T11` |
| Any selected skill changes are concise and do not duplicate the full validation-budget rule | `T7` |
| No-change rationale is recorded for owner surfaces that already satisfy the M3 contract | `T1`, `T10` |

## Milestone coverage map

| Milestone | Coverage |
|---|---|
| `M1. Owner-surface audit and minimal validation-budget guidance` | `T1`-`T11` |

## Test cases

### T1. M3 implementation scope and owner-surface audit stay narrow

- Covers: `R5`, `R12`, `R13`, `R16`, `R19`
- Level: contract, manual
- Fixture/setup:
  - approved M3 spec
  - active M3 plan
  - final implementation diff
  - active plan, change metadata, explain-change, or another tracked rationale surface
- Steps:
  - Confirm implementation audits `docs/workflows.md`, selector behavior, wrapper behavior, and validation-related stage skill reminders before editing.
  - For each owner surface, record one outcome: edited, unchanged with rationale, or deferred with owner/slice.
  - Confirm the implementation stays within `docs/workflows.md`, optional focused static proof, active plan/change metadata, and other required lifecycle evidence unless the plan is revised first.
  - Confirm implementation does not add lifecycle token-cost summaries, hard token gates, release packaging, adapter packaging, dynamic benchmark requirements, or progressive-loading restructuring.
  - Confirm `skills/implement/SKILL.md`, `skills/code-review/SKILL.md`, and `skills/verify/SKILL.md` remain untouched unless a later approved plan identifies a specific stage-local gap.
- Expected result: M3 remains a focused validation-budget guidance slice with visible owner-surface decisions.
- Failure proves: implementation absorbed a deferred workstream or skipped required no-change rationale.
- Automation location: manual final diff review, `git diff --name-only`, active plan/change metadata/explain-change evidence.

### T2. Workflow guidance presents targeted validation before broad smoke

- Covers: `R1`, `R3`, `R5`, `E1`, `EC9`
- Level: static, manual
- Fixture/setup:
  - `docs/workflows.md`
  - `scripts/test-select-validation.py`, if static proof is added or updated
- Steps:
  - Confirm `docs/workflows.md` or a tracked no-change rationale identifies selector-selected or explicit-path targeted proof as the first validation layer when changed paths are known.
  - Confirm the guidance does not present no-argument `bash scripts/ci.sh` or routine broad smoke as the normal first proof step.
  - Confirm targeted validation guidance points to repo-owned selector and wrapper commands.
  - If static proof is updated, assert stable behavior cues instead of a single exact sentence.
- Expected result: contributors see targeted validation as the default first layer without weakening later triggers.
- Failure proves: M3 either fails to reduce validation overreach or makes broad smoke routine by wording.
- Automation location: `scripts/test-select-validation.py` stable cue checks plus manual wording review.

### T3. Broad-smoke and stronger-validation triggers remain mandatory

- Covers: `R2`-`R4`, `R14`, `E3`, `E4`, `EC1`-`EC4`
- Level: unit, static, manual
- Fixture/setup:
  - `docs/workflows.md`
  - `scripts/test-select-validation.py`
  - selector broad-smoke trigger tests
  - final implementation diff
- Steps:
  - Confirm the broad-smoke trigger set still includes selector mode `main`, selector mode `release`, explicit `--broad-smoke`, the active-plan broad-smoke-required flag, test-spec requirement, review-resolution requirement, and release metadata.
  - Confirm guidance states that review-resolution, release metadata, active plans, and test specs may require stronger validation than path-based targeting alone.
  - Confirm existing broad-smoke source-attribution tests remain present or are updated only with equivalent coverage.
  - Confirm M3 wording does not let targeted validation override release, review-resolution, or material-finding closeout requirements.
- Expected result: broad smoke remains trigger-driven and mandatory when an authoritative trigger exists.
- Failure proves: M3 weakened mandatory validation semantics.
- Automation location: `scripts/test-select-validation.py`, selected CI output, manual review of changed guidance.

### T4. Guidance-only changes do not change selector behavior

- Covers: `R6`, `R7`, `R9`, `R10`, `E6`, `EC6`
- Level: contract, manual
- Fixture/setup:
  - final implementation diff
  - active plan/change metadata/explain-change evidence
  - selector output before and after implementation, if relevant
- Steps:
  - If implementation only changes `docs/workflows.md` or selected wording, confirm `scripts/validation_selection.py`, `scripts/select-validation.py`, and `scripts/ci.sh` are unchanged.
  - Confirm implementation records selector behavior as unchanged with rationale.
  - Confirm no skill prose or docs wording claims to be the source of truth for executable selected-check behavior.
  - Confirm selected check coverage, command exit behavior, failure detection, and required validation evidence are unchanged by guidance-only wording.
- Expected result: guidance-only implementation remains guidance-only, with selector authority preserved in repository scripts.
- Failure proves: wording changes silently altered executable behavior or authority boundaries.
- Automation location: manual final diff review, selected validation output, no-change rationale evidence.

### T5. Selector behavior changes, if scoped later, get executable regression coverage

- Covers: `R8`, `E5`, `EC2`, `EC5`, `EC6`
- Level: unit, integration, conditional
- Fixture/setup:
  - `scripts/validation_selection.py`
  - `scripts/select-validation.py`
  - `scripts/ci.sh`
  - `scripts/test-select-validation.py`
  - any later approved plan/test-spec revision that broadens M3 into selector behavior
- Steps:
  - If implementation changes selector behavior, stop unless the active plan/test spec explicitly scopes that behavior.
  - Add or update selector regression tests for changed classification, selected checks, broad-smoke trigger sources, unclassified-path blocking, or wrapper execution behavior.
  - Run `python scripts/test-select-validation.py`.
  - Run selected CI for the changed selector and lifecycle paths.
  - Confirm skill-only or docs-only proof is rejected as insufficient for executable selector changes.
- Expected result: selector behavior changes have direct executable proof.
- Failure proves: executable validation selection changed without regression coverage.
- Automation location: `scripts/test-select-validation.py`, `python scripts/select-validation.py --mode explicit ...`, `bash scripts/ci.sh --mode explicit ...`.

### T6. Static proof uses stable behavior cues and avoids brittle prose

- Covers: `R7`, `R9`, `E6`
- Level: unit, static, manual
- Fixture/setup:
  - `scripts/test-select-validation.py`
  - `docs/workflows.md`
  - changed static tests, if any
- Steps:
  - If static proof is added, assert it checks stable behavior cues, owner-surface terms, selected check IDs, trigger phrases, section presence, or forbidden-sequence absence.
  - Confirm static proof does not require a full exact sentence when equivalent wording satisfies the M3 contract.
  - Confirm static proof does not perform broad natural-language scoring or infer semantic validation sufficiency from skill prose.
  - Confirm tests remain focused on the affected owner surfaces rather than rewriting every workflow or skill assertion.
- Expected result: static tests protect M3 boundaries without freezing prose.
- Failure proves: M3 created brittle validation that will cause unnecessary review and maintenance cost.
- Automation location: `scripts/test-select-validation.py`, manual review of changed assertions.

### T7. Skill-local reminder boundaries remain concise and subordinate

- Covers: `R5`, `R6`, `R11`-`R13`, `EC7`
- Level: contract, manual
- Fixture/setup:
  - final implementation diff
  - `docs/workflows.md`
  - `skills/workflow/SKILL.md`
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/verify/SKILL.md`
- Steps:
  - Confirm M3 does not edit every stage skill.
  - Confirm any skill-local wording is short, local to the stage, and subordinate to `docs/workflows.md` for the full validation-budget rule.
  - Confirm no stage skill copies a long validation checklist or makes skill prose the executable selected-check authority.
  - Confirm `implement`, `code-review`, and `verify` remain unchanged unless a later approved plan scopes a specific gap before implementation.
- Expected result: skill surfaces remain concise and avoid duplicating workflow guidance.
- Failure proves: M3 recreated the duplicated-guidance cost pattern it is intended to reduce.
- Automation location: manual diff review, code-review checklist, skill validation only if canonical skills change.

### T8. Release, adapter, generated-output, and material-review boundaries remain intact

- Covers: `R2`, `R14`-`R16`, `E2`, `E4`, `EC4`, `EC10`
- Level: contract, manual
- Fixture/setup:
  - final implementation diff
  - `docs/workflows.md`
  - release and adapter support surfaces if touched
  - review-resolution artifacts if triggered
- Steps:
  - Confirm implementation does not change release validation, adapter packaging, generated public adapter output, token-cost report validation, material-finding closeout, or generated-output drift rules.
  - Confirm `skills/` remains the authored skill source if any skill wording changes.
  - Confirm no generated public adapter skill bodies are added back to tracked source.
  - If release metadata or generated adapter release output changes unexpectedly, stop and route to the appropriate later slice or proposal.
- Expected result: M3 preserves completed single-source and release/adapter boundaries.
- Failure proves: M3 reopened completed cleanup tracks or weakened release/review safety.
- Automation location: manual final diff review, selected validation output, release/adapter checks only if a later approved scope requires them.

### T9. Dirty-worktree compatible selected validation is used

- Covers: `R1`, `R17`, `E1`, `EC5`, `EC8`, `EC9`
- Level: integration, smoke
- Fixture/setup:
  - changed implementation paths
  - `scripts/select-validation.py`
  - `scripts/ci.sh`
  - active plan and change-local artifacts
- Steps:
  - Run `python scripts/select-validation.py --mode explicit` with changed implementation paths and changed lifecycle artifacts.
  - Run `bash scripts/ci.sh --mode explicit` with the same path set.
  - Confirm selected checks match changed paths and include lifecycle, review-artifact, change-metadata, selector, or skill checks when their paths are touched.
  - Confirm no changed path is unclassified before relying on selected validation.
  - Confirm broad smoke is not required unless an authoritative trigger is present.
- Expected result: validation is targeted, complete for changed paths, and safe in a dirty worktree.
- Failure proves: proof is either under-selected, path-incomplete, or unnecessarily broad.
- Automation location: selected validation and selected CI output.

### T10. No-change rationale and observability evidence are durable

- Covers: `R5`, `R10`, `R18`, `R19`, `E6`
- Level: contract, manual
- Fixture/setup:
  - active plan
  - change metadata
  - explain-change when created
  - final implementation diff
- Steps:
  - Confirm implementation records changed owner surfaces.
  - Confirm implementation records whether selector behavior changed, stayed unchanged with rationale, or was deferred to a later selector slice.
  - Confirm implementation records whether broad smoke was required and why.
  - Confirm no-change rationale exists for `docs/workflows.md`, selector behavior, or stage skills that already satisfy the M3 contract.
  - Confirm selected check IDs and commands run are recorded in validation evidence.
- Expected result: reviewers can evaluate M3 without relying on chat-only rationale.
- Failure proves: M3 lacks durable evidence for changed or unchanged validation owner surfaces.
- Automation location: manual review of active plan, change metadata, explain-change, and validation notes.

### T11. Final verification matches governing validation triggers

- Covers: `R2`, `R14`, `R15`, `R17`, `R18`, `E2`-`E4`, `EC1`-`EC4`, `EC10`
- Level: manual, contract, smoke
- Fixture/setup:
  - accepted plan
  - active test spec
  - review-resolution if triggered
  - release metadata if touched
  - selected validation output
  - verify output
- Steps:
  - During final verify, compare actual validation evidence against the accepted plan, this test spec, review-resolution, and release metadata triggers.
  - Confirm broad smoke ran when any authoritative trigger required it, or confirm no trigger existed.
  - Confirm any required review-resolution, release validation, adapter validation, generated-output drift check, skill validation, or lifecycle validation evidence exists when its path or artifact requires it.
  - Confirm inability to run required validation blocks readiness unless a governing artifact explicitly allows a temporary state with rationale, owner, and follow-up.
- Expected result: final verify can prove M3 satisfied targeted validation without skipping mandatory stronger proof.
- Failure proves: validation-budget guidance caused under-validation or mismatched evidence.
- Automation location: `verify` output, selected CI output, review-resolution and release metadata when present.

## Fixtures and data

- Workflow guidance and owner surface:
  - `docs/workflows.md`
- Selector and wrapper surfaces:
  - `scripts/validation_selection.py`
  - `scripts/select-validation.py`
  - `scripts/ci.sh`
  - `scripts/test-select-validation.py`
- Stage skills for audit or no-change rationale:
  - `skills/workflow/SKILL.md`
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/verify/SKILL.md`
- Lifecycle and review surfaces:
  - `specs/cost-bounded-rigor-m3-validation-budget-guidance.md`
  - `specs/cost-bounded-rigor-m3-validation-budget-guidance.test.md`
  - `docs/plans/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance.md`
  - `docs/plan.md`
  - `docs/changes/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance/`

No new runtime fixtures, adapter fixtures, release fixtures, generated output fixtures, or benchmark fixtures are required for M3.

## Mocking/stubbing policy

No mocks or stubs are required for final proof. Tests operate on repository files and repository-owned validation scripts. Do not mock `scripts/select-validation.py`, `scripts/ci.sh`, or review/lifecycle validators for final M3 proof.

Temporary fixtures inside `scripts/test-select-validation.py` are acceptable only for selector regression tests, broad-smoke source attribution, unclassified-path blocking, or wrapper execution behavior.

## Migration or compatibility tests

No data migration is required. Compatibility proof is manual and static:

- existing selector behavior remains valid unless a later approved plan/test-spec revision scopes a focused selector change;
- existing broad-smoke triggers remain valid;
- existing release and adapter validation behavior remains valid;
- existing stage skills remain valid unless they contradict the M3 contract;
- rollback for guidance-only implementation is removal of unnecessary wording while preserving existing selector behavior and mandatory validation rules.

## Observability verification

No runtime logs, metrics, traces, or hosted observability changes are required. Observable proof is:

- owner-surface decisions;
- selected check IDs and commands run;
- whether selector behavior changed;
- whether broad smoke was required and why;
- no-change rationale for unaffected owner surfaces;
- any validation conflicts between selector output and governing artifacts.

## Security/privacy verification

- Confirm M3 does not introduce secrets, credentials, external services, or new data exposure.
- Confirm guidance still prefers targeted paths, stable IDs, counts, diffs, and excerpts over broad dumps of logs or generated output.
- Confirm security-sensitive validation gates, release gates, material-review closeout, and generated-output validation remain intact.

## Performance checks

- No dynamic benchmark comparison is required for M3.
- No token-cost measurement is required unless implementation unexpectedly changes canonical skill wording and the active plan is revised to include that proof.
- Do not introduce hard token gates.
- Treat any optional measurement as diagnostic and warning-only.

## Manual QA checklist

- Confirm the owner-surface audit covers workflow guidance, selector behavior, wrapper behavior, and validation-related stage skills.
- Confirm targeted validation is presented as the first layer when changed paths are known.
- Confirm broad-smoke triggers remain mandatory and source-attributed.
- Confirm selector behavior is recorded as changed, unchanged with rationale, or deferred.
- Confirm skill-local wording, if any, is concise and subordinate to `docs/workflows.md`.
- Confirm forbidden release, adapter, generated-output, dynamic benchmark, token-gate, and progressive-loading surfaces remain untouched.
- Confirm validation evidence names the actual commands run.
- Confirm final verify checks validation evidence against plan, test spec, review-resolution, and release metadata triggers.

## What not to test

- Do not test runtime end-to-end behavior; RigorLoop has no deployed runtime for this slice.
- Do not run release validation, adapter packaging validation, generated public adapter archive checks, or adapter smoke unless a later approved artifact broadens scope.
- Do not run broad smoke by default.
- Do not run dynamic token benchmarks by default.
- Do not add lifecycle token-cost summary artifacts.
- Do not require exact workflow prose when stable behavior cues prove the contract.
- Do not add natural-language semantic scoring for validation sufficiency.
- Do not retest all M1 scope-budget or M2 selected-skill-reminder behavior except where needed to prove M3 owner boundaries.

## Uncovered gaps

None. If implementation discovers that M3 requires selector behavior changes, release/adapter work, dynamic benchmarks, lifecycle token-cost summaries, hard token gates, or progressive-loading restructuring, stop and route that work through a plan revision or later accepted slice before implementation continues.

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

Active proof-planning surface for M3. Implementation may proceed under the approved M3 spec, reviewed M3 plan, and this test spec.
