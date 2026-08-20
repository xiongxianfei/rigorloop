---
name: bugfix
description: Proof-first fixes.
argument-hint: [bug description, failing behavior, error message, issue number, or regression]
---

# Fix

Use proof before correction. Bind one repository, one concrete defect, and one expected-versus-actual outcome. Split independent defects unless they share one cause, behavior basis, correction scope, and proof bundle.

## Operation and authority

Operation is exactly `diagnose-only` or `fix`. Explicit diagnosis, explanation, reproduction, or root-cause wording selects `diagnose-only`, even with `$bugfix`. Explicit repair wording, or bare `$bugfix` naming one concrete defect and no narrower outcome, selects `fix`. Conflicting intent permits diagnosis but blocks mutation. A later diagnosis-to-fix expansion MUST rerun preflight.

Command authority is exactly `not-required`, `current-bounded`, `absent-or-stale`, or `invalid-or-ambiguous`. Write authority is exactly `none`, `portable-request-bound`, `governed-scope-bound`, `absent-or-stale`, or `invalid-or-ambiguous`. Bind every writable fix to repository identity, normalized defect, authority source, permitted command owner or set, path roots, write categories, governing contract, and current evidence identities.

Diagnose-only may run exact inspection or reproduction commands only with current-bounded authority and intentionally changes no tracked file or durable external state. Unknown, destructive, privileged, network, database, or durable effects need their separate authority or are skipped. Unexpected mutation stops and is reported.

Governed signal is exactly `no-governed-signal`, `single-governed-candidate`, or `invalid-or-ambiguous-governed-signal`. Explicit change IDs, workflow identities, and structured owning-change fields count even when malformed. Invalid, stale, conflicting, duplicated, escaped, or unsafe signals stop and never fall back to portable authority.

## Evidence

Classify these axes before dependent consistency checks; unknown values fail closed:

- reproduction: `reproduced`, `deterministic-alternative`, `not-established`, `conflicting`;
- contract basis: `settled`, `resolvable-restoration`, `missing`, `conflicting`, `behavior-change-request`;
- test feasibility: `feasible`, `infeasible-with-rationale`, `unresolved`;
- regression proof: `failing-automated-test`, `deterministic-alternative`, `missing`, `conflicting`;
- root-cause support: `supported`, `uncertain`, `conflicting`.

`resolvable-restoration` binds one current authoritative source, owner, precedence, affected behavior, expected result, and conflict check. It restores conformance without adding, removing, broadening, narrowing, or reinterpreting observable behavior. Implementation, a test, a report, or plausible expectation alone is insufficient.

A `deterministic-alternative` is an independently repeatable command, fixture, static contract check, or controlled manual procedure. Record exact inputs, environment assumptions, steps, expected observation, objective completion, and limitations. Subjective inspection and infeasibility alone are not proof.

## Phases and proof

Phases are ordered `diagnosis`, `proof-authoring`, `production-correction`, `post-fix-validation`. After non-proof prerequisites pass, proof-authoring may write only bounded tests, fixtures, test-only helpers, or controlled reproduction artifacts; production behavior remains unchanged.

Use this exhaustive proof-action table:

| Test feasibility | Regression proof | Current action |
| --- | --- | --- |
| Any recognized | failing-automated-test | apply-production-correction |
| Any recognized | conflicting | stop-blocked |
| feasible | missing or deterministic-alternative | author-automated-proof |
| unresolved | missing or deterministic-alternative | resolve-test-feasibility |
| infeasible-with-rationale | complete deterministic-alternative | apply-production-correction |
| infeasible-with-rationale | missing | stop-blocked |

Before production mutation, record the proof kind, command or procedure, fixture and input identities, environment assumptions, expected and observed pre-fix result, feasibility, and infeasibility rationale. Post-fix validation reruns the same proof identity. A changed test, fixture, command, input, or environment is a different proof and cannot establish that the original regression passes.

## Cause, action, and result

Root cause is exactly `implementation-defect`, `contract-gap`, `integration-mismatch`, `data-or-migration`, `race-or-timing`, `configuration-or-environment`, `test-defect`, `external-dependency`, or `unknown`.

Current action is exactly `stop-blocked`, `route-owner`, `continue-diagnosis`, `complete-diagnosis`, `resolve-test-feasibility`, `author-automated-proof`, `apply-production-correction`, `run-post-fix-validation`, or `complete-fix`. Apply these conditions in order:

1. Unknown value, conflicting axis, unsafe identity, invalid authority, missing required authority, or fix with write authority `none`: `stop-blocked`.
2. `contract-gap`, or basis `missing`, `conflicting`, or `behavior-change-request`: `route-owner` to `spec` or the contract owner.
3. Cause `unknown`, or unresolved reproduction/support: `continue-diagnosis`.
4. A required long-lived design decision: `route-owner` to `architecture`.
5. Environment or dependency cause without settled resilience behavior and scope: `route-owner` to its system owner.
6. Diagnose-only with supported evidence and no owner action: `complete-diagnosis`.
7. A correction exists and identity-equal proof or required blast-radius validation fails: `stop-blocked`.
8. A correction exists and all required checks pass: `complete-fix`.
9. A correction exists with checks pending: `run-post-fix-validation`.
10. An eligible fix without correction: select exactly one proof-table action.

Cause `unknown` never authorizes mutation. A `test-defect` is writable only from `settled` or `resolvable-restoration` basis; never weaken expectations speculatively. Environment and dependency corrections require exact settled resilience behavior and scope.

On return, terminal result is exactly `diagnosis-complete`, `diagnosis-incomplete`, `fix-applied`, `routed-to-owner`, or `blocked`. Map `complete-diagnosis`, unresolved diagnosis, `complete-fix`, `route-owner`, and unsafe/incomplete work respectively. Intermediate actions are not terminal results.

## Write boundary

| Context and phase | Permitted writes |
| --- | --- |
| Portable diagnose-only | None |
| Portable proof-authoring | Request-bound tests, fixtures, test-only helpers, and controlled reproduction artifacts |
| Portable production-correction | Request-bound implementation and explicitly scoped non-authoritative documentation or examples |
| Governed diagnose-only | None |
| Governed proof-authoring | Exact governed proof surfaces and one existing authorized evidence destination |
| Governed production-correction | Exact governed implementation, existing authorized evidence, and only scope-named non-authoritative documentation |

Proposals, specs, architecture, ADRs, plans, `change.yaml`, workflow and automation state, reviews, review resolution, explanation, verification, PR, release, deployment, and publication are read-only. Normative changes route to their owner. Missing or ambiguous governed evidence placement blocks durable recording; do not invent a path, artifact, or lifecycle state.

## Completion and handoff

Rerun the original reproduction or exact alternative, the identity-equal regression proof, and the smallest surrounding validation justified by blast radius. A failed, conflicting, skipped-required, or mismatched check prevents `fix-applied`.

Report operation, terminal result, authority classifications, repository and defect, commands actually run, proof identity, unexecuted checks, uncertainty, changed surfaces, blockers, and next owner. Changed implementation hands off to independent `code-review`; no stage continues automatically. Never claim review approval, explanation, verification, hosted CI, branch or PR readiness, release, deployment, publication, lifecycle completion, or `Done`.

## Package measurement

Keep this package as one `SKILL.md`. Report before/after LF-normalized words and UTF-8 bytes; identify the tokenizer or model basis for any token estimate. Counts are diagnostic evidence, not a semantic gate. The skill MUST NOT omit, blur, or relocate required behavior to improve a count. Complete meaning, deterministic interpretation, safety, and package parity take precedence.

## Evidence collection efficiency

Use summary and stable-ID first reasoning. Prefer check IDs, requirement IDs, file paths, and line citations.

## When full-file read is required

Read fully when the whole file is the review target, bounded searches disagree, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Expected output

Return the completion record.
