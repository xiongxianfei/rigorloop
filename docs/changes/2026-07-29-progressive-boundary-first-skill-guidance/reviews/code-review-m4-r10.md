# M4 Code Review R10

Review ID: code-review-m4-r10
Stage: code-review
Round: 10
Reviewer: two independent L2 Codex reviewers
Target: 4c08b788..f970d7e0
Reviewed artifact: commit f970d7e0
Reviewed milestone: M4
Review date: 2026-07-29
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m4-r9-resolution
Reviewer context ID: m4-r10-primary-and-second-independent-agents
Context separation mechanism: separate-agents
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: strict equivalence source; default-ignorable Unicode; fail-closed parsing
Risk-tier classifier: deterministic-changed-surface-check
Governing artifacts: specs/progressive-boundary-first-skill-guidance.md; specs/progressive-boundary-first-skill-guidance.test.md; docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: governing artifacts plus commit:f970d7e0.diff@f970d7e0#sha256:d05299152d40d5014cd3cbd07fff2fd597dd6e4a8faddbd9333f6e0a5e55af73
Prompt template version: code-review-v1
Initial packet hash: sha256:d05299152d40d5014cd3cbd07fff2fd597dd6e4a8faddbd9333f6e0a5e55af73
Manifest owner: workflow-orchestrator
Affected behavior: cross-adapter workflow invocation portability
Highest-impact failure modes: rendering canonicalizes invalid command source or invisible marks split labels
Changed boundaries: code-span source; placeholder syntax; Unicode combining and variation marks
Evidence expected: strict literal equivalence records plus separate rendered residual normalization
Areas requiring direct inspection: portability parser and mutation matrix
Areas intentionally out of scope: final holistic review, final verification, and PR
Risk classes considered: portability; normalization; fail-closed input
Falsifiable review questions: Can rendered normalization approve a nonliteral invocation record; can an invisible combining or variation mark hide an adapter label
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Material findings: CR-M4-R10-001, CR-M4-R10-002
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Findings

### CR-M4-R10-001 — Rendered text substitutes for exact equivalence source

Finding ID: CR-M4-R10-001
Severity: blocker
Location: `scripts/adapter_distribution.py`; `scripts/test-adapter-distribution.py`
Evidence: HTML parsing, entity decoding, and invisible-character removal canonicalize nonliteral Claude/OpenCode identities, operations, and placeholder syntax before approval.
Required outcome: Approved equivalence semantics require exact literal Markdown code-span records independently of rendered residual-label normalization.
Safe resolution path: Validate the exact raw code-span multiset for Codex, Claude, OpenCode, and declared placeholders before using rendered text only for residual discovery.
needs-decision rationale: none
Auto-fix class: declared-safe

### CR-M4-R10-002 — Invisible combining and variation marks hide adapter labels

Finding ID: CR-M4-R10-002
Severity: blocker
Location: `scripts/adapter_distribution.py`; `scripts/test-adapter-distribution.py`
Evidence: Combining grapheme joiner and variation selectors, including entity forms, remain between visible label fragments and evade the residual-label regex.
Required outcome: Residual-label normalization removes default-ignorable combining and variation marks.
Safe resolution path: Remove the explicit CGJ and variation-selector ranges and add literal and entity regressions.
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
Compressed requirement risk: present in strict-source and rendered-label separation
Requirement-fidelity no-finding rationale: not-applicable because material findings exist

## Result

M4 remains open for strict literal equivalence records and explicit default-ignorable mark removal.
