# Architecture Authoring Evidence

Stage: architecture
Artifact: `docs/architecture/system/architecture.md`
Date: 2026-08-10

## Result

Architecture surface: canonical-update

The canonical architecture now specializes the existing published-skill resource-integrity and product-gate architecture for the `code-review` package. It defines universal-inline versus conditional-reference ownership, asset boundaries, the rule-disposition ledger role, conditional loading, deterministic and semantic proof separation, atomic package deployment, and rollback.

## Changed architecture sections

- Related artifacts
- Building Block View: `Level 2 White-Box: Code-Review Skill Package`
- Runtime View: `Code-review package loading and simplification flow`
- Deployment View: `Published-skill target deployment boundary`
- Crosscutting Concepts: `Code-review package composition`

No C4 diagram changes are required because the existing published-skill validation component diagram already shows canonical packages, Gate A, Gate B, supported targets, semantic review, and target-runtime exclusion. The change specializes ownership and loading inside one package rather than adding a component or interaction.

No new ADR is required. The package composition, mapped-resource identity, generated-target parity, deterministic acceptance boundary, and semantic-review responsibility are already durable decisions in `ADR-20260623-published-skill-resource-integrity` and `ADR-20260810-published-skill-first-validation-architecture`. This update applies those decisions to one skill without adding a new source of truth, runtime, persistence model, validation family, or release boundary.

## Requirement mapping

| Spec requirements | Architecture owner |
| --- | --- |
| R1-R7 | Code-review package building block and composition boundary |
| R8-R14 | Rule-disposition ledger and separate measurement scopes |
| R15-R20 | Deterministic Gate A/Gate B proof plus independent semantic review; target runtimes excluded |
| R21-R22 | Published-skill resource integrity and generated package parity |
| R23 | Sole `code-review` semantic and lifecycle ownership |
| R24 | Recorded architecture assessment and this canonical update |
| R25 | Atomic package deployment and complete-package rollback |

## Readiness

Ready for `architecture-review`. No direction or specification blocker remains.
