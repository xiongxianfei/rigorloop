# ADR-20260419-repository-source-layout: Canonical Workflow Sources and Codex Compatibility Output

## Status
Proposed

## Context

The workflow spec requires the repository to separate canonical generic workflow content from tool-specific adapter guidance and generated output. The current repository has two parallel skill trees:

- `skills/`
- `.codex/skills/`

Those trees have already drifted, which means the repository no longer has a single trustworthy source for skill content. The current Codex runtime in this repository still reads `.codex/skills/`, so the design cannot simply delete that path without a compatibility plan.

The repository had used `.codex/PLANS.md` as planning guidance even though plan structure is generic workflow content rather than Codex-specific runtime output. That compatibility file has now been removed, so the architecture needs one canonical plan-template path instead of a second helper path.

## Decision

For the first release:

1. Canonical generic workflow content lives in normal repository paths:
   - `docs/`
   - `specs/`
   - `skills/`
   - `schemas/`
   - `scripts/`
2. `skills/` is the canonical authored source for workflow skills.
3. `.codex/skills/` is generated Codex compatibility output derived from `skills/` and must not be hand-edited.
4. `docs/plans/0000-00-00-example-plan.md` is the canonical plan template/example.
5. `docs/plans/0000-00-00-example-plan.md` is the only plan-template source of truth. `.codex/PLANS.md` is removed and must not be reintroduced as a compatibility helper.
6. The first release keeps the current top-level repository shape and does not introduce a larger `method/`, `adapters/`, or `dist/` layout.

## Alternatives considered

### Make `.codex/skills/` canonical

- Simpler for the current runtime.
- Rejected because it couples generic workflow content to a tool-specific namespace and weakens the source-of-truth split.

### Keep both skill trees editable

- Lowest immediate migration work.
- Rejected because drift already exists and makes review ambiguous.

### Introduce a larger `method/` + `adapters/` + `dist/` layout immediately

- Cleaner long-term conceptual separation.
- Rejected for the first release because it creates too much structural churn before the workflow is implemented and validated.

## Consequences

- The repository needs a `build-skills.py` or equivalent generation step.
- CI needs a drift check so generated Codex output stays synchronized with canonical skill source.
- Root guidance must clearly identify canonical authored paths and generated paths.
- The first release preserves current Codex runtime compatibility without treating `.codex/skills/` as an editable source.

## Follow-up

- Add `schemas/` and `docs/changes/` in implementation.
- Generate or synchronize `.codex/skills/` from `skills/`.
- Update any remaining guidance to point directly to `docs/plans/0000-00-00-example-plan.md`.
- Update `README.md`, `docs/workflows.md`, and `AGENTS.md` so contributors can identify canonical versus generated paths quickly.
