# M1 preservation inventories

Milestone: M1

The current flat skill remained byte-identical while the simplification boundary was frozen. Its LF-normalized baseline is 1,175 words, 8,224 bytes, and SHA-256 `8a26dde3b27ec13717cf385948a50b78a37d89c72536d260077416b9caccf95b`.

## Inventories

- `explain-change-rule-disposition.yaml` assigns every behaviorally significant rule one closed treatment and owner.
- `explain-change-literal-compatibility.yaml` records exact workflow, review, readiness, path, result, and assembly literals together with known consumers.
- `fixtures/explain-change-simplification-scenarios.yaml` covers the three governed-signal classes, three output actions, four loaded assemblies, target and authority failures, missing resources, atomic-write uncertainty, reviewed-subject tails, handback claims, historical artifacts, measurement failures, and architecture triggers.

Unknown vocabulary values use the explicit `not_in_vocabulary` fixture and are rejected before consistency checks.

## Architecture boundary

The selected implementation reuses the current packaged-skill resource model, existing change-local evidence, and single-file replacement behavior. It adds no identity store, transaction record, schema, lifecycle state, routing owner, cross-stage write owner, Markdown parser, runtime generator, or external integration. The bounded result remains `architecture-not-required`; discovery of any listed architecture trigger stops M2 and routes back to architecture assessment.

## Consumer inventory

Exact consumers were located in `docs/workflows.md`, the workflow, code-review, verify, PR, and implement skills, `scripts/workflow_automation_policy.py`, `scripts/workflow_automation_state.py`, `scripts/workflow_automation.py`, and `scripts/test-skill-validator.py`. Cross-skill path and readiness literals remain owned by those surfaces; the explain-change package may report only explanation-owned state.

## Validation

- `python scripts/test-skill-validator.py ExplainChangeSkillSimplificationTests` — passed, 5 tests.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-18-explain-change-skill-simplification/change.yaml` — passed.
