# Boundary-First Proof Modeling Architecture Review R6

Review ID: architecture-review-r6
Stage: architecture-review
Round: 6
Reviewer: Codex architecture-review skill with context-separated independent reviewer
Target: M2 runtime-attestation architecture revision
Reviewed artifact: docs/architecture/system/architecture.md; docs/architecture/system/diagrams/component-boundary-proof.mmd; docs/adr/ADR-20260726-codex-permission-profile-boundary-harness.md
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-26
Recording status: recorded
Material findings: BFP-AR9
Immediate next stage: architecture revision
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: boundary-first-runtime-architecture-author
Reviewer context ID: boundary-first-architecture-r6-independent-reviewer
Context separation mechanism: separate-agent
Author context excluded: true
Risk tier: critical
Risk-tier triggers: runtime sandbox, experimental features, built-in tools, connectors, subagents, and network
Risk-tier classifier: security-and-external-runtime-boundary
Governing artifacts: specs/rigorloop-workflow.md; specs/rigorloop-workflow.test.md; docs/adr/ADR-20260725-boundary-first-proof-modeling.md; docs/plans/2026-07-25-boundary-first-proof-modeling.md; validation-m2.md
Formal criteria: R28y; T48-T50; accepted hermetic behavior trust boundary
Initial packet inventory: docs/architecture/system/architecture.md@70c6ffb39c8950b4834ae1922d434eedb597a3f4#sha256:a21aa81df114d0586b0f9218b196cbd0c23af44ced65953985441b2091c5cf76; docs/architecture/system/diagrams/component-boundary-proof.mmd@70c6ffb39c8950b4834ae1922d434eedb597a3f4#sha256:423640dda5e78626f418116818ee13972361e729a71d53ca1b73b591610817cd; docs/adr/ADR-20260726-codex-permission-profile-boundary-harness.md@70c6ffb39c8950b4834ae1922d434eedb597a3f4#sha256:8e1099c3438ea0160446fdaeec7b39db8599738cddd85f74aa64b657f6809d5a
Prompt template version: review-gate/v1
Initial packet hash: sha256:078a0f06179389e3f5ae7455dfd679cab265bd9400904df4a9ea64f04eb6feb3
Manifest owner: workflow orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded
Clean-review sufficiency receipt: no

Affected behavior: the child runtime's model-visible tool surface before any lifecycle turn starts.
Highest-impact failure modes: an unenumerated built-in tool remains enabled; a later feature row is omitted by pagination; a newly enabled tool-bearing feature bypasses the closed capability boundary.
Changed boundaries: Codex experimental feature inventory, generated protocol schema, thread-start dynamic capabilities, and pre-turn acceptance.
Evidence expected: a fully paginated feature inventory, an exact permitted built-in tool set, exhaustive feature classification, and unknown-value rejection before turn start.
Areas requiring direct inspection: canonical architecture, proposed runtime ADR, and generated app-server schema.
Areas intentionally out of scope: spec relaxation, M2 implementation, skill mutation, publication, M3-M4, and verification.
Risk classes considered: incomplete inventory, protocol drift, pagination loss, unknown feature activation, and post-hoc-only rejection.
Falsifiable review questions: can an enabled tool-bearing feature be absent from the accepted inventory; can an unknown feature pass; can dynamic tools or environments be added at thread start?

## Findings

### BFP-AR9: Pre-turn built-in tool closure is incomplete

Finding ID: BFP-AR9
- Severity: blocker
- Status: open
- Location: canonical hermetic behavior trust boundary and proposed runtime ADR
- Evidence: the current app-server schema exposes no generic `tool/list`, `config/read` is partial, and the architecture does not require fully paginated `experimentalFeature/list` evidence or an exhaustive mapping from enabled features to the permitted built-in tool set.
- Required outcome: Define the exact model-visible built-in tool set and prove every feature row is exhaustively classified before `turn/start`.
- Safe resolution path: Require fully paginated `experimentalFeature/list`; bind the generated protocol schema; permit only sandboxed command execution and isolated-workspace file change; prohibit dynamic tools, environments, apps, plugins, MCP/connectors, subagents, goals, browser/computer/image/search, realtime/remote, and external-environment capabilities; fail closed on missing, unknown, or newly enabled rows.
- auto_fix_class: declared-safe
- deterministic_recipe: add a closed version/schema-bound feature classification and reject any row or protocol item outside the two permitted side-effect classes
- named_inputs: generated schema identity, fully paginated feature rows, thread-start parameters, runtime-owned capability inventories
- named_outputs: typed pre-turn capability-closure decision
- allowed_paths: architecture; proposed ADR; change-local review evidence
- forbidden_paths: specs; skills; production harness
- acceptance_criteria: no post-hoc event filter or partial config projection can independently satisfy built-in tool closure
- required_validation: architecture-review-r7
- needs-decision rationale: none

## Result

Review status: changes-requested
Spec reopening: not required
M2 handoff: blocked
Immediate next stage: architecture revision followed by architecture-review-r7
