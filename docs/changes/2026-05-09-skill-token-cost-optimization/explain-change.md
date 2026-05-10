# Skill Token Cost Optimization Change Rationale

## Status

- current

## Scope

This change implements the approved skill token-cost optimization contract.

The core invariant is:

```text
Find the smallest evidence surface that can answer the current question.
Correctness still outranks token savings.
```

The change tightens skill-contract requirements, selected skill guidance, static proof, generated local skill mirrors, and public adapter output so agents prefer bounded evidence before broad reads without weakening validation coverage, review obligations, artifact obligations, or full-file-read escape conditions.

## Rationale

### M1. Skill Contract and Static Proof

- `specs/skill-contract.md` now defines token-cost discipline as a normal skill-contract requirement.
- `specs/skill-contract.test.md` maps the contract amendment to focused proof for bounded evidence, full-file-read escape conditions, output-cap limits, unchanged validation semantics, and the no-new-skill boundary.
- `scripts/test-skill-validator.py` adds narrow static checks for the accepted wording instead of broad semantic quality scoring.
- Code-review M1 completed cleanly with no material findings before M2 started.

### M2. Shared Evidence Guidance and Canonical Skills

- `templates/shared/evidence-collection-efficiency.md` now says to use bounded evidence before broad reads, preserve validation semantics, treat output caps as safety rails rather than query design, and expand exact ranges only when narrower evidence is insufficient.
- The selected high-volume canonical skills copied the tightened evidence guidance: `proposal`, `proposal-review`, `spec`, `spec-review`, `plan`, `plan-review`, `implement`, `code-review`, `verify`, `pr`, and `learn`.
- `skills/workflow/SKILL.md` was aligned only because it already consumed the shared evidence block; this avoided shared-block drift without expanding the feature scope.
- Code-review M2 completed cleanly with no material findings before M3 started.

### M3. Generated Skill and Adapter Output

- `.codex/skills/` was regenerated from canonical `skills/` sources.
- `dist/adapters/` was regenerated with `python scripts/build-adapters.py --version 0.1.1`.
- Generated skill drift, adapter drift, adapter validation, adapter distribution tests, skill validation, and skill validator tests passed after regeneration.
- Code-review M3 completed cleanly with no material findings before M4 started.

### M4. Lifecycle Evidence Preparation

- This rationale is the durable Markdown explanation for the change-local baseline pack.
- `change.yaml` records the current artifact set, changed files, review state, and validation evidence.
- The active plan remains the live workflow-state owner. `docs/plan.md` remains an active lifecycle index entry; it is intentionally unchanged in M4 because the plan is not ready to move to Done until M5 final lifecycle closeout.

## Requirement Coverage

- `R1` through `R6` are covered by the skill-contract amendment, selected skill guidance, and validator proof.
- `R7` is covered by project-portable public skill wording and adapter validation.
- `R8` is covered by narrow static validation in `scripts/test-skill-validator.py`.
- `R9` is covered by generated skill drift, adapter drift, adapter validation, and adapter distribution proof.
- `R10` is covered by review-skill guidance and milestone code-review handoff evidence.

## Validation Evidence

Detailed command evidence is recorded in the active plan and `change.yaml`.

Important proof surfaces include:

- review artifact closeout validation for the resolved plan-review material finding;
- lifecycle validation for the proposal, spec, test spec, skill contract, change metadata, explain-change, active plan, and plan index;
- skill validator and skill validation checks;
- generated skill drift checks;
- versioned adapter drift and adapter validation;
- adapter distribution tests;
- scoped whitespace checks for changed plan and change-local artifacts.

## Current Handoff

Use the active plan `Current Handoff Summary` for current live state. This rationale is scoped evidence and does not own final verification, branch readiness, PR readiness, or the active plan's current next stage.
