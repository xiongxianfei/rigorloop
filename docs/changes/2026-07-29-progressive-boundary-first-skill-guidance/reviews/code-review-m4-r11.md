# M4 Code Review R11

Review ID: code-review-m4-r11
Stage: code-review
Round: 11
Reviewer: two independent L2 Codex reviewers
Target: af44db0a..8c9ffef6
Reviewed artifact: commit 8c9ffef6
Reviewed milestone: M4
Review date: 2026-07-29
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m4-r10-resolution
Reviewer context ID: m4-r11-primary-and-second-independent-agents
Context separation mechanism: separate-agents
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: literal whitespace; Unicode label projection; fail-closed parsing
Risk-tier classifier: deterministic-changed-surface-check
Governing artifacts: specs/progressive-boundary-first-skill-guidance.md; specs/progressive-boundary-first-skill-guidance.test.md; docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: governing artifacts plus commit:8c9ffef6.diff@8c9ffef6#sha256:0c90dea9ed509590edb6bcd411b320e38f66a05f1c2602b8c65fdf8e5d682b37
Prompt template version: code-review-v1
Initial packet hash: sha256:0c90dea9ed509590edb6bcd411b320e38f66a05f1c2602b8c65fdf8e5d682b37
Manifest owner: workflow-orchestrator
Affected behavior: cross-adapter workflow invocation portability
Highest-impact failure modes: whitespace folding approves nonliteral commands or invisible characters split labels
Changed boundaries: raw list records; Unicode residual labels
Evidence expected: byte-exact records and conservative ASCII label projection
Areas requiring direct inspection: portability parser and mutation matrix
Areas intentionally out of scope: final holistic review, final verification, and PR
Risk classes considered: portability; normalization; fail-closed input
Falsifiable review questions: Can non-ASCII whitespace satisfy an approved raw record; can any non-ASCII character split a residual adapter label
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Material findings: CR-M4-R11-001, CR-M4-R11-002
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Findings

### CR-M4-R11-001 — Whitespace folding bypasses exact source validation

Finding ID: CR-M4-R11-001
Severity: blocker
Location: `scripts/adapter_distribution.py`; `scripts/test-adapter-distribution.py`
Evidence: NBSP, EM SPACE, and tab separators in Claude or OpenCode records are folded to canonical ASCII spaces before comparison.
Required outcome: The three approved Markdown list records match literal source, including ASCII whitespace and wrapping.
Safe resolution path: Compare each captured raw list record byte-for-byte with its canonical multiline source.
needs-decision rationale: none
Auto-fix class: declared-safe

### CR-M4-R11-002 — Invisible controls and Hangul fillers split residual labels

Finding ID: CR-M4-R11-002
Severity: blocker
Location: `scripts/adapter_distribution.py`; `scripts/test-adapter-distribution.py`
Evidence: C0 controls and default-ignorable Hangul fillers remain between visible OpenCode fragments and evade word-boundary matching.
Required outcome: No intervening non-ASCII or formatting character can split a residual ASCII adapter label.
Safe resolution path: Match adapter labels on a conservative ASCII-alphanumeric projection of rendered remaining text and add control and Hangul-filler regressions.
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
Compressed requirement risk: present in literal whitespace and residual-label projection
Requirement-fidelity no-finding rationale: not-applicable because material findings exist

## Result

M4 remains open for byte-exact approved records and conservative residual-label projection.
