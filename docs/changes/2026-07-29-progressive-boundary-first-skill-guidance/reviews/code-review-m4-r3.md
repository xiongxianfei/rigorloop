# M4 Code Review R3

Review ID: code-review-m4-r3
Stage: code-review
Round: 3
Reviewer: two independent L2 Codex reviewers
Target: 52fbd3e3..a69944eb
Reviewed artifact: commit a69944eb
Reviewed milestone: M4
Review date: 2026-07-29
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m4-r2-resolution
Reviewer context ID: m4-r3-primary-and-second-independent-agents
Context separation mechanism: separate-agents
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: portability validation; explicit selection; fail-closed input
Risk-tier classifier: deterministic-changed-surface-check
Governing artifacts: specs/progressive-boundary-first-skill-guidance.md; specs/progressive-boundary-first-skill-guidance.test.md; docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: governing artifacts plus commit:a69944eb.diff@a69944eb#sha256:c84c57537eca435631760343f231ad8ef9fb5d056dc398da8164b4082320852b
Prompt template version: code-review-v1
Initial packet hash: sha256:c84c57537eca435631760343f231ad8ef9fb5d056dc398da8164b4082320852b
Manifest owner: workflow-orchestrator
Affected behavior: cross-adapter invocation equivalence and explicit clean-install selection
Highest-impact failure modes: accepting broken equivalents or silently dropping requested names
Changed boundaries: public invocation; portability classification; CLI selection; package completeness claim
Evidence expected: exact equivalent forms and fail-closed selection vocabulary
Areas requiring direct inspection: portability detector; mapped-resource selector; CLI result
Areas intentionally out of scope: final holistic review, final verification, and PR
Risk classes considered: portability; closed vocabulary; package completeness
Falsifiable review questions: Can unrelated prose make a broken invocation portable; can a mixed valid and unknown skill selection pass
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Material findings: CR-M4-R3-001; CR-M4-R3-002
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Findings

### CR-M4-R3-001 — Invocation-equivalence detection is phrase-based

Finding ID: CR-M4-R3-001
Severity: blocker
Location: `scripts/adapter_distribution.py`; `scripts/test-adapter-distribution.py`
Evidence: Broken or unrelated commands remain portable when four prose fragments survive; the detector neither binds the `$skill` identity nor requires exact shared arguments.
Required outcome: Require the exact approved Codex, Claude, and OpenCode workflow forms with identical `auto: <target-stage>` semantics and reject missing, malformed, mismatched, or renamed forms.
Safe resolution path: Parse one bounded equivalence sentence or block and add negative mutations for each form, skill identity, and shared argument.
needs-decision rationale: none
Auto-fix class: declared-safe

### CR-M4-R3-002 — Explicit skill selection ignores mixed unknown names

Finding ID: CR-M4-R3-002
Severity: major
Location: `scripts/adapter_distribution.py`; `scripts/validate-adapters.py`; `scripts/test-adapter-distribution.py`
Evidence: `--skill workflow --skill does-not-exist` exits zero and reports both names as validated because the unknown selection is discarded once one valid mapped skill remains.
Required outcome: Reject every explicit name that does not resolve to exactly one canonical mapped skill before archive or install validation.
Safe resolution path: Compare the requested closed set with resolved mapped-skill identities and add mixed-valid/unknown, duplicate, and alias-boundary tests.
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
Compressed requirement risk: present in invocation and selection closure
Requirement-fidelity no-finding rationale: not-applicable because material findings exist

## Result

The exact three-adapter package identities and historical measurement now
reproduce. M4 remains open for invocation-equivalence and explicit-selection
closure.
