---
name: bugfix
description: Fix defects with proof-first correction.
argument-hint: [bug description, failing behavior, error message, issue number, or regression]
---

# Fix

## Inputs

Read governance, contract, evidence, code, tests, and context. Bind one repository and one concrete defect; split independent defects.

## Classification and authority

Operation: `diagnose-only` or `fix`. Explicit diagnosis wins; a bare concrete-defect request selects fix. A later fix MUST rerun preflight.

Command authority: `not-required`, `current-bounded`, `absent-or-stale`, `invalid-or-ambiguous`. Write authority: `none`, `portable-request-bound`, `governed-scope-bound`, `absent-or-stale`, `invalid-or-ambiguous`. Fix authority binds repository, defect, source, commands, paths, write kinds, and identities. Diagnose-only allows bounded commands, not tracked or durable external mutation. Dangerous commands need separate authority.

Governed signal: `no-governed-signal`, `single-governed-candidate`, `invalid-or-ambiguous-governed-signal`. Explicit IDs, workflow identities, and owning-change fields count. Invalid signals stop and never fall back to portable authority.

## Evidence and phases

Record reproduction, contract, feasibility, proof, cause, blast radius, uncertainty. `resolvable-restoration` means one authoritative outcome without peer/higher conflict or invented behavior. A `deterministic-alternative` records steps, inputs, environment, results, limits.

Phases: diagnosis, `proof-authoring`, `production-correction`, validation. Proof-authoring writes only tests, fixtures, helpers, or reproduction artifacts. Production correction requires a `failing-automated-test`, or `infeasible-with-rationale` plus complete deterministic-alternative proof. Rerun the same proof identity.

## Action selection

Cause is exactly `implementation-defect`, `contract-gap`, `configuration-or-environment`, `external-dependency`, `test-defect`, or `unknown`.

Actions: `stop-blocked`, `route-owner`, `continue-diagnosis`, `resolve-test-feasibility`, `author-automated-proof`, `apply-production-correction`, `run-post-fix-validation`, `complete-fix`. Precedence:

1. invalid authority, identity, safety, or evidence conflict: stop-blocked;
2. contract-gap or behavior change: route-owner;
3. unknown/unsupported cause: continue-diagnosis;
4. correction exists and proof fails: stop-blocked;
5. correction exists and proof passes: complete-fix;
6. correction exists pending validation: run-post-fix-validation;
7. eligible fix without correction: resolve feasibility, author proof, apply correction.

Never weaken tests without exact basis. Route environment/dependency causes unless contract requires resilience.

Terminal result is exactly `diagnosis-complete`, `diagnosis-incomplete`, `fix-applied`, `routed-to-owner`, or `blocked`.

## Write boundary

Write only authorized proof/implementation. Specs, architecture, plans, `change.yaml`, workflow state, reviews, verification, PR, and release state are read-only. Use an exact evidence location; do not invent governed state or paths.

## Completion and handoff

Rerun unchanged proof and checks. Report commands actually run, unexecuted checks, changed surfaces, uncertainty, and result. Changes hand off to `code-review`; no stage continues automatically. Never claim PR readiness or lifecycle completion.

## Evidence collection efficiency

Use summary and stable-ID first reasoning. Prefer check IDs, requirement IDs, file paths, and line citations.

## When full-file read is required

Read fully when the whole file is the review target, bounded searches disagree, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Expected output

Return the completion record.
