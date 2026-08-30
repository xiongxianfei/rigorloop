# M4 canonical review responsibilities implementation

Change ID: 2026-08-28-consolidate-rigorloop-review-gates
Milestone: M4
Stage authority: implement
Subject path: docs/plans/2026-08-29-consolidate-rigorloop-review-gates.md
Validation result: pass

## Scope completed

- Added one embedded Feasibility section to the canonical proposal asset and proposal guidance. The section records assessment, basis, constraints, and blockers; no standalone feasibility artifact, skill, state, or gate was added.
- Added distinct canonical `design-review` and `delivery-review` skills with exact package inputs, independent review boundaries, three finding scopes, durable evidence, CLI recording and settlement, isolation, and bounded claims.
- Updated authoring, workflow, Code Review, Explain Change, Verify, and PR guidance to consume exact package authority while preserving separate authorship and downstream assurance.
- Marked the four retiring artifact-review skills as pre-cutover historical entrypoints and explicitly prohibited aliases. Actual public inventory removal remains the atomic M6 cutover responsibility.
- Updated governance and workflow contracts with the cutover-ready stage graph and retained the implementing change's explicit pre-cutover exception.
- Added CRG-T03 and CRG-T13 skill-contract regressions and updated superseded workflow baseline assertions.

## Changed surfaces

- Proposal: `skills/proposal/`, `skills/proposal-review/`
- New reviews: `skills/design-review/`, `skills/delivery-review/`
- Authoring handoffs: `skills/architecture/`, `skills/spec/`, `skills/plan/`, `skills/test-spec/`, `skills/implement/`
- Retiring entrypoints: `skills/spec-review/`, `skills/architecture-review/`, `skills/plan-review/`, `skills/test-spec-review/`
- Downstream consumers: `skills/workflow/`, `skills/code-review/`, `skills/explain-change/`, `skills/verify/`, `skills/pr/`
- Governance and tests: `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, `specs/rigorloop-workflow.md`, `specs/skill-contract.md`, `scripts/test-skill-validator.py`

## Unaffected with rationale

- Lifecycle CLI and package state: unchanged; M2 and M3 already provide package context, settlement, invalidation, and routing behavior consumed by these skills.
- Generated adapter manifest and release archives: unchanged; M5 owns deterministic adapter inventory and archive parity, and M6 owns atomic public cutover.
- Proposal content beyond Feasibility: unchanged; broader proposal simplification is a non-goal.
- Code Review, Explain Change, Verify, and PR decision semantics: unchanged; only their package-authority inputs were made explicit.
- Aggregate and member hashes: not introduced; package identity remains the visible artifact ID-to-path map plus upstream and package review IDs.

## Validation

- `python scripts/validate-skills.py`: passed; 26 canonical skills validated.
- `python scripts/test-skill-validator.py`: passed; 450 tests, 16 skipped.
- `python scripts/build-skills.py --check`: passed using a temporary generated local mirror.
- `python scripts/validate-documentation-prose.py --mode audit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path specs/rigorloop-workflow.md`: passed with zero errors and 48 pre-existing reviewer warnings.
- `git diff --check`: passed.

## Review handoff

M4 is ready for independent Code Review of feasibility ownership, exact-package review responsibilities, finding attribution, review independence, cutover wording, downstream claim preservation, and generated-local-mirror parity. This evidence does not claim Code Review approval or milestone closeout.

## R1 correction

- CRG-M4-CR1: qualified the complete constitutional package-gate block with the atomic cutover boundary and explicitly retained the pre-cutover sequence for this implementing change and other legacy-dependent work.
- CRG-M4-CR2: added the exact post-cutover automation target inventory to the short workflow guide and strengthened the focused regression to reject every retired review target in that inventory.
- `python scripts/test-skill-validator.py`: passed; 450 tests, 16 skipped.
- `python scripts/validate-skills.py`: passed; 26 canonical skills validated.
- `python scripts/build-skills.py --check`: passed.
- `python scripts/validate-documentation-prose.py --mode audit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path specs/rigorloop-workflow.md`: passed with zero errors and 48 baseline reviewer warnings.
- `git diff --check`: passed.
