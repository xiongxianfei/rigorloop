# M4 Code Review R4

Review ID: code-review-m4-r4
Stage: code-review
Round: 4
Reviewer: two independent L2 Codex reviewers
Target: 0afe743e..9a0bfb59
Reviewed artifact: commit 9a0bfb59
Reviewed milestone: M4
Review date: 2026-07-29
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m4-r3-resolution
Reviewer context ID: m4-r4-primary-and-second-independent-agents
Context separation mechanism: separate-agents
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: invocation closure; validation order; fail-closed input
Risk-tier classifier: deterministic-changed-surface-check
Governing artifacts: specs/progressive-boundary-first-skill-guidance.md; specs/progressive-boundary-first-skill-guidance.test.md; docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: governing artifacts plus commit:9a0bfb59.diff@9a0bfb59#sha256:c3417e7d4fe71490a55286c4a22fdfe004198f63497fb52e7169e391cb585c6e
Prompt template version: code-review-v1
Initial packet hash: sha256:c3417e7d4fe71490a55286c4a22fdfe004198f63497fb52e7169e391cb585c6e
Manifest owner: workflow-orchestrator
Affected behavior: additive invocation forms and explicit-name preflight
Highest-impact failure modes: contradictory portable commands or masked unknown selections
Changed boundaries: skill text; portability parser; CLI ordering; archive preflight
Evidence expected: closed invocation records and name validation before archive checks
Areas requiring direct inspection: invocation parser; selection helper; validate-adapters CLI
Areas intentionally out of scope: final holistic review, final verification, and PR
Risk classes considered: portability; closed vocabulary; validation order
Falsifiable review questions: Can an additional contradictory invocation survive; can missing archives mask an unknown selected skill
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Material findings: CR-M4-R4-001; CR-M4-R4-002
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Findings

### CR-M4-R4-001 — Invocation closure ignores additive contradictory forms

Finding ID: CR-M4-R4-001
Severity: blocker
Location: `scripts/adapter_distribution.py`; `scripts/test-adapter-distribution.py`
Evidence: Valid equivalence prose plus bare, non-auto, case-variant, wrong-argument, or conflicting Claude/OpenCode forms remains portable.
Required outcome: Parse every recognized adapter invocation occurrence and reject any identity, operation, argument, or case outside the approved forms.
Safe resolution path: Extract bounded code-span invocation records for all three adapters and add additive mutations for bare, non-auto, case, identity, and argument failures.
needs-decision rationale: none
Auto-fix class: declared-safe

### CR-M4-R4-002 — Archive failures mask invalid explicit skill names

Finding ID: CR-M4-R4-002
Severity: major
Location: `scripts/validate-adapters.py`; `scripts/adapter_distribution.py`; `scripts/test-adapter-distribution.py`
Evidence: An empty archive root plus `--skill does-not-exist` reports only missing archives because the CLI never reaches clean-install selection validation.
Required outcome: Validate explicit skill names before archive validation, regardless of archive state.
Safe resolution path: Expose one selection-preflight helper, call it from the CLI first, and cover invalid-selection plus invalid-archive composition.
needs-decision rationale: none
Auto-fix class: declared-safe

## Requirement-fidelity receipt

Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: scripts/adapter_distribution.py; scripts/validate-adapters.py; scripts/test-adapter-distribution.py; skills/workflow/SKILL.md
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
Compressed requirement risk: present in additive closure and validation ordering
Requirement-fidelity no-finding rationale: not-applicable because material findings exist

## Result

M4 remains open for complete invocation parsing and CLI selection preflight.
