# Docs changes usage policy plan

- Status: active
- Owner: maintainer + Codex
- Start date: 2026-04-21
- Last updated: 2026-04-21
- Related issue or PR: none yet
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
  - [ ] targeted validation passed
  - [ ] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] milestone committed
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
  - [ ] targeted validation passed
  - [ ] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] milestone committed
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
- [ ] M2 completed.
- [ ] M3 completed.

## Decision log

- 2026-04-21: split implementation into workflow/summaries first, validator/fixtures second, and repo-wide proof/example alignment last. Reason: this keeps the highest-risk contract wording settled before executable enforcement and CI wiring.
- 2026-04-21: keep canonical artifact-key enforcement in `scripts/validate-change-metadata.py` rather than redesigning `schemas/change.schema.json`. Reason: the approved architecture explicitly preserves the existing scalar-path schema shape.
- 2026-04-21: treat tracked-source normalization as a hard prerequisite before `test-spec` or `implement`. Reason: the accepted proposal, approved spec, approved architecture, and this plan currently exist only as local worktree artifacts.
- 2026-04-21: make the workflow contract and summary surfaces state the ordinary baseline pack separately from the `0001-skill-validator/` example. Reason: M1 needed to stop contributors from treating the shipped rich example as the universal minimum pack for non-trivial work.

## Surprises and discoveries

- 2026-04-21: the existing archived `specs/rigorloop-workflow.test.md` still owns the main proof surface for `change.yaml`, explain-change, and `0001` behavior, so M1 required workflow-test alignment rather than only editing summary docs.

## Validation notes

- 2026-04-21: plan created and indexed under `Active` in `docs/plan.md`.
- 2026-04-21: created `specs/docs-changes-usage-policy.test.md` and moved the proposal, spec, architecture, plan, and test spec into tracked git state for downstream reliance.
- 2026-04-21: M1 validation passed.
  - `rg -n -- 'docs/changes|change\.yaml|explain-change|review-resolution|verify-report|0001-skill-validator|docs/explain' specs/rigorloop-workflow.md specs/rigorloop-workflow.test.md docs/workflows.md AGENTS.md CONSTITUTION.md README.md`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/docs-changes-usage-policy.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/architecture/2026-04-21-docs-changes-usage-policy.md`
  - `git diff --check -- README.md CONSTITUTION.md AGENTS.md docs/workflows.md specs/rigorloop-workflow.md specs/rigorloop-workflow.test.md`
  - Result: all passed.

## Outcome and retrospective

- This initiative is active. Use this section for completion, blockage, supersession, or retrospective notes once the real lifecycle outcome is known.

## Readiness

- `specs/docs-changes-usage-policy.test.md` is now the active proof-planning surface.
- The tracked-source prerequisite is satisfied for the accepted proposal, approved spec, approved architecture, active plan, and active test spec.
- M1 is complete and the initiative remains active for M2 and M3.
- The next stage is `code-review`.
