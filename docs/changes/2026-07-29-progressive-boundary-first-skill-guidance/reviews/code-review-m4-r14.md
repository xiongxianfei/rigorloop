# M4 Code Review R14

Review ID: code-review-m4-r14
Stage: code-review
Round: 14
Reviewer: two independent L2 Codex reviewers
Target: 6203f8ac..78e782b7
Reviewed artifact: commit 78e782b7
Reviewed milestone: M4
Review date: 2026-07-29
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m4-r13-resolution
Reviewer context ID: m4-r14-primary-and-second-independent-agents
Context separation mechanism: separate-agents
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: recognized Markdown only; entity source order; visible punctuation
Risk-tier classifier: deterministic-changed-surface-check
Governing artifacts: specs/progressive-boundary-first-skill-guidance.md; specs/progressive-boundary-first-skill-guidance.test.md; docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: governing artifacts plus commit:78e782b7.diff@78e782b7#sha256:5f2cca59637de313a0b9cc15d2ec325431441cd475da6897e6544e05c979a270
Prompt template version: code-review-v1
Initial packet hash: sha256:5f2cca59637de313a0b9cc15d2ec325431441cd475da6897e6544e05c979a270
Manifest owner: workflow-orchestrator
Affected behavior: cross-adapter workflow invocation portability
Highest-impact failure modes: literal punctuation is erased or entities become synthetic Markdown
Changed boundaries: unmatched delimiters; unresolved references; entity-origin punctuation
Evidence expected: source-order recognition of only valid Markdown constructs
Areas requiring direct inspection: portability parser and positive/negative mutation matrix
Areas intentionally out of scope: final holistic review, final verification, and PR
Risk classes considered: portability; normalization; false-positive input
Falsifiable review questions: Can unmatched punctuation synthesize an adapter label; can entity-decoded punctuation become Markdown formatting
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Material findings: CR-M4-R14-001
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Finding

### CR-M4-R14-001 — Literal delimiters are treated as rendered Markdown

Finding ID: CR-M4-R14-001
Severity: blocker
Location: `scripts/adapter_distribution.py`; `scripts/test-adapter-distribution.py`
Evidence: Unmatched backticks/brackets, unresolved references, and entity-origin delimiter characters are erased and synthesize adapter labels.
Required outcome: Only recognized and resolved Markdown constructs lose delimiters; literal punctuation remains a visible boundary.
Safe resolution path: Normalize code spans, inline links, resolved references, and paired emphasis in source order before HTML entity decoding; add literal and entity negative controls.
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
Compressed requirement risk: present in recognized-versus-literal delimiter handling
Requirement-fidelity no-finding rationale: not-applicable because a material finding exists

## Result

M4 remains open for source-order recognition of Markdown constructs and literal delimiter preservation.
