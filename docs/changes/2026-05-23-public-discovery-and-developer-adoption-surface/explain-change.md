# Explain Change: Public Discovery and Developer Adoption Surface

## Purpose

This change improves RigorLoop's first-contact public adoption surface while
preserving the existing workflow and runtime boundaries. It makes the repository
easier to discover, easier to understand from the first README screen, and
easier to evaluate through durable proof artifacts.

The governing direction is the accepted proposal, approved spec, active test
spec, and reviewed plan for
`2026-05-23-public-discovery-and-developer-adoption-surface`.

## What Changed

### Repository Metadata

The live GitHub repository metadata was updated to the approved external
settings:

- description:
  `Git-first workflow for AI coding agents: proposals, specs, tests, review gates, and durable validation evidence from idea to PR.`
- topics: the approved 18-topic set for AI coding, developer tooling, code
  review, Git workflow, CLI/npm delivery, validation, and supported adapter
  discovery.
- website: blank, by the approved first-slice decision.

Because GitHub metadata is external state, the durable before/after proof lives
in `repository-metadata-proof.md` instead of relying on a PR diff alone.

### Root README

`README.md` was updated as the main first-contact adoption surface:

- added a direct `@latest init --adapter codex` first command near the top;
- added a near-top link group for Quick Start, workflow, proof example,
  contribution, issue templates, and security guidance;
- preserved the generated vision block boundary;
- preserved the value-first `When to use / When not to use` contract;
- updated current Quick Start examples from stale `@0.1.5` pins to `@latest`
  and reproducible `@0.2.0` examples;
- added a static Mermaid lifecycle diagram with caption text that keeps manual
  skill invocations scoped and does not imply full workflow completion.

This keeps the README as a landing surface, not a replacement for workflow
specs or detailed docs.

### npm Package Surface

`packages/rigorloop/package.json` now uses a description aligned with the
approved repository positioning and has keywords mirroring the approved topic
set where npm metadata supports keywords.

`packages/rigorloop/README.md` now aligns current-use install and archive
examples with the current stable `0.2.0` release, while preserving the npm
delivery-channel boundary: npm is an install surface, not the canonical source
for workflow rules, skills, schemas, templates, or adapter archives.

### Proof Artifacts

The change-local proof pack records the parts that are not fully represented by
normal diffs:

- `repository-metadata-proof.md`: approved metadata, before-state, permission
  status, mutation command, after-state, and metadata acceptance status.
- `version-sync-proof.md`: GitHub and npm version sources and stale-version
  sweep results.
- `readme-ownership-proof.md`: generated-region boundaries and source-of-truth
  checks.
- `adoption-surface-review.md`: cold-read, link, command, stale-version,
  unsupported-claim, and visual accuracy evidence.
- `behavior-preservation.md`: no-runtime-change matrix across CLI, adapters,
  skills, validators, release boundaries, workflow semantics, README, package
  metadata, and repository metadata.

## Why These Changes

The proposal identified a mismatch between RigorLoop's internal rigor and its
external discovery surface. A visitor could find substantial internal artifacts
but still need too much effort to answer what the project is, who it serves, how
to try it, and how to inspect proof.

The implementation keeps the approved first slice narrow:

- public metadata;
- README first-contact comprehension;
- Quick Start freshness;
- static lifecycle visual;
- contribution and security routing;
- npm package landing alignment;
- durable proof for external and subjective checks.

It deliberately does not change runtime behavior, workflow semantics, skills,
adapters, validators, release automation, or release archive trust boundaries.

## Requirement Coverage

- `DXA-R1` through `DXA-R3`: satisfied by live GitHub metadata update and
  `repository-metadata-proof.md`.
- `DXA-R4` through `DXA-R9`: satisfied by README updates,
  `readme-ownership-proof.md`, and `adoption-surface-review.md`.
- `DXA-R10` through `DXA-R13`: satisfied by package metadata/package README
  alignment and `version-sync-proof.md`.
- `DXA-R14` through `DXA-R18`: satisfied by ownership, cold-read/link,
  behavior-preservation, no-runtime-change, and validation evidence.
- `AC-DXA-001` through `AC-DXA-018`: covered by the metadata proof, README and
  npm diffs, proof artifacts, package tests, lifecycle validators, stale-version
  scans, unsupported-claim sweeps, and review records.

## Behavior Preservation

Runtime and workflow behavior are unchanged.

The only product-package file touched is package metadata/README content; the
CLI implementation and tests are unchanged. The package test suite passed after
the package metadata and README changes.

No adapter distribution files, authored skill files, validator scripts, schemas,
release archives, release automation, or workflow-contract files were changed
for product behavior.

## Validation Summary

Validation evidence is recorded in the active plan and `change.yaml`. The M5
handoff validation includes:

- review artifact closeout validation;
- change metadata validation;
- lifecycle explicit-path validation;
- npm package tests;
- validation selector regression;
- stale-version sweep;
- repository metadata after-state check;
- whitespace validation.

This artifact explains the implementation and prepares the milestone for
`code-review`. It does not claim code-review completion, final verify
completion, PR readiness, branch readiness, or Done.
