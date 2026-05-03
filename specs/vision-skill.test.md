# Vision Skill Test Spec

## Status

- active

## Related spec and plan

- Spec: [Vision Skill](vision-skill.md)
- Migration spec: [Vision Skill Simplification and VISION.md Migration](vision-skill-simplification-and-vision-md-migration.md), approved after spec-review on 2026-05-01.
- Active plan: [2026-05-01 Vision Skill Simplification and VISION.md Migration](../docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md)
- Related proposal: [Vision Skill Simplification and VISION.md Migration](../docs/proposals/2026-05-01-vision-skill-simplification-and-vision-md-migration.md)
- Prior proposal: [Vision Skill](../docs/proposals/2026-04-29-vision-skill.md)
- Prior refinement: [Vision Skill Quality Refinement](../docs/proposals/2026-04-30-vision-skill-quality-refinement.md)
- Architecture: not required. The active change is a workflow-governance, source-of-truth, selector, skill, README, spec, and generated-output migration without a runtime boundary, data store, dependency, deployment boundary, or architecture package.
- Spec-review findings: approved on 2026-05-01 after the no-vision and migration-recognized legacy `vision.md` behavior was clarified.
- Plan-review findings: approved on 2026-05-01 after test-spec creation moved to the immediate `test-spec` stage and implementation milestones were made test-first and green by closeout.

## Testing strategy

- Contract tests inspect authored Markdown for `VISION.md` source-of-truth wording, state-based `vision` skill behavior, proposal `Vision fit` status-line rules, and retirement of the old lowercase-path and user-facing mode model.
- Selector unit and fixture tests prove `VISION.md`, migration-time legacy `vision.md`, README marker validation, PR-mode routing, and both-file conflict behavior.
- Migration proof combines Git rename inspection, root-file existence checks, selector behavior, and manual diff review to prove the final branch has exactly one canonical vision artifact and does not rewrite historical artifacts.
- Generated-output integration uses existing generators so `.codex/skills/` and `dist/adapters/` remain derived from canonical `skills/`.
- Lifecycle and metadata proof keeps the approved spec, active test spec, active plan, proposal follow-ons, and change-local metadata coherent.

## Requirement coverage map

| Requirement IDs | Test IDs | Notes |
| --- | --- | --- |
| `R1`-`R8` | `T1`, `T2`, `T10` | Canonical path, source order, README source boundary, and historical-reference scope. |
| `R9`-`R19` | `T3`, `T10` | Skill metadata, state-based interface, legacy intent handling, and output reporting. |
| `R20`-`R31` | `T4`, `T5`, `T10` | Establishment, update, sync, overwrite protection, both-file conflict, and causal-link gates. |
| `R32`-`R39`, `R68`-`R72` | `T6`, `T10` | Vision prose quality, security, research, readability, and bounded reads. |
| `R40`-`R48` | `T7` | README marker pair, generated front-matter contents, marker insertion limits, and no helper script. |
| `R49`-`R62` | `T8` | Proposal and proposal-review `Vision fit` behavior. |
| `R63`-`R67` | `T1`, `T9`, `T10` | Workflow boundary, generated-output ownership, selector classification, and both-path validation failure. |

## Example coverage map

| Example | Test IDs | Notes |
| --- | --- | --- |
| `E1` | `T4`, `T7` | Establishing project vision creates `VISION.md` and deterministic README markers. |
| `E2` | `T3`, `T4` | Installing or regenerating the skill does not create root vision content. |
| `E3` | `T5` | Existing vision updates remain bounded and classified. |
| `E4` | `T7` | README sync leaves `VISION.md` unchanged. |
| `E5` | `T8` | Proposal guidance requires `Vision fit` when a vision exists. |
| `E6` | `T8` | Proposal guidance handles the no-vision state. |
| `E7` | `T8` | Proposal-review classifies vision conflicts. |
| `E8` | `T3` | Legacy wording can be interpreted as intent without preserving a mode interface. |

## Edge case coverage

- Root `vision.md` exists and root `VISION.md` does not: `T2`, `T9`
- Root `VISION.md` exists and root `vision.md` also exists: `T5`, `T9`
- Neither root vision file exists and README already has markers: `T4`, `T7`
- Root `VISION.md` exists and README lacks markers: `T7`
- README has malformed, nested, or multiple marker pairs: `T7`
- Proposal says `fits the current vision` while no canonical or migration-recognized legacy vision exists: `T8`
- Proposal omits `Vision fit` after adoption: `T8`
- Vision update changes scope but is labeled editorial: `T5`
- User asks to update vision but does not name a section or direction: `T5`
- README sync finds front-matter already current: `T7`
- Historical proposal references lowercase `vision.md`: `T1`, `T2`

## Acceptance criteria coverage map

| Acceptance criterion | Test IDs | Notes |
| --- | --- | --- |
| `AC1` | `T1`, `T2` | `VISION.md` is the canonical artifact. |
| `AC2` | `T3` | Authored `vision` skill validates and uses state-based behavior. |
| `AC3` | `T4`, `T5`, `T7` | Safe establishment, update, and README sync behavior remains. |
| `AC4` | `T5` | Substantive/editorial and causal-link gates remain present. |
| `AC5` | `T1`, `T7` | README front-matter links to `VISION.md` and stays marker-bounded. |
| `AC6` | `T8` | Proposal guidance requires `Vision fit` against `VISION.md`. |
| `AC7` | `T8` | Proposal-review checks fit and explicit exceptions. |
| `AC8` | `T1` | Normal lifecycle chain does not require `vision`. |
| `AC9` | `T3`, `T10` | Active old contract surfaces stop requiring lowercase path and user-facing mode names. |
| `AC10` | `T6`, `T7`, `T10` | Still-valid safety and quality rules remain present. |

## Test cases

### T1. Canonical path, governance, README ownership, and lifecycle boundary

- Covers: `R1`-`R8`, `R63`, `AC1`, `AC5`, `AC8`
- Level: contract/manual
- Fixture/setup:
  - `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, `README.md`
  - `skills/vision/SKILL.md`, `skills/proposal/SKILL.md`, `skills/proposal-review/SKILL.md`
- Steps:
  - Inspect active governance, workflow, README, proposal, proposal-review, and vision-skill guidance for `VISION.md` as the canonical project-vision path.
  - Inspect source-of-truth wording to confirm `CONSTITUTION.md` outranks `VISION.md` and README front-matter is generated from `VISION.md`.
  - Inspect README front-matter for a link to `VISION.md`.
  - Confirm root `vision.md` is not described as canonical in active guidance after migration.
  - Confirm the normal lifecycle chain still does not add `vision` as a required stage.
  - Confirm historical artifacts are not rewritten solely to replace old `vision.md` references.
- Expected result:
  - Active guidance uses `VISION.md`, preserves the source order, and keeps `vision` upstream of the lifecycle.
- Automation location:
  - Focused assertions in `scripts/test-skill-validator.py`
  - Manual diff review for historical-artifact non-rewrite scope

### T2. Root vision migration final state and rename safety

- Covers: `R1`, `R7`-`R8`, edge cases involving legacy lowercase input
- Level: migration/manual
- Fixture/setup:
  - Repository state before migration has root `vision.md` and no root `VISION.md`.
- Steps:
  - Use the plan's safe two-step Git rename strategy when needed: `git mv vision.md .vision.tmp`, then `git mv .vision.tmp VISION.md`.
  - Confirm final branch state has root `VISION.md`.
  - Confirm final branch state does not have root `vision.md`.
  - Inspect the diff to confirm project vision content is unchanged except path-sensitive links or generated front-matter.
- Expected result:
  - The branch ends with exactly one root project-vision file and no content rewrite beyond approved path-sensitive changes.
- Automation location:
  - `git diff --name-status -- vision.md VISION.md`
  - `git diff --check -- VISION.md vision.md`
  - Manual diff review

### T3. Vision skill state-based interface and output reporting

- Covers: `R9`-`R19`, `AC2`, `AC9`
- Level: contract
- Fixture/setup:
  - `skills/vision/SKILL.md`
- Steps:
  - Assert metadata still uses `name: vision`.
  - Assert the description covers project vision and README front-matter.
  - Assert the skill uses state-based behavior and ordinary user intent.
  - Assert legacy words such as `create`, `revise`, and `mirror` are not exposed as user-facing operating modes.
  - Assert every run reports changed files and README front-matter action.
  - Assert establishment reports assumptions and open questions, updates report changed sections and classification, and README-only sync reports `VISION.md` unchanged.
- Expected result:
  - The skill interface is state-based and preserves required reporting.
- Automation location:
  - Focused assertions in `scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py skills/vision/SKILL.md`

### T4. Initial establishment and pre-vision behavior

- Covers: `R20`-`R22`, no-vision proposal behavior
- Level: contract
- Fixture/setup:
  - `skills/vision/SKILL.md`
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
- Steps:
  - Assert the skill creates root `VISION.md` only when the user explicitly asks to establish project vision.
  - Assert ordinary README maintenance or skill installation does not create `VISION.md`.
  - Assert missing canonical vision without establishment intent stops and asks whether to create `VISION.md`.
  - Assert proposal/proposal-review no-vision behavior applies only when neither `VISION.md` nor migration-recognized legacy `vision.md` exists.
- Expected result:
  - Pre-vision repositories can bootstrap safely, while this repository migration does not use `no vision exists yet` just because uppercase migration is not complete.
- Automation location:
  - Focused assertions in `scripts/test-skill-validator.py`

### T5. Vision update, classification, overwrite, and causal-link gates

- Covers: `R23`-`R31`, `AC3`, `AC4`
- Level: contract
- Fixture/setup:
  - `skills/vision/SKILL.md`
  - `docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/change.yaml`
  - `docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/explain-change.md`
- Steps:
  - Assert update guidance limits edits to the requested section or clearly related sections.
  - Assert unavoidable cross-section effects must be explained before finalizing.
  - Assert unclear update intent stops before editing `VISION.md`.
  - Assert every update asks or confirms `substantive` versus `editorial`.
  - Assert substantive updates tied to a required change-local pack require causal links in `change.yaml` and `explain-change.md`.
  - Assert editorial updates and README-only sync changes do not create a pack solely because the skill ran.
  - Assert existing `VISION.md` is not silently overwritten and both-file states are not merged automatically.
- Expected result:
  - Meaning-changing vision updates are bounded, classified, and traceable.
- Automation location:
  - Focused assertions in `scripts/test-skill-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/change.yaml`

### T6. Security, privacy, research, readability, and bounded-read rules remain present

- Covers: `R32`-`R39`, `R68`-`R72`, `AC10`
- Level: contract
- Fixture/setup:
  - `skills/vision/SKILL.md`
  - `specs/vision-skill.md`
- Steps:
  - Assert the skill excludes secrets, credentials, private local filesystem paths, private machine names, and unintended personal data.
  - Assert external information is not fetched unless user-requested research or workflow-invoked research applies.
  - Assert researched facts are distinguished from project assumptions when research is used.
  - Assert `VISION.md` remains plain Markdown and does not require rendered tables, diagrams, HTML layout, or generated assets.
  - Assert bounded-read behavior remains present and full-file reads are reserved for source-of-truth or structure-dependent cases.
- Expected result:
  - Simplification and path migration do not weaken publication safety or evidence-collection discipline.
- Automation location:
  - Focused assertions in `scripts/test-skill-validator.py`

### T7. README front-matter remains marker-bounded

- Covers: `R40`-`R48`, `AC3`, `AC5`, `AC10`
- Level: contract/integration
- Fixture/setup:
  - `README.md`
  - `skills/vision/SKILL.md`
- Steps:
  - Assert the marker pair is exactly `<!-- vision:start -->` and `<!-- vision:end -->`.
  - Assert generated front-matter includes only pitch, differentiator, target audience, and a link to `VISION.md`.
  - Assert README front-matter is derived from `VISION.md`.
  - Assert automatic marker insertion is allowed only during initial `VISION.md` creation.
  - Assert existing valid marker blocks are replaced only inside the markers.
  - Assert missing, malformed, nested, or multiple markers stop update or sync unless explicitly authorized.
  - Assert no required README synchronization helper script is added.
  - Run README marker validation after README changes.
- Expected result:
  - README front-matter stays generated, bounded, and safe to synchronize.
- Automation location:
  - `python scripts/validate-readme.py README.md --vision-markers`
  - Focused assertions in `scripts/test-skill-validator.py`

### T8. Proposal and proposal-review Vision fit behavior

- Covers: `R49`-`R62`, `AC6`, `AC7`
- Level: contract
- Fixture/setup:
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
- Steps:
  - Assert proposal reads root `VISION.md` when present.
  - Assert every new or substantively revised proposal requires `Vision fit`.
  - Assert legacy untouched proposals are not invalid solely because they reference `vision.md` or lack `Vision fit`.
  - Assert the first non-empty line of `Vision fit` must be exactly one of `fits the current vision`, `may conflict with the current vision`, `proposes a vision revision`, or `no vision exists yet`.
  - Assert `no vision exists yet` is forbidden when `VISION.md` exists or during this repository migration while legacy `vision.md` is migration-recognized.
  - Assert proposal-review checks fit, classifies conflicts, and preserves explicit exception evidence.
- Expected result:
  - Proposal guidance uses the status-line contract and handles pre-vision and migration states distinctly.
- Automation location:
  - Focused assertions in `scripts/test-skill-validator.py`

### T9. Selector routing, PR routing, and both-path conflict behavior

- Covers: `R66`-`R67`
- Level: unit/integration
- Fixture/setup:
  - `scripts/validation_selection.py`
  - `scripts/test-select-validation.py`
- Steps:
  - Assert explicit-mode selection for root `VISION.md` classifies as a supported vision surface.
  - Assert explicit-mode and PR-mode selection for root `VISION.md` selects README vision marker validation or equivalent repository-owned proof.
  - Assert migration-time legacy root `vision.md` is classified so deletion, rename, or migration does not block as `unclassified-path`.
  - Assert both root files existing blocks or fails validation.
  - Assert reintroduced root `vision.md` after migration is classified as legacy or conflict instead of ignored.
- Expected result:
  - Validation can route the migration safely before and after the rename.
- Automation location:
  - `python scripts/test-select-validation.py`
  - `python scripts/select-validation.py --mode explicit --path VISION.md`
  - `python scripts/select-validation.py --mode explicit --path vision.md`

### T10. Retire old lowercase-path and user-facing mode requirements

- Covers: `AC9`, `AC10`
- Level: contract
- Fixture/setup:
  - `specs/vision-skill.md`
  - `specs/vision-skill.test.md`
  - `skills/vision/SKILL.md`
  - generated `.codex/skills/`
  - generated public adapters under `dist/adapters/`
- Steps:
  - Assert active vision contract surfaces no longer require root `vision.md` as the canonical project-vision artifact.
  - Assert active vision contract surfaces no longer require user-facing `create`, `revise`, or `mirror` operating modes.
  - Assert old words, if present, are framed only as legacy natural-language intent or historical context.
  - Assert still-valid rules remain: overwrite protection, deterministic marker handling, no silent marker insertion during update or sync, substantive/editorial confirmation, plain Markdown readability, sensitive-information exclusion, and bounded-read behavior.
  - Assert reintroduced lowercase root `vision.md` is treated as legacy or conflict, not canonical.
- Expected result:
  - The old model is retired without losing safety or quality.
- Automation location:
  - Focused assertions in `scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`

## Fixtures and data

- Existing root `vision.md` is the legacy migration input for this repository until M2 renames it to `VISION.md`.
- Existing `README.md` includes the live marker-bounded front-matter block and is the marker-validation fixture.
- Temporary Git repositories in `scripts/test-select-validation.py` cover PR-mode rename, deletion, and coexistence selector cases.
- `docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/change.yaml` and `explain-change.md` are the durable traceability fixtures.

## Mocking/stubbing policy

- Selector PR-mode tests may use temporary local Git repositories instead of the real repository history.
- README marker tests may use temporary README files for malformed, missing, multiple, and valid marker cases.
- Generated-output checks must use real repository generators rather than mocked generated files.
- Skill and proposal guidance tests inspect real authored Markdown, not snapshots of expected full files.
- No network, hosted CI, or adapter runtime execution is mocked or required.

## Migration or compatibility tests

- `T2` proves final repository state and rename safety.
- `T3` proves legacy words are compatibility intent, not operating modes.
- `T8` proves pre-vision behavior and migration-recognized legacy `vision.md` behavior are distinct.
- `T9` proves selector routing for uppercase, legacy lowercase, PR-mode changes, and both-file conflict.
- `T10` proves active old contract requirements are retired or rewritten while safety rules remain.

## Observability verification

- `T3` verifies required `vision` skill user-facing output fields by contract text.
- `T5` verifies substantive update causal-link reporting by contract text and change-local metadata.
- No runtime logs, metrics, traces, or audit events are introduced.

## Security/privacy verification

- `T6` verifies sensitive-information exclusion, research boundaries, fact-versus-assumption reporting, and plain Markdown readability.
- Manual diff review confirms the approved project vision content is not rewritten beyond path-sensitive or generated front-matter changes.
- No external research is required for this migration.

## Performance checks

- No runtime performance behavior is introduced.
- Evidence collection remains bounded through existing workflow and skill guidance.
- Do not add broad smoke unless selector output, test-spec review, review-resolution, release metadata, or another authoritative artifact requires it.

## Manual QA checklist

- Confirm the final branch has root `VISION.md` and no root `vision.md`.
- Confirm project vision content is unchanged except path-sensitive references or generated front-matter.
- Confirm README front-matter links to `VISION.md` and content outside markers is preserved.
- Confirm active guidance names `VISION.md` without rewriting historical artifacts solely for path text.
- Confirm `vision` skill behavior is state-based and does not report a selected operating mode.
- Confirm `proposal` and `proposal-review` use `proposes a vision revision`.
- Confirm generated `.codex/skills/` and `dist/adapters/` diffs are generated only during the generated-output milestone.

## What not to test

- Do not run an external agent workflow for old invocation words; this change tests repository skill guidance and validation surfaces.
- Do not rewrite or quality-score the approved project vision prose.
- Do not add or test a README synchronization helper script.
- Do not rewrite old proposals, specs, plans, reviews, change-local artifacts, or PR records solely to update historical `vision.md` text.
- Do not test external Codex, Claude Code, or opencode execution.
- Do not add runtime performance, UI, network, storage, or deployment tests.
- Do not extract shared evidence-collection guidance across skills.

## Uncovered gaps

None. Requirements are covered by focused skill assertions, selector tests, README marker validation, generated-output drift checks, adapter validation, lifecycle validation, change metadata validation, manual migration diff review, or final selected CI proof.

## Next artifacts

- `code-review` for completed M1-M3 implementation
- `verify`
- `explain-change`
- `pr`

## Follow-on artifacts

- `plan-review`: approved on 2026-05-01 with updates to test-spec timing and milestone test-first closeout.

## Readiness

This test spec is the active proof map for the consolidated `vision` skill contract and `VISION.md` migration.

Immediate next repository stage: `code-review` for the completed M1-M3 implementation from [2026-05-01 Vision Skill Simplification and VISION.md Migration](../docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md).
