# RigorLoop first-release branch rationale

## Summary

This explanation covers the first-release implementation branch from `45629e0` through `aa11d3b`.

That branch turns the repository from a generic AI-ready template into a RigorLoop starter kit with:

- an explicit workflow contract;
- canonical authored workflow sources under `docs/`, `specs/`, `skills/`, `schemas/`, and `scripts/`;
- tracked generated Codex compatibility output under `.codex/skills/`;
- local validators for skill structure and machine-readable change metadata;
- repo-owned CI checks;
- a shipped golden-path example under `docs/changes/0001-skill-validator/`.

The diff is large because it had to establish both the contract and the concrete proof-of-value example in one coherent branch. The actual implementation range changed 90 files with 8294 insertions and 125 deletions.

This explanation does not justify unrelated working-tree deletions in `.agents/skills/` or `.codex/PLANS.md`. Those deletions were pre-existing and were intentionally left outside the reviewed initiative work.

## Problem

The repository already had workflow-shaped directories and template files, but it did not yet behave like a reviewable workflow product.

The main problems were:

- the repository still presented itself as a generic template instead of RigorLoop;
- workflow expectations were implicit or spread across docs, chats, and untracked working-tree files;
- canonical authored content and generated compatibility output were not clearly separated in tracked history;
- CI still pointed at placeholder behavior instead of repo-owned validation;
- there was no concrete proof-of-value example showing how a non-trivial change moved from proposal to verification with durable artifacts.

## Decision trail

| Artifact | Decision carried into the branch | How it shaped the diff |
| --- | --- | --- |
| `docs/proposals/2026-04-19-rigorloop-workflow-product.explore.md` | Choose a starter-kit workflow product over a generic template or platform build. | The branch focuses on workflow surfaces, validators, examples, and reviewability instead of runtime orchestration. |
| `docs/proposals/2026-04-19-rigorloop-project-direction.md` | Make RigorLoop an artifact-driven, Git-first AI engineering workflow with a fast lane plus full lifecycle. | `README.md`, `docs/workflows.md`, `AGENTS.md`, `specs/`, and the change-local example now present that contract explicitly. |
| `specs/rigorloop-workflow.md` | Define the first-release contract, including fast-lane boundaries, milestone rules, validation rules, source-of-truth boundaries, and change metadata. | The branch adds the required docs, schemas, scripts, fixtures, generated-output handling, and example artifacts. |
| `docs/architecture/2026-04-19-rigorloop-first-release-repository-architecture.md` and `docs/adr/ADR-20260419-repository-source-layout.md` | Keep `skills/` canonical, `.codex/skills/` generated, `schemas/` authored, and `docs/changes/<change-id>/` as the durable change-local pack. | The branch tracks both skill trees, adds deterministic generation, and ships the `0001-skill-validator` pack without creating a second authored workflow tree. |
| `docs/proposals/2026-04-19-implementation-milestone-commit-policy.md` | Treat completed planned milestones as commit boundaries without forcing one PR per milestone. | The branch history is deliberately split into `M1` through `M6` commits plus review-driven follow-up commits. |
| `docs/plans/2026-04-19-rigorloop-first-release-implementation.md` | Implement the release in six reviewable milestones. | The diff groups naturally into M1 guidance, M2 schemas, M3 fixtures, M4 validator/generator, M5 CI, and M6 proof-of-value artifacts. |
| `docs/changes/0001-skill-validator/review-resolution.md` | Preserve durable review dispositions for material follow-up items. | The final branch includes fixes that were driven by review, not just the original plan. |

## Milestone map

| Milestone | Commits | Outcome |
| --- | --- | --- |
| `M1` | `45629e0`, `bdc7ecf`, `32ff76d`, `2e57b1c`, `6681dea` | Aligned root guidance, tracked referenced contract artifacts, tracked `skills/` and `.codex/skills/`, and aligned the plan surfaces. |
| `M2` | `44a8eaf`, `7d82242` | Added `schemas/`, metadata validation, and valid/invalid change-metadata fixtures. |
| `M3` | `ca0f214` | Normalized the canonical skill corpus and added skill-validator fixtures. |
| `M4` | `8347d73`, `8dab0f3`, `972a11a` | Added skill validation, fixture runner, deterministic generation, first deliberate `.codex/skills/` sync, and the missing-`SKILL.md` regression fix. |
| `M5` | `4f4a9ec` | Replaced template CI behavior with repo-owned structural checks and a thin GitHub Actions wrapper. |
| `M6` | `a066630`, `aa11d3b` | Published the `0001-skill-validator` golden-path artifact pack and added durable review resolution. |

## Diff rationale by area

| Area | Files | Change | Reason | Source artifact | Test or evidence |
| --- | --- | --- | --- | --- | --- |
| Workflow contract and public positioning | `README.md`, `docs/workflows.md`, `AGENTS.md`, `.github/pull_request_template.md`, `specs/rigorloop-workflow.md`, `specs/rigorloop-workflow.test.md` | Replaced template posture with the approved RigorLoop workflow contract, fast-lane rules, milestone policy, PR-summary expectations, and repository boundaries. | Contributors needed one tracked contract surface instead of scattered instructions and working-tree-only guidance. | Project direction proposal, workflow spec, workflow test spec | Manual contract checks `T1` to `T4`, `T14`, `T16`; final verify pass |
| Planning and design record | `docs/plan.md`, `docs/plans/0000-00-00-example-plan.md`, `docs/plans/2026-04-19-rigorloop-first-release-implementation.md`, `docs/proposals/*.md`, `docs/architecture/*.md`, `docs/adr/*.md` | Added the design trail and the living plan that justified the implementation order and recorded review follow-ups. | The branch had to make the workflow itself reviewable, not just the resulting scripts. | Explore, proposal, architecture, milestone policy, active plan | Plan-review, spec-review, architecture-review, code-review history recorded in the plan |
| Canonical and generated skill surfaces | `skills/*/SKILL.md`, `.codex/skills/*/SKILL.md` | Tracked the canonical workflow skill set, aligned plan/implement/workflow guidance to the approved contract, and kept `.codex/skills/` as generated compatibility output after the deliberate M4 sync. | Clean checkouts needed to expose the same authored and generated surfaces the docs described. | Workflow spec `R20` to `R24a`, architecture and ADR | `diff -qr skills .codex/skills`, `python scripts/build-skills.py --check`, final verify pass |
| Machine-readable traceability | `schemas/change.schema.json`, `schemas/skill.schema.json`, `scripts/validate-change-metadata.py`, `tests/fixtures/change-metadata/*` | Added the first-release metadata contract and a stdlib-only validator with valid and invalid fixtures. | The repository needed a concrete `change.yaml` shape before the golden-path example could claim machine-readable traceability. | Workflow spec `R25` to `R25e`, plan M2 | `python scripts/validate-change-metadata.py ...`, negative fixture runs for missing and malformed metadata |
| Skill validation and drift control | `scripts/skill_validation.py`, `scripts/validate-skills.py`, `scripts/test-skill-validator.py`, `scripts/build-skills.py`, `tests/fixtures/skills/*` | Added the structural skill validator, fixture-driven CLI tests, generated-output drift checks, and deterministic generation from `skills/` to `.codex/skills/`. | The first proof-of-value change was intentionally a small, objective validator instead of a subjective workflow scorer. | Workflow spec `R13` to `R19`, architecture decision to keep validator and schema roles separate | `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, `python scripts/build-skills.py --check`, review-driven mixed-tree regression fix |
| CI and contributor rerun surface | `scripts/ci.sh`, `.github/workflows/ci.yml` | Replaced placeholder CI behavior with the real repo-owned validation commands and kept hosted CI as a thin wrapper. | The workflow contract requires CI to enforce structural correctness using repo-owned logic instead of duplicating behavior in YAML. | Workflow spec `R9`, `R9a`, `R18`, `R19`; plan M5 | `bash scripts/ci.sh`, deliberate stale-generated-output failure, wrapper review `T13` and `T14` |
| Golden-path proof-of-value pack | `docs/changes/0001-skill-validator/*` | Added concise change-local wrapper artifacts, valid `change.yaml`, verification notes, explain-change notes, and durable `review-resolution.md`. | The branch needed one end-to-end example that showed proposal, spec, plan, tests, verify, explain-change, and traceability without duplicating the full top-level contract. | Workflow spec `R13`, `R14`, `R25f`, `R25g`; M6 plan and review-resolution policy | `python scripts/validate-change-metadata.py docs/changes/0001-skill-validator/change.yaml`, manual artifact review, `T15`, `T16` |

## Review-driven corrections

Some of the most important changes were not part of the first draft of each milestone. They were added because code review exposed real contract gaps.

| Review item | Correction | Why it mattered |
| --- | --- | --- |
| Root docs pointed to spec, architecture, and proposal artifacts that were not tracked in git. | Added the referenced top-level artifacts to the branch in M1 follow-up work. | Clean checkouts needed to resolve the documented contract from repository history. |
| Docs described canonical and generated skill surfaces that were still not tracked or aligned. | Tracked `skills/` and `.codex/skills/`, then aligned canonical `plan`, `implement`, and `workflow` guidance. | Contributor docs had to match the actual branch surfaces. |
| The example plan and plan index still lagged the milestone policy. | Updated `docs/plan.md` and `docs/plans/0000-00-00-example-plan.md`. | Required-reading surfaces had to match `R8` through `R8e`. |
| The initial skill validator missed the case where a sibling directory lacked `SKILL.md`. | Broadened source-skill discovery and added the `missing-skill-file` regression fixture. | This closed a correctness gap against `R15`; one valid sibling could no longer hide a broken directory. |
| The proof-of-value pack lacked durable review resolution after multiple material review rounds. | Added `review-resolution.md` and linked it from `change.yaml`, `verify-report.md`, and `explain-change.md`. | The shipped example needed to satisfy `R12c`, not only the earlier implementation milestones. |

## Tests added or changed

| Test surface | What it proves | Why this level is appropriate |
| --- | --- | --- |
| `tests/fixtures/change-metadata/valid-basic/change.yaml` plus invalid metadata fixtures | `change.yaml` accepts the approved first-release shape and rejects missing or malformed required fields. | Metadata validation is a file-contract concern, so fixture-backed integration checks are more useful than unit tests against parser internals. |
| `tests/fixtures/skills/*` | The approved minimum skill-structure failures are objective and reproducible: missing metadata, missing sections, duplicate names, placeholder text, and missing `SKILL.md` in mixed trees. | The workflow contract intentionally keeps the validator simple and structural, so explicit fixtures are the clearest proof. |
| `scripts/test-skill-validator.py` | The public CLI `python scripts/validate-skills.py` behaves correctly for the valid and invalid fixture corpus. | Testing the CLI matches the documented contributor command surface and avoids proving only internal helpers. |
| `python scripts/build-skills.py --check` plus deliberate drift injection during milestone validation | Generated output is deterministic, tracked, and fails clearly when stale or hand-edited. | Drift detection is fundamentally an integration check across authored and generated trees. |
| `bash scripts/ci.sh` | The repo-owned CI wrapper runs the exact structural checks the release depends on. | The workflow wants CI logic in repo scripts, not duplicated across shell snippets in workflow YAML. |

## Verification evidence

Final verification was based on the implemented branch state, not only on milestone-local checks.

Commands rerun during final verify:

- `bash scripts/ci.sh`
  - pass
  - validated canonical skills, ran the skill-validator fixture suite, and confirmed generated skills are in sync
- `python scripts/validate-change-metadata.py docs/changes/0001-skill-validator/change.yaml`
  - pass
  - reported `valid change metadata`
- `! python scripts/validate-change-metadata.py tests/fixtures/change-metadata/missing-title/change.yaml`
  - expected failure
  - proved missing required top-level metadata is rejected
- `! python scripts/validate-change-metadata.py tests/fixtures/change-metadata/bad-review-shape/change.yaml`
  - expected failure
  - proved malformed review data is rejected
- `! python scripts/validate-skills.py .codex/skills`
  - expected failure
  - proved generated output is not accepted as authored source of truth

Known CI boundary:

- the local repo-owned CI wrapper passed;
- `.github/workflows/ci.yml` now matches the thin-wrapper design;
- no hosted GitHub Actions run was observed from this environment, so remote CI success is not claimed here.

## Alternatives rejected

These alternatives were explicitly rejected during proposal and implementation, and they explain why the diff looks the way it does.

- Keep the repository as a generic template.
  - Rejected because the branch needed a concrete product identity and a stable workflow contract.
- Build a broader platform or orchestration layer.
  - Rejected because the repository strength is explicit artifacts and Git-based review, not a hosted runtime.
- Add richer skill metadata, writing-quality scoring, or philosophy scoring to the first validator.
  - Rejected because the first release needed objective structural checks with low adoption friction.
- Treat `.codex/skills/` as authored content.
  - Rejected because that would collapse the canonical-versus-generated boundary the architecture was trying to establish.
- Require a PR after every milestone.
  - Rejected because the workflow standardizes trustworthy commit boundaries, not mandatory PR fragmentation.
- Copy the full top-level proposal/spec/architecture docs into the `0001` example pack.
  - Rejected because the change-local pack should stay concise and link back to the approved source artifacts.

## Scope control

The branch intentionally did not do several things that might look adjacent:

- it did not build a hosted service, agent runtime, or control plane;
- it did not replace Git, pull requests, CI, or human review with repository automation;
- it did not redesign release automation beyond making contributor-facing docs honest about current repo-owned validation;
- it did not introduce network dependencies or third-party validator libraries for the first release;
- it did not make generated output the source of truth;
- it did not require the full artifact lifecycle for trivial fast-lane changes.

## Risks and follow-ups

The branch is functionally ready, but a few follow-ups remain visible:

- `docs/changes/0001-skill-validator/change.yaml` still under-reports traceability slightly because its machine-readable requirement and test lists do not yet name `R10` to `R12c` and `T16`.
- `README.md` still says “Active implementation work is tracked in” even though M1 through M6 are complete.
- `scripts/build-skills.py` still carries an unused `shutil` import.
- Final verify was run locally; hosted GitHub Actions execution was not observed from this environment.
- The working tree still contains unrelated pre-existing deletions outside this initiative:
  - `.agents/skills/prepare-release/SKILL.md`
  - `.agents/skills/verify-change/SKILL.md`
  - `.codex/PLANS.md`

## PR-ready summary

- Repositioned the repository from a generic template to the RigorLoop workflow product with explicit fast-lane and full-lifecycle guidance.
- Added the first-release workflow contract, test spec, architecture, ADR, and living implementation plan.
- Tracked canonical `skills/`, generated `.codex/skills/`, and deterministic generation/drift checks between them.
- Added first-release metadata schemas, metadata validation, and skill-structure validation with objective fixtures.
- Replaced placeholder CI with repo-owned structural checks and a thin GitHub Actions wrapper.
- Shipped `docs/changes/0001-skill-validator/` as the end-to-end proof-of-value example, including durable review resolution.
