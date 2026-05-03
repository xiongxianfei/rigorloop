# Vision Skill Simplification and VISION.md Migration Test Spec

## Status

- active

## Related spec and plan

- Spec: [Vision Skill Simplification and VISION.md Migration](vision-skill-simplification-and-vision-md-migration.md), approved after spec-review on 2026-05-01.
- Proposal: [Vision Skill Simplification and VISION.md Migration](../docs/proposals/2026-05-01-vision-skill-simplification-and-vision-md-migration.md), accepted on 2026-05-01.
- Plan: [2026-05-01 Vision Skill Simplification and VISION.md Migration](../docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md), approved by plan-review on 2026-05-01.
- Architecture: not required. The approved change is a workflow-governance, source-of-truth, selector, skill, README, spec, and generated-output migration without a runtime boundary, service boundary, data store, dependency, network integration, deployment boundary, or architecture package change.
- Spec-review findings: approved on 2026-05-01 after the no-vision and migration-recognized legacy `vision.md` behavior was clarified.
- Plan-review findings: approved on 2026-05-01 after test-spec creation moved to the immediate `test-spec` stage and implementation milestones were made test-first and green by closeout.

## Testing strategy

- Contract tests inspect authored Markdown for `VISION.md` source-of-truth wording, state-based `vision` skill behavior, proposal `Vision fit` status-line rules, and retirement of the old lowercase-path and user-facing mode model.
- Selector unit and fixture tests prove `VISION.md`, migration-time legacy `vision.md`, README marker validation, PR-mode routing, and both-file conflict behavior.
- Migration proof combines Git rename inspection, root-file existence checks, selector behavior, and manual diff review to prove the final branch has exactly one canonical vision artifact and does not rewrite historical artifacts.
- Generated-output integration uses the existing skill and adapter generators so `.codex/skills/` and `dist/adapters/` remain derived from canonical `skills/`.
- Lifecycle and metadata proof keeps the approved spec, active test spec, active plan, proposal follow-ons, and change-local metadata coherent.
- Manual review is limited to scope, prose-safety, and project-vision content preservation checks that are not useful as automated validators.

## Requirement coverage map

| Requirement IDs | Test IDs | Notes |
| --- | --- | --- |
| `R1`-`R8` | `T1`, `T2`, `T12` | Canonical path, source order, README source boundary, and historical-reference scope. |
| `R9`-`R15` | `T2`, `T9`, `T12` | Migration final state, coexistence invalidity, owner-decision boundary, rename safety, rollback. |
| `R16`-`R27` | `T3`, `T13` | `vision` skill name, state-based interface, legacy mode-word handling, and output reporting. |
| `R28`-`R31` | `T4`, `T13` | Initial establishment and no-vision behavior while preserving quality, privacy, research, and readability rules. |
| `R32`-`R40` | `T5`, `T12` | Bounded updates, substantive/editorial gate, causal links, overwrite protection, and both-file merge protection. |
| `R41`-`R49` | `T6` | README marker pair, generated front-matter contents, marker insertion limits, and no helper script. |
| `R50`-`R57` | `T7` | Proposal `Vision fit`, status values, no-vision wording, and no silent vision redefinition. |
| `R58`-`R62` | `T8` | Proposal-review checks, conflict classification, and explicit exception recording. |
| `R63`-`R65` | `T1`, `T11` | Governance, workflow, README, proposal, proposal-review, and vision-skill path/source updates. |
| `R66`-`R69` | `T9` | Selector classification, README marker selection, and both-path validation failure. |
| `R70`-`R71` | `T3`, `T9` | Focused skill-validator and selector coverage for simplified behavior and `VISION.md` routing. |
| `R72`-`R74` | `T10` | Generated `.codex/skills/` and adapter output refreshed only through generators and checked for drift. |
| `R75` | `T1` | Normal lifecycle chain does not add `vision` as a required stage. |
| `R76`-`R80` | `T11`, `T13` | Active spec, test spec, skill, generated output, safety, quality, and bounded-read rule preservation. |
| `R81`-`R83` | `T4`, `T7`, `T9`, `T11` | Pre-vision state, no-vision proposal behavior, and reintroduced legacy `vision.md` classification. |

## Example coverage map

| Example | Test IDs | Notes |
| --- | --- | --- |
| `E1` | `T2`, `T12` | Legacy lowercase input migrates to one uppercase canonical file. |
| `E2` | `T2`, `T9` | Both files existing is invalid and requires owner decision. |
| `E3` | `T4` | Establishing project vision creates `VISION.md` and deterministic README markers. |
| `E4` | `T4` | Missing vision without establishment intent stops before editing README. |
| `E5` | `T5`, `T6` | Existing vision update is classified and README sync stays marker-bounded. |
| `E6` | `T5`, `T12` | Substantive update stops when required causal link is missing. |
| `E7` | `T6` | README sync leaves `VISION.md` unchanged. |
| `E8` | `T6` | Malformed README markers stop update or sync unless explicitly authorized. |
| `E9` | `T3` | Legacy `mirror` wording is interpreted as intent without reporting a mode. |
| `E10` | `T7` | Proposals use uppercase vision reference and do not use no-vision wording when a vision exists. |
| `E11` | `T7` | No canonical or migration-recognized legacy vision requires `no vision exists yet`. |

## Edge case coverage

| Edge case | Test IDs | Notes |
| --- | --- | --- |
| 1 | `T2` | Legacy lowercase-only state migrates to uppercase-only final state. |
| 2 | `T2`, `T9` | Both vision paths existing blocks validation and skill behavior. |
| 3 | `T4`, `T6` | Initial establishment may replace existing marker content after creating `VISION.md`. |
| 4 | `T6` | Existing `VISION.md` with README missing markers stops update or sync without authorization. |
| 5 | `T6` | Multiple start markers fail README marker validation and skill guidance stops. |
| 6 | `T7` | Proposal with no real vision must use `no vision exists yet`. |
| 7 | `T7` | Proposal missing `Vision fit` after approval is rejected by proposal-review. |
| 8 | `T5` | Scope-changing update labeled editorial is treated as substantive or clarified. |
| 9 | `T5` | Unclear update section stops before editing. |
| 10 | `T6` | README sync that already matches reports no content changes. |
| 11 | `T10` | Adapter drift catches missing generated `vision` skill updates. |
| 12 | `T1`, `T12` | Historical `vision.md` references are not rewritten solely for path text. |
| 13 | `T3` | `vision mirror` is legacy intent, not an operating mode. |
| 14 | `T2` | Case-only rename uses two-step Git rename when needed. |
| 15 | `T2`, `T9` | This repository cannot end with neither root vision file. |
| 16 | `T4`, `T7` | Pre-vision repositories may have neither path and must use no-vision proposal behavior. |
| 17 | `T9`, `T11` | Reintroduced root `vision.md` after migration is classified as legacy or conflict. |

## Acceptance criteria coverage map

| Acceptance criterion | Test IDs | Notes |
| --- | --- | --- |
| `AC1` | `T1`, `T2` | `VISION.md` is the only canonical artifact. |
| `AC2` | `T2` | Root `vision.md` is absent in final migrated state. |
| `AC3` | `T1`, `T11` | Active guidance names `VISION.md`. |
| `AC4` | `T1`, `T6` | README front-matter links to `VISION.md` and stays marker-bounded. |
| `AC5` | `T3`, `T11` | `vision` skill validates and no longer exposes user-facing modes. |
| `AC6` | `T3`, `T4`, `T5`, `T6` | State-based establishment, update, and README sync stay safe. |
| `AC7` | `T5` | Substantive/editorial and causal-link gates remain present. |
| `AC8` | `T7` | Proposal guidance requires `Vision fit` against `VISION.md`. |
| `AC9` | `T8` | Proposal-review checks fit and explicit exceptions. |
| `AC10` | `T9` | Root `VISION.md` selector classification exists. |
| `AC11` | `T9` | Both root vision files block or fail validation. |
| `AC12` | `T9` | Explicit and PR-mode routing for root `VISION.md` is covered. |
| `AC13` | `T10` | `.codex/skills/` is generated through `build-skills.py`. |
| `AC14` | `T10` | `dist/adapters/` is generated through `build-adapters.py`. |
| `AC15` | `T1`, `T12` | Historical artifacts are not rewritten solely for lowercase references. |
| `AC16` | `T1` | Normal lifecycle chain does not require `vision`. |
| `AC17` | `T11` | Active old contract surfaces stop requiring lowercase path and user-facing modes. |
| `AC18` | `T11`, `T13` | Still-valid safety and quality rules remain present. |
| `AC19` | `T9` | Both root `VISION.md` and legacy `vision.md` route during migration. |
| `AC20` | `T9`, `T11` | Reintroduced lowercase path is classified as legacy or conflict. |
| `AC21` | `T7` | Proposal status line accepts exactly one allowed value. |

## Test cases

### T1. Canonical path, governance, README ownership, and lifecycle boundary

- Covers: `R1`-`R8`, `R63`-`R65`, `R75`, `AC1`, `AC3`, `AC4`, `AC15`, `AC16`
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
- Failure proves:
  - The migration left active source-of-truth drift or broadened lifecycle scope.
- Automation location:
  - Focused assertions in `scripts/test-skill-validator.py`
  - Manual diff review for historical-artifact non-rewrite scope

### T2. Root vision migration final state and rename safety

- Covers: `R9`-`R15`, `E1`, `E2`, edge cases 1, 2, 14, 15, `AC1`, `AC2`
- Level: migration/manual
- Fixture/setup:
  - Repository state before migration has root `vision.md` and no root `VISION.md`.
- Steps:
  - Use the plan's safe two-step Git rename strategy when needed: `git mv vision.md .vision.tmp`, then `git mv .vision.tmp VISION.md`.
  - Confirm final branch state has root `VISION.md`.
  - Confirm final branch state does not have root `vision.md`.
  - Inspect the diff to confirm project vision content is unchanged except path-sensitive links or generated front-matter.
  - Confirm rollback guidance restores exactly one canonical path.
- Expected result:
  - The branch ends with exactly one root project-vision file and no content rewrite beyond approved path-sensitive changes.
- Failure proves:
  - The migration left competing, missing, or content-drifted vision artifacts.
- Automation location:
  - `git diff --name-status -- vision.md VISION.md`
  - `git diff --check -- VISION.md vision.md`
  - Manual diff review

### T3. Vision skill state-based interface and output reporting

- Covers: `R16`-`R27`, `R70`, `E9`, edge case 13, `AC5`, `AC6`
- Level: contract
- Fixture/setup:
  - `skills/vision/SKILL.md`
- Steps:
  - Assert metadata still uses `name: vision`.
  - Assert the description covers project vision and README front-matter without requiring `create`, `revise`, or `mirror` as user-facing modes.
  - Assert the skill does not present a required `create`/`revise`/`mirror` mode table.
  - Assert the skill does not require `Mode used` in output.
  - Assert legacy mode words may be interpreted only as natural-language intent.
  - Assert every run reports changed files and README front-matter action.
  - Assert establishment reports assumptions and open questions, updates report changed sections and classification, and README-only sync reports `VISION.md` unchanged.
- Expected result:
  - The skill interface is state-based and preserves required reporting.
- Failure proves:
  - The skill still exposes old modes as the interface or lost required observability.
- Automation location:
  - Focused assertions in `scripts/test-skill-validator.py`

### T4. Initial establishment and pre-vision behavior

- Covers: `R28`-`R31`, `R81`-`R82`, `E3`, `E4`, edge cases 3, 16, `AC6`, `AC18`
- Level: contract
- Fixture/setup:
  - `skills/vision/SKILL.md`
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
- Steps:
  - Assert the skill creates root `VISION.md` only when the user explicitly asks to establish project vision.
  - Assert ordinary README maintenance or skill installation does not create `VISION.md`.
  - Assert missing canonical vision without establishment intent stops and asks whether to create `VISION.md`.
  - Assert initial vision content keeps the still-valid 500-word cap, required section order, plain-language, no requirements-vocabulary, no implementation-detail, drafting, privacy, research, and Markdown readability rules.
  - Assert proposal/proposal-review no-vision behavior applies only when neither `VISION.md` nor migration-recognized legacy `vision.md` exists.
- Expected result:
  - Pre-vision repositories can bootstrap safely, while this repository migration does not use `no vision exists yet` just because uppercase migration is not complete.
- Failure proves:
  - The skill creates vision artifacts too eagerly or proposal behavior misreads the migration state.
- Automation location:
  - Focused assertions in `scripts/test-skill-validator.py`

### T5. Vision update, classification, overwrite, and causal-link gates

- Covers: `R32`-`R40`, `R80`, `E5`, `E6`, edge cases 8, 9, `AC6`, `AC7`, `AC18`
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
  - Assert scope, users, commitments, refusals, proposal-fit framing, or falsifiability changes are substantive unless owner rationale says otherwise.
  - Assert substantive updates tied to a required change-local pack require causal links in `change.yaml` and `explain-change.md`.
  - Assert editorial updates and README-sync-only changes do not create a pack solely because the skill ran.
  - Assert existing `VISION.md` is not silently overwritten and both-file states are not merged automatically.
- Expected result:
  - Meaning-changing vision updates are bounded, classified, and traceable.
- Failure proves:
  - The simplified skill removed safety gates that the old modes protected.
- Automation location:
  - Focused assertions in `scripts/test-skill-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/change.yaml`

### T6. README front-matter remains marker-bounded

- Covers: `R41`-`R49`, `E7`, `E8`, edge cases 4, 5, 10, `AC4`, `AC6`
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
- Failure proves:
  - The migration introduced broad README edit authority or unsafe marker handling.
- Automation location:
  - `python scripts/validate-readme.py README.md --vision-markers`
  - Focused assertions in `scripts/test-skill-validator.py`

### T7. Proposal Vision fit status line and no-vision rules

- Covers: `R50`-`R57`, `R81`-`R82`, `E10`, `E11`, edge cases 6, 7, 16, `AC8`, `AC21`
- Level: contract
- Fixture/setup:
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
- Steps:
  - Assert proposal reads root `VISION.md` when present.
  - Assert every new or substantively revised proposal requires `Vision fit`.
  - Assert legacy untouched proposals are not invalid solely because they reference `vision.md` or lack `Vision fit`.
  - Assert the first non-empty line of `Vision fit` must be exactly one of:
    - `fits the current vision`
    - `may conflict with the current vision`
    - `proposes a vision revision`
    - `no vision exists yet`
  - Assert `no vision exists yet` is forbidden when `VISION.md` exists or during this repository migration while legacy `vision.md` is migration-recognized.
  - Assert a proposal must not silently redefine project vision outside `Vision fit` and normal rationale.
- Expected result:
  - Proposal guidance uses the new status-line contract and handles pre-vision and migration states distinctly.
- Failure proves:
  - Proposal guidance still uses the old status value, silently bypasses vision fit, or mishandles legacy migration state.
- Automation location:
  - Focused assertions in `scripts/test-skill-validator.py`

### T8. Proposal-review conflict and exception behavior

- Covers: `R58`-`R62`, `AC9`
- Level: contract
- Fixture/setup:
  - `skills/proposal-review/SKILL.md`
- Steps:
  - Assert proposal-review checks `Vision fit` against root `VISION.md` when it exists.
  - Assert missing `Vision fit` in applicable proposals requests revision.
  - Assert a conflict with `VISION.md` is classified as revise proposal, revise vision, or record explicit exception.
  - Assert explicit exceptions include owner or owning stage, conflict evidence, why proposal revision is not chosen, why vision revision is not chosen, recording location, and one-time versus future-trigger classification.
  - Assert explicit exceptions are recorded in both proposal `Vision fit` and proposal-review output.
- Expected result:
  - Proposal-review preserves meaningful vision governance after the path migration.
- Failure proves:
  - Vision conflicts can be waved through without durable rationale.
- Automation location:
  - Focused assertions in `scripts/test-skill-validator.py`

### T9. Selector routing, PR routing, and both-path conflict behavior

- Covers: `R66`-`R69`, `R71`, `R83`, `E2`, edge cases 2, 15, 17, `AC10`-`AC12`, `AC19`, `AC20`
- Level: unit/integration
- Fixture/setup:
  - `scripts/validation_selection.py`
  - `scripts/test-select-validation.py`
  - temporary Git repositories used by selector tests
- Steps:
  - Assert explicit-mode selection for root `VISION.md` classifies as a supported vision surface.
  - Assert explicit-mode and PR-mode selection for root `VISION.md` selects README vision marker validation or equivalent repository-owned proof.
  - Assert migration-time legacy root `vision.md` is classified so deletion, rename, or migration does not block as `unclassified-path`.
  - Assert both root files existing blocks or fails validation.
  - Assert reintroduced root `vision.md` after migration is classified as legacy or conflict instead of ignored.
  - Assert selector-selected CI runs the expected checks for changed selector and selector-test paths.
- Expected result:
  - Validation can route the migration safely before and after the rename.
- Failure proves:
  - The migration cannot be validated reliably or could silently accept an invalid legacy conflict.
- Automation location:
  - `python scripts/test-select-validation.py`
  - `python scripts/select-validation.py --mode explicit --path VISION.md`
  - `python scripts/select-validation.py --mode explicit --path vision.md`
  - `bash scripts/ci.sh --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py`

### T10. Generated skill and adapter output stays derived

- Covers: `R72`-`R74`, `R77`, edge case 11, `AC13`, `AC14`
- Level: integration
- Fixture/setup:
  - canonical `skills/`
  - generated `.codex/skills/`
  - generated `dist/adapters/`
- Steps:
  - Run `python scripts/build-skills.py` after canonical skill changes.
  - Run `python scripts/build-adapters.py --version 0.1.1` after canonical skill changes.
  - Inspect generated diffs for expected `VISION.md` and state-based guidance propagation.
  - Run generator drift checks and adapter validation.
  - Confirm generated output is not hand-edited.
- Expected result:
  - Generated skill and adapter output matches canonical skill sources.
- Failure proves:
  - Adapter or Codex runtime mirrors are stale, missing the migration, or hand-edited.
- Automation location:
  - `python scripts/build-skills.py --check`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`

### T11. Retire old lowercase-path and user-facing mode requirements

- Covers: `R7`, `R18`-`R19`, `R76`-`R80`, `R83`, `AC17`, `AC18`, `AC20`
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
  - Assert old mode words, if present, are framed only as legacy natural-language intent or historical context.
  - Assert still-valid rules remain: overwrite protection, deterministic marker handling, no silent marker insertion during update or sync, substantive/editorial confirmation, plain Markdown readability, sensitive-information exclusion, and bounded-read behavior.
  - Assert reintroduced lowercase root `vision.md` is treated as legacy or conflict, not canonical.
- Expected result:
  - The old model is retired without losing safety or quality.
- Failure proves:
  - Active approved surfaces conflict with the new spec or safety rules were dropped during simplification.
- Automation location:
  - Focused assertions in `scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - generated-output checks from `T10`

### T12. Lifecycle and migration traceability stay coherent

- Covers: `R8`, `R13`, `R15`, `R37`, `AC15`, `E1`, `E6`, edge case 12
- Level: contract/manual
- Fixture/setup:
  - `docs/plan.md`
  - active execution plan
  - accepted proposal
  - approved spec
  - this test spec
  - `docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/change.yaml`
  - `docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/explain-change.md`
- Steps:
  - Validate lifecycle artifacts explicitly after creating this test spec and after implementation closeout.
  - Validate change metadata after the change-local pack exists.
  - Confirm causal links for substantive vision-skill and vision-path contract changes are recorded.
  - Confirm the plan, plan index, proposal, spec, and test spec follow-on/readiness surfaces are not stale.
  - Confirm historical artifacts are not mass-rewritten solely for old lowercase references.
- Expected result:
  - The migration has durable traceability and no stale lifecycle state.
- Failure proves:
  - Reviewers cannot connect implementation evidence back to the approved contract.
- Automation location:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md --path docs/proposals/2026-05-01-vision-skill-simplification-and-vision-md-migration.md --path specs/vision-skill-simplification-and-vision-md-migration.md --path specs/vision-skill-simplification-and-vision-md-migration.test.md --path specs/vision-skill.md --path specs/vision-skill.test.md --path docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/change.yaml`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/change.yaml`

### T13. Security, privacy, research, readability, and bounded-read rules remain present

- Covers: `R31`, `R80`, `AC18`
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
- Failure proves:
  - The old mode/path rewrite accidentally removed still-valid quality and safety rules.
- Automation location:
  - Focused assertions in `scripts/test-skill-validator.py`

## Fixtures and data

- Existing root `vision.md` is the legacy migration input for this repository until M2 renames it to `VISION.md`.
- Existing `README.md` includes the live marker-bounded front-matter block and is the marker-validation fixture.
- Temporary Git repositories in `scripts/test-select-validation.py` should be used for PR-mode rename, deletion, and coexistence selector cases.
- `docs/changes/2026-05-01-vision-skill-simplification-and-vision-md-migration/change.yaml` and `explain-change.md` are created during M1 and become the durable traceability fixtures.
- No external services, generated assets, network calls, or user-specific local paths are fixtures for this change.

## Mocking/stubbing policy

- Selector PR-mode tests may use temporary local Git repositories instead of the real repository history.
- README marker tests may use temporary README files for malformed, missing, multiple, and valid marker cases.
- Generated-output checks must use real repository generators rather than mocked generated files.
- Skill and proposal guidance tests inspect real authored Markdown, not snapshots of expected full files.
- No network, hosted CI, or adapter runtime execution is mocked or required.

## Migration or compatibility tests

- `T2` proves final repository state and rename safety.
- `T3` proves legacy mode words are compatibility intent, not operating modes.
- `T7` proves pre-vision behavior and migration-recognized legacy `vision.md` behavior are distinct.
- `T9` proves selector routing for uppercase, legacy lowercase, PR-mode changes, and both-file conflict.
- `T11` proves active old contract requirements are retired or rewritten while safety rules remain.

## Observability verification

- `T3` verifies required `vision` skill user-facing output fields by contract text.
- `T5` verifies substantive update causal-link reporting by contract text and change-local metadata.
- `T10` and `T12` verify repository-owned command output and lifecycle evidence are recorded in validation notes.
- No runtime logs, metrics, traces, or audit events are introduced.

## Security/privacy verification

- `T13` verifies sensitive-information exclusion, research boundaries, fact-versus-assumption reporting, and plain Markdown readability.
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
- Confirm `vision` skill behavior is state-based and no longer reports `Mode used`.
- Confirm `proposal` and `proposal-review` use `proposes a vision revision`, not the old `intentionally proposes a vision revision` value.
- Confirm generated `.codex/skills/` and `dist/adapters/` diffs are generated and expected.
- Confirm the active plan and `docs/plan.md` are synchronized before PR readiness is claimed.

## What not to test

- Do not run an external agent workflow for actual `vision create`, `vision revise`, or `vision mirror`; this change tests repository skill guidance and validation surfaces.
- Do not rewrite or quality-score the approved project vision prose.
- Do not add or test a README synchronization helper script.
- Do not rewrite old proposals, specs, plans, reviews, change-local artifacts, or PR records solely to update historical `vision.md` text.
- Do not test external Codex, Claude Code, or opencode execution.
- Do not add runtime performance, UI, network, storage, or deployment tests.
- Do not extract shared evidence-collection guidance across skills.

## Uncovered gaps

None. Requirements are covered by focused skill assertions, selector tests, README marker validation, generated-output drift checks, adapter validation, lifecycle validation, change metadata validation, manual migration diff review, or final selected CI proof.

## Next artifacts

- `implement` M1: completed selector and validation support for root `VISION.md`, legacy root `vision.md`, README marker selection, and both-file conflict behavior.
- `implement` M2: authored `VISION.md` migration, governance/docs/spec/skill updates, and focused skill-validator updates.
- `implement` M3: generated skill and adapter output refresh plus lifecycle closeout.
- `code-review`
- `verify`
- `explain-change`
- `pr`

## Follow-on artifacts

None yet.

## Readiness

This test spec is the active proof map for the `VISION.md` migration and vision skill simplification.

Immediate next repository stage: `implement` M2 from [2026-05-01 Vision Skill Simplification and VISION.md Migration](../docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md).
