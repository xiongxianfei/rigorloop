# M4 Code Review R17

Review ID: code-review-m4-r17
Stage: code-review
Round: 17
Reviewer: two independent L2 Codex reviewers
Target: 4b2f843f..e1bcf9ed
Reviewed artifact: commit e1bcf9ed
Reviewed milestone: M4
Review date: 2026-07-29
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m4-r16-resolution
Reviewer context ID: m4-r17-primary-and-second-independent-agents
Context separation mechanism: separate-agents
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: token termination; variable prefixes; command phrase boundaries
Risk-tier classifier: deterministic-changed-surface-check
Governing artifacts: specs/skill-contract.md; specs/progressive-boundary-first-skill-guidance.md; specs/progressive-boundary-first-skill-guidance.test.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: governing artifacts plus commit:e1bcf9ed.diff@e1bcf9ed#sha256:053d8c349072173c3f01e18a3001c70347edd89e821b32c3ce0e7100d38fb9c7
Prompt template version: code-review-v1
Initial packet hash: sha256:053d8c349072173c3f01e18a3001c70347edd89e821b32c3ce0e7100d38fb9c7
Manifest owner: workflow-orchestrator
Affected behavior: published workflow portability classification
Highest-impact failure modes: governed-name variable prefixes reject; exact slash-command phrases escape
Changed boundaries: Unicode identifier continuation; closing math delimiter; vertical whitespace; phrase punctuation
Evidence expected: paired complete-token positives and variable/path negatives
Areas requiring direct inspection: dollar-token right boundary; slash-command terminators; mutation matrix
Areas intentionally out of scope: final holistic review, final verification, and PR
Risk classes considered: portability; normalization; maintainability
Falsifiable review questions: Do governed names inside longer variables or math delimiters remain portable; do exact slash commands terminate at structural whitespace and phrase delimiters
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Material findings: CR-M4-R17-001, CR-M4-R17-002
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Findings

### CR-M4-R17-001 — Governed names still match variable and math prefixes

Finding ID: CR-M4-R17-001
Severity: blocker
Location: `scripts/adapter_distribution.py:94-101`
Evidence: `$plan_value`, `$workflow_id`, `$spec₂`, and `$plan$` are classified as governed invocations even though they are longer variables or math notation.
Required outcome: A governed dollar invocation matches only a complete published-skill token.
Safe resolution path: Exclude Unicode word continuation, hyphens, and closing dollar delimiters at the right boundary; add paired negative and complete-token positive controls.
needs-decision rationale: none
Auto-fix class: declared-safe

### CR-M4-R17-002 — Exact slash commands escape at phrase terminators

Finding ID: CR-M4-R17-002
Severity: blocker
Location: `scripts/adapter_distribution.py:103-105`; `scripts/adapter_distribution.py:467-470`
Evidence: Exact `/workflow` followed by LF, CRLF, a code-span delimiter, or ordinary phrase punctuation is not recognized; longer route/file suffixes correctly remain portable.
Required outcome: Recognize exact slash commands at structural whitespace and safe phrase terminators without matching route, file, hyphen, or identifier continuations.
Safe resolution path: Define an explicit terminator class and add newline, code-span, and punctuation positives beside route/path negatives.
needs-decision rationale: none
Auto-fix class: declared-safe

## Requirement-fidelity receipt

Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: scripts/adapter_distribution.py; scripts/test-adapter-distribution.py
Requirement-fidelity matched path triggers: scripts/*validator*
Requirement-fidelity matched category triggers: spec-derived validators
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause > feature spec > implementation diff > validator assertions > validation evidence
Requirement-property decomposition evidence: present
Requirement-fidelity receipt: yes
Relevant spec clauses decomposed: yes
Property matrix complete: no
Multi-surface contracts identified: yes
Validator assertions checked against spec: yes
Compressed requirement risk: incomplete token termination exceeds R3l
Requirement-fidelity no-finding rationale: not-applicable because material findings exist

## Result

M4 remains open for complete-token dollar boundaries and explicit slash-command phrase terminators.
