# Boundary-First Proof Modeling Architecture Review R5

Review ID: architecture-review-r5
Stage: architecture-review
Round: 5
Reviewer: Codex architecture-review skill with context-separated independent reviewer
Target: M2 runtime-attestation architecture revision
Reviewed artifact: docs/architecture/system/architecture.md; docs/architecture/system/diagrams/component-boundary-proof.mmd; docs/adr/ADR-20260726-codex-permission-profile-boundary-harness.md
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-26
Recording status: recorded
Material findings: BFP-AR5, BFP-AR6, BFP-AR7, BFP-AR8
Immediate next stage: architecture revision
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: boundary-first-runtime-architecture-author
Reviewer context ID: boundary-first-architecture-r5-independent-reviewer
Context separation mechanism: separate-agent
Author context excluded: true
Risk tier: critical
Risk-tier triggers: runtime sandbox, experimental protocol, credentials, managed configuration, tools, connectors, subagents, and network
Risk-tier classifier: security-and-external-runtime-boundary
Governing artifacts: specs/rigorloop-workflow.md; specs/rigorloop-workflow.test.md; docs/adr/ADR-20260725-boundary-first-proof-modeling.md; docs/plans/2026-07-25-boundary-first-proof-modeling.md; validation-m2.md
Formal criteria: R28y; T48-T50; accepted hermetic behavior trust boundary
Initial packet inventory: specs/rigorloop-workflow.md@70c6ffb3#sha256:cce7047761aaa99d81263cf226261e73de3de35e9064e93732274d3a3a8ae1f8; specs/rigorloop-workflow.test.md@70c6ffb3#sha256:94fdf3da61d35647596d550eaa0527d130daf49ca3af2cf7ff933e330f860f91; docs/adr/ADR-20260725-boundary-first-proof-modeling.md@70c6ffb3#sha256:58cf98aa38f3de6605aba5a14fe3c59514a2f93ba6cc514698f7d07355891519
Prompt template version: review-gate/v1
Initial packet hash: sha256:5c574701d7cb0f9e76cc5f64f16d0655d2f6ba971780fef68a5d8c831a989a2c
Manifest owner: workflow orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded
Clean-review sufficiency receipt: no

Affected behavior: the child-runtime trust boundary and the evidence accepted before real lifecycle-skill execution.
Highest-impact failure modes: undeclared runtime tools remain available; experimental fields drift; probe and thread use different policy; credential material reaches child commands.
Changed boundaries: Codex permission profiles, app-server protocol, managed requirements, control-plane authentication, and C4 evidence flow.
Evidence expected: runtime-owned effective config and inventories, exact experimental schema, profile equivalence, managed-policy binding, and canary-based secret isolation.
Areas requiring direct inspection: canonical architecture, proposed runtime ADR, component diagram, generated app-server schema, and local permission-profile behavior.
Areas intentionally out of scope: spec relaxation, full M2 implementation, skill mutation, publication, M3-M4, and verification.
Risk classes considered: capability closure, protocol drift, profile provenance, managed config, credential leakage, evidence overclaim, and C4 consistency.
Falsifiable review questions: can disabled config still expose a tool; can optional metadata disappear; can sandbox omit managed constraints; can auth reach environment/argv/stdin/process files?

## Findings

### BFP-AR5: Runtime capability closure is asserted

Finding ID: BFP-AR5
- Severity: blocker
- Status: open
- Location: canonical architecture and proposed runtime ADR
- Evidence: `thread/start` does not enumerate tools, connectors, plugins, MCP servers, or subagent capability.
- Required outcome: Bind runtime-owned effective configuration and exact capability inventories before the turn; reject extras.
- Safe resolution path: Require `config/read`, `app/list`, `plugin/list`, `mcpServerStatus/list`, and `skills/list`, plus unexpected tool-event rejection.
- auto_fix_class: declared-safe
- deterministic_recipe: define exact empty inventories and exact five-skill inventory from the manifest
- named_inputs: generated config, manifest-bound skills, runtime inventory responses
- named_outputs: typed capability-closure receipt
- allowed_paths: architecture; proposed ADR; diagram; change-local review evidence
- forbidden_paths: specs; skills; production harness
- acceptance_criteria: no config assertion alone can satisfy capability closure
- required_validation: architecture-review-r6
- needs-decision rationale: none

### BFP-AR6: Experimental protocol identity is undefined

Finding ID: BFP-AR6
- Severity: blocker
- Status: open
- Location: proposed runtime ADR and canonical trust-boundary flow
- Evidence: permission-profile fields require experimental API negotiation and are optional in the generated schema.
- Required outcome: Bind exact experimental schema and fail on missing, null, extra, or incompatible protocol fields.
- Safe resolution path: Generate schema with the identified executable, initialize with `experimentalApi: true`, hash the bundle, and validate exact methods/fields.
- auto_fix_class: declared-safe
- deterministic_recipe: schema generation, canonical bundle identity, closed required-method and field projection
- named_inputs: identified runtime executable and experimental schema bundle
- named_outputs: schema identity and protocol compatibility decision
- allowed_paths: architecture; proposed ADR; diagram; change-local review evidence
- forbidden_paths: specs; skills; production harness
- acceptance_criteria: version floor alone never proves protocol support
- required_validation: architecture-review-r6
- needs-decision rationale: none

### BFP-AR7: Profile equivalence and auth isolation are underproved

Finding ID: BFP-AR7
- Severity: blocker
- Status: open
- Location: hermetic trust boundary and proposed runtime ADR
- Evidence: profile ID exposes no effective rules; sandbox probes omitted managed configuration; auth-path denial does not prove environment, argv, stdin, or process isolation.
- Required outcome: Bind generated and managed config across both paths and prove credential absence from all command-visible channels.
- Safe resolution path: use `--include-managed-config`, runtime-owned config reads, exact identities, a transient canary, exact environment-name allowlist, and argv/stdin/process denial.
- auto_fix_class: declared-safe
- deterministic_recipe: compare config identities and effective profile; inject canary; run closed negative probes; persist typed result only
- named_inputs: generated config, managed requirements, permission profile, transient canary
- named_outputs: profile-equivalence and credential-isolation receipts
- allowed_paths: architecture; proposed ADR; diagram; change-local review evidence
- forbidden_paths: specs; skills; production harness
- acceptance_criteria: no private value or path enters durable evidence and all child-visible channels reject the canary
- required_validation: architecture-review-r6
- needs-decision rationale: none

### BFP-AR8: Canonical decision package overstates and omits the new ADR

Finding ID: BFP-AR8
- Severity: major
- Status: open
- Location: canonical Architecture Decisions and component-boundary-proof.mmd
- Evidence: the proposed ADR was not linked and the diagram summarized only probes plus thread metadata.
- Required outcome: Link the ADR and depict schema, effective config/inventory, managed-profile, and probe evidence.
- Safe resolution path: add the decision link and correct the runtime-adapter evidence arrow.
- auto_fix_class: mechanical
- auto_fix_kind: architecture-projection
- affected_paths: architecture.md; component-boundary-proof.mmd
- deterministic_authority: accepted R28y and the proposed refinement ADR
- required_validation: architecture-review-r6
- needs-decision rationale: none

## Result

Review status: changes-requested
Spec reopening: not required
M2 handoff: blocked
