# M4 Code Review R1

Review ID: code-review-m4-r1
Stage: code-review
Round: 1
Reviewer: two independent L2 Codex reviewers
Target: 19d49e1e..72259213
Reviewed artifact: commit 72259213
Reviewed milestone: M4
Review date: 2026-07-29
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m4-implementation
Reviewer context ID: m4-r1-primary-and-second-independent-agents
Context separation mechanism: separate-agents
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: package parity; fail-closed validation; measurement evidence
Risk-tier classifier: deterministic-changed-surface-check
Governing artifacts: specs/progressive-boundary-first-skill-guidance.md; specs/progressive-boundary-first-skill-guidance.test.md; docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: governing artifacts plus commit:72259213.diff@72259213#sha256:f5ed5e4a91c2395b23cc90518259a154cb9dbad217e396d68bb7692cbcb7c1a8
Prompt template version: code-review-v1
Initial packet hash: sha256:f5ed5e4a91c2395b23cc90518259a154cb9dbad217e396d68bb7692cbcb7c1a8
Manifest owner: workflow-orchestrator
Affected behavior: clean-install resource parity, loading-profile validation, and package-readiness evidence
Highest-impact failure modes: accepting unowned installed resources, malformed schema versions, or overstated candidate proof
Changed boundaries: canonical resources; generated output; archives; clean installs; measurement fixtures; lifecycle evidence
Evidence expected: exact inventory rejection, closed-schema mutations, and reproducible before-and-after identities
Areas requiring direct inspection: clean-install validator; loading-profile parser; M4 evidence
Areas intentionally out of scope: final holistic review, final verification, and PR
Risk classes considered: package parity; closed vocabulary; evidence integrity
Falsifiable review questions: Can an unowned resource survive; can a non-integer equal version 1; does evidence identify baseline and candidate
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Material findings: CR-M4-R1-001; CR-M4-R1-002; CR-M4-R1-003
Immediate next stage: review-resolution
Milestone closeout: open
Required review-resolution: yes
Verify readiness: blocked
Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable

## Findings

### CR-M4-R1-001 - Clean-install validation accepts unowned boundary resources

Finding ID: CR-M4-R1-001
Severity: blocker
Location: `scripts/adapter_distribution.py`; `scripts/test-adapter-distribution.py`
Evidence: The validator proves required mapped resources exist and match but does not reject additional installed `boundary-first-*.md` resources. Exact package ownership therefore is not proven.
Required outcome: Compare each installed skill's governed boundary-resource inventory with the manifest-derived expected inventory for that adapter, while leaving unrelated legitimate assets outside that governed namespace alone.
Safe resolution path: Build the expected resource set from the manifest-derived identities, inventory the governed installed namespace, reject set differences, and add representative adapter and resource-family tests.
needs-decision rationale: none
Auto-fix class: declared-safe

### CR-M4-R1-002 - Loading-profile schema version accepts non-integers

Finding ID: CR-M4-R1-002
Severity: major
Location: `scripts/skill_validation.py`; `scripts/test-skill-validator.py`
Evidence: Python equality lets `true` and `1.0` satisfy `schema_version == 1`.
Required outcome: Require the exact integer type and version, and cover boolean, float, string, null, missing-field, and extra-field mutations.
Safe resolution path: Check `type(value) is int` before equality and expand the existing closed-schema mutation test.
needs-decision rationale: none
Auto-fix class: declared-safe

### CR-M4-R1-003 - Package-readiness evidence does not identify the full baseline and candidate

Finding ID: CR-M4-R1-003
Severity: major
Location: `docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/evidence/m4-package-readiness.md`
Evidence: The evidence labels the compact-core file hash as an aggregate inventory hash, omits the required pre-split byte and loading baseline, identifies only the candidate parent rather than its commit/tree/diff, and reports adapter parity without compact generated/archive/install identity summaries.
Required outcome: Record an accurately labelled pre-split and current baseline, the exact candidate commit/tree/diff, and per-adapter mapped-resource identities for generated, archived, and installed layers.
Safe resolution path: Reconstruct the tracked pre-M1 baseline, label per-resource and aggregate identities precisely, bind the implementation commit/tree/diff, and summarize manifest-keyed parity for each adapter layer.
needs-decision rationale: none
Auto-fix class: declared-safe

## Requirement-fidelity receipt

Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: scripts/adapter_distribution.py; scripts/test-adapter-distribution.py; scripts/skill_validation.py; scripts/test-skill-validator.py; scripts/fixtures/boundary-first/loading-profiles.yaml; docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/evidence/m4-package-readiness.md
Requirement-fidelity matched path triggers: scripts/*validator*
Requirement-fidelity matched category triggers: spec-derived validators
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause > decomposition > implementation diff > validator assertions > validation evidence
Requirement-property decomposition evidence: present
Requirement-fidelity receipt: yes
Relevant spec clauses decomposed: yes
Property matrix complete: no
Multi-surface contracts identified: yes
Validator assertions checked against spec: yes
Compressed requirement risk: present in exact inventory and evidence identity
Requirement-fidelity no-finding rationale: not-applicable because material findings exist

## Result

M4 remains open. The three findings must be resolved and independently
re-reviewed before milestone closeout.
