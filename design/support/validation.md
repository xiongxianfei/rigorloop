# Engineering Validation Model Design

Model validation contract: model-document-v1

## Introduction and Goals

Run a small essential regression suite through ordinary native test runners. The maintainer explicitly selected reduced automated coverage on 2026-10-18. This replaces the custom selector, scheduler, per-case adapters and report-envelope infrastructure. Product behavior, final independent review and distinct Verify remain governed by their existing owners.

## Context and Scope

[System](../architecture/composition.md) owns test quality; this model owns repository commands and execution scope. [Development](development.md#validation) owns contributor practice. Packaging, Installation and Release own their actual artifact and publication checks. Tests cannot grant publication authority.

## Architecture Constraints

The supported routine command is `bash scripts/ci.sh`, without arguments. It executes the same four groups locally, on pull requests and on main. Native runners own discovery, failure output and process exit status. There is no path classification, worker scheduler, report destination, result cache, broad-smoke mode or implicit release-candidate preparation. Removed contributor options fail with a usage error instead of silently narrowing checks.

## Requirements

| ID | Required behavior |
| --- | --- |
| VAL-SR-01 | The direct runner MUST execute the declared essential groups with isolated mutable fixtures and propagate a failed command. |
| VAL-SR-12 | Evidence MUST state actual commands, results, scope and limitations. A selected suite pass MUST NOT claim complete product coverage or hosted CI success. Native runner output is sufficient; custom timing/report schemas are retired. |
| VAL-SR-13 | Removal MUST reconcile actual imports, callers, fixtures, model coverage and generated consumers. The authorized reduction and residual risks MUST remain explicit. |
| VAL-SR-14 | Retained direct test entrypoints MUST discover and execute their declared population without optional hidden cases. Public command/store/archive claims require observations at those real boundaries. |
| VAL-SR-15 | Release qualification MUST retain actual candidate integrity and public observations under Release ownership; routine CI MUST NOT publish or substitute source tests for candidate checks. |
| VAL-SR-16 | Current consumers MUST agree on the smaller suite; historical judgments and customer contracts retain their original meaning. |
| VAL-SR-17 | Tests MUST own temporary state and cleanup, preserve user files, and avoid leaking credentials or private environment data. |
| VAL-SR-18 | Performance claims MUST identify measured scope and environment; fewer cases or lines alone are not a measured speedup. |
| VAL-SR-38 | Complete-suite claims MUST describe only the selected essential suite. Unimplemented model scenarios remain explicit gaps, not inferred coverage. |

The earlier execution/adoption obligations VAL-SR-02–11, 19–37 are retired as mandatory repository mechanisms by the selected minimal-suite policy. This includes exhaustive path admission, canonical check catalogs, worker budgets, per-case isolation adapters, timing JSON and automated complete-model coverage admission. Their original definitions remain in Git at `d7761c8c9c34f0f3a4bb3a74504190e0ceafed53:design/support/validation.md`. Independent product requirements and historical outcomes are not retired by this disposition.

## Solution Strategy

Reuse assertions for high-consequence outcomes, consolidate setup only where useful, and remove test-only infrastructure. Keep model and generation commands available for changes that need them; ordinary CI does not run every validator. No automatic replacement of semantic review with phrase checks is selected.

## Architecture Overview

`ci.sh` invokes native Node tests for workflow, storage/recovery and installation safety, then Python tests for packed installation/archive integrity and skill resources. GitHub CI installs the existing Node dependency and invokes that same command. Release invokes its actual qualification commands and a small release-boundary group. Tests use real temporary stores and archives; no repository-global test result store is introduced.

## Runtime View

Run from the repository root, reject arguments, execute declared groups in order, stop on nonzero exit, and preserve ordinary command output. No hidden path-based selection or success-on-empty discovery is permitted. A missing file is an error. An interrupted command is incomplete evidence.

### Test sources, groups and fixtures

| Group | Current sources | Protection |
| --- | --- | --- |
| Workflow | `packages/rigorloop/test/operational-review.test.js` | Complete the review-free intermediate path; block missing independent final approval, self-approval, missing/stale Verify and unresolved findings. |
| Storage/recovery | `packages/rigorloop/test/operational-{store,update,maintenance}.test.js` | Persist/resume real records, reject malformed/stale requests atomically, preserve corrupt data and safely restore/recover backups. |
| Installation | `packages/rigorloop/test/installer-replacement.test.js`; `tests/engineering/packaging/test-npm-package-publication.py`; `tests/engineering/packaging/test-adapter-distribution.py` | Actual tarball and target installation, authored archive resources, conflicts, unsafe paths and interrupted replacement. |
| Skill integrity | `tests/skill/test-skill-validator.py` | Current skill/resource validity and missing-resource detection. |
| Release boundary | `tests/engineering/release/test-release-transaction.py`; existing release validators | Candidate identity, publication authority and failure handling. Executed at release qualification, not routine PR CI. |

Keep support local and small. Tests may contain an ordered recovery scenario; native runner execution does not require a custom scheduler or a receipt per case. Runtime generators, release scripts and record examples are product inputs and are not deleted merely because they live under scripts or fixtures.

### Proof quality, maintenance and evidence

The selected reduction intentionally removes automatic coverage of exhaustive malformed-input combinations, detailed CLI rendering, legacy import permutations, model/schema validators, documentation wording, browser interaction and rare concurrency/interruption interleavings. These are reduced-assurance areas, not unsupported product features. Changes affecting them must allocate explicit focused tests or concrete manual/review evidence; the essential suite cannot establish their correctness. Preserve high-consequence state, authority and destructive-write assertions in the retained groups. Historical catalogs keep scenario intent and explicit missing realizations.

### Execution cost reporting

Use native test output and optional external wall-clock timing for a scoped observation. No worker-duration JSON, report reservation, cache, performance threshold or benchmark ledger is required. The old environment variables are no longer report interfaces.

### Model-owned test-design admission

Supporting catalogs describe intended scenarios and actual realization references. A removed test reference becomes a documented proof gap. The optional structural validator may check those references using ordinary native discovery; it does not select routine tests or establish sufficient coverage.

### Boundary scan and acceptance scenarios

| Dimension | Requirement basis | Distinct outcome to demonstrate |
| --- | --- | --- |
| Input domain | VAL-SR-01 | Arguments to the direct runner reject before tests; valid invocation runs all essential groups. |
| State/lifecycle | VAL-SR-12 | Failed or interrupted execution cannot establish a passing complete-suite claim. |
| Identity/authority | VAL-SR-15 | Routine checks grant no publication authority; release still checks actual candidate identity. |
| Composition/path | VAL-SR-13, VAL-SR-14 | Every retained source is reached by its native entrypoint; deleted helpers have no current executable consumers. |
| Temporal/retry | VAL-SR-01, VAL-SR-17 | A repeated invocation owns fresh fixtures; no stale cache result replaces execution. |
| Failure/recovery | VAL-SR-14, VAL-SR-17 | Negative and recovery scenarios observe preserved state and user files. |
| Compatibility/migration | VAL-SR-16 | Removed contributor options reject; product records and historical judgments retain their meaning. |
| External/environment | VAL-SR-15, VAL-SR-18 | Tests use qualified local tools and controlled public-service fixtures; public observations remain release-owned. |

## Deployment View

Local and ordinary CI execution require Python and the package-supported Node version, with package dependencies installed. Routine CI does not install Chromium, Puppeteer, D2 or jsonschema. Changes to browser/model generators use their existing declared tools on demand. Release retains its own tool and authority boundaries.

## Crosscutting Concepts

Use [shared test-design rules](test-design/rules.md) for assertion quality, explicit limitations and meaningful negative cases. User-authorized reduction of regression breadth is distinct from an equivalence-preserving refactor. Review must judge the selected essential protection and disclosed residual risk rather than infer preserved coverage from a green run.

## Architecture Decisions

Keep the existing command name and required release entrypoints, replace their implementation directly, remove unused internal execution layers and reconcile all current consumers. Do not retain mode aliases or a dormant legacy suite. Git history is the recovery source.

## Quality Requirements

Failures remain visible; tests must detect the intended defect, preserve unrelated files and leave no private fixture state in the repository. Whole-change review and distinct Verify remain required.

## Risks and Technical Debt

Less automatic coverage makes changes outside the essential path more dependent on deliberate scoped proof. No empirical reliability or productivity improvement is claimed. Release public-service behavior still requires the actual observations specified by Release.

## Historical provenance

The prior validation contract and removed tests are recoverable at `d7761c8c9c34f0f3a4bb3a74504190e0ceafed53`. The [minimal-suite plan](../../docs/plans/2026-10-18-minimal-tests.md) records the selected scope; results and judgments belong to its Change.
