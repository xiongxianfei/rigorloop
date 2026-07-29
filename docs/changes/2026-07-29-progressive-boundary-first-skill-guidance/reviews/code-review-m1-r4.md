# M1 Code Review R4

Review ID: code-review-m1-r4
Stage: code-review
Round: 4
Reviewer: two independent L2 Codex reviewers
Target: 9d16bbe2..0e5e4877
Reviewed artifact: commit 0e5e4877
Reviewed milestone: M1
Review date: 2026-07-29
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m1-r3-resolution
Reviewer context ID: m1-r4-primary-and-second-fresh-agents
Context separation mechanism: fresh-separate-agents-blind-first
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: validator behavior; generated-output machinery; compatibility identity; multi-component change
Risk-tier classifier: deterministic-changed-surface-check
Governing artifacts: specs/progressive-boundary-first-skill-guidance.md@0e5e4877#sha256:983a6cab29dd12ff18866f06a2a818ab9c198dd3a3ccddccc06c8e95516d2dd2; specs/progressive-boundary-first-skill-guidance.test.md@0e5e4877#sha256:30595f49cb782e772588334dc9b6c31c728f5b6567892784d6fa27488e3f5257; docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md@0e5e4877#sha256:7aa4b69d2636eb0ff6bf6fb77bcf6835ad2dd5c889feaa8b786e1badce65d5c1; docs/adr/ADR-20260729-progressive-boundary-guidance-resources.md@0e5e4877#sha256:ad78a2f644679a6b0dbaaa6000c1c9b0a8751f9abeb238fcb74cee04e16181c9
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: specs/progressive-boundary-first-skill-guidance.md@0e5e4877#sha256:983a6cab29dd12ff18866f06a2a818ab9c198dd3a3ccddccc06c8e95516d2dd2; specs/progressive-boundary-first-skill-guidance.test.md@0e5e4877#sha256:30595f49cb782e772588334dc9b6c31c728f5b6567892784d6fa27488e3f5257; docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md@0e5e4877#sha256:7aa4b69d2636eb0ff6bf6fb77bcf6835ad2dd5c889feaa8b786e1badce65d5c1; docs/adr/ADR-20260729-progressive-boundary-guidance-resources.md@0e5e4877#sha256:ad78a2f644679a6b0dbaaa6000c1c9b0a8751f9abeb238fcb74cee04e16181c9; commit:0e5e4877.diff@0e5e4877#sha256:82e29bb4f72220b5ed2de95e46fac75cbb8a3167a4e4a6c47509cd823efb817c
Prompt template version: code-review-v1
Initial packet hash: sha256:377aab5f96556ba1292efcc5273dc1290ae0861e4a2805b1fcfb70e5977d9215
Manifest owner: workflow-orchestrator
Affected behavior: manifest authority; projection recovery; activation, CLI, and skill-validation diagnostics
Highest-impact failure modes: malformed-manifest traceback and untrusted scalar disclosure
Changed boundaries: validation error propagation; diagnostic privacy; identity authority
Evidence expected: malformed/missing manifest public-path probes and secret-bearing scalar probes
Areas requiring direct inspection: diagnostic construction, projection formatter, activation translation, skill-validation exception boundary
Areas intentionally out of scope: M2, M3, M4, PR, CI, and final verification
Risk classes considered: diagnostics; privacy; recovery; identity authority; compatibility
Falsifiable review questions: Can malformed input cause a traceback; can untrusted scalar content appear in a public diagnostic
Material findings: CR-M1-R4-001, CR-M1-R4-002
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Findings

### CR-M1-R4-001 — Skill validation leaks malformed-manifest exceptions

Finding ID: CR-M1-R4-001
Severity: blocker
Location: `scripts/skill_validation.py`, `scripts/validate-skills.py`
Evidence: Manifest-backed resource allowlisting lets `ProjectionContractError` escape. An isolated invalid-schema CLI probe emitted a traceback with an absolute temporary path.
Required outcome: Missing or malformed manifests through skill validation return structured repository-relative errors without traceback or private paths.
Safe resolution path: Translate the projection contract exception at the skill-validation boundary and add public CLI regressions.
needs-decision rationale: none
Auto-fix class: declared-safe

### CR-M1-R4-002 — Manifest diagnostics expose untrusted scalar values

Finding ID: CR-M1-R4-002
Severity: blocker
Location: `scripts/boundary_first_reference.py`, `scripts/boundary_first_validation.py`
Evidence: Unknown consumers are interpolated into the message, and path-only redaction allows a secret-like value to appear through projection and activation diagnostics.
Required outcome: Preserve stable identity, path, expectation, and reason without reproducing untrusted manifest payloads.
Safe resolution path: Keep untrusted values out of messages, render offending values through one consistently redacted representation, and add CLI and activation regressions.
needs-decision rationale: none
Auto-fix class: declared-safe

## Prior-finding reconciliation

All R1 through R3 findings are resolved. The raw manifest digest is an independent invariant rather than a parallel projection matrix; catchable interruption recovery, exact resource inventory, and missing-resource diagnostics passed direct probes.

## Requirement-fidelity receipt

Applicability: applicable
Relevant spec clauses decomposed: yes
Property matrix complete: yes
Multi-surface contracts identified: yes
Validator assertions checked against spec: yes
Compressed requirement risk: present for PBS-R037 privacy and the skill-validation sibling path
No-finding rationale: not-applicable because material findings exist

## Independent-review receipts

Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded
Independence level: L2
Second review: satisfied; both reviewers requested changes
Confidence: high
Unreviewed surfaces: M2 automatic guidance; M3 selector routing; M4 package readiness; final verification

No clean-review sufficiency receipt is issued because the review is not clean.
