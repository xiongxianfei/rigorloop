# Skill Readability and Self-Containment Test Spec

## Status

active

## Related spec and plan

- Spec: [skill-readability-contract.md](skill-readability-contract.md)
- Plan: [2026-05-18-skill-readability-self-containment.md](../docs/plans/2026-05-18-skill-readability-self-containment.md)
- Proposal: [2026-05-18-skill-readability-self-containment.md](../docs/proposals/2026-05-18-skill-readability-self-containment.md)
- Change evidence: [docs/changes/2026-05-18-skill-readability-self-containment](../docs/changes/2026-05-18-skill-readability-self-containment)

Architecture and ADR artifacts are not required for this change. The approved spec and clean plan-review records scope the work to canonical skill text, focused validation, generated-output evidence, cold-read proof, behavior-parity proof, and token-cost evidence without changing runtime architecture, persistence, APIs, adapter package format, release archive format, or workflow stage semantics.

## Testing strategy

The pilot is verified through a staged proof surface:

- Unit: focused validator tests in `scripts/test-skill-validator.py` for workflow role blocks, output skeletons, forbidden internal references, known closed enum placement, and front matter compatibility.
- Contract/static: `scripts/validate-skills.py`, `scripts/build-skills.py --check`, and artifact lifecycle validators prove canonical skill shape, generated-output derivation, and lifecycle state.
- Integration: temporary adapter build and adapter validation prove installed output is derived from canonical source and inspectable for cold-read.
- Manual: cold-read checklist and behavior-parity classification record quality and clarity conditions that cannot be fully automated without turning validation into semantic prose scoring.
- Performance: `scripts/measure-skill-tokens.py` records baseline and after-change token counts for the pilot pair and checks the R49-R52 thresholds.
- Migration/compatibility: front matter compatibility and generated-output boundaries are checked before shipping `version` or `schema-version`.

The test order follows the plan:

1. Define tests and baseline evidence before rewriting skill text.
2. Rewrite the pilot pair only after tests and token baseline exist.
3. Prove generated-output derivation, cold-read self-containment, behavior parity, and token thresholds before rollout handoff.

## Requirement coverage map

| Requirement | Tests | Notes |
|---|---|---|
| R1 | T1, T10, T16 | Canonical source remains under `skills/`. |
| R2 | T10, T16 | Generated adapter output is derived and not hand-edited. |
| R3 | T9, T11, T14, T16 | Normative behavior parity is checked before rollout. |
| R4 | T9, T11, T14, T16 | Quality regressions block rollout. |
| R5 | T13, T14, T16 | Priority order is checked during review and evidence recording. |
| R6 | T12, T13, T14 | Token savings cannot justify quality or clarity regressions. |
| R7 | T5, T9, T16 | Installed pilot skills must be self-contained. |
| R8 | T5, T9 | Unavailable internal runtime dependencies fail or block. |
| R9 | T5, T9 | Legitimate project-local references remain allowed. |
| R10 | T5, T9, T16 | Portable defaults and ambiguity blocking are cold-read items. |
| R11 | T2, T7, T9 | Workflow role block is statically and manually checked. |
| R12 | T2, T9 | Required fields are checked. |
| R13 | T2 | `role_name` must match skill name. |
| R14 | T2 | Closed `stage` enum is checked. |
| R15 | T2, T9 | Summary length is checked statically or manually. |
| R16 | T3, T7, T16 | Known closed enums are fenced or tabled exactly once. |
| R17 | T3, T7 | Duplicate enum prose is rejected where known. |
| R18 | T3, T7, T11 | Existing enum spelling and membership are preserved. |
| R19 | T4, T7, T9 | Long named enumerations use tables. |
| R20 | T4, T16 | Ordered procedures may remain lists when order is the contract. |
| R21 | T7, T9, T16 | Intra-skill deduplication is review-checked. |
| R22 | T7, T16 | Intentional safety reminders must identify themselves. |
| R23 | T6, T7, T9 | Workflow-wide rules are labeled. |
| R24 | T6, T7, T9 | Skill-local and workflow-wide rules are distinguishable. |
| R25 | T8, T9 | Pilot artifact-producing skills have fenced output skeletons. |
| R26 | T8, T9, T11 | Skeletons include required top-level fields. |
| R27 | T8 | Skeletons use fillable placeholders. |
| R28 | T8, T11 | Review skill result and recording fields are preserved. |
| R29 | T1, T7, T8, T9, T10, T11, T12 | Pilot covers `proposal` and `proposal-review`. |
| R30 | T15, T16 | Remaining rollout list is recorded as follow-on work. |
| R31 | T15 | Out-of-list adoption stays optional unless later approved. |
| R32 | T10, T16 | Front matter is checked before pilot shipping. |
| R33 | T10 | `schema-version` value is checked. |
| R34 | T10, T16 | `version` value must be chosen and applied consistently. |
| R35 | T10 | Existing consumers tolerate unknown front matter fields. |
| R36 | T2, T7 | Static validation checks workflow role blocks. |
| R37 | T8 | Static validation checks output skeletons. |
| R38 | T5 | Static validation checks forbidden required internal references. |
| R39 | T3 | Known closed enum duplicate checks are optional but expected in pilot tests. |
| R40 | T5 | Project-local references are allowed when clearly conditional. |
| R41 | T9 | Cold-read is required before full rollout. |
| R42 | T9, T10 | Cold-read inspects installed adapter output. |
| R43 | T9 | Normative references must resolve to installed or project-local artifacts. |
| R44 | T9 | Cold-read discoverability checklist covers role, enums, sections, skeletons, handoff, stop conditions, and rule scope. |
| R45 | T11 | Behavior parity compares rewritten pilot outputs to baseline outputs. |
| R46 | T11 | Differences are classified. |
| R47 | T11, T16 | Any regression blocks rollout until resolved or spec-changed. |
| R48 | T12 | Token measurement compares baseline and rewritten skills. |
| R49 | T12 | Zero-regression target is recorded. |
| R50 | T12, T13 | Up to five percent increase requires recorded readability justification. |
| R51 | T12, T16 | Greater than ten percent blocks rollout unless spec changes. |
| R52 | T12, T13, T14 | Token thresholds cannot override quality or clarity floors. |
| R53 | T5, T7, T16 | Plan's pilot blocking/non-pilot warning lint mode is implemented and recorded. |
| R54 | T1, T10, T16 | Out-of-scope packaging, partials, format, and legacy archive changes are excluded. |
| R55 | T2, T16 | Missing workflow role block fails or must have out-of-scope rationale. |
| R56 | T8, T16 | Missing output skeleton fails or must have out-of-scope rationale. |
| R57 | T5, T9, T16 | Unresolvable cold-read reference blocks rollout. |
| R58 | T11, T16 | Behavior regression blocks rollout. |
| R59 | T12, T16 | Token hard-cap breach blocks rollout. |
| R60 | T6, T7, T16 | Ambiguous rule ownership is preserved and recorded, not deleted. |

## Example coverage map

| Example | Tests | Notes |
|---|---|---|
| E1 proposal skill exposes artifact shape | T2, T3, T4, T8, T9 | Role, tabled sections, fenced enums, and skeleton are checked. |
| E2 proposal-review preserves review quality | T8, T9, T11, T14 | Review result shape and behavior parity are checked. |
| E3 cold-read catches dangling internal reference | T5, T9 | Forbidden internal reference and installed-output cold-read checks cover this. |
| E4 token reduction cannot override clarity | T3, T12, T13, T14 | Token deltas are subordinate to enum and clarity preservation. |
| E5 workflow-wide rule is marked | T6, T7, T9 | Rule-scope labeling is checked. |

## Edge case coverage

| Edge case | Tests | Expected handling |
|---|---|---|
| Skill has no durable output artifact | T8, T15 | Non-artifact-producing status must be recorded; pilot pair is artifact-producing. |
| Closed enum appears in output skeleton | T3, T8 | Authoritative enum remains in one fenced block or table; skeleton references rather than restates values. |
| Skill mentions `docs/workflows.md` | T5, T9 | Allowed only as project-local/conditional, not required RigorLoop repository context. |
| Ordered procedure is clearer as a list | T4, T16 | Manual review accepts list when order is the contract. |
| Safety-critical rule appears in multiple skills | T7, T16 | Cross-skill repetition is allowed for self-containment; duplicate within one skill needs reminder labeling. |
| Rewritten review skill misses a material finding | T11 | Classified as `regression` and blocks rollout. |
| Token increase exceeds five percent but improves clarity | T12, T13 | Allowed only at or below ten percent with recorded readability justification. |
| Front matter consumer rejects unknown fields | T10 | Block or defer front matter until compatibility is resolved. |

## Test cases

### T1. Pilot scope and source boundaries are preserved

- Covers: R1, R2, R29, R54
- Level: contract
- Fixture/setup: current git diff and repository tree after each milestone.
- Steps:
  - Confirm edited authored skill files are under `skills/proposal/SKILL.md` and `skills/proposal-review/SKILL.md`.
  - Confirm no generated adapter skill body is hand-edited or added as tracked authored source.
  - Confirm no build-time partial/include mechanism, adapter package format, manifest format, release archive contract, or legacy archive rewrite is introduced.
  - Confirm non-pilot R30 skills are not rewritten in this pilot unless the plan is revised.
- Expected result: pilot scope is limited to canonical source, focused validation, evidence, and lifecycle artifacts.
- Failure proves: the implementation exceeded pilot scope or violated source/generated-output ownership.
- Automation location: manual diff review, `git status --short`, `git diff --name-only`, `python scripts/build-skills.py --check`.

### T2. Workflow role block validation covers required fields and stage enum

- Covers: R11, R12, R13, R14, R15, R36, R55, E1
- Level: unit
- Fixture/setup: positive and negative skill fixtures for `proposal` and `proposal-review`, plus canonical pilot skill files after rewrite.
- Steps:
  - Add failing validator cases for missing workflow role block, missing field, mismatched `role_name`, invalid `stage`, and overlong summary.
  - Run the validator against failing fixtures and confirm each defect is named.
  - Run the validator against rewritten pilot skills and confirm both pass.
- Expected result: pilot skills include valid workflow role blocks near the top with required fields and allowed stage values.
- Failure proves: readers cannot reliably identify lifecycle role or stage, or static validation misses a required role defect.
- Automation location: `scripts/test-skill-validator.py`, `scripts/validate-skills.py`.

### T3. Closed enum placement and duplicate enum checks are enforced for known pilot enums

- Covers: R16, R17, R18, R39, E1, E4
- Level: unit
- Fixture/setup: validator fixtures containing known pilot closed enums for status, Vision fit, review status/verdict, recording status, finding disposition, and behavior-parity classification.
- Steps:
  - Add negative fixture coverage for missing fenced/table enum, duplicate authoritative enum block, and changed enum value spelling.
  - Run validator tests and confirm each defect is detected for known pilot enums.
  - Review pilot skills to confirm closed enum values appear in exactly one authoritative fenced block or table per skill.
- Expected result: valid enum values are scannable and not silently reworded or duplicated in prose.
- Failure proves: the rewrite risks silent enum drift or unclear value discovery.
- Automation location: `scripts/test-skill-validator.py`, `scripts/validate-skills.py`, manual review for enum values not yet known to validator.

### T4. Long named enumerations use tables unless ordered procedure is clearer

- Covers: R19, R20, E1
- Level: manual
- Fixture/setup: rewritten `proposal` and `proposal-review` skill text.
- Steps:
  - Identify required proposal sections, review dimensions, decision-quality checklists, closed classifications, and other named enumerations in the pilot pair.
  - Confirm named-field/comparison/classification lists use tables.
  - Confirm any retained list is an ordered procedure or has a recorded clarity rationale.
- Expected result: scannable contracts use tables, while order-sensitive procedures remain readable lists.
- Failure proves: the rewrite missed the clarity goal or forced a table where it harms procedure clarity.
- Automation location: manual review checklist in change-local implementation notes or code-review evidence.

### T5. Forbidden internal reference lint blocks required unavailable context and allows project-local references

- Covers: R7, R8, R9, R10, R38, R40, R53, R57, E3
- Level: unit
- Fixture/setup: positive and negative skill fixtures with references to `specs/`, `schemas/`, `docs/workflows.md`, `CONSTITUTION.md`, `AGENTS.md`, and project-local guarded variants.
- Steps:
  - Add negative fixtures where skill text requires RigorLoop repository-internal paths as runtime context.
  - Add positive fixtures where the same path is clearly conditional/project-local, such as "if present in the user's project."
  - Confirm pilot-touched skills fail on unqualified required internal references.
  - Confirm non-pilot skills are warning-only or out of blocking enforcement during this pilot, matching the plan.
- Expected result: unavailable repository-internal references cannot become required adopter context, while legitimate project-local guidance remains allowed.
- Failure proves: installed skills are not self-contained or validation rejects valid adopter-local references.
- Automation location: `scripts/test-skill-validator.py`, `scripts/validate-skills.py`.

### T6. Workflow-wide and skill-local rule boundaries remain distinguishable

- Covers: R23, R24, R60, E5
- Level: manual
- Fixture/setup: rewritten pilot skill text and implementation notes.
- Steps:
  - Confirm workflow-wide rules use an explicit label or section boundary.
  - Confirm skill-local rules are distinguishable by section placement, label, or wording.
  - Confirm any ambiguous rule is kept and recorded for spec or plan resolution rather than deleted or weakened.
- Expected result: users can tell which obligations apply across the workflow and which are local to the skill.
- Failure proves: the rewrite can cause incorrect handoff, recording, or scope behavior.
- Automation location: manual review checklist and code-review evidence.

### T7. Pilot skill static and editorial contract review

- Covers: R16, R17, R18, R21, R22, R23, R24, R29, R36, R39, R53, R60
- Level: contract
- Fixture/setup: rewritten `skills/proposal/SKILL.md` and `skills/proposal-review/SKILL.md`.
- Steps:
  - Run focused static validation.
  - Manually review intra-skill rule deduplication, intentional safety reminders, workflow-wide labels, skill-local boundaries, and closed enum preservation.
  - Confirm validator checks stay focused on explicit headings, fields, blocks, and path phrases rather than semantic prose scoring.
- Expected result: pilot skills satisfy the readability contract without introducing brittle natural-language validation.
- Failure proves: the implementation either under-validates required contract shape or overfits prose wording.
- Automation location: `scripts/test-skill-validator.py`, `scripts/validate-skills.py`, manual code-review checklist.

### T8. Output skeletons preserve required artifact and review result shape

- Covers: R25, R26, R27, R28, R37, R56, E1, E2
- Level: unit
- Fixture/setup: positive and negative skill fixtures for artifact-producing skills, plus rewritten pilot pair.
- Steps:
  - Add validator cases for missing fenced output skeleton, missing required top-level fields, and prose-only placeholders.
  - Confirm `proposal` skeleton includes required proposal sections.
  - Confirm `proposal-review` skeleton preserves the required `## Result` block and formal review recording fields.
  - Confirm review recording skeleton does not weaken review-resolution boundaries.
- Expected result: users can copy/fill the expected artifact shape without reading repository specs.
- Failure proves: artifact-producing skills still lack a self-contained output contract.
- Automation location: `scripts/test-skill-validator.py`, `scripts/validate-skills.py`, manual review for field completeness.

### T9. Cold-read installed adapter output proves self-containment and scanability

- Covers: R7, R8, R10, R11, R15, R19, R23, R24, R25, R26, R29, R41, R42, R43, R44, R57, E1, E3, E5
- Level: manual
- Fixture/setup: temporary adapter output generated outside tracked source and installed into a fresh empty project.
- Steps:
  - Build adapter output to a temporary directory.
  - Install or inspect the adapter output in a clean project without using repository `specs/`, `schemas/`, or internal docs as context.
  - For `proposal` and `proposal-review`, confirm workflow role, valid enums, required sections, output skeleton, handoff, stop conditions, and workflow-wide versus skill-local rule boundaries are discoverable.
  - Confirm every normative reference resolves to installed skill text or project-local artifacts visible to an adopter.
  - Record the inspected adapter output path and pass/fail checklist in the change-local pack.
- Expected result: the installed pilot pair is readable and self-contained without RigorLoop repository context.
- Failure proves: the user-facing contract still depends on unavailable maintainer context or is not scannable.
- Automation location: manual cold-read report under `docs/changes/2026-05-18-skill-readability-self-containment/` or a report path chosen during M3.

### T10. Generated-output, adapter validation, and front matter compatibility hold

- Covers: R1, R2, R32, R33, R34, R35, R42, R54
- Level: integration
- Fixture/setup: rewritten pilot pair and temporary adapter output directory.
- Steps:
  - Confirm `schema-version` is `skill-readability-v1` when front matter is added.
  - Confirm the pilot pair uses a consistent `version` value chosen during implementation.
  - Run canonical skill validation and generated skill check.
  - Build adapters to a temporary output directory and run adapter validation.
  - Confirm no existing consumer rejects unknown `version` or `schema-version`; if one does, defer or remove the fields before shipping.
- Expected result: front matter is additive and generated output remains derived from canonical source.
- Failure proves: the rewrite breaks compatibility or generated-output ownership.
- Automation location: `scripts/validate-skills.py`, `python scripts/build-skills.py --check`, `python scripts/build-adapters.py --version <current-or-next-version> --output-dir /tmp/rigorloop-skill-readability-adapters`, `python scripts/validate-adapters.py --root /tmp/rigorloop-skill-readability-adapters --version <current-or-next-version>`.

### T11. Behavior parity blocks quality regressions

- Covers: R3, R4, R18, R26, R28, R45, R46, R47, R58, E2
- Level: manual
- Fixture/setup: representative proposal fixture and representative proposal-review fixture selected during M1; baseline outputs from unrewritten skills; rewritten outputs from pilot skills.
- Steps:
  - Run or simulate the baseline `proposal` and `proposal-review` skills on representative inputs before rewrite, preserving outputs or review notes in the change-local pack.
  - Run or simulate rewritten skills on the same inputs after rewrite.
  - Compare required sections, verdicts/statuses, finding severity, rationale strength, scope preservation, handoff clarity, stop conditions, and recording fields.
  - Classify each observed difference as `equivalent`, `improvement`, or `regression`.
  - Block rollout for any `regression` unless a later approved spec changes the behavior.
- Expected result: rewritten skills preserve or improve output quality and do not miss required findings or artifact fields.
- Failure proves: the rewrite weakened the quality floor.
- Automation location: behavior-parity report under `docs/changes/2026-05-18-skill-readability-self-containment/` or fixture directory/report path chosen during M1.

### T12. Token-cost measurement enforces thresholds without overriding quality

- Covers: R6, R29, R48, R49, R50, R51, R52, R59, E4
- Level: performance
- Fixture/setup: baseline and after-change token measurements for `proposal` and `proposal-review`.
- Steps:
  - Record baseline token counts before rewriting pilot skills.
  - Record after-change token counts after rewrite.
  - Compute absolute and percentage delta for each pilot skill.
  - Confirm zero-regression target, five percent tolerance, and ten percent hard cap are applied.
  - Block rollout for any hard-cap breach unless the spec is revised.
- Expected result: token deltas are visible and within the approved thresholds or blocked.
- Failure proves: token-cost regressions are unmanaged or quality/clarity priorities were inverted.
- Automation location: `python scripts/measure-skill-tokens.py`, token report at `docs/reports/token-cost/skills/2026-05-18-skill-readability-self-containment.md`.

### T13. Accepted token increase requires readability justification and quality floor proof

- Covers: R5, R6, R50, R52, E4
- Level: manual
- Fixture/setup: token report and behavior-parity/cold-read evidence.
- Steps:
  - If a pilot skill increases token cost up to five percent, confirm the change-local pack records the readability gain.
  - Confirm behavior-parity and cold-read checks passed before accepting the increase.
  - Confirm no token saving or token increase is accepted when it removes required enums, skeleton fields, stop conditions, or recording obligations.
- Expected result: token cost remains a constraint, not the driver.
- Failure proves: token metrics are overriding quality or clarity.
- Automation location: manual report review in change-local pack and code-review checklist.

### T14. Priority-order review protects output quality and clarity

- Covers: R3, R4, R5, R6, R52, E2, E4
- Level: manual
- Fixture/setup: final pilot diff, behavior-parity evidence, cold-read evidence, token report.
- Steps:
  - Confirm high-quality skill output is preserved before accepting any clarity or token changes.
  - Confirm clarity and concision are improved or preserved before accepting token changes.
  - Confirm token-cost changes are not used to justify weaker artifacts, verdicts, rationale, scope preservation, handoff, stop conditions, or recording behavior.
- Expected result: final review follows the spec priority order.
- Failure proves: implementation inverted the user-stated priority ranking.
- Automation location: code-review, explain-change, and verify checklists.

### T15. Follow-on rollout ownership preserves full R30 scope

- Covers: R30, R31
- Level: contract
- Fixture/setup: M3 follow-on rollout record, plan update, or `docs/follow-ups.md` entry if needed.
- Steps:
  - Confirm M3 records follow-on ownership for every R30 skill outside the pilot pair.
  - Confirm no R30 skill is silently excluded; any exclusion must be justified by plan revision or later approved artifact.
  - Confirm skills outside R30 remain optional unless later approved scope adds them.
- Expected result: the pilot does not erase the full rollout contract.
- Failure proves: the change ships the pilot but drops required follow-on ownership.
- Automation location: manual lifecycle review, plan update, optional follow-up register entry.

### T16. Stop-condition and closeout gate review

- Covers: R1, R3, R4, R10, R20, R21, R22, R30, R32, R34, R47, R51, R53, R54, R55, R56, R57, R58, R59, R60
- Level: contract
- Fixture/setup: final implementation evidence, validation logs, review records, plan state, and change metadata.
- Steps:
  - Confirm all required validation evidence exists for touched surfaces.
  - Confirm missing role block, missing output skeleton, unresolved cold-read reference, behavior regression, token hard-cap breach, or ambiguous rule ownership triggers stop or recorded resolution.
  - Confirm no forbidden packaging, partial/include, stage-order, adapter format, manifest, release archive, or generated-output hand-editing change is present.
  - Confirm plan and `docs/plan.md` state are synchronized before PR handoff.
- Expected result: closeout blocks on unresolved contract violations and records any accepted exceptions.
- Failure proves: final lifecycle state can claim readiness despite unresolved quality, clarity, scope, or compatibility defects.
- Automation location: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`, `python scripts/validate-change-metadata.py docs/changes/2026-05-18-skill-readability-self-containment/change.yaml`, `python scripts/validate-review-artifacts.py docs/changes/2026-05-18-skill-readability-self-containment`, final selected CI, manual verify.

## Fixtures and data

- Canonical pilot skills:
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
- Existing fixture root for validator tests: `tests/fixtures/skills/`
- New focused validator fixtures should live under a scoped subdirectory of `tests/fixtures/skills/` if fixture files are needed.
- Behavior-parity fixtures should use synthetic or public-safe proposal/review inputs. Preferred location: `tests/fixtures/skills/skill-readability/behavior-parity/` or a change-local report path chosen in M1.
- Cold-read output should use a temporary adapter output directory such as `/tmp/rigorloop-skill-readability-adapters` and record the inspected installed skill paths in the change-local pack.
- Token evidence should be recorded in `docs/reports/token-cost/skills/2026-05-18-skill-readability-self-containment.md`.
- Lifecycle evidence lives under `docs/changes/2026-05-18-skill-readability-self-containment/`.

## Mocking/stubbing policy

Do not mock final validation of canonical skill files, generated adapter output, token measurement, artifact lifecycle validation, change metadata validation, or review artifact validation.

Temporary synthetic fixtures are allowed for unit tests in `scripts/test-skill-validator.py`. Temporary adapter output under `/tmp` is allowed for generated-output and cold-read proof. Behavior-parity fixtures may be synthetic, but final classification must compare baseline and rewritten skill outputs or recorded reviewer judgments on the same input.

Do not rely on snapshots alone for behavior parity. Snapshot-like text comparisons are allowed only as supporting evidence for required sections, fields, or known markers.

## Migration or compatibility tests

- T10 covers compatibility for additive `version` and `schema-version` front matter.
- T1 and T10 cover generated-output ownership and adapter validation.
- T16 covers rollback and no forbidden package/format/stage behavior changes.
- No data migration is required.

## Observability verification

Required evidence:

- Static validation output names the skill and missing contract element.
- Cold-read evidence names the adapter output inspected, skills inspected, and pass/fail checklist items.
- Behavior-parity evidence names each fixture, compared skill, and `equivalent`, `improvement`, or `regression` classification.
- Token-cost evidence names baseline tokens, after-change tokens, percentage delta, and accepted-increase rationale if any.
- Change-local evidence records rollout-blocking defects and their resolution or stop state.

## Security/privacy verification

- Fixtures must use synthetic or public-safe proposal/review content.
- Cold-read projects must not require secrets, private keys, tokens, private repository metadata, or unrelated machine-local paths.
- Installed skill text must not require adopters to expose private data to satisfy this spec.
- Generated adapter output must not expose repository-maintainer-only implementation mechanics as user-facing requirements.

## Performance checks

Run `python scripts/measure-skill-tokens.py` before and after pilot skill rewrite. Record baseline, after-change count, percentage delta, target status, tolerance status, hard-cap status, and any accepted readability justification in the token report.

Performance checks are subordinate to behavior parity and cold-read quality. A lower token count does not pass the test spec if output quality or clarity regresses.

## Manual QA checklist

- Open installed adapter output for `proposal` and `proposal-review` without using repository specs or internal docs.
- Confirm workflow role is discoverable near the top.
- Confirm closed enums are in fenced blocks or tables and not duplicated in prose.
- Confirm required proposal/review sections are tabled where appropriate.
- Confirm output skeletons are fenced, fillable, and complete.
- Confirm formal review result and recording fields are preserved in `proposal-review`.
- Confirm workflow-wide and skill-local rules are distinguishable.
- Confirm stop conditions remain visible.
- Confirm project-local references are conditional and adopter-visible.
- Confirm behavior-parity differences are classified and no `regression` remains.
- Confirm token increases, if any, are within thresholds and justified.
- Confirm follow-on ownership for non-pilot R30 skills is recorded.

## What not to test

- Do not test build-time partials or include mechanisms; they are out of scope.
- Do not test adapter package format, manifest format, release archive format, or legacy archive migration beyond proving they were not changed.
- Do not run broad release validation unless implementation unexpectedly touches release or adapter packaging surfaces.
- Do not require dynamic LLM execution for every behavior-parity case; representative fixture comparison and recorded reviewer classification are sufficient for this pilot.
- Do not rewrite or validate every R30 skill in this pilot. Record follow-on ownership instead.
- Do not add semantic prose scoring that rejects valid equivalent wording.

## Uncovered gaps

None. If implementation discovers that behavior-parity fixture selection, front matter compatibility, or forbidden-path lint enforcement cannot be decided within the current plan, stop and route the issue to plan revision or spec revision before implementation continues.

## Next artifacts

- `implement` M1: static validator foundations and baseline evidence.
- `code-review` for M1 after implementation closes the milestone.

## Follow-on artifacts

None yet.

## Readiness

This test spec is active and ready for M1 implementation. Implementation remains limited to `M1. Static validator foundations and baseline evidence` until that milestone is closed and reviewed.
