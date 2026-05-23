# Behavior Preservation

## Purpose

Record that the M2 README adoption-surface implementation improved public
documentation without changing runtime behavior, workflow semantics, skills,
adapters, validators, or release trust boundaries.

## Preservation matrix

| Surface | Baseline | M2 proof | Preservation result |
| --- | --- | --- | --- |
| CLI behavior | Existing package CLI behavior and tests | M2 touched no CLI source files | unchanged |
| Adapter behavior | Existing adapter install and release-archive contract | M2 touched no adapter source, manifest, or release archive files | unchanged |
| Skill behavior | Existing authored skills under `skills/` | M2 touched no skill files | unchanged |
| Validator behavior | Existing repository-owned validation scripts | M2 touched no script or schema files | unchanged |
| Workflow semantics | Existing `CONSTITUTION.md`, `docs/workflows.md`, and workflow specs | M2 touched no workflow contract files | unchanged |
| README Quick Start | Root README pinned current-use examples used `@0.1.5` | Root README now uses `@latest` for quick trials and `@0.2.0` for reproducible examples | improved |
| README lifecycle visual | No first-slice Mermaid lifecycle visual | README now includes static Mermaid chain from Idea to PR with manual-invocation caption | improved |
| Contribution routing | Existing contribution, issue, and security files existed but were less visible near the top | README now links to workflow, proof example, contribution guide, issue templates, and security policy | improved |
| Repository metadata | M1 recorded blank before-state and approved target values | M2 did not mutate live metadata | unchanged; M4 owns mutation |
| npm metadata/package README | Current package surfaces still contain stale `@0.1.5` examples | M2 did not edit package metadata or package README | unchanged; M3 owns alignment |
| npm metadata/package README after M3 | Package description was generic and package README had current-use `@0.1.5` examples | Package description/keywords now align with approved positioning and package README examples use `@latest` or `@0.2.0` | improved |
| Repository metadata after M4 | Blank description, blank website, and no topics | Live repository metadata now has the approved description, 18 approved topics, and blank website | improved |

## Diff boundary

M2 changed:

- `README.md`
- `docs/changes/2026-05-23-public-discovery-and-developer-adoption-surface/readme-ownership-proof.md`
- `docs/changes/2026-05-23-public-discovery-and-developer-adoption-surface/version-sync-proof.md`
- `docs/changes/2026-05-23-public-discovery-and-developer-adoption-surface/adoption-surface-review.md`
- `docs/changes/2026-05-23-public-discovery-and-developer-adoption-surface/behavior-preservation.md`
- active plan, plan index, and compact change metadata lifecycle records

M3 changed:

- `packages/rigorloop/package.json`
- `packages/rigorloop/README.md`
- `docs/changes/2026-05-23-public-discovery-and-developer-adoption-surface/version-sync-proof.md`
- `docs/changes/2026-05-23-public-discovery-and-developer-adoption-surface/adoption-surface-review.md`
- `docs/changes/2026-05-23-public-discovery-and-developer-adoption-surface/behavior-preservation.md`
- active plan, plan index, and compact change metadata lifecycle records

M2 did not change:

- CLI implementation files
- adapter distribution files
- authored skill files
- validator scripts or schemas
- release archives or release automation
- workflow contracts
- package metadata or package README

M3 did not change:

- CLI implementation files
- adapter distribution files
- authored skill files
- validator scripts or schemas
- release archives or release automation
- workflow contracts
- live repository metadata

M4 changed:

- GitHub repository description for `xiongxianfei/rigorloop`
- GitHub repository topics for `xiongxianfei/rigorloop`
- GitHub repository website field remains blank by approved decision
- `docs/changes/2026-05-23-public-discovery-and-developer-adoption-surface/repository-metadata-proof.md`
- active plan, plan index, and compact change metadata lifecycle records

M4 did not change:

- CLI implementation files
- package metadata or package README
- adapter distribution files
- authored skill files
- validator scripts or schemas
- release archives or release automation
- workflow contracts

## Unsupported-claim result

The README preserves negative/boundary positioning around hosted platforms,
centralized control planes, replacement behavior, pull requests, CI, and human
review. No unsupported broad-adoption, production maturity, hosted-platform,
autonomous-merge, fake-status, or replacement claim was added.

## Status

M2 behavior preservation result: documentation-only adoption-surface change;
runtime and workflow behavior unchanged.

M3 behavior preservation result: npm package metadata and package README
adoption-surface change only; `npm test --prefix packages/rigorloop` passed
with 107 tests, and runtime/workflow behavior remains unchanged.

M4 behavior preservation result: external repository metadata and proof change
only; runtime, package, adapter, skill, validator, release, and workflow
behavior remain unchanged.

M5 behavior preservation result: lifecycle rationale, plan state, plan index,
and change metadata evidence only; runtime, package, adapter, skill, validator,
release, and workflow behavior remain unchanged.
