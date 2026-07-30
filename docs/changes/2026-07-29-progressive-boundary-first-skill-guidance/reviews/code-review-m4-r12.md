# M4 Code Review R12

Review ID: code-review-m4-r12
Stage: code-review
Round: 12
Reviewer: two independent L2 Codex reviewers
Target: 490fa65f..b0eec089
Reviewed artifact: commit b0eec089
Reviewed milestone: M4
Review date: 2026-07-29
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m4-r11-resolution
Reviewer context ID: m4-r12-primary-and-second-independent-agents
Context separation mechanism: separate-agents
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: visible-boundary preservation; control ordering; false-positive portability
Risk-tier classifier: deterministic-changed-surface-check
Governing artifacts: specs/progressive-boundary-first-skill-guidance.md; specs/progressive-boundary-first-skill-guidance.test.md; docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: governing artifacts plus commit:b0eec089.diff@b0eec089#sha256:d3a324a133b2fe044cfa24854976ea6f9b8212af0a43dadaba0f6dbdafb4ec0b
Prompt template version: code-review-v1
Initial packet hash: sha256:d3a324a133b2fe044cfa24854976ea6f9b8212af0a43dadaba0f6dbdafb4ec0b
Manifest owner: workflow-orchestrator
Affected behavior: cross-adapter workflow invocation portability
Highest-impact failure modes: projection invents labels or whitespace folding hides control-split invocations
Changed boundaries: visible punctuation; non-ASCII text; controls; Markdown emphasis
Evidence expected: boundary-preserving rendered normalization with positive and negative controls
Areas requiring direct inspection: portability parser and mutation matrix
Areas intentionally out of scope: final holistic review, final verification, and PR
Risk classes considered: portability; normalization; false-positive input
Falsifiable review questions: Can visible portable prose synthesize an adapter label; can whitespace-classified controls split an invocation
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Material findings: CR-M4-R12-001, CR-M4-R12-002
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Findings

### CR-M4-R12-001 — Projection synthesizes labels from visible portable prose

Finding ID: CR-M4-R12-001
Severity: blocker
Location: `scripts/adapter_distribution.py`; `scripts/test-adapter-distribution.py`
Evidence: Removing every visible separator turns benign `Encode X`, `open code`, `open-code`, and `cod_ex` text into adapter-label substrings.
Required outcome: Ordinary visible whitespace, punctuation, identifiers, and non-ASCII characters remain boundaries.
Safe resolution path: Remove only governed non-rendering characters, normalize paired Markdown constructs contextually, and add benign negative controls.
needs-decision rationale: none
Auto-fix class: declared-safe

### CR-M4-R12-002 — Whitespace folding hides control-split invocations

Finding ID: CR-M4-R12-002
Severity: blocker
Location: `scripts/adapter_distribution.py`; `scripts/test-adapter-distribution.py`
Evidence: C0 and NEL controls classified as whitespace become ordinary spaces before slash-invocation detection.
Required outcome: Non-rendering controls are removed before structural whitespace normalization and invocation matching.
Safe resolution path: Normalize non-rendering characters first, preserve visible non-ASCII boundaries, and run syntax checks on the resulting text.
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
Compressed requirement risk: present in positive and negative normalization boundaries
Requirement-fidelity no-finding rationale: not-applicable because material findings exist

## Result

M4 remains open for boundary-preserving rendered normalization and control-first syntax checking.
