# M4 Code Review R6

Review ID: code-review-m4-r6
Stage: code-review
Round: 6
Reviewer: two independent L2 Codex reviewers
Target: 4052f86a..57d2a5ec
Reviewed artifact: commit 57d2a5ec
Reviewed milestone: M4
Review date: 2026-07-29
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m4-r5-resolution
Reviewer context ID: m4-r6-primary-and-second-independent-agents
Context separation mechanism: separate-agents
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: adapter label closure; HTML normalization; fail-closed parsing
Risk-tier classifier: deterministic-changed-surface-check
Governing artifacts: specs/progressive-boundary-first-skill-guidance.md; specs/progressive-boundary-first-skill-guidance.test.md; docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: governing artifacts plus commit:57d2a5ec.diff@57d2a5ec#sha256:90925fdfa37ad6056d7d443c751ee27a2ba432bf2fda9799bac823b25474e01d
Prompt template version: code-review-v1
Initial packet hash: sha256:90925fdfa37ad6056d7d443c751ee27a2ba432bf2fda9799bac823b25474e01d
Manifest owner: workflow-orchestrator
Affected behavior: residual adapter-labeled invocation detection
Highest-impact failure modes: verb, identity, operation, formatting, or entity changes hide an occurrence
Changed boundaries: adapter labels; HTML entities; arbitrary prose verbs
Evidence expected: exact-block subtraction followed by residual-label rejection
Areas requiring direct inspection: portability parser and mutation matrix
Areas intentionally out of scope: final holistic review, final verification, and PR
Risk classes considered: portability; normalization; fail-closed input
Falsifiable review questions: Can any residual adapter label survive; can HTML encoding hide a Codex invocation
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Material findings: CR-M4-R6-001
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Finding

### CR-M4-R6-001 — Residual adapter-label closure depends on incomplete syntax

Finding ID: CR-M4-R6-001
Severity: blocker
Location: `scripts/adapter_distribution.py`; `scripts/test-adapter-distribution.py`
Evidence: Codex-labeled composed forms, HTML entities, and Claude/OpenCode forms using unlisted verbs or noun syntax remain portable.
Required outcome: After removing the one exact approved equivalence block, reject every residual Codex, Claude, or OpenCode label and normalize HTML entities first.
Safe resolution path: Decode HTML, remove markup, subtract the exact block, and fail on any case-insensitive residual adapter label or dollar/slash invocation.
needs-decision rationale: none
Auto-fix class: declared-safe

## Requirement-fidelity receipt

Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: scripts/adapter_distribution.py; scripts/test-adapter-distribution.py; skills/workflow/SKILL.md
Requirement-fidelity matched path triggers: skills/; scripts/*validator*
Requirement-fidelity matched category triggers: skill instructions derived from specs; spec-derived validators
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause > decomposition > implementation diff > validator assertions > validation evidence
Requirement-property decomposition evidence: present
Requirement-fidelity receipt: yes
Relevant spec clauses decomposed: yes
Property matrix complete: no
Multi-surface contracts identified: yes
Validator assertions checked against spec: yes
Compressed requirement risk: present in residual-label closure
Requirement-fidelity no-finding rationale: not-applicable because a material finding exists

## Result

M4 remains open for exact-block subtraction and residual adapter-label closure.
