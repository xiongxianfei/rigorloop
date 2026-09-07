# Docs changes usage policy plan

- Status: done
- Owner: maintainer + Codex
- Start date: 2026-04-21
- Last updated: 2026-04-21
- Related issue or PR: closed PR #9; carried forward on branch `feat/docs-changes-skill-enforcement-v2`
- Supersedes: none

## Purpose / big picture

Implement the approved `docs/changes/` packaging contract as a small, reviewable guidance-and-validation change.

This initiative should make the repository's intended rule easy to apply:

- fast-lane work may omit `docs/changes/` when the approved fast-lane policy allows it;
- non-trivial work must carry `docs/changes/<change-id>/change.yaml` plus durable Markdown reasoning;
- `review-resolution.md` and `verify-report.md` remain conditional rather than universal;
- the shipped `0001-skill-validator` pack remains a rich reference example rather than the minimum required pack for every non-trivial change.

The implementation must stay inside the approved architecture boundary:

- no `change.yaml` schema redesign;
- no new registry, database, or orchestration state;
- no forced migration of legacy approved `docs/explain/*.md` artifacts;
- no weakening of the existing workflow contract.

## Source artifacts

- Proposal: `docs/proposals/2026-04-20-docs-changes-usage-policy.md`
- Spec: `specs/docs-changes-usage-policy.md`
- Spec-review findings carried into this plan:
  - new non-trivial work defaults to `docs/changes/<change-id>/explain-change.md`;
  - approved legacy top-level `docs/explain/*.md` artifacts remain valid until migrated or retired;
  - canonical snake_case `change.yaml` artifact keys and scalar string path values are part of the approved contract;
  - this feature clarifies workflow and packaging behavior without redesigning `change.yaml`.
- Architecture: `docs/architecture/2026-04-21-docs-changes-usage-policy.md`
- Architecture-review findings carried into this plan:
  - no new ADR is required;
  - validator tightening should stay in repo-owned scripts rather than a schema redesign;
  - the architecture artifact has already been normalized to `approved` before planning relies on it.
- Test spec: `specs/docs-changes-usage-policy.test.md`
- Related workflow and repository context:
  - `specs/rigorloop-workflow.md`
  - `specs/rigorloop-workflow.test.md`
  - `docs/architecture/2026-04-19-rigorloop-first-release-repository-architecture.md`
  - `docs/adr/ADR-20260419-repository-source-layout.md`
  - `schemas/change.schema.json`
  - `scripts/validate-change-metadata.py`
  - `docs/changes/0001-skill-validator/`
  - `README.md`

## Context and orientation

- The authoritative workflow contract already requires:
  - `docs/changes/<change-id>/change.yaml` for non-trivial work;
  - durable Markdown reasoning beyond `change.yaml`;
  - PR text as the reviewer-facing summary surface;
  - standalone `review-resolution.md` only when the workflow contract's durable review-memory triggers apply.
- `docs/changes/<change-id>/` is already the authored per-change memory home in the first-release architecture.
- `schemas/change.schema.json` and `scripts/validate-change-metadata.py` already enforce the current `change.yaml` structure:
  - `artifacts` is a flat mapping;
  - artifact values are scalar strings;
  - property names are not yet semantically constrained to the new canonical list.
- The existing top-level workflow test spec already covers `change.yaml`, the `0001-skill-validator` example, and the explain-change/review-resolution split, so workflow-contract wording changes must keep that proof surface coherent:
  - `specs/rigorloop-workflow.test.md`
- The shipped `docs/changes/0001-skill-validator/change.yaml` already demonstrates the intended snake_case artifact-key style:
  - `test_spec`
  - `verify_report`
  - `explain_change`
  - `review_resolution`
- `README.md` and the workflow summaries already mention `docs/changes/` and `0001-skill-validator/`, so contributor-facing wording drift matters beyond the governing spec alone.
- The accepted proposal, approved spec, approved architecture, and this plan currently exist only as local worktree artifacts. Downstream stages must not rely on them as authoritative repository state until they are tracked.
- The current branch is also carrying unrelated proposal-closeout work. This initiative should remain scoped to the docs-changes policy artifacts and should later move to its own review branch before PR preparation.

## Non-goals

- Redesign `schemas/change.schema.json` into nested artifact objects.
- Make `docs/changes/` optional for non-trivial work.
- Require every non-trivial change to match the full `0001-skill-validator` pack.
- Invalidate or mass-migrate approved legacy `docs/explain/*.md` artifacts as part of this feature.
- Reclassify fast-lane versus non-trivial work beyond the existing approved workflow contract.
- Turn `docs/changes/` into a second long-form source of truth that duplicates approved top-level proposal, spec, architecture, or plan artifacts.
- Pull unrelated local branch work into this initiative's future PR.

## Pre-implementation prerequisites

- Track the accepted proposal, approved spec, approved architecture, and this plan before `test-spec` or `implement` relies on them as authoritative repository state:
  - `docs/proposals/2026-04-20-docs-changes-usage-policy.md`
  - `specs/docs-changes-usage-policy.md`
  - `docs/architecture/2026-04-21-docs-changes-usage-policy.md`
  - `docs/plans/2026-04-21-docs-changes-usage-policy.md`
- Create `specs/docs-changes-usage-policy.test.md` after `plan-review` and before implementation.
- Keep this initiative out of the unrelated proposal-closeout branch/PR scope when later preparing a review branch.

## Requirements covered

| Requirement IDs | Planned implementation surface |
| --- | --- |
| `R1`-`R1b`, `R7`-`R8` | `specs/rigorloop-workflow.md`, `docs/workflows.md`, `AGENTS.md`, `CONSTITUTION.md`, `README.md` |
| `R2`-`R3f`, `R4`-`R6b` | `specs/rigorloop-workflow.md`, summary surfaces, `docs/changes/0001-skill-validator/`, and any minimal example wording needed to keep `0001` truthful as a rich example |
| `R9`-`R9c` | `scripts/validate-change-metadata.py`, `tests/fixtures/change-metadata/`, `docs/changes/0001-skill-validator/change.yaml`, and repo-owned fixture tests |
| Acceptance criteria and edge cases | future `specs/docs-changes-usage-policy.test.md`, targeted metadata-validation tests, manual review of contributor-facing guidance, and final repo-owned validation commands |

## Milestones

### M1. Align the normative workflow and contributor summary surfaces

- Goal:
  - Encode the approved docs-changes packaging rule in the workflow contract and the main contributor-facing summaries without weakening the existing behavior.
- Requirements:
  - `R1`-`R1b`, `R2`-`R8`
- Files/components likely touched:
  - `specs/rigorloop-workflow.md`
  - `specs/rigorloop-workflow.test.md`
  - `docs/workflows.md`
  - `AGENTS.md`
  - `CONSTITUTION.md`
  - `README.md`
- Dependencies:
  - approved spec
  - approved architecture
  - tracked-source-artifact prerequisite must be satisfied before downstream stages treat this milestone as authoritative repository state
- Tests to add/update:
  - review and update `specs/rigorloop-workflow.test.md` where existing workflow-proof cases cover:
    - `change.yaml` expectations for non-trivial work;
    - the explain-change and review-resolution split;
    - the `0001-skill-validator` example as a rich pack rather than a universal minimum.
  - the future feature test spec should cover:
    - fast-lane omission remaining allowed only under the approved fast-lane policy;
    - baseline non-trivial pack = `change.yaml` plus durable reasoning;
    - PR text alone not satisfying durable reasoning;
    - legacy `docs/explain/*.md` compatibility;
    - `0001-skill-validator/` remaining a rich example rather than the universal minimum pack;
    - cross-references to the updated workflow-test coverage where the governing workflow test spec already owns broader repository-contract proof.
- Implementation steps:
  - update `specs/rigorloop-workflow.md` so the packaging rule and artifact-role split are explicit in the normative contract;
  - review and update `specs/rigorloop-workflow.test.md` where the existing workflow proof surface would otherwise drift from the revised workflow contract;
  - update `docs/workflows.md`, `AGENTS.md`, and `CONSTITUTION.md` so they summarize the rule without competing with the workflow spec;
  - update `README.md` if needed so repository entrypoints do not imply that every non-trivial change must replicate the `0001` pack;
  - remove stale wording that treats `change.yaml` as sufficient on its own or treats `0001` as the minimum required pack.
- Validation commands:
  - `rg -n 'docs/changes|change.yaml|explain-change|review-resolution|verify-report|0001-skill-validator|docs/explain' specs/rigorloop-workflow.md specs/rigorloop-workflow.test.md docs/workflows.md AGENTS.md CONSTITUTION.md README.md`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/docs-changes-usage-policy.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/architecture/2026-04-21-docs-changes-usage-policy.md`
  - `git diff --check -- README.md CONSTITUTION.md AGENTS.md docs/workflows.md specs/rigorloop-workflow.md specs/rigorloop-workflow.test.md`
- Expected observable result:
  - contributors can find one consistent rule for baseline versus conditional docs-changes artifacts, and no summary surface weakens the workflow contract.
- Commit message: `M1: align docs-changes packaging guidance`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - summary surfaces may accidentally weaken or oversimplify the normative rule;
  - README may continue to imply the `0001` pack is universal if not aligned explicitly.
- Rollback/recovery:
  - revert the workflow and summary-surface edits together;
  - restore the prior wording while keeping the approved feature artifacts intact if a narrower rewrite is needed.

### M2. Enforce the `change.yaml` artifact-index contract in repo-owned validation

- Goal:
  - Make the approved canonical artifact-key and scalar-value-shape rules executable without redesigning the `change.yaml` schema.
- Requirements:
  - `R9`-`R9c`
- Files/components likely touched:
  - `scripts/validate-change-metadata.py`
  - `scripts/test-change-metadata-validator.py`
  - `tests/fixtures/change-metadata/`
  - `docs/changes/0001-skill-validator/change.yaml`
- Dependencies:
  - M1 should settle the contributor-facing rule first so executable checks enforce the same vocabulary
- Tests to add/update:
  - add repo-owned fixture coverage for:
    - valid canonical snake_case artifact keys;
    - invalid noncanonical artifact keys;
    - artifact-map scalar string values remaining valid;
    - the shipped `0001-skill-validator/change.yaml` remaining valid.
- Implementation steps:
  - add lightweight semantic checks in `scripts/validate-change-metadata.py` for canonical `artifacts` keys while preserving the existing schema-driven object/string shape;
  - add a dedicated fixture runner for change-metadata validation if one does not already exist;
  - add or update fixtures so failures are reviewable and deterministic;
  - keep `docs/changes/0001-skill-validator/change.yaml` truthful and passing under the tightened validator.
- Validation commands:
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/0001-skill-validator/change.yaml`
  - `git diff --check -- scripts/validate-change-metadata.py scripts/test-change-metadata-validator.py tests/fixtures/change-metadata docs/changes/0001-skill-validator/change.yaml`
- Expected observable result:
  - repo-owned validation rejects noncanonical artifact keys while continuing to accept the current scalar-path shape and the shipped `0001` example.
- Commit message: `M2: enforce docs-changes metadata contract`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - semantic checks may overconstrain artifact keys beyond the approved list;
  - validator changes may break the shipped `0001` example or the existing fixture shape unexpectedly.
- Rollback/recovery:
  - revert the validator, test runner, fixtures, and example `change.yaml` together;
  - keep the schema unchanged and fall back to documentation-only guidance if executable enforcement needs redesign.

### M3. Wire the new proof surface into repo-wide validation and finish example alignment

- Goal:
  - Ensure the new change-metadata proof surface participates in the repository's normal validation path and that the shipped example still reads as a rich example rather than a universal minimum pack.
- Requirements:
  - `R6b`, `R7a`-`R7b`, acceptance criteria
- Files/components likely touched:
  - `scripts/ci.sh`
  - `.github/workflows/ci.yml` only if wrapper inputs need adjustment
  - `README.md` and `docs/changes/0001-skill-validator/` if any example wording still drifts after M1 and M2
- Dependencies:
  - M2 should land first so there is a concrete repo-owned validator test runner to wire into CI
- Tests to add/update:
  - the future test spec should cover:
    - repo-wide validation including the change-metadata validator proof surface;
    - `0001-skill-validator/` remaining valid without implying every non-trivial change needs its full artifact set.
- Implementation steps:
  - add the new change-metadata validator fixture runner to `scripts/ci.sh`;
  - keep `.github/workflows/ci.yml` as a thin wrapper unless the CI wrapper contract itself changes;
  - update any remaining example wording in `README.md` or the `0001` pack if contributor entrypoints still imply the rich example is universal;
  - run the final repo-owned validation set for this initiative.
- Validation commands:
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/0001-skill-validator/change.yaml`
  - `bash scripts/ci.sh`
  - `git diff --check -- README.md scripts/ci.sh .github/workflows/ci.yml docs/changes/0001-skill-validator`
- Expected observable result:
  - the repository's standard CI wrapper exercises the new change-metadata proof surface, and contributor entrypoints no longer imply that the `0001` example is the mandatory minimum pack.
- Commit message: `M3: finish docs-changes usage policy proof`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - CI proof may remain incomplete if the new validator test runner is not wired into the repository wrapper;
  - example wording drift may survive in entrypoint docs even after the normative contract is fixed.
- Rollback/recovery:
  - revert the CI-wrapper and example-alignment changes together;
  - continue using direct validator commands as narrower proof while reworking repo-wide wiring.

## Validation plan

- Planning change validation:
  - `rg -n "^# Docs changes usage policy plan$|^## (Purpose / big picture|Source artifacts|Context and orientation|Non-goals|Pre-implementation prerequisites|Requirements covered|Milestones|Validation plan|Risks and recovery|Dependencies|Progress|Decision log|Surprises and discoveries|Validation notes|Outcome and retrospective|Readiness)$" docs/plans/2026-04-21-docs-changes-usage-policy.md`
  - `git diff --check -- docs/plan.md docs/plans/2026-04-21-docs-changes-usage-policy.md`
- Per-milestone validation is listed inside each milestone and should be copied into the later test spec.
- Final initiative validation should run:
  - the targeted change-metadata validator tests;
  - the shipped `0001` example validation;
  - `bash scripts/ci.sh`;
  - lifecycle validation over the proposal, spec, architecture, future test spec, and active plan before PR readiness.

## Risks and recovery

- Risk: contributor-facing summaries drift from the approved workflow contract.
  - Recovery: keep M1 ahead of validator work and rerun explicit artifact lifecycle validation on the governing feature artifacts after summary updates.
- Risk: key enforcement grows into an unapproved `change.yaml` schema redesign.
  - Recovery: keep semantic checks in `scripts/validate-change-metadata.py` and leave `schemas/change.schema.json` structurally unchanged.
- Risk: local-only proposal/spec/architecture/plan artifacts are mistaken for authoritative tracked state.
  - Recovery: keep tracked-source normalization as a hard prerequisite before `test-spec` or `implement`.
- Risk: the current unrelated branch/PR scope contaminates later review preparation.
  - Recovery: create a fresh feature branch for this initiative before `pr`.

## Dependencies

- The accepted proposal, approved spec, approved architecture, and this plan must be tracked before `test-spec` or `implement`.
- `plan-review` must approve this milestone split before implementation starts.
- `specs/docs-changes-usage-policy.test.md` must exist before `implement`.
- `scripts/validate-change-metadata.py` remains the existing enforcement seam; keep changes small and schema-compatible.
- `bash scripts/ci.sh` remains the repository-wide validation wrapper for final proof.

## Progress

- [x] 2026-04-21: architecture metadata normalized to `approved` before planning relied on it.
- [x] 2026-04-21: plan created and indexed under `Active` in `docs/plan.md`.
- [x] 2026-04-21: tracked-source prerequisite satisfied for proposal, spec, architecture, plan, and test spec before downstream implementation reliance.
- [x] 2026-04-21: `specs/docs-changes-usage-policy.test.md` created as the active proof-planning surface for implementation.
- [x] 2026-04-21: M1 aligned the workflow contract, existing workflow proof surface, contributor summaries, and README to the approved baseline-versus-conditional docs-changes rule.
- [x] M1 completed.
- [x] 2026-04-21: M2 added repo-owned metadata fixture tests, negative fixtures for invalid artifact keys and value shapes, and canonical artifact-key enforcement in `scripts/validate-change-metadata.py` without changing the schema shape.
- [x] M2 completed.
- [x] 2026-04-21: M3 wired the change-metadata fixture runner into `scripts/ci.sh` and confirmed the repo-wide CI wrapper now exercises the new proof surface while `.github/workflows/ci.yml` stays a thin delegate.
- [x] M3 completed.
- [x] 2026-04-21: `explain-change` captured the implementation rationale at `docs/explain/2026-04-21-docs-changes-usage-policy.md` and moved the active plan/test-spec readiness to the `pr` gate.

## Decision log

- 2026-04-21: split implementation into workflow/summaries first, validator/fixtures second, and repo-wide proof/example alignment last. Reason: this keeps the highest-risk contract wording settled before executable enforcement and CI wiring.
- 2026-04-21: keep canonical artifact-key enforcement in `scripts/validate-change-metadata.py` rather than redesigning `schemas/change.schema.json`. Reason: the approved architecture explicitly preserves the existing scalar-path schema shape.
- 2026-04-21: treat tracked-source normalization as a hard prerequisite before `test-spec` or `implement`. Reason: the accepted proposal, approved spec, approved architecture, and this plan currently exist only as local worktree artifacts.
- 2026-04-21: make the workflow contract and summary surfaces state the ordinary baseline pack separately from the `0001-skill-validator/` example. Reason: M1 needed to stop contributors from treating the shipped rich example as the universal minimum pack for non-trivial work.
- 2026-04-21: enforce the approved `artifacts` contract through an allowlist of canonical snake_case keys instead of regex-only naming checks. Reason: the approved spec names the canonical key set directly, and rejecting unknown keys keeps the validator aligned with that contract.
- 2026-04-21: keep `.github/workflows/ci.yml` unchanged in M3. Reason: it already satisfied the approved thin-wrapper boundary by delegating validation logic to `bash scripts/ci.sh`.

## Surprises and discoveries

- 2026-04-21: the existing archived `specs/rigorloop-workflow.test.md` still owns the main proof surface for `change.yaml`, explain-change, and `0001` behavior, so M1 required workflow-test alignment rather than only editing summary docs.
- 2026-04-21: the pre-M2 metadata validator already enforced scalar string artifact values through schema validation, but it silently accepted noncanonical artifact keys until the semantic allowlist check was added.
- 2026-04-21: after M1 wording alignment, no additional README or `docs/changes/0001-skill-validator/` edits were needed in M3; the only remaining gap was the missing CI-wrapper hook for the new metadata fixture runner.

## Validation notes

- 2026-04-21: plan created and indexed under `Active` in `docs/plan.md`.
- 2026-04-21: created `specs/docs-changes-usage-policy.test.md` and moved the proposal, spec, architecture, plan, and test spec into tracked git state for downstream reliance.
- 2026-04-21: M1 validation passed.
  - `rg -n -- 'docs/changes|change\.yaml|explain-change|review-resolution|verify-report|0001-skill-validator|docs/explain' specs/rigorloop-workflow.md specs/rigorloop-workflow.test.md docs/workflows.md AGENTS.md CONSTITUTION.md README.md`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/docs-changes-usage-policy.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/architecture/2026-04-21-docs-changes-usage-policy.md`
  - `git diff --check -- README.md CONSTITUTION.md AGENTS.md docs/workflows.md specs/rigorloop-workflow.md specs/rigorloop-workflow.test.md`
  - Result: all passed.
- 2026-04-21: M2 fail-first proof confirmed the gap before the semantic check landed.
  - Copied the pre-M2 `scripts/validate-change-metadata.py` from `HEAD` into a temporary script under `scripts/` and ran it against `tests/fixtures/change-metadata/bad-artifact-key/change.yaml`.
  - Result: the pre-M2 validator incorrectly reported the invalid artifact key fixture as valid.
- 2026-04-21: M2 validation passed.
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/0001-skill-validator/change.yaml`
  - `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/bad-artifact-key/change.yaml`
  - `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/bad-artifact-value-shape/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-04-21-docs-changes-usage-policy.md --path specs/docs-changes-usage-policy.test.md`
  - `git diff --check -- scripts/validate-change-metadata.py specs/docs-changes-usage-policy.test.md docs/plans/2026-04-21-docs-changes-usage-policy.md`
  - Result: all passed, and the invalid fixtures now fail with contributor-actionable messages.
- 2026-04-21: M3 fail-first proof confirmed the repo-wide wrapper gap before wiring landed.
  - Ran `bash scripts/ci.sh` and captured its output before editing `scripts/ci.sh`.
  - Result: the wrapper passed, but it did not invoke `python scripts/test-change-metadata-validator.py` yet.
- 2026-04-21: M3 validation passed.
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/0001-skill-validator/change.yaml`
  - `bash scripts/ci.sh`
  - `git diff --check -- README.md scripts/ci.sh .github/workflows/ci.yml docs/changes/0001-skill-validator`
  - Result: all passed, and the standard CI wrapper now exercises the change-metadata proof surface.
- 2026-04-21: M3 code-review rerun passed.
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/0001-skill-validator/change.yaml`
  - `bash scripts/ci.sh`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-04-21-docs-changes-usage-policy.md --path specs/docs-changes-usage-policy.test.md`
  - `git diff --check 9c1994b^..9c1994b -- README.md scripts/ci.sh .github/workflows/ci.yml docs/changes/0001-skill-validator docs/plans/2026-04-21-docs-changes-usage-policy.md`
  - Result: approve, no findings.
- 2026-04-21: verify passed on the completed M1-M3 implementation range.
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/0001-skill-validator/change.yaml`
  - `bash scripts/ci.sh`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-20-docs-changes-usage-policy.md --path specs/docs-changes-usage-policy.md --path docs/architecture/2026-04-21-docs-changes-usage-policy.md --path docs/plans/2026-04-21-docs-changes-usage-policy.md --path specs/docs-changes-usage-policy.test.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md`
  - `git diff --check -- docs/plans/2026-04-21-docs-changes-usage-policy.md specs/docs-changes-usage-policy.test.md`
  - Result: pass, with only unrelated warning-level baseline artifact debt from historical proposal files during diff-derived lifecycle validation.
- 2026-04-21: explain-change completed.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-04-21-docs-changes-usage-policy.md --path specs/docs-changes-usage-policy.test.md`
  - `git diff --check -- docs/explain/2026-04-21-docs-changes-usage-policy.md docs/plans/2026-04-21-docs-changes-usage-policy.md specs/docs-changes-usage-policy.test.md`
  - Result: passed.

## Outcome and retrospective

- This plan is done on-branch and now belongs in `docs/plan.md` under `Done`.
- What changed: the feature clarified the repository rule for baseline versus conditional `docs/changes/` artifacts, aligned the governing workflow/test surfaces and summaries, added canonical `change.yaml` artifact-key enforcement plus negative fixtures, and wired the metadata fixture runner into `bash scripts/ci.sh`.
- What went well: splitting the work into guidance alignment, validator enforcement, and repo-wide proof kept the reviews narrow and made it easy to isolate real contract drift from feature work.
- What was harder than expected: lifecycle-managed artifacts still needed explicit post-review and post-verify readiness normalization even after the milestone implementation work was complete.
- Spec accuracy: the approved spec held through implementation once the durable-reasoning default, legacy `docs/explain/` compatibility, and canonical artifact-key contract were made explicit. The most important constraint was clarifying the workflow contract without weakening it.
- Test effectiveness: the dedicated change-metadata fixture runner and negative fixtures were the highest-value executable proof because they turned the new artifact-key contract into a small, deterministic validator seam, while manual workflow/test-spec review remained the right proof level for the guidance surfaces.
- Architecture accuracy: the approved small design held. The feature never needed a schema redesign, second registry, or new storage model; the validator seam plus existing workflow surfaces were sufficient.
- Process issues: pre-PR lifecycle closeout still matters for completed planned work. `docs/plan.md` and the plan body both needed an explicit transition to `Done` before the PR stage so review would not inherit stale active-state bookkeeping.
- Follow-up actions: open a replacement PR from `feat/docs-changes-skill-enforcement-v2` once the combined domain work is ready, then do only normal review and merge follow-up there.

## Readiness

- This plan is done on-branch.
- The tracked-source prerequisite and active test spec are in place.
- M1 through M3 are complete.
- `code-review`, `verify`, and `explain-change` are complete.
- The next expected state change is a replacement PR from `feat/docs-changes-skill-enforcement-v2` or later merge follow-up there, not more implementation on this completed initiative.

## Historical closeout rationale

Retained from `docs/explain/2026-04-21-docs-changes-usage-policy.md` when the legacy explanation directory was retired during the 2026-09-07 repository cleanup. The quoted text preserves the original account, commands and paths; it is historical evidence, not current plan state or a fresh verification result. New work uses the owning change’s contract-selected Verify report.

> # Docs Changes Usage Policy rationale
>
> ## Summary
>
> This explanation covers the docs-changes usage policy feature stack from `443f217` through `174ae58`.
>
> The change turns an implicit repository habit into an explicit contract: non-trivial work must carry `docs/changes/<change-id>/change.yaml` plus durable Markdown reasoning, `review-resolution.md` and `verify-report.md` remain conditional, the shipped `0001-skill-validator` pack stays a rich example rather than a universal minimum, and the `change.yaml` artifact index now has executable canonical-key enforcement. It also wires that proof surface into the normal repo-owned CI wrapper and keeps the active plan and test spec truthful through verify.
>
> ## Problem
>
> The repository already had most of the pieces for per-change traceability, but contributors still had to infer the practical packaging rule from scattered sources:
>
> - the workflow contract already required `change.yaml` for non-trivial work;
> - durable reasoning already had to exist beyond PR text alone;
> - `docs/changes/0001-skill-validator/` showed a rich pack, but not the minimum pack;
> - the metadata schema enforced structural shape, but not the new canonical artifact-key vocabulary.
>
> That left two common failure modes:
>
> - under-specifying non-trivial work by treating `change.yaml` as sufficient or by relying on PR text alone for durable reasoning;
> - over-specifying ordinary work by cargo-culting the full `0001` pack, including standalone `verify-report.md` or `review-resolution.md`, even when their triggers did not apply.
>
> ## Decision trail
>
> | Artifact | Decision carried into the change | How it shaped the diff |
> | --- | --- | --- |
> | [`2026-04-20-docs-changes-usage-policy.md`](../proposals/2026-04-20-docs-changes-usage-policy.md) | Clarify the existing contract rather than weaken it; keep `change.yaml` plus durable reasoning for non-trivial work; make `verify-report.md` conditional through objective triggers. | The implementation updates workflow/governance docs first, then adds small validator checks that enforce the approved key contract without redesigning `change.yaml`. |
> | [`docs-changes-usage-policy.md`](../../specs/docs-changes-usage-policy.md) | Make `docs/changes/<change-id>/explain-change.md` the default durable reasoning surface for new work, preserve legacy approved `docs/explain/*.md`, define canonical snake_case artifact keys, and keep scalar path values. | The diff adds the feature spec/test-spec trail, updates the governing workflow contract, and adds semantic validation on top of the existing schema. |
> | [`docs-changes-usage-policy.test.md`](../../specs/docs-changes-usage-policy.test.md) | Use three proof layers: manual workflow/guidance review, integration checks for metadata validation, and smoke coverage through `bash scripts/ci.sh`. | The change adds a dedicated metadata fixture runner, negative fixtures, and one CI-wrapper hook rather than a new subsystem. |
> | [`2026-04-21-docs-changes-usage-policy.md`](../architecture/2026-04-21-docs-changes-usage-policy.md) | Keep the design small: workflow spec remains normative, `docs/changes/` remains the default home for new change packs, legacy `docs/explain/` remains valid, and any enforcement lives in repo-owned validator logic. | The implementation leaves `schemas/change.schema.json` structurally unchanged and puts the new key checks in [`scripts/validate-change-metadata.py`](../../scripts/validate-change-metadata.py). |
> | [`2026-04-21-docs-changes-usage-policy.md`](../plans/2026-04-21-docs-changes-usage-policy.md) | Split the work into guidance alignment, validator/fixture enforcement, and repo-wide proof wiring. | The branch lands as M1 (`443f217`), M2 (`e3269ba`), M3 (`9c1994b`), then readiness syncs for post-code-review (`7267471`) and post-verify (`174ae58`). |
>
> ## Milestone map
>
> | Milestone or stage | Commits | Outcome |
> | --- | --- | --- |
> | M1 | `443f217` | Added the proposal/spec/architecture/plan/test-spec trail, updated the governing workflow contract and its existing workflow proof surface, and aligned repository summaries so they describe the baseline-versus-conditional docs-changes rule consistently. |
> | M2 | `e3269ba` | Added canonical artifact-key enforcement in the metadata validator, a dedicated fixture runner, and negative fixtures for invalid artifact keys and invalid nested artifact values. |
> | M3 | `9c1994b` | Wired the new metadata fixture runner into `bash scripts/ci.sh` so the normal repo-owned proof path exercises the feature. |
> | Post-review / verify lifecycle sync | `7267471`, `174ae58` | Normalized the active plan and test spec after review and verify so the touched lifecycle-managed artifacts no longer advertised stale downstream stages. |
>
> ## Diff rationale by area
>
> | Area | Files | Change | Reason | Source artifact | Test or evidence |
> | --- | --- | --- | --- | --- | --- |
> | Durable feature artifacts | [`2026-04-20-docs-changes-usage-policy.md`](../proposals/2026-04-20-docs-changes-usage-policy.md), [`docs-changes-usage-policy.md`](../../specs/docs-changes-usage-policy.md), [`docs-changes-usage-policy.test.md`](../../specs/docs-changes-usage-policy.test.md), [`2026-04-21-docs-changes-usage-policy.md`](../architecture/2026-04-21-docs-changes-usage-policy.md), [`2026-04-21-docs-changes-usage-policy.md`](../plans/2026-04-21-docs-changes-usage-policy.md), [`docs/plan.md`](../plan.md) | Added the full proposal/spec/test-spec/architecture/plan trail and tracked the initiative under `Active` so the policy, proof strategy, and execution history are durable instead of chat-only. | This feature changes repository contract and validation behavior; it needed tracked source artifacts before implementation could safely rely on it. | Proposal, spec, architecture, test spec, plan | M1 commit `443f217`; lifecycle validation over the feature artifacts during verify |
> | Workflow contract and existing proof surface | [`specs/rigorloop-workflow.md`](../../specs/rigorloop-workflow.md), [`specs/rigorloop-workflow.test.md`](../../specs/rigorloop-workflow.test.md) | Made the baseline pack explicit for ordinary non-trivial work, kept `review-resolution.md` and `verify-report.md` conditional, preserved legacy `docs/explain/` compatibility, and rewrote the existing workflow proof surface so it matches the new packaging rule. | The approved spec made `specs/rigorloop-workflow.md` the normative home, and the existing workflow test spec already owned overlapping proof for `change.yaml`, `0001`, and explain/review memory behavior. | Spec `R1`-`R8`; plan M1 | Manual workflow-surface review; explicit-path lifecycle validation during M1 and verify |
> | Contributor and governance summaries | [`docs/workflows.md`](../workflows.md), [`README.md`](../../README.md), [`AGENTS.md`](../../AGENTS.md), [`CONSTITUTION.md`](../../CONSTITUTION.md) | Summarized the same rule-of-thumb: fast-lane omission stays narrow, `change.yaml` alone is not enough for non-trivial work, and `0001` is a rich example rather than the minimum pack. | The workflow spec is normative, but the summaries are where contributors and agents tend to look first; they had to reinforce the contract instead of competing with it. | Spec `R1a`, `R1b`, `R7`, `R8`; architecture source-of-truth boundary | M1 grep-based wording checks recorded in the plan |
> | Metadata validator and fixtures | [`scripts/validate-change-metadata.py`](../../scripts/validate-change-metadata.py), [`scripts/test-change-metadata-validator.py`](../../scripts/test-change-metadata-validator.py), [`tests/fixtures/change-metadata/bad-artifact-key/change.yaml`](../../tests/fixtures/change-metadata/bad-artifact-key/change.yaml), [`tests/fixtures/change-metadata/bad-artifact-value-shape/change.yaml`](../../tests/fixtures/change-metadata/bad-artifact-value-shape/change.yaml) | Added a canonical-key allowlist (`explain_change`, `review_resolution`, `verify_report`, etc.) as a semantic post-schema check, plus a fixture-driven test runner and targeted invalid fixtures. | The schema already preserved the scalar string value shape; the missing executable contract was the approved artifact-key vocabulary. The architecture explicitly said to tighten semantics in repo-owned validator logic, not by redesigning the schema. | Spec `R9`-`R9c`; architecture validator-boundary rule; plan M2 | `python scripts/test-change-metadata-validator.py`; direct validator runs against valid and invalid fixtures |
> | Repo-owned CI wrapper | [`scripts/ci.sh`](../../scripts/ci.sh) | Added `python scripts/test-change-metadata-validator.py` to the standard repo-owned CI wrapper. | M3's goal was to ensure the new proof surface participates in the normal validation path instead of living only as an optional local command. | Test spec `T8`; plan M3 | `bash scripts/ci.sh` after `9c1994b` |
> | Shipped compatibility example | [`docs/changes/0001-skill-validator/change.yaml`](../changes/0001-skill-validator/change.yaml), [`README.md`](../../README.md), [`specs/rigorloop-workflow.test.md`](../../specs/rigorloop-workflow.test.md) | Kept the shipped `0001` pack valid and explicitly repositioned it as a rich reference example, not a universal minimum. | The feature should tighten the baseline contract without forcing every non-trivial change to carry standalone review-memory or verification artifacts. | Spec `R6b`, `R7a`, `R7b`; proposal rationale | `python scripts/validate-change-metadata.py docs/changes/0001-skill-validator/change.yaml`; manual review of contributor wording |
> | Lifecycle bookkeeping after review and verify | [`2026-04-21-docs-changes-usage-policy.md`](../plans/2026-04-21-docs-changes-usage-policy.md), [`docs-changes-usage-policy.test.md`](../../specs/docs-changes-usage-policy.test.md) | Synced the active plan and test spec after code review and verify so they stopped advertising stale next-stage text. | This repository treats active lifecycle-managed artifacts as current execution state. Once review and verify completed, those surfaces needed to reflect that settled state before downstream stages relied on them. | Verify-stage lifecycle rules in `AGENTS.md` and `CONSTITUTION.md`; plan/test-spec lifecycle expectations | `174ae58`; explicit-path lifecycle validation over the active plan and test spec after the sync |
>
> ## Tests added or changed
>
> - [`docs-changes-usage-policy.test.md`](../../specs/docs-changes-usage-policy.test.md) was added as the tracked feature test spec. It maps:
>   - `R1`-`R8` into manual contract review across the workflow spec, workflow test spec, summaries, `0001`, and legacy `docs/explain/` artifacts;
>   - `R9`-`R9c` into executable validator checks;
>   - smoke proof into `bash scripts/ci.sh`.
> - [`specs/rigorloop-workflow.test.md`](../../specs/rigorloop-workflow.test.md) was updated because the docs-changes rule changes behavior already covered by the repository-level workflow proof surface.
> - [`scripts/test-change-metadata-validator.py`](../../scripts/test-change-metadata-validator.py) was added as the dedicated fixture runner for the metadata contract.
> - The negative fixtures added in M2 prove the important failure cases:
>   - noncanonical artifact keys fail with actionable errors;
>   - nested artifact-map values fail because the value shape must remain a plain scalar path string.
>
> That test level is appropriate because the feature is mostly contract and validation alignment. The new runtime-like behavior lives in one validator seam, so a focused fixture runner plus repo-wide smoke proof covers the real risk without inventing a larger harness.
>
> ## Verification evidence
>
> Final implementation verification was run against the feature stack through `174ae58`.
>
> Commands run:
>
> - `python scripts/test-change-metadata-validator.py`
>   - pass
>   - important evidence: the valid fixture and shipped `0001` example pass, and the invalid key/value-shape fixtures fail for the intended reasons
> - `python scripts/validate-change-metadata.py docs/changes/0001-skill-validator/change.yaml`
>   - pass
> - `bash scripts/ci.sh`
>   - pass
>   - important evidence: the normal repo-owned wrapper now runs the metadata fixture surface in addition to the existing skill and lifecycle checks
> - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-20-docs-changes-usage-policy.md --path specs/docs-changes-usage-policy.md --path docs/architecture/2026-04-21-docs-changes-usage-policy.md --path docs/plans/2026-04-21-docs-changes-usage-policy.md --path specs/docs-changes-usage-policy.test.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md`
>   - pass
>   - important evidence: `validated 8 artifact files in explicit-paths mode`
> - `git diff --check -- docs/plans/2026-04-21-docs-changes-usage-policy.md specs/docs-changes-usage-policy.test.md`
>   - pass during verify lifecycle sync
>
> Explain-change stage closeout checks for this artifact and the post-explanation lifecycle sync:
>
> - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-04-21-docs-changes-usage-policy.md --path specs/docs-changes-usage-policy.test.md`
> - `git diff --check -- docs/explain/2026-04-21-docs-changes-usage-policy.md docs/plans/2026-04-21-docs-changes-usage-policy.md specs/docs-changes-usage-policy.test.md`
>
> Validation boundary:
>
> - Hosted GitHub Actions CI is still unobserved from this environment, so this explanation does not claim hosted CI passed.
> - No PR body exists yet. The `pr` stage is still outstanding.
>
> ## Alternatives rejected
>
> - Redesigning `change.yaml` into nested artifact objects.
>   - Rejected because the approved architecture keeps the existing scalar-path schema shape and limits enforcement to lightweight validator logic.
> - Making `docs/changes/` optional for ordinary non-trivial work.
>   - Rejected because the proposal and spec were explicitly framed as clarification of the approved contract, not a relaxation.
> - Treating the full `0001-skill-validator` pack as the universal minimum.
>   - Rejected because ordinary non-trivial work only needs the baseline pack plus conditional artifacts whose triggers actually apply.
> - Forcing migration of approved legacy `docs/explain/*.md` artifacts.
>   - Rejected because the approved compatibility rule preserves them until they are migrated, superseded, archived, or otherwise retired.
> - Expanding M3 into direct `.github/workflows/ci.yml` logic.
>   - Rejected because the workflow already satisfied the thin-wrapper contract; the right change was to update [`scripts/ci.sh`](../../scripts/ci.sh), not duplicate logic in GitHub Actions YAML.
>
> ## Scope control
>
> This feature intentionally did not:
>
> - redesign `schemas/change.schema.json`;
> - require every non-trivial change to replicate the `0001` artifact pack;
> - weaken the existing workflow contract around non-trivial change traceability;
> - invalidate or mass-migrate approved legacy `docs/explain/*.md` artifacts;
> - promote `docs/changes/` into a second long-form source of truth for proposal/spec/architecture/plan content;
> - add network-dependent CI logic or claim hosted CI coverage from local verification.
>
> ## Risks and follow-ups
>
> - Hosted CI is still unknown from this environment.
> - The current branch is still `chore/close-workflow-handoff-proposal`, and the plan explicitly kept this feature out of that unrelated proposal-closeout review scope. The `pr` stage should move the verified tip onto a dedicated review branch or otherwise ensure the PR scope is clean.
> - The feature is ready for PR preparation, but PR creation itself still needs the normal branch/base/readiness checks.
>
> ## PR-ready summary
>
> - Added the full proposal/spec/test-spec/architecture/plan trail for the docs-changes usage policy feature.
> - Updated the governing workflow contract and repository summaries so non-trivial work clearly requires `change.yaml` plus durable reasoning, while `review-resolution.md` and `verify-report.md` stay conditional.
> - Added canonical `change.yaml` artifact-key enforcement, a dedicated metadata fixture runner, and targeted invalid fixtures without redesigning the schema.
> - Wired the metadata fixture runner into `bash scripts/ci.sh` so the normal repo-owned proof path covers the feature.
> - Synced the active plan and test spec through review and verify so the lifecycle-managed artifacts stayed truthful before PR preparation.
