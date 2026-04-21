# Docs Changes Usage Policy rationale

## Summary

This explanation covers the docs-changes usage policy feature stack from `443f217` through `174ae58`.

The change turns an implicit repository habit into an explicit contract: non-trivial work must carry `docs/changes/<change-id>/change.yaml` plus durable Markdown reasoning, `review-resolution.md` and `verify-report.md` remain conditional, the shipped `0001-skill-validator` pack stays a rich example rather than a universal minimum, and the `change.yaml` artifact index now has executable canonical-key enforcement. It also wires that proof surface into the normal repo-owned CI wrapper and keeps the active plan and test spec truthful through verify.

## Problem

The repository already had most of the pieces for per-change traceability, but contributors still had to infer the practical packaging rule from scattered sources:

- the workflow contract already required `change.yaml` for non-trivial work;
- durable reasoning already had to exist beyond PR text alone;
- `docs/changes/0001-skill-validator/` showed a rich pack, but not the minimum pack;
- the metadata schema enforced structural shape, but not the new canonical artifact-key vocabulary.

That left two common failure modes:

- under-specifying non-trivial work by treating `change.yaml` as sufficient or by relying on PR text alone for durable reasoning;
- over-specifying ordinary work by cargo-culting the full `0001` pack, including standalone `verify-report.md` or `review-resolution.md`, even when their triggers did not apply.

## Decision trail

| Artifact | Decision carried into the change | How it shaped the diff |
| --- | --- | --- |
| [`2026-04-20-docs-changes-usage-policy.md`](../proposals/2026-04-20-docs-changes-usage-policy.md) | Clarify the existing contract rather than weaken it; keep `change.yaml` plus durable reasoning for non-trivial work; make `verify-report.md` conditional through objective triggers. | The implementation updates workflow/governance docs first, then adds small validator checks that enforce the approved key contract without redesigning `change.yaml`. |
| [`docs-changes-usage-policy.md`](../../specs/docs-changes-usage-policy.md) | Make `docs/changes/<change-id>/explain-change.md` the default durable reasoning surface for new work, preserve legacy approved `docs/explain/*.md`, define canonical snake_case artifact keys, and keep scalar path values. | The diff adds the feature spec/test-spec trail, updates the governing workflow contract, and adds semantic validation on top of the existing schema. |
| [`docs-changes-usage-policy.test.md`](../../specs/docs-changes-usage-policy.test.md) | Use three proof layers: manual workflow/guidance review, integration checks for metadata validation, and smoke coverage through `bash scripts/ci.sh`. | The change adds a dedicated metadata fixture runner, negative fixtures, and one CI-wrapper hook rather than a new subsystem. |
| [`2026-04-21-docs-changes-usage-policy.md`](../architecture/2026-04-21-docs-changes-usage-policy.md) | Keep the design small: workflow spec remains normative, `docs/changes/` remains the default home for new change packs, legacy `docs/explain/` remains valid, and any enforcement lives in repo-owned validator logic. | The implementation leaves `schemas/change.schema.json` structurally unchanged and puts the new key checks in [`scripts/validate-change-metadata.py`](../../scripts/validate-change-metadata.py). |
| [`2026-04-21-docs-changes-usage-policy.md`](../plans/2026-04-21-docs-changes-usage-policy.md) | Split the work into guidance alignment, validator/fixture enforcement, and repo-wide proof wiring. | The branch lands as M1 (`443f217`), M2 (`e3269ba`), M3 (`9c1994b`), then readiness syncs for post-code-review (`7267471`) and post-verify (`174ae58`). |

## Milestone map

| Milestone or stage | Commits | Outcome |
| --- | --- | --- |
| M1 | `443f217` | Added the proposal/spec/architecture/plan/test-spec trail, updated the governing workflow contract and its existing workflow proof surface, and aligned repository summaries so they describe the baseline-versus-conditional docs-changes rule consistently. |
| M2 | `e3269ba` | Added canonical artifact-key enforcement in the metadata validator, a dedicated fixture runner, and negative fixtures for invalid artifact keys and invalid nested artifact values. |
| M3 | `9c1994b` | Wired the new metadata fixture runner into `bash scripts/ci.sh` so the normal repo-owned proof path exercises the feature. |
| Post-review / verify lifecycle sync | `7267471`, `174ae58` | Normalized the active plan and test spec after review and verify so the touched lifecycle-managed artifacts no longer advertised stale downstream stages. |

## Diff rationale by area

| Area | Files | Change | Reason | Source artifact | Test or evidence |
| --- | --- | --- | --- | --- | --- |
| Durable feature artifacts | [`2026-04-20-docs-changes-usage-policy.md`](../proposals/2026-04-20-docs-changes-usage-policy.md), [`docs-changes-usage-policy.md`](../../specs/docs-changes-usage-policy.md), [`docs-changes-usage-policy.test.md`](../../specs/docs-changes-usage-policy.test.md), [`2026-04-21-docs-changes-usage-policy.md`](../architecture/2026-04-21-docs-changes-usage-policy.md), [`2026-04-21-docs-changes-usage-policy.md`](../plans/2026-04-21-docs-changes-usage-policy.md), [`docs/plan.md`](../plan.md) | Added the full proposal/spec/test-spec/architecture/plan trail and tracked the initiative under `Active` so the policy, proof strategy, and execution history are durable instead of chat-only. | This feature changes repository contract and validation behavior; it needed tracked source artifacts before implementation could safely rely on it. | Proposal, spec, architecture, test spec, plan | M1 commit `443f217`; lifecycle validation over the feature artifacts during verify |
| Workflow contract and existing proof surface | [`specs/rigorloop-workflow.md`](../../specs/rigorloop-workflow.md), [`specs/rigorloop-workflow.test.md`](../../specs/rigorloop-workflow.test.md) | Made the baseline pack explicit for ordinary non-trivial work, kept `review-resolution.md` and `verify-report.md` conditional, preserved legacy `docs/explain/` compatibility, and rewrote the existing workflow proof surface so it matches the new packaging rule. | The approved spec made `specs/rigorloop-workflow.md` the normative home, and the existing workflow test spec already owned overlapping proof for `change.yaml`, `0001`, and explain/review memory behavior. | Spec `R1`-`R8`; plan M1 | Manual workflow-surface review; explicit-path lifecycle validation during M1 and verify |
| Contributor and governance summaries | [`docs/workflows.md`](../workflows.md), [`README.md`](../../README.md), [`AGENTS.md`](../../AGENTS.md), [`CONSTITUTION.md`](../../CONSTITUTION.md) | Summarized the same rule-of-thumb: fast-lane omission stays narrow, `change.yaml` alone is not enough for non-trivial work, and `0001` is a rich example rather than the minimum pack. | The workflow spec is normative, but the summaries are where contributors and agents tend to look first; they had to reinforce the contract instead of competing with it. | Spec `R1a`, `R1b`, `R7`, `R8`; architecture source-of-truth boundary | M1 grep-based wording checks recorded in the plan |
| Metadata validator and fixtures | [`scripts/validate-change-metadata.py`](../../scripts/validate-change-metadata.py), [`scripts/test-change-metadata-validator.py`](../../scripts/test-change-metadata-validator.py), [`tests/fixtures/change-metadata/bad-artifact-key/change.yaml`](../../tests/fixtures/change-metadata/bad-artifact-key/change.yaml), [`tests/fixtures/change-metadata/bad-artifact-value-shape/change.yaml`](../../tests/fixtures/change-metadata/bad-artifact-value-shape/change.yaml) | Added a canonical-key allowlist (`explain_change`, `review_resolution`, `verify_report`, etc.) as a semantic post-schema check, plus a fixture-driven test runner and targeted invalid fixtures. | The schema already preserved the scalar string value shape; the missing executable contract was the approved artifact-key vocabulary. The architecture explicitly said to tighten semantics in repo-owned validator logic, not by redesigning the schema. | Spec `R9`-`R9c`; architecture validator-boundary rule; plan M2 | `python scripts/test-change-metadata-validator.py`; direct validator runs against valid and invalid fixtures |
| Repo-owned CI wrapper | [`scripts/ci.sh`](../../scripts/ci.sh) | Added `python scripts/test-change-metadata-validator.py` to the standard repo-owned CI wrapper. | M3's goal was to ensure the new proof surface participates in the normal validation path instead of living only as an optional local command. | Test spec `T8`; plan M3 | `bash scripts/ci.sh` after `9c1994b` |
| Shipped compatibility example | [`docs/changes/0001-skill-validator/change.yaml`](../changes/0001-skill-validator/change.yaml), [`README.md`](../../README.md), [`specs/rigorloop-workflow.test.md`](../../specs/rigorloop-workflow.test.md) | Kept the shipped `0001` pack valid and explicitly repositioned it as a rich reference example, not a universal minimum. | The feature should tighten the baseline contract without forcing every non-trivial change to carry standalone review-memory or verification artifacts. | Spec `R6b`, `R7a`, `R7b`; proposal rationale | `python scripts/validate-change-metadata.py docs/changes/0001-skill-validator/change.yaml`; manual review of contributor wording |
| Lifecycle bookkeeping after review and verify | [`2026-04-21-docs-changes-usage-policy.md`](../plans/2026-04-21-docs-changes-usage-policy.md), [`docs-changes-usage-policy.test.md`](../../specs/docs-changes-usage-policy.test.md) | Synced the active plan and test spec after code review and verify so they stopped advertising stale next-stage text. | This repository treats active lifecycle-managed artifacts as current execution state. Once review and verify completed, those surfaces needed to reflect that settled state before downstream stages relied on them. | Verify-stage lifecycle rules in `AGENTS.md` and `CONSTITUTION.md`; plan/test-spec lifecycle expectations | `174ae58`; explicit-path lifecycle validation over the active plan and test spec after the sync |

## Tests added or changed

- [`docs-changes-usage-policy.test.md`](../../specs/docs-changes-usage-policy.test.md) was added as the tracked feature test spec. It maps:
  - `R1`-`R8` into manual contract review across the workflow spec, workflow test spec, summaries, `0001`, and legacy `docs/explain/` artifacts;
  - `R9`-`R9c` into executable validator checks;
  - smoke proof into `bash scripts/ci.sh`.
- [`specs/rigorloop-workflow.test.md`](../../specs/rigorloop-workflow.test.md) was updated because the docs-changes rule changes behavior already covered by the repository-level workflow proof surface.
- [`scripts/test-change-metadata-validator.py`](../../scripts/test-change-metadata-validator.py) was added as the dedicated fixture runner for the metadata contract.
- The negative fixtures added in M2 prove the important failure cases:
  - noncanonical artifact keys fail with actionable errors;
  - nested artifact-map values fail because the value shape must remain a plain scalar path string.

That test level is appropriate because the feature is mostly contract and validation alignment. The new runtime-like behavior lives in one validator seam, so a focused fixture runner plus repo-wide smoke proof covers the real risk without inventing a larger harness.

## Verification evidence

Final implementation verification was run against the feature stack through `174ae58`.

Commands run:

- `python scripts/test-change-metadata-validator.py`
  - pass
  - important evidence: the valid fixture and shipped `0001` example pass, and the invalid key/value-shape fixtures fail for the intended reasons
- `python scripts/validate-change-metadata.py docs/changes/0001-skill-validator/change.yaml`
  - pass
- `bash scripts/ci.sh`
  - pass
  - important evidence: the normal repo-owned wrapper now runs the metadata fixture surface in addition to the existing skill and lifecycle checks
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-20-docs-changes-usage-policy.md --path specs/docs-changes-usage-policy.md --path docs/architecture/2026-04-21-docs-changes-usage-policy.md --path docs/plans/2026-04-21-docs-changes-usage-policy.md --path specs/docs-changes-usage-policy.test.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md`
  - pass
  - important evidence: `validated 8 artifact files in explicit-paths mode`
- `git diff --check -- docs/plans/2026-04-21-docs-changes-usage-policy.md specs/docs-changes-usage-policy.test.md`
  - pass during verify lifecycle sync

Explain-change stage closeout checks for this artifact and the post-explanation lifecycle sync:

- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-04-21-docs-changes-usage-policy.md --path specs/docs-changes-usage-policy.test.md`
- `git diff --check -- docs/explain/2026-04-21-docs-changes-usage-policy.md docs/plans/2026-04-21-docs-changes-usage-policy.md specs/docs-changes-usage-policy.test.md`

Validation boundary:

- Hosted GitHub Actions CI is still unobserved from this environment, so this explanation does not claim hosted CI passed.
- No PR body exists yet. The `pr` stage is still outstanding.

## Alternatives rejected

- Redesigning `change.yaml` into nested artifact objects.
  - Rejected because the approved architecture keeps the existing scalar-path schema shape and limits enforcement to lightweight validator logic.
- Making `docs/changes/` optional for ordinary non-trivial work.
  - Rejected because the proposal and spec were explicitly framed as clarification of the approved contract, not a relaxation.
- Treating the full `0001-skill-validator` pack as the universal minimum.
  - Rejected because ordinary non-trivial work only needs the baseline pack plus conditional artifacts whose triggers actually apply.
- Forcing migration of approved legacy `docs/explain/*.md` artifacts.
  - Rejected because the approved compatibility rule preserves them until they are migrated, superseded, archived, or otherwise retired.
- Expanding M3 into direct `.github/workflows/ci.yml` logic.
  - Rejected because the workflow already satisfied the thin-wrapper contract; the right change was to update [`scripts/ci.sh`](../../scripts/ci.sh), not duplicate logic in GitHub Actions YAML.

## Scope control

This feature intentionally did not:

- redesign `schemas/change.schema.json`;
- require every non-trivial change to replicate the `0001` artifact pack;
- weaken the existing workflow contract around non-trivial change traceability;
- invalidate or mass-migrate approved legacy `docs/explain/*.md` artifacts;
- promote `docs/changes/` into a second long-form source of truth for proposal/spec/architecture/plan content;
- add network-dependent CI logic or claim hosted CI coverage from local verification.

## Risks and follow-ups

- Hosted CI is still unknown from this environment.
- The current branch is still `chore/close-workflow-handoff-proposal`, and the plan explicitly kept this feature out of that unrelated proposal-closeout review scope. The `pr` stage should move the verified tip onto a dedicated review branch or otherwise ensure the PR scope is clean.
- The feature is ready for PR preparation, but PR creation itself still needs the normal branch/base/readiness checks.

## PR-ready summary

- Added the full proposal/spec/test-spec/architecture/plan trail for the docs-changes usage policy feature.
- Updated the governing workflow contract and repository summaries so non-trivial work clearly requires `change.yaml` plus durable reasoning, while `review-resolution.md` and `verify-report.md` stay conditional.
- Added canonical `change.yaml` artifact-key enforcement, a dedicated metadata fixture runner, and targeted invalid fixtures without redesigning the schema.
- Wired the metadata fixture runner into `bash scripts/ci.sh` so the normal repo-owned proof path covers the feature.
- Synced the active plan and test spec through review and verify so the lifecycle-managed artifacts stayed truthful before PR preparation.
