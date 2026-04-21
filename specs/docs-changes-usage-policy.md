# Docs Changes Usage Policy

## Status
- approved

## Related proposal

- [Docs Changes Usage Policy](../docs/proposals/2026-04-20-docs-changes-usage-policy.md)

## Goal and context

This spec defines the contributor-visible packaging policy for `docs/changes/<change-id>/` so non-trivial changes consistently include the required machine-readable metadata and durable Markdown reasoning without treating the `0001-skill-validator` example as the minimum pack for every change.

The existing workflow contract already requires `change.yaml`, durable Markdown reasoning, PR summary, and conditional standalone review-memory artifacts. What is missing is a concise operational rule for which change-local artifacts are baseline, which are conditional, and which are only example-specific.

## Glossary

- `change-local artifact pack`: the authored files stored under `docs/changes/<change-id>/` for one change.
- `baseline change-local artifacts`: the minimum change-local artifacts that non-trivial work must carry under the approved workflow contract.
- `conditional change-local artifact`: a change-local artifact required only when its governing trigger applies.
- `durable reasoning artifact`: a Markdown artifact that preserves human-readable rationale for the final diff beyond PR text alone.
- `standalone verification artifact`: a dedicated Markdown record of verification evidence that is kept separate from `explain-change.md`.
- `equivalent approved reasoning surface`: an artifact explicitly named by the workflow spec as satisfying the durable reasoning requirement for the change.

## Examples first

### Example E1: fast-lane change omits `docs/changes/`

Given a trivial fast-lane documentation clarification
When the change remains inside the approved fast-lane categories
Then the change may omit `docs/changes/<change-id>/change.yaml` and other change-local artifacts, while still carrying the required fast-lane spec and validation evidence in a tracked or review-visible location.

### Example E2: ordinary non-trivial change uses the baseline pack

Given a non-trivial change with concise verification evidence and no standalone review-memory trigger
When the contributor prepares the change-local artifact pack
Then the baseline pack contains `docs/changes/<change-id>/change.yaml` plus `docs/changes/<change-id>/explain-change.md`, and it does not require `review-resolution.md` or `verify-report.md`.

### Example E3: review-resolution becomes standalone only when its trigger applies

Given a non-trivial change goes through multiple material review rounds with deferred items
When the workflow contract's standalone review-resolution trigger applies
Then the change-local artifact pack includes `docs/changes/<change-id>/review-resolution.md` in addition to the baseline artifacts.

### Example E4: complex verification requires `verify-report.md`

Given a change has multiple verification commands across separate environments
When the verification evidence cannot remain concise inside `explain-change.md`
Then the change-local artifact pack includes `docs/changes/<change-id>/verify-report.md` as a standalone verification record.

### Example E5: the `0001` example is rich, not minimum

Given a contributor inspects `docs/changes/0001-skill-validator/`
When they use it as a reference model
Then they treat it as a valid rich example of a fully formed pack, not as proof that every non-trivial change must include the same artifact set.

## Requirements

R1. The repository MUST define one contributor-visible packaging rule for `docs/changes/<change-id>/` that clarifies baseline versus conditional change-local artifacts without relaxing the already-approved workflow contract.

R1a. The normative home for that packaging rule MUST be `specs/rigorloop-workflow.md`.

R1b. `CONSTITUTION.md`, `docs/workflows.md`, and `AGENTS.md` MAY summarize the rule, but they MUST NOT weaken or contradict the workflow-spec contract.

R2. For every non-trivial change, the change-local artifact pack MUST include `docs/changes/<change-id>/change.yaml`.

R2a. Fast-lane changes MAY omit `docs/changes/<change-id>/change.yaml` only when the approved fast-lane policy allows omission.

R2b. A non-trivial change missing `docs/changes/<change-id>/change.yaml` MUST be treated as incomplete.

R3. For every non-trivial change, durable Markdown reasoning for the final diff MUST exist in addition to `change.yaml`.

R3a. The default change-local artifact for that durable reasoning MUST be `docs/changes/<change-id>/explain-change.md`.

R3b. PR text alone MUST NOT satisfy the durable reasoning requirement for non-trivial work.

R3c. The only allowed equivalent to `docs/changes/<change-id>/explain-change.md` is another artifact explicitly named by the workflow spec as satisfying the durable reasoning requirement for the change.

R3d. For new non-trivial work, the default durable reasoning artifact location MUST be `docs/changes/<change-id>/explain-change.md`.

R3e. Approved legacy top-level explain artifacts, including approved artifacts under `docs/explain/`, MUST remain valid durable-reasoning surfaces until they are migrated, superseded, archived, or otherwise retired.

R3f. New top-level explain artifacts MUST NOT be created unless the workflow spec explicitly allows that artifact class.

R4. Change-local artifact roles MUST remain distinct and MUST NOT be treated as interchangeable.

R4a. `change.yaml` MUST be treated as machine-readable change metadata and artifact indexing.

R4b. `explain-change.md` MUST be treated as durable human-readable rationale for the final diff.

R4c. `review-resolution.md` MUST be treated as durable review-disposition memory for accepted, rejected, or deferred review items when a standalone review-resolution artifact is required.

R4d. `verify-report.md` MUST be treated as durable verification evidence when a standalone verification artifact is required.

R5. `docs/changes/<change-id>/review-resolution.md` MUST be conditionally required only when the workflow contract requires review resolution to exist as a standalone artifact.

R5a. When the workflow contract does not require standalone review resolution, review-resolution evidence MAY remain in PR text or the durable reasoning artifact instead of a separate `review-resolution.md`.

R6. `docs/changes/<change-id>/verify-report.md` MUST be conditionally required only when at least one of the following is true:
- the change has non-trivial verification evidence that cannot be kept concise in `explain-change.md`;
- the change requires a durable standalone verification record for reviewer or maintainer audit;
- the change has multiple verification commands, environments, or result groups that need separate traceable reporting;
- repository policy for the change type explicitly requires a standalone verification artifact;
- a reviewer or maintainer explicitly requests a standalone verify report;
- the verification stage is itself a reviewed deliverable for the change.

R6a. When none of the `R6` triggers apply, verification evidence MAY remain inside `explain-change.md` or the PR summary, provided the existing workflow contract's durability and concision requirements remain satisfied.

R6b. A contributor SHOULD NOT add `verify-report.md` only because the `0001-skill-validator` example contains one.

R7. The change-local artifact pack MUST stay concise and MUST link back to approved top-level artifacts instead of becoming a second long-form source of truth.

R7a. This policy MUST NOT require every non-trivial change to carry the full `0001-skill-validator` artifact set.

R7b. `docs/changes/0001-skill-validator/` SHOULD be documented as a valid rich reference example rather than the minimum required pack.

R8. The contributor-facing packaging rule MUST make the baseline pack for ordinary non-trivial work observable:
- `change.yaml`;
- durable Markdown reasoning; and
- only the conditional change-local artifacts whose governing triggers apply.

R9. When a change-local artifact exists under `docs/changes/<change-id>/`, `change.yaml` MUST index it through the `artifacts` mapping according to the governing `change.yaml` contract.

R9a. The `artifacts` mapping in `change.yaml` MUST use canonical snake_case keys for change-local and related durable artifacts.

R9b. Canonical artifact keys include:
- `proposal`
- `spec`
- `architecture`
- `adr`
- `plan`
- `test_spec`
- `change_summary`
- `explain_change`
- `review_resolution`
- `verify_report`
- `pr_body`
- `retrospective`

R9c. The `artifacts` mapping MUST use plain scalar string path values. This spec MUST NOT change the existing artifact-map value shape unless a later schema change explicitly does so.

## Inputs and outputs

Inputs:

- change classification as fast-lane or non-trivial;
- whether standalone review-resolution is required by the workflow contract;
- whether standalone verification triggers apply;
- approved workflow-spec rules for durable reasoning equivalents;
- canonical snake_case artifact keys for `change.yaml`;
- the current change-local artifact set and PR summary.

Outputs:

- a contributor-visible packaging rule in the workflow contract and summaries;
- a correctly scoped change-local artifact pack for each change;
- `change.yaml` artifact indexing that reflects the durable Markdown artifacts actually present.

## State and invariants

- Every non-trivial change has machine-readable traceability at `docs/changes/<change-id>/change.yaml`.
- Every non-trivial change also has durable Markdown reasoning beyond PR text alone.
- Change-local artifact roles remain distinct: metadata, rationale, review disposition, and verification evidence do not collapse into one file type.
- Conditional artifacts appear only when their governing triggers apply.
- The `0001-skill-validator` example remains a valid rich pack without becoming the minimum pack for every non-trivial change.
- Change-local artifacts remain concise and do not replace approved top-level proposal, spec, architecture, or plan artifacts.

## Error and boundary behavior

- If a non-trivial change omits `change.yaml`, the change is incomplete.
- If a non-trivial change relies only on PR text for durable reasoning, the change is incomplete.
- If a contributor claims an equivalent approved reasoning surface that is not explicitly named by the workflow spec, the claim is invalid and the default `explain-change.md` requirement remains.
- If standalone review-resolution or standalone verification triggers apply and the corresponding artifact is missing, the change is incomplete.
- If a fast-lane change falls outside the approved fast-lane categories, it must follow the non-trivial packaging rules instead of omitting `docs/changes/`.
- A richer-than-minimum change-local pack is allowed when its artifact set is truthful, but contributors must not treat the rich example as a blanket requirement for every non-trivial change.

## Compatibility and migration

- This feature clarifies the packaging contract; it does not change the underlying `change.yaml` schema.
- Existing rich change-local packs such as `docs/changes/0001-skill-validator/` remain valid and do not need to be reduced.
- Approved legacy top-level explain artifacts remain valid durable-reasoning surfaces until later migration or retirement.
- Existing contributor-facing summaries may be updated to match this clarified rule, but the workflow spec remains the normative source.
- New non-trivial authored change work should default to `docs/changes/<change-id>/explain-change.md`.
- Later approved changes may define additional explicit equivalent durable reasoning surfaces or additional standalone verification triggers without invalidating this baseline policy.

## Observability

- A reviewer SHOULD be able to inspect a non-trivial change and determine whether it carries the baseline pack or additional conditional artifacts.
- The workflow spec and its summaries SHOULD make clear that `change.yaml` alone is insufficient for non-trivial work.
- `change.yaml` SHOULD make the presence or absence of change-local Markdown artifacts inspectable through its `artifacts` mapping.
- Manual review and test-spec coverage SHOULD be able to distinguish missing baseline artifacts from missing conditional artifacts.

## Security and privacy

- `change.yaml`, `explain-change.md`, `review-resolution.md`, and `verify-report.md` MUST NOT be used to store secrets, credentials, or sensitive runtime configuration.
- Concise packaging guidance MUST NOT encourage contributors to move required durable reasoning into private chat or untracked notes.

## Edge cases

1. A trivial fast-lane change may omit `docs/changes/<change-id>/` while still carrying the required fast-lane spec and validation evidence in another approved surface.
2. A non-trivial change with concise validation evidence and no standalone triggers may satisfy the policy with `change.yaml` plus `explain-change.md`.
3. A non-trivial change with multiple verification environments requires `verify-report.md` even if `explain-change.md` also exists.
4. A non-trivial change with routine review feedback does not require standalone `review-resolution.md` when the workflow contract's standalone review-resolution triggers do not apply.
5. An approved legacy top-level explain artifact may remain the durable reasoning surface for already-shipped work until it is migrated or retired.
6. A contributor may not cite an ad hoc document or PR text alone as the equivalent durable reasoning surface unless the workflow spec explicitly names it.
7. The `artifacts` mapping in `change.yaml` uses canonical snake_case keys with scalar string path values rather than nested objects.
8. The `0001-skill-validator` example may include more artifacts than an ordinary non-trivial change without making those extra artifacts universal.

## Non-goals

- Redesigning the `change.yaml` schema.
- Making `docs/changes/` optional for non-trivial work.
- Requiring every non-trivial change to replicate the full `0001-skill-validator` artifact pack.
- Replacing PR text as the reviewer-facing summary surface.
- Reclassifying fast-lane versus non-trivial work beyond the already-approved workflow contract.
- Promoting change-local artifacts into a second top-level source of truth that duplicates proposal, spec, architecture, or plan artifacts.

## Acceptance criteria

- A contributor can determine from the workflow spec whether a change needs no `docs/changes/`, the baseline non-trivial pack, or additional conditional artifacts.
- A reviewer can tell that `change.yaml` plus PR text alone is insufficient for non-trivial work unless the workflow spec names an equivalent durable reasoning surface.
- A reviewer can distinguish valid legacy top-level explain artifacts from the default location for new work.
- A reviewer can distinguish when `review-resolution.md` is required versus optional.
- A reviewer can distinguish when `verify-report.md` is required versus when verification evidence may remain in `explain-change.md` or the PR summary.
- A reviewer can determine the canonical `change.yaml` artifact keys and that their values are scalar string paths.
- The rich `0001-skill-validator` example remains valid without being interpreted as the minimum required pack for every non-trivial change.
- The workflow contract remains stronger than contributor summaries, and the summaries do not contradict it.

## Open questions

- None.

## Next artifacts

- `architecture-review`
- `test-spec`

## Follow-on artifacts

- `docs/architecture/2026-04-21-docs-changes-usage-policy.md`
- `specs/docs-changes-usage-policy.test.md`

## Readiness

This spec is approved.

Architecture work is now tracked in `docs/architecture/2026-04-21-docs-changes-usage-policy.md`.

Test-spec work is now tracked in `specs/docs-changes-usage-policy.test.md`.

No further `spec-review` action is pending.
