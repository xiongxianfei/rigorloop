# Proposal authoring evidence

- Operation: `create-primary-proposal`
- Assembly: `PA1G-governed-gated`
- Change ID: `2026-08-24-governed-lifecycle-cli`
- Artifact ID: `proposal`
- Proposal ID: `RL-PROP-CLI-001`
- Proposal path: `docs/proposals/2026-08-24-governed-lifecycle-cli.md`
- Proposal content identity: `sha256:8eedbed3d8c9ea286df1f554c518f24478179bdcdcc32e22c4e8d4eedef31838`
- Evidence basis: user-provided proposal direction; current `CONSTITUTION.md`, `VISION.md`, and `docs/workflows.md`; the accepted `docs/proposals/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow.md`; the current CLI boundary in `docs/architecture/system/architecture.md`; and direct inspection of `packages/rigorloop/`.
- Bounded conditional evidence reason: the existing CLI proposal and architecture package establish the product boundary that this proposal extends; direct package inspection confirms the current executable surface without relying on the project map as implementation authority.
- Specialized predicates: `initial_intent_table_context`, `scope_budget_context`
- Result: proposal authored and transitioned to `review-required`
- Next stage: `proposal-review`
