# Project Artifact Location Guide and Examples Surface Test Spec

## Status

active

## Stage-owned lifecycle proof alignment

Compatibility projection: `CP-030`.

For a change governed by `stage-owned-change-local-v1`, proof expectations for
the replaced subject named by this test spec's matching feature specification
are superseded by
`specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.test.md`,
especially T14.
Existing rows remain historical evidence or proof of the retained behavior
named by that feature specification's reciprocal notice.
They must not authorize the retired writer for governed current work.
This alignment requires `test-spec-review` before M1 relies on it.

## Related spec and plan

- Spec: [Project Artifact Location Guide and Examples Surface](project-artifact-location-guide-and-examples-surface.md), approved.
- Plan: [Project Artifact Location Guide and Examples Surface Plan](../docs/plans/2026-05-13-project-artifact-location-guide-and-examples-surface.md), active.
- Proposal: [Project Artifact Location Guide and Examples Surface](../docs/proposals/2026-05-13-project-artifact-location-guide-and-examples-surface.md), accepted.
- Spec review: [spec-review-r1](../docs/changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording/reviews/spec-review-r1.md), [spec-review-r2](../docs/changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording/reviews/spec-review-r2.md).
- Plan review: [plan-review-r1](../docs/changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording/reviews/plan-review-r1.md), [plan-review-r2](../docs/changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording/reviews/plan-review-r2.md).
- Architecture: not required. The approved plan records no runtime architecture package because this change is workflow guidance, skill text, examples routing, validation, and generated output.

## Testing strategy

This change is verified through repository-owned static and validator checks rather than runtime end-to-end tests.

- Contract and documentation checks prove `docs/workflows.md` has a concise artifact-location map with source-rank and schema-disclaimer wording.
- Skill static checks prove public skills use token-efficient lookup wording, do not duplicate long artifact tables, and do not expose repository-internal validator paths.
- Selector, lifecycle, review-artifact, and change-metadata tests prove deleted-path compatibility is bounded and retained fixtures are explicit.
- Generated-output checks prove canonical skill edits are reflected in generated local skill output and public adapter output.
- Manual review covers judgement-heavy source-rank, no-broad-search, custom-path, and public wording constraints that should not become brittle snapshot-only tests.

Broad smoke is not required by this test spec. Use milestone-specific validation first, then selected explicit-path CI when implementation paths are known.

## Requirement coverage map

| Requirement | Coverage |
|---|---|
| `R1`-`R1d` | `T1`, `T2`, `T14` |
| `R2`-`R2g` | `T2`, `T4`, `T11` |
| `R3`-`R3b` | `T3`, `T11` |
| `R4`-`R4c` | `T1`, `T14` |
| `R5`-`R5aa` | `T2`, `T4` |
| `R5b`-`R5g` | `T2`, `T4`, `T9` |
| `R6`-`R6e` | `T5`, `T6`, `T7`, `T12` |
| `R7`-`R7d` | `T8`, `T12` |
| `R8`-`R8a` | `T8`, `T12` |
| `R9`-`R9b` | `T2`, `T4` |
| `R10`-`R10b` | `T4`, `T9` |
| `R11`-`R11d` | `T5`, `T6`, `T7`, `T8`, `T10` |
| `R12`-`R12b` | `T11`, `T14` |
| Security/privacy `MUST` | `T12` |

## Example coverage map

| Example | Coverage |
|---|---|
| `E1` | `T1` |
| `E2` | `T1`, `T7` |
| `E3` | `T2`, `T4` |
| `E4` | `T2`, `T11` |
| `E5` | `T5`, `T6` |
| `E6` | `T7` |
| `E7` | `T8` |
| `E8` | `T3`, `T11` |
| `E9` | `T2`, `T4` |

## Edge case coverage

| Edge case | Coverage |
|---|---|
| `EC1` | `T1`, `T3` |
| `EC2` | `T2`, `T4` |
| `EC3` | `T2`, `T11` |
| `EC4` | `T5`, `T6` |
| `EC5` | `T7` |
| `EC6` | `T8` |
| `EC7` | `T8` |
| `EC8` | `T2`, `T4` |
| `EC9` | `T1`, `T11` |
| `EC10` | `T9` |

## Milestone coverage map

| Milestone | Coverage |
|---|---|
| `M1. Workflow Artifact Map And Retained Fixture Rationale` | `T1`, `T2`, `T3`, `T8`, `T11`, `T12`, `T14` |
| `M2. Stage Skill Lookup Wording And Static Proof` | `T2`, `T4`, `T9`, `T11`, `T14` |
| `M3. Examples Routing And Lifecycle Validation` | `T5`, `T6`, `T7`, `T8`, `T10`, `T12`, `T14` |
| `M4. Generated Output Refresh And Final Milestone Review` | `T9`, `T10`, `T14` |

## Test cases

### T1. Workflow guide contains artifact-location map without becoming a schema

- Covers: `R1`-`R1c`, `R4`-`R4c`, `E1`, `E2`, `EC1`, `EC9`
- Level: contract, manual
- Fixture/setup: `docs/workflows.md`, `specs/project-artifact-location-guide-and-examples-surface.md`
- Steps:
  - Assert `docs/workflows.md` contains a clear `Artifact locations` section.
  - Assert the table names the required artifact types from `R4`.
  - Assert the table defines default locations and owning skills.
  - Assert the table says exact shapes, required fields, lifecycle statuses, and validation rules live in governing specs, schemas, or references.
  - Assert the formal review records row points to the formal review recording contract for exact receipt/root rules.
  - Assert review-resolution and verify-report rows are conditional.
- Expected result: users can find default artifact locations without mistaking the table for a full schema.
- Failure proves: `docs/workflows.md` cannot answer the path question or competes with governing specs.
- Automation location: `scripts/test-skill-validator.py` or a focused workflow-doc assertion, plus manual review.

### T2. Source rank and discovery order remain distinct

- Covers: `R1d`, `R2`-`R2g`, `R5`, `R5a`, `R5aa`, `R5e`-`R5g`, `R9`-`R9b`, `E3`, `E4`, `E9`, `EC2`, `EC3`, `EC8`
- Level: contract, manual
- Fixture/setup: `docs/workflows.md`, affected public skills, `scripts/test-skill-validator.py`
- Steps:
  - Assert workflow guidance states that source rank is precedence when sources conflict, not mandatory read order.
  - Assert shared skill lookup wording includes explicit user path or change ID, active metadata, known governing spec or schema constraints, `docs/workflows.md`, portable default, and block-on-ambiguity.
  - Assert public skills discourage broad authoritative-document searches solely to discover paths.
  - Assert public skills still obey known governing specs, schemas, active metadata, explicit paths, and safety constraints.
  - Assert customized project paths in `docs/workflows.md` outrank portable defaults without requiring copied custom tables in each skill.
- Expected result: skills can find paths cheaply while still respecting higher-priority constraints.
- Failure proves: SR-001 regressed or public skills waste tokens broad-searching docs for simple path discovery.
- Automation location: `scripts/test-skill-validator.py`, manual review of touched public skill text.

### T3. Workflow skill creates or refreshes the guide only on defined triggers

- Covers: `R3`-`R3b`, `E8`, `EC1`
- Level: contract, manual
- Fixture/setup: `skills/workflow/SKILL.md`, `docs/workflows.md`
- Steps:
  - Assert `workflow` says it creates or refreshes `docs/workflows.md` when the project adopts RigorLoop and the guide is missing.
  - Assert `workflow` names artifact-location, review-recording, examples, reports, change-root, generated-output, and stale-guide trigger cases.
  - Assert ordinary task routing references the guide instead of rewriting it when current.
  - Assert `workflow` does not claim ownership of writing proposals, specs, plans, reviews, ADRs, or exact schemas.
- Expected result: `workflow` owns guide freshness without becoming a general artifact author.
- Failure proves: guide refreshes can be skipped or workflow can absorb stage-skill responsibilities.
- Automation location: `scripts/test-skill-validator.py`, manual review.

### T4. Public stage skills use concise portable artifact lookup wording

- Covers: `R2d`-`R2g`, `R5b`-`R5g`, `R9`, `R10b`, `E3`, `E9`, `EC2`, `EC8`
- Level: contract, integration
- Fixture/setup: `skills/proposal`, `skills/spec`, `skills/architecture`, `skills/plan`, `skills/test-spec`, review skills, `skills/explain-change`, `skills/verify`, `skills/pr`
- Steps:
  - Add or update static checks for affected public skills that create, review, verify, or hand off artifacts.
  - Assert each affected skill refers to the project workflow guide or artifact-location map when placement matters.
  - Assert each affected skill keeps only its own short portable default path where needed.
  - Assert no affected skill copies the full artifact-location table, long review-root algorithm, or long example path list.
  - Assert public skill text does not hardcode RigorLoop repository-internal validator or fixture paths when project-portable wording is enough.
- Expected result: public skills remain concise, portable, and aligned with the artifact-location map.
- Failure proves: path rules can drift across skills or public skill text can leak maintainer-only repository details.
- Automation location: `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`

### T5. Retired example paths have bounded deletion compatibility

- Covers: `R6`-`R6c`, `R11a`, `E5`, `EC4`
- Level: unit
- Fixture/setup: `scripts/validation_selection.py`, `scripts/test-select-validation.py`
- Steps:
  - Run one selector test for a deleted path under the retired examples prefix.
  - Assert the path uses the bounded retired-example compatibility category.
  - Assert no lifecycle validator is selected solely for the deleted path.
- Expected result: deletion diffs remain selectable without preserving an examples feature.
- Failure proves: removing the directory makes the cleanup diff unclassifiable.
- Automation location: `python scripts/test-select-validation.py`

### T6. Lifecycle fixtures remain isolated

- Covers: `R6c`, `R6d`, `R11b`, `E5`, `EC4`
- Level: unit, integration
- Fixture/setup: temporary repositories created by lifecycle validator tests
- Steps:
  - Create plan-shaped negative fixtures only inside temporary repositories.
  - Assert validation results are scoped to the temporary root.
- Expected result: fixture state cannot become active project lifecycle state.
- Failure proves: test setup can leak synthetic lifecycle state into the repository.
- Automation location: `python scripts/test-artifact-lifecycle-validator.py`

### T7. Formal review fixtures remain test-owned

- Covers: `R6e`, `R11c`, `E2`, `E6`, `EC5`
- Level: unit, integration
- Fixture/setup: temporary review-artifact repositories and `scripts/test-review-artifact-validator.py`
- Steps:
  - Create review-shaped negative cases only inside temporary repositories or test-fixture paths.
  - Assert those cases cannot contribute state to the real repository.
- Expected result: executable review cases remain test-owned.
- Failure proves: fixture isolation is incomplete.
- Automation location: `python scripts/test-review-artifact-validator.py`, `python scripts/test-artifact-lifecycle-validator.py`

### T8. Skill-validator fixtures are test-owned

- Covers: `R7`-`R8a`, `R11d`, `E7`, `EC6`, `EC7`
- Level: integration, manual
- Fixture/setup: synthetic cases under `tests/fixtures/**` and validators that consume them
- Steps:
  - Assert synthetic cases and their artifact references remain under `tests/fixtures/`.
  - Assert no selector or validator has a special production-path fixture category.
  - Validate the test-owned metadata with the relevant validators.
- Expected result: validator inputs are test-owned and cannot resemble active project state.
- Failure proves: contributors and validators can mistake synthetic input for current lifecycle state.
- Automation location: `python scripts/test-change-metadata-validator.py`, `python scripts/test-artifact-lifecycle-validator.py`, `python scripts/test-select-validation.py`, manual reference review.

### T9. Generated output is checked after canonical skill changes

- Covers: `R10`-`R10b`, `EC10`
- Level: integration
- Fixture/setup: canonical `skills/**`, generated public adapters under `dist/adapters/**`
- Steps:
  - After canonical skill edits, run `python scripts/build-skills.py --check`.
  - Run `python scripts/build-adapters.py --version 0.1.1 --check`.
  - Run `python scripts/validate-adapters.py --version 0.1.1`.
  - Run `python scripts/test-adapter-distribution.py`.
  - Assert generated public output changes are deterministic and derived from canonical skill source.
  - Assert `.codex/skills/` remains ignored local runtime state and is not used as tracked release evidence.
- Expected result: generated outputs are current and public adapter packages remain valid.
- Failure proves: public adapter output can drift from canonical skill text.
- Automation location: listed generation and adapter validation commands.

### T10. Repository-owned validation covers the artifact-location contract

- Covers: `R11`-`R11d`
- Level: integration
- Fixture/setup: selector, lifecycle, review-artifact, change-metadata, skill, and adapter validation scripts
- Steps:
  - Run all milestone-specific validator test commands named in the active plan for the touched milestone.
  - Confirm deleted-path routing, lifecycle behavior, formal-review fixture behavior, test-owned skill-validator fixtures, and skill lookup wording are covered by repository-owned tests or explicit manual checks.
  - Use `bash scripts/ci.sh --mode explicit --path <changed-path>...` when selected-check execution is required for the changed path set.
- Expected result: every acceptance criterion has executable or explicit manual proof.
- Failure proves: the artifact-location map can pass by documentation alone without validation coverage.
- Automation location: active plan validation commands and selected explicit-path CI.

### T11. Workflow order and source-of-truth rank do not regress

- Covers: `R1d`, `R2a`, `R2g`, `R3a`, `R12`-`R12b`, `E4`, `E8`, `EC3`, `EC9`
- Level: manual, contract
- Fixture/setup: `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, approved spec, active plan
- Steps:
  - Confirm no touched guidance changes the standard workflow order.
  - Confirm no touched guidance makes `docs/workflows.md` outrank `CONSTITUTION.md`, approved specs, schemas, architecture, active plan state, matching test specs, or explicit safe user paths.
  - Confirm exact review receipt/root shape remains governed by the formal review recording contract.
  - Confirm stale-map conflicts are reported or resolved, not silently ignored.
- Expected result: the guide is a path index and workflow summary, not a hidden constitution or schema.
- Failure proves: the change altered governance rank or formal review recording scope.
- Automation location: manual review; add static assertions in `scripts/test-skill-validator.py` only for stable repeated wording.

### T12. Fixtures and artifact-location guidance do not introduce sensitive local data

- Covers: security/privacy `MUST`, `R6`, `R7b`
- Level: manual, contract
- Fixture/setup: `docs/workflows.md`, owning skill assets, test fixtures, retained fixture rationale
- Steps:
  - Inspect touched assets and fixture rationale for secrets, credentials, private keys, host-specific debug artifacts, and unjustified machine-local paths.
  - Confirm test fixtures remain test-only and reusable shapes remain in owning assets.
- Expected result: fixtures and guidance remain safe to publish.
- Failure proves: public guidance or fixtures can leak sensitive or machine-local data.
- Automation location: manual review plus normal repository diff review.

### T13. Validation remains targeted unless an authority triggers broad smoke

- Covers: performance expectations and validation-boundary behavior
- Level: manual, integration
- Fixture/setup: active plan, selector output, review-resolution, release metadata
- Steps:
  - Run milestone-specific validation first.
  - Inspect selected checks for changed paths when using the CI wrapper.
  - Add broad smoke only if selector output, test spec review, review-resolution, release metadata, or another authority requires it.
- Expected result: validation is sufficient and proportional without making broad smoke a default requirement.
- Failure proves: the change either under-validates touched behavior or wastes time with unjustified broad validation.
- Automation location: `python scripts/select-validation.py --mode explicit --path <changed-path>...`, `bash scripts/ci.sh --mode explicit --path <changed-path>...`

### T14. Lifecycle artifacts stay synchronized through implementation milestones

- Covers: `R12`, active plan state, lifecycle closeout expectations
- Level: integration, manual
- Fixture/setup: active plan, `docs/plan.md`, change-local root, review records
- Steps:
  - After each milestone, update the active plan progress, Current Handoff Summary, validation notes, and change metadata.
  - Validate changed lifecycle artifacts with explicit-path lifecycle validation.
  - Validate review artifacts in structure or closeout mode as appropriate for the current review state.
  - Confirm final closeout only occurs after M1-M4 are implemented, code-reviewed, closed, and required review-resolution is closed.
- Expected result: lifecycle state stays synchronized and downstream readiness is not claimed early.
- Failure proves: the implementation can drift from the approved plan or skip required milestone review gates.
- Automation location: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`, `python scripts/validate-review-artifacts.py --mode structure|closeout ...`, `python scripts/validate-change-metadata.py ...`

## Fixtures and data

- `docs/workflows.md` is the contract surface for the artifact-location map.
- Temporary plan-shaped and review-shaped cases are test fixtures.
- Temporary validator fixtures may be added under `tests/fixtures/**` when behavior needs reusable negative coverage.
- The change-local root for this initiative is `docs/changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording/`.

## Mocking/stubbing policy

No network or external service mocking is needed.

Use temporary directories for selector, lifecycle, review-artifact, or change-metadata negative fixtures. Do not mutate tracked examples solely to create failing fixtures.

## Migration or compatibility tests

- Removing a production-path fixture requires same-slice reference, selector, validator, test, and guidance updates.
- Existing downstream project custom paths are verified by preserving map-before-default wording rather than by building a synthetic downstream project.
- Generated public adapter compatibility is verified through adapter build/check/validation and distribution tests.

## Observability verification

Observability is through tracked artifacts and validator output:

- `docs/workflows.md` visibly contains the artifact-location map, source-rank rule, schema disclaimer, and conditional artifact rows.
- Public skills visibly contain concise lookup wording.
- Selector output visibly bounds retired-example deletion compatibility.
- Lifecycle and review-artifact validation output proves fixture isolation.
- Review logs, review-resolution, change metadata, plan progress, and validation notes record milestone state.

## Security/privacy verification

Run manual review on touched documentation, skill assets, fixture rationale, and generated public output. Confirm no secrets, credentials, private keys, sensitive runtime values, or unjustified machine-local paths were added.

## Performance checks

No runtime performance checks are needed. Token-efficiency is covered by static/manual checks that public skills discourage broad authoritative-document searches for path discovery and avoid duplicated long path tables.

## Manual QA checklist

- [ ] `docs/workflows.md` answers where common artifacts go.
- [ ] The artifact table says it is not a schema.
- [ ] Source-rank and lookup/read order are distinguishable.
- [ ] Review rows point to the formal review recording contract for exact shapes.
- [ ] Public skills use concise lookup wording and short local defaults.
- [ ] Public skills do not expose maintainer-only validator or adapter internals where portable wording is enough.
- [ ] No parallel documentation examples surface remains.
- [ ] Synthetic validator cases live only under test-owned fixture paths.
- [ ] Generated adapter output is current after canonical skill edits.
- [ ] Plan, plan index, change metadata, review log, and review-resolution remain synchronized.

## What not to test

- Do not test a new runtime artifact-placement engine; this change does not add one.
- Do not encode every possible downstream custom path as fixtures; one map-before-default contract check plus manual review is sufficient.
- Do not snapshot entire public skills or `docs/workflows.md`; assert stable contractual phrases and behavior instead.
- Do not require broad smoke by default.
- Do not test formal review receipt field shape here beyond ensuring the artifact-location map delegates exact shape to the formal review recording contract.

## Uncovered gaps

None.

If implementation discovers that the retained fixture cannot be safely retained or moved under the current spec rules, return to spec or plan before guessing.

## Next artifacts

```text
implement M1
code-review M1
implement M2
code-review M2
implement M3
code-review M3
implement M4
code-review M4
explain-change
verify
pr
```

## Follow-on artifacts

None yet.

## Readiness

Active proof surface for implementation.

Immediate next repository stage: `implement` M1.
