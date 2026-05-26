# Explain Change: CI-Maintenance Skill Rename and Workflow Authoring

## Summary

This change renames the authored CI skill from `ci` to `ci-maintenance`, adds reusable GitHub Actions authoring resources, makes the new contract validator-enforced, and records generated adapter proof for the hard rename.

The implementation keeps actual repository `.github/workflows/*.yml` behavior unchanged. It improves the skill that authors and reviews CI infrastructure; it does not use that skill to rewrite this repository's own workflows.

## Problem

The original skill had a mixed identity: the front matter and directory used `ci`, while the body already described the role as `ci-maintenance`. The skill also stated good CI principles but lacked reusable structure for concise, risk-scoped GitHub Actions workflows.

The approved direction was to treat the rename as an identifier migration and add a workflow skeleton plus a changed-surface risk map so CI authoring is fast on PRs, stronger at schedule/manual/release boundaries, least-privilege by default, and explicit about command ownership.

## Decision Trail

| Stage | Decision | Evidence |
| --- | --- | --- |
| Proposal | Chose Option 4: rename plus skeleton asset plus risk-to-check reference. | `docs/proposals/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring.md` |
| Proposal review | Required explicit alias policy, command ownership boundary, and portable risk-map boundary. | `review-resolution.md`, findings `CIM-PR1` through `CIM-PR3` |
| Spec | Required hard rename, no first-slice alias, no duplicate active skill bodies, metadata front matter, resources, validator checks, adapter proof, and no workflow behavior changes. | `specs/ci-maintenance-skill.md`, especially `CIM-R1` through `CIM-R65` |
| Test spec | Mapped rename, resources, validator behavior, adapter proof, and workflow non-change to deterministic tests and manual proof. | `specs/ci-maintenance-skill.test.md` |
| Architecture | Skipped by plan because the change uses existing skill/resource/validator/adapter mechanisms and adds no new runtime architecture. | Plan `Source Artifacts` and `Decision Log` |
| Plan | Split implementation into M1 skill/resources, M2 validator/tests, and M3 adapter proof/migration evidence. | `docs/plans/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring.md` |
| Code review | M1, M2, and M3 each passed clean code review with no material findings. | `reviews/code-review-m1-r1.md`, `reviews/code-review-m2-r1.md`, `reviews/code-review-m3-r1.md` |

## Diff Rationale By Area

| File or area | Change | Reason | Source artifact | Test/evidence |
| --- | --- | --- | --- | --- |
| `skills/ci-maintenance/SKILL.md` | Created the canonical renamed skill with `name: ci-maintenance`, `version`, `schema-version`, role boundaries, command-source rules, GitHub Actions defaults, output expectations, and resource map. | Satisfies the identity migration and makes the skill's job author/review CI maintenance, not merely run CI. | `CIM-R1`, `CIM-R2`, `CIM-R3a`, `CIM-R12` through `CIM-R19`, `CIM-R34` through `CIM-R49` | `validate-skills.py`, `test-skill-validator.py` |
| `skills/ci/SKILL.md` | Removed the old authored skill body. | Prevents two active skill identities and enforces hard rename. | `CIM-R7`, `CIM-R8`, `AC-CIM-013` | Stale-reference scans, adapter archive inspection |
| `skills/ci-maintenance/assets/github-workflow-skeleton.yml` | Added copy-and-fill GitHub Actions skeleton with PR changed-risk checks, boundary checks, permissions, concurrency, timeouts, action-ref placeholders, install/check placeholders, and cache guidance. | Gives workflow authoring a safe reusable YAML shape without inventing commands or SHAs. | `CIM-R20` through `CIM-R28`, `AC-CIM-006` through `AC-CIM-008`, `AC-CIM-PERM-001` through `AC-CIM-PERM-003` | `test-skill-validator.py`, `build-skills.py --check` |
| `skills/ci-maintenance/references/risk-to-check-map.md` | Added READ reference with portable core rows, project-specific extension rows, and unmapped-surface fail-safe. | Makes risk coverage derivable from changed surfaces while keeping RigorLoop-specific rows non-universal. | `CIM-R29` through `CIM-R33`, `AC-CIM-019` through `AC-CIM-021` | `test-skill-validator.py` |
| Governance/workflow references | Updated direct skill-identifier references in `AGENTS.md`, `skills/workflow/SKILL.md`, `specs/skill-contract.md`, `specs/rigorloop-workflow.md`, and related tests. | Keeps workflow routing and contributor guidance aligned with the new identifier while preserving generic CI prose. | `CIM-R4` through `CIM-R6`, `CIM-R55`, `CIM-R56` | Stale-reference scan and validator tests |
| `scripts/skill_validation.py` | Added `validate_ci_maintenance_contract` checks for front matter, stale identifiers, resources, skeleton defaults, risk-map structure, command blockers, permissions/cache guardrails, and workflow-review guardrails. Later scoped metadata enforcement so generated Claude/OpenCode adapter transforms remain valid. | Converts the skill contract into deterministic repository validation and preserves existing adapter transform behavior. | `CIM-R55` through `CIM-R61`, `CIM-R62` through `CIM-R64`, `AC-CIM-FM-004` | `test-skill-validator.py`, `test-adapter-distribution.py` |
| `scripts/test-skill-validator.py` | Added copied-fixture regression tests that mutate one contract surface at a time and assert stable validator failures. | Proves the validator catches missing metadata, stale identifiers, wrong resource verbs, weakened skeleton/risk-map/defaults, and command/review guardrail regressions. | Test spec `TCIM-001` through `TCIM-030` as applicable | `python scripts/test-skill-validator.py` passed with 191 tests |
| `dist/adapters/manifest.yaml` | Replaced active adapter skill entry `ci` with `ci-maintenance`. | Makes tracked adapter metadata match the canonical hard rename. | `CIM-R7` through `CIM-R11`, `CIM-R62`, `CIM-R63` | Temporary adapter archive validation and inspection |
| `dist/adapters/README.md` | Added migration note telling adopters to use `ci-maintenance` and update direct `ci` invocations; no `ci` alias is installed in this release. | Documents adopter-visible hard rename. | `CIM-R11`, `AC-CIM-015` | M3 code review and generated-output proof |
| `docs/changes/.../generated-output-proof.md` | Recorded generated skill output, temporary `v0.1.5` adapter archives, archive content inspection, and tracked-tree check caveat. | Proves generated public adapter packages include the renamed skill/resources and no active `ci` body without hand-editing generated output. | `CIM-R62` through `CIM-R64`, `TCIM-025`, `TCIM-026` | `build-adapters.py --version v0.1.5`, `validate-adapters.py --root`, archive inspection |
| `docs/changes/.../behavior-preservation.md` | Recorded identity correction, workflow behavior non-change, validator strengthening, generated adapter migration, and migration guidance. | Preserves the proof requested by the proposal and plan. | Plan behavior-preservation requirement | Lifecycle validation |
| Proposal/spec/test-spec/plan/review artifacts | Added and revised lifecycle artifacts, review records, review log, review resolution, active plan state, and plan index. | Keeps the change governed, reviewed, traceable, and milestone-aware. | Repository workflow contract and plan | Review artifact validation, change metadata validation, lifecycle validation |

## Tests Added Or Changed

| Test or proof | What it proves | Why this level is appropriate |
| --- | --- | --- |
| `test_ci_maintenance_contract_validates_canonical_skill` and related validator fixture tests | Canonical `ci-maintenance` passes while weakened contract surfaces fail. | Unit-level validator tests are deterministic and do not rely on model judgment. |
| Missing metadata and stale identifier tests | `version`, `schema-version`, stale `name: ci`, stale `role_name: ci`, and stale invocation wording are rejected. | Directly covers the identifier migration and published-skill metadata requirements. |
| Resource and skeleton tests | Resource map verbs, skeleton defaults, placeholders, permissions, cache/action-reference guidance, and risk-map fail-safe stay present. | Static tests are the right level for published skill text and packaged resources. |
| Review/command guardrail tests | Overbroad permissions, unsafe path filters, unjustified slow PR checks, and missing command-source blockers remain represented in the skill contract. | The approved scope was contract guidance, not executing hosted CI or semantically evaluating arbitrary workflow YAML. |
| Adapter distribution regression suite | Adapter generation, release-validation fixtures, archive packaging, and non-Codex metadata transforms still work after the rename. | Integration-level proof is appropriate because adapter output spans generated packages and release validation. |
| Temporary adapter archive proof | `v0.1.5` Codex, Claude, and OpenCode archives include `ci-maintenance` resources and no active `/ci/` body. | Generated public adapter proof must be archive-based for `v0.1.3+`, not hand-edited tracked package trees. |
| `.github/workflows` diff proof | Repository workflow behavior did not change. | The non-goal is file-level and can be directly proven by no workflow diff. |

## Validation Evidence Available Before Final Verify

The plan records these completed checks:

- `python scripts/test-skill-validator.py` passed after M3 with 191 tests.
- `python scripts/test-adapter-distribution.py` passed after M3 with 112 tests.
- `python scripts/validate-skills.py` passed after M3, validating 23 canonical skill files.
- `python scripts/build-skills.py --check --output-dir /tmp/rigorloop-cim-m3-skills/skills` passed.
- Temporary `python scripts/build-adapters.py --version v0.1.5 --output-dir "$tmpdir"` plus `python scripts/validate-adapters.py --root "$tmpdir" --version v0.1.5` passed.
- Archive inspection of `/tmp/tmp.eXBa1HTkJk/*.zip` found `ci-maintenance/SKILL.md`, `assets/github-workflow-skeleton.yml`, and `references/risk-to-check-map.md` for Codex, Claude, and OpenCode, with no active `/ci/` skill body.
- `git diff -- .github/workflows` produced no output after M3.
- `python scripts/validate-review-artifacts.py --mode structure` and `--mode closeout` passed after code-review M3.
- `python scripts/validate-change-metadata.py .../change.yaml` passed after code-review M3.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` passed after code-review M3.
- `git diff --check --` passed after code-review M3.

`python scripts/build-adapters.py --check --version v0.1.5 --verbose` reports expected tracked-tree archive-era drift and an existing `command_aliases` version-support diagnostic. This is recorded because `v0.1.3+` public adapter skill bodies are release archives rather than tracked source under `dist/adapters/`; the authoritative M3 adapter proof is the temporary archive build plus `validate-adapters.py --root`.

Hosted CI status is not claimed here.

## Review Resolution Summary

`review-resolution.md` is closed. It records 6 resolved material findings:

- `CIM-PR1`, `CIM-PR2`, `CIM-PR3` from proposal review;
- `CIM-SR1`, `CIM-SR2`, `CIM-SR3` from spec review.

Implementation code reviews for M1, M2, and M3 recorded no material findings. No review-resolution work is required for the implementation milestones.

## Alternatives Rejected

| Alternative | Why rejected |
| --- | --- |
| Rename only | Would fix identity but leave CI workflow authoring as principles without reusable structure. |
| Add guidance while keeping `ci` | Would preserve the existing mixed identity and less precise public skill name. |
| Add skeleton without risk map | Would provide YAML shape but not derive checks from changed risk surfaces. |
| Keep `ci` as a first-slice alias | No safe non-duplicating alias mechanism was approved for this slice; duplicate active skills risk routing ambiguity. |
| Hand-edit generated public adapter package output | Repository policy treats generated adapter bodies for `v0.1.3+` as release archives, not tracked source. |
| Change actual repository workflows | Explicitly out of scope; this change improves the CI-maintenance skill, not this repository's `.github/workflows/*.yml`. |
| Add language-specific skeletons or deployment/release workflows | Deferred because the first slice owns one generic GitHub Actions skeleton and non-secret-bearing CI authoring/review guidance. |

## Scope Control

Preserved non-goals:

- No repository `.github/workflows/*.yml` behavior changed.
- No deployment, release publishing, self-hosted runner, or organization-level Actions policy was added.
- No language-specific workflow skeletons were added.
- No `ci` compatibility alias or duplicate active `ci` skill body was shipped.
- No hidden policy was moved into assets; `SKILL.md` remains the operating contract.
- No validation commands or action SHAs were invented.

## Risks And Follow-Ups

- Final `verify` still needs to run before PR readiness is claimed.
- Hosted CI has not been claimed.
- `build-adapters.py --check --version v0.1.5 --verbose` remains an expected mismatch for archive-era adapter output; final verification should continue to rely on temporary archive generation and `validate-adapters.py --root` for generated public adapter proof.
- Follow-on work remains separate: language-specific CI workflow skeletons, actual repository workflow optimization using `ci-maintenance`, GitHub Actions security scanner integration, and release/deploy workflow templates.

## Readiness Statement

This explanation records the rationale for the reviewed implementation. The active plan can move to `verify`; this artifact does not claim verify, branch, PR, hosted CI, or release readiness.
