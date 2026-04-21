# RigorLoop workflow test spec

## Status

- archived

## Related spec and plan

- Spec: `specs/rigorloop-workflow.md`
- Plan: `docs/plans/2026-04-19-rigorloop-first-release-implementation.md`
- Architecture: `docs/architecture/2026-04-19-rigorloop-first-release-repository-architecture.md`
- ADR: `docs/adr/ADR-20260419-repository-source-layout.md`

## Testing strategy

- Use documentation and contract review for requirements that are intentionally enforced through contributor-facing guidance rather than code.
- Use filesystem-backed integration tests for skill validation, metadata validation, generation, and drift detection.
- Use smoke tests through `bash scripts/ci.sh` for the required structural CI contract.
- Prefer real files and fixture directories under `tests/fixtures/` over mocks or snapshots.
- Use manual verification only where the first release intentionally relies on docs, templates, or repository controls instead of code enforcement.

## Requirement coverage map

| Requirement IDs | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `R1`-`R7b` | `T1` | manual | Workflow documentation and contributor guidance contract |
| `R8`-`R8e` | `T2` | manual | Planned milestone work, commit format, and PR boundary rules |
| `R9`, `R18`, `R19` | `T13` | smoke | `scripts/ci.sh` runs the required structural checks |
| `R9a`, `R27` | `T14` | manual | GitHub workflow remains a thin wrapper over repo-owned commands |
| `R10`-`R12c` | `T3`, `T16` | manual, integration | PR summary, explain-change split, and review-resolution visibility |
| `R13`, `R14` | `T15` | integration | Golden-path skill-validator example and artifact pack |
| `R15`, `R15a` | `T8`, `T9`, `T10` | integration | Canonical skill validation and intentionally simple rule set |
| `R16` | `T9`, `T10` | integration | Invalid fixture cases for the required validator failures |
| `R17` | `T11`, `T12` | integration | Deterministic generation and stale/hand-edited drift failure |
| `R20`-`R24a` | `T4`, `T11`, `T12`, `T14` | manual, integration | Canonical versus generated boundaries and repo guidance |
| `R25`, `R25a`-`R25e` | `T5`, `T6`, `T7`, `T15` | integration | `change.yaml` schema shape and validation |
| `R25f`, `R25g` | `T15`, `T16` | manual, integration | Narrative remains in Markdown and reviewer summary remains in PR text |
| `R25h` | `T1`, `T4` | manual | Fast-lane guidance may omit `change.yaml` unless explicitly required |
| `R26` | `T4`, `T13` | manual, smoke | Early enforcement remains structure-first rather than ceremony-first |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| `E1` | `T15`, `T13` | Golden path example plus the structural checks it depends on |
| `E2` | `T1` | Fast-lane docs-only flow remains explicitly documented |
| `E3` | `T1` | Fast-lane rejection for workflow-order or CI changes remains explicit |
| `E4` | `T2` | Multiple milestone commits may share one PR |
| `E5` | `T2` | Fast-lane or unplanned single-slice work does not require milestone commit format |

## Edge case coverage

- Fast-lane docs-only work may omit `change.yaml` while still requiring a visible spec and validation note: `T1`, `T4`
- A workflow-order or CI-behavior change must be rejected from fast lane: `T1`
- Planned milestone work with one or more milestones must still honor milestone closeout and commit rules: `T2`
- Canonical `skills/` may be valid while stale `.codex/skills/` is invalid due to drift: `T12`
- Invalid metadata with missing top-level fields, malformed validation records, or malformed review data must fail clearly: `T6`, `T7`
- Placeholder text and duplicate names must fail even if other skill structure is valid: `T10`
- Baseline validation must not require secrets, network access, or Codex installation: `T17`

## Test cases

### T1. Workflow documentation exposes the two-lane contract

- Covers: `R1`, `R2`, `R3`, `R4`, `R5`, `R6`, `R7`, `R7a`, `R7b`, `R25h`, `E2`, `E3`
- Level: manual
- Fixture/setup:
  - `README.md`
  - `docs/workflows.md`
  - `AGENTS.md`
  - `.github/pull_request_template.md`
- Steps:
  - Review the contributor-facing docs and confirm they describe both fast lane and full lifecycle.
  - Confirm the fast-lane allowlist, disallow list, required spec fields, and allowed spec locations are visible.
  - Confirm the stage-classification table and enforcement model match the approved workflow spec.
- Expected result:
  - A contributor can determine when fast lane is allowed, when it is rejected, and what evidence is required without reading chat history.
- Failure proves:
  - The starter kit workflow contract is still implicit or internally inconsistent.
- Automation location:
  - Manual review during M1 using the updated docs and template surfaces.

### T2. Planned milestone work rules are visible and unambiguous

- Covers: `R8`, `R8a`, `R8b`, `R8c`, `R8d`, `R8e`, `E4`, `E5`
- Level: manual
- Fixture/setup:
  - `specs/rigorloop-workflow.md`
  - `docs/plans/0000-00-00-example-plan.md`
  - `skills/plan/SKILL.md`
  - `skills/implement/SKILL.md`
- Steps:
  - Review the workflow spec, example plan, and canonical plan/implement skill guidance.
  - Confirm milestone closeout evidence, milestone commit format, and multi-milestone PR behavior are described consistently.
  - Confirm fast-lane or unplanned single-slice work is explicitly exempt from milestone-formatted commits.
- Expected result:
  - Planned milestone work has one clear closeout rule and one clear commit-boundary rule across the repo.
- Failure proves:
  - Milestone planning and implementation guidance can drift into contradictory commit expectations.
- Automation location:
  - Manual review during M1 using canonical docs and skill content.

### T3. PR summary and explain-change guidance match the contract

- Covers: `R10`, `R11`, `R12`
- Level: manual
- Fixture/setup:
  - `.github/pull_request_template.md`
  - `README.md`
  - `docs/workflows.md`
- Steps:
  - Review PR-facing guidance and confirm every change requires a reviewer-facing summary.
  - Confirm the split between PR summary, durable Markdown artifacts, and machine-readable metadata is described accurately.
- Expected result:
  - Reviewer-facing requirements for summary, validation, and artifact links are clear before implementation.
- Failure proves:
  - Contributors may satisfy the scripts but still produce incomplete review packages.
- Automation location:
  - Manual review during M1.

### T4. Root guidance preserves canonical-versus-generated boundaries

- Covers: `R20`, `R20a`, `R21`, `R22`, `R23`, `R24`, `R24a`, `R25h`, `R26`, `R27`
- Level: manual
- Fixture/setup:
  - `README.md`
  - `AGENTS.md`
  - `docs/workflows.md`
  - `docs/architecture/2026-04-19-rigorloop-first-release-repository-architecture.md`
- Steps:
  - Confirm root guidance identifies `skills/` as canonical and `.codex/skills/` as generated.
  - Confirm `.codex/PLANS.md` is not referenced as a live compatibility path.
  - Confirm docs still position Git, PRs, CI, and human review as authoritative.
- Expected result:
  - Contributors know what may be hand-edited, what is generated, and what repository controls remain authoritative.
- Failure proves:
  - The source-of-truth split is not enforceable in practice.
- Automation location:
  - Manual review during M1 and M4.

### T5. Valid `change.yaml` passes metadata validation

- Covers: `R25`, `R25a`, `R25b`, `R25c`, `R25d`, `R25e`
- Level: integration
- Fixture/setup:
  - `schemas/change.schema.json`
  - `scripts/validate-change-metadata.py`
  - `tests/fixtures/change-metadata/valid-basic/change.yaml`
- Steps:
  - Run `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/valid-basic/change.yaml`.
- Expected result:
  - The command exits zero and reports the sample metadata file as valid.
- Failure proves:
  - The repository cannot validate the canonical `change.yaml` contract even for a correct sample.
- Automation location:
  - M2 validation and follow-on regression checks.

### T6. Missing required `change.yaml` fields fail validation

- Covers: `R25b`
- Level: integration
- Fixture/setup:
  - invalid fixtures such as:
    - `tests/fixtures/change-metadata/missing-title/change.yaml`
    - `tests/fixtures/change-metadata/missing-review/change.yaml`
- Steps:
  - Run `python scripts/validate-change-metadata.py <invalid-fixture>` for each missing-field case.
- Expected result:
  - Each invalid file exits non-zero and names the missing required field.
- Failure proves:
  - The metadata validator does not actually enforce the documented top-level contract.
- Automation location:
  - Direct validator invocation against invalid fixtures.

### T7. Malformed validation or review records fail metadata validation

- Covers: `R25d`, `R25e`
- Level: integration
- Fixture/setup:
  - invalid fixtures such as:
    - `tests/fixtures/change-metadata/bad-validation-record/change.yaml`
    - `tests/fixtures/change-metadata/bad-review-shape/change.yaml`
- Steps:
  - Run `python scripts/validate-change-metadata.py <invalid-fixture>` for each malformed-record case.
- Expected result:
  - The validator exits non-zero and identifies the invalid validation or review structure.
- Failure proves:
  - `change.yaml` can pass even when it cannot support traceability or review-state inspection.
- Automation location:
  - Direct validator invocation against invalid fixtures.

### T8. Canonical skills pass structural validation

- Covers: `R15`, `R15a`, `R23`
- Level: integration
- Fixture/setup:
  - canonical `skills/*/SKILL.md`
  - `scripts/validate-skills.py`
- Steps:
  - Run `python scripts/validate-skills.py` on the repository after M3 normalization and M4 validator implementation.
- Expected result:
  - The canonical `skills/` tree passes validation with no missing metadata, missing required sections, placeholder text, or source-of-truth violations.
- Failure proves:
  - The canonical workflow source is not good enough to generate or validate reliably.
- Automation location:
  - M4 validation and `bash scripts/ci.sh`.

### T9. Missing metadata or required sections fail skill validation

- Covers: `R15`, `R16`
- Level: integration
- Fixture/setup:
  - `tests/fixtures/skills/valid-basic/`
  - `tests/fixtures/skills/missing-name/`
  - `tests/fixtures/skills/missing-description/`
  - `tests/fixtures/skills/missing-title/`
  - `tests/fixtures/skills/missing-expected-output/`
- Steps:
  - Run `python scripts/test-skill-validator.py`.
- Expected result:
  - The valid fixture passes and each missing-field or missing-section fixture fails for the expected reason.
- Failure proves:
  - The validator cannot enforce the minimum structural skill contract.
- Automation location:
  - `scripts/test-skill-validator.py`

### T10. Duplicate names and placeholder text fail skill validation

- Covers: `R15`, `R16`
- Level: integration
- Fixture/setup:
  - `tests/fixtures/skills/duplicate-name/`
  - `tests/fixtures/skills/placeholder-text/`
  - canonical `skills/` corpus
- Steps:
  - Run `python scripts/test-skill-validator.py`.
  - Run `python scripts/validate-skills.py` against canonical `skills/`.
- Expected result:
  - Duplicate-name and placeholder fixtures fail, and canonical `skills/` contains neither duplicate names nor placeholder markers.
- Failure proves:
  - The validator misses cross-skill or content-quality failures that the first-release contract explicitly includes.
- Automation location:
  - `scripts/test-skill-validator.py` plus canonical corpus validation.

### T11. Skill generation is deterministic and produces tracked output

- Covers: `R17`, `R23`, `R24a`
- Level: integration
- Fixture/setup:
  - canonical `skills/`
  - generated `.codex/skills/`
  - `scripts/build-skills.py`
- Steps:
  - Run the generation command once to refresh `.codex/skills/`.
  - Re-run the same command or `--check` mode without further edits.
- Expected result:
  - The first run produces the expected generated tree, and the second run reports no drift or unexpected churn.
- Failure proves:
  - Generated compatibility output is not stable enough to review or track in git.
- Automation location:
  - `scripts/build-skills.py`

### T12. Drift check fails on stale or hand-edited generated output

- Covers: `R17`, `R23`, `R24`
- Level: integration
- Fixture/setup:
  - a deliberately edited or stale file under `.codex/skills/`
  - `scripts/build-skills.py --check`
- Steps:
  - Introduce a controlled mismatch between `skills/` and `.codex/skills/`.
  - Run `python scripts/build-skills.py --check`.
- Expected result:
  - The drift check exits non-zero and identifies the canonical and generated paths that diverged.
- Failure proves:
  - Generated output can drift silently from canonical source.
- Automation location:
  - direct `--check` invocation in local validation and CI.

### T13. Repository CI script runs the required structural checks

- Covers: `R9`, `R18`, `R19`, `E1`
- Level: smoke
- Fixture/setup:
  - working `scripts/ci.sh`
  - all required validation scripts present
- Steps:
  - Run `bash scripts/ci.sh` in a passing repository state.
  - Re-run in a controlled failing state, such as stale generated output or an invalid fixture.
- Expected result:
  - The passing run executes skill validation, fixture tests, and drift check successfully.
  - The failing run exits non-zero on the first broken structural check.
- Failure proves:
  - The repository does not actually enforce the first-release CI contract.
- Automation location:
  - `scripts/ci.sh`

### T14. GitHub CI workflow stays a thin wrapper over repo-owned commands

- Covers: `R9a`, `R18`, `R27`
- Level: manual
- Fixture/setup:
  - `.github/workflows/ci.yml`
  - `scripts/ci.sh`
- Steps:
  - Inspect the workflow definition and confirm it calls the repo script rather than duplicating validation logic.
  - Confirm the workflow does not redefine CI behavior inconsistently with the repo script.
- Expected result:
  - GitHub Actions delegates to `bash scripts/ci.sh` and remains a thin integration surface.
- Failure proves:
  - CI logic may drift between repository scripts and hosted automation.
- Automation location:
  - Manual workflow review during M5.

### T15. Golden-path skill-validator artifacts are complete and coherent

- Covers: `R13`, `R14`, `R25f`, `R25g`, `E1`
- Level: integration
- Fixture/setup:
  - `docs/changes/0001-skill-validator/`
  - `docs/changes/0001-skill-validator/change.yaml`
  - top-level proposal/spec/architecture artifacts
- Steps:
  - Confirm the change-local artifact directory contains proposal, spec, plan, test-spec, verify report, explain-change, and `change.yaml`.
  - Run `python scripts/validate-change-metadata.py docs/changes/0001-skill-validator/change.yaml`.
  - Confirm the change-local docs link or summarize the approved top-level artifacts instead of contradicting them.
- Expected result:
  - The repository contains one coherent proof-of-value example from durable artifacts through validation evidence.
- Failure proves:
  - The advertised golden path is incomplete, invalid, or disconnected from the approved contract.
- Automation location:
  - M6 validation plus manual artifact review.

### T16. Review-resolution and reviewer-facing explanation stay visible

- Covers: `R10`, `R11`, `R12`, `R12a`, `R12b`, `R12c`
- Level: manual
- Fixture/setup:
  - `.github/pull_request_template.md`
  - `docs/changes/0001-skill-validator/explain-change.md`
  - `docs/changes/0001-skill-validator/review-resolution.md` when required
- Steps:
  - Confirm the PR template asks for summary, why, verification, and risks.
  - Confirm the example or final change package has a visible place for review resolution when review feedback exists.
  - If a standalone `review-resolution.md` is used, confirm it is only used for the durable/high-impact cases defined by the spec.
- Expected result:
  - Reviewers can find summary and review disposition without reverse-engineering commit history.
- Failure proves:
  - The repository can satisfy automation while still hiding review reasoning from humans.
- Automation location:
  - Manual artifact and template review.

### T17. Baseline validation works without secrets, network, or Codex installation

- Covers: security/privacy and boundary behavior sections of the workflow spec
- Level: smoke
- Fixture/setup:
  - local shell with no repository secrets exported
  - baseline scripts:
    - `scripts/validate-skills.py`
    - `scripts/test-skill-validator.py`
    - `scripts/build-skills.py --check`
    - `scripts/validate-change-metadata.py`
- Steps:
  - Run the baseline validation commands in a normal local environment without providing secrets.
  - Confirm they operate only on repository files and do not require Codex runtime installation or external network access.
- Expected result:
  - Baseline structural validation succeeds or fails for repo-local reasons only.
- Failure proves:
  - The first-release validation surface is more operationally fragile than the contract allows.
- Automation location:
  - Manual smoke verification during M4-M6 and before `verify`.

### T18. Validation failures are specific and contributor-actionable

- Covers: observability requirements from the workflow spec and architecture
- Level: integration
- Fixture/setup:
  - one invalid skill fixture
  - one invalid metadata fixture
  - one stale `.codex/skills/` file
- Steps:
  - Run the skill validator, metadata validator, and drift check against failing cases.
  - Inspect exit codes and failure messages.
- Expected result:
  - Each failure is non-zero and names the file, fixture, skill, or path that caused the error.
- Failure proves:
  - Contributors will struggle to fix failures even if the enforcement logic exists.
- Automation location:
  - direct validator and drift-check invocations.

### T19. Repository-scale performance smoke stays proportional

- Covers: performance/scalability expectations from the architecture
- Level: manual
- Fixture/setup:
  - current repository tree
- Steps:
  - Run the main validation commands on the repository-sized fixture set.
  - Record rough local wall-clock behavior.
- Expected result:
  - Validation behaves like linear filesystem work and does not require a build service, cache, or database.
- Failure proves:
  - The first-release implementation is more operationally heavy than the approved architecture allows.
- Automation location:
  - manual smoke check before `verify`.

## Fixtures and data

- Skill fixtures:
  - `tests/fixtures/skills/valid-basic/`
  - `tests/fixtures/skills/missing-name/`
  - `tests/fixtures/skills/missing-description/`
  - `tests/fixtures/skills/missing-title/`
  - `tests/fixtures/skills/missing-expected-output/`
  - `tests/fixtures/skills/duplicate-name/`
  - `tests/fixtures/skills/placeholder-text/`
- Metadata fixtures:
  - `tests/fixtures/change-metadata/valid-basic/change.yaml`
  - `tests/fixtures/change-metadata/missing-title/change.yaml`
  - `tests/fixtures/change-metadata/missing-review/change.yaml`
  - `tests/fixtures/change-metadata/bad-validation-record/change.yaml`
  - `tests/fixtures/change-metadata/bad-review-shape/change.yaml`
- Real repository corpus:
  - canonical `skills/`
  - generated `.codex/skills/`
  - `docs/changes/0001-skill-validator/`

## Mocking and stubbing policy

- Do not mock filesystem structure for validator, generator, or drift behavior when a temp directory or real fixture tree can be used.
- Do not use snapshots as the only proof for behavioral requirements.
- Prefer real fixture directories and direct CLI invocations over unit tests that stub file contents.
- If a test needs a stale generated tree, create it by controlled file edits in a temp copy rather than by mocking the drift logic.

## Migration and compatibility tests

- `T4` verifies no contributor-facing guidance still depends on `.codex/PLANS.md`.
- `T11` and `T12` verify the one-way `skills/` to `.codex/skills/` compatibility flow.
- `T14` verifies CI remains a thin wrapper rather than a second source of truth.
- `T15` verifies the first change-local artifact pack coexists with the approved top-level artifacts rather than replacing them.

## Observability verification

- `T13` verifies CI exits non-zero on structural failure.
- `T18` verifies validators and drift checks emit file-specific, path-specific failures.
- `T15` and `T16` verify reviewers can inspect validation evidence and review resolution without reading every artifact.

## Security and privacy verification

- `T17` verifies baseline validation does not require secrets, network, or Codex installation.
- Manual review should confirm no fixture, `change.yaml`, or docs artifact stores credentials or sensitive runtime configuration.

## Performance checks

- `T19` is a manual smoke check only; there is no hard benchmark gate for the first release.
- If repository-scale validation becomes noticeably slow, treat it as an implementation issue to fix before broadening CI scope.

## Manual QA checklist

- [ ] `README.md`, `docs/workflows.md`, `AGENTS.md`, and `.github/pull_request_template.md` describe the same workflow and source-of-truth split.
- [ ] No contributor-facing doc still references `.codex/PLANS.md`.
- [ ] `skills/` is clean enough for deliberate generation and `.codex/skills/` is only updated during the generation milestone.
- [ ] `bash scripts/ci.sh` names and runs the real structural commands.
- [ ] `docs/changes/0001-skill-validator/` contains the required artifact pack and a valid `change.yaml`.
- [ ] Validation failures name the failing skill, file, or path clearly enough for a contributor to act.

## What not to test

- Do not test subjective writing quality, philosophy, or “good taste” in skill content.
- Do not test GitHub release publishing end to end in this initiative.
- Do not test Codex installation or hosted runtime behavior as a prerequisite for baseline validation.
- Do not test preservation of milestone commits after squash/rebase merge on the default branch; the contract only guarantees branch and PR review visibility.
- Do not add network-dependent checks for the baseline validator, generator, or metadata validation surface.

## Uncovered gaps

- None blocking at the spec or architecture level.
- The implementation should add invalid metadata fixtures alongside the valid sample fixture early enough that `T6` and `T7` are not deferred past code review.
- If the implementation cannot validate YAML with the repository’s chosen runtime assumptions, return to planning before widening implementation scope.

## Follow-on artifacts

- Final disposition: archived after the first-release workflow baseline merged and became the repository's current workflow contract.
- Replacement: none. This artifact remains historical evidence for that merged baseline.

## Readiness

This test spec is archived. Its coverage now describes the merged first-release workflow baseline as historical evidence and no longer serves as the active proof-planning surface.

No further implementation-stage action is pending for this artifact.
