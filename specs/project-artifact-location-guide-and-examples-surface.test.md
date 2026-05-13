# Project Artifact Location Guide and Examples Surface Test Spec

## Status

active

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
- Selector, lifecycle, review-artifact, and change-metadata tests prove `docs/examples/**` remains non-lifecycle example content and retained fixtures are explicit.
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

### T5. `docs/examples/**` is selected as examples, not active lifecycle state

- Covers: `R6`-`R6c`, `R11a`, `E5`, `EC4`
- Level: unit
- Fixture/setup: `scripts/validation_selection.py`, `scripts/test-select-validation.py`
- Steps:
  - Run selector tests for `docs/examples/README.md`, `docs/examples/plans/example-plan.md`, and `docs/examples/formal-review-recording/**`.
  - Assert each path is classified as `examples` or equivalent documentation/example content.
  - Assert selector output has no unclassified paths or blocking results for these paths.
  - Assert `artifact_lifecycle.validate` is not selected solely because an example path resembles a lifecycle artifact.
- Expected result: examples are known non-lifecycle paths.
- Failure proves: examples can be routed as active project state.
- Automation location: `python scripts/test-select-validation.py`

### T6. Lifecycle validation does not treat examples as active artifacts

- Covers: `R6c`, `R6d`, `R11b`, `E5`, `EC4`
- Level: unit, integration
- Fixture/setup: `scripts/test-artifact-lifecycle-validator.py`, `docs/examples/plans/example-plan.md`
- Steps:
  - Keep or add a lifecycle validator test using `docs/examples/plans/example-plan.md`.
  - Assert the file is not treated as an active plan body.
  - Add coverage, if missing, that example proposal, change, review, or report-looking paths under `docs/examples/**` do not become active lifecycle-managed artifacts.
  - Run explicit-path lifecycle validation against representative example paths.
- Expected result: lifecycle validation ignores examples unless a specific fixture opts in.
- Failure proves: example files can make active lifecycle validation fail or create false project state.
- Automation location: `python scripts/test-artifact-lifecycle-validator.py`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/examples/plans/example-plan.md`

### T7. Formal review examples do not trigger active review closeout

- Covers: `R6e`, `R11c`, `E2`, `E6`, `EC5`
- Level: unit, integration
- Fixture/setup: `docs/examples/formal-review-recording/**`, `scripts/test-review-artifact-validator.py`
- Steps:
  - Add or keep review-artifact or lifecycle coverage proving files under `docs/examples/formal-review-recording/**` are examples.
  - Assert review-like headings in examples do not require `review-log.md`, `review-resolution.md`, or active closeout evidence.
  - Assert copied examples only become active review fixtures when placed in an explicit test fixture or change root.
- Expected result: formal review examples illustrate shapes without becoming active review records.
- Failure proves: examples can trigger false review closeout failures.
- Automation location: `python scripts/test-review-artifact-validator.py`, `python scripts/test-artifact-lifecycle-validator.py`

### T8. Retained skill-validator fixture either moves safely or carries rationale

- Covers: `R7`-`R8a`, `R11d`, `E7`, `EC6`, `EC7`
- Level: integration, manual
- Fixture/setup: `docs/changes/0001-skill-validator/**`, optional `docs/examples/changes/skill-validator/**`, validators and references that cite either path
- Steps:
  - Search references to `docs/changes/0001-skill-validator/` before deciding whether to move it.
  - If moved, assert references, tests, validators, selectors, and contributor-facing guidance are updated in the same slice.
  - If retained, assert a tracked or review-visible rationale says it is a retained validator fixture and historical proof pack, not an active change root or universal template.
  - Assert retained rationale identifies `docs/examples/changes/skill-validator/` as the preferred future move target.
  - Validate retained or moved metadata with the relevant validators.
- Expected result: the active-looking fixture is either safely moved or visibly explained.
- Failure proves: contributors and validators can mistake the fixture for current lifecycle state or a universal minimum artifact pack.
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
  - Confirm examples routing, lifecycle behavior, formal-review example behavior, retained-fixture outcome, and skill lookup wording are covered by repository-owned tests or explicit manual checks.
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

### T12. Examples and artifact-location guidance do not introduce sensitive local data

- Covers: security/privacy `MUST`, `R6`, `R7b`
- Level: manual, contract
- Fixture/setup: `docs/workflows.md`, `docs/examples/**`, retained fixture rationale
- Steps:
  - Inspect touched examples and fixture rationale for secrets, credentials, private keys, host-specific debug artifacts, and unjustified machine-local paths.
  - Confirm any intentionally illustrative local path is clearly marked as reviewed example data.
  - Confirm examples remain non-normative and not active lifecycle artifacts.
- Expected result: examples and guidance remain safe to publish.
- Failure proves: public documentation or examples can leak sensitive or machine-local data.
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
- `docs/examples/README.md`, `docs/examples/plans/example-plan.md`, and `docs/examples/formal-review-recording/**` are example-content fixtures.
- `docs/changes/0001-skill-validator/**` is the retained fixture or migration candidate for the fixture-rationale path.
- Temporary validator fixtures may be added under `tests/fixtures/**` when a behavior needs negative coverage without treating `docs/examples/**` as active lifecycle state.
- The change-local root for this initiative is `docs/changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording/`.

## Mocking/stubbing policy

No network or external service mocking is needed.

Use temporary directories for selector, lifecycle, review-artifact, or change-metadata negative fixtures. Do not mutate tracked examples solely to create failing fixtures.

## Migration or compatibility tests

- Moving `docs/changes/0001-skill-validator/**` requires same-slice reference, selector, validator, test, and guidance updates.
- Retaining `docs/changes/0001-skill-validator/**` requires durable retained-fixture rationale and validation proof.
- Existing downstream project custom paths are verified by preserving map-before-default wording rather than by building a synthetic downstream project.
- Generated public adapter compatibility is verified through adapter build/check/validation and distribution tests.

## Observability verification

Observability is through tracked artifacts and validator output:

- `docs/workflows.md` visibly contains the artifact-location map, source-rank rule, schema disclaimer, and conditional artifact rows.
- Public skills visibly contain concise lookup wording.
- Selector output visibly classifies `docs/examples/**` as examples.
- Lifecycle and review-artifact validation output proves examples are not active state.
- Review logs, review-resolution, change metadata, plan progress, and validation notes record milestone state.

## Security/privacy verification

Run manual review on touched documentation, examples, fixture rationale, and generated public output. Confirm no secrets, credentials, private keys, sensitive runtime values, or unjustified machine-local paths were added.

## Performance checks

No runtime performance checks are needed. Token-efficiency is covered by static/manual checks that public skills discourage broad authoritative-document searches for path discovery and avoid duplicated long path tables.

## Manual QA checklist

- [ ] `docs/workflows.md` answers where common artifacts go.
- [ ] The artifact table says it is not a schema.
- [ ] Source-rank and lookup/read order are distinguishable.
- [ ] Review rows point to the formal review recording contract for exact shapes.
- [ ] Public skills use concise lookup wording and short local defaults.
- [ ] Public skills do not expose maintainer-only validator or adapter internals where portable wording is enough.
- [ ] `docs/examples/**` reads as examples, not active lifecycle state.
- [ ] `docs/changes/0001-skill-validator/**` is either safely moved or clearly retained with rationale.
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
