# Explain Change: RigorLoop CLI New Change

## Summary

This change adds the first `rigorloop new-change` CLI slice to the existing `@xiongxianfei/rigorloop` package. The command scaffolds one safe, draft change metadata file at `docs/changes/<change-id>/change.yaml`, with deterministic contents and a complete write plan, so users do not need to memorize the baseline change metadata shape.

The implementation deliberately remains a scaffold. It does not create `explain-change.md`, review records, specs, plans, PR bodies, adapter files, `rigorloop.yaml`, or `rigorloop.lock`, and it does not claim that any downstream lifecycle stage has completed.

## Problem

RigorLoop had strong repository-local workflow artifacts and validators, but starting a new change still required users and agents to know the expected `docs/changes/<change-id>/change.yaml` structure and safe path conventions. The approved CLI direction identified `new-change` as a narrow follow-up after the initial CLI package, Codex init, and lockfile slices.

The main risk was overclaiming. A scaffolded file must not look like durable reasoning, review completion, verification, branch readiness, or PR readiness. The command also needed the same safety bar as prior CLI work: dry-run plans must name every mutation, symlinks and overwrites must block before writes, and partial write failures must be observable.

## Decision Trail

The umbrella CLI proposal authorized a broad CLI direction, but follow-up work is handled one implementable slice at a time. After the lockfile PR merged, `FU-005` became the next active follow-up: `rigorloop new-change` artifact pack scaffolding.

Spec-review initially requested changes for three contract gaps:

- `SR1-F1`: option domains for `--type` and `--risk` were underdefined.
- `SR1-F2`: an `explain-change.md` placeholder could be mistaken for durable reasoning.
- `SR1-F3`: partial mutation failure behavior was incomplete.

The revised spec resolved those by defining exact value domains, removing the first-slice `explain-change.md` placeholder, and requiring explicit non-atomic partial-failure reporting. `spec-review-r2` approved the revised spec.

Architecture then recorded `new-change` as an additive CLI scaffold inside the existing package boundary. No new ADR was required because the command does not introduce a new source of truth, package boundary, persistence mechanism, release policy, or validation authority.

The approved plan split implementation into three reviewable milestones:

- M1: command argument validation and deterministic metadata rendering.
- M2: write-plan, dry-run, symlink/overwrite safety, and successful scaffolding.
- M3: partial failure behavior, output polish, and final integration.

## Diff Rationale By Area

| File | Change | Reason | Source artifact | Test/evidence |
|---|---|---|---|---|
| `packages/rigorloop/dist/bin/rigorloop.js` | Added `new-change` help text, dispatch, JSON/human output routing, and result-to-exit handling. | Exposes the approved command through the existing `rigorloop` binary while reusing the stable CLI envelope and exit helper. | Spec R1-R12, R57-R70; plan M1-M3. | `TNC-001`, `TNC-008`, `TNC-018`, full package tests. |
| `packages/rigorloop/dist/lib/new-change.js` | Added package-local validation and metadata rendering helpers. | Keeps public option domains and deterministic `change.yaml` content testable without filesystem mutation. | Spec R3-R10, R13-R19, R27-R37. | `TNC-002` through `TNC-007`; `CR1-F1` regression for `review.unresolved_items: 0`. |
| `packages/rigorloop/dist/lib/new-change-filesystem.js` | Added write-plan, artifact reporting, mutation, blocker, warning, and partial-failure helpers. | Separates filesystem planning/application from CLI output and makes partial write failure deterministic to test. | Spec R20-R26, R44-R56k, R63-R68. | `TNC-009` through `TNC-017`, `TNC-019` through `TNC-021`. |
| `packages/rigorloop/test/cli.test.js` | Added `TNC-001` through `TNC-021` coverage and copied new helper files into fixture packages. | Proves the public command surface, value domains, generated metadata, mutation safety, output modes, and non-goals. | Test spec `specs/rigorloop-cli-new-change.test.md`. | `npm test --prefix packages/rigorloop`. |
| `scripts/validate-change-metadata.py` | Recognizes inline `{}` and `[]` as empty map/list literals. | Generated metadata intentionally uses inline empty collections; the repository validator needed to parse that valid first-slice shape. | Spec R31-R37; plan M2 discovery. | `scripts/test-change-metadata-validator.py`, `TNC-020`. |
| `scripts/test-change-metadata-validator.py` | Added regression coverage for inline empty collections in `change.yaml`. | Prevents validator drift against the generated metadata shape. | Test spec `TNC-020`. | `python scripts/test-change-metadata-validator.py`. |
| `specs/rigorloop-cli-new-change.md` | Added the accepted command contract. | Defines the observable behavior before implementation: command surface, value domains, mutation safety, output, non-goals, and acceptance criteria. | `FU-005`, approved proposal direction. | `spec-review-r2`. |
| `specs/rigorloop-cli-new-change.test.md` | Added traceable test plan `TNC-001` through `TNC-022`. | Maps each requirement and edge case to concrete tests before implementation. | Approved spec and plan. | Package tests and selected CI. |
| `docs/architecture/system/architecture.md` and `container.mmd` | Added the `new-change` flow and CLI scaffold boundary to the canonical architecture. | Records that `new-change` is additive, local, non-networked, and not a lifecycle-completion source. | Architecture-review input. | `architecture-review-r1`. |
| `docs/follow-ups.md`, `docs/plan.md`, and plan files | Closed stale prior follow-ups, made `FU-005` the active slice, and tracked milestone state through implementation closeout. | Keeps lifecycle state synchronized as work moved from lockfile closeout to the new active follow-up. | Workflow and plan policy. | Artifact lifecycle validation and selected CI. |
| `docs/changes/2026-05-16-rigorloop-cli-new-change/*` | Added change metadata, reviews, review log, review resolution, and this explanation. | Provides durable evidence for spec, architecture, plan, implementation reviews, and rationale. | Workflow contract for non-trivial work. | Review artifact validation and change metadata validation. |

## Tests Added Or Changed

The test spec defines `TNC-001` through `TNC-022`; implemented package coverage currently includes `TNC-001` through `TNC-021`, with `TNC-022` represented by selected validation and final verify.

- `TNC-001` proves help exposes `new-change`.
- `TNC-002` through `TNC-005` prove required arguments and exact option domains.
- `TNC-006` proves deterministic metadata defaults and field order, including the `CR1-F1` fix for `review.unresolved_items: 0`.
- `TNC-007` proves YAML scalar escaping and avoids local environment leakage.
- `TNC-008` proves the JSON envelope and command-specific `change` object.
- `TNC-009` and `TNC-010` prove standard and minimal profiles create only `change.yaml`, with minimal-profile warning behavior.
- `TNC-011` and `TNC-012` prove dry-run and existing-directory write plans.
- `TNC-013`, `TNC-014`, and `TNC-016` prove conflict, symlink, and overwrite blocking before mutation.
- `TNC-015` and `TNC-019` prove scope control: no forbidden artifacts, project manifests, lockfiles, adapter work, network use, Git requirement, or PR inspection.
- `TNC-017` proves non-atomic partial failure reporting through a package-local helper seam.
- `TNC-018` proves human, JSON, quiet, debug, and no-color output behavior.
- `TNC-020` proves generated metadata validates with the repository validator.
- `TNC-021` proves write-plan scope stays proportional to the scaffolded paths.

The validator regression test for inline empty collections was added because generated first-slice metadata uses `artifacts: {}` and empty arrays. Without that parser support, valid generated metadata would fail the repository validator.

## Validation Evidence Available Before Final Verify

Implementation and review stages recorded passing evidence for:

```bash
npm test --prefix packages/rigorloop
python scripts/test-select-validation.py
python scripts/test-change-metadata-validator.py
python scripts/validate-change-metadata.py docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml
python scripts/validate-review-artifacts.py docs/changes/2026-05-16-rigorloop-cli-new-change
python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...
bash scripts/ci.sh --mode explicit ...
git diff --check -- ...
```

The latest selected CI run after `code-review-m3-r1` passed the selected checks for review artifacts, artifact lifecycle, change metadata regression, change metadata validation, and the RigorLoop CLI package test suite.

This explanation is not final `verify` evidence. The next lifecycle stage owns final verification.

## Review Resolution Summary

Review resolution is recorded in `docs/changes/2026-05-16-rigorloop-cli-new-change/review-resolution.md`.

- Material findings resolved: 5.
- Unresolved findings: 0.
- Accepted and resolved spec findings: `SR1-F1`, `SR1-F2`, `SR1-F3`.
- Accepted and resolved code-review findings: `CR1-F1`, `CR2-F1`.
- Clean later reviews: `spec-review-r2`, `architecture-review-r1`, `plan-review-r1`, `code-review-m1-r2`, `code-review-m2-r2`, `code-review-m3-r1`.

## Alternatives Rejected

- Creating `explain-change.md` as a placeholder during `new-change` was rejected because it could look like durable reasoning before the explain-change stage actually ran.
- Recording `artifacts.explain_change` in generated metadata was rejected for the same reason.
- Supporting `--force` was rejected for the first slice to keep mutation safety simple and non-destructive.
- Making `new-change` inspect Git, PR state, workflow status, validators, adapters, or lockfiles was rejected because this slice is only metadata scaffolding.
- Implementing atomic rollback was rejected for the first slice; instead, the spec requires honest partial-failure reporting.
- Permission-dependent partial-failure tests were avoided in favor of a helper-level deterministic failure seam, reducing platform flakiness.

## Scope Control

The change preserves these non-goals:

- No `status` or `validate` command behavior.
- No adapter installation.
- No network access.
- No `rigorloop.yaml` write.
- No `rigorloop.lock` write.
- No proposal, spec, plan, review, verify, or PR artifact scaffolding.
- No lifecycle advancement claim.
- No public npm publication or release-hardening change.

## Risks And Follow-Ups

The main residual risk is user interpretation: a generated `change.yaml` is useful starting metadata, not proof that a change is ready. The implementation mitigates this by leaving artifacts and evidence arrays empty, setting review state to pending, and avoiding durable-looking Markdown placeholders.

The first slice also does not provide repair commands for partial writes. If users hit a write failure after directories are created, the CLI reports completed and failed actions; later tooling could add cleanup or repair behavior under a separate spec.

The active plan state after this artifact should move from implementation closeout to final verification. The initiative remains active until `verify` and PR handoff produce their own evidence.
