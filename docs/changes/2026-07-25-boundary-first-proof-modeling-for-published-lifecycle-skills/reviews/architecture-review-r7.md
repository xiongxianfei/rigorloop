# Boundary-First Proof Modeling Architecture Review R7

Review ID: architecture-review-r7
Stage: architecture-review
Round: 7
Reviewer: Codex architecture-review skill with context-separated independent reviewer
Target: M2 runtime-attestation architecture revision
Reviewed artifact: docs/architecture/system/architecture.md; docs/architecture/system/diagrams/component-boundary-proof.mmd; docs/adr/ADR-20260726-codex-permission-profile-boundary-harness.md
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-26
Recording status: recorded
Material findings: BFP-AR10
Immediate next stage: architecture revision
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: boundary-first-runtime-architecture-author
Reviewer context ID: boundary-first-architecture-r7-independent-reviewer
Context separation mechanism: separate-agent
Author context excluded: true
Risk tier: critical
Risk-tier triggers: runtime sandbox, experimental protocol vocabulary, effective capabilities, and prohibited events
Risk-tier classifier: security-and-external-runtime-boundary
Governing artifacts: specs/rigorloop-workflow.md; specs/rigorloop-workflow.test.md; docs/adr/ADR-20260725-boundary-first-proof-modeling.md; docs/plans/2026-07-25-boundary-first-proof-modeling.md; validation-m2.md
Formal criteria: R28y; T48-T50; accepted hermetic behavior trust boundary
Initial packet inventory: docs/architecture/system/architecture.md@70c6ffb39c8950b4834ae1922d434eedb597a3f4#sha256:06e79aee80c0e3f7f43374b55c06b12f07853b89eae79e06821b38210ca24141; docs/architecture/system/diagrams/component-boundary-proof.mmd@70c6ffb39c8950b4834ae1922d434eedb597a3f4#sha256:423640dda5e78626f418116818ee13972361e729a71d53ca1b73b591610817cd; docs/adr/ADR-20260726-codex-permission-profile-boundary-harness.md@70c6ffb39c8950b4834ae1922d434eedb597a3f4#sha256:0d25af7e0a1050b9e3fc3660e2d732fc0d97ee9e03a576858b551e05dca3d11c
Prompt template version: review-gate/v1
Initial packet hash: sha256:4e8892a8e878384673ced7abd51b4d78c6c5ed9e159bf3d8d52f936648fe9aee
Manifest owner: workflow orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded
Clean-review sufficiency receipt: no

Affected behavior: the relationship between supported protocol vocabulary and effectively enabled child capabilities.
Highest-impact failure modes: the feasibility gate rejects every supported current runtime because disabled protocol variants still exist in its schema.
Changed boundaries: generated experimental schema, pre-turn capability closure, and in-turn event validation.
Evidence expected: complete schema identity, exhaustive item classification, pre-turn disabled-capability proof, and prohibited-event rejection.
Areas requiring direct inspection: canonical architecture, proposed runtime ADR, generated app-server schema, and R6 correction.
Areas intentionally out of scope: spec relaxation, M2 implementation, skill mutation, publication, M3-M4, and verification.
Risk classes considered: schema/capability conflation, unconditional environment rejection, and event-surface drift.
Falsifiable review questions: can a schema-supported but disabled capability cause either false acceptance or unconditional rejection?

## Findings

### BFP-AR10: Protocol vocabulary is conflated with effective enablement

Finding ID: BFP-AR10
- Severity: blocker
- Status: open
- Location: canonical hermetic behavior trust boundary and proposed runtime ADR
- Evidence: Codex 0.144.6's generated experimental schema necessarily declares item variants for disabled capabilities such as MCP, web search, image generation, and subagent activity, while the architecture requires the schema itself to contain only the two permitted side-effect classes.
- Required outcome: Distinguish protocol vocabulary support from effective runtime capability without weakening pre-turn closure.
- Safe resolution path: Bind and classify the complete schema; prove prohibited capabilities disabled through pre-turn feature, configuration, and inventory evidence; reject any observed prohibited event during the accepted turn.
- auto_fix_class: declared-safe
- deterministic_recipe: replace schema-absence enforcement with complete variant classification plus effective-disablement and observed-event checks
- named_inputs: generated schema identity, feature/configuration/inventory evidence, accepted-turn events
- named_outputs: schema compatibility, pre-turn capability closure, and event-conformance decisions
- allowed_paths: architecture; proposed ADR; change-local review evidence
- forbidden_paths: specs; skills; production harness
- acceptance_criteria: supported-but-disabled protocol variants neither authorize a capability nor make the intended runtime unconditionally unavailable
- required_validation: architecture-review-r8
- needs-decision rationale: none

## Result

Review status: changes-requested
BFP-AR9: resolved
Spec reopening: not required
M2 handoff: blocked
Immediate next stage: architecture revision followed by architecture-review-r8
