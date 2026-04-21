# Docs Changes Usage Policy

## Status

- accepted

## Problem

RigorLoop already has a strong structural contract for change-local artifacts:

- non-trivial changes use `docs/changes/<change-id>/change.yaml`;
- narrative rationale lives in Markdown artifacts rather than only in metadata;
- the first shipped example is `docs/changes/0001-skill-validator/`.

But the repository still lacks one practical, contributor-facing rule of thumb for when to create `docs/changes/` at all and how much to put in it.

That gap causes two failures:

- contributors can under-use `docs/changes/` and treat it as optional even for non-trivial work;
- contributors can over-use it and assume every change needs a full `0001`-style artifact pack or misclassify which change-local Markdown artifacts are baseline versus conditional.

Without a clearer usage policy, review quality and traceability will stay inconsistent across changes even though the repository already has the schema, example pack, and architecture support for change-local artifacts.

## Goals

- Make the `docs/changes/` policy easy to apply during normal work.
- Preserve the existing requirement that non-trivial changes carry structured traceability.
- Distinguish baseline required change-local artifacts from conditionally required ones.
- Distinguish clearly between trivial fast-lane changes, ordinary non-trivial changes, and larger or heavily reviewed changes.
- Keep change-local packs concise and proportional to the actual change.
- Use `docs/changes/0001-skill-validator/` as the practical model for what a well-formed pack looks like.

## Non-goals

- Replacing PR text as the reviewer-facing summary surface.
- Requiring every change to carry the full `0001-skill-validator` artifact set.
- Redesigning the `change.yaml` schema itself.
- Redefining the repository’s fast-lane or non-trivial classification model beyond what is needed to clarify `docs/changes/` usage.
- Turning `docs/changes/` into a second long-form source of truth that duplicates top-level proposal, spec, architecture, or plan artifacts.

## Context

- The workflow spec already requires `docs/changes/<change-id>/change.yaml` for each non-trivial change in `R25` of `specs/rigorloop-workflow.md`.
- Fast-lane changes may omit `change.yaml` per `R25h` in `specs/rigorloop-workflow.md`.
- The constitution says change-local artifacts should stay concise and link back to top-level artifacts instead of becoming a second long-form source of truth in `CONSTITUTION.md`.
- The architecture already treats `docs/changes/<change-id>/` as the authored location for per-change durable reasoning and traceability in `docs/architecture/2026-04-19-rigorloop-first-release-repository-architecture.md`.
- The first shipped example pack is `docs/changes/0001-skill-validator/`, and it demonstrates the upper end of the current artifact model.
- Recent work exposed an operational ambiguity: a contributor can understand the hard rule for `change.yaml` from the spec, but still be unsure which change-local Markdown artifacts are always required, which are conditional, and which are example-specific.

## Options considered

### Option 1: Keep the current policy implicit

- Advantages:
  - no new policy surface to maintain
  - contributors can infer usage from the spec and the `0001` example
- Disadvantages:
  - operational ambiguity remains
  - contributors will continue to under-use or over-use `docs/changes/`
  - review quality depends too much on oral tradition and chat context

### Option 2: Require a full `0001`-style change pack for every non-trivial change

- Advantages:
  - maximum consistency
  - reviewers always know where to look
- Disadvantages:
  - too heavy for many ordinary non-trivial changes
  - encourages cargo-cult artifact creation
  - makes the workflow feel bureaucratic instead of proportional

### Option 3: Adopt a tiered usage policy for `docs/changes/`

- Advantages:
  - aligns with the current spec and constitution
  - gives contributors a simple operational rule
  - keeps ordinary non-trivial changes lightweight while preserving structured traceability
  - reserves larger Markdown packs for larger or review-heavy work
- Disadvantages:
  - requires one more policy layer to explain what “minimal Markdown artifacts needed” means
  - still depends on correct classification of trivial versus non-trivial work

### Option 4: Make `docs/changes/` optional and rely on PR text plus plans

- Advantages:
  - very light contributor burden
  - less duplication risk
- Disadvantages:
  - directly weakens the structured traceability contract already defined in `R25`
  - makes machine-readable change history inconsistent
  - loses the repository’s intended durable per-change memory model

## Recommended direction

Choose Option 3.

The repository should make the `docs/changes/` policy explicit as a tiered rule of thumb:

- trivial fast-lane change: no `docs/changes/`
- non-trivial change: create `docs/changes/<change-id>/change.yaml` and include the baseline durable Markdown reasoning required by the workflow contract
- additional change-local Markdown artifacts: add only the conditional artifacts whose governing stage contracts apply

The practical standard should be:

- this policy does not relax the approved workflow contract;
- for every non-trivial change, `docs/changes/<change-id>/change.yaml` is required;
- for every non-trivial change, durable Markdown reasoning is also required;
- the default change-local Markdown artifact for that reasoning is `explain-change.md`;
- the only allowed equivalent is another artifact explicitly named by the workflow spec as satisfying that durable reasoning requirement for the change;
- PR text alone does not satisfy that durable reasoning requirement;
- `review-resolution.md` is required when review resolution must exist as a standalone artifact under the workflow contract;
- `verify-report.md` is required only when the standalone verification trigger rules defined by the workflow contract apply;
- other change-local Markdown artifacts are required only when their governing stage contracts say so;
- `docs/changes/0001-skill-validator/` is the reference model for a fully formed pack, not a mandatory minimum shape for every non-trivial change.

This policy should be expressed in a contributor-facing way so people do not have to reverse-engineer it from `R25` and one example directory.

This proposal clarifies packaging and contributor guidance. It does not reduce the already-approved minimum artifact contract.

## Change-local artifact matrix

| Artifact | Role | Requirement level |
| --- | --- | --- |
| `change.yaml` | machine-readable change metadata and artifact index | always required for non-trivial work |
| `explain-change.md` | durable human-readable rationale for the final diff | default required for non-trivial work |
| `review-resolution.md` | durable record of accepted/rejected/deferred review feedback | conditionally required when standalone review-resolution is required |
| `verify-report.md` | standalone durable record of verification evidence | conditionally required when a standalone verification artifact is required |

These artifacts are not interchangeable.

- `change.yaml` is metadata.
- `explain-change.md` is rationale.
- `review-resolution.md` is review disposition.
- `verify-report.md` is verification evidence.

## Standalone verification artifact trigger

`docs/changes/<change-id>/verify-report.md` is conditionally required.

It is required only when at least one of the following is true:

1. the change has non-trivial verification evidence that cannot be kept concise in `explain-change.md`
2. the change requires a durable standalone verification record for reviewer or maintainer audit
3. the change has multiple verification commands, environments, or result groups that need separate traceable reporting
4. repository policy for the change type explicitly requires a standalone verification artifact
5. a reviewer or maintainer explicitly requests a standalone verify report
6. the verification stage is itself a reviewed deliverable for the change

Otherwise, verification evidence may remain inside `explain-change.md` or the PR summary, as long as the workflow contract’s durability and concision requirements are still met.

## Expected behavior changes

- Contributors will stop treating `docs/changes/` as optional for non-trivial work.
- Contributors will stop assuming every non-trivial change needs a full `0001`-sized artifact pack.
- Contributors will have a clearer baseline rule for which change-local artifacts are universal versus conditional.
- Reviewers will be able to expect:
  - no `docs/changes/` for trivial fast-lane work;
  - `change.yaml` plus baseline durable reasoning for ordinary non-trivial work;
  - additional Markdown artifacts only when their governing stage contracts apply.
- PRs and verifies will become more consistent because the traceability expectations will be explicit rather than implied.

## Architecture impact

This is mainly a workflow and governance clarification, not a runtime architecture change.

- Components affected:
  - `specs/rigorloop-workflow.md`
  - `CONSTITUTION.md` for high-level governance alignment
  - `docs/workflows.md` for contributor-facing summary
  - possibly `AGENTS.md` if a short operational summary is useful
  - `docs/changes/0001-skill-validator/` as the reference example, not as new implementation work
- Boundaries preserved:
  - `docs/changes/` remains authored per-change traceability
  - PR text remains the reviewer-facing summary surface
  - top-level proposal/spec/architecture/plan artifacts remain the long-form source of truth
  - `specs/rigorloop-workflow.md` remains the normative home for workflow-contract behavior

## Testing and verification strategy

- Update the workflow spec, with summary alignment in `CONSTITUTION.md`, `docs/workflows.md`, and `AGENTS.md` as needed, so the tiered policy is explicit and reviewable.
- Add or update a test spec that checks:
  - fast-lane changes may omit `docs/changes/`
  - non-trivial changes require `change.yaml`
  - non-trivial changes also require baseline durable reasoning
  - conditional artifacts such as `review-resolution.md` and `verify-report.md` appear only when their governing triggers apply
- Manual review should confirm that the clarified policy matches the existing `0001-skill-validator` example and does not require full-pack boilerplate for every non-trivial change.

## Rollout and rollback

Rollout:

- add the explicit tiered policy to the governing workflow artifacts;
- align contributor-facing summaries with that policy;
- keep `0001-skill-validator` as the example of a rich pack rather than redefining it;
- use the new policy on the next non-trivial change to prove it is practical.

Rollback:

- revert the policy clarification if it creates confusion;
- fall back temporarily to the current harder rule from `R25` plus ad hoc reviewer judgment;
- do not remove existing `docs/changes/` support or the `change.yaml` schema.

## Risks and mitigations

- Risk: contributors read the rule of thumb as weakening `R25`.
  - Mitigation: make explicit that non-trivial changes still require `change.yaml`; only the Markdown pack size is tiered.
- Risk: contributors read the guidance as making `explain-change.md`, `review-resolution.md`, and `verify-report.md` interchangeable.
  - Mitigation: include a small artifact-role matrix and make the trigger rules explicit.
- Risk: contributors use “trivial” too loosely to avoid change-local artifacts.
  - Mitigation: keep the current fast-lane boundaries authoritative and point back to them.
- Risk: contributors still over-produce artifacts because “larger or reviewed change” is vague.
  - Mitigation: replace that vague phrase with objective trigger language tied to the current workflow contract.
- Risk: policy detail gets duplicated across too many files.
  - Mitigation: keep `specs/rigorloop-workflow.md` normative and use concise summaries in `CONSTITUTION.md`, `docs/workflows.md`, and `AGENTS.md`.

## Open questions

- Should the next workflow test spec explicitly include negative cases where a non-trivial change has no `change.yaml`?
- Should `docs/workflows.md` include the short rule-of-thumb bullets directly, or only point back to the spec?

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-04-20 | Clarify `docs/changes/` usage with a tiered rule of thumb instead of leaving it implicit. | Contributors need an operational rule, not only schema requirements and one example pack. | Keeping the policy implicit leaves too much ambiguity. |
| 2026-04-20 | Keep `change.yaml` mandatory for non-trivial work. | This preserves the existing structured traceability contract in `R25`. | Making `docs/changes/` fully optional would weaken the workflow. |
| 2026-04-20 | Keep baseline durable Markdown reasoning mandatory for non-trivial work. | This preserves the already-approved durable reasoning contract rather than weakening it to `change.yaml` alone. | Treating Markdown artifacts as optional for ordinary non-trivial work would conflict with the current workflow contract. |
| 2026-04-20 | Treat `0001-skill-validator` as the rich reference example, not the minimum required pack for every non-trivial change. | This keeps the workflow proportional while preserving a strong exemplar. | Requiring a full pack for all non-trivial changes would be too heavy. |

## Next artifacts

- `proposal-review`
- `spec`
- `test-spec`

## Follow-on artifacts

- `specs/docs-changes-usage-policy.md`
- `docs/architecture/2026-04-21-docs-changes-usage-policy.md`

## Readiness

This proposal is accepted.

Spec work is tracked in `specs/docs-changes-usage-policy.md`.

Architecture work is tracked in `docs/architecture/2026-04-21-docs-changes-usage-policy.md`.

No further `proposal-review` action is pending.
