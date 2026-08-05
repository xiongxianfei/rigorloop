# M4 Code Review R9

Review ID: code-review-m4-r9
Stage: code-review
Round: 9
Reviewer: two independent L2 Codex reviewers
Target: 68a33089..8312f2c1
Reviewed artifact: commit 8312f2c1
Reviewed milestone: M4
Review date: 2026-07-29
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m4-r8-resolution
Reviewer context ID: m4-r9-primary-and-second-independent-agents
Context separation mechanism: separate-agents
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: reference Markdown rendering; placeholder normalization; fail-closed parsing
Risk-tier classifier: deterministic-changed-surface-check
Governing artifacts: specs/progressive-boundary-first-skill-guidance.md; specs/progressive-boundary-first-skill-guidance.test.md; docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: governing artifacts plus commit:8312f2c1.diff@8312f2c1#sha256:9b39a7f5687cecbe7d932457395bfb0676855b0770efd7220e05b4d236e3ace6
Prompt template version: code-review-v1
Initial packet hash: sha256:9b39a7f5687cecbe7d932457395bfb0676855b0770efd7220e05b4d236e3ace6
Manifest owner: workflow-orchestrator
Affected behavior: cross-adapter workflow invocation portability
Highest-impact failure modes: reference links hide labels or placeholder normalization changes input semantics
Changed boundaries: reference Markdown; custom HTML tags; literal and encoded private-use text
Evidence expected: conservative reference normalization and collision-free parser-local placeholders
Areas requiring direct inspection: portability parser and mutation matrix
Areas intentionally out of scope: final holistic review, final verification, and PR
Risk classes considered: portability; normalization; fail-closed input
Falsifiable review questions: Can a reference-style link hide an adapter label; can placeholder normalization convert noncanonical input into an approved contract
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Material findings: CR-M4-R9-001, CR-M4-R9-002
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Findings

### CR-M4-R9-001 — Reference-style Markdown hides rendered adapter labels

Finding ID: CR-M4-R9-001
Severity: blocker
Location: `scripts/adapter_distribution.py`; `scripts/test-adapter-distribution.py`
Evidence: Full, collapsed, and shortcut reference links render Codex, Claude, or OpenCode labels while retaining bracket syntax in the normalized source.
Required outcome: Residual-label closure conservatively normalizes every reference-link label form.
Safe resolution path: Remove reference-link bracket syntax after inline-link normalization and add all three reference forms across the supported adapter labels.
needs-decision rationale: none
Auto-fix class: declared-safe

### CR-M4-R9-002 — In-band placeholder normalization changes invocation semantics

Finding ID: CR-M4-R9-002
Severity: blocker
Location: `scripts/adapter_distribution.py`; `scripts/test-adapter-distribution.py`
Evidence: Literal or entity-decoded private-use sentinels become approved placeholders, while genuine `argument` or `target-stage` custom HTML tags are protected globally and can hide a rendered OpenCode label.
Required outcome: Only actual approved placeholder source in the exact contract records may satisfy equivalence, without caller-controlled sentinel state.
Safe resolution path: Remove in-band sentinels and preserve placeholder start tags only in parser instances used for exact equivalence and command-record comparison.
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
Compressed requirement risk: present in rendered reference and placeholder closure
Requirement-fidelity no-finding rationale: not-applicable because material findings exist

## Result

M4 remains open for reference-link normalization and collision-free, parser-local placeholder handling.
