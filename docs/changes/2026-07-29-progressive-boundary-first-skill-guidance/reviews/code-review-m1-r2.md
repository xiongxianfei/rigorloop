# M1 Code Review R2

Review ID: code-review-m1-r2
Stage: code-review
Round: 2
Reviewer: two independent L2 Codex reviewers
Target: 9d16bbe2..3e740c76
Reviewed artifact: commit 3e740c76
Reviewed milestone: M1
Review date: 2026-07-29
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m1-resolution
Reviewer context ID: m1-r2-primary-and-second-fresh-agents
Context separation mechanism: fresh-separate-agents-blind-first
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: validator behavior; generated-output machinery; compatibility identity; multi-component change
Risk-tier classifier: deterministic-changed-surface-check
Governing artifacts: specs/progressive-boundary-first-skill-guidance.md@3e740c76#sha256:983a6cab29dd12ff18866f06a2a818ab9c198dd3a3ccddccc06c8e95516d2dd2; specs/progressive-boundary-first-skill-guidance.test.md@3e740c76#sha256:30595f49cb782e772588334dc9b6c31c728f5b6567892784d6fa27488e3f5257; docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md@3e740c76#sha256:7aa4b69d2636eb0ff6bf6fb77bcf6835ad2dd5c889feaa8b786e1badce65d5c1; docs/adr/ADR-20260729-progressive-boundary-guidance-resources.md@3e740c76#sha256:ad78a2f644679a6b0dbaaa6000c1c9b0a8751f9abeb238fcb74cee04e16181c9
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: specs/progressive-boundary-first-skill-guidance.md@3e740c76#sha256:983a6cab29dd12ff18866f06a2a818ab9c198dd3a3ccddccc06c8e95516d2dd2; specs/progressive-boundary-first-skill-guidance.test.md@3e740c76#sha256:30595f49cb782e772588334dc9b6c31c728f5b6567892784d6fa27488e3f5257; docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md@3e740c76#sha256:7aa4b69d2636eb0ff6bf6fb77bcf6835ad2dd5c889feaa8b786e1badce65d5c1; docs/adr/ADR-20260729-progressive-boundary-guidance-resources.md@3e740c76#sha256:ad78a2f644679a6b0dbaaa6000c1c9b0a8751f9abeb238fcb74cee04e16181c9; commit:3e740c76.diff@3e740c76#sha256:bddfddf8ca791fec836439663d731236cf5539da8a28b2851c0a5eea3efb5228
Prompt template version: code-review-v1
Initial packet hash: sha256:77daed1de323c907cf954a0e8be8884fcccc061d54f87b0c92ffe86ec25e9411
Manifest owner: workflow-orchestrator
Affected behavior: manifest authority; resource split; 14-target projection; stage maps; activation identity; recovery and diagnostics
Highest-impact failure modes: additional mixed-version resource accepted; structured failure identity lost; partial mutation; competing authority; false digest closure
Changed boundaries: identity authority; composition; temporal retry; recovery; compatibility; filesystem environment
Evidence expected: T1, T2, T5 negative matrices; semantic accounting; exact maps; independent digests; activation and CLI diagnostics
Areas requiring direct inspection: parser; unexpected inventory; write restoration; digest; activation; CLI; skill validation; canonical split; tests
Areas intentionally out of scope: M2, M3, M4, PR, CI, and final verification
Risk classes considered: identity authority; composition; temporal retry; recovery; compatibility; filesystem containment; fidelity; diagnostics
Falsifiable review questions: Can alternate versions pass; can any failure lose its resource path; can a handled interruption leave partial state; is the 14-record identity complete
Material findings: CR-M1-R2-001, CR-M1-R2-002
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, invocation manifest, review log, and review resolution
- Open blockers: two R2 findings plus failed remediation of CR-M1-R1-004
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: CR-M1-R2-001, CR-M1-R2-002
- Recording status: recorded
- Recording blocker: none
- Review record: reviews/code-review-m1-r2.md
- Review log: review-log.md
- Review resolution: review-resolution.md
- Reviewed milestone: M1
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3, M4
- Required review-resolution: yes
- Finding IDs: CR-M1-R2-001, CR-M1-R2-002
- Verify readiness: not-claimed

## Findings

### CR-M1-R2-001 — Alternate-version resources escape inventory validation

Finding ID: CR-M1-R2-001
Severity: blocker
Location: `scripts/boundary_first_reference.py`
Evidence: Unexpected-projection discovery scans only `boundary-first-*-v1.md`. Adding a `boundary-first-method-v2.md` or `boundary-first-proof-v2.md` under a governed skill leaves projection and activation validation successful.
Required outcome: Reject every additional or alternate-version boundary resource at canonical and governed skill-local layers.
Safe resolution path: Inventory the complete `boundary-first-*.md` namespace recursively at canonical and governed reference roots, compare it with the manifest-derived exact set, and add canonical, skill-local, nested, and activation regressions.
needs-decision rationale: none
Auto-fix class: declared-safe

### CR-M1-R2-002 — Structured diagnostics remain incomplete on sibling paths

Finding ID: CR-M1-R2-002
Severity: blocker
Location: `scripts/project-boundary-first-reference.py`, `scripts/boundary_first_reference.py`, `scripts/boundary_first_validation.py`
Evidence: The projection CLI prints only `str(error)`, omitting path, offending value, and expected value. Missing feature/proof sources still use an unstructured error, causing activation validation to substitute the compact-core path.
Required outcome: Every direct CLI and activation projection failure identifies its stable check, actual repository-relative resource, expected condition, privacy-bounded offending value, and reason.
Safe resolution path: Structure missing-source and path errors, add one bounded formatter used by the CLI, remove the compact fallback for non-core errors, and add subprocess and activation sibling-path tests.
needs-decision rationale: none
Auto-fix class: declared-safe

## Prior-finding reconciliation

| Finding | Result | Basis |
| --- | --- | --- |
| CR-M1-R1-001 | resolved | Exact tuple and canonical version mutations now fail. |
| CR-M1-R1-002 | resolved | Compact scan exists in the core and all ten projections. |
| CR-M1-R1-003 | resolved | Early, middle, and final handled write failures restore prior bytes and retry succeeds. |
| CR-M1-R1-004 | failed-remediation | Manifest errors are structured, but missing family sources remain attributed to compact core. |

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | PBS-R015, PBS-R033, and PBS-R037 remain unsatisfied. |
| Test coverage | block | Alternate-version inventory and sibling diagnostics lack proof. |
| Edge cases | block | Mixed-version additional resource passes. |
| Error handling | block | CLI and missing-family-source diagnostics lose fields. |
| Architecture boundaries | pass | Expected resource ownership and pending activation remain aligned. |
| Compatibility | block | An alternate version can coexist undetected. |
| Security/privacy | pass | Existing containment and redaction remain effective. |
| Derived artifact currency | block | Additional versioned resources are accepted. |
| Unrelated changes | pass | The target remains M1-scoped. |
| Validation evidence | concern | All commands pass, but direct probes falsify sufficiency. |

## Requirement-fidelity receipt

Applicability: applicable
Relevant spec clauses decomposed: yes
Property matrix complete: yes
Multi-surface contracts identified: yes
Validator assertions checked against spec: yes
Compressed requirement risk: present for mixed-version inventory and diagnostics
No-finding rationale: not-applicable because material findings exist

## Independent-review receipts

Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded
Independence level: L2
Second review: satisfied; both reviewers requested changes
Confidence: high

No clean-review sufficiency receipt is issued because the review is not clean.
