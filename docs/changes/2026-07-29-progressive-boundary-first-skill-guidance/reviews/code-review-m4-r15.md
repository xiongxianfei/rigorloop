# M4 Code Review R15

Review ID: code-review-m4-r15
Stage: code-review
Round: 15
Reviewer: two independent L2 Codex reviewers
Target: 267362b5..1a141f2a
Reviewed artifact: commit 1a141f2a
Reviewed milestone: M4
Review date: 2026-07-29
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m4-r14-resolution
Reviewer context ID: m4-r15-primary-and-second-independent-agents
Context separation mechanism: separate-agents
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: reference block context; narrow static scope; checker complexity
Risk-tier classifier: deterministic-changed-surface-check
Governing artifacts: specs/skill-contract.md; specs/progressive-boundary-first-skill-guidance.md; specs/progressive-boundary-first-skill-guidance.test.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: governing artifacts plus commit:1a141f2a.diff@1a141f2a#sha256:ebf10120ca2f54210df9b78ca5fc8b4e81b347ed845590a6426516b085fb7011
Prompt template version: code-review-v1
Initial packet hash: sha256:ebf10120ca2f54210df9b78ca5fc8b4e81b347ed845590a6426516b085fb7011
Manifest owner: workflow-orchestrator
Affected behavior: published workflow portability classification
Highest-impact failure modes: partial CommonMark emulation creates false positives and negatives
Changed boundaries: multiline references; block containers; fences; images; hidden definitions
Evidence expected: contract-aligned narrow static checks rather than rendered-prose interpretation
Areas requiring direct inspection: portability parser; skill-contract R3l; mutation matrix
Areas intentionally out of scope: final holistic review, final verification, and PR
Risk classes considered: portability; normalization; maintainability
Falsifiable review questions: Does the checker emulate Markdown beyond narrow phrase/path validation; can block context change its classification
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Material findings: CR-M4-R15-001
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Finding

### CR-M4-R15-001 — Reference handling requires a Markdown block parser

Finding ID: CR-M4-R15-001
Severity: blocker
Location: `scripts/adapter_distribution.py`; `scripts/test-adapter-distribution.py`
Evidence: Multiline/container definitions, fenced pseudo-definitions, non-rendering definitions, and reference images produce contradictory classifications.
Required outcome: Portability validation obeys R3l's narrow phrase/path boundary without partial rendered-Markdown semantics.
Safe resolution path: Retain byte-exact approved workflow records and narrow raw dollar/slash invocation checks; remove residual adapter-label rendering and its speculative CommonMark matrix.
needs-decision rationale: none
Auto-fix class: declared-safe

## Requirement-fidelity receipt

Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: scripts/adapter_distribution.py; scripts/test-adapter-distribution.py; skills/workflow/SKILL.md
Requirement-fidelity matched path triggers: skills/; scripts/*validator*
Requirement-fidelity matched category triggers: skill instructions derived from specs; spec-derived validators
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause > feature spec > implementation diff > validator assertions > validation evidence
Requirement-property decomposition evidence: present
Requirement-fidelity receipt: yes
Relevant spec clauses decomposed: yes
Property matrix complete: no
Multi-surface contracts identified: yes
Validator assertions checked against spec: yes
Compressed requirement risk: partial Markdown parsing exceeds R3l
Requirement-fidelity no-finding rationale: not-applicable because a material finding exists

## Result

M4 remains open for removal of rendered-Markdown semantics from the narrow published-skill portability check.
