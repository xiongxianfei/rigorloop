# Artifact status lifecycle ownership rationale

## Summary

This explanation covers the artifact lifecycle ownership feature stack from `3613da2` through `d9c7fc5`.

The change establishes a repo-wide lifecycle model for proposals, specs, test specs, architecture docs, and ADRs; implements a small validator plus fixtures and CLI entrypoint; aligns workflow docs, templates, and skills with the approved contract; wires deterministic validation into `verify` and CI; migrates the relied-on historical test specs that still used stale lifecycle state; and closes the initiative itself to `Done` during verify once the outcome was already known on-branch.

The feature is mostly workflow-contract and repository-state work rather than runtime product behavior. The diff is therefore broad in artifact count but narrow in product scope: it makes authoritative workflow artifacts truthful and machine-checkable instead of changing user-facing application behavior.

## Problem

The repository had already solved stale lifecycle bookkeeping for execution plans, but the same failure mode still existed across other top-level workflow artifacts:

- proposals still said `draft` long after acceptance or merge;
- specs and architecture docs still used `reviewed` or stale readiness text after approval;
- historical test specs still advertised long-lived `complete`;
- ADR guidance drifted between mixed-case and lowercase models;
- verification could block stale plan lifecycle state, but not stale relied-on proposal/spec/architecture/test-spec state.

That weakened the repository's source-of-truth order. A tracked artifact could look pre-review, active, or historical for reasons unrelated to its real role in the repository, which forced later work to rely on chat history or ad hoc cleanup passes instead of trustworthy tracked state.

## Decision trail

| Artifact | Decision carried into the change | How it shaped the diff |
| --- | --- | --- |
| [`2026-04-20-artifact-status-lifecycle-ownership.md`](../proposals/2026-04-20-artifact-status-lifecycle-ownership.md) | Keep status inside each artifact, make `reviewed` transitional only, distinguish settlement from closeout, make `verify` block on touched/referenced/generated/authoritative stale artifacts, and include a small validator in the first enforcement step. | The diff adds lifecycle rules plus executable validation instead of a docs-only cleanup or a separate status registry. |
| [`artifact-status-lifecycle-ownership.md`](../../specs/artifact-status-lifecycle-ownership.md) | Define the contract in `R1`-`R15b`: allowed status vocabularies, ownership of durable transitions, compact workflow summary, verify block/warn behavior, and migration of stale relied-on artifacts. | The diff updates governance docs, templates, skills, validator logic, CI, and historical artifacts to satisfy those rules directly. |
| [`artifact-status-lifecycle-ownership.test.md`](../../specs/artifact-status-lifecycle-ownership.test.md) | Use a mixed proof surface: executable validator tests plus manual and structural checks for guidance, migration, and CI wiring. | The diff adds validator fixtures and targeted regression coverage while still recording scans and manual lifecycle reviews where prose is the contract. |
| [`2026-04-20-artifact-status-lifecycle-ownership.md`](../architecture/2026-04-20-artifact-status-lifecycle-ownership.md) | Keep enforcement repo-native and small: one stable executable contract registry, deterministic scope by mode, tracked-snapshot reads for CI modes, no network inspection, no second registry. | The diff centers on `scripts/artifact_lifecycle_contracts.py`, `scripts/artifact_lifecycle_validation.py`, `scripts/validate-artifact-lifecycle.py`, and thin CI wiring instead of broad schema machinery. |
| [`ADR-20260419-repository-source-layout.md`](../adr/ADR-20260419-repository-source-layout.md) and the first-release architecture doc | Keep `skills/` canonical, `.codex/skills/` generated, and repo-owned scripts as the enforcement path. | The feature updates canonical skills first, regenerates `.codex/skills/`, and keeps `.github/workflows/ci.yml` as a thin wrapper over `scripts/ci.sh`. |
| [`2026-04-20-artifact-status-lifecycle-ownership.md`](../plans/2026-04-20-artifact-status-lifecycle-ownership.md) | Split implementation into four milestones: validator core, guidance alignment, CI integration, and relied-on artifact migration. Keep the active plan current through review and verify. | The branch history lands as M1 (`3613da2`, `4b228ea`), M2 (`ede28fd`, `eabc1dd`, `95ee525`), M3 (`8aae805`, `385fb42`, `8f352ca`, `4bb3129`), M4 (`71c79e0`), readiness sync (`337e662`), and verify closeout (`d9c7fc5`). |

## Milestone map

| Milestone or stage | Commits | Outcome |
| --- | --- | --- |
| M1 | `3613da2`, `4b228ea` | Added the lifecycle contract registry, validator, CLI, fixtures, and regression fixes for mixed `specs/` content, duplicate-ID severity, draft readiness, and `Next artifacts`. |
| M2 | `ede28fd`, `eabc1dd`, `95ee525` | Aligned workflow docs, templates, approved example surfaces, canonical/generated skills, and the relied-on ADR with the approved lifecycle model, including the shared lowercase ADR status family. |
| M3 | `8aae805`, `385fb42`, `8f352ca`, `4bb3129` | Wired deterministic lifecycle validation into `scripts/ci.sh` and GitHub Actions, then fixed diff-mode scope handling so PR and push validation use merge-base diffs, tracked snapshots, and current-plan context only. |
| M4 | `71c79e0` | Migrated the relied-on historical test specs from stale `complete` state to truthful `archived` closeout state. |
| Verify closeout | `337e662`, `d9c7fc5` | Synced the plan to post-code-review readiness, then closed the initiative itself to `Done` after verify confirmed the full outcome was already known on-branch. |

## Diff rationale by area

| Area | Files | Change | Reason | Source artifact | Test or evidence |
| --- | --- | --- | --- | --- | --- |
| Durable feature artifacts | [`2026-04-20-artifact-status-lifecycle-ownership.md`](../proposals/2026-04-20-artifact-status-lifecycle-ownership.md), [`artifact-status-lifecycle-ownership.md`](../../specs/artifact-status-lifecycle-ownership.md), [`artifact-status-lifecycle-ownership.test.md`](../../specs/artifact-status-lifecycle-ownership.test.md), [`2026-04-20-artifact-status-lifecycle-ownership.md`](../architecture/2026-04-20-artifact-status-lifecycle-ownership.md), [`2026-04-20-artifact-status-lifecycle-ownership.md`](../plans/2026-04-20-artifact-status-lifecycle-ownership.md) | Added the full proposal/spec/test-spec/architecture/plan trail and kept the plan current through implementation, review, verify, and closeout. | The lifecycle model needed tracked decision memory and stage-state evidence, not chat-only review outcomes. | Proposal, spec, architecture, test spec, plan; `CONSTITUTION.md` active-plan rule | Proposal-review, spec-review, architecture-review, plan-review, code-review, and verify findings are recorded in the plan history. |
| Validator core and contract registry | [`artifact_lifecycle_contracts.py`](../../scripts/artifact_lifecycle_contracts.py), [`artifact_lifecycle_validation.py`](../../scripts/artifact_lifecycle_validation.py), [`validate-artifact-lifecycle.py`](../../scripts/validate-artifact-lifecycle.py) | Implemented one stable executable contract surface, artifact parsing, status and closeout checks, related-scope classification, and mode-aware CLI entrypoints. | The approved architecture required executable enforcement from v0.1, but only for objective structural lifecycle defects. | Spec `R4`-`R13c`; architecture registry and mode model; plan M1 and M3 | `python scripts/test-artifact-lifecycle-validator.py`; targeted `validate-artifact-lifecycle.py` runs; `bash scripts/ci.sh` |
| Fixture suite and validator regressions | [`tests/fixtures/artifact-lifecycle/`](../../tests/fixtures/artifact-lifecycle), [`test-artifact-lifecycle-validator.py`](../../scripts/test-artifact-lifecycle-validator.py) | Added valid and invalid fixtures for proposal/spec/test-spec/architecture/ADR lifecycle shapes, related-scope expansion, merge-base PR scope, tracked-only CI baselines, generated-source boundaries, draft readiness, and migrated historical-state cases. | The highest-risk logic in this feature is validator correctness, not prose formatting alone. | Test spec `T3`-`T6`, `T8`-`T11`, `T14`; plan M1 and M3 | 32 validator tests pass in the final branch state. |
| Workflow contract and human guidance | [`specs/rigorloop-workflow.md`](../../specs/rigorloop-workflow.md), [`docs/workflows.md`](../workflows.md), [`CONSTITUTION.md`](../../CONSTITUTION.md), [`AGENTS.md`](../../AGENTS.md), [`specs/feature-template.md`](../../specs/feature-template.md), [`specs/feature-template.test.md`](../../specs/feature-template.test.md) | Added the compact lifecycle summary, settlement-versus-closeout wording, closeout patterns, verify policy, and template guidance for lifecycle-managed artifacts. | Contributors needed discoverable human guidance that matched the validator and did not depend on chat history. | Spec `R1`-`R3c`, `R7`-`R10e`, `R14`-`R14b`; plan M2 | Guidance scans recorded in the plan; `bash scripts/ci.sh`; manual review of settled versus terminal wording |
| Stage skills and generated compatibility output | [`skills/proposal/SKILL.md`](../../skills/proposal/SKILL.md), [`skills/spec/SKILL.md`](../../skills/spec/SKILL.md), [`skills/test-spec/SKILL.md`](../../skills/test-spec/SKILL.md), [`skills/architecture/SKILL.md`](../../skills/architecture/SKILL.md), [`skills/verify/SKILL.md`](../../skills/verify/SKILL.md), [`skills/workflow/SKILL.md`](../../skills/workflow/SKILL.md), matching [`.codex/skills/`](../../.codex/skills/) files | Aligned the canonical lifecycle skills and regenerated the Codex compatibility mirror so contributors see the same lifecycle model across authoring, review, verify, and workflow routing. | Leaving skills stale would have reintroduced contradictory lifecycle guidance immediately after the spec landed. | Spec `R3c`, `R11`-`R13c`; architecture generated-boundary rule; plan M2 | `python scripts/validate-skills.py`; `python scripts/build-skills.py`; `python scripts/build-skills.py --check` |
| CI integration and deterministic scope | [`scripts/ci.sh`](../../scripts/ci.sh), [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml), [`artifact_lifecycle_validation.py`](../../scripts/artifact_lifecycle_validation.py), [`docs/workflows.md`](../workflows.md) | Wired lifecycle validation into repo-owned CI, then fixed PR-mode diffs, tracked-snapshot reads, and active-plan scope filtering so diff-derived validation behaves deterministically and does not treat future milestone work as current blockers. | The spec required `verify` and CI to block only on related stale artifacts, not on arbitrary local filesystem noise or future plan backlog. | Spec `R11`-`R13c`; architecture scope-mode contract; plan M3 | `validate-artifact-lifecycle.py --mode pr-ci ...`; `--mode push-main-ci ...`; `bash scripts/ci.sh` |
| Historical artifact migration and lifecycle closeout | [`specs/rigorloop-workflow.test.md`](../../specs/rigorloop-workflow.test.md), [`specs/constitution-governance-surface.test.md`](../../specs/constitution-governance-surface.test.md), [`specs/plan-index-lifecycle-ownership.test.md`](../../specs/plan-index-lifecycle-ownership.test.md), [`docs/plan.md`](../plan.md), [`2026-04-20-artifact-status-lifecycle-ownership.md`](../plans/2026-04-20-artifact-status-lifecycle-ownership.md) | Archived the relied-on historical test specs instead of leaving them at `complete`, then moved this initiative itself from `Active` to `Done` during verify once the outcome was already known on-branch. | The feature would have been self-contradictory if it shipped a validator but left the known stale artifacts or its own lifecycle state unresolved. | Spec `R15`-`R15b`; plan M4; verify findings | Final explicit-path validation, `bash scripts/ci.sh`, `docs/plan.md` section scan, per-slug uniqueness loop, and manual plan-body closeout review |

## Tests added or changed

This feature needed both executable validation tests and a tracked manual/structural test plan.

- [`artifact-status-lifecycle-ownership.test.md`](../../specs/artifact-status-lifecycle-ownership.test.md) maps `R1`-`R15b`, `E1`-`E6`, and `EC1`-`EC9` to 14 checks covering validator behavior, guidance alignment, CI wiring, and migration.
- [`test-artifact-lifecycle-validator.py`](../../scripts/test-artifact-lifecycle-validator.py) adds the executable proof for objective validator behavior:
  - valid and invalid status vocabularies by artifact class
  - missing sections and placeholder text
  - duplicate identifiers
  - generated-source boundary enforcement
  - related-scope expansion from `change.yaml`, explain-change, plans, and optional PR body
  - merge-base PR diffs and tracked-only diff-mode baselines
  - `Next artifacts`, `Follow-on artifacts`, and `superseded_by` rules
  - migrated historical test-spec closeout behavior
- [`tests/fixtures/artifact-lifecycle/`](../../tests/fixtures/artifact-lifecycle) holds the concrete repository shapes those tests exercise, including both valid baseline artifacts and intentionally stale or malformed examples.

This test level is appropriate because the feature changes repository workflow contracts and validator logic, not product runtime behavior. The right proof is a combination of fixture-driven validator tests and explicit checks over the actual authoritative artifacts and guidance surfaces.

## Verification evidence

Final verification was run against the branch state through `d9c7fc5`.

Commands run:

- `python scripts/test-artifact-lifecycle-validator.py`
  - pass
  - important output: 32 validator tests passed, including merge-base PR scope, tracked-only CI baselines, and active-plan scope filtering
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-20-artifact-status-lifecycle-ownership.md --path specs/artifact-status-lifecycle-ownership.md --path docs/architecture/2026-04-20-artifact-status-lifecycle-ownership.md --path specs/rigorloop-workflow.test.md --path specs/constitution-governance-surface.test.md --path specs/plan-index-lifecycle-ownership.test.md`
  - pass
  - important output: validated 6 artifact files in explicit-paths mode
- `python scripts/validate-skills.py`
  - pass
  - important output: validated 22 skill files
- `python scripts/build-skills.py --check`
  - pass
  - important output: generated skills are in sync
- `python scripts/validate-artifact-lifecycle.py --mode pr-ci --base "$(git rev-parse HEAD~1)" --head "$(git rev-parse HEAD)"`
  - pass with warnings only after the final M3 scope fix
- `python scripts/validate-artifact-lifecycle.py --mode push-main-ci --before "$(git rev-parse HEAD~1)" --after "$(git rev-parse HEAD)"`
  - pass with warnings only after the final M3 scope fix
- `rg -n '^## Status$|^- (draft|under review|accepted|rejected|abandoned|superseded|archived|approved|active|proposed|deprecated|reviewed|complete)$|^## (Next artifacts|Follow-on artifacts|Readiness)$|^superseded_by:' docs/proposals specs docs/architecture docs/adr`
  - pass
- `rg -n "^## (Active|Blocked|Done|Superseded)$" docs/plan.md`
  - pass
- per-slug uniqueness loop over `docs/plan.md` for the indexed plans
  - pass
- `bash scripts/ci.sh`
  - pass
  - important output: repo-owned validation passed, including skills validation, skill fixtures, generated-skill drift check, artifact lifecycle validator tests, and tracked-diff lifecycle validation
- `git diff --check -- docs/plan.md docs/plans/2026-04-20-artifact-status-lifecycle-ownership.md`
  - pass during verify closeout

Manual checks:

- reviewed the migrated historical test specs to confirm `archived` was used instead of inventing false replacement pointers;
- reviewed the completed plan body's `Status`, `Outcome and retrospective`, and `Readiness` text after verify closeout;
- confirmed `docs/plan.md` now lists the initiative under `Done` and leaves `## Active` empty.

Validation boundary:

- `python scripts/validate-artifact-lifecycle.py --mode local` was intentionally not used as milestone proof because the working tree contains two unrelated untracked proposal drafts, and the approved plan limited `local` mode to clean-worktree optional checks only.
- Hosted GitHub Actions CI was not observed from this environment, so this explanation does not claim remote CI passed.

## Alternatives rejected

- Docs-only lifecycle guidance without executable enforcement.
  - Rejected because the approved proposal and spec made executable validation part of the first enforcement step.
- A second central lifecycle registry.
  - Rejected because artifact-local status remains the source of truth and the approved architecture keeps one small executable contract registry rather than a second tracked state system.
- Git or PR state as the lifecycle source of truth.
  - Rejected because merge state cannot express `rejected`, `superseded`, `archived`, or "accepted but still current guidance" cleanly.
- Diff-mode validation from the live working tree.
  - Rejected during M3 review because it let unrelated untracked drafts leak into local CI-mode proofs in ways hosted CI would never reproduce.
- Treating all active-plan references as current related scope.
  - Rejected during M3 review because future milestone backlog and validation history are not current authoritative inputs for scope classification.
- Marking the historical test specs `superseded`.
  - Rejected in M4 because no direct replacement test specs were created; those files are historical evidence, not replaced authorities.

## Scope control

This feature intentionally did not:

- promote `docs/changes/*`, explain-change artifacts, or review-resolution artifacts into top-level authoritative lifecycle state;
- add network calls, GitHub API inspection, or draft-PR scraping to the validator;
- create a generalized Markdown schema framework;
- rewrite every historical proposal, spec, architecture doc, or ADR in the repository;
- redefine the already-approved plan lifecycle model beyond referencing it consistently from the broader artifact lifecycle contract;
- hand-edit generated `.codex/skills/` output outside the normal regeneration path.

## Risks and follow-ups

- Hosted CI remains unobserved from this environment.
- The local branch is still `main` ahead of `origin/main`; PR preparation is a separate stage after this explanation artifact.
- Two unrelated untracked proposal drafts remain in the working tree and must stay out of any PR based on this feature:
  - [`2026-04-20-docs-changes-usage-policy.md`](../proposals/2026-04-20-docs-changes-usage-policy.md)
  - [`2026-04-20-workflow-stage-handoff-clarity.md`](../proposals/2026-04-20-workflow-stage-handoff-clarity.md)
- Proposal and architecture lifecycle guidance still relies partly on skills and approved examples rather than dedicated per-class templates. That was an intentional scope choice here, but if the repository later wants stronger authoring consistency it may choose to add canonical proposal or architecture templates.

## PR-ready summary

- Added the full proposal/spec/test-spec/architecture/plan trail for artifact lifecycle ownership.
- Implemented a small artifact lifecycle validator, CLI, and fixture suite with deterministic scope handling for explicit, PR, and push validation modes.
- Aligned workflow docs, templates, canonical skills, and generated skills with the approved settlement-versus-closeout lifecycle model.
- Migrated the relied-on historical test specs from stale `complete` state to truthful `archived` closeout state.
- Closed the feature itself to `Done` during verify because the final outcome was already known on-branch.
