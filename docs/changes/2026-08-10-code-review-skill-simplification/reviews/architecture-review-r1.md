# Code-Review Skill Simplification Architecture Review R1

Review ID: architecture-review-r1
Stage: architecture-review
Round: r1
Reviewer: Codex independent architecture-review context
Target: `docs/architecture/system/architecture.md`
Review date: 2026-08-10
Status: changes-requested
Material findings: CRSIM-AR1

## Result

- Review surface: canonical-architecture-update
- Review status: changes-requested
- Material findings: CRSIM-AR1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-10-code-review-skill-simplification/reviews/architecture-review-r1.md`
- Review log: `docs/changes/2026-08-10-code-review-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-10-code-review-skill-simplification/review-resolution.md#CRSIM-AR1`
- Open blockers: CRSIM-AR1
- Required canonical updates: make installed supported-target parity deterministic even when materialization is pure copy
- Required ADR updates: none
- Next stage: review-resolution

## Finding CRSIM-AR1

Finding ID: CRSIM-AR1
Finding: The architecture weakens installed-target proof from mandatory package coverage to an optional check based on installer complexity.
Location: `docs/architecture/system/architecture.md`, `Level 2 White-Box: Code-Review Skill Package`, `Code-review package loading and simplification flow`, and `Published-skill target deployment boundary`
Severity: material
Evidence: Spec R21 requires every canonical, generated, packed, and installed supported package target to contain every mapped reference and asset with required raw-byte parity. The architecture says installer inspection remains conditional on materialization logic beyond copying, and says a pure-copy install adds no distinct acceptance layer. Package/archive parity demonstrates source bytes but does not directly establish the installed supported target named by R21.
Required outcome: Define deterministic installed-tree parity for every supported installed target while retaining the prohibition on target-agent execution. Pure-copy installation may use a local archive extraction or copy fixture followed by filesystem inventory, relative-path, and raw-byte identity comparison; additional materialization logic may use the existing bounded filesystem smoke.
Safe resolution path: Amend the four affected architecture passages so Gate B or the installer-filesystem proof deterministically materializes each supported package into a temporary tree and compares mapped resources. Keep the proof repository-local, network-free, and model-free; do not create a fourth semantic gate or a new validator family.
needs-decision rationale: none

## Review dimensions

| Dimension | Verdict | Notes |
| --- | --- | --- |
| Spec alignment | block | R21 installed-target proof is weaker in the architecture. |
| Package shape | pass | Focused canonical update is the correct surface. |
| Boundary clarity | pass | Inline, conditional reference, asset, ledger, and semantic-review ownership are clear. |
| Data ownership | pass | No new persisted product data; ledger ownership is change-local. |
| Interface safety | concern | Installed package equivalence needs a direct proof boundary. |
| Runtime and failure handling | pass | Conditional loading, partial package failure, and rollback are explicit. |
| Deployment and execution boundaries | block | Pure-copy installed targets are not directly covered. |
| Security/privacy | pass | The design is local and excludes credentials, prompts, transcripts, and network runtime calls. |
| Quality and operations | pass | Maintenance footprint and common-path cost are separated. |
| Testing feasibility | concern | The missing installed-tree fixture is deterministic and feasible. |
| Complexity discipline | pass | No new service, validator family, scheduler, cache, or runtime system. |
| ADR quality | pass | Existing resource-integrity and product-gate ADRs own the durable decisions. |
| Plan readiness | block | Planning would otherwise be free to omit R21's installed-target proof. |

The architecture should be corrected and rereviewed before planning.
