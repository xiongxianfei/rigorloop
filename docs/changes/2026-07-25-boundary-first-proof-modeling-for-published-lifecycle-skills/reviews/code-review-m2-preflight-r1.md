# Boundary-First Proof Modeling Code Review M2 Preflight R1

Review ID: code-review-m2-preflight-r1
Stage: code-review
Round: M2 preflight R1
Reviewer: Codex code-review skill with context-separated independent reviewer
Target: initial M2 preflight working-tree candidate
Reviewed artifact: scripts/boundary_proof_behavior.py; scripts/test-boundary-proof.py
Reviewed milestone: M2 environment-feasibility preflight
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-26
Recording status: recorded
Material findings: BFP-M2-CR1, BFP-M2-CR2
Immediate next stage: review-resolution M2 preflight
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: boundary-first-m2-preflight-author
Reviewer context ID: boundary-first-m2-preflight-r1-independent-reviewer
Context separation mechanism: separate-agent
Author context excluded: true
Risk tier: critical
Risk-tier triggers: child-runtime trust boundary, sandbox attestation, executable identity, and authentication isolation
Risk-tier classifier: security-and-external-runtime-boundary
Governing artifacts: specs/rigorloop-workflow.md; specs/rigorloop-workflow.test.md; docs/architecture/system/architecture.md; docs/adr/ADR-20260725-boundary-first-proof-modeling.md; docs/plans/2026-07-25-boundary-first-proof-modeling.md
Formal criteria: R28y; T49; M2 preflight promotion gate
Initial packet inventory: specs/rigorloop-workflow.md@450bb65f#sha256:cce7047761aaa99d81263cf226261e73de3de35e9064e93732274d3a3a8ae1f8; specs/rigorloop-workflow.test.md@450bb65f#sha256:94fdf3da61d35647596d550eaa0527d130daf49ca3af2cf7ff933e330f860f91; docs/architecture/system/architecture.md@450bb65f#sha256:a766457e13872dcb01af9587fd3e23d1a7cd3cf7162a27457a70e076a9e6e9f0; docs/plans/2026-07-25-boundary-first-proof-modeling.md@450bb65f#sha256:70c1bdbbe5714a2477526cdd4b7b7f645fc580782a115a92a1c36aa6dddde9b1
Prompt template version: review-gate/v1
Initial packet hash: sha256:52f05d9b8c6c722566163fb7c85ed3be0c8587f3b3eb00962891651384b629b8
Manifest owner: workflow orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded
Clean-review sufficiency receipt: no

Affected behavior: parent-observed hermetic runtime feasibility and fail-closed environment routing.
Highest-impact failure modes: CLI documentation is mistaken for active confinement; a replaced executable is accepted under the wrong identity.
Changed boundaries: runtime discovery to effective enforcement; executable path to executed byte identity.
Evidence expected: active-state attestation or safe refusal; unreadable, removed, and replaced executable contrasts.
Areas requiring direct inspection: scripts/boundary_proof_behavior.py and focused environment tests.
Areas intentionally out of scope: full harness, lifecycle skill mutation, baseline, immutable run publication, M3-M4, and verification.
Risk classes considered: filesystem confinement, network denial, connector/subagent closure, authentication isolation, runtime metadata, TOCTOU identity, and secret-free evidence.
Falsifiable review questions: can advertised flags pass without enforcement; can runtime bytes change between execution and hashing; can identity failure escape as a traceback?

## Findings

### BFP-M2-CR1: CLI help text is treated as effective enforcement

Finding ID: BFP-M2-CR1
- Severity: blocker
- Status: open
- Location: `scripts/boundary_proof_behavior.py`; `scripts/test-boundary-proof.py`
- Evidence: The candidate marked controls passing when option names occurred in `codex exec --help`; the synthetic advertising-help fixture passed without any effective state.
- Required outcome: Accept only authoritative parent-observed machine-readable effective state; otherwise return `environment-unavailable`.
- Safe resolution path: Remove the help-based positive path, fail closed until an approved authoritative interface exists, and add an advertised-but-unattested regression.
- auto_fix_class: declared-safe
- deterministic_recipe: treat CLI flags only as discovery; require effective-state attestation for pass; otherwise emit the stable unavailable diagnostic
- named_inputs: resolved runtime, version output, CLI capability surface, approved R28y trust boundary
- named_outputs: bounded environment receipt and negative regression
- allowed_paths: `scripts/boundary_proof_behavior.py`; `scripts/test-boundary-proof.py`
- forbidden_paths: skills; specs; architecture; baseline; canonical behavior evidence
- acceptance_criteria: advertised controls cannot pass without effective state and the live unsupported runtime exits 2 without skill mutation
- required_validation: `python scripts/test-boundary-proof.py`; live `check-environment --json`; Python compilation
- needs-decision rationale: none

The candidate marked controls passing when option names occurred in
`codex exec --help`. That does not prove effective roots, network denial,
connector/subagent absence, private authentication, or runtime/model metadata.

Required outcome: accept only authoritative parent-observed machine-readable
effective state; otherwise return `environment-unavailable`. An advertised
but unattested profile must fail.

### BFP-M2-CR2: executable identity is not bound across probes

Finding ID: BFP-M2-CR2
- Severity: major
- Status: open
- Location: `scripts/boundary_proof_behavior.py`; `scripts/test-boundary-proof.py`
- Evidence: The candidate executed the runtime before hashing its path and allowed identity-read errors to escape.
- Required outcome: Bind stable executable filesystem metadata and raw-byte identity before and after every probe and fail safely on identity error.
- Safe resolution path: Capture and compare device, inode, size, timestamps, and SHA-256 around probes; add unreadable, removed, and replaced contrasts.
- auto_fix_class: declared-safe
- deterministic_recipe: fingerprint before version, after version, and after profile probe; reject any missing or changed fingerprint
- named_inputs: resolved executable path and raw executable bytes
- named_outputs: stable runtime identity or bounded unavailable diagnostic
- allowed_paths: `scripts/boundary_proof_behavior.py`; `scripts/test-boundary-proof.py`
- forbidden_paths: skills; specs; architecture; baseline; canonical behavior evidence
- acceptance_criteria: read, removal, or replacement cannot traceback or bind stale identity
- required_validation: `python scripts/test-boundary-proof.py`; Python compilation
- needs-decision rationale: none

The candidate executed the runtime before hashing its path and did not handle
identity-read failure. Replacement could bind evidence to bytes other than
those probed.

Required outcome: bind stable executable filesystem metadata and raw-byte
identity before and after each probe, fail safely on read/remove/replace, and
add direct regressions.

## Result

Review status: changes-requested
Next stage: review-resolution M2 preflight
