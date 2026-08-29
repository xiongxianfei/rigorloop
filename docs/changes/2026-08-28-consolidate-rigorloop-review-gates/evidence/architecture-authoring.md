# Architecture authoring evidence

Stage: architecture-assessment
Assessment mode: isolated
Applicability: required
Route: architecture-required
Action: canonical-update-with-adr
Assembly: AA2-governed-authoring
Change ID: 2026-08-28-consolidate-rigorloop-review-gates
Spec identity: sha256:ae8b9452fc028fadb9cdd616f3d6d07ce312847951ee178e874aab753a1c357c
Evidence state: complete

## Ordered target manifest

| Order | Artifact ID | Kind | Role | Path | Prior identity | Current identity | Dependencies | Commit group | Independently valid commit point |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `adr-consolidated-review-package-topology` | `adr` | `supporting` | `docs/adr/ADR-20260828-consolidated-review-package-topology.md` | absent | `sha256:1c69b99ef3d6fac92b60fd0100d576dd0743b1ed09f2b92f0755a6aa986487c9` | approved spec and accepted lifecycle ADRs | `consolidated-review-package-architecture` | yes; the ADR records the complete durable decision |
| 2 | `architecture` | `architecture` | `primary` | `docs/architecture/system/architecture.md` | `sha256:78e708c76b5f787e4f54e55d16d7abc827dd16f90ea578b4dec11f06cf93ff67` | `sha256:9cd77c439580c8ebdfbd687547b3560e169fc0382026c276efa1cbd14e93b585` | target 1 and `docs/architecture/system/diagrams/component-workflow-automation.mmd` at `sha256:9f544093d4fd686850f841920467ce09eeb077c9aa833f4bcff74e71005318d4` | `consolidated-review-package-architecture` | yes when target 1 and the diagram are present |

## Authored design

- Added explicit v1/v2 topology coexistence and a checked-revision activation manifest.
- Added deterministic design and delivery membership derived from registered artifacts.
- Defined `review-package-sha256-v1` with transient member hashes and one durable aggregate revision.
- Kept mutable status solely in `change.yaml` through compact `review_packages` projections.
- Extended the existing lifecycle command family with package review recording and atomic settlement operations.
- Added distinct Design Review and Delivery Review skill boundaries while preserving v1 compatibility skills.
- Preserved generated-adapter, Code Review, Explain Change, Verify, PR, and workflow-routing ownership.

## Validation

- The new ADR passes documentation prose validation.
- `git diff --check` passes for the architecture package.
- The canonical architecture prose validator continues to report pre-existing mechanically wrapped lines outside this change; no new inserted line uses that wrapping pattern.
- Architecture review remains required before reliance or planning.
