# Docs Changes Usage Policy test spec

## Status

- active

## Related spec and plan

- Spec: `specs/docs-changes-usage-policy.md`
- Related proposal: `docs/proposals/2026-04-20-docs-changes-usage-policy.md`
- Architecture: `docs/architecture/2026-04-21-docs-changes-usage-policy.md`
- Plan: `docs/plans/2026-04-21-docs-changes-usage-policy.md`
- Related workflow and validation surfaces:
  - `specs/rigorloop-workflow.md`
  - `specs/rigorloop-workflow.test.md`
  - `docs/workflows.md`
  - `AGENTS.md`
  - `CONSTITUTION.md`
  - `README.md`
  - `skills/workflow/SKILL.md`
  - `skills/implement/SKILL.md`
  - generated `.codex/skills/`
  - `schemas/change.schema.json`
  - `scripts/validate-change-metadata.py`
  - `scripts/ci.sh`
  - `.github/workflows/ci.yml`
  - `docs/changes/0001-skill-validator/`
  - `docs/explain/`

## Testing strategy

- Use manual contract review for the workflow spec, workflow test spec, README, and summary surfaces because much of this feature is repository guidance rather than new runtime behavior.
- Treat stage-local `workflow` and `implement` skills as part of the manual proof surface when they operationalize the approved docs-changes contract.
- Use integration coverage for `scripts/validate-change-metadata.py` and `tests/fixtures/change-metadata/` because canonical artifact-key enforcement and scalar-path preservation are executable validator behavior.
- Use the shipped `docs/changes/0001-skill-validator/` pack and approved legacy `docs/explain/*.md` artifacts as real compatibility fixtures rather than synthetic stand-ins.
- Use smoke validation through `bash scripts/ci.sh` after the dedicated change-metadata fixture runner is wired into the repo-owned CI wrapper.
- Treat workflow-test-spec alignment as part of the proof surface because M1 changes the governing workflow contract and the existing top-level workflow test spec already covers `change.yaml`, `0001`, and durable-review-memory behavior.
- Keep migration/compatibility coverage focused on preserving existing valid artifact shapes and legacy explain surfaces rather than forcing a mass migration.

## Requirement coverage map

| Requirement IDs | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `R1`, `R1a`, `R1b`, `R7`, `R8` | `T1` | manual | Normative home, summary-surface alignment, and contributor-visible baseline-versus-conditional rule |
| `R2`, `R2a`, `R2b` | `T2` | manual | Fast-lane omission boundary and required `change.yaml` for non-trivial work |
| `R3`, `R3a`, `R3b`, `R3c`, `R3d`, `R3e`, `R3f` | `T3` | manual | Durable reasoning default, equivalent-surface boundary, and legacy `docs/explain/` compatibility |
| `R4`, `R4a`, `R4b`, `R4c`, `R4d`, `R5`, `R5a` | `T4` | manual | Distinct artifact roles and standalone review-resolution triggers |
| `R6`, `R6a`, `R6b`, `R7a`, `R7b` | `T5`, `T8` | manual, smoke | Objective `verify-report.md` triggers and rich-example non-universality |
| `R9`, `R9a`, `R9b`, `R9c` | `T6`, `T7` | integration | Canonical snake_case keys, scalar string values, and actionable validator failures |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| `E1` | `T2` | Fast-lane work may omit `docs/changes/` only under the approved fast-lane policy |
| `E2` | `T3` | Ordinary non-trivial work uses `change.yaml` plus `explain-change.md` |
| `E3` | `T4` | `review-resolution.md` becomes standalone only when its trigger applies |
| `E4` | `T5` | `verify-report.md` is required only when the objective trigger set applies |
| `E5` | `T8` | `0001-skill-validator/` remains rich reference example, not minimum universal pack |

## Edge case coverage

- Edge case 1: trivial fast-lane change may omit `docs/changes/<change-id>/`: `T2`
- Edge case 2: ordinary non-trivial change can use `change.yaml` plus `explain-change.md`: `T3`
- Edge case 3: multiple verification environments require `verify-report.md`: `T5`
- Edge case 4: routine review feedback does not require standalone `review-resolution.md`: `T4`
- Edge case 5: approved legacy top-level explain artifact remains valid until retired: `T3`
- Edge case 6: PR text or ad hoc docs alone cannot serve as equivalent durable reasoning: `T3`
- Edge case 7: `artifacts` mapping uses canonical snake_case keys with scalar string path values: `T6`, `T7`
- Edge case 8: `0001-skill-validator/` may contain more artifacts than an ordinary non-trivial change without making them universal: `T5`, `T8`

## Test cases

### T1. Workflow contract and summary surfaces expose one consistent packaging rule

- Covers: `R1`, `R1a`, `R1b`, `R7`, `R8`
- Level: manual
- Fixture/setup:
  - `specs/docs-changes-usage-policy.md`
  - `specs/rigorloop-workflow.md`
  - `specs/rigorloop-workflow.test.md`
  - `docs/workflows.md`
  - `AGENTS.md`
  - `CONSTITUTION.md`
  - `README.md`
  - `skills/workflow/SKILL.md`
  - `skills/implement/SKILL.md`
- Steps:
  - Review the approved feature spec, the governing workflow spec, the existing workflow test spec, the contributor summary surfaces, and the stage-local `workflow`/`implement` skills.
  - Confirm `specs/rigorloop-workflow.md` is the normative home for the packaging rule.
  - Confirm `docs/workflows.md`, `AGENTS.md`, `CONSTITUTION.md`, and `README.md` summarize the same baseline-versus-conditional artifact rule without weakening it.
  - Confirm `skills/workflow/SKILL.md` and `skills/implement/SKILL.md` operationalize the same approved baseline-versus-conditional rule rather than treating the change-local pack as optional for ordinary non-trivial work.
  - Confirm the existing workflow test spec remains aligned where it already covers `change.yaml`, `0001-skill-validator/`, and explain-change/review-resolution behavior.
- Expected result:
  - Contributors can find one coherent packaging rule across normative workflow docs, summary surfaces, and stage-local execution guidance.
- Failure proves:
  - The repository would have contract drift between the governing workflow spec, summaries, stage-local skills, and the existing workflow test surface.
- Automation location:
  - Manual review during M1.

### T2. Fast-lane omission stays narrow and non-trivial work still requires `change.yaml`

- Covers: `R2`, `R2a`, `R2b`, `E1`
- Level: manual
- Fixture/setup:
  - `specs/docs-changes-usage-policy.md`
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `AGENTS.md`
  - `skills/workflow/SKILL.md`
  - `skills/implement/SKILL.md`
- Steps:
  - Review the packaging rule in the approved feature spec, the updated workflow/summaries, and the stage-local `workflow`/`implement` guidance.
  - Confirm only approved fast-lane work may omit `docs/changes/<change-id>/change.yaml`.
  - Confirm ordinary non-trivial work missing `change.yaml` is described as incomplete rather than merely discouraged.
  - Confirm the skill guidance does not broaden the docs-changes requirement into the approved fast-lane lane.
- Expected result:
  - The fast-lane omission boundary remains narrow, and ordinary non-trivial work still requires machine-readable change metadata.
- Failure proves:
  - Contributors could misclassify ordinary non-trivial work as docs-changes-optional, or the skill layer could accidentally broaden the requirement into fast-lane work.
- Automation location:
  - Manual review during M1.

### T3. Durable reasoning defaults and legacy equivalents remain truthful

- Covers: `R3`, `R3a`, `R3b`, `R3c`, `R3d`, `R3e`, `R3f`, `E2`
- Level: manual
- Fixture/setup:
  - `specs/docs-changes-usage-policy.md`
  - `specs/rigorloop-workflow.md`
  - `skills/implement/SKILL.md`
  - approved artifacts under `docs/explain/`
- Steps:
  - Review the approved feature spec, updated workflow surfaces, and stage-local implementation guidance.
  - Confirm the default durable reasoning artifact for new non-trivial work is `docs/changes/<change-id>/explain-change.md`.
  - Confirm PR text alone is not a valid substitute.
  - Confirm only workflow-spec-named equivalents may replace the default durable reasoning artifact for a change.
  - Confirm `skills/implement/SKILL.md` treats `docs/changes/<change-id>/explain-change.md` as the default durable reasoning surface for new ordinary non-trivial work unless an approved equivalent already applies.
  - Confirm approved legacy top-level explain artifacts remain valid until migrated or retired, and new top-level explain artifacts are not the default for new work.
- Expected result:
  - New work defaults to change-local `explain-change.md` in both contract and stage-local implementation guidance, while legacy approved `docs/explain/*.md` artifacts remain valid compatibility surfaces.
- Failure proves:
  - Contributors could rely on PR text alone, create new top-level explain artifacts by default, or see stage-local implementation guidance drift from the approved durable reasoning default.
- Automation location:
  - Manual review during M1.

### T4. Artifact roles stay distinct and standalone review-resolution remains conditional

- Covers: `R4`, `R4a`, `R4b`, `R4c`, `R4d`, `R5`, `R5a`, `E3`
- Level: manual
- Fixture/setup:
  - `specs/docs-changes-usage-policy.md`
  - `specs/rigorloop-workflow.md`
  - `docs/changes/0001-skill-validator/explain-change.md`
  - `docs/changes/0001-skill-validator/review-resolution.md`
- Steps:
  - Review the approved artifact-role matrix and the workflow contract's review-resolution rules.
  - Confirm `change.yaml`, `explain-change.md`, `review-resolution.md`, and `verify-report.md` are described as distinct artifact types with different roles.
  - Confirm standalone `review-resolution.md` is required only when the workflow contract's durable review-memory triggers apply.
  - Confirm routine review disposition may remain in PR text or durable reasoning when the standalone trigger does not apply.
- Expected result:
  - Artifact roles stay non-interchangeable, and standalone review-resolution remains conditional instead of becoming universal boilerplate.
- Failure proves:
  - Contributors could cargo-cult standalone review-memory or collapse multiple artifact roles into one ambiguous file.
- Automation location:
  - Manual review during M1.

### T5. Standalone `verify-report.md` uses only the approved trigger set

- Covers: `R6`, `R6a`, `R6b`, `R7a`, `R7b`, `E4`
- Level: manual
- Fixture/setup:
  - `specs/docs-changes-usage-policy.md`
  - `docs/changes/0001-skill-validator/verify-report.md`
  - `README.md`
- Steps:
  - Review the approved `verify-report.md` trigger list.
  - Confirm standalone `verify-report.md` is required only when one of the objective triggers applies.
  - Confirm guidance does not imply that `verify-report.md` is always required just because the shipped `0001` example contains one.
  - Confirm contributor-facing wording still treats `0001-skill-validator/` as a rich reference example rather than the universal minimum pack.
- Expected result:
  - `verify-report.md` remains conditional, and the rich example does not expand into a blanket requirement.
- Failure proves:
  - Contributors could overproduce standalone verification artifacts or misread `0001` as the baseline pack for all non-trivial work.
- Automation location:
  - Manual review during M1 and M3.

### T6. Canonical artifact keys and scalar string values pass repo-owned validation

- Covers: `R9`, `R9a`, `R9b`, `R9c`
- Level: integration
- Fixture/setup:
  - `docs/changes/0001-skill-validator/change.yaml`
  - `tests/fixtures/change-metadata/valid-basic/change.yaml`
  - repo-owned runner: `scripts/test-change-metadata-validator.py`
- Steps:
  - Run `python scripts/test-change-metadata-validator.py`.
  - Run `python scripts/validate-change-metadata.py docs/changes/0001-skill-validator/change.yaml tests/fixtures/change-metadata/valid-basic/change.yaml`.
  - Confirm the shipped `0001` example and the valid fixture both pass with canonical snake_case artifact keys and scalar string path values.
- Expected result:
  - Repo-owned validation accepts canonical artifact keys and the unchanged scalar-path value shape.
- Failure proves:
  - The approved artifact-index contract is not executable or the shipped example drifted from the approved key/value shape.
- Automation location:
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/0001-skill-validator/change.yaml tests/fixtures/change-metadata/valid-basic/change.yaml`

### T7. Invalid artifact keys or value shapes fail with actionable validator output

- Covers: `R9a`, `R9b`, `R9c`
- Level: integration
- Fixture/setup:
  - invalid fixtures:
    - `tests/fixtures/change-metadata/bad-artifact-key/change.yaml`
    - `tests/fixtures/change-metadata/bad-artifact-value-shape/change.yaml`
  - repo-owned runner: `scripts/test-change-metadata-validator.py`
- Steps:
  - Run `python scripts/test-change-metadata-validator.py` after the invalid fixtures are added.
  - Run `python scripts/validate-change-metadata.py <invalid-fixture>` for each invalid fixture.
  - Confirm the validator identifies the invalid artifact-key naming or invalid value-shape problem precisely enough for a contributor to fix it.
- Expected result:
  - Invalid artifact-key names or nested/non-scalar artifact values fail with specific, contributor-actionable errors.
- Failure proves:
  - The validator silently accepts contract drift or fails too vaguely to support the intended packaging policy.
- Automation location:
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-change-metadata.py <invalid-fixture>`

### T8. Repository proof keeps `0001-skill-validator/` valid and includes the metadata test surface

- Covers: `R6b`, `R7a`, `R7b`, `E5`
- Level: smoke
- Fixture/setup:
  - `docs/changes/0001-skill-validator/`
  - `scripts/ci.sh`
  - `.github/workflows/ci.yml`
  - `README.md`
- Steps:
  - Run `python scripts/test-change-metadata-validator.py`.
  - Run `python scripts/validate-change-metadata.py docs/changes/0001-skill-validator/change.yaml`.
  - Run `bash scripts/ci.sh`.
  - Inspect `.github/workflows/ci.yml` and confirm it stays a thin wrapper over the repo-owned CI script.
  - Confirm the `0001` example and contributor entrypoints still read as a rich example rather than a mandatory universal pack.
- Expected result:
  - The repository's standard proof path exercises the change-metadata validator, the shipped `0001` example stays valid, and CI wiring remains thin.
- Failure proves:
  - The new proof surface is missing from the normal validation path, or contributor entrypoints still imply the rich example is universal.
- Automation location:
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/0001-skill-validator/change.yaml`
  - `bash scripts/ci.sh`

## Fixtures and data

- Use the real repository workflow and contributor surfaces:
  - `specs/rigorloop-workflow.md`
  - `specs/rigorloop-workflow.test.md`
  - `docs/workflows.md`
  - `AGENTS.md`
  - `CONSTITUTION.md`
  - `README.md`
- Use real change-local and legacy reasoning artifacts:
  - `docs/changes/0001-skill-validator/`
  - approved artifacts under `docs/explain/`
- Use the existing change-metadata fixtures plus the new negative fixtures planned in M2:
  - `tests/fixtures/change-metadata/valid-basic/change.yaml`
  - `tests/fixtures/change-metadata/missing-title/change.yaml`
  - `tests/fixtures/change-metadata/missing-review/change.yaml`
  - `tests/fixtures/change-metadata/bad-validation-record/change.yaml`
  - `tests/fixtures/change-metadata/bad-review-shape/change.yaml`
  - `tests/fixtures/change-metadata/bad-artifact-key/change.yaml`
  - `tests/fixtures/change-metadata/bad-artifact-value-shape/change.yaml`
- Use repo-owned scripts rather than ad hoc shell parsing as the executable proof surface:
  - `scripts/validate-change-metadata.py`
  - `scripts/test-change-metadata-validator.py`
  - `scripts/ci.sh`

## Mocking/stubbing policy

- Do not add mocks or stubs for this feature. The authoritative inputs are real repository artifacts, real fixtures, and repo-owned validation scripts.
- Do not simulate a schema redesign because the approved architecture explicitly keeps the scalar-path `change.yaml` shape.
- Do not fake hosted GitHub Actions results; local smoke coverage stops at the repo-owned CI wrapper and thin workflow inspection.

## Migration or compatibility tests

- Confirm approved legacy top-level `docs/explain/*.md` artifacts remain valid until retired: `T3`.
- Confirm the shipped `0001-skill-validator/` pack remains valid without reduction: `T5`, `T8`.
- Confirm canonical artifact-key enforcement does not redesign the scalar string value shape: `T6`, `T7`.
- Confirm the existing workflow test spec remains coherent where it already covers `change.yaml`, `0001`, and durable review memory: `T1`.

## Observability verification

- Confirm contributor-facing surfaces make the baseline-versus-conditional rule visible without reverse-engineering `0001`: `T1`, `T5`.
- Confirm validator failures identify invalid artifact-key names or invalid artifact-map value shapes precisely enough to fix: `T7`.
- Confirm `change.yaml` remains an inspectable index of present artifacts rather than a hidden metadata blob: `T6`, `T8`.

## Security/privacy verification

- Confirm the updated packaging guidance does not encourage contributors to rely on private chat notes or PR text alone for durable reasoning: `T3`.
- Confirm `change.yaml`, `explain-change.md`, `review-resolution.md`, and `verify-report.md` continue to be treated as inappropriate locations for secrets or sensitive runtime configuration: `T4`.
- Confirm repo-owned validation and smoke proof remain file-local and do not require secrets or external network access: `T8`.

## Performance checks

- No benchmark suite is required for this feature.
- The approved architecture adds no new subsystem, queue, or network dependency.
- Manual confirmation is sufficient that validation remains file-based and linear in the size of the checked metadata files:
  - `scripts/validate-change-metadata.py`
  - `scripts/test-change-metadata-validator.py`

## Manual QA checklist

- Review the updated workflow spec, workflow test spec, and summary surfaces together and confirm the packaging rule is consistent.
- Review the durable reasoning and legacy compatibility wording and confirm PR text alone is never treated as enough for non-trivial work.
- Review `docs/changes/0001-skill-validator/` and confirm it still reads as a rich example rather than a universal minimum pack.
- Run the metadata validation commands on the shipped `0001` example and the valid fixture.
- Run the new negative fixtures once M2 lands and confirm the validator errors are specific.
- Run `bash scripts/ci.sh` after M3 and confirm the repo-wide proof path includes the new change-metadata test surface.

## What not to test

- Do not add tests for a nested-object `change.yaml` redesign. That behavior is explicitly out of scope.
- Do not add hosted-GitHub-only checks as the main proof surface. Hosted CI observation belongs to later verify/PR work.
- Do not force migration tests that require rewriting all approved `docs/explain/*.md` artifacts. The approved contract preserves them until later migration or retirement.
- Do not treat `0001-skill-validator/` as the required artifact set for every non-trivial change in fixtures or manual review.

## Uncovered gaps

- No blocking spec or architecture gaps remain.
- No blocking implementation gaps remain for the M2 metadata proof surface. The dedicated repo-owned metadata fixture runner now exists at `scripts/test-change-metadata-validator.py`.

## Next artifacts

- `implement`
- `code-review`
- `verify`

## Follow-on artifacts

- None yet

## Readiness

- This test spec is active.
- The tracked-source prerequisite is satisfied for the accepted proposal, approved spec, approved architecture, active plan, and this test spec.
- `implement`, `code-review`, and `verify` are complete for the implementation milestones.
- `explain-change` is complete at `docs/explain/2026-04-21-docs-changes-usage-policy.md`.
- The next stage is `pr`.
- It remains the current proof-planning surface for this initiative until lifecycle closeout moves it to a terminal state.
